# Selector-Regression Profile Proof

Proof ID: MP-SEL-001
Change ID: 2026-06-27-selector-regression-runtime-reduction
Recorded: 2026-06-27T03:57:27-07:00
Owner stage: M1. Baseline, Profile, and Identity Inventory

## Environment

- Runner: local WSL2
- OS: Linux LAPTOP-RLULAM5H 6.6.87.2-microsoft-standard-WSL2
- Python: 3.12.3
- CPU class: Intel Core Ultra 9 275HX, 24 vCPU visible
- Branch: proposal/selector-regression-runtime-reduction
- HEAD: bf3f97dba7f16c807c38d20923f298da0aa4afb8
- Worktree state: dirty with this change's lifecycle artifacts and M1 selector-route edits in progress

## Commands

Baseline timing:

```bash
for run in 1 2 3; do printf 'RUN %s\n' "$run"; /usr/bin/time -p python scripts/test-select-validation.py; done
```

Grouped timing:

```bash
/usr/bin/time -p python scripts/test-select-validation.py -k ci_wrapper
/usr/bin/time -p python scripts/test-select-validation.py -k ScriptOutputContractTests
/usr/bin/time -p python scripts/test-select-validation.py -k broad_smoke
/usr/bin/time -p python scripts/test-select-validation.py -k ValidationSelectionTests
```

Selector identity and route check:

```bash
python scripts/select-validation.py --mode explicit --path scripts/test-select-validation.py --path scripts/validation_selection.py --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-profile.md --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-runtime-baseline.yaml --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-preservation.md --path specs/selector-regression-runtime-reduction.md --path specs/selector-regression-runtime-reduction.test.md --path docs/plans/2026-06-27-selector-regression-runtime-reduction.md
```

## Baseline Duration

| Run | Tests | Suite duration | `/usr/bin/time` real | Result |
| --- | ---: | ---: | ---: | --- |
| 1 | 109 | 175.30s | 165.71s | pass |
| 2 | 109 | 174.41s | 164.73s | pass |
| 3 | 109 | 172.79s | 161.13s | pass |

Median baseline:

- Suite duration median: 174.41s
- Real duration median: 164.73s
- Test count: 109

## Timeout Behavior

No command-level timeout fired during M1 baseline collection. The median real duration remains close to the selected-CI timeout boundary and above the previously desired inner-loop feedback range.

## Selected Checks Observed

After registering selector runtime YAML evidence, the selector classified the M1 evidence paths as deterministic registered evidence and selected:

- `artifact_lifecycle.validate`
- `selector.regression`

The selector initially reported a `tracked_authoritative_artifacts` blocker while new authoritative lifecycle files were untracked. After staging the M1 artifact set, the selector returned `status: ok`, `blocking_results: []`, and `registration_debt: []`. Registration debt for `selector-regression-runtime-baseline.yaml` was removed by adding the `selector-regression-runtime` evidence class.

## Dominant Contributors

Grouped timing showed:

| Group command | Tests | Real duration | Result |
| --- | ---: | ---: | --- |
| `python scripts/test-select-validation.py -k ci_wrapper` | 21 | 7.61s | pass |
| `python scripts/test-select-validation.py -k ScriptOutputContractTests` | 10 | 1.96s | pass |
| `python scripts/test-select-validation.py -k broad_smoke` | 13 | 4.13s | pass |
| `python scripts/test-select-validation.py -k ValidationSelectionTests` | 99 | 164.20s | pass |

The broad `ValidationSelectionTests` bucket accounts for nearly the entire default command duration. This bucket includes pure selector classification cases, temporary repository fixtures, route-registration checks, selected-CI wrapper fixtures, cache-boundary checks, broad-smoke classification checks, and subprocess-backed boundary cases.

## Instrumentation Limitations

This M1 proof used wall-clock baseline timing and grouped `-k` timing rather than a line-level profiler. The grouped timings overlap because several boundary and broad-smoke tests live inside `ValidationSelectionTests`. The evidence is sufficient to identify the next safe target as duplicate work inside selector-regression structure, but M2 should use local per-case timing if a finer-grained conversion order is needed.

## Safe Reduction Identified

Safe reduction candidate for M2:

- Keep subprocess tests for CLI and wrapper boundaries.
- Convert pure selector scenarios inside `ValidationSelectionTests` to shared in-process table-driven fixtures where command-boundary behavior is not under test.
- Reuse immutable or resettable changed-path fixtures and avoid repeated temporary repository setup when a stable path list is enough.

M1 did not implement the runtime reducer. The only code change in M1 registers the approved selector-runtime evidence file names so baseline/result evidence does not create manual-routing debt.

## No-Safe-Reduction Rationale

Not applicable for M1. Profiling found a safe candidate for M2; runtime reduction remains unclaimed until M2/M3 evidence exists.

## Follow-Up Decision

Proceed to M2 only after M1 code-review. M2 should target duplicate work in `ValidationSelectionTests` while preserving selected-check identity, missing-route blockers, CLI-boundary subprocess tests, cache-boundary metadata, and broad-smoke classification behavior.

## M3 Outcome

M3 recorded revised runtime evidence after M2 code-review closed:

- Baseline median real duration: 164.73s for 109 tests.
- Revised median real duration: 36.23s for 111 tests.
- Median reduction: 78.01%.
- Selected-CI timeout override status: no 180-second override is required for the selector-regression path; selected-CI completed `selector.regression` in 36.47s without `--timeout 300`.

The runtime result is recorded in `selector-regression-runtime-result.yaml`. M3 also fixed a broad-smoke elapsed-time output regression discovered during timing; the fix preserves sequential broad-smoke execution and changes only duration reporting.
