# Monitoring Playbook

Monitor the scaffold that exists today; everything beyond it is explicitly pending, not assumed.

## Per-service signals

- Backend: uvicorn process logs (plain text today — structured logs with request IDs are Gate 7 work)
  plus the `/health` liveness endpoint (returns `{"status":"ok"}`; probes no dependencies by design).
- Compose: `docker compose ps` health states — all services `running (healthy)` except the completed
  one-shot migrator. Anything else is an incident, not a quirk.
- Database: `pg_isready` against the `db` service (private `internal` network only, no published ports).
- Disk: `pgdata` volume growth and `backups/` directory size on the host.
- Future (pending, no outbox exists yet): queue/outbox backlog once durable async work lands (FMCG-008+).

## Log commands (run from the repository root)

```sh
docker compose ps
docker compose logs backend frontend db
docker compose logs -f backend
docker compose exec db pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"
curl -fsS "http://localhost:${FRONTEND_PORT:-8080}/health"
```

On any smoke-test failure, collect `docker compose logs backend frontend db` before changing anything
(see `docs/DEPLOYMENT.md` step 5).

## What to watch daily

- Service health (`docker compose ps`), previous-day close status, backup age, pending outbox —
  the opening checks in `docs/DEPLOYMENT.md` step 8 and `docs/DATA_AND_OPERATIONS.md`.
- Failed payments, stock conflicts, approval queues, document-number errors and access anomalies once
  those domains exist (FMCG-009 and later).

## Alert and SLO thresholds — owner-pending (FMCG-016)

- No alert thresholds, SLO targets, on-call owner or escalation path are defined yet.
- Defining service-level objectives, on-call ownership, escalation and incident severity is required
  before launch (see `docs/DATA_AND_OPERATIONS.md`); tracked under FMCG-016 load and recovery testing.
- Until then, monitoring is manual commands above plus human judgment — do not claim coverage that
  does not exist.
