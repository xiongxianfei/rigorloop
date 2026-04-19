# 0001 Skill Validator Test Spec

## Source of truth

The normative test mapping lives in `../../../specs/rigorloop-workflow.test.md`.

## Relevant tests for this change

- `T5`-`T7`: `change.yaml` schema shape and metadata validation
- `T8`-`T10`: skill validator behavior against valid and invalid fixtures
- `T11`-`T12`: deterministic generation and generated-output drift detection
- `T13`-`T14`: repo-owned CI command surface and thin GitHub Actions wrapper
- `T15`: change-local artifact pack completeness and valid `change.yaml`
- `T17`-`T18`: local-only validation and contributor-actionable failures

## Core commands

- `bash scripts/ci.sh`
- `python scripts/validate-change-metadata.py docs/changes/0001-skill-validator/change.yaml`
