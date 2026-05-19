# Published Skill Design Spec Family Skill Audit

## Scope

Change: `2026-05-19-published-skill-design-spec-family`

Milestone: M1 spec-family audit and evidence scaffold

Skill body edit scope for this rollout:

- `skills/spec/SKILL.md`
- `skills/spec-review/SKILL.md`

This audit does not merge, retire, rename, remove, or change ownership of any skill.

## Method

Bounded evidence collected on 2026-05-19:

- Read `skills/spec/SKILL.md` and `skills/spec-review/SKILL.md`.
- Checked description lengths with a frontmatter extraction script.
- Checked section inventory with `rg` for `Workflow role`, output skeleton/template, stop/rule/output sections, and resource map indicators.
- Checked packaged resource directories with `find skills/spec skills/spec-review -mindepth 1 -maxdepth 1 -type d`.
- Measured baseline static token estimates with `python scripts/measure-skill-tokens.py --skills-root skills`.

## Inventory Summary

| Skill | Description chars | Baseline estimated tokens | Existence basis | Audit classification | M3 action |
| --- | ---: | ---: | --- | --- | --- |
| `spec` | 251 | 2288 | durable contract-level feature specification artifact | description routing gap; missing near-miss boundary; missing workflow role; missing compact output skeleton; behavior-preservation required before rewrite | rewrite in M3 |
| `spec-review` | 241 | 1992 | formal feature-spec review gate | description routing gap; missing near-miss boundary; missing workflow role; missing compact output skeleton; behavior-preservation required before rewrite | rewrite in M3 |

## Finding Classes

### Description routing gap

- `spec`: current description states capability and broad trigger contexts for externally observable behavior, APIs, UI, config, data contracts, error behavior, compatibility, security, and safety-sensitive logic. It does not name important near misses for proposal authoring, spec review, architecture, execution planning, test planning, or implementation.
- `spec-review`: current description states capability and broad trigger contexts for reviewing feature specs before architecture, test planning, execution planning, or implementation. It does not name important near misses for spec authoring, architecture review, plan review, code review, final verification, or PR handoff.

### Missing near-miss boundary

- `spec`: needs explicit boundary that it writes or amends a feature specification, not proposals, reviews, architecture, plans, tests, implementation, verification, or PR handoff.
- `spec-review`: needs explicit boundary that it reviews feature specs as a contract gate, not proposals, plans, architecture docs, implementation diffs, validation logs, final verification, or PR handoff.

### Body contains hidden trigger logic

No mandatory trigger logic was confirmed as body-only in M1.

M3 must still preserve the rule that required selection logic appears in frontmatter `description`, not only in body guidance.

### Missing workflow role

- `spec`: no `## Workflow role` section was found.
- `spec-review`: no `## Workflow role` section was found.

M3 should add workflow-role blocks because both skills produce, review, or gate lifecycle artifacts and participate in stage handoff.

### Missing output template

- `spec`: no compact fenced output skeleton or reviewed equivalent template was found. The skill lists required spec sections and expected output, but not a copyable skeleton.
- `spec-review`: no compact fenced output skeleton or reviewed equivalent template was found. The skill lists expected output fields, but not a copyable skeleton.

M3 should add or preserve compact output skeletons without replacing execution guidance.

### Unavailable internal dependency

None confirmed for the target pair in M1.

Both skills mention project-local artifacts such as `AGENTS.md`, `CONSTITUTION.md`, `docs/project-map.md`, `docs/workflows.md`, related specs, architecture docs, ADRs, interfaces, schemas, APIs, UI flows, config, and data contracts. These are framed as project-local or conditional inputs, not required RigorLoop repository-root dependencies.

### Resource map missing

None.

No packaged `references/`, `scripts/`, or `assets/` directories exist under `skills/spec/` or `skills/spec-review/`.

### Validation over-applied

None in M1.

M2 must avoid broad semantic scoring and runtime auto-selection claims.

### Validation under-specified

The spec-family rollout needs:

- routing coverage tables for `spec` and `spec-review`;
- behavior-preservation notes for behavior-significant wording that M3 may rewrite;
- behavior-parity evidence for representative spec and spec-review artifacts;
- token-cost evidence before and after M3.

### Generic skill candidate

None.

Both target skills earn their existence:

- `spec` owns a durable contract-level artifact with required sections, examples, requirements, edge cases, acceptance criteria, and readiness.
- `spec-review` owns a formal contract-review gate with material findings, recording obligations, readiness assessment, and downstream handoff boundaries.

### Script candidate

None for M1.

M2 may add deterministic validator fixtures only if existing validation does not already cover a concrete spec-family risk.

### Reference split candidate

None required in M1.

If M3 adds long examples or rare variant detail, move them to packaged resources and add a resource map.

### Example or counterexample candidate

- `spec`: routing examples should cover obvious, casual, edge, near-negative, competing-skill, and should-not-trigger prompts.
- `spec-review`: routing examples should cover obvious, casual, edge, near-negative, competing-skill, and should-not-trigger prompts.

### Token-cost risk

Baseline static estimates:

| Skill | Bytes | Lines | Estimated tokens | Largest sections |
| --- | ---: | ---: | ---: | --- |
| `spec` | 9164 | 192 | 2288 | `Required sections` 378; `Upstream status settlement` 352; `Rules` 222 |
| `spec-review` | 7968 | 183 | 1992 | `Isolation and Recording` 417; `Rules` 261; `Review dimensions` 227 |

M3 should target no material token regression, record rationale for any increase, and avoid duplicating the full routing contract in the body after moving routing into `description`.

## Merge or Retire Candidates

None recorded in this audit.

No merge, retirement, rename, removal, or ownership change is approved by this rollout.
