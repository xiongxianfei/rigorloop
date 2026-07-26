# Boundary-First Proof Modeling Spec Review R33

Review ID: spec-review-r33
Stage: spec-review
Round: 33
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: R32 resolution candidate at a049d939
Reviewed artifact: `specs/rigorloop-workflow.md` and `specs/rigorloop-workflow.test.md`
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR-R33-1, BFP-SR-R33-2, BFP-SR-R33-3, BFP-SR-R33-4
Immediate next stage: spec revision
Architecture assessment: architecture-required-after-approval
Eventual test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Manifest owner: workflow orchestrator

Reviewed spec identity: `sha256:0a51b12618e58f0cf0a5128ad0b90fd4bfff299a0cab39fe6ea867f87ab647cb`

Reviewed test-spec identity: `sha256:f9b82e259409a1ff22ff1a42d18eb3f84563c1f915fe9c2055330e8d763d5156`

Reviewed plan identity: `sha256:c12dc73192ae5c82713d223077f327a8b06c3ba74c0667d2c90fc7697d220357`

## Findings

### BFP-SR-R33-1 - Malformed-temp recovery is unreachable

Finding ID: BFP-SR-R33-1
Severity: blocking
Location: R28y global discovery and recovery temp cleanup
Evidence: Generic malformed-object rejection runs before the constrained
malformed-temp cleanup route.
Required outcome: Add one lexically valid, lease-bound malformed-temp
classification that reaches cleanup while all ambiguous cases remain closed.
Safe resolution: Split name validation from content validation and select one
recoverable temp exception only after unique lease/run/recovery binding.

### BFP-SR-R33-2 - Unknown-event evidence cannot be independently verified

Finding ID: BFP-SR-R33-2
Severity: major
Location: R28y protocol classification evidence
Evidence: The record stores only an event-shape hash and no value-free
projection from which validation can recompute it.
Required outcome: Retain the exact value-free projection and canonical identity
without recording protocol values or raw logs.
Safe resolution: Add `event_shape_projection` and define path/type
canonicalization and hash equality.

### BFP-SR-R33-3 - Observed output roles have no authoritative source

Finding ID: BFP-SR-R33-3
Severity: major
Location: R28y output evaluator
Evidence: Filesystem observation supplies path and bytes but the raw observed
descriptor also asserts a semantic role; exact matching is undefined.
Required outcome: Derive roles only from the stage-policy path map and define
path/identity matching exactly.
Safe resolution: Store observed `{path, identity}` only and project roles from
the unique required path descriptor.

### BFP-SR-R33-4 - Liveness pause drops prior non-output diagnostics

Finding ID: BFP-SR-R33-4
Severity: blocking
Location: R28y transport routing matrix
Evidence: Complete diagnostic retention permits protocol/runtime conditions
before failed termination, but the liveness row accepts only liveness+timeout.
Required outcome: Retain all prior non-output diagnostics with uninspected
output while keeping the route paused.
Safe resolution: Define a liveness tuple family containing liveness, ordered
zero-or-more non-output diagnostics, and timeout, with no output diagnostic.

## Review result

The spec remains blocked until R33-1 through R33-4 are resolved and
independently rereviewed.
