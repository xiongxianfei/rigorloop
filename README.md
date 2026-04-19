# RigorLoop

RigorLoop is an open-source AI engineering workflow for building software with explicit proposals, specs, architecture, plans, tests, review gates, verification, and explainable change history.

It is a Git-first starter kit. It does not replace pull requests, CI, or human review. It makes the path from idea to reviewed change explicit and auditable.

## What This Repository Contains

- a fast lane for trivial or low-risk work
- a full lifecycle for non-trivial work
- canonical workflow sources in `docs/`, `specs/`, `skills/`, `schemas/`, and `scripts/`
- generated Codex compatibility output in `.codex/skills/`
- a change-local artifact pattern under `docs/changes/<change-id>/` for the golden-path example and later non-trivial work

## Workflow At A Glance

Non-trivial work follows the reference lifecycle:

`constitution / project-map when needed -> explore -> research when needed -> proposal -> proposal-review -> spec -> spec-review -> architecture -> architecture-review when needed -> plan -> plan-review -> test-spec -> implement -> code-review -> verify -> ci when GitHub workflow automation for a material risk is missing or stale -> explain-change -> pr -> learn`

Trivial work may use the fast lane:

`spec -> implement -> verify -> pr`

Use the fast lane only for:

- typos
- formatting-only changes
- small documentation clarifications
- comment-only changes
- small test-fixture corrections
- small non-behavioral renames
- minor generated-artifact refreshes that do not change generator behavior

Do not use the fast lane for:

- public behavior changes
- workflow order or stage-policy changes
- skill triggering rules
- architecture changes
- security-sensitive behavior
- CI behavior changes
- release packaging changes
- schema changes
- generated-output logic changes
- changes that are hard to roll back safely

Fast-lane evidence must include a spec with:

- intent
- expected change
- out of scope
- validation

That spec may live in the PR body, issue comment, commit message, or a linked change note.

The normative contract lives in `specs/rigorloop-workflow.md`. The short operational summary lives in `docs/workflows.md`.

## Source Of Truth

- Edit canonical workflow content in:
  - `docs/`
  - `specs/`
  - `skills/`
  - `schemas/`
  - `scripts/`
- Do not hand-edit generated Codex compatibility output in:
  - `.codex/skills/`
- Execution plans follow:
  - `docs/plans/0000-00-00-example-plan.md`

## Validation Commands

Before PR, run the same structural checks that CI runs:

- `python scripts/validate-skills.py`
- `python scripts/test-skill-validator.py`
- `python scripts/build-skills.py --check`

Use `bash scripts/ci.sh` to run the same checks through the repository-owned CI wrapper.

## Current Focus

The first proof-of-value change is a skill metadata validator with fixture tests, generated-output drift checks, and CI integration.

The shipped golden-path example for that change lives in:

- `docs/changes/0001-skill-validator/`

Active implementation work is tracked in:

- `docs/plans/2026-04-19-rigorloop-first-release-implementation.md`
- `specs/rigorloop-workflow.test.md`

## Repository Layout

```text
.
├── AGENTS.md
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── pull_request_template.md
│   └── workflows/
├── docs/
│   ├── plan.md
│   ├── proposals/
│   ├── roadmap.md
│   ├── workflows.md
│   ├── changes/
│   │   └── 0001-skill-validator/
│   ├── plans/
│   │   └── 0000-00-00-example-plan.md
│   ├── architecture/
│   └── adr/
├── .codex/
│   └── skills/
├── scripts/
├── skills/
├── schemas/
└── specs/
```

The first shipped change-local artifact pack is `docs/changes/0001-skill-validator/`.

## License

This repository currently ships with the MIT license.
