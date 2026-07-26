# Portable text normalizer

## Status

approved

Boundary model version: v1
Boundary model scope: R1-R4

## Problem

Callers need one portable text-normalization contract whose accepted modes and failure behavior do not vary by implementation.

## Goals

- Define the complete closed mode vocabulary and observable results.
- Model every core boundary dimension as applicable or explicitly not applicable.
- Preserve examples as governed illustrations or regressions rather than completeness claims.

## Non-goals

- Choosing a programming language, storage system, transport, or deployment topology.
- Adding locale-specific transformations or implicit mode aliases.

## Requirements

R1. The public normalizer contract accepts `mode` as a Unicode scalar-value string and `text` as a sequence of Unicode scalar values; it MUST accept exactly the mode values `trim` and `preserve` by exact scalar-sequence comparison without normalization or case folding. It performs no externally observable state mutation, authorization action, or hidden alternate-entrypoint behavior. Ill-formed encoded byte sequences are outside this typed API domain. A conformance claim MUST include executable evidence for the typed input domain and complete mode partition.

R2. `trim` MUST NOT normalize text; it removes only the longest leading and trailing sequences containing exactly these Unicode scalar values: U+0009-U+000D, U+0020, U+0085, U+00A0, U+1680, U+2000-U+200A, U+2028, U+2029, U+202F, U+205F, and U+3000. This set is version-independent and changes only through a contract revision. On success it returns exactly `{"mode":"trim","text":<normalized scalar-value string>}`. A conformance claim MUST include executable evidence for every listed edge scalar, interior preservation, and adjacent non-member stopping.

R3. `preserve` MUST perform no Unicode normalization and return the exact input scalar-value sequence unchanged as `{"mode":"preserve","text":<original scalar-value string>}`. A conformance claim MUST include executable evidence covering trim-set members and canonically equivalent but scalar-distinct sequences.

R4. Every other exact mode scalar sequence, including empty, differently cased, and future-looking values, MUST return exactly `{"error":"unknown-mode"}` and MUST NOT return `mode` or `text`. A conformance claim MUST include executable evidence for each named unknown-mode class. Because the accepted mode tokens contain only ASCII scalars and are invariant under Unicode normalization, no distinct canonically equivalent mode exists; that empty class is not an unknown-mode evidence obligation.

## Boundary model

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| canonical-trust | applicable | R1, R2, R3 | text.canonical.requirements | - |
| identity-freshness | not-applicable | - | - | No persisted identity is consumed. |
| closed-vocabulary | applicable | R1, R4 | text.mode.valid, text.mode.unknown | - |
| state-transition | not-applicable | - | - | The function is stateless. |
| authorization-scope | not-applicable | - | - | The function grants no authority. |
| mutation-atomicity | not-applicable | - | - | The function performs no mutation. |
| interruption-recovery | not-applicable | - | - | The contract exposes one returned result and no partial state or recovery obligation. |
| concurrency-idempotency | not-applicable | - | - | The pure result has no shared state. |
| composition-bypass | not-applicable | - | - | Conformance is defined only for this public normalizer contract; wrappers and alternate entrypoints may claim conformance only by preserving it. |
| compatibility-migration | not-applicable | - | - | No legacy representation exists. |
| outcome-stop | applicable | R2, R3, R4 | text.outcome.value, text.outcome.error | - |
| evidence-claims | applicable | R1, R2, R3, R4 | text.evidence.tests | - |

Extensions: none.

## Examples

| Example ID | Role | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap |
| --- | --- | --- | --- | --- | --- |
| text.example.preserve | illustration | R1, R3 | text.mode.valid, text.outcome.value | - | - |
| text.example.trim | illustration | R1, R2 | text.mode.valid, text.outcome.value | - | - |
| text.example.unknown | regression | R1, R4 | text.mode.unknown, text.outcome.error | text.regression.unknown-mode | - |

## Interactions

None selected. The closed mode and outcome partitions do not create a cross-boundary hazard.

## Observable behavior and errors

The input domain and the success/error records are closed by R1-R4. A result is exactly one success record or the error-only record; fields are never combined across those alternatives.

## Compatibility

The contract is additive for a new normalizer. Future modes require a contract revision and may not be accepted implicitly.

## Acceptance criteria

- Both valid modes produce the exact requirement-defined result record.
- Every scalar in the fixed trim set is removed at both edges and preserved in the interior; adjacent scalars outside the set stop trimming.
- Empty, differently cased, and future-looking modes fail with `unknown-mode` and no text.
- Every core boundary dimension has one explicit applicability decision.
- Every example links to governing requirements and boundary IDs.
