# Test and CI Speed Optimization M1-M4 Explain Change

## Summary

M1 adds the metadata and command-line contract needed before the wrapper can safely run selected checks in parallel. The catalog now records explicit `parallel_safe` metadata and exposes an `is_parallel_safe_check` helper. The wrapper now accepts `--jobs`, `--timeout`, `--fail-fast`, and `--verbose`, rejects invalid numeric flag values before selector invocation, and keeps existing selector arguments unchanged.

M2 replaces ad hoc selected-check execution with a deterministic sequential result model. Selected checks now run through captured stdout/stderr buffers, produce stable summary rows, show failed logs after the summary, hide successful logs unless `--verbose` is supplied, enforce per-check timeouts, and distinguish ordinary nonzero exits, signal kills, timed-out checks, and unavailable commands.

M3 adds bounded scheduling for reviewed parallel-safe checks. Consecutive allowlisted checks can run concurrently up to `--jobs`, non-allowlisted checks run alone, default execution continues launching queued work after failures, and `--fail-fast` stops only queued checks that have not started while preserving already-started results.

M4 documents the wrapper execution flags in contributor guidance, adds a contract test that hosted CI remains thin and matrix-free, leaves `.github/workflows/ci.yml` unchanged because it already delegates to `scripts/ci.sh`, and records final six-script plus broad-smoke proof.

## Decision Trail

- Proposal: `docs/proposals/2026-05-04-test-and-ci-speed-optimization.md`
- Spec: `specs/test-and-ci-speed-optimization.md`
- Test spec: `specs/test-and-ci-speed-optimization.test.md`
- Plan: `docs/plans/2026-05-04-test-and-ci-speed-optimization.md`
- Milestones: M1, catalog metadata and wrapper flag contract; M2, deterministic sequential runner and failure attribution; M3, bounded parallel scheduling and fail-fast; M4, contributor guidance and final proof

## Diff Rationale

| File or area | Change | Reason | Evidence |
| --- | --- | --- | --- |
| `scripts/validation_selection.py` | adds `parallel_safe` catalog metadata and marks only the six reviewed regression check IDs safe | satisfies the allowlist boundary without changing selector routing or command identities | `python scripts/test-select-validation.py` |
| `scripts/ci.sh` | parses `--jobs`, `--timeout`, `--fail-fast`, and `--verbose`; adds default timeout and CPU-minus-one default job helper; adds the captured-result runner and bounded scheduler | establishes the wrapper-level invocation contract, deterministic summaries, output capture, timeout handling, failure attribution, parallel-safe bounded execution, non-allowlisted serial execution, and fail-fast queued cancellation | `python scripts/test-select-validation.py` |
| `scripts/test-select-validation.py` | adds M1 regression tests for catalog metadata and wrapper flags, M2 regression tests for sequential reporting, M3 regression tests for concurrent scheduling, and M4 contract tests for workflow guidance plus hosted CI boundary behavior | proves the new contract before production code and guards selector/wrapper and workflow-boundary compatibility | red then green `python scripts/test-select-validation.py` |
| `docs/workflows.md` | documents `--jobs`, `--jobs 1`, `--timeout`, `--fail-fast`, `--verbose`, and the matrix-free hosted-CI boundary | makes the completed wrapper behavior discoverable without implying caching, matrix fan-out, or hosted-CI redesign | `python scripts/test-select-validation.py` |
| `.github/workflows/ci.yml` | unchanged | inspection and T17 proof show the workflow already delegates to `scripts/ci.sh` for PR and main modes without matrix fan-out, hardcoded check IDs, caching, distributed execution, or sandbox setup | `python scripts/test-select-validation.py` |
| `docs/changes/2026-05-04-test-and-ci-speed-optimization/` | creates the baseline change-local pack | satisfies the non-trivial change evidence contract | change metadata validation |
| `docs/plans/2026-05-04-test-and-ci-speed-optimization.md` and `docs/plan.md` | records M1-M4 progress and validation evidence | keeps the active plan and plan index current during implementation | selector-selected validation |

## Same-Slice Completeness

- In scope through M4: M1 requirements `R2`, `R2a`, `R2b`, `R2c`, `R3`, `R3a`, `R3b`, `R4`, `R4c`, `R4d`, `R5`, `R7`, `R10`, `R16`, `R16a`, and `R20`; M2 requirements `R1`, `R2a`, `R3c`, `R3d`, `R3e`, `R6`, `R8`-`R14`, `R16`, `R16a`, and `R20`; M3 requirements `R2c`, `R2d`, `R4a`, `R4b`, `R6`, `R7`-`R7c`, `R8a`, `R9a`, `R9c`, `R10b`, `R11`, `R12`, and `R20`; M4 requirements `R9`, `R10`, `R15`, `R17`-`R20`, and acceptance criteria `AC1`-`AC9`.
- Out of scope through M4: hosted CI matrix fan-out, caching, distributed execution, sandboxing, persistent result caching, and per-check resource isolation.
- `.github/workflows/ci.yml` is intentionally unchanged in M4 because the tracked workflow already calls `scripts/ci.sh --mode pr` and `scripts/ci.sh --mode main` without duplicating selector path classification, stable check lists, or matrix axes.
- `docs/architecture/system/architecture.md` is intentionally unchanged because M1-M4 preserve the existing selector, catalog, wrapper, and hosted CI boundaries without introducing a new helper module or parser boundary.
- `specs/test-and-ci-speed-optimization.test.md` is intentionally unchanged in M3 because it already contained the required `T4`, `T6`, `T7`, `T8`, and `T9` scheduler cases.
- `specs/test-and-ci-speed-optimization.test.md` is intentionally unchanged in M4 because it already contained the required `T15`-`T19` final proof, hosted-CI boundary, and safety-evidence cases.

## Parallel-Safety Evidence

The initial allowlist marks only reviewed regression scripts. Source inspection used targeted searches for writes, temporary directories, subprocess calls, Git mutation, ports, locks, and file deletion. The observed writes are either absent or scoped to temporary fixture directories created by the test process.

| Check ID | Command | Safety evidence |
| --- | --- | --- |
| `adapters.regression` | `python scripts/test-adapter-distribution.py` | Writes fixture adapter and release outputs under `tempfile.TemporaryDirectory()` roots; no fixed ports, shared lockfiles, or global Git configuration. |
| `artifact_lifecycle.regression` | `python scripts/test-artifact-lifecycle-validator.py` | Copies fixtures into `tempfile.mkdtemp()` roots and mutates only those fixture repos; Git config is local to temporary repositories. |
| `change_metadata.regression` | `python scripts/test-change-metadata-validator.py` | Reads repository fixtures and invokes the validator; no tracked-path writes or shared external resources. |
| `review_artifacts.regression` | `python scripts/test-review-artifact-validator.py` | Copies and mutates review fixtures only under `tempfile.mkdtemp()` roots; no tracked-path writes or shared external resources. |
| `selector.regression` | `python scripts/test-select-validation.py` | Uses temporary repositories, selector fixtures, and process-unique temp traces; no fixed ports, shared lockfiles, or global Git configuration. |
| `skills.regression` | `python scripts/test-skill-validator.py` | Reads skill fixtures and invokes the validator; no tracked-path writes or shared external resources. |

## Validation Evidence

- `python scripts/test-select-validation.py`
  - First run: expected failure before M1 implementation.
  - Second run: passed after adding catalog metadata and wrapper flag parsing.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml`
  - Passed after creating the baseline change-local pack.
- `python scripts/select-validation.py --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path scripts/ci.sh --path specs/test-and-ci-speed-optimization.test.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path docs/plan.md`
  - Passed and selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `selector.regression`, and `broad_smoke.repo`.
- `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path scripts/ci.sh --path specs/test-and-ci-speed-optimization.test.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path docs/plan.md`
  - Passed the selected checks, including direct broad-smoke delegation required by the active plan.
- `git diff --check -- scripts/validation_selection.py scripts/test-select-validation.py scripts/ci.sh specs/test-and-ci-speed-optimization.test.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md docs/changes/2026-05-04-test-and-ci-speed-optimization docs/proposals/2026-05-04-test-and-ci-speed-optimization.md specs/test-and-ci-speed-optimization.md docs/plan.md`
  - Passed.
- `python scripts/test-select-validation.py`
  - First M2 run: expected failure before implementation. New M2 regressions exposed live child output, fail-first execution, missing summary/output sections, missing timeout enforcement, and invalid-byte leakage.
  - Final M2 run: passed with 49 tests after adding the sequential captured-result runner, large-output isolation proof, and default-timeout constant proof.
- `bash scripts/ci.sh --mode explicit --path scripts/ci.sh --jobs 1 --timeout 60 --verbose`
  - Passed with `selector.regression` selected, proving the new summary and verbose successful-output path through the wrapper.
- `python scripts/select-validation.py --mode explicit --path scripts/ci.sh --path scripts/test-select-validation.py --path specs/test-and-ci-speed-optimization.test.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path docs/plan.md`
  - Passed and selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `selector.regression`, and `broad_smoke.repo`.
- `bash scripts/ci.sh --mode explicit --path scripts/ci.sh --path scripts/test-select-validation.py --path specs/test-and-ci-speed-optimization.test.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path docs/plan.md --jobs 1`
  - Initially exposed an incorrect selected-check outer timeout on `broad_smoke.repo`; after removing that outer timeout, passed all selected checks with `broad_smoke.repo` completing successfully.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml`
  - Passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.test.md`
  - Passed.
- `git diff --check -- scripts/ci.sh scripts/test-select-validation.py specs/test-and-ci-speed-optimization.test.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md docs/changes/2026-05-04-test-and-ci-speed-optimization docs/plan.md`
  - Passed.
- `python scripts/test-select-validation.py`
  - First M3 run: expected failure before implementation. New M3 regressions exposed sequential-only execution, missing CPU-count fixture behavior, missing concurrent sibling start, and ignored fail-fast queued cancellation.
  - Second M3 run: passed with 54 tests after adding the bounded scheduler.
- `bash scripts/ci.sh --mode explicit --path scripts/test-skill-validator.py --path scripts/test-adapter-distribution.py --path scripts/test-artifact-lifecycle-validator.py --jobs 3`
  - Passed selected checks `skills.regression`, `adapters.regression`, `adapters.drift`, `adapters.validate`, and `artifact_lifecycle.regression`.
- `bash scripts/ci.sh --mode explicit --path scripts/test-skill-validator.py --path scripts/test-adapter-distribution.py --path scripts/test-artifact-lifecycle-validator.py --jobs 1`
  - Passed the same selected checks through the explicit sequential fallback.
- `python scripts/select-validation.py --mode explicit --path scripts/ci.sh --path scripts/validation_selection.py --path scripts/test-select-validation.py --path specs/test-and-ci-speed-optimization.test.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md`
  - Passed and selected `artifact_lifecycle.validate`, `selector.regression`, and `broad_smoke.repo`.
- `bash scripts/ci.sh --mode explicit --path scripts/ci.sh --path scripts/validation_selection.py --path scripts/test-select-validation.py --path specs/test-and-ci-speed-optimization.test.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --jobs 2`
  - Passed selected checks `artifact_lifecycle.validate`, `selector.regression`, and `broad_smoke.repo`.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml`
  - Passed after M3 closeout evidence updates.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.test.md`
  - Passed after M3 closeout evidence updates.
- `python scripts/select-validation.py --mode explicit --path scripts/ci.sh --path scripts/test-select-validation.py --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md`
  - Passed and selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `selector.regression`, and `broad_smoke.repo`.
- `bash scripts/ci.sh --mode explicit --path scripts/ci.sh --path scripts/test-select-validation.py --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --jobs 2`
  - Passed selected checks `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `selector.regression`, and `broad_smoke.repo`.
- `git diff --check -- scripts/ci.sh scripts/test-select-validation.py docs/plan.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md docs/changes/2026-05-04-test-and-ci-speed-optimization`
  - Passed.
- `rg -n '[[:blank:]]$|\\t' scripts/ci.sh scripts/test-select-validation.py docs/plan.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md docs/changes/2026-05-04-test-and-ci-speed-optimization`
  - Returned no matches.
- `python scripts/test-select-validation.py`
  - First M4 run: expected failure before documentation update. New T17 coverage exposed missing wrapper-flag guidance in `docs/workflows.md`.
  - Second M4 run: passed with 55 tests after adding the workflow-guidance flag assertions and hosted-CI matrix-free assertions.
- `bash scripts/ci.sh --mode explicit --path scripts/test-skill-validator.py --path scripts/test-adapter-distribution.py --path scripts/test-change-metadata-validator.py --path scripts/test-review-artifact-validator.py --path scripts/test-select-validation.py --path scripts/test-artifact-lifecycle-validator.py --jobs 6`
  - Passed selected checks `skills.regression`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `review_artifacts.regression`, `artifact_lifecycle.regression`, `change_metadata.regression`, and `selector.regression`.
- `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path .github/workflows/ci.yml --path scripts/ci.sh --path scripts/validation_selection.py --path scripts/test-select-validation.py --path specs/test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.test.md --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/plan.md`
  - Passed and selected `artifact_lifecycle.validate`, `selector.regression`, and `broad_smoke.repo`.
- `bash scripts/ci.sh --mode explicit --path docs/workflows.md --path .github/workflows/ci.yml --path scripts/ci.sh --path scripts/validation_selection.py --path scripts/test-select-validation.py --path specs/test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.test.md --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/plan.md --jobs 2`
  - Passed selected checks `artifact_lifecycle.validate`, `selector.regression`, and `broad_smoke.repo`.
- `bash scripts/ci.sh --mode broad-smoke`
  - Passed direct broad smoke.
- `rg -n "matrix:|check-id:|fromJson|select-validation|scripts/ci.sh|actions/cache" .github/workflows/ci.yml docs/workflows.md`
  - Returned only expected documentation and wrapper-call references; no matrix, check-id, fromJson, or actions/cache matches were present.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml`
  - Passed after M4 closeout evidence updates.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.test.md`
  - Passed after M4 closeout evidence updates.
- `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path .github/workflows/ci.yml --path scripts/test-select-validation.py --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md`
  - Passed and selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `selector.regression`, and `broad_smoke.repo`.
- `bash scripts/ci.sh --mode explicit --path docs/workflows.md --path .github/workflows/ci.yml --path scripts/test-select-validation.py --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --jobs 2`
  - Passed selected checks `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `selector.regression`, and `broad_smoke.repo`.
- `bash scripts/ci.sh --mode broad-smoke`
  - Passed direct broad smoke after closeout evidence updates.
- `git diff --check -- docs/workflows.md .github/workflows/ci.yml scripts/ci.sh scripts/validation_selection.py scripts/test-select-validation.py specs/test-and-ci-speed-optimization.md specs/test-and-ci-speed-optimization.test.md docs/proposals/2026-05-04-test-and-ci-speed-optimization.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md docs/plan.md docs/changes/2026-05-04-test-and-ci-speed-optimization`
  - Passed.
- `rg -n '[[:blank:]]$|\\t' docs/workflows.md scripts/test-select-validation.py docs/plan.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md docs/changes/2026-05-04-test-and-ci-speed-optimization`
  - Returned no matches.

## Readiness

M1, M2, M3, and M4 implementation are complete. The change is ready for code-review.
