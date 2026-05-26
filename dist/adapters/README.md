# RigorLoop Adapter Installation

`skills/` is the canonical `skills/` authored source.

`dist/adapters/manifest.yaml` is the tracked adapter support matrix. It records adapter support and opencode command aliases; it must not contain generated skill bodies.

For `v0.1.3` and later, public adapter installation uses GitHub release archives. The repository keeps adapter metadata and install guidance under `dist/adapters/`; generated public adapter skill bodies are not tracked source.

Download the adapter archive for your tool from the GitHub release assets and extract it into the target project root:

| Adapter | Archive name | Target install root |
| --- | --- | --- |
| Codex | `rigorloop-adapter-codex-<version>.zip` | `.agents/skills/` |
| Claude Code | `rigorloop-adapter-claude-<version>.zip` | `.claude/skills/` |
| opencode | `rigorloop-adapter-opencode-<version>.zip` | `.opencode/skills/` |

Adapter artifact metadata and checksums are recorded under `docs/reports/adapter-artifacts/releases/<version>.yaml`.

Historical note: v0.1.2 kept repository-tree adapter packages during the compatibility window while introducing release archives. For `v0.1.3` and later, release archives are the active public adapter install path.

`.codex/skills/` is an ignored local runtime install directory and not a public adapter install source. Use the Codex release archive for public Codex adapter output, and keep `.codex/skills/` untracked if you copy skills there for local runtime use.

## Migration notes

The CI workflow authoring/review skill has been renamed from `ci` to `ci-maintenance`. Use `ci-maintenance` for direct skill invocation. Existing direct `ci` invocations should be updated; this adapter release does not install `ci` as a compatibility alias.
