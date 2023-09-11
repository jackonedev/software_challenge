from functools import lru_cache
import pytest
from jose import jwt
from .database import client, session

from schemas.users import UserOut, Token
from utils import config

@lru_cache()
def get_settings():
    return config.Settings()

settings = get_settings()


@pytest.fixture()
def test_user(client):
    user_data = {"username": "admin", "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

def test_create_user(client):
    res = client.post("/users/", json={"username": "admin", "password": "password123"})
    print(res.json())
    user = UserOut(**res.json())

    assert res.status_code == 201
    assert user.username == "admin"

def test_login_user(client, test_user):
    res = client.post("/login/", data={"username": test_user["username"], "password": test_user["password"]})
    
    # Token validation
    login_res = Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")

    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
