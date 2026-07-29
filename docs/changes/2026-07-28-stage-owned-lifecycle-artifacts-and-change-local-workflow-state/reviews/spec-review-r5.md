<!-- Template: spec-review-result-skeleton-v1 -->
<!-- Skill: spec-review -->
<!-- Template status: normative -->

# Spec Review R5

Review ID: spec-review-r5
Stage: spec-review
Round: 5
Reviewer: Codex spec-review skill
Target: specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md
Status: changes-requested
Original review source: User-requested `$spec-review` after resolving
SLA-SR10 on 2026-07-29.
Material findings: SLA-SR11
Immediate next stage: spec revision
Eventual test-spec readiness: not-ready
Automatic downstream handoff: none

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: SLA-SR11
- Recording status: recorded
- Recording blocker: none
- Review record:
  docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/spec-review-r5.md
- Review log:
  docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/review-log.md
- Review resolution:
  docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/review-resolution.md#spec-review-r5
- Open blockers: SLA-SR11
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: Complete the same-rank compatibility inventory and rerun
  spec-review before architecture assessment.

## Findings

## Finding SLA-SR11

Finding ID: SLA-SR11
Severity: blocking
Location: SLA-R074c through SLA-R074e; same-rank plan, evidence-access, learn,
skill-contract, and workflow-map specifications
Evidence: R4's named source set now has matching notices, but a repository-wide
subject audit found additional approved requirements that still make the
active plan or plan index the live-state owner, require plan-body lifecycle
updates, permit artifact-local settlement, or route mutable follow-up state
into the active plan. The directly conflicting sources are:
`change-record-catalog-registration-and-bounded-read-model.md`,
`cost-bounded-rigor-m5-progressive-loading-follow-through.md`,
`learn-artifact-model.md`, `milestone-aware-review-handoff.md`,
`plan-index-lifecycle-ownership.md`,
`progressive-loading-high-cost-public-skills.md`,
`release-process-contract.md`, `skill-contract.md`, and
`workflow-skill-artifact-location-map.md`.
Because SLA-R074d keeps every unlisted same-rank requirement authoritative, a
governed change would still have contradictory current-state and write
ownership rules.
Required outcome: Make the compatibility source set complete for every
approved specification that directly assigns mutable lifecycle or handoff
state to a retired owner.
Safe resolution path: Add one concise reciprocal subject-level notice to each
listed source and add its exact replaced subject and retained behavior to
SLA-R074c. Preserve stable plan intent, historical evidence, asset packaging,
bounded-read efficiency, review behavior, release safety, and learn routing
to owner surfaces. Do not add requirement selectors or treat keyword matching
as normative completeness proof.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | pass | The stage-owned model, fixed writers, and one-target automation boundary are explicit. |
| normative language | pass | State schemas, legal transitions, route-back behavior, and stale-proof handling use testable requirements. |
| completeness | block | The closed compatibility source set still omits nine directly conflicting approved specifications. |
| testability | pass | Artifact, workflow, automation, compatibility, and boundary behavior can be mapped to deterministic and semantic proof. |
| examples | pass | Examples remain requirement-owned and do not invent behavior. |
| compatibility | block | Unlisted same-rank plan and artifact-settlement writers remain authoritative under SLA-R074d. |
| observability | pass | State, review, transition, pause, and target information are observable through bounded change-local evidence. |
| security/privacy | pass | Repository-local scope and external-action prohibitions remain intact. |
| non-goals | pass | The revision adds no hashes, interception, hosted state, selectors, or additional authorization layer. |
| acceptance criteria | concern | AC-SLA-027 and AC-SLA-032 cannot pass until the complete direct-conflict set has reciprocal notices. |

## Confirmed prior-finding resolution

SLA-SR10 is resolved.
All nine sources named by R4 now carry reciprocal subject-level notices, the
main compatibility table names their replaced and retained subjects, and
SLA-R074e prevents stale dependent test specs from authorizing
implementation.

## Recommendation

Changes requested.
The revised mechanism itself is coherent and simpler, but approval would be
unsafe while additional same-rank specifications still name retired writers.

This direct review is isolated and does not start architecture, planning, test
specification, implementation, or workflow automation.
