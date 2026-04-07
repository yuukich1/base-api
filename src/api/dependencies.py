# src/api/dependencies.py
from typing import AsyncGenerator, Annotated
from fastapi import Depends, Security
from src.application import AuthService, UserService
from src.domain.enum import UserAccessLevel
from src.infrastructure.connect import async_session_maker
from src.infrastructure.unit_of_work import UnitOfWork
from src.domain.interfaces.unit_of_work import AbstractUnitOfWork
from src.infrastructure.security import FullSecurityService, JWTUserSchema
from src.domain.exceptions import ForbidenError
from src.config import settings, oauth2_scheme



async def get_uow() -> AsyncGenerator[AbstractUnitOfWork, None]:
    async with UnitOfWork(async_session_maker) as uow:
        yield uow

def get_security_service() -> FullSecurityService:
    return FullSecurityService(
        secret_key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )


UOWDep = Annotated[AbstractUnitOfWork, Depends(get_uow)]
SecurityDep = Annotated[FullSecurityService, Depends(get_security_service)]

def get_auth_service(
    security: SecurityDep,
    uow: UOWDep,
) -> AuthService:
    return AuthService(uow=uow, security=security)


def get_current_user(
    security: SecurityDep,
    token: str = Security(oauth2_scheme)
) -> JWTUserSchema:
    return security.get_current_user(token)


def check_access(requred_level: UserAccessLevel):
    def _check(user_data: JWTUserSchema = Security(get_current_user)):
        if user_data.access_level != requred_level:
            raise ForbidenError
        return user_data
    return _check

def get_user_service(security: SecurityDep,uow: UOWDep):
    return UserService(uow=uow, security=security)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
CurrentUserDep = Annotated[JWTUserSchema, Depends(get_current_user)] 

AdminAccessDep = Annotated[JWTUserSchema, Depends(check_access(UserAccessLevel.ADMIN))]
EmployeeAccessDep = Annotated[JWTUserSchema, Depends(check_access(UserAccessLevel.EMPLOYEE))]
UserAccessDep = Annotated[JWTUserSchema, Depends(check_access(UserAccessLevel.USER))]
