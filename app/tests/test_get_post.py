import pytest


@pytest.mark.parametrize(
    "id", [
        (1),
        (2),
        (3)
    ])
def test_get_post(auth_client, test_posts, id):

    res = auth_client.get(f"/get_data/{id}/")
    print(res.json())

    assert res.status_code == 200
