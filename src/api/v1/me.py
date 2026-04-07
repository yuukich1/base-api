from fastapi import APIRouter
from src.api.dependencies import CurrentUserDep, UserServiceDep

router = APIRouter(prefix='/me', tags=['me'])

@router.get('')
async def get_me(user_service: UserServiceDep, user_data: CurrentUserDep):
    return await user_service.get_by_id(user_data.get('id')) # type: ignore

