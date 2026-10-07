"""Alembic environment: single metadata registry, URL from FMCG_DATABASE_URL (fail closed)."""

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from app.core.config import database_url
from app.db.base import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# The URL is read lazily inside the run functions (never at import), so plain
# inspection commands work without FMCG_DATABASE_URL set. Migration runs still
# fail closed when it is missing or invalid.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (SQL script rendering)."""
    config.set_main_option("sqlalchemy.url", database_url())
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations against the given connection inside a transaction."""
    context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode over an async engine."""
    config.set_main_option("sqlalchemy.url", database_url())
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
