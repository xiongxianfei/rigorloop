# Composed boundary-first fixture

## Status

approved

boundary_contract: boundary-first-v1

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: FIX-R001, FIX-R002

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | FIX-R001 | BND-INPUT-001 | - |
| state-lifecycle | applicable | FIX-R002 | BND-STATE-001 | - |
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
| BND-STATE-001 | state-lifecycle | FIX-R002 | initial to active, active to terminal | terminal is immutable | continue, stop | FIX-R002 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | FIX-R001, FIX-R002 | BND-INPUT-001, BND-STATE-001 | invalid input attempts a terminal transition | reject without changing state |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| FIX-E001 | illustration | FIX-R001 | BND-INPUT-001 | - | - |
| FIX-E002 | regression | FIX-R002 | BND-STATE-001 | FIX-REG-001 | - |
