# Workflow Simplification Measurements

Measurement date: 2026-08-11
Baseline revision: `320b41f6`
Final canonical source measured: implementation tree after cross-adapter and PR-gate compatibility repairs
Convention: canonical authored files, LF-normalized text, Unicode whitespace-separated words, UTF-8 bytes, each unique resource counted once in documented load order. Token estimates are omitted because no pinned repository tokenizer is required.

## Resource identities and final size

| Resource | SHA-256 | Words | UTF-8 bytes |
| --- | --- | ---: | ---: |
| `SKILL.md` | `adeb3aa29dab0792d1f3e2d0be96eaa127c29027a8af491fe4927a870a2f6f9d` | 2,719 | 20,323 |
| governed reference | `e7e533ecc3ab1e2b38c0b2b01d498cc6bf87035b613a1886b7002bb985e1aafb` | 568 | 4,601 |
| automation reference | `da189e873228d2258ed3756fc83381c43d31f07bb0d2c86bad77b62ab439fbc0` | 724 | 5,689 |
| guide reference | `c42d12d4d4d6a66bf123df6b6994b35c27cb46d16504d8fc74e573e9356ae82c` | 409 | 3,046 |
| boundary reference | `4268fbe89ecdfd7b79ca1321b8d6b19b2ed24e8adeda17cae8c319b087760f6f` | 857 | 6,346 |
| guide skeleton | `c0333144cbb631f1a10a6aee5a7228d1ad3dd0ee34093180fabb3854813bc3d9` | 1,236 | 9,551 |
| Total package | all six unique resources | 6,513 | 49,556 |

## Final assemblies

The boundary-first reference is independently additive and does not rename the base assembly. `WPB` reports the unique resources loaded through successful post-validation reclassification; before reclassification its entry set is the same as `WPS`.

| Assembly | Unique resources in load order | Words | UTF-8 bytes | With boundary words | With boundary bytes |
| --- | --- | ---: | ---: | ---: | ---: |
| `WP0` | skill | 2,719 | 20,323 | 3,576 | 26,669 |
| `WP1` | skill, governed | 3,287 | 24,924 | 4,144 | 31,270 |
| `WP2` | skill, governed, automation | 4,011 | 30,613 | 4,868 | 36,959 |
| `WP3` | skill, guide, skeleton | 4,364 | 32,920 | 5,221 | 39,266 |
| `WP4` | skill, governed, guide, skeleton | 4,932 | 37,521 | 5,789 | 43,867 |
| `WPB` | skill, automation, governed | 4,011 | 30,613 | 4,868 | 36,959 |
| `WPS` | skill, automation | 3,443 | 26,012 | 4,300 | 32,358 |

## Before and after

| Surface | Word delta | Word change | Byte delta | Byte change |
| --- | ---: | ---: | ---: | ---: |
| `WP0` | -1,614 | -37.2% | -11,751 | -36.6% |
| `WP1` | -1,046 | -24.1% | -7,150 | -22.3% |
| `WP2` | -322 | -7.4% | -1,461 | -4.6% |
| `WP3` | -1,205 | -21.6% | -8,705 | -20.9% |
| `WP4` | -637 | -11.4% | -4,104 | -9.9% |
| `WPB` | -322 | -7.4% | -1,461 | -4.6% |
| `WPS` | -890 | -20.5% | -6,062 | -18.9% |
| Total package | +87 | +1.4% | +1,585 | +3.3% |

The desired non-normative 35-50 percent `WP0` target is met. Every valid assembly is smaller. The 3.3 percent package-byte increase is justified by explicit predicate, trigger, ownership, bootstrap, failure, cross-adapter invocation, and closed review-disposition clauses that enable safe progressive disclosure without losing portability; maintenance content was relocated and clarified rather than misreported as deletion.

## Structural ownership counts

| Metric | Before | After | Interpretation |
| --- | ---: | ---: | --- |
| Mapped resources | 2 | 5 | Three conditional procedures are now explicit package members. |
| Inline copy-and-fill result structures | 1 | 1 | Workflow retains its compact universal result block; the guide skeleton remains the only guide structure. |
| Explicit removed duplicate clusters | 1 | 0 | Repeated orientation/result restatement now has one compact owner. |

No word, byte, line, or token value becomes a permanent acceptance gate.
