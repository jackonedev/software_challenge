from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from main import app
from database.database import Base, engine
from database import models
from schemas import posts


def test_create_post():
    # Crea una instancia del cliente de prueba
    client = TestClient(app)

    # Crea una sesión de base de datos temporal
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # Crea un objeto de prueba de tipo PostCreate
    post = posts.PostCreate(
        field_1="foo",
        author="elon musk",
        description="bar",
        my_numeric_field=123
    )

    # Envía una solicitud POST al endpoint 'create_post'
    response = client.post("input/field_1", json=post.model_dump())

    # Verifica que la respuesta tenga un código de estado 201
    assert response.status_code == 201

    # Verifica que la respuesta tenga un campo 'id'
    assert "id" in response.json()

    # Verifica que el objeto de prueba haya sido agregado a la base de datos
    db_post = db.query(models.Post).filter(models.Post.ID == response.json()["id"]).first()
    assert db_post is not None

    # Verifica que el campo 'field_1' del objeto de prueba haya sido convertido a mayúsculas
    assert db_post.field_1 == post.model_dump()["field_1"].upper()