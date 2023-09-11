from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from main import app
from database.database import Base, engine
from database import models
from schemas import posts


def test_get_post():
    # Crea una instancia del cliente de prueba
    client = TestClient(app)

    # Crea una sesión de base de datos temporal
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # Crea un objeto de prueba de tipo PostCreate
    post = posts.PostCreate(
        field_1="Microsoft",
        author="Bill Gates",
        description="Microsoft Corporation es una empresa multinacional de origen estadounidense, fundada el 4 de abril de 1975 por Bill Gates y Paul Allen. Desarrolla, fabrica, licencia y provee software y servicios informáticos, siendo sus productos más usados el sistema operativo Microsoft Windows y la suite Microsoft Office, los cuales tienen una importante posición entre los ordenadores personales. Con el lanzamiento de Microsoft Windows, Microsoft dominó el mercado de sistemas operativos para ordenadores personales, con la serie Microsoft Windows dominando el mercado de computadoras personales, con una cuota de mercado cercana al 90% desde la década de 1990.​",
        my_numeric_field=123
    )

    # Agrega el objeto de prueba a la base de datos
    db_post = models.Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    # Envía una solicitud GET al endpoint 'get_post'
    response = client.get(f"get_data/{db_post.ID}")
    print(db_post.ID)
    # Verifica que la respuesta tenga un código de estado 200
    assert response.status_code == 200

    # Verifica que la respuesta tenga los mismos campos que el objeto de prueba
    assert response.json()["field_1"] == post.field_1
    assert response.json()["author"] == post.author
    assert response.json()["description"] == post.description
    assert response.json()["my_numeric_field"] == post.my_numeric_field
