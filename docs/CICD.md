# CI/CD Pipeline Map

Two workflows exist in `.github/workflows/`. Both use SHA-pinned actions; re-pin deliberately, never float.

## `quality.yml` — every change

- Triggers: `pull_request` targeting `main`, and `push` to `main`.
- Permissions are read-only (`contents: read`); concurrency cancels superseded runs per ref.
- Three jobs, all required before merge:
  - `docs`: yamllint on `config/agent-policy.yaml`, markdownlint over README/docs/agents,
    `python3 scripts/check_docs.py`, then the gitleaks secret scan.
  - `backend`: Python `3.11.17` (`actions/setup-python`), installs `backend/requirements-dev.txt`,
    then `ruff check`, `mypy app` (strict) and `pytest -q`.
  - `frontend`: Node `22.23.3` (`actions/setup-node` with npm cache on `frontend/package-lock.json`),
    then `npm ci`, `npm run check` (`tsc -b`), `npm test` (vitest), `npm run build` (vite).
- Pinned SHAs today: checkout `11bd7190`, setup-python `0b93645e`, setup-node `60edb5dd`,
  gitleaks-action `ff98106e`. Two of these still carry a TODO: verify and pin the setup-python and
  gitleaks SHAs to reviewed immutable values before release (tracked in `docs/LAUNCH_CHECKLIST.md`).

## `release.yml` — tags only

- Triggers: push of a `v*` tag, plus manual `workflow_dispatch`. Nothing else builds release images.
- Uses the `docker-container` buildx driver, logs in to GHCR with `GITHUB_TOKEN`, and mirrors to
  Docker Hub with the owner-held `DOCKERHUB_USERNAME` / `DOCKERHUB_TOKEN` repository secrets
  (set via `gh secret set`; values never appear in the file or its logs).
- Builds backend (`backend/Dockerfile`) and frontend (`frontend/Dockerfile`), pushes to
  `ghcr.io/<owner>/fmcg-erp-backend` and `.../fmcg-erp-frontend` plus the Docker Hub mirror,
  with SBOM (`sbom: true`) and `provenance: mode=max` on both images.

## Known incidents already fixed on this branch

- Gitleaks on PR events failed without credentials: the step now passes
  `GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}` (gitleaks-action requires it for `pull_request` scans).
- Gitleaks scanned an unresolvable range on shallow checkouts: the docs job now sets `fetch-depth: 0`
  so the PR base..head range resolves. First green run: `37502034199` (Python 3.11.17, Node 22.23.3).

## How to read a run

- `gh pr checks` — per-job status on the current pull request.
- `gh run view <run-id> --log-failed` — failing steps with output; start from the first red job.
- `gh run watch <run-id>` — follow a release-tag run until digests are published.

## Local gate equivalents (before pushing)

```sh
npx --yes markdownlint-cli2 "README.md" "docs/**/*.md" ".agents/**/*.md"
python3 scripts/check_docs.py
cd backend && ../.venv/bin/ruff check . && ../.venv/bin/mypy app && ../.venv/bin/pytest -q
npm run check --prefix frontend && npm test --prefix frontend && npm run build --prefix frontend
```

Local greens exercise the code but not the pinned runtimes — the authoritative signal is always the
green `quality.yml` run on the PR (see `docs/COMPATIBILITY.md`).
