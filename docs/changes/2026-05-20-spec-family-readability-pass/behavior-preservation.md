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

### Normalized baseline gate

| Check | Evidence | Result |
| --- | --- | --- |
| `version` and `schema-version` front matter | `skills/test-spec/SKILL.md`, lines 1-8 | present |
| Workflow role | `skills/test-spec/SKILL.md`, lines 16-23 | present |
| Stop conditions | `skills/test-spec/SKILL.md`, lines 25-30 | present before normal artifact-generation guidance |
| Fenced output skeleton | `skills/test-spec/SKILL.md`, lines 152-246 | present |
| Normalization evidence | `docs/changes/2026-05-20-test-spec-contract-normalization/` | predecessor evidence present on branch |

### Same-slice scope

| Surface | Treatment |
| --- | --- |
| `skills/test-spec/SKILL.md` | Tabulate required sections and coverage rules, add authoritative closed-enum surfaces, and replace duplicate inline enum lists with enum references. |
| Produced test-spec artifact contract | Preserve output skeleton headings, required sections, coverage-map obligations, test-case format fields, stop conditions, and rules. |
| Generated adapter output | Validate from canonical skills in M3; generated public adapter skill bodies are not hand-edited. |
| Routing description | Unchanged. |
| Packaging, generated adapter skill bodies, build-time partials | Unchanged in M3. |

### Content-preservation matrix

| Source content | Existing location | New location | Change type | Preservation proof |
| --- | --- | --- | --- | --- |
| Required test-spec section list: Status; Related spec and plan; Testing strategy; Requirement coverage map; Example coverage map; Edge case coverage; Test cases; Fixtures and data; Mocking/stubbing policy; Migration or compatibility tests; Observability verification; Security/privacy verification; Performance checks; Manual QA checklist; What not to test; Uncovered gaps; Next artifacts; Follow-on artifacts; Readiness | `skills/test-spec/SKILL.md`, baseline `## Required sections`, lines 69-89 | `skills/test-spec/SKILL.md`, edited `## Required sections` table, lines 69-91 | tabulated | Same 19 section names, same order, no section added or removed. Obligations are preserved in the table cells. |
| Test spec status values: `draft`, `active`, `abandoned`, `superseded`, `archived` | `skills/test-spec/SKILL.md`, baseline `## Required sections`, line 71, and output skeleton, line 121 | `skills/test-spec/SKILL.md`, edited `## Closed enums`, lines 118-128 | fenced | Same spelling and membership; required-section table and output skeleton use `<test spec status>`. |
| Test case level values: `unit`, `integration`, `e2e`, `smoke`, `manual` | `skills/test-spec/SKILL.md`, baseline `## Test case format`, line 98, and output skeleton, line 154 | `skills/test-spec/SKILL.md`, edited `## Closed enums`, lines 130-138 | fenced | Same spelling and membership; test-case format and output skeleton use `<test case level>`. |
| Coverage map level values: `unit`, `integration`, `e2e`, `smoke`, `manual`, `contract`, `migration` | `skills/test-spec/SKILL.md`, baseline output skeleton requirement coverage map, line 137 | `skills/test-spec/SKILL.md`, edited `## Closed enums`, lines 140-150 | fenced | Same spelling and membership; requirement coverage map uses `<coverage map level>`. |
| Coverage rules: every `MUST` requirement needs coverage; every error behavior needs coverage; every migration or compatibility claim needs coverage or explicit manual verification; every architectural boundary that could break wiring needs an integration or contract test; bugs require a regression test that fails before the fix when feasible | `skills/test-spec/SKILL.md`, baseline `## Coverage rules`, lines 106-112 | `skills/test-spec/SKILL.md`, edited `## Coverage rules` table, lines 108-116 | tabulated | Same five rules, same order, no coverage rule added or removed. |
| Stop conditions for unreviewed or unstable specs and `not-ready` or `not-assessed` spec-review outcomes | `skills/test-spec/SKILL.md`, baseline `## Stop conditions`, lines 25-30 | `skills/test-spec/SKILL.md`, edited `## Stop conditions`, lines 25-30 | unchanged | Stop conditions remain before normal output guidance. |
| Output skeleton required sections and order | `skills/test-spec/SKILL.md`, baseline `## Output skeleton`, lines 114-208 | `skills/test-spec/SKILL.md`, edited `## Output skeleton`, lines 152-246 | enum-reference only | Same headings and order; only status and level placeholders change from inline full enum lists to authoritative enum references. |
| Rules, evidence collection, and expected output obligations | `skills/test-spec/SKILL.md`, baseline lines 210-238 | `skills/test-spec/SKILL.md`, edited lines 248-276 | unchanged | M3 does not change rules, evidence collection guidance, full-file-read guidance, or expected output obligations. |

### Enum authority map

| Skill | Enum | Existing source | Authoritative destination | Values | Duplicate handling |
| --- | --- | --- | --- | --- | --- |
| `test-spec` | test spec status | Required sections and output skeleton | `## Closed enums` fenced `Test spec status` block, lines 118-128 | `draft`; `active`; `abandoned`; `superseded`; `archived` | Required-section table and output skeleton use `<test spec status>`. |
| `test-spec` | test case level | Test case format and output skeleton | `## Closed enums` fenced `Test case level` block, lines 130-138 | `unit`; `integration`; `e2e`; `smoke`; `manual` | Test case format and output skeleton use `<test case level>`. |
| `test-spec` | coverage map level | Output skeleton requirement coverage map | `## Closed enums` fenced `Coverage map level` block, lines 140-150 | `unit`; `integration`; `e2e`; `smoke`; `manual`; `contract`; `migration` | Requirement coverage map uses `<coverage map level>`. |

### Section-order exceptions

None for M3. Stop conditions remain before input handling, required sections,
coverage rules, closed enums, and output skeleton. The new `Closed enums`
section is placed before the output skeleton so the skeleton can reference the
authoritative values without duplicating them.

### Generated adapter output boundary

Generated public adapter skill bodies were not hand-edited. M3 validation
attempted the repository-owned generation and adapter validation commands from
the active plan. `python scripts/build-adapters.py --version v0.1.5 --check`
and `python scripts/validate-adapters.py --version v0.1.5` failed on existing
adapter-layout debt: repository-tree adapter directories are absent under
`dist/adapters/`, and the tracked manifest includes command aliases rejected by
the v0.1.5 adapter check. The active plan anticipated this failure mode and
permits recording an explicit deferral for unrelated baseline archive-layout
debt. M3 therefore defers repository-tree adapter output validation while
continuing to rely on selected CI's adapter archive drift check for the current
supported adapter proof. Generated adapter skill bodies were not hand-edited.

### Cold-read notes

| Skill | Required sections or dimensions | Closed enums | Boundaries and output expectations | Result |
| --- | --- | --- | --- | --- |
| `spec` | `## Required sections` table, lines 108-136 | `## Closed enums`, lines 161-179 | Workflow role, upstream status settlement, rules, output skeleton, and handoff behavior remain findable by top-level heading. | pass |
| `spec-review` | `## Review dimensions` table, lines 48-65 | `## Closed enums`, lines 67-75 | Workflow role, material findings, isolation/recording, rules, handoff behavior, and output skeleton remain findable by top-level heading. | pass |
| `test-spec` | `## Required sections` table, lines 69-91, and `## Coverage rules` table, lines 108-116 | `## Closed enums`, lines 118-150 | Workflow role, stop conditions, input handling, test-case format, output skeleton, rules, and expected output remain findable by top-level heading. | pass |
