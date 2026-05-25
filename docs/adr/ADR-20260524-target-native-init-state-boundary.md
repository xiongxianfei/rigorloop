# ADR-20260524-target-native-init-state-boundary: Target-Native Init and Explicit State Boundary

## Status

accepted

Allowed statuses: `draft`, `proposed`, `accepted`, `active`, `deprecated`, `superseded`, `archived`, `abandoned`.

## Context

The existing CLI init architecture exposed the internal adapter packaging model through public commands such as:

```bash
rigorloop init --adapter codex
rigorloop init --adapter claude
rigorloop init --adapter opencode
```

It also wrote durable project state by default. That made first-run tool bootstrap heavier than the user intent: install verified support for the user's tool.

The `v0.2.0` publication incident also showed that dry-run release smoke is not enough. Dry-run did not exercise the real package-bundled metadata validation path used by non-dry-run install.

The approved target-native init spec changes public CLI syntax, downstream project state schemas, default mutation behavior, and release-smoke gates. That is a durable architecture decision because it revises the CLI package boundary, downstream state boundary, and release validation boundary.

## Decision

For `0.3.0`, make the public init surface target-native:

```bash
rigorloop init codex
rigorloop init claude
rigorloop init opencode
```

Remove `--adapter` from the public CLI. Any `--adapter` use fails before archive download, extraction, state-file writes, or target-root mutation, and reports migration guidance.

Default `rigorloop init <target>` is install-only. It verifies package-bundled metadata, verifies archive bytes, verifies installed roots, installs generated target support, and must not create or mutate `rigorloop.yaml` or `rigorloop.lock`.

Managed state is explicit:

```bash
rigorloop init <target> --write-state
```

`--write-state` writes target-oriented state after verification:

- `rigorloop.yaml` schema v2 uses top-level `targets`;
- `rigorloop.lock` schema v3 uses `generated.targets`;
- new state-file schema keys do not use `adapter` or `adapters`;
- historical archive filename values such as `rigorloop-adapter-codex-v0.3.0.zip` may remain until a separate internal/archive rename is approved.

Default init preserves existing state files byte-for-byte, including legacy adapter-oriented files. Byte preservation does not prevent safety reads. Before target-root mutation, existing state is parsed enough to detect selected-target drift, overlapping roots, or conflicting root mappings. Malformed or ambiguous state blocks non-dry-run mutation.

Release validation for target-native init must run real non-dry-run packed-package smoke before publish and live registry/download smoke after publish for every supported target. Dry-run output remains useful for planning and JSON checks, but it is not install-smoke proof.

## Alternatives considered

### Keep `init --adapter <target>` as canonical

Rejected because it keeps internal packaging terminology in first-run UX and preserves the old support contract.

### Keep `--adapter` as a deprecated hidden alias

Rejected for `0.3.0` because the owner chose a breaking cleanup rather than keeping adapter terminology alive in the CLI parser.

### Keep writing `rigorloop.yaml` and `rigorloop.lock` by default

Rejected because default init should match tool bootstrap intent. Durable managed state remains available through `--write-state`.

### Fully rename internal `dist/adapters/`, archive filenames, and package metadata fields now

Rejected for the first slice because those surfaces are non-user-visible release and validator internals. Renaming them would add broad release-archive churn without being required for the public UX or state-file schema change.

### Treat dry-run smoke as release install proof

Rejected because the publication incident showed dry-run can bypass the real metadata validation path.

## Consequences

- Public docs and CLI help teach target-native init rather than adapter install.
- Existing documented `0.2.x` `--adapter` commands break in `0.3.0` with migration guidance.
- Default first-run init leaves no RigorLoop project state files to remove.
- Users who want managed drift/re-run state opt in explicitly with `--write-state`.
- Downstream state schemas advance to target-oriented shapes while legacy state remains compatibility input.
- Implementation must separate state-file byte preservation from safety parsing.
- Release automation must include real packed-package and live post-publish install smoke for every supported target.
- Internal adapter archive names and `dist/adapters/` paths remain technical debt for a possible later rename, not part of the first slice.

## Follow-up

- Add test-spec coverage for target-native parsing, removed `--adapter`, install-only default, `--write-state`, state safety parsing, metadata/archive coherence, docs sweep, and packed/live smoke.
- Plan implementation milestones after architecture review.
- Consider a later proposal for full internal rename from adapter to target or skill bundle.
