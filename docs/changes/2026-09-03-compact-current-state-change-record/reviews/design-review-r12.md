# Design Review R12: Review outcomes and bootstrap closeout

Review ID: design-review-r12
Stage: design-review
Round: r12
Reviewer: Independent Codex design-review context
Reviewer authority: design-review
Target: design package `architecture`, `spec`, `adr-compact-current-state-transaction`
Reviewed artifact: design package `architecture`, `spec`, `adr-compact-current-state-transaction`
Review date: 2026-09-04
Package kind: design
Package members: architecture=docs/architecture/2026-09-03-compact-current-state-change-record.md, spec=specs/compact-current-state-change-record.md, adr-compact-current-state-transaction=docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md
Upstream review ID: proposal-review-r7
Status: changes-requested
Material findings: CCSR-DR12-1, CCSR-DR12-2
Correction targets: architecture, spec, adr-compact-current-state-transaction
Recording status: recorded

## Result

- Skill: design-review
- Review status: changes-requested
- Package members: architecture=`docs/architecture/2026-09-03-compact-current-state-change-record.md`, spec=`specs/compact-current-state-change-record.md`, adr-compact-current-state-transaction=`docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md`
- Upstream review ID: proposal-review-r7
- Review ID and round: design-review-r12, r12
- Material findings: CCSR-DR12-1, CCSR-DR12-2
- Correction targets: architecture and adr-compact-current-state-transaction owned by architecture; spec owned by spec
- Recording status: recorded
- Settlement status: withheld pending exact-package CLI settlement
- Open blockers: CCSR-DR12-1, CCSR-DR12-2, plus legacy-resurrected CCSR-M3-CR2
- Immediate next stage: architecture correction, then specification reconciliation
- Claim limitations: this review grants no Design, Delivery, implementation, or final readiness authority

### Finding CCSR-DR12-1

Finding ID: CCSR-DR12-1
Severity: major
Location: Architecture stable-review/evaluator/correction sections, Specification `ReviewOutcome` and settlement rules, and ADR review replacement boundary
Evidence: The accepted Proposal now separates review judgment, explicit decision-owner acceptance, and lifecycle progression. The Specification still defines `ReviewOutcome` as `approved | changes-requested | blocked | inconclusive` and requires approval for progression, correction closure, milestone closure, and Verify. Architecture and the ADR do not define a clear exact-subject judgment as distinct from a material owner decision.
Required outcome: Define one current review judgment model in which a clear exact-subject review with no blocking findings satisfies the ordinary review prerequisite, explicit acceptance is retained only for material owner decisions, and progression remains mechanically derived rather than stored as another approval.
Safe resolution path: Architecture and ADR define the responsibility and transaction boundary; Specification defines exact vocabulary and transition behavior; then perform a fresh consolidated Design Review.
needs-decision rationale: none; Proposal Review R7 settled the direction.
Finding scope: cross-artifact
Affected artifact IDs: architecture, spec, adr-compact-current-state-transaction
Owning stages: architecture, spec

### Finding CCSR-DR12-2

Finding ID: CCSR-DR12-2
Severity: major
Location: Architecture compatibility sections, Specification SR-34/SR-35 and BND-COMPAT rows, and ADR activation decision
Evidence: All three members require every in-flight legacy change, including this implementing change, to finish solely under its registered contract. The accepted Proposal now authorizes one bounded preactivation closeout that binds this change to an exact-current-set identity, validates current consequential state without Git or PR identity, ignores already-settled superseded procedure, and activates compact writing only after clear final review and passing Verify.
Required outcome: Define the implementing-change bootstrap as one closed compatibility exception, its exact-current-set identity inputs, current-only validation boundary, failure behavior, non-migration constraint, and atomic activation condition.
Safe resolution path: Revise Architecture and ADR first, reconcile exact observable requirements and boundaries in Specification, then obtain fresh Design and Delivery review before implementation correction.
needs-decision rationale: none; Proposal Review R7 explicitly accepted the bounded exception.
Finding scope: cross-artifact
Affected artifact IDs: architecture, spec, adr-compact-current-state-transaction
Owning stages: architecture, spec

## Design coherence

The existing package remains coherent for compact persistence, recovery, evidence freshness, projections, and prospective legacy compatibility. It is not coherent with the newly accepted outcome semantics or implementing-change bootstrap, so Delivery cannot safely rely on it.

## Independence statement

This review did not edit any package member, authoring evidence, or lifecycle state. It reviewed the exact current package against Proposal Review R7.
