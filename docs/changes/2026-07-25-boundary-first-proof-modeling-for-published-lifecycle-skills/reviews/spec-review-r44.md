# Boundary-First Proof Modeling Spec Review R44

Review ID: spec-review-r44
Stage: spec-review
Round: 44
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: deny-only stage-authority candidate at 7c645bc0
Reviewed artifact: specs/rigorloop-workflow.md
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR44-1
Immediate next stage: spec
Architecture assessment: architecture-required
Test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent

Reviewed spec identity: `sha256:7c286ad0c3474c1834e4d750f9a30e897cce4fa190363d70de8b5e7019df13f0`

## Result

The v2 current path, shared deny-only file-change policy, cause-specific
decline trace, generic carriers, and intrinsic workspace-failure bound are
sound. One compatibility gap remains: the claimed historical-v1 shape does
not match the actual tracked v1 evidence.

## Material finding

### BFP-SR44-1 — Historical v1 compatibility describes a nonexistent shape

Finding ID: BFP-SR44-1

Severity: major

Location: workflow spec historical runtime-attestation compatibility contract

Evidence:

The tracked v1 implementation manifest lacks `transport_policy`,
`artifact_policy`, and several later attestation/probe fields. The spec instead
describes v1 as nearly identical to v2, so a reader cannot select a parser
deterministically from the reused v1 labels.

Required outcome:

Make historical readability deterministic for actual persisted evidence
without permitting any v1 record as current evidence.

Safe resolution:

Use an exact legacy registry keyed by an immutable discriminator, narrow
support to explicit immutable historical evidence identities, or preserve v1
as opaque unsupported data. Unknown or ambiguous v1 variants fail closed.

## Review dimensions

| Dimension | Result |
| --- | --- |
| Requirement clarity | concern |
| Normative language | pass |
| Completeness | block |
| Testability | block |
| Compatibility | block |
| Observability | pass |
| Security and privacy | pass |
| Non-goals | pass |
| Acceptance criteria | concern |

## Readiness

Not ready for architecture or test-spec reliance. Resolve BFP-SR44-1 and
obtain an approved spec rereview.
