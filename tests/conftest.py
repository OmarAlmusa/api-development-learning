from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from app.main import app
from app.postgres_ORM import get_session
from sqlmodel import Session, SQLModel, create_engine
from app.config import settings
import pytest
from app import schemas
from app.oauth2 import verify_access_token

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


user = settings.database_user
name = settings.database_name
password = settings.database_password
port = settings.database_port
hostname = settings.database_hostname

@pytest.fixture(name="session")
def session_fixture():
    postgres_URL = f"postgresql://{user}:{password}@{hostname}:{port}/{name}_test"

    engine = create_engine(postgres_URL)

    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as test_session:
          yield test_session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
            return session
    
    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

test_users = [
    {
        "username": "User 5656",
        "email": "account5656@gmail.com",
        "password": "password5656"
    },
    {
        "username": "User 2323",
        "email": "account2323@gmail.com",
        "password": "password2323"
    },
    {
        "username": "User 0098",
        "email": "account0098@gmail.com",
        "password": "password0098"
    },
]

@pytest.fixture(name="create_users")
def create_users_fixture(client: TestClient):
    for user_data in test_users:
        response = client.post("/users/", json=user_data)
        new_user = schemas.GetUser(**response.json())
        assert response.status_code == 201
        assert new_user.username == user_data["username"]


# The test will be carried on first user only for convenience
@pytest.fixture(name="login_user")
def login_user_fixture(client: TestClient, create_users):
    response = client.post("/login/",
                           data={
                               "username": test_users[0]["email"],
                               "password": test_users[0]["password"]
                           })
    
    login_res = schemas.Token(**response.json())
    res_token = verify_access_token(login_res.access_token, credentials_exception)

    assert response.status_code == 200
    assert res_token.id == 1
    return login_res.access_token


test_characters = [
     {
          "name": "Alex",
          "surname": "Benington",
          "gender": "Male",
          "age": 27,
          "roles": ["Fighter", "Warrior", "Strength"]
     },
     {
          "name": "Lucy",
          "surname": "Kimbers",
          "gender": "Female",
          "age": 24,
          "roles": ["Support", "Healer", "Intelligence"]
     },
     {
          "name": "Vox",
          "gender": "???",
          "age": 9999999,
          "roles": ["Monster", "Chaos", "Strength"]
     }
]

@pytest.fixture(name="create_characters")
def create_characters_fixture(client: TestClient, login_user):
     headers = {
          "Authorization": f"Bearer {login_user}"
     }
     for character_data in test_characters:
          response = client.post("/api/v1/characters/",
                                 json=character_data,
                                 headers=headers)
          new_character = schemas.get_character(**response.json())
          assert response.status_code == 201
          assert new_character.name == character_data["name"]