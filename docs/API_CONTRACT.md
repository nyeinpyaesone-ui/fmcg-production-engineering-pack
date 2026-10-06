# API Contract

The rules every endpoint follows — current surface first, then the binding conventions for future work
(FMCG-007 onward). The frontend treats every response as untrusted (see `.agents/frontend-agent.md`).

## Current surface (verify any time)

- `GET /health` → `200 {"status":"ok"}`. Liveness only: asserts nothing about dependencies, by design.
- Framework-provided: `/docs`, `/redoc`, `/openapi.json` (development aid, not a product contract).
- CORS: allow-list from `FMCG_CORS_ORIGINS` (defaults for Vite dev `http://localhost:5173`,
  `http://127.0.0.1:5173` and compose/prod `http://localhost:8080`, `http://127.0.0.1:8080`);
  foreign origins are rejected. Verified live during foundation checks.
- There is deliberately no `/ready` yet — a readiness probe that asserts nothing would be dishonest
  (tracked deviation in `docs/COMPATIBILITY.md`).

## Conventions for new endpoints (binding from FMCG-007)

1. **Versioned prefix:** `/api/v1/...`; breaking changes require `/api/v2`, never silent v1 changes.
2. **Errors:** use FastAPI `HTTPException` with a plain-string `detail` (e.g. `{"detail": "order is submitted"}`);
   4xx for caller faults, never stack traces or SQL text in responses.
3. **State transitions:** submitted/posted documents reject edits with `409`; corrections use reversal flows.
4. **Idempotency:** every retryable `POST` accepts (and for payments, requires) an `Idempotency-Key` header;
   replays with the same key return the original result without re-executing.
5. **Money and time:** `Decimal`/`NUMERIC` in JSON as strings, UTC timestamps with offset (`...+06:30` accepted).
6. **Pagination:** list endpoints paginate (`limit` default 50, max 500) with stable ordering; no unbounded lists.
7. **OpenAPI is the contract:** routers must render clean schemas; the frontend generates or mirrors its types from
   them at FMCG-013 — never hand-maintained parallel types.
8. **No browser-authoritative math:** tax, availability and posting totals are computed server-side, always.

## Change control

New endpoints arrive with contract tests (success, validation, authz, idempotent replay) and an
`docs/ARCHITECTURE.md`-consistent changelog note in the PR. Removing or renaming a field is a MAJOR change.
