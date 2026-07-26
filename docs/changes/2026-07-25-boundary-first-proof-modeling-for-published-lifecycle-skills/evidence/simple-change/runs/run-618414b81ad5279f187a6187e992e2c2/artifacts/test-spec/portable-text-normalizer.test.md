# Portable text normalizer test spec

## Status

active

Boundary model version: v1
Boundary model scope: R1-R4

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| text.proof.canonical | R1 | text.canonical.requirements | T1, T2 | automated | - |
| text.proof.evidence | R1, R2, R3, R4 | text.evidence.tests | T1, T2, T3 | automated | - |
| text.proof.mode | R1, R4 | text.mode.valid, text.mode.unknown | T1, T2 | automated | - |
| text.proof.outcome | R2, R3, R4 | text.outcome.value, text.outcome.error | T1, T2, T3 | automated | - |

## Test cases

T1. `trim` removes surrounding Unicode whitespace and returns the selected mode.

T2. Every unknown mode fails with `unknown-mode` and returns no text.

T3. `preserve` returns the input unchanged and returns the selected mode.
