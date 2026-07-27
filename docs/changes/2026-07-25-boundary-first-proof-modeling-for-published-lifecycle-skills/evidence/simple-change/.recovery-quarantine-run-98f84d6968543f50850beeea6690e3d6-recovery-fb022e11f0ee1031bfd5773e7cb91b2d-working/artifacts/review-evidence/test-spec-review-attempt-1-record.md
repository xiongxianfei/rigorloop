# Portable text normalizer test specification review

Review ID: test-spec-review-r1
Stage: test-spec-review
Status: changes-requested
Reviewed artifact identity: sha256:a0b1f0d4b39896403ba058f01c8c350a52d66d251b39c21319ac9c1d6b0b2a35
Material findings: finding.unicode-boundary-proof
Recording status: recorded

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: finding.unicode-boundary-proof
- Recording status: recorded
- Recording blocker: none
- Review record: reviews/test-spec-review.md
- Review log: review-log/test-spec-review.md
- Review resolution: review-resolution/test-spec-review.md
- Open blockers: finding.unicode-boundary-proof
- Immediate next stage: review-resolution
- Implementation handoff: not-allowed
- Stop condition: Revise and re-review the test specification before relying on its proof map.

## Review dimensions

| Review dimension | Verdict |
| --- | --- |
| Governing-contract alignment | pass |
| Requirement coverage | concern |
| Example coverage | pass |
| Negative and boundary coverage | block |
| Proof-level adequacy | concern |
| Milestone mapping | pass |
| Command validity | pass |
| Fixture and data design | concern |
| Manual-proof boundary | pass |
| Observability | pass |
| Determinism and isolation | pass |
| Scope and non-goals | pass |
| Execution economics | pass |
| Traceability | concern |
| Implementation handoff | block |

## Boundary-first review

Boundary model version v1 and scope R1-R4 match the approved feature record. The proof map cites every defined applicable boundary and the selected interaction with exact IDs. Proof for `boundary.unicode-whitespace`, however, is incomplete: T2 and T3 exercise only a fixed positive list and do not distinguish the authoritative Unicode `White_Space` property from a substituted or overbroad classifier. The canonical-trust boundary therefore lacks direct proof against conflicting classification, and the claim of exhaustive boundary handling is broader than the specified evidence.

## Findings

## Finding finding.unicode-boundary-proof

- Finding ID: finding.unicode-boundary-proof
- Severity: material
- Location: Testing strategy; proof.unicode-whitespace; T2; T3; Fixtures and data
- Evidence: T2 hard-codes the 25 positive `White_Space` code points and T3 checks those code points internally, but no test supplies boundary code points outside that property, including adjacent or confusable non-members. An implementation that trims all listed members plus additional non-members could pass. The fixture also does not state how its hard-coded membership remains tied to the authoritative Unicode property while claiming exhaustive handling.
- Required outcome: Add direct automated proof that `trim` retains representative boundary non-members chosen to expose substituted or overbroad whitespace classification, and state a deterministic basis that ties the positive membership fixture to the Unicode `White_Space` property without adding a new product requirement.
- Safe resolution path: Revise the existing `boundary.unicode-whitespace` proof and test cases to include positive property members and targeted negative boundary non-members, identify the fixture's Unicode property source or generated-data basis as test evidence, update affected coverage text, and submit the revised test specification for a new review round.
- needs-decision rationale: none
