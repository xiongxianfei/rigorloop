# Design Review R8: Explicit correction lifecycle

Review ID: design-review-r8
Stage: design-review
Round: r8
Reviewer: Independent Codex design-review context
Reviewer authority: design-review
Target: design package `architecture`, `spec`, `adr-compact-current-state-transaction`
Reviewed artifact: design package `architecture`, `spec`, `adr-compact-current-state-transaction`
Review date: 2026-09-04
Package kind: design
Package members: architecture=docs/architecture/2026-09-03-compact-current-state-change-record.md, spec=specs/compact-current-state-change-record.md, adr-compact-current-state-transaction=docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md
Upstream review ID: proposal-review-r6
Status: changes-requested
Material findings: CCSR-DR8-1
Correction targets: spec
Recording status: recorded

## Result

- Skill: design-review
- Review status: changes-requested
- Package members: architecture=`docs/architecture/2026-09-03-compact-current-state-change-record.md`, spec=`specs/compact-current-state-change-record.md`, adr-compact-current-state-transaction=`docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md`
- Upstream review ID: proposal-review-r6
- Review ID and round: design-review-r8, r8
- Material findings: CCSR-DR8-1
- Correction targets: spec, owned by spec
- Recording status: recorded
- Settlement status: withheld pending exact-package CLI settlement of the changes-requested outcome
- Open blockers: CCSR-DR8-1
- Immediate next stage: specification authoring owner through Workflow correction routing
- Claim limitations: this outcome grants no Design package authority and does not authorize Delivery, implementation, verification, branch, pull-request, release, or deployment readiness

### Finding CCSR-DR8-1

Finding ID: CCSR-DR8-1
Severity: major
Location: `specs/compact-current-state-change-record.md` SR-22, SR-25, reusable `ActiveCorrection`, and the `route-correction` payload
Evidence: `ActiveCorrection` now correctly contains the derived correction `status`, but the closed `route-correction` payload still accepts an entire `ActiveCorrection`. A caller can therefore submit `status: review-required` or `status: blocked` even though the eligibility matrix says a new route must produce `authoring`. Accepting and ignoring that field still violates the closed request contract, while accepting it semantically violates the single-evaluator rule. This directly contradicts SR-22 and SR-25, which prohibit caller-supplied derived lifecycle fields.
Required outcome: Define a separate closed semantic correction input that omits derived kind and status, use it for `route-correction`, and require the evaluator alone to construct the persisted `ActiveCorrection` with `kind: correction` and `status: authoring`. Unknown or caller-supplied derived correction fields must reject.
Safe resolution path: The specification owner should make the bounded request-schema correction, retain the durable `ActiveCorrection` shape, register only the specification, return through Workflow, and request a fresh exact-package Design Review.
needs-decision rationale: none
Finding scope: artifact-local
Affected artifact IDs: spec
Owning stages: spec

## Design coherence

The R7 corrections otherwise resolve both prior findings. Projection input now identifies the optional operation exactly, and correction return preserves the active correction until required review settlement. The package remains aligned on current-state sufficiency, local trust, operation-scoped eligibility, non-loss, evidence freshness, recovery, and prospective activation. CCSR-DR8-1 is material because the request boundary would otherwise permit callers to propose the derived state that the evaluator exclusively owns.

## Proposal preservation

The required separation is internal to the approved CLI semantic boundary. It preserves explicit correction return, review-owned settlement, and CLI-derived coordination without adding a permission claim, history dependency, or new service.

## Independence statement

This review did not edit the proposal, architecture, specification, ADR, authoring evidence, or workflow routing state. CCSR-DR8-1 is recorded for the specification owner.
