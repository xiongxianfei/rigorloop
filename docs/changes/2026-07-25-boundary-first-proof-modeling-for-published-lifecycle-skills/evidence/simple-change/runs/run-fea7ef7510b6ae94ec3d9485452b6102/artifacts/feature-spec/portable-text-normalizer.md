<!-- Template: spec-skeleton-v1 -->
<!-- Skill: spec -->

# Portable text normalizer

## Status

draft

## Related proposal

Direct authoritative behavior request.

## Goal and context

Define the observable behavior of a portable text normalizer in two closed modes.

## Glossary

- `White_Space`: the Unicode property named `White_Space`.
- `unknown-mode`: the required failure for a mode other than `trim` or `preserve`.

## Examples first

The classified examples are recorded in the contiguous boundary record below.

## Requirements

R1. The normalizer MUST accept exactly the closed modes `trim` and `preserve`.

R2. In `trim` mode, the normalizer MUST remove leading and trailing Unicode whitespace, where whitespace means code points with the Unicode `White_Space` property.

R3. In `preserve` mode, the normalizer MUST return the input text unchanged.

R4. For every unknown mode, the normalizer MUST fail with `unknown-mode` and return no text.

Boundary model version: v1
Boundary model scope: R1-R4

## Boundary model

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| canonical-trust | applicable | R2 | b.unicode.white-space | - |
| identity-freshness | not-applicable | - | - | The requirements define no identity or freshness-sensitive evidence. |
| closed-vocabulary | applicable | R1, R4 | b.mode.vocabulary | - |
| state-transition | not-applicable | - | - | The requirements define no persistent states or transitions. |
| authorization-scope | not-applicable | - | - | The requirements define no actor or authorization decision. |
| mutation-atomicity | not-applicable | - | - | The requirements define no mutation or commit point. |
| interruption-recovery | not-applicable | - | - | The requirements define no prepared or interruptible work. |
| concurrency-idempotency | not-applicable | - | - | The requirements define no concurrent, duplicate, or replayed work. |
| composition-bypass | not-applicable | - | - | The requirements define no direct, helper, public, sibling, or retry paths. |
| compatibility-migration | not-applicable | - | - | The requirements define no old representation or migration behavior. |
| outcome-stop | applicable | R3, R4 | b.result.outcome | - |
| evidence-claims | not-applicable | - | - | The requirements define no evidence or claim contract. |

Extensions:

| Extension ID | Title | Applicability | Rationale | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- | --- | --- |
| x.text.transformation | Text transformation | applicable | The core dimensions do not represent the requested trim and preserve transformations. | R2, R3 | b.text.transformation | - |

## Examples

| Example ID | Role | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap |
| --- | --- | --- | --- | --- | --- |
| ex.mode.known | illustration | R1 | b.mode.vocabulary | - | - |
| ex.trim.white-space | illustration | R2 | b.unicode.white-space, b.text.transformation | - | - |
| ex.preserve.unchanged | illustration | R3 | b.result.outcome, b.text.transformation | - | - |
| ex.mode.unknown | illustration | R1, R4 | b.mode.vocabulary, b.result.outcome | - | - |

## Interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Rationale |
| --- | --- | --- | --- |
| i.trim.classification | R2 | b.unicode.white-space, b.text.transformation | composed-path |
| i.mode.outcome | R1, R3, R4 | b.mode.vocabulary, b.result.outcome | state-coupling |

## Inputs and outputs

The contract concerns input text, a mode, returned text, and the `unknown-mode` failure as governed by R1-R4.

## State and invariants

No persistent state is specified. R1-R4 are the complete behavioral contract.

## Error and boundary behavior

R4 defines the error and no-text boundary for every unknown mode.

## Compatibility and migration

Not applicable; no compatibility or migration behavior is specified.

## Observability

Limited to the returned text or the failure and absence of text required by R2-R4.

## Security and privacy

Not applicable; no security or privacy behavior is specified.

## Accessibility and UX

Not applicable; no user interface is specified.

## Performance expectations

Not applicable; no performance behavior is specified.

## Edge cases

- ec.trim.all-white-space: Governed by R2.
- ec.trim.no-edge-white-space: Governed by R2.
- ec.preserve.white-space: Governed by R3.
- ec.mode.unknown: Governed by R4.

## Non-goals

Input shape, transport, storage, logging, implementation, performance, compatibility, security, privacy, accessibility, and user-interface requirements are outside this specification.

## Acceptance criteria

| Acceptance criterion ID | Requirement IDs | Criterion |
| --- | --- | --- |
| ac.mode.closed | R1 | R1 is demonstrated for both accepted modes and an unknown mode. |
| ac.trim.unicode | R2 | R2 is demonstrated with leading and trailing code points having the Unicode `White_Space` property. |
| ac.preserve.unchanged | R3 | R3 is demonstrated with input text returned unchanged. |
| ac.mode.unknown | R4 | R4 is demonstrated with an unknown mode producing `unknown-mode` and no text. |

## Open questions

None.

## Next artifacts

A spec review may assess R1-R4 and the boundary record.

## Follow-on artifacts

None yet

## Readiness

ready for spec-review
