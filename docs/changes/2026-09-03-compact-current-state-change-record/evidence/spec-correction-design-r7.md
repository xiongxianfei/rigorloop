# Design Review R7 specification correction

Authoring result: complete

Artifact path: specs/compact-current-state-change-record.md
Prior artifact identity: sha256:f5d5cb43a06369e852a5486871bfd831becf22dfdab04b87b22cec8d615e0c14
Artifact identity: sha256:941e9e21ace58a5a33fce458cc8b6df71c2048b03a85c3c9014e2b4ba206119f
Finding IDs: CCSR-DR7-1, CCSR-DR7-2
Evidence state: complete

The specification now keeps an explicit correction active from route through return and required review settlement. `ActiveCorrection` records its return stage and phase; return changes `authoring` to `review-required`, and only an exact approving settlement with valid finding dispositions clears it. Non-approved settlement retains or coherently revises the correction.

Projection input now accepts one optional exact requested operation for every bounded view and binds its presence or absence to the two operation-eligibility output fields.

## Validation

- `python scripts/validate-boundary-first.py --check --path specs/compact-current-state-change-record.md`: passed.
- `python scripts/validate-documentation-prose.py --mode enforce --path specs/compact-current-state-change-record.md`: passed with zero errors and warnings.
- `python scripts/validate-markdown-readability.py specs/compact-current-state-change-record.md`: passed with advisory long-line warnings.
- `git diff --check`: passed.

## Handoff

The corrected specification is ready for the required exact-package Design Review. This evidence does not claim review approval or progression readiness.
