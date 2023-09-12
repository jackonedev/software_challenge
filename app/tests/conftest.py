import pytest
from auth.oauth2 import create_access_token
from database import models


from functools import lru_cache
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from utils import config
from database.database import get_db
from database.database import Base

@lru_cache()
def get_settings():
    return config.Settings()

settings = get_settings()

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    "Database instance for testing"
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    "App instance for testing"
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def test_user(client):
    user_data = {"username": "admin", "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": str(test_user["id"])}) #TODO: CHECKOUT type consistency - oauth vs schema


@pytest.fixture
def auth_client(client, token):
    client.headers = {
        **client.headers, 
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture()
def test_posts(test_user, session):
    posts_data = [
        {"field_1":"foo",
         "author": "elon musk",
         "description": "bar",
         "my_numeric_field": 123},
        {"field_1":"apple",
         "author": "steve jobs",
         "description": "music",
         "my_numeric_field": 456},
        {"field_1":"banana",
         "author": "andrew warhol",
         "description": "painting",
         "my_numeric_field": 789}
    ]

    # ## Corroborar rendimiento
    # def create_post_model(post):
    #     return models.Post(**post)
    # post_map = map(create_post_model, posts_data)
    # post_map = list(post_map)
    # ##

    session.add_all([models.Post(**post) for post in posts_data])
    session.commit()

    posts = session.query(models.Post).all()
    return posts