# Launch Checklist — FMCG Production Engineering Pack

A launch here means the repository is public, reproducible and honestly described — **not** production-ready.
Production readiness is defined separately in `docs/IMPLEMENTATION_PLAN.md` (Gates 0–8) and is not claimed by this
checklist.

How to use: tick a box only with linked evidence (commit SHA, CI run URL, command output). Anything without evidence
stays unticked, no matter how confident the narrative sounds.

## 1. Repository and remote

- [x] Public repository created: `nyeinpyaesone-ui/fmcg-production-engineering-pack` (visibility PUBLIC).
- [x] `main` (`31f0ec8`) and `feat/gate1-gate2-foundation` (`274b91d`) pushed with tracking configured.
- [x] Default branch is `main`; work is done on `feat/*` branches per `docs/QUALITY_AND_RELEASE.md`.
- [x] Worktree clean at launch; 51 tracked files; `node_modules/`, `dist/`, `.venv/` and tool caches excluded
  (root `.gitignore` plus tool-generated nested ignores).
- [ ] Pull request opened for `feat/gate1-gate2-foundation` → this triggers the first remote CI run.
- [ ] Review completed and explicit merge approval recorded (policy: `merge_to_main: explicit_human_approval`).

## 2. Governance and approvals

- [x] Agent contracts (`.agents/`), operating model, task backlog (`plans/WORK_ITEMS.csv`) and policy
  (`config/agent-policy.yaml`, human-supervised, default-deny) are in place.
- [ ] FMCG-001 `in_review`: confirm authoritative branch/commit of `/home/admin/ERP`, deployment target,
  tenancy/branch model, user count, transaction volume and RPO/RTO. Partial evidence gathered: role default is
  `"user"` (`models.py:28`) and payment totals aggregate (`routers/payments.py:112`) in that repo.
- [ ] FMCG-002: v1 workflows and operating rules approved by the business owner (`approval_gate: yes`).
- [ ] FMCG-004: compatibility selections approved by a human (`approval_gate: yes`) after a green CI run.

## 3. CI and delivery

- [x] Docs job defined and green locally: yamllint, markdownlint (15 files, 0 issues), `check_docs.py`, gitleaks action.
- [x] Backend job repaired (installs the dev lockfile so `ruff`/`mypy`/`pytest` exist) and its exact steps proven
  green locally: `ruff check`, `mypy --strict`, `pytest -q` (3 passed).
- [x] Frontend job extended to typecheck, tests and production build; all three proven green locally
  (`tsc -b`, `vitest` 1 passed, `vite build` emitting `dist/`).
- [ ] First green run of `.github/workflows/quality.yml` on the PR — the authoritative signal for Python 3.11.17
  and Node 22.23.3, which the developer machine (Python 3.14.4) cannot replicate.
- [ ] Format gate: `ruff format` configured and invoked; frontend formatter installed and checked in CI
  (tracked deviation in `docs/COMPATIBILITY.md`, required by `config/agent-policy.yaml`).
- [ ] Workflow yamllint for `.github/workflows/*.yml` (tracked in FMCG-005 notes).
- [ ] Review and pin the `setup-python`/gitleaks action SHAs flagged TODO in `quality.yml` before release.

## 4. Security

- [x] No secrets in the tree: pattern scan clean, no `.env` files, `.gitignore` covers env/db/log artifacts.
- [ ] Gitleaks action result from the first CI run reviewed (local binary unavailable; `Makefile` tolerates this).
- [ ] Security reporting contact documented (no `SECURITY.md` yet — decide owner and channel).

## 5. Backend — Gate 1 workspace (FMCG-003 `in_progress`)

- [x] Runtime and dev pins with hashes compiled by `uv` for Python 3.11.17 (`requirements.txt`,
  `requirements-dev.txt` plus their `.in` sources, all committed).
- [x] FastAPI `/health` with CORS allow-list and `FMCG_CORS_ORIGINS` override; health test green.
- [ ] Green backend CI run on the pinned interpreter (pending first PR run).

## 6. Frontend — Gate 1 workspace (FMCG-003 `in_progress`)

- [x] `package-lock.json` committed; installed versions match the matrix
  (react 18.3.1, vite 6.0.3, typescript 5.6.3, vitest 3.2.7, jsdom 29.1.1).
- [ ] Green frontend CI run on Node 22.23.3 (pending first PR run).

## 7. Database — Gate 2 foundation (FMCG-006 `in_progress`)

- [x] Single metadata registry with naming conventions (`app/db/base.py`).
- [x] Fail-closed database configuration (`FMCG_DATABASE_URL` required, no silent default).
- [x] Async Alembic environment with `0001` empty anchor revision; tables start at FMCG-008.
- [x] Empty-database upgrade and downgrade/re-upgrade harness green locally (isolated SQLite file, same async path).
- [x] CLI `alembic upgrade head` and fail-closed refusal without the env var both demonstrated.
- [ ] Disposable-PostgreSQL migration verification (required before release, Gate 7).

## 8. Documentation

- [x] All markdown lint-clean; compatibility selections recorded with explicit verification status and known
  deviations (no `/ready` endpoint, no format gate, no built image yet).
- [x] README scope statement matches reality (docs + Gate 1 scaffold checks in this repo; full ERP CI elsewhere).
- [ ] Keep the README "Start here" list in sync when adding entry points (`scripts/check_docs.py` enforces this).

## 9. Deployment stage

- [x] Backend Dockerfile (pinned Python, hash-verified install, non-root `appuser`, stdlib healthcheck).
- [x] Frontend multi-stage Dockerfile (pinned Node build, pinned nginx, non-root `web` on 8080, `/health` proxy).
- [x] `docker-compose.yml`: private network, no published DB ports, one-shot `migrator`, health-gated startup.
- [x] `.env.example` with placeholders only; `.env` git-ignored and never baked into images.
- [x] `release.yml`: tag/manual trigger only, SHA-pinned actions, GHCR push with SBOM and `provenance: mode=max`.
- [x] `docs/DEPLOYMENT.md`: exact configure → build → backup → migrate → smoke-test → update/rollback procedure.
- [ ] First image build (no local Docker daemon; happens in `release.yml` or on the deployment host).
- [ ] Record built image digests, migration range and smoke-test output at release time (Gate 8).

## Sign-off

- Release owner: _pending_
- Decision (launch / launch with exceptions / hold): _pending_
- Date and evidence links: _pending_
