# Test and CI Speed Optimization M1-M2 Explain Change

## Summary

M1 adds the metadata and command-line contract needed before the wrapper can safely run selected checks in parallel. The catalog now records explicit `parallel_safe` metadata and exposes an `is_parallel_safe_check` helper. The wrapper now accepts `--jobs`, `--timeout`, `--fail-fast`, and `--verbose`, rejects invalid numeric flag values before selector invocation, and keeps existing selector arguments unchanged.

M2 replaces ad hoc selected-check execution with a deterministic sequential result model. Selected checks now run through captured stdout/stderr buffers, produce stable summary rows, show failed logs after the summary, hide successful logs unless `--verbose` is supplied, enforce per-check timeouts, and distinguish ordinary nonzero exits, signal kills, timed-out checks, and unavailable commands.

Bounded concurrent scheduling and fail-fast queued-check cancellation remain in M3. Contributor guidance and hosted-CI boundary proof remain in M4.

## Decision Trail

- Proposal: `docs/proposals/2026-05-04-test-and-ci-speed-optimization.md`
- Spec: `specs/test-and-ci-speed-optimization.md`
- Test spec: `specs/test-and-ci-speed-optimization.test.md`
- Plan: `docs/plans/2026-05-04-test-and-ci-speed-optimization.md`
- Milestones: M1, catalog metadata and wrapper flag contract; M2, deterministic sequential runner and failure attribution

## Diff Rationale

| File or area | Change | Reason | Evidence |
| --- | --- | --- | --- |
| `scripts/validation_selection.py` | adds `parallel_safe` catalog metadata and marks only the six reviewed regression check IDs safe | satisfies the allowlist boundary without changing selector routing or command identities | `python scripts/test-select-validation.py` |
| `scripts/ci.sh` | parses `--jobs`, `--timeout`, `--fail-fast`, and `--verbose`; adds default timeout and CPU-minus-one default job helper; adds the sequential captured-result runner | establishes the wrapper-level invocation contract, early invalid-value rejection, deterministic summaries, output capture, timeout handling, and failure attribution | `python scripts/test-select-validation.py` |
| `scripts/test-select-validation.py` | adds M1 regression tests for catalog metadata and wrapper flags plus M2 regression tests for sequential reporting, output capture, timeout, signal, decode, unavailable-command, and verbose behavior | proves the new contract before production code and guards selector/wrapper boundary compatibility | red then green `python scripts/test-select-validation.py` |
| `docs/changes/2026-05-04-test-and-ci-speed-optimization/` | creates the baseline change-local pack | satisfies the non-trivial change evidence contract | change metadata validation |
| `docs/plans/2026-05-04-test-and-ci-speed-optimization.md` and `docs/plan.md` | records M1-M2 progress and validation evidence | keeps the active plan and plan index current during implementation | selector-selected validation |

## Same-Slice Completeness

- In scope through M2: M1 requirements `R2`, `R2a`, `R2b`, `R2c`, `R3`, `R3a`, `R3b`, `R4`, `R4c`, `R4d`, `R5`, `R7`, `R10`, `R16`, `R16a`, and `R20`; M2 requirements `R1`, `R2a`, `R3c`, `R3d`, `R3e`, `R6`, `R8`-`R14`, `R16`, `R16a`, and `R20`.
- Out of scope through M2: bounded parallel scheduling, fail-fast queued-check cancellation, hosted CI matrix fan-out, caching, distributed execution, sandboxing, and final contributor guidance.
- `docs/workflows.md` is intentionally unchanged until M4 because contributor guidance belongs after the scheduler behavior exists end to end.
- `.github/workflows/ci.yml` is intentionally unchanged because the approved first slice keeps hosted CI topology and matrix fan-out out of scope.
- `docs/architecture/system/architecture.md` is intentionally unchanged because M1-M2 preserve the existing selector, catalog, wrapper, and hosted CI boundaries without introducing a new helper module or parser boundary.

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

## Readiness

M1 and M2 implementation are complete. M3 remains the next implementation milestone after this M2 closeout commit.
