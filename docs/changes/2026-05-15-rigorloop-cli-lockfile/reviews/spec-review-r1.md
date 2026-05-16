# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review skill
Target: specs/rigorloop-cli-lockfile.md
Reviewed artifact: specs/rigorloop-cli-lockfile.md
Review date: 2026-05-15
Recording status: recorded
Status: changes-requested

## Scope

Reviewed the draft RigorLoop CLI lockfile contract against the accepted scaffolding CLI proposal, the approved first-slice CLI spec, `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md`.

The review focused on whether the draft is precise enough for architecture, test-spec, and implementation without guessing. No implementation code was reviewed.

## Dimension Results

| Dimension | Result | Notes |
|---|---|---|
| Requirement clarity | block | The spec says which individual fields must be recorded, but it does not define the complete top-level `rigorloop.lock` document shape. |
| Normative language | concern | Most requirements are testable, but `R66` says unknown future sections can be preserved or blocked explicitly without choosing one first-slice rule. |
| Completeness | concern | Normal, dry-run, malformed lockfile, drift, and migration boundaries are covered, but the durable file schema is incomplete. |
| Testability | block | Tests cannot assert a complete lockfile fixture without inventing where package, manifest, adapter metadata release, and generated entries live. |
| Examples | concern | Examples describe behavior but do not include a full expected `rigorloop.lock` example. |
| Compatibility | pass | Existing first-slice projects without `rigorloop.lock` remain valid, and public npm publication remains out of scope. |
| Observability | pass | JSON, human output, drift reporting, and validation evidence requirements are covered. |
| Security/privacy | pass | The spec forbids secrets, absolute paths, host-specific values, and trust-boundary expansion. |
| Non-goals | pass | Exclusions for `new-change`, `status`, `validate`, non-Codex adapters, workflow outputs, and npm publishing are explicit. |
| Acceptance criteria | concern | Acceptance criteria are observable except for the incomplete durable lockfile shape. |

## Findings

### SR1-F1: Durable lockfile document shape is incomplete

Finding ID: SR1-F1

Severity: blocking

Location: `specs/rigorloop-cli-lockfile.md:91`, `specs/rigorloop-cli-lockfile.md:111`, `specs/rigorloop-cli-lockfile.md:165`, `specs/rigorloop-cli-lockfile.md:344`

Evidence: `R10` requires `schema_version: 1`, `R15` through `R17` require package, manifest hash, and `generated.adapters`, and `R18` defines a Codex adapter entry fragment. However, the spec never gives the complete lockfile document shape: it does not define the top-level key for package identity, the manifest object keys, the adapter metadata release field name, whether generated adapters are nested under `generated.adapters` beside or below `tree_hash_algorithm`, or a complete YAML example. `AC3` lists required data, but not where it appears. Because `rigorloop.lock` is a durable compatibility surface, architecture, tests, and implementation would have to invent public structure.

Required outcome: The spec must define a complete normative `schema_version: 1` lockfile document shape before architecture, test-spec, or implementation relies on it.

Safe resolution path: Add a full required YAML example and matching requirements for every top-level section. For example, define exact keys for `rigorloop.package`, `rigorloop.version`, `manifest.path`, `manifest.sha256`, `generated.adapters[]`, `release`, `archive`, `archive_sha256`, `installed_root`, `tree_hash_algorithm`, `tree_sha256`, and `file_count`. Also choose a first-slice unknown-field policy: either preserve unknown top-level sections byte-for-byte where possible or block on unknown fields until a migration/preservation spec exists.

## Requirement Notes

- `R1` through `R8`: pass for scope and authority.
- `R9` through `R17`: incomplete until the full document schema is specified.
- `R18` through `R23`: directionally sound but currently only an entry fragment, not a full lockfile contract.
- `R24` through `R32`: pass; they inherit the previously approved tree-hash algorithm.
- `R34` through `R45`: concern; write/update behavior depends on knowing whether unknown fields are preserved or blocked.
- `R46` through `R53`: pass for drift and mutation conflict behavior.
- `R54` through `R61`: pass for public JSON and exit behavior.
- `R62` through `R66`: concern; compatibility claims need the first-slice unknown-field policy to be deterministic.

## Recommendation

Changes requested.

Immediate next repository stage: spec.

Eventual test-spec readiness: not-ready.

Stop condition: revise `specs/rigorloop-cli-lockfile.md` to define the complete durable lockfile document shape and rerun `spec-review`.
