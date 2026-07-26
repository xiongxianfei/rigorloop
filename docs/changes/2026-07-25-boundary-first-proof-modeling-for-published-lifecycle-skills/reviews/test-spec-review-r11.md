# Boundary-First Proof Modeling Test-Spec Review R11

Review ID: test-spec-review-r11
Stage: test-spec-review
Round: 11
Reviewer: Codex test-spec-review skill with context-separated independent reviewer
Target: refreshed exact Codex 0.145.0 proof contract
Reviewed artifact: specs/rigorloop-workflow.test.md
Status: changes-requested
Review status: changes-requested
Material findings: BFP-TSR11-1, BFP-TSR11-2
Immediate next stage: test-spec revision
Implementation readiness: not-ready
Implementation handoff: not-allowed
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Initial packet inventory: approved R26 spec, R13 architecture, R14 plan, refreshed test spec
Manifest owner: workflow orchestrator

## Findings

### BFP-TSR11-1 - Governing review prose is stale

Finding ID: BFP-TSR11-1
Severity: major

The input-identity table correctly names architecture-review R13 and
plan-review R14, but the related-artifact prose still names R11 and R12.

Required outcome: Make every governing review reference identify the current
approved architecture and plan review.

### BFP-TSR11-2 - The exact runtime projection lacks a literal proof oracle

Finding ID: BFP-TSR11-2
Severity: major

T49 requires an exact runtime projection but does not record the two approved
literal identities or the exact feature-row cardinality. The existing
synthetic projection test proves comparison mechanics but not conformity to
the approved Codex 0.145.0 oracle.

Required outcome: Record the exact schema identity, protocol-classification
identity, and 96-row feature inventory in T49, then add direct positive
assertions and missing, additional, or wrong-projection contrasts.

## Review result

The runtime proof design is otherwise aligned. Both findings block the M2
implementation handoff until correction and same-stage rereview.
