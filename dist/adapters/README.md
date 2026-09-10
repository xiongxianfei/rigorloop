# RigorLoop Adapter Installation

`skills/` is the authored source. `dist/adapters/manifest.yaml` records the current Codex and Claude Code candidate support matrix. Generated skill bodies are release archives, not tracked source here. Builds do not install skills into this repository's runtime.

| Target | Archive | Installed skills |
| --- | --- | --- |
| Codex | `rigorloop-adapter-codex-<version>.zip` | `.agents/skills/` |
| Claude Code | `rigorloop-adapter-claude-<version>.zip` | `.claude/skills/` |

Use `rigorloop init codex` or `rigorloop init claude`. The CLI acquires and verifies the matching official archive before checking all candidate destinations. Existing skill directories or files conflict even when identical; the command lists conflicts and installs nothing. Use `--force` for complete replacement of selected candidate skills, including obsolete content. Local changes within replaced skill directories leave the active installation; originals are retained at reported private paths outside skill discovery for separate inspection and cleanup. Unrelated files and shared parents stay untouched. Integrity, containment and symlink checks apply in both modes.

`--from-archive <path>` verifies a local archive against the same bundled trust root. `--dry-run` does not acquire, extract or write; it identifies preliminary checks and unperformed verification. See the [CLI installation guide](../../packages/rigorloop/README.md#target-init) for failure and retry behavior.

Installation ignores and preserves project `rigorloop.yaml` and `rigorloop.lock`. It neither writes state nor performs automatic managed upgrades. OpenCode, its aliases, `--write-state` and `--adapter` are retired. Historical archives and evidence remain unchanged; current candidate availability does not authorize publication or project-governance adoption.

## Retired skill entries

Current candidates contain `design` and `route`. Retired `spec`, `architecture` and `workflow` entries require separate inspection and reconciliation. The installer preserves them and reports their exact paths; `--force` does not perform noncandidate cleanup. See [retired authoring guidance](../../packages/rigorloop/README.md#upgrading-retired-authoring-skills).

Adapter artifact metadata for historical releases remains at `docs/reports/adapter-artifacts/releases/<version>.yaml`. Current package metadata is candidate evidence, not a publication record.
