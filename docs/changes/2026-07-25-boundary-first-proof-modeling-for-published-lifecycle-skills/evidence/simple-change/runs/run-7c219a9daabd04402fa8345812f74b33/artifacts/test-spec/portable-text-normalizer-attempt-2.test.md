# Portable text normalizer test specification

## Status

draft

## Related spec and plan

- Spec: Portable text normalizer approved by `spec-review-r1`
- Plan: Not supplied; outside this isolated behavior-evidence review
- Architecture/ADRs: Not applicable

## Input artifact identities

| Input | Path | Status / Review state | Identity |
| --- | --- | --- | --- |
| Feature spec | Attached authoritative stage input | approved | `sha256:4ce06ce616f93f1c7eaab789f7f1af40110f0df7d05d7eebdda7ab5b757ca5f1` |
| Spec review | `reviews/spec-review.md` | approved and recorded | `spec-review-r1` |
| Test-spec review | `reviews/test-spec-review.md` | changes-requested | `test-spec-review-r1` |
| Plan | - | outside isolated scenario | - |
| Plan review | - | outside isolated scenario | - |
| Architecture/ADRs | - | not applicable | - |

## Testing strategy

Use automated contract tests against the normalizer's public behavior. Cover both accepted modes, every Unicode whitespace character at each R2 boundary partition, unchanged preservation, generated unknown modes, and the composed mode-to-outcome interaction. Integration, end-to-end, smoke, manual, and migration testing are not required by the approved contract.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T1, T4, T5, T6 | contract | Proves exactly the two accepted modes and rejection of generated values outside the closed vocabulary. |
| R2 | T1, T2, T3, T6 | contract | Covers every Unicode whitespace character at leading, trailing, combined, and all-whitespace partitions. |
| R3 | T4, T6 | contract | Proves unchanged text preservation for generated input text. |
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
| EC1 | T2 | Covers all-whitespace inputs across the complete Unicode whitespace fixture. |
| EC2 | T3 | Covers input with no leading or trailing Unicode whitespace. |
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

### T1. Trim every Unicode whitespace character at text boundaries

- Covers: R1, R2, example.trim
- Level: unit
- Command IDs: none
- Fixture/setup: Deterministically enumerate the complete Unicode `White_Space` property from the pinned Unicode Character Database fixture. For each enumerated character, construct leading-only, trailing-only, and combined-boundary inputs around fixed non-whitespace content.
- Steps: Invoke the normalizer in `trim` mode for every constructed input.
- Expected result: Every invocation returns only the fixed interior content, with all enumerated leading and trailing Unicode whitespace removed.
- Failure proves: The accepted `trim` mode fails to remove at least one Unicode whitespace character at a required boundary.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T2. Trim complete Unicode all-whitespace inputs

- Covers: R2, EC1
- Level: unit
- Command IDs: none
- Fixture/setup: Use the same complete pinned Unicode `White_Space` enumeration as T1; construct one input per character and one input containing the complete enumeration.
- Steps: Invoke the normalizer in `trim` mode for every constructed all-whitespace input.
- Expected result: Every invocation returns empty text.
- Failure proves: Trim mode fails for an all-whitespace input governed by R2.
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
- Failure proves: Trim mode modifies text outside the required boundary removal.
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
- Fixture/setup: Cases for `trim` using every character in the complete pinned Unicode `White_Space` enumeration at leading, trailing, combined, and all-whitespace boundaries; `preserve` using the same inputs; and generated modes excluding both accepted values.
- Steps: Invoke the normalizer for each case and inspect the complete observable result.
- Expected result: `trim` returns only the required trimmed text, `preserve` returns only unchanged text, and every generated unknown mode returns only `unknown-mode` failure with no text.
- Failure proves: Mode classification does not compose with exactly one requirement-owned outcome.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

## Validation commands

No validation commands are part of this proof map because no repository test command or implementation location was supplied.

## Milestone proof map

Not applicable because milestones are outside this isolated behavior-evidence scenario.

## Fixtures and data

Use a deterministic fixture generated from the complete Unicode Character Database `White_Space` property, with the Unicode data version pinned and the enumerated code-point inventory retained with the fixture. Use that inventory for every leading, trailing, combined-boundary, and all-whitespace R2 partition. Use generators for arbitrary text and modes outside the two-value vocabulary.

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

None within the isolated behavior-evidence review scope. No architecture, plan, plan-review, command, milestone, automation-location, or implementation authority is inferred.

## Next artifacts

Submit this substantive correction for a new isolated `test-spec-review` round.

## Follow-on artifacts

- `test-spec-review-r1`: changes requested; both recorded findings addressed by this revision.

## Readiness

The boundary-first proof record covers R1-R4, every applicable boundary, and `interaction.mode-outcome`. This revision is eligible for isolated behavior-evidence re-review. Implementation handoff remains not-allowed.
