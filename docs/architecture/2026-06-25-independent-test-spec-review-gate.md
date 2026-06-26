# Independent Test-Spec-Review Gate Architecture

## Status

- approved

## Related artifacts

- Proposal: [Independent Test-Spec-Review Gate for Proof-Map Adequacy](../proposals/2026-06-25-independent-test-spec-review-gate.md)
- Spec: [Test-Spec-Review Gate](../../specs/test-spec-review-gate.md)
- ADR: [ADR-20260625-independent-test-spec-review-gate](../adr/ADR-20260625-independent-test-spec-review-gate.md)
- Plan: None yet

## Introduction and Goals

This architecture record explains how RigorLoop adds an independent `test-spec-review` gate without changing runtime application code. The design must make the lifecycle graph, artifact ownership, validator boundaries, skill inventory, and generated package impact visible before execution planning.

The primary goal is to ensure implementation consumes an independently reviewed proof map rather than merely an active test spec.

## Summary

The architecture adds one workflow stage and one public review skill using the existing review-family pattern. It changes repository workflow artifacts, skills, validators, and generated package proof, but it does not add a runtime service, persistent data store, external dependency, or deployment system.

## Requirements covered

| Requirement IDs | Architecture coverage |
| --- | --- |
| R1-R4 | Workflow graph and artifact-state separation. |
| R5-R12 | Review result, next-stage, and implementation-handoff enums. |
| R13-R18 | Proof-map review dimensions, manual proof, commands, and fixture boundaries. |
| R19-R21 | Staleness and upstream revision routing. |
| R22-R24 | Formal review record placement and claim boundaries. |
| R25-R28 | Skill routing, implement precondition, validator behavior, and generated package inclusion. |

## Architecture Constraints

- The workflow spec owns stage order and downstream-blocking semantics.
- The skill contract owns normalized skill shape, claim boundaries, resource maps, assets, and generated-output expectations.
- Test specs retain the durable artifact state `active`.
- Formal review approval is recorded in change-local review evidence, not in the test spec.
- Generated public adapter skill bodies are derived release archives and must not be hand-edited.
- The new gate must preserve `code-review` and `verify` as downstream backstops.

## Context and Scope

The affected system is the repository workflow artifact system:

- governing specs under `specs/`;
- canonical public skills under `skills/`;
- review assets under skill-local `assets/`;
- validators under `scripts/`;
- workflow guide and change-local review records under `docs/`;
- generated adapter support surfaces.

No product runtime, deployment service, database, API, or user interface boundary is affected.

## Solution Strategy

Use the existing review-family architecture pattern:

1. add a dedicated stage and skill for one review responsibility;
2. keep the reviewed artifact state independent from review status;
3. record formal reviews under `docs/changes/<change-id>/reviews/`;
4. validate closed enums and status/handoff consistency before downstream reliance;
5. package the new skill and assets through normal generation.

This avoids a new review engine or external routing service. The workflow remains artifact-driven and validator-backed.

## Proposed architecture

The proposed architecture is a stage-and-evidence extension to the existing workflow:

- add `test-spec-review` as a formal review stage after `test-spec`;
- add canonical skill source and review-result assets under `skills/test-spec-review/`;
- update neighboring stage skills so `test-spec` routes to review and `implement` requires approved review evidence;
- extend validators to recognize the new stage and fail closed on unknown closed-vocabulary values;
- include the skill and assets in generated adapter packages through normal generation.

## Building Block View

| Building block | Responsibility | Change |
| --- | --- | --- |
| Workflow contract | Stage order, obligations, blocking semantics | Insert `test-spec-review` between `test-spec` and `implement`. |
| Skill contract | New skill legitimacy, resource maps, assets, portability | Treat `test-spec-review` as justified by distinct recurring proof-map review ownership. |
| `test-spec` skill | Author active proof map | Route formal workflow-managed output to `test-spec-review`. |
| `test-spec-review` skill | Independently review proof-map adequacy | New canonical skill with result and finding assets. |
| `implement` skill | Consume approved proof before coding | Require current approved `test-spec-review` evidence. |
| Review validators | Parse review records and enforce closed vocabularies | Add stage/result fields and status/handoff consistency. |
| Generated adapters | Package public skills and assets | Include new skill and mapped assets through generation. |

## Interfaces and contracts

| Interface or contract | Contract change |
| --- | --- |
| Standard workflow chain | `plan-review -> test-spec -> test-spec-review -> implement`. |
| Test-spec artifact lifecycle | Durable status remains `active`; review approval is external evidence. |
| Review result | Closed `Review status`, `Immediate next stage`, and `Implementation handoff` fields. |
| Formal review records | `docs/changes/<change-id>/reviews/test-spec-review-r<n>.md` plus `review-log.md`. |
| Implementation precondition | Active test spec plus approved, current, recorded test-spec-review evidence. |
| Generated packages | Include new skill and mapped assets without hand-editing generated output. |

## Runtime View

Formal workflow-managed path:

```text
plan-review
-> test-spec
-> test-spec-review
-> implement
```

Review routing:

```text
approved
  -> Implementation handoff: allowed
  -> Immediate next stage: implement

changes-requested
  -> Implementation handoff: not-allowed
  -> Immediate next stage: test-spec revision or review-resolution

blocked
  -> Implementation handoff: not-allowed
  -> Immediate next stage: upstream revision or none

inconclusive
  -> Implementation handoff: not-allowed
  -> Immediate next stage: none
```

Staleness routing:

```text
approved review
-> substantive test-spec change
-> review stale
-> implementation handoff unavailable until re-review
```

## Deployment View

No runtime deployment changes are introduced.

Packaging impact exists for public skill distribution: generated Codex, Claude, and opencode adapter packages must include the new `test-spec-review` skill and skill-local assets. Canonical source remains under `skills/`.

## Crosscutting Concepts

| Concern | Architecture rule |
| --- | --- |
| Review independence | Review happens as a distinct stage before implementation consumes the proof map. |
| Closed vocabularies | Unknown review status, next-stage, and handoff values fail before consistency checks. |
| Artifact state separation | Test spec remains `active`; review record carries approval. |
| Portability | Published skill text uses project-local workflow surfaces and packaged assets, not repository-internal paths as customer requirements. |
| Security | Review-time command checks are optional and bounded to no-side-effect checks. |
| Observability | Every formal result records status, material findings, review paths, next stage, handoff, and stop condition. |

## Architecture Decisions

- [ADR-20260625-independent-test-spec-review-gate](../adr/ADR-20260625-independent-test-spec-review-gate.md) - adds a dedicated proof-map adequacy review gate instead of folding ownership into adjacent stages.

## Quality Requirements

| Quality | Scenario | Measure |
| --- | --- | --- |
| Traceability | A reviewer inspects implementation eligibility | Active test spec, approved review record, no-open-findings state, and staleness evidence are visible. |
| Safety | A review returns an unknown status | Validator fails before downstream routing. |
| Portability | Generated adapters are built | New skill and assets are present without hand-edited generated source. |
| Bounded cost | Reviewer validates a command claim | Only low-risk resolvability, help, or dry-run checks are permitted during review. |

## Risks and Technical Debt

- The first slice may rely on tracked review evidence and change comparison for stale-review detection rather than content hashes.
- The review-family result schema may accumulate repeated logic across review skills; a reusable schema can be proposed later if duplication grows.
- Model/vendor diversity remains a broader review-independence policy, not this stage's architecture.

## Glossary

- `proof-map adequacy`: whether the active test spec can prove the approved contract and plan without implementation guessing.
- `implementation handoff`: deterministic routing signal that either allows or blocks implementation after review.

## Next artifacts

- Architecture review.
- Plan after clean architecture review.

## Follow-on artifacts

- None yet.

## Readiness

Ready for `architecture-review`.
