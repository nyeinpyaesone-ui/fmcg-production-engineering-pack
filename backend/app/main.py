"""FMCG ERP application entry point: CORS allow-list plus the liveness endpoint."""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

DEFAULT_CORS_ORIGINS = (
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
)


def cors_origins() -> list[str]:
    """Parse FMCG_CORS_ORIGINS, rejecting wildcard and non-http(s) entries.

    Wildcard is forbidden with allow_credentials=True (browsers reject the
    combination, and origin-echo fallbacks are over-permissive).
    """
    configured = os.environ.get("FMCG_CORS_ORIGINS")
    if configured is None:
        return list(DEFAULT_CORS_ORIGINS)
    origins: list[str] = []
    for raw in configured.split(","):
        origin = raw.strip()
        if not origin:
            continue
        if origin.strip("\"'") == "*":
            raise RuntimeError(
                'FMCG_CORS_ORIGINS contains "*": wildcard is forbidden with '
                "allow_credentials=True; list explicit http(s):// origins."
            )
        if not origin.startswith(("http://", "https://")):
            raise RuntimeError(
                f"FMCG_CORS_ORIGINS has invalid origin {origin!r}; " "expected comma-separated http(s)://host[:port]."
            )
        if origin not in origins:
            origins.append(origin)
    if not origins:
        raise RuntimeError(
            "FMCG_CORS_ORIGINS is set but empty; unset it for dev defaults " "or provide at least one explicit origin."
        )
    return origins


def create_app() -> FastAPI:
    """Build the application so tests can construct it under any environment."""
    application = FastAPI(title="FMCG ERP", version="0.1.0")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins(),
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "Idempotency-Key"],
    )

    @application.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return application


app = create_app()
