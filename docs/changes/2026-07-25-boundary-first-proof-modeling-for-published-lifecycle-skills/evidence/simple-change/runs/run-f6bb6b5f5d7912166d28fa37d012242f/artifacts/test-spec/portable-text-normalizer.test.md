# Portable text normalizer proof map

Boundary model version: v1
Boundary model scope: R1-R4

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| proof.mode-closed-values | R1, R4 | mode.closed-values | T1, T2, T3 | automated | - |
| proof.normalization-results | R2, R3, R4 | outcome.normalization-results | T1, T2, T3 | automated | - |
| proof.mode-outcome | R1, R2, R3, R4 | interaction.mode-outcome | T1, T2, T3 | automated | - |

## Test cases

### T1. Trim mode removes surrounding Unicode whitespace

- Covers: R1, R2, example.trim-whitespace, EC1, EC2, EC3
- Level: unit
- Command IDs: none
- Fixture/setup: Inputs containing leading and trailing Unicode whitespace, only Unicode whitespace, no surrounding Unicode whitespace, and empty text; mode is exactly `trim`.
- Steps: Normalize each input in `trim` mode.
- Expected result: The mode is accepted; all leading and trailing Unicode whitespace is removed, interior content is preserved, whitespace-only input becomes empty text, and input without surrounding whitespace or empty input remains unchanged.
- Failure proves: The closed accepted-mode contract or trim outcome is violated.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T2. Preserve mode returns text unchanged

- Covers: R1, R3, example.preserve-text, EC3
- Level: unit
- Command IDs: none
- Fixture/setup: Representative text including surrounding Unicode whitespace and empty text; mode is exactly `preserve`.
- Steps: Normalize each input in `preserve` mode.
- Expected result: The mode is accepted and the returned text is exactly the input text.
- Failure proves: The closed accepted-mode contract or preserve outcome is violated.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T3. Every unknown mode fails without text

- Covers: R1, R4, example.reject-unknown, EC4
- Level: unit
- Command IDs: none
- Fixture/setup: Parameterize over every supported mode value other than exact `trim` and `preserve`, including unknown values that differ by case or content where those values are representable.
- Steps: Request normalization for each unknown mode with representative input text.
- Expected result: Every request fails with `unknown-mode` and returns no text.
- Failure proves: An unknown mode was accepted, produced the wrong failure, or returned text.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

## Status

draft

## Related spec and plan

- Spec: Portable text normalizer authoritative stage input
- Plan: Not applicable; no execution plan or milestones are part of the supplied stage input.
- Architecture/ADRs: not applicable

## Input artifact identities

| Input | Path | Status / Review state | Identity |
| --- | --- | --- | --- |
| Feature spec | Authoritative stage input | draft with approved formal review | sha256:8574c215aa6074cb967947c16f1a5a984131cddb3d78525c9a37eab09715e7ca |
| Spec review | Approved formal review | approved; no material findings | spec-review-r1 |
| Plan | - | not supplied; not applicable to this proof-map-only request | - |
| Architecture/ADRs | - | not applicable | - |

## Testing strategy

Use automated unit tests for the complete mode-to-outcome contract. No integration, end-to-end, smoke, manual, migration, or compatibility proof is required by R1-R4.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T1, T2, T3 | unit | Proves both exact accepted modes and rejection of every other mode. |
| R2 | T1 | unit | Proves trimming across the specified edge cases. |
| R3 | T2 | unit | Proves exact preservation, including empty text. |
| R4 | T3 | unit | Proves `unknown-mode` with no returned text for every unknown mode. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| example.trim-whitespace | T1 | Direct illustration coverage. |
| example.preserve-text | T2 | Direct illustration coverage. |
| example.reject-unknown | T3 | Direct illustration coverage. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 | T1 | Unicode-whitespace-only input becomes empty text in `trim` mode. |
| EC2 | T1 | Text without surrounding Unicode whitespace remains unchanged in `trim` mode. |
| EC3 | T1, T2 | Empty input is covered in both accepted modes. |
| EC4 | T3 | Every mode other than exact `trim` and `preserve` is rejected. |

## Validation commands

No validation commands are part of this proof map because the authoritative inputs identify no repository test command or implementation location.

## Milestone proof map

Not applicable because no approved execution-plan milestones or staged validation gates were supplied.

## Fixtures and data

Use table-driven Unicode text fixtures for surrounding whitespace, whitespace-only text, unchanged text, and empty text. Use a parameterized unknown-mode set spanning every mode value supported by the implementation except exact `trim` and `preserve`.

## Mocking/stubbing policy

No mocks or stubs are required; assert normalization results directly.

## Migration or compatibility tests

Not applicable; the feature specification defines no compatibility or migration behavior.

## Observability verification

Assert only the returned text or `unknown-mode` failure. Logging and telemetry are outside the contract.

## Security/privacy verification

Not applicable; no security or privacy behavior is specified.

## Performance checks

Not applicable; no performance contract is specified.

## Manual QA checklist

Not applicable; the complete R1-R4 proof is automated.

## What not to test and why

Do not test input shape, transport, storage, logging, performance, implementation structure, missing-mode behavior, or additional fields because the feature specification explicitly leaves those concerns outside R1-R4.

## Uncovered gaps

None within R1-R4.

## Next artifacts

Independent test-spec review.

## Follow-on artifacts

None yet.

## Readiness

Ready for test-spec-review; implementation, verification, and later lifecycle stages have not been performed.
