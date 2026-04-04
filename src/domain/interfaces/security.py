from abc import ABC, abstractmethod
from typing import Any, Dict

class AbstractSecurityService(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str: ...

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool: ...

    @abstractmethod
    def create_token(self, payload: Dict[str, Any], expires_delta: int = 3600) -> str:
        raise NotImplementedError

    @abstractmethod
    def decode_token(self, token: str) -> Dict[str, Any]:
        raise NotImplementedError