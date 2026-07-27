# Portable text normalizer

## Status

draft

## Related proposal

None.

## Goal and context

Define the observable mode-dependent behavior of a portable text normalizer.

## Glossary

Unicode whitespace: code points with the Unicode `White_Space` property.

Boundary model version: v1
Boundary model scope: R1-R4

## Boundary model

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| canonical-trust | not-applicable | - | - | No competing authoritative sources are defined. |
| identity-freshness | not-applicable | - | - | The behavior does not use identity-bound or freshness-sensitive evidence. |
| closed-vocabulary | applicable | R1 | boundary.mode.closed | - |
| state-transition | not-applicable | - | - | No persistent states or transitions are defined. |
| authorization-scope | not-applicable | - | - | No authorization decisions are defined. |
| mutation-atomicity | not-applicable | - | - | No stored mutation or commit point is defined. |
| interruption-recovery | not-applicable | - | - | No prepared or interruptible work is defined. |
| concurrency-idempotency | not-applicable | - | - | No concurrent, replayed, or duplicate work is defined. |
| composition-bypass | not-applicable | - | - | No helper, public, sibling, or retry paths are defined. |
| compatibility-migration | not-applicable | - | - | No earlier representation or migration is defined. |
| outcome-stop | applicable | R4 | boundary.mode.unknown-outcome | - |
| evidence-claims | not-applicable | - | - | No evidence-derived claims are defined. |

Extensions:

| Extension ID | Title | Applicability | Rationale | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- | --- | --- |
| x.text.trim | Trim normalization | applicable | Defines the feature-specific transformation for trim mode. | R2 | boundary.text.trim | - |
| x.text.preserve | Preserve normalization | applicable | Defines the feature-specific transformation for preserve mode. | R3 | boundary.text.preserve | - |

## Examples

| Example ID | Role | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap |
| --- | --- | --- | --- | --- | --- |
| example.mode.closed | illustration | R1 | boundary.mode.closed | - | - |
| example.trim.whitespace | illustration | R2 | boundary.text.trim | - | - |
| example.preserve.unchanged | illustration | R3 | boundary.text.preserve | - | - |
| example.mode.unknown | illustration | R4 | boundary.mode.unknown-outcome | - | - |

## Interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Rationale |
| --- | --- | --- | --- |
| interaction.mode.outcome | R1, R4 | boundary.mode.closed, boundary.mode.unknown-outcome | composed-path |

## Requirements

R1. The normalizer MUST accept exactly the closed modes `trim` and `preserve`.

R2. In `trim` mode, the normalizer MUST remove leading and trailing Unicode whitespace from the input text, where whitespace means code points with the Unicode `White_Space` property.

R3. In `preserve` mode, the normalizer MUST return the input text unchanged.

R4. For every unknown mode, the normalizer MUST fail with `unknown-mode` and return no text.

## Inputs and outputs

The behavior consumes input text and a mode.
Its observable result is the text required by R2 or R3, or the failure required by R4.

## State and invariants

No state is defined.

## Error and boundary behavior

Unknown modes have the failure behavior defined by R4.

## Compatibility and migration

Not applicable; no earlier contract or data representation is specified.

## Observability

The returned text or `unknown-mode` failure is the observable result.
No logging, metrics, traces, or audit requirements are specified.

## Security and privacy

Not applicable; no security or privacy behavior is specified.

## Accessibility and UX

Not applicable; no user interface is specified.

## Performance expectations

Not applicable; no performance contract is specified.

## Edge cases

EC1. In `trim` mode, input containing leading or trailing code points with the Unicode `White_Space` property is governed by R2.

EC2. In `preserve` mode, input containing Unicode whitespace is governed by R3.

EC3. Any mode other than `trim` or `preserve` is governed by R4.

## Non-goals

Input-shape, transport, performance, storage, logging, and implementation requirements are out of scope.

## Acceptance criteria

| Criterion | Requirement IDs | Observable acceptance condition |
| --- | --- | --- |
| acceptance.mode.closed | R1 | Exactly `trim` and `preserve` are accepted modes. |
| acceptance.trim | R2 | Leading and trailing Unicode `White_Space` code points are removed in `trim` mode. |
| acceptance.preserve | R3 | The input text is returned unchanged in `preserve` mode. |
| acceptance.mode.unknown | R4 | Every unknown mode produces `unknown-mode` and no text. |

## Open questions

None.

## Next artifacts

Spec review, followed by a traceable test specification after approval and intervening required lifecycle stages.

## Follow-on artifacts

None yet

## Readiness

ready for spec-review
