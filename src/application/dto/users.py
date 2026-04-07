from pydantic import BaseModel, EmailStr, Field, model_validator

from src.domain.models import UserBase
from typing import Optional, Self

class UpdateUserRequest(UserBase):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    age: Optional[int] = None


class UpdateUserPasswordRequest(BaseModel):
    old_password: str 
    new_password: str = Field(min_length=8, max_length=22)
    confirm_password: str = Field(min_length=8, max_length=22)

    @model_validator(mode='after')
    def check_password_match(self) -> Self:
        if self.new_password != self.confirm_password:
            raise ValueError('new password do not match')
        return self