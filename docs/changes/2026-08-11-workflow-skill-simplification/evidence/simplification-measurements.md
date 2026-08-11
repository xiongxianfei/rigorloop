# Workflow Simplification Measurements

Measurement date: 2026-08-11
Baseline revision: `320b41f6`
Final canonical source measured: M3 implementation tree after cross-adapter compatibility repair
Convention: canonical authored files, LF-normalized text, Unicode whitespace-separated words, UTF-8 bytes, each unique resource counted once in documented load order. Token estimates are omitted because no pinned repository tokenizer is required.

## Resource identities and final size

| Resource | SHA-256 | Words | UTF-8 bytes |
| --- | --- | ---: | ---: |
| `SKILL.md` | `0e6d616777477eb27ed1c3c8adfc235549dd45f85afdac985ffab6adcd9b1f1c` | 2,710 | 20,223 |
| governed reference | `e7e533ecc3ab1e2b38c0b2b01d498cc6bf87035b613a1886b7002bb985e1aafb` | 568 | 4,601 |
| automation reference | `da189e873228d2258ed3756fc83381c43d31f07bb0d2c86bad77b62ab439fbc0` | 724 | 5,689 |
| guide reference | `c42d12d4d4d6a66bf123df6b6994b35c27cb46d16504d8fc74e573e9356ae82c` | 409 | 3,046 |
| boundary reference | `4268fbe89ecdfd7b79ca1321b8d6b19b2ed24e8adeda17cae8c319b087760f6f` | 857 | 6,346 |
| guide skeleton | `c0333144cbb631f1a10a6aee5a7228d1ad3dd0ee34093180fabb3854813bc3d9` | 1,236 | 9,551 |
| Total package | all six unique resources | 6,504 | 49,456 |

## Final assemblies

The boundary-first reference is independently additive and does not rename the base assembly. `WPB` reports the unique resources loaded through successful post-validation reclassification; before reclassification its entry set is the same as `WPS`.

| Assembly | Unique resources in load order | Words | UTF-8 bytes | With boundary words | With boundary bytes |
| --- | --- | ---: | ---: | ---: | ---: |
| `WP0` | skill | 2,710 | 20,223 | 3,567 | 26,569 |
| `WP1` | skill, governed | 3,278 | 24,824 | 4,135 | 31,170 |
| `WP2` | skill, governed, automation | 4,002 | 30,513 | 4,859 | 36,859 |
| `WP3` | skill, guide, skeleton | 4,355 | 32,820 | 5,212 | 39,166 |
| `WP4` | skill, governed, guide, skeleton | 4,923 | 37,421 | 5,780 | 43,767 |
| `WPB` | skill, automation, governed | 4,002 | 30,513 | 4,859 | 36,859 |
| `WPS` | skill, automation | 3,434 | 25,912 | 4,291 | 32,258 |

## Before and after

| Surface | Word delta | Word change | Byte delta | Byte change |
| --- | ---: | ---: | ---: | ---: |
| `WP0` | -1,623 | -37.5% | -11,851 | -36.9% |
| `WP1` | -1,055 | -24.3% | -7,250 | -22.6% |
| `WP2` | -331 | -7.6% | -1,561 | -4.9% |
| `WP3` | -1,214 | -21.8% | -8,805 | -21.2% |
| `WP4` | -646 | -11.6% | -4,204 | -10.1% |
| `WPB` | -331 | -7.6% | -1,561 | -4.9% |
| `WPS` | -899 | -20.7% | -6,162 | -19.2% |
| Total package | +78 | +1.2% | +1,485 | +3.1% |

The desired non-normative 35-50 percent `WP0` target is met. Every valid assembly is smaller. The 3.1 percent package-byte increase is justified by explicit predicate, trigger, ownership, bootstrap, failure, and cross-adapter invocation clauses that enable safe progressive disclosure without losing portability; maintenance content was relocated and clarified rather than misreported as deletion.

## Structural ownership counts

| Metric | Before | After | Interpretation |
| --- | ---: | ---: | --- |
| Mapped resources | 2 | 5 | Three conditional procedures are now explicit package members. |
| Inline copy-and-fill result structures | 1 | 1 | Workflow retains its compact universal result block; the guide skeleton remains the only guide structure. |
| Explicit removed duplicate clusters | 1 | 0 | Repeated orientation/result restatement now has one compact owner. |

No word, byte, line, or token value becomes a permanent acceptance gate.
