# Architecture-Review Simplification Measurements

- Measurement basis: canonical authored files, LF normalization, Unicode whitespace-separated words, UTF-8 bytes, and each loaded procedure counted once in `SKILL.md`, method-reference, recording-reference order.
- Baseline identity: `f7faa8f919317eb55e1d8da0c86451d99d7bce566b6ed50cd57f66e99bdcb4a9`

## Loaded profiles

| Profile | Before bytes | After bytes | Byte delta | Before words | After words | Word delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| ARR0 | 15,982 | 7,784 | -8,198 | 2,192 | 977 | -1,215 |
| ARR0M | 15,982 | 10,366 | -5,616 | 2,192 | 1,301 | -891 |
| ARR1 | 15,982 | 13,313 | -2,669 | 2,192 | 1,672 | -520 |
| ARR1M | 15,982 | 15,895 | -87 | 2,192 | 1,996 | -196 |

Both required formal profiles decrease in words and bytes. ARR1 decreases 16.7 percent by bytes and 23.7 percent by words. ARR1M decreases 0.5 percent by bytes and 8.9 percent by words.

## Canonical resources

| Resource | Bytes | Words | SHA-256 |
| --- | ---: | ---: | --- |
| `SKILL.md` | 7,784 | 977 | `ece1cb196bc24ed41450d84068481ae5f79cbb813c19acc8c3db4352e05a9c16` |
| `architecture-package-review.md` | 2,582 | 324 | `08ef88484daee03f9d500b4a9a09effe62e0d96c74e8c6bc27699dc5a0c43503` |
| `architecture-review-recording-and-settlement.md` | 5,529 | 695 | `7b7671ecc330152490d721d92859dcb59898b77f3aef661bc0676b80d0e69fc1` |
| Total canonical package | 15,895 | 1,996 | `cdaf9bbc212bee39073c27de0b595574c44401e3f18cd938f32abf3c21b942fd` |

The total canonical package decreases by 87 bytes and 196 words. No relocation is presented as deletion; each resource and the full loaded assemblies remain visible.
