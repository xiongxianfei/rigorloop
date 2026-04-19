# 0001 Skill Validator Spec

## Normative sources

- Workflow spec: `../../../specs/rigorloop-workflow.md`
- Repository architecture: `../../architecture/2026-04-19-rigorloop-first-release-repository-architecture.md`
- Source-layout ADR: `../../adr/ADR-20260419-repository-source-layout.md`

## Delivered contract in this change

1. `python scripts/validate-skills.py` validates canonical `skills/` using the first-release rule set from `R15` and `R15a`.
2. `python scripts/test-skill-validator.py` exercises the valid and invalid fixtures required by `R16`.
3. `python scripts/build-skills.py --check` fails when generated `.codex/skills/` drifts from canonical `skills/`.
4. `bash scripts/ci.sh` and `.github/workflows/ci.yml` run the structural checks required by `R18` and `R19`.
5. `docs/changes/0001-skill-validator/` provides the first change-local artifact pack and `change.yaml` required by `R13`, `R14`, and `R25`.

## Source-of-truth boundaries

- Canonical authored skill content lives in `skills/`.
- Generated Codex compatibility output lives in `.codex/skills/` and must not be hand-edited.
- Machine-readable traceability for this non-trivial change lives in `docs/changes/0001-skill-validator/change.yaml`.

## Out of scope

- alternative metadata formats
- networked validation
- non-Codex adapter generation
- subjective scoring or linting beyond the approved structural rules
