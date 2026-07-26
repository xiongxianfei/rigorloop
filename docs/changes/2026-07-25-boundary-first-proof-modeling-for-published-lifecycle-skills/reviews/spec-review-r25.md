# Boundary-First Proof Modeling Spec Review R25

Review ID: spec-review-r25
Stage: spec-review
Round: 25
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: Codex 0.145.0 runtime projection amendment
Reviewed artifact: specs/rigorloop-workflow.md; specs/rigorloop-workflow.test.md; docs/architecture/system/architecture.md; docs/adr/ADR-20260726-codex-permission-profile-boundary-harness.md; docs/plans/2026-07-25-boundary-first-proof-modeling.md; scripts/boundary_proof_behavior.py; scripts/test-boundary-proof.py
Status: changes-requested
Review status: changes-requested
Material findings: BFP-RUNTIME-1, BFP-RUNTIME-2, BFP-RUNTIME-3, BFP-RUNTIME-4
Immediate next stage: focused spec and implementation revision
Spec readiness: not-ready
Test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Initial packet inventory: exact 0.145.0 feature and eleven-row skill projection
Manifest owner: workflow orchestrator

## Findings

### BFP-RUNTIME-1 - Protocol and schema projection is not closed

Finding ID: BFP-RUNTIME-1
Severity: blocker

The candidate derived classifications from the generated schema but did not
compare the complete schema or protocol projection with an approved exact
version-bound identity. A same-version added method could therefore receive a
fallback non-side-effect classification.

Required outcome: Pin the exact runtime-version/schema identity and complete
protocol-classification identity. Reject every missing, additional, or changed
schema member, method, or classification.

### BFP-RUNTIME-2 - Observed prohibited events are not enforced

Finding ID: BFP-RUNTIME-2
Severity: blocker

The candidate recorded notification methods but checked only selected
`item/completed` item types. Prohibited MCP, app, plugin, remote-control, or
permission events could therefore be observed without stopping the turn.

Required outcome: Resolve every observed server request and notification
against the exact classification and reject unknown or prohibited variants.

### BFP-RUNTIME-3 - Workspace-root request binding lacks direct proof

Finding ID: BFP-RUNTIME-3
Severity: major

Production code supplied the isolated workspace in both requests, but focused
proof covered only the returned thread metadata.

Required outcome: Build and test both request records directly, requiring one
exact isolated root and no alternate caller-supplied root surface.

### BFP-RUNTIME-4 - Governing identities and approvals are stale

Finding ID: BFP-RUNTIME-4
Severity: major

The runtime amendment changed the workflow spec, test spec, architecture, ADR,
and active plan after their approving reviews and recorded identities.

Required outcome: Close the runtime findings, refresh all bound identities,
and rerun spec, architecture, plan, and test-spec reviews before M2 handoff.

## Review result

The exact feature additions, disabled `review-agent`, eleven-row inventory,
closed proxy-name forwarding, live sandbox proof, and focused test results are
directionally sound. The four findings above block implementation handoff.
