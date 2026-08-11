# Test-Spec-Review Simplification Measurements

Milestone: M3  
Date: 2026-08-11  
Baseline commit: `9b0cd7d4`  
After implementation commit: `76b1f857`

Measurements use canonical authored files, LF-normalized UTF-8 bytes, Unicode whitespace-separated words, and one count per unique loaded resource in documented load order. No tokenizer estimate is used.

## Resource measurements

| Resource | Before lines | After lines | Before words | After words | Before bytes | After bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `SKILL.md` | 359 | 315 | 2722 | 2136 | 19768 | 16105 |
| recording and settlement reference | 0 | 109 | 0 | 658 | 0 | 4964 |
| boundary method reference | 110 | 110 | 857 | 857 | 6346 | 6346 |
| boundary proof reference | 41 | 41 | 356 | 356 | 2305 | 2305 |
| result asset | 25 | 25 | 132 | 132 | 952 | 952 |
| finding asset | 14 | 14 | 55 | 55 | 460 | 460 |
| Total package | 549 | 614 | 4122 | 4194 | 29831 | 31132 |

The four pre-existing resources retain byte identity. The new reference has SHA-256 `5c3540fe5c096d9316d0adf4875d829604c2fa62506851d40e35299cabe78b29`.

## Loaded assemblies

| Assembly | Before words | After words | Word delta | Before bytes | After bytes | Byte delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `TSR0-isolated` | 2722 | 2136 | -586 (-21.53%) | 19768 | 16105 | -3663 (-18.53%) |
| `TSR0B-isolated-boundary` | 3935 | 3349 | -586 (-14.89%) | 28419 | 24756 | -3663 (-12.89%) |
| recording overlay | 132 | 790 | +658 | 952 | 5916 | +4964 |
| `TSR1-formal` | 2854 | 2926 | +72 (+2.52%) | 20720 | 22021 | +1301 (+6.28%) |
| `TSR1B-formal-boundary` | 4067 | 4139 | +72 (+1.77%) | 29371 | 30672 | +1301 (+4.43%) |
| material-finding addition | 55 | 55 | 0 | 460 | 460 | 0 |
| Total package | 4122 | 4194 | +72 (+1.75%) | 29831 | 31132 | +1301 (+4.36%) |

The ordinary path is materially smaller. It does not reach the advisory 30-40 percent planning target because classification, proof quality, statuses, stops, claim boundaries, resource failure, isolation, staleness, evidence reading, and generated-Markdown readability are universal and remain inline. Removing any of those solely to hit the target would weaken the self-sufficient advisory profile.

The formal profile and package grow slightly because the previously interleaved recording and settlement mechanics now form one complete, conditionally loaded procedure with explicit shared-recording and formal-only sections. The delta is disclosed as relocation and clarification, not deletion. Formal invocations pay that cost; ordinary invocations no longer do.

## Ownership measurements

| Measure | Before | After |
| --- | ---: | ---: |
| Behaviorally significant rule clusters accounted for | 19 | 19 |
| Identified repeated clusters with multiple prose owners | 6 | 0 |
| Inline copy-and-fill templates | 0 | 0 |
| Mapped references | 2 | 3 |
| Mapped assets | 2 | 2 |

The six reviewed duplication clusters were quick-guide, routing, stop, recording, finding, and output structure. Each now has one policy or structural owner. The additional mapped reference is the intentional progressive-disclosure boundary; it does not own universal review policy.

## Acceptance interpretation

The change meets the normative success contract: all 19 rules have one disposition, all 16 exact literal dependencies are classified, duplicate ownership is removed, the ordinary profile materially shrinks, total movement is reported separately, and semantic review found no behavioral loss. The advisory percentage is not used as a semantic gate, and no permanent size or tokenizer validator was added.
