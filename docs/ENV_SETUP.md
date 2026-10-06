# Environment Setup (Developer Machine)

Exact steps for a clean clone. All commands run from the repository root unless noted.

## Prerequisites

- Python 3.11+ locally (CI enforces exactly 3.11.17; see the version caveat below).
- Node.js 22 (CI enforces exactly 22.23.3).
- No Docker needed for code/test work (only for image builds and compose deploys).

## 1. Python workspace

```sh
python3 -m venv .venv
.venv/bin/pip install -r backend/requirements-dev.txt
```

The dev lockfile includes the runtime lockfile, so this one install covers `ruff`, `mypy`, `pytest` and `httpx`.
Verify: `../.venv/bin/pytest -q` from `backend/` (expect 3 passed).

## 2. Frontend workspace

```sh
npm ci --prefix frontend
```

Verify: `npm run check --prefix frontend` (typecheck), `npm test --prefix frontend` (vitest),
`npm run build --prefix frontend` (production build into `frontend/dist/`, git-ignored).

## 3. Run the stack locally

```sh
# Terminal 1 — backend on :8000
cd backend && ../.venv/bin/uvicorn app.main:app --reload --port 8000

# Terminal 2 — frontend on :5173, /health proxied to the backend
npm run dev --prefix frontend
```

Smoke: `curl -fsS http://127.0.0.1:8000/health` → `{"status":"ok"}`.

## 4. Local database (migrations only — no domain tables yet)

```sh
export FMCG_DATABASE_URL="sqlite+aiosqlite:///$PWD/backend/dev.db"
cd backend && ../.venv/bin/alembic upgrade head && ../.venv/bin/alembic current
```

Production uses PostgreSQL; SQLite here exercises the same async Alembic path. Never point this at a real
database file you care about, and never commit `*.db` (git-ignored).

## Version caveat (read before trusting local greens)

The developer machine may run a different interpreter (e.g. 3.14) than the pinned 3.11.17. Local `ruff`/`mypy`/
`pytest` runs exercise the code but **not** the pinned runtime — the authoritative signal is always the green
`quality.yml` run on the PR. See `docs/COMPATIBILITY.md` for the full statement.
