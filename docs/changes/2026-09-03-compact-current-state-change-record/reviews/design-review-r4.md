# Design Review R4: Compact Current-State Change Record

Review ID: design-review-r4
Stage: design-review
Round: r4
Reviewer: Independent Codex design-review context
Reviewer authority: design-review
Target: design package `architecture`, `spec`, `adr-compact-current-state-transaction`
Reviewed artifact: design package `architecture`, `spec`, `adr-compact-current-state-transaction`
Review date: 2026-09-04
Package kind: design
Package members: architecture=docs/architecture/2026-09-03-compact-current-state-change-record.md, spec=specs/compact-current-state-change-record.md, adr-compact-current-state-transaction=docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md
Upstream review ID: proposal-review-r1
Status: approved
Material findings: none
Correction targets: none
Recording status: recorded

## Result

- Skill: design-review
- Review status: approved
- Package members: architecture=`docs/architecture/2026-09-03-compact-current-state-change-record.md`, spec=`specs/compact-current-state-change-record.md`, adr-compact-current-state-transaction=`docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md`
- Upstream review ID: proposal-review-r1
- Review ID and round: design-review-r4, r4
- Material findings: none
- Correction targets: none
- Recording status: recorded
- Settlement status: pending exact-package CLI settlement
- Open blockers: none at the Design judgment layer; M1 implementation findings remain owned downstream
- Immediate next stage: Workflow returns the existing M1 correction to Implementation after settlement
- Claim limitations: approval covers only the exact corrected Design package; it does not approve M1 implementation, close a Code Review finding, restore Delivery authority by itself, or establish verification or external readiness

## Correction review

The R4 delta adds `change_id`, `lifecycle_contract`, and `lifecycle_revision` to the normative exact Projection shape. This directly reconciles SR-21 with SR-39: every bounded projection is attributable without an enclosing transport, and the closed schema no longer forbids identities required by skill context. The change does not alter the five-surface model, transaction boundary, semantic ownership, evidence freshness, compatibility, or no-Git/no-PR correctness constraints.

The architecture's projection service and resumability scenarios already require current lifecycle identity and remain coherent with the corrected shape. The ADR requires projections derived solely from the current authoritative set and does not prescribe a conflicting envelope. The accepted proposal likewise requires bounded current-state projections without external history. No architecture or ADR edit is necessary for this bounded schema reconciliation.

## Boundary and package judgment

The correction strengthens BND-AUTH-002 and BND-COMPOSE-001 by making attribution explicit in each closed view. INT-003 remains coherent because renderers and enclosing result envelopes cannot substitute or invent those identities. No boundary partition, authority owner, recovery state, compatibility behavior, or example outcome changed.

## Independence statement

This review did not edit the proposal, architecture, specification, ADR, implementation, authoring evidence, or workflow routing state.

## No-Finding Statement

Clean formal Design Review completed with no material findings against the exact R4 package.
