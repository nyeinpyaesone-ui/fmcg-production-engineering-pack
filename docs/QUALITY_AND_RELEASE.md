# Quality, Version Control and Release Contract

## Version control

- Use protected `main`; feature branches use `feat/<scope>-<short-name>`, fixes `fix/<scope>-<short-name>`, releases
  `release/vX.Y.Z`.
- Require pull requests, review, passing required checks and resolved conversations.
- Do not force-push protected branches or commit secrets, local data, generated exports or production dumps.
- Keep changes small and reversible. Use conventional commit subjects where practical: `feat:`, `fix:`, `docs:`,
  `test:`, `build:`, `ci:`, `security:`.
- Semantic versioning: MAJOR for incompatible API/data behavior, MINOR for backward-compatible features, PATCH for
  compatible fixes.
- Tag only the exact verified commit: `vX.Y.Z`. Record image digest, migration range, SBOM, test evidence and deployment
  notes.
- Never claim remote merge, release or deployment without tool-confirmed evidence.

## Version baseline policy

The export shows Python 3.11-slim, Node 22 in CI, PostgreSQL 15, Redis 7 and several dated Python pins. These are
**source observations, not a verified current compatibility matrix**.

- Select a currently supported Python patch and pin it exactly for CI and runtime; do not silently mix 3.11 and 3.12.
- Keep PostgreSQL on a supported major line; pin image digest for production.
- Pin Node to an approved LTS major and exact CI version.
- Pin all direct and transitive dependencies via lockfiles; update through reviewed dependency PRs.
- Pin GitHub Actions to reviewed immutable commit SHAs in production workflows.
- Record versions in `docs/COMPATIBILITY.md` before implementation. Run compatibility tests before upgrades.

## Required CI stages

1. Checkout and validate repository policy.
2. Install from lockfiles.
3. Format check and lint.
4. Static type check.
5. Unit tests.
6. Integration tests against disposable PostgreSQL.
7. API/contract and migration tests.
8. Frontend tests and production build.
9. Dependency, secret and container scans.
10. Build immutable container artifact and attach provenance/SBOM.
11. Publish only from approved release workflow.

## Minimum quality gates

- No failing tests or migration drift.
- No known critical/high exploitable vulnerabilities without documented, time-bound exception approval.
- No secret findings.
- Authorization tests cover role and branch/company boundaries.
- Financial posting and inventory concurrency invariants are tested.
- Production image runs as non-root and has no unnecessary tools.
- Health and readiness semantics are verified.
- Release notes and operational runbooks are updated.

## Rollback and database changes

Application rollback is not automatically safe after schema changes. Prefer expand/migrate/contract:

1. Add backward-compatible schema.
2. Deploy code compatible with old and new schema.
3. Backfill and verify.
4. Switch reads/writes.
5. Remove old schema in a later release. For irreversible data changes, use a tested forward-fix plan. Restore from
   backup only under an approved incident procedure.
