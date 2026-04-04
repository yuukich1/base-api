from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, TypeVar
from pydantic import EmailStr
from sqlmodel import SQLModel

T = TypeVar("T", bound=SQLModel)

class AbstractRepository(ABC, Generic[T]):
    
    @abstractmethod
    async def get(self, id: Any) -> T:
        raise NotImplementedError

    @abstractmethod
    async def list(self, **kwargs) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    async def create(self, data: dict) -> T:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: Any, data: dict) -> T:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: Any) -> None:
        raise NotImplementedError
    

class AbstractUserRepository(AbstractRepository[T]):
    @abstractmethod
    async def get_by_email(self, email: EmailStr) -> Optional[T]: ...
    
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[T]: ...

    @abstractmethod
    async def get_by_refresh_token(self, refresh_tokem: str) -> Optional[T]: ...

class AbstractRefreshTokenRepository(AbstractRepository[T]):
    @abstractmethod
    async def delete_by_refresh_token(self, refresh_token: str): ...

    @abstractmethod
    async def update_refresh_token(self, old_refresh: str, new_refresh: str, expire: int): ...