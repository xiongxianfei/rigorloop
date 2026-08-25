# M1 Review Correction Evidence R1

## Scope

This bounded correction closes the two accepted findings from `code-review-m1-r1`. It does not expose a lifecycle command or implement behavior assigned to M2-M7.

## Corrections

- `RLCLI-CR-M1-1`: added a closed per-operation contract for all eight first-release mutations. Each operation now requires its complete request shape, validates identifiers and repository-relative paths, and rejects unknown authority, repair-condition, and operation values before transition consistency.
- `RLCLI-CR-M1-2`: froze `actor` and `recorded_at` as the version-one provenance exclusion set in the shared conformance fixture. Revision canonicalization strips only those keys recursively; mutation-relevant state still changes the revision.

## Artifact identities

- `packages/rigorloop/dist/lib/lifecycle-contract.js`: `sha256:3461e64b7178dbaa59e202876501b3cb250e4117a0727e64ffcda07a0e07b5a2`
- `packages/rigorloop/test/fixtures/lifecycle/conformance-v1.json`: `sha256:2aaca3487414c9cb0adb37b2025fdaede131c3c5d0fbb73ce98e12a24a4bf5ee`
- `packages/rigorloop/test/lifecycle-contract.test.js`: `sha256:26335d80d6c23fc728c3d77b458f1e44f06064c6797336f3fc0fd17c98ecc09d`
- `scripts/test-lifecycle-cli-conformance.py`: `sha256:6f7b7dfc67dd0a7c4d6a66ac687842830ee633b67d4dfc82630fe3358ba42b33`

## Validation

- `node --test packages/rigorloop/test/lifecycle-contract.test.js`: passed, 21 tests.
- `python3 scripts/test-lifecycle-cli-conformance.py`: passed, six invalid YAML fixtures and ten protected failure classes.
- `node --test packages/rigorloop/test/*.test.js`: passed, 138 tests.
- `python3 scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`: passed for the five M1 lifecycle artifacts.
- `python3 scripts/validate-change-metadata.py docs/changes/2026-08-24-governed-lifecycle-cli/change.yaml`: passed.
- `python3 scripts/validate-review-artifacts.py docs/changes/2026-08-24-governed-lifecycle-cli`: passed with eight reviews, eight findings, eight log entries, and eight resolution entries.

## Handoff

Both accepted M1 findings have direct regression evidence and are ready for formal rereview. Milestone closure remains owned by code review and workflow routing.
