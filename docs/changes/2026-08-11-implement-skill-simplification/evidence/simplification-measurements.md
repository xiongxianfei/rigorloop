# Implement Skill Simplification Measurements

Milestone: M3
Date: 2026-08-11
Baseline commit: `53df8ce2`
Final measured package: canonical working tree after approved CMD7 correction

## Measurement convention

Measurements use canonical authored files with LF line endings. Each unique loaded resource is counted once in documented load order. Unicode whitespace-separated words and UTF-8 bytes are the portable measures. The existing repository token estimator is reported only for `SKILL.md`; no new tokenizer or permanent size gate was added.

The result asset is counted for each completed result. The boundary reference remains an independent conditional addition and is reported separately rather than silently included in every profile.

## Resource measurements

| Resource | Before words | After words | Before bytes | After bytes | SHA-256 after |
| --- | ---: | ---: | ---: | ---: | --- |
| `SKILL.md` | 3338 | 2187 | 23906 | 16165 | `f28889bb5f1d30e47c0e31b3b4ead07fad76e583bfa2032145dbc0e6ae8136b8` |
| boundary reference | 857 | 857 | 6346 | 6346 | `4268fbe89ecdfd7b79ca1321b8d6b19b2ed24e8adeda17cae8c319b087760f6f` |
| planned reference | 0 | 441 | 0 | 3282 | `4450380ea9989c7fccca1b4e0b67713dd728d55d9fa6ec0d88d2c6906672390a` |
| automation reference | 0 | 544 | 0 | 4265 | `e94a2d52c08e495a3f188f48db81d70fe754103e812f7f114ba21235727d9a54` |
| result asset | 0 | 199 | 0 | 1454 | `c3b6dc912d2d0afd18fcc9a89a308aaa86cbe14d35f3e604846c703c35a2ee2d` |
| total package | 4195 | 4228 | 30252 | 31512 | derived from the five unique resources |

`SKILL.md` decreased by 1,151 words (34.48%) and 7,741 bytes (32.38%). Its pinned advisory estimate decreased from 5,977 to 4,042 tokens (32.37%). Total package size increased by 33 words (0.79%) and 1,260 bytes (4.17%), honestly reflecting the new explicit conditional procedures and grouped asset.

## Invocation profiles

| Profile | Loaded resources after | Before words | After words | Word delta | Before bytes | After bytes | Byte delta |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `IP0-isolated` | `SKILL.md` + result asset | 3338 | 2386 | -952 (-28.52%) | 23906 | 17619 | -6287 (-26.30%) |
| `IP1-planned` | `SKILL.md` + planned reference + result asset | 3338 | 2827 | -511 (-15.31%) | 23906 | 20901 | -3005 (-12.57%) |
| `IP2-planned-armed` | `SKILL.md` + planned reference + automation reference + result asset | 3338 | 3371 | +33 (+0.99%) | 23906 | 25166 | +1260 (+5.27%) |

The independent boundary trigger adds 857 words and 6,346 bytes before and after, so it does not change any profile delta.

## Acceptance interpretation

`IP0-isolated` materially improves and lands close to the advisory 30–45% target without hiding universal policy. `IP1-planned` also materially improves even after its explicit milestone procedure and result asset are counted. `IP2-planned-armed` has a small justified increase: it is the only profile that loads the newly explicit independent-review, fidelity, bounded-correction, and promotion procedure. That conditional cost replaces implicit and repeated common-path prose and does not burden isolated or ordinary planned work.

| Structural metric | Before | After |
| --- | ---: | ---: |
| Identified duplication/procedure clusters without one owner | 7 | 0 |
| Complete inline result structures | 2 | 0 |
| Mapped resources | 1 | 4 |
| Conditional implementation references | 0 | 2 |
| Structural result assets | 0 | 1 |

No percentage is used as a permanent validation gate.
