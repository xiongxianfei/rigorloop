# Portable text normalizer test specification

## Status

draft

## Related spec and plan

- Spec: Portable text normalizer authoritative stage input
- Plan: Not applicable; no execution milestones or implementation plan were supplied for this isolated proof-map stage.
- Architecture/ADRs: Not applicable.

## Input artifact identities

| Input | Path | Status / Review state | Identity |
| --- | --- | --- | --- |
| Feature spec | Authoritative stage input | draft with approved formal review | sha256:1a39ede7c08ec8341fe0b4858942a15c276972dfb33bc8cfe80f523c24db3081 |
| Spec review | reviews/spec-review.md | approved | spec-review-r1 |
| Plan | - | not applicable | No plan was supplied. |
| Architecture/ADRs | - | not applicable | The supplied feature defines no architecture dependency. |

## Testing strategy

Use contract-level automated tests against the public normalizer behavior. Test the closed mode vocabulary, both text-result modes, exhaustive Unicode `White_Space` boundary handling, preservation of those same code points when internal, and the composed mode-to-result outcomes. No end-to-end, smoke, migration, or manual proof is required by the supplied contract.

Boundary model version: v1
Boundary model scope: R1-R4

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| proof.mode-vocabulary | R1, R4 | boundary.mode-vocabulary | T1, T5 | automated | - |
| proof.unicode-whitespace | R2 | boundary.unicode-whitespace | T2, T3 | automated | - |
| proof.text-result | R2, R3 | boundary.text-result | T2, T3, T4 | automated | - |
| proof.unknown-mode-outcome | R4 | boundary.unknown-mode-outcome | T5 | automated | - |
| proof.mode-result | R1, R2, R3, R4 | interaction.mode-result | T1, T2, T3, T4, T5 | automated | - |

## Test cases

### T1. Accept exactly the two closed modes

- Covers: R1, example.trim-whitespace, example.preserve-text
- Level: contract
- Command IDs: none
- Fixture/setup: Public normalizer invocation with retained non-whitespace text and modes `trim` and `preserve`.
- Steps: Invoke once with each accepted mode.
- Expected result: Both modes are accepted and produce their requirement-owned text results; no other accepted mode is asserted here.
- Failure proves: The closed accepted vocabulary or its mode-to-result composition is broken.
- Evidence artifact: not applicable
- Automation location: To be selected during implementation.
- Required by milestone: test-spec-review

### T2. Remove every Unicode White_Space code point at text boundaries

- Covers: R2, EC1, example.trim-whitespace
- Level: contract
- Command IDs: none
- Fixture/setup: Deterministically enumerate `U+0009` through `U+000D`, `U+0020`, `U+0085`, `U+00A0`, `U+1680`, `U+2000` through `U+200A`, `U+2028`, `U+2029`, `U+202F`, `U+205F`, and `U+3000`; use retained non-whitespace sentinels `A` and `B`.
- Steps: For every enumerated code point, invoke `trim` with it before `AB`, after `AB`, and at both boundaries of `AB`.
- Expected result: Every enumerated boundary code point is removed and the returned text is exactly `AB` in every case.
- Failure proves: R2 is violated for at least one code point or boundary position.
- Evidence artifact: not applicable
- Automation location: To be selected during implementation.
- Required by milestone: test-spec-review

### T3. Preserve every Unicode White_Space code point between retained code points

- Covers: R2, EC1
- Level: contract
- Command IDs: none
- Fixture/setup: Use the exact deterministic Unicode `White_Space` enumeration from T2 and retained non-whitespace sentinels `A` and `B`.
- Steps: For every enumerated code point, invoke `trim` with the text `A<code point>B`.
- Expected result: The returned text is exactly `A<code point>B`; the internal code point is preserved.
- Failure proves: Trimming exceeds the leading and trailing boundaries defined by R2.
- Evidence artifact: not applicable
- Automation location: To be selected during implementation.
- Required by milestone: test-spec-review

### T4. Preserve input text unchanged

- Covers: R3, EC2, example.preserve-text
- Level: contract
- Command IDs: none
- Fixture/setup: Inputs containing no whitespace, boundary whitespace, internal whitespace, and the empty text.
- Steps: Invoke `preserve` with each input.
- Expected result: Each returned text is exactly identical to its input.
- Failure proves: Preserve mode transforms text or returns the wrong result.
- Evidence artifact: not applicable
- Automation location: To be selected during implementation.
- Required by milestone: test-spec-review

### T5. Reject every unknown mode with no text

- Covers: R1, R4, EC3, example.unknown-mode
- Level: contract
- Command IDs: none
- Fixture/setup: A parameterized or property-based mode source constrained only to values unequal to `trim` and `preserve`, within the implementation's supplied mode input domain.
- Steps: Invoke the normalizer for each generated unknown mode with retained non-whitespace text.
- Expected result: Every invocation fails with `unknown-mode` and returns no text.
- Failure proves: An unknown mode is accepted, reports a different failure, or returns text.
- Evidence artifact: not applicable
- Automation location: To be selected during implementation.
- Required by milestone: test-spec-review

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T1, T5 | contract | Proves accepted and rejected vocabulary partitions. |
| R2 | T2, T3 | contract | Exhaustively enumerates Unicode `White_Space` for boundary removal and internal preservation. |
| R3 | T4 | contract | Proves unchanged text across representative text partitions. |
| R4 | T5 | contract | Quantifies over supplied modes outside the closed vocabulary. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| example.trim-whitespace | T1, T2 | Proves the illustrated accepted mode and trimming outcome. |
| example.preserve-text | T1, T4 | Proves the illustrated accepted mode and unchanged result. |
| example.unknown-mode | T5 | Proves the illustrated closed failure outcome. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 | T2, T3 | Covers every Unicode `White_Space` code point at boundaries and between retained code points. |
| EC2 | T4 | Covers unchanged text including whitespace-bearing and empty text. |
| EC3 | T5 | Covers arbitrary supplied modes outside the accepted vocabulary. |

## Validation commands

No validation commands are part of this proof map because the authoritative inputs provide no repository, test runner, or command contract.

## Milestone proof map

Not applicable because no execution plan, staged validation, or implementation milestone was supplied.

## Fixtures and data

The Unicode fixture is the deterministic 25-code-point `White_Space` enumeration recorded in T2. Retained sentinels are `A` and `B`. T4 uses representative unchanged-text inputs. T5 uses unknown modes constrained only by inequality with the two accepted strings.

## Mocking/stubbing policy

Do not mock Unicode classification or the public normalizer result. Generators may supply cases but must not compute expected outcomes by calling the implementation under test.

## Migration or compatibility tests

Not applicable; the feature specifies no migration or compatibility behavior.

## Observability verification

Verify only returned text or the `unknown-mode` failure with absence of text. Logs, metrics, traces, and audit events are outside the contract.

## Security/privacy verification

Not applicable; the feature specifies no security or privacy behavior.

## Performance checks

Not applicable; the feature specifies no performance behavior.

## Manual QA checklist

Not applicable; all proof obligations are automated.

## What not to test and why

Do not test input shape, transport, storage, logging, performance, UI, or implementation structure because the approved specification makes them non-goals. Do not require normalization of internal whitespace in `trim` mode; R2 governs only leading and trailing boundaries.

## Uncovered gaps

None in the approved R1-R4 boundary record. Repository-specific automation paths, validation commands, and milestone gates remain unset because no execution plan or repository conventions were supplied.

## Next artifacts

Independent test-spec review.

## Follow-on artifacts

None yet.

## Readiness

The boundary-first proof map is complete for every applicable boundary and the selected interaction. The draft is ready for test-spec-review; implementation remains outside this stage.
