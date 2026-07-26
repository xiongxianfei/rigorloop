# Boundary-First Proof Modeling Spec Review R42

Review ID: spec-review-r42
Stage: spec-review
Round: 42
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: bounded read-only workspace-integrity candidate at a101ec89
Reviewed artifact: specs/rigorloop-workflow.md
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR42-1, BFP-SR42-2
Immediate next stage: spec
Architecture assessment: architecture-required
Test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent

Reviewed spec identity: `sha256:02d6f95bb515c3c96a4323d126aa7cf2e19753dcaff56088301f02c65f6ab7a1`

## Result

The read-only command/descendant boundary and bounded race-resistant scanner
are sound. Two gaps remain: the separate app-server file-change/apply-patch
path is asserted rather than independently proved, and pre-turn baseline
failure reasons have no legal typed result surface.

## Material findings

### BFP-SR42-1 — App-server file-change denial is asserted but not proved

Finding ID: BFP-SR42-1

Severity: blocking

Location: workflow spec runtime attestation and probe contract

Evidence:

The exact probes cover command-path direct and descendant write denial. The
separate app-server file-change/apply-patch path remains a permitted protocol
side effect, and the canary does not require an attempt through that path.

Required outcome:

Before accepting a stage turn, independently prove the app-server
file-change/apply-patch path cannot mutate the workspace, or make that path
absent/prohibited and reject every invocation.

Safe resolution:

Add a parent-observed app-server file-change denial probe over bounded
parent-created fixtures. Bind its exact policy through runtime version,
feature/protocol classification, effective configuration, canary, and
generation attestation. Require the denial event, unchanged workspace, and no
raw model prose in evidence.

### BFP-SR42-2 — Baseline failure reasons have no defined result surface

Finding ID: BFP-SR42-2

Severity: major

Location: workflow spec preflight response and baseline contract

Evidence:

`workspace-baseline-invalid` says it carries the first closed reason, but the
exact five-field preflight response has no reason field and generation creates
no transport row or alternative typed failure record.

Required outcome:

Give every baseline failure one exact bounded privacy-safe representation in
preflight and generation without a transport row or raw paths/exceptions.

Safe resolution:

Add a versioned nullable `workspace_failure` object to the preflight response
and one exact generation-start failure result. Bind the closed reason,
integrity-policy identity, canonical identity, nullability, size limit, and
unrelated-diagnostic behavior.

## Review dimensions

| Dimension | Result |
| --- | --- |
| Requirement clarity | block |
| Normative language | concern |
| Completeness | block |
| Testability | block |
| Compatibility | concern |
| Observability | block |
| Security and privacy | block |
| Non-goals | pass |
| Acceptance criteria | concern |

## Readiness

Not ready for architecture or test-spec reliance. Resolve BFP-SR42-1 and
BFP-SR42-2 and obtain an approved spec rereview.
