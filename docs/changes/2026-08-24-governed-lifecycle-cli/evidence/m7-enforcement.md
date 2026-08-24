# M7 CI Enforcement Evidence

Milestone: M7
Validation result: passed
Subject: commit `77fe9f11`

## Enforcement boundary

- `scripts/ci.sh` runs wrapper regression tests and the public governed lifecycle validation wrapper in direct product gates.
- The wrapper enumerates all 28 records using `stage-owned-change-local-v1` and invokes `rigorloop lifecycle validate --change <id> --format json` for each one.
- The only accepted baseline warning is change `2026-08-05-activate-boundary-first-v1-v0-3-7`, and only when its status, empty error set, blocker-code set, and ten known unresolved finding IDs match exactly.
- Any new error, blocker shape, finding identity, invalid JSON result, or other failing change blocks CI.

## Validation

- `python3 scripts/test-governed-lifecycle-cli-validator.py`: passed, 3 tests.
- `python3 scripts/validate-governed-lifecycle-cli.py`: passed, 28 changes validated, one exact known baseline warning, zero failures.
- `python3 scripts/test-artifact-lifecycle-validator.py`: passed, 170 tests.
- `python3 scripts/test-change-metadata-validator.py`: passed, 63 tests.
- `python3 scripts/test-review-artifact-validator.py`: passed, 103 tests.
- `bash -n scripts/ci.sh`: passed.

This activates repository CI enforcement of the public lifecycle interpreter. It does not claim malicious-maintainer resistance, hosted authorization, PR execution, or workflow routing authority.
