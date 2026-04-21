# Workflows

This file is the short operational summary for working in this repository. The normative workflow contract lives in `specs/rigorloop-workflow.md`.

## Choose A Lane

- Use the fast lane for trivial or low-risk work only.
  - Reference path: `spec -> implement -> verify -> pr`
  - Allowed categories: typos, formatting-only changes, small documentation clarifications, comment-only changes, small test-fixture corrections, small non-behavioral renames, and minor generated-artifact refreshes that do not change generator behavior.
  - Do not use fast lane for: behavior changes, workflow-stage changes, skill-triggering changes, architecture changes, security-sensitive behavior, CI behavior changes, release packaging, schemas, generated-output logic, or changes that are hard to roll back safely.
  - Fast-lane evidence: record a spec with intent, expected change, out of scope, and validation in the PR body, issue comment, commit message, or a linked change note.
- Use the full lifecycle for non-trivial work.
  - Required for behavior changes, workflow-stage changes, CI behavior changes, schema changes, architecture changes, and generated-output logic.

## Full Lifecycle

`constitution / project-map when needed -> explore -> research when needed -> proposal -> proposal-review -> spec -> spec-review -> architecture -> architecture-review when needed -> plan -> plan-review -> test-spec -> implement -> code-review -> verify -> ci when GitHub workflow automation for a material risk is missing or stale -> explain-change -> pr -> learn`

Notes:

- `ci` means creating or updating GitHub workflows or related automation for a material risk. It does not mean waiting for routine CI to run.
- Not every stage is required for every change; stage classification and enforcement rules are defined in `specs/rigorloop-workflow.md`.

## Planned Milestone Work

- Use a concrete plan under `docs/plans/` for multi-file, risky, ambiguous, migration-heavy, or milestone-based work.
- `docs/plan.md` is the lifecycle index for planned initiatives; concrete plan bodies live under `docs/plans/`.
- During execution, `implement` keeps the active plan body's progress, decisions, discoveries, and validation notes current.
- When a planned initiative changes lifecycle state, final lifecycle closeout updates both `docs/plan.md` and the plan body.
- `verify` blocks PR readiness when stale lifecycle state remains between the plan index and the plan body.
- Execution plans follow `docs/plans/0000-00-00-example-plan.md`.
- Each completed planned milestone ends with a coherent commit using:
  - `M<n>: <completed milestone outcome>`
- A pull request may contain one or more completed milestone commits when that is the clearest review boundary.

## Artifact Lifecycle

Lifecycle-managed top-level artifacts keep their own tracked status. Do not treat PR state, branch state, or chat-only review outcomes as a replacement for artifact-local lifecycle state.

| Artifact | Settlement states | Closeout or terminal states |
| --- | --- | --- |
| Proposal | `accepted` | `rejected`, `abandoned`, `superseded`, `archived` |
| Spec | `approved` | `abandoned`, `superseded`, `archived` |
| Architecture | `approved` | `abandoned`, `superseded`, `archived` |
| Test spec | `active` | `abandoned`, `superseded`, `archived` |
| ADR | `Accepted` | `Superseded`, `Archived` |

Notes:

- `reviewed` is transitional review output, not a durable relied-on state for proposals, top-level specs, test specs, or architecture docs.
- `accepted`, `approved`, `active`, and `Accepted` are settlement states. `done`, `rejected`, `abandoned`, `superseded`, and `archived` are closeout or terminal states.
- Keep `Next artifacts` as planning history while an artifact is active. Use `Follow-on artifacts` or `Closeout` for actual downstream artifacts or final disposition. If a `Follow-on artifacts` section appears before real follow-ons exist, it must say `None yet`.
- `superseded` artifacts must identify their replacement with `superseded_by` or equivalent labeled text. `archived` artifacts do not require a replacement pointer.
- `verify` blocks on stale lifecycle-managed artifacts that are touched, referenced, generated, or authoritative for the changed area, and it warns on unrelated stale baseline artifacts.
- Draft PR-body references participate in `verify` only when draft PR text already exists. Before that, `verify` uses `docs/changes/<change-id>/change.yaml`, explain-change artifacts, the active plan, and other touched or referenced authoritative artifacts.

## Source Of Truth

- Edit canonical workflow content in:
  - `docs/`
  - `specs/`
  - `skills/`
  - `schemas/`
  - `scripts/`
- Do not hand-edit generated Codex compatibility output in:
  - `.codex/skills/`
- Use `docs/plans/0000-00-00-example-plan.md` for plan structure. Do not reintroduce a second plan-template path.

## Validation

Run these first-release structural checks before PR:

- `python scripts/validate-skills.py`
- `python scripts/test-skill-validator.py`
- `python scripts/build-skills.py --check`

Use `bash scripts/ci.sh` to run the same checks through the repository-owned CI wrapper and report the commands you actually ran.

## CI And Release

- `.github/workflows/ci.yml` should remain a thin wrapper around repo-owned validation commands. It may set up required tooling, but validation logic belongs in `scripts/ci.sh`.
- Current release automation remains conservative and tag-driven. Do not treat `scripts/release-verify.sh` as a mature release gate until repository-specific checks replace the template behavior.

## Documentation Ownership

- `README.md`: public project overview
- `docs/workflows.md`: operational workflow summary
- `docs/plan.md`: index of active, blocked, done, and superseded plans
- `docs/plans/*.md`: concrete execution plans
- `specs/*.md`: normative behavior contract
- `specs/*.test.md`: contract-to-test mapping
