# src/api/dependencies.py
from typing import AsyncGenerator, Annotated
from fastapi import Depends
from src.application.auth import AuthService
from src.infrastructure.connect import async_session_maker
from src.infrastructure.unit_of_work import UnitOfWork
from src.domain.interfaces.unit_of_work import AbstractUnitOfWork
from src.infrastructure.security import FullSecurityService
from src.config import settings 

async def get_uow() -> AsyncGenerator[AbstractUnitOfWork, None]:
    async with UnitOfWork(async_session_maker) as uow:
        yield uow

def get_security_service() -> FullSecurityService:
    return FullSecurityService(
        secret_key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

def get_auth_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
    security: FullSecurityService = Depends(get_security_service)
) -> AuthService:
    return AuthService(uow=uow, security=security)

UOWDep = Annotated[AbstractUnitOfWork, Depends(get_uow)]
SecurityDep = Annotated[FullSecurityService, Depends(get_security_service)]
AuthDep = Annotated[AuthService, Depends(get_auth_service)]