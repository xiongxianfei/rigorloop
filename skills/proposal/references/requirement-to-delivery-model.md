# Lightweight requirement-to-delivery model

Use this model when a stage needs to explain how an incoming need becomes requirements, design, work, implementation, or evidence.

## Requirement refinement

```text
RR → IR → SR → AR
```

- **RR — Raw Requirement:** the incoming need, normally represented by the existing request, issue, report, or referenced source.
- **IR — Initial Requirement:** the approved proposal-level direction. The proposal is the durable IR-level artifact.
- **SR — System Requirement:** observable, testable behavior owned by the specification.
- **AR — Allocated Requirement:** the conceptual assignment of an SR to an architecture or delivery boundary.

RR, IR, and AR do not require separate artifacts or identifiers. SR identities are the durable downstream requirement references. Architecture realizes SRs; planning allocates SRs and architecture boundaries into executable work.

## Work decomposition

```text
Epic → Feature → Story → Task
```

The two views are not equivalent hierarchies. Requirement refinement explains what is needed and where responsibility is allocated. Work decomposition explains how delivery effort is divided. Their relationship may be many-to-many.

For example:

```text
SR-01 → M1 and M2
SR-01 + SR-02 → M2
```

Here one requirement needs two work items, while one work item realizes two requirements. These mappings use existing SR and milestone identities; they create no new allocation entity.

Use only the work levels that improve the current change. Add a work level only when it materially improves ownership, sequencing, reviewability, traceability, or coordination. A modest change may use one milestone and a few tasks without Epic, Feature, or Story records.

## Traceability

The forward path is:

```text
incoming need → approved proposal → SR → architecture realization
→ allocated milestone or work item → implementation
```

The reverse evidence path is:

```text
evidence → implementation → allocated work → SR → approved proposal → incoming need
```

Every lower-level work item should explain why it exists. Every important SR should identify where it is realized and proved. A non-requirement obligation such as maintenance, packaging, migration, or documentation may be cited explicitly instead of inventing an SR.

## Authority boundary

This model explains relationships only. It creates no lifecycle stage, artifact, identifier, settlement authority, readiness claim, or required hierarchy. Each stage's local contract continues to own its artifact, decisions, stop conditions, and review authority. Deterministic checks may validate structure and references; formal review judges semantic adequacy.
