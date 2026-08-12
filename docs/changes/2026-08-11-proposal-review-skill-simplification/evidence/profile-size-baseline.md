# Proposal-Review Profile Size Baseline

Milestone: M1
Date: 2026-08-12
Canonical baseline commit: `f6a239c4`

Measurements use canonical authored files, LF-normalized bytes, Unicode whitespace-separated words, and one count per unique loaded resource.

| Resource | SHA-256 | Lines | Words | UTF-8 bytes |
| --- | --- | ---: | ---: | ---: |
| `skills/proposal-review/SKILL.md` | `a8fb68839b05901fb405355b0f9a6fa216a467ae82ef7966d84e5588728eaad9` | 346 | 2295 | 16879 |
| `assets/review-result-skeleton.md` | `7d7de75b718a044007b0b66f604e56e5c167faae86c41ab2baa9810c03096fe2` | 37 | 135 | 1039 |
| `assets/material-finding.md` | `f8c783c7d5b297dee4c70ba6177dcedf5bd887e841189b94d8d40254fe1e22f2` | 14 | 55 | 457 |
| Total package | derived | 397 | 2485 | 18375 |

Baseline profile names match the approved future assemblies. The current package has no conditional references, so all governing procedure is loaded from `SKILL.md`; the result and finding assets are counted only when their output structure is used.

| Baseline assembly | Unique resources | Words | UTF-8 bytes |
| --- | --- | ---: | ---: |
| `PRR0-core` | `SKILL.md`, result asset | 2430 | 17918 |
| `PRR0G-context-gated` | `SKILL.md`, result asset | 2430 | 17918 |
| `PRR1-recorded` | `SKILL.md`, result asset | 2430 | 17918 |
| `PRR1G-recorded-context-gated` | `SKILL.md`, result asset | 2430 | 17918 |
| Material-finding addition | finding asset once per finding | 55 | 457 |

The final measurement will add each triggered reference once and report every profile and total-package delta. The 30–45 percent common-path reduction is advisory; no tokenizer or permanent size gate is introduced.
