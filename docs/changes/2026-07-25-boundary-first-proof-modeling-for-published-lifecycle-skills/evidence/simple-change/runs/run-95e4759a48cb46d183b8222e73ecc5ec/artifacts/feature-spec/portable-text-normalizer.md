# Portable Text Normalizer

## Status

draft

## Related proposal

None.

## Goal and context

Define the observable mode-dependent behavior of a portable text normalizer.

## Glossary

- Unicode whitespace: characters classified as whitespace by Unicode.
- Unknown mode: any mode other than `trim` or `preserve`.

Boundary model version: v1
Boundary model scope: R1-R4

## Boundary model

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| canonical-trust | not-applicable | - | - | The contract has no competing sources of authority. |
| identity-freshness | not-applicable | - | - | The behavior uses no identity-bound or freshness-sensitive evidence. |
| closed-vocabulary | applicable | R1, R4 | mode.vocabulary | - |
| state-transition | not-applicable | - | - | The contract defines no persistent states or transitions. |
| authorization-scope | not-applicable | - | - | The contract defines no authorization decisions. |
| mutation-atomicity | not-applicable | - | - | The contract defines no stored mutation or commit point. |
| interruption-recovery | not-applicable | - | - | The contract defines no prepared or interruptible work. |
| concurrency-idempotency | not-applicable | - | - | The contract defines no concurrent, duplicate, or replayed operation. |
| composition-bypass | not-applicable | - | - | The contract defines no distinct helper, public, sibling, or retry paths. |
| compatibility-migration | not-applicable | - | - | The contract defines no old representation or migration behavior. |
| outcome-stop | applicable | R2, R3, R4 | normalization.outcome | - |
| evidence-claims | not-applicable | - | - | The contract defines no evidence-based claims. |

Extensions: none.

## Examples

| Example ID | Role | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap |
| --- | --- | --- | --- | --- | --- |
| example.trim-whitespace | illustration | R1, R2 | mode.vocabulary, normalization.outcome | - | - |
| example.preserve-whitespace | illustration | R1, R3 | mode.vocabulary, normalization.outcome | - | - |
| example.unknown-mode | illustration | R4 | mode.vocabulary, normalization.outcome | - | - |

## Interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Rationale |
| --- | --- | --- | --- |
| interaction.mode-outcome | R1, R2, R3, R4 | mode.vocabulary, normalization.outcome | state-coupling |

### Example details

Example `example.trim-whitespace`: Given text `  hello   ` and mode `trim`, the returned text is `hello`.

Example `example.preserve-whitespace`: Given text `  hello   ` and mode `preserve`, the returned text is `  hello   ` unchanged.

Example `example.unknown-mode`: Given any text and mode `collapse`, the result is `unknown-mode` with no returned text.

## Requirements

R1. The normalizer MUST accept exactly the closed modes `trim` and `preserve`.

R2. In `trim` mode, the normalizer MUST remove leading and trailing Unicode whitespace from the input text.

R3. In `preserve` mode, the normalizer MUST return the input text unchanged.

R4. For every unknown mode, the normalizer MUST fail with `unknown-mode` and return no text.

## Inputs and outputs

The contract concerns input text, a mode, returned text, and the `unknown-mode` failure identified by R1-R4.

## State and invariants

Not applicable; no persistent state is defined.

## Error and boundary behavior

Defined by R4 and the boundary record.

## Compatibility and migration

Not applicable.

## Observability

Observable results are the returned text or the R4 failure with no text.

## Security and privacy

Not applicable.

## Accessibility and UX

Not applicable.

## Performance expectations

Not applicable.

## Edge cases

Leading and trailing Unicode whitespace is covered by R2. Unknown modes are covered by R4. No additional behavior is specified.

## Non-goals

Input shape, transport, performance, storage, logging, and implementation behavior are outside this specification.

## Acceptance criteria

R1-R4 are each demonstrated by direct tests, including the three illustrated examples and unknown-mode coverage.

## Open questions

None.

## Next artifacts

A spec review may assess this draft.

## Follow-on artifacts

None yet.

## Readiness

Ready for `spec-review`; no later lifecycle stage is claimed.
