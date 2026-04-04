# src/infrastructure/security.py
import time
from typing import Any, Dict
from authlib.jose import JsonWebToken
from authlib.jose.errors import JoseError
from passlib.context import CryptContext
from src.domain.interfaces.security import AbstractSecurityService
from src.domain.exceptions import InvalidTokenError

class FullSecurityService(AbstractSecurityService):


    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        
        self.pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
        
        self.jwt_mechanics = JsonWebToken([algorithm])

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_token(self, payload: Dict[str, Any], expires_delta: int = 3600) -> str:
        header = {"alg": self.algorithm}
        now = int(time.time())

        full_payload = {
            **payload,
            "iat": now,
            "exp": now + expires_delta
        }
        
        token_bytes = self.jwt_mechanics.encode(header, full_payload, self.secret_key)
        return token_bytes.decode("utf-8")

    def decode_token(self, token: str) -> Dict[str, Any]:
        try:
            claims = self.jwt_mechanics.decode(token, self.secret_key)
            return dict(claims)
        except JoseError:
            raise InvalidTokenError()