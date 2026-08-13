# Proposal Review R2: Plan Skill Simplification

Review ID: proposal-review-r2
Stage: proposal-review
Round: r2
Reviewer: external independent proposal-review result supplied by the user
Target: `docs/proposals/2026-08-12-plan-skill-simplification.md`
Reviewed artifact: commit `65b32cb1`
Review date: 2026-08-13
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: PLSIM-PR4, PLSIM-PR5, PLSIM-PR6
- Open blockers: new-plan bootstrap, review-settled initialization, and milestone-format compatibility require proposal revision
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this review does not approve the proposal, authorize specification, or continue the workflow

## Finding identity mapping

The supplied second-round review reused first-round labels `PLSIM-PR1`, `PLSIM-PR2`, and `PLSIM-PR3` for new findings. This durable record assigns unique change-local identities while preserving the supplied order and substance:

| Supplied label | Durable finding ID |
| --- | --- |
| `PLSIM-PR1` | `PLSIM-PR4` |
| `PLSIM-PR2` | `PLSIM-PR5` |
| `PLSIM-PR3` | `PLSIM-PR6` |

## Overall assessment

The proposal retains the correct package design: a shorter portable `SKILL.md`, one governed plan-authoring reference, the existing boundary reference, exactly three structural assets, and `change.yaml` as the only current milestone-state owner. Portable and governed planning are separated at a real authority boundary, universal planning quality remains inline, and measurement separates procedural context from copied structure.

Three lifecycle contracts still need closure. Governed creation currently requires an identity it is meant to create, pre-review `planned_work` initialization can diverge after plan-review revision, and the old/new milestone format lacks an explicit activation and compatibility boundary.

## Material findings

### PLSIM-PR4 — Major: governed new-plan creation is circular

Finding ID: PLSIM-PR4
Severity: major
Location: Invocation classification and resource loading; Governed reference ownership
Evidence: `governed_change_context` requires an existing plan artifact identity while the governed reference also owns primary plan and plan-entry creation. A legitimate first plan has a valid governed change and deterministic intended path but no pre-existing plan identity. The proposal cannot currently distinguish that case from a missing or inconsistent plan.
Required outcome: Separate governed change authority from plan operation, with closed `create-primary-plan` and `revise-primary-plan` behavior and fail-closed file/entry identity checks.
Safe resolution path: For creation, require one governed change, settled prerequisites, plan-authoring authority, and deterministic intended path; require both file and plan entry to be absent; write the candidate plan, compute its identity, then create the matching entry. For revision, require one present matching entry and file identity. Stop on asymmetry, mismatch, or multiple primary candidates.
needs-decision rationale: none; the proposal must close its own bootstrap sequence.

### PLSIM-PR5 — Major: `planned_work` initialization conflicts with review-driven plan revision

Finding ID: PLSIM-PR5
Severity: major
Location: Universal `SKILL.md` ownership; Governed reference ownership; lifecycle compatibility
Evidence: The proposal initializes `planned_work` from a draft plan before `plan-review`, then prohibits `plan` from replacing or updating it. `plan-review` may request milestone, sequencing, proof, or dependency changes, which would leave the revised plan inconsistent with already-initialized state. No owner or restart protocol reconciles the definitions.
Required outcome: Initialize live `planned_work` only from an approved plan and plan-review identity, or define an equally explicit invalidation protocol. Amend the current pre-review initialization contract directly.
Safe resolution path: Select post-approval initialization. Plan authoring writes stable plan content and requests review without creating `planned_work`. After clean settlement, a bounded plan-owned initializer creates missing state exactly once from the approved identity. Identical retry is a no-op; any existing mismatch stops. Post-initialization substantive milestone changes route to a governed replan or migration contract.
needs-decision rationale: none; post-approval initialization is the smallest coherent ownership model.

### PLSIM-PR6 — Major: milestone-format migration lacks a closed read-old/write-new contract

Finding ID: PLSIM-PR6
Severity: major
Location: Asset ownership and milestone-state migration; Rollout and Rollback
Evidence: The proposal says new assets omit mutable state, historical plans remain readable, and live consumers move to `change.yaml`, but it does not decide the write activation, old active-plan behavior, source precedence on disagreement, incomplete `planned_work`, dual-parser compatibility, or literal retirement sequence.
Required outcome: Adopt an explicit read-old/write-new compatibility model with `stage-owned-change-local-v1` as the current-state authority marker and closed failure behavior for active legacy plans.
Safe resolution path: New governed writers emit stable intent only. Readers accept old and new stable structures, but current governed state comes exclusively from complete `change.yaml#workflow_state.planned_work`. Historical terminal plans remain unchanged. Active governed plans with missing/incomplete authoritative state or identity/kind conflicts stop for explicit workflow-owned migration. Prohibit reverse synchronization in either direction.
needs-decision rationale: none; compatibility must be closed before parser migration.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Portable planning, governed mutation, and stale plan-body state are concrete. |
| User value | pass | Both portable and governed planning should become easier to scan. |
| Option diversity | pass | The alternatives are materially different. |
| Decision rationale | pass | One conditional reference remains proportionate. |
| Vision fit | pass | The change strengthens reviewable and durable planning. |
| Scope control | pass | Work remains bounded to `plan` and directly coupled consumers. |
| Architecture awareness | pass | Existing architecture likely suffices after bounded assessment and direct contract amendment. |
| Testability | block | Creation, initialization settlement, and old/new compatibility are not yet deterministic. |
| Risk honesty | concern | The proposal recognizes parser migration but not the full activation boundary. |
| Rollout realism | block | Active legacy plans and pre-review initialized state lack a closed migration path. |
| Readiness for spec | block | PLSIM-PR4 through PLSIM-PR6 require proposal revision. |

## Scope Preservation Review

- Scope-preservation result: pass. All initial user goals remain visible. The findings close the selected package's lifecycle behavior without adding a runtime, skill, reference family, asset, or new persistence model.

## Recommended Proposal Edits

- Separate governed authority from `create-primary-plan` and `revise-primary-plan` operation classification.
- Move one-time `planned_work` initialization after clean plan-review settlement and define post-initialization replan behavior.
- Add an explicit read-old/write-new matrix and forbid inference or reverse synchronization from historical plan-body state.

## Recommendation

- Recommendation: revise the proposal to resolve PLSIM-PR4 through PLSIM-PR6, then rerun independent `proposal-review` against a frozen revision. No automatic downstream handoff follows this review.

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-12-plan-skill-simplification/reviews/proposal-review-r2.md`
- Finding-record paths: `docs/changes/2026-08-12-plan-skill-simplification/reviews/proposal-review-r2.md`

## Formal-settlement group

- Review ID: proposal-review-r2
- Review record: `docs/changes/2026-08-12-plan-skill-simplification/reviews/proposal-review-r2.md`
- Review log: `docs/changes/2026-08-12-plan-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-12-plan-skill-simplification/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-12-plan-skill-simplification`
- Formal next-stage eligibility: proposal revision only
