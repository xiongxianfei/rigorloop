# Boundary-First Proof Modeling Architecture Review R14

Review ID: architecture-review-r14
Stage: architecture-review
Round: 14
Reviewer: Codex architecture-review skill with context-separated independent reviewer
Target: architecture candidate at 19415360
Reviewed artifact: canonical architecture, boundary-proof component diagram, and ADR-20260725
Status: changes-requested
Review status: changes-requested
Material findings: BFP-AR14-1
Immediate next stage: architecture revision
Plan readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent

Reviewed architecture identity: `sha256:c2218e8b771144c7306690d06ded651660eb0397dddebd1a93d27f575106550b`

Reviewed component-diagram identity: `sha256:a468c1726aa8e619d9fd1407d8e15f39ecd53e7ef1f3f771ba647f97b73987a0`

Reviewed ADR identity: `sha256:e6a540578a95a6093f93331200befaaa2b365a41bd4a29dc599093e2800a0b90`

## Finding

### BFP-AR14-1 - Component view contradicts transport and publication ownership

Finding ID: BFP-AR14-1
Severity: material
Location: `docs/architecture/system/diagrams/component-boundary-proof.mmd`
Evidence: The diagram combines the acquired kernel lock with the durable
publisher lease, installs the immutable run before the prepared receipt, and
routes child events directly to the harness instead of the transport/output
reconciler.
Required outcome: Distinguish runtime lock from durable lease, project
discovery/recovery while locked, restore staged-run to prepared-receipt to
immutable-run to pointer ordering, and route events through transport/output
reconciliation.
Safe resolution: Correct the component nodes and relationships from the
approved R28y transaction and ownership contracts; no owner decision is
required.

## Review result

Canonical prose and ADR-20260725 otherwise align with the approved spec.
Planning remains blocked until the diagram is corrected and architecture
review R15 approves the package.
