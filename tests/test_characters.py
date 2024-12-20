from fastapi.testclient import TestClient
from app import schemas
import pytest
from .conftest import test_characters



def test_get_characters(client: TestClient, create_characters):
    response = client.get("/api/v1/characters/")
    new_characters = response.json()
    assert response.status_code == 200
    for i, single_character in enumerate(new_characters):
        assert schemas.get_character_with_votes(**single_character).name == test_characters[i]["name"]



@pytest.mark.parametrize("test_id", [1, 2, 3])
def test_get_single_character(client: TestClient, create_characters, test_id):
    response = client.get(f"/api/v1/characters/{test_id}")
    new_character = schemas.get_character_with_votes(**response.json())
    assert response.status_code == 200
    assert new_character.id == test_id


def test_create_character(client: TestClient, login_user):
    json_data = {
                    "name": "Luna",
                    "gender": "Female",
                    "age": 23,
                    "roles": ["Assassin", "Agility"]
                }
    
    headers = {
        "Authorization": f"Bearer {login_user}"
    }
    
    response = client.post("/api/v1/characters/",
                           json=json_data,
                           headers=headers)
    
    new_character = schemas.get_character(**response.json())
    
    assert response.status_code == 201
    assert new_character.name == json_data["name"]
    assert new_character.user.id == 1



@pytest.mark.parametrize("test_id", [1, 2, 3])
def test_delete_character(client: TestClient, login_user, create_characters, test_id):
    headers = {
        "Authorization": f"Bearer {login_user}"
    }
    response = client.delete(f"/api/v1/characters/{test_id}",
                             headers=headers
                             )

    assert response.status_code == 200
    assert response.json() == {
        "msg": f"Character with id of {test_id} was deleted successfully!"
        }
    
@pytest.mark.parametrize("test_id, new_name", [(1, "Kevin"), (2, "Lina"), (3, "Trax")])
def test_update_character(client: TestClient, login_user, create_characters, test_id, new_name):
    
    json_data = {
        "name": f"{new_name}"
    }


    headers = {
        "Authorization": f"Bearer {login_user}"
    }

    response = client.patch(f"/api/v1/characters/{test_id}",
                            json=json_data,
                            headers=headers
                            )

    updated_character = schemas.get_character(**response.json())
    assert response.status_code == 200
    assert updated_character.name == json_data["name"]
