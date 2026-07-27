# Portable text normalizer

## Status

draft

## Related proposal

Authoritative behavior request supplied with this spec.

## Goal and context

Define the observable behavior of a portable text normalizer with two accepted modes and a closed failure outcome for every unknown mode.

Boundary model version: v1
Boundary model scope: R1-R4

## Boundary model

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| canonical-trust | applicable | R2 | boundary.unicode-whitespace | - |
| identity-freshness | not-applicable | - | - | The requirements define no identity or freshness-dependent evidence. |
| closed-vocabulary | applicable | R1, R4 | boundary.mode-vocabulary | - |
| state-transition | not-applicable | - | - | The requirements define no persistent states or transitions. |
| authorization-scope | not-applicable | - | - | The requirements define no authorization decisions. |
| mutation-atomicity | not-applicable | - | - | The requirements define no mutation or commit operation. |
| interruption-recovery | not-applicable | - | - | The requirements define no prepared or interruptible work. |
| concurrency-idempotency | not-applicable | - | - | The requirements define no concurrent, duplicate, or replayed work. |
| composition-bypass | not-applicable | - | - | The requirements define no direct, helper, public, sibling, or retry paths. |
| compatibility-migration | not-applicable | - | - | The requirements define no old representation or migration behavior. |
| outcome-stop | applicable | R4 | boundary.unknown-mode-outcome | - |
| evidence-claims | not-applicable | - | - | The requirements define no evidence-based claims. |

Extensions:

| Extension ID | Title | Applicability | Rationale | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- | --- | --- |
| x.text.result | Text result transformation | applicable | The core dimensions do not represent the mode-specific relationship between input text and returned text. | R2, R3 | boundary.text-result | - |

## Examples

| Example ID | Role | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap |
| --- | --- | --- | --- | --- | --- |
| example.trim-whitespace | illustration | R1, R2 | boundary.mode-vocabulary, boundary.unicode-whitespace, boundary.text-result | - | - |
| example.preserve-text | illustration | R1, R3 | boundary.mode-vocabulary, boundary.text-result | - | - |
| example.unknown-mode | illustration | R1, R4 | boundary.mode-vocabulary, boundary.unknown-mode-outcome | - | - |

## Interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Rationale |
| --- | --- | --- | --- |
| interaction.mode-result | R1, R2, R3, R4 | boundary.mode-vocabulary, boundary.unicode-whitespace, boundary.text-result, boundary.unknown-mode-outcome | composed-path |

## Glossary

- Unicode whitespace: code points with the Unicode `White_Space` property.
- Unknown mode: every mode other than `trim` and `preserve`.

## Examples first

The classified examples in the boundary record illustrate trimming Unicode whitespace, preserving input text, and rejecting an unknown mode.

## Requirements

R1. The normalizer MUST accept exactly the closed modes `trim` and `preserve`.

R2. In `trim` mode, the normalizer MUST remove leading and trailing Unicode whitespace, where whitespace means code points with the Unicode `White_Space` property.

R3. In `preserve` mode, the normalizer MUST return the input text unchanged.

R4. For every unknown mode, the normalizer MUST fail with `unknown-mode` and return no text.

## Inputs and outputs

The behavioral inputs are text and a mode. The observable result is the text required by R2 or R3, or the failure and absence of text required by R4.

## State and invariants

The accepted mode vocabulary is exactly the set defined by R1. No persistent state is specified.

## Error and boundary behavior

R4 defines the complete specified error behavior. Unicode whitespace at the leading and trailing boundaries is governed by R2.

## Compatibility and migration

Not applicable; no compatibility or migration behavior is specified.

## Observability

The returned text or the `unknown-mode` failure with no text is the required observable outcome. No logging, metrics, tracing, or audit behavior is specified.

## Security and privacy

Not applicable; no security or privacy behavior is specified.

## Accessibility and UX

Not applicable; no user interface is specified.

## Performance expectations

Not applicable; no performance requirement is specified.

## Edge cases

EC1. In `trim` mode, leading or trailing code points with the Unicode `White_Space` property are removed as required by R2.

EC2. In `preserve` mode, the input text is returned unchanged as required by R3.

EC3. Every mode outside the closed vocabulary fails with `unknown-mode` and returns no text as required by R4.

## Non-goals

Input-shape, transport, performance, storage, logging, and implementation requirements are outside this spec.

## Acceptance criteria

| Acceptance criterion | Governing requirement IDs |
| --- | --- |
| Exactly `trim` and `preserve` are accepted modes. | R1 |
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

ready for spec-review
