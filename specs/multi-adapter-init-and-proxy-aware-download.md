# Multi-Adapter Init and Proxy-Aware Adapter Download

## Status

approved

## Related proposal

- [Multi-Adapter Init and Proxy-Aware Adapter Download](../docs/proposals/2026-05-18-multi-adapter-init-and-proxy-aware-download.md)

## Goal and context

This spec defines the next CLI adapter-install contract for:

```bash
rigorloop init --adapter codex
rigorloop init --adapter claude
rigorloop init --adapter opencode
```

It extends the approved Codex-only CLI and lockfile contracts to Claude Code and opencode, while preserving Codex installation under `.agents/skills`. It also defines first-slice proxy-aware download diagnostics for Node `fetch` environments where proxy behavior depends on Node env-proxy support.

When approved, this spec supersedes only the parts of `specs/rigorloop-cli-package-and-codex-init.md` and `specs/rigorloop-cli-lockfile.md` that limit `init` and durable lockfile writes to Codex. The existing archive verification, mutation safety, exit-code envelope, tree-hash algorithm, local archive verification, and source-of-truth boundaries continue to apply unless this spec explicitly extends them.

## Glossary

- `adapter descriptor`: the CLI-owned contract for one supported adapter, including adapter name, archive filename pattern, expected install roots, required roots, and lockfile shape.
- `single-root adapter`: an adapter whose generated output is recorded under one install root, currently Codex and Claude Code.
- `multi-root adapter`: an adapter whose generated output is recorded under more than one install root, currently opencode.
- `runtime install root`: the project-relative directory where verified generated adapter output is extracted for a target tool.
- `trusted adapter metadata`: official adapter release metadata bundled with the installed CLI package and verified before use.
- `declared command aliases`: opencode command alias files listed by trusted metadata for the selected archive.
- `older opencode archive`: an official opencode archive in an accepted release range whose trusted metadata does not contain `command_aliases.opencode`.
- `Node env-proxy support`: Node runtime support for using proxy environment variables with `fetch()` when the runtime has that support enabled.
- `safe proxy fact`: a diagnostic fact that does not expose credentials, raw proxy URLs, private hostnames, tokens, usernames, temporary paths, or raw environment variable values.

## Examples first

### Example E1: Codex still installs under `.agents/skills`

Given the installed CLI has trusted metadata for `rigorloop-adapter-codex-v0.1.6.zip`
When the user runs `rigorloop init --adapter codex`
Then the command verifies the official Codex archive
And it installs generated Codex adapter output under `.agents/skills`
And it does not install Codex output under `.codex/skills`.

### Example E2: Claude Code installs under `.claude/skills`

Given the installed CLI has trusted metadata for `rigorloop-adapter-claude-v0.1.6.zip`
When the user runs `rigorloop init --adapter claude`
Then the command verifies the official Claude Code archive
And it installs generated Claude Code adapter output under `.claude/skills`.

### Example E3: opencode installs skills and declared commands

Given the installed CLI has trusted metadata for `rigorloop-adapter-opencode-v0.1.6.zip`
And the metadata declares opencode command aliases under `.opencode/commands`
When the user runs `rigorloop init --adapter opencode`
Then the command verifies the official opencode archive
And it installs generated opencode skills under `.opencode/skills`
And it installs declared command aliases under `.opencode/commands`
And it refuses to claim success if a declared command alias is missing.

### Example E4: local archive works for every supported adapter

Given the user has `./rigorloop-adapter-claude-v0.1.6.zip`
When the user runs `rigorloop init --adapter claude --from-archive ./rigorloop-adapter-claude-v0.1.6.zip`
Then the command verifies the local archive against bundled trusted metadata
And it does not require a user-supplied metadata file
And it records only the archive basename in durable project output.

### Example E5: wrong archive for selected adapter fails

Given the user has `./rigorloop-adapter-codex-v0.1.6.zip`
When the user runs `rigorloop init --adapter claude --from-archive ./rigorloop-adapter-codex-v0.1.6.zip`
Then the command rejects the archive before extraction
And it does not create or update Claude Code adapter files
And it does not create or update a lockfile entry claiming Claude Code was installed.

### Example E6: schema v2 records mixed single-root and multi-root adapters

Given Codex is already recorded as a single-root adapter
When the user successfully installs opencode
Then `rigorloop.lock` uses `schema_version: 2`
And the Codex entry uses `installed_root`
And the opencode entry uses `installed_roots` and `root_hashes`.

### Example E7: older opencode archive installs skills only with warning

Given the installed CLI has trusted metadata for an older official opencode archive
And the metadata does not contain `command_aliases.opencode`
When the user runs `rigorloop init --adapter opencode`
Then the command installs generated opencode skills under `.opencode/skills`
And it does not create `.opencode/commands`
And it emits warning code `opencode-command-aliases-not-declared`
And `rigorloop.yaml` and `rigorloop.lock` record only the installed `skills` root.

### Example E8: proxy download failure reports safe diagnostics

Given the user runs `rigorloop init --adapter opencode`
And the network archive download fails before archive bytes are verified
When proxy-related environment variables are present
Then the command reports only safe proxy facts
And it recommends downloading the trusted public archive URL and rerunning with `--from-archive`
And it does not print proxy credentials, raw proxy URLs, private hostnames, tokens, or raw environment values.

### Example E9: dry-run plans multi-adapter init without mutation

Given a project has no `rigorloop.yaml`, no adapter roots, and no `rigorloop.lock`
When the user runs `rigorloop init --adapter opencode --dry-run --json`
Then stdout is JSON only
And it reports planned writes for `rigorloop.yaml`, `.opencode/skills`, `.opencode/commands` when declared, and `rigorloop.lock`
And no files or directories are created.

## Requirements

### Supported adapter command surface

MAI-R1. `rigorloop init --adapter codex` MUST remain supported.

MAI-R2. `rigorloop init --adapter claude` MUST be supported.

MAI-R3. `rigorloop init --adapter opencode` MUST be supported.

MAI-R4. Supported adapter names for this spec MUST be exactly `codex`, `claude`, and `opencode`.

MAI-R5. Unsupported adapter names MUST return status `blocked`, exit code `2`, and a stable blocker code `adapter-unknown`.

MAI-R6. The command surface defined by this spec MUST NOT imply support for `rigorloop status`, `rigorloop validate`, workflow YAML generation, generated workflow docs, or programmatic Undici proxy dispatcher support.

### Adapter descriptors and install roots

MAI-R7. The CLI MUST use adapter descriptors rather than Codex-only constants to select archive names, expected roots, required roots, and lockfile shape.

MAI-R8. The Codex descriptor MUST use archive filename pattern `rigorloop-adapter-codex-<release>.zip`.

MAI-R9. The Codex descriptor MUST use `skills: .agents/skills` as its only install root.

MAI-R10. The CLI MUST NOT install Codex adapter output under `.codex/skills`.

MAI-R11. The Claude Code descriptor MUST use archive filename pattern `rigorloop-adapter-claude-<release>.zip`.

MAI-R12. The Claude Code descriptor MUST use `skills: .claude/skills` as its only install root.

MAI-R13. The opencode descriptor MUST use archive filename pattern `rigorloop-adapter-opencode-<release>.zip`.

MAI-R14. The opencode descriptor MUST recognize `skills: .opencode/skills` and `commands: .opencode/commands` as possible install roots.

MAI-R14a. Trusted metadata MUST determine which opencode roots are required for a selected archive.

MAI-R15. Runtime install roots MUST be project-relative POSIX paths.

MAI-R16. Runtime install roots MUST NOT be treated as canonical authored source. Canonical public skill behavior remains authored under `skills/`.

### Trusted metadata and archive acquisition

MAI-R17. Network installs MUST use trusted adapter metadata bundled with the installed CLI package before fetching archive bytes.

MAI-R18. Local archive installs MUST use trusted adapter metadata bundled with the installed CLI package before extracting archive bytes.

MAI-R19. The CLI MUST verify bundled adapter metadata against the bundled release index before using it.

MAI-R20. Trusted metadata for each selected adapter MUST identify adapter name, release tag, archive filename, official public archive URL, archive SHA-256, size when available, tree-hash algorithm, and validation result.

MAI-R21. Trusted metadata for new opencode archives that include command aliases MUST declare the expected command alias paths.

MAI-R21a. Trusted metadata for single-root adapters MUST include `install_root`, `tree_sha256`, and `file_count`.

MAI-R21b. Trusted metadata for multi-root adapters MUST include `install_roots` and `root_hashes` keyed by root role.

MAI-R21c. Each `root_hashes` entry MUST include `tree_sha256` and `file_count`.

MAI-R21d. Trusted metadata for opencode command aliases MUST use a `command_aliases.opencode` section with `count` and exact project-relative alias paths when aliases are declared.

MAI-R21e. Absence of `command_aliases.opencode` in trusted metadata MUST be treated as the only signal that the selected official opencode archive is an older skills-only archive.

MAI-R21f. Skills-only older opencode archive behavior is allowed only for release ranges explicitly listed in bundled trusted metadata as compatible with skills-only opencode installation.

MAI-R22. If trusted metadata for the selected adapter and release is unavailable, the command MUST return status `blocked`, exit code `2`, and blocker code `metadata-unavailable`.

MAI-R23. Network installs MUST fetch only the exact official public archive URL selected from trusted metadata.

MAI-R24. A network archive URL that does not match trusted metadata MUST return status `error`, exit code `3`, and error code `non-official-archive-url`.

MAI-R25. `--from-archive <path>` MUST select local archive mode for all supported adapters.

MAI-R26. Local archive mode MUST NOT require a user-facing metadata path.

MAI-R27. A local archive whose filename, adapter identity, release, SHA-256, or size does not match trusted metadata MUST be rejected before extraction.

MAI-R28. A wrong archive for the selected adapter MUST return status `error`, exit code `3`, and an adapter/archive mismatch error code.

### Archive verification and extraction safety

MAI-R29. The CLI MUST verify archive SHA-256 before extraction.

MAI-R30. The CLI MUST verify archive size when trusted metadata provides `size_bytes`.

MAI-R31. The CLI MUST reject archive entries with absolute paths, parent-directory traversal, empty paths, drive-letter paths, unsupported symlinks, or paths outside the selected adapter's expected roots.

MAI-R32. The CLI MUST extract only files under the selected adapter's expected roots.

MAI-R33. The CLI MUST reject a selected adapter archive when trusted metadata says `validation.result` is not `pass`.

MAI-R34. The CLI MUST compute installed generated-output tree hashes using `rigorloop-tree-hash-v1`.

MAI-R35. `rigorloop-tree-hash-v1` semantics from `specs/rigorloop-cli-lockfile.md` MUST apply unchanged.

MAI-R36. The CLI MUST compare computed installed tree hashes to trusted metadata before claiming install success.

MAI-R37. Failed archive SHA-256, size, path traversal, unsupported symlink, metadata hash, metadata schema, or installed tree-hash verification MUST return status `error` and exit code `3`.

MAI-R38. If adapter installation is blocked or fails, the CLI MUST NOT create or update a lockfile entry claiming the adapter was installed.

### opencode command alias handling

MAI-R39. opencode skills MUST be installed under `.opencode/skills`.

MAI-R40. opencode command aliases MUST be installed under `.opencode/commands` when trusted metadata declares command aliases.

MAI-R41. New opencode archives MUST include command aliases when trusted metadata declares command aliases.

MAI-R42. Missing declared opencode command aliases MUST be a validation failure for new archives.

MAI-R43. The CLI MUST NOT silently install only `.opencode/skills` when trusted metadata declares `.opencode/commands` aliases.

MAI-R44. Older opencode archives that lack command-alias metadata MAY install without `.opencode/commands`, but the command MUST emit a warning that command aliases were not declared by the selected archive metadata.

MAI-R45. The warning for older opencode archives without command-alias metadata MUST NOT imply that slash-command aliases are available.

MAI-R46. opencode command aliases MUST remain generated output and MUST NOT become source of truth for RigorLoop skill behavior.

MAI-R46a. Skills-only older opencode installs MUST emit warning code `opencode-command-aliases-not-declared`.

MAI-R46b. Skills-only older opencode installs MUST NOT create `.opencode/commands`.

MAI-R46c. Skills-only older opencode installs MUST record only the `skills` root in `rigorloop.yaml` and `rigorloop.lock`.

### `rigorloop.yaml`

MAI-R47. Successful non-dry-run init MUST create `rigorloop.yaml` when it is absent and no blocker prevents initialization.

MAI-R48. `rigorloop.yaml` MUST record each selected adapter and its install root or roots.

MAI-R49. Single-root adapter entries in `rigorloop.yaml` MUST use `install_root`.

MAI-R50. Multi-root adapter entries in `rigorloop.yaml` MUST use `install_roots` keyed by root role.

MAI-R51. Codex entries in `rigorloop.yaml` MUST record `install_root: ".agents/skills"`.

MAI-R51a. Claude Code entries in `rigorloop.yaml` MUST record `install_root: ".claude/skills"`.

MAI-R51b. opencode entries in `rigorloop.yaml` MUST record `install_roots.skills: ".opencode/skills"`.

MAI-R51c. opencode entries in `rigorloop.yaml` MUST record `install_roots.commands: ".opencode/commands"` only when command aliases are installed.

MAI-R51d. The minimum `rigorloop.yaml` adapter shape for this spec is:

```yaml
adapters:
  - name: codex
    install_root: ".agents/skills"
    source:
      type: release-archive
      release: "v0.1.6"
  - name: opencode
    install_roots:
      skills: ".opencode/skills"
      commands: ".opencode/commands"
    source:
      type: release-archive
      release: "v0.1.6"
```

MAI-R51e. A skills-only older opencode install MUST omit `install_roots.commands` from `rigorloop.yaml`.

MAI-R51f. When `rigorloop.yaml` exists and is valid, init MUST update only the selected adapter entry and package/source metadata needed for that operation.

MAI-R51g. Init MUST preserve unrelated valid adapter entries in `rigorloop.yaml`.

MAI-R51h. Duplicate entries for the selected adapter in `rigorloop.yaml` MUST block before mutation with status `blocked`, exit code `2`, and blocker code `duplicate-adapter-entry`.

MAI-R51i. Unsupported manifest schema, malformed adapter entries, unsupported adapter entry fields that cannot be safely preserved, or a selected adapter entry whose shape conflicts with this spec MUST block before mutation.

MAI-R52. `rigorloop.yaml` MUST record `source.type: release-archive` for network installs.

MAI-R53. `rigorloop.yaml` MUST record `source.type: local-archive` for `--from-archive` installs.

MAI-R54. `rigorloop.yaml` MUST NOT record absolute local archive paths, usernames, hostnames, proxy URLs, credentials, tokens, temporary directories, or raw environment variable values.

### `rigorloop.lock` schema v2

MAI-R55. Successful non-dry-run init for any supported adapter MUST create or update `rigorloop.lock` only after verified adapter installation succeeds.

MAI-R56. `--dry-run` MUST report planned lockfile content and MUST NOT create or modify `rigorloop.lock`.

MAI-R57. Multi-adapter lockfile support MUST use `schema_version: 2`.

MAI-R58. `schema_version: 2` lockfiles MUST keep the top-level `rigorloop`, `manifest`, and `generated.adapters` sections from `schema_version: 1`.

MAI-R59. `schema_version: 2` lockfiles MUST sort generated adapter entries by adapter name.

MAI-R60. Codex lockfile entries MUST continue to use the single-root field `installed_root: ".agents/skills"`.

MAI-R61. Claude Code lockfile entries MUST use the single-root field `installed_root: ".claude/skills"`.

MAI-R62. opencode lockfile entries MUST use `installed_roots` and `root_hashes`.

MAI-R63. Multi-root adapter entries MUST NOT use a top-level `tree_sha256` or `file_count` in place of per-root hashes.

MAI-R64. Single-root adapter entries MUST include `tree_sha256` and `file_count`.

MAI-R64a. Skills-only older opencode lockfile entries MUST use `installed_roots.skills` and `root_hashes.skills` only.

MAI-R64b. Skills-only older opencode lockfile entries MUST omit `installed_roots.commands` and `root_hashes.commands`.

MAI-R65. Each lockfile adapter entry MUST include adapter name, release tag, source, archive basename, archive SHA-256, and tree hash algorithm.

MAI-R66. `source` MUST be either `release-archive` or `local-archive`.

MAI-R67. Local archive lockfile entries MUST record the local archive basename only, not its absolute or relative input path.

MAI-R68. `rigorloop.lock` MUST NOT record absolute local paths, usernames, hostnames, proxy URLs, credentials, tokens, temporary directories, raw environment variable values, or full proxy environment values.

MAI-R69. The CLI MUST preserve backward-compatible parsing of existing `schema_version: 1` Codex single-root lockfiles.

MAI-R70. When adding Claude Code or opencode to a project with a valid `schema_version: 1` Codex lockfile, the CLI MAY upgrade the lockfile to `schema_version: 2` only after verifying the existing Codex generated output still matches the recorded Codex tree hash.

MAI-R71. If an existing `schema_version: 1` Codex lockfile has drift, the CLI MUST block before adding or updating unrelated adapter entries.

MAI-R72. Unsupported schema versions, unknown top-level fields, unknown adapter-entry fields, malformed lockfiles, unsupported adapter entries, or unsupported tree hash algorithms MUST block before mutation according to the existing lockfile error-class contract.

MAI-R73. The CLI MUST NOT silently discard, preserve, or rewrite unknown lockfile fields during schema upgrade.

MAI-R74. Re-running init for an adapter whose installed output and lockfile entry already match MAY report the adapter and lockfile as unchanged.

MAI-R75. Reinstalling the same adapter through a different delivery mode MAY update `source` after archive and installed tree verification succeeds.

MAI-R76. The CLI MUST NOT mutate unrelated valid adapter entries except when upgrading the document wrapper from `schema_version: 1` to `schema_version: 2` after required drift checks pass.

The preferred `schema_version: 2` shape is:

```yaml
schema_version: 2

rigorloop:
  package: "@xiongxianfei/rigorloop"
  version: "0.1.6"

manifest:
  path: "rigorloop.yaml"
  sha256: "<sha256>"

generated:
  adapters:
    - adapter: codex
      release: "v0.1.6"
      source: release-archive
      archive: "rigorloop-adapter-codex-v0.1.6.zip"
      archive_sha256: "<sha256>"
      installed_root: ".agents/skills"
      tree_hash_algorithm: rigorloop-tree-hash-v1
      tree_sha256: "<sha256>"
      file_count: 23
    - adapter: opencode
      release: "v0.1.6"
      source: release-archive
      archive: "rigorloop-adapter-opencode-v0.1.6.zip"
      archive_sha256: "<sha256>"
      tree_hash_algorithm: rigorloop-tree-hash-v1
      installed_roots:
        skills: ".opencode/skills"
        commands: ".opencode/commands"
      root_hashes:
        skills:
          tree_sha256: "<sha256>"
          file_count: 23
        commands:
          tree_sha256: "<sha256>"
          file_count: 5
```

### Proxy-aware network behavior

MAI-R77. First-slice proxy support MUST use Node built-in env-proxy behavior only when the current runtime supports and enables it.

MAI-R78. This spec MUST NOT add programmatic Undici proxy dispatcher support.

MAI-R79. If network archive download fails, the command MUST include actionable diagnostics in human output or JSON fields according to the existing CLI envelope.

MAI-R80. Download failure diagnostics MUST include adapter name, adapter release version, download failure class, the trusted public archive URL from metadata, and `--from-archive` fallback guidance.

MAI-R81. JSON diagnostics MUST expose `proxy_env_vars_detected` as an array of environment variable names only.

MAI-R81a. `proxy_env_vars_detected` MUST include only names from this allowlist: `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`, `http_proxy`, `https_proxy`, `no_proxy`.

MAI-R82. JSON diagnostics MUST expose `node_env_proxy_status`.

MAI-R82a. `node_env_proxy_status` MUST be one of `enabled`, `disabled`, `unsupported`, or `unknown`.

MAI-R82b. When the CLI cannot determine Node env-proxy support without guessing, it MUST use `unknown`.

MAI-R82c. JSON diagnostics MUST expose `download_failure_class`.

MAI-R82d. `download_failure_class` MUST be one of `dns`, `tls`, `timeout`, `http-status`, `proxy`, `network`, or `unknown`.

MAI-R82e. JSON diagnostics MUST expose `archive_url` as the trusted public archive URL selected from metadata.

MAI-R83. Download failure diagnostics MUST NOT include proxy credentials, raw proxy URLs, private hostnames, access tokens, raw environment variable values, usernames, machine-local paths, temporary directories, or request headers.

MAI-R84. A network download failure before archive verification MUST return status `blocked` and exit code `2` when retrying later or using `--from-archive` is a valid next action.

MAI-R85. Proxy diagnostics MUST NOT weaken official URL validation, archive verification, or local archive verification.

### JSON and human output

MAI-R86. JSON output MUST continue to use the stable CLI envelope from `specs/rigorloop-cli-package-and-codex-init.md`.

MAI-R87. JSON output for successful non-dry-run init MUST include actions and artifacts for generated adapter output, `rigorloop.yaml`, and `rigorloop.lock` when written or updated.

MAI-R88. JSON output for `--dry-run` MUST include planned adapter roots and planned lockfile content without writing files.

MAI-R89. Human output MUST state the selected adapter, release tag, install root or roots, archive source type, and lockfile action.

MAI-R90. Human output MUST NOT print JSON fragments as routine output.

MAI-R91. `--quiet`, `--debug`, `--no-color`, and `NO_COLOR` MUST preserve the existing CLI behavior contracts.

### Generated adapter validation

MAI-R92. If this initiative changes canonical public skills, adapter templates, adapter generation, adapter metadata, or release archive contents, validation MUST regenerate temporary adapter output from canonical `skills/` and approved templates.

MAI-R93. Generated adapter output MUST be validated against expected install roots, metadata, archive hashes, tree hashes, opencode command aliases, and security scanning before release evidence claims support.

MAI-R94. Generated adapter output MUST NOT be hand-edited.

MAI-R95. Validation commands MUST NOT treat `.agents/skills`, `.claude/skills`, `.opencode/skills`, or `.opencode/commands` in a user project as authored source.

## Inputs and outputs

Inputs:

- command-line arguments for `rigorloop init --adapter <adapter>`;
- `--from-archive <path>`, when supplied;
- `--dry-run`, `--json`, `--quiet`, `--debug`, `--no-color`, and `NO_COLOR`;
- bundled trusted adapter metadata for the installed CLI package;
- official public archive URLs selected from trusted metadata;
- local archive bytes supplied through `--from-archive`;
- existing project files, including `rigorloop.yaml`, `rigorloop.lock`, and adapter install roots.

Outputs:

- generated adapter files under `.agents/skills`, `.claude/skills`, `.opencode/skills`, and `.opencode/commands` according to selected adapter and trusted metadata;
- `rigorloop.yaml`;
- `rigorloop.lock`;
- stable JSON envelope when `--json` is supplied;
- human output otherwise;
- exit codes from the existing CLI exit-code contract.

## State and invariants

- Canonical public skill behavior remains authored under `skills/`.
- Runtime install roots contain verified generated output, not authored source.
- Adapter archives remain GitHub release artifacts and are not bundled into the npm package as authored source.
- The CLI owns metadata trust through bundled trusted metadata.
- A lockfile entry may claim generated output only after archive and installed tree verification succeed.
- Local archive mode changes delivery mode only; it does not change the metadata trust root.
- Proxy diagnostics must help recovery without exposing sensitive network data.

## Error and boundary behavior

1. Unsupported adapters block with exit code `2`.
2. Missing trusted metadata blocks with exit code `2`.
3. Wrong archive for selected adapter fails with exit code `3`.
4. Non-official network archive URL fails with exit code `3`.
5. Archive checksum, size, traversal, unsupported symlink, metadata hash, metadata schema, or installed tree-hash mismatch fails with exit code `3`.
6. Existing user-file conflicts fail with exit code `5`.
7. Existing generated-output drift blocks destructive replacement by default.
8. Malformed project config or malformed lockfile shape follows the existing CLI invalid-config and lockfile error-class contracts.
9. Network download failure before verification blocks with exit code `2` when fallback remains possible.
10. Partial installation failure must report whether scaffold files, adapter files, or lockfile state may have changed.

## Compatibility and migration

The change is additive for command syntax: Codex remains supported and keeps `.agents/skills`.

Existing projects with no `rigorloop.lock` remain valid. Successful init may create a `schema_version: 2` lockfile after verification.

Existing projects with valid `schema_version: 1` Codex lockfiles remain valid. The CLI may upgrade them to `schema_version: 2` when adding or updating adapter entries only after validating the existing Codex generated output against its recorded hash.

Existing malformed, unsupported, unknown-field, or drifted lockfiles require user repair or a later migration command; this spec does not define a general lockfile repair command.

Older official opencode archives without command-alias metadata remain installable with a warning. New opencode archives with declared aliases must install both skills and commands or fail verification.

Rollback is to keep Codex init support and reject unsupported adapters clearly. A rollback must not remove existing verified generated output or silently rewrite lockfiles.

## Observability

- JSON output MUST expose adapter selection, source type, planned or actual roots, lockfile action, warnings, blockers, errors, and diagnostics using stable fields.
- Human output MUST identify the selected adapter, release tag, archive source type, install root or roots, and next action for blockers.
- Verification failures MUST identify the failed verification category without printing large file bodies or sensitive values.
- Proxy diagnostics MUST report safe facts only.
- Validation evidence for this feature must name commands that verified adapter selection, local archive fallback, proxy diagnostics, and lockfile schema v2 behavior.

## Security and privacy

- The command MUST NOT require secrets or credentials for normal public release-archive installation.
- The command MUST NOT trust user-supplied metadata.
- The command MUST NOT fetch archive URLs outside trusted metadata.
- Archive extraction MUST defend against path traversal and unsupported symlinks.
- The lockfile and manifest MUST NOT record secrets, tokens, credentials, raw proxy URLs, private hostnames, usernames, temporary directories, or raw environment values.
- Proxy diagnostics MUST NOT print request headers or proxy authentication material.
- Generated adapter output and command aliases MUST NOT broaden tool permissions beyond the target user's existing agent configuration.

## Accessibility and UX

No graphical UI is involved.

Human CLI output must be concise and actionable. Failure output should include a concrete next action when available, especially for network failures that can be worked around with `--from-archive`.

## Performance expectations

Dry-run planning SHOULD avoid downloading archive bytes when trusted metadata is enough to report planned actions.

Archive verification and tree hashing SHOULD be linear in the number and size of generated files.

The command MUST avoid reading, hashing, or printing files outside the selected adapter roots except as needed to check existing `rigorloop.yaml`, `rigorloop.lock`, and mutation conflicts.

Proxy diagnostics MUST NOT perform additional live network probes beyond the selected official archive download attempt.

## Edge cases

1. Existing `rigorloop.yaml` lists Codex only; adding Claude Code updates or plans the adapter list without removing Codex.
2. Existing `rigorloop.lock` is schema v1 Codex-only and matches the installed tree; adding opencode upgrades to schema v2.
3. Existing `rigorloop.lock` is schema v1 Codex-only but `.agents/skills` has drift; adding Claude Code or opencode blocks before mutation.
4. Existing `rigorloop.lock` is schema v2 with Codex and Claude Code; adding opencode preserves both existing entries after validation.
5. Existing `.opencode/skills` is a file; opencode init fails with mutation conflict exit code `5`.
6. Existing `.opencode/commands` contains unrelated files; opencode init refuses to overwrite or delete them.
7. Trusted metadata declares opencode command aliases but the archive omits one; init fails verification.
8. Trusted metadata lacks command-alias metadata for an older opencode archive; init may install skills and emits a warning that command aliases were not declared.
9. Local archive basename matches the selected adapter but SHA-256 differs; init fails before extraction.
10. Network fetch fails with proxy environment variables present; diagnostics report variable names only and fallback guidance.
11. Network fetch succeeds but archive SHA-256 fails; diagnostics report verification failure, not a proxy failure.
12. `--dry-run --json` is used with each supported adapter; no files are written.
13. Unsupported adapter values such as `cursor` block and do not create files.
14. Package version and adapter release are incompatible; init blocks with `release-version-incompatible`.
15. Lockfile schema version is unsupported; init blocks before adapter extraction.

## Non-goals

- No `rigorloop status`.
- No `rigorloop validate`.
- No workflow YAML generation.
- No generated workflow docs.
- No npm-bundled adapter archives.
- No user-supplied metadata option.
- No programmatic Undici proxy dispatcher support.
- No Codex install-root migration to `.codex/skills`.
- No lockfile repair command.
- No adapter archive packaging redesign.
- No live GitHub or live proxy dependency in normal tests.

## Acceptance criteria

- AC1. The spec defines supported adapter descriptors for Codex, Claude Code, and opencode.
- AC2. Codex init remains compatible and installs under `.agents/skills`.
- AC3. Claude Code init installs verified adapter output under `.claude/skills`.
- AC4. opencode init installs verified adapter output under `.opencode/skills` and declared command aliases under `.opencode/commands`.
- AC5. Unsupported adapter names block with exit code `2` and no adapter output writes.
- AC6. Network installs fetch only trusted official archive URLs from bundled metadata.
- AC7. `--from-archive` works for all supported adapters without a user-supplied metadata path.
- AC8. Wrong archive, checksum mismatch, size mismatch, traversal, symlink, and tree-hash mismatch failures are verified before success is claimed.
- AC9. `rigorloop.yaml` records adapter-specific root or roots without machine-local paths.
- AC10. Successful non-dry-run init writes or updates `rigorloop.lock` after verification.
- AC11. `schema_version: 2` supports mixed Codex single-root and opencode multi-root entries.
- AC12. Existing schema v1 Codex lockfiles remain compatible when not drifted.
- AC13. Drifted existing generated output blocks destructive replacement by default.
- AC14. Proxy failure diagnostics report safe facts and fallback guidance without leaking sensitive values.
- AC15. Normal tests for network and proxy behavior are hermetic and do not require live GitHub or a live proxy.
- AC16. Generated adapter validation uses temporary output from canonical `skills/` and approved templates when adapter output changes.

## Open questions

None.

## Next artifacts

- architecture and ADR
- `plan`
- `plan-review`
- `test-spec`

## Follow-on artifacts

- Spec review: `../docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/reviews/spec-review-r2.md`
- Architecture: `../docs/architecture/system/architecture.md`
- ADR: `../docs/adr/ADR-20260518-multi-adapter-init-and-proxy-download.md`

## Readiness

Approved by `spec-review-r2` and ready for architecture review.
