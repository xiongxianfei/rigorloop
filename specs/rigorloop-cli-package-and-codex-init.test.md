# RigorLoop CLI Package and Codex Init Test Spec

## Status

active

## Related spec and plan

- Spec: [RigorLoop CLI Package and Codex Init](rigorloop-cli-package-and-codex-init.md), approved.
- Plan: [RigorLoop CLI package and Codex init](../docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md), active and approved by `plan-review-r1`.
- Proposal: [RigorLoop Scaffolding CLI and Machine-Readable Workflow](../docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md), accepted.
- Architecture: [RigorLoop Canonical System Architecture](../docs/architecture/system/architecture.md), approved.
- ADR: [ADR-20260515-rigorloop-cli-package-and-codex-init](../docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md), accepted.
- Change metadata: [change.yaml](../docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml).
- Review records:
  - `docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/reviews/spec-review-r2.md`
  - `docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/reviews/architecture-review-r1.md`
  - `docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/reviews/plan-review-r1.md`

## Testing strategy

This is a public command, filesystem mutation, archive verification, package-boundary, and security-sensitive first slice. The proof must use automated package tests, fixture-backed CLI execution, and repository selected CI. Manual verification is limited to inspecting command output readability where automation cannot judge wording quality.

- Unit tests prove argument parsing, package metadata discovery, JSON envelope shape, exit-code mapping, `rigorloop.yaml` rendering, write-plan classification, tree-hash calculation, and metadata validation.
- Integration tests execute the local CLI in temporary project directories and assert stdout, stderr, exit code, filesystem effects, no-lockfile behavior, overwrite refusal, and target confinement.
- Archive tests use small fixture ZIP files and bundled metadata fixtures to prove success, checksum failure, size failure, tree-hash failure, traversal rejection, symlink rejection, install-root rejection, and metadata-unavailable behavior.
- Network behavior is tested with stubbed fetch/client behavior. Tests must not depend on live GitHub availability.
- Smoke tests execute the built package entrypoint or the repository-local equivalent for `--help`, `version`, dry-run init, and a successful local-archive init.
- Selected CI must include this test spec, active plan, change metadata, and package paths touched by implementation.

## Requirement coverage map

| Requirement | Coverage |
|---|---|
| R1-R4 | T1, T2, T3, T28 |
| R5-R8 | T2, T3, T4, T5 |
| R9-R20 | T6, T7, T8, T9, T10, T11 |
| R21-R24 | T12, T13, T14, T18 |
| R25-R29a | T15, T16, T17, T18, T19 |
| R30-R37c | T20, T21, T22, T23 |
| R38-R45 | T24, T25, T26, T27 |
| R46-R48 | T30, T31, T32, T33, T34 |
| R49-R50h | T15, T18, T19, T29 |
| R51-R55 | T29, T35, T36, T37, T38 |
| R56-R61c | T30, T31, T32, T33, T34, T39, T40 |
| R62-R67 | T22, T23, T41 |
| R68-R75 | T42, T43, T44 |
| R76-R79 | T1, T28, T45 |

## Example coverage map

| Example | Coverage |
|---|---|
| E1 | T2 |
| E2 | T3 |
| E3 | T6, T12, T22, T24 |
| E4 | T15, T20, T23, T29, T41 |
| E5 | T18, T29, T30, T42 |
| E6 | T26, T27 |
| E7 | T23, T41 |

## Edge case coverage

| Edge case | Coverage |
|---|---|
| Existing `rigorloop.yaml` is present and valid | T21 |
| Existing `rigorloop.yaml` is incompatible | T21 |
| `.agents/skills` exists but is empty | T20, T25 |
| `.agents/` exists and `.agents/skills` is missing | T24 |
| `.agents/` and `.agents/skills` both exist | T24 |
| `.agents` exists as a file | T26 |
| `.agents/skills` exists as a file | T26 |
| `.agents/skills` contains unrelated files | T26, T27 |
| Release metadata lists multiple adapters | T35 |
| Bundled adapter metadata unavailable | T19 |
| `--from-archive` path does not exist | T14 |
| Archive contains symlinks | T33 |
| Archive contains files outside `.agents/skills` | T30, T31 |
| Package version cannot be determined | T3, T11 |
| `--json` and `--quiet` are combined | T8 |
| `NO_COLOR` is set | T10 |
| Local archive release is incompatible with concrete package version | T17 |

## Milestone coverage map

| Milestone | Coverage |
|---|---|
| M1. Package skeleton, command discovery, and command contract core | T1-T11, T28, T45 |
| M2. Init dry-run, write planning, and `rigorloop.yaml` scaffold | T12-T14, T20-T27, T41 |
| M3. Codex adapter metadata, archive verification, extraction, and tree hash | T15-T19, T29-T40, T42-T44 |
| Lifecycle closeout | T46, selected CI, final package test command |

## Test cases

### T1. Package metadata exposes one public binary

- Covers: R1, R2, R3, R4, R76-R79
- Level: unit, contract
- Fixture/setup: `packages/rigorloop/package.json`
- Steps:
  - Read package metadata.
  - Assert package name is `@xiongxianfei/rigorloop`.
  - Assert `bin` contains exactly one public binary named `rigorloop`.
  - Assert the bin target points to the built CLI entrypoint.
  - Assert package files do not include adapter archive ZIP files as authored source.
- Expected result: the package has one command entrypoint and no bundled adapter archives.
- Failure proves: the first-slice package boundary is wider than the approved spec.
- Automation location: package test suite under `packages/rigorloop`.

### T2. Help output shows only the implemented command surface

- Covers: R4, R5, E1
- Level: smoke, integration
- Fixture/setup: built or source CLI entrypoint
- Steps:
  - Run `rigorloop --help`.
  - Assert exit code `0`.
  - Assert stdout mentions `rigorloop`, `rigorloop version`, and `rigorloop init --adapter codex`.
  - Assert stdout does not imply `new-change`, `status`, or `validate` are implemented.
- Expected result: help discovers the first command surface without overclaiming future commands.
- Failure proves: users can be directed to unsupported behavior.
- Automation location: package CLI integration tests.

### T3. Version output reports package identity

- Covers: R1, R6, package-version edge case, E2
- Level: unit, smoke
- Fixture/setup: package metadata with version `0.1.3`; negative fixture with missing version
- Steps:
  - Run `rigorloop version`.
  - Assert stdout contains `@xiongxianfei/rigorloop` and the package version.
  - In the missing-version fixture, assert the command reports an error instead of guessing.
- Expected result: version reporting is deterministic.
- Failure proves: JSON and compatibility behavior can be based on guessed package identity.
- Automation location: package tests.

### T4. Unknown commands return usage errors

- Covers: R7
- Level: integration
- Fixture/setup: local CLI
- Steps:
  - Run `rigorloop unknown-command`.
  - Assert exit code `4`.
  - Assert the output includes an actionable usage error.
- Expected result: unsupported command syntax is rejected as invalid usage.
- Failure proves: command dispatch fails open.
- Automation location: package CLI tests.

### T5. Unsupported adapters are blocked

- Covers: R8, R21
- Level: integration
- Fixture/setup: temporary project directory
- Steps:
  - Run `rigorloop init --adapter claude --json`.
  - Assert status `blocked`, exit code `2`, and a blocker identifying the unsupported adapter.
  - Assert no `.claude`, `.opencode`, `.agents`, `rigorloop.yaml`, or `rigorloop.lock` files are written.
- Expected result: only Codex is supported in this slice.
- Failure proves: non-Codex scope leaks into the first implementation.
- Automation location: package CLI tests.

### T6. JSON envelope is stable and stdout contains JSON only

- Covers: R9-R15, E3
- Level: contract, integration
- Fixture/setup: temporary empty project directory
- Steps:
  - Run `rigorloop init --adapter codex --dry-run --json`.
  - Parse stdout as exactly one JSON object.
  - Assert top-level fields: `schema_version`, `command`, `package`, `cwd`, `status`, `summary`, `actions`, `artifacts`, `blockers`, `warnings`, `errors`, `diagnostics`.
  - Assert action, artifact, blocker, warning, and error entries use stable fields when present.
  - Assert stderr does not contain routine JSON fragments.
- Expected result: agents and CI can parse output deterministically.
- Failure proves: machine-readable output is not a stable contract.
- Automation location: package CLI tests.

### T7. Human output is not JSON-fragment output

- Covers: R16, R17
- Level: integration
- Fixture/setup: temporary project directory
- Steps:
  - Run `rigorloop init --adapter codex --dry-run` without `--json`.
  - Assert stdout is human-readable and not a raw JSON envelope.
  - Trigger a known usage error and assert human diagnostics may appear on stderr while JSON stdout rules are unaffected in JSON mode.
- Expected result: human mode and JSON mode are distinct.
- Failure proves: user-facing output and machine output are mixed.
- Automation location: package CLI tests.

### T8. Quiet mode does not change JSON shape or behavior

- Covers: R18, R19, JSON/quiet edge case
- Level: contract
- Fixture/setup: temporary project directory
- Steps:
  - Run `rigorloop init --adapter codex --dry-run --json --quiet`.
  - Assert stdout remains a complete JSON envelope.
  - Assert exit code and status match the same command without `--quiet`.
- Expected result: `--quiet` suppresses only non-essential human output.
- Failure proves: quiet mode breaks CI or agent parsing.
- Automation location: package tests.

### T9. Debug mode preserves stable top-level JSON fields

- Covers: R18
- Level: contract
- Fixture/setup: temporary project directory
- Steps:
  - Run `rigorloop init --adapter codex --dry-run --json --debug`.
  - Assert all stable top-level fields remain.
  - Assert extra details, if any, appear under `diagnostics`.
- Expected result: debug adds information without breaking contract fields.
- Failure proves: debug mode changes the public API shape.
- Automation location: package tests.

### T10. Color is disabled by flag and environment

- Covers: R20, accessibility edge case
- Level: unit, integration
- Fixture/setup: human output command
- Steps:
  - Run help or dry-run with `--no-color`.
  - Run the same command with `NO_COLOR=1`.
  - Assert no ANSI escape sequences appear.
- Expected result: output is readable without color.
- Failure proves: accessibility and deterministic text output are not honored.
- Automation location: package tests.

### T11. Exit-code mapping is enforced

- Covers: R12, package-version edge case
- Level: unit, contract
- Fixture/setup: table-driven command/result cases
- Steps:
  - Assert success and warning map to `0`.
  - Assert blocked maps to `2`.
  - Assert validation/archive verification failures map to `3`.
  - Assert usage/config errors map to `4`.
  - Assert overwrite refusal maps to `5`.
  - Assert unexpected internal errors map to `1`.
- Expected result: every public failure class uses the spec exit code.
- Failure proves: CI cannot distinguish expected blockers from internal errors.
- Automation location: package unit tests.

### T12. Dry-run init performs no writes

- Covers: R21, R22, R31, R39, R40, E3
- Level: integration
- Fixture/setup: temporary empty project directory
- Steps:
  - Snapshot directory contents.
  - Run `rigorloop init --adapter codex --dry-run --json`.
  - Assert planned actions include `.agents`, `.agents/skills`, and `rigorloop.yaml` in deterministic order.
  - Assert `planned_lockfile` is present when metadata or install planning is available.
  - Assert the directory contents are unchanged.
- Expected result: dry-run is a pure planning operation.
- Failure proves: users cannot safely inspect planned writes.
- Automation location: package CLI tests.

### T13. Init requires `--adapter codex`

- Covers: R21
- Level: integration
- Fixture/setup: temporary project directory
- Steps:
  - Run `rigorloop init`.
  - Assert exit code `4` or blocked usage behavior defined by the implementation contract.
  - Assert output tells the user to provide `--adapter codex`.
  - Assert no files are written.
- Expected result: the first slice has no implicit adapter.
- Failure proves: init behavior can become ambiguous.
- Automation location: package tests.

### T14. Local archive path validation is deterministic

- Covers: R24, missing `--from-archive` edge case
- Level: integration
- Fixture/setup: temporary project directory
- Steps:
  - Run `rigorloop init --adapter codex --from-archive ./missing.zip`.
  - Assert exit code `4`.
  - Assert no files are written.
- Expected result: nonexistent local archive paths are invalid input.
- Failure proves: local archive mode can proceed without an input artifact.
- Automation location: package tests.

### T15. Network mode uses bundled metadata and official archive URL

- Covers: R25, R26, R28, R49, R50e, R50f, R61
- Level: integration, contract
- Fixture/setup: bundled metadata fixture whose Codex artifact URL points to an official or stubbed official archive URL
- Steps:
  - Run `rigorloop init --adapter codex` without `--from-archive`.
  - Assert the command verifies bundled metadata against the bundled release index before using archive metadata.
  - Assert the command downloads only the Codex archive URL named by the trusted bundled metadata.
  - Assert non-official URLs such as `data:`, `file:`, `http:`, wrong host, wrong owner/repo, wrong release, wrong archive filename, query strings, and fragments are rejected before fetch.
  - Assert unavailable archive download produces status `blocked`, exit code `2`, and a next action such as retry or `--from-archive`.
- Expected result: network mode uses bundled metadata as the metadata trust root and only fetches the official adapter archive.
- Failure proves: network install can depend on a missing metadata asset or use an untrusted source.
- Automation location: package tests with stubbed client.

### T16. Pinned and prerelease package versions map to matching release tags

- Covers: R26, R27
- Level: unit
- Fixture/setup: package-version table
- Steps:
  - Assert `0.1.3` maps to `v0.1.3`.
  - Assert a prerelease package version maps to the matching prerelease tag.
- Expected result: version-to-release mapping is deterministic.
- Failure proves: pinned setup cannot be reproduced.
- Automation location: package unit tests.

### T17. Incompatible local archive release is blocked

- Covers: R29, R29a, release mismatch edge case
- Level: integration
- Fixture/setup: package metadata expecting one release; local archive fixture named for another release
- Steps:
  - Run `rigorloop init --adapter codex --from-archive <incompatible-archive.zip> --json`.
  - Assert status `blocked`, exit code `2`, and blocker code `release-version-incompatible`.
  - Assert no files are extracted.
- Expected result: cross-version archive support is not silently allowed in this slice.
- Failure proves: package and adapter compatibility can drift.
- Automation location: package tests.

### T18. Local archive mode uses bundled metadata and no metadata flag

- Covers: R24, R50, R50a-R50c, E5
- Level: integration
- Fixture/setup: bundled metadata fixture for `v0.1.3`; matching archive fixture
- Steps:
  - Run `rigorloop init --adapter codex --from-archive <matching-archive.zip> --json`.
  - Assert the command does not require or advertise `--metadata`.
  - Assert archive verification uses bundled metadata for the package's compatible release.
- Expected result: local archive UX stays one archive argument while preserving verification.
- Failure proves: local install either becomes unsafe or too complex for normal users.
- Automation location: package tests.

### T19. Missing bundled metadata blocks local archive install

- Covers: R50b-R50d, R61a, metadata-unavailable edge case, AC11
- Level: integration
- Fixture/setup: package test fixture with no metadata for requested adapter/release
- Steps:
  - Run `rigorloop init --adapter codex --from-archive <archive.zip> --json`.
  - Assert status `blocked`, exit code `2`, and blocker code `metadata-unavailable`.
  - Assert no files are extracted.
- Expected result: local archive install cannot proceed without official bundled metadata.
- Failure proves: unverified local archives can install.
- Automation location: package tests.

### T20. Actual init writes minimum `rigorloop.yaml` and Codex install root

- Covers: R30, R32-R34, R37a, R37b, AC4
- Level: integration
- Fixture/setup: temporary empty project; matching local archive fixture
- Steps:
  - Run successful `rigorloop init --adapter codex --from-archive <matching-archive.zip>`.
  - Read `rigorloop.yaml`.
  - Assert `schema_version: 1`, package name/version, adapter `codex`, install root `.agents/skills`, and source type/release are present.
  - Assert `.agents/skills` contains the installed adapter files.
- Expected result: actual init creates only the first-slice manifest and adapter output.
- Failure proves: project scaffold is missing or incompatible with the spec.
- Automation location: package integration tests.

### T21. Existing manifest handling is non-destructive

- Covers: R30, R38, R41, manifest edge cases
- Level: integration
- Fixture/setup: valid existing `rigorloop.yaml`; incompatible existing `rigorloop.yaml`
- Steps:
  - Run init in a project with a valid existing manifest and assert the file is reported existing or skipped, not overwritten.
  - Run init in a project with an incompatible manifest and assert the command blocks with an actionable config error.
- Expected result: init never merges or overwrites project config blindly.
- Failure proves: existing user configuration can be damaged.
- Automation location: package tests.

### T22. Dry-run reports planned manifest content

- Covers: R31, R63-R66, E3
- Level: integration
- Fixture/setup: temporary empty project
- Steps:
  - Run dry-run JSON.
  - Assert artifacts/actions include planned `rigorloop.yaml`.
  - Assert JSON includes planned manifest content or enough action detail to reconstruct the planned write.
  - Assert `planned_lockfile.tree_hash_algorithm` is `rigorloop-tree-hash-v1` when lockfile planning is available.
- Expected result: dry-run is reviewable by humans and agents.
- Failure proves: mutation planning is opaque.
- Automation location: package tests.

### T23. Generated manifest avoids forbidden claims and validation commands

- Covers: R35-R37c, E7
- Level: integration
- Fixture/setup: successful init fixture
- Steps:
  - Read generated `rigorloop.yaml`.
  - Assert it does not include branch-ready, PR-ready, workflow-accepted, validation-success, lockfile-authority, or `validation.commands`.
  - If future implementation reserves validation command names, assert names are limited to the spec list and inactive or example-only.
- Expected result: first-slice config does not overclaim workflow state.
- Failure proves: init can create misleading source-of-truth state.
- Automation location: package tests.

### T24. Write plan precedes mutation

- Covers: R38, R40
- Level: unit, integration
- Fixture/setup: temporary project; mocked writer
- Steps:
  - Invoke init through a test seam that can observe planned writes before the writer runs.
  - Assert every created, skipped, blocked, or updated path appears in the plan.
  - Assert `.agents` and `.agents/skills` are each first-class `create-dir` actions.
  - Assert existing `.agents` and `.agents/skills` directories are reported as existing or skipped.
  - Assert JSON output includes the same planned or completed actions.
- Expected result: mutation is planned and observable.
- Failure proves: filesystem writes can happen outside the safety model.
- Automation location: package unit and integration tests.

### T25. Empty existing install root is allowed

- Covers: R38-R40, empty `.agents/skills` edge case
- Level: integration
- Fixture/setup: temporary project with empty `.agents/skills`
- Steps:
  - Run successful local archive init.
  - Assert install succeeds after conflict planning.
- Expected result: existing empty directories are not treated as conflicts.
- Failure proves: normal rerunnable project setup is unnecessarily blocked.
- Automation location: package tests.

### T26. User-file overwrite conflicts are refused

- Covers: R41, R45, AC6, E6
- Level: integration
- Fixture/setup: temporary project with `.agents/skills/proposal/SKILL.md` containing unrelated content
- Steps:
  - Run local archive init.
  - Assert exit code `5`.
  - Assert blocker or error names the conflicting path.
  - Assert the existing file content is unchanged.
  - Repeat with `.agents` as a file and assert `.agents/skills` is not created.
  - Repeat with `.agents/skills` as a file and assert `.agents` is reported existing or skipped while `.agents/skills` is blocked.
- Expected result: init refuses user-file overwrite.
- Failure proves: adapter install can corrupt user files.
- Automation location: package tests.

### T27. Force does not replace arbitrary user files

- Covers: R42-R44, unrelated-file edge case
- Level: integration
- Fixture/setup: same as T26, with `--force`
- Steps:
  - Run local archive init with `--force`.
  - Assert arbitrary user files are not replaced.
  - Assert any allowed force behavior is limited to documented generated outputs identifiable by the current install plan.
- Expected result: `--force` remains narrow in the first slice.
- Failure proves: `--force` bypasses the safety model.
- Automation location: package tests.

### T28. Package contents do not create publication behavior

- Covers: R76-R79, AC10
- Level: contract
- Fixture/setup: package files
- Steps:
  - Assert no release workflow or package script performs public npm publication.
  - Assert package files do not bundle adapter archives or generated adapter skill bodies as canonical source.
  - Assert docs or package notes preserve the public-publication blocker when package documentation is added.
- Expected result: package creation does not imply public npm publication.
- Failure proves: first-slice implementation exceeds release authority.
- Automation location: package tests and selected CI; manual package metadata review.

### T29. Release metadata shape and pass result are validated

- Covers: R51-R55, R61b, E4
- Level: unit
- Fixture/setup: valid and invalid metadata fixtures
- Steps:
  - Validate metadata with required release, metadata, artifacts, and validation fields.
  - Assert wrong source repository is rejected.
  - Assert missing or non-Codex artifact selection is rejected.
  - Assert Codex install root other than `.agents/skills` is rejected.
  - Assert `validation.result` other than `pass` is rejected.
- Expected result: only official passing Codex metadata can drive installation.
- Failure proves: untrusted or failing release metadata can install.
- Automation location: package metadata validation tests.

### T30. Archive traversal paths are rejected

- Covers: R46, R47, R60, R61c, archive traversal edge cases
- Level: integration, security
- Fixture/setup: malicious archive fixtures with `../`, absolute path, drive-letter path, empty path, and paths outside `.agents/skills`
- Steps:
  - Run local archive init for each malicious archive.
  - Assert status `error` and exit code `3`.
  - Assert no files are written outside the target root or expected install root.
- Expected result: archive extraction is confined.
- Failure proves: archive install can write arbitrary paths.
- Automation location: package security tests.

### T31. Archive entries must remain under `.agents/skills`

- Covers: R47, archive outside-root edge case
- Level: integration, security
- Fixture/setup: archive fixture with safe-looking relative paths that resolve outside the install root contract
- Steps:
  - Run local archive init.
  - Assert status `error`, exit code `3`, and an error naming install-root verification.
- Expected result: archive content cannot target unsupported roots.
- Failure proves: Codex adapter install root is not enforced.
- Automation location: package tests.

### T32. Partial installation failures are reported

- Covers: R48
- Level: integration
- Fixture/setup: mocked writer or permission-denied fixture after scaffold write and before adapter write
- Steps:
  - Trigger a controlled write failure.
  - Assert output identifies whether scaffold files, adapter files, or both may have been written.
  - Assert the failure is not reported as success.
- Expected result: partial state is visible for recovery.
- Failure proves: users cannot recover from failed init safely.
- Automation location: package tests.

### T33. Symlink archive entries are rejected

- Covers: R46, symlink edge case
- Level: integration, security
- Fixture/setup: ZIP fixture containing a symlink entry or platform-equivalent metadata
- Steps:
  - Run local archive init.
  - Assert status `error` and exit code `3`.
  - Assert no symlink is written.
- Expected result: symlink writes are not allowed.
- Failure proves: archive extraction can escape path checks indirectly.
- Automation location: package tests.

### T34. Archive verification failures use exit code 3

- Covers: R60, R61c, AC8
- Level: integration
- Fixture/setup: archive fixtures for checksum mismatch, size mismatch, bundled metadata-hash mismatch, metadata schema invalid, tree-hash mismatch, and path traversal
- Steps:
  - Run init for each fixture.
  - Assert status `error` and exit code `3`.
  - Assert the output names the failed verification step.
- Expected result: expected verification failures are not internal errors.
- Failure proves: CI cannot classify archive verification failures.
- Automation location: package tests.

### T35. Multiple-adapter metadata selects only Codex

- Covers: R53, multiple-adapter edge case
- Level: unit, integration
- Fixture/setup: metadata fixture listing Codex, Claude, and opencode artifacts
- Steps:
  - Run metadata selection for `--adapter codex`.
  - Assert only the Codex artifact is selected.
  - Assert no Claude or opencode files are planned or written.
- Expected result: metadata breadth does not widen first-slice adapter support.
- Failure proves: non-Codex adapters can leak into init.
- Automation location: package metadata tests.

### T36. Metadata source repository is official

- Covers: R52
- Level: unit
- Fixture/setup: metadata fixture with `release.source_repository: attacker/rigorloop`
- Steps:
  - Validate metadata.
  - Assert it is rejected with status `blocked` or validation failure according to the command path.
- Expected result: unofficial metadata is rejected.
- Failure proves: network or bundled metadata can be spoofed.
- Automation location: package metadata tests.

### T37. Metadata install root must be `.agents/skills`

- Covers: R54
- Level: unit
- Fixture/setup: metadata fixture with Codex artifact install root `.codex/skills`
- Steps:
  - Validate metadata.
  - Assert it is rejected.
- Expected result: `.codex/skills` is never accepted as public adapter source or install root.
- Failure proves: local runtime state can become public install behavior.
- Automation location: package metadata tests.

### T38. Metadata validation result must pass

- Covers: R55
- Level: unit
- Fixture/setup: metadata fixture with `validation.result: fail`
- Steps:
  - Validate metadata.
  - Assert it is rejected.
- Expected result: known failing release artifacts cannot install.
- Failure proves: release validation evidence is ignored.
- Automation location: package tests.

### T39. Archive SHA-256 and size are checked before extraction

- Covers: R56, R57
- Level: integration, security
- Fixture/setup: matching archive, wrong SHA fixture, wrong size metadata fixture; extraction spy
- Steps:
  - Run init with wrong SHA metadata and assert extraction is not called.
  - Run init with wrong size metadata and assert extraction is not called.
  - Assert both return status `error` and exit code `3`.
- Expected result: invalid archives are rejected before extraction.
- Failure proves: unsafe content can be processed before verification.
- Automation location: package tests.

### T40. Missing metadata and unknown adapter failures are blocked

- Covers: R61, R61a, R61b, AC7
- Level: integration
- Fixture/setup: missing bundled metadata, metadata without Codex artifact, unsupported adapter command
- Steps:
  - Run each command path.
  - Assert status `blocked` and exit code `2`.
  - Assert blocker codes include `metadata-unavailable` or `adapter-unknown` where specified.
- Expected result: recoverable missing-decision/source cases are blockers.
- Failure proves: expected blockers are treated as internal errors or successes.
- Automation location: package tests.

### T41. Lockfile is never durably written

- Covers: R62-R67, AC5, E7
- Level: integration
- Fixture/setup: temporary empty project and project with existing `rigorloop.lock`
- Steps:
  - Run dry-run init and successful actual init.
  - Assert JSON includes `planned_lockfile` when metadata or install planning is available.
  - Assert actual init emits warning code `lockfile-spec-not-approved` when planned lockfile content is available.
  - Assert no new `rigorloop.lock` is created.
  - Assert an existing `rigorloop.lock` is not modified.
- Expected result: planned lockfile content is output only.
- Failure proves: the first package creates durable truth before a lockfile spec.
- Automation location: package tests.

### T42. Tree hash uses normalized sorted manifest

- Covers: R68-R75, E5
- Level: unit
- Fixture/setup: generated output fixture with multiple text files, nested paths, CRLF content, BOM content, and binary file
- Steps:
  - Compute expected per-file hashes from normalized bytes.
  - Build the canonical manifest string with sorted relative POSIX paths and tab separators.
  - Assert `tree_sha256` equals SHA-256 of the UTF-8 manifest.
- Expected result: `rigorloop-tree-hash-v1` is deterministic across platforms.
- Failure proves: lockfile planning and metadata verification can drift.
- Automation location: package tree-hash tests.

### T43. Tree hash excludes unsupported filesystem entries

- Covers: R68-R72
- Level: unit, security
- Fixture/setup: generated output fixture with directories, symlink, temp file, and regular files
- Steps:
  - Assert regular files are included.
  - Assert directories, symlinks, temporary files, absolute paths, metadata fields, and any lockfile path are excluded or rejected as specified.
- Expected result: tree hash covers generated files only.
- Failure proves: environment-specific metadata affects verification.
- Automation location: package tests.

### T44. Installed tree hash mismatch fails

- Covers: R58, R59, R61c
- Level: integration
- Fixture/setup: valid archive with metadata containing a different `tree_sha256`
- Steps:
  - Run local archive init.
  - Assert status `error`, exit code `3`, and an error naming tree-hash verification.
- Expected result: extracted output must match release metadata.
- Failure proves: archive contents can differ from validated metadata.
- Automation location: package tests.

### T45. Generated adapter files are not canonical package source

- Covers: R78, R79, source-of-truth invariants
- Level: contract
- Fixture/setup: package source tree and built package file list
- Steps:
  - Assert package source does not include generated adapter skill bodies as canonical source files.
  - Assert bundled metadata is metadata only, not adapter archive contents.
  - Assert tests do not use `.codex/skills` as the install source.
- Expected result: npm remains a CLI delivery channel, not the skill source of truth.
- Failure proves: source-boundary discipline regressed.
- Automation location: package tests and selected CI review.

### T46. Final selected CI includes lifecycle and package proof

- Covers: AC1-AC11
- Level: smoke, integration
- Fixture/setup: completed implementation branch
- Steps:
  - Run `npm test --prefix packages/rigorloop` or the equivalent package test command recorded by implementation.
  - Run selected CLI smoke commands for help, version, dry-run JSON, and local archive init.
  - Run `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path specs/rigorloop-cli-package-and-codex-init.md --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml`.
  - Run `git diff --check -- <touched paths>`.
- Expected result: final local proof covers package behavior and lifecycle artifacts.
- Failure proves: implementation cannot be reviewed or verified as a coherent slice.
- Automation location: package tests, selected CI, final verify.

## Fixtures and data

- Package tests should live under `packages/rigorloop` with fixtures in a package-local fixture directory unless implementation chooses a documented repository fixture convention.
- CLI integration tests must create temporary project roots and must not write into the repository root.
- Archive fixtures must be minimal and safe to track. They should include:
  - matching Codex archive fixture;
  - wrong SHA fixture or metadata fixture;
  - wrong size metadata fixture;
  - wrong tree hash metadata fixture;
  - traversal archive fixtures;
  - symlink archive fixture;
  - metadata-unavailable fixture;
  - incompatible release fixture.
- Bundled metadata fixtures must include the official-compatible `v0.1.3` shape required by the spec and negative variants for source repository, adapter name, install root, validation result, missing metadata, and multiple adapters.
- Tests must use temporary directories for extraction and must assert no writes outside the target project.

## Mocking/stubbing policy

- Network access must be stubbed in automated tests. No test should require live GitHub release availability.
- Filesystem writes should use temporary directories, with writer or extraction seams mocked only when needed to force partial-failure paths.
- Package version discovery may use package metadata fixtures for missing-version and prerelease-version cases.
- Archive checksum and tree-hash tests should use deterministic fixture files rather than snapshots of broad generated output.
- Snapshot assertions are allowed only for narrow stable strings. Behavioral requirements must assert fields, exit codes, files, hashes, and blockers directly.

## Migration or compatibility tests

- Existing repository scripts, adapter generation commands, release checks, and `dist/adapters/README.md` install guidance must continue to exist; this slice does not remove them.
- Tests must prove the package does not publish to npm and does not introduce public publication automation.
- Tests must prove the package does not create or modify `rigorloop.lock`.
- Tests must prove existing documented release-archive installation remains possible without using the CLI by not deleting or rewriting the adapter support surface.
- Rollback before public publication is covered by keeping the package isolated under `packages/rigorloop` and avoiding repository-wide dependency on the package for existing validation.

## Observability verification

- JSON output must include action and artifact lists sufficient to reconstruct planned or completed mutations.
- Human init output must summarize created, skipped, blocked, and warning items.
- Verification failures must name the failed step: metadata, archive checksum, archive size, path safety, symlink, install root, or tree hash.
- Debug output must not print large adapter file bodies by default.
- Commands must not claim hosted CI, release validation, workflow validation, branch readiness, PR readiness, or lockfile authority unless the owning stage or validation actually ran.

## Security/privacy verification

- Archive extraction must reject traversal, absolute paths, drive-letter paths, empty paths, symlink entries, and paths outside `.agents/skills`.
- Network mode must use bundled official metadata and fetch only official adapter archives for the requested Codex adapter.
- The command must not require secrets or credentials.
- The command must not print environment secrets or config secrets.
- The command must not send project file contents over the network.
- Tests must include at least one assertion that no `.codex/skills` path is used as adapter source or install root.

## Performance checks

- Dry-run planning for an empty target must not download an adapter archive when metadata is enough for planning.
- Actual init tests should assert the implementation reads or hashes only the target scaffold paths and extracted adapter output where feasible through test seams or documented code review evidence.
- Archive processing tests should avoid asserting a specific implementation strategy, but must confirm large file bodies are not emitted in routine output.

## Manual QA checklist

- Inspect `rigorloop --help` text for concise human readability.
- Inspect one successful human `init --adapter codex --from-archive <fixture>` output for clear created/skipped/warning sections.
- Inspect one overwrite-refusal error for a useful next action.
- Confirm no docs or package metadata imply public npm publication has happened.

## What not to test

- Do not test `rigorloop new-change`, `rigorloop status`, or `rigorloop validate`; they are out of scope.
- Do not test durable `rigorloop.lock` update semantics beyond proving the first slice does not write it.
- Do not test workflow YAML, generated workflow docs, frozen drift checks, or non-Codex adapters.
- Do not test public npm trusted publishing or provenance in this slice.
- Do not port or re-test all repository Python validators through the CLI.
- Do not use live GitHub release availability as the only proof for network mode.

## Uncovered gaps

None that require returning to spec or architecture before implementation.

The exact package test command is expected to become `npm test --prefix packages/rigorloop` or an equivalent package-local command chosen during M1. If implementation chooses a different package runner, update this test spec and plan validation notes before relying on it for implementation closeout.

## Next artifacts

- Implementation of M1 from `docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md`.
- Code-review for each completed implementation milestone.

## Follow-on artifacts

None yet.

## Readiness

This test spec is active and ready to guide implementation.

Immediate next stage: implement M1.

Implementation readiness is limited to M1 first; M2 and M3 remain planned until earlier milestones are implemented, reviewed, and closed according to the active plan.
