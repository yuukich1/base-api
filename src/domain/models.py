from typing import Optional
import uuid

from sqlmodel import SQLModel, Field
from pydantic import ConfigDict, EmailStr


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)
    age: Optional[int] = None

class UserDomain(UserBase):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    access_level: str = Field(default='USER')

    class Config:
        from_attributes = True

class RefreshTokenDomain(SQLModel):

    token: str = Field(index=True, unique=True, primary_key=True)
    expire: int