# Compact Change Validation Metadata Review Resolution

## Summary

Closeout status: closed

Review closeout: spec-review-r1

## Resolution Entries

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
