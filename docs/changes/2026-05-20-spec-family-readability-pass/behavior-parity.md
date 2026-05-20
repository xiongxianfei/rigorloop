# Spec-Family Readability Pass Behavior Parity

## Status

active

Representative behavior parity supplements the source-to-destination
preservation matrix. It does not replace preservation proof.

## M1. Spec Skill Readability

### Representative input

Representative input: the accepted proposal
`docs/proposals/2026-05-20-spec-family-readability-pass.md`.

This input exercises the `spec` skill's core responsibilities: status
settlement reliance on accepted proposal state, examples-first spec authoring,
requirement and edge-case coverage, non-goals, acceptance criteria, next
artifacts, follow-on artifacts, and readiness.

### Parity classification

| Compared behavior | Baseline expectation | Edited expectation | Classification | Evidence |
| --- | --- | --- | --- | --- |
| Spec status values | Output skeleton permits `draft`, `approved`, `abandoned`, `superseded`, `archived`. | Same values are defined once in `Spec status`; output skeleton references `<spec status>`. | `equivalent` | Enum authority map in `behavior-preservation.md`. |
| Upstream status settlement result values | Report skeleton permits `updated`, `blocked`, `not-needed`. | Same values are defined once in `Settlement result`; report skeleton references `<settlement result>`. | `equivalent` | Enum authority map in `behavior-preservation.md`. |
| Required spec sections | `spec` requires the 21 baseline sections in order. | `spec` requires the same 21 sections in a table in the same order. | `equivalent` | Content-preservation matrix in `behavior-preservation.md`. |
| Output skeleton structure | Skeleton contains the same 21 top-level headings from `Status` through `Readiness`. | Skeleton contains the same 21 top-level headings from `Status` through `Readiness`. | `equivalent` | Content-preservation matrix in `behavior-preservation.md`. |
| Rules and handoff behavior | Rules and workflow handoff behavior control requirement quality and next-stage handoff. | Rules and workflow handoff behavior are unchanged. | `equivalent` | Diff inspection for M1. |

### Regression assessment

No M1 representative-output difference is classified as `regression`.

## M2. Spec-Review Skill Readability

Pending M2 implementation.

## M3. Test-Spec Skill Readability And Generated Output Proof

Pending M3 implementation.
