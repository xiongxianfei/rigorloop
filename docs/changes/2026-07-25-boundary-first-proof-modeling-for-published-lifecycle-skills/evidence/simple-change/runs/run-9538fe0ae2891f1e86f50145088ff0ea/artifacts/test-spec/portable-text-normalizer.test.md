Boundary model version: v1
Boundary model scope: R1-R4

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| proof.mode.closed-values | R1 | mode.closed-values | T1 | automated | - |
| proof.text.trim-whitespace | R2 | text.trim-whitespace | T2 | automated | - |
| proof.text.preserve-input | R3 | text.preserve-input | T3 | automated | - |
| proof.outcome.unknown-mode | R4 | outcome.unknown-mode | T4 | automated | - |
| proof.interaction.mode-behavior | R1, R2, R3 | interaction.mode-behavior | T5 | automated | - |
| proof.interaction.unknown-mode-stop | R1, R4 | interaction.unknown-mode-stop | T6 | automated | - |

## Test cases

### T1. Accept exactly the closed mode vocabulary

- Covers: R1, mode.closed-values
- Level: unit
- Command IDs: none
- Fixture/setup: Inputs using modes `trim` and `preserve`; a generator over every supported mode value other than those two exact values.
- Steps: Normalize representative text with each accepted mode; then attempt normalization for every generated excluded value.
- Expected result: Exactly `trim` and `preserve` are accepted; every excluded value is rejected as an unknown mode.
- Failure proves: The accepted mode vocabulary is incomplete or not closed.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T2. Trim every Unicode White_Space code point only at text boundaries

- Covers: R2, example.trim, text.trim-whitespace
- Level: unit
- Command IDs: none
- Fixture/setup: A deterministic table containing every Unicode `White_Space` code point: U+0009, U+000A, U+000B, U+000C, U+000D, U+0020, U+0085, U+00A0, U+1680, U+2000, U+2001, U+2002, U+2003, U+2004, U+2005, U+2006, U+2007, U+2008, U+2009, U+200A, U+2028, U+2029, U+202F, U+205F, and U+3000. Retained non-whitespace sentinels are `A` and `B`.
- Steps: For each table entry `W`, normalize `WAB`, `ABW`, and `WABW` in `trim` mode; normalize `AWB` in `trim` mode; also normalize `AB` and a string composed only of table entries.
- Expected result: Each boundary case returns `AB`; each `AWB` case returns exactly `AWB`; `AB` remains `AB`; the whitespace-only string returns the empty string.
- Failure proves: A Unicode `White_Space` code point is not removed at a boundary, an internal occurrence is removed, non-boundary text is altered, or boundary trimming is incomplete.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T3. Preserve input text exactly

- Covers: R3, example.preserve, text.preserve-input
- Level: unit
- Command IDs: none
- Fixture/setup: Representative text including empty text, ordinary text, and text containing every code point from T2 at leading, internal, and trailing positions.
- Steps: Normalize each fixture in `preserve` mode and compare the returned text code point for code point with its input.
- Expected result: Every returned text is identical to its input.
- Failure proves: `preserve` mode changes, removes, inserts, or reorders input text.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T4. Reject every unknown mode without returning text

- Covers: R4, example.unknown-mode, outcome.unknown-mode
- Level: unit
- Command IDs: none
- Fixture/setup: A generator over every supported mode value except exact `trim` and `preserve`, including case variants, prefixed or suffixed values, and lookalike values.
- Steps: Attempt normalization of representative text for each generated unknown mode.
- Expected result: Every attempt fails with exactly `unknown-mode` and returns no text.
- Failure proves: An unknown mode succeeds, produces a different failure, or leaks a text result.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T5. Compose accepted mode classification with the selected behavior

- Covers: R1, R2, R3, example.trim, example.preserve, interaction.mode-behavior
- Level: unit
- Command IDs: none
- Fixture/setup: Input `\u0020hello\u00A0` paired separately with exact modes `trim` and `preserve`.
- Steps: Normalize both pairs through the same public normalizer entry point.
- Expected result: `trim` returns `hello`; `preserve` returns the input unchanged.
- Failure proves: Accepted-mode classification selects the wrong behavior or the composed path diverges from R2 or R3.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable

### T6. Stop unknown modes before any text result

- Covers: R1, R4, example.unknown-mode, interaction.unknown-mode-stop
- Level: unit
- Command IDs: none
- Fixture/setup: Representative text `hello` and the unknown mode `other`, plus the unknown-mode generator from T4.
- Steps: Attempt normalization through the same public normalizer entry point for each unknown mode and inspect both failure and text-result channels.
- Expected result: Each attempt produces exactly `unknown-mode` and no text.
- Failure proves: Closed-mode classification fails to trigger the required stop outcome or permits a success payload.
- Evidence artifact: not applicable
- Automation location: not applicable
- Required by milestone: not applicable
