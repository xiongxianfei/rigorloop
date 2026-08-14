# Project-Map Simplification Measurements

## Convention

Measurements use canonical authored files, LF-normalized content, UTF-8 bytes, Unicode whitespace-separated words, each unique resource once, and documented load order. Token estimates are omitted because the repository has no required pinned tokenizer for this assembly.

## Procedural assemblies

| Surface | Before bytes | After bytes | Byte change | Before words | After words | Word change |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `SKILL.md` | 15,545 | 11,727 | -24.56% | 2,297 | 1,610 | -29.91% |
| `PMA0-simple-root-create` | 15,545 | 11,727 | -24.56% | 2,297 | 1,610 | -29.91% |
| `PMA1-maintenance-or-coordinated` | 15,545 | 15,527 | -0.12% | 2,297 | 2,135 | -7.05% |
| Representative written-output assembly | 17,555 | 13,737 | -21.75% | 2,610 | 1,923 | -26.32% |
| Complete package | 17,555 | 17,537 | -0.10% | 2,610 | 2,448 | -6.21% |

Both real procedural assemblies decrease in both primary metrics. PMA1 has only a small byte reduction because the extracted transaction uses explicit identity and recovery wording, but it removes 162 loaded words and does not grow the total package.

## Final resources

| Resource | UTF-8 bytes | Words | SHA-256 |
| --- | ---: | ---: | --- |
| `skills/project-map/SKILL.md` | 11,727 | 1,610 | `ba1ae521fe2ad5992f945793725c70366fee79c54e924ec9ea5aa66a5a31e65a` |
| `skills/project-map/references/map-maintenance-and-area-coordination.md` | 3,800 | 525 | `d28ae2198d747e33b32e1fdbc2f0950c5f1b90e669f09a2d017ceae460b1b8ed` |
| `skills/project-map/assets/project-map-skeleton.md` | 2,010 | 313 | `1bfc68c053deac5df9124c4f630492b263043ae65c4dd524fe964f4490ba3efe` |

PMA1 concatenates `SKILL.md` then the conditional reference and has SHA-256 `2f5d199886c6ab0188df0cbb6ceeb9d596b523e1f08d17cd71c47642c6efd58c`. The representative written-output assembly concatenates `SKILL.md` then the skeleton. The complete package adds all three resources once.

## Ownership and package accounting

| Baseline duplicate cluster | Final owner |
| --- | --- |
| Operation and scope classification | `SKILL.md#Invocation-classification` |
| Evidence and freshness explanation | `SKILL.md#Map-metadata-and-freshness` and `#Evidence-and-confidence`, without conditional copies |
| Root/area coordination and recovery | Conditional maintenance and coordination reference |
| Map structural labels and registration columns | Skeleton only |
| Result shape and legacy migration | `SKILL.md#Output-skeleton` and `#Invocation-classification` |

The mapped-resource count increases from one to two because the package gains one conditional reference. The Markdown package-file count increases from two to three. Total package bytes nevertheless decrease by 18 and total words by 162, so relocation is not presented as deletion or hidden package growth.
