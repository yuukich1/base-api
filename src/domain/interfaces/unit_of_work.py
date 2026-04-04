from abc import ABC, abstractmethod
from .repository import AbstractRefreshTokenRepository, AbstractUserRepository

class AbstractUnitOfWork(ABC):

    users: AbstractUserRepository
    refresh_token: AbstractRefreshTokenRepository

    async def __aenter__(self) -> "AbstractUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):

        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError
    
    @abstractmethod
    async def refresh(self, instance):
        raise NotImplementedError