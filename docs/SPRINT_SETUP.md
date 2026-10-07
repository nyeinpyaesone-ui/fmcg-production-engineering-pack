# Sprint Setup

How work is sequenced, planned and reviewed. There are no story points here: the unit of work is the FMCG work
item with explicit acceptance criteria and approval gates.

## Backlog source of truth

`plans/WORK_ITEMS.csv` is the only backlog. Columns that matter most:

- `depends_on` — hard sequencing (e.g. FMCG-006 needs FMCG-003). `scripts/check_docs.py` validates references.
- `approval_gate` — `yes` / `security_review` / `domain_review` / `business_owner_approval_required` stop
  autopilot; work pauses until the named human approves.
- `status` — controlled vocabulary from `docs/AGENT_OPERATING_MODEL.md`:
  `proposed` → `ready` → `in_progress` → `blocked` or `in_review` → `verified` → `done`.

## Sprint cadence (weekly, adjust by agreement)

1. **Plan (start of week):** move at most two P0 items to `ready`; confirm owners and unblocked dependencies.
2. **Execute:** one item `in_progress` per owner; keep PRs small and reversible; CI must stay green on `main`.
3. **Review:** demo working behavior (not slides); update `notes` with evidence links (CI runs, digests, test output).
4. **Retro:** record one process fix as a follow-up task or a playbook edit in this `docs/` suite.

## Work-in-progress limits

- Max two `in_progress` items per owner; max one release candidate in flight.
- A `blocked` item must name the blocker, the owner waiting on, and the date it was raised — within one day.
- Nothing moves to `verified` without the acceptance criteria demonstrated (command output or CI URL attached).

## Definition of ready (all required before `ready`)

Acceptance criteria written, dependencies `done` or explicitly waived, approval path known, test commands known.
