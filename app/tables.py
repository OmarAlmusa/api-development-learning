from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, timezone
from typing import List, Optional
import json
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Column, String, ForeignKey


class Users(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    email: str = Field(index=True, nullable=False, unique=True)
    password: str = Field(nullable=False)
    username: str = Field(nullable=False, index=True, unique=True)
    profile_picture: str | None = Field(default=None, index=True)
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    characters: List["Characters"] = Relationship(back_populates="user")


class Characters(SQLModel, table=True):

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    surname: str | None = Field(default=None, index=True)
    gender: str = Field(index=True)
    age: int = Field(index=True)
    roles: List[str] = Field(sa_column=Column(ARRAY(String)), default=[])
    image: str | None = Field(default=None, index=True)
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user_id: int = Field(sa_column=Column(ForeignKey('users.id', ondelete="SET NULL"), nullable=True))

    user: Optional["Users"] = Relationship(back_populates="characters")

    @property
    def roles_list(self) -> List[str]:
        """Deserialize JSON string into Python list."""
        return json.loads(self.roles)

    @roles_list.setter
    def roles_list(self, value: List[str]):
        """Serialize Python list into JSON string."""
        self.roles = json.dumps(value)


class Votes(SQLModel, table=True):
    character_id: int = Field(sa_column=Column(ForeignKey('characters.id', ondelete="CASCADE"), primary_key=True))
    user_id: int = Field(sa_column=Column(ForeignKey('users.id', ondelete="CASCADE"), primary_key=True))