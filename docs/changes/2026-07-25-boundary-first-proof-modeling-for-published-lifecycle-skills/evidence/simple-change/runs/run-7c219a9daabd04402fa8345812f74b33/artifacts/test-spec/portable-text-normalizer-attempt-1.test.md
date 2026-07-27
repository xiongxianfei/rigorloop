# Portable text normalizer test specification

## Status

draft

## Related spec and plan

- Spec: Portable text normalizer approved by `spec-review-r1`
- Plan: Not supplied
- Architecture/ADRs: Not applicable; the approved review records architecture as not required

## Input artifact identities

| Input | Path | Status / Review state | Identity |
| --- | --- | --- | --- |
| Feature spec | Attached authoritative stage input | approved | `sha256:4ce06ce616f93f1c7eaab789f7f1af40110f0df7d05d7eebdda7ab5b757ca5f1` |
| Spec review | `reviews/spec-review.md` | approved and recorded | `spec-review-r1` |
| Plan | - | not supplied | - |
| Plan review | - | not supplied | - |
| Architecture/ADRs | - | not applicable | Architecture not required by approved review |

## Testing strategy

Use automated contract tests against the normalizer's public behavior. Cover both accepted modes, Unicode trimming partitions, exact preservation, generated unknown modes, and the composed mode-to-outcome interaction. Integration, end-to-end, smoke, migration, and manual testing are not required by the approved contract.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T1, T4, T5, T6 | contract | Proves the two accepted modes and rejection of every generated value outside the closed vocabulary. |
| R2 | T1, T2, T3, T6 | contract | Covers bounded Unicode whitespace, all-whitespace input, and input requiring no trimming. |
| R3 | T4, T6 | contract | Proves byte-for-byte-equivalent text preservation for generated input text. |
| R4 | T5, T6 | contract | Proves `unknown-mode` and absence of returned text for generated unknown modes. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| example.trim | T1 | Covers leading and trailing Unicode whitespace removal. |
| example.preserve | T4 | Covers unchanged returned text. |
| example.unknown | T5 | Covers the required failure and absence of text. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 | T2 | Input consists entirely of Unicode whitespace. |
| EC2 | T3 | Input has no leading or trailing Unicode whitespace. |
| EC3 | T5, T6 | Generated modes exclude exactly `trim` and `preserve`. |

Boundary model version: v1
Boundary model scope: R1-R4

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| proof.mode-selection | R1 | mode.selection | T1, T4, T5 | automated | - |
| proof.text-trim | R2 | text.trim | T1, T2, T3 | automated | - |
| proof.text-preserve | R3 | text.preserve | T4 | automated | - |
| proof.mode-unknown | R4 | mode.unknown | T5 | automated | - |
| proof.mode-outcome | R1, R2, R3, R4 | interaction.mode-outcome | T6 | automated | - |

## Test cases

### T1. Trim leading and trailing Unicode whitespace

- Covers: R1, R2, example.trim
- Level: unit
- Command IDs: none
- Fixture/setup: Input text containing non-whitespace content bounded by representative Unicode whitespace characters; mode `trim`.
- Steps: Invoke the normalizer with the fixture.
- Expected result: The returned text contains the original interior content with all leading and trailing Unicode whitespace removed.
- Failure proves: The accepted `trim` mode or its required transformation is incorrect.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T2. Trim all-whitespace input

- Covers: R2, EC1
- Level: unit
- Command IDs: none
- Fixture/setup: Input text consisting entirely of representative Unicode whitespace characters; mode `trim`.
- Steps: Invoke the normalizer with the fixture.
- Expected result: The returned text is empty.
- Failure proves: The trim transformation does not correctly handle all-whitespace input.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T3. Preserve already-trimmed content in trim mode

- Covers: R2, EC2
- Level: unit
- Command IDs: none
- Fixture/setup: Input text with no leading or trailing Unicode whitespace; mode `trim`.
- Steps: Invoke the normalizer with the fixture.
- Expected result: The returned text equals the input text.
- Failure proves: Trim mode modifies text outside the required leading and trailing whitespace removal.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T4. Preserve arbitrary input text

- Covers: R1, R3, example.preserve
- Level: unit
- Command IDs: none
- Fixture/setup: Generated input text, including empty text and text containing Unicode whitespace; mode `preserve`.
- Steps: Invoke the normalizer for each generated input.
- Expected result: Each returned text equals its corresponding input text unchanged.
- Failure proves: The accepted `preserve` mode changes input text.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T5. Reject every generated unknown mode

- Covers: R1, R4, example.unknown, EC3
- Level: unit
- Command IDs: none
- Fixture/setup: Generated mode values constrained to exclude exactly `trim` and `preserve`, with arbitrary input text.
- Steps: Invoke the normalizer for each generated unknown mode.
- Expected result: Every invocation fails with `unknown-mode` and returns no text.
- Failure proves: The closed vocabulary or unknown-mode stop outcome is violated.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T6. Compose mode selection with its exclusive outcome

- Covers: R1, R2, R3, R4, interaction.mode-outcome
- Level: unit
- Command IDs: none
- Fixture/setup: Cases for `trim` with bounded Unicode whitespace, `preserve` with the same input, and generated modes excluding both accepted values.
- Steps: Invoke the normalizer for each case and inspect the complete observable result.
- Expected result: `trim` returns only the trimmed text, `preserve` returns only unchanged text, and every generated unknown mode returns only `unknown-mode` failure with no text.
- Failure proves: Mode classification does not compose with exactly one requirement-owned outcome.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

## Validation commands

No validation commands are part of this proof map because no repository test command or implementation location was supplied.

## Milestone proof map

Not applicable because no approved execution plan or milestones were supplied.

## Fixtures and data

Use representative Unicode whitespace fixtures for bounded examples and generators for arbitrary text and modes outside the two-value vocabulary. No transport or input-shape fixtures are included.

## Mocking/stubbing policy

No mocks or stubs are required; tests exercise the observable normalizer contract directly.

## Migration or compatibility tests

Not applicable; the specification defines no migration or compatibility behavior.

## Observability verification

Not applicable; the specification defines no observability behavior.

## Security/privacy verification

Not applicable; the specification defines no security or privacy behavior.

## Performance checks

Not applicable; the specification defines no performance behavior.

## Manual QA checklist

Not applicable; every proof obligation is automated.

## What not to test and why

Input shape, transport, storage, logging, implementation structure, performance, and user-interface behavior are excluded because the approved specification identifies them as non-goals or not applicable.

## Uncovered gaps

An approved execution plan, plan review, validation commands, automation locations, and milestone mapping were not supplied. These workflow inputs must be added before implementation handoff.

## Next artifacts

Supply and approve the execution plan, settle command and milestone mappings, then perform `test-spec-review`.

## Follow-on artifacts

None yet.

## Readiness

The boundary-first proof record is complete for R1-R4, all applicable boundaries, and `interaction.mode-outcome`. The test specification is not ready for implementation or final `test-spec-review` handoff until the required approved plan context is supplied.
