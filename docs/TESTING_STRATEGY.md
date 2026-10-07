# Testing Strategy

Tests are evidence, not decoration: every suite below must be runnable with one command, green on `main`, and
required in CI before its gate is claimed.

## Pyramid (what lives where)

- **Unit** — `backend/tests/` (`pytest`), `frontend/src/**/*.test.tsx` (vitest/jsdom). Pure logic, validation,
  error paths. Fast (< 1 min combined today).
- **Migration** — `backend/tests/test_migrations.py`: empty-DB upgrade plus downgrade/re-upgrade on an isolated
  file. Shape-guarantee only; dialect risk is covered at the next level.
- **Integration** (from FMCG-006 exit / Gate 7) — disposable PostgreSQL service: concurrent stock operations,
  payment replay, journal balance, migration upgrade from a prior fixture.
- **Contract/API** (from FMCG-007) — OpenAPI-conformant requests, authz matrices (role × branch/company scope),
  idempotent replay of payment/submission endpoints.
- **End-to-end** (from FMCG-013) — browser flows for order-to-cash and procure-to-pay against staging.
- **Load/recovery** (Gate 7, FMCG-016) — agreed workload, latency/error targets, restore drills.

## Commands (the whole strategy in five lines)

```sh
cd backend && ../.venv/bin/ruff check . && ../.venv/bin/mypy app && ../.venv/bin/pytest -q
npm run check --prefix frontend && npm test --prefix frontend && npm run build --prefix frontend
npx markdownlint-cli2 "README.md" "docs/**/*.md" ".agents/**/*.md" && python3 scripts/check_docs.py
```

Loop runner `scripts/verify_all.sh` executes all of the above with per-suite retries and `EVENT` lines
(`BUILD_FRONTEND=1` includes the production build); it exits nonzero if anything stays red.

## Rules

1. New behavior ships with tests for success, validation failure, authorization denial and (for money/stock)
   concurrency/replay. Untested invariants do not exist.
2. Test data is synthetic; fixtures live with the tests; no production dumps, ever.
3. Flaky tests are quarantined the same day they flake — a red `main` stops all feature work.
4. Security-relevant tests (escalation, cross-scope access, replay) are reviewed by QA/security eyes (FMCG-015).
