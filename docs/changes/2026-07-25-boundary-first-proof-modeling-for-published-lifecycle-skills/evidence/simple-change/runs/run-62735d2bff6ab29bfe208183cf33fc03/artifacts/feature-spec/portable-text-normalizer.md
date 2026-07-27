<!-- Template: spec-skeleton-v1 -->
<!-- Skill: spec -->

# Portable text normalizer

## Status

draft

## Related proposal

Authoritative behavior request supplied with this spec.

## Goal and context

Define the observable mode-dependent behavior of a portable text normalizer.

## Glossary

- Unicode whitespace: code points with the Unicode `White_Space` property.
- No text: the operation produces no text result.

## Examples first

See the classified examples in the contiguous boundary record below.

Boundary model version: v1
Boundary model scope: R1-R4

## Boundary model

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| canonical-trust | applicable | R2 | whitespace.authority | - |
| identity-freshness | not-applicable | - | - | The requirements define no identity or freshness-dependent evidence. |
| closed-vocabulary | applicable | R1, R4 | mode.vocabulary | - |
| state-transition | not-applicable | - | - | The requirements define no persistent states or transitions. |
| authorization-scope | not-applicable | - | - | The requirements define no authorization decisions. |
| mutation-atomicity | not-applicable | - | - | The requirements define no mutation or commit point. |
| interruption-recovery | not-applicable | - | - | The requirements define no prepared or interrupted work. |
| concurrency-idempotency | not-applicable | - | - | The requirements define no concurrency, replay, or duplicate-work behavior. |
| composition-bypass | not-applicable | - | - | The requirements define no direct, helper, public, sibling, or retry paths. |
| compatibility-migration | not-applicable | - | - | The requirements define no old representation or migration behavior. |
| outcome-stop | applicable | R4 | unknown.outcome | - |
| evidence-claims | not-applicable | - | - | The requirements define no evidence-backed claims. |

Extensions:

| Extension ID | Title | Applicability | Rationale | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- | --- | --- |
| x.text.output-semantics | Mode-specific text output | applicable | The core dimensions do not represent the required text transformation and preservation outcomes. | R2, R3 | text.output | - |

## Examples

| Example ID | Role | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap |
| --- | --- | --- | --- | --- | --- |
| example.trim.whitespace | illustration | R1, R2 | mode.vocabulary, whitespace.authority, text.output | - | - |
| example.preserve.unchanged | illustration | R1, R3 | mode.vocabulary, text.output | - | - |
| example.unknown.failure | illustration | R1, R4 | mode.vocabulary, unknown.outcome | - | - |

## Interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Rationale |
| --- | --- | --- | --- |
| interaction.trim.result | R1, R2 | mode.vocabulary, whitespace.authority, text.output | composed-path |
| interaction.preserve.result | R1, R3 | mode.vocabulary, text.output | composed-path |
| interaction.unknown.result | R1, R4 | mode.vocabulary, unknown.outcome | state-coupling |

## Requirements

R1. The normalizer MUST accept exactly the closed modes `trim` and `preserve`.

R2. In `trim` mode, the normalizer MUST remove leading and trailing Unicode whitespace, where whitespace means code points with the Unicode `White_Space` property.

R3. In `preserve` mode, the normalizer MUST return the input text unchanged.

R4. For every unknown mode, the normalizer MUST fail with `unknown-mode` and return no text.

## Inputs and outputs

The behavior contract is limited to the input text, the mode named in R1, the text outcomes in R2 and R3, and the failure outcome in R4.

## State and invariants

No stateful behavior is specified.

## Error and boundary behavior

R4 defines the complete specified failure behavior. R1 and R2 define the closed mode and whitespace boundaries.

## Compatibility and migration

Not applicable; no compatibility or migration behavior is specified.

## Observability

Observable results are limited to the text outcomes in R2 and R3 and the failure outcome in R4.

## Security and privacy

Not applicable; no security or privacy behavior is specified.

## Accessibility and UX

Not applicable; no UI behavior is specified.

## Performance expectations

Not applicable; no performance behavior is specified.

## Edge cases

EC1. A `trim` input with Unicode `White_Space` code points at either boundary is governed by R2.

EC2. A `preserve` input containing boundary whitespace is governed by R3.

EC3. Any mode other than `trim` or `preserve` is governed by R4.

## Non-goals

Input-shape, transport, performance, storage, logging, and implementation requirements are out of scope.

## Acceptance criteria

| Criterion | Requirement IDs |
| --- | --- |
| The closed mode vocabulary is testable. | R1 |
| Unicode boundary-whitespace removal in `trim` is testable. | R2 |
| Unchanged output in `preserve` is testable. | R3 |
| Unknown-mode failure with no text is testable. | R4 |

## Open questions

None.

## Next artifacts

Spec review of this contract.

## Follow-on artifacts

None yet

## Readiness

ready for spec-review
