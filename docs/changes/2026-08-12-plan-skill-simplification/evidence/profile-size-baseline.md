# Plan Profile Size Baseline

Milestone: M2
Date: 2026-08-13
Canonical baseline commit: `702e5940`

Measurements use canonical authored files, LF-normalized bytes, Unicode whitespace-separated words, and one count per unique loaded procedural resource. Assets are reported separately.

| Resource | SHA-256 | Words | UTF-8 bytes |
| --- | --- | ---: | ---: |
| `skills/plan/SKILL.md` | `87fca53ed138ef61dc39f8b517cbf957336dadc0d52a1ef0ad748bd82b93b3f0` | 2555 | 18680 |
| `references/boundary-first-method-v1.md` | `4268fbe89ecdfd7b79ca1321b8d6b19b2ed24e8adeda17cae8c319b087760f6f` | 857 | 6346 |
| `assets/plan-skeleton.md` | `9cc724febd69027b3b4c4e6ed5cd94852923ea5f00af1ec2bfe646b10acd248e` | 211 | 1560 |
| `assets/milestone.md` | `156fa395448cd19ede216739ab6901fb34ca205c0a5923b0b5ac974bc61880e8` | 120 | 980 |
| `assets/decision-log-row.md` | `f461dd267b53fa6690f9ee8222e4fa8642e27a3cafe530fd8fa75bb2243bb5fb` | 32 | 320 |
| Total package | derived | 3775 | 27886 |

| Baseline profile | Unique procedural resources | Words | UTF-8 bytes |
| --- | --- | ---: | ---: |
| `PL0` | `SKILL.md` | 2555 | 18680 |
| `PL0B` | `SKILL.md`, boundary reference | 3412 | 25026 |
| `PL1` | `SKILL.md` because governed procedure was inline | 2555 | 18680 |
| `PL1B` | `SKILL.md`, boundary reference | 3412 | 25026 |

The future governed reference is absent from the baseline. Final acceptance adds it to PL1 and PL1B, requires both PL0 and PL1 to decrease, and reports structural assets and total-package change independently.
