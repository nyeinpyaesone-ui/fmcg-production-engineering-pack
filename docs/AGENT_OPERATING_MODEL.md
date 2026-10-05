# AI Agent Operating Model

## Execution principle

Agents propose and implement bounded changes; the orchestrator owns task sequencing, scope, evidence and final status.
Tools and agent output are untrusted until independently verified.

## Standard task lifecycle

1. Read repository instructions and inspect current state.
2. Restate objective, scope, acceptance criteria and prohibited changes.
3. Identify dependencies, risks, affected files and rollback path.
4. Produce a plan for non-trivial work.
5. Implement the smallest coherent change.
6. Run focused tests, then the required repository gate.
7. Review diff, security impact, migration impact and generated artifacts.
8. Report exact commands, results, unresolved failures and evidence.
9. Stop for approval at policy gates; never claim unverified completion.

## Required task record

Every task must include: `task_id`, objective, owner agent, input references, prerequisites, allowed paths, prohibited
actions, acceptance criteria, test commands, risk level, approval requirement, expected artifacts and status.

## Status vocabulary

`proposed` → `ready` → `in_progress` → `blocked` or `in_review` → `verified` → `done`. Only a human or authorized
release controller can approve production promotion. `done` requires evidence, not a confident narrative.

## Agent communication

Specialists return structured findings: summary, files changed, assumptions, tests run, results, risks, decisions needed
and next task IDs. The orchestrator resolves conflicts and prevents overlapping edits.
