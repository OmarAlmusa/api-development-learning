from .setting_db import client_fixture, session_fixture, test_users, create_users_fixture, login_user_fixture, create_characters_fixture, test_characters
from fastapi.testclient import TestClient
from app import schemas
import pytest

def test_get_characters(client: TestClient, create_characters):
    response = client.get("/api/v1/characters/")
    new_characters = response.json()
    assert response.status_code == 200
    for i, single_character in enumerate(new_characters):
        assert schemas.get_character_with_votes(**single_character).name == test_characters[i]["name"]