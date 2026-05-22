# Compact Change Validation Metadata Review Resolution

## Summary

Closeout status: closed

Review closeout: spec-review-r1
Review closeout: code-review-m2-r1

## Resolution Entries

### code-review-m3-r1

## Findings

#### CVM-M3-CR1

Finding ID: CVM-M3-CR1
Disposition: accepted
Status: resolved
Owner: implement
Owning stage: review-resolution
Chosen action: Reject compact summary blocker entries that are not derived from non-pass validation events.
Rationale: M3 currently checks for missing blockers but allows arbitrary extra blockers, leaving stored summary data inconsistent with event-derived truth.
Required outcome: Compact validation rejects `open_validation_blockers` entries that do not correspond to non-pass events requiring blocker representation.
Safe resolution path: Derive expected blocker stages from `validation_events`, compare stored blocker stages exactly against that derived set, and add an invalid fixture proving all-pass events with an extra blocker fail.
Validation target: `scripts/test-change-metadata-validator.py` includes an invalid extra-blocker fixture and `scripts/validate-change-metadata.py` rejects it with a stable summary-drift diagnostic.
Resolution: Updated compact summary validation to derive expected blocker stages from `validation_events` and reject both missing blockers and extra blockers not derived from event truth. Added `compact-invalid-extra-summary-blocker` to prove all-pass events with an arbitrary summary blocker fail validation.
Validation evidence: `python scripts/test-change-metadata-validator.py` passed, and `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-invalid-extra-summary-blocker/change.yaml` failed as expected with `extra blocker not derived from validation_events: fake-blocker`.

#### CVM-M3-CR2

Finding ID: CVM-M3-CR2
Disposition: accepted
Status: resolved
Owner: implement
Owning stage: review-resolution
Chosen action: Replace the inline compactness measurement with representative reconstruction-gated fixture proof.
Rationale: The current compactness test measures inline strings that are not a valid compact common-read fixture and does not prove reconstruction preservation before the 30% threshold.
Required outcome: M3 proves material compactness on a representative high-rerun legacy/compact fixture or equivalent tracked fixture surfaces only after compact reconstruction preservation passes.
Safe resolution path: Add a representative legacy/compact fixture pair or equivalent tracked fixture surfaces, validate/reconstruct the compact evidence first, then assert the compact common-read surface is at least 30% smaller.
Validation target: `scripts/test-change-metadata-validator.py` proves reconstruction passes before evaluating compactness and reports the measured reduction for a representative high-rerun fixture.
Resolution: Replaced the inline-string compactness proof with representative legacy and compact fixture files. The test now validates both fixtures, reconstructs the compact accumulated lifecycle path set through `reconstruct_compact_path_sets`, and only then measures the compact common-read surface against the legacy common-read validation surface.
Validation evidence: `python scripts/test-change-metadata-validator.py` passed, including `test_compact_common_read_reduction_helper`. Direct fixture validation passed for `tests/fixtures/change-metadata/compactness-representative-compact/change.yaml` and `tests/fixtures/change-metadata/compactness-representative-legacy/change.yaml`.

#### CVM-M3-CR3

Finding ID: CVM-M3-CR3
Disposition: accepted
Status: resolved
Owner: implement
Owning stage: review-resolution
Chosen action: Make the no-execution sentinel command create the sentinel if it is ever executed.
Rationale: The current sentinel command raises a Python error if run and would not create the sentinel file, so the test passes even under the command-execution regression it is meant to detect.
Required outcome: The no-execution proof fails if metadata validation executes bundle commands.
Safe resolution path: Replace the inert sentinel command with a valid compact command string that writes a repo-relative sentinel file if executed, then assert validation leaves the file absent.
Validation target: `scripts/test-change-metadata-validator.py::test_compact_validator_does_not_execute_bundle_commands` would fail if bundle commands are executed during metadata validation.
Resolution: Replaced the inert no-execution sentinel command with a valid compact command string that writes `tests/fixtures/change-metadata/compact-command-sentinel` if executed. The test removes the sentinel before validation, validates metadata, and asserts the sentinel remains absent.
Validation evidence: `python scripts/test-change-metadata-validator.py` passed, including `test_compact_validator_does_not_execute_bundle_commands`.

### code-review-m2-r1

## Findings

#### CVM-M2-CR1

Finding ID: CVM-M2-CR1
Disposition: accepted
Status: resolved
Owner: implement
Owning stage: review-resolution
Chosen action: Add compact bundle-command safety validation and a focused unsafe-command regression fixture.
Rationale: The approved spec's security/privacy boundary includes bundle commands, but the M2 implementation only safety-checks path variables, event paths, and transcript references.
Required outcome: Compact validation rejects unsafe bundle command strings containing machine-local paths, hostnames, credentials, proxy URLs, or secret-like values, without executing commands or changing selected validation behavior.
Safe resolution path: Add a fixture with an unsafe `validation_bundles.<id>.command`, assert the validator rejects it, extend bundle validation to apply the approved safety checks to command strings, and rerun M2 targeted validation.
Validation target: `scripts/test-change-metadata-validator.py` includes an unsafe bundle-command fixture, and `scripts/validate-change-metadata.py` rejects that fixture with a stable actionable message.
Resolution: Extended compact bundle validation to run string-level command safety checks against `validation_bundles.<id>.command`. The validator now rejects unsafe machine-local paths, credential-bearing URLs, and secret-like values without executing bundle commands or changing command-selection behavior. Added fixture-backed coverage for unsafe local paths, credential-bearing URLs, secret-like command tokens, and a valid repo-relative command with a compact path variable.
Validation evidence: `python scripts/test-change-metadata-validator.py`, `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-valid/change.yaml`, `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/valid-basic/change.yaml`, direct expected-failure checks for `compact-invalid-unsafe-bundle-command-local-path`, `compact-invalid-unsafe-bundle-command-credential-url`, and `compact-invalid-unsafe-bundle-command-secret`, `python -m py_compile scripts/validate-change-metadata.py scripts/change_metadata_semantics.py`, and `git diff --check --` passed after the fix.

### spec-review-r1

## Findings

#### CVM-SR1

Finding ID: CVM-SR1
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Specify a single literal-brace escape syntax and matching validator behavior.
Rationale: R13 and AC20 require escaping, but downstream tests and implementation cannot infer the syntax.
Required outcome: The spec defines one literal-brace escape syntax and the validator behavior for escaped and unmatched braces.
Safe resolution path: Add requirements, examples, edge cases, and acceptance criteria for the chosen literal-brace escape syntax.
Validation target: Revised `specs/compact-change-validation-metadata.md` contains concrete literal-brace escaping rules.
Resolution: Defined doubled-brace literal escaping for compact path templates. `{var}` remains the only interpolation form. `{{` resolves to literal `{` and `}}` resolves to literal `}`. Validators reject unmatched braces, unknown variables, nested interpolation, and `${var}` syntax.
Validation evidence: `git diff --check --`, `python scripts/validate-change-metadata.py docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-21-compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.md --path docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml --path docs/changes/2026-05-21-compact-change-validation-metadata/review-log.md --path docs/changes/2026-05-21-compact-change-validation-metadata/review-resolution.md`, and `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-compact-change-validation-metadata` passed after the spec revision.

#### CVM-SR2

Finding ID: CVM-SR2
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Define artifact first-exists stage mapping and current-stage comparison semantics.
Rationale: R22-R24 require stage-derived filesystem checks, but the spec does not define enough stage data for validators to decide when a path must exist.
Required outcome: The spec defines artifact-class-to-first-exists-stage rules, current lifecycle stage source, stage ordering, and unknown-stage behavior.
Safe resolution path: Add a first-exists stage table and validation rules for known and unknown artifact classes/stages.
Validation target: Revised `specs/compact-change-validation-metadata.md` contains testable first-exists stage rules.
Resolution: Added deterministic first-exists stage semantics. Compact validation events now carry both a human-readable `stage` and normalized `lifecycle_stage`. The spec defines lifecycle-stage ordering, artifact-class-to-first-exists-stage mapping, optional/triggered artifact behavior, unknown-stage failure behavior, and transcript-reference existence rules.
Validation evidence: `git diff --check --`, `python scripts/validate-change-metadata.py docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-21-compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.md --path docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml --path docs/changes/2026-05-21-compact-change-validation-metadata/review-log.md --path docs/changes/2026-05-21-compact-change-validation-metadata/review-resolution.md`, and `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-compact-change-validation-metadata` passed after the spec revision.

#### CVM-SR3

Finding ID: CVM-SR3
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Define how `validation_summary.stages_validated` is derived from `validation_events`.
Rationale: R48 references compact summary rules that are not defined, leaving summary consistency ambiguous.
Required outcome: The spec defines exactly which event results are included in `stages_validated` and how non-pass events are represented.
Safe resolution path: Add a derivation rule, update examples, and add acceptance criteria for pass, fail, blocked, skipped, and not-run events.
Validation target: Revised `specs/compact-change-validation-metadata.md` contains testable `stages_validated` derivation rules.
Resolution: Defined `validation_summary.stages_validated` as the ordered list of validation event `stage` values with `result: pass`. Non-pass events are excluded and must be represented through `all_passed: false`, blocker details, or accepted skip details. Duplicate event stage identifiers are invalid.
Validation evidence: `git diff --check --`, `python scripts/validate-change-metadata.py docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-21-compact-change-validation-metadata.md --path specs/compact-change-validation-metadata.md --path docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml --path docs/changes/2026-05-21-compact-change-validation-metadata/review-log.md --path docs/changes/2026-05-21-compact-change-validation-metadata/review-resolution.md`, and `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-compact-change-validation-metadata` passed after the spec revision.
