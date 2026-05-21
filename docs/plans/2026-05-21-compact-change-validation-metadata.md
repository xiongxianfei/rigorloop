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

- Current milestone: M1. Compact Shape Recognition And Legacy Compatibility
- Current milestone state: review-requested
- Last reviewed milestone: none
- Review status: M1 implementation complete; code-review pending
- Remaining in-scope implementation milestones: M2, M3
- Next stage: code-review M1
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: M1 is awaiting code-review, M2 and M3 are not implemented or reviewed, final explain-change and verify have not run, and PR handoff is not prepared.

## Milestones

### M1. Compact Shape Recognition And Legacy Compatibility

- Milestone state: review-requested
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

### M2. Path Variables, Lifecycle Stages, And Transcript References

- Milestone state: planned
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

### M3. Reconstruction, Summary Derivation, Review Counts, And Compactness Proof

- Milestone state: planned
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

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-21 | Split implementation into shape, path/lifecycle, and evidence-consistency milestones. | The approved spec has separable risk areas: version compatibility, path safety/existence, and audit reconstruction/count consistency. | One large validator milestone that would hide reviewable risk. |
| 2026-05-21 | Treat architecture as not required for this slice. | The spec routes work through existing validator, schema, fixtures, and tests without new runtime components or deployment boundaries. | Add a standalone architecture artifact for a bounded validator/schema change. |
| 2026-05-21 | Require test spec before implementation. | The change is schema and validator behavior with many failure cases; implementation should be fixture-driven. | Implement directly from the spec and backfill tests. |

## Surprises and discoveries

- none yet

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

## Outcome and retrospective

- Pending until all implementation milestones, reviews, review-resolution when triggered, explain-change, verify, and PR handoff are complete.

## Readiness

- See `Current Handoff Summary`.
- Ready for `code-review M1`; not ready for M2, final closeout, verify, or PR handoff.
