# Spec-Review Testability Routing and Output Consolidation Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Owner: maintainers
- Start date: 2026-05-25
- Last updated: 2026-05-25
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

Implement the accepted spec-review routing/readiness consolidation so `spec-review` can no longer validly route directly to `test-spec`, while preserving eventual test-spec readiness as the quality assessment that makes approval meaningful.

The change must separate routing from readiness in canonical skill text, review-result assets, validation fixtures, and generated-output proof. It must preserve review dimensions, review status values, finding severity values, recording behavior, material-finding sufficiency, workflow stage order, and autoprogression boundaries.

## Source artifacts

- Proposal: [Spec-Review Testability Routing and Output Consolidation](../proposals/2026-05-25-spec-review-testability-routing-output-consolidation.md)
- Spec: [Test-Spec Readiness And Skill Workflow Alignment](../../specs/test-spec-readiness-and-skill-workflow-alignment.md)
- Architecture: not-required; this is a skill-output contract, asset, and validation update inside existing authored skill and validator boundaries.
- Test spec: [Test-Spec Readiness And Skill Workflow Alignment test spec](../../specs/test-spec-readiness-and-skill-workflow-alignment.test.md), requires amendment after plan-review before implementation.
- Change metadata: [change.yaml](../changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml)
- Review evidence: [proposal-review-r1](../changes/2026-05-25-spec-review-testability-routing-output-consolidation/reviews/proposal-review-r1.md), [spec-review-r3](../changes/2026-05-25-spec-review-testability-routing-output-consolidation/reviews/spec-review-r3.md)

## Context and orientation

Canonical authored skill source lives under `skills/`. `skills/spec-review/SKILL.md` is the operating contract for the review stage. `skills/spec-review/assets/review-result-skeleton.md` owns the copied result structure, while `skills/spec-review/assets/material-finding.md` owns the detailed material-finding field shape. Generated skill mirrors and adapter archives are derived output and must not be hand-edited.

The approved spec amendment changes the `spec-review` output contract:

- `Immediate next stage` is a routing field with exactly `spec revision`, `review-resolution`, `architecture`, `plan`, and `none`.
- `test-spec` is never a valid `Immediate next stage` value from `spec-review`.
- `Eventual test-spec readiness` is a separate assessment with exactly `ready`, `conditionally-ready`, and `not-ready`.
- `approved` pairs only with `ready` or `conditionally-ready`.
- Routing values are bound to review status so `approved` cannot route back to revision.
- Missing reviewer inputs use `inconclusive`, `Immediate next stage: none`, `Eventual test-spec readiness: not-ready`, and a stop condition.

The matching test spec previously contained older `not-assessed`, empty-route, and `spec` repair-surface expectations. It was amended after plan-review-r2 and now governs implementation.

## Non-goals

- Do not remove eventual `test-spec` readiness.
- Do not allow `test-spec` as an immediate next stage from `spec-review`.
- Do not change review dimensions, review status values, finding severity values, recording status values, or material-finding asset field shape.
- Do not change workflow stage order or broaden autoprogression.
- Do not update `spec`, `test-spec`, `plan`, or `workflow` skill behavior in the first implementation slice unless a failing test or direct drift dependency proves it is required.
- Do not hand-edit generated skill mirrors or public adapter output.
- Do not add broad natural-language validator scoring.
- Do not claim architecture completion, plan-review approval, test-spec completion, implementation completion, verify, branch readiness, or PR readiness from this plan.

## Requirements covered

- R1, R1a, R1b: M2, with M1 deterministic coverage and test-spec amendment proof.
- R1c, R1d: M2 if implementation discovers workflow invariant drift; otherwise plan records no workflow edit needed.
- R2, R2a-R2j: M1 validator/test coverage and M2 canonical skill/result-skeleton wording.
- R3, R3a-R3k: M1 validator/test coverage and M2 canonical skill/result-skeleton wording.
- R4, R4a-R4c: M2 manual contract proof and behavior-preservation evidence.
- R5, R5a-R5b: test-spec amendment and M2 drift check; `plan-review` edited only if a direct conflict is found.
- R6, R6a-R6b: test-spec amendment and M2 drift check; `test-spec` edited only if a direct conflict is found.
- R7, R7a: all implementation milestones enforce the first-pass scope boundary.
- R8, R8a-R8e: M1 adds deterministic checks where feasible; recorded review-artifact field enforcement remains deferred unless parser support already exists.
- AC-SRTR-ROUTE-001 through AC-SRTR-ROUTE-005: test-spec amendment, M1, and M2.
- AC-SRTR-UX-001 through AC-SRTR-UX-004: already satisfied by spec; preserved through plan-review and verify.

## Current Handoff Summary

- Current milestone: M3
- Current milestone state: review-requested
- Last reviewed milestone: M2
- Review status: implementation complete for M3; code-review pending
- Remaining in-scope implementation milestones: M3
- Next stage: code-review M3
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: M3 code-review, explain-change, verify, and PR handoff remain.

## Milestones

### M1. Validator and Fixture Scaffolding

- Milestone state: closed
- Goal: Add controlled fixture and helper/parser scaffolding for the closed `spec-review` routing/readiness contract without enabling canonical `spec-review` skill enforcement yet.
- Requirements: R2, R2a-R2j, R3, R3a-R3k, R8, R8a-R8d, AC-SRTR-ROUTE-001 through AC-SRTR-ROUTE-005
- Files/components likely touched:
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`
  - `tests/fixtures/skills/` if existing fixture layout needs file-backed cases
  - `docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml`
  - this plan and `docs/plan.md`
- Dependencies:
  - Plan-review approval.
  - Matching test-spec amendment approved or active enough to govern implementation tests.
- Tests to add/update:
  - Controlled negative fixture: `Immediate next stage: test-spec` fails.
  - Controlled positive fixture: `Immediate next stage: plan` with `Eventual test-spec readiness: ready` passes.
  - Controlled negative fixture: `Review status: approved` with `Eventual test-spec readiness: not-ready` fails.
  - Controlled positive fixture: missing-input path uses `inconclusive`, `Immediate next stage: none`, `Eventual test-spec readiness: not-ready`, and a stop condition.
  - Controlled status-to-routing contradiction checks for `approved` with `spec revision`, `review-resolution`, or `none`, and non-approved statuses with forward values.
  - Helper/parser scaffolding for structural single-ownership checking of the complete material-finding field-label set if feasible without prose overfitting.
- Implementation steps:
  - Add helper checks against representative filled result fixtures.
  - Prefer field labels and enum values over exact paragraph text.
  - Keep recorded review-artifact result-field validation deferred unless the existing parser can inspect those fields without broad parser redesign.
  - Add controlled positive and negative fixtures before or alongside the helper implementation.
  - Do not enable canonical enforcement against unchanged `skills/spec-review/SKILL.md` or `skills/spec-review/assets/review-result-skeleton.md` in M1.
  - Record fixture-level proof only; any canonical-skill enforcement expected to fail before canonical assets are updated belongs in M2.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `git diff --check -- scripts/skill_validation.py scripts/test-skill-validator.py tests/fixtures/skills`
- Expected observable result: controlled fixture validation catches the historical direct-to-`test-spec` routing failure and approved/not-ready contradiction without requiring unchanged canonical skill assets to satisfy the new contract.
- Implementation evidence:
  - Added controlled `spec-review` result-field validation helper in `scripts/skill_validation.py`.
  - Added controlled fixture tests in `scripts/test-skill-validator.py` for the allowed immediate-stage enum, rejected `test-spec` routing, rejected pseudo-routing values, approved/not-ready, `not-assessed`, status-to-routing contradictions, missing-input stop conditions, and `conditionally-ready` conditions.
  - Kept canonical `spec-review` skill and result-skeleton enforcement out of M1; M2 still owns canonical enforcement after canonical asset updates.
- Commit message: `M1: add spec-review routing readiness validation`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handoff commit prepared
  - code-review completed for M1
- Risks:
  - Validator overfits prose instead of field structure.
  - Existing parser support is too narrow for actual review-record result fields.
  - M1 accidentally enables canonical enforcement before M2 updates canonical assets.
- Rollback/recovery:
  - Narrow checks to the result skeleton and explicit fixtures.
  - Record recorded-artifact parser enforcement as deferred if parser support is insufficient.
  - Move any canonical asset enforcement attempted in M1 into M2.

### M2. Canonical Spec-Review Skill and Asset Contract

- Milestone state: closed
- Goal: Update canonical `spec-review` skill guidance and `review-result-skeleton.md` so routing and readiness are separate closed fields and material-finding field ownership is de-duplicated.
- Requirements: R1, R1a, R1b, R2, R2a-R2j, R3, R3a-R3k, R4, R4a-R4c, R5, R6, R7, R7a, R8d, AC-SRTR-ROUTE-001 through AC-SRTR-ROUTE-005
- Files/components likely touched:
  - `skills/spec-review/SKILL.md`
  - `skills/spec-review/assets/review-result-skeleton.md`
  - `skills/spec-review/assets/material-finding.md` only if parity review finds a structural defect
  - `skills/plan-review/SKILL.md` only if direct drift is found against R5
  - `skills/test-spec/SKILL.md` only if direct drift is found against R6
  - `specs/rigorloop-workflow.md` only if direct invariant drift is found against R1c/R7
  - `docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/behavior-preservation.md`
  - `docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml`
  - this plan and `docs/plan.md`
- Dependencies:
  - M1 validator helpers available.
  - Approved or active matching test-spec amendment.
- Tests to add/update:
  - Update M1 fixtures or expected strings to match final canonical wording.
  - Enable canonical skill and result-skeleton validation for closed routing/readiness enums and status-to-routing bindings.
  - Manual contract check that review dimensions, statuses, severities, recording statuses, and material-finding sufficiency are unchanged.
- Implementation steps:
  - Add a consolidated `Routing and testability assessment` section to `skills/spec-review/SKILL.md`.
  - Replace scattered `test-spec` routing/readiness reminders with the consolidated routing and readiness contracts.
  - Update `assets/review-result-skeleton.md` to expose `Immediate next stage`, `Eventual test-spec readiness`, and `Stop condition` distinctly with the approved enums.
  - Enable canonical enforcement against `skills/spec-review/SKILL.md` and `skills/spec-review/assets/review-result-skeleton.md` after those canonical assets are updated.
  - Preserve `assets/material-finding.md` field shape unless parity review finds a defect.
  - Replace duplicate full material-finding field-list prose in `SKILL.md` with a short reference to `assets/material-finding.md`, while preserving the material-finding sufficiency rule.
  - Check `plan-review` and `test-spec` skill wording for direct conflict; edit only if required by the approved spec or failing validation.
  - Create behavior-preservation evidence mapping baseline behavior to new wording.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py skills/spec-review/SKILL.md`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/test-spec-readiness-and-skill-workflow-alignment.md --path specs/test-spec-readiness-and-skill-workflow-alignment.test.md --path skills/spec-review/SKILL.md --path skills/spec-review/assets/review-result-skeleton.md --path skills/spec-review/assets/material-finding.md --path docs/plans/2026-05-25-spec-review-testability-routing-output-consolidation.md --path docs/plan.md --path docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml`
  - `git diff --check -- skills/spec-review/SKILL.md skills/spec-review/assets/review-result-skeleton.md skills/spec-review/assets/material-finding.md docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation docs/plans/2026-05-25-spec-review-testability-routing-output-consolidation.md docs/plan.md`
- Expected observable result: `spec-review` teaches one routing contract and one readiness contract, and the result skeleton makes the wrong immediate route structurally invalid.
- Implementation evidence:
  - Added canonical `spec-review` routing/readiness validation in `scripts/skill_validation.py`.
  - Added canonical and negative fixture tests in `scripts/test-skill-validator.py`.
  - Updated `skills/spec-review/SKILL.md` with one consolidated routing/readiness section.
  - Updated `skills/spec-review/assets/review-result-skeleton.md` with closed `Immediate next stage`, `Eventual test-spec readiness`, and `Stop condition` fields.
  - Left `skills/spec-review/assets/material-finding.md` unchanged and removed the duplicate full material-finding field list from `SKILL.md`.
  - Updated `skills/test-spec/SKILL.md` to remove stale `not-assessed` readiness wording.
  - Updated `specs/rigorloop-workflow.md` because the durable workflow invariant still contained the old empty-route and `not-assessed` contract.
  - Checked `skills/plan-review/SKILL.md`; no edit was required because it preserves `Immediate next stage: <test-spec | plan revision | blocked>` and treats implementation readiness as downstream.
  - Created behavior-preservation evidence for M2.
- Commit message: `M2: separate spec-review routing and readiness output`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
  - code-review requested for M2
- Risks:
  - Removing scattered wording accidentally weakens the readiness gate.
  - Material-finding de-duplication removes useful sufficiency guidance.
  - Adjacent skill edits widen scope.
- Rollback/recovery:
  - Restore sufficiency wording while keeping the asset as field-shape owner.
  - Keep adjacent skill edits out unless tests prove direct drift.
  - Preserve validator checks for invalid `Immediate next stage: test-spec` if the output contract remains valid.

### M3. Generated Output and Final Proof

- Milestone state: review-requested
- Goal: Prove generated local skills and public adapter archives include the updated `spec-review` skill and assets, then record final behavior-preservation and validation evidence.
- Requirements: R4, R4a-R4c, R7, R7a, R8, R8e, generated-output proof from proposal SRTO-010
- Files/components likely touched:
  - `docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/behavior-preservation.md`
  - `docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml`
  - temporary adapter output under `/tmp`
  - this plan and `docs/plan.md`
- Dependencies:
  - M2 canonical skill and asset updates complete.
  - Current adapter version selected from repository release guidance or manifest.
- Tests to add/update:
  - Generated skill mirror proof through `python scripts/build-skills.py --check`.
  - Temporary adapter archive build and validation.
  - Content check that generated Codex/Claude/opencode archives contain updated `spec-review` skill body and result skeleton.
  - Behavior-preservation matrix covering approval readiness, routing, readiness, material findings, recording, statuses, severities, and generated adapters.
- Implementation steps:
  - Run generated local skill validation from canonical `skills/`.
  - Build temporary adapter archives for the current version.
  - Validate adapter archives.
  - Inspect generated archive content for the updated `spec-review` wording and assets.
  - Record behavior-preservation evidence and update change metadata.
- Validation commands:
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version <version> --output-dir <tmpdir>`
  - `python scripts/validate-adapters.py --root <tmpdir> --version <version>`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/test-spec-readiness-and-skill-workflow-alignment.md --path specs/test-spec-readiness-and-skill-workflow-alignment.test.md --path skills/spec-review/SKILL.md --path skills/spec-review/assets/review-result-skeleton.md --path skills/spec-review/assets/material-finding.md --path docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/behavior-preservation.md --path docs/plans/2026-05-25-spec-review-testability-routing-output-consolidation.md --path docs/plan.md --path docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml`
  - `git diff --check -- docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation docs/plans/2026-05-25-spec-review-testability-routing-output-consolidation.md docs/plan.md`
- Expected observable result: generated output is current from canonical `skills/`, and preservation evidence proves the change clarified routing without weakening review behavior.
- Implementation evidence:
  - Ran generated local skill proof with `python scripts/build-skills.py --check`.
  - Built temporary `v0.1.5` Codex, Claude, and opencode adapter archives under `/tmp/rigorloop-srto-m3-adapters-byvYm0`.
  - Validated the temporary adapter archives with `python scripts/validate-adapters.py --root /tmp/rigorloop-srto-m3-adapters-byvYm0 --version v0.1.5`.
  - Inspected each generated archive's `spec-review/SKILL.md` and `spec-review/assets/review-result-skeleton.md` with Python `zipfile` and confirmed the updated routing/readiness contract is present and the forbidden immediate `test-spec`/`not-assessed` forms are absent.
  - Updated behavior-preservation evidence for generated adapters.
- Commit message: `M3: prove spec-review routing output packaging`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
  - code-review requested for M3
- Risks:
  - Adapter version selection is unclear.
  - Local adapter validation requires unavailable tools.
  - Generated archive content checks become ad hoc.
- Rollback/recovery:
  - Use `dist/adapters/manifest.yaml` or release guidance for the version.
  - If adapter tooling is unavailable, record blocker and smallest next action instead of claiming generated-output proof.
  - Keep content checks bounded to `spec-review` skill body and mapped assets.

## Validation plan

- `python scripts/test-skill-validator.py`: validates helper and fixture coverage for routing/readiness separation.
- `python scripts/validate-skills.py skills/spec-review/SKILL.md`: validates the changed canonical skill directly.
- `python scripts/validate-skills.py`: validates all canonical skill files after wiring checks.
- `python scripts/build-skills.py --check`: proves generated local skill mirrors are current from canonical sources.
- `python scripts/build-adapters.py --version <version> --output-dir <tmpdir>`: builds temporary public adapter archives.
- `python scripts/validate-adapters.py --root <tmpdir> --version <version>`: validates temporary adapter output.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation`: validates formal review evidence.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation`: validates closed review findings after resolution.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml`: validates change metadata.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path <touched lifecycle artifact> [...]`: validates touched lifecycle artifacts.
- `git diff --check -- <touched files>`: catches whitespace errors.

## Milestone validation boundaries

| Milestone | Validation boundary | May request code-review? |
| --- | --- | --- |
| M1 | Controlled fixtures and helper/parser scaffolding pass; canonical enforcement is not enabled against unchanged canonical skill assets. | yes |
| M2 | Canonical `spec-review` skill and result skeleton are updated; canonical enforcement is enabled; full skill validation passes. | yes |
| M3 | Generated skill and adapter output proof passes, or unavailable local tooling is recorded as a blocker with the smallest next action. | yes |

## Risks and recovery

- Risk: The plan implements skill wording before the stale test spec is amended.
  - Recovery: Stop after plan-review and run `test-spec` before implementation.
- Risk: A milestone requests code-review while named validation is expected to fail.
  - Recovery: Keep M1 fixture-scoped and enable canonical enforcement only in M2, or combine M1 and M2 into one passable implementation milestone.
- Risk: Validation checks overfit exact prose and block harmless wording improvements.
  - Recovery: Restrict checks to field labels, enum values, skeleton structure, and controlled fixtures.
- Risk: The readiness assessment is weakened while removing scattered wording.
  - Recovery: Preserve the approval-to-readiness requirements and add negative tests for approved/not-ready.
- Risk: The material-finding field shape drifts while de-duplicating prose.
  - Recovery: Keep `assets/material-finding.md` unchanged unless a parity defect is found; validate structural single ownership where feasible.
- Risk: Generated output drifts from canonical `skills/`.
  - Recovery: Use repository-owned build and adapter validation commands with temporary output.
- Risk: Adjacent workflow or review-family skills appear similar and invite broad refactoring.
  - Recovery: Keep adjacent review-family changes as separate proposals unless a direct failing check proves this slice depends on them.

## Dependencies

- Plan-review must approve this sequencing before test-spec amendment or implementation relies on it.
- Matching test-spec amendment updated stale `not-assessed`, empty-route, and `spec` repair-surface expectations before implementation.
- No separate architecture artifact is expected because the change stays within existing skill, asset, validation, and generated-output boundaries.
- Generated adapter proof depends on repository-owned adapter build and validation scripts.
- Existing review-recording, skill-contract, and review-family asset specs continue to govern recording and asset boundaries.

## Progress

- 2026-05-25: Plan created from accepted proposal, approved spec amendment, clean `spec-review-r3`, and existing change-local review evidence.
- 2026-05-25: Plan-review-r1 found `SRTR-PR1`; plan revision narrowed M1 to controlled fixture/parser scaffolding and moved canonical enforcement to M2.
- 2026-05-25: Plan-review-r2 approved the revised plan with no material findings; next stage is matching test-spec amendment.
- 2026-05-25: Matching test spec was amended for the closed routing/readiness contract; next stage is implement M1.
- 2026-05-25: Maintainer approved the active test spec; implementation M1 remains next.
- 2026-05-25: M1 implementation added controlled result-field fixture validation and is ready for code-review.
- 2026-05-25: Code-review-m1-r1 closed M1 with no material findings; next stage is implement M2.
- 2026-05-25: M2 implementation separated canonical `spec-review` routing/readiness output, enabled canonical validation, updated direct `test-spec` and workflow-spec drift, and is ready for code-review.
- 2026-05-25: Code-review-m2-r1 found `SRTR-CR1`; M2 remains open pending review-resolution for stale workflow-spec immediate-stage wording.
- 2026-05-25: `SRTR-CR1` was resolved by aligning `specs/rigorloop-workflow.md` around explicit `Immediate next stage: none` and adding adjacent-drift regression coverage; M2 is ready for rerun code-review.
- 2026-05-25: Code-review-m2-r2 closed M2 with no material findings; next stage is implement M3.
- 2026-05-26: M3 generated local skill and temporary adapter archive proof completed; M3 is ready for code-review.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-25 | Amend the existing test-spec readiness workflow spec rather than creating a new feature spec. | The existing spec already owns immediate-stage versus eventual-readiness behavior; a parallel spec would split the contract. | Create a separate spec for the routing/readiness consolidation. |
| 2026-05-25 | Require test-spec amendment after plan-review before implementation. | The matching test spec reflected the older `not-assessed` and empty-route contract. | Implement from the approved spec while leaving test-spec stale. |
| 2026-05-25 | Use three implementation milestones. | Validator coverage, canonical skill/assets wording, and generated-output proof are reviewable slices with different risks and validation commands. | One large implementation milestone; separate milestones for every small wording edit. |
| 2026-05-25 | Treat architecture as not required. | The change does not alter runtime architecture, persistence, APIs, deployment, security boundaries, or hard-to-reverse technical design. | Create an architecture artifact for a localized skill/output-contract change. |
| 2026-05-25 | Keep M1 separate but fixture-scoped after plan-review-r1. | This preserves TDD-oriented fixture/parser work while giving M1 a passable validation boundary before code-review. | Combine M1 and M2; make M1 a red-test milestone with no code-review closeout. |
| 2026-05-25 | Keep canonical spec-review enforcement disabled in M1. | M1 is scoped to controlled fixture/parser scaffolding; M2 updates canonical `spec-review` assets and enables canonical enforcement. | Enable canonical checks before updating canonical assets. |
| 2026-05-25 | Update `specs/rigorloop-workflow.md` in M2. | The durable workflow invariant still contained the old `not-assessed`, `spec`, and empty immediate-stage wording, so R1c/R7 required direct alignment. | Leave stale workflow invariant for a later milestone. |

## Surprises and discoveries

- The existing matching test spec is stale relative to the approved 2026-05-25 amendment and must be updated before implementation.
- M1 cannot enable canonical skill enforcement before M2 updates the canonical skill and result skeleton without creating an intentionally failing implementation milestone.
- Controlled fixture validation can cover the historical routing/readiness failures without inspecting unchanged canonical skill assets.
- M2 found direct adjacent drift in `skills/test-spec/SKILL.md` and `specs/rigorloop-workflow.md`; `skills/plan-review/SKILL.md` already preserves the immediate `test-spec` handoff and downstream implementation-readiness distinction.

## Validation notes

- 2026-05-25: Planning read the accepted proposal, approved amended spec, clean proposal/spec review evidence, current plan index, and existing related test spec.
- 2026-05-25: Plan revision resolved `SRTR-PR1` by making M1 fixture/parser scaffolding only and moving canonical enforcement to M2.
- 2026-05-25: Active test spec approval recorded in change metadata.
- 2026-05-25: M1 targeted validation passed: `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, and `git diff --check -- scripts/skill_validation.py scripts/test-skill-validator.py`.
- 2026-05-25: M1 lifecycle validation passed: `python scripts/validate-change-metadata.py docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation`, and focused `git diff --check -- ...`.
- 2026-05-25: Code-review-m1-r1 reran `python scripts/test-skill-validator.py -k spec_review_result_fixture`, `python scripts/validate-change-metadata.py docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation`, and `git diff --check --`; all passed.
- 2026-05-25: M2 targeted validation passed: `python scripts/test-skill-validator.py -k spec_review`, `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py skills/spec-review/SKILL.md`, `python scripts/validate-skills.py skills/test-spec/SKILL.md`, `python scripts/validate-skills.py`, and `python scripts/build-skills.py --check`.
- 2026-05-25: M2 lifecycle validation passed: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation`, `python scripts/validate-change-metadata.py docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`, and focused `git diff --check -- ...`. The lifecycle validator reported pre-existing lifecycle-language warnings in `specs/rigorloop-workflow.md`; no M2 blocker was reported.
- 2026-05-25: Code-review-m2-r1 targeted stale-wording search found `SRTR-CR1` in `specs/rigorloop-workflow.md`; review-resolution and re-review are required before M2 can close.
- 2026-05-25: Code-review-m2-r1 recording validation passed: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation`, `python scripts/validate-change-metadata.py docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml`, and `git diff --check -- docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation docs/plans/2026-05-25-spec-review-testability-routing-output-consolidation.md docs/plan.md`.
- 2026-05-25: `SRTR-CR1` fix validation passed: `python scripts/test-skill-validator.py -k spec_review_routing_adjacent`, `python scripts/test-skill-validator.py -k spec_review`, `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py skills/spec-review/SKILL.md`, `python scripts/validate-skills.py skills/test-spec/SKILL.md`, `python scripts/validate-skills.py`, and `python scripts/build-skills.py --check`.
- 2026-05-25: `SRTR-CR1` lifecycle validation passed: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation`, `python scripts/validate-change-metadata.py docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`, and `git diff --check --`. The lifecycle validator reported existing lifecycle-language warnings in `specs/rigorloop-workflow.md`.
- 2026-05-25: Code-review-m2-r2 reran `python scripts/test-skill-validator.py -k spec_review`, `python scripts/validate-skills.py`, `python scripts/build-skills.py --check`, `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation`, `python scripts/validate-change-metadata.py docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`, and `git diff --check --`; all passed. The lifecycle validator reported existing lifecycle-language warnings in `specs/rigorloop-workflow.md`.
- 2026-05-25: Code-review-m2-r2 recording validation passed: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation`, `python scripts/validate-change-metadata.py docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml`, and `git diff --check -- docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation docs/plans/2026-05-25-spec-review-testability-routing-output-consolidation.md docs/plan.md`.
- 2026-05-26: M3 generated-output proof passed: `python scripts/build-skills.py --check`, `python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-srto-m3-adapters-byvYm0`, `python scripts/validate-adapters.py --root /tmp/rigorloop-srto-m3-adapters-byvYm0 --version v0.1.5`, and Python `zipfile` content inspection of Codex, Claude, and opencode archives.
- 2026-05-26: M3 validation passed: `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation`, `python scripts/validate-change-metadata.py docs/changes/2026-05-25-spec-review-testability-routing-output-consolidation/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`, and `git diff --check -- ...`.

## Outcome and retrospective

- Pending code-review for M3, explain-change, verify, and PR handoff.

## Readiness

- See `Current Handoff Summary`.
- Ready for `code-review M3`. Readiness is not Done; M3 review, explain-change, verify, and PR gates remain.
