# ADR-20260729: Progressive Boundary Guidance Resources

## Owning change record

`docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/change.yaml`

## Context

The pending `boundary-first-v1` capability currently projects one complete
method reference into all ten governed skills. That preserves semantic parity,
but every stage packages and may load feature-authoring and proof detail even
when it needs only a compact boundary scan or an approved artifact slice.

The approved progressive-guidance spec keeps one semantic version and one
boundary model while requiring three logical resource layers, stage-family
ownership, prompt-independent compact scanning, deterministic package parity,
purpose-scoped validation selection, representative loading measurements, and
atomic activation and rollback.

This revises the resource-composition portion of
`ADR-20260728-portable-boundary-first-release-manifest-and-package-rollback.md`.
That ADR's reviewed release manifest, immutable grandfathering baseline,
read-only package rollback validation, and external release-operator boundary
remain in force.

## Decision

Keep `specs/references/boundary-first-method-v1.md` as the compatibility-stable
canonical filename for the compact core. Its skill-local target remains
`references/boundary-first-method-v1.md`, so no second alias or semantic
version is introduced.

Add exactly two canonical stage-family resources:

- `specs/references/boundary-first-feature-authoring-v1.md`, projected only to
  `spec` and `spec-review`;
- `specs/references/boundary-first-proof-v1.md`, projected only to `test-spec`
  and `test-spec-review`.

Each projected target uses the same basename under the consuming skill's
`references/` directory and is mapped with `READ` plus a stage-specific load
condition. Every governed skill packages the compact core. No other governed
skill packages either family resource.

Use `specs/boundary-first-resources.yaml` as the sole declarative projection
manifest. Its exact schema is:

```yaml
schema_version: 1
contract_version: boundary-first-v1
resources:
  - id: compact-core
    source: specs/references/boundary-first-method-v1.md
    target: references/boundary-first-method-v1.md
    consumers:
      - workflow
      - spec
      - spec-review
      - plan
      - plan-review
      - test-spec
      - test-spec-review
      - implement
      - code-review
      - verify
  - id: feature-authoring
    source: specs/references/boundary-first-feature-authoring-v1.md
    target: references/boundary-first-feature-authoring-v1.md
    consumers:
      - spec
      - spec-review
  - id: proof
    source: specs/references/boundary-first-proof-v1.md
    target: references/boundary-first-proof-v1.md
    consumers:
      - test-spec
      - test-spec-review
```

The top-level key set is exactly `schema_version`, `contract_version`, and
`resources`. `schema_version` is the integer `1`;
`contract_version` is `boundary-first-v1`; and `resources` contains exactly
the three entries above in `compact-core`, `feature-authoring`, `proof` order.
Each entry contains exactly `id`, `source`, `target`, and `consumers`.
Consumer order is the relative order shown by the compact-core list.

Unknown or missing fields, values, resource IDs, or consumers fail closed.
Duplicate resource IDs, sources, targets, or consumers fail closed. Source and
target paths are normalized repository-relative POSIX paths; absolute paths,
`.` or `..` segments, path escape, symlinks, missing sources, and targets
outside `references/` fail closed. Hashes and load conditions do not appear in
this manifest: validators derive hashes from raw bytes, while each consuming
`SKILL.md` owns its stage-specific load condition.

The projection module interprets and validates this manifest; it no longer
owns a parallel hard-coded resource or consumer inventory.

Identity has three layers:

1. each canonical or projected file uses raw-byte SHA-256;
2. the manifest identity is the raw-byte SHA-256 of
   `specs/boundary-first-resources.yaml`;
3. the projection-set identity hashes sorted UTF-8 records of
   `<repository-target-path>\0<lowercase-raw-byte-sha256>\n`.

The activation manifest keeps `canonical_reference` and
`canonical_reference_sha256` as compact-core compatibility fields and adds
`resource_manifest` and `resource_manifest_sha256`. Its existing
`projection_sha256` becomes the complete multi-resource projection-set
identity. Validation requires the compatibility fields, manifest identity,
canonical resources, expected projections, and projection-set identity to
agree before activation.

Copy the four compact-scan questions directly into all ten governed skill
bodies from one contributor-owned shared block under
`templates/shared/boundary-first-compact-scan.md`. Existing shared-block drift
checks preserve exact wording. The shared-block implementation detail is not
published as maintainer guidance. Direct skill text lets a stage decide that
no deeper context is needed without loading a formal resource.

Downstream stages begin with cited approved boundary, interaction, and proof
rows from project-local artifacts. They load the compact core only when the
cited slice is missing, stale, unknown, ambiguous, conflicting, or escaped.
They never load feature-authoring or proof guidance unless they are one of the
owning stage families.

Representative loading evidence uses a tracked fixture under
`scripts/fixtures/boundary-first/loading-profiles.yaml`. For each stage family
and representative decision it records mapped resource IDs, initial loaded
resource IDs, and permitted expansion resource IDs. Measurement reports:

- canonical bytes per resource before and after the split;
- mapped-resource count per governed skill;
- representative initial and expanded loaded-resource counts by stage family.

These are reviewable baselines, not runtime instrumentation or release gates.

Activation has one atomic state switch and two explicitly different surfaces.

The tracked activation transaction is the complete reviewed repository tree
change containing:

- the resource and activation manifests;
- the three canonical resources and compact shared block;
- the ten canonical skill bodies, resource maps, and expected tracked
  projections;
- projection, validation, selector, measurement, and regression code and
  fixtures; and
- repository-tracked evidence or evidence references required by the change.

The derived proof set contains temporary generated adapter trees, packed
release candidates, release archives, clean installed Codex, Claude, and
opencode target trees, and their computed identities and results. Those trees
are generated, release, or temporary output. They are not added to the tracked
transaction and are not Git rollback targets.

While the accepted or released repository state remains `pending`, the
reviewed candidate tree may contain the proposed `active` marker so tooling
can generate and validate the exact tree that would be accepted. The candidate
does not establish active capability by file presence alone. Release metadata
binds generated package evidence to the candidate source revision; the
activation manifest binds the resource-manifest and projection-set identities.
Every required tracked and derived layer must match before review can accept
that candidate. Acceptance of the reviewed tracked tree containing the marker
is the atomic activation boundary; a partially passing candidate cannot
activate or publish the capability.

Before activation, rollback reverts or abandons the complete tracked
progressive-resource transaction, then discards temporary derived output or
regenerates it from the restored pending single-reference tree. Rollback does
not attempt to Git-revert installed target directories or release-output
directories. After activation, rollback continues to select the immutable
release recorded by the existing activation manifest.

Skill-only paths select purpose-built skill, boundary, projection, adapter,
and prose checks. Artifact-lifecycle validation is selected only for actual
lifecycle-managed artifacts and change records; mixed changed sets retain both
families with check-owned affected paths.

## Alternatives considered

### Keep the full shared reference and change only trigger wording

Rejected because automatic invocation would still load authoring and proof
detail in stages that do not own it.

### Rename the compact core and keep the old filename as an alias

Rejected because two projected core paths add compatibility and validation
surface without changing semantics. Reusing the established filename gives
existing package and resource-map paths a narrow migration.

### Keep the resource inventory in Python constants

Rejected because the resource matrix is durable reviewed architecture data.
A declarative manifest is easier to diff and prevents projection,
validation, and measurement code from owning competing inventories.

### Require every stage to load the compact core before scanning

Rejected because the four stable questions are small enough to live directly
in stage-local text and can avoid a resource read for non-behavior work.

### Generate a per-stage context packet

Rejected because approved artifacts already own stable IDs and exact slices.
A new packet would duplicate lifecycle and synchronization responsibilities.

### Introduce hard byte, token, or loaded-resource budgets

Rejected for the first slice because no representative baseline exists yet.
Measurement precedes any future budget proposal.

## Consequences

- The common resource path stays stable, but its contents become the compact
  core rather than the complete authoring and proof method.
- Two additional canonical resources and bounded projections increase package
  inventory while reducing irrelevant per-stage guidance.
- Direct compact-scan text is duplicated in shipped skills but has one checked
  contributor source, avoiding semantic drift without a runtime include
  mechanism.
- The projection script and validators must read and fail closed on a
  declarative closed manifest, including unknown fields, resource IDs,
  consumers, paths, and duplicate mappings.
- The activation manifest gains resource-manifest identity while preserving
  compact-core compatibility fields and immutable release rollback.
- Generated, packed, archived, and installed trees remain derived proof bound
  to the exact candidate source identity; they do not become tracked rollback
  state.
- Pre-activation recovery reverts or abandons the tracked source transaction
  and regenerates or discards derived output instead of pretending Git owns
  external install trees.
- Selector regression becomes part of the same coherent rollback unit as
  skill/resource changes, preventing skill-only optimization from narrowing
  lifecycle coverage for mixed changes.
- Measurement can compare package and representative loading cost without
  claiming actual model token use or adding a release gate.

## Follow-up

- Update the canonical resource set, shared block, governed skills, projection
  module, validators, selector, fixtures, generated packages, and activation
  evidence through the approved plan and test specification.
- Record the first before-and-after resource and representative loading
  baseline in change-local implementation evidence.
- Revisit hard context budgets only through a later approved proposal and
  specification informed by the baseline.
