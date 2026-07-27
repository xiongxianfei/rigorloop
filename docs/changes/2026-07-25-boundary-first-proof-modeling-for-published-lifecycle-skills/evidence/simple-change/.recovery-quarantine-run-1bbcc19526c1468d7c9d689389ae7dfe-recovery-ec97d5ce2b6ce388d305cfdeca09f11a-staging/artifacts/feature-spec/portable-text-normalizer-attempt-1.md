# Portable text normalizer

## Status

draft

## Related proposal

Authoritative behavior request in this invocation.

## Goal and context

Define a portable text normalizer with two closed modes and explicit behavior for unknown modes.

## Glossary

- Unicode whitespace: characters classified as whitespace by Unicode.
- No text: the failure result contains no normalized text.

## Examples first

The classified examples are recorded in the contiguous boundary record below.

## Requirements

R1. The normalizer MUST accept exactly the closed modes `trim` and `preserve`.

R2. In `trim` mode, the normalizer MUST remove leading and trailing Unicode whitespace from the input text.

R3. In `preserve` mode, the normalizer MUST return the input text unchanged.

R4. For every unknown mode, the normalizer MUST fail with `unknown-mode` and return no text.

Boundary model version: v1
Boundary model scope: R1-R4

## Boundary model

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| canonical-trust | not-applicable | - | - | The contract has no competing authoritative sources. |
| identity-freshness | not-applicable | - | - | The contract has no identity or freshness evidence. |
| closed-vocabulary | applicable | R1, R4 | boundary.mode.vocabulary | - |
| state-transition | not-applicable | - | - | The requested behavior defines no persistent states or transitions. |
| authorization-scope | not-applicable | - | - | The requested behavior defines no authorization decisions. |
| mutation-atomicity | not-applicable | - | - | The requested behavior defines no externally observable mutation. |
| interruption-recovery | not-applicable | - | - | The requested behavior defines no prepared or interrupted work. |
| concurrency-idempotency | not-applicable | - | - | The requested behavior defines no concurrent or replayed work. |
| composition-bypass | not-applicable | - | - | The requested behavior defines no direct, helper, public, sibling, or retry paths. |
| compatibility-migration | not-applicable | - | - | The requested behavior defines no prior representation or migration. |
| outcome-stop | applicable | R4 | boundary.unknown.outcome | - |
| evidence-claims | not-applicable | - | - | The requested behavior defines no evidence-backed claims. |

Extensions:

| Extension ID | Title | Applicability | Rationale | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- | --- | --- |
| x.text.normalization | Mode-selected text transformation | applicable | The core dimensions do not represent the requested trim and preserve transformations. | R2, R3 | boundary.text.transformation | - |

## Examples

| Example ID | Role | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap |
| --- | --- | --- | --- | --- | --- |
| example.trim.whitespace | illustration | R1, R2 | boundary.mode.vocabulary, boundary.text.transformation | - | - |
| example.preserve.unchanged | illustration | R1, R3 | boundary.mode.vocabulary, boundary.text.transformation | - | - |
| example.unknown.failure | illustration | R4 | boundary.mode.vocabulary, boundary.unknown.outcome | - | - |

## Interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Rationale |
| --- | --- | --- | --- |
| interaction.mode.transformation | R1, R2, R3 | boundary.mode.vocabulary, boundary.text.transformation | composed-path |
| interaction.mode.failure | R4 | boundary.mode.vocabulary, boundary.unknown.outcome | state-coupling |

## Inputs and outputs

The input is text together with a mode. Successful normalization returns text. Unknown-mode failure returns `unknown-mode` and no text.

## State and invariants

The accepted mode vocabulary is closed to `trim` and `preserve`.

## Error and boundary behavior

Unknown modes produce the failure behavior in R4. Leading and trailing Unicode whitespace is governed by R2.

## Compatibility and migration

Not applicable; no prior representation or migration behavior is specified.

## Observability

The observable results are the returned text or the `unknown-mode` failure with no text.

## Security and privacy

Not applicable; no security or privacy behavior is specified.

## Accessibility and UX

Not applicable; no user interface is specified.

## Performance expectations

Not applicable; no performance contract is specified.

## Edge cases

- In `trim` mode, text with Unicode whitespace only is governed by R2.
- In `preserve` mode, text containing leading or trailing Unicode whitespace is governed by R3.
- Any mode other than `trim` or `preserve` is governed by R4.

## Non-goals

Input shape, transport, performance, storage, logging, and implementation behavior are outside this specification.

## Acceptance criteria

| Requirement | Acceptance criterion |
| --- | --- |
| R1 | Tests demonstrate that `trim` and `preserve` are accepted and every other mode is unknown. |
| R2 | Tests demonstrate removal of leading and trailing Unicode whitespace in `trim` mode. |
| R3 | Tests demonstrate byte-for-byte unchanged returned text in `preserve` mode. |
| R4 | Tests demonstrate `unknown-mode` and absence of returned text for every unknown mode tested. |

## Open questions

None.

## Next artifacts

Spec review, followed by a traceable test specification after approval.

## Follow-on artifacts

None yet

## Readiness

Ready for spec-review.
