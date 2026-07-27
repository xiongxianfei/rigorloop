# Portable text normalizer spec review

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: f.examples.serialization
- Recording status: recorded
- Recording blocker: none
- Review record: reviews/spec-review.md
- Review log: review-log/spec-review.md
- Review resolution: review-resolution/spec-review.md
- Open blockers: f.examples.serialization
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: The authored E1-E3 examples do not satisfy the boundary-first example serialization contract.

Review ID: spec-review-r1
Stage: spec-review
Status: changes-requested
Reviewed artifact identity: sha256:5f1a5d72d59b3777c1f39ccafa946a25b964cac3c62d768a8c2126ef69f2fefe
Material findings: f.examples.serialization
Recording status: recorded

## Review dimensions

| Review dimension | Verdict |
| --- | --- |
| requirement clarity | pass |
| normative language | pass |
| completeness | concern |
| testability | pass |
| examples | block |
| compatibility | pass |
| observability | pass |
| security/privacy | pass |
| non-goals | pass |
| acceptance criteria | pass |

## Findings

## Finding f.examples.serialization

- Finding ID: f.examples.serialization
- Severity: major
- Location: Examples first; boundary record `## Examples`
- Evidence: The prose examples are authored as `E1`, `E2`, and `E3`, which do not match the required dotted lowercase example-ID grammar. They are not themselves classified with one of the required roles; the boundary record instead contains separately identified examples whose relationship to E1-E3 is implicit.
- Required outcome: Give every authored example a valid stable ID and an explicit permitted role, with requirement and boundary links satisfying the boundary record rules.
- Safe resolution path: Replace E1-E3 with the already valid IDs `e.trim.whitespace`, `e.preserve.unchanged`, and `e.unknown.failure`, identify each as an illustration, and use those same identities in the boundary record without changing example behavior.
- needs-decision rationale: none

No automatic downstream handoff is authorized. The finding is recorded before revision and requires no owner decision.
