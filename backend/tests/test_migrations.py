"""Gate 2 migration harness: empty-DB upgrade plus downgrade/re-upgrade (FMCG-006).

Runs Alembic online against an isolated SQLite file through the same async path the
runtime uses. PostgreSQL remains the production target; dialect-specific migrations
must additionally be verified against disposable PostgreSQL before release (Gate 7).
"""

import sqlite3
from pathlib import Path

import pytest

from alembic import command
from alembic.config import Config

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def migrated_db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Config, Path]:
    """Point Alembic at an isolated SQLite file via the required env var."""
    db_file = tmp_path / "migration-test.db"
    monkeypatch.setenv("FMCG_DATABASE_URL", f"sqlite+aiosqlite:///{db_file}")
    cfg = Config()
    cfg.set_main_option("script_location", str(ROOT / "alembic"))
    return cfg, db_file


def _applied_versions(db_file: Path) -> set[str]:
    """Read Alembic's version table with the stdlib driver (no app imports)."""
    if not db_file.exists():
        return set()
    with sqlite3.connect(db_file) as conn:
        tables: set[str] = {str(row[0]) for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if "alembic_version" not in tables:
            return set()
        return {str(row[0]) for row in conn.execute("SELECT version_num FROM alembic_version")}


def test_upgrade_empty_database(migrated_db: tuple[Config, Path]) -> None:
    cfg, db_file = migrated_db
    command.upgrade(cfg, "head")
    assert _applied_versions(db_file) == {"0001"}


def test_downgrade_then_reupgrade(migrated_db: tuple[Config, Path]) -> None:
    cfg, db_file = migrated_db
    command.upgrade(cfg, "head")
    command.downgrade(cfg, "base")
    assert _applied_versions(db_file) == set()
    command.upgrade(cfg, "head")
    assert _applied_versions(db_file) == {"0001"}
