from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    # Environment
    ENV: str = Field(default="development")
    DEBUG: bool = True

    # App
    APP_NAME: str = "Visblow"
    API_PREFIX: str = "/api/v1"

    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database (PostgreSQL async example)
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/visblow_db"

    # Redis
    REDIS_URL: str | None = None
    REDIS_HOST=localhost
    REDIS_PORT=6379
    REDIS_DB=0

    CELERY_BROKER_URL=redis://localhost:6379/0
    CELERY_RESULT_BACKEND=redis://localhost:6379/0

    # Escrow
    ESCROW_FEE_PERCENT: float = 5.0

    # Feature Flags
    ENABLE_DISPUTES: bool = True
    ENABLE_REVIEWS: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings():
    return Settings()
