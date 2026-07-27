# Portable text normalizer

## Status

draft

## Related proposal

Direct authoritative behavior request; no separate proposal.

## Goal and context

Define the observable behavior of a portable text normalizer with two closed modes.

## Glossary

- `White_Space`: the Unicode `White_Space` property.
- `unknown-mode`: the required failure for a mode other than `trim` or `preserve`.

## Examples first

Example e.trim.outer-whitespace: trim outer Unicode whitespace
Given input text `\u00A0hello\u3000` and mode `trim`
When the text is normalized
Then the returned text is `hello`

Example e.preserve.unchanged: preserve text unchanged
Given input text `  hello  ` and mode `preserve`
When the text is normalized
Then the returned text is `  hello  `

Example e.mode.unknown: reject an unknown mode
Given input text `hello` and mode `other`
When normalization is attempted
Then it fails with `unknown-mode` and returns no text

## Requirements

R1. The normalizer MUST accept exactly the closed modes `trim` and `preserve`.

R2. In `trim` mode, the normalizer MUST remove leading and trailing code points having the Unicode `White_Space` property.

R3. In `preserve` mode, the normalizer MUST return the input text unchanged.

R4. For every unknown mode, the normalizer MUST fail with `unknown-mode` and return no text.

Boundary model version: v1
Boundary model scope: R1-R4

## Boundary model

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| canonical-trust | not-applicable | - | - | No competing authoritative source is part of R1-R4. |
| identity-freshness | not-applicable | - | - | R1-R4 define no evidence identity or freshness behavior. |
| closed-vocabulary | applicable | R1, R4 | mode.vocabulary | - |
| state-transition | not-applicable | - | - | R1-R4 define no persistent states or transitions. |
| authorization-scope | not-applicable | - | - | R1-R4 define no authorization behavior. |
| mutation-atomicity | not-applicable | - | - | R1-R4 define no mutation or commit behavior. |
| interruption-recovery | not-applicable | - | - | R1-R4 define no prepared or interrupted work. |
| concurrency-idempotency | not-applicable | - | - | R1-R4 define no concurrency, replay, or duplicate-work behavior. |
| composition-bypass | not-applicable | - | - | R1-R4 define behavior without distinct helper, public, sibling, or retry paths. |
| compatibility-migration | not-applicable | - | - | R1-R4 define no old representation or migration behavior. |
| outcome-stop | applicable | R4 | outcome.unknown-mode | - |
| evidence-claims | not-applicable | - | - | R1-R4 define no evidence or claim behavior. |

Extensions:

| Extension ID | Title | Applicability | Rationale | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- | --- | --- |
| x.text.transformation | Mode-specific text transformation | applicable | The core dimensions do not classify the required text result for each accepted mode. | R2, R3 | text.transformation | - |

## Examples

| Example ID | Role | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap |
| --- | --- | --- | --- | --- | --- |
| example.trim.outer-whitespace | illustration | R2 | text.transformation | - | - |
| example.preserve.unchanged | illustration | R3 | text.transformation | - | - |
| example.mode.unknown | illustration | R1, R4 | mode.vocabulary, outcome.unknown-mode | - | - |

## Interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Rationale |
| --- | --- | --- | --- |
| interaction.unknown-mode-outcome | R4 | mode.vocabulary, outcome.unknown-mode | state-coupling |
| interaction.accepted-mode-transform | R1, R2, R3 | mode.vocabulary, text.transformation | composed-path |

## Inputs and outputs

The input is text plus a mode. A successful result is text. The R4 failure result is `unknown-mode` with no text.

## State and invariants

The accepted-mode vocabulary is exactly `trim` and `preserve`. The result for each accepted mode is governed by R2 or R3.

## Error and boundary behavior

Unknown modes have the failure behavior specified by R4. Leading and trailing Unicode `White_Space` code points are governed by R2.

## Compatibility and migration

Not applicable; R1-R4 define no compatibility or migration behavior.

## Observability

Not applicable; R1-R4 define no logging, metrics, tracing, or audit behavior.

## Security and privacy

Not applicable; R1-R4 define no security or privacy behavior.

## Accessibility and UX

Not applicable; R1-R4 define no user-interface behavior.

## Performance expectations

Not applicable; R1-R4 define no performance behavior.

## Edge cases

- An input consisting entirely of Unicode `White_Space` code points is governed by R2.
- An input containing no leading or trailing Unicode `White_Space` code points is governed by R2.
- An unknown mode is governed by R4 regardless of the input text.

## Non-goals

Input shape, transport, performance, storage, logging, and implementation behavior are outside this specification.

## Acceptance criteria

| Requirement ID | Acceptance criterion |
| --- | --- |
| R1 | Exactly `trim` and `preserve` are accepted modes. |
| R2 | `trim` removes leading and trailing Unicode `White_Space` code points. |
| R3 | `preserve` returns the input text unchanged. |
| R4 | Every unknown mode produces `unknown-mode` and no text. |

## Open questions

None.

## Next artifacts

Spec review.

## Follow-on artifacts

None yet

## Readiness

Ready for spec-review.
