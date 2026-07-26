# Boundary-First Proof Modeling Test-Spec Review R9

Review ID: test-spec-review-r9
Stage: test-spec-review
Round: 9
Reviewer: Codex test-spec-review skill with context-separated independent reviewer
Target: refreshed M2 proof contract
Reviewed artifact: specs/rigorloop-workflow.test.md
Status: changes-requested
Review status: changes-requested
Material findings: BFP-TSR9-1, BFP-TSR9-2
Immediate next stage: test-spec revision
Implementation readiness: not-ready
Implementation handoff: not-allowed
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Initial packet inventory: approved R24 spec, R11 architecture, R12 plan, refreshed test spec
Manifest owner: workflow orchestrator

## Findings

### BFP-TSR9-1 - Configuration-origin derivation rules lack structural contrasts

Finding ID: BFP-TSR9-1
Severity: major

T49 mutated the origin-key set but did not prove independent flattening of
nested TOML tables, zero-based arrays, or preserved quoted-key bytes. A fixed
allowlist could satisfy the existing cases.

Required outcome: Add positive and negative fixtures for every flattening rule
and require exact equality with the complete runtime-returned origin-key set.

### BFP-TSR9-2 - Four required M2 validation commands are unclassified

Finding ID: BFP-TSR9-2
Severity: major

The approved plan requires canonical skill validation, generated-skill drift
checking, boundary CLI smoke, and four-file Python compilation, but the
validation-command registry and M2 proof map omitted them.

Required outcome: Give each command a stable ID, owner, failure behavior,
evidence target, safe side-effect boundary, and M2 mapping.

## Review result

The remaining M2 proof map is complete. BFP-TSR9-1 and BFP-TSR9-2 block
implementation handoff until correction and rereview.
