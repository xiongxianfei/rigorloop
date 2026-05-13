# ADR-20260513-v0-1-3-adapter-release-archive-install-surface: v0.1.3 Adapter Release Archive Install Surface

## Status

accepted

## Context

RigorLoop already treats `skills/` as the only authored skill source. The `v0.1.2` archive-introduction release preserved tracked generated public adapter skill bodies under `dist/adapters/**/skills` while also publishing per-adapter downloadable archives, artifact metadata, checksums, install guidance, and release validation evidence.

That release satisfied the compatibility-window precondition from the generated-output migration architecture: downstream users had one stable release where repository-tree adapter installation and release-archive installation were both available.

The `v0.1.3` release now needs to complete the public adapter untracking step without removing adapter support or weakening validation. The durable architecture decision is where the active public install surface lives after tracked generated adapter package fragments leave Git.

## Decision

For `v0.1.3` and later, public adapter installation uses release archives as the active install surface.

Keep only these adapter support surfaces tracked under `dist/adapters/`:

```text
dist/adapters/README.md
dist/adapters/manifest.yaml
```

Do not keep generated public adapter package fragments tracked under `dist/adapters/<adapter>/`, including generated skill bodies, generated adapter instruction entrypoints, or generated opencode command wrappers.

Generate complete Codex, Claude Code, and opencode adapter packages from canonical `skills/` and approved adapter templates into temporary or release-output directories. Validate those generated packages and the release archives rather than comparing canonical skills to tracked adapter package trees.

Use `dist/adapters/README.md` as the concise repository install-contract surface. Root guidance points contributors to that README instead of duplicating archive names, install roots, and checksum metadata.

This ADR supersedes the tracked-package storage assumptions in `ADR-20260424-generated-adapter-packages.md` for `v0.1.3` and later. It does not supersede adapter support, generation from canonical skills, release archive publication, artifact metadata, checksums, token-cost public-source rules, or release verification obligations.

## Alternatives considered

### Keep generated adapter package trees tracked for another release

Rejected because `v0.1.2` already provided the stable compatibility window with both repository-tree adapter packages and release archives. Keeping generated package trees tracked would continue duplicated skill diffs and generated-output review noise without adding a new compatibility guarantee.

### Remove tracked package trees without release archive validation

Rejected because release archives become the active install surface and must remain reproducible, checksummed, and structurally validated.

### Keep non-skill adapter entrypoints tracked while removing only skill bodies

Rejected for this slice because partial tracked packages are easy to mistake for installable repository-tree adapter packages. Complete adapter packages should exist in generated temporary output or release archives, not as mixed tracked fragments under `dist/adapters/<adapter>/`.

### Duplicate detailed install guidance in root files

Rejected because `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` should stay concise and point to `dist/adapters/README.md` as the install-contract surface.

## Consequences

- Contributors edit public skill behavior only under `skills/` or approved source templates and generator inputs.
- Repository diffs stop carrying generated skill-body copies for Codex, Claude Code, and opencode.
- `dist/adapters/README.md` and `dist/adapters/manifest.yaml` become the only default tracked adapter support files under `dist/adapters/`.
- Release validation must fail if tracked generated adapter skill bodies remain for `v0.1.3` or later.
- Release validation must generate adapter output outside tracked `dist/adapters/`, validate generated package structure, validate release archives, validate metadata and checksums, and prove the release gate no longer depends on tracked adapter package trees.
- Root guidance must remove or version-qualify compatibility-window wording so ordinary contributors are not directed to retired repository-tree skill-body paths as the active install model.
- Token-cost dynamic benchmarks continue to use generated public adapter output or release archive output and must not use `.codex/skills/` as the public skill source.
- `v0.1.2` release evidence remains valid historical compatibility-window evidence.

## Follow-up

- Update the canonical architecture package to record the `v0.1.3` release archive install surface and validation replacement.
- Create the `v0.1.3` execution plan, test spec, implementation, review, explain-change, verify, PR, and release evidence.
- Update `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, and `dist/adapters/README.md` during implementation, or record explicit unaffected rationales where allowed by the spec.
