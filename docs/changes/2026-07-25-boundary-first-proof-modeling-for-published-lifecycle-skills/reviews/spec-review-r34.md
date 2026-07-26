# Boundary-First Proof Modeling Spec Review R34

Review ID: spec-review-r34
Stage: spec-review
Round: 34
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: R33 resolution candidate at 15d1fc23
Reviewed artifact: `specs/rigorloop-workflow.md` and `specs/rigorloop-workflow.test.md`
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR-R34-1, BFP-SR-R34-2, BFP-SR-R34-3, BFP-SR-R34-4
Immediate next stage: spec revision
Architecture assessment: architecture-required-after-approval
Eventual test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Manifest owner: workflow orchestrator

Reviewed spec identity: `sha256:15705dbe18de1ef9bd3273f5942949ebf2fd1a523ed46fc7035b5ccb6e70aa80`

Reviewed test-spec identity: `sha256:10cd9b07d1dbbd3a0f837891ba444a62f9d96016b424ec1248b6d38ecac382d0`

Reviewed plan identity: `sha256:e3a54ad63cc50e21869d02f6a3a85c778cbafe6a527d411640b525f7eec1af1a`

## Findings

### BFP-SR-R34-1 - Conditional protocol prohibition has no route

Finding ID: BFP-SR-R34-1
Severity: blocking
Location: R28y protocol diagnostics and T49/T52
Evidence: Unsafe values of a statically permitted remote-control notification
are neither schema-invalid, unknown, nor statically prohibited.
Required outcome: Add a closed value-sensitive policy diagnostic with
privacy-safe rule evidence and all status/nullness cases.
Safe resolution: Add `protocol-conditional-policy-violation` and a closed
remote-control rule record containing only booleans.

### BFP-SR-R34-2 - Completed recovery history conflicts with fresh runs

Finding ID: BFP-SR-R34-2
Severity: blocking
Location: R28y global discovery
Evidence: Preserved completed run-A recovery objects and active run-B lease
name two runs under the generic multi-run conflict rule.
Required outcome: Validate completed history separately and exclude valid
completed history from active candidate/conflict projection.
Safe resolution: Build historical and active projections before applying the
single-active-run invariant.

### BFP-SR-R34-3 - Timeout and termination bounds are not policy-bound

Finding ID: BFP-SR-R34-3
Severity: blocking
Location: R28y implementation manifest, transport rows, and T52
Evidence: Arbitrary nonnegative deadlines and unspecified termination waits
permit zero/caller-selected or unbounded behavior.
Required outcome: Add positive manifest-owned turn and termination-wait bounds,
policy identity, monotonic comparisons, and thread/process binding.
Safe resolution: Add one closed transport policy to the implementation
manifest and bind every row/evidence record to it.

### BFP-SR-R34-4 - Runtime identity instability lacks resource/checkpoint binding

Finding ID: BFP-SR-R34-4
Severity: major
Location: R28y runtime identity diagnostic and T49/T52
Evidence: Unequal hashes do not identify launcher versus package, checkpoint,
or the bound expected identity.
Required outcome: Add closed identity kind/checkpoint fields and require exact
attestation binding and same-resource observation.
Safe resolution: Project the existing before/after runtime checks into exact
diagnostic evidence enums.

## Review result

The spec remains blocked until R34-1 through R34-4 are resolved and
independently rereviewed.
