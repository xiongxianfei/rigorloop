# Simplification Measurements

Date: 2026-08-10
Method: exact CMD10 and CMD11 from the approved test spec

## Before and after

| Metric | Before | After | Delta |
| --- | ---: | ---: | ---: |
| `SKILL.md` lines | 518 | 355 | -163 (-31.5%) |
| `SKILL.md` words | 4514 | 2647 | -1867 (-41.4%) |
| `SKILL.md` estimated tokens | 8160 | 4813 | -3347 (-41.0%) |
| Conditional-reference words | 0 | 886 | +886 |
| Conditional-reference estimated tokens | 0 | 1749 | +1749 |
| Total package words | 5569 | 4588 | -981 (-17.6%) |
| Total package estimated tokens | 10116 | 8518 | -1598 (-15.8%) |
| Duplicated rule clusters | 7 | 0 | -7 |
| Inline templates | 1 | 0 | -1 |
| Mapped resources | 3 | 4 | +1 |

CMD10 independently reported `code-review/SKILL.md` at 19,251 bytes, 355
lines, and 4,813 estimated tokens. CMD11 accounted for every Markdown file in
the package and used the same repository estimator.

## Interpretation

The non-normative planning target is met for common-path words and estimated
tokens. More importantly, every identified duplicate cluster has one owner,
the full inline templates are gone, and the total package shrank rather than
merely shifting maintenance cost into a reference. The one-resource increase is
the approved conditional automation reference. No line, word, token, or prose
metric was added as a permanent validation gate.
