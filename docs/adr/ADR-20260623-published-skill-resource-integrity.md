# ADR-20260623-published-skill-resource-integrity: Published Skill Resource Integrity

## Status

accepted

## Context

RigorLoop publishes skills through local mirrors, generated adapter packages,
release archives, and target-specific installations. A recent architecture
skill invocation found that the installed architecture skill referenced
`templates/architecture.md`, `templates/diagram-styles.mmd`, and
`templates/adr.md`, but the installed skill tree contained only `SKILL.md`.

The runtime fallback was safe for that specific invocation because `SKILL.md`
still contained enough normative structure to produce a compliant architecture
artifact. That does not make the installed package valid. A published skill that
references unavailable skill-local resources can produce inconsistent artifacts,
stale generated output, invented template content, or late failures in customer
repositories.

The existing generated-output and adapter-release ADRs establish that `skills/`
is the only authored skill source and that generated adapter output and release
archives are derived. They do not define exact resource identity for packaged
skill-local resources across canonical source, generated output, packed release
candidates, and installed target trees.

## Decision

Use explicit mapped skill-local resources as the package-integrity contract.

Every required skill-local resource dependency is represented in the skill's
`Resource map`. Resource-map verbs map to approved resource classes:

```text
COPY -> assets/
READ -> references/
RUN  -> scripts/
```

`templates/` is not an implicit packaged skill resource class. Legacy
`templates/...` instructions are migration lint input until they are removed,
mapped to approved classes, or covered by an approved temporary exception.

For untransformed mapped resources, parity is:

```text
skill-root relative path + SHA-256 of raw file bytes
```

Generated output, adapter packages, locally packed release candidates, and
installed target skill trees preserve that identity. File timestamps do not
participate. Line-ending normalization and content rewriting are transformations,
not implicit compatibility behavior.

Any intentional resource transformation requires a transformation contract that
names the input path, transformation owner, output path, expected output
identity, and validation command.

Pre-publish clean-install proof uses locally packed release candidates installed
into empty Codex, Claude, and opencode target projects. The proof inspects the
real installed skill roots. Live registry installation remains post-publish
release evidence unless the release contract explicitly requires it earlier.

Runtime fallback remains an emergency work-continuation boundary. Missing mapped
resources still fail package validation. Runtime execution stops when the
missing resource owns normative, schema, security, legal, or non-obvious
structural content. A bounded disclosed fallback may continue only for redundant
convenience resources whose complete contract is already in `SKILL.md`.

## Alternatives considered

### Copy missing resources into local installed skill trees

Rejected because it repairs one machine-local installation, does not identify
the first divergent layer, and can be overwritten by generation or
installation.

### Keep everything inline in `SKILL.md`

Rejected as the general contract because it avoids packaging defects by
discarding progressive disclosure. It remains valid for resources that do not
earn separate files.

### Validate only explicit resource-map entries

Rejected as a complete first slice because the triggering defect was a raw
legacy `templates/...` instruction outside a resource map. The durable contract
uses resource maps, but migration needs bounded legacy-reference lint.

### Broadly scan every path-like Markdown string

Rejected because it would over-classify artifact examples, customer-project
paths, repository docs paths, and code snippets as packaged resource
dependencies.

### Use presence-only package checks

Rejected because presence-only checks cannot detect stale generated copies.
Raw-byte SHA-256 parity is deterministic and reviewable.

### Require live registry install proof before implementation closeout

Rejected for this contract. Pre-publish implementation proof should inspect the
locally packed release candidate. Live registry install proof belongs to release
evidence unless a release contract explicitly moves it earlier.

## Consequences

- Canonical skill validation gains resource-map path, verb, containment,
  existence, and bounded legacy-reference checks.
- Generated-output and adapter validation compare mapped resource inventories
  and raw-byte SHA-256 identity.
- Release-candidate clean-install smoke inspects real installed Codex, Claude,
  and opencode skill roots.
- Existing unmapped legacy resource references can be audited before global
  enforcement, but new or changed skills cannot introduce new debt.
- Architecture skill resources must be classified by purpose: copy-and-fill
  structures under `assets/`, read-only guidance under `references/`, and
  deterministic helpers under `scripts/`.
- Runtime fallback can preserve safe work only within a narrow boundary and does
  not affect package-validation failure.

## Follow-up

- Audit the architecture skill resource chain and identify the first divergent
  layer.
- Normalize architecture skill resources and `Resource map` entries.
- Add validator fixtures for mapped resources, legacy references, false-positive
  path examples, stale generated resources, and clean-install target trees.
- Record architecture behavior-preservation evidence for trigger behavior,
  arc42 sections, C4 obligations, ADR structure, architecture-review boundaries,
  and handoff semantics.
