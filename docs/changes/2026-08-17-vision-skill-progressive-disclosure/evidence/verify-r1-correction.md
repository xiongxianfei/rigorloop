# Verify R1 correction: material-finding discovery

## Failure

Final PR-mode CI stopped in lifecycle validation because the detailed records for `VIS-M2-CR1` and `VIS-FINAL-CR1` used heading-only identities. The review log and resolution referenced both IDs, but the repository parser discovers material findings through the explicit `Finding ID:` field.

The semantic findings, evidence, required outcomes, safe resolutions, dispositions, and approving rereviews were already present. The defect was structural discoverability and one stale closeout-evidence sentence.

## Correction

- Added explicit parser-owned `Finding ID`, `Severity`, and `Location` fields to both detailed review records.
- Preserved the existing finding IDs, judgments, evidence, required outcomes, safe resolutions, dispositions, and lifecycle effects.
- Reconciled the `VIS-FINAL-CR1` validation-evidence sentence with the completed `code-review-final-r3` rereview.
- Added explicit closeout links from both blocking review occurrences to their already recorded same-stage approving rereviews.
- Did not modify the vision package, focused tests, specification, plan, or test specification.

## Focused proof

The correction must pass review-artifact structure and closeout validation, PR-scope lifecycle validation, change metadata validation, and a fresh final holistic code review before verification can be retried.
