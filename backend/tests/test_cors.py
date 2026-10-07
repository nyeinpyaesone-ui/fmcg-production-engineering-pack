"""CORS allow-list: defaults, validation, and per-app preflight (no skip branches)."""

import pytest
from fastapi.testclient import TestClient

from app.main import DEFAULT_CORS_ORIGINS, cors_origins, create_app


def test_defaults_cover_dev_and_compose_origins(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FMCG_CORS_ORIGINS", raising=False)
    assert set(cors_origins()) == {
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    }
    assert set(DEFAULT_CORS_ORIGINS) == set(cors_origins())


def test_env_override_parsing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FMCG_CORS_ORIGINS", "https://a.example, https://b.example ,, https://a.example")
    assert cors_origins() == ["https://a.example", "https://b.example"]


def test_wildcard_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FMCG_CORS_ORIGINS", "https://a.example, *")
    with pytest.raises(RuntimeError, match="wildcard"):
        cors_origins()


def test_non_http_origin_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FMCG_CORS_ORIGINS", "notaurl")
    with pytest.raises(RuntimeError, match="invalid origin"):
        cors_origins()


def test_empty_override_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FMCG_CORS_ORIGINS", "  , ")
    with pytest.raises(RuntimeError, match="empty"):
        cors_origins()


def test_preflight_allowed_origin(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FMCG_CORS_ORIGINS", "http://localhost:8080")
    response = TestClient(create_app()).options(
        "/health",
        headers={"Origin": "http://localhost:8080", "Access-Control-Request-Method": "GET"},
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:8080"


def test_preflight_foreign_origin_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FMCG_CORS_ORIGINS", "http://localhost:8080")
    response = TestClient(create_app()).options(
        "/health",
        headers={"Origin": "http://evil.example", "Access-Control-Request-Method": "GET"},
    )
    assert response.status_code == 400
