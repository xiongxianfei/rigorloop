# Design Review R11: Milestone selection and compact-state coherence

Review ID: design-review-r11
Stage: design-review
Round: r11
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
- Review ID and round: design-review-r11, r11
- Material findings: none
- Correction targets: none
- Recording status: recorded
- Settlement status: pending exact-package CLI settlement
- Open blockers: none at the Design judgment layer
- Immediate next stage: Workflow settlement, then Delivery plan reconciliation and review
- Claim limitations: approval covers this exact Design package; it does not approve the stale Delivery package, implementation, verification, branch, pull-request, release, or deployment readiness

## Package judgment

The package now defines one complete milestone-selection contract without relying on Git, pull-request state, plan-prose parsing, or caller-constructed coordination. Specification SR-46 accepts only the exact pending milestone identity plus the bounded `null` to `planned` transition. The evaluator verifies the typed `remaining_work` entry, removes that entry, constructs `active_work`, rejects ambiguous or stale retries, and clears active work only through reviewed milestone closure.

Architecture assigns the same behavior to the current-state coordinator and pure transition evaluator. Its runtime sequence covers first selection, code-review closure, return to `implement` when another milestone remains, explicit next selection, and deterministic retry. The transaction ADR already governs the resulting exact-set multi-file mutation, so no new ADR is required.

The package remains coherent on current-state sufficiency, independent review, explicit non-adjacent correction return, stable review replacement, material-decision retention, evidence freshness, fail-closed vocabularies, atomic mutation, deterministic recovery, local execution trust, prospective adoption, and bounded projections.

## Prior finding closeout

- CCSR-M3-CR7 is resolved by SR-46, the typed `RemainingWorkItem`, the nullable milestone-activation payload, exact eligibility and mutation rules, EC14, AC-14, and the matching architecture runtime.
- CCSR-DR10-1 is resolved by coordinator ownership, evaluator-derived activation, explicit milestone selection and progression steps, retry behavior, and the multi-milestone quality scenario.

## No-Finding Statement

Clean formal Design Review completed with no material findings against the exact R11 package.

## Independence statement

This review did not edit the proposal, architecture, specification, ADR, authoring evidence, or workflow routing state.
