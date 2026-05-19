# Published Skill Design Pilot Skill Audit

## Scope

Change: `2026-05-19-rigorloop-published-skill-design-contract`

Milestone: M1 audit and evidence scaffold

Audit target: canonical RigorLoop skills under `skills/*/SKILL.md`.

Pilot skill body edit scope:

- `skills/proposal/SKILL.md`
- `skills/proposal-review/SKILL.md`

This audit does not merge, retire, rename, remove, or change ownership of any skill.

## Method

Bounded evidence collected on 2026-05-19:

- `rg --files skills | sort` found 23 canonical skill files.
- Frontmatter description inventory measured every canonical skill description at less than 1024 characters.
- `find skills -mindepth 2 -maxdepth 2 -type d \( -name references -o -name scripts -o -name assets \)` found no packaged resource directories.
- `rg` section inventory found `Workflow role` and `Output skeleton` in both pilot skills.
- A bounded internal-path scan found project-local references such as `AGENTS.md`, `CONSTITUTION.md`, `docs/workflows.md`, and `specs/`; those references require later self-containment review for changed skills, but the audit did not find packaged resource directories that would require a current `Resource map`.

## Inventory Summary

| Skill | Description chars | Existence basis | Audit classification | Pilot action |
| --- | ---: | --- | --- | --- |
| `architecture` | 259 | durable architecture artifact and design decision workflow | reference split candidate; future workflow-role check when in scope | none |
| `architecture-review` | 178 | formal architecture review gate | future workflow-role/output-template check when in scope | none |
| `bugfix` | 227 | repeatable defect workflow and regression-test discipline | future workflow-role/output-template check when in scope | none |
| `ci` | 229 | recurring CI maintenance and validation behavior | future workflow-role/output-template check when in scope | none |
| `code-review` | 190 | formal implementation review gate | already normalized in historical baseline; no M1 action | none |
| `constitution` | 223 | governing artifact authoring | future workflow-role/output-template check when in scope | none |
| `explain-change` | 336 | durable change-rationale artifact | future workflow-role/output-template check when in scope | none |
| `explore` | 202 | option expansion before proposal/spec | future output-template check when in scope | none |
| `implement` | 240 | milestone implementation workflow and validation gate | already normalized in historical baseline; no M1 action | none |
| `learn` | 252 | durable lesson capture workflow | already normalized in historical baseline; no M1 action | none |
| `plan` | 234 | durable execution plan artifact | already normalized in historical baseline; no M1 action | none |
| `plan-review` | 231 | formal plan review gate | future workflow-role/output-template check when in scope | none |
| `pr` | 217 | PR handoff artifact and readiness summary | already normalized in historical baseline; no M1 action | none |
| `project-map` | 219 | repository orientation artifact | future workflow-role/output-template check when in scope | none |
| `proposal` | 229 | durable proposal artifact before spec | description routing gap; near-miss boundary needed; behavior-preservation required before rewrite | M3 pilot |
| `proposal-review` | 206 | formal proposal review gate | description routing gap; near-miss boundary needed; behavior-preservation required before rewrite | M3 pilot |
| `research` | 270 | assumption validation before lifecycle decisions | future output-template check when in scope | none |
| `spec` | 251 | contract-level feature specification artifact | future workflow-role/output-template check when in scope | none |
| `spec-review` | 241 | formal spec review gate | future workflow-role/output-template check when in scope | none |
| `test-spec` | 241 | durable test specification artifact | future workflow-role/output-template check when in scope | none |
| `verify` | 244 | final verification gate | already normalized in historical baseline; no M1 action | none |
| `vision` | 291 | project vision artifact | future workflow-role/output-template check when in scope | none |
| `workflow` | 379 | workflow orchestration and state assessment | already normalized in historical baseline; no M1 action | none |

## Finding Classes

### Description routing gap

Pilot findings:

- `proposal`: the current description states capability and broad trigger context, but does not name near-miss boundaries for `explore`, `spec`, or `plan`.
- `proposal-review`: the current description states capability and broad trigger context, but does not name near-miss boundaries for `spec-review`, `code-review`, implementation review, or final verification.

Future-slice note:

- Other skills were inventoried but are not required to satisfy R27-R36 until their approved slice.

### Missing near-miss boundary

Pilot findings:

- `proposal`: needs explicit boundary that it authors proposals, not specs, execution plans, reviews, implementation, or final verification.
- `proposal-review`: needs explicit boundary that it reviews proposals before spec, not specs, plans, code diffs, or verification evidence.

### Body contains hidden trigger logic

Pilot findings:

- No mandatory trigger logic was confirmed as body-only during M1. M3 must still preserve the rule that any required selection logic appears in frontmatter `description`, not only in body sections.

### Missing workflow role

Pilot findings:

- None. `proposal` and `proposal-review` both contain `## Workflow role`.

Future-slice note:

- Several non-pilot lifecycle skills do not currently have `## Workflow role`. This is recorded as future-slice audit context only and does not make them failing in M1.

### Missing output template

Pilot findings:

- None. `proposal` and `proposal-review` both contain `## Output skeleton`.

Future-slice note:

- Several non-pilot skills do not currently have `## Output skeleton` or `## Output template`. This is future-slice audit context only.

### Unavailable internal dependency

Pilot findings:

- None confirmed for the pilot pair in M1. Both pilot skills frame `AGENTS.md`, `CONSTITUTION.md`, `docs/project-map.md`, and `docs/workflows.md` as project-local or conditional evidence.

M2/M3 validation still must distinguish project-local paths from required RigorLoop repository-root internal dependencies.

### Resource map missing

Pilot findings:

- None. No packaged `references/`, `scripts/`, or `assets/` directories exist under `skills/proposal/` or `skills/proposal-review/`.

### Validation over-applied

Pilot findings:

- None in M1. Future validator work must avoid broad semantic scoring and runtime auto-selection claims.

### Validation under-specified

Pilot findings:

- `proposal` and `proposal-review` need routing coverage tables, behavior-preservation notes, behavior-parity evidence, and token-cost evidence before M3 closeout.

### Generic skill candidate

Pilot findings:

- None. Every current skill has at least one repeatable artifact, review gate, validation behavior, trust boundary, or recurring workflow role.

### Script candidate

Pilot findings:

- None for M1. Future validator work may add deterministic checks in repository-root scripts, but no skill-local packaged script is proposed by this audit.

### Reference split candidate

Pilot findings:

- None required for M1. If M3 adds long examples or rare variant detail, move them to packaged references and add a resource map.

Future-slice note:

- `architecture` mentions that full examples belong outside the common skill body; a future architecture-skill slice may decide whether packaged references are warranted.

### Example or counterexample candidate

Pilot findings:

- `proposal`: routing examples should cover obvious, casual, edge, near-negative, competing-skill, and should-not-trigger prompts.
- `proposal-review`: routing examples should cover obvious, casual, edge, near-negative, competing-skill, and should-not-trigger prompts.

### Token-cost risk

Pilot findings:

- `proposal` and `proposal-review` are among the longest canonical skills by line count. M3 must record static token-cost deltas and apply the zero target, `+5%` rationale tolerance, and `+10%` hard cap.

## Merge or Retire Candidates

None recorded in this audit.

If a future audit records a candidate, it must include:

- skill name;
- reason it may not earn its existence;
- affected artifacts or gates;
- likely owner;
- whether a separate proposal or spec amendment is required.

No merge, retirement, rename, removal, or ownership change is approved by this pilot.
