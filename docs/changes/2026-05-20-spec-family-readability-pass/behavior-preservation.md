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
| Downstream status-settlement regression fixture | `scripts/test-skill-validator.py`, baseline expected exact string `Settlement result: updated | blocked | not-needed` | `scripts/test-skill-validator.py`, edited skill-specific expectations | validation fixture aligned | The regression requires `spec` to use `<settlement result>` plus the authoritative `## Closed enums` fenced values, while unchanged `architecture` and `plan` still require the exact inline value list. |

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

### Same-slice scope

| Surface | Treatment |
| --- | --- |
| `skills/spec-review/SKILL.md` | Tabulate review-dimension guidance and add an authoritative review-dimension verdict enum surface. |
| Produced spec-review result contract | Preserve review status values, material-finding fields, recording fields, eventual test-spec readiness values, stop-condition behavior, and output skeleton shape. |
| Routing description | Unchanged. |
| Packaging, generated adapter skill bodies, build-time partials | Unchanged in M2. |

### Content-preservation matrix

| Source content | Existing location | New location | Change type | Preservation proof |
| --- | --- | --- | --- | --- |
| Review dimensions: requirement clarity; normative language; completeness; testability; examples; compatibility; observability; security/privacy; non-goals; acceptance criteria | `skills/spec-review/SKILL.md`, baseline `## Review dimensions`, lines 48-50 | `skills/spec-review/SKILL.md`, edited `## Review dimensions` table, lines 48-63 | tabulated | Same 10 review dimensions, same order, no dimension added or removed. The table uses only the dimension names and `<review dimension verdict>` placeholder; non-baseline review-focus examples are not present. |
| Review-dimension verdict values: `pass`, `concern`, `block` | `skills/spec-review/SKILL.md`, baseline `## Review dimensions`, line 50 | `skills/spec-review/SKILL.md`, edited `## Closed enums`, lines 67-75 | fenced | Same spelling and membership; review-dimension instruction references `<review dimension verdict>` instead of restating the full list. |
| Review coverage guidance: check normal, empty, boundary, error, permission, migration, rollout, rollback, old-client, and old-data behavior when relevant; acceptance must be observable, not aspirational | `skills/spec-review/SKILL.md`, baseline `## Review dimensions`, line 52 | `skills/spec-review/SKILL.md`, edited `## Review dimensions`, line 65 | unchanged | Sentence preserved verbatim. |
| Finding severity values and semantics: `blocking`, `major`, `minor` | `skills/spec-review/SKILL.md`, baseline `## Finding severity`, lines 54-61 | `skills/spec-review/SKILL.md`, edited `## Finding severity`, lines 77-84 | unchanged | M2 does not change finding severity guidance. |
| Review result output skeleton and recording obligations | `skills/spec-review/SKILL.md`, baseline `## Output skeleton`, lines 152-178 | `skills/spec-review/SKILL.md`, edited `## Output skeleton`, lines 175-201 | unchanged | Review status, recording status, review record/log/resolution fields, findings shape, test-spec readiness values, and stop-condition field remain unchanged. |

### Enum authority map

| Skill | Enum | Existing source | Authoritative destination | Values | Duplicate handling |
| --- | --- | --- | --- | --- | --- |
| `spec-review` | review dimension verdict | `## Review dimensions` prose | `## Closed enums` fenced `Review dimension verdict` block, lines 67-75 | `pass`; `concern`; `block` | Review-dimension instruction uses `<review dimension verdict>`. |

### Section-order exceptions

None for M2. The new `Closed enums` section is placed after review dimensions
and before finding severity. Formal review recording, material-finding
requirements, rules, workflow handoff behavior, and output expectations remain
visible in their previous relative order.

### M2 unaffected surfaces

| Surface | Rationale |
| --- | --- |
| `skills/spec/SKILL.md` | Closed in M1. |
| `skills/test-spec/SKILL.md` | Owned by M3. |
| Generated adapter output validation | Owned by M3 after all canonical skill edits are present. |
| Cold-read proof across all three skills | Owned by M3 after all three skills have been edited. |

## M3. Test-Spec Skill Readability And Generated Output Proof

Pending M3 implementation.
