# RigorLoop Published Skill Design Contract Execution Plan

- Status: active
- Owner: maintainers
- Start date: 2026-05-19
- Last updated: 2026-05-19
- Related proposal: [RigorLoop Published Skill Design Contract](../proposals/2026-05-19-rigorloop-published-skill-design-contract.md)
- Related spec: [Skill Contract](../../specs/skill-contract.md)
- Change root: [docs/changes/2026-05-19-rigorloop-published-skill-design-contract](../changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml)
- Supersedes: none

## Purpose / big picture

Implement the approved published-skill design contract as an audit-first, pilot-scoped change. The work must make the `proposal` and `proposal-review` skills demonstrate the new contract without rewriting every skill or changing lifecycle stage ownership.

## Source artifacts

- Proposal: [RigorLoop Published Skill Design Contract](../proposals/2026-05-19-rigorloop-published-skill-design-contract.md), accepted.
- Proposal review: [proposal-review-r2](../changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/proposal-review-r2.md), approved.
- Spec: [Skill Contract](../../specs/skill-contract.md), approved after [spec-review-r3](../changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/spec-review-r3.md).
- Architecture: not required. This change affects Markdown skill contracts, canonical skill bodies, validation scripts, fixtures, and generated adapter validation; it does not add runtime components, persistence, APIs, deployment, or hard-to-reverse data flow.
- Existing test spec: [Skill Contract Test Spec](../../specs/skill-contract.test.md), active for the historical skill-contract baseline and to be amended during `test-spec` for R27-R36.
- Project map: [RigorLoop Project Map](../project-map.md), read for repository orientation.

## Context and orientation

- `skills/` is the only authored skill source. Edit `skills/proposal/SKILL.md` and `skills/proposal-review/SKILL.md` only for the pilot.
- Generated public adapter skill bodies are release archives for `v0.1.3` and later. Do not hand-edit generated adapter package output.
- `scripts/skill_validation.py`, `scripts/validate-skills.py`, and `scripts/test-skill-validator.py` own static skill validation and regression fixtures.
- `scripts/build-skills.py --check`, `scripts/build-adapters.py --check`, and `scripts/validate-adapters.py` prove generated-output and adapter-package consistency.
- `scripts/measure-skill-tokens.py` provides deterministic static token estimates for canonical skills.
- Change-local audit, routing coverage, behavior-preservation, and behavior-parity evidence should live under the change root and link back to canonical artifacts rather than becoming a second source of truth.

## Non-goals

- Do not rewrite all skills in this change.
- Do not merge, retire, rename, remove, or change ownership of any skill.
- Do not add a required `when_to_use` frontmatter field.
- Do not introduce broad semantic scoring of skill prose or CI claims about deterministic model auto-selection.
- Do not add a build-time partial/include system.
- Do not change adapter install roots, lockfile semantics, release archive trust boundaries, or CLI behavior.
- Do not require resource-map sections for skills without packaged resources.

## Requirements covered

| Requirement | Planned coverage |
| --- | --- |
| R27-R28 | Audit current skills against the existence gate and portable operating-documentation standard. |
| R29 | Add validator/test coverage for `description` as routing source, including `<= 1024` character cap and no required `when_to_use`. |
| R30-R31 | Update pilot skills so lifecycle role and body execution guidance are explicit without making body routing sections the primary routing source. |
| R32-R33 | Validate resource-map behavior and repository-root versus packaged-resource self-containment boundaries. |
| R34 | Ensure artifact-producing pilot skills include compact fenced output skeletons or reviewed equivalent templates. |
| R35 | Add deterministic routing coverage table evidence and bounded fixture/transcript-review expectations. |
| R36 | Keep the implementation audit-first and pilot-scoped, record merge/retire candidates only as follow-ons, record token-cost deltas, and produce behavior-preservation and behavior-parity evidence. |

## Current Handoff Summary

- Current milestone: M3. Pilot skill rewrite and generated-output validation
- Current milestone state: planned
- Last reviewed milestone: M2. Validator and fixture support
- Review status: M2 code-review rerun clean-with-notes; M3 ready for implement
- Remaining in-scope implementation milestones: M3
- Next stage: implement M3
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: M3 is not implemented or reviewed, explain-change is absent, final verification has not run, and PR handoff is not prepared.

## Milestones

### M1. Audit and evidence scaffold

- Milestone state: closed
- Goal: create the change-local evidence structure for the published-skill design pilot before changing validators or skill bodies.
- Requirements: R27, R28, R35e-R35g, R36a, R36d, R36e, R36g-R36j.
- Files/components likely touched:
  - `docs/changes/2026-05-19-rigorloop-published-skill-design-contract/skill-audit.md`
  - `docs/changes/2026-05-19-rigorloop-published-skill-design-contract/routing-coverage.md`
  - `docs/changes/2026-05-19-rigorloop-published-skill-design-contract/behavior-preservation.md`
  - `docs/changes/2026-05-19-rigorloop-published-skill-design-contract/behavior-parity.md`
  - `docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml`
- Dependencies: approved spec and this reviewed plan.
- Tests to add/update: none yet; this milestone creates evidence inputs consumed by M2/M3 and `test-spec`.
- Implementation steps:
  - Audit current skills for the R36a finding classes.
  - Record merge/retire candidates only as follow-ons with the required R36e fields.
  - Create routing coverage tables for `proposal` and `proposal-review`.
  - Create behavior-preservation note templates for both pilot skills.
  - Define representative proposal and proposal-review artifacts for parity evidence.
- Validation commands:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml`
  - `git diff --check -- docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md docs/changes/2026-05-19-rigorloop-published-skill-design-contract`
- Expected observable result: reviewers can inspect the audit, routing coverage tables, preservation notes, and parity fixture scope before implementation changes behavior.
- Commit message: `M1: scaffold published skill design pilot evidence`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] hand off to code-review for M1 if this milestone is reviewed separately
- Risks: audit scope could expand into unauthorized skill retirement or broad rewrite.
- Rollback/recovery: remove or revise change-local evidence files; do not touch canonical skills in this milestone.

### M2. Validator and fixture support

- Milestone state: closed
- Goal: make the deterministic parts of R27-R36 checkable without adding broad semantic scoring.
- Requirements: R29, R32, R33, R35, R36f.
- Files/components likely touched:
  - `scripts/skill_validation.py`
  - `scripts/validate-skills.py`
  - `scripts/test-skill-validator.py`
  - `tests/fixtures/skills/`
  - `specs/skill-contract.test.md`
  - `docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml`
- Dependencies: M1 routing coverage and evidence format decisions; `test-spec` must define exact test expectations before implementation.
- Tests to add/update:
  - Description length cap and routing-source checks.
  - Optional `when_to_use` does not replace `description`.
  - Resource-map coverage for packaged resources.
  - Repository-root internal path checks distinguish skill-local packaged resources.
  - Routing coverage table presence and bounded phrase coverage without semantic scoring.
- Implementation steps:
  - Extend static skill validation for deterministic R29/R32/R33 checks.
  - Add fixtures for valid and invalid published-skill design pilot cases.
  - Add or update regression tests in `scripts/test-skill-validator.py`.
  - Keep validator checks narrow and positive-first.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml`
  - `git diff --check -- scripts tests specs docs/changes/2026-05-19-rigorloop-published-skill-design-contract`
- Expected observable result: static validation catches deterministic contract violations and does not claim runtime model routing proof.
- Commit message: `M2: validate published skill design contract checks`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] hand off to code-review for M2
- Risks: phrase checks could become brittle or accidentally semantic.
- Rollback/recovery: revert validator and fixture changes for M2 while preserving M1 evidence.

### M3. Pilot skill rewrite and generated-output validation

- Milestone state: planned
- Goal: update only `proposal` and `proposal-review` to comply with the published-skill design contract and prove no behavior-significant rule was weakened.
- Requirements: R27-R36.
- Files/components likely touched:
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `specs/skill-contract.test.md`
  - change-local routing, preservation, parity, token-cost, and validation evidence under `docs/changes/2026-05-19-rigorloop-published-skill-design-contract/`
  - adapter support metadata only if validation proves it is stale
- Dependencies: M1 evidence scaffold; M2 validator/test support; approved amended test spec.
- Tests to add/update:
  - Behavior-parity proof for representative proposal and proposal-review artifacts.
  - Static token-cost comparison for `proposal` and `proposal-review`.
  - Generated local skill and adapter checks from canonical `skills/`.
- Implementation steps:
  - Update pilot skill descriptions, workflow role, execution guidance, output skeletons, and resource-map wording only where required.
  - Fill behavior-preservation notes for removed or rewritten behavior-significant wording.
  - Record behavior-parity evidence for material review status, finding format, recording obligations, stop conditions, validation obligations, and claim boundaries.
  - Record token-cost delta against the pre-change baseline and apply the zero target, `+5%` rationale tolerance, and `+10%` hard cap.
  - Run generated-output and adapter validation without hand-editing generated public adapter bodies.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/measure-skill-tokens.py --skills-root skills`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --check`
  - `python scripts/validate-adapters.py --version 0.1.4`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-19-rigorloop-published-skill-design-contract`
  - `git diff --check -- skills scripts tests specs docs/changes/2026-05-19-rigorloop-published-skill-design-contract`
- Expected observable result: the pilot skills demonstrate the new contract, static validation passes, adapter checks remain derived from canonical skills, and preservation/parity/token evidence is inspectable.
- Commit message: `M3: pilot published skill design contract`
- Milestone closeout:
  - [ ] targeted validation passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] hand off to code-review for M3
- Risks: skill rewrite may bloat common-path text or weaken lifecycle recording boundaries.
- Rollback/recovery: revert pilot skill edits and any validator expectations tied only to those edits; keep the spec and plan unless the contract itself is revised.

## Validation plan

- Before implementation: run plan-stage artifact validation and `git diff --check` for touched lifecycle files.
- Before M2 implementation: update `specs/skill-contract.test.md` through `test-spec` so every new `MUST` has concrete proof coverage.
- During each milestone: run the milestone's targeted commands before handoff to `code-review`.
- Before final closeout: run selected repository validation for changed paths, skill validation, generated-output checks, adapter validation, review-artifact closeout validation, change metadata validation, artifact lifecycle validation, and whitespace checks.
- Hosted CI must not be claimed unless it is actually observed.

## Risks and recovery

- Scope creep into all-skill rewrite: block and revise the plan; R36 limits pilot skill body edits to `proposal` and `proposal-review`.
- Merge/retire side effects: record candidates as follow-ons only; actual ownership changes require a separate proposal or explicit spec amendment.
- Runtime routing overclaim: keep routing tests as fixtures and transcript-review inputs unless a later approved harness defines a deterministic oracle.
- Token-cost regression: move rare detail into references or reduce duplication; above `+10%` blocks the pilot unless the spec changes.
- Adapter drift: regenerate or validate from canonical `skills/`; do not hand-edit generated public adapter skill bodies.

## Dependencies

- `plan-review` must approve or request changes before `test-spec`.
- `test-spec` must amend `specs/skill-contract.test.md` before behavior-changing implementation.
- M2 depends on M1 evidence shape decisions.
- M3 depends on M2 validator/test support and the amended test spec.
- `code-review` is required after each implemented milestone or after a deliberately grouped implementation slice.
- `explain-change`, `verify`, and `pr` remain downstream gates after implementation and review closeout.

## Progress

- 2026-05-19: plan created after clean `spec-review-r3`; spec status settled to `approved`.
- 2026-05-19: clean `plan-review-r1` approved the plan; `specs/skill-contract.test.md` amended for R27 through R36.
- 2026-05-19: owner approved `specs/skill-contract.test.md`; next stage remains `implement M1`.
- 2026-05-19: M1 implementation started; evidence scaffold in progress.
- 2026-05-19: M1 evidence scaffold created and targeted validation passed; M1 moved to `review-requested`.
- 2026-05-19: code-review-m1-r1 returned `clean-with-notes`; M1 closed; next stage is `implement M2`.
- 2026-05-19: M2 implementation started; validator fixtures and narrow published-skill design checks in progress.
- 2026-05-19: M2 validator and fixture support completed; targeted validation passed; M2 moved to `review-requested`.
- 2026-05-19: code-review-m2-r1 returned `changes-requested` with RLSDC-M2-CR1; M2 moved to `resolution-needed`.
- 2026-05-19: RLSDC-M2-CR1 fix implemented and validated; M2 returned to `review-requested` for code-review rerun.
- 2026-05-19: code-review-m2-r2 returned `clean-with-notes`; M2 closed; next stage is `implement M3`.

## Decision log

- 2026-05-19: use a three-milestone plan: audit/evidence scaffold, validator/fixture support, and pilot skill rewrite with generated-output validation. This keeps evidence decisions visible before validator and skill-body changes.
- 2026-05-19: keep architecture out of scope because the approved change affects Markdown contracts, validation scripts, fixtures, and canonical skills without introducing new runtime architecture.
- 2026-05-19: keep M1 evidence files as change-local Markdown linked from `change.yaml` changed files rather than `artifacts` keys. Rationale: the change metadata schema accepts only known artifact keys, while M1 evidence files are supporting proof surfaces.
- 2026-05-19: implement M2 deterministic checks in `scripts/skill_validation.py` and fixture tests rather than broad natural-language scoring. Rationale: R35 allows table presence and bounded phrase coverage, while runtime model routing and broad semantic quality remain out of scope.
- 2026-05-19: keep repository-root dependency validation tied to the opted-in published pilot/readability contract for now. Rationale: canonical non-pilot skills remain valid until their approved slice, while M3 will rewrite the pilot pair under the stricter published-skill contract.

## Surprises and discoveries

- 2026-05-19: `bash scripts/ci.sh --mode explicit` blocks arbitrary change-local support Markdown such as `skill-audit.md`, `routing-coverage.md`, `behavior-preservation.md`, and `behavior-parity.md` with `manual-routing-required`. M1 therefore uses direct change metadata, artifact lifecycle, and whitespace validation for those evidence files, plus selected CI on the supported plan and change metadata paths.
- 2026-05-19: M2 fixture tests failed before implementation for the new description-length, `when_to_use`, resource-map, packaged-script, and repository-root dependency cases, then passed after validator changes.
- 2026-05-19: RLSDC-M2-CR1 showed that the original repository-root dependency check did not treat ordinary imperative command verbs as required context. The fix adds command-context detection while exempting actual packaged skill-local resources found under the skill directory.

## Validation notes

- 2026-05-19: `python scripts/validate-change-metadata.py docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml` passed.
- 2026-05-19: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-19-rigorloop-published-skill-design-contract` passed.
- 2026-05-19: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-19-rigorloop-published-skill-design-contract.md --path specs/skill-contract.md --path docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md --path docs/plan.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-log.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-resolution.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/spec-review-r3.md` passed.
- 2026-05-19: `git diff --check -- docs/proposals/2026-05-19-rigorloop-published-skill-design-contract.md specs/skill-contract.md docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md docs/plan.md docs/changes/2026-05-19-rigorloop-published-skill-design-contract` passed.
- 2026-05-19: `test-spec` amended `specs/skill-contract.test.md` for R27 through R36 and aligned `scripts/test-skill-validator.py` expectations with the approved `baseline normalization first slice` wording.
- 2026-05-19: `python scripts/test-skill-validator.py` passed.
- 2026-05-19: `python scripts/validate-change-metadata.py docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml` passed after test-spec.
- 2026-05-19: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-19-rigorloop-published-skill-design-contract` passed after test-spec.
- 2026-05-19: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-19-rigorloop-published-skill-design-contract.md --path specs/skill-contract.md --path specs/skill-contract.test.md --path docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md --path docs/plan.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-log.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-resolution.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/plan-review-r1.md` passed.
- 2026-05-19: `git diff --check -- specs/skill-contract.test.md scripts/test-skill-validator.py docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md docs/plan.md docs/changes/2026-05-19-rigorloop-published-skill-design-contract` passed.
- 2026-05-19: `bash scripts/ci.sh --mode explicit --path specs/skill-contract.test.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md --path docs/plan.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-log.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-resolution.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/plan-review-r1.md` passed selected skill regression, skill generation regression, review-artifact, artifact-lifecycle, change-metadata regression, and change-metadata checks.
- 2026-05-19 M1 validation: `python scripts/validate-change-metadata.py docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml` passed.
- 2026-05-19 M1 validation: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml` passed.
- 2026-05-19 M1 validation: `git diff --check -- docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md docs/changes/2026-05-19-rigorloop-published-skill-design-contract` passed.
- 2026-05-19 M1 validation: `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml` passed selected artifact-lifecycle, change-metadata regression, and change-metadata checks.
- 2026-05-19 M1 code-review recording validation: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-19-rigorloop-published-skill-design-contract` passed.
- 2026-05-19 M1 code-review recording validation: `python scripts/validate-change-metadata.py docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml` passed.
- 2026-05-19 M1 code-review recording validation: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md --path docs/plan.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-log.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-resolution.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/code-review-m1-r1.md` passed.
- 2026-05-19 M1 code-review recording validation: `git diff --check -- docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md docs/plan.md docs/changes/2026-05-19-rigorloop-published-skill-design-contract` passed.
- 2026-05-19 M1 code-review recording validation: `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md --path docs/plan.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-log.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-resolution.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/code-review-m1-r1.md` passed selected review-artifact, artifact-lifecycle, change-metadata regression, and change-metadata checks.
- 2026-05-19 M2 test-first validation: targeted new published-design fixture tests failed before implementation for expected reasons.
- 2026-05-19 M2 validation: targeted new published-design fixture tests passed.
- 2026-05-19 M2 validation: `python scripts/validate-skills.py` passed.
- 2026-05-19 M2 validation: `python scripts/test-skill-validator.py` passed.
- 2026-05-19 M2 validation: `python scripts/validate-change-metadata.py docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml` passed.
- 2026-05-19 M2 validation: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md --path docs/plan.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml` passed.
- 2026-05-19 M2 validation: `git diff --check -- scripts tests specs docs/changes/2026-05-19-rigorloop-published-skill-design-contract docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md docs/plan.md` passed.
- 2026-05-19 M2 validation: `bash scripts/ci.sh --mode explicit --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path tests/fixtures/skills/published-design/description-too-long/SKILL.md --path tests/fixtures/skills/published-design/when-to-use-replaces-description/SKILL.md --path tests/fixtures/skills/published-design/missing-resource-map/SKILL.md --path tests/fixtures/skills/published-design/missing-resource-map/references/detail.md --path tests/fixtures/skills/published-design/resource-map-missing-resource/SKILL.md --path tests/fixtures/skills/published-design/resource-map-missing-resource/references/detail.md --path tests/fixtures/skills/published-design/packaged-script-valid/SKILL.md --path tests/fixtures/skills/published-design/packaged-script-valid/scripts/check.py --path tests/fixtures/skills/published-design/packaged-script-missing-failure/SKILL.md --path tests/fixtures/skills/published-design/packaged-script-missing-failure/scripts/check.py --path tests/fixtures/skills/published-design/required-root-script/SKILL.md --path docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md --path docs/plan.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml` passed selected skills regression, skill generation regression, artifact-lifecycle, change-metadata regression, and change-metadata checks.
- 2026-05-19 M2 code-review: `code-review-m2-r1` recorded RLSDC-M2-CR1 and requires review-resolution before M2 fixes and rerun review.
- 2026-05-19 M2 code-review recording validation: `python scripts/validate-review-artifacts.py docs/changes/2026-05-19-rigorloop-published-skill-design-contract` passed.
- 2026-05-19 M2 code-review recording validation: `python scripts/validate-change-metadata.py docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml` passed.
- 2026-05-19 M2 code-review recording validation: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md --path docs/plan.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-log.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-resolution.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/code-review-m2-r1.md` passed.
- 2026-05-19 M2 code-review recording validation: `git diff --check -- docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md docs/plan.md docs/changes/2026-05-19-rigorloop-published-skill-design-contract` passed.
- 2026-05-19 M2 code-review recording validation: `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md --path docs/plan.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-log.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-resolution.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/code-review-m2-r1.md` passed selected review-artifact, artifact-lifecycle, change-metadata regression, and change-metadata checks.
- 2026-05-19 RLSDC-M2-CR1 validation: `python scripts/validate-skills.py tests/fixtures/skills/published-design/required-root-script-command` failed as expected with `required repository-root dependency by command wording: scripts/validate-internal.py`.
- 2026-05-19 RLSDC-M2-CR1 validation: `python scripts/validate-skills.py tests/fixtures/skills/published-design/packaged-script-resource-map` passed.
- 2026-05-19 RLSDC-M2-CR1 validation: targeted published-design fixture tests passed.
- 2026-05-19 RLSDC-M2-CR1 validation: `python scripts/test-skill-validator.py` passed.
- 2026-05-19 RLSDC-M2-CR1 validation: `python scripts/validate-skills.py` passed.
- 2026-05-19 RLSDC-M2-CR1 validation: `git diff --check --` passed.
- 2026-05-19 RLSDC-M2-CR1 validation: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-19-rigorloop-published-skill-design-contract` passed.
- 2026-05-19 RLSDC-M2-CR1 validation: `python scripts/validate-change-metadata.py docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml` passed.
- 2026-05-19 RLSDC-M2-CR1 validation: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md --path docs/plan.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-log.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-resolution.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/code-review-m2-r1.md` passed.
- 2026-05-19 RLSDC-M2-CR1 validation: `bash scripts/ci.sh --mode explicit --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path tests/fixtures/skills/published-design/required-root-script-command/SKILL.md --path tests/fixtures/skills/published-design/packaged-script-resource-map/SKILL.md --path tests/fixtures/skills/published-design/packaged-script-resource-map/scripts/validate_output.py --path docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md --path docs/plan.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-log.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-resolution.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/code-review-m2-r1.md` passed selected skills regression, skill generation regression, review-artifact, artifact-lifecycle, change-metadata regression, and change-metadata checks.
- 2026-05-19 M2 rerun code-review: `code-review-m2-r2` returned `clean-with-notes`; M2 closed and ready for `implement M3`.
- 2026-05-19 M2 rerun code-review recording validation: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-19-rigorloop-published-skill-design-contract` passed.
- 2026-05-19 M2 rerun code-review recording validation: `python scripts/validate-change-metadata.py docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml` passed.
- 2026-05-19 M2 rerun code-review recording validation: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md --path docs/plan.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-log.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-resolution.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/code-review-m2-r2.md` passed.
- 2026-05-19 M2 rerun code-review recording validation: `git diff --check -- docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md docs/plan.md docs/changes/2026-05-19-rigorloop-published-skill-design-contract` passed.
- 2026-05-19 M2 rerun code-review recording validation: `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md --path docs/plan.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-log.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-resolution.md --path docs/changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/code-review-m2-r2.md` passed selected review-artifact, artifact-lifecycle, change-metadata regression, and change-metadata checks.

## Outcome and retrospective

- Pending. Do not use this section for current handoff state while the plan is active; see `Current Handoff Summary`.

## Readiness

- See `Current Handoff Summary`.
- This plan is ready for `implement M3`, not final verification, branch readiness, or PR readiness.

## Risks and follow-ups

- Follow-up candidates identified by the M1 audit must include skill name, reason it may not earn its existence, affected artifacts or gates, likely owner, and whether a separate proposal or spec amendment is required.
