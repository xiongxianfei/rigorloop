# Spec Review R3

Review ID: spec-review-r3
Stage: spec-review
Round: 3
Reviewer: Codex spec-review
Target: `specs/rigorloop-workflow.md`, `specs/workflow-stage-autoprogression.md`, `specs/milestone-aware-review-handoff.md`, matching test specs, and affected workflow skill guidance
Status: changes-requested

## Review inputs

- Workflow spec amendment: `specs/rigorloop-workflow.md`
- Autoprogression spec amendment: `specs/workflow-stage-autoprogression.md`
- Related milestone spec: `specs/milestone-aware-review-handoff.md`
- Matching test specs: `specs/rigorloop-workflow.test.md`, `specs/workflow-stage-autoprogression.test.md`, `specs/milestone-aware-review-handoff.test.md`
- Workflow summary: `docs/workflows.md`
- Affected stage skill: `skills/code-review/SKILL.md`
- Prior review-resolution: `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md`

## Findings

### SR8 - Stale direct-verify closeout wording remains in milestone-aware surfaces

Finding ID: SR8
Severity: major

Evidence: The main amended workflow now says final closeout routes through `ci-maintenance` when triggered, then `explain-change`, then `verify`, then `pr`. `specs/rigorloop-workflow.md:185-190` and `specs/workflow-stage-autoprogression.md:115-120` already express that sequence. However, related milestone-aware surfaces still preserve direct-`verify` closeout wording. `specs/milestone-aware-review-handoff.md:65` says ambiguous remaining milestones do not hand off to `verify`; lines 73-75 say milestones must not be skipped to make `verify` available and that `verify` may proceed after revision. `specs/workflow-stage-autoprogression.md:295` still says ambiguous milestone state stops "instead of routing a clean review to `verify`". `specs/workflow-stage-autoprogression.test.md:297-300` still expects clean final milestone reviews to route to `verify` and speaks of plan readiness for `verify`. `specs/milestone-aware-review-handoff.test.md:180`, `274`, and `276` still use direct-`verify` routing or availability as the proof target. `skills/code-review/SKILL.md:238` still tells the public skill to hand a clean final milestone to `verify`.

Required outcome: All milestone-aware closeout examples, requirements, test specs, and affected stage guidance must describe final closeout readiness and the current final closeout sequence rather than direct final-milestone-to-`verify` routing. Isolated direct `verify` behavior must remain intact.

Safe resolution: Replace stale direct-`verify` closeout references with final closeout wording. Where an immediate next stage is needed after a clean final implementation milestone, use `ci-maintenance` when triggered; otherwise `explain-change`. Where the text describes a blocker or readiness state, use final closeout readiness. Update canonical `skills/code-review/SKILL.md`, regenerate generated skill and adapter copies, and extend or update static wording checks so the old direct-`verify` closeout phrases cannot return.

## Review dimensions

| Dimension | Result | Notes |
|---|---|---|
| Requirement clarity | concern | The main workflow and autoprogression examples point to final closeout, but milestone-aware examples and skill guidance still point directly to `verify`. |
| Normative language | concern | `specs/milestone-aware-review-handoff.md` requirements use final closeout, while nearby examples and public skill handoff text use `verify`. |
| Completeness | concern | The previous SR5/SR7 fix did not fully update all related milestone-aware and skill surfaces. |
| Testability | concern | Current test specs would still prove direct final-milestone-to-`verify` behavior. |
| Examples | concern | Milestone-aware examples E4 and E5 use stale direct-`verify` language. |
| Compatibility | pass | Isolated direct `verify`, direct `pr`, manual skill invocation, and bugfix compatibility remain specified. |
| Observability | pass | The intended final closeout sequence is observable and can be statically checked once wording is aligned. |
| Security/privacy | pass | No security-sensitive behavior is introduced. |
| Non-goals | pass | Merge, release, deploy, and destructive Git automation remain excluded. |
| Acceptance criteria | concern | The autoprogression test spec still contains direct-`verify` expectations for milestone closeout. |

## Review outcome

Changes requested.

No automatic downstream handoff is performed because this was a direct `spec-review` request.

Immediate next repository stage: none

Eventual `test-spec` readiness: not-ready

Stop condition: upstream spec, matching test-spec, and affected skill-guidance fixes are required before downstream planning or implementation should rely on the amended milestone-aware closeout contract.
