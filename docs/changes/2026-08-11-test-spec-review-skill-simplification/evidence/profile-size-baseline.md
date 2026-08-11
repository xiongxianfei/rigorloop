# Test-spec-review Profile Size Baseline

Milestone: M1
Date: 2026-08-11
Canonical baseline commit: `9b0cd7d4`

Measurements use canonical authored files, LF-normalized bytes, Unicode whitespace-separated words, and one count per unique loaded resource.

| Resource | SHA-256 | Lines | Words | UTF-8 bytes |
| --- | --- | ---: | ---: | ---: |
| `skills/test-spec-review/SKILL.md` | `ba47ef669d2296aa14ae49e347fb3bb7e457e10fd9c92272818d308a505e5a99` | 359 | 2722 | 19768 |
| `references/boundary-first-method-v1.md` | `4268fbe89ecdfd7b79ca1321b8d6b19b2ed24e8adeda17cae8c319b087760f6f` | 110 | 857 | 6346 |
| `references/boundary-first-proof-v1.md` | `ec8e8239c642bf340c4c8aba2105ae9783bced35230bb5bf6501b7b931e6cc4d` | 41 | 356 | 2305 |
| `assets/review-result-skeleton.md` | `c9d8b983046988dd2d70790268f37698723db01956cb721a6454235766a5ea76` | 25 | 132 | 952 |
| `assets/material-finding.md` | `65386ed0c02147484b95b982d8b0389effdafb78f11fde98a789d35a67373193` | 14 | 55 | 460 |
| Total package | derived | 549 | 4122 | 29831 |

Baseline assembly accounting uses the future profile names to make before-and-after comparison stable. The current package has no standalone recording reference; its recording mechanics remain inline. The result asset is counted for recorded/formal output, and the finding asset is an additive per-material-finding copy.

| Baseline assembly | Unique resources | Words | UTF-8 bytes |
| --- | --- | ---: | ---: |
| `TSR0-isolated` | `SKILL.md` | 2722 | 19768 |
| `TSR0B-isolated-boundary` | `SKILL.md`, both boundary references | 3935 | 28419 |
| `TSR1-formal` | `SKILL.md`, result asset | 2854 | 20720 |
| `TSR1B-formal-boundary` | `SKILL.md`, both boundary references, result asset | 4067 | 29371 |
| Material-finding addition | finding asset once per finding | 55 | 460 |

The final measurement will add the recording reference as a separately reported overlay and will report all resource and total-package deltas honestly. The 30-40 percent `SKILL.md` reduction is advisory; no tokenizer or permanent size gate is introduced.
