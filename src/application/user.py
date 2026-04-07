

import uuid
from src.application.dto.users import UpdateUserRequest, UpdateUserPasswordRequest
from src.domain.interfaces.security import AbstractSecurityService
from src.domain.interfaces.unit_of_work import AbstractUnitOfWork
from src.domain.exceptions import PasswordInvalidError, UserNotFound
from src.domain.models import UserBase
class UserService:

    def __init__(self, security: AbstractSecurityService, uow: AbstractUnitOfWork):
        self.security = security
        self.uow = uow

    async def get_by_id(self, user_id: uuid.UUID):
        user = await self.uow.users.get(user_id)
        if not user:
            raise UserNotFound
        return UserBase.model_validate(user)
    
    async def update_user_by_id(self, user_id: uuid.UUID, data: UpdateUserRequest):
        update_data = data.model_dump(exclude_none=True)
        updated_user = await self.uow.users.update(user_id, update_data)
        if not updated_user:
            raise UserNotFound
        await self.uow.commit()
        return UserBase.model_validate(updated_user)
    
    async def update_password(self, user_id: uuid.UUID, data: UpdateUserPasswordRequest):
        user = await self.uow.users.get(user_id)
        if not user: 
            raise UserNotFound
        if not self.security.verify_password(data.old_password, user.hashed_password):
            raise PasswordInvalidError
        hashed_password = self.security.hash_password(data.new_password)
        await self.uow.users.update(user_id, {'hashed_password': hashed_password})
        return {'status': 'OK'}
        