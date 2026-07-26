# Boundary-First Proof Modeling Spec Review R22

Review ID: spec-review-r22
Stage: spec-review
Round: 22
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: corrected deterministic schema/config projection
Reviewed artifact: specs/rigorloop-workflow.md; specs/rigorloop-workflow.test.md; docs/architecture/system/architecture.md; docs/plans/2026-07-25-boundary-first-proof-modeling.md; docs/plan.md
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR22-1
Immediate next stage: spec revision
Spec readiness: not-ready
Test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Initial packet inventory: R21 corrections and proof projection
Manifest owner: workflow orchestrator

## Finding

### BFP-SR22-1 - T49 does not require duplicate-name rejection unambiguously

Finding ID: BFP-SR22-1
Severity: major

T49 grouped duplicate-name and malformed-JSON inputs with semantic mutations
whose expected result allowed either a changed identity or failure.

Required outcome: Require object-key reorder to preserve identity, semantic
array/member changes to change identity, and duplicate names or malformed JSON
to fail with `schema-bundle-invalid`.
