# Release Transaction Automation Review Resolution

## Scope

This record tracks review finding closeout for the release transaction automation change.

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: spec-review-r1
Review closeout: architecture-review-r1
Review closeout: plan-review-r1
Review closeout: test-spec-review-r1
Review closeout: test-spec-review-r2
Review closeout: test-spec-review-r3
Review closeout: code-review-m1-r1
Review closeout: code-review-m2-r1

## Resolution Entries

### proposal-review-r1

No material findings.

### spec-review-r1

No material findings.

### architecture-review-r1

No material findings.

### plan-review-r1

No material findings.

### test-spec-review-r1

Finding ID: RTA-TSR1
Disposition: accepted
Status: resolved
Owner: maintainer
Owning stage: test-spec revision
Rationale: The active plan requires test-spec-review to approve these proof-contract details before implementation, and the current test spec defers them to implementation.
Required outcome: The test spec must define, or explicitly constrain with testable compatibility rules, generated-region marker behavior, literal-audit baseline artifact shape, timing evidence field names, and fixture layout enough for implementation without proof-semantics guessing.
Chosen action: Added a proof-contract section to `specs/release-transaction-automation.test.md` defining generated-region marker syntax, allowed generated surface IDs, literal-audit baseline schema and closed enums, timing evidence schema and phase/result values, fixture layout, local/stubbed execution boundaries, and proof tests.
Validation target: `test-spec-review-r2` approved the revised test spec with no material findings.
Validation evidence: `test-spec-review-r2` passed with no material findings after confirming the revised test spec defines generated-region marker syntax, generated surface IDs, literal-audit baseline schema and enums, timing evidence schema and enums, fixture layout, and `TRTA-GEN-*`, `TRTA-LIT-*`, `TRTA-TIME-*`, and `TRTA-FIX-*` proof tests.

Finding ID: RTA-TSR2
Disposition: accepted
Status: resolved
Owner: maintainer
Owning stage: test-spec revision
Rationale: Implementation needs a command ownership and activation matrix before it can rely on the proof map; the current test spec leaves existing versus planned commands ambiguous.
Required outcome: The test spec must provide a validation command matrix that classifies existing, planned, manual-only, and external/release-owned commands with owner milestone, activation point, safe-mode expectations, and missing/zero-test behavior.
Chosen action: Added an implementation-handoff command matrix classifying existing, planned, manual-only, and external/release-owned command families, including owner milestone, activation point, missing-command behavior, safe/dry-run expectations, zero-test behavior, CI workflow static checks, public `npx` smoke ownership, and explicit handling for absent `python scripts/test-release-validation.py`.
Validation target: `test-spec-review-r2` approved the revised test spec with no material findings.
Validation evidence: `test-spec-review-r2` passed with no material findings after confirming the revised test spec includes the implementation-handoff command matrix, command ownership rules, `TRTA-CMD-*` proof tests, and explicit handling for absent `python scripts/test-release-validation.py`.

### test-spec-review-r2

No material findings.

### test-spec-review-r3

No material findings.

### code-review-m1-r1

Finding ID: CR-RTA-M1-F1
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement
Rationale: The finding identifies a direct proof gap against `specs/release-transaction-automation.test.md` `RTA-T001` and the active plan M1 test list.
Required outcome: M1 must add direct tests and fixtures for the required missing profile and missing required profile-field failures, or revise the approved test spec and plan before claiming M1 review closeout.
Chosen action: Added focused negative fixtures and assertions in `scripts/test-release-transaction.py` for missing profile path, missing `release_tag`, missing `package_version`, missing `npm_package`, missing `adapter_artifacts`, missing `publication`, missing `evidence`, and missing `validation`. The existing missing `targets` case remains in the table-driven required-field coverage.
Validation target: Rerun `python scripts/test-release-transaction.py`, `python scripts/validate-release.py --help`, selector explicit routing, change metadata validation, lifecycle explicit-path validation, review artifact validation, and whitespace validation before rerunning `code-review M1`.
Validation evidence: `python scripts/test-release-transaction.py` passed after the targeted fix: 11 tests. Remaining lifecycle validation is recorded in the active plan and change metadata.

### code-review-m1-r2

No material findings. No resolution entry is required for this clean review round.

### code-review-m2-r1

Finding ID: CR-RTA-M2-F1
Disposition: accepted
Status: resolved after implementation
Owner: implementer
Owning stage: implement
Rationale: The finding identifies a direct proof gap against the approved literal-audit proof contract.
Required outcome: Add a direct literal-audit negative fixture and test proving an entry missing `classification` fails with a diagnostic naming `classification`.
Chosen action: Added `tests/fixtures/release-transaction/literal-audit/invalid-missing-classification.yaml` and a focused `LiteralAuditBaselineTests` assertion proving an entry missing `classification` fails with a diagnostic naming `literal audit entry literal-baseline-001` and `classification`.
Validation target: Rerun M2 focused release transaction tests and lifecycle validation after the targeted fixture/test fix.
Validation evidence: `python scripts/test-release-transaction.py` passed with 23 tests. Existing literal-audit negative tests for unknown classification, changed unauthorized literal, historical fixture without rationale, and generated-current without owner remain green.

Finding ID: CR-RTA-M2-F2
Disposition: accepted
Status: resolved after implementation
Owner: implementer
Owning stage: implement
Rationale: The finding identifies an incomplete surface ownership inventory and a direct proof gap against the approved M2 surface-classification test case.
Required outcome: Add prior profile snapshots to the M2 surface inventory and valid fixture as a `historical-immutable` surface, and add a direct negative fixture/test proving an unclassified surface fails with an owner/classification diagnostic.
Chosen action: Added prior profile snapshots as a `historical-immutable` surface in the change-local release surface inventory and valid fixture. Added `tests/fixtures/release-transaction/surface-inventory/invalid-missing-classification.yaml` and a focused `ReleaseSurfaceInventoryTests` assertion proving a surface missing `classification` fails with a diagnostic naming `prior-profile-snapshots` and `classification`.
Validation target: Rerun M2 focused release transaction tests and lifecycle validation after the targeted inventory and fixture/test fix.
Validation evidence: `python scripts/test-release-transaction.py` passed with 23 tests. No release preparation, preflight, publication closeout, release verification, CI workflow, or generated evidence behavior changed in this M2 resolution.

### code-review-m2-r2

No material findings. No resolution entry is required for this clean review round.
