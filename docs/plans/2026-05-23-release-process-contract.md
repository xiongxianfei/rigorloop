# Release Process Contract Execution Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Owner: maintainer
- Start date: 2026-05-23
- Last updated: 2026-05-23
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

Implement the approved standing release-process contract without turning routine publishes into new lifecycle changes. The first implementation slice should make the process executable and reviewable: release evidence has a stable template/checklist, release evidence paths route through validation, the release gate has concrete commands and dry-run proof, and downstream validation can catch stale generated output, missing registry verification, unsafe emergency deferrals, and secret-bearing evidence.

## Source artifacts

- Proposal: `docs/proposals/2026-05-23-release-process-contract.md`
- Spec: `specs/release-process-contract.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260523-release-process-contract.md`
- Architecture review: `docs/changes/2026-05-23-release-process-contract/reviews/architecture-review-r1.md`
- Test spec: `specs/release-process-contract.test.md`
- Change metadata: `docs/changes/2026-05-23-release-process-contract/change.yaml`

## Context and orientation

Existing release support already includes `docs/releases/<version>/release.yaml`, `docs/releases/<version>/release-notes.md`, `docs/releases/v0.1.4/npm-publication.md`, `docs/releases/v0.1.5/npm-publication.md`, `scripts/validate-release.py`, `scripts/validate-release-ci.py`, `scripts/release-verify.sh`, and release selector routing.

The new standing release-process evidence file is `docs/releases/v<version>.md`. That path is deliberately version-scoped and separate from change-local evidence. Current selector routing categorizes all `docs/releases/` paths as release paths, but release-version inference only handles `docs/releases/<version>/<file>` and must be extended or explicitly handled for `docs/releases/v<version>.md`.

Generated-output currency is already represented by `skills.drift`, `adapters.drift`, `scripts/build-skills.py --check`, `scripts/build-adapters.py --check`, adapter archive validation, and release validation. The implementation should reuse those checks and avoid introducing a parallel release validation authority.

## Non-goals

- Do not publish a package as part of this implementation.
- Do not require proposal/spec/plan for each routine publish.
- Do not change package contents, CLI public behavior, skill behavior, adapter layout, lockfile semantics, release archive trust boundaries, or npm package name.
- Do not add staged publishing in the first slice.
- Do not build a fully automated release CLI.
- Do not backfill historical release evidence into the new `docs/releases/v<version>.md` shape.
- Do not store npm tokens, OTPs, credentials, private environment dumps, hostnames, usernames, or machine-local paths in release evidence.

## Requirements covered

- REL-R1 through REL-R6: M1, M2, M3
- REL-R7 through REL-R13: M1, M2
- REL-R14 through REL-R27: M1, M3
- REL-R28 through REL-R41: M1, M2
- REL-R42 through REL-R50: M1, M3
- REL-R51 through REL-R56: M1, M3
- REL-R57 through REL-R64: M1, M2, M3
- REL-R65 through REL-R72: M1, M2
- AC-REL-001 through AC-REL-014: M1, M2, M3, M4

## Current Handoff Summary

- Current milestone: M4. Lifecycle closeout and final validation
- Current milestone state: closed
- Last reviewed milestone: M4. Lifecycle closeout and final validation
- Review status: code-review-m4-r1 clean-with-notes; no review-resolution required
- Remaining in-scope implementation milestones: none
- Next stage: hosted CI and human review
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: all implementation milestones are closed, explain-change is recorded, code-review is clean, final verify passed, and PR #89 is open for hosted CI and human review; final lifecycle closeout is not claimed before PR review completes.

## Milestones

### M1. Release evidence template and checklist

- Milestone state: closed
- Goal: Create the durable authoring surfaces for routine release evidence and the initial release-evidence checklist without adding a dedicated validator yet.
- Requirements: REL-R1 through REL-R18, REL-R23 through REL-R41, REL-R42 through REL-R50, REL-R57 through REL-R72, AC-REL-001 through AC-REL-014
- Files/components likely touched:
  - `docs/releases/README.md`
  - `docs/releases/index.md`
  - `templates/release-evidence.md`
  - `specs/release-process-contract.test.md`
  - `docs/changes/2026-05-23-release-process-contract/change.yaml`
- Dependencies:
  - Plan-review approval.
  - Test spec created before implementation.
- Tests to add/update:
  - Test-spec cases for required evidence sections, release type/no-new-decision claim, version/dist-tag recording, gate table, package contents, publish path, registry verification, recovery notes, secret suppression, emergency deferrals, and non-deferrable requirements.
- Implementation steps:
  - Add a contributor-facing `docs/releases/README.md` that explains the version-scoped evidence contract and how it relates to existing `docs/releases/<version>/release.yaml` and release notes.
  - Add or initialize `docs/releases/index.md` with the approved index shape.
  - Add `templates/release-evidence.md` with the required evidence headings and checklist fields from the approved spec.
  - Keep the checklist explicit that routine publishes do not update `docs/plan.md` unless tied to an active lifecycle plan.
- Validation commands:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/release-process-contract.test.md --path docs/plans/2026-05-23-release-process-contract.md --path docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `git diff --check -- docs/releases/README.md docs/releases/index.md templates/release-evidence.md specs/release-process-contract.test.md docs/plans/2026-05-23-release-process-contract.md docs/changes/2026-05-23-release-process-contract`
- Expected observable result: Maintainers have a stable release evidence template and checklist that can reconstruct the release without exposing secrets or replacing upstream lifecycle review.
- Commit message: `M1: add release evidence template and checklist`
- Milestone closeout:
  - targeted validation passed
  - progress updated
  - decision log update not needed
  - validation notes updated
  - milestone handoff prepared for code-review
- Risks:
  - The template could duplicate old release YAML semantics instead of layering the new standing evidence record.
- Rollback/recovery:
  - Revert the template/index/README additions and keep the approved spec/architecture unchanged until a smaller template slice is planned.

### M2. Release evidence routing and checklist validation fixtures

- Milestone state: closed
- Goal: Ensure `docs/releases/v<version>.md` routes deterministically and that checklist validation can reject missing or unsafe release evidence without introducing a broad dedicated validator prematurely.
- Requirements: REL-R6, REL-R28 through REL-R41, REL-R63 through REL-R72, AC-REL-003, AC-REL-005, AC-REL-010 through AC-REL-014
- Files/components likely touched:
  - `scripts/validation_selection.py`
  - `scripts/test-select-validation.py`
  - `scripts/artifact_lifecycle_contracts.py` or `scripts/artifact_lifecycle_validation.py` if lifecycle validation needs a lightweight release-evidence artifact class
  - `scripts/test-artifact-lifecycle-validator.py` if lifecycle validation is extended
  - `specs/release-process-contract.test.md`
  - `docs/changes/2026-05-23-release-process-contract/change.yaml`
- Dependencies:
  - M1 template/checklist shape is available.
- Tests to add/update:
  - Selector test proving `docs/releases/v1.2.3.md` or equivalent routes without `manual-routing-required`.
  - Test proving old `docs/releases/v1.2.3/release.yaml` routing still works.
  - Checklist/lifecycle tests for secret-suppression fields and emergency deferral completeness when implemented as lightweight structural checks.
- Implementation steps:
  - Extend release-version inference or routing so `docs/releases/v<version>.md` is a known release evidence path.
  - Preserve existing release-directory routing for `docs/releases/<version>/release.yaml`, `release-notes.md`, and `npm-publication.md`.
  - Add fixtures for routine evidence, valid emergency deferral, invalid non-deferrable registry-verification deferral, missing owner approval, and secret-bearing evidence markers.
  - Keep first-slice validation lightweight: artifact lifecycle plus checklist, not a fully separate release-evidence validator.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/release-process-contract.test.md --path docs/plans/2026-05-23-release-process-contract.md --path docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `git diff --check -- scripts/validation_selection.py scripts/test-select-validation.py scripts/artifact_lifecycle_contracts.py scripts/artifact_lifecycle_validation.py scripts/test-artifact-lifecycle-validator.py specs/release-process-contract.test.md docs/changes/2026-05-23-release-process-contract`
- Expected observable result: The new `docs/releases/v<version>.md` evidence class has deterministic routing and initial structural/checklist proof, with no broad release validator introduced ahead of evidence-shape stabilization.
- Commit message: `M2: route release evidence and add checklist fixtures`
- Milestone closeout:
  - targeted validation passed
  - progress updated
  - decision log update not needed
  - validation notes updated
  - milestone handoff prepared for code-review
- Risks:
  - A route that is too broad could hide unrelated files under release validation.
- Rollback/recovery:
  - Revert the route and fixtures, then use explicit-path validation only until a narrower route is designed.

### M3. Release gate command integration and dry-run rehearsal evidence

- Milestone state: closed
- Goal: Connect the standing contract to existing release gate commands and record a non-publishing rehearsal proving the gate/checklist can execute without relying on local memory.
- Requirements: REL-R14 through REL-R27, REL-R42 through REL-R56, REL-R57 through REL-R64, AC-REL-005 through AC-REL-009, AC-REL-012, AC-REL-013
- Files/components likely touched:
  - `scripts/release-verify.sh`
  - `scripts/validate-release.py`
  - `scripts/validate-release-ci.py`
  - `scripts/test-adapter-distribution.py`
  - `scripts/test-npm-package-publication.py`
  - `docs/changes/2026-05-23-release-process-contract/release-process-dry-run.md`
  - `specs/release-process-contract.test.md`
  - `docs/changes/2026-05-23-release-process-contract/change.yaml`
- Dependencies:
  - M1 and M2 are closed.
- Tests to add/update:
  - Tests proving the release gate names generated-output drift checks, package preview/pack proof, packed install smoke, registry-verification expectations, and manual fallback behavior.
  - Dry-run proof that no publish command is executed and no real package version is claimed as released.
- Implementation steps:
  - Update release gate documentation or command output only as needed to make the standing gate explicit.
  - Keep existing release-specific validation authoritative for named historical releases.
  - Record a dry-run rehearsal in change-local evidence, not as a real release evidence record.
  - Do not configure real trusted publishing or publish to npm in this milestone.
- Validation commands:
  - `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.5`
  - `python scripts/validate-release-ci.py --version v0.1.5`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/test-npm-package-publication.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/release-process-contract.test.md --path docs/plans/2026-05-23-release-process-contract.md --path docs/plan.md --path docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `git diff --check -- scripts/release-verify.sh scripts/validate-release.py scripts/validate-release-ci.py scripts/test-adapter-distribution.py scripts/test-npm-package-publication.py docs/plans/2026-05-23-release-process-contract.md docs/plan.md docs/changes/2026-05-23-release-process-contract`
  - `git diff --check -- scripts/release-verify.sh scripts/validate-release.py scripts/validate-release-ci.py scripts/test-adapter-distribution.py scripts/test-npm-package-publication.py docs/changes/2026-05-23-release-process-contract`
- Expected observable result: The release gate can be rehearsed without publishing, and dry-run evidence shows the standing process does not claim the implementation itself is a release.
- Commit message: `M3: connect release gate and record dry-run rehearsal`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Gate changes could accidentally weaken existing release validation for `v0.1.4` or `v0.1.5`.
- Rollback/recovery:
  - Revert gate-command changes while retaining M1/M2 documentation and routing; rerun existing release validation tests to prove historical release behavior is preserved.

### M4. Lifecycle closeout and final validation

- Milestone state: closed
- Goal: Close the lifecycle evidence after implementation milestones are reviewed, explain the change, run final verification, and prepare PR handoff.
- Requirements: AC-REL-001 through AC-REL-014
- Files/components likely touched:
  - `docs/changes/2026-05-23-release-process-contract/explain-change.md`
  - `docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `docs/plans/2026-05-23-release-process-contract.md`
  - `docs/plan.md`
- Dependencies:
  - M1, M2, and M3 are closed after code-review and any required review-resolution.
  - Test spec exists and is current.
- Tests to add/update:
  - No new product tests; final validation reruns the approved command set and selected checks from implementation milestones.
- Implementation steps:
  - Run `explain-change`.
  - Run final `verify`.
  - Synchronize plan body, plan index, and change metadata before PR handoff.
  - Prepare PR handoff only after verify passes.
- Validation commands:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-23-release-process-contract`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-23-release-process-contract.md --path specs/release-process-contract.md --path specs/release-process-contract.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260523-release-process-contract.md --path docs/plans/2026-05-23-release-process-contract.md --path docs/changes/2026-05-23-release-process-contract/change.yaml --path docs/changes/2026-05-23-release-process-contract/review-log.md --path docs/changes/2026-05-23-release-process-contract/review-resolution.md`
  - `bash scripts/ci.sh --mode pr --base <base-sha> --head <head-sha>`
- Expected observable result: The plan and change metadata reflect the real completed milestones, review state, validation evidence, and PR readiness only after downstream gates pass.
- Commit message: `M4: close release process contract lifecycle`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Final closeout could drift between `docs/plan.md`, the plan body, and `change.yaml`.
- Rollback/recovery:
  - Keep plan active and fix stale lifecycle state before verify or PR handoff claims readiness.

## Validation plan

- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-23-release-process-contract`: validate formal review evidence and material-finding closeout.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-23-release-process-contract/change.yaml`: validate change metadata as plan, tests, and implementation evidence accumulate.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`: validate proposal, spec, test spec, architecture, ADR, plan, and change-local lifecycle artifacts.
- `python scripts/test-select-validation.py`: prove deterministic routing for release evidence paths.
- `python scripts/test-artifact-lifecycle-validator.py`: prove lifecycle/checklist behavior when release evidence support touches lifecycle validation.
- `python scripts/test-adapter-distribution.py`: preserve generated adapter release behavior.
- `python scripts/test-npm-package-publication.py`: preserve package preview and packed smoke behavior.
- `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.5`: rehearse the release gate without publishing.
- `python scripts/validate-release-ci.py --version v0.1.5`: prove release validation remains executable through the CI wrapper.
- `bash scripts/ci.sh --mode pr --base <base-sha> --head <head-sha>`: final PR-scope validation when implementation is complete.

## Risks and recovery

- Risk: The new `docs/releases/v<version>.md` evidence path could remain unregistered and produce `manual-routing-required`.
  - Recovery: Block M2 closeout until selector tests prove deterministic routing.
- Risk: Emergency deferral handling could become a broad gate bypass.
  - Recovery: Keep non-deferrable requirements in checklist/tests and fail evidence that defers registry verification, evidence creation, secret suppression, or recovery/follow-up recording.
- Risk: A release dry-run could be mistaken for a real release.
  - Recovery: Store rehearsal evidence under the change root and explicitly state that no package was published.
- Risk: Release evidence could leak secrets or machine-local data.
  - Recovery: Checklist and tests reject secret-bearing fields and machine-local path dependencies; final review verifies no such values were recorded.
- Risk: Existing release-specific behavior for `v0.1.4` or `v0.1.5` could regress.
  - Recovery: Preserve current release directory validation and run existing release/npm package tests before closeout.

## Dependencies

- Plan-review must approve this execution plan before implementation.
- A matching test spec must be created before implementation.
- Implementation milestones must be code-reviewed; material findings require review-resolution before the next milestone closes.
- Trusted publishing configuration is not required for this first slice; manual fallback remains documented and gated.
- No npm publication happens in this plan.

## Progress

- 2026-05-23: Plan created after accepted proposal, approved spec, approved architecture review, and accepted ADR.
- 2026-05-23: Test spec created at `specs/release-process-contract.test.md`; next stage is implement M1 after this artifact validates.
- 2026-05-23: M1 implementation started; scope is limited to release evidence README, index, and template/checklist surfaces.
- 2026-05-23: M1 added `docs/releases/README.md`, `docs/releases/index.md`, and `templates/release-evidence.md`; milestone validation passed and M1 is ready for code-review.
- 2026-05-23: M1 code-review completed clean-with-notes in `docs/changes/2026-05-23-release-process-contract/reviews/code-review-m1-r1.md`; M1 closed and next stage is implement M2.
- 2026-05-23: M2 implementation started; scope is limited to release evidence selector routing and lightweight lifecycle/checklist fixtures.
- 2026-05-23: M2 extended selector release-version inference for `docs/releases/v<version>.md`, routed release guidance files without package-version requirements, and added lightweight lifecycle/checklist tests for routine gate failures, emergency deferrals, non-deferrable registry verification, and forbidden release-evidence markers.
- 2026-05-23: M2 targeted validation passed and the milestone is ready for code-review.
- 2026-05-23: M2 code-review r1 found CR-M2-1: the flat release evidence path selects only `release.validate`, so the implemented lifecycle/checklist validation is not selected for `docs/releases/v<version>.md`. M2 is in review-resolution.
- 2026-05-23: CR-M2-1 resolved by routing flat release evidence files to `artifact_lifecycle.validate` and updating selector tests to assert the checklist route. M2 is ready for code-review re-review.
- 2026-05-23: M2 code-review r2 completed clean-with-notes in `docs/changes/2026-05-23-release-process-contract/reviews/code-review-m2-r2.md`; M2 closed and next stage is implement M3.
- 2026-05-23: M3 implementation started; scope is limited to release gate dry-run contract output, regression proof, and non-publishing rehearsal evidence.
- 2026-05-23: M3 added standing release-process gate rehearsal output to `scripts/release-verify.sh`, recorded non-publishing dry-run evidence in `docs/changes/2026-05-23-release-process-contract/release-process-dry-run.md`, and added regression coverage for dry-run gate output.
- 2026-05-23: M3 fixed the CI wrapper to rebuild historical adapter release archives from the recorded release source commit before validating current release metadata. This preserves `v0.1.5` release proof after later repository source changes.
- 2026-05-23: M3 targeted validation passed and the milestone is ready for code-review.
- 2026-05-23: M3 code-review completed clean-with-notes in `docs/changes/2026-05-23-release-process-contract/reviews/code-review-m3-r1.md`; M3 closed and next stage is implement M4.
- 2026-05-23: M4 recorded `docs/changes/2026-05-23-release-process-contract/explain-change.md`, refreshed lifecycle metadata, and prepared the milestone for code-review. Final verify and PR readiness remain downstream gates.
- 2026-05-23: M4 targeted validation passed and the milestone is ready for code-review.
- 2026-05-23: M4 code-review completed clean-with-notes in `docs/changes/2026-05-23-release-process-contract/reviews/code-review-m4-r1.md`; all implementation milestones are closed and next stage is verify.
- 2026-05-23: Final verify passed on committed branch state after registering `release-process-dry-run.md` as a routed change evidence class; next stage is PR handoff.
- 2026-05-23: PR #89 opened for hosted CI and human review.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-23 | Split implementation into evidence template, routing/checklist validation, release-gate rehearsal, and lifecycle closeout milestones. | Keeps the first slice reviewable and avoids publishing or broad automation before evidence shape stabilizes. | One large release automation milestone; documentation-only implementation without selector routing. |
| 2026-05-23 | Treat `docs/releases/v<version>.md` selector routing as an implementation milestone. | Architecture review and spec require deterministic release evidence; current release-version inference handles only version directories. | Leave routing to final verify and risk `manual-routing-required`. |

## Surprises and discoveries

- Current selector release-version inference handles `docs/releases/<version>/<file>` but not the new standing evidence file shape `docs/releases/v<version>.md`.
- `python scripts/validate-release-ci.py --version v0.1.5` rebuilt adapter archives from the current workspace even though `v0.1.5` metadata records source commit `5315a6d08b9d79e52d3276fd532b02f97c727e55`; later skill changes made the historical checksum comparison fail. M3 changed the wrapper to materialize the recorded source commit for archive generation while validating against the current release metadata.

## Validation notes

- 2026-05-23: Planning inspection only. Implementation validation has not run.
- 2026-05-23: Test-spec authoring validation passed through change metadata, review-artifact closeout, explicit-path artifact lifecycle, and `git diff --check`.
- 2026-05-23: M1 validation passed:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/release-process-contract.test.md --path docs/plans/2026-05-23-release-process-contract.md --path docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `git diff --check -- docs/releases/README.md docs/releases/index.md templates/release-evidence.md specs/release-process-contract.test.md docs/plans/2026-05-23-release-process-contract.md docs/changes/2026-05-23-release-process-contract`
- 2026-05-23: M1 code-review recorded clean-with-notes; no material findings and no review-resolution required.
- 2026-05-23: M2 validation passed:
  - `python scripts/test-select-validation.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/release-process-contract.test.md --path docs/plans/2026-05-23-release-process-contract.md --path docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `git diff --check -- scripts/validation_selection.py scripts/test-select-validation.py scripts/artifact_lifecycle_contracts.py scripts/artifact_lifecycle_validation.py scripts/test-artifact-lifecycle-validator.py specs/release-process-contract.test.md docs/changes/2026-05-23-release-process-contract`
- 2026-05-23: M2 handoff-state sync validation passed after updating `docs/plan.md`:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/release-process-contract.test.md --path docs/plans/2026-05-23-release-process-contract.md --path docs/plan.md --path docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `git diff --check -- scripts/validation_selection.py scripts/test-select-validation.py scripts/artifact_lifecycle_contracts.py scripts/artifact_lifecycle_validation.py scripts/test-artifact-lifecycle-validator.py specs/release-process-contract.test.md docs/plans/2026-05-23-release-process-contract.md docs/plan.md docs/changes/2026-05-23-release-process-contract`
- 2026-05-23: M2 code-review r1 recording validation passed:
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-23-release-process-contract`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-23-release-process-contract.md --path docs/plan.md --path docs/changes/2026-05-23-release-process-contract/change.yaml --path docs/changes/2026-05-23-release-process-contract/review-log.md --path docs/changes/2026-05-23-release-process-contract/review-resolution.md --path docs/changes/2026-05-23-release-process-contract/reviews/code-review-m2-r1.md`
- 2026-05-23: CR-M2-1 resolution validation passed:
  - `python scripts/select-validation.py --mode explicit --path docs/releases/v1.2.3.md`
  - `python scripts/select-validation.py --mode explicit --path docs/releases/README.md --path docs/releases/index.md`
  - `python scripts/select-validation.py --mode explicit --path docs/releases/v0.1.5/release.yaml`
  - `python scripts/test-select-validation.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
- 2026-05-23: CR-M2-1 active change checks passed except review closeout, which is expected to remain blocked until same-stage M2 re-review records a clean result:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/release-process-contract.test.md --path docs/plans/2026-05-23-release-process-contract.md --path docs/plan.md --path docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `git diff --check --`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-23-release-process-contract`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-23-release-process-contract.md --path docs/plan.md --path docs/changes/2026-05-23-release-process-contract/change.yaml --path docs/changes/2026-05-23-release-process-contract/review-log.md --path docs/changes/2026-05-23-release-process-contract/review-resolution.md --path docs/changes/2026-05-23-release-process-contract/reviews/code-review-m2-r1.md`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-23-release-process-contract` failed with expected pre-re-review blocker: `blocking review outcome requires same-stage re-review or explicit closeout`.
- 2026-05-23: M2 code-review r2 recorded clean-with-notes; no material findings and no review-resolution required.
- 2026-05-23: M2 code-review r2 closeout validation passed:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-23-release-process-contract`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/release-process-contract.test.md --path docs/plans/2026-05-23-release-process-contract.md --path docs/plan.md --path docs/changes/2026-05-23-release-process-contract/change.yaml --path docs/changes/2026-05-23-release-process-contract/review-log.md --path docs/changes/2026-05-23-release-process-contract/review-resolution.md --path docs/changes/2026-05-23-release-process-contract/reviews/code-review-m2-r1.md --path docs/changes/2026-05-23-release-process-contract/reviews/code-review-m2-r2.md`
  - `git diff --check --`
- 2026-05-23: M3 validation passed:
  - `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.5`
  - `python scripts/validate-release-ci.py --version v0.1.5`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/test-npm-package-publication.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/release-process-contract.test.md --path docs/plans/2026-05-23-release-process-contract.md --path docs/plan.md --path docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `git diff --check -- scripts/release-verify.sh scripts/validate-release.py scripts/validate-release-ci.py scripts/test-adapter-distribution.py scripts/test-npm-package-publication.py docs/plans/2026-05-23-release-process-contract.md docs/plan.md docs/changes/2026-05-23-release-process-contract`
- 2026-05-23: M3 code-review recorded clean-with-notes; no material findings and no review-resolution required.
- 2026-05-23: M4 validation passed:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-23-release-process-contract`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-23-release-process-contract.md --path specs/release-process-contract.md --path specs/release-process-contract.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260523-release-process-contract.md --path docs/plans/2026-05-23-release-process-contract.md --path docs/plan.md --path docs/changes/2026-05-23-release-process-contract/change.yaml --path docs/changes/2026-05-23-release-process-contract/explain-change.md --path docs/changes/2026-05-23-release-process-contract/review-log.md --path docs/changes/2026-05-23-release-process-contract/review-resolution.md`
  - `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-23-release-process-contract/change.yaml --path docs/changes/2026-05-23-release-process-contract/explain-change.md --path docs/plans/2026-05-23-release-process-contract.md --path docs/plan.md --path specs/release-process-contract.test.md`
  - `bash scripts/ci.sh --mode pr --base ef8e29ee1c1bad1fefb5d8c9c933a0b164e21325 --head HEAD`
  - `git diff --check -- docs/changes/2026-05-23-release-process-contract/change.yaml docs/changes/2026-05-23-release-process-contract/explain-change.md docs/plans/2026-05-23-release-process-contract.md docs/plan.md`
- 2026-05-23: M4 code-review recorded clean-with-notes; no material findings and no review-resolution required.
- 2026-05-23: Final verify validation passed:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-23-release-process-contract`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-23-release-process-contract/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
  - `bash scripts/ci.sh --mode pr --base HEAD~1 --head HEAD`
  - `python scripts/test-select-validation.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/test-npm-package-publication.py`
  - `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.5`
  - `python scripts/validate-release-ci.py --version v0.1.5`
  - `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped`
  - `git diff --check --`

## Outcome and retrospective

- Pending. This plan is active and not complete.

## Readiness

- See `Current Handoff Summary`.
- PR #89 is open for hosted CI and human review.
- Not ready for final lifecycle closeout or any npm publish operation. This change did not publish a package.
