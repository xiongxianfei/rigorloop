Boundary model version: v1
Boundary model scope: R1-R4

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| proof.mode-vocabulary | R1, R4 | mode.vocabulary | T1, T2, T3, T4 | automated | - |
| proof.normalization-outcome | R2, R3, R4 | normalization.outcome | T1, T2, T3, T4 | automated | - |
| proof.mode-outcome | R1, R2, R3, R4 | interaction.mode-outcome | T1, T2, T3, T4 | automated | - |

## Test cases

T1. Trim mode removes surrounding Unicode whitespace
- Covers: R1, R2
- Level: unit
- Fixture/setup: Text `  hello   ` and mode `trim`.
- Steps: Normalize the fixture text using the fixture mode.
- Expected result: Returned text is `hello` and no `unknown-mode` failure occurs.
- Failure proves: The valid `trim` mode was rejected or its required outcome was not produced.
- Automation location: Portable text normalizer unit tests.

T2. Preserve mode returns text unchanged
- Covers: R1, R3
- Level: unit
- Fixture/setup: Text `  hello   ` and mode `preserve`.
- Steps: Normalize the fixture text using the fixture mode.
- Expected result: Returned text is exactly `  hello   ` and no `unknown-mode` failure occurs.
- Failure proves: The valid `preserve` mode was rejected or altered the input text.
- Automation location: Portable text normalizer unit tests.

T3. Illustrated unknown mode fails without text
- Covers: R1, R4
- Level: unit
- Fixture/setup: Any text and mode `collapse`.
- Steps: Normalize the fixture text using the fixture mode.
- Expected result: The result is `unknown-mode` and no text is returned.
- Failure proves: An unknown mode was accepted, produced the wrong failure, or returned text.
- Automation location: Portable text normalizer unit tests.

T4. Every mode outside the closed vocabulary follows the unknown-mode outcome
- Covers: R1, R4
- Level: unit
- Fixture/setup: Parameterized or generated mode values excluding exactly `trim` and `preserve`, with arbitrary text.
- Steps: Normalize the text once for each generated unknown mode.
- Expected result: Every invocation results in `unknown-mode` and returns no text.
- Failure proves: The accepted vocabulary is broader than specified or an unknown mode does not fail closed.
- Automation location: Portable text normalizer unit tests.
