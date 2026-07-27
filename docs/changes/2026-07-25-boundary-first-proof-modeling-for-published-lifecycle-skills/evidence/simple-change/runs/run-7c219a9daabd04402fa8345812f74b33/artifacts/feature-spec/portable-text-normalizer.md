# Portable text normalizer

## Status

draft

## Related proposal

Authoritative behavior request supplied with this spec.

## Goal and context

Define the observable mode selection, text normalization, and unknown-mode failure behavior of a portable text normalizer.

## Glossary

- Unicode whitespace: characters classified as whitespace by the Unicode standard.
- Input text: the text supplied to the normalizer.

Boundary model version: v1
Boundary model scope: R1-R4

## Boundary model

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| canonical-trust | not-applicable | - | - | The requirements define no competing sources of authority. |
| identity-freshness | not-applicable | - | - | The behavior uses no identity-bound or freshness-sensitive evidence. |
| closed-vocabulary | applicable | R1 | mode.selection | - |
| state-transition | not-applicable | - | - | The requirements define no persistent states or transitions. |
| authorization-scope | not-applicable | - | - | The requirements define no authorization decisions. |
| mutation-atomicity | not-applicable | - | - | The requirements define no persistent mutation or commit point. |
| interruption-recovery | not-applicable | - | - | The requirements define no prepared or interruptible work. |
| concurrency-idempotency | not-applicable | - | - | The requirements define no concurrent, duplicate, or replayed work. |
| composition-bypass | not-applicable | - | - | The requirements define no distinct helper, public, sibling, or retry paths. |
| compatibility-migration | not-applicable | - | - | The requirements define no legacy representation or migration behavior. |
| outcome-stop | applicable | R4 | mode.unknown | - |
| evidence-claims | not-applicable | - | - | The requirements define no evidence-derived claims. |

Extensions:

| Extension ID | Title | Applicability | Rationale | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- | --- | --- |
| x.text.transformation | Text transformation | applicable | The feature contract distinguishes two observable transformations not represented by a core dimension. | R2, R3 | text.trim, text.preserve | - |

## Examples

| Example ID | Role | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap |
| --- | --- | --- | --- | --- | --- |
| example.trim | illustration | R1, R2 | mode.selection, text.trim | - | - |
| example.preserve | illustration | R1, R3 | mode.selection, text.preserve | - | - |
| example.unknown | illustration | R1, R4 | mode.selection, mode.unknown | - | - |

## Interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Rationale |
| --- | --- | --- | --- |
| interaction.mode-outcome | R1, R2, R3, R4 | mode.selection, text.trim, text.preserve, mode.unknown | composed-path |

## Examples first

Example example.trim: trim mode
Given input text with leading and trailing Unicode whitespace
When the normalizer is invoked in `trim` mode
Then the returned text has that leading and trailing Unicode whitespace removed.

Example example.preserve: preserve mode
Given any input text
When the normalizer is invoked in `preserve` mode
Then the returned text is unchanged.

Example example.unknown: unknown mode
Given a mode other than `trim` or `preserve`
When the normalizer is invoked
Then it fails with `unknown-mode` and returns no text.

## Requirements

R1. The normalizer MUST accept exactly the closed modes `trim` and `preserve`.

R2. In `trim` mode, the normalizer MUST remove leading and trailing Unicode whitespace from the input text.

R3. In `preserve` mode, the normalizer MUST return the input text unchanged.

R4. For every unknown mode, the normalizer MUST fail with `unknown-mode` and return no text.

## Inputs and outputs

The behavior consumes a mode and input text. Its observable result is the text required by R2 or R3, or the failure and absence of text required by R4.

## State and invariants

No persistent state is defined. The selected mode determines exactly one of the outcomes specified by R2, R3, and R4.

## Error and boundary behavior

Unknown-mode behavior is defined exclusively by R4.

## Compatibility and migration

Not applicable; no compatibility or migration behavior is specified.

## Observability

Not applicable; no logging, metrics, tracing, or audit requirements are specified.

## Security and privacy

Not applicable; no security or privacy behavior is specified.

## Accessibility and UX

Not applicable; no user interface is specified.

## Performance expectations

Not applicable; no performance behavior is specified.

## Edge cases

EC1. Input consisting entirely of Unicode whitespace in `trim` mode is governed by R2.

EC2. Input with no leading or trailing Unicode whitespace in `trim` mode is governed by R2.

EC3. Every mode outside the closed vocabulary in R1 is governed by R4.

## Non-goals

Input shape, transport, performance, storage, logging, and implementation behavior are outside this specification.

## Acceptance criteria

| Criterion | Governing requirement IDs | Observable acceptance condition |
| --- | --- | --- |
| Modes | R1 | Exactly `trim` and `preserve` are accepted modes. |
| Trim | R2 | Leading and trailing Unicode whitespace is removed in `trim` mode. |
| Preserve | R3 | Input text is returned unchanged in `preserve` mode. |
| Unknown | R4 | Every unknown mode produces `unknown-mode` and no text. |

## Open questions

None.

## Next artifacts

Spec review, followed by a traceable test specification after approval and the intervening required workflow stages.

## Follow-on artifacts

None yet

## Readiness

Ready for spec-review.
