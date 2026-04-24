# RigorLoop v0.1.0-rc.1

## Generated Adapter Packages

This release candidate records the generated adapter package set under `dist/adapters/` for public trial. Install one adapter by copying that adapter package root into a project root.

## Supported Tools

- `codex`: `dist/adapters/codex/`
- `claude`: `dist/adapters/claude/`
- `opencode`: `dist/adapters/opencode/`

## Skill Support

All 22 current RigorLoop skills pass the portable-core gate for Codex, Claude Code, and opencode in this release candidate package set.

These adapter compatibility claims are versioned for `v0.1.0-rc.1`. If external tool contracts change, update the affected adapter contract through the RigorLoop lifecycle before changing release claims.

No current non-portable skill exclusions.

## Verification

The repository-owned release gate is `bash scripts/release-verify.sh v0.1.0-rc.1`. It checks canonical skills, generated `.codex/skills/`, generated adapter drift, adapter validation, release metadata, release notes, and security scans without requiring ordinary contributors to install all supported tools.

## Known Limitations

- Manual adapter smoke has not been run yet for Codex, Claude Code, or opencode.
- Stable `v0.1.0` remains blocked until every supported tool smoke row passes with tool version and evidence.
