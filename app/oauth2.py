from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
# from dotenv import load_dotenv
# import os
from . import schemas, tables
from .postgres_ORM import get_session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# load_dotenv(dotenv_path="app/.env")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    
    except InvalidTokenError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception)

    current_user = session.exec(select(tables.Users).where(tables.Users.id == token_data.id)).first()

    return current_user