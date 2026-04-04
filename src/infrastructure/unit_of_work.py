from src.domain.interfaces import AbstractUnitOfWork
from src.infrastructure.repository import UserRepository, RefreshTokenRepository

class UnitOfWork(AbstractUnitOfWork):

    users: UserRepository
    refresh_token: RefreshTokenRepository

    def __init__(self, session_factory):
        self.session_factory = session_factory 

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = UserRepository(self.session)
        self.refresh_token = RefreshTokenRepository(self.session)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def refresh(self, instance): 
        await self.session.refresh(instance)