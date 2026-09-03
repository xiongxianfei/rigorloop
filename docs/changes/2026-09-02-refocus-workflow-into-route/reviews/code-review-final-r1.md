# Final Holistic Code Review R1: Refocus Workflow into Route

Review ID: code-review-final-r1
Stage: code-review
Round: r1
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Target: branch diff e8148e83..a7beee8d
Reviewed artifact: complete cross-milestone implementation through a7beee8d
Reviewed milestone: final holistic cross-milestone review
Review date: 2026-09-03
Status: changes-requested
Review status: changes-requested
Material findings: RFR-FINAL-CR1
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-09-02-refocus-workflow-into-route/reviews/code-review-final-r1.md`; `docs/changes/2026-09-02-refocus-workflow-into-route/review-log.md`; `docs/changes/2026-09-02-refocus-workflow-into-route/review-resolution.md`; `docs/changes/2026-09-02-refocus-workflow-into-route/change.yaml`
- Open blockers: RFR-FINAL-CR1
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: RFR-FINAL-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-09-02-refocus-workflow-into-route/reviews/code-review-final-r1.md`
- Review log: `docs/changes/2026-09-02-refocus-workflow-into-route/review-log.md`
- Review resolution: `docs/changes/2026-09-02-refocus-workflow-into-route/review-resolution.md`
- Reviewed milestone: final
- Milestone closeout: all implementation milestones closed; final review correction required
- Remaining implementation milestones: none
- Required review-resolution: yes
- Finding IDs: RFR-FINAL-CR1
- Verify readiness: blocked

## Review inputs

- Actual diff: branch range `e8148e83..a7beee8d`, covering M1 through M3 and their accepted corrections.
- Approved Design package: `design-review-r1`, with current specification, architecture, and ADR identities and granted authority.
- Approved Delivery package: `delivery-review-r1`, with current plan identity and granted authority.
- Milestone state: M1, M2, and M3 are closed; no implementation milestone remains.
- Review-resolution state: nine earlier material findings are resolved and no earlier finding remains open.
- Milestone evidence: `evidence/m1-workflow-context.md`, `evidence/m2-route-canonical-cutover.md`, and `evidence/m3-adapter-and-release-parity.md`.
- Validation evidence: the complete M3 run passed 156 adapter tests, 365 package tests with 2 historical skips, 352 skill-validator tests, and 12 broad-smoke checks; focused guide, boundary, and review-artifact suites were also rechecked during this review.
- Authoritative current context: `rigorloop workflow-context --change 2026-09-02-refocus-workflow-into-route --format json` reports v3 active, all milestones closed, no blocker, current stage `code-review`, and only `route-correction` plus `record-review` as permitted operations.

## Actual-diff summary

The complete implementation adds bounded read-only workflow context, replaces the current public workflow skill and guide authority with route plus CLI-derived facts, preserves semantic stage ownership and stored workflow protocol identity, and propagates the route-only package through validators, adapters, migration behavior, documentation, and an unpublished v0.5.1 candidate. The milestone implementations and their local corrections are coherent. The first real v3 closeout exposes a lifecycle coordination defect: the CLI has no representable final holistic Code Review completion authority, so route cannot advance this otherwise completed change into Verify.

## Findings

### Finding RFR-FINAL-CR1

Finding ID: RFR-FINAL-CR1
Severity: critical
Location: `packages/rigorloop/dist/lib/lifecycle-stage-routing.js:8`; `packages/rigorloop/dist/lib/lifecycle-stage-routing.js:25`; `packages/rigorloop/dist/lib/lifecycle-read.js:279`; `packages/rigorloop/dist/lib/lifecycle-read.js:406`
Evidence: For `code-review`, `artifactForStage` selects the primary plan, but `expectedReviewAuthority` recognizes only proposal review. `stageIsComplete` therefore finds no code-review-owned artifact entry and always returns false after the last implementation milestone is closed. The current exact-change context consequently offers `record-review` rather than `advance-stage`; that operation is artifact-review-shaped and cannot grant final branch-review authority through the plan. A durable final review file and the top-level review projection cannot change this result because neither is consumed by `stageIsComplete`. The active v3 graph requires `code-review -> verify`, and FV-R8 requires Verify to resolve a current final holistic review basis, so this first v3 example cannot make its required transition through the authoritative CLI.
Required outcome: Give v3 an explicit, identity-bound representation and CLI operation for final holistic Code Review completion, make `stageIsComplete` consume that exact current evidence, and prove that a clean final review permits `code-review -> verify` while missing, stale, changed-requested, or milestone-local evidence does not. The same representation must support routing an implementation-owned finding discovered by final review without requiring a nonexistent active milestone.
Safe resolution path: Extend the existing lifecycle coordination model with a final-review occurrence or equivalent stage-owned receipt rather than attaching branch-review meaning to the plan artifact. Add focused lifecycle tests for final clean registration, stale reviewed-subject rejection, finding/correction routing after all milestones close, idempotent retry, and successful advance to Verify. Keep Code Review read-only and have route perform only the resulting permitted lifecycle mutation.
needs-decision rationale: none; the current v3 contract already requires final holistic Code Review and the direct transition to Verify. The correction must implement that existing contract without redesigning stage ownership.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | The route/CLI separation is implemented, but the authoritative CLI cannot represent the final review basis needed by the active v3 route. |
| Test coverage | block | Current lifecycle tests cover artifact reviews and milestone closeout but do not exercise final holistic review registration and `code-review -> verify`. |
| Edge cases | block | No active milestone exists for a final-review implementation finding, so its correction route is also unproved. |
| Error handling | pass | Context fails closed by withholding advancement rather than inventing authority. |
| Architecture boundaries | pass | The implemented route and CLI fact/semantic split is otherwise preserved. |
| Compatibility | pass | Historical records and v0.5.0 remain unchanged; v0.5.1 remains unpublished. |
| Security/privacy | pass | Reviewed context and diagnostics remain bounded and repository-relative. |
| Derived artifact currency | pass | Canonical route and generated candidate inventories agree under the recorded M3 proof. |
| Unrelated changes | pass | The branch diff remains within the approved M1-M3 scope. |
| Validation evidence | block | Passing suites do not establish the mandatory final v3 transition, and the live exact-change result demonstrates the omission. |

## No automatic downstream handoff

The final holistic review is not clean. Verify must not start because the active v3 runtime cannot record the final review basis or authorize the required transition. Review Resolution must accept and scope RFR-FINAL-CR1, then implementation must correct the lifecycle coordination boundary and return for final holistic rereview.
