# src/api/dependencies.py
from typing import AsyncGenerator, Annotated
from fastapi import Depends, Security
from src.application import AuthService, UserService
from src.domain.enum import UserAccessLevel
from src.infrastructure.connect import async_session_maker
from src.infrastructure.unit_of_work import UnitOfWork
from src.domain.interfaces.unit_of_work import AbstractUnitOfWork
from src.infrastructure.security import FullSecurityService
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
) -> dict:
    return security.get_current_user(token)


def check_access(requred_level: UserAccessLevel):
    def _check(user_data: dict = Security(get_current_user)):
        if user_data.get('access_level') != requred_level:
            raise ForbidenError
        return user_data
    return _check

def get_user_service(uow: UOWDep):
    return UserService(uow=uow)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
CurrentUserDep = Annotated[dict, Depends(get_current_user)]
AdminAccessDep = Annotated[dict, Depends(check_access(UserAccessLevel.ADMIN))]
EmployeeAccessDep = Annotated[dict, Depends(check_access(UserAccessLevel.EMPLOYEE))]
UserAccessDep = Annotated[dict, Depends(check_access(UserAccessLevel.USER))]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
