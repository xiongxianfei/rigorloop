# Proposal: Stage Evidence Access Contracts for Cost-Bounded Rigor

## Status

accepted

## Problem

RigorLoop's skills currently tell agents what artifacts may be relevant, but they do not consistently define the smallest sufficient evidence set each stage should inspect before expanding.

This creates recurring token waste and workflow amplification. Agents can read broad governance surfaces, full skill files, specs, plans, generated outputs, and review history before knowing whether that evidence is actually needed. The context-budget learn session already captured this failure mode: one broad workflow/state search returned 511 lines and about 26k output tokens, and a later learn search returned 2,118 lines and about 93k output tokens.

The current cost-bounded-rigor proposal correctly identifies the remaining problem as workflow amplification from broad proposal scope, broad evidence collection, repeated findings, repeated validation, and repeated state reconciliation.

The skills also show why a simple "read only two files" rule is not enough. `implement` needs the active plan, spec, test spec, relevant code/tests, and validation commands for the milestone. `code-review` needs the actual diff or changed files, governing artifacts, plan, test spec, validation evidence, and related code/tests when needed.

The missing model is:

```text
default evidence set
+ conditional evidence set
+ justified expansion
+ bounded-read rule
```

Without that model, agents either over-read and waste tokens or under-read and weaken rigor.

## Goals

- Define a stage evidence access model for RigorLoop skills.
- Make each skill start from the smallest sufficient evidence set.
- Allow evidence expansion when justified.
- Require a short reason when a skill reads outside its default or conditional evidence set.
- Reduce broad searches across specs, docs, skills, generated output, and historical artifacts.
- Preserve rigorous review, validation, material-finding, and source-of-truth behavior.
- Keep public skill wording concise.
- Avoid hard token gates in the first slice.
- Support the existing cost-bounded-rigor direction without turning it into another broad multi-plan initiative.

## Non-goals

- Do not forbid necessary evidence reads.
- Do not create rigid allow-lists that make stages unsafe.
- Do not weaken `code-review`, `verify`, formal review recording, or material-finding requirements.
- Do not require a detailed evidence-expansion table for every normal file read.
- Do not add semantic runtime validation in the first slice.
- Do not rewrite every skill at once.
- Do not make token totals hard release blockers.
- Do not replace stage artifacts with chat-only summaries.

## Vision fit

fits the current vision

This proposal supports RigorLoop's goal of traceable, reviewable AI-assisted delivery by making evidence access deliberate, bounded, and reconstructable without wasting context on broad searches.

## Context

RigorLoop already has token-cost guidance: diagnose cost by static size, dynamic input, command-output amplification, full-file reads, repeated reads, generated-output reads, and broad-search signals before optimizing.

The v0.1.1 Token-Friendliness report showed that dynamic cost is real: static skill total was 54,294 estimated tokens, median input tokens were 71,483, and the largest observed single command output was 20,738 estimated tokens in `implement-handoff`.

The accepted progressive-loading direction also shows that the problem is not only file length; agents often read whole skill files or broad sections when a small operating section would be enough.

Therefore, the next improvement should define who may read what by default, when extra evidence is justified, and how that expansion is recorded.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Define what each skill/stage should look at | in scope | Goals, Recommended direction, Evidence access contract |
| Require a reason when a skill reads more | in scope | Evidence expansion rule |
| Keep implementation and review evidence bounded | in scope | Stage examples |
| Keep rules simple and concise | in scope | First implementation slice, Non-goals |
| Avoid excessive token use | in scope | Problem, Acceptance criteria |
| Preserve rigor | in scope | Non-goals, Risks and mitigations |

## Options considered

### Option 1: Hard allow-list per skill

Example:

```text
implement/code-review may only read spec, test-spec, and CONSTITUTION.md
```

Advantages:

- Very simple.
- Strongly reduces accidental broad reads.

Disadvantages:

- Unsafe for real implementation and review.
- `implement` normally needs the active plan, relevant code/tests, and validation commands.
- `code-review` normally needs the diff or changed files, validation evidence, plan milestone, and related tests.
- Can force under-reading and false clean results.

### Option 2: No access model; rely on existing evidence-efficiency wording

Advantages:

- No new process.
- Existing skills already mention bounded evidence.

Disadvantages:

- Prior incidents show the existing wording is not operational enough.
- Broad searches still happen.
- Agents lack a stage-specific default read set.

### Option 3: Default + conditional + justified expansion model

Advantages:

- Preserves rigor.
- Reduces unnecessary reads.
- Allows expansion when needed.
- Makes evidence expansion reviewable.
- Fits cost-bounded-rigor direction.

Disadvantages:

- Requires concise updates to several skills.
- Requires careful wording to avoid bureaucracy.

## Recommended direction

Choose Option 3.

Adopt a Stage Evidence Access Contract.

Each stage skill defines:

```text
Default evidence:
  read first without extra explanation.

Conditional evidence:
  read when a named trigger applies.

Expansion evidence:
  read only when default/conditional evidence is missing, stale, contradictory, insufficient, or the artifact is the review target.

Broad/full-file evidence:
  read only when bounded evidence cannot answer the stage-owned question.
```

Core rule:

```text
A skill may read what it needs to prove its owned claim.
If it reads beyond the default and conditional set, it records why.
```

### Evidence access contract

Each participating skill should include a short section:

```md
## Evidence access

Use the smallest sufficient evidence set.

Read default evidence first. Read conditional evidence only when the trigger applies.

If you read beyond this skill's default and conditional set, record the reason in the result or owning artifact.

Only include `Evidence expansion` output when substantive out-of-set evidence was read.

Do not broad-search authoritative documents just to discover paths or state. Use `docs/workflows.md`, active metadata, headings, stable IDs, counts, targeted excerpts, and diffs before broad reads.

Full-file reads are allowed only when the whole file is the target, the relevant section cannot be isolated safely, bounded evidence is contradictory or incomplete, or the decision depends on whole-file context.
```

### Existing input contract preservation

This proposal does not silently remove existing mandatory operating inputs.

When updating a skill, classify current inputs as:

```text
- standing operating instructions
- default task evidence
- conditional task evidence
- expansion evidence
- obsolete or duplicated guidance
```

Any removed or downgraded input must have a rationale.

Each touched skill should use a small migration table or equivalent review-visible note:

```md
| Existing input | New classification | Rationale |
|---|---|---|
| `CONSTITUTION.md` | standing/conditional governance evidence | read when governance or source-of-truth constraints matter |
| active plan | default evidence for implement | owns milestone scope |
| actual diff | default evidence for code-review | owns review surface |
```

### Evidence expansion rule

When a skill expands beyond its default and conditional evidence set, record a compact reason.

Bounded discovery is not evidence expansion.

Bounded discovery includes:

```text
- path inventory
- heading scan
- line-number search
- count query
- targeted diff summary
- metadata lookup
```

Evidence expansion begins when the skill reads substantive content outside its default or triggered conditional set. Record a reason only for substantive out-of-set reads, not for bounded discovery.

Preferred shape:

```md
## Evidence expansion

| Artifact read | Reason | Trigger | Bounded method | Result |
|---|---|---|---|---|
| `docs/adr/ADR-...md` | Needed to verify architecture constraint | Milestone touches adapter packaging | Read decision section only | Constraint applied |
```

For chat output, a one-line form is acceptable:

```text
Evidence expansion: read ADR-20260424 because the current milestone changes adapter packaging; read decision section only.
```

Do not require this for normal default evidence.

Only include `Evidence expansion` in the result or owning artifact when expansion occurred.

### Stage default evidence sets

#### `proposal`

Default evidence:

```text
- user request
- VISION.md when proposal fit matters
- CONSTITUTION.md for governance, source-of-truth, workflow, or release-policy changes
- related proposal only when superseding or extending it
```

Conditional evidence:

```text
- docs/project-map.md when architecture/repository orientation matters
- existing specs/ADRs when the proposal changes their direction
- docs/workflows.md when artifact placement or workflow routing matters
- code only when current behavior is part of the decision
```

Expansion examples:

```text
Read implementation code only when the proposal depends on current behavior.
Read multiple prior proposals only when continuity, supersession, or conflict matters.
```

#### `proposal-review`

Default evidence:

```text
- proposal under review
- user's original request or initial intent
- VISION.md / CONSTITUTION.md when standing gates or vision fit matter
```

Conditional evidence:

```text
- linked specs, ADRs, plans, or learn sessions only when the proposal relies on them
- docs/workflows.md when workflow behavior or artifact placement is proposed
- code only when the proposal depends on current implementation reality
```

Expansion trigger:

```text
Read broader governance or related artifacts only when the proposal claims they are affected or conflicts are suspected.
```

#### `spec`

Default evidence:

```text
- accepted proposal
- latest proposal-review result
- review-resolution if proposal-review findings exist
- existing related spec when amending, superseding, or overlapping behavior
```

Conditional evidence:

```text
- architecture/ADR when behavior depends on design constraints
- docs/workflows.md when artifact placement or workflow behavior matters
- code only when current behavior must be specified and no artifact describes it
- CONSTITUTION.md when governance or source-of-truth constraints are active
```

Expansion trigger:

```text
Read broader code/docs only when the behavior contract cannot be written from proposal/review/spec context.
```

#### `plan`

`plan` evidence guidance is included as future-slice design context only. The first slice does not update `plan` unless proposal-review promotes it into scope.

Default evidence:

```text
- accepted proposal
- approved spec
- test spec when present
- architecture/ADR when relevant
- docs/plan.md and active plan only when updating existing plan state
```

Conditional evidence:

```text
- docs/project-map.md when repository orientation is unclear
- relevant code/tests/CI only for implementation sequencing and validation planning
- review-resolution when planning review-finding fixes
```

Expansion trigger:

```text
Read broader repository surfaces only when the plan cannot identify affected files, dependencies, or validation from bounded evidence.
```

#### `implement`

Default evidence:

```text
- active plan Current Handoff Summary
- current milestone section
- approved spec
- test spec
- code and tests named by the milestone
- validation commands for the milestone
```

Conditional evidence:

```text
- architecture/ADR when the milestone touches architecture boundaries
- review-resolution when implementing accepted review findings
- docs/workflows.md when stage routing or artifact placement is ambiguous
- CONSTITUTION.md when governance, source-of-truth, or safety constraints matter
- neighboring files only when needed to follow existing patterns
```

Expansion trigger:

```text
Read beyond the milestone only when bounded evidence is missing, stale, contradictory, or insufficient to implement the approved slice.
```

#### `code-review`

Default evidence:

```text
- actual diff or changed files
- approved spec
- test spec
- current plan milestone
- validation evidence
- relevant tests
```

Conditional evidence:

```text
- architecture/ADR when architecture is touched
- review-resolution when reviewing fixes for findings
- change metadata when lifecycle state or review closeout matters
- CONSTITUTION.md when source-of-truth, governance, or safety boundaries matter
- related code paths when the diff depends on them
```

Expansion trigger:

```text
Read broader specs, docs, historical reviews, or generated outputs only when the diff, finding, validation result, or user request names them.
```

### Where this model lives

Use this ownership split:

```text
docs/workflows.md:
  operational evidence-access model and bounded-read lookup order

specs/skill-contract.md or focused cost-bounded-rigor spec:
  normative rule only if validators enforce the contract, default/conditional sets become mandatory across many skills, or review finds drift between skills

individual skills:
  concise default/conditional evidence sets

scripts/test-skill-validator.py:
  static checks for required evidence-access sections in first-slice skills

docs/reports/token-cost/:
  measurement and diagnostics, not policy
```

`docs/workflows.md` already functions as the artifact-location and workflow guide. The project artifact-location work says `docs/workflows.md` provides the project-local artifact-location map, while specs, schemas, and references define exact shapes and validation rules.

The first slice is operational guidance. It does not create a new normative spec unless the implementation adds validator-enforced requirements.

### First implementation slice

Keep the first slice focused on proposal-side evidence control.

In scope:

```text
- add evidence-access contract wording to docs/workflows.md
- update proposal and proposal-review skills
- update spec only if needed for immediate proposal-to-spec handoff
- add concept-level static skill-validator checks only if needed
```

Out of scope:

```text
- implement
- code-review
- plan
- updating every skill
- runtime enforcement
- semantic read auditing
- hard token limits
- lifecycle token-cost summary implementation
- full progressive-loading implementation
```

Why these skills first:

```text
proposal and proposal-review prevent early scope amplification
spec controls requirement evidence only when the first handoff needs it
implement and code-review are high-cost, high-risk evidence consumers and move to a later execution/review slice
```

## Expected behavior changes

Before:

```text
A skill can read many plausible artifacts without saying why.
```

After:

```text
The skill starts from its default evidence and records a reason when expanding beyond it.
```

Before:

```text
Agents broad-search authoritative docs to find paths or state.
```

After:

```text
Agents use active artifacts, docs/workflows.md, headings, counts, diffs, and targeted excerpts first.
```

Before:

```text
Token-cost guidance is general.
```

After:

```text
Each participating stage has a concrete evidence-access model.
```

## Architecture impact

No runtime architecture change.

This is a workflow/skill-contract improvement affecting stage guidance and token-cost behavior.

Affected surfaces may include:

```text
docs/workflows.md
skills/proposal/SKILL.md
skills/proposal-review/SKILL.md
skills/spec/SKILL.md
skills/implement/SKILL.md
skills/code-review/SKILL.md
scripts/test-skill-validator.py
```

No adapter packaging, release artifact, or generated-output source model changes are expected.

## Testing and verification strategy

Suggested M1 validation:

```bash
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/select-validation.py --mode explicit --path docs/workflows.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md
python scripts/measure-skill-tokens.py
git diff --check --
```

If M1 updates `spec`, include `--path skills/spec/SKILL.md` in the selected validation command and diff check.

Suggested M2 validation:

```bash
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/select-validation.py --mode explicit --path skills/implement/SKILL.md --path skills/code-review/SKILL.md
python scripts/measure-skill-tokens.py
git diff --check --
```

If the implementation only changes skill wording and workflow docs, do not run release validation or adapter artifact validation unless selected validation requires it.

## Rollout and rollback

### Rollout

#### M1 - Proposal-side evidence access

- Add the shared model to `docs/workflows.md`.
- Add concise evidence-access sections to `proposal` and `proposal-review`.
- Update `spec` only if immediate proposal-to-spec handoff needs the same evidence-access rule.

#### M2 - Execution/review evidence access

- Add concise evidence-access sections to `implement` and `code-review`.
- Align `plan` only if proposal-review or M2 implementation finds planning evidence access is needed.

#### M3 - Static validation

- Add static checks only if needed to prevent the section from being accidentally removed.
- Keep checks concept-based and avoid exact long wording requirements.

Concept checks may look for:

```text
Evidence access
default evidence
conditional evidence
record the reason
bounded evidence before broad reads
full-file reads allowed when bounded evidence is insufficient
```

#### M4 - Measurement

- Run static token measurement.
- Record whether skill size increased or decreased.
- Defer dynamic benchmark comparison unless the plan/test-spec requires it.

### Rollback

If the evidence-access model causes unsafe under-reading:

```text
restore broader read permissions
keep the expansion-reason rule
add clearer full-file-read escape conditions
```

If the sections make skills too long:

```text
move shared wording to docs/workflows.md
keep only per-skill default/conditional evidence tables
```

If static checks are brittle:

```text
downgrade them to review guidance until examples stabilize
```

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Agents under-read important evidence | Preserve conditional evidence and full-file-read escape rules |
| Skills become longer | Keep per-skill sections concise; move shared explanation to docs/workflows.md |
| Evidence expansion log becomes bureaucracy | Require it only for substantive out-of-set reads; bounded discovery is not expansion |
| Static checks become brittle | Use concept checks, not long exact text |
| Review rigor weakens | Keep code-review and formal review evidence requirements intact |
| Token savings are not measured | Run static measurement and optional dynamic checks when triggered |

## Open questions

| Question | Proposed handling |
|---|---|
| Should this become normative in `specs/skill-contract.md` or a focused cost-bounded-rigor spec? | Not in M1. Add a spec only if validators enforce the contract, default/conditional sets become mandatory across many skills, or review finds drift between skills. |
| Should static validation be added immediately or only after the wording stabilizes? | Treat it as conditional work: add concept checks only if needed to prevent accidental removal. |
| Should the first slice include `plan` even though design context defines a plan evidence set? | No. Defer `plan` unless proposal-review promotes it into scope. |
| How much dynamic measurement is required for this first slice? | Do not require dynamic benchmark comparison unless the plan/test-spec later requires it. |

## Decision log

| Date | Decision | Reason |
|---|---|---|
| 2026-05-14 | Propose stage evidence access contracts. | High token cost comes from unbounded evidence collection and broad reads across stages. |
| 2026-05-14 | Use default/conditional/expansion read sets instead of hard allow-lists. | Hard allow-lists risk under-reading; unlimited reads waste tokens. |
| 2026-05-14 | Define design guidance for proposal, proposal-review, spec, plan, implement, and code-review. | These stages are high leverage for scope, requirements, planning, implementation, and review cost. |
| 2026-05-14 | Split rollout into proposal-side M1 and execution/review M2. | Proposal-side evidence control addresses the earliest amplification point without weakening implementation or review inputs too early. |
| 2026-05-14 | Preserve existing input contracts through migration classification. | Cost reduction must not silently downgrade mandatory operating instructions or safety context. |

## Next artifacts

```text
proposal-review
spec, if this becomes normative skill-contract behavior
plan
test-spec
implement
code-review
explain-change
verify
pr
```

## Follow-on artifacts

- Proposal-review finding record: `docs/changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording/reviews/proposal-review-r1.md`
- Proposal-review approval: `docs/changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording/reviews/proposal-review-r3.md`
- Review-resolution closeout: `docs/changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording/review-resolution.md`
- Spec: `specs/stage-evidence-access-contracts-for-cost-bounded-rigor.md`

## Readiness

Accepted after clean proposal-review evidence. The focused spec owns the next contract step.

## Acceptance criteria

- `docs/workflows.md` defines the stage evidence access model.
- M1 updates `proposal` and `proposal-review`; `spec` is updated only if immediate proposal-to-spec handoff needs it.
- M2 updates `implement` and `code-review`; `plan` is aligned only if promoted into scope.
- Each participating skill has default evidence and conditional evidence guidance.
- Each participating skill says expansion beyond default/conditional evidence must record a reason.
- Each touched skill preserves existing mandatory operating inputs or records a rationale for removal or downgrade.
- Bounded discovery is not treated as evidence expansion.
- `Evidence expansion` output appears only when substantive out-of-set evidence was read.
- Skills discourage broad authoritative-document searches for path/state discovery.
- Full-file reads remain allowed when bounded evidence is insufficient or the whole file is the review target.
- Safety-critical review, validation, material-finding, and source-of-truth rules remain intact.
- Static skill token measurement is run after changes.
- No hard token gates are introduced.

## Core invariant

```text
Read the smallest sufficient evidence.

Do not under-read.

When reading outside the normal set, record why.
```
