# Selector-regression profile

- Proof ID: MP-SEL-001
- Commit or HEAD: `b91cbb06eddb5686ff80cb8bd404bf77231500f9`
- Worktree state: dirty; lifecycle-managed proposal, spec, test spec, plan, review evidence, and M1 evidence are not yet committed.
- Environment: local WSL2 Linux `6.6.87.2-microsoft-standard-WSL2 x86_64`; Python `3.12.3`; timing wrapper `/usr/bin/time -p`.
- Commands:
  - `/usr/bin/time -p python scripts/test-select-validation.py`
  - `/usr/bin/time -p python scripts/select-validation.py --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --json`
  - `/usr/bin/time -p python scripts/test-select-validation.py -k preflight`
  - `/usr/bin/time -p bash scripts/ci.sh --mode explicit --timeout 180 --path scripts/validation_selection.py --path scripts/test-select-validation.py --path specs/validation-runtime-follow-through.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/script-performance-baseline.yaml --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-regression-profile.md`
  - `/usr/bin/time -p bash scripts/ci.sh --mode explicit --timeout 300 --path scripts/validation_selection.py --path scripts/test-select-validation.py --path specs/validation-runtime-follow-through.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/script-performance-baseline.yaml --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-regression-profile.md`
- Baseline duration: direct selector-regression suite passed 103 tests; suite reported `142.65s`; `/usr/bin/time` reported `real 135.04`, `user 5.39`, `sys 22.61`.
- Timeout behavior: direct suite completed without wrapper timeout. The selected-CI wrapper path timed out at `--timeout 180`: `artifact_lifecycle.validate` passed in `0.49s`, `selector.regression` timed out after `180.12s`, and the wrapper exited `124`. The same wrapper path passed with `--timeout 300`: `artifact_lifecycle.validate` passed in `0.47s`, `selector.regression` passed in `273.28s`, and focused phase timing was `273.75s`.
- Timeout override used: `--timeout 180` was attempted and timed out; `--timeout 300` was required for a successful local selected-wrapper proof.
- Selected checks observed: `selector.regression` for the selector implementation surface.
- Dominant contributors: selector-regression suite execution dominates the measured selected-validation surface; selector calculation for the same paths completed in `1.18s`; preflight-only selector tests completed in `0.16s` real time; selected-wrapper `selector.regression` completed in `273.28s` when the timeout was raised to `300s`.
- Limitations:
  - This is a single local run, not a cross-machine median.
  - The current scripts do not emit per-test timing, Git inspection counts, subprocess counts, or filesystem bytes inspected.
  - Broad-smoke and final verify were not re-run for this M1 proof because broad-smoke reduction is a later classification slice and final verify requires stable committed tracked state.
- Safe reduction identified: no
- No-safe-reduction rationale: M1 records the profile before optimization. The evidence identifies the direct suite and selected-wrapper `selector.regression` path as the bottleneck but does not yet isolate a behavior-preserving implementation change inside `selector.regression`.
- Follow-up decision: M2 must add preservation evidence for selected-check identity and failure sensitivity before accepting any selector-regression runtime optimization. If no behavior-preserving reduction is found, M2 records a no-safe-reduction result rather than lowering coverage.

## Replay notes

Run from repository root with the same Python interpreter used for repository validation. If the selected wrapper path is run before the new lifecycle-managed artifacts are tracked, selected CI can preflight-block on untracked authoritative artifacts; stage or otherwise track the lifecycle artifacts before using the wrapper result as M1 evidence.
