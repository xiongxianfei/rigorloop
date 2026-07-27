Boundary model version: v1
Boundary model scope: R1-R4

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| proof.mode.vocabulary | R1, R4 | mode.vocabulary | T1, T4 | automated | - |
| proof.text.transformation | R2, R3 | text.transformation | T2, T3 | automated | - |
| proof.outcome.unknown-mode | R4 | outcome.unknown-mode | T4 | automated | - |
| proof.interaction.accepted-mode-transform | R1, R2, R3 | interaction.accepted-mode-transform | T1, T2, T3 | automated | - |
| proof.interaction.unknown-mode-outcome | R4 | interaction.unknown-mode-outcome | T4 | automated | - |

## Test cases

### T1. Accept exactly the closed mode vocabulary

- Covers: R1
- Level: unit
- Command IDs: none
- Fixture/setup: Inputs using mode `trim` and mode `preserve`.
- Steps: Normalize representative text once with each mode.
- Expected result: Both modes are accepted and return text according to their transformations, as asserted fully by T2 and T3.
- Failure proves: An accepted mode is rejected or accepted-mode classification does not reach its required transformation.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T2. Trim every Unicode White_Space code point at boundaries and preserve it internally

- Covers: R2, example.trim.outer-whitespace, the all-White_Space input edge case, and the no-boundary-White_Space edge case
- Level: unit
- Command IDs: none
- Fixture/setup: Deterministically enumerate `U+0009`, `U+000A`, `U+000B`, `U+000C`, `U+000D`, `U+0020`, `U+0085`, `U+00A0`, `U+1680`, `U+2000`, `U+2001`, `U+2002`, `U+2003`, `U+2004`, `U+2005`, `U+2006`, `U+2007`, `U+2008`, `U+2009`, `U+200A`, `U+2028`, `U+2029`, `U+202F`, `U+205F`, and `U+3000` as the complete Unicode `White_Space` fixture; use retained non-whitespace anchors `A` and `B`.
- Steps: For each enumerated code point `W`, normalize `WA`, `AW`, `WAW`, and `AWB` in `trim` mode. Normalize an input formed solely from the complete fixture, an input with the complete fixture before and after `A`, an input with the complete fixture between `A` and `B`, and `AB`.
- Expected result: Each `WA`, `AW`, and `WAW` returns `A`; each `AWB` returns unchanged. The all-White_Space input returns empty text; the fixture surrounding `A` returns `A`; the fixture between `A` and `B` remains unchanged; and `AB` remains unchanged.
- Failure proves: `trim` fails to remove a Unicode `White_Space` code point at a text boundary, removes the same code point between retained non-whitespace code points, mishandles all-whitespace text, or changes text without boundary whitespace.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T3. Preserve input text unchanged

- Covers: R3, example.preserve.unchanged
- Level: unit
- Command IDs: none
- Fixture/setup: Representative text including `  hello  ` and text containing every code point in the T2 fixture at leading, internal, and trailing positions.
- Steps: Normalize each input in `preserve` mode.
- Expected result: Every returned text is code-point-for-code-point identical to its input.
- Failure proves: `preserve` changes the input or accepted-mode classification reaches the wrong transformation.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T4. Reject every unknown mode with no text

- Covers: R1, R4, example.mode.unknown, and the unknown-mode-regardless-of-input edge case
- Level: unit
- Command IDs: none
- Fixture/setup: Quantify over every mode value other than `trim` and `preserve`; include `other` and vary the input across ordinary, empty, and Unicode-White_Space text.
- Steps: Attempt normalization for each unknown mode and input.
- Expected result: Every attempt fails with `unknown-mode` and returns no text.
- Failure proves: A value outside the closed vocabulary is accepted, an unknown mode produces a different outcome, text is returned on failure, or input text changes the required stop outcome.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable
