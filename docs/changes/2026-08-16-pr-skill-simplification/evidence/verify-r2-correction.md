# Verify R2 correction: historical review-record structure

## Failure

The corrected PR skill contract passed its focused and broad checks, but final
PR-mode CI stopped in lifecycle validation. The two historical
`test-spec-review` records did not expose the current required top-level result
fields, and the material findings in the first spec and test-spec reviews used
bulleted labels that the current review-artifact parser does not treat as
finding fields.

The semantic review outcomes, finding IDs, dispositions, and recorded evidence
were already present. The defect was structural discoverability under the
current durable review contract.

## Correction

- Added `Status`, `Review status`, `Material findings`, `Recording status`,
  `Immediate next stage`, and `Implementation handoff` to the two
  `test-spec-review` receipt headers.
- Converted `PRSSIM-SR1` and `TSPRSIM-TSR1` from bulleted field labels to the
  parser-owned field form without changing their text or dispositions.
- Did not change either historical judgment, settlement outcome, or lifecycle
  transition.

## Focused proof

`python scripts/validate-artifact-lifecycle.py --mode pr-ci --base origin/main --head HEAD`
passed and validated the three change-local artifact files selected by PR scope.
Repository-baseline missing-Status warnings remain warnings and are outside this
change.
