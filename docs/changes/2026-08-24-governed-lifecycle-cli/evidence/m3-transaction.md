# M3 Transaction and Recovery Evidence

## Delivered

- Exact expected-revision rejection before filesystem mutation.
- Fixed sibling lock and recovery paths with exclusive `0600` creation.
- Fsynced candidate, recovery, replacement, phase update, directory, and cleanup ordering.
- Complete prior bytes, prior/candidate hashes, nonce, phase, candidate filename, and original file mode in the recovery bundle.
- Automatic byte-exact restoration after post-validation failure.
- Identity-based reconciliation of interrupted prepared and replaced states.
- Live-lock rejection and orphan/unverifiable-lock refusal pending the named M5 repair.

## Validation

- `node --test packages/rigorloop/test/lifecycle-transaction.test.js`: passed, five tests.
- `npm test --prefix packages/rigorloop`: passed, 149 tests.
- `python3 scripts/validate-npm-package.py`: passed.

The suite covers successful replacement, stale and live-lock refusal, post-validation restoration, pre-replacement interruption, post-replacement interruption, private transient modes, original durable mode preservation, and transient cleanup.

## Exposure

The transaction adapter is internal. Public mutation commands remain unavailable until semantic transitions are implemented and reviewed.
