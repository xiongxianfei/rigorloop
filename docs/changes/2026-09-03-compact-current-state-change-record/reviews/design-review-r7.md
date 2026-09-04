# Design Review R7: Scoped operation eligibility and correction return

Review ID: design-review-r7
Stage: design-review
Round: r7
Reviewer: Independent Codex design-review context
Reviewer authority: design-review
Target: design package `architecture`, `spec`, `adr-compact-current-state-transaction`
Reviewed artifact: design package `architecture`, `spec`, `adr-compact-current-state-transaction`
Review date: 2026-09-04
Package kind: design
Package members: architecture=docs/architecture/2026-09-03-compact-current-state-change-record.md, spec=specs/compact-current-state-change-record.md, adr-compact-current-state-transaction=docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md
Upstream review ID: proposal-review-r6
Status: changes-requested
Material findings: CCSR-DR7-1, CCSR-DR7-2
Correction targets: spec
Recording status: recorded

## Result

- Skill: design-review
- Review status: changes-requested
- Package members: architecture=`docs/architecture/2026-09-03-compact-current-state-change-record.md`, spec=`specs/compact-current-state-change-record.md`, adr-compact-current-state-transaction=`docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md`
- Upstream review ID: proposal-review-r6
- Review ID and round: design-review-r7, r7
- Material findings: CCSR-DR7-1, CCSR-DR7-2
- Correction targets: spec, owned by spec
- Recording status: recorded
- Settlement status: withheld pending exact-package CLI settlement of the changes-requested outcome
- Open blockers: CCSR-DR7-1, CCSR-DR7-2
- Immediate next stage: specification authoring owner through Workflow correction routing
- Claim limitations: this outcome grants no Design package authority and does not authorize Delivery, implementation, verification, branch, pull-request, release, or deployment readiness

### Finding CCSR-DR7-1

Finding ID: CCSR-DR7-1
Severity: major
Location: `docs/architecture/2026-09-03-compact-current-state-change-record.md` Runtime View, Correction route and return; `specs/compact-current-state-change-record.md` Operation eligibility matrix, `return-correction`
Evidence: The architecture requires correction state to clear only after the return condition and required rereview are current and consistent. The specification instead says that `return-correction` clears routing state before that rereview. Clearing the only active correction at return loses the durable owner, return condition, and expected review while the correction is still awaiting settlement, and it contradicts the approved explicit-return direction.
Required outcome: Define return as a transition that records corrected content ready for the named required review while keeping the correction active. Define review settlement as the operation that closes the correction on approval or keeps/revises/blocks it for every non-approved outcome, with the finding remaining visible until valid resolution.
Safe resolution path: The specification owner should revise the return and settlement predicates and their state invariants, register only the corrected specification, return through Workflow, and request a fresh exact-package Design Review.
needs-decision rationale: none
Finding scope: artifact-local
Affected artifact IDs: spec
Owning stages: spec

### Finding CCSR-DR7-2

Finding ID: CCSR-DR7-2
Severity: major
Location: `specs/compact-current-state-change-record.md` SR-21, Inputs and outputs, Projection schema, and Operation eligibility matrix
Evidence: SR-21 and the closed Projection schema define requested-operation eligibility, but the normative projection input accepts only change identity, view or skill name, and output format. With no optional requested operation in that input, an implementation cannot determine which exact operation to evaluate without inventing an implicit selection rule. Such inference would make independent implementations disagree and could reintroduce the same global-status authorization ambiguity this refinement is intended to remove.
Required outcome: Add one optional requested operation to the projection input contract, define its behavior for each bounded view, and require exact agreement with `requested_operation` and `operation_eligibility`; absence must continue to produce null for both fields.
Safe resolution path: The specification owner should make the bounded input correction, update boundary and acceptance coverage where needed, register only the corrected specification, return through Workflow, and request a fresh exact-package Design Review.
needs-decision rationale: none
Finding scope: artifact-local
Affected artifact IDs: spec
Owning stages: spec

## Design coherence

The package correctly separates overall progression readiness from operation-specific eligibility and preserves global blockers without using them as a blanket authorization decision. The proposal, architecture, ADR, and most of the specification agree that a globally blocked change can expose an exact safe corrective operation. CCSR-DR7-1 and CCSR-DR7-2 remain material because the current closed contract otherwise gives incompatible correction lifetimes and no interoperable input for the new eligibility result.

## Proposal preservation

Both corrections implement decisions already approved by Proposal Review R6: explicit correction return remains review-bound, and operation-specific eligibility remains distinct from overall progression readiness. They do not broaden the product direction or require Git, pull-request state, caller authentication, or an external service.

## Independence statement

This review did not edit the proposal, architecture, specification, ADR, authoring evidence, or workflow routing state. CCSR-DR7-1 and CCSR-DR7-2 are recorded for the specification owner.
