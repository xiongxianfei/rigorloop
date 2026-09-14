# AGENTS.md

## Start here

Read [CONSTITUTION.md](CONSTITUTION.md) for authority, quality, review, permissions and cleanup rules.
Use [System](docs/design/system.md) to find the relevant owning Design; read only the models and retained contracts needed for the task.
Before implementation, read the governing contract, applicable architecture decisions, owning plan and verification allocation, then the files to change.
Use [docs/project-map.md](docs/project-map.md) only when current for the area; otherwise inspect the sources directly and state the map limitation or refresh it.

## Workflow

- Use `rigorloop workflow-context` for project-local workflow facts and `route` for semantic routing. The local executable is `node packages/rigorloop/dist/bin/rigorloop.js`.
- Follow [Workflow](docs/design/skill/workflow.md) and [Assessment](docs/design/skill/assessment.md) for progression, ownership and review gates.
- Read `docs/plan.md` as navigation; concrete plans live under `docs/plans/`, and mutable state belongs to the owning `docs/changes/<change-id>/change.json` and its registered records.
- Use scoped CLI reads, subject inspection and targeted recording under [CLI](docs/design/cli/cli.md) and [Records](docs/design/cli/records.md). Do not routinely reconstruct record stores or resume retired formats.
- Use `bugfix` for defects, `ci-maintenance` for CI configuration changes and `pr` for a ready external handoff. Individual skill requests stay isolated unless broader progression is authorized.

## Editing conventions

- Make the smallest complete change, preserve user work and avoid unrelated refactors.
- Follow [System's directory layout](docs/design/system.md#repository-directory-layout); preserve stable model IDs and declared example ownership.
- Edit canonical sources in `docs/`, `specs/`, `skills/`, `schemas/`, `scripts/` and `templates/`; `skills/` is the only authored skill source.
- Keep architecture and ADR scaffolds in `templates/`. Use `skills/plan/assets/plan-skeleton.md` for plans; do not create duplicate scaffolds or overwrite an unrelated initiative's plan.
- Do not hand-edit generated adapter output. Keep local `.codex/skills/` untracked; use [adapter guidance](dist/adapters/README.md) and [Packaging](docs/design/engineering/packaging.md).
- Treat published skills as user-facing: keep repository-maintainer mechanics out of their instructions. Add a skill only for a distinct recurring responsibility, artifact, gate or operational process.
- Edit `VISION.md` for project vision; README content between the vision markers is generated from it.
- Closed-vocabulary validators must reject unknown values before consistency checks, unless intentional fall-through is documented. Add an unknown-value regression test for each new closed vocabulary.
- Use Git history for retired material under the Constitution's [cleanup policy](CONSTITUTION.md#repository-cleanup-and-historical-retention); reconcile live dependencies before deleting files.

## Validation and handoff

Follow [CONTRIBUTING.md](CONTRIBUTING.md#validation-scope), the owning plan and [Validation](docs/design/engineering/validation.md).
Reuse existing commands; start with the smallest relevant checks and complete the required scope before claiming readiness.

```bash
bash scripts/ci.sh --mode local
bash scripts/ci.sh --mode explicit --path PATH
```

For packaging or release work, follow the owning [Packaging](docs/design/engineering/packaging.md) and [Release](docs/design/engineering/release.md) checks, including tracked release notes and actual candidate evidence.
Report what changed, commands actually run, results and material limitations; reconcile governed records when applicable.
