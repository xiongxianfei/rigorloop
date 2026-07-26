# Boundary-First Proof Modeling Spec Review R15

Review ID: spec-review-r15
Stage: spec-review
Round: 15
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: deterministic runtime-attestation amendment
Reviewed artifact: specs/rigorloop-workflow.md
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR15-1, BFP-SR15-2, BFP-SR15-3, BFP-SR15-4
Immediate next stage: spec revision
Spec readiness: not-ready
Test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Initial packet inventory: exact R15 spec candidate; R14 findings and resolutions; accepted runtime ADR; T48-T50 candidate
Manifest owner: workflow orchestrator

## Findings

### BFP-SR15-1 - Thread provider and instruction expectations remain incomplete

Finding ID: BFP-SR15-1
Severity: blocker

The instruction list permits an arbitrary subset and provider is only
format-checked.

Required outcome: Require complete parent-owned instruction and provider
expectations.

### BFP-SR15-2 - Residual identity-preimage rules remain open

Finding ID: BFP-SR15-2
Severity: blocker

Runtime-package discovery, non-regular bundle entries, path substitution, and
secret-key detection are not deterministic.

Required outcome: Close package-root discovery, traversal, substitution, and
secret exclusion with direct proof.

### BFP-SR15-3 - Passing preflight is not evidence-bound

Finding ID: BFP-SR15-3
Severity: major

Pass output does not reference bounded attestation, and unavailable,
unreadable, or malformed runtime branches lack diagnostics.

Required outcome: Bind pass to a durable conditional attestation reference and
map every unavailable-runtime branch.

### BFP-SR15-4 - Report-selector invalidation is missing from T50

Finding ID: BFP-SR15-4
Severity: minor

T50 stops its tamper cascade at the current pointer.

Required outcome: Prove the complete report-selector invalidation cascade.
