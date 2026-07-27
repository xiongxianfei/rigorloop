<!-- Template: spec-skeleton-v1 -->
# Portable text normalizer

Boundary model version: v1
Boundary model scope: R1-R4

## Boundary model

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| canonical-trust | not-applicable | - | - | No competing authoritative sources are defined. |
| identity-freshness | not-applicable | - | - | The behavior does not bind evidence to an identity or freshness period. |
| closed-vocabulary | applicable | R1, R4 | boundary.mode.selection | - |
| state-transition | not-applicable | - | - | The behavior defines no persistent states or transitions. |
| authorization-scope | not-applicable | - | - | The behavior defines no authorization decisions. |
| mutation-atomicity | not-applicable | - | - | The behavior defines no stored mutation or commit point. |
| interruption-recovery | not-applicable | - | - | The behavior defines no prepared or resumable work. |
| concurrency-idempotency | not-applicable | - | - | The behavior defines no concurrent or replayable mutation. |
| composition-bypass | not-applicable | - | - | The contract defines no distinct helper, public, sibling, or retry paths. |
| compatibility-migration | not-applicable | - | - | No prior representation or migration behavior is specified. |
| outcome-stop | applicable | R4 | boundary.unknown.outcome | - |
| evidence-claims | not-applicable | - | - | The behavior makes no evidence-based claims. |

Extensions:

| Extension ID | Title | Applicability | Rationale | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- | --- | --- |
| x.text.transformation | Mode-selected text transformation | applicable | The core dimensions do not represent the text transformation selected by a recognized mode. | R2, R3 | boundary.text.transformation | - |

## Examples

| Example ID | Role | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap |
| --- | --- | --- | --- | --- | --- |
| example.trim.whitespace | illustration | R1, R2 | boundary.mode.selection, boundary.text.transformation | - | - |
| example.preserve.unchanged | illustration | R1, R3 | boundary.mode.selection, boundary.text.transformation | - | - |
| example.unknown.rejected | illustration | R4 | boundary.mode.selection, boundary.unknown.outcome | - | - |

## Interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Rationale |
| --- | --- | --- | --- |
| interaction.mode.result | R1, R2, R3, R4 | boundary.mode.selection, boundary.text.transformation, boundary.unknown.outcome | composed-path |

## Status

draft

## Related proposal

Authoritative behavior request supplied with this spec.

## Goal and context

Define the observable behavior of a portable text normalizer with two recognized modes and a closed failure outcome for every other mode.

## Glossary

- Unicode whitespace: characters classified as whitespace by Unicode.
- Input text: the text supplied to the normalizer.
- Mode: the value selecting normalization behavior.

## Examples first

Example example.trim.whitespace: trim surrounding Unicode whitespace
Given input text with leading and trailing Unicode whitespace
When the mode is `trim`
Then the returned text excludes that leading and trailing whitespace.

Example example.preserve.unchanged: preserve text exactly
Given any input text
When the mode is `preserve`
Then the returned text is unchanged.

Example example.unknown.rejected: reject an unknown mode
Given a mode other than `trim` or `preserve`
When normalization is requested
Then the result is `unknown-mode` and contains no text.

## Requirements

R1. The normalizer MUST accept exactly the closed modes `trim` and `preserve`.

R2. In `trim` mode, the normalizer MUST remove leading and trailing Unicode whitespace from the input text.

R3. In `preserve` mode, the normalizer MUST return the input text unchanged.

R4. For every unknown mode, the normalizer MUST fail with `unknown-mode` and return no text.

## Inputs and outputs

The contract concerns an input mode, input text, and the result defined by R1-R4.

## State and invariants

No persistent state is part of this contract.

## Error and boundary behavior

Unknown-mode behavior is defined by R4. No additional error behavior is specified.

## Compatibility and migration

Not applicable; no prior representation or migration behavior is specified.

## Observability

The returned text or the `unknown-mode` failure with no text is the observable result. No logging, metrics, tracing, or audit behavior is specified.

## Security and privacy

Not applicable; no security, authorization, secret-handling, or data-exposure behavior is specified.

## Accessibility and UX

Not applicable; no user interface is specified.

## Performance expectations

Not applicable; no performance contract is specified.

## Edge cases

EC1. In `trim` mode, input containing Unicode whitespace only returns text with that leading and trailing whitespace removed, as required by R2.

EC2. In `preserve` mode, leading and trailing Unicode whitespace remains unchanged, as required by R3.

EC3. Any mode outside the closed set, including an otherwise similar value, produces the R4 outcome.

## Non-goals

Input-shape, transport, performance, storage, logging, and implementation behavior are outside this specification.

## Acceptance criteria

| Acceptance criterion | Requirement IDs |
| --- | --- |
| Tests demonstrate that only `trim` and `preserve` are accepted modes. | R1 |
| Tests demonstrate removal of leading and trailing Unicode whitespace in `trim` mode. | R2 |
| Tests demonstrate unchanged text in `preserve` mode. | R3 |
| Tests demonstrate `unknown-mode` with no returned text for every tested unknown mode partition. | R4 |

## Open questions

None.

## Next artifacts

Spec review, followed by a traceable test specification after the required intervening lifecycle stages.

## Follow-on artifacts

None yet

## Readiness

Ready for spec-review.
