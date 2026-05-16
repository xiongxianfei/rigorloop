# Spec Review R2

Review ID: spec-review-r2
Stage: spec-review
Round: 2
Reviewer: Codex spec-review skill
Target: specs/rigorloop-cli-lockfile.md
Reviewed artifact: specs/rigorloop-cli-lockfile.md
Review date: 2026-05-15
Recording status: recorded
Status: changes-requested

## Scope

Reviewed the revised RigorLoop CLI lockfile contract after `spec-review-r1` finding `SR1-F1` was accepted and the spec was updated with a complete `schema_version: 1` lockfile document shape.

The review focused on whether the revised spec now defines the durable lockfile shape precisely enough for architecture, test-spec, and implementation without guessing. No implementation code was reviewed.

## Dimension Results

| Dimension | Result | Notes |
|---|---|---|
| Requirement clarity | block | `SR1-F1` is resolved, but local archive lockfile semantics now conflict with the allowed first-slice `source` value. |
| Normative language | concern | The new shape requirements are normative, but `R18c` conflicts with `R20` and the input surface. |
| Completeness | concern | Complete document shape, unknown fields, missing fields, and unsupported schema behavior are covered. Local archive write behavior remains inconsistent. |
| Testability | block | Tests cannot determine whether `--from-archive` writes a lockfile with `source: local-archive`, `source: release-archive`, or blocks durable lockfile writes. |
| Examples | concern | The full document example is now concrete, but it covers only release archive mode while the spec still names local archive mode. |
| Compatibility | pass | Existing first-slice projects without lockfiles remain valid, unknown future shapes block, and public npm publication remains out of scope. |
| Observability | pass | JSON, human output, drift reporting, and exit behavior are covered. |
| Security/privacy | pass | The lockfile does not record absolute local paths and keeps the adapter trust boundary intact. |
| Non-goals | pass | Exclusions for `new-change`, `status`, `validate`, non-Codex adapters, workflow outputs, and npm publishing are explicit. |
| Acceptance criteria | concern | Acceptance criteria cover full lockfile shape and unknown-field blocking, but not the local archive source conflict. |

## Prior Finding Closeout

| Finding ID | Result | Evidence |
|---|---|---|
| SR1-F1 | closed | The revised spec defines the full top-level shape with `schema_version`, `rigorloop`, `manifest`, and `generated.adapters[]`; it defines generated adapter fields and the strict first-slice unknown-field policy. |

## Findings

### SR2-F1: Local archive lockfile source semantics conflict

Finding ID: SR2-F1

Severity: blocking

Location: `specs/rigorloop-cli-lockfile.md:143`, `specs/rigorloop-cli-lockfile.md:183`, `specs/rigorloop-cli-lockfile.md:203`, `specs/rigorloop-cli-lockfile.md:245`

Evidence: The spec includes `rigorloop init --adapter codex --from-archive <path>` as an input and `R20` says a local-archive Codex entry must include the basename of the local archive. However, `R18c` says the first-slice allowed `source` value is `release-archive`, and the complete YAML shape only shows `source: release-archive`. Architecture and tests would have to guess whether local archive mode writes no lockfile, writes `source: local-archive`, or records a local install as `source: release-archive`.

Required outcome: The spec must define one consistent local archive lockfile rule before architecture, test-spec, or implementation relies on it.

Safe resolution path: Choose one of these contracts:

- Allow local archive durable lockfile writes and define `source: local-archive` as a first-slice allowed value, with `archive` set to the basename and `release` still recording the metadata release tag.
- Or keep `source: release-archive` as the only first-slice durable lockfile source and explicitly block durable lockfile writes for `--from-archive`, while preserving dry-run planned lockfile output if desired.

## Requirement Notes

- `R17a` through `R17h`: pass; they resolve the missing top-level document shape.
- `R18` through `R18i`: concern; `R18c` conflicts with local archive mode.
- `R20`: concern; it implies local archive entries are in scope but does not have a consistent allowed `source` value.
- `R23c` through `R23k`: pass; unknown-field and unsupported-shape policy is now deterministic.
- `R34` through `R45c`: concern only where update behavior depends on local archive source semantics.

## Recommendation

Changes requested.

Immediate next repository stage: spec.

Eventual test-spec readiness: not-ready.

Stop condition: revise `specs/rigorloop-cli-lockfile.md` to define local archive lockfile semantics consistently, then rerun `spec-review`.
