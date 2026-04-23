# Multi-agent adapters first public release review resolution

## Scope

This record captures material review feedback for the M1 adapter portability core.

## Review items

| Source | Item | Decision | Action | Rationale |
| --- | --- | --- | --- | --- |
| M1 code review | Manifest exclusion reasons were rendered as unquoted YAML scalars, so colon-bearing reasons such as unsupported frontmatter could make `dist/adapters/manifest.yaml` invalid. | accepted | quoted generated manifest reason strings and added an unsupported-frontmatter regression test | The manifest is release evidence for M2 and must remain parseable for every generated human-readable exclusion reason. |
| M1 rereview | The portable-core gate could mark a skill portable even when its Markdown instruction body was not Agent Skills-compatible. | accepted | reused the repository skill body validator inside `evaluate_skill` and added an invalid-body fixture | `R17` requires portable skills to have valid `SKILL.md` structure, not only parseable frontmatter. |
| M1 rereview | Test spec `T4` required a partial-portability fixture for a skill portable to Codex and Claude Code but not opencode, but no such fixture or assertion existed. | accepted | added `partial-portability` and explicit opencode-incompatibility handling with manifest coverage | Edge case 9 requires exact adapter lists and a reason when a skill is non-portable overall. |

## Summary

Accepted items are implemented in the M1 review-resolution follow-ups. No review items were rejected or deferred.
