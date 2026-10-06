# Code Review Playbook

Reviews protect `main`, not egos. Every comment must point at a rule below, a doc, or a failing check.

## 1. Keep diffs small

- One work item per pull request where practical; name the FMCG ID in the PR body.
- Touch only assigned paths — no drive-by refactors (see `.agents/orchestrator.md`).
- A diff too large to review in one sitting goes back for splitting before content review starts.

## 2. Migration second-eyes rule

- Any change under `backend/alembic/` needs a second reviewer who did not write the revision.
- The reviewer checks upgrade/downgrade pairing, data-preserving intent, and the backup-before-upgrade
  precondition from `docs/DEPLOYMENT.md` step 4.
- Migration tests in `backend/tests/test_migrations.py` must be green; see `docs/DATABASE_MANAGEMENT.md`.

## 3. Security pass (every PR, no exceptions)

- No secrets, tokens, passwords, dumps, `.env` files or `dist/` output in the diff.
- Auth, permission or role changes require a security review (`security_review_required` in
  `config/agent-policy.yaml`); financial-posting changes require domain and QA review.
- Confirm SHA-pinned actions and hashed lockfiles are untouched unless the PR is a reviewed upgrade.

## 4. Tests with evidence

- The PR body lists the exact verification commands and their outputs, not claims of greenness.
- New behavior ships with tests per `docs/TESTING_STRATEGY.md`; one failed criterion fails the task.
- QA verdicts follow `docs/QA.md`: derive checks from acceptance criteria, not from the implementation.

## 5. Docs sync

- Behavior changes update `docs/COMPATIBILITY.md`, the README start-here list, and `plans/WORK_ITEMS.csv`
  notes in the same PR (the PR template has a checkbox for this).
- Stale statements get corrected or marked pending with owner and task ID — never silently deleted.

## 6. Approval and merge rules

- Approval matrix lives in `config/agent-policy.yaml`: `merge_to_main` needs explicit human approval,
  and `approval_gate: yes` tasks need their named approval first.
- Merge only with all `quality.yml` checks green; a human performs the merge (see `docs/DEV_FLOW.md`).
- Never force-push `main`; never merge with red checks. Revert a bad merge with `git revert` on a new
  branch, and forward-fix schema-carrying releases per `docs/DEPLOYMENT.md` step 7.
