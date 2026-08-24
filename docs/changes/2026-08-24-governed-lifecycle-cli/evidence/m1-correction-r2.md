# M1 Review Correction Evidence R2

## Scope

This bounded correction closes `RLCLI-CR-M1-3` without changing the operation vocabulary, revision exclusion set, or any M2-M7 behavior.

## Correction

- Admitted only `actor` and `recorded_at` as common optional mutation-request provenance.
- Required `actor` to be a non-empty string.
- Required `recorded_at` to be a structurally and calendrically valid RFC 3339 timestamp with a bounded UTC offset.
- Retained fail-closed rejection for every other request field.

## Artifact identities

- `packages/rigorloop/dist/lib/lifecycle-contract.js`: `sha256:844f053761a9ce1f30a1516f206ee2ee6701ba123deed0783cae23ee16546f22`
- `packages/rigorloop/test/lifecycle-contract.test.js`: `sha256:599465764de42bafe338657467a50c223fedab5e8ef88a8ea1992eb2156852b6`

## Validation

- `node --test packages/rigorloop/test/*.test.js`: passed, 139 tests.
- `python3 scripts/test-lifecycle-cli-conformance.py`: passed, six invalid YAML fixtures and ten protected failure classes.
- `python3 scripts/validate-change-metadata.py docs/changes/2026-08-24-governed-lifecycle-cli/change.yaml`: passed.
- `python3 scripts/validate-review-artifacts.py docs/changes/2026-08-24-governed-lifecycle-cli`: passed with nine reviews, nine findings, nine log entries, and nine resolution entries.

## Handoff

The documented request-provenance partition now has positive and fail-closed regressions. Formal rereview still owns M1 settlement.
