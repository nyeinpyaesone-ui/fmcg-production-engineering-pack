# Data Integrity and Operations

## Data integrity controls

- Define a data owner and classification for every domain.
- Use database constraints as the final integrity boundary.
- Use `Decimal` and explicit rounding rules for money, tax and unit conversions.
- Keep source documents, stock ledger movements and posted accounting entries traceable by stable IDs.
- Use idempotency keys for retryable commands and unique constraints for external references.
- Record actor, timestamp, action, entity, correlation ID and before/after summary in append-only audit records; avoid
  logging secrets or unnecessary personal data.
- Apply least privilege to database roles and separate migration credentials from runtime credentials.
- Use tenant/company/branch scoping consistently in queries, unique constraints and authorization.

## Operations baseline

- Separate local, test, staging and production configuration and data.
- Expose only the reverse proxy/API publicly. Keep PostgreSQL, Redis and brokers on private networks.
- Use managed secret injection; never ship `.env` files in images.
- Provide liveness, readiness and dependency health checks with bounded timeouts.
- Emit structured logs with request IDs; redact credentials, tokens, payroll/bank data and customer-sensitive fields.
- Monitor request rate, latency, error rate, DB pool saturation, connection failures, queue/outbox backlog, disk space,
  backup age and reconciliation failures.
- Define service-level objectives, on-call owner, escalation and incident severity before launch.

## Backup and recovery

Before production, the business owner must set explicit RPO/RTO targets.

- Automate encrypted database backups and retention.
- Keep backup credentials separate from application credentials.
- Monitor backup success and age.
- Perform scheduled restore drills into an isolated environment.
- Verify row counts, ledger balances, financial trial balance and application smoke tests after restore.
- Document point-in-time recovery, key rotation and disaster recovery contacts.

## Daily operational controls

- Opening checks: service readiness, previous-day close status, backup status, pending outbox, unresolved reconciliation
  exceptions.
- During operations: monitor failed payments, stock conflicts, approval queues, document-number errors and access
  anomalies.
- Closing: reconcile cash/bank receipts, sales invoices, stock movements, returns, GL postings and branch totals;
  require sign-off for exceptions.
- Preserve an auditable correction path; do not silently edit posted transactions.
