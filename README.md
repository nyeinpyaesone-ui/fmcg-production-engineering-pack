# FMCG ERP — Production Engineering Pack

**Status:** Planning and governance package derived from the supplied `ERP-FMCG.xml` Repomix export.  
**Not a compiled application, production release, or proof of deployment.**

> Pack rebuilt 2026-10-05: CI validates this repo's docs (markdown, YAML, CSV integrity, secret scan) plus the Gate 1
> scaffold's backend checks and frontend typecheck, tests and build. Full ERP application CI belongs to the ERP
> repository.

## Scope

The source contains FMCG ERP backend fragments (FastAPI/SQLAlchemy/PostgreSQL), Docker/Compose and CI examples, plus a
separate AI-native React/Vite scaffold. Treat these as separate source contexts until repository ownership and intended
product boundaries are confirmed.

## Start here

1. `docs/SOURCE_ASSESSMENT.md` — source-supported findings and limitations.
2. `docs/ARCHITECTURE.md` — target modular-monolith architecture.
3. `docs/IMPLEMENTATION_PLAN.md` — gated implementation sequence.
4. `plans/WORK_ITEMS.csv` — task-level execution backlog.
5. `.agents/` — orchestrator and specialist-agent contracts.
6. `config/agent-policy.yaml` — permissions, approval gates and execution controls.
7. `docs/QUALITY_AND_RELEASE.md` — test, CI, release and rollback requirements.
8. `docs/DATA_AND_OPERATIONS.md` — data integrity, operations, backup and observability.
9. `.github/workflows/quality.yml` — docs lint, integrity checks, and Gate 1 scaffold backend/frontend checks.
10. `docs/LAUNCH_CHECKLIST.md` — launch readiness checklist with verified evidence and pending gates.
11. `.github/pull_request_template.md` — PR format: task IDs, evidence, risks and approvals.
12. `docs/DEPLOYMENT.md` — single-host deployment runbook: configure, build, backup, migrate, verify, rollback.
13. `docs/LIFECYCLE.md` — full software life cycle with owners and exit criteria.
14. `CHANGELOG.md` — notable changes per release.

## Playbooks

- `docs/PROJECT_STRUCTURE.md` — repository layout and directory ownership.
- `docs/SPRINT_SETUP.md` — sprint cadence and work-item flow.
- `docs/ENV_SETUP.md` — clean-clone developer environment setup.
- `docs/DEV_FLOW.md` — branch to pull-request to merge.
- `docs/API_CONTRACT.md` — API versioning and compatibility rules.
- `docs/DATABASE_MANAGEMENT.md` — migration discipline and review rules.
- `docs/SECURITY.md` — vulnerability reporting and standing rules.
- `docs/TESTING_STRATEGY.md` — test pyramid and runnable commands.
- `docs/QA.md` — independent verification before every gate.
- `docs/CODE_REVIEW.md` — review checklist for safe merges.
- `docs/CICD.md` — pipeline map and incident history.
- `docs/RELEASE_MANAGEMENT.md` — versioning, tagging and evidence bundle.
- `docs/MONITORING.md` — per-service signals and pending thresholds.
- `docs/BACKUP_RECOVERY.md` — backup policy with concrete commands.
- `docs/PERFORMANCE.md` — budgets and load-test plan.
- `docs/DISASTER_RECOVERY.md` — scenarios and restore hierarchy.
- `docs/MAINTENANCE.md` — dependency and image upkeep commands.
- `docs/DOCUMENTATION.md` — docs standards and enforcement gates.
- `docs/ISSUE_MANAGEMENT.md` — templates, triage and linkage rules.

## Important

The uploaded XML is a read-only packed representation. Changes belong in the original repository, not in this export. Do
not treat code fragments or example configuration as a complete repository. No credentials should be copied from source
into this package or committed to a repository.
