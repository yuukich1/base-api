import uuid

from src.domain.exceptions import UserAlreadyExists, InvalidCredentialError, InvalidTokenError
from src.domain.interfaces import AbstractSecurityService, AbstractUnitOfWork
from src.domain.models import UserDomain
from src.application.dto.auth import UserLoginRequest, UserRegisterRequest, UserRegisterResponse, UserLoginResponse, AccessTokenResponse
from src.domain.enum import UserAccessLevel
from src.config import settings
from loguru import logger
class AuthService:

    def __init__(self, security: AbstractSecurityService, uow: AbstractUnitOfWork):
        self.security = security
        self.uow = uow

    async def register(self, data: UserRegisterRequest):
        user_data = data.model_dump(exclude={'confirm_password', 'password'})
        user_data['hashed_password'] = self.security.hash_password(data.password)
        if await self.uow.users.get_by_email(data.email) or await self.uow.users.get_by_username(data.username):
            raise UserAlreadyExists
        user = await self.uow.users.create(user_data)
        await self.uow.commit()
        access_token, refresh_token = self.__create_pair_token(user)
        return UserRegisterResponse(
            status='OK',
            user=UserDomain.model_validate(user),
            auth=AccessTokenResponse(access_token=access_token, expire=settings.ACCESS_EXPIRE)
        ), refresh_token

    async def login(self, data: UserLoginRequest):
        user = await self.uow.users.get_by_email(data.email)
        if not user or not self.security.verify_password(data.password, user.hashed_password):
            raise InvalidCredentialError
        access_token, refresh_token = self.__create_pair_token(user)
        await self.uow.refresh_token.create({
            'token': refresh_token,
            'user_id': user.id,
            'expire': settings.REFRESH_EXPIRE
        })
        await self.uow.commit()
        return UserLoginResponse(
            status='OK',
            auth=AccessTokenResponse(access_token=access_token, expire=settings.ACCESS_EXPIRE)
        ), refresh_token

    def __create_payload(self, data: UserDomain):
        return {
            "id": str(data.id),
            "email": data.email,
            "access_level": data.access_level
        }

    def __create_pair_token(self, user: UserDomain):
        payload = self.__create_payload(user)
        access_token, refresh_token = self.security.create_token(payload=payload, expires_delta=settings.ACCESS_EXPIRE), self.security.create_token(payload=payload, expires_delta=settings.REFRESH_EXPIRE)
        return access_token, refresh_token

    async def refresh(self, old_refresh: str):
        logger.debug(old_refresh)
        user = await self.uow.users.get_by_refresh_token(old_refresh)
        if not user:
            raise InvalidTokenError
        access_token, refresh_token = self.__create_pair_token(user)
        await self.uow.refresh_token.update_refresh_token(old_refresh=old_refresh, new_refresh=refresh_token, expire=settings.REFRESH_EXPIRE)
        await self.uow.commit()
        return UserLoginResponse(
            status='OK',
            auth=AccessTokenResponse(access_token=access_token, expire=settings.ACCESS_EXPIRE)
        ), refresh_token

    async def exit(self, user_id: uuid.UUID):
        await self.uow.refresh_token.delete_by_user_id(user_id)
        return