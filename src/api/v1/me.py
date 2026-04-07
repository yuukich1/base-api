from fastapi import APIRouter
from src.api.dependencies import CurrentUserDep, UserServiceDep
from src.application.dto.users import UpdateUserRequest, UpdateUserPasswordRequest
router = APIRouter(prefix='/me', tags=['me'])

@router.get('')
async def get_me(user_service: UserServiceDep, user_data: CurrentUserDep):
    return await user_service.get_by_id(user_data.id)


@router.patch('')
async def update_me(data: UpdateUserRequest, user_service: UserServiceDep, user_data: CurrentUserDep):
    return await user_service.update_user_by_id(user_data.id, data)


@router.patch('/password')
async def update_password(data: UpdateUserPasswordRequest, user_service: UserServiceDep, user_data: CurrentUserDep):
    return await user_service.update_password(user_data.id, data)