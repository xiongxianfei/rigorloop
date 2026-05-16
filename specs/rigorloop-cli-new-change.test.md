# RigorLoop CLI New Change Test Spec

## Status

active

## Related spec and plan

- Spec: [RigorLoop CLI New Change](rigorloop-cli-new-change.md), approved.
- Plan: [RigorLoop CLI New Change](../docs/plans/2026-05-16-rigorloop-cli-new-change.md), active and approved by `plan-review-r1`.
- Proposal: [RigorLoop Scaffolding CLI and Machine-Readable Workflow](../docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md), accepted.
- Architecture: [RigorLoop Canonical System Architecture](../docs/architecture/system/architecture.md), approved.
- Change metadata: [change.yaml](../docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml).
- Review records:
  - `docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r2.md`
  - `docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/architecture-review-r1.md`
  - `docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/plan-review-r1.md`

## Testing strategy

This slice adds a local filesystem scaffolding command to the existing CLI package. Proof must cover public command behavior, stable JSON/human output, safe path planning, generated `change.yaml` shape, no lifecycle claim leakage, no forbidden file writes, and observable partial failures.

- Unit or helper-level tests prove value-domain validators, deterministic metadata rendering, YAML scalar escaping, write-plan construction, and deterministic partial-failure result shaping.
- Integration tests execute the local CLI in temporary project directories and assert stdout, stderr, exit codes, filesystem effects, JSON actions, blockers, warnings, and generated file content.
- Regression tests keep existing `init`, lockfile, and archive behavior green after shared parser or output helper changes.
- No tests should depend on network access, Git repository state, hosted CI, global npm state, or machine-local paths.
- Partial write failure should use a deterministic helper seam when available. Do not rely only on platform-sensitive permission behavior.

## Requirement coverage map

| Requirement | Coverage |
|---|---|
| R1-R2 | TNC-001, TNC-019 |
| R3-R4 | TNC-002 |
| R5-R5c | TNC-004, TNC-006 |
| R6 | TNC-006, TNC-009 |
| R7-R7b | TNC-005, TNC-006 |
| R8 | TNC-006, TNC-009 |
| R9-R10 | TNC-005, TNC-009, TNC-010 |
| R11 | TNC-002, TNC-004, TNC-005, TNC-018 |
| R12 | TNC-001 |
| R13-R19 | TNC-003, TNC-011, TNC-013, TNC-014 |
| R20-R26 | TNC-009, TNC-010, TNC-015, TNC-019 |
| R27-R30 | TNC-006, TNC-007, TNC-009, TNC-020 |
| R31-R37 | TNC-006, TNC-007, TNC-009, TNC-010, TNC-015, TNC-020 |
| R38-R43 | TNC-009, TNC-010, TNC-011, TNC-015 |
| R44-R50 | TNC-011, TNC-012 |
| R51-R51b | TNC-013, TNC-014 |
| R52-R56 | TNC-013, TNC-016 |
| R56a-R56k | TNC-012, TNC-013, TNC-017 |
| R57-R60 | TNC-008, TNC-011, TNC-018 |
| R61-R62 | TNC-002, TNC-003, TNC-004, TNC-005, TNC-013, TNC-014, TNC-016 |
| R63-R64 | TNC-009, TNC-010 |
| R65-R68 | TNC-008, TNC-011, TNC-012, TNC-013, TNC-017 |
| R69-R70 | TNC-018 |
| R71-R76 | TNC-009, TNC-010, TNC-015, TNC-019 |
| Compatibility and migration | TNC-009, TNC-012, TNC-016, TNC-019 |
| Observability | TNC-008, TNC-011, TNC-017, TNC-018 |
| Security/privacy | TNC-003, TNC-007, TNC-014, TNC-015, TNC-019 |
| Performance expectations | TNC-019, TNC-021 |
| Acceptance criteria AC1-AC13 | TNC-001-TNC-021 |

## Example coverage map

| Example | Coverage |
|---|---|
| E1 standard scaffold creates change metadata | TNC-009, TNC-020 |
| E2 minimal scaffold creates only change metadata | TNC-010 |
| E3 dry-run JSON reports every planned mutation | TNC-011 |
| E4 existing change metadata is not overwritten | TNC-016 |
| E5 invalid change id is rejected before path planning | TNC-003 |

## Edge case coverage

| Edge case | Coverage |
|---|---|
| `docs/` absent | TNC-011, TNC-009 |
| `docs/` exists as a file | TNC-013 |
| `docs/changes/` absent | TNC-011, TNC-009 |
| `docs/changes/` exists as a file | TNC-013 |
| Change root exists but is empty | TNC-012 |
| Change root exists with unrelated files | TNC-012 |
| `change.yaml` exists | TNC-016 |
| Existing `explain-change.md` | TNC-015, TNC-016 |
| Symlink at `docs`, `docs/changes`, or change root | TNC-014 |
| Title contains quotes or colon characters | TNC-007 |
| `--json --quiet` | TNC-018 |
| `--dry-run` with conflicts | TNC-013, TNC-016 |
| Directory creation succeeds but file write fails | TNC-017 |

## Milestone coverage map

| Milestone | Coverage |
|---|---|
| M1. Command contract helpers and metadata generation | TNC-001-TNC-008 |
| M2. Write plan, dry-run, and safe metadata scaffolding | TNC-009-TNC-016, TNC-020-TNC-021 |
| M3. Partial failure behavior, output polish, and final integration | TNC-017-TNC-019 |
| Lifecycle closeout | TNC-022 and final selected CI/verify commands |

## Test cases

### TNC-001. Help and package command surface includes `new-change`

- Covers: R1, R2, R12, AC1
- Level: integration
- Fixture/setup: existing local `packages/rigorloop` package.
- Steps:
  - Run `rigorloop --help`.
  - Assert exit code `0`.
  - Assert help mentions `rigorloop new-change <change-id>` or equivalent command description.
  - Assert help still mentions existing `version` and `init --adapter codex`.
- Expected result: implemented command surface is discoverable without hiding existing commands.
- Failure proves: the public CLI surface does not expose the new command, or the existing command surface regressed.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TNC-002. Required positional change ID and title are enforced

- Covers: R3, R4, R11, R57-R61
- Level: integration
- Fixture/setup: empty temporary project directory.
- Steps:
  - Run `rigorloop new-change --title "Missing id" --json`.
  - Run `rigorloop new-change docs-only --json`.
  - Run cases with missing option values such as `--title`, `--type`, `--risk`, and `--profile`.
  - Assert exit code `4`, status `error`, and field-specific error codes such as `missing-change-id` or `missing-title`.
  - Assert no files or directories are created.
- Expected result: invalid usage fails before path planning or mutation.
- Failure proves: public command preconditions are not stable.
- Automation location: package CLI tests.

### TNC-003. Change ID validation rejects unsafe path segments

- Covers: R13-R19, R61, AC5, E5
- Level: integration
- Fixture/setup: empty temporary project directory.
- Steps:
  - Run valid IDs including `a`, `docs-typo`, and `feature123`.
  - Run invalid IDs including `../outside`, `a/b`, `a\\b`, `.hidden`, `-bad`, `bad-`, `bad id`, `bad%2Fid`, `bad%5Cid`, `a:b`, and a control-character case.
  - Assert invalid cases return status `error`, exit code `4`, code `invalid-change-id`.
  - Assert invalid cases do not create `docs/`.
- Expected result: only one safe repository-relative path segment is accepted.
- Failure proves: path traversal or multi-segment writes could reach outside the approved root.
- Automation location: package CLI tests.

### TNC-004. Classification token validation is exact

- Covers: R5-R5c, R11, R61, AC11
- Level: integration
- Fixture/setup: temporary project directories.
- Steps:
  - Run valid `--type` values such as `docs`, `workflow`, `cli-123`, and a 64-character lowercase token.
  - Run invalid values including empty, `High`, `security review`, `../x`, `medium/high`, `bad%2Fx`, `bad\\x`, control characters, leading digit, and 65 characters.
  - Assert invalid values return status `error`, exit code `4`, code `invalid-classification`.
  - Assert valid values appear in generated or planned `change.yaml` as `classification`.
- Expected result: classification accepts only the approved lowercase token domain.
- Failure proves: persisted metadata values are ambiguous or unsafe.
- Automation location: package CLI tests.

### TNC-005. Risk and profile validation are exact

- Covers: R7-R11, R61, AC11
- Level: integration
- Fixture/setup: temporary project directories.
- Steps:
  - Run `--risk low`, `--risk medium`, and `--risk high`.
  - Run invalid risks such as `High`, `critical`, `medium/high`, and empty value.
  - Run `--profile standard`, `--profile minimal`, and invalid profile values.
  - Assert invalid risks return code `invalid-risk`.
  - Assert invalid profiles return code `unsupported-profile`.
- Expected result: only the approved risk and profile domains are accepted.
- Failure proves: generated metadata can contain unreviewed public values.
- Automation location: package CLI tests.

### TNC-006. Generated metadata defaults and field order are deterministic

- Covers: R5-R8, R27-R35, R57-R68, AC6, AC7
- Level: unit, integration
- Fixture/setup: temporary project; optional helper-level metadata renderer.
- Steps:
  - Generate metadata with only required `--title`.
  - Assert deterministic top-level field order: `change_id`, `title`, `classification`, `risk`, `artifacts`, `requirements`, `tests`, `validation`, `changed_files`, `review`.
  - Assert default `classification: default` and `risk: medium`.
  - Assert `artifacts: {}`, empty arrays for requirements/tests/validation/changed_files, and `review.status: pending`.
  - Generate the same metadata twice and assert byte-identical output.
- Expected result: scaffolded metadata is stable and schema-compatible.
- Failure proves: downstream tools cannot rely on reproducible first-release metadata.
- Automation location: package helper tests and CLI integration tests.

### TNC-007. YAML scalar escaping and privacy are enforced

- Covers: R27-R37, security/privacy, edge case 10
- Level: integration
- Fixture/setup: temporary project.
- Steps:
  - Run with titles containing quotes, colon characters, brackets, hashes, leading/trailing spaces, and newline-like text if the parser permits it.
  - Parse the generated `change.yaml` with repository validation.
  - Assert title value is preserved without corrupting YAML shape.
  - Assert generated content does not contain temp directory path, username, hostname, environment variables, stderr text, tokens, or absolute paths.
- Expected result: user text cannot break YAML or leak local machine details.
- Failure proves: generated metadata is unsafe or invalid.
- Automation location: package CLI tests plus `scripts/validate-change-metadata.py` fixture check.

### TNC-008. JSON envelope and command-specific `change` object are stable

- Covers: R57-R68, observability
- Level: integration
- Fixture/setup: temporary project.
- Steps:
  - Run `rigorloop new-change json-case --title "JSON Case" --dry-run --json`.
  - Assert stdout is JSON only and stderr is empty.
  - Assert stable top-level fields match the existing CLI envelope.
  - Assert `command: "new-change"`.
  - Assert `change.change_id`, `change.root`, `change.metadata_path`, and `change.profile` are present.
  - Assert actions use `type`, `path`, `status`, and `reason`.
- Expected result: agents and CI can consume a stable command result.
- Failure proves: public JSON output is not contract-compatible.
- Automation location: package CLI tests.

### TNC-009. Standard profile creates only `change.yaml`

- Covers: R6, R8-R10, R20-R26, R27-R36, R38-R43, R63, R71-R76, AC1, AC6, AC8, AC9, E1
- Level: integration
- Fixture/setup: empty temporary project.
- Steps:
  - Run `rigorloop new-change adapter-install-cli --title "Adapter install CLI" --type workflow`.
  - Assert exit code `0` and human output names the change root.
  - Assert only `docs/changes/adapter-install-cli/change.yaml` is created under the change root.
  - Assert no `explain-change.md`, review files, plan/spec/proposal/architecture/ADR files, `rigorloop.yaml`, or `rigorloop.lock` are created.
  - Assert generated metadata does not claim lifecycle readiness.
- Expected result: standard profile scaffolds only draft change metadata.
- Failure proves: the command creates durable-looking lifecycle artifacts or readiness claims.
- Automation location: package CLI tests.

### TNC-010. Minimal profile creates only metadata and warns

- Covers: R9-R10, R22-R26, R31-R36, R38-R43, R64, R71-R76, AC2, E2
- Level: integration
- Fixture/setup: empty temporary project.
- Steps:
  - Run `rigorloop new-change docs-typo --title "Fix docs typo" --type docs --profile minimal --json`.
  - Assert exit code `0`, status `warning`, and warning code `durable-reasoning-not-scaffolded`.
  - Assert only `change.yaml` is created.
  - Assert `artifacts` is empty and no `artifacts.explain_change` exists.
- Expected result: minimal profile is explicit about durable-reasoning omission without weakening later workflow requirements.
- Failure proves: minimal profile can be mistaken for complete workflow evidence.
- Automation location: package CLI tests.

### TNC-011. Dry-run JSON reports every planned mutation and writes nothing

- Covers: R17-R18, R44-R50, R57-R68, AC3, E3
- Level: integration
- Fixture/setup: empty temporary project.
- Steps:
  - Record project file listing.
  - Run `rigorloop new-change new-feature --title "New feature" --dry-run --json`.
  - Assert actions appear in deterministic order: `docs`, `docs/changes`, `docs/changes/new-feature`, `docs/changes/new-feature/change.yaml`.
  - Assert directory actions are planned or skipped as appropriate and file action is planned.
  - Assert project file listing is unchanged.
- Expected result: dry-run is a complete no-write plan.
- Failure proves: dry-run omits hidden mutations or writes files.
- Automation location: package CLI tests.

### TNC-012. Existing safe directories and unrelated files are handled correctly

- Covers: R44-R50, R56a-R56c, compatibility
- Level: integration
- Fixture/setup: temporary project with existing `docs/`, `docs/changes/`, and either an empty change root or unrelated file under the change root.
- Steps:
  - Run dry-run and actual `new-change`.
  - Assert existing directories are reported as existing/skipped.
  - Assert unrelated files are preserved.
  - Assert only `change.yaml` is added.
- Expected result: compatible existing project structure is not rewritten or hidden.
- Failure proves: non-destructive behavior is too strict, too loose, or inaccurate in the write plan.
- Automation location: package CLI tests.

### TNC-013. Directory path conflicts block before mutation

- Covers: R17-R19, R46-R48, R51, R56, R62, edge cases 2, 4, 12
- Level: integration
- Fixture/setup: temporary projects where `docs`, `docs/changes`, or `docs/changes/<change-id>` exists as a file.
- Steps:
  - Run `new-change` with `--json`, both dry-run and actual where useful.
  - Assert status `blocked`, exit code `5`, blocker code `path-not-directory`.
  - Assert blockers name the conflicting path.
  - Assert no new directories or files are created.
- Expected result: path-type conflicts block before mutation.
- Failure proves: the command can partially mutate after a known conflict.
- Automation location: package CLI tests.

### TNC-014. Symlink path conflicts block before mutation

- Covers: R51a-R51b, R56, R62, AC13, edge case 9
- Level: integration
- Fixture/setup: temporary projects with symlink at `docs`, `docs/changes`, or `docs/changes/<change-id>` where supported by the platform.
- Steps:
  - Run `new-change --json`.
  - Assert status `blocked`, exit code `5`, blocker code `path-not-directory`.
  - Assert command does not follow the symlink and creates nothing through the symlink target.
- Expected result: planned directory symlinks are rejected.
- Failure proves: the command can write outside the intended root.
- Automation location: package CLI tests; skip with explicit platform reason only if symlink creation is unavailable.

### TNC-015. Forbidden artifacts, network access, and project files are not touched

- Covers: R21, R23-R26, R38-R43, R71-R76, AC8, AC9, edge case 8
- Level: integration
- Fixture/setup: temporary project, optional existing `explain-change.md`, existing `rigorloop.yaml`, and existing `rigorloop.lock`.
- Steps:
  - Run successful standard and minimal profile commands.
  - Assert no forbidden lifecycle artifacts are created.
  - Assert existing `rigorloop.yaml` and `rigorloop.lock` are byte-identical after the command.
  - Install a test fetch seam that throws if called, or otherwise assert no network path is reachable.
  - Assert command succeeds even when `rigorloop.yaml` is absent.
- Expected result: `new-change` remains local change metadata scaffolding only.
- Failure proves: scope leaked into project init, adapter install, network, or workflow evidence.
- Automation location: package CLI tests.

### TNC-016. Existing `change.yaml` is not overwritten

- Covers: R52-R56, R62, R73, AC4, E4, edge case 7
- Level: integration
- Fixture/setup: temporary project with existing `docs/changes/new-feature/change.yaml` and optional existing `explain-change.md`.
- Steps:
  - Record original file bytes.
  - Run `rigorloop new-change new-feature --title "New feature" --json`.
  - Assert status `blocked`, exit code `5`, blocker code `path-exists`.
  - Assert original `change.yaml` bytes are unchanged.
  - Assert rerun is not treated as success.
- Expected result: planned files are never overwritten.
- Failure proves: non-destructive behavior is broken.
- Automation location: package CLI tests.

### TNC-017. Partial write failure reports done and failed actions

- Covers: R56a-R56k, R57-R68, AC12, edge case 13
- Level: unit, integration if deterministic
- Fixture/setup: package-local helper seam or fixture command path that makes directory creation succeed and `change.yaml` writing fail.
- Steps:
  - Execute the mutation path with JSON output.
  - Assert status `error`, exit code `1`, and an `errors[]` entry naming `docs/changes/<change-id>/change.yaml`.
  - Assert completed directory actions are marked `done`.
  - Assert failed file action is marked `failed`.
  - Assert summary and artifacts do not claim artifact-pack creation success.
- Expected result: non-atomic failure is observable and honest.
- Failure proves: partial mutation can look like success or hide changed filesystem state.
- Automation location: package helper tests; CLI integration only if deterministic without platform-specific permission assumptions.

### TNC-018. Human, quiet, debug, and no-color output obey shared CLI rules

- Covers: R57-R70, R61-R62, observability
- Level: integration
- Fixture/setup: temporary project.
- Steps:
  - Run successful human-mode `new-change` and assert output is concise, names the change root, and is not JSON.
  - Run `--json --quiet` and assert JSON is still printed.
  - Run `--json --debug` and assert stable top-level fields remain with diagnostics included.
  - Run with `--no-color` and `NO_COLOR=1` and assert no ANSI sequences.
  - Run an unknown option and assert exit `4` with no mutation.
- Expected result: `new-change` follows existing CLI output contracts.
- Failure proves: command-specific output diverged from package conventions.
- Automation location: package CLI tests.

### TNC-019. Existing CLI behavior and execution boundaries do not regress

- Covers: R1-R2, R24-R26, R74-R76, compatibility, performance expectations
- Level: integration, regression
- Fixture/setup: existing package tests and temporary non-Git project.
- Steps:
  - Run the full existing package test suite.
  - Assert `version`, `init --adapter codex`, lockfile parsing, archive verification, and official URL tests still pass.
  - Run `new-change` in a temporary directory that is not a Git repository.
  - Assert no Git remote, branch, hosted CI, PR, or project validation state is required.
- Expected result: `new-change` is additive and local-only.
- Failure proves: shared parser or package wiring regressed existing commands or added unapproved environmental dependencies.
- Automation location: `npm test --prefix packages/rigorloop`.

### TNC-020. Generated metadata validates with repository schema

- Covers: R27-R37, AC6, E1
- Level: integration, contract
- Fixture/setup: temporary project containing generated `change.yaml`.
- Steps:
  - Run successful standard and minimal `new-change` commands.
  - Validate generated metadata with `python scripts/validate-change-metadata.py <generated-change.yaml>` or an equivalent fixture copied into a stable temp path.
  - Assert validator passes.
- Expected result: generated change metadata satisfies repository-owned schema validation.
- Failure proves: command output cannot be consumed by current RigorLoop validation.
- Automation location: package CLI tests plus validation command in implementation milestone notes when feasible.

### TNC-021. Command scope is proportional to scaffolded paths

- Covers: performance expectations, R74-R76
- Level: integration, smoke
- Fixture/setup: temporary project with unrelated nested directories outside `docs/changes/<change-id>`.
- Steps:
  - Run `new-change --dry-run --json`.
  - Assert output actions include only approved planned paths.
  - Assert unrelated directories are not listed, modified, or required.
- Expected result: command behavior is tied to the scaffold plan, not repository-wide scans.
- Failure proves: implementation performs broad unapproved project inspection.
- Automation location: package CLI tests.

### TNC-022. Final selected validation covers implementation artifacts

- Covers: lifecycle closeout, selected CI readiness
- Level: smoke, CI
- Fixture/setup: completed implementation milestone or final branch state.
- Steps:
  - Run `npm test --prefix packages/rigorloop`.
  - Run `python scripts/test-select-validation.py`.
  - Run selected CI for `packages/rigorloop`, this spec, the plan, the test spec, and the change metadata.
  - Run `git diff --check --` for touched files.
- Expected result: repository-owned validation passes for code, tests, plans, and lifecycle artifacts.
- Failure proves: implementation evidence is incomplete or selector routing is broken.
- Automation location: local validation and final `verify` evidence.

## Fixtures and data

- Use temporary project roots from `mkdtempSync(join(tmpdir(), "rigorloop-cli-test-"))`.
- Reuse the existing `runCli`, `tempProject`, `listProject`, `readProjectFile`, and `actionFor` helpers where possible.
- Add fixture helpers for:
  - reading generated `change.yaml`;
  - asserting project tree contents;
  - creating symlinks where supported;
  - creating file/directory conflict states;
  - optional deterministic write-failure injection for partial failure tests.
- Keep generated metadata fixtures small and textual. Do not commit machine-local paths, temp paths, usernames, hostnames, or environment values.

## Mocking/stubbing policy

- Network access must not be used by `new-change`; tests may install a fetch seam that throws if called.
- Partial write failure should use an internal helper seam rather than public runtime environment variables.
- Do not add public environment-variable overrides solely for tests.
- Do not mock repository validators for `TNC-020`; use the real `validate-change-metadata.py` when running the integration validation step.
- Do not mock `exitCodeForResult`; assert command paths use it through process exit status.

## Migration or compatibility tests

- Existing `rigorloop init --adapter codex` and lockfile tests must continue passing.
- Existing projects without `rigorloop.yaml` must allow `new-change`.
- Existing projects with safe `docs/changes/` content must allow scaffolding when the selected `change.yaml` is absent.
- Existing `rigorloop.yaml`, `rigorloop.lock`, and unrelated files must remain unchanged.
- Existing change roots are not migrated or rewritten.

## Observability verification

- JSON output tests assert stable envelope fields, `command: "new-change"`, `actions`, `artifacts`, `blockers`, `warnings`, `errors`, `diagnostics`, and command-specific `change`.
- Human output tests assert concise non-JSON output that names the change root.
- Debug output tests assert diagnostics do not destabilize top-level JSON fields.
- No metrics, traces, or audit events are required or tested in this slice.

## Security/privacy verification

- Path validation tests reject traversal, absolute/multi-segment IDs, URL-encoded separators, whitespace, and control characters.
- Symlink tests prove planned directory paths are not followed.
- Generated file tests assert no machine-local absolute paths, usernames, hostnames, temp paths, tokens, environment variables, or stderr are written.
- Network-denial tests prove `new-change` does not fetch.

## Performance checks

- No benchmark is required.
- `TNC-021` acts as a proportional-scope smoke test by proving unrelated project trees do not appear in actions or output.
- The final package test suite should remain fast enough for selected CI; broad smoke is not required by this slice.

## Manual QA checklist

- Run `node packages/rigorloop/dist/bin/rigorloop.js new-change manual-check --title "Manual check"` in a temporary project.
- Inspect `docs/changes/manual-check/change.yaml`.
- Confirm no `explain-change.md`, `rigorloop.yaml`, or `rigorloop.lock` was created.
- Run the same command again and confirm it blocks rather than overwrites.

Manual QA is optional when automated coverage above passes.

## What not to test

- Do not test `rigorloop status` or `rigorloop validate`; they are future follow-ups.
- Do not test adapter installation through `new-change`.
- Do not test network download behavior for `new-change`.
- Do not test public npm publication.
- Do not test workflow YAML canonicality, generated workflow docs, or frozen drift checks.
- Do not test placeholder Markdown template behavior; the spec explicitly defers it.
- Do not require atomic rollback behavior; the spec requires observable non-atomic partial-failure reporting.

## Uncovered gaps

None. All normative first-slice requirements have direct automated or explicit validation coverage.

## Next artifacts

- Implement M1 from `docs/plans/2026-05-16-rigorloop-cli-new-change.md`.
- Run code-review after each implementation milestone.

## Follow-on artifacts

- None yet.

## Readiness

This test spec is active and ready to guide implementation of M1. Implementation must keep the active plan's current handoff summary, progress, decisions, and validation notes synchronized as milestones move through implementation and review.
