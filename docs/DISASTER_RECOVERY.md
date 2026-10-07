# Disaster Recovery Playbook

Recovery objectives are owner-pending. This page defines the hierarchy and scenarios now, so the
FMCG-001/FMCG-016 decisions land on a ready structure.

## RPO/RTO — owner-pending (FMCG-001/FMCG-016)

- No RPO/RTO targets are set; the business owner must set them before production.
- Load and recovery testing (FMCG-016, approval gate `yes`) must prove the targets with restore drills.
- Until targets exist and drills are green, no production data and no recovery claims.

## Scenarios

- Host loss: rebuild on a fresh host from the release tag, restore the latest verified backup,
  migrate to the release head, verify per the runbook.
- Disk exhaustion: `pgdata` or `backups/` fills the volume; database stalls or backups fail.
  Free retention first, then restore service — never delete the only good backup to make room.
- Bad migration: `upgrade head` fails or lands wrong schema. Stop, keep the pre-migration backup,
  forward-fix preferred; restore only under the approved procedure.
- Credential leak: rotate the exposed credential at the source, replace it in host `.env`, recreate
  services; treat logged or committed secrets as compromised even after removal from the tree.

## Escalation contacts — pending

- Release owner, on-call engineer and business decision-maker: all pending; recorded in
  `docs/LAUNCH_CHECKLIST.md` sign-off once appointed.
- Suspected vulnerabilities follow `docs/SECURITY.md`: private contact to the owner, never a public
  issue, with coordinated disclosure.

## Restore hierarchy (in order, stop at the first that works)

1. Restore the pre-migration backup into an isolated environment (`docs/BACKUP_RECOVERY.md`).
2. Rebuild from the release tag (`git checkout vX.Y.Z`, `docker compose pull` on digest refs).
3. Migrate to the release head (`docker compose run --rm migrator`, confirm with `alembic current`).
4. Verify per the runbook: smoke tests, then ledger/trial-balance reconciliation.
5. Roll forward or roll back only under the approved procedure in `docs/DEPLOYMENT.md` step 7 —
  application rollback after schema changes is not automatically safe.

## References

- Procedure: `docs/DEPLOYMENT.md` steps 4 (backup/migrate), 5 (smoke-test) and 7 (update/rollback).
- Policy: `docs/DATA_AND_OPERATIONS.md` backup and recovery section.
- Evidence: release bundle per `docs/RELEASE_MANAGEMENT.md`; drill sign-off in the launch checklist.
