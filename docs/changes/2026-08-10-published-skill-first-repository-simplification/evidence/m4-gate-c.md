# M4 Gate C Evidence

## Result

`validate-release.py` now emits the stable `Gate C (release integrity)` owner
on success, warnings, recorded-source results, archive-safety failures, and
ordinary validation failures. `release-verify.sh` composes the public gates in
this order:

1. Gate A canonical skill integrity;
2. generated-skill currency and Gate B adapter regression/build proof;
3. npm package content and filesystem materialization when applicable; and
4. Gate C release metadata, archive artifacts, notes, checksums, security, and
   release/rollback consistency.

The shell wrapper uses `set -euo pipefail`, so an underlying Gate A or Gate B
failure stops immediately under that owner's diagnostic rather than being
reinterpreted as release-only correctness.

## Runtime exclusion

A direct command-graph test inspects and rehearses the real wrapper. It rejects
prospective use of `codex exec`, `claude --`, `opencode run`, transcript
analysis, model matrices, and dynamic benchmark runners. The wrapper contains
none of those commands. Its “smoke” wording was narrowed to filesystem
materialization; historical release records and public CLI-init evidence remain
readable and are not rewritten.

The only version-specific token-cost validation retained by the wrapper is the
existing static report-shape check for historical v0.1.1. M4 neither executes a
model benchmark nor makes historical dynamic results a new-release oracle.

## Test-first evidence

The new failure-owner test initially received only `unsupported release target:
v9.9.9`. After the smallest existing-owner change, the same failure reports
`Gate C (release integrity): unsupported release target: v9.9.9`. The command
composition/runtime-exclusion test passed before and after the label change.

## Validation

- `python scripts/test-release-transaction.py` — pass; 104 tests in 3.242 seconds.
- `python scripts/validate-release.py --recorded-source-auto --version v0.4.0` — pass; local archives rebuilt from recorded commit `c7b0babe6e8c91655c2b98f4092197eef5fabc69` and validated by Gate C.
- `RELEASE_VERIFY_DRY_RUN=1 RELEASE_OUTPUT_DIR=/tmp/tmp.6LiXjIPWLb RELEASE_COMMIT=fixture-commit bash scripts/release-verify.sh v0.4.0` — pass; the real wrapper selected every required local command in Gate A/B/C order and published nothing.
- `python scripts/test-adapter-distribution.py` — pass in current M3 evidence; 150 tests. M4 changes no adapter code, fixtures, or generated package surface.
- Targeted deterministic Gate C tests — pass; composition order/runtime exclusion and failure-owner output.

The dry-run output directory was temporary and empty; no tag, push, registry
write, network publication, target runtime, prompt, or transcript was used.

## Metrics and rollback

M4 changes two existing release entry points and adds two tests; it adds no new
CLI or parser. Gate C remains one composition boundary. Revert the M4 commit to
restore the prior labels and wording; validation semantics, historical release
evidence, adapter formats, and public artifacts remain unchanged.
