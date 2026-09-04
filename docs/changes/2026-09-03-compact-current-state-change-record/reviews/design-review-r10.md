# Design Review R10: Milestone activation package coherence

Review ID: design-review-r10
Stage: design-review
Round: r10
Reviewer: Independent Codex design-review context
Reviewer authority: design-review
Target: design package `architecture`, `spec`, `adr-compact-current-state-transaction`
Reviewed artifact: design package `architecture`, `spec`, `adr-compact-current-state-transaction`
Review date: 2026-09-04
Package kind: design
Package members: architecture=docs/architecture/2026-09-03-compact-current-state-change-record.md, spec=specs/compact-current-state-change-record.md, adr-compact-current-state-transaction=docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md
Upstream review ID: proposal-review-r6
Status: changes-requested
Material findings: CCSR-DR10-1
Correction targets: architecture
Recording status: recorded

## Result

- Skill: design-review
- Review status: changes-requested
- Package members: architecture=`docs/architecture/2026-09-03-compact-current-state-change-record.md`, spec=`specs/compact-current-state-change-record.md`, adr-compact-current-state-transaction=`docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md`
- Upstream review ID: proposal-review-r6
- Review ID and round: design-review-r10, r10
- Material findings: CCSR-DR10-1
- Correction targets: architecture, owned by architecture
- Recording status: recorded
- Settlement status: withheld pending exact-package CLI settlement of the changes-requested outcome
- Open blockers: CCSR-DR10-1 and upstream CCSR-M3-CR7
- Immediate next stage: architecture authoring owner through Workflow correction routing
- Claim limitations: this outcome grants no Design package authority and does not authorize Delivery, implementation, verification, branch, pull-request, release, or deployment readiness

### Finding CCSR-DR10-1

Finding ID: CCSR-DR10-1
Severity: major
Location: `docs/architecture/2026-09-03-compact-current-state-change-record.md` Building Block View, Runtime View, and quality scenarios
Evidence: Corrected SR-46 now defines typed pending milestone work, explicit `null → planned` selection, evaluator-derived active state, removal from `remaining_work`, reviewed closure, next-milestone routing, and stale retry behavior. The architecture still describes only generic current milestone state and contains no component responsibility or runtime flow for selecting the first or next milestone. Delivery and implementation could therefore choose incompatible sources, mutate remaining work differently, or reintroduce plan-prose parsing or caller-constructed coordination.
Required outcome: Architecture must assign typed remaining-work selection to the current-state coordinator and pure evaluator, define the selection/closure runtime flow and retry boundary, preserve route as semantic ID selector rather than state constructor, and add a multi-milestone quality scenario consistent with SR-46.
Safe resolution path: Revise only the canonical architecture, register its exact identity through the Architecture stage, return through Workflow, and perform a fresh consolidated Design Review of the unchanged Specification, corrected Architecture, and applicable ADR.
needs-decision rationale: none; SR-46 fixes the observable behavior and Architecture owns its technical realization.
Finding scope: artifact-local
Affected artifact IDs: architecture
Owning stages: architecture

## Design coherence

The specification correction is bounded and coherent: it preserves one active-work record, avoids procedural history, accepts only a current milestone ID as semantic input, and lets the evaluator construct coordination. The transaction ADR remains applicable and unchanged because selection is another ordinary exact-set semantic mutation. The package cannot be approved until Architecture realizes that behavior explicitly.

## Independence statement

This review did not edit any package member, authoring evidence, or workflow state. It inspected the complete exact package and records one architecture-local reconciliation finding.
