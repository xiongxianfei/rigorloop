# Plan Simplification Measurements

Date: 2026-08-13
Baseline commit: `702e5940`
Current package commit: `92d63604`

Measurements use canonical authored files, LF line endings, UTF-8 bytes, Unicode whitespace-separated words, documented load order, and one count per unique procedural resource. Copied assets are excluded from procedural profiles and reported separately. No token estimate is used because the repository has no required pinned tokenizer for this assembly.

## Current resource identities

| Resource | SHA-256 | Words | UTF-8 bytes |
| --- | --- | ---: | ---: |
| `skills/plan/SKILL.md` | `324aec0e65ec7e3ce4e2b456b61962bc907f67db6dca024b8a5de2a5724e43a2` | 1988 | 14888 |
| `references/governed-plan-authoring.md` | `8152a01c8500ed9fe02a5a2c02c81881b7d4ecdcdbc07d23857da16641d1d2c5` | 465 | 3595 |
| `references/boundary-first-method-v1.md` | `4268fbe89ecdfd7b79ca1321b8d6b19b2ed24e8adeda17cae8c319b087760f6f` | 857 | 6346 |
| `assets/plan-skeleton.md` | `9cc724febd69027b3b4c4e6ed5cd94852923ea5f00af1ec2bfe646b10acd248e` | 211 | 1560 |
| `assets/milestone.md` | `0331d18674fb0631b5fa672210a9f28204bf2e645965cbbdf60f0db028fc4bab` | 119 | 995 |
| `assets/decision-log-row.md` | `f461dd267b53fa6690f9ee8222e4fa8642e27a3cafe530fd8fa75bb2243bb5fb` | 32 | 320 |
| Total package | derived | 3672 | 27704 |

## Procedural profiles

| Profile | Load order | Baseline words | Current words | Word delta | Baseline bytes | Current bytes | Byte delta |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `PL0` | `SKILL.md` | 2555 | 1988 | -567 | 18680 | 14888 | -3792 |
| `PL0B` | `SKILL.md`, boundary reference | 3412 | 2845 | -567 | 25026 | 21234 | -3792 |
| `PL1` | `SKILL.md`, governed reference | 2555 | 2453 | -102 | 18680 | 18483 | -197 |
| `PL1B` | `SKILL.md`, governed reference, boundary reference | 3412 | 3310 | -102 | 25026 | 24829 | -197 |

Both primary profiles decrease. The portable reduction is large because governed mechanics no longer load. The governed reduction is intentionally modest because exact authority, identity, retry, and failure procedure remains explicit. Boundary variants inherit the same absolute reduction because the unchanged boundary reference is loaded once. Total package size decreases by 103 words and 182 bytes, so relocation is not misrepresented as deletion or hidden growth.

The three structural assets total 362 words and 2875 bytes. The milestone asset changes from 120 words and 980 bytes to 119 words and 995 bytes because stable execution-intent labels replace mutable progress fields; this asset delta is reported separately from procedural context.
