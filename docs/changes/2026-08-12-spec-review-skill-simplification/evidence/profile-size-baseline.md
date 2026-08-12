# Spec-Review Profile Size Baseline

Milestone: M1
Date: 2026-08-12
Canonical baseline commit: `027eb7f6`

Measurements use canonical authored files, LF-normalized bytes, Unicode whitespace-separated words, and one count per unique loaded resource.

| Resource | SHA-256 | Lines | Words | UTF-8 bytes |
| --- | --- | ---: | ---: | ---: |
| `skills/spec-review/SKILL.md` | `914b6f5ebe7bedc2a2c3888f1e8466379b9a2b10dee9eed8e69e71c7c8dbc32e` | 284 | 2174 | 16304 |
| `references/boundary-first-method-v1.md` | `4268fbe89ecdfd7b79ca1321b8d6b19b2ed24e8adeda17cae8c319b087760f6f` | 110 | 857 | 6346 |
| `references/boundary-first-feature-authoring-v1.md` | `962180f3b6d2699c1001fe0c2792f9e8bb3c9c60a7c7f2053dfb73fdf99df7fe` | 66 | 350 | 2324 |
| `assets/review-result-skeleton.md` | `b6101bfa784bfb3d8ceb53672c4908c98b010d6242336c4016bf9e7078e4f25d` | 28 | 154 | 1103 |
| `assets/material-finding.md` | `2ee22933a2681b0fc376692d3ec940ea0f05b2e2ab59c4dc8ca856ceb394dd1f` | 14 | 55 | 445 |
| Total package | derived | 502 | 3590 | 26522 |

The future profile names make comparison stable. The current package has no governed settlement reference, so all settlement and automation procedure remains inline. The result asset is included for every formal invocation; the finding asset is additive once per material finding.

| Baseline profile | Unique resources | Words | UTF-8 bytes |
| --- | --- | ---: | ---: |
| `SR1-isolated-formal` | `SKILL.md`, result asset | 2328 | 17407 |
| `SR1B-isolated-formal-boundary` | isolated profile plus both boundary references | 3535 | 26077 |
| `SR2-governed-manual` | `SKILL.md`, result asset | 2328 | 17407 |
| `SR2-governed-automated` | `SKILL.md`, result asset | 2328 | 17407 |
| `SR2B-governed-formal-boundary` | governed profile plus both boundary references | 3535 | 26077 |
| Material-finding addition | finding asset once per finding | 55 | 445 |

Final acceptance will add the governed reference to SR2 profiles, report every resource and total-package delta, require lower SR1 words and bytes, and reject unexplained governed growth. No tokenizer or permanent size gate is introduced.
