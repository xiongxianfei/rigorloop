# Portable Text Normalizer

## Status

draft

## Related proposal

Direct behavior request; no separate proposal.

## Goal and context

Define portable text normalization for two closed modes and the failure outcome for every unknown mode.

## Glossary

- `trim`: Mode that removes leading and trailing Unicode whitespace.
- `preserve`: Mode that leaves the input text unchanged.
- `unknown-mode`: Failure returned for any mode other than `trim` or `preserve`.

Boundary model version: v1
Boundary model scope: R1-R4

## Boundary model

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| canonical-trust | not-applicable | - | - | No conflicting authority sources are part of this contract. |
| identity-freshness | not-applicable | - | - | Evidence identity and staleness are outside this contract. |
| closed-vocabulary | applicable | R1, R4 | mode.closed-vocabulary | - |
| state-transition | not-applicable | - | - | The requested behavior defines no persistent states or transitions. |
| authorization-scope | not-applicable | - | - | The requested behavior defines no authorization decisions. |
| mutation-atomicity | not-applicable | - | - | The requested behavior defines no mutation or commit point. |
| interruption-recovery | not-applicable | - | - | The requested behavior defines no prepared or interruptible work. |
| concurrency-idempotency | not-applicable | - | - | The requested behavior defines no concurrency, replay, or duplicate-work semantics. |
| composition-bypass | not-applicable | - | - | The requested behavior defines no distinct helper, public, sibling, or retry paths. |
| compatibility-migration | not-applicable | - | - | The requested behavior defines no legacy representation or migration. |
| outcome-stop | applicable | R2, R3, R4 | normalization.outcome | - |
| evidence-claims | not-applicable | - | - | Runtime evidence and claim provenance are outside this contract. |

Extensions: none

## Examples

| Example ID | Role | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap |
| --- | --- | --- | --- | --- | --- |
| example.trim | illustration | R1, R2 | mode.closed-vocabulary, normalization.outcome | - | - |
| example.preserve | illustration | R1, R3 | mode.closed-vocabulary, normalization.outcome | - | - |
| example.unknown | illustration | R4 | mode.closed-vocabulary, normalization.outcome | - | - |

Example `example.trim`: Given text with leading and trailing Unicode whitespace and mode `trim`, the result contains the text without that surrounding whitespace.

Example `example.preserve`: Given any text and mode `preserve`, the result is the unchanged input text.

Example `example.unknown`: Given any mode other than `trim` or `preserve`, the result is failure `unknown-mode` with no text.

## Interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Rationale |
| --- | --- | --- | --- |
| interaction.mode-outcome | R1, R2, R3, R4 | mode.closed-vocabulary, normalization.outcome | composed-path |

## Requirements

R1. The normalizer MUST accept exactly the closed modes `trim` and `preserve`.

R2. In `trim` mode, the normalizer MUST remove leading and trailing Unicode whitespace from the input text.

R3. In `preserve` mode, the normalizer MUST return the input text unchanged.

R4. For every unknown mode, the normalizer MUST fail with `unknown-mode` and return no text.

## Inputs and outputs

The behavioral inputs are text and a mode. Successful normalization returns text. An unknown mode returns failure `unknown-mode` and no text.

## State and invariants

The behavior is stateless. The selected accepted mode determines the successful text outcome.

## Error and boundary behavior

The closed mode boundary and its unknown-mode outcome are defined by R1 and R4. Unicode whitespace at the beginning or end of text is governed by R2.

## Compatibility and migration

Not applicable; no prior representation or migration behavior is specified.

## Observability

The observable surfaces are returned text, failure `unknown-mode`, and absence of returned text on failure.

## Security and privacy

Not applicable; no additional security or privacy behavior is specified.

## Accessibility and UX

Not applicable; no user interface is specified.

## Performance expectations

Not applicable; no performance requirement is specified.

## Edge cases

- `trim` with Unicode whitespace only is covered by R2.
- `trim` with no leading or trailing Unicode whitespace is covered by R2.
- `preserve` with Unicode whitespace is covered by R3.
- Every value outside the two accepted modes is covered by R4.

## Non-goals

Input shape, transport, performance, storage, logging, implementation design, and behavior beyond R1-R4 are outside this specification.

## Acceptance criteria

- R1 is demonstrated with both accepted modes and values outside the closed vocabulary.
- R2 is demonstrated with leading whitespace, trailing whitespace, both, neither, and Unicode whitespace-only text.
- R3 is demonstrated by exact equality between input and returned text.
- R4 is demonstrated with unknown modes, the exact failure `unknown-mode`, and absence of returned text.
- `interaction.mode-outcome` is demonstrated for `trim`, `preserve`, and unknown-mode outcomes.

## Open questions

None.

## Next artifacts

Spec review.

## Follow-on artifacts

None yet.

## Readiness

Ready for spec review. No later lifecycle stage is claimed.
