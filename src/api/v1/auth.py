from fastapi import APIRouter, Response, Request
from src.application.dto.auth import UserRegisterResponse, UserRegisterRequest, UserLoginResponse, UserLoginRequest
from src.api.dependencies import AuthServiceDep, CurrentUserDep
from src.config import settings
from src.domain.exceptions import InvalidTokenError
router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register', status_code=201)
async def register(response: Response, data: UserRegisterRequest, auth_service: AuthServiceDep) -> UserRegisterResponse:
    res_dto, refresh_token = await auth_service.register(data)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=not settings.DEBUG, samesite="lax")
    return res_dto

@router.post('/login', status_code=200, response_model=UserLoginResponse)
async def login(response: Response, data: UserLoginRequest, auth_service: AuthServiceDep) -> UserLoginResponse:
    access_token, refresh_token = await auth_service.login(data)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=not settings.DEBUG, samesite="lax")
    return access_token

@router.post('/refresh', status_code=201, response_model=UserLoginResponse)
async def refresh(response: Response, request: Request, auth_service: AuthServiceDep) -> UserLoginResponse:
    old_refresh = request.cookies.get('refresh_token')
    if not old_refresh:
        raise InvalidTokenError
    access_token, refresh_token = await auth_service.refresh(old_refresh)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=not settings.DEBUG, samesite="lax")
    return access_token

@router.delete('/exit', status_code=204)
async def exit(response: Response, user_data: CurrentUserDep, auth_service: AuthServiceDep):
    await auth_service.exit(user_data.get('id')) # type: ignore
    response.delete_cookie(key='refresh_token')
    return {'status': 'OK'}
