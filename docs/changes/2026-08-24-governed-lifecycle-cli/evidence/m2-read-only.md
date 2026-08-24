# M2 Read-Only Lifecycle Evidence

## Delivered

- Added governed change discovery with explicit and single-active selection.
- Added one immutable interpreter for effective status, artifact identities, stale evidence, blockers, permitted operations, and lifecycle revision.
- Added bounded stage context and repository validation views.
- Exposed `rigorloop lifecycle status`, `context <stage>`, and `validate` with human and JSON output from the same result.
- Kept mutation commands unexposed.

## Validation

- `node --test packages/rigorloop/test/lifecycle-read.test.js packages/rigorloop/test/lifecycle-contract.test.js`: passed, 26 tests.
- `npm test --prefix packages/rigorloop`: passed, 143 tests.
- `python3 scripts/validate-npm-package.py`: passed.
- `python3 scripts/test-npm-package-publication.py -k package_policy`: passed, one test.
- `npm audit --prefix packages/rigorloop --audit-level=moderate`: passed with zero vulnerabilities.
- Real-repository `lifecycle status --change 2026-08-24-governed-lifecycle-cli --format json`: success with no blockers or errors.

## Boundaries

Diagnostics contain repository-relative paths and stable identities, not absolute paths or environment values. Read commands perform no writes. Evidence inference remains structural and does not claim semantic approval.
