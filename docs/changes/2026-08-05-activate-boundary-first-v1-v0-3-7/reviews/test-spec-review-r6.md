# Test Specification Review R6

Review ID: test-spec-review-r6
Stage: test-spec-review
Round: 6
Reviewer: independent Codex test-spec-review peer
Target: `specs/boundary-first-v1-v0-3-7-activation-release.test.md`
Target revision: `0ac4ffec7c3e2e46fec400c8e61e19424868e172`
Status: changes-requested
Review status: changes-requested
Material findings: BFA-TSR6-001, BFA-TSR6-002
Immediate next stage: test-spec revision
Implementation handoff: not-allowed

## Result

- Skill: test-spec-review
- Recording status: recorded
- Recording blocker: none
- `BFA-TSR5-001`: initial named rows corrected; residual overclaims are BFA-TSR6-001.
- `BFA-TSR5-002`: sentinel partitions corrected; residual M2 ownership is BFA-TSR6-002.

## Material Findings

### Finding BFA-TSR6-001

Finding ID: BFA-TSR6-001
Severity: major
Location: PRF-004, PRF-012
Evidence: PRF-004 claims atomic and public npm evidence without producing
CMD17/CMD18. PRF-012 claims public npm evidence without CMD18 and the full MP1
publication path without CMD17.
Required outcome: Claimed atomic/public evidence has its direct producing commands.
Safe resolution path: Add CMD17 and CMD18 to both rows.
needs-decision rationale: none.

### Finding BFA-TSR6-002

Finding ID: BFA-TSR6-002
Severity: major
Location: T12 evidence and milestone ownership; M2 proof map; security/privacy summary
Evidence: T12 now executes CMD5 privacy partitions, but omits M2 as a required
milestone and `evidence/implementation-m2.md`. The summary still names only
T6, T9, and T13.
Required outcome: Record fixture serializer proof at M2 and actual evidence
privacy proof at MP1 with complete summary traceability.
Safe resolution path: Add M2 implementation evidence and milestone ownership
to T12, include T12 in the M2 proof map, and cite T12/MP1 in the privacy summary.
needs-decision rationale: none.

## Validation Evidence

- Boundary-first validation of the test spec passed.
- Target diff whitespace and change metadata validation passed.

## Recommendation

Apply the four exact traceability corrections and perform test-spec-review R7.
