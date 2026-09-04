# Design refinement: scoped operation eligibility

Authoring result: complete

## Specification target

Artifact path: specs/compact-current-state-change-record.md
Artifact identity: sha256:f5d5cb43a06369e852a5486871bfd831becf22dfdab04b87b22cec8d615e0c14
Evidence state: complete

The specification now defines separate progression and operation diagnostics, exact requested-operation eligibility, and the invariant that global blockage cannot disable an otherwise eligible correction.

## Architecture target

Artifact path: docs/architecture/2026-09-03-compact-current-state-change-record.md
Artifact identity: sha256:6fcc1f504a10ab8150baff77b6e5c05e5f5afbba5466e29cf8b86743ab3b9760
Evidence state: complete

The projection service derives progression readiness and requested-operation eligibility independently from one normalized snapshot while preserving fail-closed operation checks.

## ADR target

Artifact path: docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md
Artifact identity: sha256:0aa7ef816b59de9e54d84cff699703205d10ddc55d8dcaf4931144e33c76c9f5
Evidence state: complete

The transaction-boundary decision now states that overall status is not an authorization primitive.

## Validation

- `python scripts/validate-boundary-first.py --check --path specs/compact-current-state-change-record.md`: passed.
- Documentation prose enforcement for all three targets: passed with zero errors and warnings.

## Handoff

The exact revised Design package requires fresh Design Review. This evidence does not claim approval.
