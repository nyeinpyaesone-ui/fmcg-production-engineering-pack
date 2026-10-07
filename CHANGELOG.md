# Changelog — FMCG Production Engineering Pack

All notable changes, newest first. Format follows Keep-a-Changelog conventions; versions follow semver.
Each release links its evidence bundle (digests, migration range, SBOM, smoke output, sign-off).

## [Unreleased]

### Added

- Full playbook suite (`docs/`, 30 documents) covering structure, sprints, environment, dev flow,
  API contract, database, security, testing, QA, review, CI/CD, release, deployment, monitoring,
  backup/recovery, performance, disaster recovery, maintenance, documentation and issues.
- Gate 1/2 scaffold: FastAPI `/health` with CORS allow-list, metadata registry with naming conventions,
  fail-closed DB config, async Alembic environment with `0001` empty anchor, React + TypeScript + Vite
  scaffold with vitest harness.
- Deployment stage: digest-pinned Dockerfiles (non-root), compose with private network and one-shot
  migrator, `release.yml` (GHCR + Docker Hub mirror, SBOM, `provenance: mode=max`), deployment runbook.
- CI: docs/backend/frontend/container/disposable-PostgreSQL jobs, format gates (ruff, Prettier),
  workflow yamllint, release quality gate. First green runs recorded in `docs/LAUNCH_CHECKLIST.md`.

## [v0.1.0] — planned (not yet tagged)

First immutable release. Requires: PR #1 merged with approvals, `DOCKERHUB_*` secrets set, tag on the
verified commit, release workflow green, digests recorded in `docs/COMPATIBILITY.md`.
