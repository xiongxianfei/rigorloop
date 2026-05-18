# ADR-20260518-multi-adapter-init-and-proxy-download: Multi-Adapter Init and Proxy-Aware Download Boundary

## Status

accepted

## Context

RigorLoop already publishes generated adapter archives as release assets for Codex, Claude Code, and opencode. The CLI, however, only exposes `rigorloop init --adapter codex`, and the existing lockfile-writing slice records only Codex generated output under `.agents/skills`.

The approved multi-adapter init spec extends the public CLI install surface to:

```text
rigorloop init --adapter codex
rigorloop init --adapter claude
rigorloop init --adapter opencode
```

The architecture decision is how to add Claude Code and opencode without making npm package contents, local runtime directories, or downstream lockfiles into sources of truth. The change also needs a proxy-aware network download boundary because Node `fetch()` behavior in enterprise networks depends on Node env-proxy support and runtime configuration.

## Decision

Extend the existing `@xiongxianfei/rigorloop` CLI package boundary with adapter descriptors for Codex, Claude Code, and opencode.

The CLI owns adapter selection, archive acquisition, extraction planning, tree-hash verification, `rigorloop.yaml` serialization, and `rigorloop.lock` serialization for this install surface. Canonical skill behavior remains authored under `skills/`, and generated adapter output continues to come from verified release archives or local archives verified against CLI-bundled official metadata.

Descriptor roots are:

```text
codex:   skills -> .agents/skills
claude:  skills -> .claude/skills
opencode skills -> .opencode/skills
opencode commands -> .opencode/commands
```

Codex stays on `.agents/skills`. There is no Codex migration to `.codex/skills`.

opencode is a possible multi-root adapter. Trusted metadata determines which roots are required for the selected archive. New opencode archives with declared command aliases install both skills and commands or fail verification. Older compatible opencode archives without `command_aliases.opencode` may install skills only, emit warning code `opencode-command-aliases-not-declared`, and record only installed roots in `rigorloop.yaml` and `rigorloop.lock`.

`rigorloop.lock` advances to `schema_version: 2` for multi-adapter support. Existing valid `schema_version: 1` Codex entries remain readable and may be upgraded only after drift checks pass. Single-root entries keep `installed_root`, `tree_sha256`, and `file_count`; multi-root entries use `installed_roots` and per-root `root_hashes`.

Network downloads remain release-archive installs from exact official URLs selected by trusted metadata. The first proxy-aware slice uses Node built-in env-proxy behavior only when the runtime supports and enables it. Programmatic Undici proxy dispatcher support is deferred. Download failure diagnostics expose only bounded safe facts: adapter name, release version, trusted public archive URL, detected proxy environment variable names, Node env-proxy status, download failure class, and `--from-archive` fallback guidance.

## Alternatives considered

### Patch Codex-only constants

Rejected because opencode has a second command-alias surface, lockfile schema v2 needs explicit single-root and multi-root serialization, and public CLI behavior should not expand without a testable contract.

### Move Codex to `.codex/skills`

Rejected because the accepted Codex contract and official Codex skills documentation use `.agents/skills` for repository skills. Changing the path would create migration risk without user value.

### Bundle adapter archives into npm

Rejected because adapter archives are generated release artifacts. npm remains a CLI delivery channel with bundled metadata, not the canonical adapter archive source.

### Add programmatic Undici proxy dispatch now

Rejected for the first slice because Node built-in env-proxy support plus safe diagnostics and local archive fallback handle the immediate adoption issue without adding a new dispatcher dependency or proxy credential handling surface.

## Consequences

- The CLI adapter install path becomes descriptor-driven rather than Codex-constant-driven.
- The package must bundle trusted metadata for all supported adapters and compatible releases it claims to install.
- `rigorloop.yaml` and `rigorloop.lock` need mixed single-root and multi-root serialization paths.
- Existing valid Codex lockfiles remain compatible when generated output is not drifted.
- opencode command aliases are treated as generated output and cannot be silently skipped when declared by metadata.
- Older compatible opencode archives stay usable as skills-only installs, but the warning and recorded roots make the reduced runtime surface explicit.
- Network diagnostics improve enterprise recovery while avoiding proxy credential, private hostname, raw proxy URL, request header, and raw environment-value leakage.
- Local archive mode remains the controlled-network fallback and keeps the CLI metadata trust root.
- A later proposal or spec is required for programmatic Undici proxy dispatch, lockfile repair, `rigorloop status`, `rigorloop validate`, workflow YAML, generated workflow docs, or any new adapter beyond Codex, Claude Code, and opencode.

## Follow-up

- Update the canonical architecture package to record the descriptor model, multi-root lockfile v2 boundary, proxy diagnostic boundary, and opencode older-archive compatibility behavior.
- Create architecture-review evidence for this ADR and canonical package update.
- Create a plan and test spec after architecture review approves the design.
