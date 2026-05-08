# Spec Review R2

Review ID: spec-review-r2
Stage: spec-review
Round: 2
Reviewer: Codex spec-review
Target: `specs/rigorloop-workflow.md`, `specs/workflow-stage-autoprogression.md`, `specs/skill-contract.md`, `specs/milestone-aware-review-handoff.md`, and matching test specs
Status: changes-requested

## Review inputs

- Proposal: `docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md`
- Workflow spec amendment: `specs/rigorloop-workflow.md`
- Autoprogression spec amendment: `specs/workflow-stage-autoprogression.md`
- Skill contract spec amendment: `specs/skill-contract.md`
- Related milestone spec: `specs/milestone-aware-review-handoff.md`
- Matching test specs: `specs/rigorloop-workflow.test.md`, `specs/workflow-stage-autoprogression.test.md`, `specs/milestone-aware-review-handoff.test.md`
- Governance: `CONSTITUTION.md`, `AGENTS.md`
- Workflow summary: `docs/workflows.md`
- Prior review-resolution: `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md`

## Findings

### SR4 - Retired size and risk route vocabulary still appears in the workflow contract

Finding ID: SR4
Severity: major

Evidence: `specs/rigorloop-workflow.md:201` says public workflow guidance must not classify work as fast-lane, full-lane, tiny, low-risk, high-risk, small-change, or mini-spec routes. The same spec still says the goal is to avoid forcing the full artifact lifecycle onto "trivial work" at `specs/rigorloop-workflow.md:20`, and the stage-obligation table uses "High-risk" as the `architecture-review` trigger at `specs/rigorloop-workflow.md:293`.

Required outcome: The workflow contract must remove size-class and risk-class route wording from the public workflow model while preserving concrete stage triggers.

Safe resolution: Rewrite the goal so manual isolated skill invocation, not "trivial work", explains focused use. Replace the `architecture-review` trigger with concrete conditions such as broad-impact, cross-component, migration-heavy, security-sensitive, boundary-changing, or hard-to-reverse design. Do not remove ordinary risk recording fields such as `change.yaml` `risk`; the fix is about route vocabulary in workflow guidance.

### SR5 - Lifecycle closeout still exposes direct verify routing and old verify-readiness terms

Finding ID: SR5
Severity: major

Evidence: The amended final order is `ci-maintenance` when triggered, then `explain-change`, `verify`, and `pr`, but related contract text still treats `verify` as the immediate closeout target. `specs/rigorloop-workflow.md:35` says implementation milestones close before "final verification readiness", and `specs/rigorloop-workflow.md:37` names lifecycle-closeout gates as `verify`, `explain-change`, and PR handoff. `specs/workflow-stage-autoprogression.md:128-133` says a lifecycle-closeout milestone may enter `verify`, and `specs/workflow-stage-autoprogression.md:198` still uses "verify-readiness decisions". Most directly, `specs/milestone-aware-review-handoff.md:118` says a clean final milestone's next stage must be `verify`, and `specs/milestone-aware-review-handoff.test.md:295-297` asks tests to confirm lifecycle-closeout does not block entry into `verify`.

Required outcome: Governing specs, workflow guide wording, and matching test specs must consistently use final-closeout readiness and the final closeout order: `ci-maintenance` when triggered, then `explain-change`, then `verify`, then `pr`.

Safe resolution: Replace direct final-milestone-to-`verify` requirements with final-closeout routing. Rename stale "verify-readiness" wording to "final closeout readiness" where the condition gates the whole closeout sequence. Update lifecycle-closeout examples to list `ci-maintenance`, `explain-change`, `verify`, and PR handoff in the new order. Keep isolated direct `verify` behavior intact.

### SR6 - Autoprogression still uses undefined required-or-default routing

Finding ID: SR6
Severity: major

Evidence: `specs/rigorloop-workflow.md:322-325` defines continuation in terms of the next mandatory or triggered downstream stage. `specs/workflow-stage-autoprogression.md` still uses "required or default downstream stage" in the scope statement at line 21, Example E2 at line 57, `R2` and `R2a` at lines 163-165, `R2c` through `R2e` at lines 171-175, `R3b` at line 188, and `EC2` at line 333.

Required outcome: Autoprogression requirements must use the same routing vocabulary as the workflow contract so tests can tell whether a conditional review stage is actually triggered.

Safe resolution: Replace "required or default downstream stage" with "mandatory or triggered downstream stage" in the autoprogression spec and matching tests. If "default" is intentionally retained, define it in the glossary and state that it cannot bypass stage-obligation triggers or turn manual skill invocations into workflow completion.

### SR7 - Matching test specs still assert retired fast-lane and direct-verify behavior

Finding ID: SR7
Severity: major

Evidence: `specs/rigorloop-workflow.test.md:94-95` still says generated-artifact refresh can remain fast-lane and documentation-only workflow policy changes are not fast-lane eligible. `specs/rigorloop-workflow.test.md:143-145` tells reviewers to confirm fast lane, full lifecycle, allowlists, and disallow lists, and `specs/rigorloop-workflow.test.md:555` still refers to fast-lane eligibility. `specs/workflow-stage-autoprogression.test.md:83`, `102`, `272`, `328`, and `359` still preserve fast-lane assertions. `specs/milestone-aware-review-handoff.test.md:295-297` still asserts lifecycle-closeout work does not block entry into `verify`.

Required outcome: Matching test specs must stop preserving the retired lane model and the old direct-verify closeout behavior.

Safe resolution: After the spec text is corrected, update the matching test specs to assert one recommended standard workflow, isolated manual skill invocation, `ci-maintenance` when triggered before `explain-change`, and final `explain-change -> verify -> pr` ordering. Remove fast-lane eligibility tests and replace direct-verify lifecycle-closeout assertions with final-closeout readiness assertions.

## Review dimensions

| Dimension | Result | Notes |
|---|---|---|
| Requirement clarity | concern | SR4, SR5, and SR6 leave multiple interpretations for route vocabulary and final closeout routing. |
| Normative language | concern | `MUST` requirements in the milestone-aware spec still route directly to `verify`, while the newer workflow amendment routes to final closeout. |
| Completeness | concern | Related specs and tests have not been fully amended to the new workflow model. |
| Testability | concern | Current test specs still prove fast-lane and direct-verify behavior that the amendment retires. |
| Examples | concern | Lifecycle-closeout examples still mention old verify-first ordering in related specs. |
| Compatibility | pass | Manual isolated skill invocation and direct `pr` compatibility remain covered. |
| Observability | pass | The desired final closeout sequence and public-surface checks are observable once wording is aligned. |
| Security/privacy | pass | No new security-sensitive behavior is introduced. |
| Non-goals | pass | Merge, release, deploy, and destructive Git automation remain excluded. |
| Acceptance criteria | concern | Acceptance criteria in amended specs are directionally right, but matching test specs still assert retired behavior. |

## Review outcome

Changes requested.

No automatic downstream handoff is performed because this was a direct `spec-review` request.

Immediate next repository stage: none

Eventual `test-spec` readiness: not-ready

Stop condition: upstream spec and matching test-spec fixes are required before downstream planning or implementation should rely on the amended contract.
