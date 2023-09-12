import pytest
from schemas import posts
from database.models import Post

@pytest.mark.parametrize(
    "id", [
        (1),
        (2),
        (3)
    ])
def test_get_post(auth_client, test_posts, id):

    res = auth_client.get(f"/get_data/{id}/")
    print(res.json())
    post = posts.Post(**res.json())

    assert post.ID == id
    assert post.field_1 == test_posts[id-1].field_1
    assert post.author == test_posts[id-1].author
    assert post.description == test_posts[id-1].description
    assert post.my_numeric_field == test_posts[id-1].my_numeric_field
    assert res.status_code == 200
