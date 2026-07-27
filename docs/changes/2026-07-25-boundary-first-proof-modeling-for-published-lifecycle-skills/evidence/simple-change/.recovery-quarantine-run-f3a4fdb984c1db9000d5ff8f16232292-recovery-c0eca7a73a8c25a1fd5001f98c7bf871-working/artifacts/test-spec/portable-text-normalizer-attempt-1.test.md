Boundary model version: v1
Boundary model scope: R1-R4

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| proof.mode-vocabulary | R1, R4 | mode.vocabulary | T1, T2, T3 | automated | - |
| proof.text-transformation | R2, R3 | text.transformation | T1, T2 | automated | - |
| proof.unknown-mode-outcome | R4 | outcome.unknown-mode | T3 | automated | - |
| proof.unknown-mode-stop | R1, R4 | interaction.unknown-mode-stop | T3 | automated | - |

## Test cases

### T1. Trim Unicode whitespace

- Covers: R1, R2, example.trim-whitespace, EC1, EC2
- Level: unit
- Command IDs: none
- Fixture/setup: Generate Unicode text with leading and trailing code points from the Unicode `White_Space` property, including whitespace-only text and text containing internal non-whitespace code points.
- Steps: Normalize each input using mode `trim`.
- Expected result: The returned text has every leading and trailing Unicode `White_Space` code point removed; internal non-whitespace code points remain.
- Failure proves: The accepted `trim` mode or its required transformation does not satisfy R1 or R2.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T2. Preserve text unchanged

- Covers: R1, R3, example.preserve-text, EC3
- Level: unit
- Command IDs: none
- Fixture/setup: Generate Unicode input text, including empty text and text with leading and trailing Unicode `White_Space` code points.
- Steps: Normalize each input using mode `preserve`.
- Expected result: The returned text is exactly unchanged.
- Failure proves: The accepted `preserve` mode or its required transformation does not satisfy R1 or R3.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T3. Reject every unknown mode without text

- Covers: R1, R4, example.unknown-mode, EC4
- Level: unit
- Command IDs: none
- Fixture/setup: Generate mode values outside the closed set `trim` and `preserve`, with arbitrary input text.
- Steps: Request normalization for each generated unknown mode.
- Expected result: Every request fails with `unknown-mode` and returns no text.
- Failure proves: The mode vocabulary is not closed, the unknown-mode outcome is incorrect, or classification of an unknown mode does not stop text production.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable
