# Portable text normalizer test specification

Boundary model version: v1
Boundary model scope: R1-R4

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| proof.mode.selection | R1, R4 | boundary.mode.selection | T1, T3, T4 | automated | - |
| proof.text.transformation | R2, R3 | boundary.text.transformation | T1, T2, T3 | automated | - |
| proof.unknown.outcome | R4 | boundary.unknown.outcome | T4 | automated | - |
| proof.mode.result | R1, R2, R3, R4 | interaction.mode.result | T1, T2, T3, T4 | automated | - |

## Test cases

### T1. Trim removes surrounding Unicode whitespace

- Covers: R1, R2, example.trim.whitespace
- Level: unit
- Command IDs: none
- Fixture/setup: Input text containing non-whitespace text with leading and trailing Unicode whitespace; mode `trim`.
- Steps: Normalize the input and inspect the returned text.
- Expected result: The result contains the non-whitespace text without the surrounding Unicode whitespace.
- Failure proves: The recognized `trim` mode or its required transformation is incorrect.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T2. Trim handles Unicode-whitespace-only input

- Covers: R2, EC1
- Level: unit
- Command IDs: none
- Fixture/setup: Inputs containing only Unicode whitespace, including coverage of the applicable Unicode whitespace classification; mode `trim`.
- Steps: Normalize each input and inspect the returned text.
- Expected result: Each result contains no remaining text.
- Failure proves: Leading or trailing Unicode whitespace is not removed as required.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T3. Preserve returns text exactly unchanged

- Covers: R1, R3, example.preserve.unchanged, EC2
- Level: unit
- Command IDs: none
- Fixture/setup: Inputs including empty text, ordinary text, and text with leading and trailing Unicode whitespace; mode `preserve`.
- Steps: Normalize each input and compare the returned text with the corresponding input.
- Expected result: Every returned text is exactly equal to its input.
- Failure proves: The recognized `preserve` mode changes text or produces the wrong outcome.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T4. Every unknown mode fails closed

- Covers: R1, R4, example.unknown.rejected, EC3
- Level: unit
- Command IDs: none
- Fixture/setup: A parameterized or property-based set of supplied mode values excluding exactly `trim` and `preserve`, including otherwise similar values.
- Steps: Request normalization for each unknown mode and inspect both the outcome and text field.
- Expected result: Every request produces `unknown-mode` and returns no text.
- Failure proves: The accepted vocabulary is not closed or an unknown mode produces text or another outcome.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

## Status

draft

## Related spec and plan

- Spec: Portable text normalizer authoritative stage input
- Plan: not applicable; no execution milestones or implementation surfaces are part of the supplied stage input
- Architecture/ADRs: not applicable

## Input artifact identities

| Input | Path | Status / Review state | Identity |
| --- | --- | --- | --- |
| Feature spec | authoritative stage input | approved by formal review | sha256:54db01670ea8d00baccd90062401c816e65e1750aad998a6fd8456656f015f1a |
| Spec review | reviews/spec-review.md | approved and recorded | spec-review-r1 |
| Plan | not applicable | not supplied; no milestones govern this proof map | - |
| Plan review | not applicable | not applicable | - |
| Architecture or ADR | not applicable | not required by the supplied contract | - |

## Testing strategy

Use automated unit-level contract tests for recognized modes, Unicode-whitespace transformation, exact preservation, and closed unknown-mode failure. Integration, end-to-end, smoke, manual, and migration testing are not required because the specification defines no transport, wiring, user interface, deployment, or compatibility behavior.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T1, T3, T4 | contract | Proves both recognized modes and rejection outside the closed set. |
| R2 | T1, T2 | unit | Covers surrounding whitespace and whitespace-only input. |
| R3 | T3 | unit | Uses exact input-to-output comparison. |
| R4 | T4 | contract | Asserts both `unknown-mode` and absence of returned text. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| example.trim.whitespace | T1 | Directly exercises the illustrated trim result. |
| example.preserve.unchanged | T3 | Directly exercises unchanged preservation. |
| example.unknown.rejected | T4 | Directly exercises closed unknown-mode failure. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 | T2 | Unicode-whitespace-only inputs produce no remaining text. |
| EC2 | T3 | Surrounding Unicode whitespace remains unchanged in `preserve` mode. |
| EC3 | T4 | Otherwise similar and other values outside the closed set fail identically. |

## Validation commands

No validation commands are part of this proof map because no repository, test runner, manifest, or execution plan was supplied. Command ownership must be recorded without changing these proof obligations when an implementation surface exists.

## Milestone proof map

Not applicable because the supplied stage input defines no execution milestones, staged commands, or milestone-specific review boundaries.

## Fixtures and data

Use text fixtures for ordinary text, empty text, surrounding Unicode whitespace, Unicode-whitespace-only text, and unchanged preservation. Use generated or parameterized mode values outside exactly `trim` and `preserve` for the unknown-mode partition.

## Mocking/stubbing policy

No mocks or stubs are needed; assert the normalizer's observable result directly.

## Migration or compatibility tests

Not applicable; the specification defines no prior representation or migration behavior.

## Observability verification

Not applicable; the observable contract is limited to returned text or `unknown-mode` with no text.

## Security/privacy verification

Not applicable; no security or privacy behavior is specified.

## Performance checks

Not applicable; no performance contract is specified.

## Manual QA checklist

Not applicable; all specified behavior is directly automatable.

## What not to test and why

Do not test input shape, transport, storage, logging, implementation technique, performance, authorization, user interface behavior, or migration because each is outside the approved specification.

## Uncovered gaps

None within R1-R4. Repository-specific command and automation paths remain intentionally unset until an implementation surface is supplied.

## Next artifacts

Independent test-spec review.

## Follow-on artifacts

None yet.

## Readiness

Ready for test-spec-review as a complete boundary-first proof map for R1-R4; it does not authorize implementation or claim executed evidence.
