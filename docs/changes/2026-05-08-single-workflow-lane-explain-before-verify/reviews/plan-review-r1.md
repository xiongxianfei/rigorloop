# Plan Review R1

Review ID: plan-review-r1
Stage: plan-review
Round: 1
Reviewer: Codex plan-review
Target: `docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md`
Status: changes-requested

## Review inputs

- Plan body: `docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md`
- Plan index: `docs/plan.md`
- Proposal: `docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md`
- Workflow spec: `specs/rigorloop-workflow.md`
- Autoprogression spec: `specs/workflow-stage-autoprogression.md`
- Skill contract spec: `specs/skill-contract.md`
- Architecture package: `docs/architecture/system/architecture.md`
- Plan skill contract: `.codex/skills/plan/SKILL.md`
- Change-local review log and resolution records.

## Findings

### PLR1 - Plan-review is premature while required architecture-review is still pending

Finding ID: PLR1
Evidence: The plan's current handoff says the next stage is `architecture-review` for the latest canonical architecture package update, then `plan-review` (`docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md:86`). The architecture package is still `draft` (`docs/architecture/system/architecture.md:5`) and its readiness says it is ready for `architecture-review` (`docs/architecture/system/architecture.md:278`). The workflow contract requires architecture to produce or update the architecture package before planning continues when architecture is required (`specs/rigorloop-workflow.md:249`), and the stage table makes triggered `architecture-review` downstream-blocking (`specs/rigorloop-workflow.md:292`-`293`).
Required outcome: Plan-review must not approve or hand off to `test-spec` until the latest required architecture-review is complete, or until a reviewed source artifact explicitly removes the architecture-review dependency.
Safe resolution: Run `architecture-review` against `docs/architecture/system/architecture.md` plus `docs/architecture/system/diagrams/context.mmd` and `docs/architecture/system/diagrams/container.mmd`. If approved, normalize architecture status/readiness as allowed, update the plan handoff if needed, then rerun `plan-review`. If architecture-review requests changes, resolve them before rerunning `plan-review`.

### PLR2 - Test-spec readiness is stated as requiring test-spec completion

Finding ID: PLR2
Evidence: The plan's readiness section says "Test-spec readiness: not ready until plan-review completes and the test-spec proof map is confirmed against the approved plan" (`docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md:448`). That makes readiness for `test-spec` depend on the output of `test-spec` itself. The workflow contract says `plan-review` remains the normal immediate handoff into `test-spec` (`specs/rigorloop-workflow.md:356`) and `test-spec` authoring requires approved feature spec, spec-review findings, a concrete plan, and approved architecture or ADR inputs when relevant (`specs/rigorloop-workflow.md:358`).
Required outcome: The plan must distinguish readiness to author `test-spec` from completion or confirmation of the test-spec proof map.
Safe resolution: Change the readiness wording to say `test-spec` authoring is not ready until architecture-review and plan-review are complete. Move "test-spec proof map confirmed against the approved plan" into implementation readiness or test-spec closeout wording, not `test-spec` readiness.

### PLR3 - Lifecycle closeout is formatted like an implementation milestone

Finding ID: PLR3
Evidence: The plan says remaining in-scope implementation milestones are M1 through M5 (`docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md:85`), but M6 is titled `Lifecycle Closeout` and still has `Milestone state: planned` (`docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md:318`-`320`). The plan skill says implementation milestones have exactly one `Milestone state`, while downstream-only gates should use `lifecycle-closeout` for a milestone or section (`.codex/skills/plan/SKILL.md:131`-`159`). The workflow contract says a lifecycle-closeout milestone must not be treated as unfinished implementation work (`specs/rigorloop-workflow.md:423`).
Required outcome: The closeout section must be unmistakably excluded from in-scope implementation milestone state decisions.
Safe resolution: Reformat M6 as `Lifecycle Closeout` with `Milestone type: lifecycle-closeout` or a separate `## Lifecycle Closeout` section, and remove or replace the `Milestone state: planned` line so later agents do not count M6 as an open implementation milestone.

## Review dimensions

| Dimension | Result | Notes |
|---|---|---|
| Self-contained context | pass | A new contributor can identify the proposal, specs, architecture, change root, generated-output boundaries, and no-map rationale. |
| Source alignment | concern | Most milestones trace to requirements, but PLR1 blocks approval because the architecture source is still draft and awaiting required review. |
| Milestone size | concern | M1-M5 are reviewable; PLR3 flags M6 because it is downstream closeout but formatted like an implementation milestone. |
| Sequencing | block | PLR1 blocks plan-review approval; PLR2 also confuses the test-spec handoff sequence. |
| Scope discipline | pass | Non-goals protect lane removal, workflow-guide generator, generated-output hand edits, and `ci` path renaming. |
| Validation quality | pass | Commands are explicit and use selector, CI wrapper, validators, generated-output checks, and whitespace checks. |
| TDD readiness | concern | Test-spec surfaces are named, but PLR2 must be fixed so test-spec readiness is not conflated with test-spec completion. |
| Risk coverage | pass | Key risks include stale lifecycle state, overbroad static checks, generated drift, late findings, and premature final closeout. |
| Architecture alignment | block | The plan correctly identifies the pending architecture-review, but that pending gate blocks plan-review approval. |
| Operational readiness | pass | CI, generated output, adapter distribution, and selected validation commands are covered. |
| Plan maintainability | concern | Progress and validation notes are ready to update; PLR3 should be fixed to avoid milestone-state ambiguity at final closeout. |

## Missing milestones or dependencies

- Missing completed dependency: `architecture-review` for the latest canonical architecture package update.
- Missing corrected readiness distinction: `test-spec` readiness versus test-spec completion.
- Missing lifecycle-closeout classification: M6 should be marked as `lifecycle-closeout` rather than an implementation milestone with `Milestone state: planned`.

## Suggested edits

1. After architecture-review approval, update the current handoff from:

```text
Next stage: architecture-review for the latest canonical architecture package update, then plan-review
```

to the next actual gate, normally:

```text
Next stage: plan-review
```

2. Replace:

```text
Test-spec readiness: not ready until plan-review completes and the test-spec proof map is confirmed against the approved plan.
```

with:

```text
Test-spec readiness: not ready until architecture-review and plan-review are complete.
Test-spec closeout: pending; the proof map must be confirmed against the approved plan before implementation readiness.
```

3. Replace M6's `Milestone state: planned` with:

```text
Milestone type: lifecycle-closeout
Implementation milestone state: not applicable
```

or move M6 to a separate `## Lifecycle Closeout` section.

## Review outcome

Verdict: revise

No automatic downstream handoff is performed because this was a direct `plan-review` request and the review has material findings.

Immediate next stage for `test-spec`: not ready. Required upstream gates are `architecture-review` for the latest canonical architecture update, then a clean rerun of `plan-review`.

Downstream implementation readiness: not ready. Implementation remains blocked on architecture-review, plan-review rerun, and test-spec closeout.
