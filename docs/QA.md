# QA Process

QA is independent verification against acceptance criteria — a green build alone never passes a gate
(see `.agents/qa-security-agent.md`).

## Per-task QA (before `in_review` → `verified`)

1. Read the acceptance criteria in `plans/WORK_ITEMS.csv`; derive checks from business invariants, not from the
   implementation (derive from the docs, test against the code).
2. Re-run the exact commands from `docs/TESTING_STRATEGY.md` on a clean checkout; attach outputs.
3. Probe the priority risks for the area: privilege escalation, cross-branch access, payment replay, stock races,
   journal imbalance, data leakage, missing audit events.
4. Confirm docs sync: matrix, runbook, README list and backlog notes reflect the change.
5. Record verdict per criterion (pass/fail + evidence link). One failed criterion fails the task.

## Release QA (before any `v*` tag)

1. Full CI green on the exact tag commit (quality jobs; release workflow dry-review for tag pushes).
2. Migration rehearsal: backup → `upgrade head` → `current` shows expected head → smoke tests → reconciliation
   totals agree (see `docs/DEPLOYMENT.md` steps 4–5 and `docs/DATA_AND_OPERATIONS.md` closing controls).
3. Fresh-eyes walkthrough of order-to-cash and procure-to-pay on staging with role-based accounts.
4. Open deviations reviewed: each must have an owner, a time bound, and a tracked follow-up — or block release.
5. Sign-off recorded in `docs/LAUNCH_CHECKLIST.md` (owner, date, decision, evidence links).

## Bug handling

Reproduce first (exact commands in the issue, per the bug template), then fix on a `fix/` branch with a
regression test that fails without the fix. Classify severity by data/financial impact, not by stack-trace length.
