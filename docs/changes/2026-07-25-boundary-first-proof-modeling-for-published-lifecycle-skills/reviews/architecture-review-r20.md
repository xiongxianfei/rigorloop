# Boundary-First Proof Modeling Architecture Review R20

Review ID: architecture-review-r20
Stage: architecture-review
Round: 20
Reviewer: Codex architecture-review skill with context-separated independent reviewer
Target: canonical architecture, boundary-proof component diagram, architecture assessment, and capability-projected file-change ADR chain
Review surface: canonical-architecture-update plus proposed ADR
Reviewed artifact: R19 correction candidate at 51866f34
Status: changes-requested
Review status: changes-requested
Material findings: BFP-AR20-1, BFP-AR20-2
Recording status: recorded
Immediate next stage: architecture
Plan readiness: not-ready
Review date: 2026-07-27
Context separation mechanism: separate-agent

Reviewed commit: `51866f34660e81352f9febb2b44e63641ba14e87`

## Result

Changes requested. R19's ownership and common-gate direction is substantially
implemented, but the architecture assessment and component evidence flow
remain stale.

## Material findings

### BFP-AR20-1 — Architecture assessment still scopes handler conformance only to non-exposure

Finding ID: BFP-AR20-1

Severity: material

Evidence:

The assessment gives exposed capability only a live trace and gives fresh
handler conformance only to non-exposure, contrary to the approved spec and
corrected canonical Runtime View.

Required outcome:

State conformance as a common pre-branch gate and both branch proofs as
additions.

Safe resolution:

Replace the assessment bullets with the exact common-plus-additional model.

### BFP-AR20-2 — Component diagram bypasses the pure validation boundary for runtime evidence

Finding ID: BFP-AR20-2

Severity: material

Evidence:

Runtime adapter and conformance outputs flow directly into v3 attestations,
although architecture assigns effective-tool and conformance validation to
pure functions in `boundary_proof_model.py`.

Required outcome:

Show runtime observations and bounded conformance results crossing the pure
validator before becoming attestation evidence.

Safe resolution:

Route both inputs into the registry/validator and route only validated
projection, tool, conformance, and diagnostic decisions into v3 attestations.

## Readiness

Not ready for plan revision. Resolve both findings and rerun architecture
review.
