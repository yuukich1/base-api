from typing import List, Optional
from src.domain import UserDomain, RefreshTokenDomain
from sqlmodel import Field, Relationship, SQLModel
import uuid

class UsersTable(UserDomain, table=True):

    __tablename__: str = 'users'

    hashed_password: str 
    is_active: bool = Field(default=True)

    refresh_token: List["RefreshTokenTable"] = Relationship(back_populates='user')


class RefreshTokenTable(RefreshTokenDomain, table=True):

    __tablename__: str = 'refresh_token'

    user_id: uuid.UUID = Field(foreign_key='users.id')

    user: Optional['UsersTable'] = Relationship(back_populates='refresh_token')


