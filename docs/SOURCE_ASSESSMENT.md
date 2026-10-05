# Source Assessment

> **Archival notice (2026-10-05):** This assessment reflects the original `ERP-FMCG.xml` Repomix export. Findings #1
> (`User.role` default) and #3 (`record_payment` totals) are known stale relative to the live repository — role now
> defaults to `"user"` and payment totals aggregate prior payments. Re-verify against the current source before acting
> on any finding.

## Evidence boundary

Assessment is based on the supplied `ERP-FMCG.xml` export. It is a compressed XML/Repomix representation; empty lines
were removed, some files may be excluded, and several Python files are fragments rather than complete modules. No source
repository checkout, dependency lock, database, CI run, or deployment evidence was provided.

## Source inventory

- Backend examples: FastAPI, Pydantic, SQLAlchemy async, PostgreSQL/asyncpg, Alembic, Redis, RabbitMQ/Pika, Celery.
- Domains represented: authentication/users, products/warehouses/stock movements, sales and purchasing,
  GL/invoices/payments, HR/payroll, manufacturing/BOM/work orders, CRM.
- Frontend scaffold in nested export: React + TypeScript + Vite, design tokens, agent instruction files, a GitHub
  quality workflow.
- Runtime examples: Python 3.11-slim; PostgreSQL 15; Redis 7 Alpine; RabbitMQ 3 management; Node 22 in CI.
- Dependency sample includes FastAPI 0.115.0, Uvicorn 0.30.6, SQLAlchemy 2.0.36, asyncpg 0.29.0, Alembic 1.13.1,
  Pydantic 2.7.4, pytest 8.0.0, and other packages.

## High-priority correctness and security risks

1. `User.role` defaults to `admin`; public registration must never grant privileged roles.
2. `SECRET_KEY`, database credentials, broker credentials and CORS examples contain unsafe development
   defaults/wildcards.
3. `record_payment` example sets `total_paid = amount`, which omits prior payments and can misstate invoice status.
4. Invoice creation is described as simplified and assumes account lookups exist; the transaction and posting guarantees
   are not demonstrated.
5. Journal-entry code shown does not demonstrate debit/credit balance validation or immutable posting rules.
6. Timestamp-derived document numbering is not safe under concurrent requests.
7. Stock movement model exists, but stock availability, locking, reservations, lot/expiry tracking, returns and
   valuation rules are not demonstrated.
8. The event bus is an in-memory placeholder; no durable outbox, retry, deduplication or dead-letter strategy is shown.
9. ORM model snippets use defaults and timestamps without consistently demonstrating database constraints, timezone
   handling or tenant/branch boundaries.
10. Docker healthcheck calls `curl`, but the shown image does not install curl. Runtime health behavior therefore needs
    validation.
11. Compose examples use development credentials, publish database/broker ports, and do not demonstrate production
    secret management or hardened network exposure.
12. The frontend scaffold has empty/incomplete files and uses `latest` dependencies; it is not evidence of a functioning
    ERP UI.
13. CI sample installs dependencies without a committed lockfile and invokes `pip-audit` without showing its
    installation or pinned tool version.
14. Tests are illustrative fragments; no meaningful coverage or passing test report is included.

## Readiness conclusion

**Not production-ready based on the supplied evidence.** It is a design and code-fragment baseline. The next valid
milestone is a reproducible repository bootstrap and a runnable vertical slice, followed by domain correctness,
security, test and deployment gates.

## Unknowns requiring repository-level confirmation

- Actual repository name, default branch, current commit and working-tree state.
- Which files are authoritative versus generated experiments.
- Whether the nested AI-native scaffold is part of this ERP or a separate reusable platform.
- Target deployment host, tenancy model, branch model, user count, transaction volume and recovery objectives.
- Myanmar tax/accounting rules applicable to the intended company and operating period.
