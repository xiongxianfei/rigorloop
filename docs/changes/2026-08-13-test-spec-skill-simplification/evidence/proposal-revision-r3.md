# Proposal Revision R3 Evidence: Test-Spec Skill Simplification

Stage: proposal
Date: 2026-08-13
Artifact ID: `proposal`
Artifact: `docs/proposals/2026-08-13-test-spec-skill-simplification.md`
Completion status: complete
Review request: `docs/changes/2026-08-13-test-spec-skill-simplification/reviews/proposal-review-r4.md`

## Finding addressed

- `TSSIM-PR7`: Stale recovery now keeps the exact incomplete entry in `authoring`, preserves its artifact ID and canonical path, replaces only its authoring-evidence path, and binds a new retry identity. Workflow authorizes and routes recovery without mutating the entry. `test-spec` owns the restart evidence and same-entry content restart. Terminal abandonment, duplicate primary entries, and duplicate canonical paths are forbidden. Required partial bytes move to a distinct evidence path before same-path replacement.

## Revision result

The R3 finding is accepted and reflected in the proposal. The revised artifact is ready for independent proposal-review R4. This evidence does not claim approval or specification readiness.
