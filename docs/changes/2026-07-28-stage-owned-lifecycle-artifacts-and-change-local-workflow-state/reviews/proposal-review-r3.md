# Proposal Review R3

Review ID: proposal-review-r3
Stage: proposal-review
Round: 3
Reviewer: Codex proposal-review skill
Target: docs/proposals/2026-07-28-approved-specification-baselines-and-controlled-amendment-workflow.md
Status: changes-requested
Original review source: User-invoked `$proposal-review` after proposal revision on 2026-07-28.
Material findings: SLA-PR4
Scope-preservation result: pass
Immediate next stage: isolated stop
Automatic downstream handoff: none

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: SLA-PR4
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/proposal-review-r3.md
- Review log: docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/review-log.md
- Review resolution: docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/review-resolution.md#proposal-review-r3
- Open blockers: SLA-PR4
- Immediate next stage: isolated stop

## Material Findings

### Finding SLA-PR4

Finding ID: SLA-PR4
Severity: high
Location: Recommended Direction / Change-local lifecycle and workflow state; Testing and Verification Strategy; Risks and Mitigations; Decision Log
Evidence: The proposal says shared-state writers have “disjoint fields,” but review peers settle `artifact_states.<artifact>` while workflow later invalidates that same entry before revision. It also expects a review attempt to write routing state to fail validation, while the proposal explicitly disclaims stage-write attribution, interception, and protected-path enforcement. The Decision Log further says “Give review peers matching artifact-state settlement authority and workflow routing authority,” which grammatically assigns routing authority to the review peer and contradicts the main rule.
Required outcome: State one coherent transition-ownership model and align its proof claims with the guidance-and-review assurance boundary. The proposal must distinguish semantic state consistency, which a repository validator can check, from writer identity, which v1 cannot determine from a final diff.
Safe resolution path: Keep review-owned settlement and workflow-owned routing. Describe the shared artifact-state entry as transition-scoped rather than disjoint: review owns evidence-backed settlement transitions, while workflow owns only explicit pre-revision invalidation. Replace actor-attribution validation claims with deterministic checks that settlement matches review evidence and invalidation matches an owner-revision route. Correct the Decision Log so routing authority is assigned to workflow.
needs-decision rationale: The proposal owner must choose this narrower guidance-and-consistency model or explicitly add a state-mutation mechanism that can prove writer identity. The owning stage is `proposal`.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Cross-stage write-back and duplicated mutable state remain concrete problems. |
| User value | pass | Stable reviewed artifacts and change-local status directly support review and automation continuity. |
| Option diversity | pass | Current behavior, metadata edits, field-scoped state, and stronger enforcement are compared. |
| Decision rationale | concern | The selected direction is sound, but the Decision Log currently misstates routing ownership. |
| Scope control | pass | Hashing, interception, amendment machinery, selective reuse, migration, and external actions are bounded explicitly. |
| Architecture awareness | pass | Governance, state schema, workflow, automation authorization, skills, templates, adapters, and migration are visible. |
| Testability | concern | Semantic consistency is testable, but stage-writer attribution is claimed without an enforcement surface. |
| Risk honesty | pass | The proposal acknowledges guidance-only enforcement, shared YAML ownership, interruption, and external boundaries. |
| Rollout realism | pass | Prospective adoption and one-model-per-change migration are coherent. |
| Readiness for spec | block | The writer and transition ownership contradiction would make the downstream state contract ambiguous. |

## Scope Preservation Review

- Scope-preservation result: pass.

Every stated user goal is classified.
The revision preserves review-owned change-local settlement, read-only reviewed
artifacts, peer-stage ownership, workflow continuation without another public
parameter, no hashing, no formal amendment system, conservative replay, and
PR-visible learn evidence.

## Blocking Questions

- Will v1 remain a guidance-and-semantic-consistency model, or will it add a
  mutation surface capable of proving stage identity?

## Recommended Proposal Edits

- Replace “disjoint fields” with transition-scoped authority for the shared
  artifact-state entry.
- Limit deterministic validation to review-evidence, lifecycle-transition, and
  routing consistency.
- Keep unexpected writer behavior as a skill-contract and review finding
  unless a later proposal adds deterministic attribution.
- Correct the Decision Log to assign artifact settlement to review peers and
  routing to `workflow`.

## Recommendation

- Recommendation: changes-requested. Resolve `SLA-PR4`, rerun
  `proposal-review`, and keep this direct review isolated. Do not start `spec`
  from this review result.
