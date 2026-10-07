"""database_url(): fail-closed configuration (missing, blank, and bad-scheme inputs)."""

import pytest

from app.core.config import DATABASE_URL_ENV_VAR, database_url


def test_missing_url_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(DATABASE_URL_ENV_VAR, raising=False)
    with pytest.raises(RuntimeError, match="not set"):
        database_url()


def test_whitespace_url_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(DATABASE_URL_ENV_VAR, "   ")
    with pytest.raises(RuntimeError, match="not set"):
        database_url()


def test_sync_scheme_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(DATABASE_URL_ENV_VAR, "postgresql://user:pw@db:5432/fmcg")
    with pytest.raises(RuntimeError, match="unsupported scheme"):
        database_url()


def test_allowed_schemes_pass(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(DATABASE_URL_ENV_VAR, "postgresql+asyncpg://u:p@db:5432/fmcg")
    assert database_url() == "postgresql+asyncpg://u:p@db:5432/fmcg"
    monkeypatch.setenv(DATABASE_URL_ENV_VAR, "  sqlite+aiosqlite:///./dev.db  ")
    assert database_url() == "sqlite+aiosqlite:///./dev.db"
