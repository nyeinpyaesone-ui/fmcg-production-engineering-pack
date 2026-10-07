# Maintenance Playbook

Dependencies and base images move only through reviewed PRs. Silent upgrades do not exist here.

## Monthly dependency review

- Review open upstream advisories for every pinned component in `docs/COMPATIBILITY.md`.
- Decide per item: upgrade now (reviewed PR), defer with a dated reason, or accept the risk in writing.
- Record the decision, the approver and the date in `docs/COMPATIBILITY.md` — the matrix is the log.
- Never batch unrelated upgrades into one PR; one concern per diff (see `docs/CODE_REVIEW.md`).

## Python lockfile regeneration (exact commands, from the repository root)

```sh
uv pip compile backend/requirements.in --python-version 3.11.17 \
  --python-platform x86_64-unknown-linux-gnu --generate-hashes -o backend/requirements.txt
uv pip compile backend/requirements-dev.in --python-version 3.11.17 \
  --python-platform x86_64-unknown-linux-gnu --generate-hashes -o backend/requirements-dev.txt
```

- Direct pins live in `backend/requirements.in` and `backend/requirements-dev.in`; the hashed `.txt`
  lockfiles are what CI installs. Keep both in sync in the same PR.
- Verify after regen: `ruff check`, `mypy app` (strict), `pytest -q` from `backend/`.

## Frontend lockfile

```sh
npm update --prefix frontend
```

- The lockfile (`frontend/package-lock.json`) is committed; CI installs with `npm ci`.
- Verify after update: `npm run check`, `npm test` and `npm run build` with the `frontend` prefix.
- Do not upgrade vitest without confirming the new release still accepts the pinned vite 6.0.3
  (see the compatibility notes in `docs/COMPATIBILITY.md`).

## Base-image digest re-pinning

- Digests are pinned in `backend/Dockerfile`, `frontend/Dockerfile` and `docker-compose.yml`.
- Resolve the new digest with a registry-token `curl` against the image manifest, then update the
  Dockerfiles and record the new digest in `docs/COMPATIBILITY.md` in the same reviewed PR.
- Rebuild deterministically (`docker compose build --pull`) and confirm the release workflow still
  publishes matching digests before rollout.

## Action SHA re-pinning

```sh
gh api repos/<owner>/<repo>/commits/<tag> --jq .sha
```

- Resolve the immutable commit SHA for the new action tag, update `.github/workflows/quality.yml`
  (and `release.yml` where applicable), and keep the `# vX` comment beside each SHA.
- The setup-python and gitleaks SHAs still carry a verify-before-release TODO — clear it through
  this process, not by editing the comment away.

## Rules

- Reviewed dependency PRs only; green `quality.yml` before merge; human merge per `docs/DEV_FLOW.md`.
- Never commit a lockfile you have not installed and tested locally first.
