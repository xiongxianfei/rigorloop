# Target-Native Init Commands and Adapter Terminology Retirement

## Status

accepted

## Problem

RigorLoop's current first-run command exposes an internal packaging concept:

```bash
npx @xiongxianfei/rigorloop@latest init --adapter codex
```

That command works as a CLI shape, but `adapter` is doing the wrong job in the public UX. A new user is not trying to install an adapter. They are trying to initialize RigorLoop for the tool they use: Codex, Claude Code, or opencode.

The current README and npm usage sections repeatedly teach `init --adapter codex`, including `@latest`, pinned, project-local, and global install examples. The current CLI help also presents `rigorloop init --adapter codex|claude|opencode`. The current multi-adapter spec defines `--adapter` as the supported command contract, so this proposal intentionally changes public command direction for `0.3.0` and would need a follow-on spec amendment or replacement before implementation.

The current init command also leaves durable RigorLoop project state by default: `rigorloop.yaml` and `rigorloop.lock`. Those files are useful when the project opts into RigorLoop-managed future drift detection and update behavior, but they are friction for a first-run tool bootstrap. A user running `init codex`, `init claude`, or `init opencode` should not have to manually remove project metadata files just because they wanted verified skills installed for their tool.

The recent v0.2.0 publication incident exposed a separate but related release-quality gap: dry-run package smoke did not exercise the real metadata-validation path used by the real install command. A shorter command that fails would be worse than the current longer command, so command simplification, install-only defaults, and real non-dry-run release smoke should be handled in the same initiative.

## Goals

- Make the public first-run command use tool names directly:

  ```bash
  rigorloop init codex
  rigorloop init claude
  rigorloop init opencode
  ```

- Treat `codex`, `claude`, and `opencode` as first-class init targets in public CLI syntax, help text, README examples, npm usage, and release smoke.
- Remove `adapter` terminology from public command syntax and public user-facing prose where it describes what users do.
- Make the default target-native init command install verified tool support without creating `rigorloop.yaml` or `rigorloop.lock`.
- Generate `rigorloop.yaml` and `rigorloop.lock` only when the user explicitly asks for managed RigorLoop project state.
- Preserve the current installed file behavior for Codex, Claude Code, and opencode unless a later spec explicitly changes it.
- Publish this change as `0.3.0`.
- Remove `init --adapter <name>` entirely in `0.3.0`; do not keep a deprecated CLI alias.
- Keep the npm first-run path simple for manual trials:

  ```bash
  npx @xiongxianfei/rigorloop@latest init codex
  ```

- Require release smoke tests to run real non-dry-run init for every supported target.
- Preserve archive SHA-256, tree hash, file count, install-root, metadata, release-index, and installed-tree verification.
- Preserve lockfile-backed drift detection for the explicit managed-state mode.
- Add or strengthen metadata-vs-archive coherence validation so package-bundled metadata cannot drift from release archives again.

## Non-goals

- Do not change RigorLoop workflow semantics.
- Do not change published skill behavior or generated skill content.
- Do not change which files are installed for Codex, Claude Code, or opencode.
- Do not weaken archive verification, tree-hash verification, metadata validation, release-index validation, or release evidence.
- Do not remove package-bundled trusted metadata validation.
- Do not add a new unscoped npm package name.
- Do not make `init` the default command for arbitrary first positional arguments, such as `rigorloop codex`.
- Do not introduce a hosted service, control plane, or external registry.
- Do not rely on dry-run output as release smoke proof.
- Do not rename non-user-visible internal `dist/adapters/` paths, archive filenames, package-bundled metadata fields, or implementation names in the first slice unless the spec proves it is necessary.
- This non-goal does not apply to user-visible `rigorloop.yaml` or `rigorloop.lock` keys written by `init <target> --write-state`; those keys are in scope for target-oriented naming.
- Do not silently discard existing `rigorloop.yaml` or `rigorloop.lock` files in projects that already opted into managed state.
- Do not accept target aliases such as `claude-code`, `open-code`, `openai`, or `codex-cli` in the first slice.

## Vision fit

fits the current vision

The proposal supports RigorLoop's vision by reducing first-contact friction while preserving rigorous release evidence and trustworthy generated-output validation. It improves usability without changing the commitment to explicit artifacts, reproducible proof, and reviewable release decisions.

## Initial Intent Preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Use `init codex` directly | in scope | Goals, Recommended Direction |
| Use `init claude` directly | in scope | Goals, Recommended Direction |
| Use `init opencode` directly | in scope | Goals, Recommended Direction |
| Remove adapter terminology | in scope | Public Terminology Boundary, Scope Budget |
| Keep init simple | in scope | CLI Contract Direction |
| Do not create `rigorloop.yaml` by default | in scope | Goals, Managed State Direction |
| Do not create `rigorloop.lock` by default | in scope | Goals, Managed State Direction |
| Generate manifest and lockfile only on explicit request | in scope | Managed State Direction, Decision Log |
| Publish the change as `0.3.0` | in scope | Goals, Decision Log |
| Remove `--adapter` totally | in scope | Goals, CLI Contract Direction |
| Use `--write-state` for project state generation | in scope | Managed State Direction, Decision Log |
| Preserve existing state by default | in scope | Managed State Direction |
| Regenerate state files when `--write-state` is used | in scope | Managed State Direction |
| Avoid release incident recurrence | in scope | Release-Smoke Direction, Testing and Verification Strategy |
| Avoid broad behavior changes | in scope | Non-goals, First-Slice Boundary |
| Remove internal implementation concept completely | deferred follow-up | Internal Naming Boundary, Follow-on Artifacts |
| Decide `--adapter` compatibility | in scope | Goals, Decision Log |
| Keep release safety stronger, not weaker | in scope | Goals, Testing and Verification Strategy |

## Scope Budget

| Work item | Treatment | Reason |
|---|---|---|
| Add positional `init <target>` | core to this proposal | Primary UX improvement. |
| Support public targets `codex`, `claude`, and `opencode` | core to this proposal | These are the currently documented supported tool families. |
| Remove public command/help/docs use of `--adapter` | core to this proposal | Retires internal packaging terminology from first-run UX. |
| Update README, package README, npm usage, and CLI help | same-slice dependency | Public command contract should be taught consistently. |
| Add real non-dry-run smoke per target | same-slice dependency | Prevents recurrence of dry-run-only release smoke. |
| Add metadata-vs-archive coherence checks | same-slice dependency | Directly addresses stale and incomplete bundled metadata. |
| Make default `init <target>` install-only | core to this proposal | Removes first-run project-file cleanup burden. |
| Add explicit managed-state mode for `rigorloop.yaml` and `rigorloop.lock` | core to this proposal | Preserves drift detection and re-run state when users ask for it. |
| Define behavior when existing project state files are present | same-slice dependency | Avoids silently ignoring or corrupting already-managed projects. |
| Remove `--adapter` in `0.3.0` | core to this proposal | Owner chose a breaking release instead of a deprecation window. |
| Update current multi-adapter spec to target-native syntax | same-slice dependency | The current spec requires `--adapter`; implementation should not diverge silently. |
| Update current manifest and lockfile specs to install-only default | same-slice dependency | Existing specs require durable files on successful init. |
| Rename public release evidence wording from adapter to target/tool where practical | first-slice candidate | User-facing release notes and docs should follow the new language, but historical artifact names may remain. |
| Rename user-visible manifest and lockfile keys from `adapters` / `adapter` | core to this proposal | Owner chose not to continue user-visible `adapter` keys. |
| Rename internal `dist/adapters/`, archive filenames, and package-bundled metadata field names | separate implementation slice | These are broader release-artifact and validator churn; keep unless proposal review chooses full internal rename. |
| Change npm package name | out of scope | Higher migration cost than command simplification. |
| Add command aliases such as `claude-code` or `open-code` | deferable follow-up | Extra accepted forms increase support and test surface. |
| Add new target types | out of scope | This proposal only covers currently supported tool families. |

## Context

The current public README teaches `init --adapter codex` in Quick Start, direct `npx`, pinned, project-local, and global install examples. It also describes generated adapter packages and current install roots:

| Tool | Current release archive | Current install root |
|---|---|---|
| Codex | `rigorloop-adapter-codex-<version>.zip` | `.agents/skills/` |
| Claude Code | `rigorloop-adapter-claude-<version>.zip` | `.claude/skills/` |
| opencode | `rigorloop-adapter-opencode-<version>.zip` | `.opencode/skills/` |

The current CLI and accepted multi-adapter spec use adapter descriptors internally to select archive names, expected roots, required roots, and lockfile shape. The current specs also require successful non-dry-run init to create `rigorloop.yaml` and then create or update `rigorloop.lock` after verification. This proposal changes that public default for `0.3.0`: users initialize a tool; the CLI may still use descriptors internally, and managed project state remains available only when explicitly requested.

The v0.2.0 publication incident showed that release smoke must exercise the real public install path. The published package bundled Codex metadata without `file_count`, and with a stale `tree_sha256`. Existing dry-run smoke did not catch that because dry-run network mode intentionally does not load and validate bundled metadata.

External distribution context supports the `npx` first-run model: `npx` runs commands from npm packages without a prior project install, which fits RigorLoop's zero-install trial path. RigorLoop currently exposes one package binary, `rigorloop`, so public examples can remain short without adding a new package.

## Public Terminology Boundary

This proposal retires `adapter` as public command and user-task language.

Preferred public vocabulary:

| Current term | Preferred public term |
|---|---|
| adapter | target or tool |
| adapter name | target |
| adapter archive | release archive, target archive, or skill bundle archive |
| adapter install | target init or tool support initialization |
| adapter metadata | install metadata or target metadata |
| adapter manifest | install manifest or target manifest |

Preferred phrasing:

```text
Initialize RigorLoop for Codex:

npx @xiongxianfei/rigorloop@latest init codex
```

Avoid new public prose such as:

```text
Install the Codex adapter.
```

Use:

```text
Install RigorLoop skills for Codex.
```

or:

```text
Initialize Codex support.
```

This boundary applies to public UX and user-visible state created by the `0.3.0` CLI.

The following surfaces must use target/tool terminology in this proposal:

- public CLI syntax and help;
- README, package README, npm usage, and release notes guidance;
- new `rigorloop.yaml` content written by `--write-state`;
- new `rigorloop.lock` content written by `--write-state`.

The following non-user-visible or historical internals may continue to use `adapter` until a later compatibility-sensitive migration:

- internal code names;
- `dist/adapters/` paths;
- archive filenames;
- package-bundled metadata field names;
- historical release evidence;
- existing state files preserved unchanged by default init.

## Options Considered

### Option 1: Keep current `init --adapter <name>`

Pros:

- No compatibility risk.
- No parser changes.
- No documentation migration.

Cons:

- Continues exposing internal packaging terminology.
- Keeps the first-run command longer than needed.
- Does not match the user's tool-native mental model.
- Does not address the release-smoke gap unless paired with separate validation work.

### Option 2: Add `init <target>` and keep `--adapter` as a documented alias

Pros:

- Backward compatible.
- Easy migration.
- Low immediate support risk.

Cons:

- Public docs may teach both forms and create ambiguity.
- `adapter` remains a public concept indefinitely.
- More accepted forms require durable tests.

### Option 3: Add `init <target>`, remove `--adapter` from docs, keep `--adapter` as a hidden deprecated compatibility alias for one release window

Pros:

- New users see only the simple target-native command.
- Existing documented users are not immediately broken.
- The deprecation window can produce warning and migration guidance.
- Support and test surface is bounded and temporary.

Cons:

- `adapter` remains in code temporarily.
- Requires deprecation diagnostics and tests.
- Requires a removal milestone or explicit extension decision.

### Option 4: Hard-remove `--adapter` immediately

Pros:

- Clearest public model.
- Fully removes `adapter` from CLI syntax immediately.

Cons:

- Breaks current README-documented usage.
- Requires a breaking-release decision.
- Increases risk immediately after a publication incident.

### Option 5: Make the tool target the top-level command, such as `rigorloop codex`

Pros:

- Shortest command after package name.

Cons:

- Surprising command parsing.
- Harder to extend.
- Collides with future top-level commands.
- Makes behavior depend on first-argument shape.

This option is rejected for the first slice.

### Option 6: Keep writing `rigorloop.yaml` and `rigorloop.lock` by default

Pros:

- Preserves current drift detection and managed-project semantics.
- Requires less change to current manifest and lockfile specs.
- Makes future re-runs easier to reason about for managed projects.

Cons:

- Leaves cleanup burden on first-run users who only wanted tool skills installed.
- Makes the zero-install bootstrap feel heavier than the command suggests.
- Keeps `init codex` from being a clean, low-friction first contact.

### Option 7: Make default init install-only and add explicit managed state

Pros:

- Matches the first-run user intent: install verified skills for the selected tool.
- Avoids leaving `rigorloop.yaml` and `rigorloop.lock` unless the user asks for project state.
- Preserves managed drift detection and re-run state as an opt-in mode.
- Creates a clearer split between "bootstrap tool support" and "let RigorLoop manage this project."

Cons:

- Requires spec changes to current manifest and lockfile contracts.
- Requires careful behavior when existing managed-state files already exist.
- Requires a new explicit CLI affordance for managed state.
- Default installs without lockfiles cannot later prove drift from local state alone unless the command re-verifies from metadata or the user opts into managed state.

## Recommended Direction

Choose Option 4 and publish it as `0.3.0`.

Also choose Option 7 for project-state behavior: default target-native init should be install-only, and managed state should be explicit.

Canonical public commands:

```bash
rigorloop init codex
rigorloop init claude
rigorloop init opencode
```

By default, those commands should:

- verify the package-bundled trusted metadata;
- download or read the selected release archive;
- verify archive hash, install roots, tree hash, and file count;
- install the verified target files;
- avoid creating `rigorloop.yaml`;
- avoid creating `rigorloop.lock`.

The explicit managed-state syntax is:

```bash
rigorloop init codex --write-state
```

`--write-state` installs the target and records durable RigorLoop project state through `rigorloop.yaml` and `rigorloop.lock`. Default init preserves existing state files without mutating them; `--write-state` regenerates those files after verification.

Human-facing npm command:

```bash
npx @xiongxianfei/rigorloop@latest init codex
```

Automation and reproducible setup command:

```bash
npx @xiongxianfei/rigorloop@0.3.0 init codex
```

`--adapter` is not accepted in `0.3.0`. The follow-on spec and release notes should treat this as a breaking CLI cleanup from the documented `0.2.0` command form.

## CLI Contract Direction

Canonical syntax:

```text
rigorloop init <target> [--dry-run] [--json]
```

Managed-state syntax:

```text
rigorloop init <target> --write-state [--dry-run] [--json]
```

Allowed first-slice targets:

```text
codex
claude
opencode
```

Recommended first-slice alias policy:

```text
accept only codex, claude, and opencode
```

Rejected invalid or removed forms:

```bash
rigorloop init codex --adapter claude
rigorloop init --adapter codex claude
rigorloop init --adapter codex
rigorloop init
rigorloop init adapter codex
rigorloop init claude-code
rigorloop init open-code
```

Expected diagnostic direction:

```text
init requires exactly one target: codex, claude, or opencode
```

For any `--adapter` use:

```text
`--adapter` was removed in RigorLoop 0.3.0. Use `init codex`, `init claude`, or `init opencode`.
```

## Managed State Direction

Default `init <target>` should be an install-only bootstrap:

```text
verified archive -> verified files under target root(s) -> no RigorLoop project metadata files
```

Explicit `--write-state` init should be the path that writes RigorLoop project metadata:

```text
verified archive -> verified files under target root(s) -> rigorloop.yaml -> rigorloop.lock
```

The managed-state files still have valid roles:

- `rigorloop.yaml` records the project-level target configuration and source mode.
- `rigorloop.lock` records verified generated-output state for drift detection and reproducible re-runs.

Those roles should be opt-in because the default public command is a tool bootstrap, not a declaration that the project is now managed by RigorLoop.

Existing managed projects have explicit behavior:

- Default `init <target>` preserves existing `rigorloop.yaml` and `rigorloop.lock` unchanged.
- `init <target> --write-state` regenerates `rigorloop.yaml` and `rigorloop.lock` after target install verification succeeds.
- The spec should still define failure behavior for malformed existing state files, but the proposal direction is that `--write-state` owns replacement of the state files.

## State-File Schema Boundary

Default `init <target>` is install-only and must not create `rigorloop.yaml` or `rigorloop.lock`.

If existing `rigorloop.yaml` or `rigorloop.lock` files are present, default `init <target>` preserves them unchanged.

`init <target> --write-state` writes or regenerates `rigorloop.yaml` and `rigorloop.lock` after verified install.

New state files written by `--write-state` must use target-oriented user-visible keys, not `adapter` or `adapters`.

Existing state files that contain legacy `adapter` keys are compatibility input. The spec must define whether `--write-state` migrates them, rewrites them, or fails with migration guidance.

Recommended compatibility rule:

```text
Default init:
  preserve legacy state files unchanged.

--write-state:
  rewrite to the new target-oriented schema after successful verification.

Malformed or ambiguous existing state:
  block with migration guidance instead of silently rewriting.
```

## Internal Naming Boundary

First slice should use a split terminology boundary.

User-visible state keys in `rigorloop.yaml` and `rigorloop.lock` should not continue to use `adapter`. The follow-on spec should rename those shapes to target-oriented terms because `--write-state` creates user-visible files.

Internal implementation names such as `dist/adapters/`, adapter descriptors, archive filenames, and package-bundled release metadata field names may remain for this slice unless they appear in public docs or proposal review decides full internal rename is required.

Track B would rename internal implementation surfaces from adapter to target or skill bundle. That may be desirable later, but it is a broad compatibility-sensitive refactor touching archive names, validators, lockfiles, release evidence, scripts, and historical docs.

The first-slice boundary is:

```text
remove adapter from public UX;
rename user-visible state-file keys away from adapter;
keep non-user-visible internal adapter implementation names for compatibility unless separately approved.
```

## Release-Smoke Direction

Release smoke should run the command users run. Dry-run remains useful for planning and JSON shape tests, but it is not install-success proof.

Required per target before publication:

```bash
rigorloop init codex
rigorloop init claude
rigorloop init opencode
```

Packed-package equivalent:

```bash
npx --package <packed-tarball> rigorloop init codex
```

The exact command should be implemented with repository-owned scripts and hermetic temporary projects. The pre-publish gate should use packed package smoke with locally generated release archives or controlled fixture archives. The post-publish gate should run live registry/download smoke against the published npm package and GitHub release assets.

Required release-check direction:

1. Build release archives.
2. Derive or validate install metadata from the archive bytes.
3. Verify archive hash, tree hash, file count, install roots, and release-index metadata hash.
4. Install from the packed npm package into an empty temp project.
5. Run real non-dry-run `init <target>`.
6. Verify installed tree exists at the expected root or roots.
7. Verify installed tree hash and file count match metadata.
8. Verify command exits `0`.
9. Verify default init does not create `rigorloop.yaml` or `rigorloop.lock`.
10. Verify `init <target> --write-state` regenerates `rigorloop.yaml` and `rigorloop.lock` after verification.
11. Verify public docs no longer teach `--adapter`.
12. Verify live registry/download smoke passes after publication.

## Expected Behavior Changes

- Users initialize a tool directly:

  ```bash
  rigorloop init codex
  ```

- README and npm usage stop teaching `--adapter`.
- CLI help lists targets, not adapters.
- `--adapter` is removed in `0.3.0`; any use fails with migration guidance.
- Mixed positional and removed target forms fail deterministically.
- Default `init <target>` installs verified target files without writing `rigorloop.yaml` or `rigorloop.lock`.
- `init <target> --write-state` writes or replaces `rigorloop.yaml` and `rigorloop.lock` only after verification.
- Default init preserves existing `rigorloop.yaml` and `rigorloop.lock` unchanged.
- Real release smoke uses non-dry-run target-native commands.
- Package-bundled metadata is checked against release archive contents.
- Installed skill content and generated archive contents remain unchanged except for metadata or naming surfaces required by the new command contract.

## Architecture Impact

| Surface | Impact |
|---|---|
| CLI parser | Add positional target support for `init`; reject removed `--adapter` forms. |
| CLI help | Replace public adapter terminology with target/tool terminology. |
| Init command tests | Add canonical, removed-option, mixed-invalid, unknown-target, and dry-run cases. |
| README and package README | Replace `init --adapter codex` with `init codex`; add target examples where appropriate. |
| Release process and validators | Add real non-dry-run packed-package smoke per target. |
| Metadata validation | Check bundled metadata against archive tree hash and file count for each target/root shape. |
| Existing multi-adapter spec | Amend or supersede `--adapter` requirements with target-native command requirements. |
| Existing manifest and lockfile specs | Amend current default-write requirements so durable state is explicit rather than default. |
| Managed-state parser option | Add `--write-state` for writing `rigorloop.yaml` and `rigorloop.lock`. |
| `dist/adapters/README.md` | Update public wording while preserving necessary implementation and historical notes. |
| Adapter archive internals | Keep `dist/adapters/`, archive filenames, and non-user-visible metadata fields unless the spec chooses full internal rename. |
| Lockfile and manifest schemas | Rename user-visible state-file keys away from `adapter` for `--write-state`. |

## Testing and Verification Strategy

Planned test coverage:

| Check ID | What is verified |
|---|---|
| `TINIT-001` | `rigorloop init codex` succeeds and installs Codex target support. |
| `TINIT-002` | `rigorloop init claude` succeeds and installs Claude Code target support. |
| `TINIT-003` | `rigorloop init opencode` succeeds and installs opencode target support. |
| `TINIT-004` | `rigorloop init --adapter codex` fails in `0.3.0` with migration guidance. |
| `TINIT-005` | Mixed positional and `--adapter` target forms fail. |
| `TINIT-006` | Unknown targets fail with the allowed target list. |
| `TINIT-007` | `--dry-run --json` works with positional target and does not claim install success. |
| `TINIT-008` | Real non-dry-run smoke runs from packed npm package for every target. |
| `TINIT-009` | Package-bundled metadata matches each target archive. |
| `TINIT-010` | README, package README, and CLI help no longer teach `--adapter`. |
| `TINIT-011` | New public docs do not describe users as installing adapters. |
| `TINIT-012` | Existing archive verification remains unchanged or stronger. |
| `TINIT-013` | No aliases are accepted; only `codex`, `claude`, and `opencode` are valid targets. |
| `TINIT-014` | Default `init <target>` does not create `rigorloop.yaml` or `rigorloop.lock`. |
| `TINIT-015` | `init <target> --write-state` creates or replaces `rigorloop.yaml` and `rigorloop.lock` only after verified install. |
| `TINIT-016` | Default init preserves existing `rigorloop.yaml` and `rigorloop.lock` unchanged. |
| `TINIT-017` | `--write-state` output uses target-oriented user-visible keys, not `adapter` keys. |
| `TINIT-018` | Pre-publish packed archive smoke and post-publish live registry/download smoke both run for each target. |
| `TINIT-019` | Legacy state files with `adapter` keys have explicit migration, rewrite, or block behavior in the spec. |
| `TINIT-020` | Non-user-visible archive filenames, `dist/adapters/`, and package-bundled metadata field names are not renamed in the first slice unless the spec explicitly expands scope. |

Suggested validation surfaces:

```bash
npm test --prefix packages/rigorloop
python scripts/test-npm-package-publication.py
python scripts/test-adapter-distribution.py
python scripts/validate-adapters.py --root <release-output-dir> --version <version>
bash scripts/release-verify.sh <version>
git diff --check --
```

The follow-on plan should use repository-owned actual command names and add any missing targeted scripts rather than relying on ad hoc shell smoke.

## Behavior-Preservation Proof Direction

The implementation change should create change-local behavior preservation evidence, likely:

```text
docs/changes/<change-id>/behavior-preservation.md
```

Minimum matrix:

| Surface | Baseline | New proof | Preservation result |
|---|---|---|---|
| Codex install | `init --adapter codex` installed same tree | `init codex` installs same tree | preserved |
| Claude install | current archive install proof | `init claude` installs same tree | preserved |
| opencode install | current archive install proof | `init opencode` installs same tree | preserved |
| JSON dry run | `init --adapter codex --dry-run --json` | `init codex --dry-run --json` | same shape except target terminology |
| Project files by default | current init creates `rigorloop.yaml` and `rigorloop.lock` | default `init codex` creates neither file | intentionally changed |
| Managed project files | current init writes project state | explicit managed mode writes project state after verification | preserved by opt-in |
| Metadata validation | current archive metadata check | metadata generated or checked from archive | strengthened |
| Release smoke | dry-run or partial smoke | real non-dry-run smoke | strengthened |
| Docs | adapter form | target-native form | improved |
| Compatibility | current `--adapter` | `0.3.0` rejects `--adapter` with migration guidance | breaking cleanup |
| State-file keys | current state files use `adapter` keys | `--write-state` emits target-oriented keys | intentionally changed |

## Rollout and Rollback

Rollout:

1. Accept this proposal after proposal review.
2. Write or amend the target-native init spec, including `0.3.0` breaking removal, install-only default, `--write-state`, target-oriented state-file keys, and release-smoke contract.
3. Review the spec before implementation.
4. Write a matching test spec for CLI parsing, removed-option behavior, docs sweep, release smoke, and metadata-vs-archive coherence.
5. Plan the implementation with a small first slice.
6. Implement `init <target>`, install-only default behavior, `--write-state`, removed `--adapter` diagnostics, and target-oriented state-file output.
7. Update README, package README, CLI help, release notes guidance, and public install docs.
8. Add real non-dry-run packed-package smoke per target.
9. Add metadata-vs-archive coherence checks.
10. Publish `0.3.0` only after pre-publish packed archive smoke passes.
11. Run post-publish live registry/download smoke after `0.3.0` is available.
12. Run code review, explain-change, verify, and PR handoff before release.

Rollback:

- Keep `0.2.x` as the last line that supports `init --adapter <name>` if the `0.3.0` parser is not ready.
- Revert docs to the old command only if `0.3.0` is not shipped.
- Do not remove metadata-vs-archive checks; they are a release-quality improvement independent of command UX.
- Do not publish a version whose README teaches a command the CLI does not support.
- If a version ships with broken init behavior, fix forward with a new version because npm versions are immutable once published.

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Existing users break | Publish as `0.3.0` and document the breaking command replacement. |
| Too many accepted command forms | Accept only `init <target>` and `init <target> --write-state`; reject aliases and `--adapter`. |
| Public/internal terminology drift | Public docs and user-visible state files use target/tool; non-user-visible internal adapter terms are tracked for later rename. |
| Release smoke misses real install path again | Require non-dry-run packed install smoke per target. |
| Metadata drifts from archive | Validate bundled metadata against archive hash, tree hash, and file count. |
| `claude` target ambiguity | Canonical target is `claude`; defer aliases unless tested and documented. |
| Docs still mention adapter in public guidance | Add docs sweep plus human review for public surfaces. |
| Full internal rename causes churn | Defer non-user-visible path/archive/metadata renames unless separately justified. |
| Current spec conflicts with proposal direction | Amend or supersede the current multi-adapter init spec before implementation. |
| Manifest/lockfile still expose `adapter` keys | Rename user-visible state-file keys in the `--write-state` contract. |
| Default install loses local drift record | Keep explicit managed-state mode and make release smoke verify installed tree directly from trusted metadata. |
| Existing managed projects become ambiguous | Default init preserves existing state; `--write-state` regenerates state files after verification. |
| Users need project files later | Provide `--write-state` to generate them on demand after verification. |

## Open Questions

None for proposal readiness.

Owner decisions recorded on 2026-05-24:

- Publish as `0.3.0`.
- Remove `--adapter` totally; do not keep a deprecated alias.
- Accept only `codex`, `claude`, and `opencode`.
- Show `@latest` for manual quick start; show pinned versions for automation and reproducible setup.
- Use packed archive smoke before publish and live registry/download smoke after publish.
- Do not continue user-visible `adapter` keys in `rigorloop.yaml` and `rigorloop.lock`.
- Use `rigorloop init <target> --write-state` for state generation.
- Preserve existing state files with default init.
- Regenerate `rigorloop.yaml` and `rigorloop.lock` when `--write-state` is used.

The remaining detail for spec work is exact state-file schema shape after replacing `adapter` terminology with target-oriented keys.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-05-24 | Prefer target-native `init <target>` commands. | Matches user mental model and shortens first-run command. | Keep `--adapter` canonical. |
| 2026-05-24 | Retire `adapter` terminology from public UX first. | `adapter` is an internal packaging concept for most users. | Continue teaching adapter as public concept. |
| 2026-05-24 | Keep internal rename separate. | Full rename risks release/archive/schema churn. | Rename all internal adapter paths now. |
| 2026-05-24 | Require real non-dry-run release smoke. | Dry-run missed the metadata-validation failure. | Dry-run-only release smoke. |
| 2026-05-24 | Use `@latest` for human Quick Start and pinned versions for automation. | Balances freshness and reproducibility. | Pin every public quick-start command. |
| 2026-05-24 | Make target-native init install-only by default. | Users should not manually remove `rigorloop.yaml` or `rigorloop.lock` after a simple tool bootstrap. | Always write project manifest and lockfile. |
| 2026-05-24 | Keep `rigorloop.yaml` and `rigorloop.lock` behind explicit managed-state opt-in. | Preserves managed drift detection for users who ask for it. | Remove durable state support entirely. |
| 2026-05-24 | Publish the breaking command cleanup as `0.3.0`. | Removing `--adapter` breaks documented `0.2.0` usage and should not be hidden in a patch release. | Compatibility alias in a minor release window. |
| 2026-05-24 | Remove `--adapter` totally in `0.3.0`. | The public UX should not keep adapter terminology alive. | Hidden deprecated alias. |
| 2026-05-24 | Accept only `codex`, `claude`, and `opencode` targets. | Keeps the supported command contract small and testable. | Add `claude-code`, `open-code`, or other aliases. |
| 2026-05-24 | Use `--write-state` for explicit state-file generation. | The flag states the side effect directly. | `--managed`, `--record-state`, or a separate command. |
| 2026-05-24 | Preserve existing `rigorloop.yaml` and `rigorloop.lock` in default init. | Default install-only behavior should not mutate project state. | Treat existing files as implicit managed mode. |
| 2026-05-24 | Regenerate state files when `--write-state` is used. | Explicit state writing should produce current state after verification. | Require manual deletion or only update missing files. |
| 2026-05-24 | Rename user-visible state-file keys away from `adapter`. | User-visible state should match target-native terminology. | Keep `adapter` keys in `rigorloop.yaml` and `rigorloop.lock`. |
| 2026-05-24 | Keep non-user-visible `dist/adapters/`, archive filenames, and internal metadata field names unless a later review requires full rename. | Avoid broad release-artifact churn while removing public command and state-file terminology. | Rename every internal adapter path and archive in the same slice. |
| 2026-05-24 | Split smoke gates between packed archive pre-publish and live registry/download post-publish. | Pre-publish should be deterministic; post-publish should prove real public assets. | Use only dry-run or only live smoke. |

## Next Artifacts

- `proposal-review`
- Spec or spec amendment for target-native init command, `0.3.0` breaking removal of `--adapter`, install-only default, `--write-state`, target-oriented state-file keys, and public adapter terminology retirement.
- Spec review.
- Test spec for CLI parsing, removed `--adapter` behavior, install-only default, `--write-state`, release smoke, docs sweep, and metadata-vs-archive validation.
- Architecture or ADR only if spec review determines schema naming, release artifact ownership, or internal rename decisions need one.
- Execution plan and plan review.
- Implementation, code review, explain-change, verify, and PR handoff.

## Follow-on Artifacts

None yet

Potential follow-on work after this proposal is settled:

- Proposal for full internal rename from `adapter` to `target` or `skill-bundle`.
- Proposal for an unscoped or shorter npm package name if adoption evidence justifies it.
- Proposal for additional init targets.
- Proposal for command aliases after target-native init has shipped and usage is measured.

## Readiness

Accepted after proposal-review.

This proposal is ready for a target-native init spec or spec amendment covering command syntax, default install-only behavior, explicit `--write-state`, target-oriented state files, and release-smoke ownership.

## References

- Current README and npm usage in `README.md` and `packages/rigorloop/README.md`.
- Current CLI command surface in `packages/rigorloop/dist/bin/rigorloop.js`.
- Current multi-adapter command contract in `specs/multi-adapter-init-and-proxy-aware-download.md`.
- Publication incident learn record in `docs/learn/sessions/2026-05-24-adapter-metadata-publication-gap.md`.
- npm `npx` command documentation: <https://docs.npmjs.com/cli/v8/commands/npx/>
