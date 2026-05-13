# Follow-up Ownership and Deferred Work Register Plan

- Status: active
- Owner: maintainers
- Start date: 2026-05-13
- Last updated: 2026-05-13
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

Implement the approved follow-up ownership contract so deferred work is routed to action-owning artifacts, `project-map` remains an orientation surface, and an optional `docs/follow-ups.md` register is introduced only when a qualifying unowned cross-change follow-up exists.

This plan exists because the change touches workflow guidance, canonical skill text, and validation expectations. It should land in small reviewable slices without creating a new workflow stage, new skill, empty follow-up register, or shared wording template.

## Source artifacts

- Proposal: [Follow-Up Ownership and Deferred Work Register](../proposals/2026-05-13-follow-up-ownership-and-deferred-work-register.md)
- Spec: [Follow-up Ownership and Deferred Work Register](../../specs/follow-up-ownership-and-deferred-work-register.md)
- Spec review: [spec-review-r1](../changes/2026-05-13-follow-up-ownership-and-deferred-work-register/reviews/spec-review-r1.md)
- Architecture: not required by `spec-review-r1`; the change is workflow documentation, skill wording, and optional lightweight validation rather than a boundary or runtime architecture change.
- Test spec: [Follow-up Ownership and Deferred Work Register Test Spec](../../specs/follow-up-ownership-and-deferred-work-register.test.md), active.

## Context and orientation

Relevant surfaces:

- `docs/workflows.md` is the user-facing workflow guide and must own the follow-up ownership table.
- `skills/workflow/SKILL.md` routes work through the lifecycle and should receive concise follow-up routing wording only.
- `skills/project-map/SKILL.md` describes repository orientation and should receive concise "not a backlog" boundary wording only.
- `docs/follow-ups.md` must not be created in M1 because no accepted unowned cross-change follow-up has been identified for this slice.
- `templates/shared/` must not receive a new follow-up ownership block in this slice.
- `docs/project-map.md` is absent in the current repository; no project-map content is relied on for this plan.
- `docs/plan.md` is the lifecycle index and this file is the plan body.

Validation and generated-output context:

- Canonical skill source lives under `skills/`.
- Generated public adapter skill bodies are not tracked source for `v0.1.3` and later, but adapter generation checks may still be useful when canonical skills change.
- Existing repository validation includes skill validation, artifact lifecycle validation, review artifact validation, and diff whitespace checks.

## Non-goals

- Do not create a new workflow stage.
- Do not create a new skill.
- Do not turn `project-map` into a backlog.
- Do not create an empty `docs/follow-ups.md`.
- Do not introduce a `templates/shared/` block in this slice.
- Do not migrate all historical follow-ups.
- Do not add heavy semantic validation for every possible follow-up ownership claim.
- Do not change workflow stage order.

## Requirements covered

- `R1`-`R1d`: update `docs/workflows.md` with follow-up ownership guidance and keep it as policy owner.
- `R2`-`R2f`: document action-owning artifact routing.
- `R3`-`R3d`: clarify `project-map` orientation and actionable-risk routing.
- `R4`-`R4d`: update `workflow` routing boundaries.
- `R5`-`R5c`: preserve `learn` as lesson capture, not a backlog.
- `R6`-`R6c`: avoid creating `docs/follow-ups.md` unless creation rules are met.
- `R7`-`R9g`: plan and test optional register shape, admission, and status behavior; implement only if the register is introduced.
- `R10`-`R10c`: avoid first-slice shared templates.
- `R11`-`R11f`: keep skill wording concise and avoid duplicating the full ownership table in skills.
- `R12`-`R12e`: add lightweight register validation only if `docs/follow-ups.md` is created.
- `R13`-`R13a`: record affected-surface decisions and validation evidence.

## Current Handoff Summary

- Current milestone: M2
- Current milestone state: closed
- Last reviewed milestone: M2
- Review status: M2 clean-with-notes
- Remaining in-scope implementation milestones: none
- Next stage: explain-change
- Final closeout readiness: ready
- Reason final closeout is or is not ready: all implementation milestones are closed; final closeout still needs explain-change, verify, and PR handoff.

## Milestones

### M1. Follow-up ownership guidance and concise skill boundaries

- Milestone state: closed
- Goal: Add the durable follow-up ownership rule to `docs/workflows.md` and concise operational wording to `workflow` and `project-map`.
- Requirements: `R1`-`R6c`, `R10`-`R11f`, `R13`-`R13a`
- Files/components likely touched:
  - `docs/workflows.md`
  - `skills/workflow/SKILL.md`
  - `skills/project-map/SKILL.md`
  - `docs/changes/2026-05-13-follow-up-ownership-and-deferred-work-register/change.yaml`
  - possibly generated or adapter metadata only if repository validation requires it
- Dependencies:
  - approved spec
  - plan-review approval
  - test-spec approval before implementation
- Tests to add/update:
  - update static skill validation if existing checks need to enforce concise workflow/project-map wording
  - no register validation yet unless `docs/follow-ups.md` is introduced by a later owner decision
- Implementation steps:
  - Add `Follow-up ownership` section to `docs/workflows.md`.
  - Add concise follow-up routing wording to `skills/workflow/SKILL.md`.
  - Add concise follow-up boundary wording to `skills/project-map/SKILL.md`.
  - Record affected-surface decisions for root guidance, generated public adapter output, and register creation.
  - Do not create `docs/follow-ups.md`.
  - Do not create `templates/shared/<follow-up...>.md`.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path skills/workflow/SKILL.md --path skills/project-map/SKILL.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path skills/workflow/SKILL.md --path skills/project-map/SKILL.md`
  - `git diff --check --`
- Expected observable result:
  - users can find the ownership table in `docs/workflows.md`;
  - `workflow` routes follow-ups without duplicating the full table;
  - `project-map` clearly states it does not own deferred execution;
  - no empty register or shared template exists.
- Commit message: `M1: add follow-up ownership routing guidance`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - skill wording expands into a second policy surface;
  - root guidance or generated-output implications are missed.
- Rollback/recovery:
  - revert concise skill wording and keep only the accepted spec if implementation validation exposes drift;
  - revise the spec if an affected surface proves necessary but is out of scope.

### M2. Validation alignment and lifecycle handoff

- Milestone state: closed
- Goal: Ensure repository validation and lifecycle artifacts prove the first-slice contract and prepare final closeout after implementation review.
- Requirements: `R7`-`R9g`, `R12`-`R13a`
- Files/components likely touched:
  - `scripts/test-skill-validator.py` or existing validator tests if static wording checks need updates
  - `scripts/validation_selection.py` or selector tests only if changed paths are not routed correctly
  - `docs/changes/2026-05-13-follow-up-ownership-and-deferred-work-register/change.yaml`
  - this plan body and `docs/plan.md` during lifecycle updates
- Dependencies:
  - M1 completed or ready for validation;
  - no qualifying register item unless a maintainer explicitly identifies one.
- Tests to add/update:
  - static checks for no first-slice `templates/shared` block if existing validators support it;
  - static checks that `workflow` and `project-map` contain concise required concepts if needed;
  - optional follow-up register validation only if `docs/follow-ups.md` is created.
- Implementation steps:
  - Add or update focused validator coverage only where needed to prove the spec.
  - If `docs/follow-ups.md` remains absent, record that absence as expected for `R6b`.
  - If a qualifying item is identified before implementation, revise this plan before creating the register.
  - Run focused validation and update plan progress/validation notes.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-13-follow-up-ownership-and-deferred-work-register`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-13-follow-up-ownership-and-deferred-work-register/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-13-follow-up-ownership-and-deferred-work-register.md --path specs/follow-up-ownership-and-deferred-work-register.md --path docs/plans/2026-05-13-follow-up-ownership-and-deferred-work-register.md --path docs/plan.md --path docs/changes/2026-05-13-follow-up-ownership-and-deferred-work-register/change.yaml`
  - `python scripts/build-adapters.py --check` if tracked adapter tree output is applicable to the current release surface; otherwise record the mismatch and use release-archive adapter regression proof.
  - `git diff --check --`
- Expected observable result:
  - validation catches drift in affected skill guidance where existing validators support it;
  - lifecycle artifacts remain synchronized;
  - optional register validation is not added unless the register exists.
- Commit message: `M2: validate follow-up ownership guidance`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - over-validating prose could make concise wording brittle;
  - adapter build checks may be too broad for a docs/skill wording slice.
- Rollback/recovery:
  - keep validation focused on stable phrases and required absence/presence checks;
  - if adapter checks are not applicable to current tracked output, record the reason in validation notes and use canonical skill validation as the required proof.

## Validation plan

Minimum before plan-review:

- `python scripts/validate-change-metadata.py docs/changes/2026-05-13-follow-up-ownership-and-deferred-work-register/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-13-follow-up-ownership-and-deferred-work-register.md --path specs/follow-up-ownership-and-deferred-work-register.md --path docs/plans/2026-05-13-follow-up-ownership-and-deferred-work-register.md --path docs/plan.md`
- `git diff --check --`

Implementation validation is listed per milestone.

Final verification before PR should include:

- review artifact closeout validation;
- change metadata validation;
- lifecycle explicit-path validation for touched lifecycle artifacts;
- skill validation;
- selector tests if validation routing changes;
- adapter generation check if canonical skill changes require adapter proof;
- `git diff --check --`.

## Risks and recovery

- Risk: `docs/workflows.md` grows too detailed. Recovery: keep only the ownership table and route deeper shape details to the spec.
- Risk: skills duplicate the full ownership table. Recovery: remove duplicated table and leave concise routing/boundary wording.
- Risk: `docs/follow-ups.md` is created without a qualifying item. Recovery: remove the empty file and record the no-register rationale in the plan or change metadata.
- Risk: validators enforce prose too tightly. Recovery: check stable concepts and structural outcomes rather than full paragraphs.
- Risk: generated-output expectations are stale. Recovery: follow current `dist/adapters/README.md` and record adapter-output handling evidence in validation notes.

## Dependencies

- `specs/follow-up-ownership-and-deferred-work-register.md` approved.
- `plan-review` approval before `test-spec`.
- `test-spec` approval before implementation.
- No architecture package is required unless plan-review or later evidence identifies a boundary, data-flow, or generated-output architecture change.
- No `docs/follow-ups.md` register is created unless a maintainer identifies a qualifying accepted unowned cross-change follow-up.

## Progress

- 2026-05-13: proposal accepted, spec approved, plan created and indexed.
- 2026-05-13: plan-review approved with no material findings; test spec created, active, and maintainer-approved; ready for implement M1.
- 2026-05-13: M1 implementation started; static validator tests were added first and failed against the missing workflow and skill wording as expected.
- 2026-05-13: M1 implementation completed: `docs/workflows.md` now owns the follow-up ownership table, `workflow` and `project-map` contain concise operational wording, and no `docs/follow-ups.md` or follow-up shared template was created.
- 2026-05-13: M1 code-review passed with `clean-with-notes`; M1 is closed and M2 is the next implementation milestone.
- 2026-05-13: M2 implementation started; validation alignment is being checked without introducing `docs/follow-ups.md` or register-specific validators because no qualifying register item exists.
- 2026-05-13: M2 implementation completed; validation alignment is recorded, optional register validation remains unintroduced because no register exists, and M2 is ready for code-review.
- 2026-05-13: M2 code-review passed with `clean-with-notes`; all implementation milestones are closed and final closeout starts with `explain-change`.

## Decision log

- 2026-05-13: no architecture package planned -> `spec-review-r1` found no boundary or runtime architecture change.
- 2026-05-13: first slice does not create `docs/follow-ups.md` -> no qualifying accepted unowned cross-change follow-up has been identified.
- 2026-05-13: first slice does not create `templates/shared/` wording -> only `workflow` and `project-map` need concise wording.
- 2026-05-13: test spec uses real repository files for M1 proof and synthetic fixtures only if optional register validation is introduced.
- 2026-05-13: `python scripts/build-adapters.py --check` is not applicable as a passing tree-output check in the current branch state because `dist/adapters/README.md` and `manifest.yaml` define the `v0.1.3` release-archive support surface while generated public adapter skill bodies are not tracked.

## Surprises and discoveries

- `docs/project-map.md` is absent; this plan does not rely on it.

## Validation notes

- 2026-05-13: `python scripts/test-skill-validator.py` failed before implementation on the new M1 checks because `docs/workflows.md`, `skills/workflow/SKILL.md`, and `skills/project-map/SKILL.md` did not yet contain the required follow-up ownership wording. The no-empty-register/no-shared-template check passed.
- 2026-05-13: `python scripts/test-skill-validator.py` passed after implementation.
- 2026-05-13: `python scripts/validate-skills.py` passed.
- 2026-05-13: `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path skills/workflow/SKILL.md --path skills/project-map/SKILL.md` passed and selected skill, generation, adapter, lifecycle, and selector checks for the changed workflow and skill surfaces.
- 2026-05-13: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path skills/workflow/SKILL.md --path skills/project-map/SKILL.md` passed.
- 2026-05-13: `python scripts/test-build-skills.py` passed.
- 2026-05-13: `python scripts/build-skills.py --check` passed.
- 2026-05-13: `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives` passed.
- 2026-05-13: `python scripts/test-select-validation.py` passed.
- 2026-05-13: `git diff --check --` passed.
- 2026-05-13: M1 handoff commit created with subject `M1: add follow-up ownership routing guidance`.
- 2026-05-13: M2 `python scripts/test-skill-validator.py` passed.
- 2026-05-13: M2 `python scripts/validate-skills.py` passed.
- 2026-05-13: M2 `python scripts/test-select-validation.py` passed.
- 2026-05-13: M2 `python scripts/build-adapters.py --check` failed because it still checks default `0.1.1` tracked adapter tree output and expects generated public adapter skill bodies missing from the `v0.1.3` tracked support surface. This is recorded as non-applicable to this slice rather than fixed here.
- 2026-05-13: M2 `python scripts/build-adapters.py --version v0.1.3 --check` also failed on tracked tree-output expectations and a manifest command-alias rule mismatch, confirming the check is stale for the current release-archive model.
- 2026-05-13: M2 `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives` passed as the applicable release-archive adapter regression proof.
- 2026-05-13: M2 handoff commit created with subject `M2: validate follow-up ownership guidance`.

## Outcome and retrospective

- Pending implementation and final lifecycle closeout.

## Readiness

- See `Current Handoff Summary`.
