# Portable text normalizer test specification

## Status

draft

## Related spec and plan

- Spec: Portable text normalizer authoritative stage input
- Plan: Not applicable; no execution plan or milestones govern this isolated proof-map stage.
- Architecture/ADRs: Not applicable; the approved feature defines no architecture-specific behavior.

## Input artifact identities

| Input | Path | Status / Review state | Identity |
| --- | --- | --- | --- |
| Feature specification | authoritative stage input | approved by formal spec review | sha256:4281dc93ccdbbbfe345752090ac164f5f93aaa963a675cc51fc0f41c95e40366 |
| Spec review | reviews/spec-review.md | approved and recorded | spec-review-r1 |
| Execution plan | - | not applicable | No plan was supplied or required for this isolated proof map. |
| Architecture/ADRs | - | not applicable | The approved feature has no architecture dependency. |

## Testing strategy

Use deterministic contract tests for the closed mode vocabulary, Unicode whitespace behavior, unchanged preservation, and unknown-mode failure. T2 enumerates every code point in the Unicode `White_Space` property and checks both boundary removal and interior preservation. No integration, end-to-end, smoke, migration, or manual proof is required by the approved contract.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T1, T4 | contract | Proves acceptance of exactly `trim` and `preserve` and rejection of every other mode. |
| R2 | T2 | contract | Deterministically covers all 25 Unicode `White_Space` code points at both text boundaries and between retained non-whitespace code points. |
| R3 | T3 | contract | Proves byte-for-byte or code-point-for-code-point unchanged text output, as appropriate to the implementation representation. |
| R4 | T4 | contract | Proves `unknown-mode` and no text for every mode outside the closed vocabulary. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| example.trim.whitespace | T2 | Covers Unicode boundary-whitespace removal. |
| example.preserve.unchanged | T3 | Covers unchanged preserve output, including boundary whitespace. |
| example.unknown.failure | T4 | Covers unknown-mode failure with no text. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 | T2 | Every Unicode `White_Space` code point is exercised leading, trailing, at both boundaries, and internally. |
| EC2 | T3 | Boundary whitespace and mixed Unicode text remain unchanged in `preserve` mode. |
| EC3 | T4 | A property-based or equivalent parameterized partition covers every mode unequal to the two accepted literals. |
| Empty text | T2, T3 | Confirms the specified transformations without defining input-shape behavior. |
| Whitespace-only text | T2, T3 | Confirms complete boundary removal in `trim` and unchanged output in `preserve`. |

Boundary model version: v1
Boundary model scope: R1-R4

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| proof.mode.vocabulary | R1, R4 | mode.vocabulary | T1, T4 | automated | - |
| proof.whitespace.authority | R2 | whitespace.authority | T2 | automated | - |
| proof.text.output | R2, R3 | text.output | T2, T3 | automated | - |
| proof.unknown.outcome | R4 | unknown.outcome | T4 | automated | - |
| proof.interaction.trim-result | R1, R2 | interaction.trim.result | T2 | automated | - |
| proof.interaction.preserve-result | R1, R3 | interaction.preserve.result | T3 | automated | - |
| proof.interaction.unknown-result | R1, R4 | interaction.unknown.result | T4 | automated | - |

## Test cases

### T1. Accept exactly the closed mode vocabulary

- Covers: R1, mode.vocabulary
- Level: unit
- Command IDs: none
- Fixture/setup: Representative input text and the exact mode literals `trim` and `preserve`.
- Steps: Invoke the normalizer once with `trim` and once with `preserve`.
- Expected result: Both exact literals are accepted and produce their requirement-governed outcomes.
- Failure proves: The accepted vocabulary omits a required mode or does not recognize its exact literal.
- Evidence artifact: not applicable
- Automation location: Implementation test suite, location selected during implementation.
- Required by milestone: not applicable

### T2. Enumerate Unicode White_Space trimming and interior preservation

- Covers: R2, EC1, example.trim.whitespace, whitespace.authority, text.output, interaction.trim.result
- Level: unit
- Command IDs: none
- Fixture/setup: A deterministic table containing exactly `U+0009`, `U+000A`, `U+000B`, `U+000C`, `U+000D`, `U+0020`, `U+0085`, `U+00A0`, `U+1680`, `U+2000`, `U+2001`, `U+2002`, `U+2003`, `U+2004`, `U+2005`, `U+2006`, `U+2007`, `U+2008`, `U+2009`, `U+200A`, `U+2028`, `U+2029`, `U+202F`, `U+205F`, and `U+3000`.
- Steps: For each table entry `W`, invoke `trim` with `W + A`, `A + W`, `W + A + W`, and `A + W + B`, where `A` and `B` are retained non-whitespace code points. Also invoke `trim` with `W` alone and with empty text.
- Expected result: The first three inputs return `A`; `A + W + B` is returned unchanged; `W` alone and empty text return empty text. Every listed code point is exercised independently in every stated position.
- Failure proves: The implementation uses a whitespace authority different from Unicode `White_Space`, fails either boundary, removes interior whitespace, or produces an incorrect empty result.
- Evidence artifact: not applicable
- Automation location: Implementation test suite, location selected during implementation.
- Required by milestone: not applicable

### T3. Preserve input text unchanged

- Covers: R3, EC2, example.preserve.unchanged, text.output, interaction.preserve.result
- Level: unit
- Command IDs: none
- Fixture/setup: Parameterized inputs including empty text, non-whitespace text, whitespace-only text, boundary whitespace, interior whitespace, and mixed Unicode text.
- Steps: Invoke `preserve` for each input and compare the returned text directly with the original input.
- Expected result: Each returned text is unchanged from its input.
- Failure proves: `preserve` transforms, removes, inserts, or substitutes text.
- Evidence artifact: not applicable
- Automation location: Implementation test suite, location selected during implementation.
- Required by milestone: not applicable

### T4. Fail closed for every unknown mode

- Covers: R1, R4, EC3, example.unknown.failure, mode.vocabulary, unknown.outcome, interaction.unknown.result
- Level: unit
- Command IDs: none
- Fixture/setup: A property-based or equivalent exhaustive domain partition constrained to mode values unequal to the exact literals `trim` and `preserve`.
- Steps: For each generated or enumerated unknown mode, invoke the normalizer with representative text and inspect both the failure and text-result channels.
- Expected result: Every invocation fails with `unknown-mode` and returns no text.
- Failure proves: An additional mode is accepted, the wrong failure is produced, or any text accompanies an unknown-mode result.
- Evidence artifact: not applicable
- Automation location: Implementation test suite, location selected during implementation.
- Required by milestone: not applicable

## Fixtures and data

The Unicode fixture is the explicit 25-code-point table in T2. Mode fixtures contain the two exact accepted literals and a generated or enumerated complement for the implementation's mode domain. Text fixtures remain within the input-text contract and do not prescribe transport or representation.

## Mocking/stubbing policy

No mocks or stubs are needed. Tests exercise the normalizer contract directly.

## Validation commands

No validation commands are part of this proof map because no repository command surface was supplied and command selection is implementation-owned.

## Milestone proof map

Not applicable because no approved execution plan, staged validation, or implementation milestone was supplied.

## Migration or compatibility tests

Not applicable; the specification defines no compatibility or migration behavior.

## Observability verification

Not applicable; the observable contract is fully asserted through returned text and failure outcomes.

## Security/privacy verification

Not applicable; the specification defines no security or privacy behavior.

## Performance checks

Not applicable; performance is explicitly out of scope.

## Manual QA checklist

Not applicable; every proof obligation is automated.

## What not to test and why

Do not test input shape, transport, storage, logging, performance, implementation strategy, or APIs not present in the approved specification. Missing-mode representation is excluded because input-shape behavior is a non-goal. Identity freshness, authorization, mutation, recovery, concurrency, migration, and evidence claims are excluded because their governing boundary dimensions are not applicable.

## Uncovered gaps

None. Every applicable boundary and every selected interaction has direct automated proof, and R1 through R4 are collectively covered exactly within the approved behavior contract.

## Next artifacts

Submit this draft to `test-spec-review`.

## Follow-on artifacts

None yet

## Readiness

Ready for `test-spec-review`; implementation, verification, and branch-readiness claims remain out of scope.
