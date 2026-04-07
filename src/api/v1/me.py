from fastapi import APIRouter
from src.api.dependencies import CurrentUserDep, UserServiceDep
from src.application.dto.users import UpdateUserRequest, UpdateUserPasswordRequest
from src.domain.models import UserBase
router = APIRouter(prefix='/me', tags=['me'])

@router.get('', response_model=UserBase)
async def get_me(user_service: UserServiceDep, user_data: CurrentUserDep):
    return await user_service.get_by_id(user_data.id)


@router.patch('', response_model=UserBase)
async def update_me(data: UpdateUserRequest, user_service: UserServiceDep, user_data: CurrentUserDep):
    return await user_service.update_user_by_id(user_data.id, data)


@router.patch('/password', status_code=204)
async def update_password(data: UpdateUserPasswordRequest, user_service: UserServiceDep, user_data: CurrentUserDep):
    return await user_service.update_password(user_data.id, data)