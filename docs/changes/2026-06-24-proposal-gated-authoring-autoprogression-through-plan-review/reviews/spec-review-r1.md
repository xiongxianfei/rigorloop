# Spec Review R1: Proposal-Gated Authoring Autoprogression Through Plan Review

## Result

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review
Target: specs/workflow-stage-autoprogression.md; specs/rigorloop-workflow.md
Status: changes-requested

- Skill: spec-review
- Review status: changes-requested
- Material findings: SR-APGA-001
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/spec-review-r1.md
- Review log: docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-log.md
- Review resolution: docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/review-resolution.md
- Open blockers: SR-APGA-001
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: material finding SR-APGA-001 requires spec revision before architecture, plan, or test-spec can rely on the draft amendments.

## Review Inputs

- Accepted proposal: `docs/proposals/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md`
- Draft spec amendment: `specs/workflow-stage-autoprogression.md`
- Draft workflow spec amendment: `specs/rigorloop-workflow.md`
- Formal proposal review: `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/proposal-review-r1.md`
- Review log and change metadata under `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/`

## Findings

### Finding SR-APGA-001

Finding ID: SR-APGA-001
Severity: major
Location: `specs/workflow-stage-autoprogression.md` requirement `R2r`; `specs/rigorloop-workflow.md` requirement `R7er`
Evidence: `R2r` says profile authorization "SHOULD be persisted" in `change.yaml`, while `R7er` says policy metadata "MAY be recorded" in `change.yaml` or the fallback `workflow-policy.yaml`. The accepted proposal requires change-local, explicitly user-authorized automation, durable audit, safe resumption, and a reassertion rule for non-durable pre-pack arming. Optional persistence lets an implementation run the profile without durable authorization evidence while still appearing to satisfy `R7er`.
Required outcome: The spec amendments must require durable change-local persistence of the authorization policy before the active profile can rely on it once a change-local surface exists. The canonical surface should be `docs/changes/<change-id>/change.yaml`, with `docs/changes/<change-id>/workflow-policy.yaml` only as the specified fallback if the change-metadata contract rejects policy data.
Safe resolution path: Change the persistence requirements from optional/advisory to mandatory for durable execution. Align both specs so the orchestrator must pause rather than activate when durable authorization cannot be recorded, while preserving the rule that profile policy metadata does not own live current stage, next stage, review status, branch readiness, or PR readiness.
needs-decision rationale: none

## Review Dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | concern | Persistence is clear as a preference but not as a required precondition for durable execution. |
| normative language | concern | `SHOULD` and `MAY` undercut a safety requirement that the proposal treats as mandatory. |
| completeness | concern | The profile lifecycle is otherwise complete, but the durable authorization boundary is incomplete. |
| testability | concern | Tests cannot reliably require pause-on-missing-authorization if persistence remains optional. |
| examples | pass | The examples cover activation, stopping, isolation, and architecture ambiguity. |
| compatibility | pass | The new profile is off by default and direct reviews remain isolated. |
| observability | concern | Optional persistence weakens the audit trail needed to explain why automatic stages ran. |
| security/privacy | pass | The metadata guidance avoids secrets and credentials. |
| non-goals | pass | The spec preserves the no-test-spec, no-implementation, no-auto-fix, no-global-default boundaries. |
| acceptance criteria | concern | Acceptance criteria requiring explicit authorization and idempotent resume need a mandatory durable policy record. |

## Recommendation

Request a spec revision and rerun `spec-review`. This is a material finding because it can allow unauthorized or unauditable downstream transitions in the exact profile this change is meant to constrain.
