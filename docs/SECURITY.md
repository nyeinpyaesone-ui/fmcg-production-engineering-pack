# Security Policy

## Report a vulnerability

Do **not** open a public issue for suspected vulnerabilities. Contact the repository owner privately
(contact channel to be appointed — tracked as pending in `docs/LAUNCH_CHECKLIST.md`) with: affected
commit/tag, reproduction steps, and impact assessment. Expect acknowledgment within two business days and
coordinated disclosure — no silent fixes, no public exploit details before a patch release.

## Standing rules (from `config/agent-policy.yaml`)

- Secrets are never read, emitted, committed or baked into images. `.env` files stay local and git-ignored.
- Production data is prohibited for agents; personal data is synthetic-or-redacted only.
- No public self-service privileged role assignment; the first administrator is seeded through a controlled
  bootstrap (FMCG-007).
- Destructive operations are denied; staging/production deploys and releases need explicit human approval.

## Controls by gate

- Every PR: gitleaks secret scan (CI), dependency pins with hashes, SHA-pinned GitHub Actions.
- FMCG-007: password hashing, login throttling, token expiry/rotation/revocation, RBAC with branch/company scope.
- FMCG-015: full threat model (auth, injection, CSRF/CORS, SSRF, uploads, dependencies) with documented
  disposition of every critical/high finding before release.
- Images: non-root users, minimal bases, no secrets in layers (verify with `docker history` before release).

## Dependency and image hygiene

Direct pins live in `requirements.in` / `package.json`; hashed lockfiles are regenerated with `uv pip compile`
(Python) and `npm` (frontend) and updated only through reviewed dependency PRs. Base images are digest-pinned
in the Dockerfiles and re-pinned deliberately (see `docs/MAINTENANCE.md`).
