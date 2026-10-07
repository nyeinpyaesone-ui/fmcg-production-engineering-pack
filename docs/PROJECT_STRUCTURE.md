# Project Structure

The repository layout, what lives where, and where new work belongs. Anything not on this map needs an
explicit decision before it is added.

## Top level

- `.agents/` — orchestrator and specialist-agent contracts (who may do what).
- `.github/workflows/` — `quality.yml` (PR/`main` checks) and `release.yml` (tag/manual image builds).
- `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md` — issue and PR formats.
- `backend/` — FastAPI application, Alembic migrations, tests, lockfiles, Dockerfile.
- `frontend/` — React + TypeScript + Vite app, tests, lockfile, Dockerfile, nginx config.
- `config/agent-policy.yaml` — permissions, approval gates, quality gates.
- `docs/` — this playbook suite (see "Start here" in `README.md`).
- `plans/WORK_ITEMS.csv` — the task backlog (FMCG-001…FMCG-017) with owners, dependencies and gates.
- `scripts/check_docs.py` — integrity check for backlog IDs, dependencies and README references.
- `docker-compose.yml`, `.env.example` — single-host deployment and its placeholder configuration.
- `Makefile` — `lint` / `verify` entry points for the docs gate.

## Backend (`backend/`)

- `app/main.py` — application factory entry point (routers mount here as gates land).
- `app/core/` — configuration that fails closed (`config.py`: `FMCG_DATABASE_URL` required).
- `app/db/` — the single metadata registry (`base.py`) and engine/session factories (`session.py`).
- `app/api/`, `app/modules/` — reserved by `docs/ARCHITECTURE.md`; do not create until FMCG-007 needs them.
- `alembic/` — migrations; every schema change ships as a reviewed revision (see `docs/DATABASE_MANAGEMENT.md`).
- `tests/` — `test_health.py`, `test_migrations.py`; future `unit/`, `integration/`, `contract/` per gate plan.
- `requirements.in` / `requirements-dev.in` — pinned direct dependencies; `.txt` files are `uv`-compiled hashes.

## Frontend (`frontend/`)

- `src/` — `main.tsx`, `App.tsx`, colocated `*.test.tsx`; routes/components/tokens arrive with FMCG-013.
- `vite.config.ts` — dev `/health` proxy plus the vitest/jsdom configuration.
- `nginx.conf` — production static serving, SPA fallback and the `/health` proxy.

## Rules for new paths

1. Follow `docs/ARCHITECTURE.md` module boundaries; no parallel structures (no second `src/`, no stray scripts/).
2. Generated artifacts (`dist/`, caches, lockfile-adjacent build info) stay git-ignored, never committed.
3. Migrations are committed; test fixtures stay synthetic (policy: no production or personal data).
