# Backup and Recovery Playbook

Policy source: `docs/DATA_AND_OPERATIONS.md`. Procedure source: `docs/DEPLOYMENT.md` step 4.
This file joins them into one drillable page.

## Policy

- Automate encrypted database backups with retention; monitor backup success and age.
- Keep backup credentials separate from application credentials. (The current scaffold reuses
  `POSTGRES_*` for both — separation lands with production hardening; do not mistake today's
  convenience for the policy.)
- Drill restores on a schedule into an isolated environment — never over the live database.
- After every restore, verify row counts, ledger balances, financial trial balance and smoke tests.
- Business owner sets explicit RPO/RTO targets before production (pending — FMCG-001/FMCG-016).

## Commands (Gate 2 rule: backup before every migration)

```sh
mkdir -p backups
docker compose exec db pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" | gzip > "backups/pre-$(date +%Y%m%d-%H%M%S).sql.gz"
docker compose run --rm migrator
docker compose run --rm migrator alembic -c alembic.ini current
```

The `current` command must print the expected head revision (`0001` until FMCG-008 lands tables).

## Restore into an isolated environment

```sh
gunzip -c backups/<chosen>.sql.gz | docker compose exec -T db psql -U "$POSTGRES_USER" "$POSTGRES_DB"
docker compose up -d --force-recreate backend frontend
```

Then run the step 5 smoke tests plus ledger/trial-balance reconciliation per
`docs/DATA_AND_OPERATIONS.md` before trusting the restored data.

## Retention guidance

- Always keep the pre-migration backup of the running release until the next release is verified.
- Move old backups off the host over an encrypted channel; watch `backups/` retention during daily
  operations (`docs/DEPLOYMENT.md` step 8).
- Exact retention windows and encryption mechanism are owner-pending — record the decision here once
  the business owner sets it.

## Drill log

- Every drill is signed off in `docs/LAUNCH_CHECKLIST.md` (owner, date, decision, evidence links).
- Load and recovery testing, including restore checks against agreed RPO/RTO, is tracked in FMCG-016
  and must pass before any production data exists.

## Credential separation

- `.env` is git-ignored and never baked into images; backup scripts read it from the host only.
- Never commit dumps, never ship `.env` in images, never log credentials (see `docs/SECURITY.md`).
