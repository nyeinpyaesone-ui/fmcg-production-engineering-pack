# Database Management

PostgreSQL is the source of truth; Alembic owns every schema change. Local exercises may use SQLite through the
same async path, but SQLite behavior never qualifies a migration for production.

## Registry and configuration

- One metadata registry: `app/db/base.py` with Alembic-friendly naming conventions. All models inherit `Base`.
- Connection string comes only from `FMCG_DATABASE_URL` (`app/core/config.py` raises if unset — fail closed).
- Runtime driver is `asyncpg`; migrations run through the async Alembic environment (`backend/alembic/env.py`).

## Daily commands (from `backend/`, with `FMCG_DATABASE_URL` exported)

```sh
../.venv/bin/alembic current          # where are we?
../.venv/bin/alembic history          # the chain
../.venv/bin/alembic upgrade head     # migrate up (via compose: docker compose run --rm migrator)
../.venv/bin/alembic downgrade -1     # one step back (empty DB / staging only, never blind production)
../.venv/bin/alembic revision --autogenerate -m "<what>"   # draft only — see review rules
```

## Migration review rules (all mandatory)

1. Autogenerate is a draft assistant: hand-edit every revision, name constraints per the registry conventions,
   and prefer explicit `op.*` calls over opaque batches.
2. Every migration is backward-compatible with the running code **or** follows expand/migrate/contract across
   releases (add → deploy → backfill → switch → remove). Destructive single-step rewrites are rejected.
3. `upgrade head` **and** `downgrade base` must pass on an empty database before merge (the harness in
   `tests/test_migrations.py` enforces the shape; dialect risk needs disposable PostgreSQL per Gate 7).
4. Backup before upgrade, always (`docs/DEPLOYMENT.md` step 4). No backup, no migrate.
5. `modify_migrations: review_required` — a second pair of eyes on every revision file, no exceptions.

## Data discipline (from `docs/DATA_AND_OPERATIONS.md`)

Money as `NUMERIC`/`Decimal`, UTC storage with `Asia/Yangon` rendering, explicit branch/company ownership on
domain rows, append-only audit records with actor/timestamp/correlation ID, least-privilege DB roles with
migration credentials separated from runtime credentials.
