# Proposal Skill Simplification Measurements

## Convention

Measurements use canonical authored files, normalize CRLF and CR to LF, count each unique procedural resource once in documented load order, count Unicode whitespace-separated words, and report UTF-8 bytes. Copied output structure and total package footprint are separate from procedural loaded context. No tokenizer estimate or permanent simplicity threshold is used.

## Resource identities

| Resource | SHA-256 after LF normalization | UTF-8 bytes | Words |
| --- | --- | ---: | ---: |
| `skills/proposal/SKILL.md` | `78e1c0e78889c199c66489152f08136642a2702963e43e94819680649bec1410` | 8435 | 1092 |
| `skills/proposal/references/governed-proposal-authoring.md` | `7c371fd772422d7d622ee9c42c444a66e4ac4ec3810841d2b39d99d73cce47b0` | 3033 | 381 |
| `skills/proposal/references/strategic-and-scope-gates.md` | `22c1fcb8112036e788141840b12165c47df138dfb9082cf958647e449374466e` | 2818 | 348 |
| `skills/proposal/assets/proposal-skeleton.md` | `d5a33d410d0612c7f7430c0c42a24cefb5efdaf6cfbd552463634bf3b03d0904` | 2077 | 325 |

## Procedural assemblies

| Assembly | Loaded resources | Baseline bytes | Current bytes | Byte reduction | Baseline words | Current words | Word reduction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `PA0-portable` | `SKILL.md` | 14796 | 8435 | 6361 (43.0%) | 2122 | 1092 | 1030 (48.5%) |
| `PA0G-portable-gated` | `SKILL.md`, strategic reference | 14796 | 11253 | 3543 (23.9%) | 2122 | 1440 | 682 (32.1%) |
| `PA1-governed` | `SKILL.md`, governed reference | 14796 | 11468 | 3328 (22.5%) | 2122 | 1473 | 649 (30.6%) |
| `PA1G-governed-gated` | `SKILL.md`, governed reference, strategic reference | 14796 | 14286 | 510 (3.4%) | 2122 | 1821 | 301 (14.2%) |

Every real loaded assembly decreases in both primary metrics; no semantic-preservation exception is used.

## Structural and total package measurements

| Measurement | Baseline bytes | Current bytes | Change | Baseline words | Current words | Change |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Representative copied skeleton | 1089 | 2077 | +988 | 141 | 325 | +184 |
| Total canonical package | 15885 | 16363 | +478 (+3.0%) | 2263 | 2146 | -117 (-5.2%) |

The skeleton grows because it now structurally owns four independently composable conditional groups. Total package bytes grow slightly because conditional procedure and complete structure are packaged rather than deleted. This maintenance footprint does not negate loaded-context reduction and is not presented as simplification by deletion.
