# RigorLoop Adapter Packages

Generated adapter packages are produced from canonical `skills/`.

Do not edit generated adapter skill files by hand. `skills/` is the only authored skill source.

## Current Repository-Tree Install

For `v0.1.1`, generated adapter skill copies under `dist/adapters/` remain tracked installable output and the public adapter install path.

For `v0.1.2`, tracked adapter skill bodies under `dist/adapters/**/skills` remain available for the compatibility window while release assets introduce the forward archive install path.

The repository-tree install path remains available during the compatibility window. To install one adapter from the repository tree, copy that adapter package root's contents into a project root:

| Adapter | Package root | Skill install root |
| --- | --- | --- |
| Codex | `dist/adapters/codex/` | `.agents/skills/` |
| Claude Code | `dist/adapters/claude/` | `.claude/skills/` |
| opencode | `dist/adapters/opencode/` | `.opencode/skills/` |

`dist/adapters/manifest.yaml` remains the tracked adapter support matrix and package metadata. It records adapter support and opencode command aliases; it must not contain generated skill bodies.

## Release Artifact Migration

No downloadable adapter archives are required for `v0.1.1`. `dist/adapters/` remains the public adapter install path for this transition release.

For `v0.1.2`, download adapter archives from GitHub release assets when using the forward archive install path:

| Adapter | Archive name | Target install root |
| --- | --- | --- |
| Codex | `rigorloop-adapter-codex-<version>.zip` | `.agents/skills/` |
| Claude Code | `rigorloop-adapter-claude-<version>.zip` | `.claude/skills/` |
| opencode | `rigorloop-adapter-opencode-<version>.zip` | `.opencode/skills/` |

The release artifact metadata and checksums are recorded under `docs/reports/adapter-artifacts/releases/<version>.yaml`.

Generated adapter skill bodies are not tracked source after the later untracking release; install generated adapter skill bodies from release assets instead of treating `dist/adapters/**/skills` as authored source.

`.codex/skills/` is an ignored local runtime install directory and not a public adapter install source. For local Codex use, install or copy public Codex adapter output from `dist/adapters/codex/.agents/skills/` into `.codex/skills/`.
