<!-- Template: spec-skeleton-v1 -->
<!-- Skill: spec -->
<!-- Template status: normative -->

# Portable text normalizer

## Status

draft

## Related proposal

Authoritative behavior request supplied with this spec.

## Goal and context

Define the observable results of normalizing text under a closed mode selection.

## Glossary

- Unicode whitespace: code points with the Unicode `White_Space` property.

## Examples first

The classified examples are recorded in the contiguous boundary record below.

Boundary model version: v1
Boundary model scope: R1-R4

## Boundary model

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| canonical-trust | applicable | R2 | b.unicode.authority | - |
| identity-freshness | not-applicable | - | - | The requirements define no identity-bearing evidence or freshness period. |
| closed-vocabulary | applicable | R1, R4 | b.mode.closed | - |
| state-transition | not-applicable | - | - | The requirements define no persistent states or transitions. |
| authorization-scope | not-applicable | - | - | The requirements define no authorization decisions. |
| mutation-atomicity | not-applicable | - | - | The requirements define no persisted mutation or commit point. |
| interruption-recovery | not-applicable | - | - | The requirements define no prepared or interruptible work. |
| concurrency-idempotency | not-applicable | - | - | The requirements define no concurrent, replayed, or duplicate work. |
| composition-bypass | not-applicable | - | - | The requirements define no helper, public, sibling, or retry paths. |
| compatibility-migration | not-applicable | - | - | The requirements define no legacy representation or migration. |
| outcome-stop | applicable | R4 | b.unknown.stop | - |
| evidence-claims | not-applicable | - | - | The requirements define no evidence-backed claims. |

Extensions:

| Extension ID | Title | Applicability | Rationale | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- | --- | --- |
| x.text.transformation | Mode-specific text result | applicable | The core dimensions do not represent the text transformation selected by a recognized mode. | R2, R3 | b.text.result | - |

## Examples

| Example ID | Role | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap |
| --- | --- | --- | --- | --- | --- |
| e.mode.accepted | illustration | R1 | b.mode.closed | - | - |
| e.trim.unicode | illustration | R2 | b.unicode.authority, b.text.result | - | - |
| e.preserve.unchanged | illustration | R3 | b.text.result | - | - |
| e.unknown.rejected | illustration | R4 | b.mode.closed, b.unknown.stop | - | - |

## Interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Rationale |
| --- | --- | --- | --- |
| i.mode.outcome | R1, R2, R3, R4 | b.mode.closed, b.unicode.authority, b.text.result, b.unknown.stop | composed-path |

## Requirements

R1. The normalizer MUST accept exactly the closed modes `trim` and `preserve`.

R2. In `trim` mode, the normalizer MUST remove leading and trailing code points having the Unicode `White_Space` property.

R3. In `preserve` mode, the normalizer MUST return the input text unchanged.

R4. For every unknown mode, the normalizer MUST fail with `unknown-mode` and return no text.

## Inputs and outputs

The behavioral inputs are text and a mode governed by R1. The observable result is governed by R2, R3, or R4 according to that mode.

## State and invariants

No persistent state is specified. R1-R4 define the complete behavioral contract.

## Error and boundary behavior

Unknown-mode behavior is defined by R4. Unicode whitespace boundaries are defined by R2.

## Compatibility and migration

Not applicable; no compatibility or migration behavior is specified.

## Observability

The returned text or the `unknown-mode` failure is the observable outcome. No logging, metrics, tracing, or audit behavior is specified.

## Security and privacy

Not applicable; no security or privacy behavior is specified.

## Accessibility and UX

Not applicable; no user interface is specified.

## Performance expectations

Not applicable; no performance contract is specified.

## Edge cases

EC1. Text with no leading or trailing Unicode whitespace is governed by R2.

EC2. Text consisting entirely of Unicode whitespace is governed by R2.

EC3. An unknown mode is governed by R4 regardless of the input text.

## Non-goals

Input shape, transport, performance, storage, logging, and implementation behavior are outside this specification.

## Acceptance criteria

| Criterion | Requirement IDs |
| --- | --- |
| Both recognized modes and no others are accepted. | R1 |
| Leading and trailing Unicode `White_Space` code points are removed in `trim`. | R2 |
| Input text is unchanged in `preserve`. | R3 |
| Every unknown mode produces `unknown-mode` and no text. | R4 |

## Open questions

None.

## Next artifacts

Spec review.

## Follow-on artifacts

None yet

## Readiness

ready for spec-review
