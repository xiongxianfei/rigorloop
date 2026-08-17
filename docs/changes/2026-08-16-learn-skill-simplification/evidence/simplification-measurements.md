# Learn skill simplification measurements

Measured on 2026-08-17 from canonical authored files with LF line endings, Unicode whitespace-separated words, UTF-8 bytes, and each unique loaded procedural resource counted once in `SKILL.md`, then reference order.

| Surface | Files | Baseline words | Final words | Change | Baseline bytes | Final bytes | Change |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `LR0-route-result` | `SKILL.md` | 1,712 | 993 | -719 (-42.00%) | 12,375 | 7,578 | -4,797 (-38.76%) |
| `LR1-session` | `SKILL.md` + `session-method.md` | 1,712 | 1,610 | -102 (-5.96%) | 12,375 | 12,204 | -171 (-1.38%) |
| Universal resource | `skills/learn/SKILL.md` | - | 993 | - | - | 7,578 | - |
| Conditional resource | `skills/learn/references/session-method.md` | 0 | 617 | +617 | 0 | 4,626 | +4,626 |
| Total canonical package | both unique files | 1,712 | 1,610 | -102 (-5.96%) | 12,375 | 12,204 | -171 (-1.38%) |

SHA-256 identities:

- `skills/learn/SKILL.md`: `d0f7395e6d0a51d685aed6bdc0ef3512d9e5c549b1233a12a0fd5c2f7b8c8a44`
- `skills/learn/references/session-method.md`: `13ee89432023349ea066943da5951837bdd38c3ee6bfcfc28ebfd511af28abad`

Both real loaded profiles strictly decrease in both required measures. The package grows by one file but decreases in total words and bytes. No procedural rule has two normative owners: the root owns universal safety and route-result recording, while the reference owns full-session mechanics. The resource map names the reference and trigger but does not duplicate its procedure.

The M2 R2 review record contains an intermediate transcription of 989 words / 7,553 bytes for LR0 and 1,606 words / 12,179 bytes for LR1. The reviewed correction subsequently restored the compatibility-sensitive `pre-session trigger closeout` phrase, and M3 replaced Codex-specific `$learn` syntax with portable direct-invocation wording after adapter validation exposed it. This measurement is the canonical final profile evidence; the reduction conclusions are unchanged.
