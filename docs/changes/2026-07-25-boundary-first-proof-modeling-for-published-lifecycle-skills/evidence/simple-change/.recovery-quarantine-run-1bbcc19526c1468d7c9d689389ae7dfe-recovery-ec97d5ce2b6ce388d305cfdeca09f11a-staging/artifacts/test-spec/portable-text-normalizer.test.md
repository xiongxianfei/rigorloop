Boundary model version: v1
Boundary model scope: R1-R4

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| proof.mode.vocabulary | R1, R4 | boundary.mode.vocabulary | T1, T2, T3 | automated | - |
| proof.text.transformation | R2, R3 | boundary.text.transformation | T1, T2 | automated | - |
| proof.unknown.outcome | R4 | boundary.unknown.outcome | T3 | automated | - |
| proof.mode.failure | R4 | interaction.mode.failure | T3 | automated | - |
| proof.mode.transformation | R1, R2, R3 | interaction.mode.transformation | T1, T2 | automated | - |

## Test cases

### T1. Trim mode accepts and trims text

- Covers: R1, R2, example.trim.whitespace; valid mode, leading Unicode whitespace, trailing Unicode whitespace, no surrounding whitespace, empty text, and Unicode-whitespace-only text
- Level: unit
- Command IDs: none
- Fixture/setup: Provide representative text values for each listed partition and select `trim` mode.
- Steps: Normalize each text value in `trim` mode.
- Expected result: Each call succeeds; leading and trailing Unicode whitespace is removed, interior content is preserved, and Unicode-whitespace-only text returns empty text.
- Failure proves: The accepted-mode vocabulary, trim transformation, or their composed path violates R1 or R2.
- Evidence artifact: not applicable
- Automation location: implementation-owned unit-test suite
- Required by milestone: not applicable

### T2. Preserve mode accepts and returns text unchanged

- Covers: R1, R3, example.preserve.unchanged; valid mode, empty text, and text with leading, trailing, interior, or Unicode whitespace
- Level: unit
- Command IDs: none
- Fixture/setup: Provide representative text values for each listed partition and select `preserve` mode.
- Steps: Normalize each text value in `preserve` mode.
- Expected result: Each call succeeds and returns its input text unchanged.
- Failure proves: The accepted-mode vocabulary, preserve transformation, or their composed path violates R1 or R3.
- Evidence artifact: not applicable
- Automation location: implementation-owned unit-test suite
- Required by milestone: not applicable

### T3. Unknown modes fail without text

- Covers: R1, R4, example.unknown.failure; empty, case-substituted, near-match, additional, and arbitrary unknown mode values
- Level: unit
- Command IDs: none
- Fixture/setup: Provide representative modes other than exact `trim` and `preserve`, including empty text, `TRIM`, `Preserve`, `trim `, `preserve-extra`, and an unrelated Unicode value, together with arbitrary input text.
- Steps: Normalize the input text once with each unknown mode.
- Expected result: Every call fails with `unknown-mode` and returns no text.
- Failure proves: The closed vocabulary, unknown outcome, or mode-to-failure interaction violates R1 or R4.
- Evidence artifact: not applicable
- Automation location: implementation-owned unit-test suite
- Required by milestone: not applicable

# Portable text normalizer test specification

## Status

draft

## Related spec and plan

- Spec: Portable text normalizer specification supplied as the authoritative stage input
- Plan: not applicable; no execution plan or milestones are part of the authoritative stage input
- Architecture/ADRs: not applicable

## Input artifact identities

| Input | Path | Status / Review state | Identity |
| --- | --- | --- | --- |
| Feature specification | authoritative stage input | approved by formal review | sha256:354d11d847367cb14b3107a1fb34013faddf3e6248ae2dffb349fec37d045fbf |
| Spec review | reviews/spec-review.md | approved and recorded | spec-review-r2 |
| Execution plan | not applicable | not provided | Authoritative invocation limits this artifact to the test-spec stage without milestone planning. |
| Architecture/ADRs | not applicable | not required by the supplied feature contract | No architecture or ADR input was supplied. |

## Testing strategy

Use deterministic unit tests as the complete automated proof surface because the contract defines a pure input-to-result behavior and no transport, storage, public wiring, migration, or external system.
Contract coverage is expressed through the proof map and requirement coverage map.
Integration, end-to-end, smoke, and manual testing are not applicable to the specified boundary.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T1, T2, T3 | unit | Proves both accepted modes and representative partitions of every other mode as unknown. |
| R2 | T1 | unit | Proves leading and trailing Unicode-whitespace removal, including whitespace-only text. |
| R3 | T2 | unit | Proves unchanged returned text across representative content partitions. |
| R4 | T3 | unit | Proves `unknown-mode` and no returned text for representative unknown-mode partitions. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| example.trim.whitespace | T1 | Directly exercises trim-mode Unicode-whitespace behavior. |
| example.preserve.unchanged | T2 | Directly exercises unchanged preserve-mode behavior. |
| example.unknown.failure | T3 | Directly exercises unknown-mode failure with no text. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| Trim text containing only Unicode whitespace | T1 | Expected normalized result is empty text. |
| Trim text without surrounding Unicode whitespace | T1 | Expected content is preserved. |
| Preserve text with leading or trailing Unicode whitespace | T2 | Expected text is unchanged. |
| Empty text in either accepted mode | T1, T2 | Exercises transformation boundaries without adding input-shape behavior. |
| Case-substituted or near-match mode | T3 | Confirms the vocabulary accepts only exact closed values. |
| Empty, additional, or unrelated mode value | T3 | Confirms representative unknown partitions fail uniformly. |

## Validation commands

No validation commands are part of this proof map because the authoritative inputs specify neither a repository test runner nor an execution plan.
The implementation stage must bind T1-T3 to its configured test command without changing their assertions.

## Milestone proof map

Not applicable because the authoritative inputs contain no execution milestones, staged commands, or milestone-specific review boundaries.

## Fixtures and data

Use table-driven fixtures containing empty text, ordinary text, text with interior whitespace, text with leading and trailing Unicode whitespace, and Unicode-whitespace-only text.
Use exact accepted modes plus representative empty, substituted, near-match, additional, and unrelated unknown modes.

## Mocking/stubbing policy

No mocks or stubs are needed because the specified behavior has no external collaborators.

## Migration or compatibility tests

Not applicable; the specification defines no prior representation or migration behavior.

## Observability verification

The returned text or the `unknown-mode` failure with no text is asserted directly by T1-T3.
No logs, metrics, traces, or audit events are specified.

## Security/privacy verification

Not applicable; the specification defines no security or privacy behavior.

## Performance checks

Not applicable; the specification defines no performance contract.

## Manual QA checklist

Not applicable; all specified behavior is deterministically automatable.

## What not to test and why

Do not test input shape, transport, storage, logging, implementation structure, performance, compatibility, or migration because the approved specification identifies them as non-goals or not applicable.
Do not impose byte-level equivalence on preserve mode because R3 requires unchanged text without defining representation-level behavior.

## Uncovered gaps

None within R1-R4.
Repository-specific automation location and validation-command ownership remain implementation-plan concerns and do not alter the proof obligations.

## Next artifacts

Independent test-spec review of this proof map.

## Follow-on artifacts

None yet

## Readiness

Ready for test-spec-review; implementation and later lifecycle stages are outside this invocation.
