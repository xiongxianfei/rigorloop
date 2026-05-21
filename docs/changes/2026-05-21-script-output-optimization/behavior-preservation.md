# Script Output Optimization Behavior Preservation

Change ID: `2026-05-21-script-output-optimization`
Date: 2026-05-21
Milestone: M1 audit and baseline preservation evidence

## Scope

This matrix records baseline evidence before changing presentation. Later implementation milestones must add the new proof column and preservation result for every touched script.

## `scripts/test-select-validation.py`

| Behavior | Baseline proof | New proof | Preservation result |
| --- | --- | --- | --- |
| exit code on pass | `python scripts/test-select-validation.py` exited `0` | pending M3 | pending |
| exit code on failure | `python scripts/test-select-validation.py NoSuchTest` exited `1` | pending M3 | pending |
| selected tests/checks | `python scripts/test-select-validation.py` ran the `62` ordered unittest identifiers listed in `selected-tests-baseline.txt`; selected-set SHA-256 is `sha256:af470dd836f5b1b44c702be35206934f77621a1477d88cafae923e50a7f492bd` | pending M3 | M3 must preserve the same ordered selected-test set unless an intentional selection change is separately approved |
| failure detection | `python scripts/test-select-validation.py NoSuchTest` reported `ERROR` and `FAILED (errors=1)` | pending M3 | pending |
| failure evidence | `NoSuchTest` failure output included failed identifier, error status, exception type/message, run count, and failed summary | pending M3 | pending |
| verbose output | `python scripts/test-select-validation.py --verbose` exited `0`, ran `62` tests, and emitted the current full pass-list output | pending M3 | pending |
| quiet failure output | not available in baseline; `--quiet` is new first-slice behavior | pending M3 | pending |
| JSON behavior | `python scripts/test-select-validation.py --json` exited `2` with `unrecognized arguments: --json` | pending M3 | pending |

## `scripts/ci.sh`

`scripts/ci.sh` is conditional. Baseline evidence is recorded now so M4 can either close with no code or compare a minimal wrapper patch.

| Behavior | Baseline proof | New proof | Preservation result |
| --- | --- | --- | --- |
| selected checks | `bash scripts/ci.sh --mode explicit --path scripts/test-select-validation.py --path scripts/ci.sh` selected `selector.regression` | pending M4 | pending |
| exit code on pass | same command exited `0` | pending M4 | pending |
| successful child output hidden by default | same command emitted 10 stdout lines and did not include the child `unittest` pass list | pending M4 | pending |
| successful child output exposed with wrapper `--verbose` | `bash scripts/ci.sh --mode explicit --path scripts/test-select-validation.py --path scripts/ci.sh --verbose` exited `0` and emitted 81 stdout lines including child pass-list output | pending M4 | pending |
| failed selected-check evidence | existing `scripts/test-select-validation.py` regressions cover wrapper failure attribution for selected command failure, unavailable command, timeout, signal, decode failure, and malformed selector output | pending M4 if touched | pending |
| CI semantics if touched | baseline wrapper modes and child-process exit behavior are unchanged in M1 because no wrapper code was edited | pending M4 if touched | pending |

## Selected test/check set baseline

- Command: `python scripts/test-select-validation.py`
- Count: `62`
- Ordered list: `selected-tests-baseline.txt`
- Hash input rule: ordered identifiers joined by `\n`, with one trailing newline and no extra whitespace.
- SHA-256: `sha256:af470dd836f5b1b44c702be35206934f77621a1477d88cafae923e50a7f492bd`

The ordered list was derived from the baseline `ValidationSelectionTests` unittest identifiers. M3 must compare the post-change selected test/check set against this list and hash unless an intentional selection change is separately approved.

## M2 output-contract test extension

M2 intentionally extends `scripts/test-select-validation.py` with output-contract tests before the formatter is implemented. This is an approved test-suite change, not a validation-selection behavior change.

- M2 adds `ScriptOutputContractTests` to cover default success, default failure, verbose success, quiet success/failure, conflicting flags, zero-test failure, rerun behavior, and JSON deferral.
- M2 keeps formatter-dependent cases as `unittest.expectedFailure` so the suite remains runnable before M3 while still proving the old output does not satisfy the approved contract.
- M2 adds `ScriptOutputFixtureTests.fixture_contract_failure` as a named failure fixture that is not discovered by default because the method name does not start with `test`.
- M2 validation ran `python scripts/test-select-validation.py`: `72` tests, `7` expected failures.
- M3 must turn the expected-failure contract tests into ordinary passing tests when the output formatter is implemented.

## M1 conclusion

Baseline evidence supports the approved first-slice boundary:

- `scripts/test-select-validation.py` is the noisy script-output target.
- `scripts/ci.sh` already has quiet-success behavior at the wrapper layer for the selected pass path.
- No production code changed in M1.
- M2 should add output-contract tests before M3 changes runner presentation.
