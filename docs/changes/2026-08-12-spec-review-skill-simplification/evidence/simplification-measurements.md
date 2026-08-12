# Spec-Review Simplification Measurements

Date: 2026-08-12
Milestone: M3

Canonical files were normalized to LF, each unique loaded resource was counted once, and words use Unicode whitespace separation. Token counts are omitted because this repository has no required pinned tokenizer for this change.

| Resource | Baseline words | Final words | Baseline bytes | Final bytes | Delta |
| --- | ---: | ---: | ---: | ---: | --- |
| `SKILL.md` | 2174 | 1949 | 16304 | 14821 | -225 words, -1483 bytes |
| governed settlement reference | 0 | 454 | 0 | 3567 | conditional addition |
| method reference | 857 | 857 | 6346 | 6346 | unchanged |
| feature-authoring reference | 350 | 350 | 2324 | 2324 | unchanged |
| result asset | 154 | 194 | 1103 | 1427 | +40 words, +324 bytes |
| finding asset | 55 | 55 | 445 | 445 | unchanged |
| total package | 3590 | 3859 | 26522 | 28930 | +269 words, +2408 bytes |

| Loaded profile | Baseline words | Final words | Baseline bytes | Final bytes | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| `SR1-isolated-formal` | 2328 | 2143 | 17407 | 16248 | -7.9% words, -6.7% bytes |
| `SR1B-isolated-formal-boundary` | 3535 | 3350 | 26077 | 24918 | lower; boundary bytes unchanged |
| `SR2-governed-formal` manual | 2328 | 2597 | 17407 | 19815 | explained conditional procedure |
| `SR2-governed-formal` automated | 2328 | 2597 | 17407 | 19815 | same assembly; different authority branch |
| `SR2B-governed-formal-boundary` | 3535 | 3804 | 26077 | 28485 | explained conditional plus unchanged boundary resources |

The primary acceptance surface, isolated formal review, is materially smaller. Governed and total-package growth is not presented as deletion: it buys one explicit conditional owner for exact settlement, automation, retry, pause, and resource-failure procedure. The 25–40 percent main-file figure remains a planning target, not a gate.
