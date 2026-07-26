# Portable text normalizer

## Status

approved

Boundary model version: v1
Boundary model scope: R1-R4

## Requirements

R1. The normalizer MUST accept exactly `trim` and `preserve`.

R2. `trim` MUST remove leading and trailing Unicode whitespace.

R3. `preserve` MUST return the input text unchanged.

R4. An unknown mode MUST fail with `unknown-mode` and MUST NOT return text.

## Boundary model

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| canonical-trust | applicable | R1 | text.canonical.requirements | - |
| identity-freshness | not-applicable | - | - | No persisted identity is consumed. |
| closed-vocabulary | applicable | R1, R4 | text.mode.valid, text.mode.unknown | - |
| state-transition | not-applicable | - | - | The function is stateless. |
| authorization-scope | not-applicable | - | - | The function grants no authority. |
| mutation-atomicity | not-applicable | - | - | The function performs no mutation. |
| interruption-recovery | not-applicable | - | - | The operation is not interruptible. |
| concurrency-idempotency | not-applicable | - | - | The pure result has no shared state. |
| composition-bypass | not-applicable | - | - | One public function owns the behavior. |
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
