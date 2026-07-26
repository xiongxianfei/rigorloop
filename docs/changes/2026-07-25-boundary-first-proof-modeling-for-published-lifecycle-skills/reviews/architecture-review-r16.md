# Boundary-First Proof Modeling Architecture Review R16

Review ID: architecture-review-r16
Stage: architecture-review
Round: 16
Reviewer: Codex architecture-review skill with context-separated independent reviewer
Target: architecture candidate at 428f36d6
Reviewed artifact: canonical architecture, boundary-proof component diagram, architecture assessment, proposed stage-envelope ADR, accepted boundary-first ADR, and accepted permission-profile ADR
Status: changes-requested
Review status: changes-requested
Material findings: BFP-AR16-1, BFP-AR16-2
Immediate next stage: spec
Plan readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent

Reviewed architecture identity: `sha256:549e755d56aa305092ae4853019b6b5a5bfb651b5dd3383379ec5e1cd571457f`

Reviewed component-diagram identity: `sha256:513bd9ceb5e442102e2464f8f66cfad54902c9d844aa7c06b1f025cca6929b03`

Reviewed proposed envelope ADR identity: `sha256:06aa94198a666e423f3b4c2ec647487119dbd498aa9f17f1659c083eae41326e`

Reviewed accepted boundary-first ADR identity: `sha256:66f25f21ced5fe7cf91016a76ed5451829762678de919f9bcb87352fe85f5d41`

Reviewed accepted permission-profile ADR identity: `sha256:f757569f2bbe986f957f8a2532a6d9bd268695ff0f271779dce270b1bdb7b690`

Reviewed workflow-spec identity: `sha256:29d7f1555f937ee835733d44b6e9386fae7a4203e596ef5ded483e3551bb76a3`

## Result

The semantic-authority split is sound, but the physical-write boundary is not
yet enforceable. Child commands and file-change events can mutate the same
isolated workspace before adapter materialization, while final reread equality
proves only final bytes. The numbered Runtime View also remains on the
pre-envelope protocol. Planning and implementation remain paused.

## Material findings

### BFP-AR16-1 — The envelope-only materialization boundary remains bypassable through child filesystem writes

Finding ID: BFP-AR16-1

Severity: material

Location: accepted permission-profile ADR decision 3 and permitted tool set;
canonical architecture Building Block, Runtime, and component-boundary-proof
view; proposed stage-envelope ADR Decision

Evidence:

- The accepted permission-profile ADR makes the isolated workspace writable
  and permits both sandboxed commands and file-change/apply-patch side effects.
- The proposed transport ADR makes the envelope the only stage-output
  transport and assigns physical writes to the exact-byte materializer.
- The component view connects child tools to the same isolated workspace but
  has no pre-materialization workspace-integrity boundary.
- A child can write an expected path before returning its envelope. The
  materializer can overwrite it, and final reread equality cannot prove
  adapter-exclusive physical materialization.
- Protocol file-change observations are insufficient because a permitted shell
  command can also mutate the workspace.

Required outcome:

Define a deterministic pre-materialization child-mutation boundary covering
command and file-change writes. Capture the complete identity-bound scenario
workspace before the turn, compare it after normal completion or confirmed
stop and before materialization, and fail closed without materialization or
publication on any created, changed, removed, symlinked, or non-regular entry.
Only an unchanged result may authorize exact-byte materialization.

Safe resolution:

- Add a narrow spec contract with a closed value-free observation and
  diagnostic because the R40 transport vocabulary cannot currently represent
  this failure without reinterpretation.
- Amend the transport ADR and canonical Building Block, Runtime,
  Crosscutting, Risks, and component views.
- Exercise the same guard in the materialization canary.
- Prefer a runtime-enforced read-only child view plus parent-only
  materialization path if a supported runtime later exposes one; do not rely on
  protocol file-change events alone.

### BFP-AR16-2 — The canonical Runtime View still projects the superseded direct-output protocol

Finding ID: BFP-AR16-2

Severity: material

Location: `docs/architecture/system/architecture.md`, Boundary-first proof flow
steps 9, 13, and 15

Evidence:

- Step 9 retains only the generic workspace-write probe.
- Step 13 binds only `boundary-transport-policy-v1` and omits the lifecycle
  artifact policy.
- Step 15 omits candidate-set observation, artifact-policy identity,
  exact-byte materialization observation, and content-validation observation.
- The newer sequence appears only in later component and crosscutting text,
  leaving the canonical Runtime View internally inconsistent.

Required outcome:

Synchronize the numbered Runtime View to order runtime negotiation and
confinement probes, the separate stage-envelope canary, canary-policy
attestation, fresh generation attestation, lifecycle artifact-policy binding,
bounded candidate collection, completion or confirmed-stop reconciliation,
workspace-integrity checking, envelope validation, exact materialization,
complete reread comparison, structural content validation, snapshot, and
immutable publication.

Safe resolution:

Project the approved R40 contract and the focused workspace-integrity
clarification into the existing Runtime View. Preserve no inspection under
uncertain liveness, absent-only retry, no retry for every unsafe candidate or
protocol tuple, and non-retention of failed raw content. No new component,
persistence surface, or workflow mechanism is needed.

## Non-blocking correction

The Architecture Decisions list describes the accepted permission-profile ADR
as `Proposed`. Correct that lifecycle wording during architecture revision.

## Review dimensions

| Dimension | Result |
| --- | --- |
| Spec alignment | block |
| Canonical package shape | pass |
| C4 role consistency | pass with correction |
| Semantic ownership | pass |
| Physical mutation ownership | block |
| Candidate collection and raw retention | pass |
| Lifecycle/canary policy separation | pass |
| Timeout and retry semantics | pass outside the stale Runtime View |
| Materialization and content validation | block on mutation provenance |
| Runtime and recovery flow | block |
| Security and confinement | block on child-write handling |
| ADR lifecycle timing | pass with minor wording correction |
| Implementation and testability | concern until integrity guard is settled |
| Complexity discipline | pass |
| Plan readiness | block |

## Readiness

Not ready for plan or implementation. Route first to a focused spec amendment
for BFP-AR16-1, then synchronize the architecture package and rerun
architecture-review.
