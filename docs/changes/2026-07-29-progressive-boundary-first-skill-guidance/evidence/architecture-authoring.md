# Progressive Boundary-First Skill Guidance Architecture Authoring

## Owning change record

`docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/change.yaml`

## Result

- Architecture surface: canonical update and ADR.
- Canonical architecture:
  `docs/architecture/system/architecture.md`.
- Diagrams changed:
  `docs/architecture/system/diagrams/container.mmd` and
  `docs/architecture/system/diagrams/component-boundary-guidance.mmd`.
- Context diagram: unchanged because no actor, external system, or repository
  system boundary changes.
- ADR:
  `docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md`.
- Direction or spec blockers: none.
- Next stage: architecture-review.

## Decisions resolved

| Spec question | Architecture decision |
| --- | --- |
| Exact resource paths and compatibility | Keep `specs/references/boundary-first-method-v1.md` and its skill-local basename as the compact-core compatibility path. Add `boundary-first-feature-authoring-v1.md` only for `spec` and `spec-review`, and `boundary-first-proof-v1.md` only for `test-spec` and `test-spec-review`. |
| Projection manifest | `specs/boundary-first-resources.yaml` is the sole closed declarative resource and consumer inventory. ADR-20260729 fixes its complete top-level and entry key sets, three resource IDs, exact paths, ordered consumers, ordering, duplicate rules, and unknown-field behavior. |
| Projection identity | Bind raw-byte resource hashes, raw-byte manifest SHA-256, and a sorted repository-target-path plus raw-byte-digest projection-set SHA-256. |
| Compact-scan placement | Copy the four questions directly into governed skill text from one checked contributor shared block so non-behavior work needs no formal-resource read. |
| Downstream context | Consume exact cited approved rows first; expand to the compact core only for missing, stale, unknown, ambiguous, conflicting, or escaped identities. Do not create a context packet. |
| Measurement | Use a stage-family fixture to record mapped, initially loaded, and expandable resources; report static canonical bytes and resource counts without a hard budget or runtime token claim. |
| Rollback unit | Separate the tracked source/manifest/skill/projection/validator/selector transaction from generated, packed, archived, and installed proof. Before activation, revert or abandon tracked changes and discard or regenerate derived output; after activation, preserve immutable-release rollback. |

## Architecture-review R1 resolution

- `PBS-AR1` is addressed by the exact closed YAML schema in ADR-20260729 and
  matching Runtime and Crosscutting summaries.
- `PBS-AR2` is addressed by separating the tracked activation transaction from
  the derived proof set in the ADR, Runtime View, Deployment View,
  Crosscutting Concepts, Quality Requirements, Risks, and component diagram.
- No owner decision was required, and neither correction adds a runtime
  service, tracks generated packages, or changes the approved feature
  behavior.

## Requirement-to-architecture mapping

| Requirements | Architecture surface |
| --- | --- |
| `PBS-R001`-`PBS-R006` | Architecture Constraints, Runtime View activation flow, and ADR compatibility/supersession boundary preserve `boundary-first-v1`, pending behavior, grandfathering, and active-only formal adoption. |
| `PBS-R007`-`PBS-R011` | Solution Strategy, component diagram, Runtime View steps 1-2, and ADR direct checked compact-scan placement. |
| `PBS-R012`-`PBS-R016`, `PBS-R032`-`PBS-R034` | Building Block View, component diagram, Deployment View, Crosscutting Concepts, and ADR exact resource ownership, manifest, identities, projection, package parity, and atomic activation. |
| `PBS-R017`-`PBS-R020` | Building Block View and Runtime View specify cited-row-first downstream consumption and owner routing on expansion. |
| `PBS-R021`-`PBS-R024` | Compact-core ownership retains interaction, example, and non-Cartesian scenario rules; stage-local text retains semantic decision authority. |
| `PBS-R025`-`PBS-R031` | Runtime View step 10, component diagram, validation layering, and ADR define path-owned selector composition and bounded structural claims. |
| `PBS-R035`-`PBS-R038` | Deployment View, Crosscutting Concepts, ADR, quality scenarios, and risks preserve historical artifacts, coherent rollback, diagnostics, package portability, and external-action boundaries. |

## arc42 and C4 impact

- Introduction and Goals: progressive resource and automatic-scan goal.
- Architecture Constraints: exact ownership, manifest, and loading constraints.
- Context and Scope: unaffected; repository actors and external systems do not
  change.
- Solution Strategy: progressive disclosure and artifact-sliced reads.
- Building Block View: progressive boundary-guidance container and focused
  Level 2 decomposition.
- Runtime View: projection, selector, measurement, activation, failure, and
  rollback flow.
- Deployment View: exact packaged resources and manifest boundaries.
- Crosscutting Concepts: source ownership, projection identity, compact-scan
  drift, activation, rollback, and measurement.
- Architecture Decisions: new ADR and scoped revision of ADR-20260728.
- Quality Requirements: proportionality, parity, activation, rollback, and
  measurement scenarios.
- Risks and Technical Debt: semantic split, copied-scan drift, manifest/code
  drift, mixed selector sets, measurement claims, and interrupted projection.
- Glossary: compact core, family resource, resource manifest, projection-set
  identity, and revised activation record.
- C4 context: unchanged with rationale.
- C4 container: updated for the progressive-guidance container.
- C4 component: added because container prose alone cannot explain resource
  ownership, projection, selector composition, activation, and evidence flow.
- Deployment diagram: not required; repository packaging boundaries are fully
  expressed by Deployment View prose and the focused component diagram.

## Alternatives and consequences

The ADR records rejected full-reference, compatibility-alias, Python-inventory,
resource-loaded scan, context-packet, and hard-budget alternatives. The
selected design adds two bounded resources and a manifest while avoiding a
second semantic model, runtime service, generated context packet, or hard
budget.

## Security and privacy

The design adds no credentials, personal data, network dependency, runtime
attestation, hosted service, or external mutation authority. Diagnostics and
measurement evidence remain repository-relative and exclude private
machine-local paths.

## Validation

- `python scripts/validate-change-metadata.py docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md --path docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/change.yaml --path docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/evidence/architecture-authoring.md`
- `python scripts/validate-markdown-readability.py docs/architecture/system/architecture.md docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/evidence/architecture-authoring.md`
- `git diff --check -- docs/architecture/system/architecture.md docs/architecture/system/diagrams/container.mmd docs/architecture/system/diagrams/component-boundary-guidance.mmd docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/change.yaml docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/evidence/architecture-authoring.md`

Results are recorded in the owning change metadata.
