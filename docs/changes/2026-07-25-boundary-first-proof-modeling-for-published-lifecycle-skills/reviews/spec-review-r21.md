# Boundary-First Proof Modeling Spec Review R21

Review ID: spec-review-r21
Stage: spec-review
Round: 21
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: deterministic schema/config projection correction
Reviewed artifact: specs/rigorloop-workflow.md; specs/rigorloop-workflow.test.md; docs/architecture/system/architecture.md; docs/adr/ADR-20260726-codex-permission-profile-boundary-harness.md; docs/plans/2026-07-25-boundary-first-proof-modeling.md
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR21-1, BFP-SR21-2, BFP-SR21-3
Immediate next stage: spec revision
Spec readiness: not-ready
Test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Initial packet inventory: deterministic schema/config candidate and focused projections
Manifest owner: workflow orchestrator

## Findings

### BFP-SR21-1 - Duplicate JSON keys can escape member binding

Finding ID: BFP-SR21-1
Severity: blocking

Parsing generated schema JSON without duplicate-name detection can discard an
earlier member before canonicalization.

Required outcome: Reject duplicate object-member names recursively before
canonicalization and test top-level and nested duplicates.

### BFP-SR21-2 - Config-origin acceptance remains incomplete

Finding ID: BFP-SR21-2
Severity: blocking

The candidate did not close version format, non-empty exact origin-key
coverage, or exact source shape.

Required outcome: Derive the exact origin-key set independently from generated
TOML leaves and close source, path, profile, version, root, and effective-config
contrasts.

### BFP-SR21-3 - Architecture and plan are not synchronized

Finding ID: BFP-SR21-3
Severity: major

One architecture paragraph retained raw-byte schema identity and the plan
retained stale review pointers and invalid handoff vocabulary.

Required outcome: Use canonical-JSON schema projection consistently and
synchronize plan sources and validator-legal handoff fields.
