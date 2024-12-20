from fastapi.testclient import TestClient
import pytest


@pytest.mark.parametrize("character_id", [1, 2, 3])
def test_vote(client: TestClient, login_user, create_characters, character_id):
    json_data = {
        "character_id": character_id,
        "vote_dir": 1
    }

    headers = {
        "Authorization": f"Bearer {login_user}"
    }

    response = client.post("/votes/",
                           json=json_data,
                           headers=headers)
    
    assert response.status_code == 201
    assert response.json()["user_id"] == 1
    assert response.json()["character_id"] == character_id