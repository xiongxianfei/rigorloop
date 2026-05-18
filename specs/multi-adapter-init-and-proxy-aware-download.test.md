# Multi-Adapter Init and Proxy-Aware Adapter Download Test Spec

## Status

active

## Related spec and plan

- Spec: [Multi-Adapter Init and Proxy-Aware Adapter Download](multi-adapter-init-and-proxy-aware-download.md), approved.
- Plan: [Multi-adapter init and proxy-aware adapter download](../docs/plans/2026-05-18-multi-adapter-init-and-proxy-aware-download.md), active and approved by `plan-review-r1`.
- Proposal: [Multi-Adapter Init and Proxy-Aware Adapter Download](../docs/proposals/2026-05-18-multi-adapter-init-and-proxy-aware-download.md), accepted.
- Architecture: [RigorLoop Canonical System Architecture](../docs/architecture/system/architecture.md), approved.
- ADR: [ADR-20260518-multi-adapter-init-and-proxy-download](../docs/adr/ADR-20260518-multi-adapter-init-and-proxy-download.md), accepted.
- Change metadata: [change.yaml](../docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/change.yaml).
- Review records:
  - `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/reviews/spec-review-r2.md`
  - `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/reviews/spec-review-r3.md`
  - `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/reviews/architecture-review-r1.md`
  - `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/reviews/plan-review-r1.md`

## Testing strategy

This change expands a public filesystem-mutating CLI command, lockfile schema, release-archive trust boundary, and proxy diagnostic surface. Proof must be automated, fixture-backed, and hermetic.

- Unit and contract tests cover adapter descriptor selection, official URL validation, bundled metadata schema, lockfile schema v1/v2 parsing, deterministic serialization, tree-hash calculation, and safe diagnostic classification.
- Integration tests execute `packages/rigorloop` in temporary project directories and assert stdout, stderr, exit codes, JSON envelope fields, human output, filesystem writes, no-write dry-run behavior, manifest writes, lockfile writes, and unchanged unrelated project state.
- Archive tests use small fixture ZIP files and bundled metadata fixtures for Codex, Claude Code, opencode with commands, and older opencode skills-only archives. They must prove archive verification happens before extraction and lockfile writes.
- Network tests use mocked `fetch` or local fixture server behavior only. Normal tests must not require live GitHub, live proxies, or external internet.
- Generated adapter validation uses temporary output from canonical `skills/` and approved adapter templates when metadata, archive content, adapter generation, or release archive behavior changes.
- Selected CI must include the package tests, this test spec, active plan, change metadata, review artifacts, and all touched `packages/rigorloop` and adapter-generation paths.

## Requirement coverage map

| Requirement | Coverage |
|---|---|
| MAI-R1-MAI-R6 | TMAI-001, TMAI-002, TMAI-003, TMAI-024 |
| MAI-R7-MAI-R16 | TMAI-001, TMAI-002, TMAI-004, TMAI-005, TMAI-006, TMAI-030 |
| MAI-R17-MAI-R28 | TMAI-003, TMAI-004, TMAI-005, TMAI-006, TMAI-007, TMAI-008, TMAI-009, TMAI-010, TMAI-011, TMAI-012 |
| MAI-R29-MAI-R38 | TMAI-008, TMAI-009, TMAI-010, TMAI-011, TMAI-012, TMAI-013 |
| MAI-R39-MAI-R46c | TMAI-006, TMAI-014, TMAI-015, TMAI-016, TMAI-030 |
| MAI-R47-MAI-R54 | TMAI-017, TMAI-018, TMAI-019, TMAI-020, TMAI-023, TMAI-027 |
| MAI-R55-MAI-R68 | TMAI-021, TMAI-022, TMAI-023, TMAI-024, TMAI-027 |
| MAI-R69-MAI-R76 | TMAI-025, TMAI-026, TMAI-027, TMAI-028 |
| MAI-R77-MAI-R85 | TMAI-029, TMAI-030, TMAI-031, TMAI-032 |
| MAI-R86-MAI-R91 | TMAI-002, TMAI-020, TMAI-021, TMAI-029, TMAI-033 |
| MAI-R92-MAI-R95 | TMAI-034 |

## Example coverage map

| Example | Coverage |
|---|---|
| E1 | TMAI-004, TMAI-017, TMAI-021 |
| E2 | TMAI-005, TMAI-017, TMAI-021 |
| E3 | TMAI-006, TMAI-014, TMAI-017, TMAI-022 |
| E4 | TMAI-007, TMAI-008, TMAI-023 |
| E5 | TMAI-009 |
| E6 | TMAI-022, TMAI-025 |
| E7 | TMAI-015, TMAI-016, TMAI-023 |
| E8 | TMAI-029, TMAI-030, TMAI-031, TMAI-032 |
| E9 | TMAI-020 |

## Edge case coverage

| Edge case | Coverage |
|---|---|
| Existing `rigorloop.yaml` lists Codex only; adding Claude updates adapter list without removing Codex | TMAI-018 |
| Existing schema v1 Codex lockfile matches installed tree; adding opencode upgrades to schema v2 | TMAI-025 |
| Existing schema v1 Codex lockfile has drift; adding another adapter blocks before mutation | TMAI-026 |
| Existing schema v2 with Codex and Claude; adding opencode preserves both | TMAI-027 |
| Existing `.opencode/skills` is a file | TMAI-013 |
| Existing `.opencode/commands` contains unrelated files | TMAI-013 |
| Metadata declares command alias but archive omits one | TMAI-014 |
| Older opencode metadata lacks command aliases | TMAI-015, TMAI-016 |
| Local archive basename matches but SHA-256 differs | TMAI-010 |
| Network fetch fails with proxy env vars present | TMAI-029, TMAI-030 |
| Network fetch succeeds but checksum fails | TMAI-010, TMAI-032 |
| `--dry-run --json` for each supported adapter writes nothing | TMAI-020 |
| Unsupported adapter value such as `cursor` | TMAI-003 |
| Package version and adapter release are incompatible | TMAI-012 |
| Unsupported lockfile schema version | TMAI-028 |

## Milestone coverage map

| Milestone | Coverage |
|---|---|
| M1. Adapter descriptors and trusted metadata selection | TMAI-001 through TMAI-012, TMAI-024 |
| M2. Manifest and lockfile schema v2 | TMAI-017 through TMAI-028 |
| M3. Multi-root archive extraction and local archive fallback | TMAI-006 through TMAI-016, TMAI-034 |
| M4. Network download diagnostics and output envelope | TMAI-029 through TMAI-033 |
| M5. Documentation, package proof, and final integration | TMAI-033, TMAI-034, selected CI, final package test command |

## Test cases

### TMAI-001. Descriptor registry defines the exact supported adapter set

- Covers: MAI-R1-MAI-R4, MAI-R7-MAI-R16, AC1
- Level: unit, contract
- Fixture/setup: descriptor registry or exported helper when available; otherwise package CLI fixture metadata for all adapters.
- Steps:
  - Assert supported adapter names are exactly `codex`, `claude`, and `opencode`.
  - Assert Codex archive pattern and `skills: .agents/skills`.
  - Assert Claude archive pattern and `skills: .claude/skills`.
  - Assert opencode archive pattern and possible roots `skills: .opencode/skills` and `commands: .opencode/commands`.
  - Assert all install roots are project-relative POSIX paths.
- Expected result: descriptors match the approved contract and do not include `.codex/skills`.
- Failure proves: command behavior is still constant-driven or has unsupported adapter/path drift.
- Automation location: `packages/rigorloop/test/cli.test.js` or package-local descriptor unit tests.

### TMAI-002. Help and output surfaces do not overclaim unsupported features

- Covers: MAI-R6, MAI-R86-MAI-R91
- Level: integration, smoke
- Fixture/setup: repository-local CLI entrypoint.
- Steps:
  - Run `rigorloop --help`.
  - Assert help includes the three supported `init --adapter` values.
  - Assert help does not imply `rigorloop status`, `rigorloop validate`, workflow YAML generation, generated workflow docs, or Undici dispatcher support.
  - Run a human-mode dry-run and assert routine output is not raw JSON fragments.
- Expected result: public discovery is accurate and output modes remain distinct.
- Failure proves: the CLI claims out-of-scope behavior or mixes human/JSON output.
- Automation location: package CLI tests.

### TMAI-003. Unsupported adapters block before mutation

- Covers: MAI-R4, MAI-R5, AC5
- Level: integration
- Fixture/setup: empty temporary project.
- Steps:
  - Run `rigorloop init --adapter cursor --json`.
  - Assert status `blocked`, exit code `2`, and blocker code `adapter-unknown`.
  - Assert no `rigorloop.yaml`, `rigorloop.lock`, `.agents`, `.claude`, or `.opencode` paths are created.
- Expected result: unsupported adapter values are rejected safely.
- Failure proves: adapter scope leaks beyond the approved set.
- Automation location: package CLI tests.

### TMAI-004. Codex init remains `.agents/skills` only

- Covers: MAI-R1, MAI-R8-MAI-R10, MAI-R17-MAI-R24, AC2, E1
- Level: integration
- Fixture/setup: Codex fixture archive and trusted metadata.
- Steps:
  - Run Codex local archive or mocked-network init.
  - Assert generated files are under `.agents/skills`.
  - Assert `.codex/skills` is not created.
  - Assert metadata-selected archive name is `rigorloop-adapter-codex-<release>.zip`.
- Expected result: Codex behavior remains compatible.
- Failure proves: the implementation introduced the rejected Codex migration.
- Automation location: package CLI tests.

### TMAI-005. Claude Code init installs `.claude/skills`

- Covers: MAI-R2, MAI-R11-MAI-R12, MAI-R17-MAI-R24, AC3, E2
- Level: integration
- Fixture/setup: Claude fixture archive and trusted metadata.
- Steps:
  - Run `rigorloop init --adapter claude --from-archive <fixture> --json`.
  - Assert generated files are under `.claude/skills`.
  - Assert `.agents/skills` and `.opencode` are not created by the Claude install.
  - Assert archive filename and selected URL/metadata identity are Claude-specific.
- Expected result: Claude Code has its own verified single-root install path.
- Failure proves: descriptor selection or expected-root filtering is wrong.
- Automation location: package CLI tests.

### TMAI-006. opencode init installs skills and declared command aliases

- Covers: MAI-R3, MAI-R13-MAI-R14a, MAI-R21-MAI-R21d, MAI-R39-MAI-R43, AC4, E3
- Level: integration
- Fixture/setup: opencode fixture archive with `.opencode/skills` and `.opencode/commands`, trusted metadata with `command_aliases.opencode`.
- Steps:
  - Run `rigorloop init --adapter opencode --from-archive <fixture> --json`.
  - Assert skill files exist under `.opencode/skills`.
  - Assert each declared alias file exists under `.opencode/commands`.
  - Assert JSON actions/artifacts report both root roles.
- Expected result: opencode declared aliases are installed and verified.
- Failure proves: multi-root opencode support is incomplete.
- Automation location: package CLI tests.

### TMAI-007. Local archive mode works for all supported adapters without user metadata

- Covers: MAI-R18, MAI-R25-MAI-R27, AC7, E4
- Level: integration
- Fixture/setup: matching local archives and trusted metadata for Codex, Claude, and opencode.
- Steps:
  - Run `--from-archive` install for each supported adapter.
  - Assert no metadata path option is required or accepted as part of the install.
  - Assert each archive is verified against bundled trusted metadata.
- Expected result: local archive mode changes delivery path only, not trust root.
- Failure proves: the CLI trusts user metadata or leaves adapters without offline fallback.
- Automation location: package CLI tests.

### TMAI-008. Official network URL selection is exact

- Covers: MAI-R17, MAI-R19-MAI-R24, AC6
- Level: unit, integration
- Fixture/setup: trusted metadata and mocked fetch helper.
- Steps:
  - Run network init for each supported adapter with mocked fetch.
  - Assert fetch is called with exactly the trusted public archive URL.
  - Inject a URL mismatch and assert status `error`, exit code `3`, and `non-official-archive-url`.
- Expected result: network installs never fetch untrusted archive URLs.
- Failure proves: official URL validation can be bypassed.
- Automation location: package URL helper and CLI tests.

### TMAI-009. Wrong archive for selected adapter fails before extraction

- Covers: MAI-R27-MAI-R28, MAI-R38, AC8, E5
- Level: integration
- Fixture/setup: Codex archive used with `--adapter claude`; temporary project.
- Steps:
  - Run `rigorloop init --adapter claude --from-archive ./rigorloop-adapter-codex-<release>.zip --json`.
  - Assert status `error`, exit code `3`, and adapter/archive mismatch code.
  - Assert no Claude root, manifest entry, or lockfile entry is written.
- Expected result: selected adapter identity is enforced before extraction.
- Failure proves: local archive fallback can install the wrong generated output.
- Automation location: package CLI tests.

### TMAI-010. Archive checksum and size failures block before mutation

- Covers: MAI-R29-MAI-R30, MAI-R37-MAI-R38, AC8
- Level: integration
- Fixture/setup: fixture archives with modified bytes or metadata size mismatch.
- Steps:
  - Run local archive install with SHA mismatch.
  - Run install with size mismatch when `size_bytes` is present.
  - Assert status `error`, exit code `3`, and no adapter root or lockfile success entry.
- Expected result: archive bytes are trusted only after verification.
- Failure proves: extraction or lockfile write can happen from unverified bytes.
- Automation location: package CLI tests.

### TMAI-011. Archive path traversal, unsafe paths, and symlinks are rejected

- Covers: MAI-R31-MAI-R32, MAI-R37-MAI-R38, AC8
- Level: integration, security
- Fixture/setup: ZIP entries with absolute paths, parent traversal, empty paths, drive-letter paths, unsupported symlinks, and paths outside expected roots.
- Steps:
  - Run install for each unsafe archive fixture.
  - Assert status `error`, exit code `3`.
  - Assert no outside file is created and no lockfile entry claims success.
- Expected result: extraction remains confined to expected adapter roots.
- Failure proves: archive extraction can escape project boundaries.
- Automation location: package CLI tests.

### TMAI-012. Metadata validation result, metadata hash, and release compatibility are enforced

- Covers: MAI-R19, MAI-R22, MAI-R33, MAI-R37
- Level: integration
- Fixture/setup: release index with mismatched bundled metadata hash, unavailable adapter metadata, incompatible package/release, and `validation.result != pass`.
- Steps:
  - Run init against each metadata fixture.
  - Assert unavailable metadata blocks with exit code `2` and `metadata-unavailable`.
  - Assert invalid metadata hash/schema or failed validation returns the specified error class before extraction.
- Expected result: bundled metadata is verified before archive bytes are trusted.
- Failure proves: CLI metadata trust root can be bypassed.
- Automation location: package CLI tests.

### TMAI-013. Existing root conflicts and unrelated files block safely

- Covers: MAI-R31-MAI-R38, edge cases 5 and 6
- Level: integration
- Fixture/setup: project with `.opencode/skills` as a file; project with `.opencode/commands` containing unrelated files.
- Steps:
  - Run opencode init.
  - Assert mutation conflict exit code `5` or the existing mutation-conflict contract.
  - Assert unrelated files remain unchanged and no lockfile success entry is written.
- Expected result: adapter install does not overwrite user files.
- Failure proves: generated output can destroy unrelated project state.
- Automation location: package CLI tests.

### TMAI-014. Missing declared opencode command alias fails verification

- Covers: MAI-R21d, MAI-R40-MAI-R43, AC4, edge case 7
- Level: integration
- Fixture/setup: opencode metadata declaring two aliases; archive omits one alias.
- Steps:
  - Run opencode install.
  - Assert status `error`, exit code `3`.
  - Assert the command does not claim success or write a lockfile entry with `commands`.
- Expected result: declared opencode command aliases are mandatory.
- Failure proves: opencode can silently become skills-only despite metadata declaring commands.
- Automation location: package CLI tests.

### TMAI-015. Older opencode archive installs skills-only with warning

- Covers: MAI-R21e-MAI-R21f, MAI-R44-MAI-R46c, AC4, E7
- Level: integration
- Fixture/setup: trusted metadata for an explicitly compatible older opencode skills-only archive with no `command_aliases.opencode`.
- Steps:
  - Run opencode install.
  - Assert status success or warning according to the envelope.
  - Assert warning code `opencode-command-aliases-not-declared`.
  - Assert `.opencode/skills` exists and `.opencode/commands` does not.
- Expected result: older compatible archives work without pretending aliases exist.
- Failure proves: old archive compatibility is either broken or misleading.
- Automation location: package CLI tests.

### TMAI-016. Older opencode warning text does not imply slash-command availability

- Covers: MAI-R45, MAI-R46a-MAI-R46c
- Level: integration, UX
- Fixture/setup: same as TMAI-015.
- Steps:
  - Capture JSON warnings and human warning output.
  - Assert warning code is stable.
  - Assert output does not say command aliases or slash commands were installed.
- Expected result: reduced runtime surface is explicit.
- Failure proves: users can be misled about opencode command aliases.
- Automation location: package CLI tests.

### TMAI-017. Successful init writes correct `rigorloop.yaml` root shape

- Covers: MAI-R47-MAI-R53, AC9
- Level: integration
- Fixture/setup: clean project and successful installs for Codex, Claude, opencode with commands, and older opencode skills-only.
- Steps:
  - Run each install in a temp project.
  - Assert Codex and Claude entries use `install_root`.
  - Assert opencode with commands uses `install_roots.skills` and `install_roots.commands`.
  - Assert older opencode omits `install_roots.commands`.
  - Assert source type is `release-archive` or `local-archive` as appropriate.
- Expected result: manifest shape mirrors root cardinality and installed roots.
- Failure proves: project manifest cannot describe installed adapters reliably.
- Automation location: package CLI tests.

### TMAI-018. Existing valid manifest entries are preserved and selected entry is updated only

- Covers: MAI-R51f-MAI-R51g
- Level: integration
- Fixture/setup: existing valid `rigorloop.yaml` with Codex; add Claude or opencode.
- Steps:
  - Run init for another adapter.
  - Assert existing unrelated adapter entry remains.
  - Assert only selected adapter source/package fields are added or updated.
- Expected result: multi-adapter manifest updates are non-destructive.
- Failure proves: adding an adapter can remove valid project configuration.
- Automation location: package CLI tests.

### TMAI-019. Invalid or duplicate manifest state blocks before mutation

- Covers: MAI-R51h-MAI-R51i
- Level: integration
- Fixture/setup: duplicate selected adapter entries, unsupported manifest schema, malformed adapter entry, or unsupported selected adapter shape.
- Steps:
  - Run init with valid archive.
  - Assert status `blocked`, exit code `2`, and matching blocker code such as `duplicate-adapter-entry`.
  - Assert no adapter root or lockfile mutation occurs.
- Expected result: unsafe manifest merge cases are explicit blockers.
- Failure proves: CLI can silently rewrite ambiguous project configuration.
- Automation location: package CLI tests.

### TMAI-020. Dry-run JSON plans all roots and lockfile content without mutation

- Covers: MAI-R56, MAI-R88, MAI-R91, E9
- Level: integration
- Fixture/setup: clean project and metadata for each supported adapter.
- Steps:
  - Run `rigorloop init --adapter <adapter> --dry-run --json` for Codex, Claude, opencode with commands, and older opencode skills-only.
  - Assert JSON stdout only.
  - Assert planned roots and planned lockfile content match metadata.
  - Assert no files are created.
- Expected result: dry-run is accurate and non-mutating.
- Failure proves: planning output cannot be trusted or dry-run mutates state.
- Automation location: package CLI tests.

### TMAI-021. Successful single-root installs write schema v2 lockfile entries

- Covers: MAI-R55-MAI-R61, MAI-R64-MAI-R68, AC10, AC11
- Level: integration
- Fixture/setup: successful Codex and Claude installs.
- Steps:
  - Run installs and read `rigorloop.lock`.
  - Assert `schema_version: 2`.
  - Assert Codex uses `installed_root: ".agents/skills"`.
  - Assert Claude uses `installed_root: ".claude/skills"`.
  - Assert each single-root entry includes `tree_sha256` and `file_count`.
- Expected result: single-root entries remain explicit under schema v2.
- Failure proves: schema v2 breaks Codex compatibility or Claude recording.
- Automation location: package CLI and lockfile tests.

### TMAI-022. opencode schema v2 lockfile uses per-root hashes

- Covers: MAI-R57-MAI-R63, MAI-R65-MAI-R68, AC11, E6
- Level: integration, contract
- Fixture/setup: opencode archive with skills and commands.
- Steps:
  - Run opencode install.
  - Assert lockfile entry uses `installed_roots` and `root_hashes`.
  - Assert `root_hashes.skills` and `root_hashes.commands` include `tree_sha256` and `file_count`.
  - Assert no top-level `tree_sha256` or `file_count` appears in the opencode entry.
- Expected result: multi-root lockfile semantics are per-root.
- Failure proves: opencode generated output cannot be verified per surface.
- Automation location: package CLI and lockfile tests.

### TMAI-023. Local archive records basename only in manifest and lockfile

- Covers: MAI-R53-MAI-R54, MAI-R66-MAI-R68, AC9
- Level: integration, security
- Fixture/setup: local archives supplied from absolute temp paths containing username-like path segments.
- Steps:
  - Run local archive installs.
  - Assert `rigorloop.yaml` and `rigorloop.lock` record source type and archive basename only.
  - Assert no absolute paths, usernames, hostnames, proxy URLs, credentials, tokens, temporary directories, or raw environment values appear.
- Expected result: durable project files are portable and privacy-safe.
- Failure proves: local machine details leak into committed project state.
- Automation location: package CLI tests.

### TMAI-024. Lockfile parser accepts schema v2 and rejects unsupported shapes

- Covers: MAI-R57-MAI-R65, MAI-R72-MAI-R73
- Level: unit, contract
- Fixture/setup: valid v2 fixtures for single-root, multi-root, and skills-only opencode; invalid fixtures with unknown fields and unsupported algorithm/source.
- Steps:
  - Parse valid fixtures and assert normalized object shape.
  - Parse invalid fixtures and assert unsupported or invalid lockfile result.
  - Serialize valid fixtures twice and assert deterministic output sorted by adapter name.
- Expected result: lockfile v2 is strict and deterministic.
- Failure proves: durable lockfile state can drift, lose data, or accept unknown semantics.
- Automation location: package lockfile tests.

### TMAI-025. Valid schema v1 Codex lockfile can upgrade to schema v2 after drift check

- Covers: MAI-R69-MAI-R70, MAI-R76, AC12, E6
- Level: integration, migration
- Fixture/setup: project with valid schema v1 Codex lockfile and `.agents/skills` matching recorded tree hash.
- Steps:
  - Add Claude or opencode.
  - Assert existing Codex output is checked before mutation.
  - Assert resulting lockfile is schema v2 and retains the Codex entry.
- Expected result: existing valid Codex projects can adopt multi-adapter support.
- Failure proves: migration breaks compatibility or skips drift protection.
- Automation location: package CLI tests.

### TMAI-026. Drifted schema v1 Codex lockfile blocks unrelated adapter addition

- Covers: MAI-R71, AC13
- Level: integration, migration
- Fixture/setup: schema v1 Codex lockfile with mutated, missing, or conflicting `.agents/skills`.
- Steps:
  - Run Claude or opencode init.
  - Assert status `blocked` before new adapter extraction.
  - Assert no unrelated adapter entry is added.
- Expected result: drifted existing generated output blocks destructive replacement.
- Failure proves: unrelated adapter init can hide or overwrite drift.
- Automation location: package CLI tests.

### TMAI-027. Existing schema v2 entries are preserved

- Covers: MAI-R59, MAI-R72-MAI-R76
- Level: integration
- Fixture/setup: schema v2 lockfile with valid Codex and Claude entries.
- Steps:
  - Add opencode.
  - Assert Codex and Claude entries remain valid and sorted.
  - Assert unrelated valid adapter entries are not mutated except required manifest hash/wrapper updates.
- Expected result: schema v2 multi-adapter updates are additive and deterministic.
- Failure proves: adapter init rewrites unrelated durable state.
- Automation location: package CLI tests.

### TMAI-028. Re-run and source-mode changes behave predictably

- Covers: MAI-R74-MAI-R75
- Level: integration
- Fixture/setup: adapter already installed and matching lockfile; same archive available through local and mocked network modes.
- Steps:
  - Re-run init for the same adapter and assert unchanged reporting is allowed.
  - Reinstall through a different delivery mode after verification.
  - Assert `source` may update only after archive and installed tree verification succeeds.
- Expected result: idempotence and source changes are explicit.
- Failure proves: re-runs produce unnecessary or unsafe mutations.
- Automation location: package CLI tests.

### TMAI-029. Network failure reports bounded proxy diagnostics

- Covers: MAI-R77, MAI-R79-MAI-R84, AC14, E8
- Level: integration, observability, security
- Fixture/setup: mocked fetch failure; environment contains allowlisted proxy variables with sensitive-looking values.
- Steps:
  - Run network init with `--json`.
  - Assert status `blocked`, exit code `2` when fallback remains valid.
  - Assert diagnostics include adapter name, release version, `archive_url`, `download_failure_class`, `node_env_proxy_status`, and `proxy_env_vars_detected`.
  - Assert `proxy_env_vars_detected` contains names only.
  - Assert fallback guidance mentions `--from-archive`.
- Expected result: users get actionable, safe recovery diagnostics.
- Failure proves: proxy diagnostics are missing or leak sensitive values.
- Automation location: package CLI tests with mocked fetch.

### TMAI-030. Proxy diagnostic enums and env-var allowlist are stable

- Covers: MAI-R81-MAI-R82e, MAI-R83, AC14
- Level: unit, contract
- Fixture/setup: diagnostic helper inputs with uppercase/lowercase proxy env names and unrelated env names.
- Steps:
  - Assert detected names are limited to `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`, `http_proxy`, `https_proxy`, `no_proxy`.
  - Assert `node_env_proxy_status` is one of `enabled`, `disabled`, `unsupported`, or `unknown`.
  - Assert unknown runtime support maps to `unknown`.
  - Assert `download_failure_class` is one of the approved enum values.
- Expected result: diagnostics are testable and bounded.
- Failure proves: output can become unstable or sensitive.
- Automation location: package helper or CLI tests.

### TMAI-031. Human proxy failure output is actionable and redacted

- Covers: MAI-R79-MAI-R84, MAI-R89-MAI-R90
- Level: integration, UX, security
- Fixture/setup: mocked network failure and sensitive proxy env values.
- Steps:
  - Run network init without `--json`.
  - Assert output states selected adapter, release, trusted public archive URL, failure class, and `--from-archive` next action.
  - Assert output does not include raw proxy URLs, credentials, private hostnames, access tokens, usernames, temp directories, raw env values, or request headers.
- Expected result: human recovery guidance is useful and privacy-safe.
- Failure proves: enterprise diagnostics can leak sensitive information.
- Automation location: package CLI tests.

### TMAI-032. Proxy diagnostics do not mask verification failures

- Covers: MAI-R85, edge case 11
- Level: integration
- Fixture/setup: mocked fetch success that returns archive bytes with checksum mismatch.
- Steps:
  - Run network init with proxy env variables present.
  - Assert failure is archive verification error with exit code `3`, not proxy/network blocked status.
  - Assert no lockfile success entry is written.
- Expected result: proxy diagnostics do not weaken archive verification.
- Failure proves: network recovery handling can hide integrity failures.
- Automation location: package CLI tests.

### TMAI-033. Existing JSON, quiet, debug, no-color, and `NO_COLOR` behavior is preserved

- Covers: MAI-R86-MAI-R91
- Level: integration, contract
- Fixture/setup: dry-run and successful fixture installs.
- Steps:
  - Assert JSON output uses the stable envelope.
  - Assert `--quiet` does not suppress JSON.
  - Assert `--debug` puts extra fields under diagnostics without breaking stable fields.
  - Assert `--no-color` and `NO_COLOR` produce no ANSI sequences.
  - Assert successful JSON includes actions/artifacts for adapter output, `rigorloop.yaml`, and `rigorloop.lock`.
- Expected result: multi-adapter init preserves existing CLI output contracts.
- Failure proves: new adapter support regresses automation-facing behavior.
- Automation location: package CLI tests.

### TMAI-034. Generated adapter output is validated from canonical sources when changed

- Covers: MAI-R16, MAI-R46, MAI-R92-MAI-R95, AC16
- Level: contract, smoke
- Fixture/setup: change touches adapter templates, adapter metadata, adapter generation, release archive contents, or canonical public skills.
- Steps:
  - Run `python scripts/build-adapters.py --version <version> --output-dir <tmp-release-output>`.
  - Run `python scripts/validate-adapters.py --version <version> --root <tmp-release-output>`.
  - Assert generated archives include expected roots, metadata, archive hashes, tree hashes, opencode command aliases when declared, and no security scan failures.
  - Assert no hand-edited generated adapter output is used as source.
- Expected result: adapter archive claims are reproducible from canonical `skills/` and templates.
- Failure proves: release archive support can drift from canonical authored sources.
- Automation location: adapter generation/validation scripts and selected CI.

## Fixtures and data

- Extend `packages/rigorloop/test/cli.test.js` fixture helpers to create adapter-specific ZIP archives for:
  - Codex `.agents/skills`.
  - Claude Code `.claude/skills`.
  - opencode `.opencode/skills` plus `.opencode/commands`.
  - older opencode `.opencode/skills` only.
- Extend bundled metadata fixtures to cover:
  - single-root `install_root`, `tree_sha256`, and `file_count`;
  - multi-root `install_roots` and `root_hashes`;
  - `command_aliases.opencode` count and paths;
  - explicit compatible release range for older skills-only opencode metadata;
  - metadata-unavailable, validation-failed, metadata-hash mismatch, release-incompatible, URL mismatch, size mismatch, and checksum mismatch cases.
- Add lockfile fixtures for schema v1 Codex, valid schema v2 mixed entries, older opencode skills-only entries, unknown fields, unsupported schema, unsupported source, unsupported tree hash algorithm, and drifted generated output.

## Mocking/stubbing policy

- Mock `fetch` or use a local fixture server for all network archive tests.
- Do not call live GitHub or require a live proxy in normal tests.
- Proxy tests may set environment variables but must assert only variable names appear in diagnostics.
- Fixture archives must be small, deterministic ZIPs built in test helpers or committed fixtures.
- Do not mock archive verification, path filtering, tree hashing, manifest serialization, or lockfile serialization in tests that claim install success.

## Migration or compatibility tests

- TMAI-004 proves Codex remains `.agents/skills`.
- TMAI-021 proves schema v2 keeps single-root Codex and Claude fields.
- TMAI-025 proves schema v1 Codex lockfiles can upgrade after drift checks pass.
- TMAI-026 proves drifted schema v1 lockfiles block unrelated adapter additions.
- TMAI-027 proves schema v2 preserves unrelated valid adapter entries.
- TMAI-028 proves idempotent re-runs and delivery-mode changes are explicit.

## Observability verification

- JSON output must expose adapter selection, source type, planned or actual roots, lockfile action, warnings, blockers, errors, and diagnostics.
- Human output must state selected adapter, release tag, install root or roots, archive source type, lockfile action, and fallback guidance for network failures.
- Verification failures must identify failure category without printing large file bodies or sensitive values.
- Proxy diagnostics must use stable field names and enum values from TMAI-029 and TMAI-030.

## Security/privacy verification

- TMAI-008 proves only trusted official archive URLs are fetched.
- TMAI-010 through TMAI-012 prove archive and metadata integrity failures block before extraction.
- TMAI-011 proves archive extraction is path-confined and symlink-safe.
- TMAI-023, TMAI-029, TMAI-031, and TMAI-032 prove durable files and diagnostics do not leak local paths, proxy values, credentials, request headers, usernames, hostnames, tokens, or temp directories.

## Performance checks

- No dedicated benchmark is required.
- Archive verification and tree hashing are covered by fixture installs and should remain linear in generated file count.
- Dry-run tests must assert no archive download happens when trusted metadata is sufficient to plan output.
- Proxy diagnostics must not perform extra live network probes beyond the selected official archive download attempt.

## Manual QA checklist

Manual QA is optional after automated tests pass:

- Run `rigorloop init --adapter codex --dry-run`.
- Run `rigorloop init --adapter claude --dry-run`.
- Run `rigorloop init --adapter opencode --dry-run`.
- Inspect human output for concise adapter, release, root, source, and lockfile action wording.
- Do not use manual QA as a substitute for fixture-backed archive, lockfile, or proxy tests.

## What not to test

- Do not test `rigorloop status`, `rigorloop validate`, workflow YAML, or generated workflow docs because they are non-goals.
- Do not test programmatic Undici proxy dispatcher behavior because it is explicitly deferred.
- Do not use live GitHub or live corporate proxy access in normal tests.
- Do not test `.codex/skills` as a Codex install target because the accepted contract preserves `.agents/skills`.
- Do not test npm-bundled adapter archives because archives remain release artifacts, not npm package source.

## Uncovered gaps

None. If implementation discovers that nested manifest or lockfile parsing cannot remain safe with the current no-dependency parser, route back to architecture/spec before adding a new parser dependency or changing durable file shape.

## Next artifacts

- implement M1
- code-review M1 after targeted validation
- repeat implementation and code-review for M2 through M5
- explain-change
- verify
- pr

## Follow-on artifacts

None yet.

## Readiness

Current handoff: `implement M1`.

Implementation must add or update tests before production code when feasible and keep the active plan current as milestones move through implementation and review.
