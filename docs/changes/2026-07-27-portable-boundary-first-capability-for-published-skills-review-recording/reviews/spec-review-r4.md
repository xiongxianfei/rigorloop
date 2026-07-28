# Boundary-First Proof Model Spec Review R4

Review ID: spec-review-r4
Stage: spec-review
Round: 4
Reviewer: Independent contract rereview
Target: specs/boundary-first-proof-model.md
Status: changes-requested
Material findings: PBF-SR9
Architecture assessment: required after spec revision
Immediate next stage: spec revision
Eventual test-spec readiness: not-ready

## Result

PBF-SR4, PBF-SR5, PBF-SR7, and PBF-SR8 are resolved. PBF-SR6 is
partially resolved because the activation-time capture rule lacks an immutable
pre-activation baseline.

The contract otherwise preserves one reviewed activation manifest, existing
adapter metadata, read-only rollback validation, operator-owned external
actions, and no writer, receipt, transaction, or attestation machinery.

## Finding PBF-SR9

Finding ID: PBF-SR9
Severity: major
Location: specs/boundary-first-proof-model.md, Example E4 and PBF-R005c
Evidence: PBF-R005c captures qualifying specs inside the activating change, so
a newly introduced unmarked spec could be accepted and grandfathered by that
same change even though Example E4 limits grandfathering to specs that predate
activation.
Required outcome: derive grandfathered membership from a named immutable
pre-activation baseline and exclude paths first introduced by the activating
change.
Safe resolution path: use the parent revision of the activating reviewed
change as the inventory baseline.
needs-decision rationale: none

## Review Dimensions

| Review dimension | Verdict |
| --- | --- |
| requirement clarity | block |
| normative language | concern |
| completeness | block |
| testability | block |
| examples | concern |
| compatibility | block |
| observability | pass |
| security/privacy | pass |
| non-goals | pass |
| acceptance criteria | block |

## Recommendation

Close the temporal baseline in PBF-R005c and repeat spec review.
