# Proposal Review R3

Review ID: proposal-review-r3
Stage: proposal-review
Round: 3
Reviewer: Codex proposal-review
Target: docs/proposals/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism.md
Status: changes-requested
Material findings: BRF-PR6, BRF-PR7
Architecture assessment: architecture-required
Scope-preservation result: pass
Immediate next stage: proposal revision
Automatic downstream handoff: none

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: `BRF-PR6`, `BRF-PR7`
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/proposal-review-r3.md
- Review log: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md
- Review resolution: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md
- Open blockers: the grant invariant contradicts the proposal-review exception, and the valid `inconclusive` review outcome has no target semantics
- Immediate next stage: proposal revision
- Spec readiness: not ready

## Material Findings

### BRF-PR6 - The common grant invariant contradicts the pre-review capability

Finding ID: BRF-PR6
Severity: major
Location: `Target and authority are independent`, `Identity-bound grant envelope`, `Proposal-review bootstrap without circular authority`, and `AC-BRF-033`
Evidence: The proposal correctly gives `proposal-review` an effective capability whose concrete basis is an exact reviewable proposal rather than a clean review. However, the common invariant still says every grant has a "concrete reviewed basis," every grant records artifact and review identities, and `AC-BRF-033` requires every grant to bind a reviewed basis. Those universal statements either exclude the proposed pre-review capability or recreate the circular approval requirement that `BRF-PR5` was intended to remove. The bounded parent authorization that derives effective capabilities is also named as the authority root but is not explicitly covered by the stable identity, policy version, authorizer, maximum scope, revocation, and invalidation contract.
Required outcome: Define one internally consistent two-level authorization contract: a durable bounded parent authorization with explicit identity and maximum scope, and an effective capability with a concrete stage-appropriate basis. Review identities are required only when the stage basis can legitimately contain them.
Safe resolution path: Replace "concrete reviewed basis" with "concrete stage-appropriate basis" in the common invariant and acceptance criteria; make review identities conditional; define the parent authorization's minimum identity, policy, authorizer, change, target, maximum scope, revocation, and invalidation fields; and require every derived capability to bind both its parent identity and its concrete stage basis.
Needs-decision rationale: The proposal owner must settle the authoritative two-level invariant before the spec can define grants without choosing between contradictory proposal rules.

### BRF-PR7 - The valid inconclusive review outcome has no deterministic target behavior

Finding ID: BRF-PR7
Severity: major
Location: `Expanded target boundary`, proposal-review completion semantics
Evidence: The proposal defines proposal-review completion only for `approved`, `changes-requested`, and `blocked`. The governing proposal-review contract has a fourth valid closed outcome, `inconclusive`. Because `inconclusive` is known rather than an unknown value, the proposal's generic unknown-value fail-closed rule does not decide whether the review occurrence is recorded as reached, whether the run pauses, or whether a later target may continue.
Required outcome: Define deterministic behavior for every closed proposal-review outcome while ensuring that only `approved` satisfies the clean proposal gate.
Safe resolution path: Treat all four outcomes as durably recorded review evidence; let `approved` satisfy the gate, let `changes-requested` enter correction only with a valid correction capability, and make `blocked` and `inconclusive` pause without satisfying the gate or continuing to later targets. Add direct acceptance proof for all four outcomes and an unknown-outcome regression.
Needs-decision rationale: The proposal owner must settle whether target occurrence completion and clean-gate satisfaction are separate states; the recommended split preserves review evidence without treating inconclusive review as approval.

## Prior Finding Recheck

| Finding | Result | Evidence |
| --- | --- | --- |
| `BRF-PR1` | resolved | Pre-plan derivation and the validated-plan ownership handoff remain deterministic. |
| `BRF-PR2` | resolved | Effective grants remain identity- and scope-bound; `BRF-PR6` concerns the newly introduced parent/effective hierarchy rather than reopening status-only grants. |
| `BRF-PR3` | resolved | Prepared receipts and evidence-first transition recovery remain defined. |
| `BRF-PR4` | resolved | Repeated targets remain bound to occurrence identities and completion predicates. |
| `BRF-PR5` | resolved | The proposal now includes a review-only capability bound to the exact proposal identity, separates correction, and requires a concrete clean gate before post-proposal authoring. |

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The duplicated-mechanism problem remains explicit. |
| User value | pass | A single mechanism provides concrete routing, status, and resume value. |
| Option diversity | pass | Five materially different options, including do nothing, are compared. |
| Decision rationale | pass | The selected engine follows the proposal's stated criteria. |
| Scope control | pass | External actions, background execution, blanket risk escalation, and immediate command renaming remain excluded. |
| Architecture awareness | pass | State ownership, authority derivation, transition recovery, policy registry, and migration boundaries are visible. |
| Testability | concern | The proof map is strong, but the contradictory common grant invariant and missing `inconclusive` branch prevent exhaustive fixtures. |
| Risk honesty | pass | The new parent-authorization and circular-review risks are explicitly acknowledged. |
| Rollout realism | pass | Dual-read, single-write migration and state-based legacy retirement remain credible. |
| Readiness for spec | block | `BRF-PR6` and `BRF-PR7` require proposal-level closure. |

## Scope Preservation Review

- Scope-preservation result: pass. All initial user goals remain classified, including the explicit inclusion of `proposal-review` in the single mechanism.

## Recommended Proposal Edits

- Replace universal "reviewed basis" wording with a stage-appropriate basis invariant and make review identities conditional.
- Add a minimum durable envelope for bounded parent authorizations and require derived capabilities to bind its identity.
- Separate review-occurrence recording from clean-gate satisfaction.
- Define `approved`, `changes-requested`, `blocked`, and `inconclusive` routing, plus unknown-outcome failure.
- Add acceptance criteria and fixtures for the parent/effective authority link and every proposal-review outcome.

## Recommendation

- Recommendation: `changes-requested`. The R2 circularity finding is resolved in direction, but the common invariant and outcome matrix need one focused proposal revision before specification. This direct review remains isolated and performs no automatic downstream handoff.
