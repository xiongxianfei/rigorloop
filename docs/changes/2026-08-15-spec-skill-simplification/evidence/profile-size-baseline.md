# Spec Skill Simplification Profile Baseline

- Baseline revision: `3b0daafc`
- Measurement date: 2026-08-15
- Canonical source: `skills/spec/`
- Normalization: UTF-8 text with CRLF and CR normalized to LF
- Word convention: Unicode whitespace-separated words
- Assembly convention: count each unique procedural resource once in documented load order; copied output assets are reported separately

## Input identities

| Resource | SHA-256 | UTF-8 bytes | Words |
| --- | --- | ---: | ---: |
| `skills/spec/SKILL.md` | `bf36e707d3075a64c57c41f63ec65d7be5b6a64203f40ac04a0da3a45834427f` | 12853 | 1813 |
| `skills/spec/references/boundary-first-method-v1.md` | `4268fbe89ecdfd7b79ca1321b8d6b19b2ed24e8adeda17cae8c319b087760f6f` | 6346 | 857 |
| `skills/spec/references/boundary-first-feature-authoring-v1.md` | `962180f3b6d2699c1001fe0c2792f9e8bb3c9c60a7c7f2053dfb73fdf99df7fe` | 2324 | 350 |
| `skills/spec/assets/spec-skeleton.md` | `68a7ca96ae0c127457112f0cd2614ba5aa15d5dc06480586f857806c953fd9a8` | 1564 | 209 |

## Procedural assemblies

Both current assemblies load the same three procedural files because both boundary references are initially loaded and governed procedure is still inline.

| Assembly | Loaded procedural resources | UTF-8 bytes | Words |
| --- | --- | ---: | ---: |
| `SA0-portable` | `SKILL.md`; `boundary-first-method-v1.md`; `boundary-first-feature-authoring-v1.md` | 21523 | 3020 |
| `SA1-governed` | `SKILL.md`; `boundary-first-method-v1.md`; `boundary-first-feature-authoring-v1.md` | 21523 | 3020 |

## Structural and package totals

| Measurement | UTF-8 bytes | Words |
| --- | ---: | ---: |
| Representative copied skeleton | 1564 | 209 |
| Total canonical package | 23087 | 3229 |

The baseline records actual pre-refactor loaded context. Final evidence must show both SA0 and SA1 decreasing while reporting total package change separately.
