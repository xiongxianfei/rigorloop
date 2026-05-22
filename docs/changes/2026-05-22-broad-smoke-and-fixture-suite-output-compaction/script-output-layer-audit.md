# Broad-Smoke and Fixture-Suite Output Layer Audit

## Scope

Change ID: `2026-05-22-broad-smoke-and-fixture-suite-output-compaction`

This M1 audit records the current output layers before broad-smoke wrapper capture or producer output formatting changes. It satisfies `specs/script-output-optimization.md` R36 through R38 and supports TSRO-015.

M2 update: broad-smoke `run_check` now captures child stdout/stderr, emits default successful output as one aggregate `[PASS] broad-smoke` summary, and prints captured child output on failure or under `--verbose`.

M3 update: `scripts/test-change-metadata-validator.py` now has compact default direct-run output, preserves full unittest detail under `--verbose` and `-v`, and preserves existing unittest-compatible `--quiet` and `-q` behavior without custom quiet formatting.

M4 update: final preservation evidence confirms broad-smoke command identity and `scripts/test-change-metadata-validator.py` selected-test identity remain unchanged after the coordinated wrapper and producer changes.

The audit separates:

- producers: scripts or commands that print output directly;
- orchestrators: repository-owned wrappers or modes that run producers.

## Summary

Broad-smoke was the structural output gap for this slice at M1. The selected-CI path already captured successful child output and printed failed child output. M2 changed the broad-smoke `run_check` path from streaming to capture-on-success/show-on-failure-or-verbose behavior.

The first targeted direct-run producer remains `scripts/test-change-metadata-validator.py`. No audit exception replaces it.

## Producer and Orchestrator Matrix

| Producer or command | Direct-run success shape | Direct-run failure usefulness | Orchestrators | Current orchestrator capture policy | High-use direct-run? | First-slice treatment |
| --- | --- | --- | --- | --- | --- | --- |
| `scripts/test-select-validation.py` | Compact first-slice output: one `[PASS] test-select-validation` summary line in default mode. | Actionable first-slice output: `[FAIL]` summary plus failed names/messages/locations when available. | selected-CI explicit/local/PR/main/release paths; broad-smoke indirectly through selected-CI only when the selector includes `broad_smoke.repo` delegation. | selected-CI captures successful child output by default and emits successful child output under `--verbose`; M2 broad-smoke captures direct `run_check` child output. | yes | Baseline from PR #83; no producer change in this slice. |
| `scripts/test-change-metadata-validator.py` | M3 compact success: one `[PASS] test-change-metadata-validator: 18 passed ...` line by default; full unittest detail remains under `--verbose` and `-v`; `--quiet` and `-q` keep normal unittest quiet stderr summary. | M3 compact failure includes `[FAIL]` summary, failed test name, assertion/error message, file location, and rerun command when available. | broad-smoke direct child; selected-CI when changed paths select `change_metadata.regression`; direct local maintainer runs. | M2 broad-smoke `run_check` captures; selected-CI captures successful output by default. | yes | M3 completed compact default and verbose compatibility; quiet compatibility preserved, not custom compacted in this slice. |
| `scripts/validate-skills.py` | Validator-style direct success; not first targeted producer. | Validator failure expected to name invalid skill surface. | broad-smoke direct child; selected-CI when selected by touched paths. | M2 broad-smoke `run_check` captures; selected-CI captures successful output by default. | medium | Covered by broad-smoke wrapper capture in M2; producer formatting deferred. |
| `scripts/test-skill-validator.py` | Test/fixture success output; not first targeted producer. | Test failure output expected to identify failing fixture/test. | broad-smoke direct child; selected-CI when selected by touched paths. | M2 broad-smoke `run_check` captures; selected-CI captures successful output by default. | medium | Covered by broad-smoke wrapper capture in M2; producer formatting deferred. |
| `scripts/test-build-skills.py` | Test/fixture success output; not first targeted producer. | Test failure output expected to identify failing fixture/test. | broad-smoke direct child. | M2 broad-smoke `run_check` captures. | low | Covered by broad-smoke wrapper capture in M2; producer formatting deferred. |
| `scripts/build-skills.py --check` | Drift/check success output; not first targeted producer. | Failure output expected to identify generated skill drift. | broad-smoke direct child; selected-CI when generated skill checks are selected. | M2 broad-smoke `run_check` captures; selected-CI captures successful output by default. | medium | Covered by broad-smoke wrapper capture in M2; producer formatting deferred. |
| `scripts/test-adapter-distribution.py` | Test/fixture success output; not first targeted producer. | Test failure output expected to identify adapter distribution fixture failure. | broad-smoke direct child. | M2 broad-smoke `run_check` captures. | low | Covered by broad-smoke wrapper capture in M2; producer formatting deferred. |
| `scripts/build-adapters.py --version v0.1.3 --output-dir ...` | Build success output; not first targeted producer. | Failure output expected to identify adapter generation failure. | broad-smoke direct child. | M2 broad-smoke `run_check` captures. | low | Covered by broad-smoke wrapper capture in M2; producer formatting deferred. |
| `scripts/validate-adapters.py --root ... --version v0.1.3` | Validator success output; not first targeted producer. | Failure output expected to identify adapter archive validation failure. | broad-smoke direct child. | M2 broad-smoke `run_check` captures. | low | Covered by broad-smoke wrapper capture in M2; producer formatting deferred. |
| `scripts/test-artifact-lifecycle-validator.py` | Test/fixture success output; not first targeted producer. | Test failure output expected to identify lifecycle validation fixture failure. | broad-smoke direct child; selected-CI when selected by touched lifecycle paths. | M2 broad-smoke `run_check` captures; selected-CI captures successful output by default. | medium | Covered by broad-smoke wrapper capture in M2; producer formatting deferred. |
| `scripts/test-review-artifact-validator.py` | Test/fixture success output; not first targeted producer. | Test failure output expected to identify review artifact validation fixture failure. | broad-smoke direct child; selected-CI when review artifacts are touched. | M2 broad-smoke `run_check` captures; selected-CI captures successful output by default. | medium | Covered by broad-smoke wrapper capture in M2; producer formatting deferred. |
| `scripts/validate-review-artifacts.py <changed roots>` | Validator success output for changed review roots when present. | Failure output names invalid review artifact structure or closeout issue. | broad-smoke conditional direct child; selected-CI when review artifacts are touched. | M2 broad-smoke `run_check` captures when changed roots exist; selected-CI captures successful output by default. | medium | Covered by broad-smoke wrapper capture in M2; producer formatting deferred. |
| `scripts/validate-artifact-lifecycle.py <derived scope>` | Validator success output for derived lifecycle scope. | Failure output names lifecycle artifact issue. | broad-smoke direct child; selected-CI when lifecycle artifacts are touched. | M2 broad-smoke `run_check` captures; selected-CI captures successful output by default. | medium | Covered by broad-smoke wrapper capture in M2; producer formatting deferred. |

## Orchestrator Paths

| Orchestrator path | Runs validation producers? | Current policy | First-slice treatment |
| --- | --- | --- | --- |
| selected-CI through `scripts/ci.sh --mode local`, explicit, PR, main, and release selected paths | yes | Captures successful child output by default; prints successful child output under `--verbose`; prints failed child output with check ID, status, exit reason, elapsed runtime, and command information. | Preserve and regression-test; no intentional behavior change in this slice. |
| broad-smoke through `scripts/ci.sh --mode broad-smoke` | yes | M2: `run_check` captures successful child stdout/stderr by default, prints aggregate broad-smoke success, and emits captured child output on failure or under `--verbose`. | M2 completed; M4 must preserve final evidence. |
| broad-smoke selected delegation through `broad_smoke.repo` | yes | selected-CI captures the outer `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped` child; M2 makes the inner broad-smoke `run_check` capture child output as well. | M2 completed; selected-CI outer behavior is preserved. |

## First Producer Decision

The first targeted direct-run producer is `scripts/test-change-metadata-validator.py`.

The audit does not record an approved replacement. Reasons:

- it is a named producer in the accepted proposal and approved spec;
- it is a broad-smoke direct child;
- it is run directly by maintainers and selected-CI when change metadata paths are touched;
- baseline direct success is verbose unittest output;
- current `--quiet` and `-q` are accepted and must be preserved as compatibility, not replaced with a custom compact quiet formatter in this slice.

## Broad-Smoke Baseline Command Identity

Baseline normalized command list:

- `broad-smoke-child-commands-baseline.txt`
- SHA-256: `8b1e4d0d7f36fccc0b7d0e2fa3ad5efedc39f7f41f935bb117c8c9f6eda9565f`

Extraction method:

1. Read the `run_broad_smoke` function in `scripts/ci.sh`.
2. Record each `run_check` label and command in execution order.
3. Normalize runtime-derived values:
   - `${adapter_release_output}` for the `mktemp -d` adapter output directory;
   - `${changed_review_roots}` for changed review-artifact roots;
   - `${tracked_authored_diff_paths}` for derived artifact-lifecycle explicit paths.
4. Hash the normalized tab-separated list with `sha256sum`.

This avoids hashing nondeterministic temp paths while preserving child command identity and order.

## Producer Baseline Test Identity

Baseline ordered unittest identifier list:

- `change-metadata-validator-tests-baseline.txt`
- Count: 18
- SHA-256: `fbb2230ef0c90ae64d7d0eb34966b994f318d8e042ca56fabaa4d39edbbe108e`

Extraction method:

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

M3 replay result:

- Count: 18
- SHA-256: `fbb2230ef0c90ae64d7d0eb34966b994f318d8e042ca56fabaa4d39edbbe108e`
- Replay note: the module is registered in `sys.modules` before `exec_module()` so the extraction remains compatible with the M3 dataclass runner.

## Quiet Compatibility Baseline

`python scripts/test-change-metadata-validator.py --quiet`:

- exit code: `0`
- stdout lines: `0`
- stderr lines: `4`
- stderr shape: normal unittest quiet success summary, including `Ran 18 tests ... OK`

`python scripts/test-change-metadata-validator.py -q`:

- exit code: `0`
- stdout lines: `0`
- stderr lines: `4`
- stderr shape: normal unittest quiet success summary, including `Ran 18 tests ... OK`

## M1 Conclusion

M1 finds no reason to replace the first targeted producer. M2 should fix broad-smoke success noise at the wrapper layer. M3 should compact `scripts/test-change-metadata-validator.py` default and verbose output while preserving the existing unittest-compatible quiet invocations.

## M2 Update

M2 fixed the broad-smoke wrapper layer by changing `run_check` to capture child output and emit a single aggregate success line. The producer matrix remains otherwise unchanged; `scripts/test-change-metadata-validator.py` remains the M3 producer target.

## M3 Update

M3 fixed the first direct-run producer layer by replacing the default verbose unittest runner with a compact default runner for `scripts/test-change-metadata-validator.py`. The selected test list remains unchanged at 18 tests with SHA-256 `fbb2230ef0c90ae64d7d0eb34966b994f318d8e042ca56fabaa4d39edbbe108e`. The producer still accepts `--verbose`, `-v`, `--quiet`, and `-q`; quiet mode remains the existing unittest-compatible behavior rather than a custom compact quiet formatter.

## M4 Final Evidence Update

M4 recomputed the final broad-smoke child-command identity proof and producer selected-test identity proof:

- `broad-smoke-child-commands-post-m4.txt`: SHA-256 `8b1e4d0d7f36fccc0b7d0e2fa3ad5efedc39f7f41f935bb117c8c9f6eda9565f`
- `change-metadata-validator-tests-post-m4.txt`: SHA-256 `fbb2230ef0c90ae64d7d0eb34966b994f318d8e042ca56fabaa4d39edbbe108e`

Both hashes match the M1 baseline evidence.
