# Release Transaction Automation Test Spec

## Status

active

## Related spec and plan

- Spec: [Release Transaction Automation and Evidence Generation](release-transaction-automation.md), approved.
- Plan: [Release Transaction Automation Execution Plan](../docs/plans/2026-06-29-release-transaction-automation.md), active and approved by `plan-review-r1`.
- Architecture: [RigorLoop Canonical System Architecture](../docs/architecture/system/architecture.md), approved.
- ADR: [ADR-20260629 Release Transaction Profile](../docs/adr/ADR-20260629-release-transaction-profile.md), accepted.
- Change metadata: [change.yaml](../docs/changes/2026-06-29-release-transaction-automation/change.yaml).
- Review records:
  - `docs/changes/2026-06-29-release-transaction-automation/reviews/spec-review-r1.md`
  - `docs/changes/2026-06-29-release-transaction-automation/reviews/architecture-review-r1.md`
  - `docs/changes/2026-06-29-release-transaction-automation/reviews/plan-review-r1.md`

## Testing strategy

This test spec proves routine release automation without publishing a real package. The proof is split across release-profile schema validation, generated-surface ownership classification, generator idempotency, cheap preflight failures, full-gate preservation, workflow parity, published evidence closeout fixtures, timing evidence, security filtering, and lifecycle-state coherence.

- Unit tests cover release-profile parsing, closed vocabularies, routine/special classification, generated-surface classification, literal-audit classification, evidence-shape validators, timing file fields, command string normalization, hash formatting, and secret/private marker rejection.
- Integration tests cover `prepare-release`, `release-preflight`, `validate-release.py`, `release-verify.sh`, `.github/workflows/release.yml`, release evidence under `docs/releases/`, adapter artifact metadata fixtures, package metadata fixtures, and change/lifecycle validators.
- End-to-end tests use temporary repository fixtures for one routine release profile and generated pending/published evidence. They must not publish, create tags, push, create GitHub releases, or require npm credentials.
- Smoke tests use dry-run or fixture-safe commands only, such as `python scripts/release-preflight.py <fixture-tag>`, `python scripts/prepare-release.py <fixture-tag> --check` if implemented, and fixture-safe `bash scripts/release-verify.sh <fixture-tag>` or existing dry-run release-gate tests.
- Manual checks are limited to generated diff reviewability, release notes narrative preservation, and confirming full release-gate safety checks remain present when automation changes command wiring.
- Contract tests assert that preflight is not the full gate, generated release state derives from `docs/releases/profiles/<tag>.yaml`, local and CI release gates invoke the same repository-owned command set, and public closeout cannot mark evidence published before public proof exists.
- Migration tests preserve historical release evidence and fixtures; no test should require historical release migration or backfill.

## Proof-contract details

This section defines proof-shape decisions that implementation must not invent. Implementation may choose internal helper names, but it must not change these observable contracts without a test-spec revision and re-review.

### Generated-region marker contract

Profile-owned generated Markdown regions use this start marker:

```md
<!-- rigorloop:generated:start release-transaction surface=<surface-id> profile=<profile-path> -->
```

and this end marker:

```md
<!-- rigorloop:generated:end release-transaction surface=<surface-id> -->
```

The `release-transaction` namespace is literal. The `surface` value is a stable generated-surface ID from the closed first-slice enum below. The `profile` value is the release profile path, such as `docs/releases/profiles/v0.3.5.yaml`. Start and end markers must have the same namespace and surface ID. Nested `release-transaction` generated regions are forbidden.

Allowed first-slice generated surface IDs:

- `release-metadata`
- `adapter-artifact-expectations`
- `pending-npm-publication`
- `published-npm-publication`
- `target-init-smoke`
- `current-version-fixtures`
- `timing-evidence`

Generated-region proof tests:

| Test ID | Scenario | Expected |
| --- | --- | --- |
| TRTA-GEN-001 | Valid generated region markers | pass |
| TRTA-GEN-002 | Missing end marker | fail |
| TRTA-GEN-003 | Start/end surface mismatch | fail |
| TRTA-GEN-004 | Nested generated region | fail |
| TRTA-GEN-005 | Unknown surface ID | fail |
| TRTA-GEN-006 | Manual edit inside generated region without regeneration proof | fail or review-block |

### Literal-audit baseline artifact

The literal-audit baseline lives at:

```text
docs/changes/2026-06-29-release-transaction-automation/release-literal-audit-baseline.yaml
```

The baseline uses schema version `release-literal-audit-baseline-v1` and this shape:

```yaml
schema_version: release-literal-audit-baseline-v1
change_id: 2026-06-29-release-transaction-automation
baseline_created_at: <ISO-8601 timestamp>
audited_release_tag: v0.3.5
release_profile: docs/releases/profiles/v0.3.5.yaml

entries:
  - id: literal-baseline-001
    literal: v0.3.4
    file: scripts/example.py
    line: 42
    classification: historical-fixture
    expected_owner: historical-fixture
    disposition: allowed
    rationale: "Pinned historical release fixture."
```

Closed `classification` enum:

- `generated-current`
- `profile-owned`
- `historical-fixture`
- `version-independent`
- `baseline-drift`
- `unauthorized`

Closed `disposition` enum:

- `allowed`
- `report-only`
- `must-fix`

Newly changed unauthorized current-version literals fail. Existing baseline drift may be report-only until the audit is clean. Historical fixtures must be explicitly classified. Generated-current entries must point back to the release profile or generated region. Unauthorized entries require file, line, literal, and corrective action.

Literal-audit proof tests:

| Test ID | Scenario | Expected |
| --- | --- | --- |
| TRTA-LIT-001 | Valid baseline artifact | pass |
| TRTA-LIT-002 | Missing classification | fail |
| TRTA-LIT-003 | Unknown classification | fail |
| TRTA-LIT-004 | Newly changed unauthorized current literal | fail |
| TRTA-LIT-005 | Existing baseline drift marked report-only | pass with warning/report |
| TRTA-LIT-006 | Historical fixture without rationale | fail |
| TRTA-LIT-007 | Generated-current literal without profile/generated-region owner | fail |

### Timing evidence schema

Timing evidence lives at:

```text
docs/releases/<tag>/timing.yaml
```

and uses schema version `release-timing-v1`:

```yaml
schema_version: release-timing-v1
release_tag: v0.3.5
release_profile: docs/releases/profiles/v0.3.5.yaml
created_at: <ISO-8601 timestamp>

phases:
  - id: preflight
    command: python scripts/release-preflight.py v0.3.5
    duration_seconds: 12.34
    result: pass

checks:
  - id: adapter_distribution.regression
    command: python scripts/test-adapter-distribution.py
    phase: local_release_verify
    duration_seconds: 158.52
    result: pass
```

Closed first-slice `phase.id` enum:

- `prepare_release`
- `preflight`
- `local_release_verify`
- `ci_release_verify`
- `publication_wait`
- `public_closeout`

Closed `result` enum:

- `pass`
- `fail`
- `skipped`
- `pending`
- `not-applicable`

Missing required timing evidence fails when the release profile requires timing. A duration above target is warning-only in the first slice.

Timing proof tests:

| Test ID | Scenario | Expected |
| --- | --- | --- |
| TRTA-TIME-001 | Valid timing evidence | pass |
| TRTA-TIME-002 | Missing `duration_seconds` | fail |
| TRTA-TIME-003 | Unknown phase ID | fail |
| TRTA-TIME-004 | Unknown result value | fail |
| TRTA-TIME-005 | Duration over target | warning only |
| TRTA-TIME-006 | Missing timing when profile requires it | fail |

### Fixture layout

Release transaction fixtures live under:

```text
tests/fixtures/release-transaction/
  profiles/
  generated-regions/
  literal-audit/
  evidence/
  timing/
  commands/
```

Required first-slice fixture groups:

```text
tests/fixtures/release-transaction/
  profiles/
    valid-routine-v0.3.5.yaml
    invalid-missing-targets.yaml
    invalid-special-release-without-rationale.yaml
  generated-regions/
    valid/
    missing-end-marker/
    mismatched-surface/
    nested-region/
    unknown-surface/
  literal-audit/
    valid-baseline.yaml
    invalid-unknown-classification.yaml
    unauthorized-new-literal.yaml
    historical-fixture-without-rationale.yaml
  evidence/
    pending/
    published/
    invalid/
  timing/
    valid-timing.yaml
    missing-duration.yaml
    unknown-phase.yaml
  commands/
    release-verify-success/
    release-verify-failure/
    closeout-public-unavailable/
```

Fixture tests must not publish, create live GitHub releases, or run public npm/npx unless explicitly marked as release-owned smoke. Network-dependent behavior must be stubbed. Historical release fixtures must be clearly separated from current-release fixtures. Generated surfaces are compared against expected generated files, not hidden inside test logic.

Fixture-layout proof tests:

| Test ID | Scenario | Expected |
| --- | --- | --- |
| TRTA-FIX-001 | Fixture directory has required top-level groups | pass |
| TRTA-FIX-002 | Current and historical fixtures are mixed | fail |
| TRTA-FIX-003 | Fixture would publish or hit live npm/GitHub | fail |
| TRTA-FIX-004 | Generated expected output missing | fail |
| TRTA-FIX-005 | Invalid fixture lacks expected diagnostic | fail |

## Implementation-handoff command matrix

Every command or command family referenced by this test spec is classified as `existing/configured`, `planned-for-implementation`, `manual-only`, or `external/release-owned`. A planned command names its owning milestone and the milestone where it becomes required.

| Command / family | Status | Owner milestone | Becomes required | Missing-command behavior | Safe/dry-run expectation |
| --- | --- | --- | --- | --- | --- |
| `python scripts/test-adapter-distribution.py` | existing/configured | existing | M1 | Missing is blocker. | Local only; no publication. |
| `python scripts/validate-release.py --version <tag> ...` | existing/configured | existing | M1 | Missing is blocker. | Validates local/evidence surfaces. |
| `bash scripts/release-verify.sh <tag>` | existing/configured | existing | M6 | Missing is blocker. | Full local release gate. |
| `python scripts/prepare-release.py <tag>` | planned-for-implementation | M3 | M3 closeout | Not required before M3; missing after M3 is blocker. | Must not publish; idempotent. |
| `python scripts/release-preflight.py <tag>` | planned-for-implementation | M4 | M4 closeout | Not required before M4; missing after M4 is blocker. | Side-effect-light; no publication. |
| `python scripts/close-release-publication.py <tag>` | planned-for-implementation | M6 | M6 closeout | Not required before M6; missing after M6 is blocker. | Uses stubbed public data in tests; real public data only in release closeout. |
| `python scripts/test-release-transaction.py` | planned-for-implementation | M1 | M1 closeout | Replaces absent `python scripts/test-release-validation.py`; missing at M1 closeout is blocker. | Local fixture tests only. |
| `python scripts/select-validation.py --mode explicit ...` | existing/configured | existing | all milestones | Missing is blocker for selected validation. | Local only. |
| `python scripts/validate-change-metadata.py <change.yaml>` | existing/configured | existing | all milestones | Missing is blocker. | Local only. |
| `python scripts/validate-review-artifacts.py <change-root>` | existing/configured | existing | all milestones | Missing is blocker. | Local only. |
| `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` | existing/configured | existing | all milestones | Missing is blocker. | Local only. |
| `.github/workflows/release.yml` static command-set check | planned-for-implementation | M5 | M5 closeout | Missing check is blocker at M5 closeout. | Verifies CI invokes the same release command set. |
| public `npx @xiongxianfei/rigorloop@<version> init <target>` smoke | external/release-owned | release closeout | post-publication closeout | Not run in pre-publication unit tests. | Real public smoke only after publication; fixtures/stubs before closeout. |

`python scripts/test-release-validation.py` is not an existing command for this change. If that name is introduced later, the test spec must classify it as planned-for-implementation with an owning milestone before any milestone requires it.

Command ownership rules:

- Existing commands may be required immediately.
- Planned commands are not required before their owning milestone.
- A planned command becomes required at its owning milestone closeout.
- Missing required commands fail.
- Missing planned commands before their owning milestone are not failures.
- Commands that would publish, tag, or hit live external services must be stubbed in test fixtures unless the test is explicitly release-owned public smoke.
- Zero-test behavior must fail for test commands that are expected to execute selected tests.

Command-ownership proof tests:

| Test ID | Scenario | Expected |
| --- | --- | --- |
| TRTA-CMD-001 | Matrix contains all referenced commands | pass |
| TRTA-CMD-002 | Referenced command missing from matrix | fail |
| TRTA-CMD-003 | Existing command missing on disk | fail |
| TRTA-CMD-004 | Planned command missing before owner milestone | pass |
| TRTA-CMD-005 | Planned command missing at or after owner milestone | fail |
| TRTA-CMD-006 | Absent `python scripts/test-release-validation.py` listed as existing | fail |
| TRTA-CMD-007 | `python scripts/test-release-transaction.py` listed as planned M1 | pass |
| TRTA-CMD-008 | Public `npx` smoke attempted in pre-publication fixture test | fail |
| TRTA-CMD-009 | Test command exits 0 with zero tests when tests are expected | fail |
| TRTA-CMD-010 | Release workflow does not invoke the same `release-verify.sh <tag>` command set | fail |

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1-R4 | RTA-T001, RTA-T002, RTA-T003, TRTA-CMD-001 | unit, contract | Profile location, fields, source-of-truth ownership, and script non-ownership. |
| R5-R6 | RTA-T002, RTA-T019 | unit, contract | Routine/special classification and owner-decision boundary. |
| R7 | RTA-T004, TRTA-GEN-001 through TRTA-GEN-005 | unit, contract | Every routine release-prep surface is classified and generated surface IDs are closed. |
| R8-R10 | RTA-T005, RTA-T006, RTA-T007, TRTA-GEN-001 through TRTA-GEN-006 | integration, migration | Generated surfaces update from profile, human narrative is preserved, historical evidence is not rewritten. |
| R11 | RTA-T004, RTA-T014, TRTA-GEN-006 | unit, integration | Manual generated-surface overrides are explicit and preflight-checked. |
| R12-R13 | RTA-T005, RTA-T008, TRTA-CMD-004, TRTA-CMD-005 | integration, smoke | `prepare-release` idempotency and no publish/tag/push/publication-state effects. |
| R14-R15 | RTA-T005, RTA-T009 | unit, integration | Fixture values may be generated; test logic must not be generated or rewritten. |
| R16-R17 | RTA-T006, RTA-T010 | integration, contract | Pending evidence passes pre-publication validation and uses permitted placeholders only. |
| R18-R20 | RTA-T011, RTA-T013, TRTA-CMD-004, TRTA-CMD-005 | integration, contract | Python-owned preflight exists, is idempotent, side-effect-light, and milestone-owned. |
| R21 | RTA-T012, RTA-T014, RTA-T015, TRTA-LIT-001 through TRTA-LIT-007 | integration | Preflight covers profile, version, metadata pointer, literal, evidence shape, tags, output dir, and local inputs. |
| R22-R26 | RTA-T014, TRTA-LIT-001 through TRTA-LIT-007 | unit, integration | Literal audit enforcement, baseline report, historical/generated allowances, and diagnostics. |
| R27 | RTA-T015 | contract | Cheap deterministic release-verify failures add preflight regressions. |
| R28-R30 | RTA-T016, RTA-T017, RTA-T024, TRTA-CMD-010 | integration, smoke, manual | Full gate remains authoritative, CI parity, and safety checks remain present. |
| R31-R38 | RTA-T018, RTA-T020, RTA-T021, TRTA-CMD-008 | integration, e2e | Rerunnable closeout, public evidence inputs, public `npx` smoke, command/hash/file-count shapes, unavailable evidence behavior. |
| R39-R42 | RTA-T022, TRTA-TIME-001 through TRTA-TIME-006 | unit, integration | Timing evidence exists, required missing timing fails, durations are warning/observation first slice, and phases are separated. |
| R43-R44 | RTA-T007, RTA-T023, RTA-T024, TRTA-FIX-001 through TRTA-FIX-005 | migration, manual | Historical release evidence is not modified; generated diffs remain reviewable. |
| R45 | RTA-T025 | contract | Authoring profile stopped after plan-review and did not invoke downstream implementation/release stages. |
| AC1-AC7 | RTA-T001 through RTA-T014, TRTA-GEN-001 through TRTA-GEN-006, TRTA-LIT-001 through TRTA-LIT-007 | unit, integration, contract | Profile schema, generator idempotency, pending evidence, ownership classification, literal audit, historical literal handling. |
| AC8-AC11 | RTA-T011 through RTA-T017, TRTA-CMD-001 through TRTA-CMD-010 | integration, smoke | Preflight command, preflight fixtures, full gate required, command ownership, and CI parity. |
| AC12-AC17 | RTA-T018, RTA-T020, RTA-T021, RTA-T022, TRTA-TIME-001 through TRTA-TIME-006 | integration, e2e | Closeout rerun, unavailable public evidence, published evidence validation, public smoke, hash/command shape, timing. |
| AC18-AC20 | RTA-T007, RTA-T023, RTA-T024, TRTA-FIX-001 through TRTA-FIX-005 | migration, manual, integration | Historical immutability, fixture separation, and behavior-preservation proof. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 routine release profile drives pending evidence | RTA-T001, RTA-T005, RTA-T006 | Profile-backed generation, metadata agreement, pending evidence, and narrative preservation. |
| E2 cheap drift fails before full release verification | RTA-T012, RTA-T015 | Package/profile mismatch and cheap-drift regression path. |
| E3 published evidence uses validator-compatible shape | RTA-T020, RTA-T021 | Public closeout fixture asserts command strings, hashes, file counts, target rows, and closeout status. |
| E4 public evidence is not available yet | RTA-T018 | Closeout reports pending external evidence and avoids unrelated modifications. |
| E5 special release stays explicit | RTA-T002, RTA-T019 | New adapter target or other special boundary rejects routine automation without owner decision. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 wrong package version in profile | RTA-T012 | Preflight rejects package/profile mismatch before full gate. |
| EC2 changed unauthorized current literal | RTA-T014 | Newly changed unauthorized literal fails. |
| EC3 historical old release tag | RTA-T014, RTA-T023 | Historical fixture literals pass only when classified historical. |
| EC4 unreachable remote tag state | RTA-T015 | Diagnostic is explicit and not silently treated as pass. |
| EC5 GitHub assets visible but npm delayed | RTA-T018 | Closeout reports pending npm evidence and leaves evidence unpublished. |
| EC6 npm visible but target archive invalid | RTA-T020 | Published evidence validation fails on missing/wrong archive checksum. |
| EC7 opencode multi-root hashes/counts | RTA-T021 | Root-qualified `sha256:<hex>` and file counts are required. |
| EC8 release notes narrative plus generated regions | RTA-T006 | Human narrative outside generated regions is preserved. |
| EC9 new adapter target special release | RTA-T002, RTA-T019 | Routine schema/preflight rejects or pauses for owner decision. |
| EC10 manual override lacks rationale | RTA-T004, RTA-T014 | Override without review-visible rationale fails classification/preflight. |

## Test cases

### RTA-T001. Release profile schema validates source-of-truth fields

- Covers: R1-R4, AC1, E1
- Level: unit
- Fixture/setup: `docs/releases/profiles/v9.9.9-test.yaml` fixture and negative profile fixtures under the release validation fixture tree.
- Steps: Load the valid fixture with the shared release-profile parser; validate required fields; run negative fixtures missing release tag, package version, npm package, targets, adapter expectations, publication requirements, evidence requirements, and validation requirements.
- Expected result: Valid routine profile passes; missing fields fail with diagnostics naming the profile path and field; scripts read the profile rather than hardcoded routine state.
- Failure proves: Routine release state can remain duplicated or under-specified outside the profile.
- Automation location: `scripts/test-adapter-distribution.py` or a new focused release tooling test file selected during M1.

### RTA-T002. Routine and special release classification fails closed

- Covers: R5, R6, AC19, E5, EC9
- Level: unit, contract
- Fixture/setup: Routine profile fixture plus special fixtures for new adapter target, new publication channel, schema migration, emergency/security exception, and historical evidence rewrite.
- Steps: Validate each fixture through the profile validator and preflight classification layer.
- Expected result: Routine profile passes; special profiles reject routine automation or require an explicit owner decision fixture.
- Failure proves: Special releases can be forced through routine automation without owner review.
- Automation location: release profile validator tests and `scripts/validate-release.py` fixture tests.

### RTA-T003. Profile is not duplicated by script-owned current release constants

- Covers: R3, R4, AC2
- Level: contract
- Fixture/setup: Active profile fixture and scanner/audit fixture with stale version data in script constants.
- Steps: Run the derivation audit or literal audit against fixture files that intentionally duplicate profile-owned values outside approved generated surfaces.
- Expected result: Unauthorized current-version release state outside the profile/generated allowlist fails or reports baseline drift according to classification.
- Failure proves: The release profile became one more file rather than the source of truth.
- Automation location: release literal/derivation audit tests in M2.

### RTA-T004. Release-prep surfaces have explicit ownership classes

- Covers: R7, R11, AC5, EC10
- Level: unit, contract
- Fixture/setup: Surface inventory fixture covering package metadata pointers, adapter artifact expectations, pending npm-publication skeleton, target smoke rows, current-version fixture data, release notes narrative, migration/risk notes, prior release evidence, profile snapshots, and historical fixtures.
- Steps: Validate that each surface has exactly one classification: profile-owned generated, human-authored profile-checked, or historical immutable; run negative fixtures for unknown class and manual generated-surface override without rationale.
- Expected result: Complete classification passes; unclassified surfaces and unreviewed generated-surface overrides fail with owner diagnostics.
- Failure proves: Generators can become too weak or too broad because ownership is implicit.
- Automation location: release surface classification tests in M2.

### RTA-T005. `prepare-release` is idempotent and updates only profile-owned outputs

- Covers: R8, R12-R15, AC2, AC3, E1
- Level: integration
- Fixture/setup: Temporary repository fixture with complete routine profile, package metadata, fixture data, pending evidence templates, generated-region markers, and sentinel files outside generated ownership.
- Steps: Run `python scripts/prepare-release.py v9.9.9-test` or fixture-safe equivalent twice; compare the second run diff; inspect touched paths; verify generated fixture data and expected values come from the profile.
- Expected result: First run updates only approved profile-owned surfaces or generated regions; second run is byte-identical; test logic files are not generated or rewritten.
- Failure proves: Release prep remains hand-synchronized, non-idempotent, or too broad.
- Automation location: `scripts/test-adapter-distribution.py` or new `scripts/test-release-transaction.py`.

### RTA-T006. Pending evidence validates and preserves release-note narrative

- Covers: R9, R16, R17, AC3, AC4, E1, EC8
- Level: integration
- Fixture/setup: Release notes fixture with human narrative before/after generated regions plus pending `release.yaml` and `npm-publication.md` templates.
- Steps: Run `prepare-release`; validate pending release evidence with pre-publication validation; compare human narrative outside generated markers before and after generation; run negative fixture with an unpermitted placeholder.
- Expected result: Pending evidence passes pre-publication validation; only permitted placeholders remain; human narrative outside generated regions is unchanged.
- Failure proves: Evidence generation can still produce validator-shape loops or overwrite release-note narrative.
- Automation location: `scripts/validate-release.py` tests and generator integration tests.

### RTA-T007. Historical release evidence remains immutable

- Covers: R10, R43, AC18, EC3
- Level: migration, integration
- Fixture/setup: Temporary repository with historical `docs/releases/v0.3.4/`, prior profile snapshots, historical fixtures, and an active `v9.9.9-test` profile.
- Steps: Run `prepare-release` and preflight on the active profile; compare historical release files before/after; validate historical literal classifications.
- Expected result: Historical release evidence and historical fixtures are unchanged; old release tags are allowed only on classified historical surfaces.
- Failure proves: Routine release prep rewrites historical evidence or treats history as current state.
- Automation location: generator integration tests and literal-audit tests.

### RTA-T008. `prepare-release` has no publication, tag, push, or registry side effects

- Covers: R13, AC2
- Level: integration, smoke
- Fixture/setup: Temporary Git repository fixture with command stubs for `git tag`, `git push`, GitHub release creation, npm registry state reads, and npm publish.
- Steps: Run `prepare-release`; inspect executed command log and network/publication stubs.
- Expected result: No publish, tag, push, GitHub release creation, or npm publication-state read occurs.
- Failure proves: Release preparation crosses the publication boundary.
- Automation location: generator integration tests with local command stubs.

### RTA-T009. Fixture data may be generated but test logic is stable

- Covers: R14, R15, AC3
- Level: contract
- Fixture/setup: Test fixture data files classified as profile-owned generated and test logic files marked non-generated.
- Steps: Run `prepare-release`; inspect changed paths and generated-region markers.
- Expected result: Expected values and fixture data may change when profile-derived; test logic files are not generated or rewritten.
- Failure proves: Release automation hides behavior changes inside generated test code.
- Automation location: generator path-ownership tests.

### RTA-T010. Pending evidence shape rejects invalid placeholders

- Covers: R16, R17, AC4
- Level: unit, contract
- Fixture/setup: Pending `release.yaml`, `npm-publication.md`, and release notes fixtures with valid placeholders plus invalid placeholder vocabulary.
- Steps: Run pre-publication release validation.
- Expected result: Valid pending placeholders pass only where explicitly permitted; invalid or missing pending evidence fails before publication.
- Failure proves: Manual evidence-shape mistakes can survive until post-publication validation.
- Automation location: `scripts/validate-release.py` fixture tests.

### RTA-T011. Python-owned release preflight command exists and is idempotent

- Covers: R18-R20, AC8
- Level: integration
- Fixture/setup: Complete prepared routine release fixture and optional timing/log output path.
- Steps: Run `python scripts/release-preflight.py v9.9.9-test` twice; inspect output and changed files; run with optional explicit log/timing artifact if implemented.
- Expected result: Command exists, exits successfully on clean fixture, repeats with same result, and modifies no release artifacts except explicitly requested log/timing output.
- Failure proves: Preflight is not a stable cheap gate or has hidden generation side effects.
- Automation location: `scripts/test-release-transaction.py` or release validator test suite.

### RTA-T012. Preflight catches local profile and package drift

- Covers: R21, AC9, E2, EC1
- Level: integration
- Fixture/setup: Prepared routine release fixtures for missing profile, malformed profile, incomplete profile, package/profile version mismatch, stale metadata pointer, missing local input, and dirty release-output state.
- Steps: Run `python scripts/release-preflight.py <tag>` against each fixture.
- Expected result: Each cheap deterministic local/profile/schema defect fails with a diagnostic naming the profile path, release tag, mismatched value, expected owner, or dirty output path.
- Failure proves: Maintainers still discover cheap release-state drift through full verification.
- Automation location: preflight fixture tests.

### RTA-T013. Preflight avoids broad full-gate work

- Covers: R19, R20, performance expectations, AC8
- Level: contract
- Fixture/setup: Command-call fixture or monkeypatch that records attempted subprocesses from preflight.
- Steps: Run preflight on a clean fixture; assert it does not invoke broad adapter distribution tests, archive generation, package pack smoke, public `npx`, or full `release-verify.sh`.
- Expected result: Preflight performs cheap local/profile/schema checks only and remains suitable for an under-30-second target.
- Failure proves: Preflight duplicates full release verification and does not reduce fix-and-rerun loops.
- Automation location: preflight command tests.

### RTA-T014. Current-version literal audit enforces ownership

- Covers: R22-R26, R11, AC6, AC7, EC2, EC3, EC10
- Level: unit, integration
- Fixture/setup: Changed-file fixture with unauthorized current literal, baseline unauthorized literal, historical literal, generated current literal, and manual generated-surface override without rationale.
- Steps: Run literal audit through preflight or direct helper; inspect diagnostics.
- Expected result: Newly changed unauthorized literal fails; existing baseline drift reports without blocking initial adoption; historical literal passes only with historical classification; generated current literal passes only when profile-derived; diagnostics name literal, file, classification, and expected owner.
- Failure proves: Version literals continue drifting across hand-edited release surfaces.
- Automation location: literal audit tests and preflight fixtures.

### RTA-T015. Preflight/full-gate boundary has regression feedback

- Covers: R21, R27, AC9, EC4
- Level: contract, integration
- Fixture/setup: Fixtures for reachable remote tag conflict, unreachable remote tag state, and simulated full-gate cheap deterministic drift caught under same inputs.
- Steps: Run preflight; run fixture-safe full-gate validation where needed; inspect regression fixture inventory.
- Expected result: Reachable remote tag conflict fails; unreachable remote state produces explicit diagnostic and is not silently pass; any cheap deterministic full-gate drift case has a corresponding preflight regression.
- Failure proves: Preflight guarantees are vague or full verification keeps rediscovering cheap drift.
- Automation location: preflight tests plus release-gate boundary tests.

### RTA-T016. `release-verify.sh <tag>` remains the full gate

- Covers: R28, R30, AC10, AC20
- Level: smoke, manual
- Fixture/setup: Existing release-gate dry-run support and script text.
- Steps: Run fixture-safe `bash scripts/release-verify.sh <fixture-tag>` or existing dry-run tests; inspect script categories before and after implementation.
- Expected result: Full gate still invokes repository-owned release validation and safety checks for generated outputs, archive integrity, package contents, adapter metadata, npm/publication evidence where applicable, and smoke evidence.
- Failure proves: Automation improved speed by removing release safety checks.
- Automation location: `scripts/test-adapter-distribution.py` release-verify tests; manual behavior-preservation review.

### RTA-T017. CI release workflow delegates to the same release command set

- Covers: R29, AC11
- Level: integration, contract
- Fixture/setup: `.github/workflows/release.yml` and local `scripts/release-verify.sh`.
- Steps: Parse workflow; assert release jobs invoke the same repository-owned release verification command set for the tag/profile; run negative fixture or static check for parallel workflow-owned checks not present locally.
- Expected result: CI is a thin wrapper around repository-owned release verification and does not maintain a divergent release gate.
- Failure proves: Local release readiness and hosted release readiness can diverge.
- Automation location: `scripts/test-adapter-distribution.py` workflow static tests or new workflow release parity tests.

### RTA-T018. Published closeout is rerunnable and waits for public evidence

- Covers: R31, R37, R38, AC12, E4, EC5
- Level: integration
- Fixture/setup: Closeout fixture with GitHub release metadata available but npm registry metadata unavailable; command stubs for public metadata reads.
- Steps: Run `python scripts/close-release-publication.py v9.9.9-test`; rerun with the same unavailable public evidence; compare files outside explicitly allowed logs.
- Expected result: Command fails clearly with pending external evidence diagnostic, is safe to rerun, does not mark evidence published, and modifies no unrelated files.
- Failure proves: Closeout can prematurely publish evidence or require manual cleanup during registry delays.
- Automation location: closeout integration tests with public metadata stubs.

### RTA-T019. Special release owner decision is required

- Covers: R5, R6, AC19, E5, EC9
- Level: contract
- Fixture/setup: Profile fixture introducing a new adapter target, a new publication channel, or release schema migration with and without owner decision record.
- Steps: Run profile validation and preflight.
- Expected result: Special release without owner decision pauses/rejects; explicit owner decision routes to special handling without pretending it is routine.
- Failure proves: Routine automation expands into one-off release behavior silently.
- Automation location: profile/preflight classification tests.

### RTA-T020. Published evidence validates GitHub, npm, archive, and closeout fields

- Covers: R32, R36, R37, AC13, EC6
- Level: integration
- Fixture/setup: Public evidence fixtures for GitHub release assets, npm registry metadata, npm tarball identity, adapter archive metadata, missing target archive URL, and wrong checksum.
- Steps: Run `close-release-publication` against valid stubs and negative stubs; validate generated published evidence.
- Expected result: Valid public evidence writes published closeout fields accepted by `validate-release.py`; missing/wrong archive evidence fails and records blockers instead of pass.
- Failure proves: Published evidence can be accepted without real public GitHub/npm/archive proof.
- Automation location: closeout fixture tests and `scripts/validate-release.py` published-phase tests.

### RTA-T021. Public smoke rows and hashes use validator-compatible shapes

- Covers: R33-R35, AC14, AC15, E3, EC7
- Level: integration, e2e
- Fixture/setup: Public `npx` smoke command stubs for `version`, `init codex`, `init claude`, `init opencode`, including opencode multi-root output.
- Steps: Generate published evidence; inspect target smoke rows, command strings, tree hashes, root-qualified multi-root entries, and file counts; run negative fixtures with `npx -y` and raw hashes.
- Expected result: Evidence records validator-expected command strings, public smoke for all targets, `sha256:<hex>` tree hashes, root-qualified multi-root entries, file counts, and closeout blockers/status.
- Failure proves: The `npx -y` and raw-hash evidence-shape loops can recur.
- Automation location: closeout fixture tests and published evidence validator tests.

### RTA-T022. Timing evidence records required phases without hard duration failure

- Covers: R39-R42, AC16, AC17
- Level: unit, integration
- Fixture/setup: Timing evidence fixtures with complete phases, missing timing, missing phase, over-target duration, pending external job durations, and malformed duration values.
- Steps: Validate timing evidence through profile-required release validation; run generator/closeout timing output where implemented.
- Expected result: Required missing timing fails; complete timing passes; over-target duration records warning/observation in first slice; phases are separated for preflight, local release verification, GitHub release job, npm publish job, public smoke, and closeout when available.
- Failure proves: Timing is either absent or incorrectly used as an early hard budget.
- Automation location: `scripts/validate-release.py` timing tests and timing helper tests.

### RTA-T023. Historical releases and prior fixtures are compatibility inputs only

- Covers: R43, AC18, EC3
- Level: migration
- Fixture/setup: Existing historical release files under `docs/releases/`, historical test fixtures, and release reports.
- Steps: Run selected generator/preflight/validation commands for the active fixture; compare historical paths and route existing release paths through selector/release validation.
- Expected result: Historical files are not rewritten; historical release validation remains compatible; historical current-version literals are not treated as active generated state.
- Failure proves: Routine release automation breaks historical evidence compatibility.
- Automation location: migration tests in release tooling and selector tests.

### RTA-T024. Behavior-preservation proof covers release safety gates

- Covers: R28-R30, R44, AC10, AC20
- Level: manual, integration
- Fixture/setup: `docs/changes/2026-06-29-release-transaction-automation/behavior-preservation.md`, release gate scripts, CI workflow, and generated diff.
- Steps: Confirm behavior-preservation matrix records baseline and new proof for full release verification, GitHub release evidence, npm publication evidence, public `npx` smoke, adapter metadata, package metadata, historical immutability, timing evidence, and external wait handling; run lifecycle validation over the evidence.
- Expected result: Generated diffs remain reviewable and no release safety check is removed to improve speed.
- Failure proves: Automation weakened the supply-chain release boundary while claiming speed improvement.
- Automation location: manual code-review checklist plus lifecycle explicit-path validation.

### RTA-T025. Authoring profile stopped before test-spec and implementation

- Covers: R45
- Level: contract
- Fixture/setup: Change metadata, plan-review record, plan body, and plan index after `authoring-through-plan-review`.
- Steps: Validate change metadata and lifecycle state; inspect plan-review record and plan current handoff.
- Expected result: Profile records completion at plan-review, next stage is `test-spec`, and no test-spec, implementation, verification, PR, release, or publication stage is claimed by the authoring profile.
- Failure proves: The authorized profile crossed its stop boundary.
- Automation location: `python scripts/validate-change-metadata.py`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`.

## Fixtures and data

- `tests/fixtures/release-transaction/profiles/valid-routine-v0.3.5.yaml`: valid routine release profile fixture for `@xiongxianfei/rigorloop@0.3.5` and targets `codex`, `claude`, `opencode`.
- `tests/fixtures/release-transaction/profiles/`: negative release profile fixtures for missing fields, malformed YAML, unknown closed vocabulary, wrong package version, unknown target, and special release classification.
- `tests/fixtures/release-transaction/generated-regions/`: valid, missing end marker, mismatched surface, nested region, and unknown surface fixtures.
- `tests/fixtures/release-transaction/literal-audit/`: valid baseline, unknown classification, newly changed unauthorized current literal, historical fixture without rationale, generated current literal, and unreviewed manual override fixtures.
- `tests/fixtures/release-transaction/evidence/`: pending and published evidence fixtures, plus invalid `npx -y` command and raw tree hash fixtures.
- `tests/fixtures/release-transaction/timing/`: complete, missing-duration, unknown-phase, unknown-result, over-target, pending external, and malformed timing fixtures.
- `tests/fixtures/release-transaction/commands/`: command-behavior fixtures for release-verify success/failure and closeout public-unavailable states.
- Temporary repository fixtures for `prepare-release` idempotency and changed-path inspection must compose the fixture groups above rather than hiding generated expected output inside test logic.
- Existing historical release files under `docs/releases/` and existing release validation tests as compatibility inputs.

## Mocking/stubbing policy

- Do not contact npm, create GitHub releases, publish packages, push tags, or run public `npx` in automated tests.
- Stub public GitHub, npm, and `npx` data as fixture inputs for closeout tests.
- Use command stubs for side-effect boundary tests around `prepare-release`.
- Use fixture-safe or dry-run release gate checks for smoke tests.
- Do not mock `validate-release.py`, `release-verify.sh`, `validate-adapters.py`, or package-content validation in final behavior-preservation proof; final proof should inspect or run the real repository-owned commands in safe modes.

## Migration or compatibility tests

- Historical release evidence and historical fixtures are not rewritten.
- Existing `docs/releases/<version>/release.yaml`, `release-notes.md`, `npm-publication.md`, and `docs/releases/v<version>.md` routing remains compatible.
- Existing release-specific specs and release evidence may remain stricter than the routine release automation contract.
- The first literal-audit slice may report existing baseline drift without blocking adoption, but changed unauthorized literals fail immediately.

## Observability verification

- Preflight diagnostics name release tag, profile path, literal, file, classification, expected owner, mismatched values, tag conflict, unreachable remote state, and corrective action when applicable.
- `prepare-release`, `release-preflight`, `release-verify`, and `close-release-publication` produce concise success summaries and actionable failure diagnostics.
- Public closeout evidence records package version, dist-tag, integrity, tarball URL, archive URLs, target smoke summaries, tree hashes, file counts, closeout blockers, and closeout state.
- Timing evidence records phase names, durations, result, and limitations.

## Security/privacy verification

- Release tooling and generated evidence must reject or avoid committing npm tokens, credentials, private keys, private environment dumps, private hostnames, usernames, raw proxy values, machine-local temp paths, and private absolute paths.
- Local preflight tests verify no secrets are required for local checks.
- Published closeout fixture evidence summarizes public outputs without storing unnecessary machine-local command output.
- Manual override records must be review-visible and must not include sensitive values.

## Performance checks

- Preflight tests assert that broad adapter distribution tests, full archive validation, public `npx`, and `release-verify.sh` are not invoked by preflight.
- No hard wall-clock budget is enforced in automated tests because maintainer machines vary; the under-30-second preflight target is verified indirectly by command-scope tests and may be timed manually during implementation.
- Timing duration above target is warning/observation evidence in first slice tests, not a release failure.

## Manual QA checklist

- Review generated diffs from `prepare-release` for clear generated regions and bounded path ownership.
- Confirm release notes narrative remains human-authored outside generated regions.
- Confirm `release-verify.sh` safety-check list is not shortened when adding preflight.
- Confirm `.github/workflows/release.yml` stays a thin wrapper around repository-owned release commands.
- Confirm behavior-preservation evidence is complete before final verify.

## What not to test and why

- Do not perform real npm publication or GitHub release creation; this change prepares release automation and uses fixture-backed public evidence proof.
- Do not run live public `npx` in unit or integration tests; public smoke remains real release-operation evidence and is represented by closeout fixtures here.
- Do not migrate or rewrite historical releases.
- Do not test release-gate parallelism, background publication monitoring, remote/shared caching, or hard duration budgets; those are explicit follow-ons.
- Do not generate test logic; tests should remain hand-authored and may consume generated fixture data.

## Uncovered gaps

None. Generated-region markers, literal-audit baseline shape, timing evidence fields, fixture layout, and command ownership are defined above. Any implementation-selected detail must satisfy those closed compatibility contracts and proof tests. If implementation requires behavior outside those boundaries, return to spec, architecture, plan, or test-spec review before coding it.

## Next artifacts

- `implement M1`
- `code-review M1`
- repeat implementation/code-review for M2 through M6
- `explain-change`
- `verify`
- `pr`

## Follow-on artifacts

None yet

## Readiness

Active proof surface for implementation. The active plan `Current Handoff Summary` owns the next workflow action. This test spec does not authorize verification, PR readiness, release, or publication.
