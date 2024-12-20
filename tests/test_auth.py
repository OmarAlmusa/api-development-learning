from .setting_db import client_fixture, session_fixture, test_users, create_users_fixture, credentials_exception
from fastapi.testclient import TestClient
from app import schemas
from app.oauth2 import verify_access_token
import pytest



@pytest.mark.parametrize("user_id, token_id", [(0, 1), (1, 2), (2, 3)])
def test_login(client: TestClient, create_users, user_id, token_id):
    response = client.post("/login/",
                           data={
                               "username": test_users[user_id]["email"],
                               "password": test_users[user_id]["password"]
                           })
    
    login_res = schemas.Token(**response.json())
    res_token = verify_access_token(login_res.access_token, credentials_exception)

    assert response.status_code == 200
    assert res_token.id == token_id

