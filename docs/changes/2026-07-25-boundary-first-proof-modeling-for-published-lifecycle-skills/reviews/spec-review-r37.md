# Boundary-First Proof Modeling Spec Review R37

Review ID: spec-review-r37
Stage: spec-review
Round: 37
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: stage-authored artifact-transport candidate at 96390a11
Reviewed artifact: `specs/rigorloop-workflow.md`
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR-R37-1, BFP-SR-R37-2, BFP-SR-R37-3
Immediate next stage: spec revision
Architecture assessment: architecture-required-after-approval
Eventual test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Manifest owner: workflow orchestrator

Reviewed spec identity: `sha256:5d8e27813c36b80ff3e3e7e35597950f5a9fb8b0bf71a9353906740fa56565e5`

Reviewed test-spec identity: `sha256:84614dbc8ac28f4f011f9ec5ed1cfe063b3548113df0b4ee296fb9fcdc6a3e2e`

Reviewed plan identity: `sha256:a5d89ddfaf769af4453f0fc92716eb3ed148c30ca37b98716cb06b799456c326`

## Findings

### BFP-SR-R37-1 - Review output variants omit required correction evidence

Finding ID: BFP-SR-R37-1
Severity: blocking
Location: R28y stage-artifact policy and review-bundle contract
Evidence: The new stage matrix permits review stages to return only review
record and review-log artifacts, while the existing changes-requested and
blocked branches require stage-owned review-resolution evidence and the
harness is forbidden from synthesizing it.
Required outcome: Define exhaustive stage-occurrence and output variants for
approved, changes-requested, blocked, correction, and approving-rereview
paths, including the owner and lifecycle state of every review-resolution
artifact.
Safe resolution: Add closed outcome- and occurrence-selected artifact-set
variants. The selected stage skill authors every required byte; the adapter
only validates the selected variant and materializes it unchanged. Require
lifecycle validation to prove content/outcome agreement.

### BFP-SR-R37-2 - Candidate failures lack replayable bounded evidence

Finding ID: BFP-SR-R37-2
Severity: blocking
Location: R28y candidate retention, output-state derivation, and diagnostic evidence
Evidence: The spec declares multiple candidates, duplicate rows, stage
mismatch, and unequal candidates contradictory, but derives output state from
the last complete candidate and records only one role-free artifact list.
It also refers to materialized file evidence for incomplete envelopes that are
never materialized and provides no candidate-count or aggregate-retention
bound.
Required outcome: Define one exhaustive candidate-set grammar,
classification algorithm, bounded observation record, and durable diagnostic
representation that independently proves every output state.
Safe resolution: Classify the complete bounded candidate set; record
value-free per-candidate ordinal, parse state, identity, stage, and ordered
artifact projection; retain content transiently only for the sole accepted
candidate; replace nonexistent failed-file references with candidate
observation evidence; and fail deterministically on candidate-count or
aggregate-byte overflow.

### BFP-SR-R37-3 - Preflight canary conflicts with the lifecycle policy

Finding ID: BFP-SR-R37-3
Severity: major
Location: R28y preflight canary and closed stage-artifact matrix
Evidence: The preflight invokes `workflow` and `spec` with a
`transport-canary` artifact, while the same closed lifecycle policy permits
`spec` only a `feature-spec` artifact.
Required outcome: Define a separate exact preflight materialization policy
selected by parent-owned invocation context and reject cross-use with
lifecycle policy.
Safe resolution: Bind a `materialization-canary` policy identity into the
preflight request, response schema, and attestation. Give it an exact
one-artifact matrix, size/disposal rules, and symmetric cross-use rejection.

## Review dimensions

| Dimension | Result |
| --- | --- |
| Requirement clarity | concern |
| Normative language | pass |
| Completeness | block |
| Testability | block |
| Examples | pass |
| Compatibility | pass |
| Observability | block |
| Security and privacy | concern |
| Non-goals | pass |
| Acceptance criteria | concern |

## Review result

The semantic-ownership direction is sound, but the contract is not yet
architecture- or test-spec-ready. Resolve BFP-SR-R37-1 through
BFP-SR-R37-3 and rerun spec-review. Architecture revision remains required
after approval because the accepted architecture and ADR still assume direct
stage-owned filesystem writes.
