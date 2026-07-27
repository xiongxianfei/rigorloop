# Portable Text Normalizer

## Status

draft

## Related proposal

Direct behavior request.

## Goal and context

Define the observable behavior of a portable text normalizer with two modes.

## Glossary

Unicode whitespace: code points with the Unicode `White_Space` property.

## Examples first

The classified examples are recorded in the contiguous boundary record below.

Boundary model version: v1
Boundary model scope: R1-R4

## Boundary model

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| canonical-trust | not-applicable | - | - | No conflicting authority sources are part of this contract. |
| identity-freshness | not-applicable | - | - | The behavior does not depend on identity or freshness. |
| closed-vocabulary | applicable | R1, R4 | mode.closed-vocabulary | - |
| state-transition | not-applicable | - | - | The normalizer has no contract-level state transitions. |
| authorization-scope | not-applicable | - | - | The behavior has no authorization decisions. |
| mutation-atomicity | not-applicable | - | - | The contract defines no mutation. |
| interruption-recovery | not-applicable | - | - | The contract defines no prepared or interrupted work. |
| concurrency-idempotency | not-applicable | - | - | The contract defines no concurrent or replayed work. |
| composition-bypass | not-applicable | - | - | No direct, helper, public, sibling, or retry paths are specified. |
| compatibility-migration | not-applicable | - | - | No old representation or migration behavior is specified. |
| outcome-stop | applicable | R4 | outcome.unknown-mode | - |
| evidence-claims | not-applicable | - | - | The contract defines no evidence-based claims. |

Extensions:

| Extension ID | Title | Applicability | Rationale | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- | --- | --- |
| x.text.transformation | Mode-specific text transformation | applicable | The core dimensions do not represent the requested trim and preserve transformations. | R2, R3 | text.mode-transformation | - |

## Examples

| Example ID | Role | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap |
| --- | --- | --- | --- | --- | --- |
| example.trim.whitespace | illustration | R2 | text.mode-transformation | - | - |
| example.preserve.unchanged | illustration | R3 | text.mode-transformation | - | - |
| example.mode.unknown | illustration | R1, R4 | mode.closed-vocabulary, outcome.unknown-mode | - | - |

## Interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Rationale |
| --- | --- | --- | --- |
| interaction.mode.transformation | R1, R2, R3 | mode.closed-vocabulary, text.mode-transformation | composed-path |
| interaction.mode.stop | R1, R4 | mode.closed-vocabulary, outcome.unknown-mode | state-coupling |

## Requirements

R1. The normalizer MUST accept exactly the closed modes `trim` and `preserve`.

R2. In `trim` mode, the normalizer MUST remove leading and trailing Unicode whitespace, where whitespace means code points with the Unicode `White_Space` property.

R3. In `preserve` mode, the normalizer MUST return the input text unchanged.

R4. For every unknown mode, the normalizer MUST fail with `unknown-mode` and return no text.

## Inputs and outputs

The behavioral inputs are text and a mode governed by R1. The output is governed by R2, R3, and R4.

## State and invariants

No contract-level state is defined.

## Error and boundary behavior

Unknown-mode behavior is defined by R4. Unicode whitespace boundaries are defined by R2.

## Compatibility and migration

Not applicable; no compatibility or migration behavior is specified.

## Observability

The observable results are the returned text under R2 or R3, or the failure and absence of text under R4.

## Security and privacy

Not applicable.

## Accessibility and UX

Not applicable.

## Performance expectations

Not applicable.

## Edge cases

The closed mode boundary, Unicode whitespace boundary, unchanged-text outcome, and unknown-mode outcome are fully governed by R1-R4.

## Non-goals

Input shape, transport, performance, storage, logging, and implementation behavior are outside this specification.

## Acceptance criteria

| Requirement | Acceptance criterion |
| --- | --- |
| R1 | Exactly `trim` and `preserve` are accepted modes. |
| R2 | `trim` removes leading and trailing code points having the Unicode `White_Space` property. |
| R3 | `preserve` returns the input text unchanged. |
| R4 | Every unknown mode produces `unknown-mode` and no text. |

## Open questions

None.

## Next artifacts

Spec review.

## Follow-on artifacts

None yet.

## Readiness

Ready for spec-review.
