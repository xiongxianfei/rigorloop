<!-- Template: spec-skeleton-v1 -->
<!-- Skill: spec -->
<!-- Template status: normative -->

# Portable text normalizer

## Status

draft

## Related proposal

Authoritative behavior request supplied with this spec.

## Goal and context

Define the observable behavior of a portable text normalizer with two accepted modes and a closed failure outcome for every other mode.

## Glossary

- Unicode whitespace: code points with the Unicode `White_Space` property.
- Unknown mode: every mode other than `trim` and `preserve`.

## Examples first

Example E1: trim surrounding Unicode whitespace
Given the input text `\u0020hello\u3000` and mode `trim`
When the text is normalized
Then the returned text is `hello`

Example E2: preserve text unchanged
Given the input text `\u0020hello\u3000` and mode `preserve`
When the text is normalized
Then the returned text is `\u0020hello\u3000`

Example E3: reject an unknown mode
Given input text and mode `fold`
When normalization is requested
Then the result is `unknown-mode` with no returned text

## Requirements

R1. The normalizer MUST accept exactly the closed modes `trim` and `preserve`.

R2. In `trim` mode, the normalizer MUST remove leading and trailing code points with the Unicode `White_Space` property from the input text.

R3. In `preserve` mode, the normalizer MUST return the input text unchanged.

R4. For every unknown mode, the normalizer MUST fail with `unknown-mode` and return no text.

Boundary model version: v1
Boundary model scope: R1-R4

## Boundary model

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| canonical-trust | applicable | R2 | b.whitespace.authority | - |
| identity-freshness | not-applicable | - | - | The contract does not bind evidence to an identity or define freshness. |
| closed-vocabulary | applicable | R1, R4 | b.mode.vocabulary | - |
| state-transition | not-applicable | - | - | The contract defines no persistent states or transitions. |
| authorization-scope | not-applicable | - | - | The contract defines no authorization decision. |
| mutation-atomicity | not-applicable | - | - | The contract defines no mutation or commit point. |
| interruption-recovery | not-applicable | - | - | The contract defines no prepared or interrupted work. |
| concurrency-idempotency | not-applicable | - | - | The contract defines no concurrent, duplicate, or replayed operation. |
| composition-bypass | applicable | R1, R2, R3, R4 | b.mode.behavior-path | - |
| compatibility-migration | not-applicable | - | - | The contract defines no old representation or migration. |
| outcome-stop | applicable | R4 | b.unknown.outcome | - |
| evidence-claims | not-applicable | - | - | The contract defines no evidence-based claim. |

Extensions: none.

## Examples

| Example ID | Role | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap |
| --- | --- | --- | --- | --- | --- |
| e.trim.whitespace | illustration | R1, R2 | b.mode.behavior-path, b.mode.vocabulary, b.whitespace.authority | - | - |
| e.preserve.unchanged | illustration | R1, R3 | b.mode.behavior-path, b.mode.vocabulary | - | - |
| e.unknown.failure | illustration | R1, R4 | b.mode.behavior-path, b.mode.vocabulary, b.unknown.outcome | - | - |

## Interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Rationale |
| --- | --- | --- | --- |
| i.mode.outcome | R1, R2, R3, R4 | b.mode.behavior-path, b.mode.vocabulary, b.unknown.outcome | composed-path |
| i.trim.authority | R1, R2 | b.mode.behavior-path, b.mode.vocabulary, b.whitespace.authority | trust-or-authority |

## Inputs and outputs

The behavioral inputs are input text and a mode. Successful `trim` and `preserve` outcomes return text as defined by R2 and R3. The failure outcome is defined by R4.

## State and invariants

No persistent state is specified. The mode vocabulary and its outcomes are governed by R1-R4.

## Error and boundary behavior

Unknown-mode behavior is governed by R4. Unicode whitespace boundaries in `trim` mode are governed by R2.

## Compatibility and migration

Not applicable; no compatibility or migration behavior is specified.

## Observability

The returned text or the `unknown-mode` failure with no text is the observable result. No logging or telemetry behavior is specified.

## Security and privacy

Not applicable; no security, authorization, secret-handling, or data-exposure behavior is specified.

## Accessibility and UX

Not applicable; no user interface is specified.

## Performance expectations

Not applicable; no performance behavior is specified.

## Edge cases

EC1. In `trim` mode, input containing leading or trailing code points with the Unicode `White_Space` property is covered by R2.

EC2. In `preserve` mode, input containing such code points is covered by R3.

EC3. Any mode outside the closed vocabulary is covered by R4.

## Non-goals

Input-shape, transport, performance, storage, logging, and implementation requirements are out of scope.

## Acceptance criteria

| Criterion | Requirement IDs | Observable acceptance condition |
| --- | --- | --- |
| AC1 | R1 | Tests accept `trim` and `preserve` as the complete closed mode vocabulary. |
| AC2 | R2 | Tests show that `trim` removes leading and trailing Unicode `White_Space` code points. |
| AC3 | R3 | Tests show that `preserve` returns the input text unchanged. |
| AC4 | R4 | Tests show that every tested unknown mode fails with `unknown-mode` and returns no text. |

## Open questions

None.

## Next artifacts

Spec review.

## Follow-on artifacts

None yet

## Readiness

Ready for spec-review.
