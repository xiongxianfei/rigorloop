# Architecture Skill Simplification Measurements

- Baseline revision: `56664a41`
- Current implementation revision: `793d3acd`
- Convention: canonical authored UTF-8 files, LF normalization, Unicode whitespace-separated words, and each unique procedure once in `SKILL.md`, method-reference, governed-reference order

## Procedural resources

| Resource | SHA-256 | Bytes | Words |
| --- | --- | ---: | ---: |
| `SKILL.md` | `431964ed262f3b2365201382705368a0a402c9a1248c6d89a4e0235c8813bbd8` | 6345 | 772 |
| `references/architecture-package-method.md` | `ca2f741dd2732f8afb77527ca87bd0a12e952ac9e777a68a7de1b43d983a8729` | 2559 | 324 |
| `references/governed-architecture-authoring.md` | `d698ba101000455ba32e82f1b6f0fc5492afae80b9b5a66512a41c04e8511570` | 3976 | 497 |

## Loaded assemblies

| Assembly | Baseline bytes | Current bytes | Reduction | Baseline words | Current words | Reduction |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `AA0-assessment` | 13105 | 6345 | 51.58% | 1765 | 772 | 56.26% |
| `AA1-portable-authoring` | 13105 | 8904 | 32.06% | 1765 | 1096 | 37.90% |
| `AA2-governed-authoring` | 13105 | 12880 | 1.72% | 1765 | 1593 | 9.75% |

## Assets and representative copied output

| Resource | SHA-256 | Bytes | Words |
| --- | --- | ---: | ---: |
| `assets/architecture-skeleton.md` | `348e00f3bdb0830160879dc7f3aee26073907b55c3c158082edfdde11692f9b5` | 1741 | 223 |
| `assets/adr-skeleton.md` | `65136a94503abd3e5bc67fafcaac577971a0b0bd796411175f3f8b6e202766d3` | 571 | 68 |
| `assets/diagram-styles.mmd` | `020be16bb4b01f1eb1a1605562ffd6b31af9e5ba2ee12b1a1e1735acb6378a56` | 362 | 37 |
| Representative copied set: all three assets once | derived from rows above | 2674 | 328 |

## Total package

The canonical package decreases from 17893 to 15554 bytes, a 13.07% reduction, and from 2400 to 1921 words, a 19.96% reduction. Both references add navigation and conditional ownership, but the removal of duplicate method prose and policy-bearing asset prompts makes the complete package smaller as well as reducing every loaded assembly.

These measurements are change-local evidence, not a permanent simplicity gate or tokenizer contract.
