# Workflows

This file is the short operational summary for working in this repository. The normative workflow contract lives in `specs/rigorloop-workflow.md`.

## Choose A Lane

- Use the fast lane for trivial or low-risk work only.
  - Reference path: `spec -> implement -> verify -> pr`
- Use the full lifecycle for non-trivial work.
  - Required for behavior changes, workflow-stage changes, CI behavior changes, schema changes, architecture changes, and generated-output logic.

## Full Lifecycle

`constitution / project-map when needed -> explore -> research when needed -> proposal -> proposal-review -> spec -> spec-review -> architecture -> architecture-review when needed -> plan -> plan-review -> test-spec -> implement -> code-review -> verify -> ci when GitHub workflow automation for a material risk is missing or stale -> explain-change -> pr -> learn`

Notes:

- `ci` means creating or updating GitHub workflows or related automation for a material risk. It does not mean waiting for routine CI to run.
- Not every stage is required for every change; stage classification and enforcement rules are defined in `specs/rigorloop-workflow.md`.

## Planned Milestone Work

- Use a concrete plan under `docs/plans/` for multi-file, risky, ambiguous, migration-heavy, or milestone-based work.
- Execution plans follow `docs/plans/0000-00-00-example-plan.md`.
- Each completed planned milestone ends with a coherent commit using:
  - `M<n>: <completed milestone outcome>`
- A pull request may contain one or more completed milestone commits when that is the clearest review boundary.

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

- Until the first-release validation scripts are fully landed, use the exact validation commands named in the active plan and test spec.
- When repo-owned validation scripts are implemented, run the named repository commands before PR and report the commands you actually ran.
- Do not report success with implied or assumed checks.

## CI And Release

- `.github/workflows/ci.yml` should remain a thin wrapper around repo-owned validation commands.
- Current release automation remains conservative and tag-driven. Do not treat `scripts/release-verify.sh` as a mature release gate until repository-specific checks replace the template behavior.

## Documentation Ownership

- `README.md`: public project overview
- `docs/workflows.md`: operational workflow summary
- `docs/plan.md`: index of active, blocked, done, and superseded plans
- `docs/plans/*.md`: concrete execution plans
- `specs/*.md`: normative behavior contract
- `specs/*.test.md`: contract-to-test mapping
