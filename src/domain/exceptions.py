from typing import Optional


class DomainError(Exception):
    status_code: int = 400
    message: str = "Произошла ошибка бизнес-логики"

    def __init__(self, message: Optional[str] = None, status_code: Optional[int] = None):
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code
        super().__init__(self.message)

class UserAlreadyExists(DomainError):
    status_code = 409
    message = "Такой пользователь уже существует"

class UserNotFound(DomainError):
    status_code = 404
    message = "Пользователь не найден"

class InvalidTokenError(DomainError):
    status_code = 401
    message = "Токен недействителен или просрочен"

class InvalidCredentialErorr(DomainError):
    status_code = 400
    message = "Не верный логин или пароль"