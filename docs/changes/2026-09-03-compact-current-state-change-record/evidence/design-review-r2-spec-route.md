# Design Review R2 Specification Correction Route

Change ID: 2026-09-03-compact-current-state-change-record

Source stage: design-review

Destination artifact: spec

Reason: upstream-contract-gap

Finding IDs: CCSR-DR2

Return stage: design-review

Lifecycle revision: sha256:b5223826025bf2d89c7a625e72a93ab899b2cb23554948c5837a12c7a03cb51b

The corrected specification still leaves nested record structures and the canonical lifecycle-revision manifest encoding ambiguous, preventing independent implementations from satisfying AC-11 consistently.

Return condition: Register a corrected specification that fully defines the v1 nested schemas and lifecycle-revision normalization, record an accepted finding resolution with current validation evidence, return the correction to Design Review, and review the resulting exact package as a new round.

Expected next review: design-review-r3
