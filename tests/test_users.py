from fastapi.testclient import TestClient
from app import schemas
import pytest
from .conftest import test_users

def test_create_user(client: TestClient):
    json_data = {
                    "username": "User 5656",
                    "email": "account5656@gmail.com",
                    "password": "password5656"
                }
    
    response = client.post("/users/", json=json_data)

    new_user = schemas.GetUser(**response.json())

    assert response.status_code == 201
    assert new_user.username == json_data["username"]


def test_get_users(client: TestClient, create_users):
    response = client.get("/users/")
    new_users = response.json()
    assert response.status_code == 200
    for i, user_data in enumerate(new_users):
        assert schemas.GetUser(**user_data).username == test_users[i]["username"]


@pytest.mark.parametrize("test_id", [1, 2, 3])
def test_get_single_user(client: TestClient, create_users, test_id):
    response = client.get(f"/users/{test_id}")
    new_user = schemas.GetUser(**response.json())
    assert response.status_code == 200
    assert new_user.id == test_id


# Testing authentication on first user only
def test_update_user(client: TestClient, login_user):

    json_data = {
        "username": "random user 12312",
        "email": "randomaccount12321332213@ranked.net",
        "password": "randomrandomrandom1234234_!",
        "profile_picture": None
    }

    headers = {
        "Authorization": f"Bearer {login_user}"
    }

    response = client.patch("/users/1",
                            json = json_data,
                            headers=headers
                            )
    
    res_user = schemas.GetUser(**response.json())

    assert response.status_code == 200
    assert res_user.username == json_data["username"]