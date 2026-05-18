# Proposal: Customer-Portable Public Skills and Token-Friendly Local Guidance

## Status

accepted

## Problem

RigorLoop is now installable and usable outside the RigorLoop repository. That changes the public skill contract.

Inside the RigorLoop repository, skills can refer to internal artifacts such as:

```text
CONSTITUTION.md
AGENTS.md
specs/
docs/workflows.md
docs/architecture/
docs/reports/
docs/follow-ups.md
```

But in a customer project, those RigorLoop repository artifacts usually do not exist. A customer project may only have:

```text
installed public skills
rigorloop.yaml
rigorloop.lock
docs/workflows.md, if generated or adopted
docs/changes/<change-id>/, if created
the customer's own source files
```

Therefore, public skills must not rely on RigorLoop-internal specs, docs, reports, or governance files as required context. If they do, the skill becomes token-expensive and brittle in real customer projects.

RigorLoop has already accepted the cost-bounded rigor direction: preserve rigor, reduce waste, and make each stage prove the smallest sufficient thing with the smallest sufficient evidence. It also accepted the stage evidence access model: default evidence, conditional evidence, justified expansion, and bounded reads before broad reads.

The next step is to make those principles customer-portable.

Core problem:

```text
Public skills currently risk depending on RigorLoop repository documentation that customer projects do not have.
```

Core goal:

```text
Public skills must carry the minimum portable operating contract needed to work in any project,
while using project-local docs only when those docs exist.
```

## Goals

- Make public skills usable in customer projects without requiring RigorLoop repository docs or specs.
- Keep public skill wording simple, concise, and operational.
- Preserve rigor by embedding essential claim boundaries, stop conditions, and output obligations inside the skill itself.
- Use customer-project-local artifacts when present, especially `docs/workflows.md`, `rigorloop.yaml`, `rigorloop.lock`, and `docs/changes/<change-id>/`.
- Avoid broad searches across absent or irrelevant RigorLoop repository documentation.
- Reduce token cost by removing references that make agents search for unavailable internal docs.
- Keep RigorLoop-internal specs and docs as the development authority for the RigorLoop repository, not as required runtime dependencies for customer projects.
- Measure static skill cost before and after the change.
- Preserve the accepted single-authored skill source model: edit canonical skills under `skills/`; generated adapters remain release output.

## Non-goals

- Do not copy the full RigorLoop specs into every customer project.
- Do not make public skills longer by embedding every internal rule.
- Do not weaken safety-critical review, verification, material-finding, mutation-safety, or release-boundary rules.
- Do not implement `rigorloop status`, `rigorloop validate`, workflow YAML, or generated workflow docs in this proposal.
- Do not rewrite every skill in one implementation slice.
- Do not turn `docs/workflows.md` into a required precondition for every skill invocation.
- Do not make RigorLoop repository internals part of the customer-project public skill contract.
- Do not introduce hard token gates in this proposal.

## Vision fit

fits the current vision

This proposal improves RigorLoop's public usability. It keeps RigorLoop rigorous while making the installed skill experience simpler, cheaper, and more portable.

## Context

The accepted cost-bounded rigor proposal already says the remaining cost problem is workflow amplification: broad proposal scope, broad evidence collection, repeated findings, repeated validation, and repeated state reconciliation. It recommends the principle:

```text
Smallest sufficient decision.
Smallest sufficient evidence.
Smallest sufficient artifact set.
Smallest sufficient validation set.
```

The accepted stage evidence access proposal defines the missing operating model:

```text
default evidence set
+ conditional evidence set
+ justified expansion
+ bounded-read rule
```

It also says public skills should start from the smallest sufficient evidence set and record a reason when they expand beyond the default and conditional evidence.

Those proposals are correct for RigorLoop itself. This proposal adds the missing product boundary:

```text
In customer projects, the public skill cannot assume RigorLoop's internal docs/specs exist.
```

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Customer projects cannot use RigorLoop repo specs/docs. | in scope | Problem; Recommended direction |
| Public skills must not rely on RigorLoop-internal docs. | in scope | Goals; Public skill dependency rule |
| Token-cost and simplification proposals already exist. | in scope | Context; Recommended direction |
| Optimize skills to be simple and concise. | in scope | Goals; Essential skill content rule |
| Preserve rigor. | in scope | Goals; Non-goals; Risks and mitigations |
| Do not build more product features first. | in scope | Non-goals; Scope budget |

## Options considered

### Option 1: Keep current public skill wording

Advantages:

- No immediate skill churn.
- Existing RigorLoop repository workflows keep working.
- No validator or measurement changes are needed.

Disadvantages:

- Customer-installed skills can continue implying that RigorLoop repository docs are available.
- Agents may waste tokens searching for missing internal artifacts.
- Public skill behavior remains brittle outside this repository.

### Option 2: Copy internal workflow specs and docs into customer projects

Advantages:

- Public skills could continue depending on familiar RigorLoop artifacts.
- Customer projects would have more complete workflow reference material.

Disadvantages:

- Expands installation footprint and token cost.
- Makes customer projects inherit internal RigorLoop development detail they do not need.
- Conflicts with the goal of concise, portable public skills.

### Option 3: Embed a concise portable operating contract in public skills

Advantages:

- Public skills work from the user request, the skill's own contract, and project-local artifacts.
- Customer projects can use local workflow guidance when present without requiring it.
- RigorLoop repository specs remain internal development authority instead of runtime dependencies.
- Static validation can catch obvious regressions.

Disadvantages:

- Requires carefully auditing and updating selected high-risk skills.
- Requires discipline to keep essential behavior in the skill without copying full specs into it.

## Recommended direction

Choose Option 3.

Adopt a Customer-Portable Public Skill Contract.

Public skills should follow this rule:

```text
The skill must work from its own concise operating contract,
the user request,
and customer-project-local artifacts.

RigorLoop repository docs may guide RigorLoop development,
but they are not required customer-project evidence.
```

Use this ownership split:

```text
Public skill:
  minimum portable operating contract

Customer project docs/workflows.md:
  optional project-local artifact map and workflow guide, created or refreshed by the workflow skill

rigorloop.yaml / rigorloop.lock:
  optional project-local CLI/config state

RigorLoop specs/docs:
  internal development authority for the RigorLoop repository

Validators/tests:
  enforce shape and safety where available
```

## Customer-portable public skill contract

Public skills operate in customer-project mode by default.

They should not require RigorLoop repository-internal docs, specs, reports, or governance files as customer-project evidence.

They may use project-local `docs/workflows.md`, `rigorloop.yaml`, `rigorloop.lock`, `docs/changes/<change-id>/change.yaml`, specs, or governance files when those files exist and are relevant.

If project-local guidance is absent, skills use portable defaults where safe and block on ambiguity where no safe default exists.

Any removed internal reference should preserve the skill's essential claim boundaries, stop conditions, and output obligations.

## Repository mode boundary

Public skills operate in customer-project mode by default.

A skill may use RigorLoop repository-internal docs only when one of these is true:

- the current repository is the RigorLoop repository;
- the user explicitly asks to work on RigorLoop itself;
- the file is the direct target of the task;
- the file exists as a project-local artifact and is relevant to the task.

A skill should not broad-search for RigorLoop internal specs or docs in customer-project mode.

## Public skill dependency rule

Public skills should not say, as a required step:

```text
Read specs/...
Read docs/architecture/...
Read docs/reports/...
Read docs/follow-ups.md
Read RigorLoop CONSTITUTION.md
Read RigorLoop AGENTS.md
```

unless the skill is explicitly operating inside the RigorLoop repository or those files exist as project-local customer files.

Preferred wording:

```md
Use project-local workflow guidance when present.

If `docs/workflows.md` exists, use it for artifact locations and routing.
If it does not exist, use this skill's portable defaults and stop on ambiguity.
```

Avoid wording like:

```md
Read the RigorLoop workflow spec before proceeding.
```

Use:

```md
Follow the project-local workflow guide when present; otherwise use this skill's portable defaults.
```

## Customer-project evidence model

In a customer project, public skills should use this evidence order:

```text
1. explicit user-provided path, change ID, or instruction
2. current project files directly relevant to the task
3. active local workflow artifacts, such as:
   - docs/workflows.md
   - rigorloop.yaml
   - rigorloop.lock
   - docs/changes/<change-id>/change.yaml
   - review-log.md / review-resolution.md when present
4. targeted headings, stable IDs, diffs, or file excerpts
5. full-file reads only when bounded evidence is insufficient
6. stop and report missing local guidance when placement or status is ambiguous
```

Public skills should not broad-search for RigorLoop repository specs in a customer project.

## Missing local guidance behavior

When `docs/workflows.md`, `rigorloop.yaml`, or `docs/changes/<change-id>/change.yaml` is absent, use artifact-specific behavior:

| Need | Behavior |
|---|---|
| proposal/spec/plan output path | Use the skill's portable default unless a user path conflicts. |
| artifact placement with no safe default | Block and ask for the path. |
| formal review recording with no selectable change root | Report recording blocked instead of inventing a path. |
| upstream lifecycle/status reliance | Block if status evidence is missing or ambiguous. |
| validation command selection | Do not claim validation passed; report the missing validation surface. |
| architecture or repository orientation | Use bounded project-local evidence, or request/create a project map only when needed. |

## Essential skill content rule

Each public skill should contain the minimum contract needed to run safely without RigorLoop repository docs.

Keep inside the skill:

```text
what this skill is for
what to read first
what to produce
when to stop
what not to claim
required output shape
safety-critical blockers
```

Move out of the skill or keep internal to RigorLoop development:

```text
long examples
long path tables
internal spec references
full lifecycle policy prose
full validator implementation details
historical rationale
```

This matches the progressive-loading direction: a token-friendly skill is not only shorter; it helps the agent do the right narrow read first.

## Safety-preservation checklist

For every touched skill, the implementation should include a small migration note or equivalent review-visible evidence:

```md
| Removed or rewritten wording | Why safe | Essential rule preserved where |
|---|---|---|
```

Review should check that the change preserves:

- claim boundaries;
- stop conditions;
- required output shape;
- material-finding and review-recording rules for review skills;
- verification and PR readiness boundaries;
- mutation safety for CLI-related skills;
- release-boundary rules where relevant;
- the rule that required behavior is not moved only into RigorLoop-internal docs.

## Proposed public skill wording pattern

Use a short common pattern, not a long shared template.

```md
## Project-local evidence

Use customer-project-local artifacts.

Read `docs/workflows.md`, `rigorloop.yaml`, `rigorloop.lock`, or `docs/changes/<change-id>/change.yaml` only when they exist and are relevant.

Do not rely on RigorLoop repository specs or docs being present in the customer project.

If project-local guidance is missing, use this skill's portable defaults and stop on ambiguity.
```

For path-related skills:

```md
Default path: <portable default>.

Use the project-local workflow guide when it customizes this path.
If no guide exists and the default is unsafe or ambiguous, stop and ask for the path.
```

For review skills:

```md
Record review evidence using the project-local change root when available.

If no change root or change ID can be selected safely, report recording as blocked instead of inventing a path.
```

## Project-map caveat

`project-map` is a special case because its purpose is to map an existing repository. It may read project-local repository artifacts for orientation, including local docs, specs, package files, tests, and CI configuration when those files are relevant.

It should not assume RigorLoop repository governance files exist in a customer project.

When `AGENTS.md`, `CONSTITUTION.md`, `docs/`, or `specs/` are absent, `project-map` should continue mapping from available project-local files instead of searching for RigorLoop originals.

## Workflow guide ownership

The `workflow` skill owns creating or refreshing a customer project's local `docs/workflows.md` when RigorLoop is being adopted, artifact locations are missing, or routing depends on local workflow guidance.

Stage skills may use that project-local guide when it exists, but should not hard-require it for every task.

Use this rule:

```text
workflow generates local guidance.
stage skills use local guidance when present.
stage skills fall back to portable defaults when safe.
stage skills block on ambiguity when no safe default exists.
```

## Expected behavior changes

Before:

```text
A customer-installed public skill may imply that RigorLoop repository docs/specs are available.
```

After:

```text
The skill works from project-local artifacts and its own portable contract.
```

Before:

```text
An agent may search broadly for RigorLoop specs/docs in a customer project.
```

After:

```text
The agent starts from the user request, local artifacts, and bounded evidence.
```

Before:

```text
Skill simplification can accidentally move required behavior into RigorLoop-only docs.
```

After:

```text
Essential behavior stays in the skill; long internal rationale stays in RigorLoop docs/specs.
```

## Architecture impact

No runtime architecture change is expected.

This is a public skill-surface and documentation-boundary change.

Affected surfaces may include:

```text
skills/*/SKILL.md
docs/workflows.md
scripts/test-skill-validator.py
scripts/validate-skills.py
docs/reports/token-cost/
```

If canonical public skills change, implementation should validate generated public adapter output from canonical `skills/` using temporary or release-output generation.

Generated adapter bodies must not be hand-edited.

## Testing and verification strategy

Suggested validation:

```bash
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/measure-skill-tokens.py
python scripts/build-skills.py --check
git diff --check --
```

If the implementation changes exported/public skills, generated adapter output validation is required from canonical skills, not by editing generated bodies.

Suggested check:

```bash
python scripts/build-adapters.py --version <current-or-next-version> --output-dir <tmp-output>
python scripts/validate-adapters.py --root <tmp-output> --version <current-or-next-version>
```

If the touched skills are among previously high-cost skills, record whether the targeted customer-fixture dynamic benchmark should add any scenario beyond the first-slice default set.

## Rollout and rollback

Roll out through small implementation milestones:

```text
M1: Audit
M2: Skill wording
M3: Static checks
M4: Measurement
M5: Review and release consideration
```

Rollback is straightforward for skill wording and validator changes: revert the affected canonical skill edits and static checks, regenerate or revalidate adapter output from canonical sources as needed, and keep any token-cost report as historical evidence if it was already recorded.

### M1: Audit

- Search public skills for required RigorLoop-internal doc/spec dependencies.
- Classify each occurrence as:
  - required dependency;
  - optional project-local reference;
  - RigorLoop-repository-only reference;
  - safe governance reminder;
  - obsolete or removable wording.

### M2: Skill wording

- Apply concise project-local evidence wording.
- Preserve critical rules and output contracts.
- Avoid long shared templates.

### M3: Static checks

- Add focused static validation for forbidden required internal-doc dependency wording.
- Avoid semantic scoring.

### M4: Measurement

- Run static token measurement.
- Compare before/after.
- Run a targeted customer-fixture dynamic benchmark.
- Compare whether runtime evidence behavior avoids absent RigorLoop-internal documents.

### M5: Review and release consideration

- Code-review skill wording and static checks.
- If the public skill surface improves meaningfully, consider a patch release.

## Scope budget

| Work item | Treatment | Reason |
|---|---|---|
| Audit public skills for RigorLoop-internal required-document references | first-slice candidate | Directly addresses customer portability. |
| Add concise customer-project evidence wording to selected skills | first-slice candidate | Makes skills usable outside RigorLoop repo. |
| Update `docs/workflows.md` to clarify public/customer distinction | first-slice candidate | Keeps project-local guide role clear. |
| Static checks for forbidden internal-doc dependency wording | first-slice candidate | Prevents regression. |
| Targeted customer-fixture dynamic benchmark | first-slice candidate | Runtime behavior, not only static size, proves the agent does not search for unavailable RigorLoop internals. |
| Full rewrite of all skills | out of scope | Too broad and risky. |
| `rigorloop status`, `validate`, workflow YAML | out of scope | Product features, not skill portability. |
| New hard token gates | out of scope | Premature. |
| Full release benchmark suite | optional follow-up | Use if release scope or high-cost skill changes make it warranted. |

Scope budget treatment values:

```text
first-slice candidate:
  likely belongs in the first implementation slice, subject to proposal-review and plan shaping

optional follow-up:
  valuable only if a named trigger applies

out of scope:
  explicitly not part of this proposal
```

## First implementation slice

Keep the first slice small.

### First-slice boundary

The first implementation slice starts with an audit.

The audit classifies public-skill references to RigorLoop-internal docs as:

- required dependency;
- optional project-local reference;
- RigorLoop-repository-only reference;
- safe governance reminder;
- obsolete or removable wording.

The implementation may update only skills with required or misleading internal-document dependencies.

Do not update every skill merely to add uniform wording.

### In scope

Audit and update only public skills where internal-document dependency creates customer-project risk.

First-slice touched skills:

```text
proposal
proposal-review
spec
plan
implement
verify
pr
project-map
```

These skills have audit-proven customer-project-risky wording because they name governance, workflow, spec, plan, architecture, review, validation, or repository-orientation artifacts that are valid in RigorLoop repository mode but need explicit project-local framing in customer-project mode.

### First-slice audit output

The audit should record these first-slice touched skills and why each is touched:

| Skill | Audit result | Reason |
|---|---|---|
| `proposal` | Touch | Names `AGENTS.md`, `CONSTITUTION.md`, `VISION.md`, `docs/project-map.md`, existing specs/ADRs, and `docs/workflows.md` as evidence or gates; these need project-local framing and portable defaults when absent. |
| `proposal-review` | Touch | Reads `AGENTS.md`, `CONSTITUTION.md`, `VISION.md`, linked specs/ADRs/plans/learn sessions, `docs/project-map.md`, and `docs/workflows.md`; it needs the same customer-local caveat and no broad search for RigorLoop originals. |
| `spec` | Touch | Inputs include `AGENTS.md`, `CONSTITUTION.md`, `docs/project-map.md`, related specs, architecture docs, and ADRs; add project-local when present and relevant wording. |
| `plan` | Touch | Inputs include `AGENTS.md`, `CONSTITUTION.md`, `docs/plan.md`, `docs/project-map.md`, accepted proposal, spec, architecture, test spec, code/tests, and CI; add explicit customer-project mode wording. |
| `implement` | Touch | Inputs include `AGENTS.md`, `CONSTITUTION.md`, specs, test specs, architecture, code/tests, and validation commands; keep the change small and make those project-local when present and relevant. |
| `workflow` | Touch lightly | Owns creating or refreshing local `docs/workflows.md`; add one short caveat to avoid requiring RigorLoop repository-internal docs and to route absent or ambiguous local guidance safely. |
| `verify` | Touch | Lists `AGENTS.md` and `CONSTITUTION.md` among final verification inputs; these should be optional project-local governance evidence, not RigorLoop-internal evidence. |
| `pr` | Touch | Lists `AGENTS.md` and `CONSTITUTION.md` if relevant and uses lifecycle artifacts as PR evidence; add the customer-local caveat while preserving readiness boundaries. |
| `project-map` | Touch lightly | Reads `README.md`, `AGENTS.md`, `CONSTITUTION.md`, `docs/`, and `specs/` if present; this is valid for mapping a customer repo, but it should say these are local repository artifacts and absence is normal. |

Watchlist skills:

| Skill | First-slice treatment | Reason |
|---|---|---|
| `code-review` | Do not touch unless audit proves risk | `code-review` is safety-critical and already emphasizes actual diff, governing artifacts, validation evidence, direct proof, and claim boundaries. Avoid editing it unless a concrete required internal-doc dependency is found. |

The audit should not expand the touched list merely to make wording uniform.

The implementation may update only audited skills with required or misleading internal-document dependencies, plus `docs/workflows.md` for the concise customer-project distinction.

The workflow skill edit should be limited to a short caveat:

```md
## Customer-project workflow guide

In customer projects, create or refresh the project-local `docs/workflows.md` when RigorLoop is being adopted, artifact locations are missing, or routing depends on local workflow guidance.

Do not require RigorLoop repository-internal specs or docs to be present. Use project-local guidance when available; otherwise use portable defaults and block on ambiguity.
```

`code-review` should remain unchanged in the first slice unless the audit finds a direct required internal-doc dependency such as:

```text
must read RigorLoop CONSTITUTION.md
must read RigorLoop specs/
must read RigorLoop docs/
```

### First-slice changes

- Replace required RigorLoop-internal doc references with project-local wording.
- Keep portable defaults in each skill.
- Add a concise project-local evidence rule where needed.
- Preserve safety-critical rules.
- Add static validator checks for obvious bad wording.
- Run static token measurement before and after.
- Record a targeted customer-fixture dynamic benchmark.

### Out of scope

- Deep progressive-loading rewrite of `workflow`, `implement`, or `code-review`.
- Full evidence-access contract for every skill.
- CLI feature changes.
- Customer-project docs generation changes.
- Release/package changes.

## Static validation ideas

Add focused static checks, not broad natural-language scoring.

Check public skill files for forbidden or risky required internal dependencies such as:

```text
must read RigorLoop specs/
must read RigorLoop CONSTITUTION.md
must read RigorLoop AGENTS.md
read the RigorLoop workflow spec before proceeding
required: docs/reports/token-cost/
```

Allow safer forms:

```text
if present
project-local
when operating inside the RigorLoop repository
when this file is the review target
when the user provided this path
when governing project docs exist
```

Add checks for the presence of portable fallback wording in touched skills:

```text
project-local
portable default
stop on ambiguity
docs/workflows.md when present
```

Static checks should catch obvious required RigorLoop-internal-doc dependencies without blocking legitimate project-local docs/spec references.

## Measurement

Static before/after measurement should live at:

```text
docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills.md
```

and optionally:

```text
docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills.yaml
```

Do not place this first-slice before/after report under `docs/reports/token-cost/releases/` unless a release is part of the same change.

The report should include:

```text
- baseline static tokens by skill
- after-change static tokens by touched skill
- total public skill delta
- risky wording removed or rewritten
- safety-preservation notes
- generated adapter validation command/result
- dynamic benchmark summary and result-quality status
```

A targeted dynamic benchmark is required for the first slice because this proposal changes runtime evidence behavior in customer projects. Static size can show whether skill text changed; the dynamic benchmark should show whether agents avoid broad searches for unavailable RigorLoop internals.

Use a customer fixture with:

```text
customer-fixture/
  rigorloop.yaml
  rigorloop.lock
  docs/workflows.md
  docs/changes/example-change/change.yaml
  docs/changes/example-change/explain-change.md
  specs/customer-feature.md
  docs/plans/customer-plan.md
  src/
  tests/
```

Deliberately exclude:

```text
CONSTITUTION.md
AGENTS.md
RigorLoop internal specs/
RigorLoop internal docs/reports/
docs/follow-ups.md
docs/project-map.md unless testing project-map creation/update
```

First-slice dynamic scenarios should be targeted:

```text
proposal-customer-no-internal-docs
proposal-review-customer-local-artifacts
spec-customer-local-workflow-guide
plan-customer-local-spec-and-code
implement-customer-plan-handoff
workflow-customer-route-no-internal-docs
project-map-customer-repo-orientation
verify-customer-final-pack
pr-customer-ready-handoff
```

Optional scenarios:

```text
code-review-customer-diff-small, only if `code-review` skill text changes
```

Measure:

```text
- whether the run tries to read absent RigorLoop internal docs
- largest command output
- full-skill reads
- broad searches
- input tokens
- result quality
- whether the output uses portable defaults or blocks on ambiguity
```

## Acceptance criteria

- Public skills no longer require RigorLoop repository specs/docs as customer-project evidence.
- Touched skills use project-local wording such as `docs/workflows.md when present`.
- Touched skills include portable defaults or stop-on-ambiguity behavior.
- Audit result is recorded.
- Audit result identifies touched skills and why each is touched.
- Touched skill list is justified by the audit.
- `docs/workflows.md` contains concise customer-project portability guidance.
- No broad rewrite of all public skills occurs merely to add uniform wording.
- Essential safety-critical behavior remains inside the skill.
- Removed or rewritten internal references include migration notes or equivalent review-visible evidence.
- Static skill validation catches obvious required RigorLoop-internal-doc dependencies without blocking legitimate project-local docs/spec references.
- Static token before/after report is recorded.
- Targeted customer-fixture dynamic benchmark is recorded.
- Benchmark proves public skills do not require RigorLoop repository-internal docs in customer projects.
- Canonical skill validation passes.
- If canonical public skills change, generated adapter output validates from temporary or release-output generation.
- No generated adapter skill body is treated as source.
- No `status`, `validate`, workflow YAML, or generated workflow docs work is added in this slice.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Skills become too vague. | Keep essential operating contract in the skill. |
| Token savings move rules into unavailable docs. | Forbid required reliance on RigorLoop-internal docs. |
| Static checks become brittle. | Check only clear dangerous phrases and required portable concepts. |
| Customer projects lack `docs/workflows.md`. | Skills use portable defaults and stop on ambiguity. |
| Safety rules are accidentally removed. | Review against safety-critical rule list. |
| Too many skills change at once. | Audit first, then touch only high-risk wording. |
| Legitimate project-local specs or docs are blocked. | Static checks focus on required RigorLoop-internal dependencies, not generic path references. |

## Open questions

None blocking focused spec.

The only remaining first-slice contingency is whether later audit evidence discovers a concrete required internal-doc dependency that justifies touching safety-critical `code-review` wording. Without that evidence, `code-review` remains unchanged.

## Decision log

| Date | Decision | Reason |
|---|---|---|
| 2026-05-17 | Treat RigorLoop repo docs/specs as internal development authority, not required customer-project evidence. | Customer projects do not have those files. |
| 2026-05-17 | Keep essential behavior inside public skills. | Skills must work when installed through adapters. |
| 2026-05-17 | Use project-local docs only when present. | Avoid broad searches and missing-doc dependency. |
| 2026-05-17 | Do not implement FU-006 through FU-009 in this slice. | Current priority is skill portability and token clarity. |
| 2026-05-18 | Keep proposal status as `draft` while recording the review verdict in readiness. | Proposal status values are constrained; the review outcome is changes requested before spec/plan. |
| 2026-05-18 | Include concise `docs/workflows.md` customer-project portability guidance in the first slice. | Public skills need one project-local guidance anchor before broad skill edits. |
| 2026-05-18 | Record static before/after measurement under `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills.md`, with optional YAML. | This is skill-optimization evidence, not release evidence unless a release is in scope. |
| 2026-05-18 | Require a targeted customer-fixture dynamic benchmark in the first slice. | Runtime behavior must prove agents stop searching for unavailable RigorLoop internals; static size alone is insufficient. |
| 2026-05-18 | First-slice touched skills are `proposal`, `proposal-review`, `spec`, `plan`, `implement`, `workflow`, `verify`, `pr`, and `project-map`; `code-review` stays watchlist unless audit proves direct risk. | Touch only audit-proven risky wording and the workflow-owned local guide caveat while avoiding a broad skill rewrite. |
| 2026-05-18 | Add one short `workflow` skill caveat because workflow owns creating or refreshing local `docs/workflows.md`; keep `code-review` unchanged unless a direct required internal-doc dependency is found. | Workflow should make customer projects self-guiding, while safety-critical review wording should not change without audit-proven need. |

## Next artifacts

```text
proposal-review
focused spec or spec amendment
plan
test-spec
implement
code-review
explain-change
verify
pr
```

Recommended focused spec title:

```text
specs/customer-portable-public-skill-evidence.md
```

Keep the spec narrow:

```text
- customer-project mode rule
- project-local evidence rule
- missing-local-guidance behavior
- static validation boundaries
- first-slice audit requirement
```

Do not put every skill rewrite into the spec.

## Follow-on artifacts

- [Customer-Portable Public Skill Evidence](../../specs/customer-portable-public-skill-evidence.md)

## Readiness

Ready for focused spec after proposal-review acceptance.

## Core invariant

```text
Public skills must work in customer projects.

Customer projects may not have RigorLoop's specs or docs.

Therefore:
skills carry the essential portable contract,
customer-local docs guide local paths when present,
and RigorLoop repository docs stay internal development authority.
```
