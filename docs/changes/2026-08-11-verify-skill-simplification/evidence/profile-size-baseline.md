# Verify Skill Profile Size Baseline

Milestone: M1
Date: 2026-08-11
Canonical baseline commit: `2718ee79`

| Resource | SHA-256 | Lines | Words | UTF-8 bytes |
| --- | --- | ---: | ---: | ---: |
| `skills/verify/SKILL.md` | `9dda0c3d14024416dddb254bcdf15cba708129bee8ed78792db074ca6329e8ca` | 308 | 2896 | 20715 |
| `skills/verify/references/boundary-first-method-v1.md` | `4268fbe89ecdfd7b79ca1321b8d6b19b2ed24e8adeda17cae8c319b087760f6f` | 110 | 857 | 6346 |
| Total package | derived | 418 | 3753 | 27061 |

Before simplification, scoped and final verification both load the 2896-word `SKILL.md`; the boundary reference adds 857 words only when independently triggered. The package has one mapped resource and no final-readiness reference.

Primary portable measurements are LF-normalized words and UTF-8 bytes. No new tokenizer dependency or permanent size gate is introduced.
