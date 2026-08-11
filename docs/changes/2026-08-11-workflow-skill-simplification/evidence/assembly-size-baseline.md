# Workflow Assembly Size Baseline

Measurement date: 2026-08-11
Canonical source revision: `320b41f6`
Normalization: canonical authored files, LF line endings, each unique loaded resource counted once, Unicode whitespace-separated words, UTF-8 bytes.

## Resource baseline

| Resource | Words | UTF-8 bytes |
| --- | ---: | ---: |
| `skills/workflow/SKILL.md` | 4,333 | 32,074 |
| `references/boundary-first-method-v1.md` | 857 | 6,346 |
| `assets/workflows-skeleton.md` | 1,236 | 9,551 |
| Total package | 6,426 | 47,971 |

## Loaded assemblies before simplification

The current skill contains governed lifecycle and automation procedure inline. The skeleton loads only for guide creation/refresh; the boundary reference is independently additive.

| Assembly | Loaded resources | Words | UTF-8 bytes |
| --- | --- | ---: | ---: |
| `WP0-generic-routing` | `SKILL.md` | 4,333 | 32,074 |
| `WP1-governed` | `SKILL.md` | 4,333 | 32,074 |
| `WP2-governed-automated` | `SKILL.md` | 4,333 | 32,074 |
| `WP3-guide-authoring` | `SKILL.md`, skeleton | 5,569 | 41,625 |
| `WP4-governed-guide-authoring` | `SKILL.md`, skeleton | 5,569 | 41,625 |
| `WPB-automation-bootstrap` | `SKILL.md` | 4,333 | 32,074 |
| `WPS-stateless-automation-command` | `SKILL.md` | 4,333 | 32,074 |

Every independently boundary-triggered variant adds 857 words and 6,346 bytes.

Token counts are omitted because this change introduces no tokenizer dependency and no existing pinned tokenizer is required by acceptance.
