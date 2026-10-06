# Issue Management Playbook

Issues are tracked work, not chat. Every issue leads to an FMCG ID, a decision, or a close reason.

## Templates (in `.github/ISSUE_TEMPLATE/`)

- Bug report (`.github/ISSUE_TEMPLATE/bug_report.md`, auto-label `bug`): what happened vs expected,
  exact reproduction commands, environment (interpreter, node, OS, commit), evidence.
- Feature request (`.github/ISSUE_TEMPLATE/feature_request.md`, auto-label `enhancement`): FMCG ID and
  gate, objective with acceptance criteria, dependencies and risks, approval required per
  `config/agent-policy.yaml`.
- Suspected vulnerabilities never become public issues — see `docs/SECURITY.md` for the private channel.

## Labels

- `bug`: something verified broken against documented behavior; needs reproduction first.
- `enhancement`: bounded change tied to the gate plan; needs an FMCG ID and acceptance criteria.
- Keep labels to these two until the backlog outgrows them; labels route, they do not decide.

## Triage SLA

- Classify every new issue within 2 days: confirm the template is complete, attach the FMCG ID,
  set priority and owner, or close with a reason.
- Incomplete reports go back to the reporter once with a specific ask; silence for 14 days closes them.
- Security-adjacent reports escalate the same day to the private channel — no public discussion first.

## Linkage rules

- Every PR names its task IDs in the body (the PR template requires it); every issue names its FMCG
  ID once triaged. Unlinked work is invisible work.
- `approval_gate: yes` tasks need their named approval recorded before merge (see
  `config/agent-policy.yaml` and `docs/CODE_REVIEW.md`).
- Backlog truth lives in `plans/WORK_ITEMS.csv`; issues execute the backlog, they do not replace it.

## Duplicates and stale handling

- Duplicates close into the surviving issue with a link; the survivor keeps the best reproduction.
- Stale issues (no activity in 30 days) get one ping with a concrete next step, then close after
  14 more days of silence. Reopening with new evidence is always welcome.
- Fixed issues close only with the verifying commit or run linked — claim-free closing is reverted.
