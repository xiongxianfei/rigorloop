# Boundary-First Proof Modeling Spec Review R46

Review ID: spec-review-r46
Stage: spec-review
Round: 46
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: specs/rigorloop-workflow.md
Reviewed artifact: R28y capability-negotiated projection candidate at 7d90c904
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR46-1, BFP-SR46-2, BFP-SR46-3, BFP-SR46-4
Immediate next stage: spec revision
Eventual test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-27
Context separation mechanism: separate-agent

Reviewed commit: `7d90c904`

Reviewed spec identity:
`sha256:b9583c065c3ba320390b9ed122f8d694ca8c170e6527e84d9e1e85068fe94e57`

## Result

Changes requested. The projection direction is sound, but v3 migration,
projection content identity, invocation-owned non-exposure evidence, and
diagnostic routing remain incomplete.

## Material findings

### BFP-SR46-1 — The v3 migration remains internally contradictory and leaves v2 without a disposition

Finding ID: BFP-SR46-1

The current schemas are v3, but stale v2 authority and upgrade language
remains and the compatibility section disposes only v1.

Required outcome: make all current authority v3; give v2 an explicit
unsupported-historical-evidence disposition when no durable v2 evidence
exists; prohibit v1 or v2 from satisfying current authority.

### BFP-SR46-2 — The runtime projection is not completely content-bound

Finding ID: BFP-SR46-2

The first projection row lacks exact values for all declared fields and the
attestation lacks a canonical projection identity.

Required outcome: define the complete first row, canonical serialization and
content identity; bind the identity into v3 evidence; reject duplicate IDs,
keys, unknown fields, and ID/content disagreement.

### BFP-SR46-3 — Non-exposure proof depends on undefined evidence

Finding ID: BFP-SR46-3

The effective tool inventory and handler-conformance proof have no closed,
invocation-owned schema or durable binding.

Required outcome: define their complete sources and identities, a versioned
handler-conformance policy/result, independent preflight and generation
execution, and closed failure behavior.

### BFP-SR46-4 — File-change diagnostic phase is ambiguous

Finding ID: BFP-SR46-4

`file-change-control-mismatch` can use two phases without a cause-to-phase
mapping or precedence contract.

Required outcome: enumerate every cause and phase, define precedence, and
reject unknown or cross-phase pairs.

## Readiness

Not ready for architecture. Resolve all four findings and rerun spec review.
