Boundary model version: v1
Boundary model scope: R1-R4

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| proof.mode.outcome | R1, R3, R4 | b.mode.vocabulary, b.result.outcome, i.mode.outcome | T1, T2, T3 | automated | - |
| proof.trim.classification | R2 | b.text.transformation, b.unicode.white-space, i.trim.classification | T4, T5, T6, T7 | automated | - |

## Test cases

### T1. Trim is an accepted mode

- Covers: R1, ex.mode.known
- Level: unit
- Command IDs: none
- Fixture/setup: Input text `text` and mode `trim`.
- Steps: Invoke the normalizer.
- Expected result: The invocation is accepted as `trim` mode and does not fail with `unknown-mode`.
- Failure proves: The accepted-mode vocabulary excludes `trim` or routes it to the unknown-mode outcome.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T2. Preserve returns input unchanged

- Covers: R1, R3, ex.mode.known, ex.preserve.unchanged, ec.preserve.white-space
- Level: unit
- Command IDs: none
- Fixture/setup: Inputs containing leading, internal, and trailing Unicode `White_Space` code points, with mode `preserve`.
- Steps: Invoke the normalizer for each input and compare the returned text code point-for-code-point with the input.
- Expected result: Each invocation is accepted and returns its input unchanged.
- Failure proves: `preserve` is rejected, changes text, or produces an outcome other than returned text.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T3. Every unknown mode fails closed

- Covers: R1, R4, ex.mode.unknown, ec.mode.unknown
- Level: unit
- Command IDs: none
- Fixture/setup: A generated mode value constrained to differ from `trim` and `preserve`.
- Steps: For every generated unknown mode, invoke the normalizer and inspect both failure and returned-text outcomes.
- Expected result: Every invocation fails with `unknown-mode` and returns no text.
- Failure proves: The mode vocabulary admits an additional value, reports the wrong failure, or leaks returned text on failure.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T4. Every Unicode White_Space code point is removed at both boundaries

- Covers: R2, ex.trim.white-space, ac.trim.unicode
- Level: unit
- Command IDs: none
- Fixture/setup: Deterministically enumerate Unicode scalar values in ascending code-point order and select every value for which an independent Unicode property oracle reports `White_Space`.
- Steps: For each enumerated code point `W`, invoke `trim` with `W + A` and with `A + W`.
- Expected result: Both invocations return exactly `A`.
- Failure proves: A Unicode `White_Space` code point is not classified or removed at a leading or trailing text boundary.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T5. Every Unicode White_Space code point is preserved internally

- Covers: R2, ex.trim.white-space
- Level: unit
- Command IDs: none
- Fixture/setup: Use the same deterministic, ascending enumeration of every Unicode `White_Space` code point as T4.
- Steps: For each enumerated code point `W`, invoke `trim` with `A + W + B`, where `A` and `B` are retained non-whitespace code points.
- Expected result: The returned text is exactly `A + W + B`.
- Failure proves: Trim classification removes or changes a `White_Space` code point between retained non-whitespace code points.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T6. All-whitespace text trims completely

- Covers: R2, ec.trim.all-white-space
- Level: unit
- Command IDs: none
- Fixture/setup: For each code point from the deterministic Unicode `White_Space` enumeration, construct a nonempty input containing only that code point.
- Steps: Invoke the normalizer in `trim` mode for each input.
- Expected result: Every invocation returns empty text.
- Failure proves: Trim retains boundary whitespace when no non-whitespace text is present.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T7. Text without edge whitespace is unchanged by trim

- Covers: R2, ec.trim.no-edge-white-space
- Level: unit
- Command IDs: none
- Fixture/setup: Text whose first and last code points do not have the Unicode `White_Space` property, including a case with internal whitespace.
- Steps: Invoke the normalizer in `trim` mode and compare the result code point-for-code-point with the input.
- Expected result: The returned text is unchanged.
- Failure proves: Trim changes retained text or treats internal whitespace as a removable boundary.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable
