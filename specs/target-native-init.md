# Target-Native Init

## Status

approved

## Related proposal

- [Target-Native Init Commands and Adapter Terminology Retirement](../docs/proposals/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement.md)
- Proposal-review evidence: [proposal-review-r3](../docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/reviews/proposal-review-r3.md)
- Supersession boundary: when this spec is approved, it supersedes the `init --adapter` command surface and default state-file write requirements in [Multi-Adapter Init and Proxy-Aware Adapter Download](multi-adapter-init-and-proxy-aware-download.md), [RigorLoop CLI Lockfile](rigorloop-cli-lockfile.md), and the `rigorloop.yaml` init requirements in [RigorLoop CLI Package and Codex Init](rigorloop-cli-package-and-codex-init.md). Archive verification, tree hashing, extraction safety, proxy diagnostics, local archive trust, and generated-output mutation safety continue to apply unless this spec explicitly changes them.

## Goal and context

This spec defines the `0.3.0` public init contract:

```bash
rigorloop init codex
rigorloop init claude
rigorloop init opencode
```

The public command initializes RigorLoop support for a target tool, not an adapter. Default init installs verified target files only and must not create or update `rigorloop.yaml` or `rigorloop.lock`. Users who want durable RigorLoop-managed project state must request it explicitly:

```bash
rigorloop init codex --write-state
```

The release-quality goal is also part of this contract: release smoke must exercise real non-dry-run target-native init from packaged artifacts, not dry-run output alone.

## Glossary

- `target`: a supported tool family initialized by RigorLoop. First-slice values are `codex`, `claude`, and `opencode`.
- `target support`: verified generated files installed for a target tool.
- `install-only init`: default `rigorloop init <target>` behavior that installs verified target support without writing RigorLoop project state files.
- `managed-state init`: `rigorloop init <target> --write-state`, which installs verified target support and then writes `rigorloop.yaml` and `rigorloop.lock`.
- `state files`: project-root `rigorloop.yaml` and `rigorloop.lock`.
- `target-oriented state keys`: user-visible YAML keys that use `target` or `targets`, not `adapter` or `adapters`.
- `trusted metadata`: package-bundled release metadata verified against the release index before archive bytes are trusted.
- `legacy state file`: an existing `rigorloop.yaml` or `rigorloop.lock` that uses `adapter` or `adapters` keys from pre-`0.3.0` behavior.

## Examples first

Example E1: default Codex init installs support without state files
Given a project has no `rigorloop.yaml`, no `rigorloop.lock`, and no `.agents/skills`
When the user runs `rigorloop init codex`
Then the command verifies the Codex release archive and installed tree
And it installs Codex target support under `.agents/skills`
And it does not create `rigorloop.yaml`
And it does not create `rigorloop.lock`.

Example E2: explicit managed state writes target-oriented files
Given a project has no `rigorloop.yaml` and no `rigorloop.lock`
When the user runs `rigorloop init codex --write-state`
Then the command verifies and installs Codex target support
And it writes `rigorloop.yaml` using `targets`
And it writes `rigorloop.lock` using `generated.targets`
And neither state file uses user-visible `adapter` or `adapters` keys.

Example E3: default init preserves existing state files unchanged
Given a project already has `rigorloop.yaml` and `rigorloop.lock`
When the user runs `rigorloop init claude`
Then the command installs verified Claude Code target support under `.claude/skills`
And the byte content of both existing state files is unchanged.

Example E4: removed adapter syntax fails with migration guidance
Given any project
When the user runs `rigorloop init --adapter codex`
Then the command fails before installation
And it reports that `--adapter` was removed in RigorLoop `0.3.0`
And it suggests `rigorloop init codex`.

Example E5: opencode installs declared roots
Given trusted metadata declares opencode skills and command aliases
When the user runs `rigorloop init opencode --write-state`
Then the command installs skills under `.opencode/skills`
And it installs command aliases under `.opencode/commands`
And `rigorloop.yaml` records `install_roots.skills` and `install_roots.commands`
And `rigorloop.lock` records per-root hashes for `skills` and `commands`.

Example E6: dry-run is not release smoke proof
Given a package artifact is ready for release validation
When release validation runs only `rigorloop init codex --dry-run --json`
Then the validation is incomplete
And release readiness must remain blocked until real non-dry-run packed-package smoke passes for every supported target.

Example E7: legacy state files are preserved by default and rewritten on request
Given a project has legacy state files using `adapters`
When the user runs `rigorloop init codex`
Then the state files remain byte-identical
When the user runs `rigorloop init codex --write-state`
Then the command rewrites state to the target-oriented schema only after verified install and compatibility checks pass.

## Requirements

### Command surface

TNI-R1. `rigorloop init codex` MUST be the canonical Codex init command.

TNI-R2. `rigorloop init claude` MUST be the canonical Claude Code init command.

TNI-R3. `rigorloop init opencode` MUST be the canonical opencode init command.

TNI-R4. The only supported first-slice targets MUST be `codex`, `claude`, and `opencode`.

TNI-R5. The CLI MUST NOT accept target aliases including `claude-code`, `open-code`, `openai`, or `codex-cli`.

TNI-R6. The CLI MUST NOT accept `--adapter` in `0.3.0`.

TNI-R7. Any use of `--adapter` with `init` MUST fail before archive download, extraction, state-file writes, or target-root mutation.

TNI-R8. Removed `--adapter` errors MUST include migration guidance naming `init codex`, `init claude`, and `init opencode`.

TNI-R9. `rigorloop init` without a target MUST fail with a diagnostic that lists `codex`, `claude`, and `opencode`.

TNI-R10. `rigorloop init <unknown-target>` MUST fail with a diagnostic that lists `codex`, `claude`, and `opencode`.

TNI-R11. Mixed removed and positional forms, such as `rigorloop init codex --adapter claude`, MUST fail before mutation.

TNI-R12. The npm manual quick-start example MUST use `npx @xiongxianfei/rigorloop@latest init codex`.

TNI-R13. Automation and reproducible setup examples SHOULD show a pinned package version such as `npx @xiongxianfei/rigorloop@0.3.0 init codex` because automation should avoid unexpected latest-version drift.

### Install behavior

TNI-R14. Default `rigorloop init <target>` MUST be install-only.

TNI-R15. Default init MUST NOT create, update, delete, rename, or reformat `rigorloop.yaml`.

TNI-R16. Default init MUST NOT create, update, delete, rename, or reformat `rigorloop.lock`.

TNI-R17. Default init MUST preserve existing `rigorloop.yaml` and `rigorloop.lock` byte-for-byte.

TNI-R18. Byte preservation MUST NOT prohibit safety reads of existing state files.

TNI-R19. When existing state files are present and default init plans to mutate a target root, the CLI MUST parse enough valid state to determine whether the selected target or target root is already managed, drifted, or conflicting.

TNI-R20. A selected target or target root is implicated by existing state when `rigorloop.yaml` records the selected target, `rigorloop.lock` records the selected target, either state file records an install root that overlaps the root the command would mutate, or either state file records a target-root mapping that conflicts with the selected target's expected root.

TNI-R21. If existing state is valid and unrelated to the selected target or target root, default init MAY proceed and MUST preserve state files unchanged.

TNI-R22. If existing state is valid but the selected target or target root is drifted or conflicting, default init MUST block before target-root mutation and report a bounded diagnostic.

TNI-R23. If either existing state file is malformed or ambiguous, default non-dry-run init MUST block before target-root mutation because the CLI cannot safely prove the selected root is unrelated.

TNI-R24. Default dry-run MAY report planned target-root writes when existing state is malformed or ambiguous, but it MUST report that the corresponding non-dry-run command would block before target-root mutation.

TNI-R25. Managed-state init MUST be requested with `--write-state`.

TNI-R26. `rigorloop init <target> --write-state` MUST install verified target support and then write or regenerate `rigorloop.yaml` and `rigorloop.lock` after verification succeeds.

TNI-R27. The CLI MUST NOT write state files before archive verification, extraction safety checks, installed tree-hash verification, and file-count verification pass.

TNI-R28. Failed, blocked, or dry-run init MUST NOT create or update state files.

TNI-R29. Codex target support MUST install under `.agents/skills`.

TNI-R30. Claude Code target support MUST install under `.claude/skills`.

TNI-R31. opencode target support MUST install skills under `.opencode/skills`.

TNI-R32. opencode target support MUST install command aliases under `.opencode/commands` when trusted metadata declares command aliases.

TNI-R33. Older official opencode archives without command-alias metadata MAY install skills only when bundled trusted metadata explicitly marks that archive range as skills-only compatible.

TNI-R34. Skills-only opencode installs MUST warn with code `opencode-command-aliases-not-declared` and MUST NOT claim command aliases are installed.

TNI-R35. Generated target files installed by this spec MUST preserve the currently approved skill behavior for Codex, Claude Code, and opencode.

### Trusted metadata, archive verification, and local archives

TNI-R36. Network installs MUST use trusted metadata bundled with the installed CLI package before fetching archive bytes.

TNI-R37. Local archive installs using `--from-archive <path>` MUST use trusted metadata bundled with the installed CLI package before extracting archive bytes.

TNI-R38. The CLI MUST verify bundled target metadata against the bundled release index before using it.

TNI-R39. Trusted metadata for each selected target MUST identify target identity, release tag, archive filename, official public archive URL, archive SHA-256, tree-hash algorithm, install roots, tree hash, file count, and validation result.

TNI-R40. Package-bundled metadata MUST include `file_count` for every verified install root.

TNI-R41. Package-bundled metadata MUST include `tree_sha256` for every verified install root.

TNI-R42. Package-bundled metadata MUST be generated from or checked against the release archive bytes before publication.

TNI-R43. Network installs MUST fetch only the exact official public archive URL selected from trusted metadata.

TNI-R44. A local archive whose filename, target identity, release, SHA-256, or size does not match trusted metadata MUST be rejected before extraction.

TNI-R45. Archive extraction MUST reject absolute paths, parent-directory traversal, empty paths, drive-letter paths, unsupported symlinks, and paths outside the selected target's expected roots.

TNI-R46. The CLI MUST compute installed generated-output tree hashes using `rigorloop-tree-hash-v1`.

TNI-R47. The `rigorloop-tree-hash-v1` semantics from `specs/rigorloop-cli-lockfile.md` MUST apply unchanged.

TNI-R48. The CLI MUST compare computed installed tree hashes and file counts to trusted metadata before claiming install success.

TNI-R49. Failed archive hash, size, path safety, metadata hash, metadata schema, installed tree-hash, or file-count verification MUST return an error and MUST NOT claim install success.

### State-file schemas

TNI-R50. New `rigorloop.yaml` content written by `--write-state` MUST use target-oriented user-visible schema keys.

TNI-R51. New `rigorloop.yaml` schema keys MUST NOT use `adapter`, `adapters`, `adapter_name`, `adapter_id`, `adapter_archive`, or equivalent adapter-oriented key names for new user-visible state.

TNI-R52. The `rigorloop.yaml` schema-key prohibition applies to schema keys, not to historical archive filename values or package-bundled metadata values that remain internal compatibility surfaces in this slice.

TNI-R53. New `rigorloop.lock` content written by `--write-state` MUST use target-oriented user-visible schema keys.

TNI-R54. New `rigorloop.lock` schema keys MUST NOT use `adapter`, `adapters`, `adapter_name`, `adapter_id`, `adapter_archive`, or equivalent adapter-oriented key names for new user-visible state.

TNI-R55. Archive filename values in `rigorloop.lock` MAY retain historical names such as `rigorloop-adapter-codex-v0.3.0.zip` until a separate archive or internal rename is approved.

TNI-R56. `rigorloop.yaml` written by this spec MUST use `schema_version: 2`.

TNI-R57. `rigorloop.yaml` written by this spec MUST record target entries under top-level `targets`.

TNI-R58. Single-root target entries in `rigorloop.yaml` MUST use `install_root`.

TNI-R59. Multi-root target entries in `rigorloop.yaml` MUST use `install_roots` keyed by root role.

TNI-R60. The minimum `rigorloop.yaml` release-archive shape MUST be:

```yaml
schema_version: 2

targets:
  - target: codex
    install_root: ".agents/skills"
    source:
      type: release-archive
      release: "v0.3.0"
  - target: opencode
    install_roots:
      skills: ".opencode/skills"
      commands: ".opencode/commands"
    source:
      type: release-archive
      release: "v0.3.0"
```

TNI-R61. `rigorloop.yaml` MUST record `source.type: local-archive` for `--from-archive` installs and MUST NOT record absolute local archive paths.

TNI-R62. `rigorloop.lock` written by this spec MUST use `schema_version: 3`.

TNI-R63. `schema_version: 3` lockfiles MUST use `generated.targets`, not `generated.adapters`.

TNI-R64. `schema_version: 3` lockfile target entries MUST use `target`, not `adapter`.

TNI-R65. `schema_version: 3` lockfiles MUST sort generated target entries by target name.

TNI-R66. Single-root target entries MUST use `installed_root`, `tree_sha256`, and `file_count`.

TNI-R67. Multi-root target entries MUST use `installed_roots` and `root_hashes` keyed by root role.

TNI-R68. The minimum `schema_version: 3` lockfile shape MUST be:

```yaml
schema_version: 3

rigorloop:
  package: "@xiongxianfei/rigorloop"
  version: "0.3.0"

manifest:
  path: "rigorloop.yaml"
  sha256: "<sha256>"

generated:
  targets:
    - target: codex
      release: "v0.3.0"
      source: release-archive
      archive: "rigorloop-adapter-codex-v0.3.0.zip"
      archive_sha256: "<sha256>"
      installed_root: ".agents/skills"
      tree_hash_algorithm: rigorloop-tree-hash-v1
      tree_sha256: "<sha256>"
      file_count: 38
    - target: opencode
      release: "v0.3.0"
      source: release-archive
      archive: "rigorloop-adapter-opencode-v0.3.0.zip"
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

TNI-R69. State files MUST NOT record secrets, tokens, credentials, raw proxy URLs, private hostnames, usernames, absolute local archive paths, temporary directories, raw environment values, or request headers.

TNI-R70. Existing legacy state files using `adapter` or `adapters` MUST be treated as compatibility input.

TNI-R71. Default init MUST preserve legacy state files unchanged.

TNI-R72. `--write-state` MAY rewrite valid legacy state files to the target-oriented schema only after validating any existing generated output needed to avoid destructive replacement.

TNI-R73. `--write-state` MUST block before mutation when existing state files are malformed, ambiguous, unsupported, contain duplicate selected-target entries, or cannot be safely migrated.

TNI-R74. A `--write-state` migration from a valid legacy lockfile MUST verify recorded existing generated-output roots before rewriting the lockfile schema.

TNI-R75. The CLI MUST NOT silently drop unrelated valid state entries during managed-state rewrite.

### Dry-run, JSON, and output

TNI-R76. `--dry-run` MUST report planned target-root writes without mutating files.

TNI-R77. `--dry-run` MUST report planned state-file writes only when state-file writes are in scope for the requested command, such as when `--write-state` is present.

TNI-R78. Default `init <target> --dry-run` MUST be install-only and MUST NOT report planned creation or update of `rigorloop.yaml` or `rigorloop.lock`.

TNI-R79. Default `rigorloop init <target> --dry-run --json` MUST report planned target-root writes and MUST NOT report planned creation or update of `rigorloop.yaml` or `rigorloop.lock`.

TNI-R80. `rigorloop init <target> --write-state --dry-run --json` MUST report planned target-root writes and planned target-oriented `rigorloop.yaml` and `rigorloop.lock` content.

TNI-R81. JSON output MUST identify `target`, not `adapter`, for the selected target in new output fields.

TNI-R82. Human output MUST describe initializing support for a target or tool, not installing an adapter.

TNI-R83. Human output for default successful init MUST state that state files were not written unless `--write-state` is used.

TNI-R84. JSON output for successful default init MUST distinguish skipped state-file writes from written artifacts.

TNI-R85. Routine human output MUST NOT print JSON fragments.

### Release smoke and documentation

TNI-R86. Pre-publish release smoke MUST run real non-dry-run init from a packed package for `codex`, `claude`, and `opencode`.

TNI-R87. Pre-publish release smoke MUST verify default init does not create `rigorloop.yaml` or `rigorloop.lock`.

TNI-R88. Pre-publish release smoke MUST verify `init <target> --write-state` writes target-oriented state files for each target.

TNI-R89. Pre-publish release smoke MUST verify installed tree hashes and file counts match package-bundled trusted metadata for each target.

TNI-R90. Dry-run output MUST NOT be accepted as release install-smoke proof.

TNI-R91. Post-publish smoke MUST run live registry/download init against the published npm package and public release assets.

TNI-R92. Public README, package README, npm usage, CLI help, and release notes guidance MUST teach `init <target>` instead of `init --adapter <target>`.

TNI-R93. Public docs MUST NOT describe the user's action as installing an adapter.

TNI-R94. Public docs MAY mention historical adapter archive filenames only when explaining compatibility, release assets, or internal implementation boundaries.

## Inputs and outputs

Inputs:

- `rigorloop init <target>`;
- `rigorloop init <target> --write-state`;
- `--from-archive <path>`;
- `--dry-run`, `--json`, `--quiet`, `--debug`, `--no-color`, and `NO_COLOR`;
- bundled trusted metadata and release index;
- official public archive URLs selected from trusted metadata;
- local archive bytes supplied through `--from-archive`;
- existing target install roots;
- existing `rigorloop.yaml` and `rigorloop.lock`.

Outputs:

- generated target files under `.agents/skills`, `.claude/skills`, `.opencode/skills`, and `.opencode/commands` according to selected target and trusted metadata;
- optional `rigorloop.yaml` only when `--write-state` is used;
- optional `rigorloop.lock` only when `--write-state` is used;
- stable JSON envelope when `--json` is supplied;
- human CLI output otherwise;
- exit codes from the existing CLI exit-code contract.

## State and invariants

- Default init is install-only and does not mutate state files.
- Managed-state init writes state files only after verification succeeds.
- State files written by this spec use target-oriented user-visible keys.
- Existing state files are preserved by default, including legacy `adapter` state files.
- Runtime install roots contain verified generated output, not authored source.
- Canonical public skill behavior remains authored under `skills/`.
- Package-bundled trusted metadata remains the metadata trust root.
- Local archive mode changes delivery mode only; it does not change the metadata trust root.
- A state-file entry may claim generated output only after archive and installed tree verification succeed.
- Release smoke must prove real installation behavior from packaged artifacts.

## Error and boundary behavior

1. Missing target fails before mutation and lists allowed targets.
2. Unknown target fails before mutation and lists allowed targets.
3. Any `--adapter` use fails before mutation with `0.3.0` migration guidance.
4. Target aliases fail before mutation.
5. Missing trusted metadata blocks before archive download or extraction.
6. Wrong local archive for selected target fails before extraction.
7. Non-official network archive URL fails before download.
8. Archive checksum, size, path traversal, unsupported symlink, metadata hash, metadata schema, installed tree-hash, or file-count mismatch fails before success is claimed.
9. Existing user-file conflicts in target roots fail with the existing mutation-conflict exit class.
10. Existing generated-output drift represented by a valid state file blocks destructive replacement unless an approved replacement rule applies.
11. Existing valid state that records the selected target, an overlapping install root, or a conflicting target-root mapping requires safety parsing before default init mutates target roots.
12. Malformed or ambiguous existing state blocks default non-dry-run init before target-root mutation.
13. Default dry-run may report planned target-root writes with malformed state, but it must report that the corresponding non-dry-run command would block before mutation.
14. `--write-state` blocks on malformed or ambiguous state files rather than silently rewriting them.
15. Partial installation failure must report whether target files or state files may have changed.

## Compatibility and migration

This is a breaking CLI cleanup in `0.3.0`: `init --adapter <target>` is removed rather than deprecated.

The installed generated files for Codex, Claude Code, and opencode remain behavior-compatible with the current release archives.

Existing projects without `rigorloop.yaml` or `rigorloop.lock` remain valid.

Existing state files using legacy `adapter` keys remain valid compatibility input. Default init preserves them unchanged. `--write-state` may migrate valid legacy state to the target-oriented schemas defined here after verification and drift checks pass.

Existing `schema_version: 1` and `schema_version: 2` lockfiles remain parseable for compatibility checks. New lockfile writes from this spec use `schema_version: 3`.

Rollback is to keep `0.2.x` as the last documented line supporting `init --adapter <target>`. A published `0.3.0` with broken init behavior must be fixed forward because npm versions are immutable.

## Observability

- JSON output must expose selected `target`, source type, planned or actual roots, state-file action, warnings, blockers, errors, and safe diagnostics using stable fields.
- Human output must identify the selected target, release tag, archive source type, install root or roots, state-file action, and next action for blockers.
- Verification failures must identify the failed verification category without printing large file bodies or sensitive values.
- Release evidence must name packed-package smoke, live post-publish smoke, metadata/archive coherence checks, tree hashes, file counts, and docs sweep results.

## Security and privacy

- The command MUST NOT require secrets or credentials for normal public release-archive installation.
- The command MUST NOT trust user-supplied metadata.
- The command MUST NOT fetch archive URLs outside trusted metadata.
- Archive extraction MUST defend against path traversal and unsupported symlinks.
- State files and diagnostics MUST NOT record secrets, tokens, credentials, raw proxy URLs, private hostnames, usernames, absolute local archive paths, temporary directories, raw environment values, or request headers.
- Generated target files MUST NOT broaden tool permissions beyond the target user's existing agent configuration.

## Accessibility and UX

No graphical UI is involved.

Human CLI output must be concise and actionable. Failure output should include a concrete next action when available. The command help must show target-native syntax and must not require users to understand the internal adapter packaging model.

## Performance expectations

Archive verification and tree hashing SHOULD remain linear in archive size plus installed regular-file bytes. Default init MUST NOT add state-file parsing or hashing work except where existing state is needed for mutation safety. Release smoke MAY be slower than dry-run smoke because it must exercise real installation.

## Edge cases

EC1. Project has no target roots and no state files.

EC2. Project has existing target roots with no state files.

EC3. Project has valid target-oriented state files.

EC4. Project has valid legacy adapter-oriented state files.

EC5. Project has malformed `rigorloop.yaml`.

EC6. Project has malformed `rigorloop.lock`.

EC7. Project has duplicate selected-target entries in state files.

EC8. Project has unsupported future state-file schema versions.

EC9. Project has existing generated-output drift recorded by a lockfile.

EC10. Project has a target install path that is a file where a directory is expected.

EC11. Local archive filename matches but SHA-256 differs.

EC12. opencode metadata declares command aliases but the archive lacks them.

EC13. opencode metadata marks an older skills-only archive as compatible.

EC14. `--dry-run --json` is combined with `--write-state`.

EC15. `--adapter` appears before or after a positional target.

## Non-goals

- No change to RigorLoop workflow semantics.
- No change to published skill behavior or generated skill content.
- No new npm package name.
- No top-level `rigorloop codex` command.
- No target aliases in the first slice.
- No public support for `adapter` syntax in `0.3.0`.
- No full internal rename of `dist/adapters/`, archive filenames, or package-bundled metadata field names.
- No hosted service, control plane, or external registry.
- No release smoke based only on dry-run output.
- No general lockfile repair command.
- No automatic migration of malformed or ambiguous state files.

## Acceptance criteria

- AC-TNI-001. `rigorloop init codex`, `rigorloop init claude`, and `rigorloop init opencode` install verified target support.
- AC-TNI-002. `rigorloop init --adapter codex` and mixed `--adapter` forms fail before mutation with `0.3.0` migration guidance.
- AC-TNI-003. Unknown targets and aliases fail before mutation and list `codex`, `claude`, and `opencode`.
- AC-TNI-004. Default init does not create `rigorloop.yaml` or `rigorloop.lock`.
- AC-TNI-005. Default init preserves existing `rigorloop.yaml` and `rigorloop.lock` byte-for-byte.
- AC-TNI-006. `init <target> --write-state` writes `rigorloop.yaml` with `schema_version: 2` and top-level `targets`.
- AC-TNI-007. `init <target> --write-state` writes `rigorloop.lock` with `schema_version: 3` and `generated.targets`.
- AC-TNI-008. New state files written by `--write-state` use target-oriented user-visible schema keys and do not use `adapter` or `adapters` as schema keys; historical archive filename values such as `rigorloop-adapter-codex-v0.3.0.zip` remain allowed until a separate internal archive rename is approved.
- AC-TNI-009. Valid legacy state files are preserved byte-for-byte by default and are migrated or rewritten only through `--write-state` after verification and drift checks.
- AC-TNI-010. Malformed or ambiguous state files block default non-dry-run init before target-root mutation and block `--write-state` with migration guidance.
- AC-TNI-011. Package-bundled metadata includes and validates archive SHA-256, tree hash, and file count for every target root.
- AC-TNI-012. Pre-publish packed-package smoke runs real non-dry-run init for every target and verifies installed tree hashes, file counts, no default state files, and `--write-state` state files.
- AC-TNI-013. Post-publish live registry/download smoke runs against the published npm package and public release assets.
- AC-TNI-014. Dry-run output is not accepted as install-smoke proof.
- AC-TNI-015. Public docs, npm usage, CLI help, and release notes teach `init <target>`, not `init --adapter <target>`.
- AC-TNI-016. Installed skill behavior for Codex, Claude Code, and opencode is unchanged except for the command and state-file behavior defined here.

## Open questions

None for spec-review readiness.

## Next artifacts

- Architecture-review for the target-native init architecture update.
- Test spec mapping target-native CLI parsing, default install-only behavior, `--write-state`, state-file schemas, metadata/archive coherence, release smoke, docs sweep, and compatibility migration behavior after architecture review.
- Execution plan after architecture review and test-spec readiness.

## Follow-on artifacts

None yet

## Readiness

Approved after spec-review R3. Ready for architecture-review, then test-spec and execution planning.
