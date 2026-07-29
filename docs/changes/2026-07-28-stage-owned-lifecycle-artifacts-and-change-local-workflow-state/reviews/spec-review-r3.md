<!-- Template: spec-review-result-skeleton-v1 -->
<!-- Skill: spec-review -->
<!-- Template status: normative -->

# Spec Review R3

Review ID: spec-review-r3
Stage: spec-review
Round: 3
Reviewer: Codex spec-review skill
Target: specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md
Status: changes-requested
Original review source: User-invoked `$spec-review` after simplifying the
selector registry around published-skill ownership on 2026-07-28.
Material findings: SLA-SR9
Immediate next stage: spec revision
Eventual test-spec readiness: not-ready
Automatic downstream handoff: none

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: SLA-SR9
- Recording status: recorded
- Recording blocker: none
- Review record:
  docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/spec-review-r3.md
- Review log:
  docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/review-log.md
- Review resolution:
  docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/review-resolution.md#spec-review-r3
- Open blockers: SLA-SR9
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: Add the higher-ranked governance alignment prerequisite and
  rerun spec-review before architecture assessment or downstream reliance.

## Findings

## Finding SLA-SR9

Finding ID: SLA-SR9
Severity: blocking
Location: SLA-R001 through SLA-R004; SLA-R065 through SLA-R074d;
Compatibility and migration; reciprocal amendment notices
Evidence: `CONSTITUTION.md` still requires lifecycle status inside top-level
artifacts, the active plan to own current handoff state, and final lifecycle
closeout to update the plan and plan index. The revised specification instead
makes `change.yaml` the sole owner for those values and removes them from
activated artifacts and plans. SLA-R074d requires reciprocal notices only in
four same-rank specifications, while the rollout prerequisite names schema,
workflow, skill, validation, and adapter surfaces but not the higher-ranked
Constitution or affected operating guidance. An activated change could
therefore satisfy this specification while published skills remain required
to follow contradictory higher-ranked instructions.
Required outcome: Make governance alignment a precondition of activation so
published skills have one authoritative ownership contract.
Safe resolution path: Add one source-level activation requirement that
requires the Constitution and affected operating guidance to be updated
consistently before the first activated change. Extend compatibility,
rollback, boundary, and acceptance language to fail activation when that
alignment is absent. Do not reintroduce selector enumeration or make a
repository script the normative owner.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | pass | Writable outputs, read-only inputs, settlement transitions, and route-back behavior are explicit. |
| normative language | concern | The new subject-level precedence is clear, but the activation prerequisite omits the higher-ranked source. |
| completeness | block | Governance alignment is missing from the prospective activation gate. |
| testability | concern | State, transition, skill, and boundary behavior are testable after the activation prerequisite is closed. |
| examples | pass | Examples remain requirement-owned and cover isolated review, route-back, interruption, legacy reads, and target consent. |
| compatibility | block | The new contract conflicts with current Constitution requirements until a required co-update is explicit. |
| observability | pass | Status output and evidence links identify artifact, review, workflow, target, and blocker state. |
| security/privacy | pass | Repository-local scope, external-action prohibition, and secret-handling boundaries are explicit. |
| non-goals | pass | Hashes, interception, hosted state, selective reuse, and automatic external actions remain excluded. |
| acceptance criteria | block | No acceptance criterion proves higher-ranked governance alignment before activation. |

## Confirmed prior-finding resolutions

- SLA-SR3 and SLA-SR6 are resolved by the occurrence-bound latest-review
  schema and positive-evidence final-closeout conjunction.
- SLA-SR4 and SLA-SR7 are resolved by closed transitions, complete stage and
  capability fields, and named retained contracts.
- SLA-SR5 and SLA-SR8 are resolved by the published-skill ownership table,
  four closed replaced subjects, and four matching reciprocal notices. The
  323-selector registry and its script-centered completeness contract are no
  longer required by this co-amendment.

## Nonblocking editorial notes

- `## Inputs and outputs` contains a duplicated `### Outputs` heading.
- EC9 is followed by a duplicated `persisted.` line.

These do not make implementation behavior ambiguous, but the next spec
revision should remove them.

## Exact wording suggestion

Add a requirement with this effect:

```text
Before the first stage-owned-change-local-v1 activation, the repository
Constitution and affected operating guidance MUST assign artifact lifecycle
state and current workflow state consistently with this specification.
Missing or contradictory higher-ranked guidance MUST block activation.
```

## Recommendation

Changes requested.
The selector simplification is materially better and keeps the contract
centered on published skills, but activation cannot be safe until the
higher-ranked governance source agrees.

This direct review is isolated and does not start architecture, planning, test
specification, implementation, or workflow automation.
