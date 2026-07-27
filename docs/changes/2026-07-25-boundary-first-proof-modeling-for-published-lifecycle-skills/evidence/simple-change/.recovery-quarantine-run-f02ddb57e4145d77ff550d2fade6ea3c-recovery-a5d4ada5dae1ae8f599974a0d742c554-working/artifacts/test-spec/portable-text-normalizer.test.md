Boundary model version: v1
Boundary model scope: R1-R4

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| proof.mode.vocabulary | R1, R4 | mode.closed-vocabulary | T1, T2, T3 | automated | - |
| proof.text.transformation | R2, R3 | text.mode-transformation | T1, T2 | automated | - |
| proof.unknown.outcome | R4 | outcome.unknown-mode | T3 | automated | - |
| proof.mode.transformation | R1, R2, R3 | interaction.mode.transformation | T1, T2 | automated | - |
| proof.mode.stop | R1, R4 | interaction.mode.stop | T3 | automated | - |

## Test cases

### T1. Trim mode removes Unicode whitespace only at text boundaries

- Covers: R1, R2, example.trim.whitespace, mode.closed-vocabulary, text.mode-transformation, interaction.mode.transformation
- Level: unit
- Command IDs: none
- Fixture/setup: Text cases covering each code point with the Unicode `White_Space` property at leading and trailing positions, mixed boundary whitespace, whitespace-only text, text without boundary whitespace, and text containing interior whitespace.
- Steps: Normalize every fixture using the exact mode `trim`.
- Expected result: The mode is accepted; the maximal leading and trailing sequences of Unicode whitespace are removed, and the remaining text is returned.
- Failure proves: The accepted-mode vocabulary, Unicode whitespace classification, boundary removal, or mode-to-transformation composition violates R1 or R2.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T2. Preserve mode returns text unchanged

- Covers: R1, R3, example.preserve.unchanged, mode.closed-vocabulary, text.mode-transformation, interaction.mode.transformation
- Level: unit
- Command IDs: none
- Fixture/setup: Empty text and varied text containing Unicode whitespace at boundaries and internally, non-whitespace Unicode code points, and line breaks.
- Steps: Normalize every fixture using the exact mode `preserve` and compare the returned text with the input text.
- Expected result: The mode is accepted and every returned text is exactly equal to its input.
- Failure proves: The accepted-mode vocabulary, unchanged-text outcome, or mode-to-transformation composition violates R1 or R3.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T3. Every unknown mode fails closed without text

- Covers: R1, R4, example.mode.unknown, mode.closed-vocabulary, outcome.unknown-mode, interaction.mode.stop
- Level: unit
- Command IDs: none
- Fixture/setup: Generated supplied mode values excluding exact `trim` and `preserve`, including empty, case-varied, prefixed, suffixed, and unrelated values supported by the eventual input harness; pair each with representative text.
- Steps: Normalize the text with each generated unknown mode and inspect both the failure and returned-text outcome.
- Expected result: Every case fails with `unknown-mode` and returns no text.
- Failure proves: The closed vocabulary, unknown-mode outcome, or composed stop behavior violates R1 or R4.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable
