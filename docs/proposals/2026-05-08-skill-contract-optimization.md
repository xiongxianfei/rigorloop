# Skill Contract Optimization

## Status

accepted

## Problem

RigorLoop skills have accumulated useful workflow guidance, but several skills now carry too much state, repeated policy, and broad lifecycle narration. That makes them harder for agents to use correctly and easier to misread as owning claims that belong to another stage.

The recurring failure pattern is claim confusion: progress, readiness, closeout, and final Done state are treated as interchangeable. Recent learn sessions captured this clearly:

- `Ready for verify` is a next-gate statement, not Done state, PR readiness, or proof that downstream gates have passed.
- Milestone implementation content is not the same as milestone closeout when validation, review-resolution, plan notes, and closeout evidence remain unreconciled.

Skills should reduce that confusion by becoming smaller, more explicit, and more locally owned. Each skill should answer when to use it, what inputs it needs, what artifact it produces or updates, what it must not claim, what the next valid handoff is, and what blocks continuation.

## Goals

- Make skills smaller, sharper, and less stateful.
- Give major skills a consistent section shape so agents can scan them quickly.
- Make each skill own only its local artifact, decision, or gate.
- Add explicit do-not-overclaim guidance where stage boundaries are commonly confused.
- Separate progress, readiness, closeout, and Done language across planning and execution skills.
- Make handoff rules compact and linked to authoritative workflow specs instead of duplicated everywhere.
- Consolidate repeated review and workflow policy into shared canonical blocks where repetition is necessary.
- Add output contracts that start with compact result summaries.
- Add reading guidance that prefers targeted evidence first and full-file reads only when needed.
- Preserve canonical source and generated-output boundaries.
- Add validation coverage for required skill sections, forbidden overclaims, shared-block drift, and generated-output drift.

## Non-goals

- Do not rewrite every skill in one large undifferentiated change.
- Do not change the lifecycle stage order merely to simplify skill text.
- Do not move authoritative workflow policy out of `specs/rigorloop-workflow.md`.
- Do not make `docs/workflows.md` a second normative workflow spec.
- Do not add a new skill unless it owns a distinct artifact, gate, review responsibility, or recurring action.
- Do not introduce a standalone `review-resolution` skill solely for this optimization.
- Do not hand-edit generated `.codex/skills/` or `dist/adapters/` output.
- Do not replace spec, test-spec, architecture, plan, review, or verification artifacts with skill prose.
- Do not require broad full-file reads as the default evidence collection method.
- Do not add semantic quality scoring for skill prose in the first validation slice.

## Vision fit

fits the current vision

This proposal supports RigorLoop's commitment to traceable, reviewable AI-assisted delivery. Smaller claim-safe skills make it easier for reviewers to reconstruct which artifact owns each decision, proof claim, readiness statement, and handoff without relying on chat history.

## Context

`CONSTITUTION.md` says RigorLoop optimizes for reviewability, traceability, trustworthy automation, and design-implementation consistency. It also says workflow or governance changes update affected operating and governance guidance, and that agents must not fake CI status, verification status, review completion, or artifact readiness.

`docs/workflows.md` already summarizes stage-owned language: `implement` reports implementation completion or readiness for `code-review`, `code-review` owns review findings, `verify` owns `branch-ready`, and `pr` owns PR readiness. The milestone-aware handoff work further clarified that clean review of one milestone does not imply whole-plan verification readiness unless no in-scope implementation milestone remains open or unresolved.

The learn records `docs/learn/sessions/2026-05-07-plan-readiness-vs-completion.md` and `docs/learn/sessions/2026-05-07-milestone-closeout-vs-progress.md` show the same underlying issue from different angles: agents need clearer language for the difference between work performed, next-stage readiness, stage closeout, and final lifecycle completion.

`docs/project-map.md` is absent, so this proposal does not rely on project-map claims.

## Options considered

### Option 1: Keep skills as they are

Leave skill structure and wording unchanged, relying on existing specs, workflows, and learn notes to correct overclaims.

Pros:

- No immediate churn in skill files or generated output.
- Avoids a broad documentation refactor.

Cons:

- Leaves recurring state and handoff confusion in the surfaces agents read most often.
- Keeps repeated policy drift likely across review and lifecycle skills.
- Makes later validators harder because each skill uses its own shape.

### Option 2: Patch only the currently noisy skills

Update `plan`, `implement`, `code-review`, `verify`, and `pr` with clearer readiness, closeout, and do-not-overclaim language.

Pros:

- Addresses the most common lifecycle confusion quickly.
- Smaller first slice than normalizing all skills.

Cons:

- Leaves inconsistent skill shape across proposal, spec, architecture, review, learn, and workflow skills.
- Does not solve shared-block drift across review skills.
- Risks creating another one-off wording layer instead of a durable skill contract.

### Option 3: Define a standard skill contract and apply it in phases

Define a compact standard shape, ownership rules, shared blocks, output summaries, evidence-reading guidance, and validation expectations. Apply the contract first to the highest-risk workflow skills, then expand to the remaining skills.

Pros:

- Fixes the root problem: unclear skill ownership and overbroad claims.
- Keeps authoritative policy in specs while making local skill handoffs easier to follow.
- Supports regression tests for structure, drift, and forbidden overclaims.
- Allows a phased rollout without rewriting every skill at once.

Cons:

- Requires coordinated updates to skills, shared templates, tests, and generated output.
- Needs careful review so normalization does not erase useful skill-specific guidance.

### Option 4: Replace skill guidance with a central workflow router

Move most skill instructions into one central workflow engine or document, leaving skills as thin command stubs.

Pros:

- Reduces duplication aggressively.
- Could make routing rules easier to maintain in one place.

Cons:

- Makes individual skills less self-contained for agents.
- Increases dependency on a single large workflow surface.
- Conflicts with the goal of small, locally useful skill contracts.

## Recommended direction

Choose Option 3.

RigorLoop should define a standard skill contract and apply it incrementally. The guiding principle is:

```text
Skills operate the workflow.
Specs define the workflow.
Docs summarize the workflow.
Learn records recurring improvements.
Validators prevent drift.
```

Each skill should stay small and answer:

```text
When do I use this?
What inputs do I need?
What exact artifact do I produce or update?
What must I not claim?
What is the next valid handoff?
What blocks me from continuing?
```

### Normative ownership

The skill contract should live in a focused spec:

```text
specs/skill-contract.md
```

Ownership should split this way:

| Surface | Owns |
|---|---|
| `specs/skill-contract.md` | standard skill shape, claim boundaries, result output expectations, shared-block rules, generated-output boundaries, and evidence-reading guidance |
| `specs/rigorloop-workflow.md` | stage order, obligation, handoff, and downstream-blocking semantics |
| `docs/workflows.md` | contributor-facing summary |
| `skills/*/SKILL.md` | local operating guidance for each skill |

The skill contract is normative in `specs/skill-contract.md`. If that spec conflicts with generated skills, adapter output, or contributor summaries, the spec wins under the repository's source-of-truth order.

### Required core sections

Every skill should include these core sections:

```md
## Purpose

## When to use

## When not to use

## Inputs to read

## Outputs

## Handoff

## Stop conditions

## Claims this skill must not make
```

Conditional sections should be used when relevant:

```md
## Preconditions

## Workflow

## Validation / proof

## Failure modes

## Examples

## Required artifact sections

## Review finding format

## Milestone state rules

## Generated-output handling
```

Skill-type variants should preserve useful domain-specific guidance:

| Skill type | Additional expected sections |
|---|---|
| Authoring skills | required artifact sections and quality checklist |
| Review skills | review checklist, statuses, finding format, material recording |
| Execution skills | validation/proof, state update, do-not-overclaim |
| Periodic skills | trigger, frame, observe, classify, route |

The highest-value sections are `When to use`, `When not to use`, `Outputs`, `Handoff`, `Stop conditions`, and `Claims this skill must not make`. These should be present and concise before adding long narrative guidance.

### First implementation slice

The first accepted implementation slice covers only:

- `skills/workflow/SKILL.md`
- `skills/plan/SKILL.md`
- `skills/implement/SKILL.md`
- `skills/code-review/SKILL.md`
- `skills/verify/SKILL.md`
- `skills/pr/SKILL.md`
- `skills/learn/SKILL.md`

The first slice adds:

- standard core sections where missing;
- do-not-overclaim guidance;
- compact result output;
- milestone, progress, readiness, and closeout wording where relevant;
- targeted evidence-reading guidance;
- generated-output drift checks when canonical skills change.

The first slice does not normalize every skill.

### Later-phase normalization order

After the first implementation slice, normalize skills in this order:

1. Core lifecycle authoring and review skills: `proposal`, `proposal-review`, `spec`, `spec-review`, `architecture`, `architecture-review`, `plan-review`, `test-spec`, `explain-change`, and `ci-maintenance`.
2. On-demand and standing or living-reference skills: `explore`, `research`, `vision`, `project-map`, and `bugfix`.
3. Newly adopted optional skills: `ui-design`, `ui-design-review`, `workflow-contract`, and `adopt-rigorloop`, when they exist and own approved artifacts or gates.

### Skill claim ownership

Skills should not claim results owned by another stage.

| Skill | May claim | Should not claim |
|---|---|---|
| `proposal` | direction recommended | behavior is specified |
| `spec` | behavior contract defined | implementation is planned |
| `architecture` | system shape and decisions | implementation sequence is complete |
| `plan` | execution sequence | code is implemented |
| `implement` | implementation work completed or ready for review | review passed or branch ready |
| `code-review` | review findings or clean-with-notes | branch ready or PR ready |
| review-resolution artifact/guidance | findings dispositioned | validation passed unless linked to owning proof |
| `verify` | validation proof and branch-ready | PR body ready |
| `pr` | PR body/opening readiness | implementation, review, or verification passed unless linked to evidence |
| `learn` | captured lesson or follow-up | new workflow policy unless routed to an authoritative artifact |

### Readiness language

Planning and execution skills should keep four concepts distinct:

| Concept | Meaning |
|---|---|
| `Progress` | What work has happened so far |
| `Readiness` | What stage can happen next |
| `Closeout` | Whether the current artifact or stage has satisfied its checklist |
| `Done` | Final lifecycle state after required gates are complete |

Plan-related guidance should prefer wording like:

```text
Status: Active.

Progress: implementation milestones are complete; code-review is complete.

Readiness: Ready for verify.

Remaining completion gates: verify, explain-change, PR handoff, then Done if no true downstream event remains.
```

### Do-not-overclaim guidance

Major skills should include a short local block that names claims the skill does not own. For example, `implement` should say the slice is ready for `code-review`, not that review is clean. `verify` should say `branch-ready`, not `pr-open-ready`.

### Forbidden-overclaim validation

Forbidden-overclaim checks should be narrow and incident-based. Validators should prefer positive required wording and check only a small list of historically dangerous phrases. They must not become broad semantic quality scoring.

The first validation slice should use this hierarchy:

1. positive required wording for each skill;
2. a small forbidden phrase list for historically dangerous claims;
3. no broad natural-language scoring.

The incident-based list should focus on claims such as:

- `implement` claiming review passed, clean review, branch-ready, PR-ready, or implementation-ready-for-verify;
- `code-review` claiming branch-ready, PR-ready, CI passed, or verification passed;
- `verify` claiming PR-ready, PR body ready, or review passed;
- `pr` claiming implementation, review, verification, or tests passed without linking to owning evidence;
- `plan` using Done, complete, ready for PR, or ready for verify without explicit remaining-gates wording.

### Shared policy blocks

Repeated policy should move into canonical shared blocks when exact consistency matters or when validator comparison is useful.

Ready for shared-block treatment in this proposal:

- `review-isolation-and-recording`;
- `evidence-collection-efficiency`;
- `generated-output-handling`.

Deferred until stable:

- `vision-fit`;
- `plan-readiness-vs-completion`;
- `milestone-aware-review-handoff`;
- `first-pass-completeness`;
- `material-finding-requirements`, if still under active simplification.

Skills can copy the shared block text, and tests can compare the copied sections against the shared source.

### Shared-block source of truth

Shared skill policy blocks live under:

```text
templates/shared/<block-name>.md
```

These files are canonical authored sources for copied skill subsections. `templates/` is already listed as canonical authored workflow content in `CONSTITUTION.md` and `AGENTS.md`; the implementation should preserve or update those governance pointers if the source boundary changes.

When a shared block is adopted:

- each consuming skill copies the block verbatim;
- `scripts/test-skill-validator.py` compares copied blocks to the shared source;
- generated skill and adapter outputs are regenerated from canonical skills;
- the shared block itself does not replace the workflow or skill-contract spec.

For v1, shared blocks are copied into canonical skills and checked for drift by `scripts/test-skill-validator.py`.

Do not generate shared blocks into skills in the first implementation slice. A later proposal may add generation if copied blocks become difficult to maintain.

### Output contracts

Major skills should start outputs with a compact result block before detailed rationale. The common core is:

```md
## Result

- Skill:
- Status:
- Artifacts changed:
- Open blockers:
- Next stage:
```

Add optional fields when relevant:

```md
- Validation:
- Review status:
- Finding IDs:
- Milestone state:
- Readiness:
- Follow-ups:
```

Authoring skills may add:

```md
- Recommended direction:
- Next artifacts:
```

`learn` may add:

```md
- Session path:
- Lessons captured:
- Follow-ups:
```

Where a skill updates an artifact, the skill should define the artifact-local output fields it expects. This makes the skill easier to review and easier to validate structurally.

### Examples

Examples are optional and should be short. A skill may include one minimal valid example and one invalid example only when they prevent recurring errors. Long examples belong in `examples/` or templates, not in skill files.

### Evidence reading

Skills should prefer targeted evidence before broad reads:

```text
Start from summaries, IDs, headings, and targeted sections.
Escalate to full-file reads only when exact wording, conflicting evidence, artifact review, or closeout proof requires it.
```

This keeps skill use efficient without weakening review obligations when exact artifact content matters.

### Generated output

Canonical skill source remains under `skills/`. Generated Codex mirrors and adapter package output are secondary proof surfaces:

```text
Edit canonical skill source.
Regenerate generated outputs.
Validate drift.
Do not hand-edit generated copies.
```

### Minimum viable skill guidance

The normative minimum viable skill rule lives in `specs/skill-contract.md`.

`docs/workflows.md` and `AGENTS.md` may summarize the rule.

Detailed examples and templates live in skill-creator guidance, such as `templates/skill.md` or `docs/skills/creating-skills.md`.

A new skill should be added only when it owns a distinct artifact, gate, review responsibility, recurring action, or approved operational process.

## Expected behavior changes

- Skill files become easier to scan because they follow a consistent section shape.
- Agents see local stop conditions and do-not-overclaim rules before broad workflow detail.
- Stage outputs start with compact result summaries and link details only as needed.
- Handoff sections name the normal next stage, conditional next stages, and the authoritative workflow spec instead of restating the whole lifecycle.
- Plan and implementation skills distinguish progress, readiness, closeout, and Done consistently.
- Review skills share identical or validator-checked wording for material-finding recording and isolation rules.
- Generated `.codex/skills/` and `dist/adapters/` files remain regenerated outputs rather than hand-edited sources.

## Architecture impact

This is a workflow-infrastructure and skill-contract change, not runtime product architecture.

Expected affected authored surfaces include:

- new `specs/skill-contract.md` for the normative skill contract.
- `specs/rigorloop-workflow.md` for a short pointer and any stage-order or handoff alignment.
- matching test specs when observable skill contract behavior is specified.
- `docs/workflows.md` for the contributor-facing summary.
- `skills/*/SKILL.md` for canonical skill source.
- `templates/shared/*.md` for repeated policy blocks that need drift checks.
- skill-creator guidance such as `templates/skill.md` or `docs/skills/creating-skills.md` if detailed minimum viable skill examples are added.
- `scripts/test-skill-validator.py` and related validation scripts for structural assertions.
- `AGENTS.md` only if root contributor guidance needs a concise summary update.

Generated mirrors under `.codex/skills/` and adapter outputs under `dist/adapters/` should be regenerated from canonical sources and checked for drift.

No new external service, storage model, package boundary, or runtime data flow is expected. A separate architecture artifact is probably unnecessary unless the spec introduces a reusable shared-block generation system or a broader validation architecture.

## Testing and verification strategy

- Add spec coverage for skill claim ownership, standard required sections, output summaries, generated-output handling, and evidence-reading guidance.
- Add test-spec coverage that maps each new skill-contract requirement to static checks or explicit manual review expectations.
- Extend skill validator tests to assert required sections for selected major skills.
- Add positive required wording assertions first, then narrow forbidden-overclaim assertions for high-risk phrases in `implement`, `code-review`, `verify`, `pr`, `plan`, and `learn`.
- Add shared-block drift checks where canonical shared blocks are adopted.
- Keep generated-output drift validation through existing build and adapter checks.
- Run selector-selected validation for touched proposal, spec, skill, template, script, generated, and adapter paths.
- Use broad smoke only when the accepted plan or selector requires it.

## Rollout and rollback

The rollout should be phased so reviewers can inspect one coherent slice at a time:

- First, specify the skill contract and normalize the highest-risk lifecycle skills: `workflow`, `plan`, `implement`, `code-review`, `verify`, `pr`, and `learn`.
- Next, normalize core lifecycle authoring and review skills: `proposal`, `proposal-review`, `spec`, `spec-review`, `architecture`, `architecture-review`, `plan-review`, `test-spec`, `explain-change`, and `ci-maintenance`.
- Then normalize on-demand and standing or living-reference skills: `explore`, `research`, `vision`, `project-map`, and `bugfix`.
- Finally, normalize newly adopted optional skills only after they exist and own approved artifacts or gates.

Rollback is straightforward for wording-only skill changes: revert the affected skill, template, validator, and generated-output updates together. If a shared block proves too rigid, keep the local skill guidance and retire only the shared-block drift assertion.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Normalization removes useful skill-specific nuance. | Apply the shape incrementally and preserve local details under compact sections where they still change behavior. |
| Shared blocks make skills feel repetitive. | Use shared blocks only for rules where exact consistency matters or where validators can prevent drift. |
| Validators overfit headings while missing actual quality. | Keep first checks structural and pair them with proposal/spec/code review for semantic quality. |
| The first implementation slice becomes too broad. | Prioritize lifecycle-confusion skills before less risky skills. |
| Generated output drifts from canonical skills. | Regenerate `.codex/skills/` and adapter outputs and run existing drift checks. |
| Skill guidance starts competing with the workflow spec. | Keep normative stage-order policy in specs and make skills link to it for full routing rules. |

## Open questions

None.

Proposal-review decisions settled later-phase normalization order, shared-block readiness, shared-block delivery, forbidden-overclaim validation strategy, and minimum viable skill guidance placement.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-05-08 | Draft proposal recommends a phased standard skill contract. | Addresses recurring overclaim and readiness confusion while avoiding a single large rewrite. | Keep skills unchanged; patch only current noisy skills; replace skills with a central router. |
| 2026-05-08 | Keep authoritative workflow policy in specs, with skills carrying local handoff and stop-condition guidance. | Preserves the existing source-of-truth order and avoids turning skills into substitute specs. | Put all workflow policy directly into each skill; move everything into `docs/workflows.md`. |
| 2026-05-08 | Treat generated outputs as secondary proof surfaces. | Matches repository generated-output policy and reduces duplicate review work. | Hand-edit generated mirrors or treat adapter copies as independent source. |
| 2026-05-08 | Normalize later-phase skills in three waves: core lifecycle authoring/review, on-demand and standing/living-reference skills, then optional skills when approved. | Gives spec and plan authors a settled rollout order without forcing every skill into the first slice. | Leave later phases open; normalize every skill immediately. |
| 2026-05-08 | Use shared blocks now for review isolation and recording, evidence collection efficiency, and generated-output handling. | These rules are stable enough and benefit from exact consistency. | Share all repeated rules now; defer all shared blocks. |
| 2026-05-08 | Copy shared blocks into skills with drift checks for v1. | Keeps the first implementation slice simple and debuggable. | Add a shared-block generation build step now. |
| 2026-05-08 | Keep forbidden-overclaim validation narrow, positive-first, and incident-based. | Avoids brittle semantic scoring while still catching recurring dangerous claims. | Broad natural-language quality scoring; no overclaim validation. |
| 2026-05-08 | Put minimum viable skill guidance normatively in `specs/skill-contract.md`, with summaries in `docs/workflows.md` and `AGENTS.md` and details in skill-creator guidance. | Keeps skill-creation policy in the focused skill contract while preserving concise contributor reminders. | Put the full rule only in `AGENTS.md`; put all details in `specs/rigorloop-workflow.md`. |

## Next artifacts

- Feature spec for `specs/skill-contract.md`.
- Matching test spec after the feature spec.
- Execution plan if the accepted spec touches multiple skills, shared templates, validators, generated output, and adapters.

## Follow-on artifacts

- Feature spec: [Skill Contract](../../specs/skill-contract.md).
- Execution plan: [Skill Contract Optimization Execution Plan](../plans/2026-05-08-skill-contract-optimization.md).
- Test spec: [Skill Contract Test Spec](../../specs/skill-contract.test.md).
- Proposal-review R1 and resolution: [review log](../changes/2026-05-08-skill-contract-optimization/review-log.md), [review resolution](../changes/2026-05-08-skill-contract-optimization/review-resolution.md), and [proposal-review-r1](../changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r1.md).
- Proposal-review R2: [proposal-review-r2](../changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r2.md).

## Readiness

Accepted after proposal-review. Follow-on feature spec, execution plan, and test spec are recorded; the active plan owns the current execution handoff.
