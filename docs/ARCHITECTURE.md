# Target Architecture

## Decision

Use a **modular monolith** for the first production-capable release. Keep business domains in one deployable backend
with explicit module boundaries. Do not introduce microservices or a message broker dependency until measured workload
or operational isolation justifies them.

## Logical components

- Web UI: React + TypeScript + Vite.
- API/application: FastAPI, with transport handlers separated from use cases.
- Domain modules: identity/access, master data, sales, procurement, inventory, finance, reporting; HR, manufacturing and
  CRM follow after core workflows are stable.
- Persistence: PostgreSQL as source of truth; SQLAlchemy 2 async and Alembic migrations.
- Background work: start with a PostgreSQL-backed outbox and a small worker only where asynchronous work is required.
  Redis is optional for cache/rate limiting. RabbitMQ/Celery are deferred until a documented use case requires them.
- Observability: structured logs, request/correlation IDs, metrics and health/readiness endpoints.
- Delivery: container image, Compose for controlled single-host deployment, GitHub Actions for CI and release evidence.

## Transactional rules

1. One application use case owns one explicit database transaction.
2. Validate authorization and business invariants before committing.
3. Use database constraints for uniqueness, foreign keys, non-negative quantities where applicable, and accounting line
   integrity.
4. Use row locks or atomic conditional updates for stock and payment-sensitive operations.
5. Use idempotency keys for externally retried commands such as payment recording and document submission.
6. Never publish an external event before the database transaction commits. Persist outbox events in the same
   transaction and deliver asynchronously.
7. Posted financial documents are immutable. Correct them with reversal/adjustment entries and preserve the audit trail.
8. Keep money as `NUMERIC`/`Decimal`; never use binary floating point for financial calculations.
9. Store timestamps in UTC; render using the configured business timezone (`Asia/Yangon` where appropriate).
10. Define explicit branch/company ownership on every relevant record before enabling multi-branch or multi-company use.

## Suggested backend layout

```text
backend/
  app/
    main.py
    core/          # config, security, logging, errors
    db/            # session, base, migrations integration
    api/           # versioned routers and dependencies
    modules/
      identity/
      master_data/
      sales/
      procurement/
      inventory/
      finance/
      reporting/
    integrations/
    workers/
  alembic/
  tests/
    unit/
    integration/
    contract/
```

Each module should contain `domain/`, `application/`, `infrastructure/`, and `api/` only where complexity warrants it.
Avoid empty ceremonial layers.

## FMCG-specific data model requirements

- Product: SKU, base unit, conversion units, barcode, active state, tax classification.
- Inventory: warehouse/location, movement ledger, reservations, lot/batch, expiry date where relevant, adjustment reason
  and actor.
- Procurement: supplier, purchase order, goods receipt, supplier bill, supplier payment.
- Sales: customer, price list, sales order, fulfillment/delivery, invoice, receipt/payment, returns and credit notes.
- Finance: chart of accounts, fiscal period, journal header/lines, posting status, source-document reference, reversal
  linkage.
- Governance: user, role/permission, branch/company scope, approval record, audit event, idempotency record, outbox
  event.

Do not implement tax rates, payroll formulas or accounting policies as assumptions. Obtain approved Myanmar-specific
rules and effective dates from the business/accounting owner before encoding them.
