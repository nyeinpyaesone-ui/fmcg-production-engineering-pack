# Deployment Runbook — Single-Host Compose

Target: one controlled host running the Gate 1/2 scaffold (FastAPI + static frontend + PostgreSQL 15).
Source of truth for versions: `docs/COMPATIBILITY.md`. Every command below is written for the repository root.

## 0. Prerequisites

- Docker Engine 24+ with Compose v2, 2 GB RAM free, TCP 8080 free on the host.
- A shell that can read `.env` (all variable references below assume `set -a; source .env; set +a`
  or an equivalent; never export secrets into history files).
- Release tag checked out for production (never deploy a feature branch to production).

## 1. Configure (once per host, then on secret rotation only)

```sh
cp .env.example .env
chmod 600 .env
# Edit .env: set POSTGRES_USER, a long random POSTGRES_PASSWORD, POSTGRES_DB,
# FMCG_CORS_ORIGINS (public browser origins) and FRONTEND_PORT.
# Verify: grep -c CHANGE_ME .env  → must print 0 before proceeding.
```

`.env` is git-ignored and never baked into images (see Dockerfiles: no `COPY .env` anywhere).

## 2. Build images

```sh
docker compose build --pull
```

Base images are digest-pinned in the Dockerfiles, so a rebuild is deterministic; `--pull` refreshes only
within the pinned digest (a no-op unless the registry serves different bytes for the same digest, which fails
closed). First image builds happen in CI (`release.yml`) or on the host — there is intentionally no local-only
build cache to trust.

## 3. Start the database and wait for health

```sh
docker compose up -d db
docker compose exec db pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"
```

The `db` service publishes no ports: PostgreSQL is reachable only on the private `internal` network.

## 4. Back up, then migrate

Back up before every migration (Gate 2 rule: backup-before-upgrade):

```sh
mkdir -p backups
docker compose exec db pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" | gzip > "backups/pre-$(date +%Y%m%d-%H%M%S).sql.gz"
docker compose run --rm migrator
docker compose run --rm migrator alembic -c alembic.ini current
```

The second command must print the expected head revision (`0001` until FMCG-008 lands its tables). The migrator
is a one-shot service: it exits after `upgrade head` and leaves no running container behind.

## 5. Start everything and smoke-test

```sh
docker compose up -d
sleep 15
curl -fsS "http://localhost:${FRONTEND_PORT:-8080}/" > /dev/null && echo "frontend OK"
curl -fsS "http://localhost:${FRONTEND_PORT:-8080}/health" && echo && echo "api OK"
docker compose ps
```

Expected: `frontend OK`, `api OK` with body `{"status":"ok"}`, and all services `running (healthy)` except the
completed migrator. On failure, collect `docker compose logs backend frontend db` before changing anything.

## 6. Release flow (immutable artifacts)

1. Freeze scope and review the diff plus any migration scripts (Gate 8).
2. Tag the exact verified commit: `git tag vX.Y.Z && git push origin vX.Y.Z`.
3. The `release` workflow builds both images with SBOM and `provenance: mode=max` and pushes them to GHCR as
   `ghcr.io/<owner>/fmcg-erp-backend:<tag>` and `.../fmcg-erp-frontend:<tag>`.
4. Record the image digests (from the workflow summary), migration range, SBOM reference and smoke-test output
   in `docs/COMPATIBILITY.md` and the release notes before rollout.
5. Deploy the tag with steps 2–5 above. GHCR images are the immutable release evidence; host builds from the
   same tag must produce the same digests.

## 7. Update and rollback

Update (forward only while schema is backward-compatible):

```sh
git fetch origin && git checkout vX.Y.Z
docker compose build --pull
# backup (step 4), migrate (step 4), restart (step 5)
docker compose up -d --force-recreate backend frontend
```

Rollback: application rollback is **not** automatically safe after schema changes (see
`docs/QUALITY_AND_RELEASE.md`). Prefer expand/migrate/contract. If a forward-fix is impossible, restore under
an approved incident procedure:

```sh
git checkout <previous-tag>
docker compose build --pull
gunzip -c backups/<chosen>.sql.gz | docker compose exec -T db psql -U "$POSTGRES_USER" "$POSTGRES_DB"
docker compose up -d --force-recreate backend frontend
# then step 5 smoke tests plus ledger/trial-balance reconciliation per docs/DATA_AND_OPERATIONS.md
```

## 8. Daily operations

- Opening: service health (`docker compose ps`), previous-day close status, backup age, pending outbox.
- Logs: `docker compose logs -f backend` (structured logs with request IDs; secrets are never logged).
- Disk: watch `pgdata` growth and `backups/` retention; old backups leave the host on an encrypted channel.
- Recovery drills and SLO/RPO/RTO targets are tracked in FMCG-016 and must pass before any production data exists.
