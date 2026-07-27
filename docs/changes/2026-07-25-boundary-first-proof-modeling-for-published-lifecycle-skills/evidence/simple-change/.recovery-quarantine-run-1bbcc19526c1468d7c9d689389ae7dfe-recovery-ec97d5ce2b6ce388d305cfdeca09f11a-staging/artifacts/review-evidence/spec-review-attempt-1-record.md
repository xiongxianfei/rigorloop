# Portable text normalizer spec review

Review ID: spec-review-r1
Stage: spec-review
Status: changes-requested
Reviewed artifact identity: sha256:c96de1db87b1bc0f2b23646105486b8ab4dbff653720fef6ac81d5a2fb36c587
Material findings: finding.acceptance.byte-equivalence
Recording status: recorded

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: finding.acceptance.byte-equivalence
- Recording status: recorded
- Recording blocker: none
- Review record: reviews/spec-review.md
- Review log: review-log/spec-review.md
- Review resolution: review-resolution/spec-review.md
- Open blockers: finding.acceptance.byte-equivalence
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: Revise the R3 acceptance criterion to remove the representation-level requirement, then perform a same-stage review.

## Review dimensions

| Review dimension | Verdict |
| --- | --- |
| requirement clarity | pass |
| normative language | pass |
| completeness | pass |
| testability | pass |
| examples | pass |
| compatibility | pass |
| observability | pass |
| security/privacy | pass |
| non-goals | pass |
| acceptance criteria | concern |

## Boundary-first review

Boundary model version v1 and scope R1-R4 are present. Every core dimension is classified exactly once; applicable boundaries have requirement owners; the extension is valid; examples are classified and correctly linked; and both selected interactions represent requirement-owned composition hazards. The record satisfies the boundary-first structural and semantic gate.

## Findings

## Finding finding.acceptance.byte-equivalence

- Finding ID: finding.acceptance.byte-equivalence
- Severity: major
- Location: Acceptance criteria, R3 row
- Evidence: R3 requires the input text to be returned unchanged, but its acceptance criterion requires a “byte-for-byte” result. Byte equivalence introduces a representation-level contract not owned by R3 and conflicts with the explicit non-goal excluding input-shape and transport requirements.
- Required outcome: Make the R3 acceptance criterion test unchanged text without imposing byte representation behavior.
- Safe resolution path: Replace the R3 criterion with: “Tests demonstrate that `preserve` returns the input text unchanged.”
- needs-decision rationale: none

No automatic downstream handoff is authorized. The finding is recorded before revision and does not require an owner decision.