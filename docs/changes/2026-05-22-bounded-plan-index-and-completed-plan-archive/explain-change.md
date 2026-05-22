# Bounded Plan Index and Completed-Plan Archive Explain Change

## Status

M2 implementation notes; final explain-change is completed in M6.

## M2 validator contract and fixtures

M2 adds structural validation for the approved plan-index archive contract before the historical migration runs.

The validator now detects explicit plan-body lifecycle markers, checks terminal plan conservation across `Done (recent)` and `Done (archive)`, rejects archive-only nonterminal plans, enforces the recent Done cap, validates terminal entry links, and enforces active supersession fields.

The test suite adds fixture-driven coverage for valid and invalid archive states, lifecycle marker contradictions and unknown values, legacy prose-only status with no terminal inference, and active supersession context.

## Validation

- `python scripts/test-artifact-lifecycle-validator.py` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/plan-index-lifecycle-ownership.md --path specs/plan-index-lifecycle-ownership.test.md` passed with the existing lifecycle-language warning in the spec.
- `python -m py_compile scripts/artifact_lifecycle_validation.py scripts/artifact_lifecycle_contracts.py` passed.
- `git diff --check --` passed.
