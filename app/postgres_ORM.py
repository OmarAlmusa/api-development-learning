from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
from .config import settings

user = settings.database_user
name = settings.database_name
password = settings.database_password
port = settings.database_port
hostname = settings.database_hostname

postgres_URL = f"postgresql://{user}:{password}@{hostname}:{port}/{name}"

# connect_args = {"check_same_thread": False}
engine = create_engine(postgres_URL)

def create_DB_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
    