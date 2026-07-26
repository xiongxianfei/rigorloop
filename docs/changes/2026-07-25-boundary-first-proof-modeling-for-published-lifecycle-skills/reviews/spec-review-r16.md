# Boundary-First Proof Modeling Spec Review R16

Review ID: spec-review-r16
Stage: spec-review
Round: 16
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: runtime-attestation v1 contract
Reviewed artifact: specs/rigorloop-workflow.md
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR16-1, BFP-SR16-2
Immediate next stage: spec revision
Spec readiness: not-ready
Test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Initial packet inventory: exact R16 spec candidate; R14-R15 findings and resolutions; accepted runtime ADR; T48-T50 candidate
Manifest owner: workflow orchestrator

## Findings

### BFP-SR16-1 - Supported runtime version predicate is incomplete

Finding ID: BFP-SR16-1
Severity: major

The spec omits the accepted 0.138.0 floor and prerelease/build precedence, so
`runtime-version-unsupported` lacks an exact trigger.

Required outcome: Define deterministic SemVer support and exact boundary tests.

### BFP-SR16-2 - Preflight destination and durable publication are undefined

Finding ID: BFP-SR16-2
Severity: blocker

The command has no change target, is called read-only despite writing evidence,
and may report pass before file and directory durability.

Required outcome: Select one exact change root and make pass conditional on a
completed recoverable publication transaction.
