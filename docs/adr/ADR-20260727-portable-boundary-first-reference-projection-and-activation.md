# ADR-20260727-portable-boundary-first-reference-projection-and-activation: Portable Boundary Reference Projection and Activation

## Status

accepted

## Context

The boundary-first contract requires ten published lifecycle skills to load the
same versioned method from their own installed skill roots.
Installed skills cannot depend on a RigorLoop repository-root path, while ten
hand-maintained copies would create semantic and packaging drift.

The contract also activates prospectively.
The repository must distinguish feature specs that existed at activation from
new specs without asking a structural validator to decide whether prose edits
are substantively normative.

The existing published-skill resource-integrity decision already defines
`READ -> references/`, skill-root-relative paths, raw-byte SHA-256 parity,
locally packed release candidates, and installed-tree inspection.
This decision specializes that architecture for one shared method and its
activation baseline.

## Decision

Use `specs/references/boundary-first-method-v1.md` as the single authored
canonical shared-reference source.

A repository-owned Python projection command reads that file and writes its
raw bytes, without normalization or templating, to:

```text
skills/<governed-skill>/references/boundary-first-method-v1.md
```

for the closed governed skill set:

```text
workflow
spec
spec-review
plan
plan-review
test-spec
test-spec-review
implement
code-review
verify
```

The projected files are tracked canonical package inputs but are derived and
must not be hand-edited.
The projection module owns the closed source path, consumer list, method
version, raw-byte copying, and check/write modes.
Skill validation imports that module's inventory rather than defining a second
consumer list.

Existing skill and adapter builders continue to copy complete skill roots.
Existing mapped-resource validation continues to prove relative-path and
raw-byte identity through generated, packed, and installed Codex, Claude Code,
and opencode trees.

Use `specs/boundary-first-activation.yaml` as the durable activation record.
The authoritative activation state remains the
`Boundary-first contract activation` field in the approved proof-model spec.
The YAML `state` is a mechanical projection that must match that field; a
mismatch fails closed and neither surface may be settled independently.

Before state becomes `active`, the record contains:

```text
contract_version
state
activated_at
canonical_reference
canonical_reference_sha256
grandfathered_specs
grandfathered_inventory_sha256
rollback_preserved_specs
rollback_preserved_inventory_sha256
governed_skills
projection_sha256
```

The grandfathered inventory is the sorted set of existing top-level
`specs/*.md` feature-contract paths whose durable lifecycle state is
`accepted`, `approved`, or `active` at activation, excluding `README.md` and
`*.test.md`, with each path's activation-time raw-byte SHA-256.
Path membership determines structural grandfathering.
The recorded hash preserves the activation baseline for audit.

Every nonterminal in-flight behavior-changing feature spec must opt in before
test-spec approval or block activation.
Draft, pending, reviewed, or otherwise nonterminal specs are not added to the
grandfathered inventory merely because their paths already exist.

Projection and grandfathered-inventory digests use one shared helper and this
algorithm:

1. express every repository-relative path with POSIX `/` separators;
2. compute the lowercase hexadecimal SHA-256 of each file's raw bytes;
3. sort records by path as Unicode code-point strings;
4. serialize each UTF-8 record as
   `<path>\\0<raw-byte-sha256>\\n`;
5. concatenate the records without a header; and
6. store the lowercase hexadecimal SHA-256 of the concatenated bytes.

`projection_sha256` covers exactly the ten governed projected reference paths.
`grandfathered_inventory_sha256` covers exactly the eligible historical spec
paths recorded in `grandfathered_specs`.
`rollback_preserved_specs` is empty before rollback. The rollback transaction
snapshots every accepted, approved, or active marked feature spec as a sorted
path and raw-byte SHA-256 before changing state. Its digest uses the same
inventory algorithm. Rolled-back validation permits markers only for exact
path-and-byte members of that closed inventory.
The generator and validator import the same helper rather than reimplementing
serialization.

After activation:

- a new top-level feature spec absent from the grandfathered inventory must
  carry `boundary_contract: boundary-first-v1`;
- a marker, when present, is structurally validated;
- an unmarked edit to a grandfathered path is routed to `spec-review` for
  substantive-revision classification;
- structural validation does not infer semantic revision status.

Activation changes the proof-model spec's activation state and record identity,
the activation YAML, projections, validators, fixtures, generated outputs, and
package evidence in one reviewed milestone.
Rollback changes the contract state to `rolled-back` and removes active
projection behavior coherently while preserving accepted marked artifacts and
the historical activation record.

## Alternatives considered

### Keep the shared method inline in every skill

Rejected because ten copies would drift and common method edits would be
difficult to review as one contract.

### Make one governed skill's reference canonical

Rejected because no lifecycle stage owns the cross-stage method and the chosen
skill would become an accidental dependency for the others.

### Put the canonical source under `templates/shared/`

Rejected because the method is read-only decision guidance, not a copy-and-fill
template or a verbatim in-body policy block.

### Generate the reference only while building adapters

Rejected because canonical skill validation requires mapped resources to exist
under each canonical skill root before generated and installed packages can be
valid.

### Use symlinks between skill roots

Rejected because archive and target installers do not share one portable
symlink contract, and symlinks would weaken containment and package-integrity
checks.

### Infer historical specs from Git history on every validation run

Rejected because validation must remain deterministic from repository-local
tracked state and should not depend on shallow-history availability.

## Consequences

- One authored Markdown source controls all ten packaged method copies.
- Tracked derived files exist under canonical skill roots and are changed only
  by the projection command.
- Existing build and adapter copy flows remain unchanged; validation gains a
  boundary-specific inventory and projection check.
- The activation YAML introduces one small repository-local state record but
  no service, database, network dependency, or runtime attestation.
- New-spec enforcement is deterministic.
- Substantive-revision classification for grandfathered specs remains a
  semantic `spec-review` judgment.
- Activation has one authoritative state owner; the YAML state is a checked
  projection and evidence record.
- Nonterminal in-flight specs cannot become accidental historical exemptions.
- Projection and grandfathered-inventory identities are reproducible across
  supported environments.
- Rollout and rollback operate on the complete skill, validator, fixture,
  generated, packed, installed, and activation bundle.

## Follow-up

- Add the canonical reference and projection module.
- Add projection write/check commands and unknown-value regressions.
- Add activation-record validation and grandfathered inventory fixtures.
- Map the reference from all ten governed skills.
- Extend generated, packed, and clean-installed parity proof.
- Record architecture-review before execution planning.
- Architecture-review R2 approved this decision on 2026-07-27.
