# Boundary-first compact core

Boundary model version: boundary-first-v1

Use this compact core when a stage needs the shared boundary vocabulary or must interpret approved boundary, interaction, or proof IDs.
Examples illustrate governed behavior; they never define the complete boundary.

## Compact scan

Before a qualifying stage-owned decision, ask:

1. Which inputs or actors can change the outcome?
2. Which state or timing conditions can change the outcome?
3. Which public, sibling, helper, or alternate path can change the outcome?
4. Which failure, retry, recovery, compatibility, or external condition can change the outcome?

The scan identifies potentially outcome-changing conditions.
It does not by itself create records, IDs, proof maps, artifacts, or a user-visible scenario inventory.

## Core dimensions

Classify every core dimension exactly once.

| Dimension ID | Boundary ID prefix | Question |
| --- | --- | --- |
| `input-domain` | `BND-INPUT-` | Which values, presence states, malformed values, limits, and unknown inputs are admitted? |
| `state-lifecycle` | `BND-STATE-` | Which current, stale, terminal, legal-transition, and illegal-transition states exist? |
| `identity-authority` | `BND-AUTH-` | Which identity, owner, permission, authority, scope, and freshness rules govern behavior? |
| `composition-path` | `BND-COMPOSE-` | Which public, helper, sibling, alternate, bypass, and composed paths are material? |
| `temporal-retry` | `BND-TEMPORAL-` | Which ordering, duplication, concurrency, retry, replay, and idempotency cases matter? |
| `failure-recovery` | `BND-RECOVERY-` | Which failure, interruption, partial-work, rollback, resume, reconciliation, and dependency-failure cases matter? |
| `compatibility-migration` | `BND-COMPAT-` | Which historical data, old clients, mixed versions, migration, retirement, and rollback cases matter? |
| `external-environment` | `BND-ENV-` | Which external systems, resources, filesystem, network, platform, and operating limits matter? |

Applicability is exactly `applicable` or `not-applicable`.
An applicable dimension cites governing requirements and at least one boundary.
A not-applicable dimension uses the ASCII `-` sentinel for requirement and boundary IDs and gives a concise rationale.
Undecidable applicability is a review blocker, not a third durable value.
Feature-specific dimensions and cross-feature boundary imports are not part of `boundary-first-v1`.

## Identifier and serialization rules

- Boundary IDs use `^BND-(INPUT|STATE|AUTH|COMPOSE|TEMPORAL|RECOVERY|COMPAT|ENV)-[0-9]{3}$`.
- Interaction IDs use `^INT-[0-9]{3}$`.
- Proof obligation IDs use `^PRF-[0-9]{3}$`.
- An empty or inapplicable cell uses the literal ASCII `-`.
- Multiple IDs are unique and separated by comma followed by one ASCII space.
- Ordering follows first governing use and stays stable downstream.
- Every boundary is defined exactly once in its owning feature contract.

## Example rule

Classify each behavioral example as exactly one of:

- `illustration`: links governing requirement and boundary IDs;
- `regression`: carries the same links plus one stable defect or regression ID;
- `discovery`: carries one stable gap ID and routes upstream without creating normative behavior.

Every cited boundary belongs to the same feature record.
Every cited requirement is governed by every cited boundary.

## Interaction rule

Select interactions from actual composed hazards rather than a Cartesian product.
Consider stale authority, partial retry, public or helper bypass, sibling drift, compatibility migration, and incident-derived hazards when admitted by the requirements.
Select an interaction whenever one boundary changes another boundary's success, failure, stale, interrupted, recovery, or stop outcome.

Every interaction cites at least two defined boundaries.
When none is selected, replace the table with:

```text
No interaction selected: <requirement-grounded rationale>
```

## Consumption and upstream-gap routing

Downstream stages consume exact approved rows and stable IDs.
They do not recreate applicability, rename IDs, or infer new outcomes.
Expand the approved slice when an ID is missing, stale, unknown, ambiguous, conflicting, or cannot explain an observed outcome.
Route a new or changed normative outcome to the feature-spec owner.
Route a missing proof obligation that does not change behavior to the proof-map owner.

## Structural validation and semantic review

Structural validation checks closed versions, headings, columns, values, identifier grammar, uniqueness, references, mapped-resource presence, and byte parity.
It does not prove applicability, completeness, interaction adequacy, milestone isolation, proof adequacy, implementation fidelity, or final coherence.

Semantic review judges whether the applicable boundaries, interactions, examples, milestones, proof, implementation, and evidence are adequate at the reviewer's owned layer.
Neither examples nor deterministic validators may invent normative behavior.

## Scenario stop rule

Select scenarios for distinct observable outcomes, authority crossings, partial or irreversible state, retry or ordering behavior, material composed paths, compatibility or external behavior, and named regressions.
Stop when every applicable boundary and selected interaction has direct proof and another scenario would repeat an already-proved outcome without adding one of those hazards.
Never require a Cartesian product of dimensions, partitions, boundaries, interactions, or scenario inputs.

## Portable stop conditions

Stop and surface a gap when:

- a core dimension is absent, duplicated, or uses an unknown value;
- non-applicability lacks a requirement-grounded rationale;
- an example is the only owner of behavior;
- an applicable boundary or selected interaction lacks direct proof;
- helper proof substitutes for an admitted public or sibling path;
- evidence is missing, stale, circular, caller-asserted, or broader than its claim; or
- a discovered boundary requires an upstream owner decision.

The method is self-contained published guidance.
It requires no specific agent runtime, model identity, network connection, sandbox, process-isolation mechanism, workspace mutation interceptor, repository-local attestation store, or immutable runtime evidence publication.
