# PR skill simplification measurements

## Result

Both real procedural profiles are smaller than the flat baseline in Unicode
whitespace-separated words and LF-normalized UTF-8 bytes.

| Surface | Authored resources | Baseline words | Final words | Change | Baseline bytes | Final bytes | Change |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| PR0 portable | `skills/pr/SKILL.md` | 1,678 | 1,373 | -305 (-18.2%) | 11,375 | 10,389 | -986 (-8.7%) |
| PR1 governed | `SKILL.md` plus `references/governed-pr-readiness.md` | 1,678 | 1,494 | -184 (-11.0%) | 11,375 | 11,303 | -72 (-0.6%) |
| PR-body asset | `assets/pr-body-skeleton.md` | 0 | 230 | +230 | 0 | 1,312 | +1,312 |
| Representative portable body assembly | PR0 plus the copied asset | 1,678 | 1,603 | -75 | 11,375 | 11,701 | +326 |
| Representative governed body assembly / total package | all three authored resources | 1,678 | 1,724 | +46 | 11,375 | 12,615 | +1,240 |

The representative and total-package growth is explicit. It comes from making
the body layout a reusable structural asset and governed aggregation a separately
mapped resource. It is not presented as deletion. The acceptance surfaces are
the actual loaded procedural profiles, PR0 and PR1, and both decreased.

## Final authored identities

| Resource | Words | UTF-8 bytes | SHA-256 |
| --- | ---: | ---: | --- |
| `skills/pr/SKILL.md` | 1,373 | 10,389 | `ed1cedd7e8f0bd7bd7257c9a803d3a40ea30e9d82bdd2077e294a8774128aaf6` |
| `skills/pr/references/governed-pr-readiness.md` | 121 | 914 | `b97883eccc9800aad7aba16a3a4bbe21719f42c8a948413d0ec67794bb24ecaa` |
| `skills/pr/assets/pr-body-skeleton.md` | 230 | 1,312 | `946247ff193e44814730c115b58b6d8828cf6d2416111a5d80fc45a3abf859ab` |

Measurements use canonical authored files, LF line endings, UTF-8 bytes, and
each unique resource once. Assets are excluded from procedural-profile totals
and reported separately.
