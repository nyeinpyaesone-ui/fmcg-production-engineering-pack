# Release Management

Releases are immutable artifacts plus evidence — never a branch name, never a rebuild-on-the-host.

## Versioning

- Semantic versioning: `vMAJOR.MINOR.PATCH`. Major for breaking schema/API changes, minor for
  backward-compatible features, patch for fixes.
- One release per tag; a tag points at the exact verified commit and is never moved or deleted.

## Tagging

- Freeze scope, review the diff plus any migration scripts, and require full CI green first (Gate 8).
- Tagging needs explicit human approval (`create_release_tag: explicit_human_approval` in
  `config/agent-policy.yaml`).
- Tag the exact verified commit and push the tag (see `docs/DEPLOYMENT.md` step 6):

```sh
git tag vX.Y.Z && git push origin vX.Y.Z
```

- The `release.yml` workflow builds both images from that commit only; nothing is built by hand.

## Release evidence bundle (recorded before rollout)

- Image digests for backend and frontend (from the workflow summary), referenced by digest, not tag.
- Migration range: `alembic current` before and after `upgrade head` (today the head is `0001`).
- SBOM and provenance references (`sbom: true`, `provenance: mode=max` on both images).
- Smoke-test output from `docs/DEPLOYMENT.md` step 5 (`frontend OK`, `api OK`, `docker compose ps`).
- Sign-off in `docs/LAUNCH_CHECKLIST.md`: release owner, decision, date and evidence links.
- Record digests, migration range and approval date in `docs/COMPATIBILITY.md` before rollout.

## Registry naming

- Primary: `ghcr.io/<owner>/fmcg-erp-backend:<tag>` and `ghcr.io/<owner>/fmcg-erp-frontend:<tag>`.
- Mirror: `<dockerhub-user>/fmcg-erp-backend:<tag>` and `<dockerhub-user>/fmcg-erp-frontend:<tag>`.
- Production deploys by digest ref (`BACKEND_IMAGE` / `FRONTEND_IMAGE` in `.env`, then
  `docker compose pull`); staging builds locally. Owner-pending: set `DOCKERHUB_USERNAME` /
  `DOCKERHUB_TOKEN` secrets and confirm the first mirrored push.

## Rollback policy

- Application rollback after schema changes is not automatically safe; prefer expand/migrate/contract.
- Forward-fix first. If a forward-fix is impossible, follow the approved restore procedure in
  `docs/DEPLOYMENT.md` step 7 (previous tag, restore backup, recreate, smoke-test, reconcile).
- Release evidence for the rollback (digests, backup used, smoke output) is recorded like any release.
