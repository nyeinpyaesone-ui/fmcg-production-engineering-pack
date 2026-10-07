# Software Lifecycle — FMCG Production Engineering Pack

The full life of this repo's software, from idea to retirement. Each stage names its owner, entry/exit criteria
and the repo machinery that enforces it. Nothing advances on narrative — only on evidence.

## 1. Ideation → backlog (`orchestrator`)

- Ideas enter as GitHub issues (see `docs/ISSUE_MANAGEMENT.md`) and become `FMCG-###` rows in
  `plans/WORK_ITEMS.csv` with owner, dependencies, acceptance criteria and approval gates.
- Enter: a bounded problem with a proposed acceptance test. Exit: `ready` status per `docs/SPRINT_SETUP.md`.

## 2. Development (`backend` / `frontend` / `devops` agents)

- One `feat/` or `fix/` branch per work item; smallest coherent change; assigned paths only
  (see `docs/DEV_FLOW.md` and `docs/PROJECT_STRUCTURE.md`).
- Exit: local gates green — `scripts/verify_all.sh` (all suites, retries, `EVENT` lines, nonzero on red).

## 3. Review (`orchestrator` + human)

- Pull request on the PR template: task IDs, verification commands with outputs, CI URL, risk review.
- Review per `docs/CODE_REVIEW.md`; QA verdicts per `docs/QA.md`. Merge is human-only with explicit
  approval (`merge_to_main: explicit_human_approval`).

## 4. Continuous integration (automated)

- `quality.yml` on every PR and `main` push: docs, backend (3.11.17), frontend (Node 22.23.3),
  containers, disposable-PostgreSQL migration proof (see `docs/CICD.md`).
- Red main stops all feature work until green again.

## 5. Release (human-approved, machine-built)

- Pre-tag gate: `scripts/release_check.sh vX.Y.Z` verifies clean tree, green CI on the exact commit,
  and tag availability — then a human approves and tags.
- `release.yml` builds immutable backend/frontend images with SBOM and `provenance: mode=max`,
  pushing to GHCR plus the Docker Hub mirror (see `docs/RELEASE_MANAGEMENT.md`).
- Evidence bundle (digests, migration range, SBOM, smoke output, sign-off) is recorded before rollout;
  changes are appended to `CHANGELOG.md` under the release heading.

## 6. Deploy (`docs/DEPLOYMENT.md`)

- Configure (`.env` from `.env.example`, never committed) → build/pull → database health →
  backup → migrate (`docker compose run --rm migrator`) → smoke-test → observe.
- Production deploys by digest ref, never by rebuild; staging builds locally.

## 7. Operate (`docs/MONITORING.md`, `docs/BACKUP_RECOVERY.md`)

- Daily: service health, close status, backup age, disk, outbox (see `docs/DEPLOYMENT.md` step 8).
- Backups encrypted, retained, restored on schedule into isolated environments; every drill signed
  in `docs/LAUNCH_CHECKLIST.md`.

## 8. Maintain (`docs/MAINTENANCE.md`)

- Monthly dependency review; lockfiles, digests and action SHAs move only through reviewed PRs.
- Format/lint gates keep every change clean; stale findings get archival notices, not silent edits.

## 9. Retire

- A release line ends with a dated notice in `CHANGELOG.md`, a final backup, and credential rotation.
- History is never rewritten: tags stay, evidence stays, the record stays honest.
