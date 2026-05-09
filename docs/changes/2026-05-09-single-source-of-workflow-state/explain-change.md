# Single Source of Workflow State Change Rationale

## Status

- current

## Scope

This change implements the approved single-source workflow-state contract for planned initiatives.

The core behavior is that the active plan `Current Handoff Summary` owns live state. Other artifacts keep scoped evidence, validation, review closeout, or rationale without becoming competing next-stage authorities.

## Rationale

### M1. Test Spec and Validator Coverage

- `specs/single-source-of-workflow-state.test.md` maps the approved spec requirements, examples, edge cases, and acceptance criteria to concrete proof surfaces before downstream implementation continues.
- `scripts/test-skill-validator.py` pins the required spec, test spec, plan scaffolding, public portability requirement, and versioned adapter validation requirement.
- `scripts/test-artifact-lifecycle-validator.py` proves active test specs may delegate live next-stage state to the active plan `Current Handoff Summary` and that stale readiness wording remains blocked.
- Code-review findings `SSWS-CR1-F1` and `SSWS-CR2-F1` were accepted and resolved before M1 closed.

### M2. Workflow and Governance Guidance

- `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, and the example plan were aligned so contributor-facing workflow guidance points to one live state owner.
- The updates preserve the existing workflow order while requiring state-sync before downstream readiness is claimed.
- `docs/plans/0000-00-00-example-plan.md` now models `Current Handoff Summary` as the live handoff block and keeps `Readiness` as a pointer instead of a duplicate next-stage owner.

### M3. Canonical Skill Contract Updates

- Canonical workflow-facing skills now describe the active plan `Current Handoff Summary` as the live state owner for planned initiatives.
- `implement` records state-sync before code-review handoff, `code-review` updates or requires current handoff updates before downstream handoff, and final evidence stages keep their scoped ownership boundaries.
- `verify`, `explain-change`, and `pr` skill wording avoids owning the active plan's current next stage.
- `scripts/test-skill-validator.py` includes static proof for the M3 skill guidance and stale wording removal.

### M4. Generated Output and Adapter Validation

- `.codex/skills/` was regenerated from canonical `skills/` sources.
- `dist/adapters/` was regenerated with `python scripts/build-adapters.py --version 0.1.1`.
- Generated skill drift, adapter drift, adapter validation, and adapter distribution tests passed after regeneration.
- The plan records that generated directories are validated through generator and adapter checks, while lifecycle validation remains scoped to authored plan/change artifacts.

### M5. Lifecycle Closeout Evidence

- M1-M4 are closed, all material review findings are resolved, and `review-resolution.md` reports `Closeout status: closed`.
- This rationale is the durable Markdown explanation for the change-local baseline pack.
- M5 keeps plan completion separate from implementation handoff. Final `verify`, PR handoff, and plan-index Done synchronization remain downstream lifecycle gates.

## Validation Evidence

Detailed command evidence is recorded in the active plan and `change.yaml`.

Important proof surfaces include:

- review artifact closeout validation for resolved material findings;
- lifecycle validation for the plan, change metadata, explain-change, spec, and test spec;
- generated skill drift checks;
- versioned adapter drift and adapter validation;
- adapter distribution tests;
- skill validator and artifact lifecycle validator tests;
- selected validation output for the touched M5 surfaces.

## Current Handoff

Use the active plan `Current Handoff Summary` for current live state. This rationale is scoped evidence and does not own final verification, branch readiness, PR readiness, or the active plan's current next stage.
