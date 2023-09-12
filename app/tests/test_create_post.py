# migration guide: Pydantic V2
# https://docs.pydantic.dev/latest/migration/#changes-to-pydanticbasemodel
import pytest
from schemas import posts
from database import models


@pytest.mark.parametrize(
    "query", [
        ("field_1"),
        ("author"),
        ("description")
    ])
def test_create_post(auth_client, test_user, test_posts, session, query):

    # Crea un objeto de prueba de tipo PostCreate
    post = posts.PostCreate(
        field_1="windows",
        author="bill gates",
        description="full",
        my_numeric_field=123
    )

    # Envía una solicitud POST al endpoint 'create_post'
    response = auth_client.post(f"input/{query}", json=post.model_dump())
    print(response.json())

    # Obtiene el id de la respuesta
    post_id = response.json()["id"]

    # Obtiene el registro de la base de datos
    db_post = session.query(models.Post).filter(
        models.Post.ID == post_id).first()

    # # Transformamos el objeto ORM en un esquema Pydantic
    db_post = posts.Post.model_validate(db_post)
    print(db_post)

    # Verifica que la respuesta tenga un código de estado 201
    assert response.status_code == 201

    # Verificar la implementación de la función mayúsculas
    if query == "field_1":
        assert db_post.field_1 == post.model_dump()["field_1"].upper()
        assert db_post.author == post.model_dump()["author"]
        assert db_post.description == post.model_dump()["description"]
        assert db_post.my_numeric_field == post.model_dump()[
            "my_numeric_field"]
    elif query == "author":
        assert db_post.field_1 == post.model_dump()["field_1"]
        assert db_post.author == post.model_dump()["author"].upper()
        assert db_post.description == post.model_dump()["description"]
        assert db_post.my_numeric_field == post.model_dump()[
            "my_numeric_field"]
    elif query == "description":
        assert db_post.field_1 == post.model_dump()["field_1"]
        assert db_post.author == post.model_dump()["author"]
        assert db_post.description == post.model_dump()["description"].upper()
        assert db_post.my_numeric_field == post.model_dump()[
            "my_numeric_field"]
