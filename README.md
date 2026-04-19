# RigorLoop

RigorLoop is an open-source AI engineering workflow for building software with explicit proposals, specs, architecture, plans, tests, review gates, verification, and explainable change history.

It is a Git-first starter kit. It does not replace pull requests, CI, or human review. It makes the path from idea to reviewed change explicit and auditable.

## What This Repository Contains

- a fast lane for trivial or low-risk work
- a full lifecycle for non-trivial work
- canonical workflow sources in `docs/`, `specs/`, `skills/`, `schemas/`, and `scripts/`
- generated Codex compatibility output in `.codex/skills/`
- change-local artifacts and machine-readable traceability under `docs/changes/<change-id>/`

## Workflow At A Glance

Non-trivial work follows the reference lifecycle:

`constitution / project-map when needed -> explore -> research when needed -> proposal -> proposal-review -> spec -> spec-review -> architecture -> architecture-review when needed -> plan -> plan-review -> test-spec -> implement -> code-review -> verify -> ci when GitHub workflow automation for a material risk is missing or stale -> explain-change -> pr -> learn`

Trivial work may use the fast lane:

`spec -> implement -> verify -> pr`

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

## Current Focus

The first proof-of-value change is a skill metadata validator with fixture tests, generated-output drift checks, and CI integration.

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
│   ├── plans/
│   │   └── 0000-00-00-example-plan.md
│   ├── architecture/
│   ├── adr/
│   └── changes/
├── .codex/
│   └── skills/
├── scripts/
├── skills/
├── schemas/
└── specs/
```

## License

This repository currently ships with the MIT license.
