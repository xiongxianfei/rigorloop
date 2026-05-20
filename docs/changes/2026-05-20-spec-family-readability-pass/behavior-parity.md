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

### Representative input

Representative input: `specs/spec-family-readability-pass.md`.

This input exercises the `spec-review` skill's core responsibilities:
reviewing requirement clarity, normative language, completeness, testability,
examples, compatibility, observability, security/privacy, non-goals,
acceptance criteria, material findings, recording state, eventual test-spec
readiness, and stop conditions.

### Parity classification

| Compared behavior | Baseline expectation | Edited expectation | Classification | Evidence |
| --- | --- | --- | --- | --- |
| Review dimensions | `spec-review` evaluates 10 named dimensions. | `spec-review` evaluates the same 10 named dimensions in a table. | `equivalent` | Content-preservation matrix in `behavior-preservation.md`. |
| Review-dimension verdict values | Review dimensions use `pass`, `concern`, and `block`. | Same values are defined once in `Review dimension verdict`; review dimensions reference `<review dimension verdict>`. | `equivalent` | Enum authority map in `behavior-preservation.md`. |
| Review coverage guidance | Normal, empty, boundary, error, permission, migration, rollout, rollback, old-client, old-data behavior, and observable acceptance guidance remains required when relevant. | Same guidance remains unchanged after the review-dimension table. | `equivalent` | Content-preservation matrix in `behavior-preservation.md`. |
| Finding severity and material-finding behavior | Finding severity and material-finding requirements define review finding shape. | Finding severity and material-finding requirements are unchanged. | `equivalent` | Diff inspection for M2. |
| Review output skeleton | Skeleton defines result, findings, test-spec readiness, and stop condition. | Skeleton is unchanged. | `equivalent` | Content-preservation matrix in `behavior-preservation.md`. |

### Regression assessment

No M2 representative-output difference is classified as `regression`.

## M3. Test-Spec Skill Readability And Generated Output Proof

### Representative input

Representative input: `specs/spec-family-readability-pass.md` and
`docs/plans/2026-05-20-spec-family-readability-pass.md`.

This input exercises the `test-spec` skill's core responsibilities: mapping
requirements, examples, edge cases, coverage expectations, milestone
boundaries, fixtures, validation commands, generated-output proof, and
readiness into a traceable test specification before implementation.

### Parity classification

| Compared behavior | Baseline expectation | Edited expectation | Classification | Evidence |
| --- | --- | --- | --- | --- |
| Normalized invocation boundary | `test-spec` stops for unreviewed or unstable specs and for `not-ready` or `not-assessed` spec-review outcomes. | Stop conditions remain unchanged and before normal output guidance. | `equivalent` | Content-preservation matrix in `behavior-preservation.md`. |
| Required test-spec sections | `test-spec` requires 19 baseline sections in order. | `test-spec` requires the same 19 sections in a table in the same order. | `equivalent` | Content-preservation matrix in `behavior-preservation.md`. |
| Test spec status values | Required sections and output skeleton permit `draft`, `active`, `abandoned`, `superseded`, and `archived`. | Same values are defined once in `Test spec status`; required sections and output skeleton reference `<test spec status>`. | `equivalent` | Enum authority map in `behavior-preservation.md`. |
| Test case level values | Test case format and output skeleton permit `unit`, `integration`, `e2e`, `smoke`, and `manual`. | Same values are defined once in `Test case level`; test-case format and output skeleton reference `<test case level>`. | `equivalent` | Enum authority map in `behavior-preservation.md`. |
| Coverage map level values | Requirement coverage map permits `unit`, `integration`, `e2e`, `smoke`, `manual`, `contract`, and `migration`. | Same values are defined once in `Coverage map level`; requirement coverage map references `<coverage map level>`. | `equivalent` | Enum authority map in `behavior-preservation.md`. |
| Coverage rules | Five baseline coverage rules govern `MUST` requirements, errors, migration/compatibility, architectural boundaries, and bug regressions. | The same five coverage rules are presented in a table in the same order. | `equivalent` | Content-preservation matrix in `behavior-preservation.md`. |
| Output skeleton structure | Skeleton contains the same top-level headings from `Status` through `Readiness`. | Skeleton contains the same top-level headings from `Status` through `Readiness`. | `equivalent` | Content-preservation matrix in `behavior-preservation.md`. |
| Rules and expected output | Rules and expected-output obligations control behavior invention, coverage honesty, integration risk, durable states, and handoff. | Rules and expected-output obligations are unchanged. | `equivalent` | Diff inspection for M3. |

### Regression assessment

No M3 representative-output difference is classified as `regression`.
