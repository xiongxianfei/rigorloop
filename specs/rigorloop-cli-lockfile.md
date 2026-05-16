# RigorLoop CLI Lockfile

## Status

approved

## Related proposal

- [RigorLoop Scaffolding CLI and Machine-Readable Workflow](../docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md)
- Follow-up: `FU-004` in [follow-ups](../docs/follow-ups.md)
- Builds on: [RigorLoop CLI Package and Codex Init](rigorloop-cli-package-and-codex-init.md)

## Goal and context

This spec defines the durable `rigorloop.lock` contract for the RigorLoop CLI after verified adapter installation.

The first CLI slice intentionally emitted only `planned_lockfile` output because a lockfile is durable source-of-truth state. This spec defines what the lockfile owns, when `init --adapter codex` may write it, how generated adapter output is hashed, how conflicts are handled, and how users and agents observe drift.

This spec does not define `new-change`, `status`, `validate`, public npm publishing, workflow YAML canonicality, generated workflow docs, or adapters other than Codex.

## Glossary

- `rigorloop.lock`: the durable project-local lockfile written at the project root.
- `lockfile owner`: the RigorLoop CLI command that writes or updates a lockfile entry after completing the corresponding verified operation.
- `generated adapter output`: files installed from a verified adapter release archive, currently Codex files under `.agents/skills`.
- `tree hash`: the `rigorloop-tree-hash-v1` digest over a generated output tree.
- `drift`: a mismatch between lockfile-recorded generated output hashes and the current filesystem.
- `manifest`: `rigorloop.yaml`.
- `planned lockfile`: lockfile-shaped output reported in JSON before durable writes are authorized or applied.

## Examples first

### Example E1: verified Codex init writes a lockfile

Given a project has no `rigorloop.lock`
And `rigorloop init --adapter codex` verifies and installs the Codex release archive
When the command completes
Then it writes `rigorloop.lock`
And the lockfile records the CLI package, manifest hash, Codex archive hash, install root, tree hash algorithm, tree hash, and file count.

### Example E2: dry-run still writes nothing

Given a project has no `rigorloop.lock`
When the user runs `rigorloop init --adapter codex --dry-run --json`
Then stdout includes `planned_lockfile`
And `rigorloop.lock` is not created.

### Example E3: unchanged generated output keeps lockfile stable

Given `rigorloop.lock` already records the installed Codex adapter
And the current `.agents/skills` tree matches the recorded tree hash
When the user reruns `rigorloop init --adapter codex`
Then the command may report the lockfile as `existing` or `unchanged`
And it must not rewrite unrelated lockfile entries.

### Example E4: adapter drift blocks by default

Given `rigorloop.lock` records a Codex adapter tree hash
And a generated adapter file under `.agents/skills` has been modified
When the user runs `rigorloop init --adapter codex`
Then the command reports drift
And it does not overwrite the modified file unless an approved generated-output replacement rule applies.

### Example E5: malformed lockfile blocks mutation

Given `rigorloop.lock` exists but is not parseable as the lockfile schema
When the user runs `rigorloop init --adapter codex`
Then the command blocks before mutating generated output
And reports an invalid-lockfile error with an actionable next step.

## Requirements

### Lockfile scope and authority

R1. `rigorloop.lock` MUST be a project-local durable file at the project root.

R2. `rigorloop.lock` MUST be generated and updated only by RigorLoop CLI mutation commands.

R3. The lockfile MUST record generated output state; it MUST NOT replace canonical authored sources, release metadata, workflow specs, skills, schemas, or adapter release archives.

R4. The first lockfile-writing command surface MUST be limited to successful `rigorloop init --adapter codex`.

R5. This spec MUST NOT authorize durable lockfile writes for `new-change`, `status`, `validate`, workflow rendering, non-Codex adapters, or public npm publication.

R6. The CLI MUST NOT write `rigorloop.lock` before the operation whose generated output it records has completed verification.

R7. `--dry-run` MUST report planned lockfile content and MUST NOT create or modify `rigorloop.lock`.

R8. If adapter installation is blocked or fails, the CLI MUST NOT create a lockfile entry claiming the adapter was installed.

### File format

R9. `rigorloop.lock` MUST be UTF-8 text with LF line endings.

R10. `rigorloop.lock` MUST use `schema_version: 1`.

R11. The lockfile format MUST be deterministic: repeated writes for identical state must produce byte-identical lockfile content.

R12. The lockfile MUST sort generated adapter entries by adapter name.

R13. The lockfile MUST use repository-relative POSIX paths and MUST NOT record absolute project paths.

R14. The lockfile MUST NOT record timestamps, usernames, hostnames, temporary directories, environment variable values, secrets, or access tokens.

R15. The lockfile MUST include the RigorLoop CLI package name and version that wrote the current lockfile content.

R16. The lockfile MUST include the project manifest path and SHA-256 hash when `rigorloop.yaml` exists.

R17. The lockfile MUST include generated adapter entries under `generated.adapters`.

## `rigorloop.lock` document shape

`rigorloop.lock` is a machine-owned durable compatibility file.

For `schema_version: 1`, the lockfile MUST use this top-level shape:

```yaml
schema_version: 1

rigorloop:
  package: "@xiongxianfei/rigorloop"
  version: "0.1.3"

manifest:
  path: "rigorloop.yaml"
  sha256: "<sha256>"

generated:
  adapters:
    - adapter: codex
      release: "v0.1.3"
      source: release-archive
      archive: "rigorloop-adapter-codex-v0.1.3.zip"
      archive_sha256: "<sha256>"
      installed_root: ".agents/skills"
      tree_hash_algorithm: rigorloop-tree-hash-v1
      tree_sha256: "<sha256>"
      file_count: 23
```

For local archive installs, the same top-level shape applies with `source: local-archive`:

```yaml
schema_version: 1

rigorloop:
  package: "@xiongxianfei/rigorloop"
  version: "0.1.3"

manifest:
  path: "rigorloop.yaml"
  sha256: "<sha256>"

generated:
  adapters:
    - adapter: codex
      release: "v0.1.3"
      source: local-archive
      archive: "rigorloop-adapter-codex-v0.1.3.zip"
      archive_sha256: "<sha256>"
      installed_root: ".agents/skills"
      tree_hash_algorithm: rigorloop-tree-hash-v1
      tree_sha256: "<sha256>"
      file_count: 23
```

### Top-level fields

R17a. `schema_version` MUST be `1`.

R17b. `rigorloop` MUST identify the CLI package that wrote or last updated the lockfile.

R17c. `rigorloop.package` MUST be the npm package name, currently `@xiongxianfei/rigorloop`.

R17d. `rigorloop.version` MUST be the CLI package version that wrote or last updated the lockfile.

R17e. `manifest` MUST identify the project manifest locked by this file.

R17f. `manifest.path` MUST be the repository-relative path to the project manifest, currently `rigorloop.yaml`.

R17g. `manifest.sha256` MUST be the SHA-256 of the normalized manifest bytes.

R17h. `generated.adapters` MUST be an array of generated adapter output entries.

### Codex adapter entry

R18. A Codex adapter lockfile entry MUST include:

```yaml
adapter: codex
release: "v0.1.3"
source: release-archive | local-archive
archive: rigorloop-adapter-codex-v0.1.3.zip
archive_sha256: "<sha256>"
installed_root: ".agents/skills"
tree_hash_algorithm: rigorloop-tree-hash-v1
tree_sha256: "<sha256>"
file_count: 23
```

R18a. `adapter` MUST be the adapter name. The first-slice allowed value is `codex`.

R18b. `release` MUST be the adapter release tag used for this install, for example `v0.1.3`.

R18c. `source` MUST identify the install delivery mode, not the metadata trust root.

R18ca. The first-slice allowed `source` values are `release-archive` and `local-archive`.

R18d. `archive` MUST be the adapter archive filename.

R18e. `archive_sha256` MUST be the SHA-256 of the adapter archive.

R18f. `installed_root` MUST be the project-relative install root, currently `.agents/skills`.

R18g. `tree_hash_algorithm` MUST be `rigorloop-tree-hash-v1`.

R18h. `tree_sha256` MUST be the normalized generated-output tree hash.

R18i. `file_count` MUST be the number of regular files included in the generated-output tree hash.

R19. A release-archive Codex entry MUST include the release tag used to resolve the official adapter archive in `release`.

R20. A local-archive Codex entry MUST include the basename of the local archive, not the absolute local archive path.

R21. The lockfile MUST record the adapter metadata release version or release tag that supplied the trusted expected archive hash.

R22. The lockfile MUST record only the verified archive SHA-256 and installed tree hash, not a copy of full adapter release metadata.

R23. `installed_root` for the first lockfile-writing slice MUST be `.agents/skills`.

R23a. The first slice MUST support only the `codex` adapter.

R23b. Other adapter entries MUST block until their lockfile entries are specified.

### `source: release-archive`

R23ba. The CLI MUST use `source: release-archive` when it downloaded the adapter archive from the official RigorLoop release URL selected by package-bundled metadata.

R23bb. For `source: release-archive`, `release` MUST be the official release tag.

R23bc. For `source: release-archive`, `archive` MUST be the official archive filename from trusted metadata.

R23bd. For `source: release-archive`, `archive_sha256` MUST match trusted metadata.

### `source: local-archive`

R23be. The CLI MUST use `source: local-archive` when it installed from `--from-archive <path>`.

R23bf. For `source: local-archive`, `release` MUST still be the official release tag from package-bundled metadata.

R23bg. For `source: local-archive`, `archive` MUST be the basename of the local archive path.

R23bh. For `source: local-archive`, `archive_sha256` MUST match the trusted metadata for the selected adapter release.

R23bi. For `source: local-archive`, the lockfile MUST NOT record absolute local paths.

R23bj. For `source: local-archive`, the lockfile MUST NOT record machine-local directories, usernames, or host-specific archive paths.

### Unknown-field policy

R23c. For `schema_version: 1`, the CLI MUST block before mutating files when `rigorloop.lock` contains an unknown top-level section.

R23d. For `schema_version: 1`, the CLI MUST block before mutating files when `rigorloop.lock` contains an unknown field inside a known section.

R23e. For `schema_version: 1`, the CLI MUST block before mutating files when `rigorloop.lock` contains an unknown field inside a `generated.adapters[]` entry.

R23f. Unsupported `schema_version` MUST block before mutation.

R23g. Unsupported adapter entries MUST block before mutation.

R23h. A `tree_hash_algorithm` other than `rigorloop-tree-hash-v1` MUST block before mutation.

R23ha. `generated.adapters[].source` MUST be one of `release-archive` or `local-archive`.

R23hb. Any other `generated.adapters[].source` value MUST block before mutation with status `blocked`, exit code `2`, and blocker code `unsupported-lockfile-shape`.

R23i. Unknown or unsupported lockfile shape MUST return status `blocked`, exit code `2`, and blocker code `unsupported-lockfile-shape`.

R23j. The CLI MUST NOT silently delete, rewrite, or preserve unknown sections in the first slice.

R23k. Malformed YAML, missing required fields, or invalid field types MUST return status `error` and exit code `4`.

### Hashing

R24. The lockfile MUST use `rigorloop-tree-hash-v1` for generated adapter output.

R25. `rigorloop-tree-hash-v1` MUST hash regular files only.

R26. `rigorloop-tree-hash-v1` MUST exclude directories, symlinks, modification times, creation times, owner, group, absolute paths, the lockfile itself, and temporary files.

R27. Tree-hash paths MUST be relative to the generated output root, use POSIX `/`, have no leading `./`, have no trailing slash, be UTF-8 strings, and be sorted lexicographically.

R28. Text generated by RigorLoop MUST be normalized to UTF-8 with LF line endings, with a UTF-8 BOM removed if present, without trimming whitespace or semantically normalizing Markdown.

R29. Binary files MUST be hashed as raw bytes.

R30. Each file hash MUST be `sha256(normalized_file_bytes)`.

R31. The canonical tree manifest MUST be:

```text
rigorloop-tree-hash-v1\n
<relative_path>\t<file_sha256>\n
<relative_path>\t<file_sha256>\n
...
```

R32. The tree hash MUST be `sha256(utf8(canonical_manifest))`.

R33. If a future generated output tree contains both text and binary files, the lockfile-writing command MUST have a deterministic way to classify file-byte normalization before it records a tree hash.

### Write and update behavior

R34. `init --adapter codex` MUST include `rigorloop.lock` in the write plan before writing or updating it.

R35. The write plan MUST distinguish planned creation, planned update, unchanged existing lockfile, blocked lockfile, and skipped lockfile actions.

R36. If no `rigorloop.lock` exists and Codex adapter installation succeeds, `init --adapter codex` MUST create one.

R37. If a valid `rigorloop.lock` exists and contains no Codex entry, `init --adapter codex` MAY add a Codex entry only when all existing entries use the supported `schema_version: 1` shape.

R38. If a valid `rigorloop.lock` exists and contains a Codex entry for the same installed root, `init --adapter codex` MAY update only that entry after verification succeeds.

R39. The CLI MUST NOT mutate unrelated entries unless a later spec defines multi-adapter update behavior.

R40. The CLI MUST refuse to update a malformed, unsupported, or semantically invalid lockfile by default.

R41. The CLI MUST NOT silently discard, preserve, or rewrite unknown top-level fields in `rigorloop.lock`.

R42. If the lockfile schema version is unsupported, the command MUST block before mutation unless a later migration spec defines an upgrade path.

R43. The CLI MUST NOT delete `rigorloop.lock` in this slice.

R44. `--force` MUST NOT permit arbitrary lockfile replacement in this slice.

R45. Any allowed `--force` behavior for lockfiles MUST be specified by a later spec before implementation.

R45a. When `rigorloop.lock` is absent, successful adapter installation MAY create it using the complete `schema_version: 1` shape.

R45b. When `rigorloop.lock` exists and matches the supported shape, the CLI MAY update only `rigorloop.version`, `manifest.sha256`, and the matching `generated.adapters[]` entry for the requested adapter.

R45c. The CLI MUST refuse to update when the existing lockfile has unknown shape, unsupported schema, or unsupported adapter entries.

R45d. If the user reinstalls the same adapter through a different delivery mode, the CLI MAY update `source` from `release-archive` to `local-archive`, or from `local-archive` to `release-archive`, because `source` records the latest install delivery mode.

R45e. The CLI MUST NOT update the matching adapter entry when archive verification, tree-hash verification, manifest validation, or mutation safety checks fail.

### Drift and conflict behavior

R46. Before replacing generated adapter files that are already represented in `rigorloop.lock`, the CLI MUST compare the current installed tree hash with the recorded tree hash.

R47. If the current installed tree hash differs from the recorded tree hash, the command MUST report drift.

R48. Drift MUST block destructive replacement by default.

R49. Drift reporting MUST identify the adapter, installed root, expected tree hash, and actual tree hash when available.

R50. Drift reporting SHOULD identify changed file paths when the command can do so without weakening the tree-hash contract.

R51. A missing generated output root that is represented in the lockfile MUST be reported as drift or missing generated output before replacement proceeds.

R52. A generated output path that exists as a non-directory where a directory is expected MUST block with mutation conflict exit code `5`.

R53. A generated file path that exists as a directory where a file is expected MUST block with mutation conflict exit code `5`.

### JSON, human output, and exit behavior

R54. JSON output MUST continue to use the stable CLI envelope from `specs/rigorloop-cli-package-and-codex-init.md`.

R55. Successful lockfile creation or update MUST be represented in `actions` and `artifacts`.

R56. `planned_lockfile` MAY remain in JSON output, but successful actual init MUST also report the durable lockfile artifact when written.

R57. The warning code `lockfile-spec-not-approved` MUST NOT be emitted after this spec is approved and implemented for the lockfile-writing command surface.

R58. Invalid or unsupported lockfile state MUST produce status `blocked` or `error` according to the stable CLI exit-class contract.

R59. Mutation conflicts involving `rigorloop.lock` or generated output MUST exit `5`.

R60. Lockfile schema validation failures MUST exit `4` when caused by invalid project config and `3` when caused by expected verification failure during generated-output validation.

R61. Unexpected filesystem, parser, or serialization failures MUST exit `1`.

### Compatibility and migration

R62. Existing projects created by the first CLI slice without `rigorloop.lock` MUST remain valid.

R63. Running the lockfile-enabled `init --adapter codex` in a first-slice project MAY create `rigorloop.lock` after verifying existing or newly installed generated output.

R64. The lockfile-enabled slice MUST NOT require public npm publication.

R65. The lockfile-enabled slice MUST remain compatible with package-local execution through `node packages/rigorloop/dist/bin/rigorloop.js` and installed execution through `rigorloop`.

R66. The first lockfile-writing slice MUST block on unknown future sections or unsupported schema versions until a later migration or preservation spec defines different behavior.

## Inputs and outputs

### Inputs

- `rigorloop init --adapter codex`
- `rigorloop init --adapter codex --from-archive <path>`
- `rigorloop init --adapter codex --dry-run --json`
- `rigorloop.yaml`
- verified bundled adapter metadata
- official or local Codex adapter archive
- existing `.agents/skills`
- existing `rigorloop.lock`, when present

### Outputs

- `rigorloop.lock` at the project root for successful non-dry-run lockfile-writing operations
- stable JSON envelope with lockfile actions and artifacts
- human output that states whether the lockfile was created, updated, unchanged, skipped, or blocked
- exit code matching the established CLI contract

## State and invariants

- The lockfile records generated output state; it is not canonical authored source.
- `rigorloop.yaml` describes selected project configuration; `rigorloop.lock` records verified installed generated output.
- A lockfile entry may claim generated output only after verification succeeds.
- A dry run is a promise, not a mutation.
- Drift must be visible before destructive replacement.
- Unknown lockfile state must block or be preserved explicitly, not silently erased.

## Error and boundary behavior

1. Missing `rigorloop.lock` in an existing first-slice project is valid.
2. Malformed `rigorloop.lock` blocks mutation and reports the parse failure.
3. Unsupported `schema_version` blocks mutation until migration behavior is specified.
4. Existing generated output with a matching tree hash may be treated as unchanged.
5. Existing generated output with a mismatched tree hash is drift and blocks replacement by default.
6. Lockfile write permission failure reports whether adapter installation already occurred.
7. Partial adapter installation must not result in a lockfile entry that claims success.
8. `--dry-run` never writes the lockfile, even when the planned lockfile is valid.

## Compatibility and migration

The lockfile-enabled behavior extends the approved first CLI slice. It supersedes the first-slice `rigorloop.lock` prohibition only for the command surface explicitly named in this spec after this spec is approved and implemented.

Projects without `rigorloop.lock` continue to work. The first lockfile-enabled successful `init --adapter codex` may create the lockfile. Existing malformed lockfiles require user repair or a later migration command; this spec does not define automatic migration.

## Observability

- JSON output must expose lockfile actions and artifacts.
- Human output must state whether `rigorloop.lock` was created, updated, unchanged, skipped, or blocked.
- Drift output must include expected and actual tree hashes when available.
- Validation evidence for this feature must name the commands that created, updated, or refused the lockfile.

## Security and privacy

- The lockfile must not contain secrets, tokens, credentials, absolute local paths, usernames, hostnames, or temporary directories.
- The lockfile must not expand the network trust boundary defined by the Codex init spec.
- Local archive paths must not be persisted beyond a basename.
- A lockfile entry must not be accepted as proof that a release archive is trustworthy unless the command also verifies the archive and installed tree according to the adapter install contract.

## Accessibility and UX

No graphical UI is involved. Human CLI output must use concise, actionable language and must not require users to understand hash internals to resolve common blockers.

## Performance expectations

Tree hashing SHOULD be linear in the number of generated files and their byte size. The command MUST avoid network access solely to write or compare `rigorloop.lock` when adapter metadata and archive verification inputs are already local.

## Edge cases

1. Existing project has `rigorloop.yaml` and no `rigorloop.lock`.
2. Existing project has an empty `rigorloop.lock`.
3. Existing project has unsupported `schema_version`.
4. Existing project has a valid lockfile with a future unknown top-level section.
5. Existing Codex generated output matches the lockfile tree hash.
6. Existing Codex generated output differs from the lockfile tree hash.
7. Existing lockfile records `.agents/skills`, but that path is missing.
8. Existing lockfile records `.agents/skills`, but that path is a file.
9. Local archive install succeeds and records only the archive basename.
10. Dry-run computes planned lockfile content but writes nothing.

## Non-goals

- No `rigorloop new-change` behavior.
- No `rigorloop status` behavior.
- No `rigorloop validate` behavior.
- No lockfile migration command.
- No lockfile writes for Claude or opencode adapters.
- No workflow YAML lockfile entries.
- No generated workflow docs lockfile entries.
- No public npm publication hardening.
- No use of `rigorloop.lock` as canonical skill, schema, workflow, or release metadata source.

## Acceptance criteria

- AC1. A successful non-dry-run `rigorloop init --adapter codex` creates `rigorloop.lock` after verified adapter install.
- AC2. `--dry-run --json` reports `planned_lockfile` and writes no lockfile.
- AC3. The spec defines a complete `schema_version: 1` `rigorloop.lock` YAML shape with top-level `schema_version`, `rigorloop`, `manifest`, and `generated.adapters[]` sections.
- AC4. Re-running init with matching generated output is deterministic and does not remove unrelated valid lockfile entries.
- AC5. Tests include a full valid lockfile fixture and prove adapter entries are nested under `generated.adapters[]`.
- AC6. Tests reject missing required fields with status `error` and exit code `4`.
- AC7. Tests block unknown top-level sections and unsupported schema versions with status `blocked`, exit code `2`, and blocker code `unsupported-lockfile-shape`.
- AC8. Generated-output drift blocks destructive replacement by default and reports expected and actual tree hashes.
- AC9. The command no longer emits `lockfile-spec-not-approved` after this spec is approved and implemented for the in-scope lockfile-writing command.
- AC10. Network install lockfiles record `source: release-archive`.
- AC11. Local archive install lockfiles record `source: local-archive`, the official release tag, and the local archive basename without recording absolute local paths.
- AC12. Unsupported `generated.adapters[].source` values block with status `blocked`, exit code `2`, and blocker code `unsupported-lockfile-shape`.
- AC13. Failed archive verification does not create or update `rigorloop.lock`.

## Open questions

- Should a later slice add a dedicated `rigorloop lock refresh` or `rigorloop repair` command for intentional regeneration after drift?
- Should future lockfile schema versions preserve unknown sections automatically or require explicit migration commands?

## Next artifacts

- Architecture or ADR update for lockfile ownership, serialization, drift comparison, and partial-failure ordering if the spec is approved.
- Test spec mapping each lockfile requirement to CLI package tests and validation commands.

## Follow-on artifacts

- Spec review: [spec-review-r3](../docs/changes/2026-05-15-rigorloop-cli-lockfile/reviews/spec-review-r3.md), approved.
- Architecture package update: [canonical architecture](../docs/architecture/system/architecture.md).
- ADR: [ADR-20260516-rigorloop-cli-lockfile](../docs/adr/ADR-20260516-rigorloop-cli-lockfile.md).
- Architecture review: [architecture-review-r1](../docs/changes/2026-05-15-rigorloop-cli-lockfile/reviews/architecture-review-r1.md), approved.
- Plan: [2026-05-16 RigorLoop CLI durable lockfile](../docs/plans/2026-05-16-rigorloop-cli-lockfile.md).
- Plan review: [plan-review-r1](../docs/changes/2026-05-15-rigorloop-cli-lockfile/reviews/plan-review-r1.md), approved.
- Test spec: [RigorLoop CLI Lockfile Test Spec](rigorloop-cli-lockfile.test.md).

## Readiness

Ready for the next lifecycle stage: M1 execution.
