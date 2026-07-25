# Proposal Review R2

Review ID: proposal-review-r2
Stage: proposal-review
Round: 2
Reviewer: Codex proposal-review
Target: docs/proposals/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism.md
Status: changes-requested
Material findings: BRF-PR5
Architecture assessment: architecture-required
Scope-preservation result: pass
Immediate next stage: proposal revision
Automatic downstream handoff: none

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: `BRF-PR5`
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/proposal-review-r2.md
- Review log: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md
- Review resolution: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md
- Open blockers: proposal-review target activation is circular under the current authoring-grant minimum basis
- Immediate next stage: proposal revision
- Spec readiness: not ready

## Material Findings

### BRF-PR5 - Proposal-review target has circular grant basis

Finding ID: BRF-PR5
Severity: major
Location: `Target and authority are independent`, `Identity-bound grant envelope`, and `Expanded target boundary`
Evidence: The public target vocabulary includes `proposal-review`, but the minimum basis for an `authoring` grant requires a clean proposal gate. A clean proposal gate already depends on an approved proposal review, so the single mechanism cannot authorize its first public review target from a reviewable proposal without circular evidence. The proposal does not define a pre-review grant basis, a stage-scoped basis refresh, or removal of `proposal-review` from the public target set.
Required outcome: Define a deterministic non-circular authorization path for the proposal-review target while preserving the rule that no transition beyond proposal-review can rely on an unapproved proposal.
Safe resolution path: Keep `proposal-review` as a public target and define stage-scoped authoring authority: proposal-review invocation binds to a reviewable proposal identity, standing artifact gates, change identity, target, and review-only mutation scope; continuation to `spec` or later requires a clean recorded proposal gate plus a refreshed or newly authorized post-proposal authoring grant. Alternatively, remove `proposal-review` from the public target vocabulary and explicitly preserve proposal-to-proposal-review outside the automated mechanism, but that alternative conflicts with the stated goal that `bounded-review-fix` is the only workflow automation mechanism.
Needs-decision rationale: The proposal owner must choose the grant boundary. The recommended choice is a review-only pre-proposal-gate grant followed by a separately identity-bound post-proposal authoring grant.

## Prior Finding Recheck

| Finding | Result | Evidence |
| --- | --- | --- |
| `BRF-PR1` | resolved | The proposal defines evidence-derived pre-plan position, fail-closed ambiguity, and handoff to the validated active plan. |
| `BRF-PR2` | resolved | Grants now bind stable identity, policy version, reviewed basis, mutation scope, and invalidation behavior. |
| `BRF-PR3` | resolved | The transition protocol now writes prepared receipts before mutation and defines retry and reconciliation behavior. |
| `BRF-PR4` | resolved | Targets now include occurrence identity and completion predicates, with milestone-local and final review separated. |

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The mechanism-duplication problem is explicit. |
| User value | pass | One automation model reduces routing and persistence drift. |
| Option diversity | pass | Five materially different options are compared, including do nothing. |
| Decision rationale | pass | Expanding the existing target-driven mechanism follows the stated criteria. |
| Scope control | pass | External actions, background execution, blanket authority, and immediate command renaming remain excluded. |
| Architecture awareness | pass | State ownership, grants, receipts, registry, migration, and ADR impact are visible. |
| Testability | concern | The new acceptance criteria are strong, but proposal-review activation lacks a non-circular basis to test. |
| Risk honesty | pass | Stale grants, recovery, duplicate writers, review independence, migration, and rollback risks are explicit. |
| Rollout realism | pass | One-way active migration plus indefinite historical reads is credible. |
| Readiness for spec | block | `BRF-PR5` requires one proposal-level authorization decision. |

## Scope Preservation Review

- Scope-preservation result: pass. Every initial user goal is classified, and the mechanism-versus-command distinction remains explicit.

## Recommended Proposal Edits

- Add a proposal-review-specific authorization basis that does not require prior proposal-review approval.
- Restrict that authority to invoking and recording proposal review; do not permit proposal mutation during the review pass.
- Require a clean recorded proposal gate and a separately identity-bound post-proposal authoring grant before `spec` or any later target can execute.
- Replace the stale `target_stage` wording with structured `target` terminology while revising the section.
- Add acceptance proof for pre-gate review authorization, post-gate grant separation, stale proposal identity, and forbidden continuation beyond proposal-review.

## Recommendation

- Recommendation: `changes-requested`. The R1 findings are resolved, but `BRF-PR5` must settle proposal-review activation before the proposal is ready for spec. This direct review remains isolated and performs no automatic downstream handoff.
