# RigorLoop

*Git-first starter kit for AI-assisted software delivery with explicit artifacts, review gates, and durable change history.*

RigorLoop helps individual contributors turn AI-assisted ideas into reviewable changes with proposals, specs, plans, tests, review gates, verification, and explainable change history. That gives contributors clearer review scope, explicit artifact history, and traceable change rationale from idea to PR. It also helps maintainers and small teams keep AI-assisted delivery explicit and auditable without replacing Git, pull requests, CI, or human review.

## When to use / When not to use

Use RigorLoop when:

- you want AI-assisted work to stay reviewable, traceable, and grounded in explicit proposals, specs, plans, tests, and verification
- you need a Git-first starter kit that leaves durable change history instead of burying decisions in chat
- you want a workflow that makes the path from idea to reviewed change visible and auditable

Do not use RigorLoop when:

- you want agents to bypass pull requests, CI, or human review
- you need a hosted orchestration platform or centralized control plane
- you want a zero-process scratchpad with no explicit artifacts or review gates

## Quick Start

1. Read the [short workflow summary](docs/workflows.md).
2. Read the [normative workflow contract](specs/rigorloop-workflow.md).
3. Inspect the [shipped proof-of-value example](docs/changes/0001-skill-validator/).
4. If the approach fits, start from the lifecycle artifacts under [docs/](docs/), [specs/](specs/), and [skills/](skills/).

## Adapter Packages

RigorLoop ships generated adapter packages for Codex, Claude Code, and opencode under `dist/adapters/`.

| Tool | Package root | Instruction entrypoint | Skill directory |
| --- | --- | --- | --- |
| Codex | `dist/adapters/codex/` | `AGENTS.md` | `.agents/skills/` |
| Claude Code | `dist/adapters/claude/` | `CLAUDE.md` | `.claude/skills/` |
| opencode | `dist/adapters/opencode/` | `AGENTS.md` | `.opencode/skills/` |

To install one adapter, copy that adapter package root's contents into a project root. The current support matrix is generated in `dist/adapters/manifest.yaml`; for `v0.1.0`, all current skills are included for Codex, Claude Code, and opencode.

Canonical skill edits happen in `skills/`. Adapter packages under `dist/adapters/` are generated release output, and `.codex/skills/` remains a separate generated local Codex runtime mirror for this repository.

Adapter compatibility claims are versioned. If external tool contracts change, update the affected adapter contract through the RigorLoop lifecycle before changing release claims.

Ordinary contributors do not need all supported tools installed locally to run non-smoke validation. Maintainer smoke for Codex, Claude Code, and opencode is recorded in `docs/releases/<version>/release.yaml` before a stable release.

## Learn More / Contribute

- Workflow detail: [docs/workflows.md](docs/workflows.md) and [specs/rigorloop-workflow.md](specs/rigorloop-workflow.md)
- Artifact and skill docs: [specs/README.md](specs/README.md) and [skills/](skills/)
- Report problems or feature ideas: [bug report template](.github/ISSUE_TEMPLATE/bug.yml) and [feature request template](.github/ISSUE_TEMPLATE/feature.yml)
- Review PR expectations before contributing: [.github/pull_request_template.md](.github/pull_request_template.md)

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

The normative contract lives in [specs/rigorloop-workflow.md](specs/rigorloop-workflow.md). The short operational summary lives in [docs/workflows.md](docs/workflows.md).

## What This Repository Contains

- a fast lane for trivial or low-risk work
- a full lifecycle for non-trivial work
- canonical workflow sources in `docs/`, `specs/`, `skills/`, `schemas/`, and `scripts/`
- generated Codex compatibility output in `.codex/skills/`
- generated public adapter packages in `dist/adapters/`
- a change-local artifact pattern under `docs/changes/<change-id>/` for the shipped example and later non-trivial work

## Change-Local Artifact Packs

- Fast-lane work may omit `docs/changes/<change-id>/` only when the approved fast-lane policy allows it.
- Ordinary non-trivial work uses the baseline pack: `docs/changes/<change-id>/change.yaml` plus `docs/changes/<change-id>/explain-change.md`.
- `review-resolution.md` and `verify-report.md` stay conditional and are added only when their governing workflow triggers apply.
- Approved legacy top-level explain artifacts under `docs/explain/` remain valid until migrated or retired.
- `docs/changes/0001-skill-validator/` is a rich reference example, not the minimum required pack for every non-trivial change.

## Source Of Truth

- Edit canonical workflow content in:
  - `docs/`
  - `specs/`
  - `skills/`
  - `schemas/`
  - `scripts/`
- Do not hand-edit generated Codex compatibility output in:
  - `.codex/skills/`
- Do not hand-edit generated public adapter packages in:
  - `dist/adapters/`
- Execution plans follow:
  - `docs/plans/0000-00-00-example-plan.md`

## Validation Commands

Before PR, run the same structural checks that CI runs:

- `python scripts/validate-skills.py`
- `python scripts/test-skill-validator.py`
- `python scripts/build-skills.py --check`
- `python scripts/build-adapters.py --version 0.1.0 --check`
- `python scripts/validate-adapters.py --version 0.1.0`
- `python scripts/validate-release.py --version v0.1.0`

Use `bash scripts/ci.sh` to run the same checks through the repository-owned CI wrapper.

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
├── dist/
│   └── adapters/
├── scripts/
├── skills/
├── schemas/
└── specs/
```

The first shipped change-local artifact pack is `docs/changes/0001-skill-validator/`, and it should be read as a rich example rather than the universal minimum pack for every non-trivial change.

## License

This repository currently ships with the MIT license.
