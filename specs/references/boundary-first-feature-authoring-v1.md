# Boundary-first feature authoring

Boundary model version: boundary-first-v1

Use this owner-scoped guidance with the compact core when authoring or semantically reviewing a feature boundary record.

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

Partitions and transitions describe only states admitted by governing requirements.
Invariants state what must remain true.
Outcomes state success, failure, stale, interrupted, recovery, and stop behavior where applicable.
An example cannot create a boundary, invariant, or outcome.

## Example ownership

Use this table:

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |

Confirm every example is governed or is an explicit discovery.
Confirm no example created normative behavior.

## Selected interactions

Use this table for selected interactions:

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |

Confirm every selected interaction follows from requirement-owned hazards and cites at least two defined boundaries.
When none is selected, use the compact core's no-interaction form.

## Semantic authoring and review

Confirm all core dimensions are classified exactly once.
Confirm applicable boundaries own partitions or transitions, invariants, outcomes, and a governing requirement.
Confirm non-applicability is requirement-grounded.
Confirm selected interactions cover actual composed hazards without creating a Cartesian product.
Route any missing or changed normative outcome to feature-spec authoring before downstream reliance.
