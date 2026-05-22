# Compact Change Validation Metadata Test Spec

## Status

active

## Related spec and plan

- Spec: [Compact Change Validation Metadata](compact-change-validation-metadata.md), approved.
- Proposal: [Compact Change Validation Metadata](../docs/proposals/2026-05-21-compact-change-validation-metadata.md), accepted.
- Plan: [Compact Change Validation Metadata Plan](../docs/plans/2026-05-21-compact-change-validation-metadata.md), active.
- Architecture/ADRs: not applicable; the approved plan records that this slice is bounded to the existing change-metadata validator, schema, semantic helper, fixtures, and tests.
- Spec review: `spec-review-r2` approved the revised spec with no material findings.
- Plan review: `plan-review-r1` approved the plan with no material findings.

## Testing strategy

- Unit tests exercise compact helper behavior that can be isolated without subprocess overhead: path-template parsing, slug derivation, lifecycle-stage comparison, summary derivation, path accumulation, and compactness measurement.
- Integration tests execute `scripts/validate-change-metadata.py` against real `change.yaml` fixtures so schema validation, YAML parsing, semantic validation, filesystem checks, transcript references, and review-artifact count checks are observed through the public CLI.
- End-to-end tests are not required for an external service or UI; the closest end-to-end proof is selected CI over the changed validator, schema, fixtures, active plan, and change metadata.
- Smoke tests validate the active change metadata and selected representative fixtures after each milestone.
- Manual verification is limited to reviewing the representative compactness fixture pair and confirming the compact fixture preserves the named legacy evidence before the size threshold is evaluated.
- Contract tests assert the validator does not execute validation bundles and does not change validation command selection, exit behavior, or failure detection.
- Migration tests prove legacy metadata remains valid, compact files require `schema_version: 2`, and mixed legacy/compact evidence in one file is rejected.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | TCVM-001 | migration | Existing valid legacy fixtures pass unchanged. |
| R2 | TCVM-002, TCVM-003 | integration | Explicit `schema_version: 2` selects compact validation. |
| R3 | TCVM-002, TCVM-003 | integration | Compact fixture declares `schema_version: 2`; compact fields without it fail. |
| R4 | TCVM-003 | migration | One file cannot be both legacy and compact. |
| R5 | TCVM-003 | migration | Mixed legacy validation list and compact events fail. |
| R6 | TCVM-001, TCVM-002 | migration | Repo may contain legacy and compact files simultaneously. |
| R7 | TCVM-002, TCVM-003 | integration | Compact required sections are enforced. |
| R8 | TCVM-006 | unit, integration | `change_id` must be dated. |
| R9 | TCVM-006 | unit, integration | `slug` is derived from `change_id`. |
| R10 | TCVM-006 | integration | Conflicting explicit `slug` fails. |
| R11 | TCVM-007 | unit, integration | `{var}` is the only interpolation syntax. |
| R12 | TCVM-007 | unit, integration | Alternate and malformed interpolation forms fail. |
| R13 | TCVM-007 | unit, integration | `{{` and `}}` resolve to literal braces. |
| R14 | TCVM-006, TCVM-008 | unit, integration | Expanded paths are deterministic and repo-relative. |
| R15 | TCVM-006, TCVM-007 | unit, integration | Unresolved, recursive, and ambiguous variables fail. |
| R16 | TCVM-008 | integration | Unsafe paths, hosts, credentials, proxy URLs, and secret-like values fail. |
| R17 | TCVM-006, TCVM-009 | integration | Dated event-record artifact paths use `change_id`. |
| R18 | TCVM-006, TCVM-009 | integration | Durable spec/test-spec paths use `slug`. |
| R19 | TCVM-009 | integration | Spec path resolves to `specs/{slug}.md`. |
| R20 | TCVM-009 | integration | Test-spec path resolves to `specs/{slug}.test.md`. |
| R21 | TCVM-009 | integration | Dated spec and test-spec paths fail. |
| R22 | TCVM-010 | integration | Filesystem existence is checked after first-exists stage. |
| R23 | TCVM-010 | integration | Existence derives from lifecycle stage and artifact first-exists stage. |
| R24 | TCVM-010 | integration | Path-local opt-out flags cannot suppress required existence. |
| R25 | TCVM-004 | integration | Bundles are a mapping of stable IDs. |
| R26 | TCVM-004 | integration | Each bundle defines `command`. |
| R27 | TCVM-004 | integration | Optional bundle fields are accepted when shaped correctly. |
| R28 | TCVM-004 | integration | Event bundle references must resolve. |
| R29 | TCVM-013 | integration | Path-expanding bundles declare expansion data. |
| R30 | TCVM-013 | integration | `paths_added` is required when path set changes. |
| R31 | TCVM-013 | integration | Path set accumulates in event order. |
| R32 | TCVM-013, TCVM-023 | integration, manual | Exact command/path-set reconstruction is possible from `change.yaml`. |
| R33 | TCVM-004 | integration | Events are ordered lists. |
| R34 | TCVM-004, TCVM-011 | integration | Events include `stage`, `lifecycle_stage`, `bundles`, and `result`. |
| R35 | TCVM-004 | integration | Result enum is closed. |
| R36 | TCVM-004, TCVM-014 | integration | `pass` means referenced bundles succeeded. |
| R37 | TCVM-005, TCVM-014 | integration | `fail` means a bundle ran and failed. |
| R38 | TCVM-005, TCVM-014 | integration | `blocked` means a required precondition blocked validation. |
| R39 | TCVM-016 | integration | `skipped` includes reason and owner decision. |
| R40 | TCVM-016 | integration | `not-run` is constrained to planned stages. |
| R41 | TCVM-005, TCVM-014 | integration | Fail and blocked events include details. |
| R42 | TCVM-005 | integration | Structured counts are integers. |
| R43 | TCVM-017 | integration | Review counts are cross-checked against parser output. |
| R44 | TCVM-017 | integration | Cross-check precondition failure reports blocked state. |
| R45 | TCVM-014, TCVM-015 | integration | Summary is stored derived data. |
| R46 | TCVM-014, TCVM-015 | integration | Stored summary disagreement fails. |
| R47 | TCVM-014 | integration | `all_passed` is false unless all completed events pass. |
| R48 | TCVM-015 | integration | `stages_validated` is pass-event stages in order. |
| R49 | TCVM-017 | integration | Final counts match derived count values and review parser output. |
| R50 | TCVM-014, TCVM-016 | integration | Open blockers include unresolved non-pass events. |
| R51 | TCVM-012 | integration | Transcript reference is optional. |
| R52 | TCVM-012 | integration | Transcript reference syntax is validated. |
| R53 | TCVM-012 | integration | Referenced transcript file must exist. |
| R54 | TCVM-012 | integration | Transcript internals are not schema-validated. |
| R55 | TCVM-012, TCVM-023 | integration, manual | Transcript is not the only ordinary proof. |
| R56 | TCVM-012, TCVM-023 | integration, manual | `change.yaml` alone is sufficient for ordinary review. |
| R57 | TCVM-020, TCVM-024 | contract, smoke | Compact metadata does not change selected command behavior. |
| R58 | TCVM-020, TCVM-024 | contract, smoke | Existing validation requirements are not weakened. |
| R59 | TCVM-019 | manual, contract | Reconstruction preservation is checked before size. |
| R60 | TCVM-019 | manual, contract | Representative compact fixture is at least 30% smaller. |
| R61 | TCVM-019 | manual, contract | Trivial fixtures are not used for compactness proof. |
| R62 | TCVM-018 | integration | Compact failures produce stable actionable messages. |
| R63 | TCVM-007 | unit, integration | Template parser follows left-to-right brace/interpolation rules. |
| R64 | TCVM-008 | integration | Resolved paths still satisfy safety rules after interpolation. |
| R65 | TCVM-011 | integration | `stage` supports stable event IDs and rerun suffixes. |
| R66 | TCVM-011 | integration | `lifecycle_stage` is normalized for comparisons. |
| R67 | TCVM-011 | unit, integration | Lifecycle-stage enum and order are enforced. |
| R68 | TCVM-011 | integration | Unknown lifecycle stages fail. |
| R69 | TCVM-011 | integration | Missing `lifecycle_stage` fails. |
| R70 | TCVM-011 | unit | Stage comparison uses the approved order. |
| R71 | TCVM-010, TCVM-011 | integration | First-exists stage is reached by equal-or-later comparison. |
| R72 | TCVM-010 | integration | Unknown artifact classes/path variables in existence checks fail. |
| R73 | TCVM-006, TCVM-010 | integration | `change_id` and `slug` are expansion-only non-artifact variables. |
| R74 | TCVM-010 | integration | Optional artifacts are not required merely because their stage exists. |
| R75 | TCVM-010 | integration | Optional artifacts become required when declared, referenced, or recorded. |
| R76 | TCVM-015 | integration | Duplicate event stage IDs fail. |
| R77 | TCVM-015, TCVM-016 | integration | Non-pass events are excluded from `stages_validated`. |
| R78 | TCVM-014 | integration | `all_passed: true` requires all pass and no blockers. |
| R79 | TCVM-014 | integration | Fail/blocked events require `all_passed: false` and blockers. |
| R80 | TCVM-016 | integration | Required `not-run` events require `all_passed: false` and blockers. |
| R81 | TCVM-016 | integration | Skipped without accepted owner decision is a blocker. |
| R82 | TCVM-017 | integration | `final_counts` agrees with latest event and review parser output. |
| R83 | TCVM-010 | integration | Review-log first-exists rule starts at the first formal review event. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | TCVM-002, TCVM-004 | Compact bundles/events happy path. |
| E2 | TCVM-013 | Accumulated path deltas reconstruct path-expanding command. |
| E3 | TCVM-014 | Summary drift with non-pass event fails. |
| E4 | TCVM-001 | Legacy metadata remains valid. |
| E5 | TCVM-003 | Mixed legacy/compact metadata is rejected. |
| E6 | TCVM-012, TCVM-023 | Transcript reference validates but remains non-load-bearing. |
| E7 | TCVM-006, TCVM-009 | Durable spec paths use derived `slug`. |
| E8 | TCVM-007 | Doubled braces produce literal braces. |
| E9 | TCVM-015 | Pass-only `stages_validated` derivation. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 | TCVM-003 | Missing compact required section fails. |
| EC2 | TCVM-001 | Legacy branch remains valid. |
| EC3 | TCVM-003 | `schema_version: 2` plus legacy entries fails. |
| EC4 | TCVM-004 | Undefined bundle reference fails. |
| EC5 | TCVM-013 | Missing changed path delta for changed path set fails. |
| EC6 | TCVM-013 | No path delta keeps prior accumulated path set. |
| EC7 | TCVM-014 | `all_passed: true` with blocked event fails. |
| EC8 | TCVM-017 | Review count disagreement fails. |
| EC9 | TCVM-009 | Dated spec path fails even if file exists. |
| EC10 | TCVM-010 | Spec path before spec stage is not required unless referenced. |
| EC11 | TCVM-010 | Missing spec after first-exists stage fails. |
| EC12 | TCVM-010 | `not_yet_created` cannot suppress required existence. |
| EC13 | TCVM-012 | Missing referenced transcript fails. |
| EC14 | TCVM-012 | Existing transcript with unconstrained internals passes. |
| EC15 | TCVM-019 | Smaller fixture with lost reconstruction fails acceptance. |
| EC16 | TCVM-019 | Trivial fixture does not satisfy compactness proof. |
| EC17 | TCVM-007 | `{{draft}}` resolves to `{draft}`. |
| EC18 | TCVM-007 | Unmatched brace fails. |
| EC19 | TCVM-007 | `${change_id}` fails. |
| EC20 | TCVM-011 | Missing `lifecycle_stage` fails. |
| EC21 | TCVM-011 | Unknown normalized lifecycle stage fails. |
| EC22 | TCVM-015 | Duplicate event stage IDs fail. |
| EC23 | TCVM-016 | Skipped with accepted owner decision is excluded and valid. |
| EC24 | TCVM-014, TCVM-015 | Blocked event is excluded, all_passed false, blockers present. |
| EC25 | TCVM-016 | Skipped without owner decision fails. |

## Test cases

### TCVM-001. Legacy metadata remains valid

- Covers: R1, R6, E4, EC2, AC1
- Level: integration, migration
- Fixture/setup: Existing legacy fixtures such as `tests/fixtures/change-metadata/valid-basic/change.yaml`, the clean-receipt fixture, and the shipped `docs/changes/0001-skill-validator/change.yaml`.
- Steps: Run `python scripts/test-change-metadata-validator.py` and direct `validate-change-metadata.py` commands against legacy valid fixtures.
- Expected result: Legacy valid files pass without compact fields.
- Failure proves: Compact support regressed historical metadata compatibility.
- Automation location: `scripts/test-change-metadata-validator.py`.

### TCVM-002. Basic compact fixture passes

- Covers: R2, R3, R7, E1, AC2
- Level: integration
- Fixture/setup: `tests/fixtures/change-metadata/compact-valid/change.yaml` with `schema_version: 2`, path vars, bundles, events, summary, and referenced files.
- Steps: Run `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-valid/change.yaml`.
- Expected result: The compact valid fixture passes.
- Failure proves: The validator does not accept the approved compact shape.
- Automation location: `scripts/test-change-metadata-validator.py`.

### TCVM-003. Compact versioning and mixed-shape rejection

- Covers: R2-R7, E5, EC1, EC3, AC3
- Level: integration, migration
- Fixture/setup: Invalid fixtures for compact fields without `schema_version: 2`, `schema_version: 2` without compact required sections, and a mixed legacy validation list plus compact `validation_events`.
- Steps: Run the validator against each invalid fixture.
- Expected result: Each invalid fixture fails with a stable message identifying missing compact sections or mixed validation evidence.
- Failure proves: The validator guesses shape heuristically or accepts ambiguous evidence.
- Automation location: `scripts/test-change-metadata-validator.py`.

### TCVM-004. Bundle and event structural validation

- Covers: R25-R28, R33-R36, E1, EC4, AC4, AC5
- Level: integration
- Fixture/setup: Compact fixtures with valid bundles/events, missing bundle commands, undefined bundle references, malformed event lists, and invalid result values.
- Steps: Run the validator against each fixture.
- Expected result: Valid structures pass; missing commands, undefined references, and invalid results fail.
- Failure proves: Compact event evidence can reference non-existent command families or invalid states.
- Automation location: `scripts/test-change-metadata-validator.py`.

### TCVM-005. Failure details and structured counts

- Covers: R37-R42, AC6, AC7
- Level: integration
- Fixture/setup: Compact fixtures for `fail`, `blocked`, missing failures, integer counts, and non-integer counts.
- Steps: Run the validator against each fixture.
- Expected result: `fail` and `blocked` events require bounded details; integer counts pass; non-integer counts fail.
- Failure proves: Failures or parser-queryable counts can drift into prose or incomplete evidence.
- Automation location: `scripts/test-change-metadata-validator.py`.

### TCVM-006. `change_id`, derived `slug`, and deterministic expansion

- Covers: R8-R10, R14-R15, R17-R18, R73, E7, AC10, AC12, AC14
- Level: unit, integration
- Fixture/setup: Fixtures with dated `change_id`, omitted `slug`, matching `slug`, conflicting `slug`, recursive variables, unresolved variables, and event/durable path vars.
- Steps: Run unit tests for slug derivation and integration fixtures through the validator.
- Expected result: Derived or matching `slug` passes; conflicting, recursive, or unresolved values fail.
- Failure proves: Path variables are ambiguous or allow dated durable-contract paths.
- Automation location: `scripts/test-change-metadata-validator.py`.

### TCVM-007. Path-template interpolation grammar

- Covers: R11-R13, R15, R63, E8, EC17-EC19, AC11, AC12
- Level: unit, integration
- Fixture/setup: Templates using `{var}`, `{{`, `}}`, unmatched braces, nested interpolation, unknown variables, `${var}`, `%var%`, and `$(var)`.
- Steps: Run unit parser cases and validator fixtures.
- Expected result: Closed `{var}` syntax and doubled braces work; unsupported or malformed syntax fails.
- Failure proves: The path template language is permissive or ambiguous.
- Automation location: `scripts/test-change-metadata-validator.py`.

### TCVM-008. Path safety after interpolation

- Covers: R14, R16, R64, AC13
- Level: integration
- Fixture/setup: Compact fixtures with repo-relative paths, absolute paths, home paths, `..` escapes, hostnames, usernames, credentials, proxy URLs, and secret-like values.
- Steps: Run the validator against safe and unsafe fixtures.
- Expected result: Safe repo-relative paths pass; unsafe values fail with actionable errors.
- Failure proves: Compact metadata can hide machine-local paths or sensitive values.
- Automation location: `scripts/test-change-metadata-validator.py`.

### TCVM-009. Canonical spec and test-spec paths

- Covers: R19-R21, E7, EC9, AC14, AC15
- Level: integration
- Fixture/setup: Fixtures where `spec` and `test_spec` resolve to `specs/{slug}.md` and `specs/{slug}.test.md`, and invalid fixtures using `specs/{change_id}.md` or `specs/{change_id}.test.md`.
- Steps: Run the validator against each fixture.
- Expected result: Slug-based paths pass when present; dated spec/test-spec paths fail even if files exist.
- Failure proves: The path-variable model creates dated durable-contract fragments.
- Automation location: `scripts/test-change-metadata-validator.py`.

### TCVM-010. Lifecycle first-exists checks

- Covers: R22-R24, R71-R75, R83, EC10-EC12, AC16, AC17, AC26
- Level: integration
- Fixture/setup: Compact fixture roots with staged events before/after artifact first-exists stages, optional artifacts, referenced artifacts, unknown artifact classes, review-log first formal review behavior, and forbidden `not_yet_created` flags.
- Steps: Run the validator against each fixture.
- Expected result: Missing artifacts fail only when stage-required or referenced; unknown classes fail; path-local opt-outs fail.
- Failure proves: Existence checks are either too weak or too eager.
- Automation location: `scripts/test-change-metadata-validator.py`.

### TCVM-011. Normalized lifecycle stages

- Covers: R34, R65-R71, EC20, EC21, AC25
- Level: unit, integration
- Fixture/setup: Events with valid normalized stages, rerun-style `stage` IDs, missing `lifecycle_stage`, and unknown lifecycle-stage values.
- Steps: Run stage-order unit tests and validator fixtures.
- Expected result: Valid stage IDs and normalized lifecycle stages pass; missing or unknown lifecycle stages fail.
- Failure proves: First-exists comparisons rely on freeform event names.
- Automation location: `scripts/test-change-metadata-validator.py`.

### TCVM-012. Transcript references are optional and non-load-bearing

- Covers: R51-R56, E6, EC13, EC14, AC19-AC21
- Level: integration, manual
- Fixture/setup: Compact fixtures with no transcript, a valid `change.validation-log.yaml#anchor` reference, missing transcript file, malformed reference, and existing transcript with unconstrained internals.
- Steps: Run validator fixtures and manually inspect the valid fixture to confirm `change.yaml` alone shows bundles, reconstructed commands, stage results, counts, blockers, and failure details.
- Expected result: Omitted transcript passes; valid reference passes; missing/malformed reference fails; transcript internals are not validated.
- Failure proves: Transcript detail became load-bearing or references can dangle.
- Automation location: `scripts/test-change-metadata-validator.py`; manual inspection recorded in implementation evidence.

### TCVM-013. Path-expanding bundle reconstruction

- Covers: R29-R32, E2, EC5, EC6, AC18
- Level: integration
- Fixture/setup: Compact fixtures with lifecycle bundle expansion, multiple events with accumulated `paths_added`, unchanged path-set events, and changed path sets without deltas.
- Steps: Run validator fixtures and assert reconstructed path sets match expected ordered lists.
- Expected result: Accumulated path sets are exact and deterministic; missing changed deltas fail.
- Failure proves: Compact metadata loses the exact historical command/path-set evidence.
- Automation location: `scripts/test-change-metadata-validator.py`.

### TCVM-014. `all_passed` and blocker consistency

- Covers: R36-R38, R41, R45-R47, R50, R78-R80, E3, EC7, EC24, AC8
- Level: integration
- Fixture/setup: Compact fixtures with all pass, pass plus fail, pass plus blocked, `all_passed: true` conflict, missing blockers, and present blockers.
- Steps: Run the validator against each fixture.
- Expected result: All-pass summaries pass; conflicts or missing blockers fail.
- Failure proves: Failed or blocked validation can be hidden behind summary fields.
- Automation location: `scripts/test-change-metadata-validator.py`.

### TCVM-015. `stages_validated` derivation and duplicate stages

- Covers: R45-R48, R76-R77, E9, EC22, EC24, AC9, AC27
- Level: integration
- Fixture/setup: Fixtures with two pass events, pass plus fail, pass plus blocked, skipped/not-run events, duplicate stage IDs, and stored stage-list drift.
- Steps: Run the validator against each fixture.
- Expected result: `stages_validated` equals ordered pass-event stage IDs only; duplicate IDs and drift fail.
- Failure proves: Summary stage evidence can drift from event truth.
- Automation location: `scripts/test-change-metadata-validator.py`.

### TCVM-016. Skipped and not-run event handling

- Covers: R39-R40, R50, R77, R80-R81, EC23, EC25, AC27
- Level: integration
- Fixture/setup: Fixtures for skipped with accepted owner decision, skipped without decision, required not-run with blocker, and required not-run without blocker.
- Steps: Run the validator against each fixture.
- Expected result: Accepted skipped events are excluded and valid; unaccepted skipped and blockerless required not-run events fail.
- Failure proves: Planned or skipped validation can silently disappear.
- Automation location: `scripts/test-change-metadata-validator.py`.

### TCVM-017. Review-artifact count cross-checking

- Covers: R43-R44, R49, R82, EC8, AC22
- Level: integration
- Fixture/setup: Compact fixtures referencing a review-artifact root with matching counts, mismatched counts, missing parser preconditions, and final-count drift.
- Steps: Run `validate-change-metadata.py` against each fixture; run `validate-review-artifacts.py --mode closeout` on the matching root as supporting proof.
- Expected result: Matching counts pass; mismatches and unavailable cross-check preconditions fail or report blocked validation state.
- Failure proves: Structured counts are unchecked copied summary.
- Automation location: `scripts/test-change-metadata-validator.py` and `scripts/validate-review-artifacts.py`.

### TCVM-018. Stable compact error messages

- Covers: R62
- Level: integration
- Fixture/setup: Representative invalid fixtures from M1-M3.
- Steps: Assert validator stderr contains stable check IDs or stable messages for each invalid compact fixture class.
- Expected result: Errors are actionable enough for fixture tests and reviewer repair.
- Failure proves: Compact validation failures are hard to test or diagnose.
- Automation location: `scripts/test-change-metadata-validator.py`.

### TCVM-019. Compactness proof under reconstruction gate

- Covers: R59-R61, EC15, EC16, AC23
- Level: manual, contract
- Fixture/setup: A representative high-rerun legacy fixture and equivalent compact fixture, plus a deliberately lossy compact fixture and a trivial low-rerun fixture.
- Steps: First run reconstruction, summary, and count-preservation tests. Then measure common-read bytes or characters for the representative fixture pair. Confirm lossy fixture fails before size evaluation and trivial fixture is not used as the material proof.
- Expected result: Representative compact common-read metadata is at least 30% smaller after evidence preservation passes.
- Failure proves: Compactness can be bought by evidence loss or measured on the wrong surface.
- Automation location: `scripts/test-change-metadata-validator.py` for the measurement helper if practical; manual evidence recorded in milestone validation notes.

### TCVM-020. Validator does not execute validation bundles

- Covers: R57, R58, AC24
- Level: contract, integration
- Fixture/setup: Compact fixture with inert bundle command strings that would create a sentinel file if executed.
- Steps: Run `validate-change-metadata.py` against the fixture and assert no sentinel side effect occurs.
- Expected result: The validator validates recorded evidence shape only and never executes bundle commands.
- Failure proves: Metadata validation changes command execution behavior or creates unsafe side effects.
- Automation location: `scripts/test-change-metadata-validator.py`.

### TCVM-021. Schema remains compatible with current change metadata

- Covers: R1-R7, compatibility behavior
- Level: migration, smoke
- Fixture/setup: Current active change metadata and existing fixture corpus.
- Steps: Run `python scripts/test-change-metadata-validator.py` and `python scripts/validate-change-metadata.py docs/changes/2026-05-21-compact-change-validation-metadata/change.yaml`.
- Expected result: Current metadata remains valid while compact fixtures are added.
- Failure proves: Schema or semantic changes broke repository-local workflow metadata.
- Automation location: `scripts/test-change-metadata-validator.py`; direct validation command.

### TCVM-022. Selected validation still routes changed metadata surfaces

- Covers: R57, R58, operational validation boundary
- Level: smoke
- Fixture/setup: Changed validator, schema, fixture, plan, and change metadata paths.
- Steps: Run selected CI named by the plan after implementation milestones.
- Expected result: Selected validation includes change metadata validation, regression tests, lifecycle validation, and review-artifact validation as appropriate.
- Failure proves: The change weakened selected validation coverage.
- Automation location: `bash scripts/ci.sh --mode explicit --path ...` command from the plan.

### TCVM-023. Ordinary reviewer can inspect compact `change.yaml` alone

- Covers: R32, R55-R56, E6, AC21
- Level: manual, contract
- Fixture/setup: Valid compact fixture with transcript reference and path-expanding bundle evidence.
- Steps: Inspect only `change.yaml` and confirm bundle IDs, reconstructed command/path-set inputs, stage results, counts, blockers, and failure details are available without opening the transcript.
- Expected result: Transcript provides forensic depth but is not required for ordinary validation verdict.
- Failure proves: The common-read artifact became insufficient.
- Automation location: Manual evidence in milestone validation notes.

### TCVM-024. Final selected CI and lifecycle smoke

- Covers: R57-R58, AC24
- Level: smoke
- Fixture/setup: Completed implementation diff.
- Steps: Run the plan's selected CI command, lifecycle validation, metadata validation, review-artifact closeout validation, and `git diff --check --`.
- Expected result: Repository-owned validation passes without broadening command selection semantics.
- Failure proves: The implementation has changed validation behavior or left lifecycle evidence stale.
- Automation location: Plan validation commands.

## Fixtures and data

- Reuse existing fixtures in `tests/fixtures/change-metadata/`.
- Add compact fixture roots under `tests/fixtures/change-metadata/`, including at minimum:
  - `compact-valid/change.yaml`
  - `compact-invalid-mixed-shape/change.yaml`
  - `compact-invalid-unresolved-var/change.yaml`
  - `compact-invalid-brace-syntax/change.yaml`
  - `compact-invalid-unsafe-path/change.yaml`
  - `compact-invalid-lifecycle-stage/change.yaml`
  - `compact-invalid-first-exists/change.yaml`
  - `compact-invalid-summary-conflict/change.yaml`
  - `compact-invalid-count-conflict/change.yaml`
  - `compact-invalid-transcript-missing/change.yaml`
  - `compact-invalid-reconstruction-loss/change.yaml`
- Add a representative high-rerun legacy/compact fixture pair for compactness proof. The pair must preserve equivalent validation stages, bundles, reconstructed path sets, results, and counts.
- Add or reuse review-artifact fixture roots when structured count cross-checks need concrete review records, review logs, and review-resolution files.
- Do not use machine-local paths, secrets, credentials, usernames, hostnames, or private URLs in fixtures.

## Mocking/stubbing policy

- Prefer real file fixtures and subprocess validation over mocks for CLI behavior.
- Unit-test pure helper functions directly when parsing, lifecycle-stage ordering, or size measurement would be awkward through only subprocess fixtures.
- Do not mock the review-artifact parser for count cross-check success; use real parser output or a parser helper exposed by the existing implementation.
- It is acceptable to use a sentinel-command fixture to prove bundle commands are not executed, but the validator must not execute shell commands during the test.

## Migration or compatibility tests

- Legacy valid fixtures continue to pass.
- Compact files require explicit `schema_version: 2`.
- Legacy and compact files may coexist in the repository.
- Mixed legacy and compact validation evidence in a single file fails.
- Existing clean-receipt review metadata semantics remain valid.
- Rollback safety is proven by keeping legacy fixtures independent of compact-only sections.

## Observability verification

- Validator errors must include stable check IDs or stable messages for compact failures.
- Valid compact metadata must expose `all_passed`, `stages_validated`, final counts, and blockers directly in `change.yaml`.
- Dangling transcript references must be reported.
- Implementation and final verification must record the exact validation commands run in the active plan and change metadata.

## Security/privacy verification

- Test unsafe path cases for absolute paths, home paths, parent-directory escapes, hostnames, usernames, credential-bearing URLs, proxy URLs, token-like values, and private-key-like values.
- Confirm transcript references are repository-relative and cannot point outside the repository.
- Confirm bundle commands are validated as recorded evidence and never executed by metadata validation.

## Performance checks

- Compact metadata validation should remain linear in bundles, events, path variables, referenced paths, and referenced review artifacts.
- Add a high-rerun representative fixture to ensure path accumulation and summary derivation are not quadratic in ordinary use.
- No benchmark threshold is required beyond the approved compactness proof; implementation should avoid repeated full parser passes when one parser pass can provide review counts.

## Manual QA checklist

- Inspect the representative compact fixture and confirm a reviewer can answer which bundles ran, which paths were checked at each stage, which stages passed, and which blockers remain without opening a transcript.
- Inspect the compactness proof and confirm the 30% reduction is measured on the `change.yaml` common-read surface after reconstruction passes.
- Confirm final implementation evidence names the exact validation commands run.

## What not to test and why

- Do not test bulk migration of historical `change.yaml` files; bulk migration is out of scope.
- Do not test internal transcript schema fields; first slice validates references only.
- Do not test CLI scaffolding that writes compact metadata; scaffolding is deferred.
- Do not test review-record semantic changes; review-artifact semantics remain governed by existing validators.
- Do not execute validation bundle commands from metadata; the validator must not run them.
- Do not require external CI logs as proof; compact `change.yaml` remains the ordinary evidence surface.

## Uncovered gaps

None. The approved spec and plan provide enough contract and sequencing for fixture-driven implementation.

## Next artifacts

```text
implement M1
code-review M1
implement M2
code-review M2
implement M3
code-review M3
explain-change
verify
pr
```

## Follow-on artifacts

None yet

## Readiness

Active proof-planning surface for `implement M1`. This test spec does not claim implementation, code-review, verification, branch, or PR readiness.
