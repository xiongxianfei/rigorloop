# Architecture Method Test-Spec Authoring

- Artifact ID: `test-spec-architecture-package-method`
- Artifact path: `specs/architecture-package-method.test.md`
- Authoring stage: `test-spec`
- Completion status: `complete`
- Resulting review-request path: `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/test-spec-review-architecture-method-r1.md`

## Scope

Update the existing R8 proof wording so T2, T5, and the compatibility fixture
distinguish stable owning-change-record metadata from mutable lifecycle status.
No test case, command, scenario, or coverage target is added or removed.

T2, T5, and the compatibility fixture now assert stable owner metadata and
change-local mutable lifecycle state without altering their coverage IDs.
The revised legacy test spec now carries one stable pointer to this owning
change record instead of embedded mutable status.

`APM-SR1-001` also requires the existing ADR proof wording to distinguish new
governed owner pointers from unmigrated historical embedded status.

T7 and its coverage row now prove exact owner-entry state for new governed
ADRs, absence of duplicated mutable status in the template, and explicit
legacy compatibility without adding a new test case.

Test-spec-review finding `APM-TSR1-001` reopens authoring for three exact
traceability summaries; proof scope and IDs remain unchanged.

The R7-R20 and AC7 coverage rows plus T12 now state stable owner pointers,
exact matching owner-entry state, absence of duplicated mutable status, and
unmigrated legacy embedded-status compatibility. No proof identity or scope
changed.
