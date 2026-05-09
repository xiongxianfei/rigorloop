# Single Source of Workflow State Change Rationale

## Status

- in progress

## Scope

This change implements the approved single-source workflow-state contract through milestone slices.

M1 adds the active test spec and focused validator proof that make later workflow, skill, generated-output, and closeout edits reviewable.

## M1 Rationale

- `specs/single-source-of-workflow-state.test.md` maps the approved spec requirements, examples, edge cases, and acceptance criteria to concrete proof surfaces before implementation continues.
- `scripts/test-skill-validator.py` now pins the single-source workflow-state spec, test spec, and plan scaffolding so later skill edits cannot drop the required proof contract, public portability requirement, or versioned adapter validation requirement.
- `scripts/test-artifact-lifecycle-validator.py` now proves active test specs may delegate live next-stage state to the active plan `Current Handoff Summary` and that stale `Ready for implement` wording remains blocked.
- The active plan and change metadata record M1 state and validation evidence without claiming review, final verification, branch readiness, or PR readiness.
- Code-review M1 R1 found and resolved `SSWS-CR1-F1`, a stale final-closeout reason inside `Current Handoff Summary`. After resolution, M1 closed and the active plan now hands off to M2.

## Validation Evidence

M1 validation is recorded in the active plan and `change.yaml`.

## Follow-on

- M1 code-review must review this milestone before M2 starts.
- M2-M5 will update this rationale as later milestone changes are implemented and verified.
