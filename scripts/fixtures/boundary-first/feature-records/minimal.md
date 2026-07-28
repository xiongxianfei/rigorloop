# Minimal boundary-first fixture

boundary_contract: boundary-first-v1

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: FIX-R001

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | FIX-R001 | BND-INPUT-001 | - |
| state-lifecycle | not-applicable | - | - | No state exists. |
| identity-authority | not-applicable | - | - | No authority exists. |
| composition-path | not-applicable | - | - | One path exists. |
| temporal-retry | not-applicable | - | - | No retry exists. |
| failure-recovery | not-applicable | - | - | No mutation exists. |
| compatibility-migration | not-applicable | - | - | No history exists. |
| external-environment | not-applicable | - | - | No dependency exists. |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | FIX-R001 | present, missing, unknown | known values only | accept, reject | FIX-R001 |

## Selected interactions

No interaction selected: Only one requirement-owned boundary is applicable.

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| FIX-E001 | illustration | FIX-R001 | BND-INPUT-001 | - | - |
