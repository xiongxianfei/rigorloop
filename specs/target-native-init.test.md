# Target-Native Init Test Spec

## Status

active

## Related spec and plan

- Spec: [Target-Native Init](target-native-init.md), approved.
- Plan: [Target-Native Init Commands](../docs/plans/2026-05-24-target-native-init-commands.md), active and approved by `plan-review-r2`.
- Proposal: [Target-Native Init Commands and Adapter Terminology Retirement](../docs/proposals/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement.md), accepted.
- Architecture: [RigorLoop Canonical System Architecture](../docs/architecture/system/architecture.md), approved.
- ADR: [ADR-20260524-target-native-init-state-boundary](../docs/adr/ADR-20260524-target-native-init-state-boundary.md), accepted.
- Change metadata: [change.yaml](../docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/change.yaml).
- Review records:
  - `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/reviews/spec-review-r2.md`
  - `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/reviews/spec-review-r3.md`
  - `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/reviews/architecture-review-r1.md`
  - `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/reviews/plan-review-r2.md`

## Testing strategy

This change alters a public filesystem-mutating CLI command, downstream state schemas, trusted release metadata, documentation promises, and release gates. Proof must be automated, fixture-backed, and explicit about pre-publish versus post-publish validation.

- Unit and contract tests cover target descriptor selection, removed parser forms, allowed target set, trusted metadata schema, release-index coherence, state serializers, lockfile parsers, official URL selection, archive path safety, and tree-hash/file-count verification helpers.
- Integration tests execute `packages/rigorloop` in temporary project directories and assert exit codes, JSON envelopes, human output, dry-run no-write behavior, target-root writes, default state-file preservation, `--write-state` state-file writes, and pre-mutation blockers.
- Archive tests use small fixture ZIP archives and package-bundled metadata for Codex, Claude Code, opencode with commands, and older skills-only opencode compatibility. These tests must prove archive verification and installed-tree verification happen before success and before state writes.
- End-to-end and smoke tests use packed npm package fixtures before publish and live registry/download evidence after publish. Dry-run output is allowed for planning checks but never as install-smoke proof.
- Documentation and release validation use repository-owned scripts to enforce target-native examples, pinned automation examples, release-note evidence, docs sweep, metadata/archive coherence, and package-content expectations.
- Migration tests cover valid legacy adapter-oriented state, malformed state, ambiguous state, unsupported schemas, duplicate selected-target entries, drifted managed output, and no silent loss of unrelated valid entries.
- Manual checks are limited to post-publish live registry/download execution when live npm/public release assets are not available during pre-publish implementation.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| TNI-R1 | TTNI-CLI-001, TTNI-INST-001, TTNI-SMOKE-001 | integration, smoke | Codex target-native command and install proof. |
| TNI-R2 | TTNI-CLI-001, TTNI-INST-001, TTNI-SMOKE-001 | integration, smoke | Claude target-native command and install proof. |
| TNI-R3 | TTNI-CLI-001, TTNI-INST-002, TTNI-SMOKE-001 | integration, smoke | opencode target-native command and install proof. |
| TNI-R4 | TTNI-CLI-001, TTNI-CLI-002 | unit, integration | Exact first-slice target set. |
| TNI-R5 | TTNI-CLI-002 | integration | Alias rejection before mutation. |
| TNI-R6 | TTNI-CLI-003 | integration | `--adapter` removed in 0.3.0. |
| TNI-R7 | TTNI-CLI-003 | integration | Removed syntax fails before download, extraction, state write, or target-root mutation. |
| TNI-R8 | TTNI-CLI-003 | integration | Migration guidance names target-native forms. |
| TNI-R9 | TTNI-CLI-002 | integration | Missing target diagnostic lists allowed targets. |
| TNI-R10 | TTNI-CLI-002 | integration | Unknown target diagnostic lists allowed targets. |
| TNI-R11 | TTNI-CLI-003 | integration | Mixed positional and removed forms fail before mutation. |
| TNI-R12 | TTNI-DOC-001 | contract | Manual npm quick start uses `@latest init codex`. |
| TNI-R13 | TTNI-DOC-001 | contract | Automation examples show pinned `0.3.0`. |
| TNI-R14 | TTNI-INST-001, TTNI-DRY-001 | integration | Default init is install-only. |
| TNI-R15 | TTNI-INST-001, TTNI-STATE-003 | integration | Default init does not create/update/delete/reformat manifest. |
| TNI-R16 | TTNI-INST-001, TTNI-STATE-003 | integration | Default init does not create/update/delete/reformat lockfile. |
| TNI-R17 | TTNI-STATE-003, TTNI-MIG-001 | migration | Existing state files byte-preserved by default. |
| TNI-R18 | TTNI-STATE-004 | integration | Byte preservation still permits safety reads. |
| TNI-R19 | TTNI-STATE-004, TTNI-STATE-005 | integration | Existing state safety parse before target-root mutation. |
| TNI-R20 | TTNI-STATE-004, TTNI-STATE-005 | integration | Implicated target/root conditions. |
| TNI-R21 | TTNI-STATE-003 | integration | Valid unrelated state may proceed and remains unchanged. |
| TNI-R22 | TTNI-STATE-005 | integration | Drifted or conflicting valid state blocks before mutation. |
| TNI-R23 | TTNI-STATE-006 | integration | Malformed or ambiguous state blocks non-dry-run mutation. |
| TNI-R24 | TTNI-DRY-003 | integration | Dry-run with malformed state reports non-dry-run blocker. |
| TNI-R25 | TTNI-STATE-001 | integration | Managed state requires `--write-state`. |
| TNI-R26 | TTNI-STATE-001, TTNI-SMOKE-002 | integration, smoke | `--write-state` writes state only after verified install. |
| TNI-R27 | TTNI-STATE-002, TTNI-ARCH-003 | integration | State writes are after archive, extraction, tree hash, and file count verification. |
| TNI-R28 | TTNI-DRY-001, TTNI-ARCH-003 | integration | Failed, blocked, and dry-run init do not write state. |
| TNI-R29 | TTNI-INST-001 | integration | Codex root is `.agents/skills`. |
| TNI-R30 | TTNI-INST-001 | integration | Claude root is `.claude/skills`. |
| TNI-R31 | TTNI-INST-002 | integration | opencode skills root is `.opencode/skills`. |
| TNI-R32 | TTNI-INST-002 | integration | opencode commands root is installed when declared. |
| TNI-R33 | TTNI-INST-003 | integration | Older official skills-only opencode compatibility. |
| TNI-R34 | TTNI-INST-003 | integration | Skills-only warning code and no command-alias overclaim. |
| TNI-R35 | TTNI-SKILL-001 | contract | Generated skill behavior remains unchanged. |
| TNI-R36 | TTNI-META-001, TTNI-ARCH-001 | unit, integration | Network installs use package-bundled trusted metadata. |
| TNI-R37 | TTNI-ARCH-001 | integration | Local archive installs use package-bundled trusted metadata. |
| TNI-R38 | TTNI-META-001 | unit | Bundled target metadata verified against release index. |
| TNI-R39 | TTNI-META-001 | unit, contract | Trusted metadata fields for each selected target. |
| TNI-R40 | TTNI-META-001, TTNI-SMOKE-001 | unit, smoke | `file_count` included for every verified root. |
| TNI-R41 | TTNI-META-001, TTNI-SMOKE-001 | unit, smoke | `tree_sha256` included for every verified root. |
| TNI-R42 | TTNI-REL-001 | contract | Package metadata generated from or checked against archive bytes. |
| TNI-R43 | TTNI-ARCH-001 | integration | Network fetches only exact official trusted URL. |
| TNI-R44 | TTNI-ARCH-002 | integration | Wrong local archive identity/hash/size rejected before extraction. |
| TNI-R45 | TTNI-ARCH-003 | integration | Unsafe archive paths and unsupported symlinks rejected. |
| TNI-R46 | TTNI-ARCH-004 | unit, integration | Installed tree hashes use `rigorloop-tree-hash-v1`. |
| TNI-R47 | TTNI-ARCH-004 | unit | Existing tree-hash semantics unchanged. |
| TNI-R48 | TTNI-ARCH-004, TTNI-SMOKE-001 | integration, smoke | Installed tree hashes and file counts compared before success. |
| TNI-R49 | TTNI-ARCH-003, TTNI-ARCH-004 | integration | Verification failures error and do not claim success. |
| TNI-R50 | TTNI-STATE-001, TTNI-STATE-002 | integration | New manifest keys are target-oriented. |
| TNI-R51 | TTNI-STATE-002 | integration | New manifest schema keys forbid adapter-oriented names. |
| TNI-R52 | TTNI-STATE-002 | integration | Adapter archive filename values remain allowed. |
| TNI-R53 | TTNI-STATE-001, TTNI-STATE-002 | integration | New lockfile keys are target-oriented. |
| TNI-R54 | TTNI-STATE-002 | integration | New lockfile schema keys forbid adapter-oriented names. |
| TNI-R55 | TTNI-STATE-002 | integration | Historical adapter archive filename values allowed in lockfile. |
| TNI-R56 | TTNI-STATE-001 | integration | Manifest schema version is 2. |
| TNI-R57 | TTNI-STATE-001 | integration | Manifest uses top-level `targets`. |
| TNI-R58 | TTNI-STATE-001 | integration | Single-root manifest entries use `install_root`. |
| TNI-R59 | TTNI-STATE-001 | integration | Multi-root manifest entries use `install_roots`. |
| TNI-R60 | TTNI-STATE-001 | integration | Minimum release-archive manifest shape. |
| TNI-R61 | TTNI-STATE-007 | integration | Local archive state uses `source.type: local-archive` and no absolute paths. |
| TNI-R62 | TTNI-STATE-001 | integration | Lockfile schema version is 3. |
| TNI-R63 | TTNI-STATE-001 | integration | Lockfile uses `generated.targets`. |
| TNI-R64 | TTNI-STATE-002 | integration | Lockfile entries use `target`, not `adapter`. |
| TNI-R65 | TTNI-STATE-008 | unit | Lockfile target entries sort by target name. |
| TNI-R66 | TTNI-STATE-001 | integration | Single-root lock entries use installed root, hash, and count. |
| TNI-R67 | TTNI-STATE-001 | integration | Multi-root lock entries use installed roots and root hashes. |
| TNI-R68 | TTNI-STATE-001 | integration | Minimum schema v3 lockfile shape. |
| TNI-R69 | TTNI-STATE-007, TTNI-SEC-001 | security | State files do not record sensitive or machine-local values. |
| TNI-R70 | TTNI-MIG-001 | migration | Legacy adapter state treated as compatibility input. |
| TNI-R71 | TTNI-MIG-001 | migration | Default init preserves legacy state unchanged. |
| TNI-R72 | TTNI-MIG-002 | migration | `--write-state` may rewrite valid legacy state only after safety validation. |
| TNI-R73 | TTNI-MIG-003 | migration | Unsafe legacy or malformed state blocks managed-state rewrite. |
| TNI-R74 | TTNI-MIG-002 | migration | Legacy lockfile migration verifies recorded generated roots. |
| TNI-R75 | TTNI-MIG-004 | migration | Managed-state rewrite does not drop unrelated valid state entries. |
| TNI-R76 | TTNI-DRY-001 | integration | Dry-run reports planned target-root writes without mutation. |
| TNI-R77 | TTNI-DRY-001, TTNI-DRY-002 | integration | Dry-run reports state plans only when state writes are in scope. |
| TNI-R78 | TTNI-DRY-001 | integration | Default dry-run is install-only. |
| TNI-R79 | TTNI-DRY-001 | integration | Default dry-run JSON has no state creation/update plan. |
| TNI-R80 | TTNI-DRY-002 | integration | `--write-state --dry-run --json` includes target-oriented state content. |
| TNI-R81 | TTNI-OUT-001 | integration | JSON output identifies `target`, not `adapter`, in new fields. |
| TNI-R82 | TTNI-OUT-002 | integration | Human output uses target/tool language. |
| TNI-R83 | TTNI-OUT-002 | integration | Default success says state files were not written. |
| TNI-R84 | TTNI-OUT-001 | integration | Default JSON distinguishes skipped state writes. |
| TNI-R85 | TTNI-OUT-002 | integration | Routine human output does not print JSON fragments. |
| TNI-R86 | TTNI-SMOKE-001 | smoke | Packed-package smoke runs real non-dry-run init for all targets. |
| TNI-R87 | TTNI-SMOKE-001 | smoke | Packed default smoke verifies no state files. |
| TNI-R88 | TTNI-SMOKE-002 | smoke | Packed managed-state smoke verifies target-oriented state files. |
| TNI-R89 | TTNI-SMOKE-001 | smoke | Packed smoke verifies tree hashes and file counts. |
| TNI-R90 | TTNI-REL-002 | contract | Dry-run output is rejected as release install-smoke proof. |
| TNI-R91 | TTNI-SMOKE-003 | manual, smoke | Post-publish live registry/download smoke. |
| TNI-R92 | TTNI-DOC-001 | contract | Public docs and help teach `init <target>`. |
| TNI-R93 | TTNI-DOC-001 | contract | Public docs do not describe user action as installing an adapter. |
| TNI-R94 | TTNI-DOC-001 | contract | Historical adapter filenames only in compatibility/internal contexts. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | TTNI-INST-001, TTNI-SMOKE-001 | Default Codex init installs support without state files. |
| E2 | TTNI-STATE-001, TTNI-SMOKE-002 | Managed state writes target-oriented manifest and lockfile. |
| E3 | TTNI-STATE-003 | Existing state byte preservation during default init. |
| E4 | TTNI-CLI-003 | Removed `--adapter` fails with migration guidance before mutation. |
| E5 | TTNI-INST-002, TTNI-STATE-001 | opencode skills and command roots plus state records. |
| E6 | TTNI-REL-002, TTNI-SMOKE-001 | Dry-run-only release proof remains incomplete. |
| E7 | TTNI-MIG-001, TTNI-MIG-002 | Legacy state preserved by default and rewritten only through managed state. |

## Edge case coverage

| Edge case | Covered by |
| --- | --- |
| EC1. No target roots and no state files | TTNI-INST-001, TTNI-SMOKE-001 |
| EC2. Existing target roots with no state files | TTNI-ARCH-004, TTNI-INST-001 |
| EC3. Valid target-oriented state files | TTNI-STATE-003, TTNI-STATE-004 |
| EC4. Valid legacy adapter-oriented state files | TTNI-MIG-001, TTNI-MIG-002 |
| EC5. Malformed `rigorloop.yaml` | TTNI-STATE-006 |
| EC6. Malformed `rigorloop.lock` | TTNI-STATE-006 |
| EC7. Duplicate selected-target entries | TTNI-MIG-003 |
| EC8. Unsupported future state-file schema versions | TTNI-MIG-003 |
| EC9. Existing generated-output drift represented by lockfile | TTNI-STATE-005, TTNI-MIG-002 |
| EC10. Target install path is a file | TTNI-INST-004 |
| EC11. Local archive filename matches but SHA-256 differs | TTNI-ARCH-002 |
| EC12. opencode metadata declares command aliases but archive lacks them | TTNI-INST-002 |
| EC13. opencode metadata marks older skills-only archive compatible | TTNI-INST-003 |
| EC14. `--dry-run --json` combined with `--write-state` | TTNI-DRY-002 |
| EC15. `--adapter` appears before or after positional target | TTNI-CLI-003 |

## Milestone coverage map

| Milestone | Covered by |
| --- | --- |
| M1. CLI Command And State Schema Contract | TTNI-CLI-001 through TTNI-CLI-003, TTNI-DRY-001, TTNI-DRY-002, TTNI-STATE-001, TTNI-STATE-002, TTNI-STATE-008, TTNI-DOC-001 |
| M2. Verified Install, Existing State Safety, And Target Roots | TTNI-INST-001 through TTNI-INST-004, TTNI-STATE-003 through TTNI-STATE-007, TTNI-MIG-001 through TTNI-MIG-004, TTNI-META-001, TTNI-ARCH-001 through TTNI-ARCH-004 |
| M3. Release, Docs, And Package Validation Hardening | TTNI-DOC-001, TTNI-REL-001, TTNI-REL-002, TTNI-SMOKE-001 through TTNI-SMOKE-003 |
| M4. Lifecycle Closeout And Broad Validation | Selected CI, artifact lifecycle validation, review artifact validation, change metadata validation, and final `verify` after implementation. |

## Test cases

### TTNI-CLI-001. Target-native parser accepts only canonical supported targets

- Covers: TNI-R1, TNI-R2, TNI-R3, TNI-R4, AC-TNI-001
- Level: integration
- Fixture/setup: package-local CLI entrypoint and temporary project directories with fixture archive or mocked network metadata for each target.
- Steps: Run `rigorloop init codex`, `rigorloop init claude`, and `rigorloop init opencode` through the test CLI harness.
- Expected result: Each command selects the matching target descriptor, proceeds into verified install planning or execution, and reports the selected target as `codex`, `claude`, or `opencode`.
- Failure proves: The public command surface still depends on adapter syntax or has unsupported target selection drift.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-CLI-002. Missing, unknown, and alias targets fail before mutation

- Covers: TNI-R4, TNI-R5, TNI-R9, TNI-R10, AC-TNI-003
- Level: integration
- Fixture/setup: empty temporary project.
- Steps: Run `rigorloop init`, `rigorloop init cursor`, `rigorloop init claude-code`, `rigorloop init open-code`, `rigorloop init openai`, and `rigorloop init codex-cli`.
- Expected result: Each command fails before filesystem mutation and lists `codex`, `claude`, and `opencode`.
- Failure proves: Parser accepts ambiguous target names or gives incomplete recovery diagnostics.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-CLI-003. Removed `--adapter` syntax fails before mutation

- Covers: TNI-R6, TNI-R7, TNI-R8, TNI-R11, AC-TNI-002, EC15, E4
- Level: integration
- Fixture/setup: empty temporary project plus a project with preexisting sentinel files under target roots.
- Steps: Run `rigorloop init --adapter codex`, `rigorloop init --adapter codex claude`, and `rigorloop init codex --adapter claude`.
- Expected result: Commands fail before download, extraction, target-root mutation, and state-file writes; diagnostics say `--adapter` was removed in `0.3.0` and suggest `rigorloop init codex`, `rigorloop init claude`, and `rigorloop init opencode`.
- Failure proves: The breaking removal is incomplete or can mutate before rejecting removed syntax.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-INST-001. Default init installs single-root targets without state files

- Covers: TNI-R14, TNI-R15, TNI-R16, TNI-R29, TNI-R30, AC-TNI-001, AC-TNI-004, E1, EC1, EC2
- Level: integration
- Fixture/setup: Codex and Claude fixture archives, trusted metadata, temporary projects without state files.
- Steps: Run default non-dry-run init for `codex` and `claude`.
- Expected result: Codex installs under `.agents/skills`, Claude installs under `.claude/skills`, no `rigorloop.yaml` or `rigorloop.lock` is created, and installed roots verify against metadata.
- Failure proves: Default init still writes managed state or single-root target mapping is wrong.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-INST-002. opencode installs skills and declared command aliases

- Covers: TNI-R31, TNI-R32, AC-TNI-001, E5, EC12
- Level: integration
- Fixture/setup: opencode fixture archive with `.opencode/skills` and `.opencode/commands`, trusted metadata declaring command aliases.
- Steps: Run `rigorloop init opencode --write-state`; also run a negative fixture where metadata declares a command alias missing from the archive.
- Expected result: Skills and commands install under expected roots, state files record both root roles, and missing declared aliases fail verification without claiming success.
- Failure proves: Multi-root opencode support or command-alias verification is incomplete.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-INST-003. Skills-only opencode compatibility is explicit and warned

- Covers: TNI-R33, TNI-R34, EC13
- Level: integration
- Fixture/setup: older official opencode skills-only fixture archive and trusted metadata marking the archive range as compatible.
- Steps: Run opencode init using the skills-only metadata range.
- Expected result: Skills install, commands are not claimed as installed, and warning code `opencode-command-aliases-not-declared` is emitted.
- Failure proves: The CLI overclaims command aliases or rejects approved compatibility archives.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-INST-004. Target-root user conflicts block without replacement

- Covers: error behavior 9, EC10
- Level: integration
- Fixture/setup: temporary projects with `.agents/skills`, `.claude/skills`, `.opencode/skills`, or `.opencode/commands` represented by files or containing unrelated conflicting user files.
- Steps: Run default init for the implicated target.
- Expected result: Command exits with the existing mutation-conflict class, preserves user files, and does not write state files.
- Failure proves: Init can overwrite user content or report success over conflicts.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-STATE-001. `--write-state` writes target-oriented manifest and lockfile

- Covers: TNI-R25, TNI-R26, TNI-R50, TNI-R53, TNI-R56, TNI-R57, TNI-R58, TNI-R59, TNI-R60, TNI-R62, TNI-R63, TNI-R66, TNI-R67, TNI-R68, AC-TNI-006, AC-TNI-007, E2, E5
- Level: integration
- Fixture/setup: verified fixture archives and metadata for all three targets.
- Steps: Run `rigorloop init <target> --write-state` for `codex`, `claude`, and `opencode`.
- Expected result: `rigorloop.yaml` has `schema_version: 2` and `targets`; single-root entries use `install_root`; opencode uses `install_roots`; `rigorloop.lock` has `schema_version: 3`, `generated.targets`, single-root hash/count fields, and multi-root `installed_roots` plus `root_hashes`.
- Failure proves: Managed-state schema output does not match the 0.3.0 contract.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-STATE-002. New state schema keys avoid adapter terminology while allowing historical archive values

- Covers: TNI-R51, TNI-R52, TNI-R54, TNI-R55, TNI-R64, AC-TNI-008
- Level: integration
- Fixture/setup: state files written by `--write-state` for all targets.
- Steps: Parse written state files as structured YAML; recursively inspect mapping keys and archive filename values.
- Expected result: No new schema key is `adapter`, `adapters`, `adapter_name`, `adapter_id`, or `adapter_archive`; lockfile entries use `target`; historical values like `rigorloop-adapter-codex-v0.3.0.zip` are allowed under target-oriented keys.
- Failure proves: Public state schemas still expose retired adapter terminology or over-reject allowed archive names.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-STATE-003. Default init preserves valid unrelated state byte-for-byte

- Covers: TNI-R15, TNI-R16, TNI-R17, TNI-R21, AC-TNI-005, E3, EC3
- Level: integration
- Fixture/setup: valid target-oriented `rigorloop.yaml` and `rigorloop.lock` recording an unrelated target/root, with exact byte snapshots.
- Steps: Run default init for another target whose root is unrelated.
- Expected result: Init may install verified target support and both state files are byte-identical after the command.
- Failure proves: Default init still reformats or rewrites managed state.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-STATE-004. Default init performs safety reads before mutating implicated roots

- Covers: TNI-R18, TNI-R19, TNI-R20
- Level: integration
- Fixture/setup: valid state files that record the selected target, overlapping roots, and conflicting target-root mappings.
- Steps: Run default init for the implicated target/root.
- Expected result: The CLI parses enough state to classify the implication before mutation and follows the matching proceed/block behavior.
- Failure proves: Byte preservation was implemented as unsafe state ignorance.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-STATE-005. Drifted or conflicting valid state blocks before mutation

- Covers: TNI-R22, error behavior 10 and 11, EC9
- Level: integration
- Fixture/setup: valid state files with selected-target entries whose recorded generated tree is missing, modified, or root-conflicting.
- Steps: Run default non-dry-run init and inspect target roots and state files after failure.
- Expected result: Command blocks before target-root mutation with bounded diagnostics and preserves state files.
- Failure proves: Managed generated-output drift can be destructively replaced.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-STATE-006. Malformed or ambiguous state blocks non-dry-run mutation

- Covers: TNI-R23, AC-TNI-010, EC5, EC6, error behavior 12 and 14
- Level: integration
- Fixture/setup: malformed `rigorloop.yaml`, malformed `rigorloop.lock`, ambiguous state shapes, and unsupported mappings.
- Steps: Run default init and `--write-state` for a target that would mutate roots.
- Expected result: Commands block before target-root mutation and give migration/fix guidance without writing state.
- Failure proves: Unsafe state can be ignored or silently rewritten.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-STATE-007. State files and diagnostics omit local or sensitive values

- Covers: TNI-R61, TNI-R69, security/privacy requirements
- Level: integration
- Fixture/setup: local archive install using an absolute archive path, proxy-related environment values, and temporary directories.
- Steps: Run `rigorloop init codex --from-archive <absolute-path> --write-state --json`.
- Expected result: Manifest records `source.type: local-archive` without absolute local paths; state files and diagnostics do not include secrets, raw proxy URLs, private hostnames, usernames, temp directories, raw env values, or request headers.
- Failure proves: State or diagnostics leak machine-local or sensitive data.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-STATE-008. Schema v3 lockfile serialization is deterministic

- Covers: TNI-R65
- Level: unit
- Fixture/setup: lockfile serializer input with targets in unsorted order.
- Steps: Serialize schema v3 lockfile content and parse it back.
- Expected result: `generated.targets` are sorted by target name and the round trip is stable.
- Failure proves: State output can churn between runs.
- Automation location: `packages/rigorloop/test/cli.test.js` or `packages/rigorloop/dist/lib/lockfile.js` unit tests.

### TTNI-MIG-001. Legacy adapter state is compatibility input and preserved by default

- Covers: TNI-R70, TNI-R71, AC-TNI-009, E7, EC4
- Level: migration
- Fixture/setup: valid legacy `rigorloop.yaml` and `rigorloop.lock` using `adapter` or `adapters`, with byte snapshots.
- Steps: Run default init for selected and unrelated targets.
- Expected result: Legacy state is parsed for safety as needed and preserved byte-for-byte by default.
- Failure proves: 0.3.0 breaks existing state files beyond the approved command-surface break.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-MIG-002. Managed-state rewrite migrates valid legacy state only after safety verification

- Covers: TNI-R72, TNI-R74, E7
- Level: migration
- Fixture/setup: valid legacy lockfile whose recorded generated roots match installed output.
- Steps: Run `rigorloop init codex --write-state`.
- Expected result: Existing generated roots are verified before rewrite, and resulting state uses target-oriented schemas.
- Failure proves: Migration rewrites state without validating managed generated output.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-MIG-003. Unsafe legacy or unsupported state blocks managed-state rewrite

- Covers: TNI-R73, EC7, EC8
- Level: migration
- Fixture/setup: duplicate selected-target entries, malformed legacy files, ambiguous shapes, and unsupported future schema versions.
- Steps: Run `rigorloop init <target> --write-state`.
- Expected result: Command blocks before mutation and does not rewrite state files.
- Failure proves: Managed-state migration can silently reinterpret unsafe state.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-MIG-004. Managed-state rewrite preserves unrelated valid entries

- Covers: TNI-R75
- Level: migration
- Fixture/setup: valid state files with multiple unrelated target entries plus the selected target.
- Steps: Run `rigorloop init <target> --write-state`.
- Expected result: Selected target entry is updated or written and unrelated valid entries remain present.
- Failure proves: State regeneration can drop user-visible managed state.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-DRY-001. Default dry-run plans target-root writes only

- Covers: TNI-R76, TNI-R77, TNI-R78, TNI-R79, TNI-R28
- Level: integration
- Fixture/setup: empty temporary project.
- Steps: Run `rigorloop init codex --dry-run --json`.
- Expected result: JSON reports planned target-root writes, writes no files, and reports no planned creation or update of `rigorloop.yaml` or `rigorloop.lock`.
- Failure proves: Dry-run still models old default state-file writes.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-DRY-002. Managed-state dry-run reports target-oriented state content

- Covers: TNI-R77, TNI-R80, EC14
- Level: integration
- Fixture/setup: empty temporary project.
- Steps: Run `rigorloop init codex --write-state --dry-run --json`.
- Expected result: JSON reports planned target-root writes plus planned target-oriented `rigorloop.yaml` and `rigorloop.lock` content, with no filesystem mutation.
- Failure proves: Managed-state planning is missing or uses retired schema keys.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-DRY-003. Dry-run with malformed state reports that non-dry-run would block

- Covers: TNI-R24, error behavior 13
- Level: integration
- Fixture/setup: malformed state file in a temporary project.
- Steps: Run default `rigorloop init codex --dry-run --json`.
- Expected result: Command may report planned target-root writes but includes a diagnostic that corresponding non-dry-run init would block before mutation.
- Failure proves: Dry-run output can mislead users about unsafe non-dry-run behavior.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-OUT-001. JSON output uses target terminology and state-action fields

- Covers: TNI-R81, TNI-R84, observability requirements
- Level: integration
- Fixture/setup: successful default init and managed-state init scenarios.
- Steps: Run commands with `--json` and parse stdout.
- Expected result: New fields identify `target`, not `adapter`; default success distinguishes skipped state-file writes from written artifacts.
- Failure proves: Public machine-readable output still exposes the retired adapter model or lacks state action observability.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-OUT-002. Human output is target-native and not JSON-fragment output

- Covers: TNI-R82, TNI-R83, TNI-R85, accessibility/UX requirements
- Level: integration
- Fixture/setup: successful default init, managed-state init, and blocker scenarios.
- Steps: Run commands without `--json`.
- Expected result: Output describes initializing target/tool support, states that default init did not write state files unless `--write-state` is used, gives concrete next actions for blockers, and does not print routine JSON fragments.
- Failure proves: Human UX still teaches adapter terminology or mixes output modes.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-META-001. Bundled metadata and release index are coherent for every target

- Covers: TNI-R36, TNI-R38, TNI-R39, TNI-R40, TNI-R41, AC-TNI-011
- Level: unit, contract
- Fixture/setup: `packages/rigorloop/dist/metadata/*.json` and release index fixtures.
- Steps: Validate each target metadata entry includes identity, release tag, archive filename, official URL, archive SHA-256, tree-hash algorithm, install roots, per-root tree hash, file count, and validation result; validate metadata hash/index binding before parse.
- Expected result: All target metadata required by the install path is present and index-verified.
- Failure proves: The package can ship stale or incomplete metadata again.
- Automation location: `packages/rigorloop/test/cli.test.js`, `scripts/test-npm-package-publication.py`, and `scripts/test-adapter-distribution.py`.

### TTNI-ARCH-001. Network and local archive modes use bundled trust roots

- Covers: TNI-R36, TNI-R37, TNI-R43
- Level: integration
- Fixture/setup: mocked network fetch and local fixture archives.
- Steps: Run network init and local `--from-archive` init.
- Expected result: Network mode fetches only the exact trusted public URL; local mode verifies archive bytes against package-bundled trusted metadata and accepts no user metadata trust root.
- Failure proves: Archive delivery can bypass package-bundled trust.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-ARCH-002. Wrong local archive identity, hash, release, or size is rejected before extraction

- Covers: TNI-R44, EC11
- Level: integration
- Fixture/setup: local archives with wrong target identity, release, filename, SHA-256, or size.
- Steps: Run `--from-archive` for a selected target using mismatched archives.
- Expected result: Each mismatch fails before extraction and leaves target roots and state files unchanged.
- Failure proves: Local archive fallback can install untrusted bytes.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-ARCH-003. Unsafe archive entries and verification failures do not claim success

- Covers: TNI-R27, TNI-R28, TNI-R45, TNI-R49
- Level: integration
- Fixture/setup: fixture archives with absolute paths, parent traversal, empty paths, drive-letter paths, unsupported symlinks, paths outside expected roots, bad metadata schema, bad hashes, and bad file counts.
- Steps: Run init using each fixture.
- Expected result: Commands fail before success and do not write state files; path safety failures happen before unsafe extraction.
- Failure proves: Archive extraction or verification boundary is unsafe.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-ARCH-004. Installed tree hash and file count verification is enforced

- Covers: TNI-R46, TNI-R47, TNI-R48, TNI-R49
- Level: unit, integration
- Fixture/setup: fixture installed trees with matching and mismatching regular files.
- Steps: Compute `rigorloop-tree-hash-v1`, compare against trusted metadata, and run init with extra, missing, or modified files.
- Expected result: Matching trees pass; mismatched tree hash or file count fails before install success or state writes.
- Failure proves: Installed output can drift from release metadata without detection.
- Automation location: `packages/rigorloop/test/cli.test.js`.

### TTNI-REL-001. Release metadata is generated from or checked against archives

- Covers: TNI-R42
- Level: contract
- Fixture/setup: generated `v0.3.0` release archives and release output directory.
- Steps: Run `python scripts/test-adapter-distribution.py` and `python scripts/validate-release.py --version v0.3.0 --release-output-dir <release-output-dir> --release-commit <commit>`.
- Expected result: Metadata file counts, archive hashes, tree hashes, and release evidence match generated archive bytes.
- Failure proves: Publication can ship stale metadata that real install rejects.
- Automation location: `scripts/test-adapter-distribution.py`, `scripts/validate-release.py`.

### TTNI-REL-002. Release validation rejects dry-run-only install smoke

- Covers: TNI-R90, AC-TNI-014, E6
- Level: contract
- Fixture/setup: release evidence fixture containing only dry-run init proof.
- Steps: Run release/package validation against the fixture.
- Expected result: Validation fails and reports that real non-dry-run packed-package smoke is required.
- Failure proves: The v0.2.0 release-smoke gap can recur.
- Automation location: `scripts/test-npm-package-publication.py`, `scripts/test-adapter-distribution.py`, `scripts/validate-release.py`.

### TTNI-SMOKE-001. Packed-package default init smoke runs for every target

- Covers: TNI-R86, TNI-R87, TNI-R89, AC-TNI-012
- Level: smoke
- Fixture/setup: packed npm package tarball, generated release archives, empty temp projects.
- Steps: Run packed-package `rigorloop init codex`, `rigorloop init claude`, and `rigorloop init opencode`.
- Expected result: Each command exits 0, installs expected roots, creates no state files, and verifies installed tree hashes and file counts against package-bundled metadata.
- Failure proves: Packaged CLI install behavior is not proven by release smoke.
- Automation location: `scripts/test-npm-package-publication.py` and release gate `RELEASE_OUTPUT_DIR=<release-output-dir> RELEASE_COMMIT=<commit> bash scripts/release-verify.sh v0.3.0`.

### TTNI-SMOKE-002. Packed-package managed-state smoke runs for every target

- Covers: TNI-R88, AC-TNI-012
- Level: smoke
- Fixture/setup: packed npm package tarball, generated release archives, empty temp projects.
- Steps: Run packed-package `rigorloop init <target> --write-state` for `codex`, `claude`, and `opencode`.
- Expected result: Each command exits 0, installs expected roots, and writes target-oriented manifest and lockfile without adapter-oriented schema keys.
- Failure proves: Managed-state behavior is not proven in the published package shape.
- Automation location: `scripts/test-npm-package-publication.py`.

### TTNI-SMOKE-003. Live post-publish registry/download smoke is recorded for every target

- Covers: TNI-R91, AC-TNI-013
- Level: manual
- Fixture/setup: published `@xiongxianfei/rigorloop@0.3.0` package and public release assets.
- Steps: After publish, run `npx @xiongxianfei/rigorloop@0.3.0 init <target>` in fresh temp projects for `codex`, `claude`, and `opencode`, then record release evidence.
- Expected result: Live registry/download init succeeds for every target and evidence names npm version, public archive URLs, installed roots, tree hashes, file counts, and command output summary.
- Failure proves: Published package or public asset delivery is broken despite pre-publish package proof.
- Automation location: release execution evidence under `docs/releases/v0.3.0/`; not required for pre-publish implementation closeout.

### TTNI-DOC-001. Public docs, help, package README, and release notes teach target-native init

- Covers: TNI-R12, TNI-R13, TNI-R92, TNI-R93, TNI-R94, AC-TNI-015
- Level: contract
- Fixture/setup: root README, package README, CLI help output, `dist/adapters/README.md`, release notes, and npm usage text.
- Steps: Assert manual quick start uses `npx @xiongxianfei/rigorloop@latest init codex`; automation examples use pinned `@0.3.0`; public surfaces do not teach `init --adapter <target>` or describe the user's action as installing an adapter; historical adapter archive filenames appear only in compatibility/internal contexts.
- Expected result: Public guidance matches the 0.3.0 command and terminology contract.
- Failure proves: Docs can send users back to the removed command or public adapter model.
- Automation location: `packages/rigorloop/test/cli.test.js`, `scripts/test-adapter-distribution.py`, and docs sweep in the active plan.

### TTNI-SKILL-001. Generated target file behavior remains unchanged

- Covers: TNI-R35, AC-TNI-016
- Level: contract
- Fixture/setup: generated archive content from canonical `skills/` and previous behavior fixtures.
- Steps: Build or inspect generated target archives and compare behavior-relevant skill content to approved canonical skill output, allowing only command/state packaging changes.
- Expected result: Codex, Claude Code, and opencode skill behavior is unchanged.
- Failure proves: The init UX change accidentally modified shipped skill behavior.
- Automation location: `python scripts/test-adapter-distribution.py` and package fixture assertions where behavior-relevant skill files are checked.

### TTNI-SEC-001. State and diagnostic privacy boundaries are enforced

- Covers: TNI-R69, security/privacy requirements
- Level: integration
- Fixture/setup: commands run with proxy-like env vars, local archive paths, and debug flags in temp directories.
- Steps: Inspect state files, JSON output, and human diagnostics for sensitive or machine-local values.
- Expected result: No secrets, credentials, raw proxy URLs, private hostnames, usernames, absolute local paths, temporary directories, raw env values, or request headers are recorded.
- Failure proves: Init leaks private runtime context into durable state or logs.
- Automation location: `packages/rigorloop/test/cli.test.js`.

## Fixtures and data

- Existing `packages/rigorloop/test/cli.test.js` helper fixtures for temporary projects, package CLI execution, JSON/human output, fixture archives, metadata overrides, local archive mode, and network mocks should be extended rather than replaced.
- Fixture archives needed for this change:
  - Codex single-root archive under `.agents/skills`;
  - Claude Code single-root archive under `.claude/skills`;
  - opencode multi-root archive under `.opencode/skills` and `.opencode/commands`;
  - older skills-only opencode archive explicitly marked compatible;
  - negative archives for wrong target identity, wrong release, wrong SHA-256, wrong size, path traversal, unsupported symlink, missing opencode alias, extra unexpected root, tree-hash mismatch, and file-count mismatch.
- State fixtures:
  - valid schema v2 `rigorloop.yaml` with `targets`;
  - valid schema v3 `rigorloop.lock` with `generated.targets`;
  - legacy adapter-oriented manifest and lockfile;
  - malformed YAML, ambiguous shapes, duplicate target entries, unsupported future schemas, drifted lockfile roots, unrelated valid entries, and conflicting root mappings.
- Release/package fixtures:
  - `v0.3.0` package metadata and release index;
  - packed npm tarball fixture or generated `npm pack` output;
  - release evidence fixtures for dry-run-only proof rejection and post-publish live evidence requirements.

## Mocking/stubbing policy

- Unit and integration tests must be hermetic. Mock network fetches or use local fixture servers; do not require live GitHub, live npm, live proxies, or external internet in normal package tests.
- Do not mock archive verification, tree hashing, file-count comparison, state-file serialization, or parser rejection in the tests that claim coverage for those behaviors.
- Packed-package smoke may use generated local tarballs before publish. Live registry/download smoke is explicitly post-publish manual or release-execution evidence.
- Environment variables used to exercise proxy/privacy behavior must be fake values and must be asserted absent from state and diagnostics.

## Migration or compatibility tests

Migration coverage is mandatory because `0.3.0` removes `--adapter` while preserving existing state files as compatibility input.

- `TTNI-MIG-001` proves legacy adapter-oriented state is byte-preserved by default.
- `TTNI-MIG-002` proves valid legacy state can be rewritten only through `--write-state` after generated-output safety checks.
- `TTNI-MIG-003` proves malformed, ambiguous, duplicate, unsupported, or unsafe state blocks managed-state rewrite.
- `TTNI-MIG-004` proves unrelated valid state entries are not silently dropped.
- `TTNI-CLI-003` proves the public CLI compatibility break is deliberate, early, and diagnostic.

## Observability verification

- JSON output tests must parse stdout and assert stable fields for selected target, source type, planned or actual roots, state-file action, warnings, blockers, errors, and safe diagnostics.
- Human output tests must assert target/tool wording, release/source/root/state action summaries, blocker next actions, and absence of routine JSON fragments.
- Release evidence validation must name packed-package smoke, live post-publish smoke, metadata/archive coherence checks, tree hashes, file counts, and docs sweep results.
- Failure diagnostics must identify verification categories without large file bodies or sensitive values.

## Security/privacy verification

- Archive extraction tests cover absolute paths, parent traversal, empty paths, drive-letter paths, unsupported symlinks, and paths outside expected roots.
- Trust-boundary tests prove user-supplied metadata is not accepted and network archive URLs come only from trusted bundled metadata.
- State and diagnostic privacy tests prove no secrets, credentials, tokens, raw proxy URLs, private hostnames, usernames, absolute local archive paths, temporary directories, raw environment values, or request headers are persisted or printed.
- Generated target files must not broaden tool permissions beyond the user's existing agent configuration; this is checked through generated archive/content validation rather than runtime permissions tests.

## Performance checks

- No standalone benchmark is required for implementation readiness.
- Tree hashing and archive verification tests should use representative fixture trees with multiple files and multi-root opencode output to catch accidental superlinear traversal behavior.
- Release smoke may be slower than dry-run smoke by design; the performance check is that dry-run remains a planning test and is not substituted for install proof.

## Manual QA checklist

- After `0.3.0` is published, run live smoke for each target:
  - `npx @xiongxianfei/rigorloop@0.3.0 init codex`
  - `npx @xiongxianfei/rigorloop@0.3.0 init claude`
  - `npx @xiongxianfei/rigorloop@0.3.0 init opencode`
- For each live smoke, verify expected target roots, no default state files, installed tree hash/file count evidence, npm version, and public archive URL.
- Record the live registry/download evidence under `docs/releases/v0.3.0/`.
- Do not treat this manual post-publish smoke as a prerequisite for pre-publish implementation closeout; pre-publish gates use packed-package smoke.

## What not to test and why

- Do not test target aliases as accepted behavior; the spec rejects aliases in the first slice.
- Do not test `rigorloop codex` as a shorthand; top-level target commands are out of scope.
- Do not test full internal renames of `dist/adapters/`, archive filenames, or package-bundled metadata fields; the approved slice defers them.
- Do not require live network access in normal package tests; live registry/download smoke belongs to post-publish release execution.
- Do not snapshot whole state files as the only assertion; parse and assert required schema keys, values, ordering, and absence of forbidden keys.
- Do not assert old `init --adapter` compatibility; `0.3.0` intentionally removes it.

## Uncovered gaps

None. Post-publish live registry/download smoke cannot run before publication, but `TTNI-SMOKE-003` defines the required manual/release-execution proof and pre-publish packed-package smoke remains automated.

## Next artifacts

- Implement M1 from the active plan using the package CLI tests first.
- Continue M2 and M3 only after the earlier milestone tests pass and the active plan is updated.
- Run code-review after each implementation milestone according to the active plan.

## Follow-on artifacts

None yet

## Readiness

Active proof surface for the approved target-native init plan. The active plan `Current Handoff Summary` owns the next workflow action; this artifact does not claim implementation, verification, release readiness, or PR readiness.
