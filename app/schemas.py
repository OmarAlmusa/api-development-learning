from datetime import datetime
from typing import List, Optional
from pydantic import EmailStr, BaseModel, conint
from typing import Annotated
from sqlmodel import Field

### USERS:

class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    profile_picture: Optional[str] = None

class GetUser(BaseModel):
    id: int
    username: str
    profile_picture: Optional[str] = None
    characters: List["get_characters_for_single_user"]

class GetUserForCharacter(BaseModel):
    id: int
    username: str
    profile_picture: Optional[str] = None

class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    profile_picture: Optional[str] = None



### CHARACTERS:

class CharacterBase(BaseModel):
    name: str
    surname: Optional[str] = None
    gender: str
    age: int
    roles: List[str]
    image: Optional[str] = None

class get_character(CharacterBase):
    id: int
    createdAt: datetime
    user: Optional["GetUserForCharacter"]

class get_character_with_votes(CharacterBase):
    id: int
    createdAt: datetime
    user: Optional["GetUserForCharacter"]
    votes: int

class get_characters_for_single_user(CharacterBase):
    id: int
    createdAt: datetime

class update_character(CharacterBase):
    name: Optional[str] = None
    surname: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    roles: Optional[List[str]] = None
    image: Optional[str] = None


### LOGIN:

class UserLogin(BaseModel):
    email: EmailStr
    password: str


### TOKEN:

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int]


### VOTING

class Vote(BaseModel):
    character_id: int
    vote_dir: Annotated[int, Field(ge=0, le=1)]


class addVote(BaseModel):
    character_id: int
    user_id: int