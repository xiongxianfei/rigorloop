# M4 Evidence Registration and Settlement Evidence

## Delivered

- Public versioned request-file handling for review, validation, finding-resolution, and settlement operations.
- Exact artifact, review, validation subject, review-log, resolution, and evidence SHA-256 registration in `change.yaml`.
- Review/outcome/round/finding-set, validation-subject, resolution-disposition/owner/proof, and stage-authority validation.
- Settlement derived from the registered current review outcome with stale, contradictory, unresolved, wrong-authority, and stale-request refusal.
- Current-revision idempotency and deterministic dry-run plans.
- All mutation flows use the M3 guarded transaction and change only `change.yaml`.

## Validation

- `node --test packages/rigorloop/test/lifecycle-evidence.test.js`: passed, three integration tests.
- `npm test --prefix packages/rigorloop`: passed, 152 tests.
- `python3 scripts/test-review-artifact-validator.py`: passed, 103 tests.
- `python3 scripts/test-artifact-lifecycle-validator.py`: passed, 170 tests.
- `python3 scripts/validate-npm-package.py`: passed.

## Authority boundary

The CLI verifies and records stage-authored judgment but does not author or revise semantic Markdown. Registration does not settle, settlement does not route, and no request accepts a target lifecycle state.
