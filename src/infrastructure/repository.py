from typing import Generic, Optional, Sequence, Type, TypeVar
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select, insert, update, delete 
from src.domain.interfaces import AbstractRepository
from src.infrastructure.models import RefreshTokenTable, UsersTable



T = TypeVar("T", bound=SQLModel)

class SQLRepository(AbstractRepository[T], Generic[T]):
    
    model: Type[T]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Optional[T]:
        stmt = select(self.model).filter_by(id=id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def list(self, limit: int | None = None, offset: int = 0, **kwargs) -> Sequence[T]:
        stmt = select(self.model).filter_by(**kwargs).offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def create(self, data: dict) -> T:
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    
    async def update(self, id: int, data: dict) -> Optional[T]:
        stmt = update(self.model).filter_by(id=id).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def delete(self, id: int) -> None: 
        stmt = delete(self.model).filter_by(id=id)
        await self.session.execute(stmt)


class UserRepository(SQLRepository[UsersTable]):

    model = UsersTable

    async def get_by_email(self, email: EmailStr) -> Optional[UsersTable]:
        stmt = select(UsersTable).filter_by(email=email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[UsersTable]:
        stmt = select(UsersTable).filter_by(username=username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_refresh_token(self, refresh_token: str) -> Optional[UsersTable]:
        stmt = select(UsersTable).join(RefreshTokenTable).filter_by(token=refresh_token)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def delete(self, id: int) -> None: 
        stmt = update(UsersTable).values(is_active=False).filter_by(id=id)
        await self.session.execute(stmt)

class RefreshTokenRepository(SQLRepository[RefreshTokenTable]):

    model = RefreshTokenTable

    async def delete_by_refresh_token(self, refresh_token):
        stmt = delete(RefreshTokenTable).filter_by(token=refresh_token)
        await self.session.execute(stmt)

    async def delete_by_user_id(self, user_id):
        stmt = delete(RefreshTokenTable).filter_by(user_id=user_id)
        await self.session.execute(stmt)

    async def update_refresh_token(self, old_refresh: str, new_refresh: str, expire: int):
        stmt = update(RefreshTokenTable).values(token=new_refresh, expire=expire).filter_by(token=old_refresh)
        await self.session.execute(stmt)
