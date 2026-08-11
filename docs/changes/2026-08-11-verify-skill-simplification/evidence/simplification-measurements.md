# Verify simplification measurements

## Convention

Measurements use canonical authored files with LF-normalized text, Unicode whitespace-separated words, and UTF-8 bytes. Each unique resource is counted once in profile load order: `SKILL.md`, branch-readiness reference when triggered, then boundary-first reference when independently triggered. Resource totals below sum file measurements without charging a synthetic separator byte.

No tokenizer was added. The percentage target remains advisory.

## Resource comparison

| Resource | Before lines | After lines | Before words | After words | Before bytes | After bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `SKILL.md` | 308 | 205 | 2,896 | 2,140 | 20,715 | 15,608 |
| branch-readiness reference | 0 | 46 | 0 | 502 | 0 | 3,827 |
| boundary-first reference | 110 | 110 | 857 | 857 | 6,346 | 6,346 |
| Total package | 418 | 361 | 3,753 | 3,499 | 27,061 | 25,781 |

The common path is 33.4% shorter by lines, 26.1% smaller by words, and 24.7% smaller by bytes. Total package content also decreases: 6.8% by words and 4.7% by bytes.

## Loaded profiles

| Profile | Loaded resources | Before words | After words | Word delta | Before bytes | After bytes | Byte delta |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `VP0-scoped` | skill | 2,896 | 2,140 | -26.1% | 20,715 | 15,608 | -24.7% |
| `VP0B-scoped-boundary` | skill + boundary | 3,753 | 2,997 | -20.1% | 27,061 | 21,954 | -18.9% |
| `VP1-final-readiness` | skill + branch | 2,896 | 2,642 | -8.8% | 20,715 | 19,435 | -6.2% |
| `VP1B-final-readiness-boundary` | skill + branch + boundary | 3,753 | 3,499 | -6.8% | 27,061 | 25,781 | -4.7% |

Before the split, final-readiness procedure was always inline, so both scoped and final profiles loaded the same main file. The new reference adds no final-profile growth; every profile and the package are smaller.

## Ownership and structure

| Metric | Before | After | Interpretation |
| --- | ---: | ---: | --- |
| Rule clusters with a recorded owner | unrecorded | 16 of 16 | No behaviorally significant rule is unaccounted for. |
| Explicit duplicate dispositions | unrecorded | 1 | Repeated quick-guide/output orientation has one retained owner. |
| Final procedure clusters inline | 3 | 0 | Prerequisites, evidence composition, and verdict completion now have one conditional owner. |
| Inline result templates | 1 | 1 | The compact profile-neutral result remains inline as approved. |
| Mapped resources | 1 | 2 | One coherent final-readiness procedure was added; boundary-first is unchanged. |

## Interpretation

The result satisfies the normative acceptance rule: scoped loading is materially reduced, final profiles do not grow, the total package shrinks, every semantic rule has one disposition, and semantic review passes. The 30-40% VP0 planning range is not met by words or bytes because universal boundary-first, portability, formal-review closeout, evidence truthfulness, claim, and result contracts must remain inline; further extraction would weaken the self-sufficient scoped contract.
