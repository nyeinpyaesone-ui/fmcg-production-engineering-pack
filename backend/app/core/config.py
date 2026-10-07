"""Application configuration helpers (fail closed on missing settings)."""

import os

DATABASE_URL_ENV_VAR = "FMCG_DATABASE_URL"


def database_url() -> str:
    """Return the configured database URL, or raise instead of guessing one."""
    url = os.environ.get(DATABASE_URL_ENV_VAR)
    if not url:
        raise RuntimeError(f"{DATABASE_URL_ENV_VAR} is not set; refusing to connect without explicit configuration.")
    return url
