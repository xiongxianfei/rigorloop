# M2 Proposal Validation and Compatibility Evidence

Milestone: M2
Validation result: passed

## Result

- Skill: implement
- Status: implemented
- Completed scope: Added current simplified-proposal structure validation, governed ownership without a reverse document pointer, settled legacy readability, unsettled legacy rejection, and closed Proposal Review vision-alignment validation.
- Artifacts changed: `scripts/artifact_lifecycle_contracts.py`, `scripts/artifact_lifecycle_validation.py`, `scripts/review_artifact_validation.py`, and their focused test modules.
- Tests added or updated: Current ordinary, material-impact, nested, portable, and governed proposals; missing, duplicate, misordered, unknown, empty-feasibility, forbidden-status, reverse-pointer, routine-vision, and governed-path-mismatch failures; untouched settled, changed settled, and unsettled legacy behavior; all four vision outcomes plus missing, duplicate, and unknown outcomes.
- Open blockers: none
- Next stage: code-review
- Claim limitations: M2 does not generate or validate adapter archives, perform M3 cutover parity, close the milestone lifecycle state, or claim final verification or PR readiness.

## Compatibility boundary

- Simplified shape is validated as the current seven-section contract.
- Portable proposal paths dated from the cutover boundary use the simplified contract without requiring `change.yaml`.
- Governed proposals obtain status and ownership only from the exact primary proposal entry in `change.yaml`; the proposal contains no reverse pointer.
- Unsettled governed legacy proposals must adopt the simplified contract before settlement.
- Settled pre-cutover legacy proposals remain readable under the prior contract and are not rewritten.
- Proposal Review receipts after the compatibility boundary require exactly one closed-vocabulary vision-alignment outcome. Existing settled review evidence remains readable.
- No document-version marker, per-document hash, compatibility document, lifecycle field, or CLI command was introduced.

## Proof results

- `python scripts/test-artifact-lifecycle-validator.py`: passed, 155 tests.
- `python scripts/test-review-artifact-validator.py`: passed, 107 tests.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-08-30-simplify-rigorloop-proposal-contract.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md`: passed, one lifecycle artifact validated.
- `python scripts/validate-review-artifacts.py docs/changes/2026-08-30-simplify-rigorloop-proposal-contract`: passed, six reviews, one historical finding, six log entries, and one resolution entry.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/change.yaml`: passed.
- `python scripts/validate-boundary-first.py --check --path specs/simplified-proposal-contract.test.md`: passed.
- `git diff --check`: passed.

## Semantic ownership note

The deterministic review validator proves that one known vision outcome is present. Whether a material conflict is adequately disclosed and owner-resolved remains Proposal Review judgment under the approved skill contract; M2 does not duplicate that semantic decision in structural software.

## Test-first proof

The focused proposal tests initially failed because the legacy validator required embedded `Status` and legacy sections. The focused Proposal Review tests initially failed because no vision-outcome validator existed. Both focused sets and the full suites pass after the bounded implementation.

Code Review R1 then exposed two missing boundary cases. The correction uses the validator's existing selected-path scope to distinguish a changed settled governed proposal from an untouched proposal reached only through its change record. It also correlates an explicitly selected stage-owned change record with the same-named proposal before portable fallback is allowed. Direct regression tests now cover both cases without introducing document hashes, version markers, reverse pointers, or a new command.
