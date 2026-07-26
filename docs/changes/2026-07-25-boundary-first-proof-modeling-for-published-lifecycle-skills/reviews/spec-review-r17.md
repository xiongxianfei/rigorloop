# Boundary-First Proof Modeling Spec Review R17

Review ID: spec-review-r17
Stage: spec-review
Round: 17
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: runtime-attestation v1 contract and projections
Reviewed artifact: specs/rigorloop-workflow.md; specs/rigorloop-workflow.test.md; docs/plans/2026-07-25-boundary-first-proof-modeling.md
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR17-1
Immediate next stage: spec revision
Spec readiness: not-ready
Test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Initial packet inventory: exact R17 contract and projections; R14-R16 findings and resolutions
Manifest owner: workflow orchestrator

## Finding

### BFP-SR17-1 - Active plan retains one stale preflight command

Finding ID: BFP-SR17-1
Severity: major

The global validation list omits the required `--change-id` even though the
M2 command and CMD-BFP-8 are current.

Required outcome: Make every active command projection identical and preserve
the evidence-only classification.
