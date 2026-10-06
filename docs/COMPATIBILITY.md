# Compatibility Matrix — Approval Required

This file intentionally distinguishes source-observed versions from target choices. Do not treat target values as tested
until CI proves compatibility.

**Status: awaiting human approval (FMCG-004, `approval_gate: yes`).** The *Selected* column records decisions taken on
2026-10-06. They are selections, not test evidence — see "Verification status" below.

| Component             | Source evidence                                               | Target policy                                           | Selected (2026-10-06)                                                                    |
| --------------------- | ------------------------------------------------------------- | ------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Python                | 3.11-slim Docker; backend sample pins unspecified interpreter | Choose one supported patch; exact pin across CI/runtime | **3.11.17** — bugfix support to 2027-10-31; runtime image `3.11.17-slim@sha256:0dd364ba` |
| FastAPI               | 0.115.0                                                       | Pin after compatibility/security review                 | **0.115.6**                                                                              |
| Uvicorn               | 0.30.6                                                        | Pin with tested worker/lifecycle configuration          | **0.32.1** — lifecycle config not yet tested                                             |
| SQLAlchemy            | 2.0.36                                                        | Keep 2.x; pin and test async transaction patterns       | **2.0.54** — 2.0 line; 2.1 held back for maturity                                        |
| asyncpg               | 0.29.0                                                        | Pin and test with selected PostgreSQL major             | **0.31.0**                                                                               |
| Alembic               | 1.13.1                                                        | Pin; migration autogeneration must be reviewed          | **1.20.0**                                                                               |
| aiosqlite             | not in export (test-only SQLite driver)                       | Pin test-only; never use in production                  | **0.22.1** — dev lockfile only                                                           |
| Pydantic              | 2.7.4                                                         | Pin compatible with FastAPI/settings package            | **2.13.5** — `pydantic-core` pinned transitively at 2.46.5                               |
| PostgreSQL            | 15                                                            | Select supported major; production image digest pin     | **15** — compose pins `15-alpine@sha256:f7d23353`; production digest recorded at release |
| nginx                 | not in export (frontend static server)                        | Pin patch and digest; non-root, unprivileged port       | **1.28-alpine@sha256:a8b39bd9**                                                          |
| Redis                 | 7-alpine                                                      | Optional; pin patch/digest if adopted                   | not adopted                                                                              |
| RabbitMQ              | 3-management                                                  | Defer unless durable async use case requires it         | deferred                                                                                 |
| Celery                | 5.6.0                                                         | Defer until worker architecture is approved             | deferred                                                                                 |
| Node.js               | 22 in nested scaffold CI                                      | Approved LTS patch, exact CI/runtime pin                | **22.23.3** — LTS support to 2027-04-30; build image `22.23.3-slim@sha256:c3de60bf`      |
| React/Vite/TypeScript | `latest` in scaffold                                          | Pin exact versions in lockfile; no floating tags        | react **18.3.1**, vite **6.0.3**, typescript **5.6.3**                                   |
| GitHub Actions        | checkout@v4/setup-python@v5/setup-node@v4                     | Pin reviewed action SHAs and update deliberately        | pinned to immutable SHAs in `.github/workflows/quality.yml`                              |

## Why these versions

- **Python 3.11.17** is the latest 3.11 patch. 3.11 is still receiving bugfix releases (until 2027-10-31), so staying on
  the line the export observed does not mean an unsupported interpreter. Bumping to 3.12 would require changing
  `requires-python`, ruff `target-version` and mypy `python_version` together; `docs/QUALITY_AND_RELEASE.md` forbids
  mixing 3.11 and 3.12 silently.
- **Node 22.23.3** is the latest 22 LTS patch, matching the export's observed major. Node 24 LTS was not adopted because
  the export and the scaffold both target 22.
- **vitest 3.2.7 runs on the pinned vite.** vitest 3.2.7 declares `vite ^5.0.0 || ^6.0.0 || ^7.0.0-0` as a direct
  dependency, which the pinned vite 6.0.3 satisfies (verified against the installed `vitest` metadata). Do not upgrade
  vitest without confirming the new release still accepts vite 6.0.3 in the same change.
- **jsdom 29.1.1, not 30.x.** jsdom 30 requires node `^22.22.2`; 29.1.1 requires `^22.13.0` and therefore works on both
  the pinned CI runtime (22.23.3) and older 22.x developer machines.
- **SQLAlchemy 2.0.54, not 2.1.x.** 2.1 is a new minor line; the 2.0 line is mature and matches the export's observed
  lineage. Re-evaluate 2.1 deliberately through a reviewed dependency PR, not silently.
- **aiosqlite 0.22.1 is test-only.** Migration-harness tests run the same async Alembic path against an isolated
  SQLite file. Production uses asyncpg/PostgreSQL; dialect-specific migrations still need disposable-PostgreSQL
  verification before release.

## Verification status

Not yet verified on the selected runtime. The available developer machine runs Python 3.14.4 and has no Python 3.11.17
interpreter, so local `ruff`, `mypy` and `pytest` runs exercise the code but **not** the pinned interpreter. The first
authoritative signal for 3.11.17 is a CI run on `.github/workflows/quality.yml`. Do not mark FMCG-004 `verified` until
that run is green.

## Known deviations from the quality contract

- **Health and readiness are not separated.** `/health` is liveness only and probes no dependencies, because no external
  dependency exists yet. `docs/QUALITY_AND_RELEASE.md` requires verified health/readiness semantics; a `/ready` endpoint
  that asserts nothing would not satisfy it. Tracked as an open deviation on FMCG-005.
- **No frontend `format` gate.** `config/agent-policy.yaml` lists `format` as required. `ruff format` is available in the
  pinned ruff but is not yet configured or invoked, and no frontend formatter is installed.
- **No image built yet.** Dockerfiles, compose and the release workflow exist with digest-pinned bases, but no
  image has been built (no local Docker daemon; first build happens in `release.yml` or on the host). Record built
  image digests here at release time.

## Recording requirement

Record selected versions, image digests, lockfile references, test run URL and approval date here before the first release
candidate.
