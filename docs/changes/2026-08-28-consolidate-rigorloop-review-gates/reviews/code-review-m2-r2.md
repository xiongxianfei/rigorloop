# Code Review M2 R2: Explicit Review Package Authority

Review ID: code-review-m2-r2
Stage: code-review
Round: r2
Reviewer: Codex independent rereview with fresh-assumption reset
Review date: 2026-08-30
Target: M2 working-tree packet `sha256:d61a2f17de8238b9e88b9f953d95653bf0c566fc4c10a20d66350bffd72be165`
Reviewed milestone: M2
Reviewed artifact: explicit review-package correction diff based on `9b0a7ba6b1d8841cfb5daf421f4230bfaefb3a6e`
Status: changes-requested
Review status: changes-requested
Material findings: CRG-M2-CR6, CRG-M2-CR7, CRG-M2-CR5
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/reviews/code-review-m2-r2.md`, `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-log.md`, and `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-resolution.md`
- Open blockers: CRG-M2-CR6, CRG-M2-CR7, CRG-M2-CR5
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CRG-M2-CR6, CRG-M2-CR7, CRG-M2-CR5
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/reviews/code-review-m2-r2.md`
- Review log: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-log.md`
- Review resolution: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-resolution.md`
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: CRG-M2-CR6, CRG-M2-CR7, CRG-M2-CR5
- Verify readiness: not-claimed

## Review inputs

- Actual diff: working-tree M2 correction packet at the target identity above.
- Governing authority: CRG-R22 through CRG-R34 in `specs/consolidated-review-gates.md`, the consolidated package ADR, M2 plan scope, and CRG-T04 through CRG-T10 in the test specification.
- Implementation evidence: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/evidence/m2-aggregate-review-packages-implementation.md`.
- Validation inspected: focused lifecycle 63/63, full package 288/288, review-artifact 104/104, metadata 66/66, governed-CLI 5/5, lifecycle consistency pass.

## Actual-diff summary

The correction removes aggregate and member hashes from package authority, exposes exact artifact ID-to-path maps, binds upstream and package review IDs, invalidates approved packages on governed member revision, makes non-approved states blocking, and validates finding owners and correction targets. The no-hash direction is coherent, and CRG-M2-CR3 and CRG-M2-CR4 are resolved. Three progression paths remain incomplete.

## Finding CRG-M2-CR6

Finding ID: CRG-M2-CR6
Severity: major
Location: `packages/rigorloop/dist/lib/lifecycle-operations.js:754-764`
Evidence: `settle-review-package` returns `already-recorded` at line 758 before rereading the registered review evidence and review log at lines 763-764. Changing that evidence after settlement therefore bypasses the exact-replay requirement even though CRG-R26 requires an identical review decision and current evidence.
Required outcome: Exact replay must revalidate current package facts and registered review evidence before returning `already-recorded`.
Safe resolution path: Move replay recognition after context and evidence revalidation, then add a public CLI regression that changes review evidence after settlement and expects stale evidence with no mutation.
needs-decision rationale: none

## Finding CRG-M2-CR7

Finding ID: CRG-M2-CR7
Severity: major
Location: `packages/rigorloop/dist/lib/lifecycle-packages.js:86-92`
Evidence: For every current registered review, line 90 chooses `settle-review-package`, including after a `changes-requested`, `blocked`, or `inconclusive` decision is already settled. The blocker then advertises that replay as its corrective operation. CRG-R29 instead requires correction routing for changes requested, an upstream resolution or stop for blocked, and evidence acquisition plus rereview for inconclusive.
Required outcome: Each non-approved settled status must expose one outcome-specific safe next action and must not recommend replaying an already settled decision.
Safe resolution path: Derive the next operation from package status and correction targets; reserve `settle-review-package` for a recorded but unsettled review, and add status assertions for all non-approved outcomes.
needs-decision rationale: none

## Finding CRG-M2-CR5

Finding ID: CRG-M2-CR5
Severity: major
Location: `packages/rigorloop/dist/lib/lifecycle-operations.js:701-733`; `packages/rigorloop/dist/lib/lifecycle-packages.js:58-72,86-92`
Evidence: Proposal settlement can replace `artifact_states.proposal.review.id`, but `settle-artifact` never invalidates an approved design package. Package context reads the new Proposal Review ID while continuing to trust the old projection's `approved` status, so the old design approval can retain authority against a different upstream review. Delivery invalidation exists for replacement Design Review, making the missing Proposal Review path asymmetric.
Required outcome: Replacing the bound Proposal Review ID must atomically set the approved design package to `review-required`, withhold authority, and retain its prior review ID as history.
Safe resolution path: Add the same dependent-package invalidation to successful proposal settlement and a public CLI regression covering Proposal Review replacement.
needs-decision rationale: none

## Checklist coverage

| Item | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | CRG-R24, CRG-R26, and CRG-R29 remain incomplete on replacement upstream review, exact replay, and next-action semantics. |
| Test coverage | concern | Broad proof passes, but no test changes settled review evidence, replaces Proposal Review, or asserts the post-settlement action for each non-approved outcome. |
| Edge cases | block | Evidence replay and replacement-upstream temporal paths can preserve stale authority. |
| Error handling | concern | Non-approved states block, but their corrective operation is misleading. |
| Architecture boundaries | block | Proposal Review replacement does not invalidate its dependent design authority. |
| Compatibility | pass | Obsolete aggregate fields are removed consistently from runtime, schema, validators, and the detailed fixture. |
| Security/privacy | pass | No new external, secret, credential, or personal-data surface was added. |
| Derived artifact currency | pass | Runtime, schema, validators, tests, and the exact output fixture agree on explicit path maps. |
| Unrelated changes | pass | The reviewed packet is bounded to M2 corrections and their governing evidence. |
| Validation evidence | pass | All named implementation suites pass; remaining findings are missing temporal and routing assertions rather than failing reported commands. |

## Direct-proof assessment

The governed member-revision, direct-edit limitation, atomic rollback, explicit map, no-hash, and owner-mapping paths have direct tests. The three findings above lack direct proof and are visible from public evaluator ordering and status derivation. A clean result is not supportable until those paths are corrected and rereviewed.

## Handoff

This formal review is isolated. There is no automatic downstream handoff or implementation fix. M2 remains open; review-resolution and an implementation correction are required before another M2 rereview. M3 must remain paused.
