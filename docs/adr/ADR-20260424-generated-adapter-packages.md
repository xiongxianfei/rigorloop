# ADR-20260424-generated-adapter-packages: Generated Public Adapter Packages

## Status
accepted

## Context

RigorLoop now needs to support Codex, Claude Code, and opencode as public adapter packages for the first public release. The accepted spec requires installable generated packages under `dist/adapters/`, a generated manifest, release metadata under `docs/releases/<version>/release.yaml`, and maintainer-run smoke evidence.

The existing source-layout ADR established that `skills/` is canonical and `.codex/skills/` is generated Codex compatibility output. That decision remains valuable for this repository's current Codex runtime, but it does not provide a public package layout for other tools.

The design must avoid creating multiple authored skill trees while still giving each tool the filesystem layout it expects.

## Decision

Create tracked generated public adapter packages under:

```text
dist/adapters/codex/
dist/adapters/claude/
dist/adapters/opencode/
```

Keep `skills/` as the only authored skill source.

Generate adapter package instruction entrypoints from authored thin templates under `scripts/adapter_templates/`.

Generate `dist/adapters/manifest.yaml` from canonical skills, adapter inclusion decisions, and the release version.

Keep `.codex/skills/` as a separate local generated Codex runtime mirror for this repository until a later accepted change explicitly retires or migrates it.

Do not generate `.codex/skills/` from `dist/adapters/codex/`, and do not generate `dist/adapters/codex/` from `.codex/skills/`. Both generated surfaces derive from canonical `skills/`.

## Alternatives considered

### Hand-author each adapter package

Rejected because it would create multiple competing skill trees and weaken the source-authored-once guarantee.

### Replace `.codex/skills/` with `dist/adapters/codex/`

Rejected for this initiative because `.codex/skills/` is the existing local runtime compatibility surface. Removing it would add migration risk before public adapter packaging is proven.

### Generate the public Codex package from `.codex/skills/`

Rejected because `.codex/skills/` is already generated output. Generated output should not become the source for another generated distribution.

### Introduce a larger `method/`, `adapters/`, and `dist/` source layout

Rejected for this initiative because the spec only needs a public generated adapter package surface. Authored templates can live under `scripts/adapter_templates/` without moving the whole repository source layout.

## Consequences

- Contributors continue editing canonical skills under `skills/`.
- Public users install from `dist/adapters/<tool>/`.
- Repo-local Codex compatibility continues through `.codex/skills/`.
- CI and release verification must check both `.codex/skills/` drift and `dist/adapters/` drift.
- Documentation must clearly distinguish authored sources, generated public packages, and the local generated Codex mirror.
- A later migration can retire `.codex/skills/`, but that requires a separate lifecycle change.

## Follow-up

- Implement adapter generation and validation scripts.
- Add release metadata validation for `docs/releases/<version>/release.yaml`.
- Update CI and release verification to enforce both generated surfaces.
- Update README, workflow docs, and root guidance so contributors know which files are authored and which are generated.
