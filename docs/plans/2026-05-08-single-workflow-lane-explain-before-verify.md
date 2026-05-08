# Single Workflow Lane, Explain-Change Before Verify Execution Plan

## Status

- active
- Owner: maintainers
- Start date: 2026-05-08
- Last updated: 2026-05-08
- Related issue or PR: none yet
- Supersedes: none
- selected_workflow_contract: refactored
- broad_smoke_required: false
- broad_smoke_reason: This initiative changes workflow-governance Markdown, public workflow guidance, canonical skill text, generated skill mirrors, public adapter package copies, static wording checks, and change-local lifecycle evidence. It does not add runtime services, storage, network boundaries, release packaging format, or deployment infrastructure.

## Purpose / Big Picture

Implement the accepted workflow-governance direction: one recommended standard workflow, isolated manual skill invocation for focused use, `ci-maintenance` when triggered before `explain-change`, final `explain-change -> verify -> pr`, and project-portable published skill text.

This plan also catches the repository up to the work already drafted through proposal, spec, architecture, and review rounds. It preserves the current facts: proposal-review, spec-review, architecture-review, and plan-review are closed, and final implementation readiness still requires test-spec alignment, implementation review, review-resolution when triggered, explain-change, verify, and PR handoff.

## Source Artifacts

- Proposal: [Single Workflow Lane, Explain-Change Before Verify, and Public Skill Surface Boundary](../proposals/2026-05-08-single-workflow-lane-explain-before-verify.md), accepted after proposal-review R2.
- Workflow spec amendment: [RigorLoop Workflow](../../specs/rigorloop-workflow.md), approved after spec-review R5.
- Autoprogression spec amendment: [Workflow Stage Autoprogression](../../specs/workflow-stage-autoprogression.md), approved after this initiative's spec-review findings were resolved.
- Skill contract amendment: [Skill Contract](../../specs/skill-contract.md), approved after public skill surface tightening and spec-review R5.
- Related milestone-aware handoff spec: [Milestone-Aware Review Handoff](../../specs/milestone-aware-review-handoff.md), touched to align final closeout wording.
- Architecture: [Canonical System Architecture](../architecture/system/architecture.md), approved after direct canonical update, C4 diagram alignment, and architecture-review R1.
- Test specs: [RigorLoop workflow test spec](../../specs/rigorloop-workflow.test.md), [Workflow stage autoprogression test spec](../../specs/workflow-stage-autoprogression.test.md), [Milestone-aware review handoff test spec](../../specs/milestone-aware-review-handoff.test.md), and [Skill contract test spec](../../specs/skill-contract.test.md).
- Project map: `docs/project-map.md` is absent. No-map rationale: this plan does not rely on repository-map claims for runtime ownership, data flow, deployment, or module boundaries. Orientation comes from `CONSTITUTION.md`, `AGENTS.md`, the accepted proposal, amended specs, canonical architecture package, current skill files, generator scripts, and existing validator patterns.
- Review records: `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md` and `review-resolution.md` record proposal-review R1/R2, spec-review R1-R5, architecture-review R1, plan-review R1/R2, and code-review R1-R5. CR1, CR2, and CR3 are resolved; M1, M2, and M3 code-review reruns are clean.

## Context and Orientation

- `CONSTITUTION.md` owns governance principles, including one standard workflow, isolated manual skill invocation, generated-output boundaries, and final verification expectations.
- `specs/rigorloop-workflow.md` owns stage order, stage obligations, manual skill isolation, active-plan transition notes, and final closeout order.
- `specs/workflow-stage-autoprogression.md` owns workflow-managed continuation into mandatory or triggered downstream stages and must preserve isolated direct-stage behavior.
- `specs/skill-contract.md` owns public skill portability boundaries and claim-safe skill structure.
- `docs/workflows.md`, `AGENTS.md`, and `README.md` are contributor-facing summaries that must not compete with the governing specs.
- Canonical skill sources live under `skills/`. `.codex/skills/` and `dist/adapters/` are generated output and must be refreshed by `scripts/build-skills.py` and `scripts/build-adapters.py`, not hand-edited.
- Public skill portability proof lives primarily in `scripts/test-skill-validator.py` and generated-output drift checks.
- `scripts/select-validation.py` and `scripts/ci.sh` are the routing and selected-CI wrappers for this change.
- The visible workflow action is `ci-maintenance`, while the current skill entrypoint remains `skills/ci/SKILL.md`.

## Non-Goals

- Do not create a separate small-change, risk-based, fast-lane, full-lane, or mini-spec route.
- Do not remove `spec`, `code-review`, `explain-change`, `verify`, or `pr` from the workflow.
- Do not make `docs/workflows.md` a competing workflow spec.
- Do not add a workflow-guide generator script in this change.
- Do not rename `skills/ci/` to `skills/ci-maintenance/`.
- Do not broaden public skill portability checks into semantic prose scoring.
- Do not hand-edit generated `.codex/skills/` or `dist/adapters/` output.
- Do not mark the initiative done until code-review, required review-resolution, `ci-maintenance` when triggered, `explain-change`, `verify`, and PR handoff are complete.

## Requirements Covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| Workflow `R1`-`R5` | Standard workflow, isolated manual skill invocation, and completion-claim boundaries in specs, docs, skills, and generated output. |
| Workflow `R6d`-`R6n` | Affected-surface alignment, `docs/workflows.md` guide ownership, and the active-plan transition note in this plan. |
| Workflow `R7`-`R7q` | Stage-obligation table, workflow-managed continuation, isolated stage behavior, immediate handoff vs downstream readiness, and test-spec prerequisites. |
| Workflow `R7x`-`R8j` | Milestone-aware implementation loop, final closeout readiness, plan index synchronization, and stale plan-state blocking behavior. |
| Workflow `R10`-`R10h` | Durable rationale before final verify and `verify` checking current `explain-change.md` rather than creating it. |
| Autoprogression `R1`-`R5` | Workflow-managed continuation into mandatory or triggered downstream stages while preserving isolated direct invocations. |
| Skill contract `R3d`-`R3l`, `R12b`, `R20`-`R20b` | Project-portable published skill text, public skill allow/block boundary, generated/public adapter scope, and source-of-truth ordering. |
| Architecture package method | Direct canonical architecture update for the lowest sufficient architecture surface, with C4 diagrams kept in the canonical package. |

## Workflow Transition Note

This plan uses the current final order:

```text
explain-change -> verify -> pr
```

Prior verification evidence recorded before `explain-change` is preliminary. Final `verify` must run after the durable `explain-change.md` artifact exists, is current, and covers the final changed surfaces. When `ci-maintenance` is triggered by validation automation or hosted workflow automation changes, it runs before `explain-change`.

## Current Handoff Summary

- Current milestone: M5. Review Evidence and Selected Validation
- Current milestone state: review-requested
- Last reviewed milestone: M4
- Review status: code-review R6 returned `clean-with-notes` with no material findings. M4 is closed; M5 review evidence and selected validation are ready for code-review.
- Commit status: M1 and M2 closeout was corrected with a scoped catch-up milestone commit before continuing M3. M3 review-resolution changes are included in the `M3: align public skill workflow surfaces` handoff commit before M3 closeout. M4 generated-output confirmation has a handoff commit before M4 closeout. M5 review-evidence work has a handoff commit before review. Future milestone closeout must not mark a milestone closed until the milestone commit exists.
- Remaining in-scope implementation milestones: M5 code-review pending.
- Next stage: `code-review M5`
- Final closeout readiness: not ready
- Reason final closeout is not ready: code-review M5, required review-resolution if triggered, `ci-maintenance` if triggered, `explain-change`, final `verify`, and `pr` remain.

## Milestones

### M1. Source Artifact Lifecycle and Review Readiness

- Milestone state: closed
- Goal: Normalize source artifact lifecycle state after architecture-review approval and remove stale readiness language that still describes already completed spec-review as future work.
- Requirements: Workflow `R6d`-`R6n`, `R7p`-`R7q`, `R8f`-`R8j`, `R8ke`; architecture package method.
- Files/components likely touched:
  - `specs/rigorloop-workflow.md`
  - `specs/workflow-stage-autoprogression.md`
  - `specs/skill-contract.md`
  - `docs/architecture/system/architecture.md`
  - `docs/architecture/system/diagrams/context.mmd`
  - `docs/architecture/system/diagrams/container.mmd`
  - `docs/plan.md`
  - `docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md`
  - `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml`
- Dependencies:
  - Architecture-review R1 approved the latest direct canonical package update.
  - Plan-review approval before implementation milestones proceed.
- Tests to add/update:
  - Lifecycle validation for the touched specs, architecture package, plan index, plan body, and change metadata.
  - Static stale-wording checks when lifecycle wording is machine-checkable.
- Implementation steps:
  - After architecture-review approval, update canonical architecture package status and readiness if the review result permits it.
  - Normalize amended spec `Status`, `Next artifacts`, `Follow-on artifacts`, and `Readiness` sections so they reflect spec-review R5 approval and this active plan.
  - Keep `docs/plan.md` as an index, not a second plan body.
  - Keep `change.yaml` artifact links current, including this plan.
- Validation commands:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/architecture/system/architecture.md --path specs/rigorloop-workflow.md --path specs/workflow-stage-autoprogression.md --path specs/skill-contract.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/architecture/system/architecture.md --path specs/rigorloop-workflow.md --path specs/workflow-stage-autoprogression.md --path specs/skill-contract.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml`
- Expected observable result: Source artifacts no longer say this amendment is waiting for completed spec-review, and implementation can rely on reviewed architecture and current lifecycle metadata.
- Commit message: `M1: normalize workflow governance lifecycle sources`
- Commit status: covered by the scoped M1/M2 catch-up milestone commit because M1 had already been marked closed before any initiative commit existed.
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed before downstream continuation
- Risks:
  - Updating lifecycle state before architecture-review would overclaim architecture readiness.
  - Leaving stale draft/readiness text can block final verify.
- Rollback/recovery:
  - Revert only the lifecycle-state edits for the affected artifacts and keep the plan active with the blocker named.

### M2. Workflow Contract and Contributor Guidance Alignment

- Milestone state: closed
- Goal: Align the authoritative workflow contract and contributor-facing summaries to one standard workflow, isolated manual skill invocation, and final closeout order.
- Requirements: Workflow `R1`-`R7q`, `R10`-`R10h`; autoprogression `R1`-`R5`.
- Files/components likely touched:
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `README.md`
  - `docs/workflows.md`
  - `specs/rigorloop-workflow.md`
  - `specs/rigorloop-workflow.test.md`
  - `specs/workflow-stage-autoprogression.md`
  - `specs/workflow-stage-autoprogression.test.md`
  - `specs/milestone-aware-review-handoff.md`
  - `specs/milestone-aware-review-handoff.test.md`
  - `specs/skill-contract.md`
  - `specs/skill-contract.test.md`
  - `scripts/test-skill-validator.py`
- Dependencies:
  - M1 lifecycle state or an explicit plan note explaining any intentionally deferred source state.
- Tests to add/update:
  - Test-spec cases for one recommended standard workflow.
  - Test-spec cases for isolated manual skill invocation.
  - Test-spec cases for `ci-maintenance` when triggered before `explain-change`.
  - Test-spec cases for final `explain-change -> verify -> pr`.
  - Static checks for retired lane and direct-verify closeout phrases.
- Implementation steps:
  - Remove public route vocabulary that reintroduces size, risk, speed, or completeness lanes.
  - Replace direct final-milestone-to-`verify` wording with final closeout readiness.
  - Keep isolated direct `verify` behavior intact.
  - Refresh `docs/workflows.md` as the readable workflow guide without making it a competing spec.
  - Keep `AGENTS.md` concise and defer detailed lifecycle wording to `docs/workflows.md` and specs.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path README.md --path docs/workflows.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path specs/workflow-stage-autoprogression.md --path specs/workflow-stage-autoprogression.test.md --path specs/milestone-aware-review-handoff.md --path specs/milestone-aware-review-handoff.test.md --path specs/skill-contract.md --path specs/skill-contract.test.md --path scripts/test-skill-validator.py`
  - `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path README.md --path docs/workflows.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path specs/workflow-stage-autoprogression.md --path specs/workflow-stage-autoprogression.test.md --path specs/milestone-aware-review-handoff.md --path specs/milestone-aware-review-handoff.test.md --path specs/skill-contract.md --path specs/skill-contract.test.md --path scripts/test-skill-validator.py`
- Expected observable result: Public workflow and governing docs describe one workflow, manual isolated skill invocation, and the current final closeout order.
- Implementation handoff:
  - M2 source and contributor guidance alignment is complete.
  - `scripts/test-skill-validator.py` was updated to assert final-closeout wording instead of the retired direct-verify test title.
  - Matching spec/test-spec tail sections now point at `code-review M2` and the remaining M3-M5 milestone loop rather than the already closed M1 handoff.
  - Targeted validation passed before handoff.
- Review closeout:
  - code-review R3 returned `clean-with-notes` with no material findings.
  - M2 is closed and the next stage is `implement M3`.
- Commit message: `M2: align standard workflow guidance`
- Commit status: covered by the scoped M1/M2 catch-up milestone commit because M2 had already been marked closed before any initiative commit existed.
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed before downstream continuation
- Risks:
  - Overcorrecting route vocabulary could remove ordinary risk recording fields such as `change.yaml` `risk`.
  - Duplicating too much spec detail in `AGENTS.md` or `docs/workflows.md` can create drift.
- Rollback/recovery:
  - Restore only the affected guidance text and keep the approved spec language as the source of truth for the next patch.

### M3. Canonical Skill and Public Skill Portability Alignment

- Milestone state: closed
- Goal: Update canonical skill guidance and static checks so shipped skills remain project-portable and claim-safe.
- Requirements: Skill contract `R3d`-`R3l`, `R12b`, `R20`-`R20b`; workflow `R1`-`R7q`.
- Files/components likely touched:
  - `skills/workflow/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/explain-change/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/spec/SKILL.md`
  - `skills/architecture/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `skills/constitution/SKILL.md`
  - other affected canonical skill files under `skills/`
  - `scripts/test-skill-validator.py`
  - `scripts/test-select-validation.py`
- Dependencies:
  - M2 public workflow contract and contributor wording.
- Tests to add/update:
  - Static checks that block retired route vocabulary using case-insensitive and hyphen/space-aware patterns.
  - Static checks that block repository-internal paths and maintainer-only mechanics in published skill text.
  - Static checks that preserve local handoff boundaries and isolated manual invocation behavior.
- Implementation steps:
  - Replace lane-selection guidance with standard workflow state and isolated manual skill invocation guidance.
  - Keep published skills from pointing users to RigorLoop repository-internal spec paths, generated mirror paths, adapter paths, selector commands, drift mechanics, or shared-block implementation details.
  - Preserve RigorLoop-maintainer details in specs, tests, plans, generator scripts, or contributor-only guidance where appropriate.
  - Keep `verify` as final validation owner and `explain-change` as durable rationale owner.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-select-validation.py`
  - `rg -n -i 'fast[- ]lane|full[- ]lane|full[- ]feature|low[- ]risk|high[- ]risk|tiny[[:space:]]+low[- ]risk|small[- ]change|mini[- ]spec|proportional[- ]evidence' README.md AGENTS.md CONSTITUTION.md docs/workflows.md skills .codex/skills dist/adapters`
  - `bash scripts/ci.sh --mode explicit --path skills --path scripts/test-skill-validator.py --path scripts/test-select-validation.py`
- Expected observable result: Canonical shipped skills use project-portable language and static checks prevent the retired route model from returning.
- Implementation handoff:
  - Canonical skill guidance no longer uses lane-selection language, retired route vocabulary, direct final-milestone-to-`verify` closeout, or repository-specific validation commands in shipped skill text.
  - `scripts/test-skill-validator.py` now checks published skill text surfaces for RigorLoop repository-internal paths and maintainer-only mechanics while leaving internal specs, plans, tests, generator scripts, and contributor docs out of scope.
  - `scripts/test-select-validation.py` now expects project-portable validation-selector and broad-validation wording in the canonical implementation and verification skills.
  - Targeted validation passed before handoff.
- Review status:
  - code-review R4 returned `changes-requested` with CR2 and CR3.
  - Review-resolution fixed CR2 and CR3 on the same milestone.
  - code-review R5 returned `clean-with-notes` with no material findings.
  - M3 is closed.
- Commit message: `M3: align public skill workflow surfaces`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - A static check that is too broad could block internal specs, tests, plans, or maintainer docs.
  - A static check that is too narrow could miss generated public adapter copies.
- Rollback/recovery:
  - Narrow the failed static check scope to shipped public skill surfaces and keep internal maintainer surfaces out of the portability block.

### M4. Generated Output and Adapter Refresh

- Milestone state: closed
- Milestone type: generated-output-confirmation
- Goal: Confirm derived Codex skill mirrors and public adapter packages remain current after M3 closeout, regenerating again only if M4 discovers drift or stale generated output.
- Requirements: Workflow `R6d`-`R6da`; skill contract `R2`, `R3i`-`R3j`, `R20`-`R20b`.
- Files/components likely touched:
  - `.codex/skills/`
  - `dist/adapters/`
  - `scripts/adapter_templates/`
  - `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml`
- Dependencies:
  - M3 canonical skill wording, validator changes, and code-review rerun.
- Tests to add/update:
  - Generated-output drift checks.
  - Adapter distribution checks if adapter package metadata or template output changes.
- Implementation steps:
  - Treat the CR2/CR3 generated-output refresh as already performed during M3 review-resolution.
  - Run generated-output drift checks after M3 closeout.
  - Regenerate with the skill and adapter generators only if M4 discovers drift or stale generated output.
  - Confirm generated public skill copies inherit the public portability cleanup.
  - Confirm adapter instructions do not expose maintainer-only repository mechanics.
- Validation commands:
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-skill-validator.py`
  - `bash scripts/ci.sh --mode explicit` with concrete generated and adapter-template paths from the M3 generated-output refresh; do not pass generated-output directories as selector paths.
- Expected observable result: Generated mirrors and adapter packages are in sync with canonical sources and remain project-portable after M3 closeout.
- Implementation handoff:
  - `python scripts/build-skills.py` and `python scripts/build-adapters.py --version 0.1.1` produced no tracked generated-output diff after M3 closeout.
  - Generated Codex skill mirrors and public adapter packages are in sync with canonical skill source.
  - Public skill portability checks still pass for generated mirrors and public adapter copies.
  - The original directory-form selected CI command was blocked by the selector; M4 replaced it with concrete generated and adapter-template path selection.
- Review status:
  - code-review R6 returned `clean-with-notes` with no material findings.
  - M4 is closed.
- Commit message: `M4: confirm generated workflow guidance`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Forgetting to regenerate one adapter family can leave drift that only final verify catches.
  - Hand-editing generated output can hide the canonical source problem.
- Rollback/recovery:
  - Re-run generators from canonical sources or revert generated output and fix the canonical source before regeneration.

### M5. Review Evidence and Selected Validation

- Milestone state: review-requested
- Goal: Complete implementation evidence, selected validation, code-review handoff, and review-resolution if findings are raised.
- Requirements: Workflow `R7x`-`R8j`, `R10`-`R10h`, `R12ao`; review-resolution contract.
- Files/components likely touched:
  - `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md`
  - `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md`
  - `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/`
  - `docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md`
  - `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml`
- Dependencies:
  - M1 through M4 implementation milestones complete enough for code-review.
- Tests to add/update:
  - Review artifact validation for any new formal review records.
  - Change metadata validation after validation evidence is added.
- Implementation steps:
  - Run selected validation over the final changed surface set.
  - Hand off the implemented milestones to `code-review`.
  - If material findings exist, record detailed review files, update `review-log.md`, and close dispositions in `review-resolution.md`.
  - Rerun selected validation after fixes.
  - Keep this plan's progress, decision log, surprises, and validation notes current.
- Validation commands:
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-08-single-workflow-lane-explain-before-verify`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-single-workflow-lane-explain-before-verify`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml`
  - `bash scripts/ci.sh --mode explicit` over concrete changed paths from the initiative range and current plan updates; do not pass `docs/changes/<change-id>/` as a directory selector path.
- Expected observable result: Code-review is complete or required review-resolution is explicitly open with current plan state; no final closeout claim is made while findings remain open.
- Implementation handoff:
  - Review artifact structure and closeout validation passed for all current review records.
  - Change metadata validation passed.
  - The original directory-form selected CI command was blocked by the selector; M5 replaced it with concrete changed paths from the initiative range and current plan update.
  - Concrete-path selected CI passed selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `readme.validate`, `readme.vision_markers`, and `selector.regression` checks.
- Review status:
  - M5 is ready for code-review.
- Commit message: `M5: record workflow governance review evidence`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Treating a clean artifact review as code-review can skip implementation-diff review.
  - Closing review-resolution with `needs-decision` findings would overclaim downstream readiness.
- Rollback/recovery:
  - Keep the milestone in `resolution-needed` and stop downstream handoff until findings are dispositioned or explicitly deferred by an authorized owner.

### M6. Lifecycle Closeout

- Milestone type: lifecycle-closeout
- Goal: Run the downstream lifecycle-closeout sequence without treating it as unfinished implementation work.
- Requirements: Workflow `R6m`-`R6n`, `R7xj`, `R8h`-`R8j`, `R10`-`R10h`.
- Files/components likely touched:
  - `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/explain-change.md`
  - `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/verify-report.md` if final verification requires standalone evidence
  - `docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md`
  - `docs/plan.md`
  - PR body or PR handoff evidence
- Dependencies:
  - All in-scope implementation milestones closed.
  - Required review-resolution closed.
  - `ci-maintenance` run when triggered by validation automation or hosted workflow automation changes.
- Tests to add/update:
  - Final selected CI and generated-output drift checks.
  - Verify checks for current `explain-change.md`.
  - Plan index/body lifecycle synchronization before PR handoff.
- Implementation steps:
  - Run `ci-maintenance` when triggered by final validation automation or hosted workflow automation changes.
  - Run `explain-change` and create or refresh durable rationale for the final diff.
  - Run `verify` after `explain-change.md` exists and is current.
  - Prepare PR handoff only after verify passes.
  - Update both `docs/plan.md` and this plan body if the initiative becomes done in the PR.
- Validation commands:
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-single-workflow-lane-explain-before-verify`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path <final changed paths>`
  - `git diff --check -- <final changed paths>`
- Expected observable result: Final closeout evidence supports PR handoff without stale lifecycle state between `docs/plan.md` and this plan.
- Commit message: `M6: close workflow governance lifecycle`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Running verify before explain-change would recreate the ordering bug this initiative fixes.
  - Updating only `docs/plan.md` or only this plan body would block verify for planned initiative state drift.
- Rollback/recovery:
  - Keep the plan active and name the missing downstream gate rather than marking it done prematurely.

## Validation Plan

- Start with the smallest selected scope for the files touched in each milestone.
- Use `python scripts/select-validation.py --mode explicit --path ...` before broad command runs when the changed path set is large.
- Use `bash scripts/ci.sh --mode explicit --path ...` for selected CI over changed authoritative surfaces.
- Run `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, and generated-output checks after canonical skill edits.
- Run `python scripts/build-skills.py --check` and `python scripts/build-adapters.py --version 0.1.1 --check` after generated output is refreshed.
- Run `python scripts/validate-review-artifacts.py --mode closeout ...` whenever new detailed review records or dispositions are added.
- Run `git diff --check -- <final changed paths>` and a whitespace scan before final handoff.

## Risks and Recovery

- Risk: Lifecycle source artifacts remain stale after review approval. Recovery: normalize only the affected status/readiness sections and validate lifecycle explicitly before implementation review.
- Risk: Public skill static checks block internal maintainer docs. Recovery: narrow portability scans to canonical shipped skill files, generated public skill copies, and public adapter skill copies.
- Risk: Generated output drifts from canonical skill sources. Recovery: fix canonical source, rerun generators, and check generated-output drift.
- Risk: A late review finding changes workflow wording after generated output is refreshed. Recovery: apply the fix to canonical sources first, rerun generated output, then repeat selected validation.
- Risk: Final closeout is claimed before `explain-change`. Recovery: keep final closeout readiness `not ready`, create/refresh `explain-change.md`, then rerun verify.

## Dependencies

- Architecture-review R1 approved the latest canonical architecture package update before implementation relies on that design.
- Plan-review must approve this plan before implementation proceeds as workflow-managed planned work.
- Test-spec confirmation must cover the approved spec amendments, changed static checks, and generated-output drift proof before implementation commits are treated as review-ready.
- Generated output depends on canonical `skills/` and `scripts/adapter_templates/` sources.
- Final closeout depends on closed implementation milestones, required review-resolution closeout, `ci-maintenance` when triggered, current explain-change, final verify, and PR handoff.

## Progress

- [x] Proposal accepted after proposal-review R2.
- [x] Spec-review R1-R5 recorded and closed with no unresolved findings.
- [x] Direct canonical architecture package update drafted.
- [x] C4 context and container diagrams updated with the direct architecture design.
- [x] Change metadata records architecture-package validation evidence.
- [x] Architecture-review for the latest canonical architecture package update.
- [x] Plan-review for this execution plan.
- [x] Test-spec confirmation for the final implementation proof map.
- [x] M1 source artifact lifecycle normalization closed after clean code-review R2 and corrected with the scoped M1/M2 catch-up milestone commit.
- [x] M2 workflow contract and contributor guidance alignment closed after clean code-review R3 and corrected with the scoped M1/M2 catch-up milestone commit.
- [x] M3 canonical skill and public skill portability alignment closed after clean code-review R5.
- [x] M4 generated output and adapter confirmation closed after clean code-review R6.
- [ ] M5 review evidence and selected validation implementation complete; code-review required before closeout.
- [ ] M6 lifecycle closeout.

## Decision Log

- 2026-05-08: Use a catch-up active plan rather than pretending implementation has not started. Rationale: proposal/spec/architecture work and draft implementation edits already exist in the working tree, but downstream gates still need a durable plan for review, validation, and closeout.
- 2026-05-08: Keep latest architecture review as the next stage before plan-review. Rationale: the canonical architecture package changed after the earlier architecture-review discussion, so the latest C4 diagram update should be reviewed before implementation relies on it.
- 2026-05-08: Treat `ci-maintenance` as expected when final changes include validation automation or hosted workflow automation updates. Rationale: the accepted workflow places automation maintenance before explain-change so rationale covers the final diff.
- 2026-05-08: Plan-review R2 approved this execution plan after architecture-review status/readiness and test-spec readiness wording were normalized. Rationale: PLR1, PLR2, and PLR3 source fixes removed the plan-review blockers.
- 2026-05-08: M1 uses approved lifecycle status in the touched specs while avoiding `Ready for implement` readiness phrasing. Rationale: lifecycle validation treats that wording as a stale earlier-stage readiness claim on approved specs.
- 2026-05-08: Code-review R1 moved M1 to review-resolution for CR1. Rationale: the current handoff and M1 milestone section exposed conflicting M1 lifecycle states.
- 2026-05-08: CR1 closed as already fixed by review bookkeeping. Rationale: the current handoff, M1 milestone section, review log, review resolution, plan index, and change metadata now consistently route M1 to code-review rerun.
- 2026-05-08: Code-review R2 closed M1 with no material findings. Rationale: M1 lifecycle/readiness state, review-resolution closeout, plan index, and change metadata are consistent and selected validation passes.
- 2026-05-08: M2 kept generated skill mirrors and adapter package regeneration out of scope. Rationale: M2 aligns governing workflow and contributor guidance; M3 owns canonical skill wording and M4 owns generated output refresh.
- 2026-05-08: M2 updated a stale static assertion title from direct-verify wording to final-closeout wording. Rationale: the test should guard the current milestone-aware contract and not require retired direct-verify language.
- 2026-05-08: Code-review R3 closed M2 with no material findings. Rationale: M2 workflow contract and contributor guidance align to one standard workflow, isolated manual skill invocation, and final closeout order while M3 and M4 continue to own canonical skill and generated-output surfaces.
- 2026-05-08: M1/M2 closeout was corrected with a scoped catch-up milestone commit before continuing M3. Rationale: M1 and M2 were marked closed after clean reviews, but no initiative commit existed; the mixed M3 worktree made exact historical per-milestone snapshots unsafe to reconstruct, so the correction commit records the closed M1/M2 source, guidance, review, and lifecycle surfaces while leaving unresolved M3 implementation work unclosed.
- 2026-05-08: M3 keeps the public skill portability check scoped to published skill text surfaces rather than every repository doc or adapter manifest. Rationale: shipped skill text must be project-portable, while maintainer docs, specs, tests, generator scripts, contributor guidance, and package manifests can still name repository mechanics.
- 2026-05-08: Code-review R4 moves M3 to review-resolution. Rationale: the public `code-review` and `verify` skill text still contains stale final-closeout ordering language that current static checks missed.
- 2026-05-08: CR2/CR3 review-resolution refreshed generated skill mirrors and adapter packages inside M3. Rationale: the accepted findings named generated public copies as affected surfaces, so generated-output correction had to happen before M3 code-review R5 rather than wait for a later standalone refresh.
- 2026-05-08: Code-review R5 closed M3 with no material findings. Rationale: CR2 and CR3 are fixed in canonical `code-review` and `verify` skill text, generated public copies are in sync, and static wording checks now reject the stale final-closeout phrases.
- 2026-05-08: M4 replaced the approved directory-form selected CI command with concrete generated-output path selection. Rationale: the selector intentionally blocks `.codex/skills`, `dist/adapters`, and `scripts/adapter_templates` directory paths; concrete generated files select the same stable drift and adapter checks without hiding unclassified paths.
- 2026-05-08: Code-review R6 closed M4 with no material findings. Rationale: generated Codex skill mirrors and public adapter packages are in sync, adapter validation passes, public skill portability checks pass, and the stale directory-form selected CI command has a concrete-path replacement.
- 2026-05-08: M5 replaced the planned `docs/changes/<change-id>/` directory selected CI command with concrete changed paths from the initiative range. Rationale: the selector intentionally blocks the change-local directory path in explicit mode; concrete files select the intended review-artifact, lifecycle, metadata, skill, adapter, README, and selector checks.

## Surprises and Discoveries

- The latest spec-review result is approved, but several touched spec files still have draft/readiness sections that describe `spec-review` as future work.
- The architecture package was updated directly, which avoids a change-local merge-back loop. Architecture-review R1 approved that direct canonical update before implementation relies on it.
- `docs/project-map.md` is absent; this plan does not rely on it.
- The existing test-spec surfaces already covered most behavioral assertions, but their related-plan and readiness sections needed alignment to the active 2026-05-08 plan before implementation M1 could start cleanly.
- Initial M1 lifecycle validation blocked on approved specs that still used `Ready for implement` wording. Rephrasing readiness as active-plan reliance fixed the inconsistency without changing the approved workflow contract.
- During M2, the first `python scripts/test-skill-validator.py` run failed because the validator still expected `T4. Inconclusive or ambiguous review never hands off to verify`. Updating the assertion to `T4. Inconclusive or ambiguous review never starts final closeout` fixed the stale test expectation.
- Code-review R3 confirmed that dirty canonical skill and generated-output files remain outside M2 closeout and are still planned for M3 and M4 review before branch-ready claims.
- M1 and M2 were mistakenly marked closed before an initiative commit existed. The closeout fix is a scoped catch-up commit covering the completed M1/M2 surfaces; future milestones must not be marked closed until their commit exists.
- M3's new published-skill portability check also scans generated skill copies under `.codex/skills/` and public adapter skill copies under `dist/adapters/`, but it does not prove generated-output drift. M4 still owns generator execution and drift checks.
- Code-review R4 found that generated skill copies can be drift-clean while still faithfully reproducing a canonical skill wording bug. The static checks need phrase coverage for the stale final-closeout claims, not only drift checks.
- CR2/CR3 turned part of M4 into M3 review-resolution scope because shipped generated copies carried the same canonical wording bug. M4 remains as a final generated-output confirmation after M3 closeout.
- Code-review R5 confirmed that M3 is clean after CR2/CR3 review-resolution. M4 remains useful as a final generated-output confirmation milestone because generated copies changed during M3 review-resolution.
- M4 generator execution after M3 closeout produced no tracked generated-output diff. The confirmation still found one stale plan command that used generated-output directories as selector paths; concrete generated files select the intended drift and adapter checks.
- Code-review R6 confirmed M4 is clean. The remaining implementation work is M5 review evidence and selected validation.
- M5 found the same directory-selector pattern for the change-local root. Concrete changed paths from the initiative range selected the intended final proof set without unclassified paths.

## Validation Notes

- 2026-05-08 architecture diagram update validation:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/context.mmd --path docs/architecture/system/diagrams/container.mmd --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed with the existing unrelated `specs/rigorloop-workflow.md` lifecycle-language warning.
  - `python scripts/select-validation.py --mode explicit --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/context.mmd --path docs/architecture/system/diagrams/container.mmd --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed with no unclassified paths.
  - `bash scripts/ci.sh --mode explicit --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/context.mmd --path docs/architecture/system/diagrams/container.mmd --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.
- 2026-05-08 plan creation validation:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/architecture/system/architecture.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed with existing `docs/plan.md` and `specs/rigorloop-workflow.md` lifecycle-language warnings.
  - `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/context.mmd --path docs/architecture/system/diagrams/container.mmd --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed with no unclassified paths.
  - `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/context.mmd --path docs/architecture/system/diagrams/container.mmd --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.
  - `python scripts/test-change-metadata-validator.py` passed.
  - `git diff --check -- docs/plan.md docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md docs/architecture/system/architecture.md docs/architecture/system/diagrams/context.mmd docs/architecture/system/diagrams/container.mmd docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.
  - Whitespace scan for the same paths passed.
- 2026-05-08 plan-review rerun validation:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-single-workflow-lane-explain-before-verify` passed.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.
  - `bash scripts/ci.sh --mode explicit --path docs/architecture/system/architecture.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/plan-review-r2.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.
- 2026-05-08 test-spec proof-map validation:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/rigorloop-workflow.test.md --path specs/workflow-stage-autoprogression.test.md --path specs/milestone-aware-review-handoff.test.md --path specs/skill-contract.test.md --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed with existing nonblocking lifecycle-language warnings.
  - `python scripts/select-validation.py --mode explicit --path specs/rigorloop-workflow.test.md --path specs/workflow-stage-autoprogression.test.md --path specs/milestone-aware-review-handoff.test.md --path specs/skill-contract.test.md --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed with no unclassified paths.
  - `bash scripts/ci.sh --mode explicit --path specs/rigorloop-workflow.test.md --path specs/workflow-stage-autoprogression.test.md --path specs/milestone-aware-review-handoff.test.md --path specs/skill-contract.test.md --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.
  - `python scripts/test-change-metadata-validator.py` passed.
  - `git diff --check -- specs/rigorloop-workflow.test.md specs/workflow-stage-autoprogression.test.md specs/milestone-aware-review-handoff.test.md specs/skill-contract.test.md docs/plan.md docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.
  - Whitespace scan and stale direct-verify closeout wording scan for the same proof-map surfaces passed.
- 2026-05-08 M1 source artifact lifecycle validation:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/architecture/system/architecture.md --path specs/rigorloop-workflow.md --path specs/workflow-stage-autoprogression.md --path specs/skill-contract.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` initially failed on stale approved-spec readiness wording, then passed with existing nonblocking lifecycle-language warnings.
  - `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/architecture/system/architecture.md --path specs/rigorloop-workflow.md --path specs/workflow-stage-autoprogression.md --path specs/skill-contract.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed with no unclassified paths.
  - `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/architecture/system/architecture.md --path specs/rigorloop-workflow.md --path specs/workflow-stage-autoprogression.md --path specs/skill-contract.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.
  - `git diff --check -- docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md specs/rigorloop-workflow.md specs/workflow-stage-autoprogression.md specs/skill-contract.md docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.
  - Whitespace scan for M1 touched paths passed.
- 2026-05-08 code-review R1 recording validation:
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-08-single-workflow-lane-explain-before-verify` passed with 11 reviews, 21 findings, 11 log entries, and 21 resolution entries.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.
  - `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/code-review-r1.md` passed with no unclassified paths.
  - `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/code-review-r1.md` passed selected review artifact, lifecycle, change-metadata regression, and change-metadata validation checks.
  - `git diff --check -- docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md docs/plan.md docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/code-review-r1.md` passed.
  - Whitespace scan for the code-review R1 recording surface passed.
- 2026-05-08 CR1 review-resolution closeout validation:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-single-workflow-lane-explain-before-verify` passed with 11 reviews, 21 findings, 11 log entries, and 21 resolution entries.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.
  - `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md` passed with no unclassified paths.
  - `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md` passed selected review artifact, lifecycle, change-metadata regression, and change-metadata validation checks.
  - `git diff --check -- docs/plan.md docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md` passed.
  - Whitespace scan for the CR1 closeout surface passed.
- 2026-05-08 code-review R2 and M1 closeout validation:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-single-workflow-lane-explain-before-verify` passed with 12 reviews, 21 findings, 12 log entries, and 21 resolution entries.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.
  - `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/architecture/system/architecture.md --path specs/rigorloop-workflow.md --path specs/workflow-stage-autoprogression.md --path specs/skill-contract.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/code-review-r2.md` passed with no unclassified paths.
  - `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/architecture/system/architecture.md --path specs/rigorloop-workflow.md --path specs/workflow-stage-autoprogression.md --path specs/skill-contract.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/code-review-r2.md` passed selected review artifact, lifecycle, change-metadata regression, and change-metadata validation checks.
  - `git diff --check -- docs/plan.md docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/code-review-r2.md` passed.
  - Whitespace scan for the code-review R2 and M1 closeout surface passed.
- 2026-05-08 M2 workflow contract and contributor guidance validation:
  - `python scripts/test-skill-validator.py` initially failed on a stale direct-verify test-title assertion, then passed after the assertion was updated to final-closeout wording.
  - `python scripts/test-select-validation.py` passed.
  - `python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path README.md --path docs/workflows.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path specs/workflow-stage-autoprogression.md --path specs/workflow-stage-autoprogression.test.md --path specs/milestone-aware-review-handoff.md --path specs/milestone-aware-review-handoff.test.md` passed with no unclassified paths.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.
  - `python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path README.md --path docs/workflows.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path specs/workflow-stage-autoprogression.md --path specs/workflow-stage-autoprogression.test.md --path specs/milestone-aware-review-handoff.md --path specs/milestone-aware-review-handoff.test.md --path specs/skill-contract.md --path specs/skill-contract.test.md --path scripts/test-skill-validator.py --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed with no unclassified paths.
  - `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path README.md --path docs/workflows.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path specs/workflow-stage-autoprogression.md --path specs/workflow-stage-autoprogression.test.md --path specs/milestone-aware-review-handoff.md --path specs/milestone-aware-review-handoff.test.md --path specs/skill-contract.md --path specs/skill-contract.test.md --path scripts/test-skill-validator.py --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed selected `skills.regression`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `readme.validate`, `readme.vision_markers`, and `selector.regression` checks.
  - `git diff --check -- CONSTITUTION.md AGENTS.md README.md docs/workflows.md specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md specs/workflow-stage-autoprogression.md specs/workflow-stage-autoprogression.test.md specs/milestone-aware-review-handoff.md specs/milestone-aware-review-handoff.test.md specs/skill-contract.md specs/skill-contract.test.md scripts/test-skill-validator.py docs/plan.md docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.
  - Whitespace scan for the same M2 handoff paths passed.
  - Final M2 bookkeeping validation after plan and change metadata updates: `python scripts/validate-change-metadata.py docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml`, `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml`, `git diff --check -- docs/plan.md docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml`, and a whitespace scan for the same paths passed.
- 2026-05-08 code-review R3 and M2 closeout validation:
  - `python scripts/test-skill-validator.py` passed during code-review R3 evidence refresh.
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-single-workflow-lane-explain-before-verify` passed with 13 reviews, 21 findings, 13 log entries, and 21 resolution entries.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.
  - `python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path README.md --path docs/workflows.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path specs/workflow-stage-autoprogression.md --path specs/workflow-stage-autoprogression.test.md --path specs/milestone-aware-review-handoff.md --path specs/milestone-aware-review-handoff.test.md --path specs/skill-contract.md --path specs/skill-contract.test.md --path scripts/test-skill-validator.py --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/code-review-r3.md` passed with no unclassified paths.
  - `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path README.md --path docs/workflows.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path specs/workflow-stage-autoprogression.md --path specs/workflow-stage-autoprogression.test.md --path specs/milestone-aware-review-handoff.md --path specs/milestone-aware-review-handoff.test.md --path specs/skill-contract.md --path specs/skill-contract.test.md --path scripts/test-skill-validator.py --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/code-review-r3.md` passed selected skills, review-artifact, artifact-lifecycle, change-metadata, README, and selector checks.
  - `git diff --check -- CONSTITUTION.md AGENTS.md README.md docs/workflows.md specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md specs/workflow-stage-autoprogression.md specs/workflow-stage-autoprogression.test.md specs/milestone-aware-review-handoff.md specs/milestone-aware-review-handoff.test.md specs/skill-contract.md specs/skill-contract.test.md scripts/test-skill-validator.py docs/plan.md docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/code-review-r3.md` passed.
  - Whitespace scan for the same M2 closeout paths passed.
  - Final bookkeeping validation after recording the code-review R3 evidence passed: review-artifact closeout validation, change-metadata validation, selected CI over plan/index/change/review artifacts, diff check, and whitespace scan.
- 2026-05-08 M1/M2 closeout commit correction validation:
  - Commit correction scope is limited to M1/M2 source, guidance, review, and lifecycle surfaces plus the already-recorded current plan state. Unresolved M3 canonical skill and generated-output changes remain unclosed for review-resolution.
  - Commit subject: `M1-M2: record workflow governance milestone closeout`.
- 2026-05-08 M3 canonical skill and public skill portability validation:
  - `python scripts/validate-skills.py` passed for 23 canonical skill files.
  - `python scripts/test-skill-validator.py` passed 46 tests, including the new published-skill internal-detail portability check.
  - `python scripts/test-select-validation.py` passed 57 tests.
  - Retired-route wording scan over `README.md`, `AGENTS.md`, `CONSTITUTION.md`, `docs/workflows.md`, `skills`, `.codex/skills`, and `dist/adapters` returned no matches.
  - `python scripts/select-validation.py --mode explicit --path skills/workflow/SKILL.md --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path skills/explain-change/SKILL.md --path skills/verify/SKILL.md --path skills/pr/SKILL.md --path skills/plan/SKILL.md --path skills/spec/SKILL.md --path skills/architecture/SKILL.md --path skills/architecture-review/SKILL.md --path skills/constitution/SKILL.md --path skills/ci/SKILL.md --path skills/explore/SKILL.md --path skills/project-map/SKILL.md --path skills/test-spec/SKILL.md --path scripts/test-skill-validator.py --path scripts/test-select-validation.py --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed with no unclassified paths.
  - `bash scripts/ci.sh --mode explicit --path skills/workflow/SKILL.md --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path skills/explain-change/SKILL.md --path skills/verify/SKILL.md --path skills/pr/SKILL.md --path skills/plan/SKILL.md --path skills/spec/SKILL.md --path skills/architecture/SKILL.md --path skills/architecture-review/SKILL.md --path skills/constitution/SKILL.md --path skills/ci/SKILL.md --path skills/explore/SKILL.md --path skills/project-map/SKILL.md --path skills/test-spec/SKILL.md --path scripts/test-skill-validator.py --path scripts/test-select-validation.py --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.drift`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression` checks.
  - `git diff --check -- skills/workflow/SKILL.md skills/implement/SKILL.md skills/code-review/SKILL.md skills/explain-change/SKILL.md skills/verify/SKILL.md skills/pr/SKILL.md skills/plan/SKILL.md skills/spec/SKILL.md skills/architecture/SKILL.md skills/architecture-review/SKILL.md skills/constitution/SKILL.md skills/ci/SKILL.md skills/explore/SKILL.md skills/project-map/SKILL.md skills/test-spec/SKILL.md scripts/test-skill-validator.py scripts/test-select-validation.py docs/plan.md docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.
  - Whitespace scan for the same M3 handoff paths passed.
  - Final M3 bookkeeping validation after recording handoff evidence passed: change metadata validation, selected CI over plan/index/change metadata, diff check, and whitespace scan.
- 2026-05-08 code-review R4 recording validation:
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-08-single-workflow-lane-explain-before-verify` passed with 14 reviews, 23 findings, 14 log entries, and 23 resolution entries.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.
  - `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/code-review-r4.md` passed with no unclassified paths and selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
  - `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/code-review-r4.md` passed selected review-artifact, lifecycle, change-metadata regression, and change-metadata validation checks.
  - `git diff --check -- docs/plan.md docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/code-review-r4.md` passed.
  - Whitespace scan for the same code-review R4 recording paths passed.
- 2026-05-08 CR2/CR3 review-resolution validation:
  - `python scripts/validate-skills.py` passed for 23 canonical skill files.
  - `python scripts/test-skill-validator.py` passed 47 tests, including stale final-closeout wording checks for public `code-review` and `verify` skill copies.
  - `python scripts/test-select-validation.py` passed 57 tests.
  - `python scripts/build-skills.py` refreshed `.codex/skills` from canonical skills.
  - `python scripts/build-adapters.py --version 0.1.1` refreshed public adapter packages.
  - `python scripts/build-skills.py --check` passed.
  - `python scripts/build-adapters.py --version 0.1.1 --check` passed.
  - `python scripts/test-adapter-distribution.py` passed 56 tests.
  - Stale final-closeout wording scan over `skills`, `.codex/skills`, and `dist/adapters` returned no matches.
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-single-workflow-lane-explain-before-verify` passed with 14 reviews, 23 findings, 14 log entries, and 23 resolution entries.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.
  - `bash scripts/ci.sh --mode explicit` over the full dirty path set passed selected skills, adapter, review artifact, lifecycle, change metadata, and selector checks.
  - `git diff --check -- $(git diff --name-only)` passed.
  - Whitespace scan over the full dirty path set passed.
- 2026-05-08 code-review R5 rerun validation:
  - `python scripts/validate-skills.py` passed for 23 canonical skill files.
  - `python scripts/test-skill-validator.py` passed 47 tests, including stale final-closeout wording checks for public `code-review` and `verify` skill copies.
  - `python scripts/test-select-validation.py` passed 57 tests.
  - `python scripts/build-skills.py --check` passed.
  - `python scripts/build-adapters.py --version 0.1.1 --check` passed.
  - `python scripts/test-adapter-distribution.py` passed 56 tests.
  - `python scripts/validate-adapters.py --version 0.1.1` passed.
  - Stale final-closeout wording scan over `skills`, `.codex/skills`, and `dist/adapters` returned no matches.
- 2026-05-08 M4 generated-output confirmation validation:
  - `python scripts/build-skills.py` passed and produced no tracked generated-output diff.
  - `python scripts/build-adapters.py --version 0.1.1` passed and produced no tracked generated-output diff.
  - `python scripts/build-skills.py --check` passed.
  - `python scripts/build-adapters.py --version 0.1.1 --check` passed.
  - `python scripts/validate-adapters.py --version 0.1.1` passed.
  - `python scripts/test-adapter-distribution.py` passed 56 tests.
  - `python scripts/test-skill-validator.py` passed 47 tests, including public skill portability checks over generated mirrors and public adapter skill copies.
  - `bash scripts/ci.sh --mode explicit --path .codex/skills --path dist/adapters --path scripts/adapter_templates` failed with selector blocking results for directory paths; this exposed a stale M4 plan command, not generated-output drift.
  - `bash -c 'args=(); while IFS= read -r path; do args+=(--path "$path"); done < <(git diff --name-only b742d0e..426d4bc -- .codex/skills dist/adapters scripts/adapter_templates); bash scripts/ci.sh --mode explicit "${args[@]}"'` passed selected `skills.drift`, `adapters.regression`, `adapters.drift`, and `adapters.validate` checks over concrete generated and adapter-template files.
- 2026-05-08 code-review R6 recording validation:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-single-workflow-lane-explain-before-verify` passed with 16 reviews, 23 findings, 16 log entries, and 23 resolution entries.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.
  - `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/code-review-r6.md` passed selected review-artifact, lifecycle, change-metadata regression, and change-metadata validation checks.
  - `git diff --check -- docs/plan.md docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/code-review-r6.md` passed.
  - Whitespace scan for the same code-review R6 recording paths passed.
- 2026-05-08 M5 review evidence and selected validation:
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-08-single-workflow-lane-explain-before-verify` passed with 16 reviews, 23 findings, 16 log entries, and 23 resolution entries.
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-single-workflow-lane-explain-before-verify` passed with 16 reviews, 23 findings, 16 log entries, and 23 resolution entries.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml` passed.
  - `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-08-single-workflow-lane-explain-before-verify --path docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md` failed because the selector blocks the change-local directory path in explicit mode.
  - `bash -c 'args=(); while IFS= read -r path; do args+=(--path "$path"); done < <({ git diff --name-only 7915f4c..HEAD; git diff --name-only; } | sort -u); bash scripts/ci.sh --mode explicit "${args[@]}"'` passed selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `readme.validate`, `readme.vision_markers`, and `selector.regression` checks.

## Outcome and Retrospective

- Initiative remains active.
- M1 implementation is closed after clean code-review R2 and covered by the scoped M1/M2 catch-up milestone commit.
- M2 implementation is closed after clean code-review R3 and covered by the scoped M1/M2 catch-up milestone commit.
- M3 implementation is closed after CR2/CR3 review-resolution and clean code-review R5.
- M4 implementation is closed after generated-output confirmation and clean code-review R6.
- M5 implementation is ready for code-review after review evidence and selected validation.
- Final closeout is not ready.

## Readiness

- Next stage: `code-review M5`.
- Plan-review readiness: complete; plan-review R2 approved this plan.
- Test-spec readiness: complete; matching test specs confirm the proof map against the approved plan.
- Implementation readiness: M5 implementation is complete and ready for code-review. Later milestones remain gated by the milestone-specific validation, code-review, and review-resolution rules in this plan.
- Final closeout readiness: not ready until all in-scope implementation milestones are closed, required review-resolution is closed, `ci-maintenance` runs when triggered, `explain-change.md` exists and is current, `verify` passes, and PR handoff is prepared.

## Risks and Follow-Ups

- Follow-up: code-review M5.
- Follow-up: when the initiative reaches final closeout, update both `docs/plan.md` and this plan body in the same PR state transition.
