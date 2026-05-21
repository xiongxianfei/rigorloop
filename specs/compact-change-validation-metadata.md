# Compact Change Validation Metadata

## Status

approved

## Related proposal

- [Compact Change Validation Metadata](../docs/proposals/2026-05-21-compact-change-validation-metadata.md)

## Goal and context

RigorLoop change metadata stores durable validation evidence in `docs/changes/<change-id>/change.yaml`. Legacy validation metadata records repeated command strings and prose-like result strings for every validation run. That shape preserves evidence but makes common review expensive when a change reruns the same validation bundles across many stages.

This spec defines compact validation metadata for new `schema_version: 2` change files. The compact shape must make the common read cheaper while preserving audit value: reviewers and validators must be able to reconstruct which validation bundles ran, which paths they used, which stages they covered, what results they produced, what counts were observed, and whether any blockers remain. Legacy change metadata remains valid during migration.

## Glossary

- `change.yaml`: Change-local metadata file under `docs/changes/<change-id>/change.yaml`.
- `legacy metadata`: Existing change metadata without compact validation fields and without `schema_version: 2`.
- `compact metadata`: Change metadata with `schema_version: 2` and compact validation sections.
- `validation bundle`: Named reusable command family declared once in `validation_bundles`.
- `validation event`: Stage-level validation result under `validation_events`.
- `path-expanding bundle`: Bundle whose exact command includes event-derived path arguments.
- `path_vars`: Mapping of reusable variables for repo-relative path templates.
- `change_id`: Dated event identifier shaped as `<YYYY-MM-DD>-<slug>`.
- `slug`: Durable contract identifier derived from `change_id` by removing the leading date prefix.
- `common-read surface`: The validation evidence stored directly in `change.yaml`, excluding optional transcript file contents.
- `transcript reference`: Optional `evidence.transcript` value pointing to a repo-relative transcript file and optional anchor.
- `first-exists stage`: Lifecycle stage at which an artifact class must exist.

## Examples first

Example E1: compact metadata records reusable bundles and stage events
Given a `schema_version: 2` `change.yaml`
When it declares `validation_bundles.lifecycle` once and references it from two `validation_events`
Then the validator accepts the compact shape only if both events reference defined bundles, use allowed results, and preserve enough path data to reconstruct each event's lifecycle command.

Example E2: path-expanding bundle uses accumulated path deltas
Given a lifecycle bundle whose command expands with `validation_events[].paths_added.lifecycle`
When `proposal-review-r1` adds `docs/proposals/{change_id}.md` and `spec-review-r1` adds `specs/{slug}.md`
Then the reconstructed lifecycle command for `spec-review-r1` includes both paths in accumulated order.

Example E3: summary drift is rejected
Given `validation_summary.all_passed: true`
When any `validation_events[].result` is `fail`, `blocked`, `skipped`, or `not-run`
Then `validate-change-metadata.py` rejects the file because the stored summary disagrees with event-derived truth.

Example E4: legacy metadata remains valid
Given an existing `change.yaml` without `schema_version: 2`
When it uses the legacy verbose validation list
Then the validator continues to validate it under the legacy contract and does not require compact sections.

Example E5: mixed validation metadata is rejected
Given a single `change.yaml`
When it contains both legacy validation entries and compact `validation_events`
Then the validator rejects it as ambiguous even though the repository may contain other legacy files and other compact files at the same time.

Example E6: transcript reference is non-load-bearing
Given a compact validation event with `evidence.transcript: change.validation-log.yaml#code-review-m1`
When the referenced file exists
Then the reference validates, but ordinary review must still be possible from `change.yaml` alone without reading transcript internals.

Example E7: durable spec paths use `slug`
Given `change_id: 2026-05-21-compact-change-validation-metadata`
When `path_vars.spec` is declared
Then it resolves to `specs/compact-change-validation-metadata.md`, not `specs/2026-05-21-compact-change-validation-metadata.md`.

Example E8: doubled braces produce literal braces
Given `path_vars.change_root: docs/changes/{change_id}`
When `path_vars.literal_brace_note` is `docs/changes/{change_id}/notes/{{draft}}.md`
Then it resolves to `docs/changes/2026-05-21-example/notes/{draft}.md`.

Example E9: stage summary excludes non-pass events
Given validation events `proposal-review-r1` with `result: pass` and `spec-review-r1` with `result: blocked`
When `validation_summary.stages_validated` is stored
Then it contains only `proposal-review-r1`, and the blocked event is represented through `all_passed: false` and `open_validation_blockers`.

## Requirements

R1. The validator MUST accept legacy change metadata files that were valid before this change.

R2. The validator MUST treat `schema_version: 2` as the compact validation metadata version.

R3. A compact `change.yaml` MUST declare `schema_version: 2`.

R4. A single `change.yaml` MUST be either wholly legacy or wholly compact.

R5. The validator MUST reject a single `change.yaml` that contains both legacy validation entries and compact `validation_events`.

R6. The repository MAY contain both legacy and compact `change.yaml` files during migration.

R7. Compact metadata MUST include `path_vars`, `validation_bundles`, `validation_events`, and `validation_summary`.

R8. `path_vars.change_id` MUST be a dated identifier shaped as `<YYYY-MM-DD>-<slug>`.

R9. The validator MUST derive `slug` from `change_id` by stripping the leading `<YYYY-MM-DD>-` prefix.

R10. Compact metadata MUST NOT redefine `slug` to a value that disagrees with the validator-derived value.

R11. Path-variable interpolation MUST use `{var}` exclusively.

R12. The validator MUST reject `${var}`, `%var%`, `$(var)`, malformed brace expressions, and other interpolation syntaxes in compact path templates.

R13. A literal `{` in a compact path template MUST be represented as `{{`, and a literal `}` MUST be represented as `}}`.

R14. Expanded path variables MUST resolve deterministically to repository-relative paths.

R15. The validator MUST reject unresolved, recursive, or ambiguous variables.

R16. The validator MUST reject absolute paths, home-directory paths, machine-local usernames, hostnames, credentials, proxy URLs, and secret-like values in compact path variables and transcript references.

R17. Dated event-record artifacts, including proposals, plans, and change-local directories, MUST use `change_id` in path templates.

R18. Durable contract artifacts, including specs and test specs, MUST use `slug` in path templates.

R19. Spec paths in compact metadata MUST resolve to `specs/{slug}.md`.

R20. Test-spec paths in compact metadata MUST resolve to `specs/{slug}.test.md`.

R21. The validator MUST reject compact spec or test-spec paths that use the full dated `change_id`.

R22. The validator MUST check resolved artifact paths against the filesystem once each artifact class's first-exists stage has been reached.

R23. Existence requirements MUST be derived from lifecycle stage and artifact first-exists stage, not from per-path opt-out flags.

R24. Compact metadata MUST NOT provide a per-path `optional`, `not_yet_created`, or equivalent flag that suppresses a stage-required existence check.

R25. `validation_bundles` MUST be a mapping of stable bundle IDs to bundle definitions.

R26. Each validation bundle MUST define `command`.

R27. A validation bundle MAY define `description`, `expands_with`, and `required_for`.

R28. Every bundle ID in `validation_events[].bundles` MUST resolve to a definition in `validation_bundles`.

R29. A path-expanding bundle MUST declare how event path data expands the command.

R30. For path-expanding bundles, each validation event MUST record `paths_added` for that bundle whenever the bundle's resolved path set changes from the prior event.

R31. For path-expanding bundles, the resolved path set at an event MUST be the ordered accumulation of that bundle's `paths_added` entries up to and including that event.

R32. A reviewer MUST be able to reconstruct the exact command and path set for each path-expanding validation event from `change.yaml` alone.

R33. `validation_events` MUST be an ordered list of stage-level validation events.

R34. Each validation event MUST include `stage`, `lifecycle_stage`, `bundles`, and `result`.

R35. `validation_events[].result` MUST be one of `pass`, `fail`, `blocked`, `skipped`, or `not-run`.

R36. `pass` MUST mean all referenced bundles for the event succeeded.

R37. `fail` MUST mean one or more referenced bundles ran and failed.

R38. `blocked` MUST mean validation could not run because a required precondition was missing.

R39. `skipped` MUST include an explicit reason and owner decision.

R40. `not-run` MUST be allowed only for planned-but-not-yet-executed stages.

R41. Events with `fail` or `blocked` results MUST include bounded failure or blocker details.

R42. Structured counts under an event MUST be integers.

R43. Structured counts that mirror review artifacts, including `reviews`, `findings`, `log_entries`, and `resolution_entries`, MUST be cross-checked against review-artifact parser output when referenced review artifacts exist.

R44. When referenced review artifacts exist and count cross-checking cannot run, the validator MUST report a blocked validation state rather than silently trusting copied counts.

R45. `validation_summary` MUST be treated as stored derived data.

R46. The validator MUST derive summary truth from `validation_events` and reject stored `validation_summary` fields that disagree.

R47. `validation_summary.all_passed` MUST be false unless every completed validation event result is `pass`.

R48. `validation_summary.stages_validated` MUST be the ordered list of `validation_events[].stage` values whose `result` is `pass`.

R49. `validation_summary.final_counts` MUST match the final derived count values from relevant validation events and review-artifact cross-checks.

R50. `validation_summary.open_validation_blockers` MUST include unresolved validation blockers derived from non-pass events.

R51. `evidence.transcript` MUST be optional.

R52. When present, `evidence.transcript` MUST be a well-formed repo-relative file reference with an optional `#anchor`.

R53. When present, the transcript file referenced by `evidence.transcript` MUST exist.

R54. The first slice MUST NOT require or validate the internal schema of `change.validation-log.yaml`.

R55. A transcript reference MUST NOT be the only proof needed for ordinary validation review.

R56. `change.yaml` alone MUST be sufficient for ordinary reviewers to determine bundles, reconstructed commands, stage results, counts, blockers, and failure details.

R57. Compact validation metadata MUST NOT change validation command selection, command exit behavior, failure detection, or required validation evidence.

R58. Compact validation metadata MUST NOT weaken lifecycle, metadata, review-artifact, whitespace, generated-output, or selected-CI validation requirements.

R59. The compact fixture used to prove material compactness MUST preserve reconstructable evidence before size reduction is evaluated.

R60. On a representative high-rerun fixture, compact `change.yaml` common-read validation metadata MUST be at least 30% smaller than equivalent legacy common-read metadata.

R61. Trivial or low-rerun fixtures SHOULD NOT be used as the material compactness proof.

R62. Validator failures for compact metadata MUST identify stable, actionable check IDs or messages suitable for fixture tests.

R63. Validators MUST parse compact path templates left to right using these rules: `{{` produces one literal `{`; `}}` produces one literal `}`; `{name}` interpolates `path_vars.name`; a single unmatched `{` or `}` fails validation; nested interpolation fails validation; unknown variable names fail validation; `${name}` and other interpolation syntaxes fail validation.

R64. After literal-brace parsing and variable interpolation, the resolved path MUST still satisfy repository-relative path safety rules.

R65. `validation_events[].stage` MUST be a stable event identifier and MAY include round, milestone, or rerun suffixes such as `spec-review-r1`, `code-review-m2-r1`, or `verify-rerun-1`.

R66. `validation_events[].lifecycle_stage` MUST be a normalized lifecycle stage used for first-exists comparisons.

R67. `validation_events[].lifecycle_stage` MUST be one of these values, in this order: `change-created`, `proposal`, `proposal-review`, `spec`, `spec-review`, `architecture`, `architecture-review`, `plan`, `plan-review`, `test-spec`, `implement`, `code-review`, `review-resolution`, `ci-maintenance`, `explain-change`, `verify`, `pr`.

R68. Unknown `lifecycle_stage` values MUST fail validation.

R69. If an event has a freeform `stage` value but no `lifecycle_stage`, validation MUST fail.

R70. Validators MUST compare lifecycle stages by the order in R67.

R71. A compact event reaches an artifact class's first-exists stage when `event.lifecycle_stage` is equal to or later than that artifact class's first-exists stage.

R72. Unknown artifact classes or unknown path variables used for first-exists checking MUST fail validation unless this spec explicitly classifies them as non-artifact variables.

R73. Non-artifact variables, including `change_id` and `slug`, MUST be used for expansion only and MUST NOT have first-exists stages.

R74. Optional lifecycle artifacts MUST NOT be required merely because their lifecycle stage exists.

R75. Optional lifecycle artifacts MUST become required when the path variable is declared for that artifact class, the path is referenced by a validation bundle, `paths_added`, summary field, or transcript reference, or the relevant lifecycle stage has recorded that artifact as produced.

R76. Each `validation_events[].stage` value MUST be unique within a compact `change.yaml`.

R77. Events with `fail`, `blocked`, `skipped`, or `not-run` results MUST be excluded from `validation_summary.stages_validated`.

R78. `validation_summary.all_passed` MUST be `true` only when every validation event has `result: pass` and `open_validation_blockers` is empty.

R79. If any event has `result: fail` or `result: blocked`, `validation_summary.all_passed` MUST be `false`, and `validation_summary.open_validation_blockers` MUST include a corresponding blocker.

R80. If any required event has `result: not-run`, `validation_summary.all_passed` MUST be `false`, and `validation_summary.open_validation_blockers` MUST include a corresponding blocker.

R81. A skipped event with no accepted owner decision MUST be treated as a blocker.

R82. `validation_summary.final_counts` MUST agree with validator-derived counts from the latest applicable validation event and review-artifact parser output when the referenced artifacts exist.

R83. For the review log first-exists rule, the first formal review stage MUST be the earliest validation event whose `lifecycle_stage` is `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, or `code-review`, or any later stage that records a formal review result.

## Artifact first-exists mapping

| Artifact class | Path variable examples | First-exists stage | Requirement |
|---|---|---|---|
| Change root | `change_root` | `change-created` | Must exist for compact metadata. |
| Change metadata | `{change_root}/change.yaml` | `change-created` | Must exist for compact metadata. |
| Proposal | `proposal` | `proposal` | Required once proposal stage is reached or when referenced by bundle paths. |
| Proposal-review record | `reviews_root/proposal-review-*.md` | `proposal-review` | Required once the formal review record is referenced or recorded. |
| Review log | `review_log` | first formal review stage | Required once any formal review result is recorded. |
| Review resolution | `review_resolution` | `review-resolution` | Required when material findings require disposition or when referenced. |
| Spec | `spec` | `spec` | Must resolve under `specs/{slug}.md`; dated `specs/{change_id}.md` fails. |
| Spec-review record | `reviews_root/spec-review-*.md` | `spec-review` | Required once referenced or recorded. |
| Architecture artifact | `architecture` | `architecture` | Required only when the architecture stage is present or the path is referenced. |
| ADR | `adr` | `architecture` | Required only when the ADR is present in path vars or referenced. |
| Plan | `plan` | `plan` | Required once plan stage is reached or when referenced. |
| Plan-review record | `reviews_root/plan-review-*.md` | `plan-review` | Required once referenced or recorded. |
| Test spec | `test_spec` | `test-spec` | Must resolve under `specs/{slug}.test.md`; dated test-spec paths fail. |
| Code-review record | `reviews_root/code-review-*.md` | `code-review` | Required once referenced or recorded. |
| Explain-change artifact | `explain_change` | `explain-change` | Required once explain-change stage is reached or when referenced. |
| Verify artifact | `verify` | `verify` | Required once verify stage is reached or when referenced. |
| PR artifact/body | `pr` | `pr` | Required once PR stage is reached or when referenced. |
| Validation transcript | `evidence.transcript` | when referenced | Optional; if present, target file must exist. |

## Inputs and outputs

Inputs:

- Legacy `docs/changes/<change-id>/change.yaml` files.
- Compact `docs/changes/<change-id>/change.yaml` files with `schema_version: 2`.
- Optional `docs/changes/<change-id>/change.validation-log.yaml` files when referenced.
- Review artifacts referenced by compact metadata counts.
- Filesystem state for resolved path existence checks.

Outputs:

- Validator pass/fail result for each target `change.yaml`.
- Actionable validation errors for malformed compact metadata.
- Reconstructable command and path evidence from compact metadata.
- No changes to selected validation commands or command exit semantics.

Compact metadata data surface:

```yaml
schema_version: 2
path_vars: {}
validation_bundles: {}
validation_events:
  - stage: spec-review-r1
    lifecycle_stage: spec-review
    bundles: []
    result: pass
validation_summary: {}
```

## State and invariants

- Compact metadata is authoritative only for compact files with `schema_version: 2`.
- Legacy metadata remains authoritative for files without compact versioning.
- One file has one validation metadata shape; there is no in-file hybrid state.
- Bundle definitions are single-source within a compact file.
- Event order is significant for path accumulation.
- Event `stage` values are unique identifiers; `lifecycle_stage` values are normalized lifecycle positions.
- `validation_summary` is checked derived data, not independent truth.
- `validation_summary.stages_validated` is derived from pass events only.
- `change.yaml` remains the common review surface even when transcript references exist.
- `slug` is derived from `change_id`; durable contract paths do not include the date prefix.
- Stage-derived existence checks cannot be disabled by path-local metadata.

## Error and boundary behavior

- Missing compact required sections in a `schema_version: 2` file fail validation.
- Mixed legacy and compact validation metadata in one file fails validation.
- Undefined bundle references fail validation.
- Invalid result enum values fail validation.
- `fail` or `blocked` events without details fail validation.
- Non-integer structured counts fail validation.
- Summary fields that disagree with event-derived truth fail validation.
- Duplicate `validation_events[].stage` values fail validation.
- Missing or unknown `validation_events[].lifecycle_stage` values fail validation.
- Path variables that are unresolved, recursive, ambiguous, unsafe, machine-local, absolute, or secret-like fail validation.
- Single unmatched literal braces, nested interpolation, unknown variables, and alternate interpolation syntaxes in path templates fail validation.
- Spec and test-spec paths using `{change_id}` fail validation.
- Resolved paths missing after their first-exists stage fail validation.
- Optional lifecycle artifacts are not required merely because their stage exists, but they fail validation when referenced or recorded and missing.
- Transcript references with malformed syntax or missing target files fail validation.
- Transcript files with unstandardized internal fields do not fail solely because of their internal shape in the first slice.
- Compactness measurements fail if reconstruction fails, regardless of byte reduction.

## Compatibility and migration

- Existing valid legacy `change.yaml` files remain valid.
- New compact files use `schema_version: 2`.
- Migration is incremental across files, not within one file.
- Historical files do not need immediate migration.
- Bulk migration of historical validation metadata is out of scope for the first slice.
- A later migration proposal may retire legacy support, but this spec does not.
- Rollback preserves legacy metadata support and removes compact validator acceptance if needed.
- If a compact file is rolled back before compact support lands, it must be converted to a legacy-valid shape.

## Observability

- Validator errors SHOULD identify the failing compact validation rule with stable check IDs or stable messages.
- Compact validation summaries MUST expose `all_passed`, validated stages, final counts, and open blockers.
- Reviewers MUST be able to inspect stage-level events without opening transcript files.
- When transcript references are present, validators MUST report dangling references.
- Validation commands run during implementation and verification MUST be named in change-local evidence.

## Security and privacy

- Compact metadata MUST NOT contain secrets, credentials, tokens, private keys, proxy credentials, or host-specific paths.
- Validators MUST reject machine-local paths and credential-bearing references in path variables, bundle commands, event paths, and transcript references.
- Bundle commands MUST remain repository validation commands or command templates, not a place to store environment-specific workarounds.
- Transcript references MUST be repo-relative and must not point outside the repository.

## Accessibility and UX

Not applicable to user-interface accessibility. The review UX requirement is that compact metadata remains readable to maintainers by showing bundle IDs, stages, results, counts, blockers, and reconstructable paths without scanning repeated command transcripts.

## Performance expectations

- Validation of compact metadata SHOULD be linear in the number of bundles, events, path variables, referenced paths, and referenced review artifacts.
- Compact metadata validation MUST NOT execute validation bundles while validating metadata; it validates recorded evidence shape and references.
- The compactness proof uses byte or character counts for the common-read validation metadata surface and excludes optional transcript internals.

## Edge cases

EC1. A compact file contains `schema_version: 2` but omits `validation_events`; validation fails.

EC2. A file without `schema_version: 2` uses legacy validation entries; validation follows the legacy contract.

EC3. A file has `schema_version: 2` and legacy validation entries; validation fails as mixed shape.

EC4. A validation event references bundle `lifecycle` when no `validation_bundles.lifecycle` exists; validation fails.

EC5. A path-expanding bundle's event omits `paths_added` when the path set changed; exact reconstruction fails validation.

EC6. A later event adds no paths for a path-expanding bundle; the prior accumulated path set remains in effect.

EC7. A compact file records `all_passed: true` while one event is `blocked`; validation fails.

EC8. A compact file records review counts that disagree with `validate-review-artifacts.py`; validation fails.

EC9. A compact file references `specs/{change_id}.md`; validation fails even if the file exists.

EC10. A compact file references `specs/{slug}.md` before the spec first-exists stage; existence is not required until that stage.

EC11. A compact file references `specs/{slug}.md` after the spec first-exists stage and the file is missing; validation fails.

EC12. A compact file includes `not_yet_created: true` for a missing required path; validation fails because path-local opt-outs are not allowed.

EC13. `evidence.transcript` points to `change.validation-log.yaml#code-review-m1` and the file is missing; validation fails.

EC14. `evidence.transcript` points to an existing transcript with unstandardized internal fields; validation passes if the reference contract is satisfied.

EC15. A compact fixture is 40% smaller but loses exact path reconstruction; acceptance fails.

EC16. A trivial compact fixture is less than 30% smaller; it does not satisfy the representative high-rerun compactness proof.

EC17. A compact path template contains `{{draft}}`; interpolation resolves it to literal `{draft}`.

EC18. A compact path template contains a single unmatched `{` or `}`; validation fails.

EC19. A compact path template contains `${change_id}`; validation fails.

EC20. A compact event has `stage: spec-review-r1` but omits `lifecycle_stage`; validation fails.

EC21. A compact event has `lifecycle_stage: spec-review-r1`; validation fails because the normalized value is unknown.

EC22. A compact file has duplicate `validation_events[].stage` values; validation fails.

EC23. A compact file has one pass event and one skipped event with an accepted owner decision; only the pass event appears in `stages_validated`.

EC24. A compact file has one pass event and one blocked event; only the pass event appears in `stages_validated`, `all_passed` is false, and `open_validation_blockers` records the blocked event.

EC25. A compact file has a skipped event without an accepted owner decision; validation fails.

## Non-goals

- Do not bulk-migrate historical `change.yaml` files.
- Do not standardize the internal schema of `change.validation-log.yaml`.
- Do not add CLI scaffolding that writes compact metadata.
- Do not change review-record, review-log, or review-resolution semantics.
- Do not change artifact lifecycle rules beyond documenting artifact naming and first-exists behavior needed for path validation.
- Do not change validation selector behavior, selected commands, command exit behavior, or failure detection.
- Do not make external CI logs the only validation proof.
- Do not optimize byte count by removing reconstructable evidence.

## Acceptance criteria

AC1. Existing legacy valid change metadata fixtures continue to pass.

AC2. A compact valid fixture with bundles, events, path variables, structured counts, and summary passes.

AC3. A mixed legacy/compact fixture fails.

AC4. Undefined bundle references fail.

AC5. Invalid event result enum values fail.

AC6. `fail` and `blocked` events without details fail.

AC7. Structured counts that are not integers fail.

AC8. `validation_summary.all_passed: true` with any non-pass event fails.

AC9. Stored summary stage and count fields that disagree with event-derived truth fail.

AC10. Path variables expand deterministically and safely.

AC11. Path-variable interpolation uses `{var}` exclusively, rejects `${var}` and other alternate forms, resolves doubled braces `{{` and `}}` to literal braces, and rejects unmatched literal braces.

AC12. Recursive and unresolved path variables fail.

AC13. Absolute, home-directory, machine-local, hostname, credential, proxy, or secret-like path values fail.

AC14. Spec and test-spec variables resolve to `specs/{slug}.md` and `specs/{slug}.test.md`.

AC15. Dated spec paths such as `specs/{change_id}.md` fail.

AC16. Missing resolved paths fail after their first-exists stage.

AC17. Per-path opt-out flags cannot suppress stage-required existence checks.

AC18. Path-expanding bundle commands reconstruct exact accumulated path sets for each event.

AC19. Optional transcript references validate syntax and target existence when present.

AC20. Transcript internals are not required by first-slice validation.

AC21. `change.yaml` alone is sufficient for ordinary validation review when transcript references are present.

AC22. Review-artifact counts are cross-checked against parser output when referenced artifacts exist.

AC23. A representative high-rerun compact fixture is at least 30% smaller on the common-read surface after reconstruction preservation passes.

AC24. No compact behavior changes validation selection, command exit behavior, failure detection, or required validation evidence.

AC25. Compact validation events include both unique human-readable `stage` values and normalized `lifecycle_stage` values from the approved stage order.

AC26. The first-exists mapping determines which referenced or produced artifacts must exist, including slug-based spec and test-spec paths, formal review records, review logs, review-resolution files, optional lifecycle artifacts, and transcript references.

AC27. `validation_summary.stages_validated` is the ordered list of validation event `stage` values whose `result` is `pass`; non-pass events are excluded and must be represented through `all_passed: false`, blocker details, or accepted skip details.

## Open questions

None.

## Next artifacts

```text
spec-review
test-spec
plan
plan-review
implementation
code-review
explain-change
verify
pr
```

## Follow-on artifacts

None yet

## Readiness

Approved after `spec-review-r2`. Ready for `plan`.
