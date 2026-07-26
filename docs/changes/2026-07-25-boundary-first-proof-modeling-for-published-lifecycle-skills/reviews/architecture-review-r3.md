# Boundary-First Proof Modeling Architecture Review R3

Review ID: architecture-review-r3
Stage: architecture-review
Round: 3
Reviewer: Codex architecture-review skill with context-separated reviewer
Target: commit `da8b961e` against `890409ac`
Reviewed artifact: docs/architecture/system/architecture.md; docs/adr/ADR-20260725-boundary-first-proof-modeling.md; docs/architecture/system/diagrams/container.mmd; docs/architecture/system/diagrams/component-boundary-proof.mmd
Status: changes-requested
Review status: changes-requested
Material findings: BFP-AR3-1, BFP-AR3-2, BFP-AR3-3
Immediate next stage: architecture revision
Plan readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Initial packet inventory: exact architecture diff; approved R13 specs and review; canonical architecture; ADR; C4 views; architecture assessment
Manifest owner: workflow orchestrator

## Result

- Skill: architecture-review
- Review status: changes-requested
- Material findings: BFP-AR3-1, BFP-AR3-2, BFP-AR3-3
- Recording status: recorded
- Recording blocker: none
- Immediate next stage: architecture revision
- Plan readiness: not-ready

## Findings

### BFP-AR3-1 - Publication ordering contradicts the approved recovery contract

Severity: material

Evidence:

- The architecture places the prepared receipt before immutable-run
  installation and describes the run and pointer as jointly atomic.
- R28y requires validated run installation before the fsynced receipt, then
  atomic pointer replacement and parent-directory fsync.

Required outcome:

Represent the exact durable sequence: validate temporary run, install immutable
run, write and fsync the receipt, write/fsync/replace the pointer, fsync the
parent directory, then reconcile and remove the receipt.

Safe resolution:

Correct the Runtime View, publisher component, ADR, and diagram labels.
State that the receipt makes publication recoverable and does not make run and
pointer installation jointly atomic.

### BFP-AR3-2 - Child-runtime trust is asserted but not enforceably owned

Severity: material

Evidence:

- Child-returned access observations cannot prove the child was confined.
- An isolated directory alone does not prevent external reads or network.
- The design does not identify credential ownership or prove that control-plane
  authentication stays outside child tools and durable evidence.

Required outcome:

Assign filesystem, tool, connector, subagent, and child-network enforcement to
a trusted parent-side or runtime-native sandbox; verify its effective profile
before accepting output; and use an opaque runtime-owned authentication channel
that is unavailable to child tools and never serialized.

Safe resolution:

Use a runtime-native sandbox/profile or parent-owned tool broker with
parent-observed attestation.
Fail with `environment-unavailable` when enforcement cannot be established and
show enforcement/authentication boundaries in both C4 views and security text.

### BFP-AR3-3 - The ADR omits the new durable architecture alternatives

Severity: material

Evidence:

The ADR records the standalone harness but does not compare it with workflow
engine reuse, transitive dependency reconstruction, in-process execution,
durable raw access logs, or general child-tool network.

Required outcome:

Record the rejected alternatives and consequences so the unsafe dependency,
execution, evidence, and network models are not reintroduced.

Safe resolution:

Add concise alternative and consequence entries covering runtime availability,
sandbox and authentication support, model cost and nondeterminism, transient
diagnostic limits, and publication recovery complexity.

## ADR Assessment

The proposed status is correct while these findings remain open.

## Diagram Assessment

The C4 roles and component level are appropriate.
The next revision must show trusted sandbox/profile enforcement,
control-plane authentication, and the exact run-to-receipt-to-pointer sequence.

Architecture assessment: architecture-required
