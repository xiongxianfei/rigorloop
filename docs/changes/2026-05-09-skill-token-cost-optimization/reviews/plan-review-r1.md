# Plan Review R1

Review ID: plan-review-r1
Stage: plan-review
Round: 1
Reviewer: Codex plan-review
Target: docs/plans/2026-05-09-skill-token-cost-optimization.md
Status: changes-requested

## Review inputs

- Plan: `docs/plans/2026-05-09-skill-token-cost-optimization.md`
- Plan index: `docs/plan.md`
- Accepted proposal: `docs/proposals/2026-05-09-skill-token-cost-optimization.md`
- Approved spec: `specs/skill-token-cost-optimization.md`
- Change metadata: `docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`

## Verdict

changes-requested

## Findings

### STCO-PR1-F1 - Pre-implementation gates are modeled as a self-referential milestone

Finding ID: STCO-PR1-F1
Severity: material
Dimension: Sequencing

Evidence: The current handoff says the next stage is `plan-review` at `docs/plans/2026-05-09-skill-token-cost-optimization.md` line 81. The plan then defines `M0. Pre-Implementation Review and Test Spec` with `Milestone state: lifecycle-closeout` at lines 87-90. M0 depends on "Plan-review approval" at line 97, but its implementation steps also include "Run `plan-review` for this plan" at line 103. M0 also creates the test spec at line 104, so it is not a lifecycle-closeout-only milestone.

Problem: The plan makes the currently running review both a prerequisite for M0 and an implementation step inside M0. It also uses the `lifecycle-closeout` milestone state for a milestone that authors a test spec, which is not only a downstream closeout gate. This can misroute the next contributor after plan-review and weaken the milestone state model the plan is trying to enforce.

Required outcome: The plan must separate pre-implementation gates from implementation/lifecycle milestones so the next stage is unambiguous and no milestone contains the review that approves the plan itself.

Safe resolution: Replace M0 with a non-milestone "Pre-implementation gates" or "Before implementation" section, or revise it into a normal planned authoring milestone that does not include `plan-review` as its own implementation step. The resulting plan should make the immediate next stage after plan-review explicit: architecture-review of the no-impact rationale must close before `test-spec`, and `test-spec` must complete before M1 implementation starts. Keep M1-M4 as the in-scope implementation milestones and M5 as final lifecycle closeout after M1-M4 review loops pass.

## Review dimensions

| Dimension | Result | Notes |
|---|---|---|
| Self-contained context | pass | The plan includes source artifacts, no-map rationale, touched surfaces, generated-output boundaries, and the current handoff summary. |
| Source alignment | pass | Milestones trace to the accepted proposal and approved spec requirements. The architecture no-impact rationale is identified as pending review. |
| Milestone size | concern | M1-M4 are coherent review slices. M0 is not a valid implementation or lifecycle-closeout milestone. See STCO-PR1-F1. |
| Sequencing | block | M0 depends on plan-review while also instructing the contributor to run plan-review. See STCO-PR1-F1. |
| Scope discipline | pass | Non-goals protect workflow order, full-file-read obligations, validation coverage, public portability, and no new token-budget skill. |
| Validation quality | pass | Milestone validation commands are explicit and include lifecycle, metadata, skill, generated-output, adapter, selected CI, and diff checks. |
| TDD readiness | pass | Test-spec creation and static proof are identified before implementation. |
| Risk coverage | pass | Risks cover under-reading, brittle checks, public-surface leakage, generated-output reviewability, and rollback. |
| Architecture alignment | concern | The plan correctly records no runtime architecture impact, but architecture-review must close before test-spec or implementation continues. |
| Operational readiness | pass | Adapter drift, adapter validation, generated-output checks, final verify, and PR handoff are covered. |
| Plan maintainability | concern | Plan sections are present, but pre-implementation routing needs clearer state ownership. |

## Missing milestones or dependencies

- No implementation milestone is missing.
- The pre-implementation review and test-spec work should not be represented as a `lifecycle-closeout` milestone that runs its own plan-review.

## Exact suggested edits

- Replace M0 with a non-milestone gate section or revise it so it has a valid state and does not include `plan-review` as an implementation step.
- Update `Current Handoff Summary` after plan revision so the next stage is the next real gate, not duplicated across M0 and the summary.
- Keep `architecture-review` before `test-spec`, and keep `test-spec` before M1 implementation.
- Keep M1-M4 code-review handoff and review closeout requirements unchanged.

## Readiness

- Immediate next stage: plan revision, then plan-review rerun.
- `test-spec` readiness: blocked until STCO-PR1-F1 is resolved and plan-review approves the revised plan.
- Implementation readiness: blocked.
- No automatic downstream handoff is performed because this was a direct `plan-review` request.
