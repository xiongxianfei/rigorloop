# Skill Readability and Self-Containment Plan Review R1

Review ID: plan-review-r1
Stage: plan-review
Round: 1
Reviewer: Codex plan-review
Target: docs/plans/2026-05-18-skill-readability-self-containment.md
Status: changes-requested

## Result

- Skill: plan-review
- Review status: changes-requested
- Material findings: SRSC-PLAN-1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-18-skill-readability-self-containment/reviews/plan-review-r1.md
- Review log: docs/changes/2026-05-18-skill-readability-self-containment/review-log.md
- Review resolution: docs/changes/2026-05-18-skill-readability-self-containment/review-resolution.md
- Open blockers: SRSC-PLAN-1
- Immediate next stage: plan revision, then plan-review rerun

## Verdict

Revise.

The plan is self-contained, traces to the approved spec, and has concrete validation commands. It is not ready to hand off because it treats `test-spec` authoring as implementation milestone work. In this workflow, `test-spec` is the lifecycle stage after plan-review and before implementation.

## Material Findings

### SRSC-PLAN-1 - Test-spec authoring is modeled as an implementation milestone

Finding ID: SRSC-PLAN-1
Severity: major
Location: `docs/plans/2026-05-18-skill-readability-self-containment.md:68`, `docs/plans/2026-05-18-skill-readability-self-containment.md:81`, `docs/plans/2026-05-18-skill-readability-self-containment.md:89`, `docs/plans/2026-05-18-skill-readability-self-containment.md:98`

Evidence: The Current Handoff Summary names `M1. Test-spec and validation design prerequisites` as the current milestone and includes `M1` in "Remaining in-scope implementation milestones." M1's goal is to "Create the test-spec" and its implementation steps say "author the test spec." The milestone closeout then says to "hand off to code-review for M1 if implementation artifacts changed."

Required outcome: Separate lifecycle-stage test-spec work from implementation milestones. The plan must make `test-spec` the immediate downstream stage after plan-review, not an implementation milestone subject to code-review closeout.

Safe resolution: Remove or reframe M1 as a pre-implementation lifecycle handoff section. Make the first implementation milestone the static-validator and baseline-evidence slice after the test spec is approved. Update the Current Handoff Summary, remaining implementation milestones, dependencies, milestone numbering if desired, and lifecycle closeout text so the sequence is `plan-review -> test-spec -> implementation milestone 1`. Then rerun plan-review.

## Review Dimensions

| Dimension | Result | Notes |
|---|---|---|
| Self-contained context | pass | The plan names source artifacts, touched surfaces, non-goals, requirements, validation commands, and follow-on boundaries. |
| Source alignment | pass | Requirements R1-R60 are mapped to plan coverage and the pilot/follow-on split matches the approved spec. |
| Milestone size | concern | The implementation slices after M1 are reviewable, but M1 is a lifecycle artifact stage rather than implementation work. |
| Sequencing | block | SRSC-PLAN-1 makes the next lifecycle stage ambiguous by putting `test-spec` inside implementation milestones. |
| Scope discipline | pass | Non-goals protect generated output, full R30 rollout expansion, build-time partials, and token savings over quality. |
| Validation quality | pass | Commands and expected observations are explicit, including generated-output and token-cost checks. |
| TDD readiness | concern | The plan correctly requires a proof map before skill rewrites, but that proof map belongs to the next `test-spec` stage. |
| Risk coverage | pass | Rollback and recovery paths are present for validation scope, skill rewrite, parity, cold-read, and token cap risks. |
| Architecture alignment | pass | Spec-review found no architecture artifact required, and the plan keeps adapter/generated-output boundaries intact. |
| Operational readiness | pass | Release/generated-output constraints, adapter validation, and follow-on rollout ownership are covered. |
| Plan maintainability | pass | The plan has handoff summary, milestone states, validation notes, decision log, and closeout sections. |

## Missing Milestones or Dependencies

No implementation milestone is missing. The issue is classification: test-spec authoring is currently included in the implementation milestone list even though it is the immediate lifecycle stage after plan-review.

## Suggested Edits

1. Replace the Current Handoff Summary with a state that says plan-review is current, `test-spec` is the next stage after plan-review, and implementation milestones begin only after the test spec is approved.
2. Remove `M1. Test-spec and validation design prerequisites` from the implementation milestone list, or convert it to a non-milestone "Next lifecycle stage: test-spec" section.
3. Rename or renumber the remaining implementation milestones so the first implementation milestone is static validator foundations and baseline evidence.
4. Update dependencies that currently say "M1 complete" to say "test spec approved" or equivalent.
5. Remove the code-review closeout line for test-spec authoring.

## Immediate Next Stage

Immediate next stage is plan revision, then plan-review rerun. If the revised plan passes, the next lifecycle stage is `test-spec`, not implementation.

## Downstream Implementation Readiness

Implementation is not ready. It should remain blocked until the plan is revised, plan-review passes, and the test spec is created and accepted or otherwise approved by the workflow.

## Isolation

This review is isolated. No automatic downstream handoff is initiated.
