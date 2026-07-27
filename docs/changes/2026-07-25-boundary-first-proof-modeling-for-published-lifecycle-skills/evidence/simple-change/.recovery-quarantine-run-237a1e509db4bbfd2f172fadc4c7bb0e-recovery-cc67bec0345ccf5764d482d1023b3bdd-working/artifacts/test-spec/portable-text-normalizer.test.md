Boundary model version: v1
Boundary model scope: R1-R4

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| p.trim.exhaustive-whitespace | R1, R2 | b.mode.behavior-path, b.mode.vocabulary, b.whitespace.authority, i.trim.authority | T1 | automated | - |
| p.preserve.unchanged | R1, R3 | b.mode.behavior-path, b.mode.vocabulary | T2 | automated | - |
| p.unknown.closed-outcome | R1, R4 | b.mode.behavior-path, b.mode.vocabulary, b.unknown.outcome | T3 | automated | - |
| p.mode.composed-outcomes | R1, R2, R3, R4 | i.mode.outcome | T1, T2, T3 | automated | - |

## Test cases

### T1. Trim every Unicode White_Space code point at boundaries and preserve it internally

- Covers: R1, R2, e.trim.whitespace, EC1
- Level: unit
- Command IDs: none
- Fixture/setup: Independently enumerate the Unicode `White_Space` property as U+0009-U+000D, U+0020, U+0085, U+00A0, U+1680, U+2000-U+200A, U+2028, U+2029, U+202F, U+205F, and U+3000; expand ranges into a deterministic ordered sequence of individual code points.
- Steps: For every enumerated code point, normalize `<code point>A` and `A<code point>` in `trim` mode and separately normalize `A<code point>B`; also normalize `\u0020hello\u3000`.
- Expected result: Each boundary case returns `A`; every internal case returns `A<code point>B` unchanged; the example returns `hello`.
- Failure proves: `trim` does not use the complete Unicode `White_Space` boundary or removes a qualifying internal code point.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T2. Preserve input text unchanged

- Covers: R1, R3, e.preserve.unchanged, EC2
- Level: unit
- Command IDs: none
- Fixture/setup: Inputs include empty text, ordinary text, `\u0020hello\u3000`, and text containing each code point from the deterministic `White_Space` fixture used by T1 at boundary and internal positions.
- Steps: Normalize each input in `preserve` mode.
- Expected result: Every returned text is code-point-for-code-point identical to its input.
- Failure proves: `preserve` is not accepted or alters input text.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T3. Reject every mode outside the closed vocabulary

- Covers: R1, R4, e.unknown.failure, EC3
- Level: unit
- Command IDs: none
- Fixture/setup: Generate values across the supported mode domain and exclude exactly `trim` and `preserve`; include the representative mode `fold`.
- Steps: Request normalization for every generated unknown mode with sentinel input text.
- Expected result: Every request fails with `unknown-mode` and returns no text.
- Failure proves: An unknown mode is accepted, produces a different failure, or returns text.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable
