# Compact Change Validation Metadata Plan

## Status

active

## Purpose / big picture

Implement the approved compact `change.yaml` validation metadata contract while keeping existing legacy metadata valid. The implementation must make compact metadata shorter and more structured without weakening validation evidence: commands and path sets stay reconstructable, failures stay explicit, review counts stay cross-checked, and old valid files continue to pass.

## Source artifacts

- Proposal: `docs/proposals/2026-05-21-compact-change-validation-metadata.md`
- Spec: `specs/compact-change-validation-metadata.md`
- Architecture: not-required; the approved spec scopes this to the existing change-metadata validator, schema, fixtures, and tests without a new cross-component runtime architecture.
- Test spec: `specs/compact-change-validation-metadata.test.md`

## Context and orientation

- `scripts/validate-change-metadata.py` owns the CLI, local YAML parsing, JSON-schema validation, and change-metadata semantic checks.
- `scripts/change_metadata_semantics.py` currently holds shared semantic checks for review metadata used by change metadata validation.
- `schemas/change.schema.json` is the formal schema surface for current change metadata.
- `scripts/test-change-metadata-validator.py` is the fixture-driven validator regression suite.
- `tests/fixtures/change-metadata/` contains current valid and invalid metadata fixtures.
- Review-artifact counts must be cross-checked against the existing review artifact parser behavior rather than copied as unchecked summary.
- Compact metadata is `schema_version: 2`; legacy metadata remains accepted and in-file mixed legacy/compact metadata is rejected.

## Non-goals

- Do not bulk-migrate historical `change.yaml` files.
- Do not standardize `change.validation-log.yaml` internals.
- Do not add CLI scaffolding that writes compact metadata.
- Do not change review-record, review-log, or review-resolution semantics.
- Do not change validation selector behavior, selected commands, command exit behavior, or failure detection.
- Do not make transcript files the only source of ordinary validation proof.

## Requirements covered

- R1-R7: M1.
- R8-R24, R51-R56, R63-R75, R83: M2.
- R25-R44: M3.
- R45-R50, R57-R62, R76-R82: M3.
- AC1-AC7: M1.
- AC8-AC13: M2 and M3.
- AC14-AC17: M2.
- AC18, AC22-AC24, AC27: M3.
- AC19-AC21, AC25-AC26: M2.

## Current Handoff Summary

- Current milestone: M3. Reconstruction, Summary Derivation, Review Counts, And Compactness Proof
- Current milestone state: closed
- Last reviewed milestone: M3
- Review status: code-review-m3-r2 clean-with-notes
- Remaining in-scope implementation milestones: none
- Next stage: verify
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: CI-maintenance fixed selected-CI routing for `tests/fixtures/change-metadata/**` and explain-change has been refreshed for that selector change, but verify must be rerun before branch readiness or PR handoff.

## Milestones

### M1. Compact Shape Recognition And Legacy Compatibility

- Milestone state: closed
- Goal: Add compact `schema_version: 2` recognition, keep legacy files valid, reject in-file mixed shape, and validate the compact top-level skeleton, bundle/event/result/count basics, and required failure details.
- Requirements: R1-R7, R25-R28, R33-R42, R57-R58, R62; AC1-AC7, AC24.
- Files/components likely touched:
  - `schemas/change.schema.json`
  - `scripts/validate-change-metadata.py`
  - `scripts/change_metadata_semantics.py`
  - `scripts/test-change-metadata-validator.py`
  - `tests/fixtures/change-metadata/**`
- Dependencies:
  - Approved spec status is settled before this plan relies on it.
  - Matching test spec must exist before implementation starts.
- Tests to add/update:
  - Legacy valid fixture still passes.
  - Basic compact valid fixture passes.
  - Missing compact required sections fail.
  - Mixed legacy validation list plus compact `validation_events` fails.
  - Undefined bundle reference fails.
  - Invalid result enum fails.
  - Non-integer counts fail.
  - `fail` and `blocked` events without details fail.
- Implementation steps:
  - Add compact shape detection through explicit `schema_version: 2`.
  - Preserve existing legacy schema and semantic checks for files without compact versioning.
  - Add compact top-level section validation for `path_vars`, `validation_bundles`, `validation_events`, and `validation_summary`.
  - Add bundle reference validation and result enum validation.
  - Add structured count integer validation.
  - Add required failure/blocker detail checks for failed or blocked events.
- Validation commands:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/valid-basic/change.yaml`
  - `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-valid/change.yaml`
  - `git diff --check --`
- Expected observable result: Existing valid legacy metadata still passes, compact skeleton metadata validates, and malformed compact shape failures are deterministic.
- Commit message: `M1: add compact metadata shape recognition`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Accidentally routing legacy files through compact-only validation could invalidate historical metadata.
  - JSON-schema changes could make current change files fail before compact semantics are ready.
- Rollback/recovery:
  - Revert compact schema/semantic additions and keep legacy schema behavior unchanged.
- Result:
  - Added M1 compact fixtures and validator regression coverage.
  - Confirmed the new compact tests failed before implementation because `schema_version: 2` files were still routed through the legacy schema.
  - Added explicit compact metadata validation branch for required compact sections, mixed-shape rejection, bundle definitions, event bundle references, result enum values, integer counts, and required failure details for `fail` and `blocked` events.
  - Preserved legacy schema and clean-review metadata semantics for non-compact files.
  - M1 implementation is complete and ready for code-review.
  - Code-review M1 R1 returned `clean-with-notes` with no material findings, so M1 is closed.

### M2. Path Variables, Lifecycle Stages, And Transcript References

- Milestone state: closed
- Goal: Implement deterministic path-variable expansion, slug derivation, doubled-brace escaping, path safety, lifecycle-stage ordering, first-exists filesystem checks, canonical spec/test-spec paths, and optional transcript reference validation.
- Requirements: R8-R24, R51-R56, R63-R75, R83; AC10-AC21, AC25-AC26.
- Files/components likely touched:
  - `scripts/validate-change-metadata.py`
  - `scripts/change_metadata_semantics.py`
  - `scripts/test-change-metadata-validator.py`
  - `tests/fixtures/change-metadata/**`
  - `tests/fixtures/review-artifacts/**` if compact fixtures need referenced review files
- Dependencies:
  - M1 compact shape validation is in place.
  - Fixture roots must include enough files for stage-derived existence checks to be deterministic.
- Tests to add/update:
  - `{var}` expansion and derived `slug` pass.
  - `{{` and `}}` resolve to literal braces.
  - Unmatched braces, nested interpolation, unknown variables, and `${var}` fail.
  - Recursive and unresolved path variables fail.
  - Absolute, home-directory, machine-local, hostname, credential, proxy, or secret-like values fail.
  - `specs/{slug}.md` and `specs/{slug}.test.md` pass when present.
  - Dated `specs/{change_id}.md` and `specs/{change_id}.test.md` fail.
  - Missing paths fail after first-exists stage and do not fail before that stage unless referenced.
  - Missing `lifecycle_stage` and unknown `lifecycle_stage` fail.
  - Optional transcript omitted passes; referenced missing transcript fails.
- Implementation steps:
  - Add a compact path-template parser with doubled-brace escaping and closed `{var}` interpolation syntax.
  - Derive `slug` from `path_vars.change_id` and reject conflicting `slug`.
  - Add path safety checks for resolved variables, event paths, bundle commands where relevant, and transcript references.
  - Add normalized lifecycle-stage enum and comparison order.
  - Add artifact-class first-exists mapping and optional/triggered artifact handling.
  - Add transcript reference syntax and target-existence validation without validating transcript internals.
- Validation commands:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-valid/change.yaml`
  - `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-invalid-unresolved-var/change.yaml`
  - `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-invalid-summary-conflict/change.yaml`
  - `git diff --check --`
- Expected observable result: Compact files expand paths deterministically, reject unsafe or ambiguous paths, enforce lifecycle-derived existence checks, and keep transcript references non-load-bearing.
- Commit message: `M2: add compact path and lifecycle validation`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Filesystem existence checks could be too eager and reject artifacts that are not yet stage-required.
  - Path safety checks could be too loose and allow machine-local or credential-bearing paths.
- Rollback/recovery:
  - Disable compact path/lifecycle validation while keeping M1 legacy-compatible shape recognition intact, or revert M2 as a standalone patch.
- Result:
  - Added M2 compact fixtures and helper coverage for `change_id` slug derivation, `{var}` interpolation, doubled-brace escaping, unsafe path detection, lifecycle-stage enums, first-exists checks, canonical `specs/{slug}.md` and `specs/{slug}.test.md` paths, per-path opt-out rejection, and transcript reference existence.
  - Confirmed the new M2 invalid fixtures failed before implementation because compact validation did not yet inspect path variables, lifecycle-stage values, artifact existence, canonical durable-contract paths, or transcript references.
  - Added deterministic compact path-variable resolution, derived `slug`, recursive/unresolved variable rejection, closed interpolation syntax, repo-relative safety checks, lifecycle-stage ordering, stage-derived first-exists checks, event path validation, and optional transcript-reference validation without validating transcript internals.
  - Preserved the legacy metadata path and the M1 compact shape checks.
  - M2 implementation is complete and ready for code-review.
  - Code-review M2 R1 found CVM-M2-CR1; M2 requires review-resolution and a same-milestone fix before re-review.
  - Review-resolution accepted CVM-M2-CR1 and added bundle-command safety validation, unsafe command fixtures, and targeted validation evidence. M2 is ready for code-review rerun.
  - Code-review M2 R2 returned `clean-with-notes` with no material findings, so M2 is closed.

### M3. Reconstruction, Summary Derivation, Review Counts, And Compactness Proof

- Milestone state: closed
- Goal: Implement exact path-expanding command reconstruction checks, stored-summary consistency, review-artifact count cross-checking, duplicate-stage rejection, skipped/not-run blocker handling, and representative compactness proof.
- Requirements: R29-R32, R43-R50, R59-R62, R76-R82; AC8-AC9, AC18, AC22-AC24, AC27.
- Files/components likely touched:
  - `scripts/validate-change-metadata.py`
  - `scripts/change_metadata_semantics.py`
  - `scripts/review_artifact_validation.py` only if an existing parser helper must be exposed without behavior changes
  - `scripts/test-change-metadata-validator.py`
  - `tests/fixtures/change-metadata/**`
  - `tests/fixtures/review-artifacts/**`
- Dependencies:
  - M1 compact event and bundle validation is in place.
  - M2 path expansion and lifecycle-stage validation is in place.
  - Existing review-artifact parser can be invoked or imported without changing review-record semantics.
- Tests to add/update:
  - Path-expanding bundles reconstruct exact accumulated path sets in event order.
  - Omitted `paths_added` is accepted only when the resolved path set did not change.
  - Summary `all_passed: true` with any non-pass event fails.
  - `stages_validated` differs from pass-event list fails.
  - Duplicate `validation_events[].stage` values fail.
  - `fail`, `blocked`, required `not-run`, and unaccepted `skipped` events require blocker representation.
  - Skipped event with accepted owner decision is excluded from `stages_validated` and validates.
  - `final_counts` and event counts agree with review-artifact parser output when referenced artifacts exist.
  - Compact representative high-rerun fixture is at least 30% smaller on the common-read surface after reconstruction passes.
- Implementation steps:
  - Implement per-bundle `paths_added` accumulation and exact reconstructed path-set checks.
  - Validate summary fields as derived data from `validation_events`.
  - Bind structured review counts to review-artifact parser output when referenced artifacts exist.
  - Add compactness measurement test using a representative high-rerun legacy/compact fixture pair.
  - Confirm no compact validation path executes validation bundles or changes selected validation commands.
- Validation commands:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-valid/change.yaml`
  - `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-invalid-summary-conflict/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-compact-change-validation-metadata`
  - `git diff --check --`
- Expected observable result: Compact metadata preserves exact validation evidence through reconstruction, rejects summary/count drift, and proves material common-read size reduction without evidence loss.
- Commit message: `M3: add compact metadata evidence checks`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Count cross-checks could create cycles or duplicate review-artifact parser behavior.
  - Compactness proof could become brittle if fixture formatting changes.
- Rollback/recovery:
  - Keep M1/M2 validation in place and temporarily reject compact files with cross-check-dependent fields until the count/reconstruction bug is fixed, or revert M3 as a standalone patch.
- Result:
  - Added M3 compact fixtures and tests for path-expanding bundle reconstruction, summary derivation, duplicate stage rejection, skipped/not-run blocker handling, review-artifact count cross-checking, compactness measurement, and no-execution behavior for bundle commands.
  - Confirmed the M3 tests failed before implementation because summary drift, duplicate stages, missing path deltas, review-count mismatches, and compactness helper behavior were not yet implemented.
  - Added deterministic accumulated path-set reconstruction for path-expanding bundles declared with `expands_with: validation_events[].paths_added.<bundle>`.
  - Added stored-summary validation for `all_passed`, pass-only `stages_validated`, `final_counts`, `open_validation_blockers`, duplicate event stages, skipped owner decisions, and blocker requirements for non-pass events.
  - Added review-artifact count cross-checking through the existing review-artifact parser when referenced review artifacts exist.
  - Added compactness measurement helper proof and confirmed compact validation does not execute bundle commands while validating metadata.
  - Preserved legacy metadata compatibility and the M1/M2 compact path/lifecycle validation behavior.
  - M3 implementation is complete and ready for code-review.
  - Code-review M3 R1 found CVM-M3-CR1, CVM-M3-CR2, and CVM-M3-CR3; M3 requires review-resolution and same-milestone fixes before re-review.
  - Review-resolution accepted and resolved CVM-M3-CR1, CVM-M3-CR2, and CVM-M3-CR3 with exact blocker derivation, representative reconstruction-gated compactness fixtures, and an effective no-execution sentinel command. M3 is ready for code-review rerun.
  - Code-review M3 R2 returned `clean-with-notes` with no material findings, so M3 is closed.

## Validation plan

- `python scripts/test-change-metadata-validator.py`: primary compact and legacy metadata regression suite.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml`: validates this change metadata while the plan evolves.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-compact-change-validation-metadata`: validates recorded review evidence and review-resolution closeout.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-21-compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.md --path docs/plans/2026-05-21-compact-change-validation-metadata.md --path docs/plan.md --path docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml --path docs/changes/2026-05-21-compact-change-validation-metadata/review-log.md --path docs/changes/2026-05-21-compact-change-validation-metadata/review-resolution.md`: validates lifecycle-managed artifact state.
- `python scripts/test-select-validation.py`: selector regression if changed validator, schema, fixtures, or plan paths alter validation selection behavior.
- `bash scripts/ci.sh --mode explicit --path scripts/validate-change-metadata.py --path scripts/change_metadata_semantics.py --path scripts/test-change-metadata-validator.py --path schemas/change.schema.json --path tests/fixtures/change-metadata --path docs/plans/2026-05-21-compact-change-validation-metadata.md --path docs/plan.md --path docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml`: selected CI after implementation milestones are complete.
- `git diff --check --`: whitespace and patch hygiene.

## Risks and recovery

- Risk: Compact support accidentally invalidates historical legacy files.
  - Recovery: Keep version-branching tests first and revert compact branch changes if legacy fixtures fail.
- Risk: Path-variable validation creates false positives for not-yet-created artifacts.
  - Recovery: Tighten first-exists mapping and optional/triggered artifact rules to the approved spec, with focused fixtures for pre-stage and post-stage behavior.
- Risk: Review-artifact count cross-checking duplicates parser behavior and drifts.
  - Recovery: Reuse or expose existing parser output instead of reimplementing count logic.
- Risk: Command reconstruction becomes best-effort rather than exact.
  - Recovery: Block compact validation until path-expanding bundles produce deterministic accumulated path sets.
- Risk: Compactness proof incentivizes evidence loss.
  - Recovery: Run reconstruction and count-preservation checks before evaluating the 30% reduction threshold.

## Dependencies

- Spec status must be approved before implementation relies on it.
- Plan-review must approve this plan before test-spec and implementation.
- Matching test spec must be written and reviewed before implementation begins.
- Existing review-artifact parser behavior remains authoritative for review counts.
- No new third-party dependency is expected.

## Progress

- 2026-05-21: Plan created after `spec-review-r2` approved the revised compact metadata spec; spec status normalized to `approved`.
- 2026-05-21: Plan-review R1 approved the plan with no material findings.
- 2026-05-21: Test spec authored at `specs/compact-change-validation-metadata.test.md` and approved by maintainer; next stage is implement M1.
- 2026-05-21: M1 tests were added first and failed against the legacy-only validator path; implementation then added compact shape recognition and M1 semantic checks.
- 2026-05-21: M1 moved to `review-requested` after targeted validation passed.
- 2026-05-21: Code-review M1 R1 recorded `clean-with-notes`; M1 closed and next stage is implement M2.
- 2026-05-21: M2 tests were added first and failed against the M1-only compact validator path; implementation then added path-variable, lifecycle-stage, first-exists, canonical durable-contract path, and transcript-reference validation.
- 2026-05-21: M2 moved to `review-requested` after targeted validation passed.
- 2026-05-21: Code-review M2 R1 recorded CVM-M2-CR1; M2 moved to `resolution-needed`.
- 2026-05-21: Review-resolution for CVM-M2-CR1 added unsafe bundle-command validation and returned M2 to `review-requested`.
- 2026-05-21: Code-review M2 R2 recorded `clean-with-notes`; M2 closed and next stage is implement M3.
- 2026-05-21: M3 tests were added first and failed against the M2 validator path; implementation then added reconstruction, summary derivation, review-count cross-checking, compactness proof, and no-execution coverage.
- 2026-05-21: M3 moved to `review-requested` after targeted validation passed.
- 2026-05-21: Code-review M3 R1 recorded CVM-M3-CR1, CVM-M3-CR2, and CVM-M3-CR3; M3 moved to `resolution-needed`.
- 2026-05-21: Review-resolution for CVM-M3-CR1, CVM-M3-CR2, and CVM-M3-CR3 added exact blocker derivation, representative compactness fixture proof, and an effective no-execution sentinel test, then returned M3 to `review-requested`.
- 2026-05-21: Code-review M3 R2 recorded `clean-with-notes`; M3 is closed and the next stage is explain-change.
- 2026-05-22: Explain-change recorded the rationale for the compact metadata branch and handed off to verify.
- 2026-05-22: Verify ran focused validator proof and broad smoke, but selected CI blocked because the validation selector does not classify the new `tests/fixtures/change-metadata/**` fixture paths. Next stage is ci-maintenance.
- 2026-05-22: CI-maintenance added selected-CI routing for change-metadata fixture paths and proved the full branch changed-file selected CI command now passes. Next stage is explain-change refresh.
- 2026-05-22: Explain-change was refreshed after ci-maintenance to include selector-routing rationale and selected-CI evidence. Next stage is verify rerun.
- 2026-05-22: Verify rerun found selected CI still blocked on title-case lifecycle headings in the accepted proposal. The lifecycle validator now matches lifecycle section headings case-insensitively and includes a title-case proposal regression test.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-21 | Split implementation into shape, path/lifecycle, and evidence-consistency milestones. | The approved spec has separable risk areas: version compatibility, path safety/existence, and audit reconstruction/count consistency. | One large validator milestone that would hide reviewable risk. |
| 2026-05-21 | Treat architecture as not required for this slice. | The spec routes work through existing validator, schema, fixtures, and tests without new runtime components or deployment boundaries. | Add a standalone architecture artifact for a bounded validator/schema change. |
| 2026-05-21 | Require test spec before implementation. | The change is schema and validator behavior with many failure cases; implementation should be fixture-driven. | Implement directly from the spec and backfill tests. |

## Surprises and discoveries

- 2026-05-21: The early M2 validation command list included `compact-invalid-summary-conflict`, but stored-summary derivation and blocker consistency are explicitly assigned to M3 by this plan and the test spec. M2 validation covers the named M2 invalid fixtures through `scripts/test-change-metadata-validator.py` and direct unresolved-variable expected-failure proof.

## Validation notes

- 2026-05-21: `git diff --check --` passed after plan creation.
- 2026-05-21: `python scripts/validate-change-metadata.py docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml` passed after plan creation.
- 2026-05-21: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-compact-change-validation-metadata` passed after plan creation with `reviews=3`, `findings=3`, `log_entries=3`, and `resolution_entries=3`.
- 2026-05-21: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-21-compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.md --path docs/plans/2026-05-21-compact-change-validation-metadata.md --path docs/plan.md --path docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml --path docs/changes/2026-05-21-compact-change-validation-metadata/review-log.md --path docs/changes/2026-05-21-compact-change-validation-metadata/review-resolution.md` passed after plan creation.
- 2026-05-21: `git diff --check --`, `python scripts/validate-change-metadata.py docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-compact-change-validation-metadata`, and `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-21-compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.test.md --path docs/plans/2026-05-21-compact-change-validation-metadata.md --path docs/plan.md --path docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml --path docs/changes/2026-05-21-compact-change-validation-metadata/review-log.md --path docs/changes/2026-05-21-compact-change-validation-metadata/review-resolution.md` passed after test-spec authoring.
- 2026-05-21: `python scripts/test-change-metadata-validator.py` passed for M1 after initially failing on compact fixtures before implementation.
- 2026-05-21: `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/valid-basic/change.yaml` passed for M1.
- 2026-05-21: `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-valid/change.yaml` passed for M1.
- 2026-05-21: `git diff --check --` passed for M1.
- 2026-05-21: `python scripts/validate-change-metadata.py docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-compact-change-validation-metadata`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-21-compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.test.md --path docs/plans/2026-05-21-compact-change-validation-metadata.md --path docs/plan.md --path docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml --path docs/changes/2026-05-21-compact-change-validation-metadata/review-log.md --path docs/changes/2026-05-21-compact-change-validation-metadata/review-resolution.md`, and `python -m py_compile scripts/validate-change-metadata.py scripts/change_metadata_semantics.py` passed for M1.
- 2026-05-21: `python scripts/test-change-metadata-validator.py` passed for M2 after initially failing on M2 compact fixtures before implementation.
- 2026-05-21: `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-valid/change.yaml` passed for M2.
- 2026-05-21: `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/valid-basic/change.yaml` passed for M2.
- 2026-05-21: `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-invalid-unresolved-var/change.yaml` failed as expected for M2 with `path_vars.change_root: unknown variable 'missing'`.
- 2026-05-21: `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-invalid-transcript-missing/change.yaml` failed as expected for M2 with a missing transcript reference.
- 2026-05-21: `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-invalid-lifecycle-stage/change.yaml` failed as expected for M2 with an unknown lifecycle stage.
- 2026-05-21: `python -m py_compile scripts/validate-change-metadata.py scripts/change_metadata_semantics.py` passed for M2.
- 2026-05-21: `git diff --check --` passed for M2.
- 2026-05-21: `git diff --check --`, `python scripts/validate-change-metadata.py docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml`, `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-21-compact-change-validation-metadata`, and `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-21-compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.test.md --path docs/plans/2026-05-21-compact-change-validation-metadata.md --path docs/plan.md --path docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml --path docs/changes/2026-05-21-compact-change-validation-metadata/review-log.md --path docs/changes/2026-05-21-compact-change-validation-metadata/review-resolution.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m1-r1.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m2-r1.md` passed after code-review M2 R1 recording. Review-artifact closeout is intentionally not run as passing because CVM-M2-CR1 is open.
- 2026-05-21: `python scripts/test-change-metadata-validator.py` passed after CVM-M2-CR1 resolution.
- 2026-05-21: `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-valid/change.yaml` passed after CVM-M2-CR1 resolution.
- 2026-05-21: `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/valid-basic/change.yaml` passed after CVM-M2-CR1 resolution.
- 2026-05-21: Direct expected-failure checks for `compact-invalid-unsafe-bundle-command-local-path`, `compact-invalid-unsafe-bundle-command-credential-url`, and `compact-invalid-unsafe-bundle-command-secret` failed with stable unsafe bundle-command diagnostics after CVM-M2-CR1 resolution.
- 2026-05-21: `python -m py_compile scripts/validate-change-metadata.py scripts/change_metadata_semantics.py` passed after CVM-M2-CR1 resolution.
- 2026-05-21: `git diff --check --` passed after CVM-M2-CR1 resolution.
- 2026-05-21: `python scripts/validate-change-metadata.py docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-compact-change-validation-metadata`, and `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-21-compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.test.md --path docs/plans/2026-05-21-compact-change-validation-metadata.md --path docs/plan.md --path docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml --path docs/changes/2026-05-21-compact-change-validation-metadata/review-log.md --path docs/changes/2026-05-21-compact-change-validation-metadata/review-resolution.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m1-r1.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m2-r1.md` passed after CVM-M2-CR1 resolution evidence was recorded.
- 2026-05-21: `git diff --check --`, `python scripts/validate-change-metadata.py docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-compact-change-validation-metadata`, and `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-21-compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.test.md --path docs/plans/2026-05-21-compact-change-validation-metadata.md --path docs/plan.md --path docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml --path docs/changes/2026-05-21-compact-change-validation-metadata/review-log.md --path docs/changes/2026-05-21-compact-change-validation-metadata/review-resolution.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m1-r1.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m2-r1.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m2-r2.md` passed after code-review M2 R2 recording.
- 2026-05-21: `python scripts/test-change-metadata-validator.py` passed for M3 after initially failing on M3 compact fixtures and helper tests before implementation.
- 2026-05-21: `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-valid/change.yaml` passed for M3.
- 2026-05-21: `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-invalid-summary-conflict/change.yaml` failed as expected for M3 with summary conflict diagnostics.
- 2026-05-21: `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-valid-review-counts/change.yaml` passed for M3.
- 2026-05-21: `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-invalid-review-counts/change.yaml` failed as expected for M3 with review-count mismatch diagnostics.
- 2026-05-21: `python -m py_compile scripts/validate-change-metadata.py scripts/change_metadata_semantics.py scripts/review_artifact_validation.py` passed for M3.
- 2026-05-21: `git diff --check --`, `python scripts/validate-change-metadata.py docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-compact-change-validation-metadata`, and `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-21-compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.test.md --path docs/plans/2026-05-21-compact-change-validation-metadata.md --path docs/plan.md --path docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml --path docs/changes/2026-05-21-compact-change-validation-metadata/review-log.md --path docs/changes/2026-05-21-compact-change-validation-metadata/review-resolution.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m1-r1.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m2-r1.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m2-r2.md` passed for M3 before handoff recording.
- 2026-05-21: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-21-compact-change-validation-metadata`, `git diff --check --`, `python scripts/validate-change-metadata.py docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml`, and `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-21-compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.test.md --path docs/plans/2026-05-21-compact-change-validation-metadata.md --path docs/plan.md --path docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml --path docs/changes/2026-05-21-compact-change-validation-metadata/review-log.md --path docs/changes/2026-05-21-compact-change-validation-metadata/review-resolution.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m1-r1.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m2-r1.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m2-r2.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m3-r1.md` passed after code-review M3 R1 recording.
- 2026-05-21: `python scripts/test-change-metadata-validator.py` passed after CVM-M3-CR1, CVM-M3-CR2, and CVM-M3-CR3 resolution.
- 2026-05-21: `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-invalid-extra-summary-blocker/change.yaml` failed as expected with an extra-blocker diagnostic after CVM-M3-CR1 resolution.
- 2026-05-21: `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compactness-representative-compact/change.yaml` and `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compactness-representative-legacy/change.yaml` passed after CVM-M3-CR2 resolution.
- 2026-05-21: `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-valid/change.yaml`, `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-valid-review-counts/change.yaml`, `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-invalid-summary-conflict/change.yaml`, and `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-invalid-review-counts/change.yaml` passed or failed as expected after M3 review-resolution fixes.
- 2026-05-21: `python -m py_compile scripts/validate-change-metadata.py scripts/change_metadata_semantics.py scripts/review_artifact_validation.py` passed after M3 review-resolution fixes.
- 2026-05-21: `git diff --check --`, `python scripts/validate-change-metadata.py docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-compact-change-validation-metadata`, and `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-21-compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.test.md --path docs/plans/2026-05-21-compact-change-validation-metadata.md --path docs/plan.md --path docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml --path docs/changes/2026-05-21-compact-change-validation-metadata/review-log.md --path docs/changes/2026-05-21-compact-change-validation-metadata/review-resolution.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m1-r1.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m2-r1.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m2-r2.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m3-r1.md` passed after M3 review-resolution fixes.
- 2026-05-21: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-compact-change-validation-metadata`, `git diff --check --`, `python scripts/validate-change-metadata.py docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml`, and `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-21-compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.test.md --path docs/plans/2026-05-21-compact-change-validation-metadata.md --path docs/plan.md --path docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml --path docs/changes/2026-05-21-compact-change-validation-metadata/review-log.md --path docs/changes/2026-05-21-compact-change-validation-metadata/review-resolution.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m1-r1.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m2-r1.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m2-r2.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m3-r1.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m3-r2.md` passed after code-review M3 R2 recording.
- 2026-05-22: `git diff --check --`, `python scripts/validate-change-metadata.py docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-compact-change-validation-metadata`, and `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-21-compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.test.md --path docs/plans/2026-05-21-compact-change-validation-metadata.md --path docs/plan.md --path docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml --path docs/changes/2026-05-21-compact-change-validation-metadata/review-log.md --path docs/changes/2026-05-21-compact-change-validation-metadata/review-resolution.md --path docs/changes/2026-05-21-compact-change-validation-metadata/explain-change.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m1-r1.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m2-r1.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m2-r2.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m3-r1.md --path docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m3-r2.md` passed after explain-change recording.
- 2026-05-22: `python scripts/test-change-metadata-validator.py`, `python -m py_compile scripts/validate-change-metadata.py scripts/change_metadata_semantics.py scripts/review_artifact_validation.py`, direct compact valid/legacy valid fixture checks, direct expected-failure compact summary/review-count/extra-blocker checks, direct representative compactness fixture checks, `git diff --check --`, `python scripts/test-select-validation.py`, active change metadata validation, review-artifact closeout validation, and lifecycle explicit-path validation passed during verify.
- 2026-05-22: `bash scripts/ci.sh --mode explicit --path scripts/validate-change-metadata.py --path scripts/change_metadata_semantics.py --path scripts/test-change-metadata-validator.py --path schemas/change.schema.json --path tests/fixtures/change-metadata --path docs/plans/2026-05-21-compact-change-validation-metadata.md --path docs/plan.md --path docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml` failed with selector status blocked because `tests/fixtures/change-metadata` is unclassified.
- 2026-05-22: Selected CI rerun with concrete branch changed files also failed with selector status blocked because `tests/fixtures/change-metadata/**` files are unclassified by the v1 selector.
- 2026-05-22: `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped` passed; artifact lifecycle emitted unrelated baseline warnings for older proposal files.
- 2026-05-22: `python scripts/test-select-validation.py` passed after adding `change-metadata-fixtures` routing.
- 2026-05-22: `python scripts/select-validation.py --mode explicit --path tests/fixtures/change-metadata/compact-valid/change.yaml --json` classified the path as `change-metadata-fixtures` and selected `change_metadata.regression`.
- 2026-05-22: `bash scripts/ci.sh --mode explicit --path scripts/validate-change-metadata.py --path scripts/change_metadata_semantics.py --path scripts/test-change-metadata-validator.py --path schemas/change.schema.json --path tests/fixtures/change-metadata/compact-valid/change.yaml --path docs/plans/2026-05-21-compact-change-validation-metadata.md --path docs/plan.md --path docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml` passed after selector routing fix.
- 2026-05-22: `bash scripts/ci.sh --mode explicit <branch-changed-files>` passed after selector routing fix, selecting review artifact validation, artifact lifecycle validation, change metadata regression, and change metadata validation.
- 2026-05-22: Clean-HEAD verify rerun found the representative selected CI command still failed in `artifact_lifecycle.validate` because `docs/proposals/2026-05-21-compact-change-validation-metadata.md` uses title-case `Recommended Direction`.
- 2026-05-22: `python scripts/test-artifact-lifecycle-validator.py` passed after adding title-case lifecycle heading support.
- 2026-05-22: `python -m py_compile scripts/artifact_lifecycle_contracts.py scripts/artifact_lifecycle_validation.py scripts/test-artifact-lifecycle-validator.py` passed after adding title-case lifecycle heading support.

## Outcome and retrospective

- Implementation milestones M1, M2, and M3 are closed after code review, ci-maintenance fixed selected-CI fixture routing, and explain-change has been refreshed. Verify must rerun before branch readiness or PR handoff can be claimed.

## Readiness

- See `Current Handoff Summary`.
- Ready for `verify`; not ready for PR handoff.
