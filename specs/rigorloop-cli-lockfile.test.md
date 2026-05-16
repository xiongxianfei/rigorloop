# RigorLoop CLI Lockfile Test Spec

## Status

active

## Related spec and plan

- Spec: [RigorLoop CLI Lockfile](rigorloop-cli-lockfile.md), approved.
- Plan: [RigorLoop CLI durable lockfile](../docs/plans/2026-05-16-rigorloop-cli-lockfile.md), active and approved by `plan-review-r1`.
- Proposal: [RigorLoop Scaffolding CLI and Machine-Readable Workflow](../docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md), accepted.
- Architecture: [RigorLoop Canonical System Architecture](../docs/architecture/system/architecture.md), approved.
- ADR: [ADR-20260516-rigorloop-cli-lockfile](../docs/adr/ADR-20260516-rigorloop-cli-lockfile.md), accepted.
- Change metadata: [change.yaml](../docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml).
- Review records:
  - `docs/changes/2026-05-15-rigorloop-cli-lockfile/reviews/spec-review-r3.md`
  - `docs/changes/2026-05-15-rigorloop-cli-lockfile/reviews/architecture-review-r1.md`
  - `docs/changes/2026-05-15-rigorloop-cli-lockfile/reviews/plan-review-r1.md`

## Testing strategy

This slice makes `rigorloop.lock` durable project state, so proof must cover data shape, deterministic serialization, mutation safety, archive-verification ordering, drift handling, and stable command output.

- Unit tests prove strict lockfile parsing, required-field validation, unknown-field blocking, deterministic serialization, normalized manifest SHA-256 calculation, and `rigorloop-tree-hash-v1`.
- Integration tests execute the local CLI in temporary project directories and assert stdout, stderr, exit codes, filesystem effects, write-plan actions, lockfile contents, and unchanged-file behavior.
- Archive tests reuse existing fixture ZIP and bundled metadata helpers from `packages/rigorloop/test/cli.test.js`; they must prove lockfile writes happen only after archive verification and installed-tree verification.
- Drift tests create a valid lockfile, then mutate, remove, or conflict with `.agents/skills` before rerunning init.
- Network behavior remains fixture-backed with mocked fetch. Tests must not depend on live GitHub availability.
- Selected CI must include this test spec, active plan, change metadata, review artifacts, and `packages/rigorloop` paths touched by implementation.

## Requirement coverage map

| Requirement | Coverage |
|---|---|
| R1-R8 | TLF-001, TLF-002, TLF-003, TLF-012, TLF-020, TLF-021 |
| R9-R17h | TLF-001, TLF-004, TLF-005, TLF-006, TLF-007, TLF-008 |
| R18-R23b | TLF-001, TLF-009, TLF-010, TLF-011 |
| R23ba-R23bj | TLF-012, TLF-013, TLF-014, TLF-015 |
| R23c-R23k | TLF-004, TLF-005, TLF-006, TLF-009, TLF-010, TLF-011 |
| R24-R33 | TLF-016, TLF-017, TLF-018 |
| R34-R45e | TLF-003, TLF-012, TLF-013, TLF-019, TLF-020, TLF-021, TLF-022 |
| R46-R53 | TLF-023, TLF-024, TLF-025, TLF-026, TLF-027 |
| R54-R61 | TLF-003, TLF-004, TLF-006, TLF-009, TLF-012, TLF-020, TLF-023, TLF-026, TLF-028 |
| R62-R66 | TLF-012, TLF-019, TLF-021, TLF-029 |

## Example coverage map

| Example | Coverage |
|---|---|
| E1 | TLF-012 |
| E2 | TLF-003 |
| E3 | TLF-019, TLF-022 |
| E4 | TLF-023, TLF-024 |
| E5 | TLF-004, TLF-005 |

## Edge case coverage

| Edge case | Coverage |
|---|---|
| Existing project has `rigorloop.yaml` and no `rigorloop.lock` | TLF-012 |
| Existing project has an empty `rigorloop.lock` | TLF-004 |
| Existing project has unsupported `schema_version` | TLF-006 |
| Existing lockfile has a future unknown top-level section | TLF-005 |
| Existing generated output matches recorded tree hash | TLF-019, TLF-022 |
| Existing generated output differs from recorded tree hash | TLF-023, TLF-024 |
| Existing lockfile records `.agents/skills`, but the path is missing | TLF-025 |
| Existing lockfile records `.agents/skills`, but that path is a file | TLF-026 |
| Local archive install succeeds and records only archive basename | TLF-013, TLF-014 |
| Dry-run computes planned lockfile content but writes nothing | TLF-003 |

## Milestone coverage map

| Milestone | Coverage |
|---|---|
| M1. Lockfile schema, parser, serializer, and write-plan contract | TLF-001-TLF-011, TLF-016-TLF-018, TLF-028 |
| M2. Successful lockfile creation and update after verified Codex install | TLF-012-TLF-015, TLF-019-TLF-022, TLF-029 |
| M3. Drift and conflict blocking for existing lockfile state | TLF-023-TLF-027 |
| Lifecycle closeout | TLF-030, selected CI, final package test command |

## Test cases

### TLF-001. Valid lockfile fixture parses and preserves the supported shape

- Covers: R1-R3, R9-R18i, R21-R23b, AC3, AC5
- Level: unit, contract
- Fixture/setup: full valid `schema_version: 1` lockfile fixture with one Codex entry under `generated.adapters[]`.
- Steps:
  - Parse the fixture through the lockfile helper.
  - Assert top-level sections are `schema_version`, `rigorloop`, `manifest`, and `generated`.
  - Assert the Codex entry includes `release`, `source`, `archive`, `archive_sha256`, `installed_root`, `tree_hash_algorithm`, `tree_sha256`, and `file_count`.
  - Assert adapter entries are nested under `generated.adapters[]`.
- Expected result: the supported lockfile shape is accepted.
- Failure proves: implementation authors invented or lost part of the public durable shape.
- Automation location: `packages/rigorloop/test/cli.test.js` or package-local lockfile unit tests.

### TLF-002. Non-CLI command surfaces do not write lockfiles

- Covers: R2, R4, R5
- Level: integration
- Fixture/setup: temporary project directory.
- Steps:
  - Run currently supported non-mutating commands such as `rigorloop --help` and `rigorloop version`.
  - Attempt unsupported future commands if dispatch exists.
  - Assert no `rigorloop.lock` is created.
- Expected result: only in-scope successful Codex init can write `rigorloop.lock`.
- Failure proves: lockfile authority leaked beyond the approved command surface.
- Automation location: package CLI tests.

### TLF-003. Dry-run reports planned lockfile and writes nothing

- Covers: R7, R34, R35, R54-R56, AC2, E2
- Level: integration
- Fixture/setup: empty temporary project.
- Steps:
  - Run `rigorloop init --adapter codex --dry-run --json`.
  - Assert JSON includes `planned_lockfile`.
  - Assert actions/artifacts include `rigorloop.lock` with a planned or skipped dry-run status.
  - Assert no `rigorloop.lock`, `rigorloop.yaml`, or `.agents/skills` files are created.
- Expected result: dry-run remains a promise, not a mutation.
- Failure proves: dry-run writes durable state or hides lockfile planning.
- Automation location: package CLI tests.

### TLF-004. Malformed or empty lockfile fails as invalid config

- Covers: R23k, R40, R58, R60, E5, edge case 2
- Level: integration
- Fixture/setup: temporary project with `rigorloop.lock` containing empty content or malformed YAML.
- Steps:
  - Run `rigorloop init --adapter codex --from-archive <valid-fixture.zip> --json`.
  - Assert status `error`, exit code `4`, and an invalid-lockfile or invalid-config error.
  - Assert generated output is not mutated.
- Expected result: malformed lockfile blocks before mutation.
- Failure proves: invalid durable state can be overwritten or treated as success.
- Automation location: package CLI tests.

### TLF-005. Unknown fields block before mutation

- Covers: R23c-R23e, R23i-R23j, R41, R45c, AC7, edge case 4
- Level: integration
- Fixture/setup: valid lockfile plus one unknown top-level section, unknown known-section field, or unknown adapter-entry field.
- Steps:
  - Run init with a valid archive fixture.
  - Assert status `blocked`, exit code `2`, blocker code `unsupported-lockfile-shape`.
  - Assert no generated output or lockfile mutation occurs.
- Expected result: first-slice unknown shape blocks.
- Failure proves: older CLIs can silently erase future lockfile data.
- Automation location: package CLI tests.

### TLF-006. Unsupported schema version, source, adapter, or tree hash algorithm blocks

- Covers: R23f-R23h, R23ha-R23hb, R42, R45c, R66, AC7, AC12
- Level: integration
- Fixture/setup: lockfile fixtures with `schema_version: 2`, `source: mirror`, `adapter: claude`, or `tree_hash_algorithm: other`.
- Steps:
  - Run init with a valid archive fixture.
  - Assert status `blocked`, exit code `2`, blocker code `unsupported-lockfile-shape`.
  - Assert no mutation occurs.
- Expected result: unsupported future or out-of-scope state blocks before mutation.
- Failure proves: unsupported lockfile semantics can be rewritten as supported state.
- Automation location: package CLI tests.

### TLF-007. Missing required fields and invalid field types fail with exit code 4

- Covers: R10-R18i, R23k, AC6
- Level: unit, integration
- Fixture/setup: lockfile fixtures missing `rigorloop.package`, `manifest.path`, `generated.adapters`, adapter `release`, adapter `tree_hash_algorithm`, or with wrong scalar/list types.
- Steps:
  - Parse fixtures through the lockfile helper.
  - Run at least one CLI integration case with a missing required field.
  - Assert status `error` and exit code `4`.
- Expected result: required shape violations are invalid config, not internal failures.
- Failure proves: invalid lockfiles are accepted or misclassified.
- Automation location: package lockfile unit tests and CLI tests.

### TLF-008. Serialization is deterministic and excludes forbidden data

- Covers: R9-R15, R17b-R17g, R39, R43, AC4
- Level: unit, contract
- Fixture/setup: parsed lockfile object with one Codex entry and supported unrelated entries only if a future fixture is allowed by the spec.
- Steps:
  - Serialize the same lockfile state twice.
  - Assert byte-identical UTF-8/LF output.
  - Assert generated adapter entries are sorted by adapter name.
  - Assert no timestamps, absolute paths, usernames, hostnames, temp paths, environment variables, secrets, or tokens appear.
- Expected result: deterministic, reviewable lockfile bytes.
- Failure proves: lockfile output is not reproducible or leaks local data.
- Automation location: package lockfile unit tests.

### TLF-009. Unsupported adapter entries block even when Codex entry is valid

- Covers: R23a-R23b, R23g, R37, R45c
- Level: integration
- Fixture/setup: lockfile with valid Codex entry plus an unsupported `claude` entry.
- Steps:
  - Run `rigorloop init --adapter codex --json`.
  - Assert status `blocked`, exit code `2`, blocker code `unsupported-lockfile-shape`.
- Expected result: first slice refuses unsupported adapter entries.
- Failure proves: multi-adapter update behavior was invented without a spec.
- Automation location: package CLI tests.

### TLF-010. Unsupported source value blocks with the required public contract

- Covers: R18c-R18ca, R23ha-R23hb, AC12
- Level: integration
- Fixture/setup: Codex lockfile entry with `source: local-folder`.
- Steps:
  - Run init with a valid archive fixture.
  - Assert status `blocked`, exit code `2`, blocker code `unsupported-lockfile-shape`.
- Expected result: only `release-archive` and `local-archive` are allowed.
- Failure proves: source semantics are not stable.
- Automation location: package CLI tests.

### TLF-011. Other install roots are rejected

- Covers: R18f, R23, R52
- Level: integration
- Fixture/setup: Codex lockfile entry with `installed_root: ".codex/skills"`.
- Steps:
  - Run init with a valid archive fixture.
  - Assert blocked or invalid-config behavior before mutation according to the implemented validation class.
  - Assert no files are written outside `.agents/skills`.
- Expected result: first-slice lockfile install root remains `.agents/skills`.
- Failure proves: lockfile can redirect generated output outside the approved root.
- Automation location: package CLI tests.

### TLF-012. Network install writes a complete lockfile after verification

- Covers: R4-R8, R18-R19, R21-R22, R23ba-R23bd, R24-R32, R36, R45a, R54-R57, R62-R65, AC1, AC3, AC10, E1
- Level: integration
- Fixture/setup: temporary project, bundled metadata fixture, mocked official GitHub archive fetch.
- Steps:
  - Run `rigorloop init --adapter codex --json`.
  - Assert exit code `0` and success or warning status.
  - Assert `rigorloop.lock` exists after adapter verification and extraction.
  - Assert lockfile records package identity, manifest path/hash, release tag, `source: release-archive`, archive filename/SHA, `.agents/skills`, `rigorloop-tree-hash-v1`, tree hash, and file count.
  - Assert JSON actions/artifacts include durable `rigorloop.lock` creation or update.
  - Assert warning code `lockfile-spec-not-approved` is absent.
- Expected result: verified network Codex init records durable generated-output state.
- Failure proves: success can occur without durable lockfile state or with stale first-slice warnings.
- Automation location: package CLI tests.

### TLF-013. Local archive install writes `source: local-archive`

- Covers: R20, R23be-R23bh, R36, AC1, AC11
- Level: integration
- Fixture/setup: temporary project and matching local fixture archive.
- Steps:
  - Run `rigorloop init --adapter codex --from-archive ./rigorloop-adapter-codex-v0.1.3.zip --json`.
  - Assert `rigorloop.lock` contains `source: local-archive`.
  - Assert `release` remains the official package-compatible tag.
  - Assert `archive_sha256` matches trusted metadata.
- Expected result: local archive delivery mode is recorded distinctly from network download.
- Failure proves: local archive installs are mislabeled or not recorded.
- Automation location: package CLI tests.

### TLF-014. Local archive lockfile omits machine-local path data

- Covers: R13-R14, R20, R23bi-R23bj, AC11
- Level: integration, security
- Fixture/setup: local archive at an absolute temp path.
- Steps:
  - Run local archive init using the absolute archive path.
  - Read `rigorloop.lock`.
  - Assert only the archive basename is recorded.
  - Assert temp directory, username, hostname, and absolute archive path substrings do not appear.
- Expected result: durable state is portable and does not leak machine-local paths.
- Failure proves: local project state leaks private or host-specific information.
- Automation location: package CLI tests.

### TLF-015. Reinstall through a different source mode updates only the Codex entry

- Covers: R38-R39, R45b-R45d
- Level: integration
- Fixture/setup: project initialized once through network mode or local mode, then rerun through the other mode with matching trusted metadata.
- Steps:
  - Capture lockfile before reinstall.
  - Rerun init through the other source mode.
  - Assert only `rigorloop.version`, `manifest.sha256`, and the matching Codex entry change.
  - Assert source changes to the latest delivery mode.
- Expected result: source mode records the latest verified install without broad lockfile rewrites.
- Failure proves: update behavior mutates unrelated state or cannot switch source modes.
- Automation location: package CLI tests.

### TLF-016. `rigorloop-tree-hash-v1` hashes normalized regular files only

- Covers: R24-R32
- Level: unit
- Fixture/setup: generated output fixture with Markdown CRLF, UTF-8 BOM, binary file, nested directories, and ignored directories.
- Steps:
  - Compute file hashes and tree hash.
  - Assert text normalizes CRLF/CR to LF and removes BOM.
  - Assert binary bytes hash raw.
  - Assert directories, symlinks, mtimes, owners, absolute paths, temp files, and `rigorloop.lock` are excluded.
  - Assert manifest rows use `<relative_path>\t<file_sha256>` and sorted POSIX paths.
- Expected result: tree hash is deterministic and platform-independent.
- Failure proves: generated-output drift checks can vary across platforms.
- Automation location: package lockfile/tree-hash unit tests.

### TLF-017. Mixed text and binary classification is deterministic

- Covers: R28-R33
- Level: unit
- Fixture/setup: generated output fixture containing `.md` files and at least one non-Markdown file if the archive fixture supports it.
- Steps:
  - Compute tree hash twice.
  - Assert the same files receive the same normalization class each time.
- Expected result: future mixed output cannot silently change hash behavior.
- Failure proves: tree hash depends on runtime guesswork.
- Automation location: package unit tests.

### TLF-018. File count matches regular files included in tree hash

- Covers: R18i, R25-R26
- Level: unit, integration
- Fixture/setup: archive fixture with directories and regular files.
- Steps:
  - Install archive.
  - Read `file_count` from lockfile.
  - Assert count equals the number of regular files included in the tree manifest.
- Expected result: file count reflects the tree-hash input set.
- Failure proves: lockfile metadata does not describe generated output accurately.
- Automation location: package CLI tests.

### TLF-019. Matching existing generated output keeps lockfile deterministic

- Covers: R11-R12, R37-R39, R45b, AC4, E3
- Level: integration
- Fixture/setup: project after successful lockfile-enabled init.
- Steps:
  - Capture `rigorloop.lock` bytes.
  - Rerun the same init with matching archive/metadata and unchanged `.agents/skills`.
  - Assert command reports unchanged, existing, or updated only where allowed.
  - Assert lockfile bytes are identical when state is identical.
- Expected result: reruns are stable and do not churn durable state.
- Failure proves: deterministic lockfile behavior is broken.
- Automation location: package CLI tests.

### TLF-020. Failed archive, metadata, or installed-tree verification does not create or update lockfile

- Covers: R6, R8, R45e, AC13
- Level: integration, security
- Fixture/setup: no lockfile and cases for metadata unavailable, archive SHA mismatch, size mismatch, archive tree-hash mismatch, path traversal, symlink, install-root invalid, and pre-existing installed-tree mismatch.
- Steps:
  - Run init for each failure case.
  - Assert the expected status and exit code from the existing archive contract.
  - Assert `rigorloop.lock` is absent.
- Required installed-tree mismatch cases:
  - extra pre-existing file under `.agents/skills`;
  - modified expected adapter file;
  - missing expected adapter file with a partial installed tree.
- Expected result: failed verification cannot claim generated output.
- Failure proves: lockfile can record untrusted or failed output.
- Automation location: package CLI tests.

### TLF-021. Failed verification leaves existing lockfile unchanged

- Covers: R8, R38-R40, R45e, AC13
- Level: integration
- Fixture/setup: valid existing lockfile, then a rerun with archive SHA mismatch, archive tree-hash mismatch, or installed-tree mismatch.
- Steps:
  - Capture lockfile bytes.
  - Run failing init.
  - Assert lockfile bytes are unchanged.
- Expected result: failures do not corrupt existing durable state.
- Failure proves: failed updates can damage the lockfile.
- Automation location: package CLI tests.

### TLF-022. Existing supported lockfile with no Codex entry can add Codex only when shape is supported

- Covers: R37, R39, R45b-R45c
- Level: integration
- Fixture/setup: supported lockfile shape with empty `generated.adapters` or only supported future-free state.
- Steps:
  - Run verified Codex init.
  - Assert a Codex entry is added.
  - Assert existing supported fields remain deterministic.
- Expected result: first lockfile-enabled install works for first-slice projects that already have a supported lockfile shell.
- Failure proves: add-entry semantics are missing or destructive.
- Automation location: package CLI tests.

### TLF-023. Drifted generated file blocks destructive replacement

- Covers: R46-R50, R58, AC8, E4
- Level: integration
- Fixture/setup: successful lockfile-enabled init, then modify one installed Markdown file.
- Steps:
  - Rerun init with matching archive.
  - Assert status `blocked` or specified drift failure status, with no overwrite.
  - Assert output identifies adapter, installed root, expected tree hash, and actual tree hash.
- Expected result: modified generated output is visible and protected.
- Failure proves: user or generated changes can be overwritten silently.
- Automation location: package CLI tests.

### TLF-024. Drifted generated output remains unchanged after blocked rerun

- Covers: R47-R48, R50, AC8
- Level: integration
- Fixture/setup: same as TLF-023.
- Steps:
  - Capture modified file content.
  - Run init.
  - Assert the modified file content remains unchanged.
- Expected result: drift blocker is non-destructive.
- Failure proves: drift detection happens too late.
- Automation location: package CLI tests.

### TLF-025. Missing generated output root represented in lockfile blocks before replacement

- Covers: R51, AC8, edge case 7
- Level: integration
- Fixture/setup: valid lockfile recording `.agents/skills`, then remove `.agents/skills`.
- Steps:
  - Run init with valid archive.
  - Assert drift or missing-generated-output blocker before replacement proceeds.
  - Assert output identifies adapter and install root.
- Expected result: missing generated output represented in the lockfile is visible.
- Failure proves: lockfile-recorded state can disappear without warning.
- Automation location: package CLI tests.

### TLF-026. Generated output directory conflicts exit 5

- Covers: R52, R59, edge case 8
- Level: integration
- Fixture/setup: lockfile records `.agents/skills`; filesystem has `.agents/skills` as a file.
- Steps:
  - Run init with valid archive.
  - Assert status `blocked`, exit code `5`, and path-specific mutation conflict.
  - Assert no lockfile update occurs.
- Expected result: directory/file conflict is a mutation conflict.
- Failure proves: filesystem conflicts are misclassified or overwritten.
- Automation location: package CLI tests.

### TLF-027. Generated file path conflicts as directory exit 5

- Covers: R53, R59
- Level: integration
- Fixture/setup: lockfile or archive expects `.agents/skills/proposal/SKILL.md`; filesystem has that path as a directory.
- Steps:
  - Run init with valid archive.
  - Assert status `blocked`, exit code `5`, and path-specific mutation conflict.
  - Assert no lockfile update occurs.
- Expected result: file/directory conflicts block safely.
- Failure proves: generated file writes can corrupt existing directories.
- Automation location: package CLI tests.

### TLF-028. Lockfile schema validation failure exit classes are stable

- Covers: R58-R61
- Level: unit, integration
- Fixture/setup: table of invalid config, expected verification failure, mutation conflict, and simulated internal serialization failure.
- Steps:
  - Assert malformed/missing required fields exit `4`.
  - Assert expected generated-output validation failure exits `3` when applicable.
  - Assert mutation conflict exits `5`.
  - Assert unexpected serializer/filesystem exception exits `1`.
- Expected result: public exit-code contract distinguishes expected failures from internal errors.
- Failure proves: agents and CI cannot classify lockfile failures reliably.
- Automation location: package CLI tests and helper-level tests.

### TLF-029. Package-local execution remains supported

- Covers: R64-R65
- Level: smoke, integration
- Fixture/setup: repository-local CLI path `node packages/rigorloop/dist/bin/rigorloop.js`.
- Steps:
  - Run package-local dry-run and local archive init with fixture metadata.
  - Assert behavior matches installed execution path.
  - Assert no public npm publication is required.
- Expected result: implementation can be verified before public npm hardening.
- Failure proves: lockfile behavior depends on an out-of-scope publish path.
- Automation location: package CLI tests or final validation command.

### TLF-030. Final selected CI and package test suite pass

- Covers: lifecycle closeout, AC1-AC13
- Level: CI, smoke
- Fixture/setup: final changed paths from implementation.
- Steps:
  - Run `npm test --prefix packages/rigorloop`.
  - Run selected CI over package paths, spec, test spec, plan, and change-local artifacts.
  - Run `git diff --check -- <touched paths>`.
- Expected result: repository-owned checks and package tests pass before code-review/final closeout.
- Failure proves: implementation proof is incomplete.
- Automation location: local validation and CI.

## Fixtures and data

- Temporary project directories from the existing package test helper.
- Fixture ZIP archives generated in tests with regular files, directories, traversal entries, symlink entries, text CRLF/BOM cases, binary files, and install-root conflicts.
- Bundled metadata fixtures compatible with `v0.1.3` and the existing `fixturePackage` helper.
- Full valid lockfile fixtures for both `source: release-archive` and `source: local-archive`.
- Invalid lockfile fixtures for malformed YAML, missing fields, wrong types, unsupported schema, unknown sections, unsupported adapter, unsupported source, unsupported tree hash algorithm, absolute path leakage, and future-field shapes.
- Drift fixtures built by installing once, then modifying, deleting, or replacing `.agents/skills` paths before rerun.

## Mocking/stubbing policy

- Mock network archive download through an internal fetch seam or `NODE_OPTIONS --import` fixture, as in the existing CLI tests.
- Do not use live GitHub in tests.
- Do not mock filesystem mutation for integration tests; use temporary project directories and assert real file contents.
- Do not use user-supplied metadata as a trust root.
- Do not snapshot the entire JSON envelope as the only proof; assert stable fields and behavior directly.

## Migration or compatibility tests

- First-slice projects with `rigorloop.yaml` and no `rigorloop.lock` must succeed and create the lockfile after verified install: TLF-012.
- Existing valid lockfiles with matching generated output must rerun deterministically: TLF-019.
- Unsupported future lockfile shapes must block rather than migrate or preserve: TLF-005, TLF-006.
- Package-local execution must remain supported without public npm publication: TLF-029.
- No automatic migration or repair command is tested because it is out of scope.

## Observability verification

- JSON output exposes lockfile actions and artifacts for planned, created, updated, unchanged, skipped, and blocked states: TLF-003, TLF-012, TLF-019, TLF-023.
- Human output states whether `rigorloop.lock` was created, updated, unchanged, skipped, or blocked where human-mode assertions are practical: TLF-012, TLF-019, TLF-023.
- Drift output includes expected and actual tree hashes when available: TLF-023.
- Validation evidence names commands that created, updated, or refused lockfile writes: TLF-030.

## Security/privacy verification

- Lockfile content must not contain secrets, tokens, absolute local paths, usernames, hostnames, temporary directories, environment variable values, or full adapter metadata: TLF-008, TLF-014.
- Lockfile writes must not expand network trust boundaries or accept user metadata: TLF-012, TLF-013, TLF-020.
- Unknown or unsupported lockfile shape blocks before mutation: TLF-005, TLF-006.
- Failed verification never writes or updates lockfile state: TLF-020, TLF-021.

## Performance checks

- Tree hashing is covered by deterministic unit fixtures and should be linear in file count and file bytes.
- No benchmark is required for this slice because Codex adapter fixture sizes are small and the spec only sets linear behavior, not a numeric budget.
- If implementation introduces a broad recursive scan outside `.agents/skills`, add a regression test that proves the scan root is restricted to the generated output root.

## Manual QA checklist

- Inspect one human-mode success message and one human-mode drift/blocker message for concise, actionable wording.
- Confirm no final evidence claims hosted CI unless the hosted run was observed.

## What not to test

- Do not test `new-change`, `status`, `validate`, workflow rendering, npm publishing, non-Codex adapters, lockfile migration, lock repair, or generated workflow docs; they are non-goals.
- Do not test real GitHub download availability; use mocked fetch for network-mode archive bytes.
- Do not require changed-file drift lists; they are best-effort and must not weaken tree-hash proof.
- Do not test broad YAML preservation because unknown-field preservation is explicitly out of scope.

## Uncovered gaps

- None. The approved spec and architecture are testable within package tests, fixture CLI integration tests, and selected CI.

## Next artifacts

- `implement` M1 from [the active lockfile plan](../docs/plans/2026-05-16-rigorloop-cli-lockfile.md).

## Follow-on artifacts

- None yet.

## Readiness

Ready for the next lifecycle stage: M1 execution.
