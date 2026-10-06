"""CORS allow-list: defaults cover dev (5173) and compose (8080) origins (FMCG drift fix)."""

import os

import pytest
from fastapi.testclient import TestClient

from app.main import DEFAULT_CORS_ORIGINS, app, cors_origins


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
    monkeypatch.setenv("FMCG_CORS_ORIGINS", "https://a.example, https://b.example ,,")
    assert cors_origins() == ["https://a.example", "https://b.example"]


def test_preflight_allowed_origin() -> None:
    # The app snapshot its middleware at import with default origins; skip if the
    # runner overrides FMCG_CORS_ORIGINS (CI and Makefile never do).
    if "FMCG_CORS_ORIGINS" in os.environ:
        pytest.skip("runner overrides FMCG_CORS_ORIGINS")
    response = TestClient(app).options(
        "/health",
        headers={"Origin": "http://localhost:8080", "Access-Control-Request-Method": "GET"},
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:8080"
