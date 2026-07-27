# Portable text normalizer proof map

Boundary model version: v1
Boundary model scope: R1-R4

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| proof.mode.vocabulary | R1, R4 | boundary.mode.vocabulary | T1, T4 | automated | - |
| proof.text.transformation | R2, R3 | boundary.text.transformation | T1, T2, T3 | automated | - |
| proof.unknown.outcome | R4 | boundary.unknown.outcome | T4 | automated | - |
| proof.mode.transformation | R1, R2, R3 | interaction.mode.transformation | T1, T2, T3 | automated | - |
| proof.unknown.stop | R1, R4 | interaction.unknown.stop | T4 | automated | - |

## Test cases

### T1. Trim Unicode whitespace boundaries

- Covers: R1, R2, example.trim.whitespace
- Level: unit
- Command IDs: none
- Fixture/setup: Parameterize every code point with the Unicode `White_Space` property at the leading and trailing boundaries of text containing a non-whitespace payload.
- Steps: Normalize each input in `trim` mode.
- Expected result: The leading and trailing Unicode whitespace is removed and the payload is returned.
- Failure proves: `trim` is not accepted or does not apply the R2 Unicode whitespace boundary transformation.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T2. Trim text without boundary whitespace

- Covers: R2, example.trim.non-whitespace, EC1
- Level: unit
- Command IDs: none
- Fixture/setup: Text containing no leading or trailing Unicode whitespace.
- Steps: Normalize the text in `trim` mode.
- Expected result: The input text is returned unchanged.
- Failure proves: `trim` alters text outside the leading or trailing Unicode whitespace boundaries governed by R2.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T3. Preserve text unchanged and trim all-whitespace text

- Covers: R1, R2, R3, example.preserve.unchanged, EC2, EC3
- Level: unit
- Command IDs: none
- Fixture/setup: Unicode-whitespace-only text and text containing leading, internal, and trailing Unicode whitespace.
- Steps: Normalize the whitespace-only text in `trim` mode; normalize both inputs in `preserve` mode.
- Expected result: `trim` returns empty text for the whitespace-only input; `preserve` returns each input unchanged.
- Failure proves: The accepted modes do not select their requirement-owned transformations or `preserve` changes input text.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T4. Reject every unknown mode without text

- Covers: R1, R4, example.unknown.failure, EC4
- Level: unit
- Command IDs: none
- Fixture/setup: Parameterize mode values outside the closed set `trim` and `preserve`.
- Steps: Invoke the normalizer with each generated unknown mode and input text.
- Expected result: Every invocation fails with `unknown-mode` and returns no text.
- Failure proves: The mode vocabulary is not closed, the required failure is absent or substituted, or an unknown mode produces text instead of stopping.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable
