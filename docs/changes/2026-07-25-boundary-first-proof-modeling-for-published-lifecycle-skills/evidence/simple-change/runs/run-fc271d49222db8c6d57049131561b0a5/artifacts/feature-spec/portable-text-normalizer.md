<!-- Template: spec-skeleton-v1 -->
<!-- Skill: spec -->
<!-- Template status: normative -->

# Portable text normalizer

## Status

draft

## Related proposal

Authoritative behavior request supplied with this specification.

## Goal and context

Define the observable mode-dependent behavior of a portable text normalizer without prescribing implementation details.

## Glossary

- Unicode whitespace: code points with the Unicode `White_Space` property.
- No text: the failure result contains no normalized text.

## Examples first

Example ex.trim.surrounding: surrounding Unicode whitespace
Given text with leading and trailing code points having the Unicode `White_Space` property
When the mode is `trim`
Then those leading and trailing code points are removed

Example ex.preserve.unchanged: preserved text
Given any input text
When the mode is `preserve`
Then the input text is returned unchanged

Example ex.unknown.failure: unknown mode
Given a mode other than `trim` or `preserve`
When normalization is requested
Then the result is `unknown-mode` with no text

Boundary model version: v1
Boundary model scope: R1-R4

## Boundary model

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| canonical-trust | not-applicable | - | - | No conflicting authoritative sources are defined. |
| identity-freshness | not-applicable | - | - | The behavior does not bind evidence to an identity or define staleness. |
| closed-vocabulary | applicable | R1, R4 | boundary.mode.vocabulary | - |
| state-transition | not-applicable | - | - | The behavior defines no persistent states or transitions. |
| authorization-scope | not-applicable | - | - | The behavior defines no authorization decision. |
| mutation-atomicity | not-applicable | - | - | The behavior defines no externally observable mutation or commit point. |
| interruption-recovery | not-applicable | - | - | The behavior defines no prepared or interrupted work. |
| concurrency-idempotency | not-applicable | - | - | The behavior defines no concurrent, duplicate, or replayed work. |
| composition-bypass | not-applicable | - | - | No direct, helper, public, sibling, or retry path distinctions are defined. |
| compatibility-migration | not-applicable | - | - | No old representation, migration, rollout, or retirement behavior is defined. |
| outcome-stop | applicable | R4 | boundary.unknown.outcome | - |
| evidence-claims | not-applicable | - | - | The behavior defines no evidence-backed claim. |

Extensions:

| Extension ID | Title | Applicability | Rationale | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- | --- | --- |
| x.text.trim | Trim transformation | applicable | Defines the required transformation for the `trim` mode. | R2 | boundary.trim.whitespace | - |
| x.text.preserve | Preserve transformation | applicable | Defines the required transformation for the `preserve` mode. | R3 | boundary.preserve.unchanged | - |

## Examples

| Example ID | Role | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap |
| --- | --- | --- | --- | --- | --- |
| example.trim.surrounding | illustration | R2 | boundary.trim.whitespace | - | - |
| example.preserve.unchanged | illustration | R3 | boundary.preserve.unchanged | - | - |
| example.unknown.failure | illustration | R4 | boundary.mode.vocabulary, boundary.unknown.outcome | - | - |

## Interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Rationale |
| --- | --- | --- | --- |
| interaction.mode.outcome | R1, R4 | boundary.mode.vocabulary, boundary.unknown.outcome | composed-path |

## Requirements

R1. The normalizer MUST accept exactly the closed modes `trim` and `preserve`.

R2. In `trim` mode, the normalizer MUST remove leading and trailing Unicode whitespace, where whitespace means code points with the Unicode `White_Space` property.

R3. In `preserve` mode, the normalizer MUST return the input text unchanged.

R4. For every unknown mode, the normalizer MUST fail with `unknown-mode` and return no text.

## Inputs and outputs

The behavioral inputs are text and a mode. The observable output is normalized text under R2 or R3, or the failure outcome under R4.

## State and invariants

No persistent state is specified. The mode vocabulary is fixed by R1.

## Error and boundary behavior

Unknown-mode behavior is specified by R4. Unicode whitespace boundaries are specified by R2.

## Compatibility and migration

Not applicable; no compatibility or migration behavior is specified.

## Observability

The returned text or `unknown-mode` failure is the only specified observation.

## Security and privacy

Not applicable; no security or privacy behavior is specified.

## Accessibility and UX

Not applicable; no user interface is specified.

## Performance expectations

Not applicable; no performance contract is specified.

## Edge cases

EC1. Input containing no leading or trailing Unicode whitespace is governed by R2.

EC2. Input consisting entirely of Unicode whitespace is governed by R2.

EC3. Empty input text in `preserve` mode is governed by R3.

EC4. Any mode outside the closed vocabulary is governed by R4.

## Non-goals

Input shape, transport, performance, storage, logging, implementation details, and behavior beyond R1-R4 are out of scope.

## Acceptance criteria

| Criterion | Requirement IDs |
| --- | --- |
| Both closed modes are accepted, and modes outside the closed vocabulary produce the specified failure with no text. | R1, R4 |
| Leading and trailing Unicode `White_Space` code points are removed in `trim` mode. | R2 |
| Input text is returned unchanged in `preserve` mode. | R3 |

## Open questions

None.

## Next artifacts

Spec review.

## Follow-on artifacts

None yet

## Readiness

ready for spec-review
