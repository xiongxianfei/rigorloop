# Proposal: RigorLoop Published Skill Design Contract

## Status

accepted

Accepted after clean `proposal-review` round 2.

---

## Problem

RigorLoop publishes skills through adapter packages for environments such as Codex, Claude Code, and opencode. In those installed environments, users often see only the published skill files and their packaged resources. They may not have RigorLoop's internal `specs/`, `schemas/`, `docs/workflows.md`, maintainer reports, or change-local proof packs.

That means a RigorLoop skill cannot behave like a pointer to internal documentation. It must be a compact, triggerable operating manual that tells a capable agent:

1. when the skill is worth invoking;
2. how to execute the workflow;
3. which packaged or project-local resources to load;
4. what good output looks like;
5. what the base model would otherwise miss, reinvent, or do inconsistently.

Current and future RigorLoop skills need a unified design contract so they remain portable, readable, traceable, and reliable across adapters. Without that contract, skills can drift into common failure modes:

- vague descriptions that under-trigger;
- descriptions that summarize the skill but do not state when to use it;
- body text that hides essential trigger logic;
- long `SKILL.md` files that include rare edge cases better placed in `references/`;
- repeated rules, repeated enum values, or duplicated lookup orders;
- instructions that point to maintainer-only RigorLoop files unavailable to adopters;
- resource folders with no explicit "when to load this" map;
- missing output skeletons for artifact-producing skills;
- validation checklists that are too broad, too automatic, or not tied to consequential failure modes;
- skills that encode generic tasks the base model can already perform.

Claude Code's official skill docs describe a skill as a `SKILL.md` file with frontmatter and markdown instructions, where the description helps decide when the skill should load and the body loads only when the skill is used. This supports using skills for procedural documentation that should be available on demand rather than always occupying context. ([Claude Code Docs][1])

---

## Goals

- Define a RigorLoop-wide design contract for published skills.
- Require every skill to justify its existence through specialized workflow value.
- Make frontmatter `description` the primary routing surface.
- Keep trigger logic in the description and execution logic in the body.
- Keep `SKILL.md` lean through progressive disclosure into packaged `references/`, `scripts/`, and `assets/`.
- Require explicit resource maps for all bundled resources.
- Require artifact-producing skills to include compact, fenced output templates.
- Preserve RigorLoop lifecycle rigor: stage ownership, claim boundaries, review recording, validation evidence, and stop conditions.
- Prevent published skills from requiring maintainer-only RigorLoop repository files.
- Add validation and realistic prompt tests for routing, near misses, output shape, and behavior parity.
- Establish transcript-based iteration so skill improvements address classes of failure rather than individual prompts.

---

## Non-goals

- Do not redesign every RigorLoop skill in one implementation slice.
- Do not add a new build-time partial/include system in this proposal.
- Do not change adapter install roots, archive verification, lockfile semantics, or CLI behavior.
- Do not make every workflow rule a hard constraint.
- Do not move all detailed examples into `SKILL.md`.
- Do not require validation loops for simple qualitative outputs where errors are obvious by inspection.
- Do not make published skills depend on internal RigorLoop `specs/`, `schemas/`, `docs/`, `scripts/`, `reports/`, or `dist/` paths unless those resources are packaged or explicitly project-local.
- Do not retroactively rewrite legacy adapter archives.

---

## Vision fit

fits the current vision

This proposal strengthens RigorLoop's artifact-first and reviewable-change model. Skills are the operating artifacts that agents use to produce, review, validate, and explain work. A well-designed skill makes the workflow easier to inspect and reproduce because it states the triggering boundary, execution steps, resource usage, output shape, and validation standard in the installed artifact itself.

The proposal also protects RigorLoop's rigor from becoming ceremony: skills should encode only the specialized workflow behavior that earns its place, not generic advice the model can already perform.

---

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Treat a skill as operating documentation for a smart agent | in scope | Problem, Recommended direction, Skill design contract |
| Require skills to earn their existence | in scope | Goals, Skill existence gate |
| Use description for routing | in scope | Routing contract |
| Avoid synonym stuffing | in scope | Routing contract |
| Put execution logic in the body | in scope | Body contract |
| Let content drive structure | in scope | Body structure guidance |
| Write imperatively | in scope | Instruction style |
| Explain important rationale | in scope | Instruction style |
| Keep `SKILL.md` lean | in scope | Progressive disclosure |
| Use references, scripts, and assets deliberately | in scope | Resource map contract |
| Branch by variant | in scope | Resource map contract |
| Bundle deterministic scripts | in scope | Script policy |
| Add validation only when warranted | in scope | Validation policy |
| Test with realistic prompts | in scope | Testing strategy |
| Iterate from transcripts | in scope | Rollout and maintenance |
| Use examples and counterexamples for style | in scope | Examples policy |
| Keep behavior unsurprising | in scope | Security and trust boundary |
| Use hard constraints sparingly | in scope | Instruction style |
| Name skills for user jobs-to-be-done | in scope | Naming contract |

---

## Context

RigorLoop skills serve multiple roles:

- artifact production, such as `proposal`, `spec`, `plan`, `test-spec`, `explain-change`, and `pr`;
- formal lifecycle review, such as `proposal-review`, `spec-review`, `plan-review`, and `code-review`;
- validation and closeout, such as `verify`;
- routing and workflow guidance, such as `workflow`.

These skills differ in shape, but they share the same design obligation: they must make the agent perform a specialized RigorLoop workflow that the base model would not reliably execute unaided.

Official Claude Code docs describe optional supporting files for skills, including templates, examples, scripts, and detailed reference documentation, and say `SKILL.md` should reference these resources so the model knows when to load them. ([Claude Code Docs][1]) Anthropic's skill-creator guidance also describes `description` as the primary triggering mechanism and recommends progressive disclosure: metadata, then `SKILL.md`, then bundled resources as needed. ([GitHub][2])

RigorLoop should adopt that general skill architecture while adding RigorLoop-specific constraints:

```text
Published skills must be portable.
Published skills must preserve lifecycle claim boundaries.
Published skills must not require maintainer-only repository context.
Published skills must produce durable, reviewable artifacts when they own an artifact.
```

This proposal builds on the accepted [Optimize Skills for User-Facing Readability and Self-Containment](./2026-05-18-skill-readability-self-containment.md) proposal. That earlier proposal owns a quality-first readability and self-containment direction for installed skills. This proposal broadens the contract into a reusable published-skill design standard, routing and prompt-test expectations, audit-first rollout, and validation criteria for future skill work.

---

## Options considered

### Option 1: Leave current skills as-is and rely on maintainers

**Pros**

- No migration work.
- No risk of accidentally changing skill behavior.
- No new validation requirements.

**Cons**

- Does not address under-triggering, redundant skill bodies, missing templates, or hidden repository dependencies.
- Leaves skill quality dependent on reviewer memory.
- Does not create a durable standard for future skills.

### Option 2: Create a separate style guide only

**Pros**

- Low cost.
- Useful for authors and reviewers.
- Avoids changing published skill bodies immediately.

**Cons**

- Easy to ignore.
- Does not create automated checks.
- Does not improve existing installed skill behavior by itself.

### Option 3: Add a strict universal `SKILL.md` template for every skill

**Pros**

- Strong consistency.
- Easier validation.
- Easier onboarding for new skill authors.

**Cons**

- Overfits different skill types to one shape.
- Can bloat simple skills.
- Conflicts with the principle that content should drive structure.

### Option 4: Adopt design principles plus a small required contract

**Pros**

- Gives all skills a consistent quality floor.
- Allows different body structures for different skill types.
- Supports progressive disclosure.
- Keeps `SKILL.md` lean.
- Can be validated with targeted checks.
- Supports incremental migration.

**Cons**

- Requires judgment in reviews.
- Some checks are qualitative and need cold-read or transcript-based review.
- Does not eliminate all source duplication by itself.

---

## Recommended direction

Choose **Option 4**.

Adopt a RigorLoop published-skill design contract with a small set of required surfaces and a broader set of design principles.

The contract should require:

```text
1. A job-to-be-done skill name.
2. A routing-focused description.
3. A short purpose or workflow-role section.
4. Imperative operating procedure.
5. Explicit resource map when resources exist.
6. Clear output expectations.
7. Validation only where consequential and checkable.
8. Self-containment for normal operation.
9. No unresolved internal repository dependencies.
10. Realistic routing and behavior tests.
```

The body structure may vary by skill type.

---

## Skill design contract

### 1. Skill existence gate

Before creating or retaining a skill, record why it deserves to exist.

A RigorLoop skill is justified when it contains at least one of these:

| Justification | Example |
| --- | --- |
| Repeatable lifecycle procedure | proposal review, spec review, verification |
| Durable artifact contract | proposal, spec, plan, review record, verify report |
| Domain-specific risk judgment | code review against RigorLoop claim boundaries |
| Tool or command sequence | validation selection, adapter build verification |
| Deterministic helper script | schema validation, artifact linting |
| Output shape the model often gets wrong | review result block, finding format |
| Safety or trust boundary | no branch-ready claim before verify |

A weak skill candidate should be rejected or merged when it is only:

```text
generic summarization
generic writing advice
generic code help
simple Q&A
a one-step task
a preference better handled by system/project instructions
```

### 2. Naming contract

Skill names should be short, concrete, lowercase, hyphenated, and action- or artifact-oriented.

Good RigorLoop names:

```text
proposal
proposal-review
spec
spec-review
plan
code-review
review-resolution
explain-change
verify
pr
```

Avoid names like:

```text
helper
misc
review-stuff
better-output
agent-guidance
```

### 3. Description routing contract

The frontmatter `description` must do three jobs:

1. state the skill capability;
2. name the trigger contexts;
3. name important near misses when needed.

The description should be assertive about legitimate use cases but not a synonym dump.

Example pattern:

```yaml
---
name: proposal-review
description: >
  Review a RigorLoop change proposal before specification. Use when the user
  asks to challenge problem framing, option quality, strategic value, scope
  boundaries, risks, vision fit, or readiness for spec. Use for proposal-review
  gate work, not for implementation review or final verification.
---
```

Description guidance:

| Do | Avoid |
| --- | --- |
| Put key trigger contexts first. | Hide "when to use" in the body. |
| Include file or artifact types when relevant. | Stuff with interchangeable synonyms. |
| Mention near misses for competing skills. | Describe only what the skill generally is. |
| Be specific enough to route. | Make broad "helps with X" descriptions. |

Claude Code docs say the `description` helps decide when to apply the skill and that optional `when_to_use` text is part of the skill listing. ([Claude Code Docs][1])

### 4. Body contract

The `SKILL.md` body should explain execution, not routing.

Recommended body sections:

```md
# Purpose

# Workflow role

# Operating procedure

# Resource map

# Important rules

# Output expectations

# Validation
```

This is not a mandatory universal template. Use only the sections the skill needs.

### 5. Workflow role block

Every RigorLoop lifecycle skill should include a short role block:

```md
## Workflow role

This skill reviews a proposal before the spec stage. It may approve the
direction, request changes, block the proposal, or return inconclusive.
It does not write the spec and does not claim downstream readiness.
```

The role block should answer:

| Question | Required answer |
| --- | --- |
| What stage is this? | Name the lifecycle role. |
| What does it receive? | Proposal, spec, plan, code, evidence, etc. |
| What does it produce? | Artifact, review, status, handoff. |
| What must it not claim? | Downstream readiness owned by other stages. |

### 6. Imperative procedure

Use direct commands.

Prefer:

```text
Read the proposal.
Check scope preservation.
Evaluate each review dimension.
Record material findings with evidence.
Return changes-requested if a material finding remains unresolved.
```

Avoid:

```text
It can be useful to consider whether the proposal has enough detail.
```

### 7. Rationale for important rules

When a rule affects judgment, explain why.

Good:

```text
Do not rely on chat approval alone because downstream reviewers must be able
to reconstruct the decision from durable artifacts.
```

Better than:

```text
Never rely on chat approval.
```

Reserve hard constraints for:

```text
security boundaries
privacy constraints
destructive actions
required output formats
claim ownership
formal review recording
schema or validation requirements
```

### 8. Progressive disclosure contract

Use three levels:

| Layer | Content | Purpose |
| --- | --- | --- |
| Frontmatter | name, description, optional routing metadata | Select the skill |
| `SKILL.md` | common operating procedure | Execute the normal workflow |
| Bundled resources | references, scripts, assets | Load optional depth only when needed |

Resource placement:

| Resource type | Use when |
| --- | --- |
| `references/` | long explanations, domain variants, examples, edge cases |
| `scripts/` | deterministic repeated work |
| `assets/` | templates, starter files, reusable output components |

Claude Code docs describe supporting files as a way to keep `SKILL.md` focused while loading detailed reference material only when needed. ([Claude Code Docs][1])

### 9. Resource map contract

If a skill ships resources, `SKILL.md` must say when to use each one.

Good:

```md
## Resource map

- Read `references/material-findings.md` when a review has one or more
  material findings.
- Use `scripts/validate_review_artifact.py` when a review record was created
  or updated.
- Use `assets/review-record-template.md` only when creating a detailed review
  record from scratch.
```

Bad:

```md
See references/ for more information.
```

### 10. Variant branching

If a skill covers variants, route to variant references rather than packing all details into the body.

Example:

```md
## Variant routing

- For proposal review, use the main procedure.
- For spec review, read `references/spec-review.md`.
- For code review, use `code-review` instead of this skill.
```

For RigorLoop, avoid overloading one skill with multiple lifecycle stages when separate stage skills are clearer.

### 11. Script policy

Bundle a script when the agent would otherwise rewrite the same deterministic helper repeatedly.

Good script candidates:

```text
validate change metadata
check review artifact shape
measure token cost
generate adapter output
validate generated adapter parity
normalize structured metadata
```

Do not bundle scripts for:

```text
subjective judgment
one-off reasoning
ambiguous interpretation
high-level strategy
```

A skill that references a script must say:

```text
when to run it
what input it expects
what output or exit code means
what to do on failure
```

### 12. Validation policy

Validation belongs where failures are:

```text
common
consequential
hard to notice by eye
objectively checkable
likely to recur
```

For RigorLoop skills, validation is warranted for:

| Case | Validation |
| --- | --- |
| Generated artifacts | shape and required fields |
| Review records | finding IDs, severity, evidence, required outcome, resolution path |
| Change metadata | schema and lifecycle status |
| Generated adapters | parity and packaged resource presence |
| Lockfiles/manifests | schema and trust-boundary fields |
| Code changes | selected tests and CI proof |

Validation may be omitted or lightweight for:

```text
small qualitative rewrite
brainstorming
brief explanatory answer
non-artifact chat-only response
```

### 13. Output expectations

Every artifact-producing skill must include a compact output skeleton.

Example:

````md
## Output template

Template ID: proposal-review-result-v1
Template status: normative

```md
## Result

- Skill:
- Review status:
- Material findings:
- Recording status:
- Recording blocker:
- Review record:
- Review log:
- Review resolution:
- Open blockers:
- Immediate next stage:

## Findings

### <Finding ID> - <summary>

- Severity:
- Location:
- Evidence:
- Required outcome:
- Safe resolution path:
```
````

### 14. Examples and counterexamples

Use examples when behavior is hard to define but easy to recognize.

Best locations:

| Example type | Location |
| --- | --- |
| Tiny inline example | `SKILL.md` |
| Longer example bank | `references/examples.md` |
| Full filled artifact | `assets/examples/` or `references/` |
| Non-normative examples | clearly labeled as examples |

Do not let examples replace the normative output skeleton.

### 15. Self-containment rule

Published skills must not require unavailable internal paths for normal operation.

The forbidden path list applies to RigorLoop repository-root internal paths, not to skill-local packaged resources.

Forbidden as required customer-project dependencies:

```text
<repo-root>/specs/
<repo-root>/schemas/
<repo-root>/maintainer-only docs/
<repo-root>/benchmarks/
<repo-root>/scripts/
<repo-root>/dist/
```

This does not forbid skill-local packaged resources such as:

```text
<skill>/references/
<skill>/scripts/
<skill>/assets/
```

Skill-local packaged resources are allowed only when they are included in the published adapter output and the `SKILL.md` resource map states when to use them.

Allowed only when framed correctly:

| Path type | Allowed use |
| --- | --- |
| Project-local docs | Use when present and relevant. |
| User-provided path | Use when explicitly supplied. |
| Packaged skill resource | Use when included in the adapter package. |
| Internal RigorLoop path | Use only when operating inside the RigorLoop repository or when it is the target artifact. |

### 16. Hard-constraint discipline

Hard constraints should be rare.

Use hard language for:

```text
Do not claim branch-ready before verify.
Do not create PR-ready claims from code-review.
Do not continue after unresolved needs-decision findings.
Do not write secrets, proxy URLs, or credentials into lockfiles.
Do not require unavailable internal repository files in published skills.
```

Use softer guidance for:

```text
Prefer concise explanations.
Use tables when they improve scanability.
Add examples when style is hard to specify.
```

### 17. Lack-of-surprise rule

A skill must not hide behavior beyond its name and description.

A review skill should review.
A verify skill should verify.
A proposal skill should produce a proposal.
A package skill should not silently run destructive commands.

Claude Code docs note that skills can grant tool permissions through frontmatter such as `allowed-tools`, and users should review project skills before trusting a repository. ([Claude Code Docs][1]) RigorLoop should therefore keep tool permissions and side effects explicit.

---

## Expected behavior changes

- Published RigorLoop skills use descriptions that route reliably.
- `SKILL.md` bodies focus on execution rather than buried trigger logic.
- Artifact-producing skills include compact output templates.
- Skills stop referencing maintainer-only repository paths as required dependencies.
- Bundled resources are used only when the skill body gives explicit conditions.
- Validation appears where it protects against consequential, checkable failures.
- Skill reviews evaluate realistic trigger and near-miss prompts.
- Future skill improvements are based on transcripts and same-class failure analysis, not one-off patches.

---

## Architecture impact

Affected surfaces:

```text
skills/*/SKILL.md
skills/*/references/ when packaged
skills/*/scripts/ when packaged
skills/*/assets/ when packaged
scripts/validate-skills.py
scripts/build-skills.py
scripts/build-adapters.py
scripts/validate-adapters.py
skill-related test fixtures
token-cost measurement reports
```

Not affected:

```text
adapter install roots
adapter archive trust model
lockfile schema
CLI init behavior
workflow stage order
review recording semantics
branch-ready or PR-ready ownership
```

---

## Testing and verification strategy

### Structural validation

| Check ID | Requirement |
| --- | --- |
| `SKILL-DESCRIPTION-001` | Description states capability and trigger contexts. |
| `SKILL-DESCRIPTION-002` | Description includes near misses when competing skills or common false positives exist. |
| `SKILL-BODY-001` | Body contains execution procedure, not only principles. |
| `SKILL-RESOURCE-001` | Every packaged resource is referenced with a specific load condition. |
| `SKILL-RESOURCE-002` | No vague "see references folder" guidance. |
| `SKILL-TEMPLATE-001` | Artifact-producing skill includes a fenced output skeleton. |
| `SKILL-SELF-CONTAIN-001` | Published skill has no required dependency on unavailable RigorLoop repository-root internal paths. |
| `SKILL-INCLUDE-001` | Published skill has no unresolved include or partial syntax. |
| `SKILL-ENUM-001` | Closed enum values appear once in one authoritative block or table. |
| `SKILL-TOKEN-001` | Token-cost delta is measured for each changed skill. |

Self-containment validation must distinguish RigorLoop repository-root `scripts/` from packaged skill-local `<skill>/scripts/`. Do not use a blunt deny-list that flags every `scripts/` mention regardless of context.

### Routing tests

Each changed skill should have prompt tests:

| Test type | Example |
| --- | --- |
| Obvious positive | "Review this RigorLoop proposal before spec." |
| Casual positive | "Can you sanity-check whether this proposal is ready?" |
| Edge positive | "This proposal has open questions and a possible vision conflict; review it." |
| Near negative | "Explain what a proposal is." |
| Competing skill | "Review this implementation diff." |
| Should not trigger | "Summarize this paragraph." |

First-slice routing tests are prompt fixtures and transcript-review inputs. They prove description coverage expectations, not deterministic model auto-selection, unless a dedicated routing harness is approved.

First-slice routing evidence may include:

- description contains positive trigger contexts;
- description contains important near-miss boundaries;
- prompt fixture set covers positives, casual positives, edge positives, near negatives, competing-skill prompts, and should-not-trigger prompts;
- transcript review records whether the skill under-triggered, over-triggered, or opened unnecessary resources.

Do not introduce broad semantic scoring of skill prose as a required CI gate in this slice.

### Behavior-parity tests

For rewritten existing skills:

```text
Representative artifact still receives the same review status.
Material finding shape remains valid.
Recording requirements remain intact.
Claim boundaries remain intact.
Validation evidence remains required where applicable.
```

### Transcript-based iteration

After pilot runs, inspect transcripts for:

```text
missed trigger
over-trigger
resource opened unnecessarily
instruction ignored
instruction over-applied
repeated helper code
output shape drift
validation skipped
validation over-applied
same-class failure recurrence
```

---

## Rollout and rollback

### Rollout

1. **Audit current skills.**
   - classify each as keep, merge, rewrite, or retire;
   - identify generic skills that do not earn their existence;
   - identify missing routing and missing output templates.
2. **Pilot on two high-visibility skills.**
   - recommended pilot: `proposal` and `proposal-review`;
   - update descriptions, workflow role, resource map, output template, and validation wording;
   - avoid broad rewrite.
3. **Run structural validation and prompt tests.**
   - include near negatives and competing-skill prompts;
   - record token-cost delta.
4. **Review transcripts.**
   - correct routing, over-triggering, and resource-use issues;
   - avoid overfitting to one prompt.
5. **Extend by skill family.**
   - proposal/spec family;
   - review family;
   - plan/test-spec family;
   - explain/verify/PR family.
6. **Regenerate adapters.**
   - generated adapter output must come from canonical `skills/`;
   - do not hand-edit adapter bodies.

### Rollback

- Revert individual skill changes.
- Preserve validation checks that remain generally correct.
- Do not alter adapter install roots, lockfiles, or release archives as part of rollback.
- If a rewritten skill over-triggers, first repair the description rather than deleting execution guidance.
- If token cost regresses materially, move rare detail into `references/` rather than removing required procedure.

---

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Description becomes too long or noisy. | Use concrete trigger contexts and near misses; avoid synonym dumps. |
| Skill body becomes too generic. | Require an execution procedure and output expectations. |
| Skill body becomes too long. | Move variant detail and long examples into `references/`. |
| Progressive resources are packaged but unused. | Require explicit resource map conditions. |
| Validation becomes ceremony. | Add validation only for consequential, checkable failure modes. |
| Normative behavior changes during readability rewrite. | Run behavior-parity fixtures. |
| Examples become mistaken for rules. | Label examples as non-normative and keep skeletons separate. |
| Hard constraints make skills brittle. | Reserve hard constraints for real invariants. |
| Skills require unavailable RigorLoop internals. | Add self-containment lint and cold-read verification. |
| Same-class failures recur across review rounds. | Use truth tables or decision matrices for branchy contracts before coding. |

---

## First-slice boundary

The first implementation slice is **audit-first**.

Audit all current RigorLoop skills and classify each finding as:

```text
description routing gap
missing near-miss boundary
body contains hidden trigger logic
missing workflow role
missing output template
unavailable internal dependency
resource map missing
validation over-applied
validation under-specified
generic skill candidate
script candidate
reference split candidate
example/counterexample candidate
token-cost risk
```

Then implement only the smallest pilot:

```text
skills/proposal/SKILL.md
skills/proposal-review/SKILL.md
validator changes needed for the pilot
generated adapter validation for changed skills
```

Do not rewrite all skills in one PR.

### Skill merge/retire boundary

The first-slice audit may classify a skill as a merge or retire candidate, but this proposal does not merge, retire, rename, or remove any skill.

If the audit finds a weak skill candidate, record it as a follow-on with:

- skill name;
- reason it may not earn its existence;
- affected artifacts or gates;
- likely owner;
- whether a separate proposal or spec amendment is required.

Any actual merge, retirement, rename, removal, or ownership change requires a separate proposal or explicit spec amendment because it can change stage ownership, artifact ownership, routing, adapter contents, and downstream validation.

---

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| `AC-SKILL-001` | A skill existence audit exists for the pilot pair. |
| `AC-SKILL-002` | Pilot skill descriptions state capability, trigger contexts, and near misses where needed. |
| `AC-SKILL-003` | Pilot skill bodies contain execution procedures and do not hide essential trigger logic. |
| `AC-SKILL-004` | Pilot artifact-producing skills include fenced output templates. |
| `AC-SKILL-005` | Any packaged resources have explicit load conditions. |
| `AC-SKILL-006` | Pilot skills do not require unavailable RigorLoop internal repository paths. |
| `AC-SKILL-007` | Closed enums, if present, appear once in authoritative blocks or tables. |
| `AC-SKILL-008` | Realistic routing tests include positives, casual positives, edge positives, near negatives, competing-skill prompts, and should-not-trigger prompts. |
| `AC-SKILL-009` | Behavior-parity fixtures confirm no lifecycle rule regression. |
| `AC-SKILL-010` | Token-cost delta is recorded and reviewed before rollout expands. |
| `AC-SKILL-011` | Adapter output is regenerated or validated from canonical `skills/`; no generated skill bodies are hand-edited. |
| `AC-SKILL-012` | Transcript review records at least one improvement decision or states no change needed with rationale. |

---

## Spec input decisions

These decisions answer the proposal-stage open questions as input to the spec amendment. The spec may refine exact wording, but implementation should not proceed against weaker defaults without recording a spec-level reason.

| Question | Spec input decision | Rationale |
| --- | --- | --- |
| Description length | Recommend and require `description` length of `<= 1024` characters. Add validator check `SKILL-DESCRIPTION-003`; warn when authors exceed the recommended target if a lower warning target is later adopted, and fail above the hard cap. | Descriptions are loaded into routing context even when the body is not. A project cap below platform truncation limits leaves room for adapter UI variants and forces concise routing text. |
| Workflow role section | Require `Workflow role` for skills that produce or close a lifecycle artifact, gate a stage, participate in stage handoff, or claim downstream readiness. Non-lifecycle skills omit it. | The role block earns its place when downstream stages depend on the skill's output; requiring it for every possible helper would become ceremony. |
| `when_to_use` frontmatter | Keep routing logic in `description`; do not require `when_to_use`. Permit `when_to_use` only as optional adapter metadata when supported, with no routing logic absent from `description`. | `description` is the portable routing field across the adapter set. Splitting routing across fields creates drift and duplicates validator complexity without portability gain. |
| Resource map presence | Require a `Resource map` section only when packaged `references/`, `scripts/`, or `assets/` resources exist. The map must name every packaged resource with a load condition. Do not require a "No bundled resources" line. | Resource absence is observable from the package. Requiring an explicit absence statement adds body text without improving agent behavior. |
| Pilot token-cost budget | Inherit the readability proposal's seeded pilot budget: target zero token regression, tolerate up to `+5%` with rationale, and block above `+10%` unless the spec revises the budget. | The accepted readability proposal already seeded this budget for the same pilot pair. Reusing it avoids fragmented numeric contracts across related proposals. |
| Merge or retire candidates | Do not name candidates at proposal stage. The first-slice audit produces candidates procedurally, and this proposal records them only as follow-ons. | Naming candidates before the audit would be speculative. Actual merge, retirement, rename, removal, or ownership change remains outside this proposal. |

---

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-19 | Treat skills as portable operating documentation. | Published skills are the user-facing execution contract. | Treat skills as links to maintainer-only docs. |
| 2026-05-19 | Make description the routing surface. | Skill bodies load only after selection, so routing must be in frontmatter. | Bury "when to use" sections in the body. |
| 2026-05-19 | Use progressive disclosure. | Keeps common-path instructions lean while preserving optional detail. | Put all details into `SKILL.md`. |
| 2026-05-19 | Pilot before broad rollout. | Reduces risk of normative regressions and token-cost bloat. | All-skill rewrite. |
| 2026-05-19 | Require realistic prompt tests. | Skills fail through routing and over/under-triggering, not just malformed markdown. | Test only direct `/skill-name` invocations. |
| 2026-05-19 | Inherit the pilot token-cost budget from the readability proposal. | The same pilot pair should not have two competing token-cost budgets. | Renegotiate a separate budget without a spec-level reason. |

---

## Next artifacts

```text
proposal-review
spec amendment: specs/skill-contract.md
spec-review
plan
test-spec
implementation
code-review
explain-change
verify
pr
```

### Spec source-of-truth boundary

`specs/skill-contract.md` remains the normative skill-contract source. This proposal amends that existing spec rather than creating a second permanent skill-contract spec.

If a separate `specs/rigorloop-published-skill-design-contract.md` drafting artifact is created, it must be merged into `specs/skill-contract.md` or explicitly referenced from `specs/skill-contract.md` as a subordinate extension before implementation relies on it.

Implementation must not rely on two competing normative skill-contract specs.

---

## Follow-on artifacts

- Proposal for build-time partials/includes if source duplication becomes costly.
- Proposal for skill conformance scoring across all published adapters.
- Proposal for transcript-based skill evaluation harness.
- Proposal for skill retirement/merge policy if audit finds weak skill candidates.

---

## Readiness

Accepted and ready for spec amendment to `specs/skill-contract.md`.

---

## Core invariant

```text
A RigorLoop skill is lean, triggerable operating documentation for a capable agent.

It must route reliably, teach a specialized workflow, disclose resources only
when needed, preserve lifecycle claim boundaries, and encode behavior the base
model would not consistently perform unaided.
```

[1]: https://docs.anthropic.com/en/docs/claude-code/skills "Extend Claude with skills - Claude Code Docs"
[2]: https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md "skills/skill-creator/SKILL.md at main - anthropics/skills"
