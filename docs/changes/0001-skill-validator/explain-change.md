# 0001 Skill Validator Explain Change

## Why this package exists

The first release needed one concrete non-trivial change that shows the full lifecycle from approved direction through validation evidence. The repository already shipped the validator across M2-M5, but contributors still needed one local artifact pack that tied those pieces together.

## What changed in M6

- added `docs/changes/0001-skill-validator/` as the durable change-local artifact home
- added `change.yaml` as the machine-readable traceability index for this example
- updated `README.md` so contributors can find the example from the project entrypoint
- updated the active plan so M6 records the artifact-pack milestone and its validation evidence

## Why each area matters

- `proposal.md`, `spec.md`, `plan.md`, and `test-spec.md` summarize the approved top-level artifacts without replacing them
- `verify-report.md` records the exact commands and results reviewers can trust
- `change.yaml` lets tools and reviewers inspect artifact links, requirements, tests, validation, changed files, and review state without parsing every Markdown artifact

## Review-resolution note

No standalone `review-resolution.md` is included for this example because there is no durable review feedback specific to the M6 artifact pack yet.
