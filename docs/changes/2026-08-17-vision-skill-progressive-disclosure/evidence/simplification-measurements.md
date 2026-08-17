# Vision Skill Simplification Measurements

## Method

Measurements use canonical authored files with LF normalization, Unicode whitespace-separated words, UTF-8 bytes, and each unique loaded procedural resource counted once in `SKILL.md`, strategic-reference, README-reference order. The flat baseline is 2,268 words and 15,845 bytes.

## Procedural resources

| Resource | Words | Bytes |
| --- | ---: | ---: |
| `SKILL.md` | 1,262 | 9,945 |
| `references/strategic-vision-authoring.md` | 492 | 3,659 |
| `references/readme-vision-sync.md` | 303 | 2,131 |

## Loaded assemblies

| Assembly | Loaded procedure | Words | Reduction | Bytes | Reduction |
| --- | --- | ---: | ---: | ---: | ---: |
| `VA0-readme-sync` | main + README | 1,565 | 703 (31.0%) | 12,076 | 3,769 (23.8%) |
| `VA0S-readme-skip` | main | 1,262 | 1,006 (44.4%) | 9,945 | 5,900 (37.2%) |
| `VA1-editorial-sync` | main + README | 1,565 | 703 (31.0%) | 12,076 | 3,769 (23.8%) |
| `VA1S-editorial-skip` | main | 1,262 | 1,006 (44.4%) | 9,945 | 5,900 (37.2%) |
| `VA2-strategic-sync` | main + strategic + README | 2,057 | 211 (9.3%) | 15,735 | 110 (0.7%) |
| `VA2S-strategic-skip` | main + strategic | 1,754 | 514 (22.7%) | 13,604 | 2,241 (14.1%) |

Every primary and secondary procedural assembly decreases in both measures. Primary profiles are `VA0`, `VA1`, and `VA2`; secondary skip variants do not substitute for their acceptance.

## Structural assets and total package

| Surface | Words | Bytes |
| --- | ---: | ---: |
| `assets/vision-skeleton.md` | 106 | 763 |
| `assets/strategic-positioning-skeleton.md` | 80 | 678 |
| Both assets | 186 | 1,441 |
| Complete final package | 2,243 | 17,176 |

Compared with the flat package, the final package has 25 fewer words (1.1% reduction) and 1,331 more bytes (8.4% growth). The byte growth is accepted because repeated output structure now has two explicit, independently copied owners, while every actually loaded procedural path is smaller and policy remains outside the assets.

## Conclusion

The change is progressive disclosure, not deletion disguised by relocation. Loaded procedure improves for all six supported paths; asset and total-package costs remain explicit.
