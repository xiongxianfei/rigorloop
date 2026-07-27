Boundary model version: v1
Boundary model scope: R1-R4

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| proof.mode.vocabulary | R1 | boundary.mode.vocabulary | T1, T6 | automated | - |
| proof.trim.whitespace | R2 | boundary.trim.whitespace | T2, T3, T4 | automated | - |
| proof.preserve.unchanged | R3 | boundary.preserve.unchanged | T5 | automated | - |
| proof.unknown.outcome | R4 | boundary.unknown.outcome | T6 | automated | - |
| proof.mode.outcome | R1, R4 | interaction.mode.outcome | T1, T6 | automated | - |

## Test cases

### T1. Accept the complete closed mode vocabulary

- Covers: R1, interaction.mode.outcome
- Level: unit
- Command IDs: -
- Fixture/setup: Inputs using the exact modes `trim` and `preserve` with representative text.
- Steps: Normalize the text once with each mode.
- Expected result: Both modes are accepted; `trim` returns the R2 result and `preserve` returns the R3 result.
- Failure proves: A required member of the closed vocabulary is rejected or routed to the unknown-mode outcome.
- Evidence artifact: -
- Automation location: planned test implementation
- Required by milestone: -

### T2. Exhaustively classify Unicode White_Space positions in trim mode

- Covers: R2, example.trim.surrounding
- Level: unit
- Command IDs: -
- Fixture/setup: Deterministically enumerate `U+0009`, `U+000A`, `U+000B`, `U+000C`, `U+000D`, `U+0020`, `U+0085`, `U+00A0`, `U+1680`, `U+2000`, `U+2001`, `U+2002`, `U+2003`, `U+2004`, `U+2005`, `U+2006`, `U+2007`, `U+2008`, `U+2009`, `U+200A`, `U+2028`, `U+2029`, `U+202F`, `U+205F`, and `U+3000` as the Unicode `White_Space` property set governing the approved specification.
- Steps: For every enumerated code point `W`, normalize `W + A`, `A + W`, `W + A + W`, and `A + W + B` in `trim` mode, where `A` and `B` are retained non-whitespace code points.
- Expected result: The first three inputs return `A`; the fourth returns `A + W + B` unchanged, proving removal at both text boundaries and preservation of the same code point between retained non-whitespace code points.
- Failure proves: An enumerated Unicode whitespace code point is not removed at a text boundary or is incorrectly removed from the retained interior.
- Evidence artifact: -
- Automation location: planned parameterized test implementation
- Required by milestone: -

### T3. Trim input consisting entirely of Unicode whitespace

- Covers: R2, EC2
- Level: unit
- Command IDs: -
- Fixture/setup: For each code point enumerated by T2, construct a nonempty input containing only that code point, including a repeated instance.
- Steps: Normalize each input in `trim` mode.
- Expected result: Every input returns empty text.
- Failure proves: Trim retains leading or trailing Unicode whitespace when no non-whitespace text exists.
- Evidence artifact: -
- Automation location: planned parameterized test implementation
- Required by milestone: -

### T4. Preserve trim input with no boundary whitespace

- Covers: R2, EC1
- Level: unit
- Command IDs: -
- Fixture/setup: Text with no leading or trailing Unicode whitespace, including text containing interior Unicode whitespace.
- Steps: Normalize the text in `trim` mode.
- Expected result: The input text is returned unchanged.
- Failure proves: Trim alters retained text when no removable boundary whitespace is present.
- Evidence artifact: -
- Automation location: planned test implementation
- Required by milestone: -

### T5. Preserve every input unchanged

- Covers: R3, example.preserve.unchanged, EC3
- Level: unit
- Command IDs: -
- Fixture/setup: Parameterized text including empty text, non-whitespace text, all-whitespace text, boundary whitespace, interior whitespace, and mixed Unicode text.
- Steps: Normalize each input in `preserve` mode.
- Expected result: Every result is exactly code-point-for-code-point equal to its input.
- Failure proves: Preserve mode changes, removes, adds, or reorders input text.
- Evidence artifact: -
- Automation location: planned parameterized test implementation
- Required by milestone: -

### T6. Reject every mode outside the closed vocabulary with no text

- Covers: R1, R4, example.unknown.failure, EC4, interaction.mode.outcome
- Level: unit
- Command IDs: -
- Fixture/setup: Exercise the implementation's mode domain by partitioning all values other than exact `trim` and `preserve`; include case-substituted, whitespace-extended, empty, and unrelated values where those values belong to that domain.
- Steps: Request normalization for each unknown-mode partition with representative text that would otherwise expose a successful transformation.
- Expected result: Every request fails with exactly `unknown-mode` and returns no normalized text; no unknown value follows the trim or preserve outcome.
- Failure proves: The vocabulary is open, an unknown mode is accepted, the failure differs from `unknown-mode`, text accompanies failure, or mode classification and outcome handling do not compose correctly.
- Evidence artifact: -
- Automation location: planned parameterized test implementation
- Required by milestone: -
