"""Async engine and session factories. One use case owns one session/transaction."""

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import database_url


def create_engine(url: str | None = None) -> AsyncEngine:
    """Create an async engine for the configured database (asyncpg in production)."""
    return create_async_engine((url or "").strip() or database_url(), pool_pre_ping=True)


def session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Build a session factory bound to the given engine."""
    return async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
