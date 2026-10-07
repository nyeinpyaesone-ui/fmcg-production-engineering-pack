"""Application configuration helpers (fail closed on missing settings)."""

import os

DATABASE_URL_ENV_VAR = "FMCG_DATABASE_URL"
_ALLOWED_SCHEMES = ("postgresql+asyncpg://", "sqlite+aiosqlite://")


def database_url() -> str:
    """Return the configured database URL, or raise instead of guessing one.

    Whitespace-only values and unsupported schemes (e.g. sync drivers passed
    to the async engine) are rejected here with a clear error instead of
    failing late inside SQLAlchemy.
    """
    url = (os.environ.get(DATABASE_URL_ENV_VAR) or "").strip()
    if not url:
        raise RuntimeError(f"{DATABASE_URL_ENV_VAR} is not set; refusing to connect without explicit configuration.")
    scheme = url.split("://", 1)[0]
    if not url.startswith(_ALLOWED_SCHEMES):
        raise RuntimeError(
            f"{DATABASE_URL_ENV_VAR} has unsupported scheme {scheme!r}; "
            f"expected one of {[s.removesuffix('://') for s in _ALLOWED_SCHEMES]}."
        )
    return url
