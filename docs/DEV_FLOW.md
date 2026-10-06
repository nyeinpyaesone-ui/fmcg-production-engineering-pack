# Development Flow (Branch → PR → Merge)

The only path to `main`. Direct pushes to `main` are for nobody, including maintainers.

## 1. Branch

```sh
git checkout main && git pull
git checkout -b feat/<scope>-<short-name>   # fix/<scope>-<short-name> for fixes
```

One branch per work item where practical; name it after the FMCG ID in the PR body, not necessarily the branch.

## 2. Implement (smallest coherent change)

- Touch only the assigned paths; no drive-by refactors (orchestrator contract).
- Keep `plans/WORK_ITEMS.csv` notes and `docs/COMPATIBILITY.md` in sync with behavior changes.
- Never commit secrets, `.env` files, dumps, caches or `dist/` output.

## 3. Gate locally, then push

```sh
# docs gate
npx markdownlint-cli2 "README.md" "docs/**/*.md" ".agents/**/*.md"
python3 scripts/check_docs.py
# backend (from backend/)
../.venv/bin/ruff check . && ../.venv/bin/mypy app && ../.venv/bin/pytest -q
# frontend
npm run check --prefix frontend && npm test --prefix frontend && npm run build --prefix frontend
git push -u origin feat/<scope>-<short-name>
```

## 4. Pull request

```sh
gh pr create --base main --fill-first   # then complete the PR template body
```

The PR template requires: task IDs, verification commands with outputs, CI run URL, risk review and approvals.
`quality.yml` runs automatically: docs, backend and frontend jobs must all pass.

## 5. Merge (human only)

- Reviewer approval recorded; `approval_gate: yes` tasks need their named approval first.
- Explicit merge approval per policy (`merge_to_main: explicit_human_approval`).
- Squash or rebase to keep history readable; never force-push `main`; never merge with red checks.

## Rollback of a bad merge

`git revert` the merge commit on a new branch and run the full flow again. For schema-carrying releases, follow
the forward-fix-first rule in `docs/DEPLOYMENT.md` — reverting code does not revert a database.
