# Documentation Standards

Docs are a gate, not decoration: `quality.yml` fails the PR when these standards break.

## Enforcement

- Lint config is `.markdownlint-cli2.jsonc`: default rules on, line length 120 (`MD013`, tables and
  code blocks exempt), `MD033` off for HTML-free prose, `MD041` first-line-heading rule relaxed.
- `python3 scripts/check_docs.py` enforces backlog integrity (unique FMCG IDs, valid dependencies)
  and README reference integrity (every backtick `docs|plans|config|.agents|.github` path must exist).
- Both run in CI on every PR and on push to `main`; run them locally before pushing (see
  `docs/DEV_FLOW.md` step 3).

## Style rules (CI depends on these)

- No markdown tables — use bullet lists and code blocks (avoids MD060 alignment failures).
- No line over 120 characters (MD013). No HTML (keeps MD033 clean).
- End every file with exactly one trailing newline (MD047).
- One heading, one idea; short imperative titles matching the existing `docs/` voice.

## Content rules

- One fact, one place. The compatibility matrix owns versions, the runbook owns commands, the
  launch checklist owns verification state — link across, never duplicate.
- Evidence over narrative: tick boxes, record digests and attach outputs. Anything without evidence
  stays marked pending (see `docs/LAUNCH_CHECKLIST.md`).
- README start-here sync rule: adding an entry point means adding its README line in the same PR;
  `check_docs.py` rejects references to files that do not exist.
- Reference only paths that exist in the repo and FMCG IDs only for their documented scope in
  `plans/WORK_ITEMS.csv`.

## Archival notices for stale findings

- When the world moves past a written finding, annotate it in place — do not rewrite history.
- Follow the `docs/SOURCE_ASSESSMENT.md` pattern: a quoted notice naming the stale items, what
  changed, and where to re-verify before acting on them.
- Stale-but-unowned statements get an owner and task ID, or an explicit pending mark — never silence.
