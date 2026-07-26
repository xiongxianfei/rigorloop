# Boundary-First Proof Modeling Spec Review R23

Review ID: spec-review-r23
Stage: spec-review
Round: 23
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: corrected deterministic runtime projection
Reviewed artifact: specs/rigorloop-workflow.md; specs/rigorloop-workflow.test.md; docs/architecture/system/architecture.md; docs/adr/ADR-20260726-codex-permission-profile-boundary-harness.md; docs/plans/2026-07-25-boundary-first-proof-modeling.md
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR23-1
Immediate next stage: spec revision
Spec readiness: not-ready
Test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Initial packet inventory: R22 correction and deterministic runtime projection
Manifest owner: workflow orchestrator

## Finding

### BFP-SR23-1 - Generation still uses the superseded five-row runtime inventory

Finding ID: BFP-SR23-1
Severity: major

R28y binds `skill_inventory_identity` to the exact ten-row runtime roster, but
T50 and the active plan still described generation as deriving a five-skill
runtime inventory.

Required outcome: Generation-time attestation independently binds the same
exact ten-row runtime roster—five enabled manifested lifecycle rows plus five
generated-config-bound disabled system rows. The distinct five-package
resource set remains labeled as package/resource input, not runtime inventory.

Safe resolution: Replace the stale generation references and require a
generation contrast for any bound ten-row inventory member.

## Review result

R22 is resolved. Canonical-JSON schema identity, recursive duplicate rejection,
complete configuration origins, and the exact preflight inventory are
deterministic. The stale generation-time inventory terminology blocks approval.
