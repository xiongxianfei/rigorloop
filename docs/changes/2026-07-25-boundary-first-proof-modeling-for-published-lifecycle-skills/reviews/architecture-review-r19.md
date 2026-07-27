# Boundary-First Proof Modeling Architecture Review R19

Review ID: architecture-review-r19
Stage: architecture-review
Round: 19
Reviewer: Codex architecture-review skill with context-separated independent reviewer
Target: canonical architecture, boundary-proof component diagram, architecture assessment, and capability-projected file-change ADR chain
Review surface: canonical-architecture-update plus proposed ADR
Reviewed artifact: R48 architecture projection at 6abc9410
Status: changes-requested
Review status: changes-requested
Material findings: BFP-AR19-1, BFP-AR19-2
Recording status: recorded
Immediate next stage: architecture
Plan readiness: not-ready
Review date: 2026-07-27
Context separation mechanism: separate-agent

Reviewed commit: `6abc941035f16851a0200e97d5bb0ad2955150fb`

## Result

Changes requested. The projection direction, v3 migration, and scoped
supersession are sound, but common handler conformance and executable component
ownership are incomplete.

## Material findings

### BFP-AR19-1 — Handler conformance is not unambiguously required for both capability branches

Finding ID: BFP-AR19-1

Severity: material

Evidence:

The approved spec requires fresh conformance before preflight and again during
generation for both capability states. The architecture attaches it explicitly
only to `not-exposed-projection`, while exposed-branch descriptions name only
the live decline trace.

Required outcome:

Make fresh invocation-owned handler conformance a common pre-branch gate.
The exposed state then adds a live correlated decline trace; the non-exposed
state adds exact projection/effective-tool proof and drift rejection.

Safe resolution:

Align the Runtime View, capability table, quality scenario, risk, and ADR.

### BFP-AR19-2 — New executable components lack an exact C4-consistent ownership projection

Finding ID: BFP-AR19-2

Severity: material

Evidence:

The component diagram introduces a runtime projection registry and
file-change handler conformance without corresponding physical-owner rows.
The registry lacks a normative spec-to-projection relationship, and seven
component relationships remain unlabeled.

Required outcome:

Assign immutable registry and selection/conformance validation to
`scripts/boundary_proof_model.py`; assign production dispatch and fresh
conformance execution to `scripts/boundary_proof_behavior.py`; align the
table, ADR, and fully labeled diagram.

Safe resolution:

Add explicit ownership rows and relationship intent labels without changing
the two-module boundary.

## Readiness

Not ready for plan revision. Resolve both findings and rerun architecture
review.
