# Publish Next Release With Single Authored Skill Source

- Status: active
- Owner: maintainer
- Start date: 2026-05-13
- Last updated: 2026-05-13
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

This plan sequences the implementation work for the `v0.1.1` single-authored-source transition release.

The release must prove the public adapter path works without making `.codex/skills/` a required release artifact. Contributors still author skills once in `skills/`; tracked public adapter output under `dist/adapters/` remains the public install path for this compatibility release; `.codex/skills/` stays ignored local runtime state.

## Source artifacts

- Proposal: `docs/proposals/2026-05-12-publish-next-release-with-single-authored-skill-source.md`
- Spec: `specs/publish-next-release-with-single-authored-skill-source.md`
- Architecture: `docs/architecture/system/architecture.md`
- Related ADR: `docs/adr/ADR-20260512-generated-skill-output-release-artifacts.md`
- Change metadata: `docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/change.yaml`
- Review log: `docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/review-log.md`
- Proposal review: `docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/reviews/proposal-review-r1.md`
- Spec reviews: `docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/reviews/spec-review-r1.md`, `docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/reviews/spec-review-r2.md`
- Architecture reviews: `docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/reviews/architecture-review-r1.md`, `docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/reviews/architecture-review-r2.md`
- Plan review: `docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/reviews/plan-review-r1.md`
- Test spec: `specs/publish-next-release-with-single-authored-skill-source.test.md`

## Context and orientation

No `docs/project-map.md` exists in this checkout, so this plan uses direct source inspection rather than a project-map reference.

Relevant implementation surfaces:

- `scripts/release-verify.sh` is the maintainer-facing release gate for `v0.1.1`.
- `scripts/validate-release.py` delegates structured validation to `adapter_distribution.validate_release_output`.
- `scripts/adapter_distribution.py` owns adapter drift, adapter validation, release metadata validation, token-cost report delegation, and changed-public-skill tracing.
- `scripts/build-adapters.py --version 0.1.1 --check` validates tracked public adapter output during the compatibility window.
- `scripts/validate-adapters.py --version 0.1.1` validates public adapter package structure and security markers.
- `scripts/build-skills.py --check` validates non-release local mirror generation into temporary output, but the `v0.1.1` release gate must not require `.codex/skills/` generation as release evidence.
- `dist/adapters/README.md` is the public adapter install guide for repository-tree adapter packages.
- `docs/releases/v0.1.1/release-notes.md` and `docs/releases/v0.1.1/release.yaml` are tracked release evidence.
- `docs/reports/token-cost/releases/v0.1.1.yaml` is structured token-friendliness release metadata.

Current known mismatch before implementation:

- `scripts/release-verify.sh v0.1.1` still invokes `python scripts/build-skills.py --check` and labels it as a generated Codex skill drift check. That conflicts with the approved transition-release spec because `.codex/skills/` must not be required release evidence for `v0.1.1`.
- `docs/releases/v0.1.1/release-notes.md` still says release verification checks generated `.codex/skills/`.
- `dist/adapters/README.md` is directionally correct, but it is not version-specific for `v0.1.1` and does not state that archives are not required for this transition release.

## Non-goals

- Do not remove tracked public adapter skill copies under `dist/adapters/**/skills`.
- Do not remove support for Codex, Claude Code, or opencode.
- Do not require downloadable adapter archives for `v0.1.1`.
- Do not change skill behavior or skill wording.
- Do not introduce a package manager, hosted registry, or installer.
- Do not replace non-release local Codex setup validation governed by `specs/single-authored-skill-source-generated-output.md`.
- Do not publish, tag, merge, or deploy as part of this implementation plan.
- Do not rewrite Git history.

## Requirements covered

- R1-R6: Preserve source and release surfaces through release-gate and docs changes.
- R7-R9: Keep `scripts/release-verify.sh` as the maintainer-facing gate and delegate structured checks to `scripts/validate-release.py`.
- R10-R19: Validate canonical skills, tracked public adapter output, adapter docs, token-cost metadata, release notes, and `.codex/skills/` ignored/untracked state without generating `.codex/skills/` as release evidence.
- R20-R25: Update adapter install and local Codex setup guidance.
- R26-R31: Keep adapter archives out of required `v0.1.1` scope while preserving optional metadata behavior if a separate accepted plan publishes archives.
- R32-R35: Preserve token-cost source behavior: static `skills/`, dynamic public Codex adapter output, never `.codex/skills/`.

## Current Handoff Summary

- Current milestone: M2. Release docs and adapter install guidance describe the transition
- Current milestone state: review-requested
- Last reviewed milestone: M2 code-review r1 changes-requested
- Review status: CR-M2-F1 accepted and resolved; M2 ready for code-review rerun
- Remaining in-scope implementation milestones: M2 review-requested, M3 planned
- Next stage: code-review M2 rerun
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: M2 needs code-review rerun after CR-M2-F1 resolution, M3 is not implemented or reviewed, final validation has not run, and PR handoff is not prepared.

## Milestones

### M1. Release gate validates public output, not `.codex/skills/`

- Milestone state: closed
- Goal: Make the `v0.1.1` release gate validate canonical skills and public adapter output without requiring `.codex/skills/` generation as release evidence.
- Requirements: R7-R19, R32-R35
- Files/components likely touched:
  - `scripts/release-verify.sh`
  - `scripts/validate-release.py`
  - `scripts/adapter_distribution.py`
  - `scripts/test-adapter-distribution.py`
  - possibly `scripts/build-skills.py` only if a clearer non-release local-smoke command or message is needed
- Dependencies:
  - Approved spec and architecture.
  - Existing token-cost validator must continue rejecting `.codex/skills/` as a public benchmark source.
- Tests to add/update:
  - Update dry-run release gate tests so `v0.1.1` no longer requires `python scripts/build-skills.py --check`.
  - Add or update release validation tests proving `.codex/skills/` tracked-state absence is checked without building `.codex/skills/`.
  - Preserve tests for historical releases if their existing release contract still requires the old check.
  - Preserve token-cost metadata tests that reject `.codex/skills/`.
- Implementation steps:
  - Remove `build-skills.py --check` from required `v0.1.1` release evidence in `scripts/release-verify.sh`.
  - Keep `python scripts/validate-skills.py` as canonical skill validation.
  - Keep `python scripts/build-adapters.py --version 0.1.1 --check` and `python scripts/validate-adapters.py --version 0.1.1` as public adapter output proof.
  - Ensure `scripts/validate-release.py` or its helper confirms `.codex/skills/` is ignored/untracked for `v0.1.1`.
  - Keep optional local Codex smoke outside required release evidence.
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.1`
  - `python scripts/validate-release.py --version v0.1.1`
  - `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml`
  - `git diff --check -- scripts/release-verify.sh scripts/validate-release.py scripts/adapter_distribution.py scripts/test-adapter-distribution.py`
- Expected observable result: The `v0.1.1` dry-run release gate lists canonical skill validation, public adapter drift validation, adapter validation, token-cost validation, and release metadata validation, but does not list `build-skills.py --check` as required release evidence.
- Commit message: `M1: align release gate with public adapter evidence`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - Accidentally weakening non-release local mirror validation.
  - Breaking historical `v0.1.0` release gate tests.
- Rollback/recovery:
  - Revert release-gate script changes and tests for M1 only.
  - Keep spec and architecture intact; do not re-track `.codex/skills/`.

### M2. Release docs and adapter install guidance describe the transition

- Milestone state: review-requested
- Goal: Make public and contributor-facing docs match the transition release contract.
- Requirements: R1-R6, R20-R31
- Files/components likely touched:
  - `dist/adapters/README.md`
  - `docs/releases/v0.1.1/release-notes.md`
  - `docs/releases/v0.1.1/release.yaml`
  - `README.md`, `docs/workflows.md`, or `AGENTS.md` only if existing contributor guidance conflicts with the approved spec
  - `CONSTITUTION.md` if governance guidance conflicts with the approved spec
  - `scripts/test-adapter-distribution.py`
- Dependencies:
  - M1 release-gate contract should be settled so docs can name the right verification behavior.
- Tests to add/update:
  - Adapter README tests for version-specific `v0.1.1` repository-tree install guidance.
  - Release-note validation tests that reject claims that `.codex/skills/` is release evidence for `v0.1.1`.
  - Documentation tests that keep `.codex/skills/` as a local runtime install directory, not a public adapter source.
- Implementation steps:
  - Update `dist/adapters/README.md` with explicit `v0.1.1` repository-tree install guidance.
  - State no downloadable adapter archives are required for `v0.1.1` unless separately published.
  - Fix adapter artifact metadata wording to `docs/reports/adapter-artifacts/releases/<version>.yaml`.
  - Update `docs/releases/v0.1.1/release-notes.md` so verification describes public adapter output and no longer says generated `.codex/skills/` is checked as release evidence.
  - Add contributor-facing local Codex setup wording where the repository already owns that guidance: generate or use the public Codex adapter, then install/copy it into ignored `.codex/skills/`.
  - Keep generated public adapter skill bodies unchanged unless M1 or docs changes require adapter package regeneration.
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-release.py --version v0.1.1`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `git diff --check -- dist/adapters/README.md docs/releases/v0.1.1/release-notes.md docs/releases/v0.1.1/release.yaml README.md docs/workflows.md AGENTS.md scripts/test-adapter-distribution.py`
- Expected observable result: Adapter docs and release notes state `dist/adapters/` remains the `v0.1.1` public install path, archives are not required, and `.codex/skills/` is ignored local runtime state rather than release evidence.
- Commit message: `M2: document transition release adapter install path`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Review notes:
  - code-review-m2-r1 requested changes for CR-M2-F1: contributor/governance docs still preserve obsolete `.codex/skills/` hand-edit/generated-output wording instead of only the concise active local setup rule.
  - M2 review-resolution checklist: Does this change delete obsolete `.codex/skills/` guidance instead of preserving it as defensive wording?
  - CR-M2-F1 was accepted and resolved by simplifying local Codex setup wording and adding static regression coverage against the stale defensive phrases.
- Risks:
  - Docs could overstate archive availability.
  - Contributor docs could imply `.codex/skills/` is generated directly as release output.
- Rollback/recovery:
  - Revert M2 docs and test expectations, then restore the prior release-note wording only if the approved spec is also revised.

### M3. Release evidence and final validation pack

- Milestone state: planned
- Goal: Prove `v0.1.1` release readiness with the updated gate, public adapter output, token-cost evidence, release notes, and lifecycle state.
- Requirements: R1-R35
- Files/components likely touched:
  - `docs/releases/v0.1.1/release.yaml`
  - `docs/reports/token-cost/releases/v0.1.1.yaml`
  - `docs/reports/token-cost/releases/v0.1.1.md`
  - `dist/adapters/manifest.yaml`
  - `dist/adapters/**` only if adapter drift is found and regenerated
  - this plan file and `docs/plan.md`
  - change-local evidence under `docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/`
- Dependencies:
  - M1 and M2 closed.
  - Plan-review and test-spec completed before implementation begins.
- Tests to add/update:
  - Test spec will define final release readiness coverage.
  - Add regression tests only for gaps found while running release validation.
- Implementation steps:
  - Run canonical skill validation.
  - Run tracked public adapter drift check and adapter validation.
  - Run token-cost report validation and confirm dynamic source is public Codex adapter output.
  - Run release metadata validation and full release dry run.
  - If generated public adapter output is stale, regenerate with `python scripts/build-adapters.py --version 0.1.1` and re-run adapter validation.
  - Record validation evidence in the plan and change metadata.
  - Keep the plan active until downstream review, explain-change, verify, and PR gates complete; this plan does not publish the release.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml`
  - `python scripts/validate-release.py --version v0.1.1`
  - `bash scripts/release-verify.sh v0.1.1`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-12-publish-next-release-with-single-authored-skill-source.md --path specs/publish-next-release-with-single-authored-skill-source.md --path docs/architecture/system/architecture.md --path docs/plans/2026-05-13-publish-next-release-with-single-authored-skill-source.md --path docs/plan.md --path docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/change.yaml`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/`
  - `git diff --check --`
- Expected observable result: The updated `v0.1.1` release gate passes without requiring `.codex/skills/` generation as release evidence, public adapter output validates, token-cost metadata validates, and lifecycle artifacts are synchronized.
- Commit message: `M3: validate transition release readiness evidence`
- Milestone closeout:
  - [ ] validation passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks:
  - Full release verification may expose stale adapter output or stale token-cost metadata.
  - Running the full release gate may depend on local tool availability for smoke-adjacent evidence.
- Rollback/recovery:
  - If full validation fails because release evidence is stale, defer publication and update the evidence through the relevant milestone.
  - If public adapter packaging fails, keep `dist/adapters/` as the public install path and defer archives.
  - Do not re-track `.codex/skills/` as recovery for this transition release.

## Validation plan

Before implementation:

- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-12-publish-next-release-with-single-authored-skill-source.md --path specs/publish-next-release-with-single-authored-skill-source.md --path docs/architecture/system/architecture.md --path docs/plans/2026-05-13-publish-next-release-with-single-authored-skill-source.md --path docs/plan.md --path docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/change.yaml`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/change.yaml`
- `python scripts/validate-review-artifacts.py docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/`
- `git diff --check -- docs/plan.md docs/plans/2026-05-13-publish-next-release-with-single-authored-skill-source.md docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source`

During implementation, run each milestone's targeted commands before code-review handoff.

Before PR handoff, run the M3 final validation pack plus any commands added by the test spec, plan-review, code-review, or verify.

## Risks and recovery

- Risk: The release gate becomes weaker than the spec by removing too much validation. Recovery: keep canonical skill validation, adapter drift checks, adapter structural validation, release metadata validation, release notes validation, token-cost metadata validation, and `.codex/skills/` ignored/untracked validation.
- Risk: The implementation conflates non-release local mirror validation with release evidence. Recovery: keep `build-skills.py --check` available for local or canonical-skill-change validation but remove it from required `v0.1.1` release evidence.
- Risk: Release docs claim archives exist or are required. Recovery: revise release notes and adapter docs to keep archives deferred unless a separate accepted archive plan publishes them.
- Risk: Adapter output drift appears late. Recovery: regenerate tracked adapter output from canonical sources with `python scripts/build-adapters.py --version 0.1.1`, inspect the diff, then rerun adapter validation.
- Risk: Token-cost metadata names the wrong dynamic skill source. Recovery: correct metadata to public Codex adapter output and rerun `scripts/validate-token-cost-report.py`.

## Dependencies

- Plan-review must approve this plan before test-spec and implementation.
- Test-spec must map spec requirements to concrete tests before implementation.
- `scripts/release-verify.sh` and `scripts/validate-release.py` must agree on the final `v0.1.1` release contract.
- `dist/adapters/**` remains tracked for this release.
- Downloadable adapter archives are out of scope unless a separate accepted plan changes scope.
- Final publication, tagging, and GitHub release operations are outside this plan.

## Progress

- [x] 2026-05-13: Proposal accepted, spec approved, canonical architecture updated, and architecture-review approved.
- [x] 2026-05-13: Execution plan created and added to `docs/plan.md`.
- [x] Plan-review completed.
- [x] Test-spec created.
- [x] M1 implemented and reviewed clean.
- [x] M2 implemented and ready for code-review.
- [ ] M3 implemented and reviewed.
- [ ] Final explain-change, verify, and PR handoff completed.

## Decision log

- 2026-05-13: Use three implementation milestones: release gate, docs/release guidance, final evidence pack. This keeps validation behavior, user-facing compatibility language, and release-readiness proof reviewable as separate slices.
- 2026-05-13: Do not create an adapter archive milestone. The approved spec makes archives a follow-on migration unless a separate accepted plan publishes them.
- 2026-05-13: Keep this plan active after creation and hand off to `plan-review`; readiness for review is not implementation completion.
- 2026-05-13: Plan-review approved the plan with no material findings; proceed to test-spec before implementation.
- 2026-05-13: Test spec created as the active proof surface for M1 implementation.
- 2026-05-13: M1 keeps `build-skills.py --check` available for historical release gates but removes it from required `v0.1.1` release evidence.
- 2026-05-13: `validate-release.py` treats a no-argument CLI invocation as an explicit empty changed-surface context, while direct helper callers still must pass changed-surface context for final `skill-token-runtime-v2` release validation.
- 2026-05-13: M1 code-review r1 did not close the milestone because the governing artifacts and change-local records are still untracked in the local worktree.
- 2026-05-13: M1 was committed as `4eb0521` and code-review r2 closed the milestone cleanly with no material findings.
- 2026-05-13: M2 updates `CONSTITUTION.md` in addition to the planned docs because it carried higher-priority stale local Codex setup guidance that conflicted with the approved transition-release contract.
- 2026-05-13: `docs/releases/v0.1.1/release.yaml` is intentionally unchanged in M2; the release metadata values remain valid and `python scripts/validate-release.py --version v0.1.1` passes after the release-note wording update.

## Surprises and discoveries

- `docs/project-map.md` is absent, so no project-map context was used.
- `scripts/build-skills.py --check` already uses temporary output, but `scripts/release-verify.sh` still treats it as required release evidence for `v0.1.1`, which is the main release-gate mismatch this plan addresses.
- `dist/adapters/README.md` already contains most transition guidance but needs `v0.1.1`-specific wording and archive-scope clarification.
- `python scripts/validate-release.py --version v0.1.1` initially failed without changed-path arguments because the CLI passed missing changed-surface context through to the structured validator; the CLI now supplies an explicit empty context for maintainer-facing release validation.
- M2 tests exposed stale local Codex setup wording in README, workflow guidance, AGENTS, and CONSTITUTION; all now point local Codex use through public Codex adapter output.

## Validation notes

- Plan creation and plan-review recording validation passed before test-spec authoring:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/`
  - `python scripts/test-change-metadata-validator.py`
  - `git diff --check -- ...`

- Test-spec creation validation passed before M1 implementation.

- M1 targeted validation passed:
  - `python scripts/test-adapter-distribution.py`
  - `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.1`
  - `python scripts/validate-release.py --version v0.1.1`
  - `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml`
  - `git diff --check -- scripts/release-verify.sh scripts/validate-release.py scripts/adapter_distribution.py scripts/test-adapter-distribution.py`

- M1 code-review r1 recorded inconclusive:
  - Review record: `docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/reviews/code-review-m1-r1.md`
  - Direct review checks passed:
    - `git ls-files -- .codex/skills/`
    - `git check-ignore -v .codex/skills/proposal/SKILL.md`
    - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_release_verify_script_supports_v0_1_1 AdapterDistributionTests.test_v0_1_1_release_validation_accepts_ignored_untracked_codex_skills AdapterDistributionTests.test_v0_1_1_release_validation_rejects_tracked_codex_skills AdapterDistributionTests.test_v0_1_1_release_validation_rejects_unignored_codex_skills AdapterDistributionTests.test_v2_final_release_validation_requires_changed_surface_input`
    - `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.1`

- M1 code-review r2 recorded clean-with-notes:
  - Review record: `docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/reviews/code-review-m1-r2.md`
  - Reviewed commit: `4eb0521`
  - Direct review checks passed:
    - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_release_verify_script_supports_v0_1_1 AdapterDistributionTests.test_v0_1_1_release_validation_accepts_ignored_untracked_codex_skills AdapterDistributionTests.test_v0_1_1_release_validation_rejects_tracked_codex_skills AdapterDistributionTests.test_v0_1_1_release_validation_rejects_unignored_codex_skills AdapterDistributionTests.test_v2_final_release_validation_requires_changed_surface_input`
    - `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.1`
    - `python scripts/validate-release.py --version v0.1.1`
    - `git ls-files -- .codex/skills/`
    - `git check-ignore -v .codex/skills/proposal/SKILL.md`

- M2 targeted validation passed:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-release.py --version v0.1.1`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `git diff --check -- dist/adapters/README.md docs/releases/v0.1.1/release-notes.md docs/releases/v0.1.1/release.yaml README.md docs/workflows.md AGENTS.md CONSTITUTION.md scripts/test-adapter-distribution.py scripts/adapter_distribution.py`

- M2 unaffected with rationale:
  - `docs/releases/v0.1.1/release.yaml` remains unchanged because M2 changed release-note prose and docs assertions only; structured validation still passes.
  - Generated public adapter skill bodies under `dist/adapters/**/skills` remain unchanged because M2 changed install guidance and release notes only.

## Outcome and retrospective

Not completed. M1 is closed; M2 implementation is ready for code-review; M3, final explain-change, verify, and PR handoff remain open.

## Readiness

See `Current Handoff Summary`.

## Remaining completion gates

- M2 implementation, targeted validation, code-review, and review-resolution if triggered.
- M3 implementation, targeted validation, code-review, and review-resolution if triggered.
- Explain-change.
- Verify.
- PR handoff.
- Public release publication remains outside this plan.
