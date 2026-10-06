# Performance Playbook

No performance target is agreed yet. Budgets below are owner-pending — this page says what will be
measured, not what is promised.

## Budgets — owner-pending

- API latency (p50/p95/p99), error-rate ceiling, and per-endpoint budgets: pending business-owner sign-off.
- Frontend bundle budget: pending. Reference point only — the current `frontend/dist/` JS bundle is
  ~143 kB (`assets/index-*.js`); treat it as a baseline to defend, not a target met.
- Database pool sizing and connection limits: pending (the scaffold runs SQLAlchemy engine defaults with
  `pool_pre_ping`; nothing is sized or limited deliberately yet).

## Gate 7 / FMCG-016 load-test plan

- Agree the workload first: representative order-to-cash and procure-to-pay flows, concurrent users,
  and transaction volumes from FMCG-001 (all currently unconfirmed).
- Agree latency and error-rate targets with the business owner before running the suite.
- Run against staging (never production), on release-digest images, with a seeded database.
- Pass criteria: agreed SLOs met, RPO/RTO and restore checks green, results recorded with the run
  configuration. FMCG-016 approval gate is `yes` — no silent self-certification.

## What to measure

- Request latency percentiles (p50/p95/p99) and error rate per endpoint.
- Database pool saturation, connection failures and slow-query counts.
- Queue/outbox backlog once durable async work exists (none today).
- Frontend bundle size per release (`npm run build` output) and time-to-interactive on staging.
- Reconciliation health: failed payments, stock conflicts and close exceptions during the run.

## Future database indexing

- No domain tables exist yet (Alembic head is the `0001` empty anchor; tables start at FMCG-008).
- Index foreign keys, tenant/branch scope columns and document-number uniques as each domain lands,
  and re-verify with `EXPLAIN` under the FMCG-016 workload — not by intuition.
- Keep migration discipline from `docs/DATABASE_MANAGEMENT.md`: every index ships as a reviewed
  revision with upgrade/downgrade coverage.
