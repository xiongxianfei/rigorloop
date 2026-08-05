# Test Specification Review R5

Review ID: test-spec-review-r5
Stage: test-spec-review
Round: 5
Reviewer: independent Codex test-spec-review peer
Target: `specs/boundary-first-v1-v0-3-7-activation-release.test.md`
Target revision: `69e2cc8346b24af85d978f937c0a1f89c928783e`
Status: changes-requested
Review status: changes-requested
Material findings: BFA-TSR5-001, BFA-TSR5-002
Immediate next stage: test-spec revision
Implementation handoff: not-allowed

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Recording status: recorded
- Recording blocker: none
- Upstream revision required: no
- Open blockers: BFA-TSR5-001, BFA-TSR5-002

## Material Findings

### Finding BFA-TSR5-001

Finding ID: BFA-TSR5-001
Severity: major
Location: PRF-003, PRF-004, PRF-010, PRF-012
Evidence: Identity rows claim actual candidate and R-to-C evidence without
CMD13; composition rows claim readiness and T16 sibling selection without
CMD14 or T16's CMD4/CMD8/CMD11/CMD12 and owning milestone evidence.
Required outcome: Every proof row cites the commands and stage-owned evidence
that directly produce its claims.
Safe resolution path: Add CMD13 to PRF-003/010; add CMD14 plus exact T16
selector commands and M1-M3 evidence to PRF-004; add T16 commands/evidence to
PRF-012; recheck producer chains.
needs-decision rationale: none; proof ownership is already defined.

### Finding BFA-TSR5-002

Finding ID: BFA-TSR5-002
Severity: major
Location: BFA-R034 coverage; T6; T12; MP1
Evidence: T6 injects private sentinels only through candidate CMD1. T12 and MP1
claim privacy-safe readiness, checkpoint, and atomic evidence without direct
sentinel injection through the M2 serializer boundary.
Required outcome: Readiness diagnostics and checkpoint/atomic serializers
receive direct privacy-negative proof.
Safe resolution path: Extend T12 with CMD5 partitions covering persisted
evidence, readiness failures, runtime identity/environment, paths, and remote
diagnostics; assert stdout, stderr, checkpoint, and atomic serialization omit
raw sentinels; map BFA-R034 to T12 and MP1.
needs-decision rationale: none; this is direct proof completeness.

## Coverage Assessment

R/C/H separability, T..R versus T..H, phase commands, exact-H race,
same-invocation binding, milestone mapping, and manual/automation boundaries
pass. Direct producer-chain traceability and readiness/publication privacy proof block.

## Validation Evidence

- Boundary-first validation of the test spec passed.
- `git diff --check d28cbc07..69e2cc83` passed.
- Change metadata validation passed.
- Planned M2 commands were not run because implementation does not yet exist.

## Recommendation

Correct the two proof-map gaps and perform test-spec-review R6 before implementation.
