# RigorLoop v0.1.0

## Generated Adapter Packages

This stable release records the generated adapter package set under `dist/adapters/`. Install one adapter by copying that adapter package root into a project root.

## Supported Tools

- `codex`: `dist/adapters/codex/`
- `claude`: `dist/adapters/claude/`
- `opencode`: `dist/adapters/opencode/`

## Skill Support

All 22 current RigorLoop skills pass the portable-core gate for Codex, Claude Code, and opencode in this stable package set.

These adapter compatibility claims are versioned for `v0.1.0`. If external tool contracts change, update the affected adapter contract through the RigorLoop lifecycle before changing release claims.

No current non-portable skill exclusions.

## Smoke Verification

Maintainer smoke passed for every supported adapter package:

- Codex: `codex-cli 0.124.0`
- Claude Code: `2.1.119 (Claude Code)`
- opencode: `1.14.22`

Each smoke check copied only the target adapter package into a clean project root and verified the expected instruction entrypoint plus `workflow` skill path.

## Verification

The repository-owned release gate is `bash scripts/release-verify.sh v0.1.0`. It checks canonical skills, generated `.codex/skills/`, generated adapter drift, adapter validation, release metadata, release notes, and security scans without requiring ordinary contributors to install all supported tools.

## Known Limitations

- No hosted runtime, registry publication, or package-manager installer is included in this release.
- Adapter packages are generated project-local files; behavior still depends on each tool's own runtime support for project instructions and skills.
