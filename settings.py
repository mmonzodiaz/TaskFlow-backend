from pydantic import BaseSettings
from pathlib import Path
from typing import Optional

class Settings(BaseSettings):
    # JWT
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_MINUTES: int = 15
    REFRESH_TOKEN_DAYS: int = 7

    # Cookies
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: str = "lax"
    COOKIE_DOMAIN: Optional[str] = None

    # Seguridad
    MAX_FAILED_LOGINS: int = 5
    LOCKOUT_MINUTES: int = 15
    PASSWORD_MIN_LENGTH: int = 8
    
    #.env
    DATABASE_URL: str
    SECRET_KEY: str
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
