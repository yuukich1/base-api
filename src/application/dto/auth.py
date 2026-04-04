from typing import Self
from src.domain.models import UserBase, UserDomain
from pydantic import EmailStr, Field, model_validator, BaseModel


class UserRegisterRequest(UserBase):

    password: str = Field(min_length=8, max_length=22)
    confirm_password: str = Field(min_length=8, max_length=22)

    @model_validator(mode='after')
    def check_password_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError('passwod do not match')
        return self
    
class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    expire: int

class UserRegisterResponse(BaseModel):
    status: str
    user: UserDomain
    auth: AccessTokenResponse

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserLoginResponse(BaseModel):
    status: str
    auth: AccessTokenResponse
    
