# Script Output Optimization Audit

Change ID: `2026-05-21-script-output-optimization`
Date: 2026-05-21
Milestone: M1 audit and baseline preservation evidence

## Scope

This audit records the first-slice script-output boundary before output shaping begins.

The first implementation target is `scripts/test-select-validation.py`. `scripts/ci.sh` remains conditional: it is touched only if post-runner-change evidence shows the wrapper must change to preserve quiet-success and loud-failure behavior.

## Candidate scripts

| Script path | User-facing? | Current success lines | Current failure usefulness | Proposed treatment | First-slice? |
| --- | --- | ---: | --- | --- | --- |
| `scripts/test-select-validation.py` | yes | 67 stderr lines for a passing 62-test run; individual `... ok` line per test plus unittest footer | Current unittest failures include failed name, error class/message, traceback/location when applicable, count, and nonzero exit; no scoped rerun guidance | summary mode in first slice; add default compact success, default actionable failure shaping, `--verbose`, `--quiet`, zero-test safety, and reliable-only rerun behavior | yes |
| `scripts/ci.sh` | yes | 10 stdout lines for selected pass without wrapper `--verbose`; 81 stdout lines with wrapper `--verbose` for the same selected path | Existing wrapper selected-check failures are covered by `scripts/test-select-validation.py` regressions; wrapper reports selected check ID, status, exit reason, elapsed runtime, command, and captured failed output | wrapper-only conditional; leave unchanged unless M3 post-change proof shows a gap | conditional |

## Baseline observations

### `scripts/test-select-validation.py`

Command:

```bash
python scripts/test-select-validation.py
```

Result:

- exit code: `0`
- stdout lines: `0`
- stderr lines: `67`
- selected/executed tests: `62`
- footer: `Ran 62 tests in 7.175s` and `OK`
- current success shape: one line per passing test/check, for example `test_architecture_support_paths_route_without_manual_blocks (...) ... ok`

Command:

```bash
python scripts/test-select-validation.py --verbose
```

Result:

- exit code: `0`
- stdout lines: `0`
- stderr lines: `67`
- selected/executed tests: `62`
- current behavior: accepted by `unittest`; equivalent to current full pass-list output

Command:

```bash
python scripts/test-select-validation.py --json
```

Result:

- exit code: `2`
- current behavior: `unrecognized arguments: --json`
- first-slice implication: do not add new JSON support

Command:

```bash
python scripts/test-select-validation.py NoSuchTest
```

Result:

- exit code: `1`
- stdout lines: `0`
- stderr lines: `11`
- current failure shape: includes failed test identifier `NoSuchTest`, `ERROR`, exception type/message, count, and `FAILED (errors=1)`

### `scripts/ci.sh`

Command:

```bash
bash scripts/ci.sh --mode explicit --path scripts/test-select-validation.py --path scripts/ci.sh
```

Result:

- exit code: `0`
- stdout lines: `10`
- stderr lines: `0`
- selected check IDs: `selector.regression`
- current success shape: wrapper reports selector status, changed paths, selected check, summary row, and final pass line; child output is hidden by default

Command:

```bash
bash scripts/ci.sh --mode explicit --path scripts/test-select-validation.py --path scripts/ci.sh --verbose
```

Result:

- exit code: `0`
- stdout lines: `81`
- stderr lines: `0`
- selected check IDs: `selector.regression`
- current verbose shape: wrapper exposes successful child output in stable order

## First-slice decision

- Implement output shaping for `scripts/test-select-validation.py`.
- Preserve full pass/check detail behind script-local `--verbose`.
- Add script-local `--quiet` with silent success and visible non-success diagnostics.
- Keep `scripts/ci.sh` unchanged for now because baseline wrapper behavior already hides successful child output by default and exposes it with wrapper `--verbose`.
- Re-evaluate `scripts/ci.sh` after M3 runner output shaping; close M4 as no-code if the wrapper still satisfies the contract.

## JSON status

`scripts/test-select-validation.py` currently lacks `--json`. The first slice must not add JSON support. If a later script touched in this change has stable JSON support, that behavior must be separately recorded and preserved.

## M3 post-change observation

M3 changed `scripts/test-select-validation.py` only. The CI wrapper remains conditional for M4.

Command:

```bash
python scripts/test-select-validation.py
```

Result:

- exit code: `0`
- stdout lines: `1`
- stderr lines: `0`
- selected/executed tests: `73`
- current success shape: `[PASS] test-select-validation: 73 passed ...`

Command:

```bash
python scripts/test-select-validation.py --quiet
```

Result:

- exit code: `0`
- stdout lines: `0`
- stderr lines: `0`

Command:

```bash
python scripts/test-select-validation.py --verbose
```

Result:

- exit code: `0`
- current verbose shape: full unittest pass-list output remains available

Command:

```bash
python scripts/test-select-validation.py --json
```

Result:

- exit code: `2`
- current behavior: `unrecognized arguments: --json`
- first-slice implication: JSON support remains deferred
