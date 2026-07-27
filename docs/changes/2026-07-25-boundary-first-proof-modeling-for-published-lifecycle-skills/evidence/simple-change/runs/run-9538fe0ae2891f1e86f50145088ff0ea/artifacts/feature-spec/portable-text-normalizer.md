# Portable text normalizer

## Status

draft

## Related proposal

Authoritative behavior request supplied with this spec.

## Goal and context

Define the observable behavior of a portable text normalizer with two modes.

Boundary model version: v1
Boundary model scope: R1-R4

## Boundary model

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| canonical-trust | applicable | R2, R3 | text.preserve-input, text.trim-whitespace | - |
| identity-freshness | not-applicable | - | - | The behavior does not bind evidence to an identity or define freshness. |
| closed-vocabulary | applicable | R1, R4 | mode.closed-values | - |
| state-transition | not-applicable | - | - | The behavior defines no persistent states or transitions. |
| authorization-scope | not-applicable | - | - | The behavior defines no authorization decision. |
| mutation-atomicity | not-applicable | - | - | The behavior defines no stored mutation or commit point. |
| interruption-recovery | not-applicable | - | - | The behavior defines no prepared or interruptible work. |
| concurrency-idempotency | not-applicable | - | - | The behavior defines no concurrent or replayed operation. |
| composition-bypass | not-applicable | - | - | No direct, helper, sibling, or retry paths are part of the contract. |
| compatibility-migration | not-applicable | - | - | No prior representation or migration behavior is specified. |
| outcome-stop | applicable | R4 | outcome.unknown-mode | - |
| evidence-claims | not-applicable | - | - | The behavior defines no evidence-backed claim. |

Extensions: none.

## Examples

| Example ID | Role | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap |
| --- | --- | --- | --- | --- | --- |
| example.trim | illustration | R1, R2 | mode.closed-values, text.trim-whitespace | - | - |
| example.preserve | illustration | R1, R3 | mode.closed-values, text.preserve-input | - | - |
| example.unknown-mode | illustration | R4 | mode.closed-values, outcome.unknown-mode | - | - |

## Interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Rationale |
| --- | --- | --- | --- |
| interaction.mode-behavior | R1, R2, R3 | mode.closed-values, text.preserve-input, text.trim-whitespace | state-coupling |
| interaction.unknown-mode-stop | R1, R4 | mode.closed-values, outcome.unknown-mode | state-coupling |

## Glossary

Unicode whitespace: code points with the Unicode `White_Space` property.

## Examples first

Example example.trim: trim surrounding Unicode whitespace
Given input text `\u0020hello\u00A0` and mode `trim`
When the text is normalized
Then the returned text is `hello`.

Example example.preserve: preserve input exactly
Given input text `\u0020hello\u00A0` and mode `preserve`
When the text is normalized
Then the returned text is unchanged.

Example example.unknown-mode: reject an unknown mode
Given input text `hello` and mode `other`
When normalization is attempted
Then the result is `unknown-mode` and no text is returned.

## Requirements

R1. The normalizer MUST accept exactly the closed modes `trim` and `preserve`.

R2. In `trim` mode, the normalizer MUST remove leading and trailing Unicode whitespace, where whitespace means code points with the Unicode `White_Space` property.

R3. In `preserve` mode, the normalizer MUST return the input text unchanged.

R4. For every unknown mode, the normalizer MUST fail with `unknown-mode` and return no text.

## Inputs and outputs

The behavioral inputs are text and a mode. Successful normalization returns text. An unknown mode returns the `unknown-mode` failure and no text.

## State and invariants

The accepted mode vocabulary is exactly `trim` and `preserve`. The behavior is stateless.

## Error and boundary behavior

Every mode outside the accepted vocabulary produces `unknown-mode` and no text. In `trim` mode, only leading and trailing code points with the Unicode `White_Space` property are removed.

## Compatibility and migration

Not applicable; no compatibility or migration behavior is specified.

## Observability

Observable results are the returned text or the `unknown-mode` failure with no text. No logging or telemetry behavior is specified.

## Security and privacy

Not applicable; no security, authorization, retention, or disclosure behavior is specified.

## Accessibility and UX

Not applicable; no user interface is specified.

## Performance expectations

Not applicable; no performance contract is specified.

## Edge cases

- In `trim` mode, text containing no leading or trailing Unicode whitespace is returned without such removal.
- In `trim` mode, Unicode whitespace at both boundaries is removed.
- In `preserve` mode, Unicode whitespace at either boundary remains unchanged.
- Every value other than `trim` and `preserve` is an unknown mode.

## Non-goals

Input shape, transport, performance, storage, logging, and implementation behavior are outside this specification.

## Acceptance criteria

| Acceptance criterion | Requirement IDs |
| --- | --- |
| Only `trim` and `preserve` are accepted modes. | R1 |
| `trim` removes leading and trailing code points with the Unicode `White_Space` property. | R2 |
| `preserve` returns the input text unchanged. | R3 |
| Every unknown mode produces `unknown-mode` and no text. | R4 |

## Open questions

None.

## Next artifacts

Spec review.

## Follow-on artifacts

None yet

## Readiness

Ready for spec-review.
