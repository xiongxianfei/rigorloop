# Spec-Family Readability Pass Behavior Preservation

## Status

active

This artifact records source-to-destination preservation proof for the
presentation-only readability pass. It is scoped by milestone.

## M1. Spec Skill Readability

### Same-slice scope

| Surface | Treatment |
| --- | --- |
| `skills/spec/SKILL.md` | Tabulate required-section guidance, add authoritative closed-enum surfaces, and replace duplicate inline enum lists with enum references. |
| `scripts/test-skill-validator.py` | Align the downstream status-settlement regression fixture with the settlement-result enum authority while preserving coverage that first-slice skills expose settlement result reporting. |
| Produced spec artifact contract | Preserve required sections, output skeleton order, status lifecycle values, settlement behavior, rules, and handoff boundaries. |
| Routing description | Unchanged. |
| Packaging, generated adapter skill bodies, build-time partials | Unchanged in M1. |

### Content-preservation matrix

| Source content | Existing location | New location | Change type | Preservation proof |
| --- | --- | --- | --- | --- |
| Required spec section list: `Status`; `Related proposal`; `Goal and context`; `Glossary`; `Examples first`; `Requirements`; `Inputs and outputs`; `State and invariants`; `Error and boundary behavior`; `Compatibility and migration`; `Observability`; `Security and privacy`; `Accessibility and UX`; `Performance expectations`; `Edge cases`; `Non-goals`; `Acceptance criteria`; `Open questions`; `Next artifacts`; `Follow-on artifacts`; `Readiness` | `skills/spec/SKILL.md`, baseline `## Required sections`, lines 108-110 | `skills/spec/SKILL.md`, edited `## Required sections` table, lines 108-134 | tabulated | Same 21 section names, same order, no section added or removed. |
| Applicability guidance: use `None`, `not applicable`, or a short rationale for sections that do not apply; `Follow-on artifacts`, when present before real follow-ons exist, says `None yet`. | `skills/spec/SKILL.md`, baseline `## Required sections`, line 112 | `skills/spec/SKILL.md`, edited `## Required sections`, line 136 | unchanged | Sentence preserved verbatim. |
| Settlement-result values: `updated`, `blocked`, `not-needed` | `skills/spec/SKILL.md`, baseline upstream status settlement report skeleton, line 75 | `skills/spec/SKILL.md`, edited `## Closed enums`, lines 173-179 | fenced | Same spelling and membership; report skeleton references `<settlement result>` instead of restating the full list. |
| Spec-status values: `draft`, `approved`, `abandoned`, `superseded`, `archived` | `skills/spec/SKILL.md`, baseline output skeleton, line 172 | `skills/spec/SKILL.md`, edited `## Closed enums`, lines 163-171 | fenced | Same spelling and membership; output skeleton references `<spec status>` instead of restating the full list. |
| Upstream status settlement behavior and blocker/reporting obligations | `skills/spec/SKILL.md`, baseline `## Upstream status settlement`, lines 39-79 | `skills/spec/SKILL.md`, edited `## Upstream status settlement`, lines 39-79 | enum-reference only | Rules, mapping, blocker handling, and reporting fields remain in the same section. |
| Output skeleton required sections and order | `skills/spec/SKILL.md`, baseline `## Output skeleton`, lines 167-216 | `skills/spec/SKILL.md`, edited `## Output skeleton`, lines 211-260 | enum-reference only | Same headings and order; only status placeholder changes from inline full enum list to `<spec status>`. |
| Downstream status-settlement regression fixture | `scripts/test-skill-validator.py`, baseline expected exact string `Settlement result: updated | blocked | not-needed` | `scripts/test-skill-validator.py`, edited expected string `Settlement result:` | validation fixture aligned | The regression still requires a settlement-result report field in first-slice skills while no longer requiring duplicate inline enum values in `spec`. |

### Enum authority map

| Skill | Enum | Existing source | Authoritative destination | Values | Duplicate handling |
| --- | --- | --- | --- | --- | --- |
| `spec` | settlement result | Upstream status settlement report skeleton | `## Closed enums` fenced `Settlement result` block, lines 173-179 | `updated`; `blocked`; `not-needed` | Report skeleton uses `<settlement result>`. |
| `spec` | spec status | Output skeleton `Status` placeholder | `## Closed enums` fenced `Spec status` block, lines 163-171 | `draft`; `approved`; `abandoned`; `superseded`; `archived` | Output skeleton uses `<spec status>`. |

### Section-order exceptions

None for M1. The new `Closed enums` section is placed before the output
skeleton. Existing behavior-significant sections, including Workflow role,
upstream status settlement, rules, evidence collection, handoff behavior, and
output expectations, remain visible in their previous relative order.

### M1 unaffected surfaces

| Surface | Rationale |
| --- | --- |
| `skills/spec-review/SKILL.md` | Owned by M2. |
| `skills/test-spec/SKILL.md` | Owned by M3. |
| Generated adapter output validation | Owned by M3 after all canonical skill edits are present. |
| Cold-read proof across all three skills | Owned by M3 after all three skills have been edited. |

## M2. Spec-Review Skill Readability

Pending M2 implementation.

## M3. Test-Spec Skill Readability And Generated Output Proof

Pending M3 implementation.
