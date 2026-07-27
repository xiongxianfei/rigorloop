Boundary model version: v1
Boundary model scope: R1-R4

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| proof.mode.selection | R1, R4 | boundary.mode.selection | T1, T2, T3, T4 | automated | - |
| proof.text.output | R2, R3 | boundary.text.output | T1, T2, T3 | automated | - |
| proof.unknown.stop | R4 | boundary.unknown.stop | T4 | automated | - |
| proof.mode.output | R1, R2, R3 | interaction.mode.output | T1, T2, T3 | automated | - |
| proof.interaction.unknown-stop | R4 | interaction.unknown.stop | T4 | automated | - |

## Test cases

### T1. Trim surrounding Unicode whitespace

- Covers: R1, R2, example.trim.whitespace, interaction.mode.output
- Level: unit
- Command IDs: none
- Fixture/setup: Text containing leading and trailing characters with the Unicode `White_Space` property, plus non-whitespace content.
- Steps: Normalize the text using mode `trim`.
- Expected result: The returned text excludes all leading and trailing Unicode whitespace and retains the content.
- Failure proves: The accepted `trim` mode or its required output transformation is incorrect.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T2. Trim Unicode-whitespace-only text

- Covers: R1, R2, edge.trim.empty, interaction.mode.output
- Level: unit
- Command IDs: none
- Fixture/setup: Text containing only characters with the Unicode `White_Space` property.
- Steps: Normalize the text using mode `trim`.
- Expected result: The returned text is empty.
- Failure proves: The `trim` boundary does not correctly handle input with no non-whitespace characters.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T3. Preserve text exactly

- Covers: R1, R3, example.preserve.whitespace, edge.preserve.empty, interaction.mode.output
- Level: unit
- Command IDs: none
- Fixture/setup: A table of inputs including empty text and text with leading and trailing Unicode whitespace.
- Steps: Normalize each input using mode `preserve`.
- Expected result: Each returned text is exactly equal to its input text.
- Failure proves: The accepted `preserve` mode changes text or mishandles empty input.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T4. Reject every unknown mode without text

- Covers: R1, R4, example.unknown.mode, edge.mode.unknown, interaction.unknown.stop
- Level: unit
- Command IDs: none
- Fixture/setup: Generate or enumerate mode values outside the closed set `trim` and `preserve`.
- Steps: Request normalization with each unknown mode and arbitrary input text.
- Expected result: Every request fails with `unknown-mode` and contains no normalized text value.
- Failure proves: The mode vocabulary is not closed or an unknown mode bypasses the required stop outcome.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable
