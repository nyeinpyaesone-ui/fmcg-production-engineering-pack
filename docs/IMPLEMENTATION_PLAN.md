# Step-by-Step Implementation Plan

## Gate 0 — Repository and scope verification

**Exit evidence:** confirmed repository, branch/commit, file inventory, ownership of generated snippets, deployment
target, user roles, business workflows, data classification and non-functional requirements.

- Preserve source and create a baseline tag/backup before edits.
- Identify duplicate/generated files and select authoritative implementations.
- Agree v1 scope: recommended first slice is product/customer setup → purchase receipt → stock visibility → sales order
  → fulfillment → invoice/payment → balanced journal posting.
- Define branch/company model, approval matrix, tax/accounting rules, MMK precision/rounding and document numbering
  policy.

## Gate 1 — Reproducible engineering foundation

**Exit evidence:** clean clone builds deterministically; CI is green.

- Standardize repository layout and Python/frontend workspace boundaries.
- Select supported Python patch and Node LTS patch; pin exact versions in runtime files and CI.
- Add Python lockfile with hashes and npm lockfile; remove `latest`.
- Add formatting, lint, type checking, tests, secret scanning, dependency audit and container build checks.
- Add `.env.example` with placeholders only; validate required secrets at startup.
- Add Docker build context exclusions, non-root runtime, signal handling and verified health probes.

## Gate 2 — Database and identity foundation

**Exit evidence:** migrations work from empty database and upgrade a prior fixture; authz tests pass.

- Build one metadata registry and Alembic environment; fail closed if migration configuration is missing.
- Add migration review rules, backup-before-upgrade and tested rollback/forward-fix procedures.
- Implement password hashing, login throttling, token expiry/rotation/revocation policy, secure cookies or bearer
  handling, and account recovery.
- Remove self-service privileged role assignment; seed initial administrator through a one-time controlled bootstrap.
- Add RBAC plus company/branch scope checks and audit events for privileged actions.

## Gate 3 — Master data and inventory ledger

**Exit evidence:** concurrent stock tests preserve ledger and availability invariants.

- Implement product, unit conversion, warehouse/location, supplier/customer master data.
- Model append-only stock movements and derived balances.
- Implement receipt, issue, transfer, adjustment, reservation, release, return and stock count workflows.
- Define valuation method and lot/expiry policy with business approval.
- Add concurrency controls, idempotency and reconciliation jobs.

## Gate 4 — Sales and procurement vertical slice

**Exit evidence:** full workflow passes integration and end-to-end tests.

- Implement purchase order → goods receipt → supplier bill.
- Implement sales order → allocation → delivery → invoice.
- Validate prices, discounts, taxes, credit limits and approval thresholds server-side.
- Enforce state transitions and prevent edits to submitted/posted documents.
- Add cancellation, returns and correction workflows.

## Gate 5 — Finance integrity

**Exit evidence:** every posted source document produces balanced, traceable entries; reconciliation reports agree.

- Implement chart of accounts and fiscal periods.
- Validate journal lines: at least two lines, non-negative amounts, exactly one side per line, debit total equals credit
  total.
- Add posting service with atomic transaction, unique source reference and idempotency.
- Implement receivables/payables allocation, partial payments, overpayment handling, reversal and period close.
- Have a qualified accounting owner approve mappings and reports.

## Gate 6 — UI, reporting and operational controls

**Exit evidence:** role-based workflows usable on target devices and reports reconcile to source records.

- Implement accessible React screens with typed API contracts and loading/error/empty states.
- Add daily closing, stock valuation, sales, receivables/payables and audit reports.
- Add export controls, data access logging and sensitive-field masking.
- Add Burmese/English labels and Myanmar date/currency display only after localization rules are approved.

## Gate 7 — Production hardening

**Exit evidence:** security, performance, recovery and operational acceptance tests pass.

- Threat model and review authentication, authorization, injection, CSRF/CORS, SSRF, upload and dependency risks.
- Run load tests against agreed workload and latency/error targets.
- Test backup restore, migration recovery, disk exhaustion, service restart and broker/cache outage behavior.
- Configure TLS/reverse proxy, firewall, secrets, log retention, alerting, monitoring and incident runbooks.
- Complete user acceptance testing and data migration rehearsal.

## Gate 8 — Release candidate and controlled rollout

**Exit evidence:** immutable image digest, signed release evidence, rollback/forward-fix plan and business sign-off.

- Freeze scope; review all diffs and migration scripts.
- Run full quality gate on the exact release commit.
- Generate SBOM and scan image/dependencies.
- Deploy to staging using production-like configuration and sanitized data.
- Execute smoke tests and reconciliation checks.
- Obtain explicit release approval; deploy progressively and monitor.
- Close release only after post-deployment verification and backup confirmation.

## Definition of production-ready

A successful frontend build alone is insufficient. Production readiness requires repeatable builds, reviewed migrations,
correct business transactions, security controls, automated tests, operational observability, tested recovery,
documented ownership and an approved release.
