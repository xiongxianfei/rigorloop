<!-- Template: spec-skeleton-v1 -->
<!-- Skill: spec -->
<!-- Template status: normative -->

# Portable text normalizer

## Status

draft

## Related proposal

Authoritative behavior request supplied with this spec.

## Goal and context

Define the observable behavior of a portable text normalizer with two closed modes.

## Glossary

- Unicode whitespace: code points with the Unicode `White_Space` property.
- No text: the operation does not return text.

## Examples first

The classified examples appear in the contiguous boundary record below and illustrate only R1-R4.

## Requirements

R1. The normalizer MUST accept exactly the closed modes `trim` and `preserve`.

R2. In `trim` mode, the normalizer MUST remove leading and trailing Unicode whitespace from the input text, where whitespace means code points with the Unicode `White_Space` property.

R3. In `preserve` mode, the normalizer MUST return the input text unchanged.

R4. For every unknown mode, the normalizer MUST fail with `unknown-mode` and return no text.

Boundary model version: v1
Boundary model scope: R1-R4

## Boundary model

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| canonical-trust | not-applicable | - | - | The contract does not select among conflicting authoritative sources. |
| identity-freshness | not-applicable | - | - | The contract does not bind evidence to an identity or define staleness. |
| closed-vocabulary | applicable | R1, R4 | boundary.mode.vocabulary | - |
| state-transition | not-applicable | - | - | The contract defines no persistent states or transitions. |
| authorization-scope | not-applicable | - | - | The contract defines no authorization decisions. |
| mutation-atomicity | not-applicable | - | - | The contract defines no mutation or commit point. |
| interruption-recovery | not-applicable | - | - | The contract defines no prepared or interruptible work. |
| concurrency-idempotency | not-applicable | - | - | The contract defines no concurrent, duplicate, or replayed work. |
| composition-bypass | not-applicable | - | - | The contract defines no distinct helper, public, sibling, or retry paths. |
| compatibility-migration | not-applicable | - | - | The contract defines no old representation or migration behavior. |
| outcome-stop | applicable | R4 | boundary.unknown.outcome | - |
| evidence-claims | not-applicable | - | - | The contract defines no evidence-backed claims. |

Extensions:

| Extension ID | Title | Applicability | Rationale | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- | --- | --- |
| x.text.transformation | Mode-selected text transformation | applicable | Defines the two requirement-owned text transformation outcomes. | R2, R3 | boundary.text.transformation | - |

## Examples

| Example ID | Role | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap |
| --- | --- | --- | --- | --- | --- |
| example.trim.whitespace | illustration | R1, R2 | boundary.mode.vocabulary, boundary.text.transformation | - | - |
| example.trim.non-whitespace | illustration | R2 | boundary.text.transformation | - | - |
| example.preserve.unchanged | illustration | R1, R3 | boundary.mode.vocabulary, boundary.text.transformation | - | - |
| example.unknown.failure | illustration | R1, R4 | boundary.mode.vocabulary, boundary.unknown.outcome | - | - |

## Interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Rationale |
| --- | --- | --- | --- |
| interaction.mode.transformation | R1, R2, R3 | boundary.mode.vocabulary, boundary.text.transformation | composed-path |
| interaction.unknown.stop | R1, R4 | boundary.mode.vocabulary, boundary.unknown.outcome | state-coupling |

## Inputs and outputs

The input is text and one mode. For `trim` and `preserve`, the output is text as specified by R2 and R3. For every unknown mode, the outcome is `unknown-mode` with no text as specified by R4.

## State and invariants

The accepted mode vocabulary is exactly the set defined by R1. The transformation and failure outcomes remain governed by R2-R4.

## Error and boundary behavior

Unknown modes have the failure behavior specified by R4. Leading and trailing Unicode whitespace has the boundary behavior specified by R2.

## Compatibility and migration

Not applicable; no compatibility or migration behavior is specified.

## Observability

The returned text or the `unknown-mode` failure with no text is the observable result. No logging, metrics, tracing, or storage requirements are specified.

## Security and privacy

Not applicable; no security or privacy behavior is specified.

## Accessibility and UX

Not applicable; no user interface behavior is specified.

## Performance expectations

Not applicable; no performance behavior is specified.

## Edge cases

EC1. In `trim` mode, input containing no leading or trailing Unicode whitespace is returned without boundary removal, as required by R2.

EC2. In `trim` mode, input consisting entirely of Unicode whitespace has all leading and trailing Unicode whitespace removed, as required by R2.

EC3. In `preserve` mode, Unicode whitespace remains unchanged, as required by R3.

EC4. Any mode other than `trim` or `preserve` produces the R4 failure outcome.

## Non-goals

Input-shape, transport, performance, storage, logging, and implementation requirements are outside this specification.

## Acceptance criteria

| Criterion | Requirement IDs | Observable acceptance condition |
| --- | --- | --- |
| Modes | R1 | `trim` and `preserve` are accepted, and no other mode is accepted. |
| Trim | R2 | Leading and trailing code points with the Unicode `White_Space` property are removed in `trim` mode. |
| Preserve | R3 | The input text is returned unchanged in `preserve` mode. |
| Unknown mode | R4 | Every unknown mode yields `unknown-mode` and no text. |

## Open questions

None.

## Next artifacts

Spec review.

## Follow-on artifacts

None yet

## Readiness

Ready for spec-review.
