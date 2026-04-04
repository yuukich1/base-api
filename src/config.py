from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field

class Settings(BaseSettings):

    DATABASE_URL: str = 'driver://user:password@host:port/db'
    JWT_SECRET_KEY: str = 'my_secret_key'
    JWT_ALGORITHM: str = 'alghorithm'
    REFRESH_DAYS_EXPIRE: int = 60
    ACCESS_EXPIRE: int = 3600
    DEBUG: bool = False
    DATABASE_ALEMIBIC_URL: str = 'driver://user:password@host:port/db'
    @computed_field
    @property
    def REFRESH_EXPIRE(self) -> int:
        return self.REFRESH_DAYS_EXPIRE * 24 * 60 * 60

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        
    )

settings = Settings()