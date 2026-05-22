# Broad-Smoke and Fixture-Suite Output Compaction Behavior Preservation

## Scope

Change ID: `2026-05-22-broad-smoke-and-fixture-suite-output-compaction`

This record starts the behavior-preservation matrix for M1. It captures baseline identity and compatibility evidence before broad-smoke wrapper capture or producer output changes. Later milestones must add post-change proof before closing.

## Baseline Evidence Summary

| Surface | Baseline proof | Baseline result | Post-change proof | Preservation result |
| --- | --- | --- | --- | --- |
| broad-smoke child commands | `broad-smoke-child-commands-baseline.txt`; SHA-256 `8b1e4d0d7f36fccc0b7d0e2fa3ad5efedc39f7f41f935bb117c8c9f6eda9565f` | 12 normalized child command rows, including conditional review-artifact validation and derived artifact-lifecycle validation. | `broad-smoke-child-commands-post-m4.txt`; SHA-256 `8b1e4d0d7f36fccc0b7d0e2fa3ad5efedc39f7f41f935bb117c8c9f6eda9565f` | unchanged through M4 |
| broad-smoke pass exit code | `bash scripts/ci.sh --mode broad-smoke` in M1 validation | exit `0` after M1 | `bash scripts/ci.sh --mode broad-smoke` after M2 | exit `0`; default success is one aggregate `[PASS] broad-smoke` line |
| broad-smoke fail exit code | deterministic failing fixture required by TSRO-018 | not produced in M1; M2 must add fixture/proof before wrapper capture closes | `python scripts/test-select-validation.py --verbose -k broad_smoke` includes failing broad-smoke fixture | wrapper exits with child status `7` in the failing fixture |
| broad-smoke failure evidence | current streamed child output through `run_check` | current path is noisy but direct streaming keeps child stdout/stderr visible | `test_broad_smoke_failure_prints_command_exit_duration_and_captured_output` | captured failure output includes failed child name, command, exit code, duration, and combined stdout/stderr in emitted order |
| broad-smoke verbose output | current `--verbose` flag is parsed by wrapper; inner broad-smoke currently streams child output regardless | baseline detail is available because output streams by default | `bash scripts/ci.sh --mode broad-smoke --verbose`; `test_broad_smoke_verbose_prints_successful_child_output_in_order` | full successful child output remains available under `--verbose` in stable child-check order |
| producer selected tests/checks | `change-metadata-validator-tests-baseline.txt`; SHA-256 `fbb2230ef0c90ae64d7d0eb34966b994f318d8e042ca56fabaa4d39edbbe108e` | 18 ordered unittest identifiers | `change-metadata-validator-tests-post-m4.txt`; SHA-256 `fbb2230ef0c90ae64d7d0eb34966b994f318d8e042ca56fabaa4d39edbbe108e` | unchanged through M4 |
| producer pass exit code | `python scripts/test-change-metadata-validator.py` | exit `0`; default success currently writes unittest detail to stderr | `python scripts/test-change-metadata-validator.py` after M3 | exit `0`; default success is one `[PASS] test-change-metadata-validator: 18 passed ...` line |
| producer quiet compatibility | `python scripts/test-change-metadata-validator.py --quiet`; `python scripts/test-change-metadata-validator.py -q` | both exit `0`; both write no stdout; both may write normal unittest quiet summary to stderr | same commands after M3 | both exit `0`; both write no stdout; both keep normal unittest quiet summary to stderr |
| producer failure evidence | deterministic failing fixture required by TSRO-021 | not produced in M1; M3 must add fixture/proof before producer output closeout | `RIGORLOOP_CHANGE_METADATA_FAILURE_FIXTURE=1 python scripts/test-change-metadata-validator.py ChangeMetadataValidatorFixtureTests.test_output_contract_fixture_failure` | exit `1`; default failure includes `[FAIL]` summary, failed test name, assertion message, file location, and scoped rerun |
| selected-CI behavior | selected-CI regression required by TSRO-026 | not changed in M1 | selected explicit CI after M4 | unchanged; selected `change_metadata.regression` and `selector.regression` pass for touched wrapper/producer/test paths |
| generated artifacts, skills, adapters, JSON, validation selection | diff inspection and selected CI in M1 validation | no M1 production changes | M4 diff inspection plus selected explicit CI and lifecycle validation | no generated artifacts, skills, adapters, JSON support, validation selection logic, or validation coverage changes introduced |

## Broad-Smoke Command Identity Proof

Baseline file: `broad-smoke-child-commands-baseline.txt`

Hash command:

```bash
sha256sum docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/broad-smoke-child-commands-baseline.txt
```

Baseline hash:

```text
8b1e4d0d7f36fccc0b7d0e2fa3ad5efedc39f7f41f935bb117c8c9f6eda9565f
```

Normalization rationale:

- `adapter_release_output` is created with `mktemp -d`, so the actual filesystem path is not stable.
- changed review roots are worktree-dependent, so the normalized command records `${changed_review_roots}`.
- artifact-lifecycle explicit paths are worktree-dependent, so the normalized command records `${tracked_authored_diff_paths}`.

The normalized list is the deterministic proof surface for command identity. M2 and M4 must compare against this normalized list unless a reviewed plan/spec change defines a stronger extraction method.

Post-M2 file: `broad-smoke-child-commands-post-m2.txt`

Post-M2 hash:

```text
8b1e4d0d7f36fccc0b7d0e2fa3ad5efedc39f7f41f935bb117c8c9f6eda9565f
```

M2 changed `run_check` output handling only. The normalized child command list and hash remain unchanged from the M1 baseline.

Post-M4 file: `broad-smoke-child-commands-post-m4.txt`

Post-M4 hash:

```text
8b1e4d0d7f36fccc0b7d0e2fa3ad5efedc39f7f41f935bb117c8c9f6eda9565f
```

M4 recomputed the normalized broad-smoke child-command proof after wrapper and producer changes. The normalized child command list and hash remain unchanged from the M1 baseline.

## Broad-Smoke Wrapper Capture Proof

M2 proof commands:

```bash
python scripts/test-select-validation.py --verbose -k broad_smoke
bash scripts/ci.sh --mode broad-smoke
bash scripts/ci.sh --mode broad-smoke --verbose
bash scripts/ci.sh --mode explicit --path scripts/ci.sh --jobs 1
```

Proof results:

- default successful broad-smoke exits `0` and prints one aggregate `[PASS] broad-smoke: 12 checks passed in 134s` line in the recorded local run;
- broad-smoke `--verbose` exits `0` and prints successful child captured output in child-check order;
- the failing broad-smoke fixture exits with child status `7` and prints the failed child name, command, exit code, duration, captured stdout, and captured stderr;
- the wrapper-mode consistency guard runs inside `scripts/test-select-validation.py`, passes against current `scripts/ci.sh`, and fails against a negative non-capturing `run_check` fixture.

## Producer Test Identity Proof

Baseline file: `change-metadata-validator-tests-baseline.txt`

Replayable extraction method:

```bash
python - <<'PY'
import hashlib
import importlib.util
import sys
import unittest
from pathlib import Path

path = Path("scripts/test-change-metadata-validator.py")
spec = importlib.util.spec_from_file_location("test_change_metadata_validator", path)
if spec is None or spec.loader is None:
    raise RuntimeError(f"could not load module spec for {path}")
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
suite = unittest.defaultTestLoader.loadTestsFromModule(module)

def iter_test_ids(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from iter_test_ids(item)
        else:
            yield item.id()

test_ids = list(iter_test_ids(suite))
data = "\n".join(test_ids) + "\n"
digest = hashlib.sha256(data.encode("utf-8")).hexdigest()

print(f"count: {len(test_ids)}")
print(f"sha256:{digest}")
for test_id in test_ids:
    print(test_id)
PY
```

Hash command:

```bash
sha256sum docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change-metadata-validator-tests-baseline.txt
```

Baseline hash:

```text
fbb2230ef0c90ae64d7d0eb34966b994f318d8e042ca56fabaa4d39edbbe108e
```

Baseline count: `18`

Post-M3 file: `change-metadata-validator-tests-post-m3.txt`

Post-M3 hash:

```text
fbb2230ef0c90ae64d7d0eb34966b994f318d8e042ca56fabaa4d39edbbe108e
```

M3 changed runner output handling only. The ordered selected-test identifier list and hash remain unchanged from the M1 baseline.

M3 review-resolution replayed the documented extraction after registering the module in `sys.modules` before `exec_module()`. The extraction succeeded with count `18` and SHA-256 `fbb2230ef0c90ae64d7d0eb34966b994f318d8e042ca56fabaa4d39edbbe108e`.

Post-M4 file: `change-metadata-validator-tests-post-m4.txt`

Post-M4 hash:

```text
fbb2230ef0c90ae64d7d0eb34966b994f318d8e042ca56fabaa4d39edbbe108e
```

M4 replayed the selected-test identity extraction after all M3 review-resolution updates. The extraction succeeded with count `18`, and the ordered selected-test identifier list and hash remain unchanged from the M1 baseline.

## Producer Compact Runner Proof

M3 proof commands:

```bash
python scripts/test-select-validation.py --verbose -k change_metadata_validator
python scripts/test-change-metadata-validator.py
python scripts/test-change-metadata-validator.py --verbose
python scripts/test-change-metadata-validator.py -v
python scripts/test-change-metadata-validator.py --quiet
python scripts/test-change-metadata-validator.py -q
RIGORLOOP_CHANGE_METADATA_FAILURE_FIXTURE=1 python scripts/test-change-metadata-validator.py ChangeMetadataValidatorFixtureTests.test_output_contract_fixture_failure
python scripts/test-change-metadata-validator.py -k no_such_test_name
```

Proof results:

- default successful producer runs exit `0` and print one `[PASS] test-change-metadata-validator: 18 passed ...` line;
- default producer failure exits `1` and includes the failed test name, assertion message, file location, and rerun command;
- `--verbose` and `-v` exit `0` and preserve full unittest pass/check detail;
- `--quiet` and `-q` exit `0`, write no stdout, and preserve normal unittest quiet success summary on stderr;
- zero selected tests exit `1` with an explicit `[FAIL] ... 0 tests run` diagnostic.

## Producer Quiet Compatibility Proof

Commands:

```bash
python scripts/test-change-metadata-validator.py --quiet
python scripts/test-change-metadata-validator.py -q
```

Baseline result:

| Command | Exit | Stdout | Stderr |
| --- | --- | --- | --- |
| `python scripts/test-change-metadata-validator.py --quiet` | `0` | 0 lines | 4 lines, normal unittest quiet summary with `Ran 18 tests ... OK` |
| `python scripts/test-change-metadata-validator.py -q` | `0` | 0 lines | 4 lines, normal unittest quiet summary with `Ran 18 tests ... OK` |

M3 must preserve accepted invocation compatibility. This slice must not add a custom compact quiet formatter for this producer.

## M1 Validation Targets

M1 validation must include:

```bash
bash scripts/ci.sh --mode broad-smoke
python scripts/test-change-metadata-validator.py
python scripts/test-change-metadata-validator.py --quiet
python scripts/test-change-metadata-validator.py -q
python scripts/validate-change-metadata.py docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml
git diff --check -- docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction
```

Results are recorded in the active plan and `change.yaml` after M1 validation runs.

## M4 Ordinary Validation and Scope Proof

M4 records that output-contract tests run under ordinary validation:

- `python scripts/test-select-validation.py` runs the broad-smoke wrapper output-contract tests and the `scripts/test-change-metadata-validator.py` subprocess output-contract tests.
- `python scripts/test-change-metadata-validator.py` runs the targeted producer validation suite with compact default output.

Selected-CI regression proof:

- `bash scripts/ci.sh --mode explicit --path scripts/ci.sh --path scripts/test-change-metadata-validator.py --path scripts/test-select-validation.py --jobs 1` selects and passes `change_metadata.regression` and `selector.regression`.
- The expanded explicit selected-CI command for M4 includes the wrapper, producer, selector test, spec, test spec, active plan, plan index, and change metadata paths.

Out-of-scope surface proof:

- M4 does not change generated artifacts, skills, adapters, JSON behavior, validation selection logic, or validation coverage.
- The only runtime surfaces changed by this slice remain `scripts/ci.sh`, `scripts/test-select-validation.py`, and `scripts/test-change-metadata-validator.py`; M4 itself updates preservation and lifecycle evidence only.
