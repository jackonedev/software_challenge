import pytest
from .database import client, session


@pytest.fixture()
def test_user(client):
    user_data = {"username": "admin", "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user
