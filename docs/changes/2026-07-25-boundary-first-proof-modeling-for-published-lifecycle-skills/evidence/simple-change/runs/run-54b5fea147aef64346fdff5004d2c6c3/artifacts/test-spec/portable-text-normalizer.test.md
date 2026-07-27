Boundary model version: v1
Boundary model scope: R1-R4

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| proof.mode-vocabulary | R1, R4 | mode.closed-vocabulary | T1, T6, T7 | automated | - |
| proof.normalization-outcome | R2, R3, R4 | normalization.outcome | T1, T2, T3, T4, T5, T6, T7 | automated | - |
| proof.mode-outcome | R1, R2, R3, R4 | interaction.mode-outcome | T8 | automated | - |

## Test cases

### T1. Trim both boundaries

Given text with leading and trailing Unicode whitespace and mode `trim`, the returned text excludes that surrounding whitespace.

### T2. Trim leading boundary

Given text with leading Unicode whitespace only and mode `trim`, the returned text excludes that leading whitespace.

### T3. Trim trailing boundary

Given text with trailing Unicode whitespace only and mode `trim`, the returned text excludes that trailing whitespace.

### T4. Trim text without surrounding whitespace

Given text with no leading or trailing Unicode whitespace and mode `trim`, the returned text equals the input text.

### T5. Trim Unicode whitespace-only text

Given Unicode whitespace-only text and mode `trim`, the returned text contains no characters.

### T6. Preserve exact input

Given text containing Unicode whitespace and mode `preserve`, the returned text is exactly equal to the input text.

### T7. Reject unknown mode

Given a mode other than `trim` or `preserve`, normalization fails with exactly `unknown-mode` and returns no text.

### T8. Compose mode classification with outcome

For mode `trim`, normalization returns the trimmed result; for mode `preserve`, it returns the unchanged input; and for an unknown mode, it fails with `unknown-mode` and returns no text.
