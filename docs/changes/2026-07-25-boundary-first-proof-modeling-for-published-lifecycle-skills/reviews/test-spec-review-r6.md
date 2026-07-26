# Boundary-First Proof Modeling Test-Spec Review R6

Review ID: test-spec-review-r6
Stage: test-spec-review
Round: 6
Reviewer: Codex test-spec-review skill with context-separated independent reviewer
Target: approved runtime-attestation proof map
Reviewed artifact: specs/rigorloop-workflow.test.md
Status: changes-requested
Review status: changes-requested
Material findings: BFP-TSR6-1, BFP-TSR6-2
Immediate next stage: test-spec revision
Implementation readiness: not-ready
Implementation handoff: not-allowed
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Initial packet inventory: exact T48-T50 candidate; approved spec-review R18; approved plan-review R11
Manifest owner: workflow orchestrator

## Findings

### BFP-TSR6-1 - Preflight envelope and recovery matrix are incomplete

Finding ID: BFP-TSR6-1
Severity: major

T49 lacks field-by-field five-field envelope mutations and exact
temporary/prior/restart recovery states.

Required outcome: Prove the exact preflight schema and every interrupted
publication branch.

### BFP-TSR6-2 - Fresh generation attestation is not contrasted with preflight

Finding ID: BFP-TSR6-2
Severity: major

T50 does not prove generation re-attests the changed five-skill inventory or
rejects copying the feasibility artifact.

Required outcome: Prove fresh generation evidence and preflight
non-substitutability through the report selector.
