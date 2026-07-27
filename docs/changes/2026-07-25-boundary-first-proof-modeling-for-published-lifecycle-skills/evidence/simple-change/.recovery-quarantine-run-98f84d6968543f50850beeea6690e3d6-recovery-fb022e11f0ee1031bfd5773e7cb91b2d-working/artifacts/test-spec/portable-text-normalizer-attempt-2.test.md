# Portable text normalizer test specification

## Status

draft

## Related spec and plan

- Spec: Portable text normalizer authoritative stage input
- Plan: Not applicable; no execution plan was supplied.
- Architecture/ADRs: Not applicable.

## Input artifact identities

| Input | Path | Status / Review state | Identity |
| --- | --- | --- | --- |
| Feature spec | Authoritative stage input | draft with approved formal review | sha256:1a39ede7c08ec8341fe0b4858942a15c276972dfb33bc8cfe80f523c24db3081 |
| Spec review | reviews/spec-review.md | approved | spec-review-r1 |
| Test-spec review | reviews/test-spec-review.md | changes-requested | test-spec-review-r1 |
| Plan | - | not applicable | No plan was supplied. |
| Architecture/ADRs | - | not applicable | The feature defines no architecture dependency. |

## Testing strategy

Use automated contract tests against the public normalizer behavior. Prove the closed mode vocabulary, positive and targeted negative Unicode `White_Space` boundary classification, internal whitespace preservation, unchanged preserve-mode results, unknown-mode failure, and the composed mode-to-result outcomes. No end-to-end, smoke, migration, or manual proof is required.

Boundary model version: v1
Boundary model scope: R1-R4

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| proof.mode-vocabulary | R1, R4 | boundary.mode-vocabulary | T1, T6 | automated | - |
| proof.unicode-whitespace | R2 | boundary.unicode-whitespace | T2, T3, T4 | automated | - |
| proof.text-result | R2, R3 | boundary.text-result | T2, T3, T4, T5 | automated | - |
| proof.unknown-mode-outcome | R4 | boundary.unknown-mode-outcome | T6 | automated | - |
| proof.mode-result | R1, R2, R3, R4 | interaction.mode-result | T1, T2, T3, T4, T5, T6 | automated | - |

## Test cases

### T1. Accept exactly the two closed modes

- Covers: R1, example.trim-whitespace, example.preserve-text
- Level: integration
- Command IDs: none
- Fixture/setup: Public normalizer invocation with retained text and modes `trim` and `preserve`.
- Steps: Invoke once with each accepted mode.
- Expected result: Both modes are accepted and produce their requirement-owned text results.
- Failure proves: The accepted vocabulary or mode-to-result composition is broken.
- Evidence artifact: not applicable
- Automation location: To be selected during implementation.
- Required by milestone: test-spec-review

### T2. Remove every authoritative Unicode White_Space member at text boundaries

- Covers: R2, EC1, example.trim-whitespace
- Level: integration
- Command IDs: none
- Fixture/setup: Generate the positive fixture from the `White_Space` property entries in the repository-pinned Unicode Character Database `PropList.txt`; fixture metadata records the Unicode version and source-file digest. Use retained non-whitespace sentinels `A` and `B`.
- Steps: For every generated property member, invoke `trim` with it before `AB`, after `AB`, and at both boundaries.
- Expected result: Every property member is removed and the returned text is exactly `AB`.
- Failure proves: R2 is violated for a property member or boundary position.
- Evidence artifact: Unicode fixture metadata produced with the automated test data.
- Automation location: To be selected during implementation.
- Required by milestone: test-spec-review

### T3. Retain targeted Unicode White_Space non-members at text boundaries

- Covers: R2, EC1
- Level: integration
- Command IDs: none
- Fixture/setup: From the same pinned `PropList.txt` evidence basis as T2, assert that targeted adjacent, confusable, or historically misclassified code points `U+180E`, `U+200B`, and `U+FEFF` are absent from `White_Space`; use sentinels `A` and `B`.
- Steps: For each asserted non-member, invoke `trim` with it before `AB`, after `AB`, and at both boundaries.
- Expected result: Each non-member remains exactly present at every supplied boundary.
- Failure proves: The implementation uses a substituted or overbroad whitespace classifier instead of the authoritative property boundary required by R2.
- Evidence artifact: Unicode fixture metadata produced with the automated test data.
- Automation location: To be selected during implementation.
- Required by milestone: test-spec-review

### T4. Preserve Unicode White_Space members between retained code points

- Covers: R2, EC1
- Level: integration
- Command IDs: none
- Fixture/setup: Use the generated positive fixture from T2 and sentinels `A` and `B`.
- Steps: For every property member, invoke `trim` with `A<code point>B`.
- Expected result: The returned text is exactly `A<code point>B`.
- Failure proves: Trimming exceeds the leading and trailing boundaries defined by R2.
- Evidence artifact: Unicode fixture metadata produced with the automated test data.
- Automation location: To be selected during implementation.
- Required by milestone: test-spec-review

### T5. Preserve input text unchanged

- Covers: R3, EC2, example.preserve-text
- Level: integration
- Command IDs: none
- Fixture/setup: Inputs containing no whitespace, boundary whitespace, internal whitespace, targeted non-members, and empty text.
- Steps: Invoke `preserve` with each input.
- Expected result: Each returned text is exactly identical to its input.
- Failure proves: Preserve mode transforms text or returns the wrong result.
- Evidence artifact: not applicable
- Automation location: To be selected during implementation.
- Required by milestone: test-spec-review

### T6. Reject every unknown mode with no text

- Covers: R1, R4, EC3, example.unknown-mode
- Level: integration
- Command IDs: none
- Fixture/setup: A parameterized or property-based mode source constrained to values unequal to `trim` and `preserve` within the supplied mode input domain.
- Steps: Invoke the normalizer for each generated unknown mode with retained text.
- Expected result: Every invocation fails with `unknown-mode` and returns no text.
- Failure proves: An unknown mode is accepted, reports another failure, or returns text.
- Evidence artifact: not applicable
- Automation location: To be selected during implementation.
- Required by milestone: test-spec-review

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T1, T6 | contract | Covers accepted and rejected vocabulary partitions. |
| R2 | T2, T3, T4 | contract | Covers authoritative positive members, targeted boundary non-members, and internal preservation. |
| R3 | T5 | contract | Covers unchanged representative inputs. |
| R4 | T6 | contract | Covers supplied modes outside the closed vocabulary. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| example.trim-whitespace | T1, T2 | Covers the accepted mode and trimming outcome. |
| example.preserve-text | T1, T5 | Covers the accepted mode and unchanged result. |
| example.unknown-mode | T6 | Covers the closed failure outcome. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 | T2, T3, T4 | Covers property members, targeted non-members, boundary positions, and internal members. |
| EC2 | T5 | Covers whitespace-bearing, non-member-bearing, and empty text. |
| EC3 | T6 | Covers supplied modes outside the accepted vocabulary. |

## Validation commands

No validation commands are part of this proof map because no repository, runner, or command contract was supplied.

## Milestone proof map

Not applicable because no execution plan or implementation milestone was supplied.

## Fixtures and data

The Unicode fixture is generated deterministically from the `White_Space` entries in the repository-pinned Unicode Character Database `PropList.txt`. Its metadata records the Unicode version and source-file digest. Targeted negative cases `U+180E`, `U+200B`, and `U+FEFF` must be verified absent from that same property source before test execution. Sentinels are `A` and `B`; other fixtures are defined by T5 and T6.

## Mocking/stubbing policy

Do not mock Unicode classification or the public normalizer result. Fixture generation may parse the pinned authoritative property data but must not derive expected results from the implementation under test.

## Migration or compatibility tests

Not applicable; no migration or compatibility behavior is specified.

## Observability verification

Verify only returned text or the `unknown-mode` failure with no text.

## Security/privacy verification

Not applicable; no security or privacy behavior is specified.

## Performance checks

Not applicable; no performance behavior is specified.

## Manual QA checklist

Not applicable; every proof obligation is automated.

## What not to test and why

Do not test input shape, transport, storage, logging, performance, UI, or implementation structure because they are non-goals. Do not require removal of internal whitespace in `trim` mode.

## Uncovered gaps

None in R1-R4. Repository-specific automation paths and commands remain unset because no repository context was supplied.

## Next artifacts

Independent test-spec re-review.

## Follow-on artifacts

review-resolution/test-spec-review.md records the bounded correction of finding.unicode-boundary-proof.

## Readiness

The corrected boundary-first proof map directly covers every applicable boundary and interaction. It is ready for a new test-spec review; implementation remains not allowed pending that review.
