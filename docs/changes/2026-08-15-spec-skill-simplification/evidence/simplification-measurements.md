# Spec Simplification Measurements

- Baseline revision: `3b0daafc`
- Current canonical revision: working tree after `791565c3`
- Normalization: UTF-8 with line endings normalized to LF
- Word convention: Unicode whitespace-separated words
- Assembly convention: each unique procedural resource once in load order; copied structure reported separately

## Canonical identities

| Resource | SHA-256 | Words | UTF-8 bytes |
| --- | --- | ---: | ---: |
| `skills/spec/SKILL.md` | `cd70ac390f8c1dd81e1efc1a74c1cc6d2ae9c7259af76f07b777f596d24c3293` | 1198 | 9292 |
| `skills/spec/references/boundary-first-method-v1.md` | `4268fbe89ecdfd7b79ca1321b8d6b19b2ed24e8adeda17cae8c319b087760f6f` | 857 | 6346 |
| `skills/spec/references/boundary-first-feature-authoring-v1.md` | `962180f3b6d2699c1001fe0c2792f9e8bb3c9c60a7c7f2053dfb73fdf99df7fe` | 350 | 2324 |
| `skills/spec/references/governed-spec-authoring.md` | `035d97768049a7405e13931206b9b44048eee0d121ad9b2dbb95ecc71454b755` | 444 | 3527 |
| `skills/spec/assets/spec-skeleton.md` | `11df4fe2aeb3ba55271bd321acc960a88b9245ad1eaff21cca700921b3018940` | 218 | 1625 |

## Loaded procedural profiles

| Profile | Loaded resources | Baseline words | Current words | Word change | Baseline bytes | Current bytes | Byte change |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `SA0-portable` | core; method; feature authoring | 3020 | 2405 | -615 (-20.36%) | 21523 | 17962 | -3561 (-16.55%) |
| `SA1-governed` | SA0; governed authoring | 3020 | 2849 | -171 (-5.66%) | 21523 | 21489 | -34 (-0.16%) |

Both real procedural profiles decrease. The governed byte reduction is deliberately small because the accepted M2 correction keeps every R21-R42 identity and preservation boundary explicit.

## Structural and package totals

| Measurement | Baseline words | Current words | Word change | Baseline bytes | Current bytes | Byte change |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Representative skeleton | 209 | 218 | +9 | 1564 | 1625 | +61 |
| Total canonical package | 3229 | 3067 | -162 (-5.02%) | 23087 | 23114 | +27 (+0.12%) |

The package adds one governed reference and one insertion marker. Total bytes therefore increase by 27 while total words and both loaded profiles decrease. This is reported as relocation and explicit conditional authority, not deletion.

## Accounting limits

No tokenizer estimate is reported because no repository-owned pinned tokenizer is needed for acceptance. These metrics are change-local evidence and do not create a permanent simplicity threshold.
