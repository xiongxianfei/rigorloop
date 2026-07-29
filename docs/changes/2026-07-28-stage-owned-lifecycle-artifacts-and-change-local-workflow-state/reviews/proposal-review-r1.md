# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Codex proposal-review skill
Target: docs/proposals/2026-07-28-approved-specification-baselines-and-controlled-amendment-workflow.md
Status: changes-requested
Original review source: User-invoked `$proposal-review` on 2026-07-28.
Material findings: SLA-PR1, SLA-PR2, SLA-PR3
Scope-preservation result: changes-requested
Immediate next stage: proposal revision
Automatic downstream handoff: none

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: SLA-PR1, SLA-PR2, SLA-PR3
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/proposal-review-r1.md
- Review log: docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/review-log.md
- Review resolution: docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/review-resolution.md#proposal-review-r1
- Open blockers: SLA-PR1, SLA-PR2, SLA-PR3
- Immediate next stage: proposal revision

## Material Findings

## Finding SLA-PR1

Finding ID: SLA-PR1
Severity: major
Location: Goals lines 37-46, Peer-stage ownership, Current workflow state lines 219-221, and CONSTITUTION.md lines 90-98
Evidence: The proposal gives the authoring stage exclusive ownership of artifact content and status, makes the review peer read-only, and makes workflow writable only toward `change.yaml`. It also says every later authoring-stage revision makes the earlier review stale. Current governance requires lifecycle-managed artifacts to carry durable embedded statuses such as `accepted` or `approved`. The proposal does not explain how a reviewed `draft` becomes durable: review or workflow changing it violates ownership, while the author changing it after review would stale the approval and repeat the cycle.
Required outcome: Define one finite settlement rule for embedded lifecycle status, or explicitly replace embedded lifecycle status with another authoritative surface and account for the governance change.
Safe resolution path: Prefer a narrow owner-performed settlement step whose allowed mutation is only the review outcome's corresponding status, with review evidence explicitly covering the candidate content and settlement rule; alternatively remove embedded status authority in the same governance change. State whether status-only settlement stales review and apply the answer consistently to every author-review pair.
needs-decision rationale: The proposal owner must choose the lifecycle model; specification must not invent the authority boundary.

## Finding SLA-PR2

Finding ID: SLA-PR2
Severity: major
Location: Testing and Verification Strategy lines 321-336 and Decision Log line 389
Evidence: The proposal says review and verification should inspect the final diff for cross-stage write-back and treats Git and PR review as sufficient audit surfaces. A final diff identifies changed paths and content, but it does not identify which skill invocation performed a write. The central claim is stage-specific, so path inspection alone cannot distinguish an authorized owner revision from a prohibited downstream revision.
Required outcome: Name a portable proof surface that can test stage-specific write behavior without reintroducing hashes, protected paths, or runtime interception, or narrow the proposal's mechanically verified claim.
Safe resolution path: Add static skill-contract checks for explicit owned outputs and read-only inputs, plus bounded fixture invocations that snapshot the fixture tree before and after each stage and assert that only declared outputs changed. Keep final PR diff review as defense in depth, not attribution proof. If invocation fixtures are out of scope, state that v1 provides guidance-and-review assurance rather than deterministic enforcement.
needs-decision rationale: The proposal owner must choose whether v1 promises behavioral proof or guidance-only assurance.

## Finding SLA-PR3

Finding ID: SLA-PR3
Severity: major
Location: Initial intent preservation line 85, Scope budget line 102, Upstream correction lines 272-274, and Follow-on Artifacts line 411
Evidence: Selective downstream reopening is classified as a deferred initial goal and deferable follow-up, but the proposal only says it can be proposed later and leaves `Follow-on Artifacts` as `None yet`. The proposal-review contract requires every deferred initial goal to have a follow-up owner.
Required outcome: Route selective downstream reuse to a concrete follow-up ownership surface.
Safe resolution path: Name a separate future proposal in `Next Artifacts` or `Follow-on Artifacts`, owned by `proposal`, and state that it is triggered only if conservative replay cost is material. If no follow-up is intended, classify the goal as out of scope rather than deferred.
needs-decision rationale: The proposal owner must choose whether selective reuse remains promised follow-up work.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The proposal clearly identifies cross-stage write-back and duplicated state ownership. |
| User value | pass | Stable review targets and one state owner improve reviewability and resumption. |
| Option diversity | pass | The proposal compares current behavior, metadata-only edits, stage ownership, and infrastructure enforcement. |
| Decision rationale | pass | The portable ownership option follows the stated simplicity constraint. |
| Scope control | block | SLA-PR3 leaves a deferred initial goal without a follow-up owner. |
| Architecture awareness | pass | Governance, workflow state, skills, adapters, and migration surfaces are identified. |
| Testability | block | SLA-PR2 relies on a final diff that cannot attribute the writing stage. |
| Risk honesty | concern | The proposal misses the embedded-status settlement loop in SLA-PR1. |
| Rollout realism | pass | Prospective adoption, one-time migration, and coherent rollback are described. |
| Readiness for spec | block | SLA-PR1 through SLA-PR3 require proposal revision and same-stage rereview. |

## Scope Preservation Review

- Scope-preservation result: changes-requested.

The proposal visibly classifies the user's initial goals and gives reasons for
rejected enforcement mechanisms. Selective downstream reuse remains classified
as deferred, but no follow-up artifact or owner is named. SLA-PR3 therefore
blocks scope preservation.

## Blocking Questions

1. How does an artifact move from `draft` or `under review` to its durable
   approved status without violating peer ownership or invalidating review?
2. Does v1 promise testable stage-write behavior, or only portable guidance
   checked through review?
3. Is selective downstream reuse owned by a future proposal, or fully out of
   scope?

## Recommended Proposal Edits

- Add a finite lifecycle-status settlement sequence and state whether the
  settlement edit invalidates the peer review.
- Replace final-diff attribution with static skill-contract checks and bounded
  stage-invocation fixtures, or narrow the assurance claim to guidance-only.
- Route selective reuse to a named future proposal owned by `proposal`, or
  classify it as out of scope.

## Recommendation

- Recommendation: changes-requested. The simplified ownership direction fits
  the project vision and is strategically sound, but artifact settlement,
  stage-write proof, and deferred-follow-up ownership are not ready for
  specification. This direct review remains isolated, does not edit the
  proposal, and does not automatically start `spec`.
