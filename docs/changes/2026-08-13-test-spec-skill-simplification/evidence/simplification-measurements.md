# Test-Spec Simplification Measurements

## Method

Measurements use canonical authored Markdown, LF-normalized content, UTF-8 bytes, Unicode whitespace-separated words, documented load order, and each unique resource once. Procedural profile totals exclude copied output assets. Token estimates are omitted because the repository has no required pinned tokenizer for this acceptance surface.

## Loaded profiles and representative assemblies

| Surface | Baseline bytes | Final bytes | Delta | Baseline words | Final words | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `SKILL.md` | 16,766 | 12,136 | -4,630 (-27.6%) | 2,427 | 1,611 | -816 (-33.6%) |
| `TSA0-portable` | 25,419 | 20,787 | -4,632 (-18.2%) | 3,640 | 2,824 | -816 (-22.4%) |
| `TSA1-governed` | 25,419 | 25,080 | -339 (-1.3%) | 3,640 | 3,387 | -253 (-7.0%) |
| Full-create assembly | 30,324 | 25,404 | -4,920 (-16.2%) | 4,403 | 3,527 | -876 (-19.9%) |
| Bounded command-row revision | 25,880 | 21,247 | -4,633 (-17.9%) | 3,701 | 2,885 | -816 (-22.0%) |
| Complete package | 30,324 | 29,697 | -627 (-2.1%) | 4,403 | 4,090 | -313 (-7.1%) |

Both procedural profiles decrease in both required metrics. The governed profile improves less because it now loads a complete identity-bound creation, stale-restart, and revision contract that was previously mixed into the common file. The complete package still shrinks despite adding that reference.

## Final resources

| Resource | Bytes | Words | SHA-256 |
| --- | ---: | ---: | --- |
| `SKILL.md` | 12,136 | 1,611 | `e3137789160789ee484166f1e777c610a17e9e41dd82f55d9a4f3aa2d8ac62c1` |
| `references/boundary-first-method-v1.md` | 6,346 | 857 | `4268fbe89ecdfd7b79ca1321b8d6b19b2ed24e8adeda17cae8c319b087760f6f` |
| `references/boundary-first-proof-v1.md` | 2,305 | 356 | `ec8e8239c642bf340c4c8aba2105ae9783bced35230bb5bf6501b7b931e6cc4d` |
| `references/governed-test-spec-authoring.md` | 4,293 | 563 | `310c0c188d6a5b5f7c2b02bae257da7772834dcd5a4ffb8b24938ed28df28764` |
| `assets/test-spec-skeleton.md` | 2,763 | 443 | `cb2bd7f0218d9ba309b51a3a8e23525fbc4874035b85233818628cdb35768e77` |
| `assets/test-case.md` | 608 | 85 | `47997f45a571167a0b0db03870e9847d35721df68b83012f4605219d8362631f` |
| `assets/coverage-map-row.md` | 410 | 60 | `82feb2c51e1ff3f487645e166e505371da5b1ddb89ce8e4864e14108925bba79` |
| `assets/validation-command-row.md` | 460 | 61 | `6249c8ecd0b09ab056fab7c60b5038146db5e301703d22e558b0e8b5b723967c` |
| `assets/milestone-proof-row.md` | 376 | 54 | `4fffad383c69defefcbf86edd1b061afb1656dd0287f0c63fc0e0952abb39e1f` |

## Ownership result

The mapped-resource count increases from seven to eight because one governed procedure reference is added while the five-asset count remains unchanged. All six baseline duplication clusters now have one loaded owner: governed authoring, boundary method, boundary proof, structural bodies, validation-command shape, and milestone-proof shape. No cluster remains governed in both `SKILL.md` and a conditional reference or asset.
