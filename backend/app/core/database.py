from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import DeclarativeBase
from collections.abc import AsyncGenerator
from core.config import get_settings


# Centralized abstraction loads application configuration from environment.
settings = get_settings()


# Class that registers metadata and mapping configuration internally, whcih all ORM models must inherit.
class Base(DeclarativeBase):
    pass


"""
Engine that manages the database connection pool. It also maintains a pool of reusable connections that are checked out and returned by sessions as needed.
Configuration:
    echo: Logs SQL statements when DEBUG=True
    pool_pre_ping: Checks connection health before use, preventing stale connection errors in production.
"""
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)


"""
Async session factory that produces AsyncSession instances.

Configuration:
    bind=engine: Ensures sessions obtain connections from the shared engine pool.
    expire_on_commit=False: Prevents ORM objects from being invalidated after commit.
    autoflush=False: Prevents automatic flushing before queries.
"""
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)


"""
FastAPI dependency that provides a request-scoped AsyncSession, creating a new session for each request and automatically closing it after completion to ensure transactional isolation and proper resource cleanup.
"""
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
