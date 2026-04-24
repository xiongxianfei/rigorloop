# RigorLoop v0.1.1

## Generated Adapter Packages

This stable patch release records the generated adapter package set under `dist/adapters/`. Install one adapter by copying that adapter package root into a project root.

## Supported Tools

- `codex`: `dist/adapters/codex/`
- `claude`: `dist/adapters/claude/`
- `opencode`: `dist/adapters/opencode/`

## Skill Support

All 22 current RigorLoop skills pass the portable-core gate for Codex, Claude Code, and opencode in this stable package set.

These adapter compatibility claims are versioned for `v0.1.1`. If external tool contracts change, update the affected adapter contract through the RigorLoop lifecycle before changing release claims.

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

## Smoke Verification

Maintainer smoke passed for every supported adapter package:

- Codex: `codex-cli 0.124.0`
- Claude Code: `2.1.119 (Claude Code)`
- opencode: `1.14.22`

Codex and Claude Code smoke checks copied only the target adapter package into a clean project root and verified the expected instruction entrypoint plus `workflow` skill path. OpenCode smoke verified the `opencode run --command proposal` one-shot command alias form by running it against a copied adapter root, loading the `proposal` skill, and repeating `ARGUMENT_MARKER_M3_SMOKE` from the command arguments.

## Verification

The repository-owned release gate is `bash scripts/release-verify.sh v0.1.1`. It checks canonical skills, generated `.codex/skills/`, generated adapter drift, adapter validation, release metadata, release notes, and security scans without requiring ordinary contributors to install all supported tools.

## Known Limitations

- No hosted runtime, registry publication, or package-manager installer is included in this release.
- Adapter packages are generated project-local files; behavior still depends on each tool's own runtime support for project instructions, skills, and command aliases.
