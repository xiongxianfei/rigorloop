# RigorLoop Adapter Packages

Generated adapter packages are produced from canonical `skills/`.

Do not edit generated adapter skill files by hand. `skills/` is the only authored skill source.

## Current Repository-Tree Install

During the public adapter compatibility window, generated adapter skill copies under `dist/adapters/` remain tracked installable output. This repository-tree install path remains valid until release assets replace it in a later release.

To install one adapter from the repository tree, copy that adapter package root's contents into a project root:

| Adapter | Package root | Skill install root |
| --- | --- | --- |
| Codex | `dist/adapters/codex/` | `.agents/skills/` |
| Claude Code | `dist/adapters/claude/` | `.claude/skills/` |
| opencode | `dist/adapters/opencode/` | `.opencode/skills/` |

`dist/adapters/manifest.yaml` remains the tracked adapter support matrix and package metadata. It records adapter support and opencode command aliases; it must not contain generated skill bodies.

## Release Artifact Migration

A later release may move generated public adapter skill copies out of ordinary tracked Git state after downloadable adapter archives, install docs, validation, release notes, and compatibility notices are ready.

When that migration happens, download adapter archives from GitHub release assets. The release artifact metadata and checksums will be recorded under `docs/reports/adapter-artifacts/releases/<version>.yaml`.

`.codex/skills/` is repository-local generated Codex runtime output and not a public adapter install source.
