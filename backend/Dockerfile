# syntax=docker/dockerfile:1
# FMCG ERP backend: FastAPI on pinned Python with hash-verified dependencies.
# Base digest recorded in docs/COMPATIBILITY.md; re-pin deliberately, never float.
FROM python:3.11.17-slim@sha256:0dd364ba7e10242f07755449e3a3d0e35f9efd987952737b90def6709ab0c5ce

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PIP_NO_CACHE_DIR=1

WORKDIR /srv/app

# Runtime lockfile first for layer caching; pip verifies every hash.
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir --require-hashes -r requirements.txt

COPY backend/app ./app
COPY backend/alembic.ini ./alembic.ini
COPY backend/alembic ./alembic

RUN useradd --create-home --uid 10001 appuser \
  && chown -R appuser:appuser /srv/app
USER appuser

EXPOSE 8000

# Liveness only: /health probes no dependencies by design (see docs/COMPATIBILITY.md).
# Uses the stdlib client because slim images ship no curl (see docs/SOURCE_ASSESSMENT.md).
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=4)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
