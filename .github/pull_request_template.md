## What and why

Task IDs (e.g. `FMCG-006`):

Summary:

Related documents / prior discussion:

## Changes

- ...
- ...

## Verification (commands with outputs, not claims)

```text
# backend
ruff check .
mypy app
pytest -q
# docs
npx markdownlint-cli2 "README.md" "docs/**/*.md" ".agents/**/*.md"
python3 scripts/check_docs.py
# frontend
npm run check --prefix frontend
npm test --prefix frontend
npm run build --prefix frontend
```

Results:

CI run URL (required before merge):

## Risk review

- [ ] No secrets, credentials, dumps or local data added
- [ ] No migration impact, or migration plan attached and reviewed
- [ ] No auth/permission changes, or security review requested
- [ ] No financial-posting changes, or domain + QA review requested
- [ ] Docs updated (`COMPATIBILITY.md`, README list, `WORK_ITEMS.csv` notes where applicable)

## Approvals needed

- [ ] Reviewer approval
- [ ] Human approval for `approval_gate: yes` tasks (state which):
- [ ] Explicit merge approval (required for `main`)
