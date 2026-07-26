# Boundary-First Proof Modeling Test-Spec Review R3

Review ID: test-spec-review-r3
Stage: test-spec-review
Round: 3
Reviewer: Codex test-spec-review skill with context-separated reviewer
Target: commit `4c8c62ae` against `8ad995de`
Reviewed artifact: specs/rigorloop-workflow.test.md; specs/skill-contract.test.md
Status: changes-requested
Review status: changes-requested
Material findings: BFP-TSR3-1
Immediate next stage: test-spec revision
Implementation handoff: not-allowed
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Initial packet inventory: exact test-spec diff; approved R13 specs; accepted R4 architecture/ADR; approved R5 plan and review
Manifest owner: workflow orchestrator

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: BFP-TSR3-1
- Recording status: recorded
- Recording blocker: none
- Immediate next stage: test-spec revision
- Implementation handoff: not-allowed

## Finding

### BFP-TSR3-1 - Hermetic input-closure negative proof is not field-complete

Finding ID: BFP-TSR3-1
Severity: major
Location: `specs/rigorloop-workflow.test.md` T48-T50 and related R28y coverage

Evidence:

- The invocation profile, contract references, instruction walk, baseline, and
  input set are named as aggregate classes.
- The proof map does not explicitly mutate all nine invocation-profile fields,
  all five contract references, instruction ordering/deduplication/symlink
  behavior, every input-set field and scenario/oracle member, or the exact
  baseline record.

Required outcome:

Every closed manifest, instruction, contract, invocation-profile, baseline,
and input-set boundary maps to explicit positive and negative proof.

Safe resolution:

Expand T48-T50 with a field-exact mutation matrix covering the omitted cases
while retaining current command and milestone ownership.

## Confirmed Adequate

- Upstream identities and plan revision are current.
- M2 includes controlled-fixture and baseline commands.
- Parent-observed sandboxing, private authentication, validator-environment
  independence, publication crash points, and changed/unchanged identities are
  otherwise represented.
- M3 covers 40 pairs and zero upstream reinvocation.
- M4 names exact parity, report, release paths, commands, and non-publishing
  boundaries.
- M1-M4 gates and command classifications are coherent.

## Handoff

- Immediate next stage: test-spec revision
- Implementation handoff: not-allowed
- Owner decision needed: no
