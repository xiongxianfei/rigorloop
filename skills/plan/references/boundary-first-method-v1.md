# Boundary-first proof model

Boundary model version: boundary-first-v1

Use this method when authoring or evaluating a behavior contract, its proof
map, or a handoff that depends on those artifacts.
Examples illustrate governed behavior; they never define the complete
boundary.

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
A not-applicable dimension uses the ASCII `-` sentinel for requirement and
boundary IDs and gives a concise rationale.
Undecidable applicability is a review blocker, not a third durable value.
Feature-specific dimensions and cross-feature boundary imports are not part of
`boundary-first-v1`.

## Identifier and serialization rules

- Boundary IDs use
  `^BND-(INPUT|STATE|AUTH|COMPOSE|TEMPORAL|RECOVERY|COMPAT|ENV)-[0-9]{3}$`.
- Interaction IDs use `^INT-[0-9]{3}$`.
- Proof obligation IDs use `^PRF-[0-9]{3}$`.
- An empty or inapplicable cell uses the literal ASCII `-`.
- Multiple IDs are unique and separated by comma followed by one ASCII space.
- Ordering follows first governing use and stays stable downstream.
- Every boundary is defined exactly once in its owning feature contract.

## Feature-spec boundary record

Keep these four headings contiguous and in this order:

```md
## Boundary model
## Boundary definitions
## Selected interactions
## Example ownership
```

Start the model with:

```text
Boundary model version: boundary-first-v1
Boundary model scope: <governed requirement IDs>
```

Use this applicability table:

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |

Use this boundary-definition table:

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |

Partitions and transitions describe only states admitted by governing
requirements.
Invariants state what must remain true.
Outcomes state success, failure, stale, interrupted, recovery, and stop
behavior where applicable.
An example cannot create a boundary, invariant, or outcome.

## Examples

Classify each behavioral example as exactly one of:

- `illustration`: links governing requirement and boundary IDs;
- `regression`: carries the same links plus one stable defect or regression ID;
- `discovery`: carries one stable gap ID and routes upstream without creating
  normative behavior.

Use this table:

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |

Every cited boundary belongs to the same feature record.
Every cited requirement is governed by every cited boundary.

## Interactions

Select interactions from actual composed hazards rather than a Cartesian
product.
Consider stale authority, partial retry, public or helper bypass, sibling
drift, compatibility migration, and incident-derived hazards when admitted by
the requirements.
Select an interaction whenever one boundary changes another boundary's
success, failure, stale, interrupted, recovery, or stop outcome.

Use this table for selected interactions:

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |

Every interaction cites at least two defined boundaries.
When none is selected, replace the table with:

```text
No interaction selected: <requirement-grounded rationale>
```

## Test-spec proof record

The proof map consumes the exact boundary and interaction IDs from its
governing feature contract.
It never defines, renames, infers, or repairs them.
Start with the same model version and scope, then use:

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Coverage state is exactly `covered` or `gap`.
A covered row supplies every field required by its proof and automation mode
and uses `-` for the uncovered-gap ID.
A gap row supplies its requirements, boundary or interaction IDs, required
milestone, and one stable gap ID.
It uses `-` for test case, proof level, automation mode, command, evidence, and
manual-procedure fields.
A gap never counts as coverage and blocks downstream reliance.

Proof level is exactly `unit`, `integration`, `contract`, `end-to-end`,
`smoke`, or `manual`.
Automation mode is exactly `automated`, `manual`, or `hybrid`.
Automated proof uses `-` for manual procedures.
Manual and hybrid proof cite a stable manual procedure and evidence artifact.

Where admitted by a boundary, proof covers valid, invalid, missing,
additional, stale, substituted, unknown, and conflicting states.
Stateful proof covers legal and illegal transitions.
Mutation proof covers commit, partial, retry, reconciliation, conflict, and
replay.
Composed proof exercises the public path and every material sibling path, not
only a helper.

## Interaction and example ownership audit

Before accepting a record:

1. confirm every example is governed or is an explicit discovery;
2. confirm every selected interaction follows from requirement-owned hazards;
3. confirm no example or structural check created normative behavior;
4. confirm every applicable boundary and selected interaction has direct proof;
5. confirm proof uses exact IDs from the governing feature contract; and
6. route any missing boundary, outcome, or proof upstream as a visible gap.

## Structural validation and semantic review

Structural validation checks closed versions, headings, columns, values,
identifier grammar, uniqueness, references, mapped-resource presence, and byte
parity.
It does not prove applicability, completeness, interaction adequacy,
milestone isolation, proof adequacy, implementation fidelity, or final
coherence.

Semantic review judges whether the applicable boundaries, interactions,
examples, milestones, proof, implementation, and evidence are adequate at the
reviewer's owned layer.
Neither examples nor deterministic validators may invent normative behavior.

## Portable stop conditions

Stop and surface a gap when:

- a core dimension is absent, duplicated, or uses an unknown value;
- non-applicability lacks a requirement-grounded rationale;
- an example is the only owner of behavior;
- an applicable boundary or selected interaction lacks direct proof;
- helper proof substitutes for an admitted public or sibling path;
- evidence is missing, stale, circular, caller-asserted, or broader than its
  claim; or
- a discovered boundary requires an upstream owner decision.

The method is self-contained published guidance.
It requires no specific agent runtime, model identity, network connection,
sandbox, process-isolation mechanism, workspace mutation interceptor,
repository-local attestation store, or immutable runtime evidence publication.
