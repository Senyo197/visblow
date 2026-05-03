from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and .env file.

    All fields can be overridden by setting the corresponding environment
    variable. Environment variables are case-sensitive.

    Attributes:
        ENV: Deployment environment name (e.g., 'development', 'staging', 'production').
        DEBUG: Enables debug mode. Should be False in production.

        APP_NAME: Name of the app.
        API_PREFIX: URL prefix for all API routes.

        SECRET_KEY: Secret key used for cryptographic signing. Must be changed in production.
        JWT_ALGORITHM: Algorithm used to sign JWT tokens.
        ACCESS_TOKEN_EXPIRE_MINUTES: Lifetime of access tokens in minutes.
        REFRESH_TOKEN_EXPIRE_DAYS: Lifetime of refresh tokens in days.

        DATABASE_URL: Async PostgreSQL connection string.

        REDIS_URL: Full Redis connection URL. Overrides host/port/db if set.
        REDIS_HOST: Redis server hostname.
        REDIS_PORT: Redis server port.
        REDIS_DB: Redis logical database index.

        CELERY_BROKER_URL: Message broker URL for Celery task queue.
        CELERY_RESULT_BACKEND: Backend URL for storing Celery task results.

        ESCROW_FEE_PERCENT: Platform fee percentage deducted from escrow transactions.

        ENABLE_DISPUTES: Feature flag to enable the disputes system.
        ENABLE_REVIEWS: Feature flag to enable the reviews system.
    """
    ENV: str = Field(default="development")
    DEBUG: bool = True

    APP_NAME: str = "Visblow"
    API_PREFIX: str = "/api/v1"

    SECRET_KEY: str = "dev-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    DATABASE_URL: str = "postgresql+asyncpg://visblow:visblow@localhost:5432/visblow_db"

    REDIS_URL: str | None = None
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    ESCROW_FEE_PERCENT: float = 5.0

    ENABLE_DISPUTES: bool = True
    ENABLE_REVIEWS: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


@lru_cache
def get_settings():
    return Settings()
