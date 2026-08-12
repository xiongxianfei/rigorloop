# Proposal-Review Simplification Measurements

Milestone: M3
Date: 2026-08-12
Baseline: `f6a239c4`
Final package: current M3 canonical files

Measurements use canonical authored files, LF-normalized UTF-8 bytes, Unicode whitespace-separated words, documented load order, and one count per unique resource. No tokenizer or target-agent runtime was used.

## Resource measurements

| Resource | Baseline words | Final words | Baseline bytes | Final bytes |
| --- | ---: | ---: | ---: | ---: |
| `SKILL.md` | 2295 | 1959 | 16879 | 14491 |
| `references/conditional-proposal-gates.md` | 0 | 445 | 0 | 3360 |
| `references/proposal-review-recording-and-settlement.md` | 0 | 678 | 0 | 5365 |
| `assets/review-result-skeleton.md` | 135 | 223 | 1039 | 1728 |
| `assets/material-finding.md` | 55 | 55 | 457 | 457 |
| Total package | 2485 | 3360 | 18375 | 25401 |

`SKILL.md` decreased by 336 words (14.6%) and 2388 bytes (14.1%). The total package increased by 875 words (35.2%) and 7026 bytes (38.2%) because two conditional procedures and four result groups are now explicit package resources. This is honest relocation and structural expansion, not deletion.

## Loaded assemblies

| Assembly | Baseline words | Final words | Word delta | Baseline bytes | Final bytes | Byte delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `PRR0-core` | 2430 | 2182 | -248 (-10.2%) | 17918 | 16219 | -1699 (-9.5%) |
| `PRR0G-context-gated` | 2430 | 2627 | +197 (+8.1%) | 17918 | 19579 | +1661 (+9.3%) |
| `PRR1-recorded` | 2430 | 2860 | +430 (+17.7%) | 17918 | 21584 | +3666 (+20.5%) |
| `PRR1G-recorded-context-gated` | 2430 | 3305 | +875 (+36.0%) | 17918 | 24944 | +7026 (+39.2%) |

`PRR0-core` is materially smaller in both portable metrics. Recorded and specialized invocations intentionally load the procedure they require; their growth is justified by closed operational modes, retry behavior, missing-resource stops, conditional gate composition, and explicit result applicability that were previously mixed or implicit.

## Ownership measurements

| Metric | Baseline | Final |
| --- | ---: | ---: |
| Rule clusters with one disposition | not classified | 21 |
| Removed duplicate clusters | 0 | 1 |
| Inline result templates | 1 | 0 |
| Mapped references | 0 | 2 |
| Mapped structural assets | 2 | 2 |

The advisory 30-45% target was not reached. Acceptance does not use that percentage: the approved contract requires material `PRR0` reduction, complete rule disposition, one owner per duplicate cluster, separate package accounting, and semantic preservation. Those conditions are satisfied.
