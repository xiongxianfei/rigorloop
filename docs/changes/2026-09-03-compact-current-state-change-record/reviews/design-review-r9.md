# Design Review R9: Compact current-state correction and eligibility contract

Review ID: design-review-r9
Stage: design-review
Round: r9
Reviewer: Independent Codex design-review context
Reviewer authority: design-review
Target: design package `architecture`, `spec`, `adr-compact-current-state-transaction`
Reviewed artifact: design package `architecture`, `spec`, `adr-compact-current-state-transaction`
Review date: 2026-09-04
Package kind: design
Package members: architecture=docs/architecture/2026-09-03-compact-current-state-change-record.md, spec=specs/compact-current-state-change-record.md, adr-compact-current-state-transaction=docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md
Upstream review ID: proposal-review-r6
Status: approved
Material findings: none
Correction targets: none
Recording status: recorded

## Result

- Skill: design-review
- Review status: approved
- Package members: architecture=`docs/architecture/2026-09-03-compact-current-state-change-record.md`, spec=`specs/compact-current-state-change-record.md`, adr-compact-current-state-transaction=`docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md`
- Upstream review ID: proposal-review-r6
- Review ID and round: design-review-r9, r9
- Material findings: none
- Correction targets: none
- Recording status: recorded
- Settlement status: pending exact-package CLI settlement
- Open blockers: none at the Design judgment layer
- Immediate next stage: Workflow settlement, then Delivery package correction and review
- Claim limitations: approval covers this exact Design package; it does not approve the stale Delivery package, implementation, verification, branch, pull-request, release, or deployment readiness

## Package judgment

The proposal, architecture, specification, and ADR now define one coherent compact current-state model. Overall progression readiness and exact requested-operation eligibility are separately derived from the same normalized snapshot. Progression blockers remain visible without blanket-denying safe correction, and an optional exact projection input selects the operation being evaluated.

Explicit correction coordination is non-lossy. A semantic route input contains no derived state; the evaluator creates an `authoring` correction, return changes that same correction to `review-required`, and only settlement of its exact required review may clear it after valid finding dispositions. Non-approved settlement retains, coherently revises, blocks, or rejects the correction without losing its owner, return condition, findings, or expected review.

The package remains aligned on repository-local current-state sufficiency without Git or pull-request history, independent review, stable review replacement, material-decision retention, typed evidence freshness, observable multi-file atomicity, deterministic recovery, local execution trust, prospective adoption, bounded projections, and fail-closed closed vocabularies.

## Prior finding closeout

- CCSR-DR7-1 is resolved by the explicit `ActiveCorrection` phase, stored return stage, return transition, settlement behavior, invariant, EC13, and AC-13.
- CCSR-DR7-2 is resolved by the optional requested-operation projection input and its exact null/non-null output coherence.
- CCSR-DR8-1 is resolved by the separate closed `CorrectionInput`; `route-correction` no longer accepts caller-supplied correction kind or status.

## No-Finding Statement

Clean formal Design Review completed with no material findings against the exact R9 package.

## Independence statement

This review did not edit the proposal, architecture, specification, ADR, authoring evidence, or workflow routing state.
