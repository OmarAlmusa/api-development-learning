from fastapi import APIRouter, HTTPException, status, Depends
from .. import schemas, utilities, oauth2, tables
from ..postgres_ORM import get_session
from sqlmodel import select, Session
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):

    db_user = session.exec(select(tables.Users).where(tables.Users.email == user_credentials.username)).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    if not utilities.verify_password(user_credentials.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    access_token = oauth2.create_access_token({"user_id": db_user.id})
    
    return schemas.Token(access_token=access_token, token_type="bearer")