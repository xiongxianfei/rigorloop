# Guide System Source-of-Truth Alignment Plan

## Status

Plan lifecycle state: done
Terminal disposition: merged

- Change ID: `2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment`
- Current owner: agent
- Current stage: done
- Next stage: none
- Blockers: none

## Purpose / big picture

Implement the approved guide-system source-of-truth alignment contract. The change makes RigorLoop's guide surfaces easier to navigate without turning README, learn sessions, project-map, or plan index into competing workflow contracts. It also adds cross-guide drift validation and records proof that the new guide system can be used without chat history.

## Source artifacts

- Proposal: [RigorLoop Guide System Optimization and Source-of-Truth Alignment](../proposals/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment.md)
- Spec: [Guide System Source-of-Truth Alignment](../../specs/guide-system-source-of-truth-alignment.md)
- Architecture: not required; spec-review R1/R2 concluded this preserves existing architecture boundaries and is guide, skill-wording, validation-ownership, and proof-contract work.
- Test spec: [Guide System Source-of-Truth Alignment Test Spec](../../specs/guide-system-source-of-truth-alignment.test.md)
- Proposal review: [proposal-review-r1](../changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/reviews/proposal-review-r1.md)
- Spec reviews: [spec-review-r1](../changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/reviews/spec-review-r1.md), [spec-review-r2](../changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/reviews/spec-review-r2.md)
- Change metadata: [change.yaml](../changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml)

## Context and orientation

The implementation touches guide surfaces, canonical skill wording only when directly contradictory, validation scripts, and change-local proof artifacts.

Relevant surfaces:

- `README.md`: first-contact landing guide that should link out to primary guides without restating their full contracts.
- `docs/workflows.md`: project-local workflow guide and artifact-location map. It should gain guide ownership/source-rank guidance while preserving the workflow-map spec's registry contract.
- `docs/project-map.md`: repository orientation map. It may mention workflow surfaces for orientation but must not own workflow policy or lifecycle artifact placement.
- `docs/plan.md`: bounded live-work index. It must be updated with this active plan but must not become a long-form plan body.
- `skills/*/SKILL.md`: stage-skill portable defaults and placement text. Edit only direct contradictions in affected skills.
- `scripts/`: likely home for a dedicated guide-system validator or an artifact-lifecycle guide-system mode plus selector routing.
- `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/`: change-local metadata, review records, behavior-preservation proof, cold-read proof, explain-change, and later verify evidence.

## Non-goals

- Do not rewrite every guide in one slice.
- Do not create `docs/guides.md` in this slice.
- Do not change lifecycle stage order.
- Do not change artifact content schemas.
- Do not change exact artifact-location registry semantics outside the workflow-map contract.
- Do not make README the authoritative workflow manual.
- Do not make `docs/workflows.md` the only source for skill-only adopters.
- Do not treat learn sessions as live routing authority.
- Do not migrate historical artifacts in this slice.
- Do not add a new CLI scaffold.
- Do not hand-edit generated adapter output.
- Do not bulk-edit stage skills for style or symmetry.

## Requirements covered

- R1-R5: M1 classifies guide surfaces and updates README guide-index behavior.
- R6-R15: M1 preserves `VISION.md`, `CONSTITUTION.md`, and `docs/workflows.md` ownership while adding guide ownership/source-rank guidance without replacing the workflow-map registry contract.
- R16-R24: M1 keeps `docs/project-map.md` as orientation and `docs/plan.md` as bounded index; plan-body placement remains aligned with the workflow-map contract.
- R25-R31: M1 clarifies learn-session non-authority and stage-skill edit boundaries.
- R32-R43: M2 adds cross-guide validation ownership and deterministic checks.
- R44-R49: M2/M3 preserve baseline-drift, migration, lifecycle-order, schema, validation, and generated-output boundaries.
- R50-R52: M3 records behavior-preservation proof, cold-read proof, and final evidence for stale guide-artifact handling.

## Current Handoff Summary

- Current milestone: M3. Proof, packaging, and lifecycle closeout
- Current milestone state: closed
- Last reviewed milestone: M3. Proof, packaging, and lifecycle closeout
- Review status: PR #100 merged after hosted CI success
- Remaining in-scope implementation milestones: none
- Next stage: none
- Final closeout readiness: terminal done
- Reason final closeout is or is not ready: M1, M2, and M3 closed after clean code-review; review-resolution closed; explain-change and verify evidence are current; PR #100 merged after hosted CI success on 2026-06-18. No downstream lifecycle stage remains for this initiative.

## Milestones

### M1. Guide surface alignment

- Milestone state: closed
- Goal: Update human-facing guide surfaces and directly contradictory stage-skill text so each guide answers its assigned question without duplicating another contract.
- Requirements: R1-R31, R44-R49
- Files/components likely touched:
  - `README.md`
  - `docs/workflows.md`
  - `docs/project-map.md`
  - `docs/plan.md`
  - `skills/workflow/SKILL.md`
  - directly contradictory stage skills only, if inspection finds any
- Dependencies:
  - Approved spec.
  - Plan-review approval.
  - Test spec coverage for guide-surface expectations before implementation.
- Tests to add/update:
  - Test-spec cases for README guide index, workflow guide ownership, project-map scope, plan index boundary, learn-session non-authority, and stage-skill direct contradiction checks.
- Implementation steps:
  - Add or tighten README "where to go next" guide index.
  - Add guide ownership/source-rank guidance to `docs/workflows.md` without changing exact artifact-location registry semantics outside the workflow-map contract.
  - Clarify `docs/project-map.md` purpose boundary only if current wording claims workflow policy ownership.
  - Clarify `docs/plan.md` index-only boundary only if current wording is insufficient or stale.
  - Inspect relevant stage skills and edit only direct contradictions with the approved workflow guide, source-rank model, or artifact-location registry.
  - Leave learn sessions as historical artifacts; do not migrate historical records.
- Validation commands:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path README.md --path docs/workflows.md --path docs/project-map.md --path docs/plan.md --path docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path README.md --path docs/workflows.md --path docs/project-map.md --path docs/plan.md --path docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml`
  - `git diff --check -- README.md docs/workflows.md docs/project-map.md docs/plan.md docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment`
- Expected observable result: A contributor can start from README, find the workflow guide for artifact routing, use project-map for repository orientation, use `docs/plan.md` for active work, and understand that learn sessions are historical rationale only.
- Commit message: `M1: align guide surfaces`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - README or `docs/workflows.md` becomes too long by duplicating contracts.
  - Stage skills are edited for style instead of direct contradiction.
- Rollback/recovery:
  - Revert guide-surface wording as a unit and keep the approved spec/plan intact for a narrower follow-up implementation.

### M2. Cross-guide validation

- Milestone state: closed
- Goal: Add deterministic cross-guide validation through a dedicated guide-system validator or artifact-lifecycle guide-system mode while keeping `validate-skills.py` scoped to skill-file checks.
- Requirements: R32-R43, R48-R49, R52
- Files/components likely touched:
  - `scripts/validate-guide-system.py` or an artifact-lifecycle guide-system validation module
  - `scripts/validation_selection.py`
  - relevant `scripts/test-*.py`
  - `tests/fixtures/` if fixture coverage is needed
  - `scripts/validate-skills.py` only if a check directly inspects packaged skill content
- Dependencies:
  - M1 guide-surface shape.
  - Test spec must name exact guide checks and failure fixtures.
- Tests to add/update:
  - README guide index link checks.
  - `docs/workflows.md` guide ownership and artifact-location section checks.
  - Workflow guide ownership vs stage-skill content ownership checks.
  - `docs/project-map.md` workflow-stage-order ownership rejection.
  - `docs/plan.md` bounded-index shape checks.
  - Learn-session live-authority rejection fixture.
  - Directly affected stage-skill placement contradiction checks.
  - Selector routing for guide-system validation.
- Implementation steps:
  - Choose the concrete validator form allowed by the spec.
  - Implement stable parsing against links, headings, fenced YAML, tables, stable text fixtures, or check IDs rather than broad prose scoring.
  - Route selected validation for changed guide surfaces.
  - Keep workflow-map registry/table consistency owned by existing workflow-map validation; call or compose it without making a second registry contract.
  - Ensure failures report stable guide check IDs.
- Validation commands:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/test-skill-validator.py` if skill checks are touched
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path README.md --path docs/workflows.md --path docs/project-map.md --path docs/plan.md --path specs/guide-system-source-of-truth-alignment.md`
  - `bash scripts/ci.sh --mode explicit --path README.md --path docs/workflows.md --path docs/project-map.md --path docs/plan.md --path scripts/validation_selection.py --path specs/guide-system-source-of-truth-alignment.md`
- Expected observable result: Selected validation fails deterministically for broken guide links, missing workflow guide ownership, project-map workflow-policy ownership, plan-index bloat indicators, learn-only routing authority, and affected stage-skill placement contradictions.
- Commit message: `M2: validate guide system drift`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Validator overfits prose or becomes a broad natural-language quality checker.
  - Cross-guide checks accidentally move into `validate-skills.py`.
- Rollback/recovery:
  - Disable the new guide-system validator entry point or selector route, preserve M1 guide text, and record the validation blocker for follow-up.

### M3. Proof, packaging, and lifecycle closeout

- Milestone state: closed
- Goal: Record behavior-preservation proof, cold-read proof, generated adapter proof when changed skill content is packaged, and final lifecycle evidence before verification.
- Requirements: R43-R52
- Files/components likely touched:
  - `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/behavior-preservation.md`
  - `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/guide-cold-read.md` or consolidated registered proof surface if metadata constraints require it
  - `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/explain-change.md`
  - `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml`
  - `docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md`
  - `docs/plan.md`
  - generated adapter proof through repository-owned commands only, if canonical skill changes require it
- Dependencies:
  - M1 and M2 closed after code-review.
  - Review-resolution closed if any material findings appear.
- Tests to add/update:
  - Manual cold-read proof answering the spec's guide-routing questions.
  - Behavior-preservation matrix for README, `VISION.md`, `CONSTITUTION.md`, `docs/workflows.md`, `docs/project-map.md`, `docs/plan.md`, stage skills, and learn sessions.
  - Adapter packaging proof when changed canonical skill content affects packaged skills.
- Implementation steps:
  - Record behavior-preservation proof.
  - Record cold-read proof without relying on chat history.
  - Run generated skill/adapter checks if canonical skill changes require them.
  - Refresh change metadata, plan progress, validation notes, and explain-change.
  - Prepare final handoff to code-review, explain-change, verify, and PR stages.
- Validation commands:
  - `python scripts/build-skills.py --check` if canonical skill files changed
  - `python scripts/test-build-skills.py` if canonical skill files changed
  - `python scripts/test-adapter-distribution.py` if generated adapter proof is required by selected validation
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path README.md --path docs/workflows.md --path docs/project-map.md --path docs/plan.md --path specs/guide-system-source-of-truth-alignment.md --path docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml`
- Expected observable result: The branch has guide-surface changes, deterministic guide validation, behavior-preservation evidence, cold-read proof, and lifecycle metadata ready for code-review and later verify.
- Commit message: `M3: prove guide system alignment`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Cold-read proof repeats intended policy instead of inspecting the actual guide system.
  - Metadata constraints reject standalone proof artifact keys.
- Rollback/recovery:
  - Consolidate proof into an allowed registered change-local surface if metadata rejects standalone proof keys; otherwise revise proof artifacts and rerun validation.

## Validation plan

- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment`: review-recording structure during planning and review.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml`: active metadata integrity.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`: lifecycle status and stale wording checks for touched proposal, spec, plan, review, guide, and metadata artifacts.
- `bash scripts/ci.sh --mode explicit --path ...`: selected repository-owned validation for touched surfaces before each handoff.
- `python scripts/test-artifact-lifecycle-validator.py`: validator regression if artifact-lifecycle guide-system mode is used.
- `python scripts/test-select-validation.py`: selector regression if guide-system validation gets selected-check routing.
- `python scripts/test-skill-validator.py` and `python scripts/validate-skills.py`: skill validation when canonical skill files change.
- `python scripts/build-skills.py --check` and `python scripts/test-build-skills.py`: generated local skill proof when canonical skill files change.
- `python scripts/test-adapter-distribution.py`: adapter packaging proof when changed canonical skill content affects generated adapters.

## Risks and recovery

- Risk: Guide surfaces duplicate contracts and become second sources of truth.
  - Recovery: Move duplicated detail back to the owning spec, workflow map, or stage skill; keep guide text focused on orientation and routing.
- Risk: The guide-system validator overfits prose.
  - Recovery: Narrow checks to stable links, headings, fenced YAML, table fields, fixture text, and check IDs.
- Risk: Plan-location confusion reappears.
  - Recovery: Keep this plan aligned with the approved workflow-map spec: `docs/plans/YYYY-MM-DD-slug.md` is the detailed plan-body path, `docs/plan.md` is the index.
- Risk: Stage-skill portability regresses.
  - Recovery: Revert broad skill edits and preserve portable defaults; edit only direct contradictions.
- Risk: Historical artifacts are accidentally migrated.
  - Recovery: Revert migrations and record baseline drift; create a separate migration proposal if needed.

## Dependencies

- Spec-review R2 approved with no material findings.
- Plan-review must approve this plan before test-spec and implementation reliance.
- Test spec must map each `MUST` requirement to concrete tests or manual proof before implementation.
- Existing workflow-map spec remains the owner of exact artifact-location registry semantics.
- No architecture stage is required unless plan-review identifies a cross-component design gap.

## Progress

- 2026-06-18: Created execution plan after spec-review R2 approved the guide-system source-of-truth alignment spec.
- 2026-06-18: Plan-review R1 approved the plan with no material findings; created the active test spec for implementation proof.
- 2026-06-18: Started M1 implementation for guide surface alignment.
- 2026-06-18: Completed M1 guide surface alignment and moved M1 to review-requested for code-review.
- 2026-06-18: Code-review M1 R1 returned clean-with-notes and closed M1; next stage is implement M2.
- 2026-06-18: Completed M2 cross-guide validator implementation and moved M2 to review-requested for code-review.
- 2026-06-18: Code-review M2 R1 requested changes for `GUIDE-CR1`; M2 is resolution-needed.
- 2026-06-18: Implemented review-resolution for `GUIDE-CR1` and moved M2 back to review-requested for code-review rerun.
- 2026-06-18: Code-review M2 R2 returned clean-with-notes and closed M2; next stage is implement M3.
- 2026-06-18: Started M3 proof, packaging, and lifecycle closeout implementation.
- 2026-06-18: Completed M3 proof artifacts and lifecycle handoff updates; moved M3 to review-requested for code-review.
- 2026-06-18: Code-review M3 R1 returned clean-with-notes and closed the final implementation milestone; next stage is explain-change.
- 2026-06-18: Updated explain-change rationale from the actual branch diff, requirements, tests, review-resolution, and validation evidence; next stage is verify.
- 2026-06-18: Completed final verify, recorded `verify-report.md`, and marked the branch ready for PR handoff. PR body readiness remains for the `pr` stage.
- 2026-06-18: Opened PR #100 for guide system source-of-truth alignment; next stage is hosted CI and human review.
- 2026-06-18: Clarified README new-repository adoption flow after PR feedback showed users could still confuse adapter installation, standing guide bootstrap, and the per-change lifecycle.
- 2026-06-18: Adjusted README bootstrap order to put `vision` before `constitution` and explicitly include `docs/plan.md` as the small live-work index.
- 2026-06-18: PR #100 merged after hosted CI success; terminal lifecycle closeout moved this plan to done and moved the plan index entry from Active to Done (recent).

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-18 | Use three implementation milestones: guide surfaces, validation, proof/closeout. | This separates human-facing guide edits, validator work, and lifecycle proof into reviewable slices. | One broad implementation milestone. |
| 2026-06-18 | No architecture stage before plan. | Spec-review R1/R2 found the change preserves existing architecture boundaries. | Add architecture artifact by default. |
| 2026-06-18 | Keep exact artifact-location registry semantics delegated to the workflow-map spec. | The guide-system spec owns guide alignment, not a second registry contract. | Redefine registry semantics in this plan. |

## Surprises and discoveries

- None yet.

## Validation notes

- Plan-review R1 validation passed before test-spec authoring.
- Pending test-spec validation after this artifact, the test spec, and `docs/plan.md` are updated.
- M1 content audit:
  - `README.md` now includes a compact "Where to go next" guide index.
  - `docs/workflows.md` now includes a guide ownership matrix and learn-session non-authority reminder.
  - `docs/project-map.md` now states that it does not own workflow stage order, exact lifecycle artifact placement, or current milestone state.
  - `docs/plan.md` was already a bounded index and only needed current active-state synchronization.
  - Stage skills were unchanged because inspection found no direct contradiction with the approved workflow guide, source-rank model, or artifact-location registry.
  - Historical artifacts were not migrated.
- M1 validation:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path README.md --path docs/workflows.md --path docs/project-map.md --path docs/plan.md --path docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml` passed.
  - `bash scripts/ci.sh --mode explicit --path README.md --path docs/workflows.md --path docs/project-map.md --path docs/plan.md --path docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml` passed selected checks: `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `readme.validate`, `readme.vision_markers`, `selector.regression`.
  - `git diff --check -- README.md docs/workflows.md docs/project-map.md docs/plan.md docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment` passed.
- M1 review:
  - `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/reviews/code-review-m1-r1.md` recorded clean-with-notes with no material findings.
- M2 content audit:
  - Added `scripts/validate-guide-system.py` as the dedicated cross-guide validator.
  - Added `scripts/test-guide-system-validator.py` fixture coverage for README guide links, workflow guide sections, project-map scope, plan-index boundary, learn-session non-authority, stage-skill plan defaults, and duplicate registry placement.
  - Updated `scripts/validation_selection.py` so guide surfaces select `guide_system.validate`, and guide-validator source changes select `guide_system.regression`.
  - Updated selector regression expectations in `scripts/test-select-validation.py`.
  - Kept `scripts/validate-skills.py` unchanged; cross-guide checks were not added to skill validation.
  - Added small M1-surface clarifications needed for deterministic validation: `docs/workflows.md` now explicitly says the workflow guide routes placement while stage skills own artifact content, and `docs/plan.md` has visible bounded-index wording.
- M2 validation:
  - `python scripts/test-guide-system-validator.py` passed 8 tests.
  - `python scripts/validate-guide-system.py` passed.
  - `python scripts/test-select-validation.py` passed 98 tests.
  - `python scripts/test-artifact-lifecycle-validator.py` passed 76 tests.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path README.md --path docs/workflows.md --path docs/project-map.md --path docs/plan.md --path specs/guide-system-source-of-truth-alignment.md` passed.
  - `bash scripts/ci.sh --mode explicit --path README.md --path docs/workflows.md --path docs/project-map.md --path docs/plan.md --path scripts/validation_selection.py --path scripts/validate-guide-system.py --path scripts/test-guide-system-validator.py --path specs/guide-system-source-of-truth-alignment.md` passed selected checks: `artifact_lifecycle.validate`, `readme.validate`, `readme.vision_markers`, `guide_system.regression`, `guide_system.validate`, `selector.regression`.
  - Final M2 consistency checks passed after lifecycle state synchronization: `python scripts/validate-change-metadata.py docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path README.md --path docs/workflows.md --path docs/project-map.md --path docs/plan.md --path specs/guide-system-source-of-truth-alignment.md --path docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml`; `git diff --check -- README.md docs/workflows.md docs/project-map.md docs/plan.md scripts/validate-guide-system.py scripts/test-guide-system-validator.py scripts/validation_selection.py scripts/test-select-validation.py docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml`; and `bash scripts/ci.sh --mode explicit --path README.md --path docs/workflows.md --path docs/project-map.md --path docs/plan.md --path scripts/validation_selection.py --path scripts/validate-guide-system.py --path scripts/test-guide-system-validator.py --path scripts/test-select-validation.py --path specs/guide-system-source-of-truth-alignment.md --path docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml`.
- M2 review:
  - `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/reviews/code-review-m2-r1.md` recorded `changes-requested` with material finding `GUIDE-CR1`.
  - `GUIDE-CR1` requires review-resolution because the new guide-system validator partially duplicates workflow-map registry checks instead of composing or selecting the existing workflow-map validator that owns registry/table consistency.
  - Review recording validation passed: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment`, `python scripts/validate-change-metadata.py docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/review-log.md --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/review-resolution.md --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/reviews/code-review-m2-r1.md --path docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md --path docs/plan.md`, `git diff --check -- docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md docs/plan.md`, and selected CI for the review-recording surfaces.
- M2 review-resolution:
  - `GUIDE-CR1` was accepted and resolved by composing the existing workflow-map validator from `scripts/validate-guide-system.py` instead of carrying a partial guide-owned registry contract.
  - Added guide-system validator regression coverage proving a registry/table mismatch fails through `workflow map contract failed`, and static coverage preventing a guide-owned required-entry list from returning.
  - Added selector regression coverage documenting that `docs/workflows.md` changes select the composed guide-system validator.
  - `python scripts/test-guide-system-validator.py` passed 10 tests.
  - `python scripts/validate-guide-system.py` passed.
  - `python scripts/test-select-validation.py` passed 99 tests.
  - `python scripts/test-skill-validator.py -k workflow` passed 31 tests.
  - `python scripts/test-skill-validator.py` passed 200 tests.
  - Final `GUIDE-CR1` resolution checks passed: `python scripts/validate-change-metadata.py docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml`; `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path README.md --path docs/workflows.md --path docs/project-map.md --path docs/plan.md --path specs/guide-system-source-of-truth-alignment.md --path docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/review-log.md --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/review-resolution.md --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/reviews/code-review-m2-r1.md`; `git diff --check --`; and selected CI for the implementation and lifecycle surfaces.
- M2 review rerun:
  - `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/reviews/code-review-m2-r2.md` recorded clean-with-notes with no material findings and closed M2.
  - Code-review rerun validation passed: `python scripts/test-guide-system-validator.py`, `python scripts/validate-guide-system.py`, `python scripts/test-select-validation.py`, and `python scripts/test-skill-validator.py -k workflow`.
  - Review-recording validation passed: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment`, `python scripts/validate-change-metadata.py docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/review-log.md --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/review-resolution.md --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/reviews/code-review-m2-r2.md --path docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md --path docs/plan.md`, `git diff --check -- docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md docs/plan.md`, and selected CI for the review-recording surfaces.
- M3 content audit:
  - Added `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/behavior-preservation.md` with the required README, `VISION.md`, `CONSTITUTION.md`, `docs/workflows.md`, `docs/project-map.md`, `docs/plan.md`, stage skills, learn sessions, generated adapters, baseline drift, migration, lifecycle-order, schema, validation, and security/privacy preservation matrix.
  - Added `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/guide-cold-read.md` answering the required guide-routing questions from current guide surfaces only.
  - Added `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/explain-change.md` as durable reasoning for the non-trivial change.
  - Closed `review-resolution.md` after `GUIDE-CR1` was accepted, resolved, and rerun clean.
  - Registered the exact `guide-cold-read.md` change-local evidence path in selected validation after selected CI correctly blocked it as unregistered deterministic evidence.
  - Adapter packaging proof was not triggered because this branch changed no canonical `skills/` files or generated adapter output.
- M3 validation:
  - `python scripts/test-select-validation.py` passed 99 tests after registering `guide-cold-read.md`.
  - `python scripts/validate-guide-system.py` passed.
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment` passed.
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml` passed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/review-resolution.md --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/behavior-preservation.md --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/guide-cold-read.md --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/explain-change.md --path docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md --path docs/plan.md` passed.
  - `git diff --check -- docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md docs/plan.md` passed.
  - `bash scripts/ci.sh --mode explicit --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/review-resolution.md --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/behavior-preservation.md --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/guide-cold-read.md --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/explain-change.md --path docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md --path docs/plan.md --path README.md --path docs/workflows.md --path docs/project-map.md --path specs/guide-system-source-of-truth-alignment.md --path specs/guide-system-source-of-truth-alignment.test.md --path scripts/validation_selection.py --path scripts/test-select-validation.py` passed selected checks: `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `readme.validate`, `readme.vision_markers`, `guide_system.validate`, `selector.regression`.
- M3 review:
  - `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/reviews/code-review-m3-r1.md` recorded clean-with-notes with no material findings and closed M3.
  - Code-review rerun validation passed: `python scripts/test-select-validation.py`, `python scripts/validate-guide-system.py`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment`, `python scripts/validate-change-metadata.py docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml`, and `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`.
  - Review-recording validation passed: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment`, `python scripts/validate-change-metadata.py docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/review-log.md --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/reviews/code-review-m3-r1.md --path docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md --path docs/plan.md`, `git diff --check -- docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md docs/plan.md`, and selected CI for the review-recording surfaces.
- Explain-change:
  - `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/explain-change.md` now links the actual branch diff to the proposal, requirements, plan milestones, tests, review outcomes, `GUIDE-CR1` review-resolution, validation evidence, alternatives rejected, scope control, and remaining risks.
  - Explain-change validation passed: `python scripts/validate-change-metadata.py docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/explain-change.md --path docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md --path docs/plan.md`, `python scripts/validate-guide-system.py`, `git diff --check -- docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/explain-change.md docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md docs/plan.md`, and selected CI for the explain-change surfaces.
- Verify:
  - `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/verify-report.md` records branch-ready evidence and the `pr` handoff.
  - Focused checks passed: `python scripts/test-guide-system-validator.py`, `python scripts/validate-guide-system.py`, `python scripts/test-select-validation.py`, `python scripts/test-skill-validator.py -k workflow`, and `python scripts/test-skill-validator.py`.
  - Lifecycle and review closeout checks passed: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment`, `python scripts/validate-change-metadata.py docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml`, and explicit-path artifact lifecycle validation for the touched guide, spec, plan, change-local, and validator surfaces.
  - Selected CI passed with `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `readme.validate`, `readme.vision_markers`, `guide_system.regression`, `guide_system.validate`, and `selector.regression`.
  - Broad smoke passed: `bash scripts/ci.sh --mode broad-smoke` reported 12 checks passed.
  - `git diff --check --` passed.
- PR handoff:
  - PR #100 opened with a body grounded in the proposal, spec, test spec, plan, explain-change, review-resolution, verify report, actual diff, and validation evidence.
  - Hosted CI was not observed before PR creation; it remains part of the next stage.
- PR feedback clarification:
  - README now states that `init codex` installs agent support and does not replace standing guide artifacts.
  - README now gives the new-repository order: install adapter, bootstrap `VISION.md`, `CONSTITUTION.md`, `docs/project-map.md`, `docs/workflows.md`, and `docs/plan.md`, then run the per-change lifecycle.
  - Validation passed: `python scripts/validate-readme.py README.md`, `python scripts/validate-guide-system.py`, explicit-path lifecycle validation, selected CI for README and lifecycle surfaces, and `git diff --check -- README.md`.
  - Follow-up validation after swapping vision before constitution passed: `python scripts/validate-readme.py README.md`, `python scripts/validate-guide-system.py`, selected CI for README and lifecycle surfaces, and `git diff --check -- README.md`.
- Terminal closeout:
  - PR #100 merged after hosted CI success.
  - `docs/plan.md` moved this initiative from Active to Done (recent).
  - `docs/plan-archive.md` received the oldest Done recent entry to keep the plan index bounded.
  - Validation passed: `python scripts/validate-change-metadata.py docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml --path docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md --path docs/plan.md --path docs/plan-archive.md`, selected CI for terminal closeout surfaces, and `git diff --check --`.

## Outcome and retrospective

- PR #100 merged on 2026-06-18.
- The guide system now has a clearer user-facing repository bootstrap path, source-ranked guide ownership, cross-guide validation, behavior-preservation proof, and cold-read proof.
- `GUIDE-CR1` was resolved by keeping workflow-map registry/table semantics delegated to the workflow-map validator instead of duplicating that contract in guide-system validation.
- No historical artifacts were migrated, no lifecycle stage order changed, no artifact schemas changed, and no generated adapter output was hand-edited.

## Readiness

- See `Current Handoff Summary`.
- Terminal done. No downstream lifecycle stage remains for this initiative.
