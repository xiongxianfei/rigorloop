# Boundary-First Proof Modeling Test-Spec Review R5

Review ID: test-spec-review-r5
Stage: test-spec-review
Round: 5
Reviewer: Codex test-spec-review skill with context-separated independent reviewer
Target: M2 runtime-boundary proof map
Reviewed artifact: specs/rigorloop-workflow.test.md
Status: blocked
Review status: blocked
Material findings: BFP-TSR5-1, BFP-TSR5-2
Immediate next stage: spec revision
Implementation readiness: not-ready
Implementation handoff: not-allowed
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Initial packet inventory: exact T48-T50 candidate; approved R13 spec; accepted R8 architecture/ADR; approved R8 plan
Manifest owner: workflow orchestrator

## Result

- Skill: test-spec-review
- Review status: blocked
- Material findings: BFP-TSR5-1, BFP-TSR5-2
- Immediate next stage: spec revision
- Implementation readiness: not-ready
- Implementation handoff: not-allowed

## Findings

### BFP-TSR5-1 - Schema, negotiation, and pagination negatives are incomplete

Finding ID: BFP-TSR5-1
Severity: major

Evidence:

- T49 lacks exact schema-bundle file/path/byte/identity drift,
  `experimentalApi` failure, required-field shape, and cursor
  termination/cycle contrasts.

Required outcome:

Prove schema identity, protocol negotiation, and pagination fail closed before
turn or output acceptance.

Safe resolution:

Add independent bundle, negotiation, method/field, cursor, and cross-page
duplication negatives.

### BFP-TSR5-2 - Runtime attestation is not durably operation-bound

Finding ID: BFP-TSR5-2
Severity: major

Evidence:

- The exact R28y implementation-manifest shape has no runtime-attestation
  field, so T48-T50 cannot bind schema/config/inventory/profile/probe/canary
  evidence to the accepted immutable run or validate stable failure classes.

Required outcome:

Define one bounded spec-owned attestation location, bind it through the
implementation manifest and input set, and test substitution and diagnostics.

Safe resolution:

Amend the exact implementation-manifest schema with one non-secret bounded
attestation record and closed diagnostics; then map its full mutation matrix
in T48-T50.

## Prior-Finding Reconciliation

The remainder of T48-T50 is aligned: runtime identity continuity, separate
feature/item classifications, exact tools/inventories, managed-profile probes,
canary channels, command ownership, and M2 mapping are complete.
