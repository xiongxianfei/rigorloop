Boundary model version: v1
Boundary model scope: R1-R4

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| proof.mode.vocabulary | R1, R4 | boundary.mode.vocabulary | T1, T5 | automated | - |
| proof.text.transformation | R2, R3 | boundary.text.transformation | T2, T3, T4 | automated | - |
| proof.unknown.outcome | R4 | boundary.unknown.outcome | T5 | automated | - |
| proof.whitespace.authority | R2 | boundary.whitespace.authority | T2, T3, T6 | automated | - |
| proof.mode.result | R1, R2, R3, R4 | interaction.mode.result | T1, T2, T4, T5 | automated | - |
| proof.whitespace.trim | R2 | interaction.whitespace.trim | T2, T3, T6 | automated | - |

## Test cases

### T1. Accept the closed mode vocabulary

- Covers: R1
- Level: unit
- Command IDs: none
- Fixture/setup: Inputs using modes `trim` and `preserve`.
- Steps: Normalize one text value once with each mode.
- Expected result: Both modes are accepted and return successful text results.
- Failure proves: The accepted mode vocabulary is not exactly usable as specified.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T2. Trim every Unicode White_Space code point at both boundaries

- Covers: R2, EC1, example.trim.whitespace
- Level: unit
- Command IDs: none
- Fixture/setup: Deterministically enumerate `U+0009` through `U+000D`, `U+0020`, `U+0085`, `U+00A0`, `U+1680`, `U+2000` through `U+200A`, `U+2028`, `U+2029`, `U+202F`, `U+205F`, and `U+3000`; use retained non-whitespace sentinels `A` and `B`.
- Steps: For each enumerated code point `W`, normalize `WAB`, `ABW`, and `WABW` in `trim` mode; also normalize text consisting only of `W`.
- Expected result: Each boundary `W` is removed, `AB` is retained, and an all-`W` input returns empty text.
- Failure proves: At least one Unicode `White_Space` member is not removed at a leading or trailing boundary.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T3. Preserve every Unicode White_Space code point internally during trim

- Covers: R2, EC2
- Level: unit
- Command IDs: none
- Fixture/setup: Use the complete deterministic enumeration from T2 and retained non-whitespace sentinels `A` and `B`.
- Steps: For each enumerated code point `W`, normalize `AWB` in `trim` mode.
- Expected result: The result is exactly `AWB`; the same `W` code point remains between the retained sentinels.
- Failure proves: Trim removes or changes Unicode `White_Space` outside leading and trailing positions.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T4. Preserve input text exactly

- Covers: R3, EC3, example.preserve.unchanged
- Level: unit
- Command IDs: none
- Fixture/setup: Empty text, ordinary text, and text containing the complete Unicode `White_Space` enumeration from T2 at boundary and internal positions.
- Steps: Normalize each fixture in `preserve` mode and compare the returned text code point for code point with its input.
- Expected result: Every returned text is identical to its input, including empty text and all whitespace positions.
- Failure proves: Preserve mode changes the input text.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T5. Reject every unknown mode without text

- Covers: R1, R4, EC4, example.unknown.failure
- Level: unit
- Command IDs: none
- Fixture/setup: Generate mode values excluding exactly `trim` and `preserve`, including `fold`.
- Steps: Attempt normalization of `hello` with each generated unknown mode.
- Expected result: Every attempt returns `unknown-mode` and contains no text.
- Failure proves: An unknown mode is accepted, yields the wrong failure, or leaks a text result.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T6. Retain boundary code points outside Unicode White_Space

- Covers: R2
- Level: unit
- Command IDs: none
- Fixture/setup: Code points immediately adjacent to the enumerated White_Space ranges but not members of the property, paired with retained sentinel `A`.
- Steps: Normalize each non-member before and after `A` in `trim` mode.
- Expected result: Every non-member boundary code point is retained unchanged.
- Failure proves: Trim uses a removal set broader than Unicode `White_Space`.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable
