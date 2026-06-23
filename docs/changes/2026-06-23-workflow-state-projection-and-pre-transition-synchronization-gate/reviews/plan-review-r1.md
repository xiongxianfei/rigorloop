# Plan Review R1

Review ID: plan-review-r1
Stage: plan-review
Round: 1
Reviewer: Codex plan-review
Target: docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md
Reviewed artifact: docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md
Review date: 2026-06-23
Recording status: recorded
Status: changes-requested

## Result

- Skill: plan-review
- Review status: changes-requested
- Material findings: WSS-PLAN1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/reviews/plan-review-r1.md
- Review log: docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-log.md
- Review resolution: docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-resolution.md#plan-review-r1
- Open blockers: WSS-PLAN1
- Immediate next stage: plan revision
- Implementation readiness: blocked until the plan is revised and re-reviewed
- Stop condition: Do not proceed to test-spec or implementation until WSS-PLAN1 is resolved and the revised plan passes plan-review.

## Findings

### WSS-PLAN1: Test-spec authoring is modeled as an implementation milestone

Finding ID: WSS-PLAN1
Severity: major
Location: docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md lines 91-128.
Evidence: The plan's M1 is titled "Test Spec and Fixture Contract" and its goal is to "Update the test specification" before production validator work starts. It lists `specs/single-source-of-workflow-state.test.md` as a likely touched file and says its implementation steps include mapping each new `MUST` requirement to named test cases. The governing per-change chain in `docs/workflows.md` routes `plan-review -> test-spec -> implement`, and the workflow summary explicitly says plan-review's normal immediate handoff is into `test-spec`. Therefore the test-spec artifact should be authored by the `test-spec` stage, not treated as an implementation milestone that later hands off to code-review.
Required outcome: Revise the plan so it separates the mandatory `test-spec` lifecycle stage from implementation milestones. The plan should route a clean plan-review to `test-spec`, and the first implementation milestone should begin only after the matching test spec exists.
Safe resolution path: Move the `specs/single-source-of-workflow-state.test.md` requirement mapping and test-case definition work out of M1 and into the expected downstream `test-spec` stage. Then redefine M1 as the first implementation milestone that consumes the approved test spec, such as adding failing/fixture-backed validator tests and parser scaffolding, or merge that work into the parser/validator milestone with explicit tests-first steps. Update dependencies, current handoff, milestone names, validation commands, and progress notes accordingly, then rerun plan-review.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| self-contained context | pass | The plan names the accepted proposal, approved spec, architecture, review evidence, change metadata, scope, constraints, requirements mapping, milestones, risks, and handoff state. |
| source alignment | concern | WSS-PLAN1 conflicts with the workflow stage chain by making test-spec authoring part of an implementation milestone. |
| milestone size | pass | The validator, review evidence consistency, workflow guidance, and closeout slices are otherwise reviewable. |
| sequencing | block | WSS-PLAN1 blocks the plan because implementation milestone M1 contains the separate mandatory `test-spec` stage work. |
| scope discipline | pass | The plan excludes historical migration, projection writer work, stage-order changes, generated-output hand edits, and new service boundaries. |
| validation quality | concern | The listed validation commands are concrete, but M1's validation proves a lifecycle artifact that should be owned by `test-spec`, not code-reviewed as implementation. |
| TDD readiness | concern | The intent is test-first, but the lifecycle sequencing must put the test specification stage before implementation milestones. |
| risk coverage | pass | The plan records active-plan normalization, review-artifact ambiguity, and generated adapter validation risks. |
| architecture alignment | pass | The plan follows the architecture decision to keep state-sync validation inside artifact-lifecycle validation and avoid a competing control plane. |
| operational readiness | concern | The plan cannot safely proceed to `test-spec` or implementation until the stage split is corrected. |
| plan maintainability | pass | The plan is detailed enough for a targeted revision without redoing proposal, spec, or architecture work. |

## Missing milestones or dependencies

- Missing: a clean separation between the downstream `test-spec` stage and the first implementation milestone that consumes that test spec.

## Suggested edits

- Change `Current Handoff Summary` after revision to reflect the post-plan-review state accurately.
- Replace M1 with an implementation milestone that starts after the test spec exists.
- Move the `TWSS-*` test-case mapping and `specs/single-source-of-workflow-state.test.md` authoring obligations into the downstream `test-spec` stage, not an implementation milestone.
- Keep parser, review consistency, workflow guidance, active audit, and behavior-preservation milestones, adjusting numbering as needed.

## Implementation-readiness notes

Implementation is not ready. A revised plan must pass plan-review before `test-spec`, and implementation remains blocked until the matching test spec is complete.

## Isolation

This was a direct plan-review request. No automatic downstream handoff is performed.
