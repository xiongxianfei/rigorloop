<!-- Template: spec-skeleton-v1 -->
<!-- Skill: spec -->

# Portable text normalizer

## Status

draft

## Related proposal

Authoritative behavior request supplied with this specification.

## Goal and context

Define portable, observable text normalization for two closed modes.

## Glossary

- `White_Space`: the Unicode property of that exact name.
- `unknown-mode`: the failure returned for a mode other than `trim` or `preserve`.

## Examples first

Example ex.trim.whitespace: trim surrounding Unicode whitespace
Given the input `\u0020hello\u00A0` and mode `trim`
When the text is normalized
Then the returned text is `hello`

Example ex.preserve.unchanged: preserve text unchanged
Given the input `\u0020hello\u00A0` and mode `preserve`
When the text is normalized
Then the returned text is `\u0020hello\u00A0`

Example ex.unknown.failure: reject an unknown mode
Given the input `hello` and mode `fold`
When normalization is attempted
Then the result is `unknown-mode` and contains no text

## Requirements

R1. The normalizer MUST accept exactly the modes `trim` and `preserve`.

R2. In `trim` mode, the normalizer MUST remove leading and trailing code points having the Unicode `White_Space` property.

R3. In `preserve` mode, the normalizer MUST return the input text unchanged.

R4. For every unknown mode, the normalizer MUST fail with `unknown-mode` and return no text.

Boundary model version: v1
Boundary model scope: R1-R4

## Boundary model

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| canonical-trust | applicable | R2 | boundary.whitespace.authority | - |
| identity-freshness | not-applicable | - | - | The contract uses no identity-bound evidence. |
| closed-vocabulary | applicable | R1, R4 | boundary.mode.vocabulary | - |
| state-transition | not-applicable | - | - | The contract defines no persistent states or transitions. |
| authorization-scope | not-applicable | - | - | The contract defines no authorization action or scope. |
| mutation-atomicity | not-applicable | - | - | The contract defines no mutation or commit point. |
| interruption-recovery | not-applicable | - | - | The contract defines no prepared or interruptible work. |
| concurrency-idempotency | not-applicable | - | - | The contract defines no concurrent, duplicate, or replayed work. |
| composition-bypass | not-applicable | - | - | The contract defines no helper, sibling, retry, or alternate public path. |
| compatibility-migration | not-applicable | - | - | The contract defines no old representation or migration. |
| outcome-stop | applicable | R4 | boundary.unknown.outcome | - |
| evidence-claims | not-applicable | - | - | The contract makes no evidence-backed operational claim. |

Extensions:

| Extension ID | Title | Applicability | Rationale | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- | --- | --- |
| x.text.transformation | Mode-specific text transformation | applicable | The core dimensions do not represent the returned-text semantics of the two accepted modes. | R2, R3 | boundary.text.transformation | - |

## Examples

| Example ID | Role | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap |
| --- | --- | --- | --- | --- | --- |
| example.trim.whitespace | illustration | R2 | boundary.whitespace.authority, boundary.text.transformation | - | - |
| example.preserve.unchanged | illustration | R3 | boundary.text.transformation | - | - |
| example.unknown.failure | illustration | R1, R4 | boundary.mode.vocabulary, boundary.unknown.outcome | - | - |

## Interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Rationale |
| --- | --- | --- | --- |
| interaction.mode.result | R1, R2, R3, R4 | boundary.mode.vocabulary, boundary.text.transformation, boundary.unknown.outcome | composed-path |
| interaction.whitespace.trim | R2 | boundary.whitespace.authority, boundary.text.transformation | trust-or-authority |

## Inputs and outputs

The input is text plus a mode. A successful result contains text; an unknown-mode result contains the `unknown-mode` failure and no text.

## State and invariants

There is no persistent state. The `preserve` result is identical to its input text, and an unknown-mode result has no text.

## Error and boundary behavior

Unknown modes produce the behavior in R4. Leading or trailing code points outside Unicode `White_Space` are outside the removal set in R2.

## Compatibility and migration

Not applicable; no prior representation or migration is specified.

## Observability

The returned text or `unknown-mode` failure is the observable result. No logging or operational telemetry requirement is specified.

## Security and privacy

Not applicable; no security, authorization, retention, or disclosure behavior is specified.

## Accessibility and UX

Not applicable; no user interface is specified.

## Performance expectations

Not applicable; no performance requirement is specified.

## Edge cases

EC1. In `trim` mode, input containing only Unicode `White_Space` code points returns empty text under R2.

EC2. In `trim` mode, internal Unicode `White_Space` code points are unchanged because R2 applies only to leading and trailing positions.

EC3. In `preserve` mode, empty text and text containing Unicode whitespace are returned unchanged under R3.

EC4. Any mode other than the two values in R1 follows R4.

## Non-goals

Input shape, transport, performance, storage, logging, and implementation behavior are not specified.

## Acceptance criteria

| Criterion | Requirement IDs | Observable acceptance |
| --- | --- | --- |
| criterion.mode.closed | R1, R4 | `trim` and `preserve` are accepted; every other mode yields `unknown-mode` with no text. |
| criterion.trim.unicode | R2 | Leading and trailing Unicode `White_Space` code points are absent from the returned text. |
| criterion.preserve.exact | R3 | The returned text is identical to the input text. |

## Open questions

None.

## Next artifacts

Spec review.

## Follow-on artifacts

None yet

## Readiness

ready for spec-review
