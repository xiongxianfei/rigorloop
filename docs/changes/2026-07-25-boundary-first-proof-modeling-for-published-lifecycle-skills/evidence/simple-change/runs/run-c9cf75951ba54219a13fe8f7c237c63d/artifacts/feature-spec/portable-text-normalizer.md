<!-- Template: spec-skeleton-v1 -->
# Portable text normalizer

## Status

draft

## Related proposal

Authoritative behavior request supplied with this spec.

## Goal and context

Define portable, observable mode-dependent text normalization with a closed mode vocabulary and an explicit unknown-mode failure.

## Glossary

- Unicode whitespace: characters classified as whitespace by Unicode.
- No text: the failure result contains no returned text.

## Examples first

The classified examples in the boundary record illustrate each required outcome without extending the requirements.

Boundary model version: v1
Boundary model scope: R1-R4

## Boundary model

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| canonical-trust | not-applicable | - | - | No competing source of authority is defined. |
| identity-freshness | not-applicable | - | - | The requirements define no identity or freshness evidence. |
| closed-vocabulary | applicable | R1, R4 | boundary.mode-vocabulary | - |
| state-transition | not-applicable | - | - | The behavior defines no persistent states or transitions. |
| authorization-scope | not-applicable | - | - | The requirements define no authorization behavior. |
| mutation-atomicity | not-applicable | - | - | The behavior defines no mutation or commit point. |
| interruption-recovery | not-applicable | - | - | The requirements define no prepared or interrupted work. |
| concurrency-idempotency | not-applicable | - | - | The requirements define no concurrent or replayed work. |
| composition-bypass | not-applicable | - | - | No direct, helper, public, sibling, or retry paths are specified. |
| compatibility-migration | not-applicable | - | - | The requirements define no old representation or migration behavior. |
| outcome-stop | applicable | R4 | boundary.unknown-stop | - |
| evidence-claims | not-applicable | - | - | The requirements define no evidence-based claims. |

Extensions:

| Extension ID | Title | Applicability | Rationale | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- | --- | --- |
| x.text.transformation | Mode-selected text transformation | applicable | The core dimensions do not represent the required text transformation outcomes. | R2, R3 | boundary.text-transformation | - |

## Examples

| Example ID | Role | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap |
| --- | --- | --- | --- | --- | --- |
| example.trim-whitespace | illustration | R1, R2 | boundary.mode-vocabulary, boundary.text-transformation | - | - |
| example.preserve-text | illustration | R1, R3 | boundary.mode-vocabulary, boundary.text-transformation | - | - |
| example.unknown-mode | illustration | R4 | boundary.mode-vocabulary, boundary.unknown-stop | - | - |

## Interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Rationale |
| --- | --- | --- | --- |
| interaction.known-mode-outcome | R1, R2, R3 | boundary.mode-vocabulary, boundary.text-transformation | composed-path |
| interaction.unknown-mode-stop | R4 | boundary.mode-vocabulary, boundary.unknown-stop | state-coupling |

## Requirements

R1. The normalizer MUST accept exactly the closed modes `trim` and `preserve`.

R2. In `trim` mode, the normalizer MUST remove leading and trailing Unicode whitespace from the input text.

R3. In `preserve` mode, the normalizer MUST return the input text unchanged.

R4. For every unknown mode, the normalizer MUST fail with `unknown-mode` and return no text.

## Inputs and outputs

The behavioral input is text plus a mode governed by R1. The observable success output is governed by R2 or R3, and the failure output is governed by R4.

## State and invariants

No persistent state is specified. The mode vocabulary remains closed as required by R1.

## Error and boundary behavior

Unknown modes have the failure behavior specified by R4. Leading and trailing Unicode whitespace is governed by R2.

## Compatibility and migration

Not applicable; no compatibility or migration behavior is specified.

## Observability

The returned text, absence of returned text, and `unknown-mode` failure are the observable results defined by R2-R4. No logging or metrics behavior is specified.

## Security and privacy

Not applicable; no security or privacy behavior is specified.

## Accessibility and UX

Not applicable; no user interface is specified.

## Performance expectations

Not applicable; no performance contract is specified.

## Edge cases

EC1. Input consisting entirely of Unicode whitespace is governed by R2.

EC2. Empty input text is governed by R2 in `trim` mode and R3 in `preserve` mode.

EC3. Every mode other than `trim` and `preserve` is governed by R4.

## Non-goals

Input-shape, transport, performance, storage, logging, and implementation requirements are out of scope.

## Acceptance criteria

| Acceptance criterion | Requirement IDs |
| --- | --- |
| The accepted mode set is exactly `trim` and `preserve`. | R1 |
| `trim` removes leading and trailing Unicode whitespace. | R2 |
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
