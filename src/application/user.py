

import uuid
from src.domain.interfaces.unit_of_work import AbstractUnitOfWork
from src.domain.exceptions import UserNotFound
from src.domain.models import UserBase
class UserService:

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def get_by_id(self, user_id: uuid.UUID):
        user = await self.uow.users.get(user_id)
        if not user:
            raise UserNotFound
        return UserBase.model_validate(user)
    
    async def delete_user(self, user_id: uuid.UUID):
        ...