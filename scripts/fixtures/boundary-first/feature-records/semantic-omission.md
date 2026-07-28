# Structurally valid semantic-omission fixture

boundary_contract: boundary-first-v1

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: FIX-R001

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | FIX-R001 | BND-INPUT-001 | - |
| state-lifecycle | not-applicable | - | - | Reviewer must judge whether hidden state exists. |
| identity-authority | not-applicable | - | - | Reviewer must judge whether authority exists. |
| composition-path | not-applicable | - | - | Reviewer must judge whether another path exists. |
| temporal-retry | not-applicable | - | - | Reviewer must judge whether retry exists. |
| failure-recovery | not-applicable | - | - | Reviewer must judge whether recovery exists. |
| compatibility-migration | not-applicable | - | - | Reviewer must judge whether history exists. |
| external-environment | not-applicable | - | - | Reviewer must judge whether a dependency exists. |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | FIX-R001 | present | accepted | continue | FIX-R001 |

## Selected interactions

No interaction selected: Reviewer must judge whether a hidden composed hazard exists.

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| FIX-E001 | illustration | FIX-R001 | BND-INPUT-001 | - | - |
