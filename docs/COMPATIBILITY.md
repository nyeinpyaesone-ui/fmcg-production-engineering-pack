# Compatibility Matrix — Approval Required

This file intentionally distinguishes source-observed versions from target choices. Do not treat target values as tested
until CI proves compatibility.

| Component             | Source evidence                                               | Target policy                                           |
| --------------------- | ------------------------------------------------------------- | ------------------------------------------------------- |
| Python                | 3.11-slim Docker; backend sample pins unspecified interpreter | Choose one supported patch; exact pin across CI/runtime |
| FastAPI               | 0.115.0                                                       | Pin after compatibility/security review                 |
| Uvicorn               | 0.30.6                                                        | Pin with tested worker/lifecycle configuration          |
| SQLAlchemy            | 2.0.36                                                        | Keep 2.x; pin and test async transaction patterns       |
| asyncpg               | 0.29.0                                                        | Pin and test with selected PostgreSQL major             |
| Alembic               | 1.13.1                                                        | Pin; migration autogeneration must be reviewed          |
| Pydantic              | 2.7.4                                                         | Pin compatible with FastAPI/settings package            |
| PostgreSQL            | 15                                                            | Select supported major; production image digest pin     |
| Redis                 | 7-alpine                                                      | Optional; pin patch/digest if adopted                   |
| RabbitMQ              | 3-management                                                  | Defer unless durable async use case requires it         |
| Celery                | 5.6.0                                                         | Defer until worker architecture is approved             |
| Node.js               | 22 in nested scaffold CI                                      | Approved LTS patch, exact CI/runtime pin                |
| React/Vite/TypeScript | `latest` in scaffold                                          | Pin exact versions in lockfile; no floating tags        |
| GitHub Actions        | checkout@v4/setup-python@v5/setup-node@v4                     | Pin reviewed action SHAs and update deliberately        |

Record selected versions, image digests, lockfile hashes, test run URL and approval date here before the first release
candidate.
