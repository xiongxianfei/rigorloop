Boundary model version: v1
Boundary model scope: R1-R4

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| proof.mode-vocabulary | R1, R4 | boundary.mode-vocabulary | T1, T5 | automated | - |
| proof.text-transformation | R2, R3 | boundary.text-transformation | T2, T3, T4 | automated | - |
| proof.unknown-stop | R4 | boundary.unknown-stop | T5 | automated | - |
| proof.known-mode-outcome | R1, R2, R3 | interaction.known-mode-outcome | T1, T2, T3, T4 | automated | - |
| proof.unknown-mode-stop | R4 | interaction.unknown-mode-stop | T5 | automated | - |

## Test cases

### T1. Accept exactly the known modes

- Covers: R1
- Level: unit
- Command IDs: none
- Fixture/setup: Invoke the normalizer with `trim` and `preserve` using ordinary text.
- Steps: Normalize the text once with each mode.
- Expected result: Both modes are accepted and return their mode-governed successful results.
- Failure proves: The closed vocabulary does not accept both required known modes.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T2. Trim leading and trailing Unicode whitespace

- Covers: R2, example.trim-whitespace
- Level: unit
- Command IDs: none
- Fixture/setup: Text with non-whitespace content surrounded by multiple Unicode whitespace characters.
- Steps: Normalize the text in `trim` mode.
- Expected result: All leading and trailing Unicode whitespace is removed while the enclosed text is returned.
- Failure proves: The `trim` transformation does not satisfy R2.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T3. Trim empty and all-whitespace text

- Covers: R2, EC1, EC2
- Level: unit
- Command IDs: none
- Fixture/setup: Empty text and text consisting entirely of Unicode whitespace.
- Steps: Normalize each input in `trim` mode.
- Expected result: Each invocation succeeds and returns empty text.
- Failure proves: The `trim` transformation mishandles an empty or all-whitespace boundary case.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T4. Preserve text unchanged

- Covers: R3, EC2, example.preserve-text
- Level: unit
- Command IDs: none
- Fixture/setup: Ordinary text, text with leading and trailing Unicode whitespace, and empty text.
- Steps: Normalize each input in `preserve` mode.
- Expected result: Every invocation returns its input text unchanged.
- Failure proves: The `preserve` transformation modifies text or mishandles empty text.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T5. Reject every unknown mode without text

- Covers: R1, R4, EC3, example.unknown-mode
- Level: unit
- Command IDs: none
- Fixture/setup: A parameterized or property-based set of modes excluding exactly `trim` and `preserve`, including empty, near-match, and unrelated string values.
- Steps: Normalize representative text with each unknown mode.
- Expected result: Every invocation fails with `unknown-mode` and returns no text.
- Failure proves: An unknown mode is accepted, produces the wrong failure, or leaks returned text across the stop boundary.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable
