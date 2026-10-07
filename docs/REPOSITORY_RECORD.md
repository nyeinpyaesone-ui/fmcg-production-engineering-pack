# Repository Record — Gate 0 Evidence

Recorded 2026-10-05, pack HEAD `d6cbb29`.

> Update 2026-10-07: PRs #1 and #2 are merged — `main` is now `55dd433` (Gate 1/2 scaffold, deployment
> stage, hardening, all CI green). The inventory below describes the Gate 0 HEAD only and is kept for history;
> see `docs/PROJECT_STRUCTURE.md` for the current layout.

## Repository

- Path: `/home/admin/fmcg/fmcg-production-engineering-pack`
- VCS: git, default branch `main`, root commit `d6cbb29` ("docs: initial commit of FMCG production engineering pack")
- Parent repo caution: the pack previously lived inside `/home/admin/.git`'s scope as untracked files. It is now its own
  repo and is excluded from the parent by its own `.git` boundary. The parent working tree at `/home/admin/.git` should
  not track this path.

## File inventory (HEAD)

- `.agents/` — 6 specialist/orchestrator contracts (md)
- `.github/workflows/quality.yml` — docs lint + integrity CI
- `config/agent-policy.yaml` — permissions and approval gates
- `docs/` — 8 documents (assessment, architecture, implementation plan, quality/release, data/operations, compatibility,
  agent model, this record)
- `plans/WORK_ITEMS.csv` — 17 tasks, all `proposed`
- `scripts/check_docs.py` — docs/CSV/README-path integrity check
- `Makefile`, `.gitignore`, `.yamllint.yaml`, `.markdownlint-cli2.jsonc`, `README.md`

## Source ownership

- This pack is derived from the `ERP-FMCG.xml` Repomix export; the export is read-only and **not** the editable source
  of truth (per `README.md` and orchestrator contract).
- The live implementation candidate is the repository at `/home/admin/ERP` (branch/commit unconfirmed — flagged for
  FMCG-001 follow-up). Confirm authoritative branch/HEAD there before Gate 1 edits.
- `/home/admin/fmcg/fmcg-production-engineering-pack.zip` is an archived copy; ignored via `.gitignore`, not committed.

## Unconfirmed (blocks full FMCG-001 closure)

- Authoritative branch/commit and owner of `/home/admin/ERP`.
- Whether the nested AI-native scaffold (React/Vite) belongs to this product or is a separate platform.
- Deployment target, tenancy/branch model, user count, transaction volume, RPO/RTO targets.
- Approved Myanmar tax/accounting rules and effective dates.

## Completion

Gate 0 item FMCG-001 is **in_review** pending human confirmation of the unconfirmed items above.
