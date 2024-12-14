from fastapi import HTTPException, status, Query, APIRouter, Depends
from .. import schemas, oauth2, tables
from ..postgres_ORM import SessionDep
from typing import Annotated
from sqlmodel import select
from sqlalchemy.sql import func

router = APIRouter(
    prefix="/api/v1/characters",
    tags=['Characters']
)


@router.get('/', response_model=list[schemas.get_character])
def get_characters(session: SessionDep,
                   offset: int = 0,
                   limit: Annotated[int, Query(le=100)] = 100):
    
    # characters = session.exec(select(tables.Characters).offset(offset).limit(limit)).all()
    query = (
        select(tables.Characters, func.count(tables.Votes.character_id), tables.Users)
        .select_from(tables.Characters)
        .join(tables.Votes, tables.Votes.character_id == tables.Characters.id, isouter=True)
        .join(tables.Users, tables.Characters.user_id == tables.Users.id, isouter=True)
        .group_by(tables.Characters.id, tables.Users.id)
    )
    # print(query)

    db_characters = session.exec(query).all()
    response = [schemas.get_character.model_validate({
        **character.dict(),
        "user": schemas.GetUserForCharacter.model_validate(user.dict()),
        "votes": votes
    }) for character, votes, user in db_characters]
    return response

@router.get('/{character_id}', response_model=schemas.get_character)
def get_single_character(character_id: int, session: SessionDep):
    # character = session.get(tables.Characters, character_id)
    # if not character:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")
    # return character
    query = (
        select(tables.Characters, func.count(tables.Votes.character_id), tables.Users)
        .select_from(tables.Characters)
        .join(tables.Votes, tables.Votes.character_id == tables.Characters.id, isouter=True)
        .join(tables.Users, tables.Characters.user_id == tables.Users.id, isouter=True)
        .where(tables.Characters.id == character_id)
        .group_by(tables.Characters.id, tables.Users.id)
    )

    db_character = session.exec(query).first()
    if not db_character:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")
    character, votes, user = db_character
    
    character_data = schemas.get_character.model_validate({
        **character.dict(),
        "user": schemas.GetUserForCharacter.model_validate(user.dict()) if user else None,
        "votes": votes
    })

    return character_data

@router.post('/', response_model=schemas.get_character)
def create_character(character: schemas.CharacterBase, session: SessionDep, current_user: int = Depends(oauth2.get_current_user)):
    character_data = character.model_dump()
    db_character = tables.Characters(**character_data, user_id = current_user.id)
    session.add(db_character)
    session.commit()
    session.refresh(db_character)
    return db_character

@router.delete('/{character_id}')
def delete_character(character_id: int, session: SessionDep, current_user: int = Depends(oauth2.get_current_user)):

    character = session.get(tables.Characters, character_id)

    if not character:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")
    
    if character.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not able to perform that action on character with id: {character_id}")
    
    
    session.delete(character)
    session.commit()
    return {'msg': f"Character with id of {character_id} was deleted successfully!"}

@router.patch('/{character_id}', response_model=schemas.get_character)
def update_character(character_id: int, character:schemas.update_character, session: SessionDep, current_user: int = Depends(oauth2.get_current_user)):

    character_db = session.get(tables.Characters, character_id)

    if not character_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")
    
    if character_db.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not able to perform that action on character with id: {character_id}")
    
    character_data = character.model_dump(exclude_unset=True)
    character_db.sqlmodel_update(character_data)
    session.add(character_db)
    session.commit()
    session.refresh(character_db)
    return character_db