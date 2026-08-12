# Post-PR CI Correction

Date: 2026-08-12
Hosted run: `31575883158`
Failed check: `Governance: review evidence regressions`

The hosted PR gate reproduced locally with `python scripts/test-review-artifact-validator.py`. The review-stage semantic-presence test searched raw skill text for lowercase `required outcome`, while the simplified proposal-review skill retained the normative field label `Required outcome`. The contract requires the concept and preserves the capitalized output label; it does not require incidental prose capitalization.

The correction case-folds each review skill before checking the five semantic terms. This keeps the same required concepts, leaves exact parser and output labels unchanged, and prevents the test from becoming a capitalization-policy owner. The missed consumer is now classified as `test-only-incidental` in the literal-compatibility inventory.

Focused proof:

- `python scripts/test-review-artifact-validator.py` passed all 103 tests.
- `python scripts/test-skill-validator.py` passed all 311 tests with 16 documented skips.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-11-proposal-review-skill-simplification` passed.
- The exact current-base PR selector and `scripts/ci.sh` gate passed locally against the complete correction.
