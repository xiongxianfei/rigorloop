Boundary model version: v1
Boundary model scope: R1-R4

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| proof.mode.closed | R1, R4 | b.mode.closed | T1, T4 | automated | - |
| proof.unicode.authority | R2 | b.unicode.authority | T2 | automated | - |
| proof.text.result | R2, R3 | b.text.result | T2, T3 | automated | - |
| proof.unknown.stop | R4 | b.unknown.stop | T4 | automated | - |
| proof.mode.outcome | R1, R2, R3, R4 | i.mode.outcome | T5 | automated | - |

## Test cases

### T1. Accept exactly the recognized modes

- Covers: R1, e.mode.accepted
- Level: unit
- Command IDs: none
- Fixture/setup: Representative text and the modes `trim` and `preserve`.
- Steps: Invoke the normalizer once with each recognized mode.
- Expected result: Both invocations are accepted and return the result selected by their mode.
- Failure proves: A recognized mode is not accepted.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T2. Trim Unicode whitespace boundaries

- Covers: R2, EC1, EC2, e.trim.unicode
- Level: unit
- Command IDs: none
- Fixture/setup: An independent fixture enumerating Unicode `White_Space` code points, non-whitespace text, text without boundary whitespace, text containing internal whitespace, and text consisting entirely of whitespace.
- Steps: Normalize the fixture cases in `trim` mode, placing each enumerated whitespace code point at leading and trailing boundaries.
- Expected result: Every leading and trailing Unicode `White_Space` code point is removed; internal whitespace and non-whitespace code points remain; text without boundary whitespace is unchanged; all-whitespace text becomes empty.
- Failure proves: `trim` does not follow the Unicode `White_Space` boundary or alters text outside the specified boundaries.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T3. Preserve input text unchanged

- Covers: R3, e.preserve.unchanged
- Level: unit
- Command IDs: none
- Fixture/setup: Empty text, non-whitespace text, boundary whitespace, internal whitespace, and all-whitespace text.
- Steps: Normalize every fixture in `preserve` mode.
- Expected result: Each returned text is exactly equal to its input text.
- Failure proves: `preserve` changes the input text.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T4. Reject every unknown mode without text

- Covers: R1, R4, EC3, e.unknown.rejected
- Level: unit
- Command IDs: none
- Fixture/setup: Multiple mode values outside the closed set `trim` and `preserve`, paired with empty, ordinary, and whitespace-only text.
- Steps: Invoke the normalizer for every unknown-mode and text pairing.
- Expected result: Every invocation fails with `unknown-mode` and returns no text.
- Failure proves: An unknown mode is accepted, produces the wrong failure, or returns text.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T5. Compose mode classification with its required outcome

- Covers: R1, R2, R3, R4, i.mode.outcome
- Level: unit
- Command IDs: none
- Fixture/setup: One text containing leading and trailing Unicode whitespace, tested with `trim`, `preserve`, and an unknown mode.
- Steps: Invoke the same normalizer entry point with each mode.
- Expected result: `trim` returns the boundary-trimmed text, `preserve` returns the exact input, and the unknown mode fails with `unknown-mode` and no text.
- Failure proves: Mode classification is not composed with the required transformation or stop outcome.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable
