# RigorLoop v0.1.2

## Generated Adapter Packages

This archive-introduction release keeps the generated adapter package set under `dist/adapters/` for the compatibility window and adds downloadable adapter archives for forward migration.

`skills/` is the canonical authored skill source. `dist/adapters/` remains the repository-tree adapter install path during the compatibility window.

For `v0.1.2`, tracked `dist/adapters/**/skills` remain available for the compatibility window.

Adapter artifact checksums and metadata are recorded in `docs/reports/adapter-artifacts/releases/v0.1.2.yaml`.

## Supported Tools

- `codex`: `dist/adapters/codex/`
- `claude`: `dist/adapters/claude/`
- `opencode`: `dist/adapters/opencode/`

## Skill Support

All 22 current RigorLoop skills pass the portable-core gate for Codex, Claude Code, and opencode in this stable package set.

These adapter compatibility claims preserve the `0.1.1` repository-tree adapter support matrix while `v0.1.2` introduces release archives. If external tool contracts change, update the affected adapter contract through the RigorLoop lifecycle before changing release claims.

No current non-portable skill exclusions.

## Command Alias Usage

OpenCode command aliases are generated for `proposal`, `proposal-review`, `spec`, `spec-review`, `plan`, `plan-review`, `test-spec`, `implement`, `code-review`, and `pr`.

OpenCode TUI examples:

```text
/proposal Evaluate whether this change should be specified.
/spec Define the observable behavior for this change.
/implement Build the approved milestone with tests first.
/code-review Review the current diff against the approved artifacts.
/pr Prepare the verified change for pull request review.
```

OpenCode one-shot example:

```text
opencode run --command proposal "Draft a proposal for the requested change."
```

Claude Code remains skill-native and uses native skill slash commands such as `/proposal`, `/spec`, `/implement`, `/code-review`, and `/pr`. This release does not generate `.claude/commands/` wrappers.

## Adapter Archives

Per-adapter release archives are available for `v0.1.2`:

- `rigorloop-adapter-codex-v0.1.2.zip` installs to `.agents/skills/`.
- `rigorloop-adapter-claude-v0.1.2.zip` installs to `.claude/skills/`.
- `rigorloop-adapter-opencode-v0.1.2.zip` installs to `.opencode/skills/`.

## Smoke Verification

Maintainer smoke passed for every supported repository-tree adapter package:

- Codex: `codex-cli 0.124.0`
- Claude Code: `2.1.119 (Claude Code)`
- opencode: `1.14.22`

Codex and Claude Code smoke checks copied only the target adapter package into a clean project root and verified the expected instruction entrypoint plus `workflow` skill path. OpenCode smoke verified the `opencode run --command proposal` one-shot command alias form by running it against a copied adapter root, loading the `proposal` skill, and repeating `ARGUMENT_MARKER_M3_SMOKE` from the command arguments.

## Verification

The repository-owned release gate is `bash scripts/release-verify.sh v0.1.2`. It checks canonical skills, tracked public adapter output under `dist/adapters/`, generated adapter archives, adapter artifact metadata, release metadata, release notes, and security scans without requiring ordinary contributors to install all supported tools.

## Known Limitations

- The repository-tree adapter package set remains available for the compatibility window.
- Adapter packages are generated project-local files; behavior still depends on each tool's own runtime support for project instructions, skills, and command aliases.
