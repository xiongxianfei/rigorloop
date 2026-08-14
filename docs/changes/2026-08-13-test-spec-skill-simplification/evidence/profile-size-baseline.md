# Test-Spec Profile Size Baseline

Measurement uses canonical authored files, LF-normalized content, UTF-8 bytes, Unicode whitespace-separated words, each unique resource once, and the documented load order. Token estimates are omitted because no existing pinned implementation is needed for acceptance.

| Surface | Resources | Bytes | Words |
| --- | --- | ---: | ---: |
| `SKILL.md` | `SKILL.md` | 16,766 | 2,427 |
| `TSA0-portable` | `SKILL.md`, boundary method, boundary proof | 25,419 | 3,640 |
| `TSA1-governed` equivalent | Current `SKILL.md`, boundary method, boundary proof; governed procedure is still inline | 25,419 | 3,640 |
| Full-create assembly | Portable procedure plus all five assets | 30,324 | 4,403 |
| Bounded command-row revision | Portable procedure plus validation-command row | 25,880 | 3,701 |
| Complete current package | Every Markdown resource under `skills/test-spec/` | 30,324 | 4,403 |

| Resource | SHA-256 | Bytes | Words |
| --- | --- | ---: | ---: |
| `SKILL.md` | `97489345c529b2ff2909dd55e2272cdf8608faf55f615925d1e69ff504a7e320` | 16,766 | 2,427 |
| `references/boundary-first-method-v1.md` | `4268fbe89ecdfd7b79ca1321b8d6b19b2ed24e8adeda17cae8c319b087760f6f` | 6,346 | 857 |
| `references/boundary-first-proof-v1.md` | `ec8e8239c642bf340c4c8aba2105ae9783bced35230bb5bf6501b7b931e6cc4d` | 2,305 | 356 |
| `assets/test-spec-skeleton.md` | `89e19447fe17a5c2ba35da7f85b81bad8fba37c88feb3ed324b8086eab969bc1` | 3,046 | 503 |
| `assets/test-case.md` | `47997f45a571167a0b0db03870e9847d35721df68b83012f4605219d8362631f` | 608 | 85 |
| `assets/coverage-map-row.md` | `82feb2c51e1ff3f487645e166e505371da5b1ddb89ce8e4864e14108925bba79` | 410 | 60 |
| `assets/validation-command-row.md` | `6249c8ecd0b09ab056fab7c60b5038146db5e301703d22e558b0e8b5b723967c` | 460 | 61 |
| `assets/milestone-proof-row.md` | `4fffad383c69defefcbf86edd1b061afb1656dd0287f0c63fc0e0952abb39e1f` | 376 | 54 |

The baseline duplication clusters are governed authoring transition and retry procedure, repeated boundary method and proof guidance, repeated structural body examples, validation-command field restatement, milestone-proof field restatement, and output assembly instructions. M3 must report each final owner and both loaded profiles separately from total package size.
