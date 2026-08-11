# Workflow Simplification Measurements

Measurement date: 2026-08-11
Baseline revision: `320b41f6`
Final canonical source measured: implementation tree after cross-adapter and PR-gate compatibility repairs
Convention: canonical authored files, LF-normalized text, Unicode whitespace-separated words, UTF-8 bytes, each unique resource counted once in documented load order. Token estimates are omitted because no pinned repository tokenizer is required.

## Resource identities and final size

| Resource | SHA-256 | Words | UTF-8 bytes |
| --- | --- | ---: | ---: |
| `SKILL.md` | `a18d54bafd74dc7462080029a15bee6f25f3353b76450f291e43583462dd3644` | 2,742 | 20,532 |
| governed reference | `e7e533ecc3ab1e2b38c0b2b01d498cc6bf87035b613a1886b7002bb985e1aafb` | 568 | 4,601 |
| automation reference | `da189e873228d2258ed3756fc83381c43d31f07bb0d2c86bad77b62ab439fbc0` | 724 | 5,689 |
| guide reference | `c42d12d4d4d6a66bf123df6b6994b35c27cb46d16504d8fc74e573e9356ae82c` | 409 | 3,046 |
| boundary reference | `4268fbe89ecdfd7b79ca1321b8d6b19b2ed24e8adeda17cae8c319b087760f6f` | 857 | 6,346 |
| guide skeleton | `c0333144cbb631f1a10a6aee5a7228d1ad3dd0ee34093180fabb3854813bc3d9` | 1,236 | 9,551 |
| Total package | all six unique resources | 6,536 | 49,765 |

## Final assemblies

The boundary-first reference is independently additive and does not rename the base assembly. `WPB` reports the unique resources loaded through successful post-validation reclassification; before reclassification its entry set is the same as `WPS`.

| Assembly | Unique resources in load order | Words | UTF-8 bytes | With boundary words | With boundary bytes |
| --- | --- | ---: | ---: | ---: | ---: |
| `WP0` | skill | 2,742 | 20,532 | 3,599 | 26,878 |
| `WP1` | skill, governed | 3,310 | 25,133 | 4,167 | 31,479 |
| `WP2` | skill, governed, automation | 4,034 | 30,822 | 4,891 | 37,168 |
| `WP3` | skill, guide, skeleton | 4,387 | 33,129 | 5,244 | 39,475 |
| `WP4` | skill, governed, guide, skeleton | 4,955 | 37,730 | 5,812 | 44,076 |
| `WPB` | skill, automation, governed | 4,034 | 30,822 | 4,891 | 37,168 |
| `WPS` | skill, automation | 3,466 | 26,221 | 4,323 | 32,567 |

## Before and after

| Surface | Word delta | Word change | Byte delta | Byte change |
| --- | ---: | ---: | ---: | ---: |
| `WP0` | -1,591 | -36.7% | -11,542 | -36.0% |
| `WP1` | -1,023 | -23.6% | -6,941 | -21.6% |
| `WP2` | -299 | -6.9% | -1,252 | -3.9% |
| `WP3` | -1,182 | -21.2% | -8,496 | -20.4% |
| `WP4` | -614 | -11.0% | -3,895 | -9.4% |
| `WPB` | -299 | -6.9% | -1,252 | -3.9% |
| `WPS` | -867 | -20.0% | -5,853 | -18.2% |
| Total package | +110 | +1.7% | +1,794 | +3.7% |

The desired non-normative 35-50 percent `WP0` target is met. Every valid assembly is smaller. The 3.7 percent package-byte increase is justified by explicit predicate, trigger, ownership, bootstrap, failure, cross-adapter invocation, closed review-disposition, and portable plan-path clauses that enable safe progressive disclosure without losing portability; maintenance content was relocated and clarified rather than misreported as deletion.

## Structural ownership counts

| Metric | Before | After | Interpretation |
| --- | ---: | ---: | --- |
| Mapped resources | 2 | 5 | Three conditional procedures are now explicit package members. |
| Inline copy-and-fill result structures | 1 | 1 | Workflow retains its compact universal result block; the guide skeleton remains the only guide structure. |
| Explicit removed duplicate clusters | 1 | 0 | Repeated orientation/result restatement now has one compact owner. |

No word, byte, line, or token value becomes a permanent acceptance gate.
