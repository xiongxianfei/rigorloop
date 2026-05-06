# Explain Change

## Summary

This change optimizes the `vision` skill so it identifies strategic project positioning before drafting or materially repositioning `VISION.md`. It also retires active lowercase `vision.md` migration behavior from user-facing guidance and repository validation.

## Positioning Delta

The current branch re-centers RigorLoop from a lower-level "Git-first starter kit" framing to a rigorous software engineering workflow for AI coding agents. Git, CI, pull requests, and repository-local artifacts remain important compatibility surfaces, but they are no longer the project category.

The durable rationale is recorded in [Strategic Positioning](../../vision/strategic-positioning.md). `VISION.md` remains the canonical public-facing project vision; the positioning rationale supports review and future proposal-fit decisions without independently overriding `VISION.md`.

## Why The Files Changed

- `specs/vision-skill.md` defines the approved strategic-positioning contract, 750/900-word policy, durable rationale path, anti-anchor rule, methodology-as-product behavior, final quality gates, and retired lowercase path behavior.
- `specs/vision-skill.test.md` maps the approved requirements and acceptance criteria to concrete proof surfaces before implementation.
- `skills/vision/SKILL.md` now instructs agents to perform the strategic-positioning pass, write rationale when required, avoid substrate anchoring, and stop treating retired root `vision.md` as migration input.
- `skills/proposal/SKILL.md` and `skills/proposal-review/SKILL.md` now anchor `Vision fit` behavior to root `VISION.md` without preserving migration-recognized lowercase exceptions.
- `scripts/test-skill-validator.py`, `scripts/test-select-validation.py`, and `scripts/validation_selection.py` enforce the active contract through static assertions and selector routing.
- `docs/vision/strategic-positioning.md` records the rationale for the current material project-vision repositioning.
- `docs/plan.md`, the active plan, and this change-local pack track lifecycle state, validation evidence, and review closeout.

## Validation

Validation evidence is recorded in `change.yaml` and the active plan. The implementation uses focused skill-validator tests, selector tests, explicit selector probes, selected CI, change metadata validation, artifact lifecycle validation, and whitespace checks.
