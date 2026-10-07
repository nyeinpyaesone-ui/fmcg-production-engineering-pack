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
    configured = os.environ.get("FMCG_CORS_ORIGINS")
    if configured is None:
        return list(DEFAULT_CORS_ORIGINS)
    return [origin.strip() for origin in configured.split(",") if origin.strip()]


app = FastAPI(title="FMCG ERP", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
