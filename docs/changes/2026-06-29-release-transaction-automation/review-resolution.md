# Release Transaction Automation Review Resolution

## Scope

This record tracks review finding closeout for the release transaction automation change.

Closeout status: open

Review closeout: proposal-review-r1
Review closeout: spec-review-r1
Review closeout: architecture-review-r1
Review closeout: plan-review-r1
Review closeout: test-spec-review-r1
Review closeout: test-spec-review-r2
Review closeout: test-spec-review-r3
Review closeout: code-review-m1-r1
Review closeout: code-review-m2-r1
Review closeout: code-review-m3-r1
Review closeout: code-review-m4-r1
Review closeout: code-review-m4-r2
Review closeout: code-review-m5-r1

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

### code-review-m3-r1

Finding ID: CR-RTA-M3-F1
Disposition: accepted
Status: resolved after implementation
Owner: implementer
Owning stage: review-resolution
Rationale: The finding identifies a direct M3 contract and proof gap against `R17`, `RTA-T006`, and `RTA-T010`: pending evidence validation can accept malformed target evidence because it searches for global fragments rather than validating target-specific pending values.
Required outcome: Add direct M3 proof that invalid pending evidence fails pre-publication validation, and strengthen the validator so target-specific malformed pending values cannot pass because another target contains a valid fragment.
Chosen action: Reworked pending npm-publication validation so target-init smoke evidence is extracted from the generated YAML block and validated per target. The validator now checks the expected target set from the release profile, rejects missing, duplicate, and unknown targets, validates target-specific command, npm version, result, and closeout blocking fields, and compares the Markdown table projection against the canonical YAML target data. Added temporary-repository negative tests proving a published target result, `npx -y` command shape, missing target, duplicate target, unknown target, and table/YAML result mismatch fail with target-specific diagnostics.
Validation target: Rerun `python scripts/test-release-transaction.py`, `python scripts/prepare-release.py --help`, M3 lifecycle validation, review artifact validation, and whitespace validation after the targeted fix.
Validation evidence: `python scripts/test-release-transaction.py` passed with 34 tests, including the new M3 pending-evidence negative tests. `python scripts/prepare-release.py --help`, `python -m py_compile scripts/release_transaction.py scripts/test-release-transaction.py scripts/prepare-release.py`, and `git diff --check --` passed. `python scripts/select-validation.py --mode explicit --path scripts/release_transaction.py --path scripts/prepare-release.py --path scripts/test-release-transaction.py --path tests/fixtures/release-transaction/evidence` reported manual routing for release transaction scripts and an unclassified static evidence fixture path; this M3 resolution uses temporary generated repository fixtures and `python scripts/test-release-transaction.py` as the approved focused proof.

### code-review-m3-r2

No material findings. No resolution entry is required for this clean review round.

### code-review-m4-r1

Finding ID: CR-RTA-M4-F1
Disposition: accepted
Status: resolved after implementation
Owner: implementer
Owning stage: review-resolution
Rationale: The review found that the preferred `python scripts/release-preflight.py <tag>` command can pass when an unauthorized current-version literal is present in the literal-audit baseline unless the caller explicitly supplies `--changed-file`.
Required outcome: The default M4 preflight command must detect newly changed unauthorized literals under normal CLI usage, or the governing command contract must be revised before M4 closeout.
Chosen action: Added Git changed-file discovery for the default CLI path. When `--changed-file` is absent, `scripts/release-preflight.py` now derives changed files from Git staged, unstaged tracked, and untracked paths. Explicit `--changed-file` remains an override for deterministic fixture tests. The CLI fails clearly when changed files cannot be derived from Git.
Validation target: Rerun M4 focused tests, `python scripts/release-preflight.py --help`, Python compilation, lifecycle validation, review artifact validation, and whitespace validation after resolution.
Validation evidence: `python scripts/test-release-transaction.py` passed with 50 tests, including CLI-level coverage for default Git discovery catching an unauthorized changed literal and non-Git roots failing without explicit `--changed-file`. `python scripts/release-preflight.py --help` and Python compilation passed.

Finding ID: CR-RTA-M4-F2
Disposition: accepted
Status: resolved after implementation
Owner: implementer
Owning stage: review-resolution
Rationale: The review found direct preflight tests for several M4 failures, but not for malformed profile, incomplete profile, or missing required local input, which are named by the active plan and approved test spec.
Required outcome: Add direct proof for the missing M4 preflight negative cases, or revise the approved artifacts before claiming M4 closeout.
Chosen action: Added direct M4 preflight negative tests for malformed profile, incomplete profile, and missing required local input. The tests exercise the preflight path and assert diagnostics naming the profile parse failure, missing profile field, or missing metadata input path.
Validation target: Rerun M4 focused tests, lifecycle validation, review artifact validation, and whitespace validation after resolution.
Validation evidence: `python scripts/test-release-transaction.py` passed with 50 tests. Existing M4 clean fixture, package mismatch, metadata pointer drift, invalid pending evidence, dirty `release-output`, helper-level changed unauthorized literal, local tag conflict, unreachable remote warning, and reachable remote conflict tests remain green.

### code-review-m4-r2

No material findings. No resolution entry is required for this clean review round.

### code-review-m5-r1

Finding ID: CR-RTA-M5-F1
Disposition: needs-decision
Status: open
Owner: implementer
Owning stage: review-resolution
Decision owner: implementer
Decision needed: Accept and wire timing evidence validation into the profile-required release validation path, or revise the approved spec/test spec to allow helper-only timing validation.
Rationale: The review found that M5 added a timing validation helper and helper-level tests, but the repository-owned release validation command used by the full release gate does not call it.
Required outcome: Missing timing evidence must fail through the profile-required release validation path when the release profile requires timing.
Chosen action: pending
Validation target: Rerun M5 focused tests, command-level release validation timing regression, release-verify dry-run, Python compilation, selector-selected validation, lifecycle validation, review artifact validation, and whitespace validation after resolution.
Validation evidence: pending
