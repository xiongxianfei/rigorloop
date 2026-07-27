<!-- Template: spec-skeleton-v1 -->
<!-- Skill: spec -->

# Portable text normalizer

## Status

draft

## Related proposal

Direct authoritative behavior request.

## Goal and context

Define the observable behavior of a portable text normalizer with two closed modes.

## Glossary

- Unicode whitespace: characters having the Unicode `White_Space` property.
- No text: the failure result contains no normalized text value.

Boundary model version: v1
Boundary model scope: R1-R4

## Boundary model

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| canonical-trust | not-applicable | - | - | The contract does not combine or resolve conflicting authoritative sources. |
| identity-freshness | not-applicable | - | - | The contract does not bind evidence to an identity or define freshness. |
| closed-vocabulary | applicable | R1, R4 | boundary.mode.selection | - |
| state-transition | not-applicable | - | - | The requested normalization behavior has no lifecycle states or transitions. |
| authorization-scope | not-applicable | - | - | The contract defines no authorization decisions. |
| mutation-atomicity | not-applicable | - | - | The contract defines no mutation or commit operation. |
| interruption-recovery | not-applicable | - | - | The contract defines no prepared or interrupted work. |
| concurrency-idempotency | not-applicable | - | - | The contract defines no concurrent, duplicate, or replayed operation. |
| composition-bypass | not-applicable | - | - | The contract identifies no distinct helper, public, sibling, or retry paths. |
| compatibility-migration | not-applicable | - | - | The request defines no old representation or migration behavior. |
| outcome-stop | applicable | R4 | boundary.unknown.stop | - |
| evidence-claims | not-applicable | - | - | The contract defines observable results but no evidence provenance or claim-inference rules. |

Extensions:

| Extension ID | Title | Applicability | Rationale | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- | --- | --- |
| x.text.output-semantics | Text output semantics | applicable | The core dimensions do not classify the mode-specific text transformation. | R2, R3 | boundary.text.output | - |

## Examples

| Example ID | Role | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap |
| --- | --- | --- | --- | --- | --- |
| example.trim.whitespace | illustration | R1, R2 | boundary.mode.selection, boundary.text.output | - | - |
| example.preserve.whitespace | illustration | R1, R3 | boundary.mode.selection, boundary.text.output | - | - |
| example.unknown.mode | illustration | R4 | boundary.mode.selection, boundary.unknown.stop | - | - |

## Interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Rationale |
| --- | --- | --- | --- |
| interaction.mode.output | R1, R2, R3 | boundary.mode.selection, boundary.text.output | state-coupling |
| interaction.unknown.stop | R4 | boundary.mode.selection, boundary.unknown.stop | state-coupling |

## Examples first

Example example.trim.whitespace: trim surrounding Unicode whitespace
Given input text with leading and trailing characters having the Unicode `White_Space` property
When normalization uses mode `trim`
Then the returned text excludes those leading and trailing characters.

Example example.preserve.whitespace: preserve text exactly
Given input text with leading and trailing Unicode whitespace
When normalization uses mode `preserve`
Then the returned text is unchanged.

Example example.unknown.mode: reject an unknown mode
Given any mode other than `trim` or `preserve`
When normalization is requested
Then the result is `unknown-mode` and contains no text.

## Requirements

R1. The normalizer MUST accept exactly the closed modes `trim` and `preserve`.

R2. In `trim` mode, the normalizer MUST remove leading and trailing Unicode whitespace from the input text.

R3. In `preserve` mode, the normalizer MUST return the input text unchanged.

R4. For every unknown mode, the normalizer MUST fail with `unknown-mode` and return no text.

## Inputs and outputs

The behavioral input is text plus a mode. Successful normalization returns text. An unknown mode produces the failure result specified by R4.

## State and invariants

No persistent state is part of this contract. The mode-specific outcomes are defined by R2 through R4.

## Error and boundary behavior

Unknown-mode behavior is defined exclusively by R4.

## Compatibility and migration

Not applicable; no compatibility or migration behavior is specified.

## Observability

The returned text or the `unknown-mode` failure with no text is the observable result. No logging, metrics, tracing, or audit behavior is specified.

## Security and privacy

Not applicable; no security, authorization, secret-handling, or privacy behavior is specified.

## Accessibility and UX

Not applicable; no user interface is specified.

## Performance expectations

Not applicable; no performance requirement is specified.

## Edge cases

edge.trim.empty: In `trim` mode, text with no characters outside the Unicode `White_Space` property yields the result implied by R2.

edge.preserve.empty: In `preserve` mode, empty input text remains unchanged under R3.

edge.mode.unknown: Every mode outside the closed vocabulary follows R4.

## Non-goals

Input-shape, transport, performance, storage, logging, and implementation behavior are outside this specification.

## Acceptance criteria

| Criterion ID | Requirement IDs | Criterion |
| --- | --- | --- |
| criterion.mode.closed | R1 | Only `trim` and `preserve` are accepted modes. |
| criterion.trim.output | R2 | Leading and trailing characters having the Unicode `White_Space` property are absent from the returned text in `trim` mode. |
| criterion.preserve.output | R3 | The returned text equals the input text in `preserve` mode. |
| criterion.unknown.failure | R4 | Every unknown mode produces `unknown-mode` with no returned text. |

## Open questions

None.

## Next artifacts

Spec review.

## Follow-on artifacts

None yet

## Readiness

Ready for spec-review.
