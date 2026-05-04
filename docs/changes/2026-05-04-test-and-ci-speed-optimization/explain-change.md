# Test and CI Speed Optimization M1 Explain Change

## Summary

M1 adds the metadata and command-line contract needed before the wrapper can safely run selected checks in parallel. The catalog now records explicit `parallel_safe` metadata and exposes an `is_parallel_safe_check` helper. The wrapper now accepts `--jobs`, `--timeout`, `--fail-fast`, and `--verbose`, rejects invalid numeric flag values before selector invocation, and keeps existing selector arguments unchanged.

This milestone does not add parallel scheduling, captured output, timeout enforcement, or fail-fast cancellation behavior. Those stay in M2 and M3.

## Decision Trail

- Proposal: `docs/proposals/2026-05-04-test-and-ci-speed-optimization.md`
- Spec: `specs/test-and-ci-speed-optimization.md`
- Test spec: `specs/test-and-ci-speed-optimization.test.md`
- Plan: `docs/plans/2026-05-04-test-and-ci-speed-optimization.md`
- Milestone: M1, catalog metadata and wrapper flag contract

## Diff Rationale

| File or area | Change | Reason | Evidence |
| --- | --- | --- | --- |
| `scripts/validation_selection.py` | adds `parallel_safe` catalog metadata and marks only the six reviewed regression check IDs safe | satisfies the allowlist boundary without changing selector routing or command identities | `python scripts/test-select-validation.py` |
| `scripts/ci.sh` | parses `--jobs`, `--timeout`, `--fail-fast`, and `--verbose`; adds default timeout and CPU-minus-one default job helper | establishes the wrapper-level invocation contract and early invalid-value rejection for M1 | `python scripts/test-select-validation.py` |
| `scripts/test-select-validation.py` | adds M1 regression tests for catalog metadata, valid wrapper flags, and invalid wrapper flags before selector invocation | proves the new contract before production code and guards selector/wrapper boundary compatibility | red then green `python scripts/test-select-validation.py` |
| `docs/changes/2026-05-04-test-and-ci-speed-optimization/` | creates the baseline change-local pack | satisfies the non-trivial change evidence contract | change metadata validation |
| `docs/plans/2026-05-04-test-and-ci-speed-optimization.md` | records M1 progress and validation evidence | keeps the active plan current during implementation | selector-selected validation |

## Same-Slice Completeness

- In scope: M1 requirements `R2`, `R2a`, `R2b`, `R2c`, `R3`, `R3a`, `R3b`, `R4`, `R4c`, `R4d`, `R5`, `R7`, `R10`, `R16`, `R16a`, and `R20`.
- Out of scope for M1: selected-check result model, output capture, timeout enforcement, signal reporting, bounded parallel scheduling, and fail-fast queued-check cancellation.
- `docs/workflows.md` is intentionally unchanged in M1 because contributor guidance belongs to M4 after the behavior exists end to end.
- `.github/workflows/ci.yml` is intentionally unchanged because the approved first slice keeps hosted CI topology and matrix fan-out out of scope.
- `docs/architecture/system/architecture.md` is intentionally unchanged because M1 preserves the existing selector, catalog, wrapper, and hosted CI boundaries.

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

## Readiness

M1 implementation and milestone validation are complete. M2 remains the next implementation milestone after this M1 closeout commit.
