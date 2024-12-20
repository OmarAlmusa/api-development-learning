from fastapi.testclient import TestClient
from app import schemas
from app.oauth2 import verify_access_token
import pytest
from .conftest import test_users, credentials_exception



@pytest.mark.parametrize("user_id, token_id", [(0, 1), (1, 2), (2, 3)])
def test_login(client: TestClient, create_users, user_id, token_id):
    response = client.post("/login/",
                           data={
                               "username": test_users[user_id]["email"],
                               "password": test_users[user_id]["password"]
                           })
    
    login_res = schemas.Token(**response.json())
    res_token = verify_access_token(login_res.access_token, credentials_exception)

    assert login_res.token_type == "bearer"
    assert response.status_code == 200
    assert res_token.id == token_id



def test_login_non_existent_user(client: TestClient):
    response = client.post("/login/",
                           data={
                               "username": "random_user_33@gmail.com",
                               "password": "passwordrandom33"
                           })
    
    assert response.status_code == 403
    assert response.json() == {
            "detail": "Invalid credentials"
        }

