# Portable text normalizer

## Status

draft

## Related proposal

Authoritative behavior request in this change.

## Goal and context

Specify portable normalization of text under two closed modes and define failure for every unknown mode.

Boundary model version: v1
Boundary model scope: R1-R4

## Boundary model

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| canonical-trust | not-applicable | - | - | The requirements define behavior without selecting among conflicting authoritative sources. |
| identity-freshness | not-applicable | - | - | The requirements do not bind evidence to an identity or define staleness. |
| closed-vocabulary | applicable | R1, R4 | mode.closed-values | - |
| state-transition | not-applicable | - | - | The normalizer has no requirement-owned lifecycle states or transitions. |
| authorization-scope | not-applicable | - | - | The requirements define no authorization decision. |
| mutation-atomicity | not-applicable | - | - | The requirements define no persistent mutation or commit point. |
| interruption-recovery | not-applicable | - | - | The requirements define no prepared or interrupted work. |
| concurrency-idempotency | not-applicable | - | - | The requirements define no concurrent, duplicate, or replayed work. |
| composition-bypass | not-applicable | - | - | The requirements define behavior independent of implementation paths. |
| compatibility-migration | not-applicable | - | - | The requirements define no prior representation or migration. |
| outcome-stop | applicable | R2, R3, R4 | outcome.normalization-results | - |
| evidence-claims | not-applicable | - | - | The requirements define no evidence or claim contract. |

Extensions: none.

## Examples

| Example ID | Role | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap |
| --- | --- | --- | --- | --- | --- |
| example.trim-whitespace | illustration | R1, R2 | mode.closed-values, outcome.normalization-results | - | - |
| example.preserve-text | illustration | R1, R3 | mode.closed-values, outcome.normalization-results | - | - |
| example.reject-unknown | illustration | R4 | mode.closed-values, outcome.normalization-results | - | - |

Example example.trim-whitespace: trim surrounding Unicode whitespace
Given text with leading and trailing Unicode whitespace
When normalization uses mode `trim`
Then the returned text has that leading and trailing Unicode whitespace removed.

Example example.preserve-text: preserve text
Given any input text
When normalization uses mode `preserve`
Then the returned text is unchanged.

Example example.reject-unknown: reject an unknown mode
Given a mode other than `trim` or `preserve`
When normalization is requested
Then the result is `unknown-mode` and contains no text.

## Interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Rationale |
| --- | --- | --- | --- |
| interaction.mode-outcome | R1, R2, R3, R4 | mode.closed-values, outcome.normalization-results | composed-path |

## Glossary

Unicode whitespace: whitespace classified as such by Unicode.

## Requirements

R1. The normalizer MUST accept exactly the closed modes `trim` and `preserve`.

R2. In `trim` mode, the normalizer MUST remove leading and trailing Unicode whitespace from the input text.

R3. In `preserve` mode, the normalizer MUST return the input text unchanged.

R4. For every unknown mode, the normalizer MUST fail with `unknown-mode` and return no text.

## Inputs and outputs

The behavior consumes input text and a mode. Its observable result is the text required by R2 or R3, or the failure required by R4.

## State and invariants

There is no requirement-owned persistent state. The mode-dependent outcomes are governed by R1-R4.

## Error and boundary behavior

Unknown-mode behavior is governed by R4.

## Compatibility and migration

Not applicable; no compatibility or migration behavior is specified.

## Observability

The returned text or `unknown-mode` failure is the observable result. No logging or telemetry behavior is specified.

## Security and privacy

Not applicable; no security or privacy behavior is specified.

## Accessibility and UX

Not applicable; no user interface is specified.

## Performance expectations

Not applicable; no performance contract is specified.

## Edge cases

EC1. Input consisting only of Unicode whitespace in `trim` mode is governed by R2.

EC2. Input without leading or trailing Unicode whitespace in `trim` mode is governed by R2.

EC3. Empty input in either accepted mode is governed by R2 or R3 respectively.

EC4. Every mode other than `trim` and `preserve` is governed by R4.

## Non-goals

Input-shape, transport, performance, storage, logging, and implementation requirements are out of scope.

## Acceptance criteria

| Acceptance criterion | Governing requirement IDs |
| --- | --- |
| Both `trim` and `preserve` are accepted, and no other mode is accepted. | R1, R4 |
| Leading and trailing Unicode whitespace is removed in `trim` mode. | R2 |
| Input text is returned unchanged in `preserve` mode. | R3 |
| Every unknown mode produces `unknown-mode` and no text. | R4 |

## Open questions

None.

## Next artifacts

Spec review.

## Follow-on artifacts

None yet

## Readiness

Ready for spec-review.
