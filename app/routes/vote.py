from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel import select
from .. import schemas, oauth2, tables
from ..postgres_ORM import SessionDep

router = APIRouter(
    prefix="/votes",
    tags=['Voting']
)

@router.post('/', status_code = status.HTTP_201_CREATED)
def vote(session: SessionDep, vote: schemas.Vote, current_user: int = Depends(oauth2.get_current_user)):

    db_character = session.exec(select(tables.Characters).where(tables.Characters.id==vote.character_id)).first()

    if not db_character:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No character with id: {vote.character_id}")
    
    db_vote = session.exec(
            select(tables.Votes).where(
                (tables.Votes.character_id==vote.character_id) & (tables.Votes.user_id == current_user.id)
            )
        ).first()

    if vote.vote_dir == 1:
        if db_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user with id {current_user.id} has already voted the character with id {vote.character_id}!")
        
        add_vote = tables.Votes.model_validate(schemas.addVote(character_id=vote.character_id, user_id=current_user.id))
        session.add(add_vote)
        session.commit()
        session.refresh(add_vote)
        return add_vote
            
    else:
        if not db_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You didn't vote for this character")
        session.delete(db_vote)
        session.commit()
        return {'msg': f"User with id {current_user.id} has successfully downvoted the character with id {vote.character_id}"}