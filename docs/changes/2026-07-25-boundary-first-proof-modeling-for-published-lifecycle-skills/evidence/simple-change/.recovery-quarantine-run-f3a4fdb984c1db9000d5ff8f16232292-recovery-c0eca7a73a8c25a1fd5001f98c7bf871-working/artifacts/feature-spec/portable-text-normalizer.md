# Portable text normalizer

## Status

draft

## Related proposal

Authoritative behavior request supplied with this spec.

## Goal and context

Define the observable behavior of a portable text normalizer with two accepted modes and a closed failure outcome for every other mode.

## Glossary

- Unicode whitespace: code points with the Unicode `White_Space` property.

Boundary model version: v1
Boundary model scope: R1-R4

## Boundary model

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| canonical-trust | not-applicable | - | - | The requirements do not define competing authoritative sources. |
| identity-freshness | not-applicable | - | - | The behavior does not depend on identity or freshness. |
| closed-vocabulary | applicable | R1, R4 | mode.vocabulary | - |
| state-transition | not-applicable | - | - | The normalizer has no requirement-owned lifecycle states or transitions. |
| authorization-scope | not-applicable | - | - | The requirements define no authorization decisions. |
| mutation-atomicity | not-applicable | - | - | The requirements define no persistent mutation. |
| interruption-recovery | not-applicable | - | - | The requirements define no prepared or interruptible work. |
| concurrency-idempotency | not-applicable | - | - | The requirements define no concurrency, replay, or duplicate-work behavior. |
| composition-bypass | not-applicable | - | - | The requirements define no distinct public, helper, sibling, or retry paths. |
| compatibility-migration | not-applicable | - | - | The requirements define no legacy representation or migration. |
| outcome-stop | applicable | R4 | outcome.unknown-mode | - |
| evidence-claims | not-applicable | - | - | The requirements define no evidence or claim-validation behavior. |

Extensions:

| Extension ID | Title | Applicability | Rationale | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- | --- | --- |
| x.text.normalization | Mode-selected text transformation | applicable | The core dimensions do not represent the required trim and preserve transformations. | R2, R3 | text.transformation | - |

## Examples

| Example ID | Role | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap |
| --- | --- | --- | --- | --- | --- |
| example.trim-whitespace | illustration | R1, R2 | mode.vocabulary, text.transformation | - | - |
| example.preserve-text | illustration | R1, R3 | mode.vocabulary, text.transformation | - | - |
| example.unknown-mode | illustration | R4 | mode.vocabulary, outcome.unknown-mode | - | - |

## Interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Rationale |
| --- | --- | --- | --- |
| interaction.unknown-mode-stop | R1, R4 | mode.vocabulary, outcome.unknown-mode | state-coupling |

## Examples first

Example example.trim-whitespace: trim Unicode whitespace
Given input text with leading and trailing code points having the Unicode `White_Space` property
When normalization uses mode `trim`
Then those leading and trailing code points are removed

Example example.preserve-text: preserve text
Given any input text
When normalization uses mode `preserve`
Then the returned text is unchanged

Example example.unknown-mode: reject an unknown mode
Given a mode other than `trim` or `preserve`
When normalization is requested
Then it fails with `unknown-mode` and returns no text

## Requirements

R1. The normalizer MUST accept exactly the closed modes `trim` and `preserve`.

R2. In `trim` mode, the normalizer MUST remove leading and trailing Unicode whitespace, where whitespace means code points with the Unicode `White_Space` property.

R3. In `preserve` mode, the normalizer MUST return the input text unchanged.

R4. For every unknown mode, the normalizer MUST fail with `unknown-mode` and return no text.

## Inputs and outputs

The behavior consumes input text and a mode. It returns text for an accepted mode, or the `unknown-mode` failure with no text for every unknown mode.

## State and invariants

The accepted mode vocabulary is exactly `trim` and `preserve`. `preserve` leaves the input text unchanged. An `unknown-mode` failure returns no text.

## Error and boundary behavior

Every mode outside the closed accepted vocabulary fails with `unknown-mode` and returns no text. In `trim`, only leading and trailing code points with the Unicode `White_Space` property are removed.

## Compatibility and migration

Not applicable; no compatibility or migration behavior is specified.

## Observability

The observable results are returned text for an accepted mode or the `unknown-mode` failure with no text for an unknown mode.

## Security and privacy

Not applicable; no security or privacy behavior is specified.

## Accessibility and UX

Not applicable; no user interface behavior is specified.

## Performance expectations

Not applicable; no performance behavior is specified.

## Edge cases

EC1. In `trim`, input containing only Unicode `White_Space` code points returns text with all such leading and trailing code points removed.

EC2. In `trim`, non-whitespace code points between leading and trailing Unicode whitespace remain.

EC3. In `preserve`, leading and trailing Unicode whitespace remains unchanged.

EC4. Every value outside `trim` and `preserve` produces `unknown-mode` and no text.

## Non-goals

Input shape, transport, performance, storage, logging, and implementation behavior are outside this spec.

## Acceptance criteria

| Requirement ID | Acceptance criterion |
| --- | --- |
| R1 | The accepted mode set is exactly `trim` and `preserve`. |
| R2 | `trim` removes leading and trailing code points with the Unicode `White_Space` property. |
| R3 | `preserve` returns the input text unchanged. |
| R4 | Every unknown mode produces `unknown-mode` and no text. |

## Open questions

None.

## Next artifacts

Spec review.

## Follow-on artifacts

None yet

## Readiness

Ready for spec-review.
