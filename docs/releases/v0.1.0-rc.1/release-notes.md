# RigorLoop v0.1.0-rc.1

## Generated Adapter Packages

This release candidate records the generated adapter package set under `dist/adapters/` for public trial once the remaining release gate work is complete.

## Supported Tools

- `codex`: `dist/adapters/codex/`
- `claude`: `dist/adapters/claude/`
- `opencode`: `dist/adapters/opencode/`

## Skill Support

All 22 current RigorLoop skills pass the portable-core gate for Codex, Claude Code, and opencode in this release candidate package set.

No current non-portable skill exclusions.

## Known Limitations

- Manual adapter smoke has not been run yet for Codex, Claude Code, or opencode.
- Stable `v0.1.0` remains blocked until every supported tool smoke row passes with tool version and evidence.
- The release verification placeholder gate remains incomplete until `placeholder_release_check` is updated to `pass` by a later milestone.
