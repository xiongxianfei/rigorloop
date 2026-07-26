# Portable text normalizer test spec

## Status

active

Boundary model version: v1
Boundary model scope: R1-R4

## Test strategy

Exercise every applicable partition directly and retain explicit non-applicability as feature-spec evidence rather than inventing tests for absent behavior.

## Boundary disposition

| Dimension ID | Applicability | Governing rationale | Test case IDs |
| --- | --- | --- | --- |
| canonical-trust | applicable | R1, R2, R3 | T1, T2, T3 |
| identity-freshness | not-applicable | No persisted identity is consumed. | - |
| closed-vocabulary | applicable | R1, R4 | T1, T2 |
| state-transition | not-applicable | The function is stateless. | - |
| authorization-scope | not-applicable | The function grants no authority. | - |
| mutation-atomicity | not-applicable | The function performs no mutation. | - |
| interruption-recovery | not-applicable | The contract exposes one returned result and no partial state or recovery obligation. | - |
| concurrency-idempotency | not-applicable | The pure result has no shared state. | - |
| composition-bypass | not-applicable | Conformance is defined only for this public normalizer contract; wrappers and alternate entrypoints may claim conformance only by preserving it. | - |
| compatibility-migration | not-applicable | No legacy representation exists. | - |
| outcome-stop | applicable | R2, R3, R4 | T1, T2, T3 |
| evidence-claims | applicable | R1, R2, R3, R4 | T1, T2, T3 |

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| text.proof.canonical | R1, R2, R3 | text.canonical.requirements | T1, T2, T3 | automated | - |
| text.proof.evidence | R1, R2, R3, R4 | text.evidence.tests | T1, T2, T3 | automated | - |
| text.proof.mode | R1, R4 | text.mode.valid, text.mode.unknown | T1, T2 | automated | - |
| text.proof.outcome | R2, R3, R4 | text.outcome.value, text.outcome.error | T1, T2, T3 | automated | - |

## Test cases

T1. For every scalar in the fixed R2 trim set, place it at each edge and in the interior; require edge removal and interior preservation. Stable case `T1-CANONICAL-PAIR` surrounds U+00E9 and the scalar-distinct U+0065 U+0301 sequence with trim scalars and requires each distinct interior sequence unchanged. Stable case `T1-NONTRIM-BOUNDARIES` places ASCII, combining-mark, BMP non-ASCII, and supplementary non-members adjacent to trimmed edges and requires trimming to stop at each member. Every case requires the exact `trim` success record and a failure-identifiable case ID.

T2. Exercise the closed unknown-mode partition with stable cases `T2-EMPTY` (empty), `T2-CASE` (`TRIM` and `Preserve`), `T2-FUTURE` (`trim-v2`), `T2-CANONICAL-CLOSURE` (enumerate the canonical-normalization closure of the two ASCII accepted tokens and prove it contains no scalar-distinct accepted alias), and `T2-OTHER` (deterministically generate non-equal scalar strings across empty, one-scalar, combining-mark, non-ASCII, and multi-scalar classes). Every case requires exactly `{"error":"unknown-mode"}` and asserts that `mode` and `text` fields are absent.

T3. Use stable cases `T3-EMPTY`, `T3-ASCII`, `T3-TRIM-SCALARS`, and `T3-CANONICAL-PAIR` (U+00E9 versus the scalar-distinct U+0065 U+0301 sequence), plus `T3-GENERATED`, a deterministic seed-`0x50544E31` corpus over empty, ASCII, every trim-set member, combining marks, BMP non-ASCII, and supplementary scalars at lengths 0 through 4. For each corpus member, require scalar-for-scalar unchanged text and exactly `{"mode":"preserve","text":<original>}`; identify a failure by stable case ID and corpus index.

## Validation

Command ID: PTN-VALIDATE-1

Command: `python -m unittest -q tests.test_portable_text_normalizer`

Owner: implementation milestone owner

Milestone: portable-text-normalizer implementation

Classification: automated deterministic validation

Expected result: exit 0 after discovering and executing T1, T2, and T3. A nonzero exit, a missing named case, or zero discovered tests blocks implementation handoff.
