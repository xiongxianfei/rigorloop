# Change-Record Catalog Registration and Bounded Read Model Test Spec

## Status

active

## Related spec and plan

- Spec: [Change-Record Catalog Registration and Bounded Read Model](change-record-catalog-registration-and-bounded-read-model.md), approved.
- Plan: [Change-Record Catalog Registration and Bounded Read Model Plan](../docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md), active.
- Architecture: [System Architecture](../docs/architecture/system/architecture.md).
- ADR: [ADR-20260522-change-record-catalog-registration-and-bounded-read-model](../docs/adr/ADR-20260522-change-record-catalog-registration-and-bounded-read-model.md), accepted.
- Spec reviews: `spec-review-r2` approved the revised spec with no material findings.
- Architecture review: `architecture-review-r1` approved the architecture and ADR with no material findings.
- Plan review: `plan-review-r1` approved the plan with no material findings.

## Testing strategy

- Unit tests exercise isolated selector registry behavior, bounded filename matching, broad-pattern rejection, ambiguous-match detection, query output construction, metadata shape detection, and query command parsing where those functions can be tested without subprocess overhead.
- Integration tests execute repository-owned CLIs: `scripts/select-validation.py`, `scripts/ci.sh`, `scripts/query-change-record.py`, metadata validators, skill validators, and generated adapter checks.
- End-to-end proof is milestone-scoped selected CI over the changed files plus final branch-local changed-path proof through `bash scripts/ci.sh --mode local`; no external service or UI e2e path is required.
- Smoke tests run the new query helper against the active change record after M3 and run selector local mode after Workstream A creates deterministic evidence files.
- Manual verification is limited to reviewing behavior-preservation and selector-routing proof artifacts, confirming full-read escalation guidance remains available, and checking that no workflow semantics are claimed as changed.
- Contract tests assert selector safety, selected-check coverage, command exit behavior, query/validation separation, repo-relative path output, and generated adapter boundaries.
- Migration tests prove existing valid legacy and compact `change.yaml` shapes remain valid and either queryable or rejected with stable unsupported-shape diagnostics; historical change records are not bulk-migrated.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| CRM-R1 | CRM-T001, CRM-T002 | unit, integration | Registry exists for recurring deterministic evidence classes. |
| CRM-R2 | CRM-T001 | unit | Entry shape includes all required fields. |
| CRM-R3 | CRM-T001 | unit | Stable ASCII IDs with no whitespace. |
| CRM-R4 | CRM-T002, CRM-T003 | unit | Evidence-class-specific patterns only. |
| CRM-R5 | CRM-T003 | unit | Broad catch-all patterns fail. |
| CRM-R6 | CRM-T002 | unit | Exact filename entries remain supported. |
| CRM-R7 | CRM-T004, CRM-T006 | integration | Evidence files route exactly once or diagnose. |
| CRM-R8 | CRM-T006 | integration | Unregistered evidence cannot silently pass. |
| CRM-R9 | CRM-T004 | integration | Registered evidence selects declared checks and roots. |
| CRM-R10 | CRM-T004 | integration | Lifecycle routes include governing `change.yaml`. |
| CRM-R11 | CRM-T005 | integration | Registry changes select selector regression coverage. |
| CRM-R12 | CRM-T008 | integration | Actual changed-path proof is required before verify. |
| CRM-R13 | CRM-T008 | contract | Fixtures are supplemental only. |
| CRM-R14 | CRM-T008 | contract | Explicit paths cannot replace changed-path proof. |
| CRM-R15 | CRM-T007, CRM-T008 | integration | Late verify discovery is prevented by earlier proof. |
| CRM-R16 | CRM-T007 | integration | `manual-routing-required` creates registration debt. |
| CRM-R17 | CRM-T007, CRM-T009 | integration, manual | Debt is resolved or explicitly deferred before verify. |
| CRM-R18 | CRM-T009 | integration | Deferral shape names owner, path, reason, impact, follow-up. |
| CRM-R19 | CRM-T007, CRM-T009 | integration | Unresolved diagnostics block verify readiness. |
| CRM-R20 | CRM-T020 | manual | First implementation slice is Workstream A only. |
| CRM-R21 | CRM-T020 | manual | Workstream A does not require query helper or skill edits. |
| CRM-R22 | CRM-T010 | contract | Bounded read contract exists for common questions. |
| CRM-R23 | CRM-T010 | contract | Questions map to smallest authoritative surfaces. |
| CRM-R24 | CRM-T010 | contract | Live workflow state stays active-plan-owned. |
| CRM-R25 | CRM-T010 | contract | Durable rationale stays explain-change-owned. |
| CRM-R26 | CRM-T010 | contract | Review status stays review-log/resolution-owned. |
| CRM-R27 | CRM-T010, CRM-T013 | integration | Validation inventory may come from change metadata. |
| CRM-R28 | CRM-T011, CRM-T013 | integration | Final validation state comes from summary or equivalent. |
| CRM-R29 | CRM-T012 | integration | Artifact paths available from metadata/query helper. |
| CRM-R30 | CRM-T011, CRM-T012, CRM-T013, CRM-T014 | integration | Required query commands exist. |
| CRM-R31 | CRM-T015 | integration | Optional commands are tested when implemented. |
| CRM-R32 | CRM-T011 | integration | `summary` includes required fields. |
| CRM-R33 | CRM-T012 | integration | `artifacts` emits only canonical paths. |
| CRM-R34 | CRM-T013 | integration | Latest validation output is latest-slice only. |
| CRM-R35 | CRM-T014 | integration | Stage validation output is stage-scoped. |
| CRM-R36 | CRM-T016 | migration | Legacy and compact valid metadata are supported when safe. |
| CRM-R37 | CRM-T016, CRM-T017 | integration | Unsupported shapes produce stable diagnostics. |
| CRM-R38 | CRM-T011, CRM-T013, CRM-T017 | integration | Failures, blockers, skipped validation, and diagnostics remain visible. |
| CRM-R39 | CRM-T018 | contract | Query helper never executes validation commands. |
| CRM-R40 | CRM-T018 | contract | Query output is deterministic. |
| CRM-R41 | CRM-T018 | security | Query output uses repo-relative paths only. |
| CRM-R42 | CRM-T019 | manual | Compact common-read ordering is reviewed only if metadata is amended. |
| CRM-R43 | CRM-T019 | manual | Full-read escalation remains allowed. |
| CRM-R44 | CRM-T021 | integration | Skills name bounded slices or query commands. |
| CRM-R45 | CRM-T021 | integration | Skills name full-read escalation conditions. |
| CRM-R46 | CRM-T021 | integration | Skills avoid broad-only `change.yaml` guidance. |
| CRM-R47 | CRM-T020, CRM-T021 | manual, integration | Skill guidance waits for stable helper commands. |
| CRM-R48 | CRM-T022 | integration | Generated adapters are validated after skill edits. |
| CRM-R49 | CRM-T023 | contract | Workflow stage and readiness semantics are unchanged. |
| CRM-R50 | CRM-T005, CRM-T023 | contract | Selector safety and selected-check behavior are preserved. |
| CRM-R51 | CRM-T016, CRM-T023 | migration | Existing valid change records remain valid. |
| CRM-R52 | CRM-T016, CRM-T023 | migration | Historical records are not bulk-migrated in first slice. |
| CRM-R53 | CRM-T018 | contract | Query behavior uses new script, not validator subcommands. |
| CRM-R54 | CRM-T001 | manual, unit | Centralized registry is preferred when selector architecture supports it. |
| CRM-R55 | CRM-T001, CRM-T002 | unit | In-selector registry table is acceptable with fixture-backed tests. |
| CRM-R56 | CRM-T024 | manual | Spec remains top-level contract with dependency references. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | CRM-T004, CRM-T008 | Registered preservation evidence routes without `manual-routing-required`. |
| E2 | CRM-T006, CRM-T007 | Unregistered evidence creates stable registration debt before verify. |
| E3 | CRM-T003 | Broad `*.md` evidence patterns are rejected. |
| E4 | CRM-T008 | Actual changed paths are required; fixtures are supplemental. |
| E5 | CRM-T011, CRM-T016 | Summary query returns common fields without full validation history. |
| E6 | CRM-T013 | Latest validation query returns latest validation slice only. |
| E7 | CRM-T014 | Stage validation query excludes unrelated stage events. |
| E8 | CRM-T019, CRM-T021 | Full-read escalation remains available in helper pointers and skill guidance. |
| E9 | CRM-T021, CRM-T022 | Updated skills name slices and pass generated adapter validation. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 | CRM-T004 | Registered `behavior-preservation.md` routes through preservation. |
| EC2 | CRM-T003 | Multiple matching evidence classes fail as ambiguous. |
| EC3 | CRM-T006 | Unregistered `notes.md` emits `manual-routing-required`. |
| EC4 | CRM-T003 | `*.md` fails broad-pattern validation. |
| EC5 | CRM-T002 | `*-audit.md` can pass with complete entry metadata. |
| EC6 | CRM-T008 | Explicit-path-only proof remains incomplete. |
| EC7 | CRM-T009 | Owner-approved unsupported status can unblock verify. |
| EC8 | CRM-T007 | Unresolved unregistered evidence blocks readiness. |
| EC9 | CRM-T011, CRM-T016 | Compact summary query avoids transcript internals. |
| EC10 | CRM-T011, CRM-T016 | Legacy summary returns supported equivalents or stable unsupported-shape diagnostic. |
| EC11 | CRM-T013 | No validation evidence returns stable diagnostic. |
| EC12 | CRM-T014 | Unknown stage returns stable stage-not-found diagnostic. |
| EC13 | CRM-T017, CRM-T018 | Malformed YAML fails closed and does not modify files. |
| EC14 | CRM-T019, CRM-T021 | Disputed validation history escalates to full read. |
| EC15 | CRM-T010, CRM-T021 | Live state reads active plan, not `change.yaml`. |
| EC16 | CRM-T020 | Skill edits before helper command stability are rejected by sequencing review. |
| EC17 | CRM-T022 | Skill edits without adapter validation fail readiness. |
| EC18 | CRM-T001, CRM-T002 | In-selector registry table with fixture-backed tests satisfies first slice. |

## Test cases

### CRM-T001. Evidence registry entry contract

- Covers: CRM-R1, CRM-R2, CRM-R3, CRM-R54, CRM-R55, EC18, AC-CRM-001
- Level: unit
- Fixture/setup: Selector registry entries in the chosen selector-owned registry surface; invalid entries missing ID, route, validator, allowed root, lifecycle stage, or conditions.
- Steps: Add focused unit coverage that instantiates or validates registry entries and invalid variants.
- Expected result: Complete entries pass; missing fields, whitespace IDs, non-ASCII IDs, and unsupported registry shapes fail before selector routing relies on them.
- Failure proves: Evidence class registration can be incomplete or unstable.
- Automation location: `scripts/test-select-validation.py`.

### CRM-T002. Registered patterns and exact filenames route by class

- Covers: CRM-R4, CRM-R6, CRM-R7, EC5, EC18, AC-CRM-001, AC-CRM-002
- Level: unit
- Fixture/setup: Registered patterns such as `*-audit.md`, `*-identity.txt`, `*-preservation.md`, `behavior-preservation.md`, `baseline.md`, plus one exact filename for a novel class.
- Steps: Exercise selector matching for each fixture path under `docs/changes/2026-05-22-example/`.
- Expected result: Each path matches exactly one class and produces the declared selector route metadata.
- Failure proves: The registry cannot support recurring evidence classes without one-off selector patches.
- Automation location: `scripts/test-select-validation.py`.

### CRM-T003. Broad and ambiguous evidence patterns fail closed

- Covers: CRM-R4, CRM-R5, EC2, EC4, AC-CRM-006, AC-CRM-007
- Level: unit
- Fixture/setup: Invalid registry entries using `*.md`, `*.txt`, equivalent broad patterns, and overlapping patterns that match the same evidence path.
- Steps: Run registry validation and selector fixture tests for broad and ambiguous entries.
- Expected result: Broad catch-all patterns and ambiguous matches fail with stable diagnostics before route selection.
- Failure proves: The registry can silently capture unrelated evidence or route one path through multiple classes.
- Automation location: `scripts/test-select-validation.py`.

### CRM-T004. Registered evidence selects declared checks and governing metadata

- Covers: CRM-R7, CRM-R9, CRM-R10, E1, EC1, AC-CRM-002
- Level: integration
- Fixture/setup: Registered evidence file paths under `docs/changes/2026-05-22-example/`, including `behavior-preservation.md`, plus governing `change.yaml`.
- Steps: Run `python scripts/select-validation.py --mode explicit --path <registered evidence path>` and selected CI explicit mode over representative registered evidence.
- Expected result: Output includes declared selected check IDs, affected root, and governing `change.yaml` when lifecycle context is required; no `manual-routing-required` appears.
- Failure proves: Registered evidence does not route deterministically through the selector.
- Automation location: `scripts/test-select-validation.py`; `bash scripts/ci.sh --mode explicit ...`.

### CRM-T005. Registry changes select selector regression and preserve selected-check behavior

- Covers: CRM-R11, CRM-R50, AC-CRM-005, AC-CRM-015, AC-CRM-017
- Level: integration, contract
- Fixture/setup: Changed selector registry source, selector tests, and representative existing route fixtures.
- Steps: Run selector tests and selected CI explicit mode over registry/test paths; compare pre-existing route expectations except intended evidence additions.
- Expected result: `selector.regression` is selected for registry changes, existing valid routes stay stable, and selected-check exit behavior is unchanged.
- Failure proves: Registry work can bypass selector regression or weaken selected-CI coverage.
- Automation location: `scripts/test-select-validation.py`; `bash scripts/ci.sh --mode explicit ...`.

### CRM-T006. Unregistered deterministic evidence produces stable manual-routing diagnostic

- Covers: CRM-R7, CRM-R8, E2, EC3, AC-CRM-003
- Level: integration
- Fixture/setup: Deterministic evidence path such as `docs/changes/2026-05-22-example/notes.md` that matches no registry entry.
- Steps: Run `python scripts/select-validation.py --mode explicit --path <unregistered evidence path>` and direct selector tests.
- Expected result: Selector output includes stable `manual-routing-required` for that path and does not select a silent pass route.
- Failure proves: Unregistered evidence can evade deterministic routing.
- Automation location: `scripts/test-select-validation.py`.

### CRM-T007. Registration debt blocks readiness without resolution

- Covers: CRM-R15, CRM-R16, CRM-R17, CRM-R19, E2, EC8, AC-CRM-004
- Level: integration
- Fixture/setup: Branch or fixture changed-path set containing unregistered deterministic evidence and no owner-approved deferral.
- Steps: Run local selector mode or equivalent changed-set fixture used only for this negative case; run selected CI wrapper if the diagnostic is surfaced there.
- Expected result: Output identifies registration debt and verify readiness remains blocked until the path is registered or deferred.
- Failure proves: `manual-routing-required` remains a late diagnostic rather than tracked debt.
- Automation location: `scripts/test-select-validation.py`; `python scripts/select-validation.py --mode local`; `bash scripts/ci.sh --mode local`.

### CRM-T008. Actual changed-path proof is required before verify

- Covers: CRM-R12, CRM-R13, CRM-R14, CRM-R15, E4, EC6, AC-CRM-005
- Level: integration, contract
- Fixture/setup: This branch's actual changed paths after Workstream A adds deterministic evidence files, plus supplemental selector fixtures.
- Steps: Run `python scripts/select-validation.py --mode local`; record selector-routing proof; separately run explicit-path validation to prove it does not substitute for local changed-path routing.
- Expected result: Actual branch changed paths are routed before verify; fixture and explicit-path commands are recorded only as supplemental proof.
- Failure proves: The implementation can recreate the original verify-stage routing surprise.
- Automation location: `scripts/test-select-validation.py`; `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/selector-routing-proof.md`.

### CRM-T009. Owner-approved unsupported deferral has required shape

- Covers: CRM-R17, CRM-R18, CRM-R19, EC7, AC-CRM-004
- Level: integration, manual
- Fixture/setup: Registration-debt fixture with accepted unsupported status and invalid variants missing owner, path, reason, validation impact, or follow-up.
- Steps: Validate the deferral parser or review-visible evidence shape; manually confirm the active plan records any real deferral before verify.
- Expected result: Complete owner-approved deferral can unblock readiness; incomplete deferrals fail and unresolved diagnostics remain blocking.
- Failure proves: `manual-routing-required` can become an undocumented workaround.
- Automation location: `scripts/test-select-validation.py` or a targeted lifecycle/review artifact test if the implementation stores deferrals outside the selector.

### CRM-T010. Bounded read source ownership map is enforced

- Covers: CRM-R22, CRM-R23, CRM-R24, CRM-R25, CRM-R26, CRM-R27, EC15
- Level: contract
- Fixture/setup: Static source ownership map in query helper docs/tests or code, active plan fixture, explain-change fixture, review log/resolution fixture, and change metadata fixture.
- Steps: Assert common questions map to active plan, explain-change, review artifacts, or change metadata as specified.
- Expected result: Live workflow state is not sourced from `change.yaml`; validation inventory remains queryable from metadata.
- Failure proves: The read model keeps treating `change.yaml` as the default state oracle.
- Automation location: `scripts/test-query-change-record.py`.

### CRM-T011. Query `summary` returns common-read slice only

- Covers: CRM-R28, CRM-R30, CRM-R32, CRM-R38, E5, EC9, EC10, AC-CRM-008
- Level: integration
- Fixture/setup: Legacy and compact `change.yaml` fixtures with artifact paths, review state, validation summary, blockers, detail pointers, and validation history.
- Steps: Run `python scripts/query-change-record.py <change-id> summary` for compact, legacy, and active change records.
- Expected result: Output includes change ID, canonical artifact paths, review state, latest validation state, open blockers, and detail pointers without dumping full validation event history.
- Failure proves: Summary reads remain broad or hide blockers/failures.
- Automation location: `scripts/test-query-change-record.py`.

### CRM-T012. Query `artifacts` returns canonical paths only

- Covers: CRM-R29, CRM-R30, CRM-R33, AC-CRM-009
- Level: integration
- Fixture/setup: Metadata fixtures with canonical artifacts and unrelated metadata fields.
- Steps: Run `python scripts/query-change-record.py <change-id> artifacts`.
- Expected result: Output contains canonical repo-relative artifact paths only and excludes review state, validation details, blockers, and transcript text.
- Failure proves: Artifact queries are not bounded to artifact path ownership.
- Automation location: `scripts/test-query-change-record.py`.

### CRM-T013. Query `validation --latest` returns latest validation slice

- Covers: CRM-R27, CRM-R28, CRM-R30, CRM-R34, CRM-R38, E6, EC11, AC-CRM-010
- Level: integration
- Fixture/setup: Change metadata fixtures with multiple validation stages, non-pass latest events, blockers, counts, and optional transcript pointers; fixture with no validation evidence.
- Steps: Run `python scripts/query-change-record.py <change-id> validation --latest`.
- Expected result: Output contains only latest stage, bundles, result, counts, blockers, and transcript pointer when present; no-validation fixture returns a stable diagnostic.
- Failure proves: Latest validation query either hides failure evidence or reads unnecessary history.
- Automation location: `scripts/test-query-change-record.py`.

### CRM-T014. Query `validation --stage <stage>` is stage-scoped

- Covers: CRM-R30, CRM-R35, E7, EC12, AC-CRM-011
- Level: integration
- Fixture/setup: Change metadata fixtures with proposal-review, spec-review, plan-review, code-review, and an absent stage.
- Steps: Run `python scripts/query-change-record.py <change-id> validation --stage spec-review-r1` and an unknown stage query.
- Expected result: Known stage output includes only requested stage evidence and detail pointers; unknown stage reports stable stage-not-found diagnostic.
- Failure proves: Stage-scoped reads leak unrelated validation events or guess on missing stages.
- Automation location: `scripts/test-query-change-record.py`.

### CRM-T015. Optional query subcommands are covered when implemented

- Covers: CRM-R31
- Level: integration
- Fixture/setup: Any implemented optional `review`, `blockers`, or `forensic` subcommands.
- Steps: If an optional subcommand is implemented in the slice, add fixture-backed tests for its output and diagnostics.
- Expected result: Implemented optional commands have deterministic bounded outputs; unimplemented optional commands are not advertised as supported.
- Failure proves: Optional query surfaces can drift outside the specified read contract.
- Automation location: `scripts/test-query-change-record.py` when applicable.

### CRM-T016. Legacy and compact metadata compatibility

- Covers: CRM-R36, CRM-R51, CRM-R52, E5, EC9, EC10, AC-CRM-012, AC-CRM-015
- Level: migration
- Fixture/setup: Existing valid legacy fixtures, valid compact fixtures, representative historical `docs/changes/*/change.yaml`, and active change metadata.
- Steps: Run `python scripts/test-change-metadata-validator.py`; run query helper against supported legacy and compact fixtures.
- Expected result: Existing valid metadata remains valid; supported shapes query successfully; unsupported safe-query shapes return stable diagnostics without forcing bulk migration.
- Failure proves: The read model breaks historical change records or requires first-slice migration.
- Automation location: `scripts/test-change-metadata-validator.py`; `scripts/test-query-change-record.py`.

### CRM-T017. Query errors are stable and fail closed

- Covers: CRM-R37, CRM-R38, EC13, AC-CRM-012
- Level: integration
- Fixture/setup: Unknown change ID, unknown subcommand, invalid option, malformed YAML, ambiguous metadata, unsupported valid shape, and invalid shape fixtures.
- Steps: Run query helper commands for each error case and assert exit status and stable diagnostic label.
- Expected result: Each case fails or reports unsupported shape without guessing, hiding blockers, or modifying files.
- Failure proves: Query helper behavior is unsafe under malformed or ambiguous inputs.
- Automation location: `scripts/test-query-change-record.py`.

### CRM-T018. Query helper safety, determinism, and command boundary

- Covers: CRM-R39, CRM-R40, CRM-R41, CRM-R53, EC13
- Level: contract, security
- Fixture/setup: Metadata fixture containing validation command strings, repo-relative paths, and invalid absolute/home/host-specific path values.
- Steps: Run query helper twice against the same state; assert identical output; assert validation command strings are not executed; assert outputs are repo-relative and the helper is a standalone script rather than a `validate-change-metadata.py` subcommand.
- Expected result: Querying is read-only, deterministic, path-safe, and separated from validation execution.
- Failure proves: Query behavior can execute proof commands, leak local paths, or blur query/validation responsibilities.
- Automation location: `scripts/test-query-change-record.py`.

### CRM-T019. Full-read escalation remains available

- Covers: CRM-R42, CRM-R43, E8, EC14, AC-CRM-014
- Level: manual, contract
- Fixture/setup: Query output or diagnostics with detail pointers; stage-skill guidance after M4.
- Steps: Review query output and affected skill text for escalation conditions covering forensic reconstruction, disputed evidence, unsupported shapes, selector debugging, migration validation, and whole-record review.
- Expected result: Bounded reads are default for common questions, and full reads remain explicitly allowed when needed.
- Failure proves: The feature over-narrows reads and makes audits harder.
- Automation location: Manual review plus targeted static assertions in `scripts/test-query-change-record.py` or `scripts/test-skill-validator.py`.

### CRM-T020. Workstream sequencing is preserved

- Covers: CRM-R20, CRM-R21, CRM-R47, EC16
- Level: manual
- Fixture/setup: Active plan, milestone diffs, and code-review evidence for M1/M2 before M3/M4.
- Steps: During milestone closeout, confirm Workstream A commits do not require `scripts/query-change-record.py` or skill guidance changes, and confirm M4 starts only after M3 command names are stable.
- Expected result: Selector routing risk and query/skill guidance risk remain separately reviewable and rollbackable.
- Failure proves: The implementation recombines the workstreams the proposal/spec intentionally separated.
- Automation location: Manual plan/code-review checklist.

### CRM-T021. Stage-skill bounded read guidance

- Covers: CRM-R44, CRM-R45, CRM-R46, CRM-R47, E8, E9, EC14, EC15, AC-CRM-013, AC-CRM-014
- Level: integration
- Fixture/setup: Canonical affected skills under `skills/`, stable query helper command help/output, and invalid skill text that says only "read `change.yaml`" for a common question.
- Steps: Run skill validator/static tests asserting bounded slice or query command references and full-read escalation conditions.
- Expected result: Affected skills name slices/commands for common stage-owned questions, keep active plan as live-state owner, and include escalation conditions.
- Failure proves: Bounded reading remains discipline-only or skill guidance drifts from the helper.
- Automation location: `scripts/test-skill-validator.py`; `python scripts/validate-skills.py`.

### CRM-T022. Generated adapter proof for skill changes

- Covers: CRM-R48, E9, EC17, AC-CRM-016
- Level: integration
- Fixture/setup: Canonical skill edits from M4 and generated adapter check surfaces.
- Steps: Run `python scripts/validate-skills.py`, `python scripts/test-skill-validator.py`, `python scripts/build-skills.py --check`, and `python scripts/build-adapters.py --check`.
- Expected result: Canonical skill text validates and generated adapter output is reproducible.
- Failure proves: Public adapter guidance can drift after bounded-read skill edits.
- Automation location: skill and adapter validation commands in M4.

### CRM-T023. Compatibility and selected-CI preservation

- Covers: CRM-R49, CRM-R50, CRM-R51, CRM-R52, AC-CRM-015, AC-CRM-017
- Level: contract, smoke, migration
- Fixture/setup: Existing selector route fixtures, valid metadata fixtures, workflow/lifecycle artifacts, active plan, and branch changed paths.
- Steps: Run milestone-selected CI and final selected CI; run existing selector and metadata regression suites.
- Expected result: Stage order, statuses, lifecycle semantics, readiness semantics, selected-check coverage, command exit behavior, and existing valid change records remain valid.
- Failure proves: The feature changed governance or validation semantics beyond the approved scope.
- Automation location: `python scripts/test-select-validation.py`; `python scripts/test-change-metadata-validator.py`; `bash scripts/ci.sh --mode local`.

Final branch-local changed-path selected-CI proof uses the repository-supported local wrapper mode:

```bash
bash scripts/ci.sh --mode local
```

`bash scripts/ci.sh --mode selected` is not a supported `scripts/ci.sh` mode in the current repository interface and must not be listed as the final verification proof command.

### CRM-T024. Spec dependency references remain authoritative

- Covers: CRM-R56
- Level: manual
- Fixture/setup: Feature spec dependency references, related selector/metadata/workflow/skill specs, architecture, ADR, and test spec.
- Steps: Review any implementation-driven spec amendments for preserved dependency references and no replacement of existing ownership surfaces.
- Expected result: This feature spec remains the top-level contract while dependent specs keep their existing ownership.
- Failure proves: The feature silently overrides selector, metadata, workflow, or skill-contract ownership.
- Automation location: Manual spec/architecture review during M5 if amendments occur.

## Fixtures and data

- Extend `scripts/test-select-validation.py` with inline fixtures or fixture files for registered evidence, unregistered evidence, broad patterns, ambiguous patterns, selector-owned registry edits, and actual-changed-path proof behavior.
- Add `scripts/test-query-change-record.py` and fixtures under `tests/fixtures/change-record-query/` or `tests/fixtures/change-metadata/` for compact metadata, legacy metadata, malformed YAML, unsupported shape, no validation evidence, unknown stage, blockers, skipped validation, transcript pointers, and unsafe path values.
- Use this change root as the active smoke fixture: `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/`.
- Add `behavior-preservation.md` and `selector-routing-proof.md` change-local evidence as required by the plan.
- Use existing valid legacy and compact metadata fixtures from `scripts/test-change-metadata-validator.py` where they already cover compatibility.

## Mocking/stubbing policy

- Do not mock selector output for selector tests; call selector functions or CLI paths that exercise the real routing logic.
- Do not mock query-helper metadata loading for integration tests; use real fixture `change.yaml` files.
- Subprocess execution may be stubbed only to prove `scripts/query-change-record.py` does not execute validation commands from metadata.
- Generated adapter checks must use the repository-owned build/check scripts, not hand-authored expected output.
- Avoid snapshots for full command output; assert stable labels, required fields, omitted fields, selected check IDs, affected roots, and exit status.

## Migration or compatibility tests

- `CRM-T016` covers legacy and compact metadata compatibility and unsupported-shape diagnostics.
- `CRM-T023` covers existing valid change records, existing selector routes, and unchanged workflow/readiness semantics.
- Historical unregistered evidence files are not bulk-migrated in the first slice; tests should not require historical file renames.
- Rollback proof is review-visible: Workstream A registry changes must be independently revertible from Workstream B query/skill changes.

## Observability verification

- Selector tests assert registered routes, selected check IDs, affected roots, and blocking `manual-routing-required` diagnostics.
- Registration debt must be visible in active plan evidence, change-local evidence, or owner-approved deferral before verify.
- Query tests assert stable diagnostic labels for not-found, usage, stage-not-found, unsupported-shape, parse failure, no-validation-evidence, and unsafe path cases.
- Query outputs must include detail pointers for escalation without dumping full history into bounded summaries.
- Implementation and review evidence must name the actual changed-path command used for Workstream A proof.

## Security/privacy verification

- Query output and selector diagnostics must use repo-relative paths only.
- Query helper tests must reject or avoid emitting home-directory paths, absolute paths, host-specific paths, usernames, proxy URLs, credentials, tokens, and secret-like values.
- Query helper tests must prove metadata command strings are not executed.
- Evidence registration tests must prove paths outside `docs/changes/<change-id>/` cannot become change-local evidence through broad patterns.
- Malformed or unsupported metadata must fail closed without broad filesystem reads.

## Performance checks

- Selector registry matching should be covered with enough representative changed paths and registered patterns to detect obvious superlinear or broad-scan behavior; no separate benchmark is required for the first slice.
- Query helper tests should include fixtures with multiple validation events and assert bounded commands omit unrelated event detail.
- Final selected CI must remain suitable for ordinary branch diffs; any noticeable slowdown should be recorded in the active plan and reviewed before PR.

## Manual QA checklist

- Confirm Workstream A closes before Workstream B skill guidance changes.
- Confirm `selector-routing-proof.md` records actual changed-path routing, not only explicit paths.
- Confirm `behavior-preservation.md` compares existing selector behavior before/after registry routing.
- Confirm query helper smoke commands answer the active change record without executing validation commands.
- Confirm affected skills reference stable helper commands or bounded slices only after M3 closes.
- Confirm generated adapter validation is recorded after skill edits.

## What not to test and why

- Do not test a bulk migration of historical change records; the approved first slice explicitly excludes it.
- Do not add tests that require query helper support for optional `review`, `blockers`, or `forensic` subcommands unless those subcommands are implemented.
- Do not test graphical accessibility; this feature has no UI.
- Do not treat broad snapshots of full `change.yaml` or full query output as proof; bounded fields and diagnostics are the contract.
- Do not require Workstream A to pass query-helper or skill-guidance tests before Workstream B begins.
- Do not test changes to workflow stage order, review status meanings, or branch/PR readiness semantics except to prove they remain unchanged.

## Uncovered gaps

None. If implementation discovers that owner-approved deferral needs a schema-owned storage location rather than selector or plan evidence, return to spec or architecture before adding that behavior.

## Next artifacts

```text
implement Workstream A M1
code-review
implement Workstream A M2
code-review
implement Workstream B M3
code-review
implement Workstream B M4
code-review
explain-change
verify
pr
```

## Follow-on artifacts

None yet

## Readiness

Active proof surface for M1 and later milestones.
