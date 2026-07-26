# Portable text normalizer test spec

## Status

active

Boundary model version: v1
Boundary model scope: R1-R4

## Proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| text.proof.canonical | R1, R2, R3 | text.canonical.requirements | T1, T2, T3 | automated | - |
| text.proof.mode | R1, R4 | text.mode.valid, text.mode.unknown | T1, T2 | automated | - |
| text.proof.outcome | R2, R3, R4 | text.outcome.value, text.outcome.error | T1, T2, T3 | automated | - |
| text.proof.evidence | R1, R2, R3, R4 | text.evidence.tests | T1, T2, T3 | automated | - |

## Test cases

T1. `trim` removes leading and trailing Unicode whitespace and returns
`{"mode": "trim", "text": "value"}`.

T2. Every string outside `trim` and `preserve`, including empty, differently
cased, and future-looking values, fails with `unknown-mode` and no text.

T3. `preserve` returns the exact input bytes and
`{"mode": "preserve"}`.
