# Script Output Optimization Behavior Preservation

Change ID: `2026-05-21-script-output-optimization`
Date: 2026-05-21
Milestone: M1 audit and baseline preservation evidence

## Scope

This matrix records baseline evidence before changing presentation. Later implementation milestones must add the new proof column and preservation result for every touched script.

## `scripts/test-select-validation.py`

| Behavior | Baseline proof | New proof | Preservation result |
| --- | --- | --- | --- |
| exit code on pass | `python scripts/test-select-validation.py` exited `0` | M3 resolution `python scripts/test-select-validation.py` exited `0` with `[PASS] test-select-validation: 73 passed ...` | unchanged success exit code |
| exit code on failure | `python scripts/test-select-validation.py NoSuchTest` exited `1` | M3 `python scripts/test-select-validation.py NoSuchTest` exited `1` with `[FAIL] test-select-validation: 1 failed, 0 passed ...` | unchanged failure exit code |
| selected tests/checks | `python scripts/test-select-validation.py` ran the `62` ordered unittest identifiers listed in `selected-tests-baseline.txt`; selected-set SHA-256 is `sha256:af470dd836f5b1b44c702be35206934f77621a1477d88cafae923e50a7f492bd` | M3 resolution ordinary validation ran `73` tests listed in `selected-tests-m3.txt`: the original `62` baseline identifiers, the approved M2 guard, and the `10` required `ScriptOutputContractTests`; current full-suite SHA-256 is `sha256:878bd8dfce24e987ee50ab36d686f54e8d821bf4a5b11fe831d381c57d164047` | preserved, with approved M2 and M3 test-suite extensions |
| failure detection | `python scripts/test-select-validation.py NoSuchTest` reported `ERROR` and `FAILED (errors=1)` | M3 `python scripts/test-select-validation.py NoSuchTest` reports a nonzero `[FAIL]` summary and failed identifier `unittest.loader._FailedTest.NoSuchTest` | preserved |
| failure evidence | `NoSuchTest` failure output included failed identifier, error status, exception type/message, run count, and failed summary | M3 `NoSuchTest` failure output includes failed identifier, exception type/message, failed count, passed count, and duration; no scoped rerun is emitted because loader failures are not reliable exact filters | same or more actionable |
| verbose output | `python scripts/test-select-validation.py --verbose` exited `0`, ran `62` tests, and emitted the current full pass-list output | M3 resolution `python scripts/test-select-validation.py --verbose` exited `0`, ran `73` tests, and emitted the full pass-list output plus unittest footer | preserved behind `--verbose` |
| quiet failure output | not available in baseline; `--quiet` is new first-slice behavior | M3 `python scripts/test-select-validation.py --quiet ScriptOutputFixtureTests.fixture_contract_failure` exited `1` and printed `[FAIL]`, failed test name, assertion message, file location, and reliable scoped rerun command | new behavior satisfies the approved first-slice contract |
| JSON behavior | `python scripts/test-select-validation.py --json` exited `2` with `unrecognized arguments: --json` | M3 `python scripts/test-select-validation.py --json` exits `2` with `unrecognized arguments: --json` | unchanged; no JSON support added |

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

## M3 selected test/check set

- Command: `python scripts/test-select-validation.py --verbose`
- Count: `73`
- Ordered list: `selected-tests-m3.txt`
- Hash input rule: ordered identifiers joined by `\n`, with one trailing newline and no extra whitespace.
- SHA-256: `sha256:878bd8dfce24e987ee50ab36d686f54e8d821bf4a5b11fe831d381c57d164047`
- Ordinary validation includes `10` `ScriptOutputContractTests` plus the M2 guard `ValidationSelectionTests.test_output_contract_red_tests_are_unmasked_and_separate`.

## M2 output-contract test extension

M2 intentionally extends `scripts/test-select-validation.py` with output-contract tests before the formatter is implemented. This is an approved test-suite change, not a validation-selection behavior change.

- M2 adds `ScriptOutputContractTests` to cover default success, default failure, verbose success, quiet success/failure, conflicting flags, zero-test failure, rerun behavior, and JSON deferral.
- M2 excluded `ScriptOutputContractTests` from ordinary validation through `load_tests` and ran the class explicitly as red-test proof before M3.
- M2 adds `ScriptOutputFixtureTests.fixture_contract_failure` as a named failure fixture that is not discovered by default because the method name does not start with `test`.
- M2 ordinary validation ran `python scripts/test-select-validation.py`: `63` tests.
- M2 red-test proof ran `python scripts/test-select-validation.py ScriptOutputContractTests`: nonzero exit with `FAILED (failures=9)` before M3.
- M3 resolution removed the `load_tests` exclusion so `ScriptOutputContractTests` run as ordinary post-M3 validation.

## M3 output shaping proof

M3 implements presentation-only output shaping around the existing unittest loader and runner result.

- `python scripts/test-select-validation.py` exits `0`, runs the output-contract acceptance tests, and prints one default success line: `[PASS] test-select-validation: 73 passed ...`.
- `python scripts/test-select-validation.py ScriptOutputContractTests` exits `0`; the focused output-contract command remains available as a diagnostic rerun.
- `python scripts/test-select-validation.py --quiet` exits `0` with empty stdout and stderr.
- `python scripts/test-select-validation.py --verbose --quiet` exits `2`, writes no stdout, names both flags in stderr, and runs no tests.
- `python scripts/test-select-validation.py -k definitely_no_script_output_tests` exits `1` with a zero-test `[FAIL]` diagnostic.
- `python scripts/test-select-validation.py --json` remains unsupported and exits `2`.
- The original M1 baseline `ValidationSelectionTests` identifiers remain present in the same order. The current full-suite ordered identifier hash is `sha256:878bd8dfce24e987ee50ab36d686f54e8d821bf4a5b11fe831d381c57d164047`.

## M1 conclusion

Baseline evidence supports the approved first-slice boundary:

- `scripts/test-select-validation.py` is the noisy script-output target.
- `scripts/ci.sh` already has quiet-success behavior at the wrapper layer for the selected pass path.
- No production code changed in M1.
- M2 should add output-contract tests before M3 changes runner presentation.
