from fastapi import HTTPException, status, Query, APIRouter, Depends
from .. import schemas, utilities, tables, oauth2
from ..postgres_ORM import SessionDep
from typing import Annotated
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.GetUser)
def create_user(user: schemas.CreateUser, session: SessionDep):
    try:

        hashed_password = utilities.hash_password(user.password)
        user.password = hashed_password

        db_user = tables.Users.model_validate(user)

        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    
    except IntegrityError as e:
        session.rollback()
        if "unique constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or Username is already in use!"
            )
        
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail ="An unexpected error occured"
        )
    
@router.get('/', response_model=list[schemas.GetUser])
def get_users(session: SessionDep,
                   offset: int = 0,
                   limit: Annotated[int, Query(le=100)] = 100):
    users = session.exec(select(tables.Users).offset(offset).limit(limit)).all()
    return users

@router.get('/{user_id}', response_model=schemas.GetUser)
def get_single_user(user_id: int, session:SessionDep):
    db_user = session.get(tables.Users, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {user_id} is not found")
    return db_user

@router.patch('/{user_id}', response_model=schemas.GetUser)
def update_user(user_id: int, user: schemas.UpdateUser, session: SessionDep, current_user: int = Depends(oauth2.get_current_user)):
    db_user = session.get(tables.Users, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {user_id} is not found")
    
    if db_user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not allowed to update user with id: {user_id}")
    
    user_data = user.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

