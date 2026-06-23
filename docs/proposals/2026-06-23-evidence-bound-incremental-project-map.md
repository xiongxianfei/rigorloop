# Proposal: Evidence-Bound and Incremental `project-map` Skill

## Status

accepted

## Problem

The current `project-map` skill has the correct fundamental purpose:

```text
Describe the repository as it exists today.
Do not invent a future design.
```

It also identifies the right orientation surfaces: modules, runtime flow, data flow, tests, CI, external boundaries, ownership, risks, and open questions.

However, several operational contracts remain implicit.

### 1. Current-state claims are not classified precisely

The skill says to separate observed facts from inferences, but it does not define:

- how to label an inference;
- what evidence is sufficient for an "observed architecture rule";
- how to distinguish configured commands from commands that were actually run;
- how to handle conflicts between code, documentation, specs, and plans.

As a result, a project map can sound authoritative even when some statements are based only on directory names or partial static inspection.

### 2. Map freshness is undefined

A project map is a living reference, but the skill does not require it to record:

- which revision or working tree it describes;
- when it was reviewed;
- which paths were inspected;
- which areas were intentionally excluded;
- what changes should trigger a refresh.

A downstream agent may therefore rely on a map that was accurate when created but is no longer current.

### 3. Repository-wide and area maps are not structurally connected

The skill permits:

```text
docs/project-map.md
docs/project-map/<area>.md
```

but does not define:

- whether the root map must always exist;
- how area maps are registered;
- how overlapping area maps are handled;
- whether area maps may become feature-specific transcripts;
- which information belongs in the root map versus an area map.

This can create orphaned maps or duplicated architecture descriptions.

### 4. The required output structure lacks a reusable skeleton

The eleven required sections are substantial enough to justify a copy-and-fill asset, but they currently live only as a numbered list in `SKILL.md`.

This makes omissions, inconsistent ordering, and output-shape drift more likely.

### 5. Source-of-truth boundaries need strengthening

A project map describes current repository reality. It should not silently treat these as equivalent evidence:

```text
current source code
runtime configuration
generated output
accepted spec
active plan
historical proposal
README description
directory name
```

In particular, planned architecture must not be represented as current architecture merely because it appears in an approved proposal or spec.

### 6. Downstream use is underspecified

The map recommends `explore`, `proposal`, or `architecture`, but it does not clearly state:

- what downstream skills may safely rely on;
- when a stale or partial map blocks downstream work;
- when architecture must inspect source directly rather than rely on the map;
- how risks are routed without turning the map into a backlog.

## Goals

- Preserve `project-map` as an observation-oriented repository orientation skill.
- Add normalized published-skill metadata and a clear workflow-role block.
- Define explicit map modes:
  - create;
  - refresh;
  - area map;
  - audit.
- Require project-map metadata describing scope, baseline, coverage, freshness, and known gaps.
- Define deterministic evidence classes for observations, inferences, and unknowns.
- Require important current-state claims to cite repository paths.
- Prevent future plans and specs from being presented as already implemented behavior.
- Define a stable relationship between the root map and area maps.
- Add a substantial project-map skeleton asset.
- Keep the root map concise and stable across unrelated changes.
- Add refresh triggers and stale-map handling.
- Clarify downstream reliance and stop conditions.
- Preserve customer-project operation without requiring RigorLoop repository internals.
- Add behavior-preservation and cold-read proof for the revised skill.

## Non-goals

- Do not turn `project-map` into an architecture-design skill.
- Do not propose future module boundaries or implementation changes.
- Do not turn the map into a backlog, plan, or follow-up registry.
- Do not require runtime instrumentation for every map.
- Do not require reading every repository file.
- Do not require every repository to have every map section populated with substantive content.
- Do not add an area map for every feature or directory.
- Do not make `docs/project-map.md` authoritative over source code, build configuration, schemas, or runtime configuration.
- Do not use proposals, plans, or unimplemented specs as proof of current behavior.
- Do not add decorative diagrams.
- Do not duplicate the complete workflow guide in the project map.
- Do not add remote scanning, telemetry, or external indexing.
- Do not hand-edit generated adapter output.

## Vision fit

fits the current vision

RigorLoop depends on work that another human or agent can inspect and resume from repository artifacts. A reliable project map reduces unsafe repository exploration while preserving the distinction between:

```text
what exists;
what is inferred;
what is unknown;
what is only planned.
```

The proposal is falsified if:

```text
- the map presents planned architecture as current reality;
- unsupported inferences are written as facts;
- area maps become orphaned or contradictory;
- stale maps are treated as current without qualification;
- project-map starts recommending implementation designs;
- map size grows with feature history instead of repository structure;
- a downstream skill relies on the map when cited evidence is missing or stale;
- the installed skill requires RigorLoop-maintainer-only files.
```

## Initial intent preservation

| Initial goal | Treatment | Where recorded |
| --- | --- | --- |
| Preserve project-map as orientation | in scope | Goals, Recommended direction |
| Describe current architecture and repository shape | in scope | Evidence contract |
| Cover runtime and data flow | in scope | Output contract |
| Cover tests, CI, and release | in scope | Output contract |
| Keep facts separate from inference | in scope | Evidence and confidence contract |
| Cite repository files | in scope | Claim evidence |
| Support narrow area maps | in scope | Root and area map contract |
| Avoid future-design proposals | in scope | Non-goals, stop conditions |
| Keep maps reusable across future work | in scope | Scope and growth strategy |
| Improve downstream use | in scope | Handoff and reliance contract |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Published-skill frontmatter normalization | core to this proposal | The current skill lacks the normalized version fields used by current public skills. |
| Workflow-role and claim-boundary block | core to this proposal | Orientation and downstream limits should be explicit. |
| Map modes | core to this proposal | Create, refresh, area, and audit operations have different effects. |
| Map metadata and freshness | core to this proposal | Downstream readers need to know what state the map describes. |
| Evidence classification | core to this proposal | Current facts and inferences must remain distinguishable. |
| Root/area map relationship | core to this proposal | Prevents orphaned or duplicated area maps. |
| Full project-map skeleton asset | first-slice candidate | The complete structure is substantial and error-prone enough to earn a file. |
| Skill-validator and fixture coverage | same-slice dependency | Validate stable contract and skeleton behavior first; expand fixtures incrementally when concrete drift appears. |
| Generated adapter proof | same-slice dependency | Updated skill and assets must ship together. |
| Automated repository graph generation | separate proposal | Larger mechanism with language and build-system complexity. |
| Runtime tracing | separate proposal | Useful only where static evidence is insufficient. |
| General project-map artifact validator | deferable follow-up | Add only after concrete drift appears in two or more produced maps after the skill contract improves. |

## Context

`project-map` is a living orientation artifact, not a normative behavior contract.

The following ownership boundaries should remain explicit:

| Question | Primary owner |
| --- | --- |
| What exists in the repository now? | source, configuration, schemas, tests, CI, and `project-map` summary |
| Why does the project exist? | `VISION.md` |
| What governance rules apply? | `CONSTITUTION.md` |
| Where do lifecycle artifacts go? | `docs/workflows.md` |
| What behavior is required? | approved specs and schemas |
| What implementation work is planned? | active plan |
| What design should be introduced? | `architecture` |
| What work should happen later? | proposal, plan, review resolution, or follow-up owner |

The project map may link to these artifacts, but it must not absorb their responsibilities.

## Options considered

### Option 1: Keep the current skill unchanged

**Pros**

- No implementation risk.
- Current guidance is directionally correct.

**Cons**

- Freshness remains implicit.
- Facts and inferences remain inconsistently represented.
- Area-map relationships remain undefined.
- Output structure can drift.

Rejected.

### Option 2: Apply a readability-only pass

Add tables, headings, and normalized frontmatter without changing the operating contract.

**Pros**

- Small change.
- Improves scanning.

**Cons**

- Does not solve stale maps, evidence quality, area-map ownership, or downstream reliance.

Insufficient.

### Option 3: Add only a project-map skeleton asset

Move the eleven required sections into `assets/project-map-skeleton.md`.

**Pros**

- Improves structural consistency.
- Reduces common-path output boilerplate.

**Cons**

- Does not resolve evidence, freshness, source ranking, or map splitting.

Insufficient alone.

### Option 4: Add evidence, freshness, scope, and area-map contracts

Preserve observation-only behavior while making the map's claims and lifecycle deterministic.

**Pros**

- Directly addresses reliability.
- Improves downstream trust.
- Keeps the skill portable.
- Supports large repositories without one unbounded map.
- Makes the map useful beyond the immediate request.

**Cons**

- Requires skill, asset, fixture, and generated-output changes.

Recommended.

### Option 5: Build an automatic repository graph generator

Use scripts to discover modules, imports, entry points, tests, and dependencies.

**Pros**

- Strong automation potential.
- Could reduce manual inspection.

**Cons**

- Language-specific.
- Risks mistaking dependency graphs for architecture.
- Larger trust and maintenance surface.
- Does not replace semantic observation.

Deferred.

## Recommended direction

Choose **Option 4**, with the structural skeleton from Option 3.

The governing model should be:

```text
project-map records current repository orientation;
code and configuration provide current-state evidence;
the map labels inference and uncertainty;
the root map stays concise;
area maps provide bounded depth;
architecture owns future design.
```

## Published-skill contract

### Frontmatter

Normalize the skill frontmatter:

```yaml
---
name: project-map
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Build, refresh, or audit a current-state repository orientation map. Use when
  architecture, module boundaries, runtime flow, data flow, test layout, CI,
  ownership, or change placement is unclear. This skill records observed
  repository structure and bounded inferences; it does not invent future
  architecture or act as a backlog.
argument-hint: [repository, area, orientation question, or refresh scope]
---
```

Use a newer schema version only if the governing published-skill contract names one before implementation.

### Workflow role

Add:

```md
## Workflow role

- role_name: project-map
- stage: orientation
- upstream: current repository state, project-local guidance, and the user's orientation question
- downstream: explore, proposal, architecture, or workflow routing
- summary: Create, refresh, or audit a current-state repository map with cited evidence, bounded inference, known gaps, and downstream orientation.
- must_not_claim: future architecture approval, implementation readiness, review approval, validation success, branch readiness, PR readiness, or final lifecycle closeout.
```

If `orientation` is not an accepted stage value in the governing skill contract, amend that contract or use the approved equivalent without silently inventing an unsupported enum.

## Operating modes

The skill should classify the invocation before reading broadly.

| Mode | Use | Artifact behavior |
| --- | --- | --- |
| `create` | No suitable project map exists | Create root or approved area map |
| `refresh` | Map exists but relevant repository state changed | Update affected sections and metadata |
| `area` | Repository is too large or the requested scope is a durable subsystem | Create/update an area map and register it in the root map |
| `audit` | User wants to know whether a map is current or complete | Report drift; do not rewrite unless requested |

The result should state the selected mode.

Recommended result block:

```md
## Result

- Skill: project-map
- Status: <created | updated | audited | blocked>
- Mode: <create | refresh | area | audit>
- Map scope: <repository | area:<slug>>
- Artifacts changed: <paths or none>
- Freshness result: <current | partial | stale>
- Correction note: <prior-map correction or none>
- Open blockers: <blockers or none>
- Next stage: <explore | proposal | architecture | workflow | none>
```

## Artifact placement

Use the project workflow guide when present.

Portable defaults:

```text
docs/project-map.md
docs/project-map/<area>.md
```

Lookup order:

```text
1. explicit user path;
2. current artifact metadata or active workflow context;
3. docs/workflows.md project-local artifact map;
4. portable default;
5. block on unresolved ambiguity.
```

`project-map` owns map content. The workflow skill owns project-local placement policy.

## Root and area map contract

### Root map

`docs/project-map.md` should always remain the repository-level entry point when any area map exists.

It should contain:

- repository-wide overview;
- major boundaries;
- major entry points;
- shared test and CI surfaces;
- external boundaries;
- links to area maps;
- scope and freshness summary for each area map.

### Area maps

Use:

```text
docs/project-map/<area>.md
```

only for a durable area such as:

- independently deployed service;
- bounded package group;
- major application;
- data platform;
- infrastructure subsystem;
- clearly owned domain.

Do not create an area map solely because it is relevant to one current feature.

As a practical floor, do not split an area into its own map until the root map's section for that area would exceed roughly one screen of content, or the area has its own deploy, release, ownership, package, domain, or data lifecycle.

### Registration

Every area map must be linked from the root map.

Recommended root-map table:

| Area | Map | Scope | Baseline | Freshness | Known gaps |
| --- | --- | --- | --- | --- | --- |

An area map without root registration is incomplete.

### Overlap

When two maps overlap:

- each map must name the overlap;
- one map must own the detailed description;
- the other should link rather than duplicate;
- contradictions block a clean refresh result.

## Map metadata and freshness

Every map should begin with:

```md
## Map metadata

- Map status: <current | partial | stale>
- Scope: <repository | area:<slug>>
- Baseline: <commit SHA, branch/ref, or working-tree state>
- Last reviewed: <YYYY-MM-DD>
- Coverage: <paths or subsystem boundaries inspected>
- Exclusions: <explicitly excluded areas or none>
- Parent map: <path or not-applicable>
- Known gaps: <gaps or none>
```

When Git is available, record both the baseline commit or ref and the last-reviewed date. If the working tree is dirty, record the baseline as `<sha>+dirty` and list the uncommitted paths inspected. When Git is unavailable, record the date plus a clear evidence baseline such as inspected archive, workspace, or supplied path set.

### Status meanings

| Status | Meaning |
| --- | --- |
| `current` | Relevant cited surfaces were inspected and no known material gap remains |
| `partial` | Scope is intentionally bounded or important evidence was unavailable |
| `stale` | A cited or relied-on surface is known to have materially changed |

A map must not claim `current` merely because the skill successfully produced a document.

### Incorrect prior map handling

If a refresh discovers that the previous map was wrong at its recorded baseline, not merely stale because the repository changed later, the refresh result should include a correction note. The note should identify the affected section, the corrected claim, and the evidence path proving the correction. This keeps the map status focused on the refreshed artifact while warning downstream readers that prior reliance on the corrected section was unsafe.

### Refresh triggers

Refresh the affected map when changes modify:

- top-level directory or package boundaries;
- runtime entry points;
- public module interfaces;
- service-to-service calls;
- storage models, schemas, or migrations;
- build or package manifests;
- test layout or test commands;
- CI, release, deployment, or infrastructure configuration;
- generated-source ownership;
- ownership boundaries;
- external integrations;
- files directly cited by the map in a way that changes the map's conclusion.

Unrelated commits do not automatically make every map stale.

## Evidence and confidence contract

### Evidence classes

Use three classes:

```text
observed
inferred
unknown
```

#### Observed

Supported by inspected repository evidence.

Example:

```md
Observed: `src/server.ts` creates the HTTP server and registers routes from
`src/routes/index.ts`.
```

#### Inferred

A reasonable conclusion not directly declared by a source-of-truth artifact.

Example:

```md
Inference: `packages/domain/` appears intended to isolate business logic because
it has no imports from the delivery packages in the inspected files.
```

#### Unknown

The available evidence cannot support a safe conclusion.

Record it under `Open questions` rather than guessing.

### Claim evidence

Material current-state claims must cite at least one repository path.

Directory names alone are insufficient when the content could change the conclusion.

Material claims include statements a downstream agent could use to choose a module, trust a boundary, select tests, assess runtime or data flow, or decide whether a map is safe to rely on. Examples:

- Material: "`src/server.ts` is the HTTP entry point that registers route handlers from `src/routes/index.ts`."
- Material: "`packages/domain/` has no imports from delivery packages in the inspected files, so it appears to isolate business logic."
- Incidental: "The repository has a `docs/` directory."
- Incidental: "Several Markdown files use sentence-case headings."

### Observed architecture rules

A pattern may be presented as an observed rule only when:

- an explicit project rule states it; or
- multiple independent examples consistently demonstrate it.

A single example should be described as an observed instance, not a repository-wide rule.

### Commands

Distinguish:

```text
configured command:
  found in a manifest, workflow, or script

executed command:
  actually run during this mapping session with result recorded
```

Do not say a command "works" merely because it is configured.

Read-only inspection commands such as `git log`, `ls`, test discovery commands, `--dry-run`, and `--help` may be run when useful for orientation. Commands that mutate state, hit the network, or run the actual test or build suite need the user's go-ahead. Record every executed command with its exit code in the map's evidence trail.

### Runtime and data flow

State whether a flow was:

```text
statically traced
demonstrated by tests
observed through execution
partially inferred
```

Do not imply runtime observation when only static source inspection occurred.

## Source-rank and conflict handling

For current-state claims, prefer:

```text
1. executable source and runtime configuration;
2. build/package manifests and schemas;
3. tests and CI workflows;
4. explicit current-state project documentation;
5. generated output with a known canonical source;
6. directory/file names alone.
```

Proposals, specs, architecture plans, and implementation plans describe intent. They are not proof that the intended change exists.

When intent artifacts conflict with implementation:

- describe the implementation as current state;
- cite the intent artifact as planned or expected state;
- record the discrepancy as a risk or open question;
- do not silently reconcile the two.

For governance questions, `CONSTITUTION.md` and applicable workflow rules retain their own authority. The project map does not override them.

## Required output structure

Keep the current eleven sections and add map metadata plus area-map registration.

Recommended structure:

```text
Map metadata
Purpose and scope
System overview
Repository layout
Runtime flow
Data flow
External boundaries
Test map
CI and release map
Architecture rules observed
Risk areas
Open questions
Area maps, when applicable
```

A required section with no applicable content should say:

```text
Not observed in the mapped scope.
```

and include a short rationale. Do not invent content merely to populate the section.

## Resource layout

Add one substantial structural asset:

```text
skills/project-map/
  SKILL.md
  assets/
    project-map-skeleton.md
```

Resource-map entry:

```md
## Resource map

- COPY `assets/project-map-skeleton.md` when creating a new root or area project
  map.
  Fill the metadata, applicable sections, evidence paths, known gaps, and area
  registration fields. Do not emit unfilled placeholders.
```

The asset may contain:

- headings;
- metadata fields;
- table headers;
- placeholders;
- short fill instructions.

The asset must not own:

- evidence-ranking rules;
- inference policy;
- refresh triggers;
- future-design prohibitions;
- handoff rules;
- claim boundaries.

Those remain in `SKILL.md`.

## Diagram contract

Use Mermaid only when it clarifies:

- runtime flow;
- data flow;
- module/service boundaries;
- deployment boundaries;
- external integrations.

Every node should correspond to an observed repository component or an explicitly marked external actor.

Diagram rules:

```text
- cite the files supporting the diagram;
- label inferred edges;
- do not include decorative layers;
- do not present a planned component as deployed;
- keep detailed area diagrams in the owning area map;
- keep the root diagram high level.
```

## Follow-up and backlog boundary

`project-map` may identify:

- unclear ownership;
- fragile coupling;
- missing tests;
- undocumented boundaries;
- stale documentation;
- unverified runtime assumptions.

It must not convert these directly into planned work.

Route action through:

```text
proposal
plan
learn
review resolution
release evidence
docs/follow-ups.md
```

according to `docs/workflows.md`.

A risk entry is orientation evidence, not an approved task.

## Downstream reliance and handoff

### Safe reliance

Downstream skills may use the map for:

- locating likely modules and entry points;
- finding tests and CI;
- identifying known boundaries;
- deciding which source files need direct inspection;
- recognizing known gaps and uncertainty.

### Unsafe reliance

Downstream skills must inspect source directly when:

- the relevant map is stale or partial;
- the intended change crosses an unreviewed area;
- map evidence conflicts with current code;
- architecture or security decisions depend on exact behavior;
- the cited path no longer exists;
- the map labels the relevant claim as inferred or unknown.

### Handoff

Recommended next stage:

| Finding | Next skill |
| --- | --- |
| Problem or options are unclear | `explore` |
| A direction decision is needed | `proposal` |
| Current boundaries are clear enough for future design | `architecture` |
| Workflow placement or routing is unclear | `workflow` |
| No downstream action requested | `none` |

The skill must not automatically start the downstream stage during an isolated invocation.

## Expected behavior changes

- Project maps state what repository state they describe.
- Important claims cite repository evidence.
- Inferences and unknowns are visible.
- Plans and specs are not represented as already implemented behavior.
- Root and area maps have a deterministic relationship.
- Large repositories can use bounded area maps without losing a root orientation surface.
- Downstream skills can determine whether the map is safe to rely on.
- Output structure becomes consistent through a packaged skeleton.
- The skill remains observation-only.

## Architecture impact

| Surface | Impact |
| --- | --- |
| `skills/project-map/SKILL.md` | Normalize and add evidence, freshness, scope, and handoff contracts |
| `skills/project-map/assets/project-map-skeleton.md` | New structural output asset |
| Skill validation | Validate frontmatter, resource map, asset presence, and required contract sections |
| Skill fixtures | Add the smallest representative first-slice cases; expand fixtures after concrete drift appears |
| Generated adapters | Include the updated skill and skeleton |
| Existing project maps | No automatic migration |
| Runtime application code | No change |

## Testing and verification strategy

The `PMAP-*` list is a coverage catalog, not a mandate to build every fixture before the skill contract lands. The first slice should validate the revised skill contract, skeleton asset, generated adapter inclusion, and a small representative output set. Additional fixtures should be added incrementally when concrete map drift is observed.

| Check ID | What is verified |
| --- | --- |
| `PMAP-001` | Published-skill frontmatter includes required normalized fields. |
| `PMAP-002` | Workflow role and must-not-claim boundaries are explicit. |
| `PMAP-003` | `create`, `refresh`, `area`, and `audit` modes are distinct. |
| `PMAP-004` | The output skeleton contains all required sections. |
| `PMAP-005` | A repository-wide map includes baseline, coverage, and freshness metadata. |
| `PMAP-006` | An area map names and links its parent map. |
| `PMAP-007` | A root map registers every area map. |
| `PMAP-008` | Important observed claims cite paths. |
| `PMAP-009` | Inference is visibly labeled. |
| `PMAP-010` | An unknown is recorded as an open question rather than guessed. |
| `PMAP-011` | A future spec is not represented as current implementation. |
| `PMAP-012` | Configured commands are not described as successfully executed without evidence. |
| `PMAP-013` | A stale relevant map blocks clean downstream reliance. |
| `PMAP-014` | An unrelated repository change does not make every map stale. |
| `PMAP-015` | Risks do not become plan or backlog entries automatically. |
| `PMAP-016` | Generated adapter output contains the project-map skeleton. |
| `PMAP-017` | No unfilled placeholders appear in representative output. |
| `PMAP-018` | A large-repository fixture produces a root map plus a bounded area map rather than one feature-overfit monolith. |
| `PMAP-019` | Refreshes that correct a previously wrong map section include a correction note rather than presenting the issue as ordinary staleness. |

## Behavior-preservation proof

Create:

```text
docs/changes/<change-id>/behavior-preservation.md
```

Required matrix:

| Surface | Baseline | Revised proof | Result |
| --- | --- | --- | --- |
| Orientation-only role | Current skill rule | Representative output | preserved |
| Current-state focus | Current skill rule | Intent-versus-current fixture | strengthened |
| Eleven required sections | Current list | Skeleton parity | preserved |
| Important path citations | Current rule | Claim fixture | strengthened |
| Observation/inference split | Current rule | Explicit evidence classes | strengthened |
| Narrow-area support | Current path option | Root/area registration fixture | strengthened |
| Risk routing | Existing boundary | No-backlog fixture | preserved |
| Handoff | Explore/proposal/architecture | Revised result fixture | preserved and clarified |
| Customer-project mode | Current contract | Clean installed skill proof | preserved |

## Rollout and rollback

### Rollout

1. Approve proposal.
2. Determine whether the existing skill contract needs a focused amendment.
3. Write or amend the test spec.
4. Write and review the implementation plan.
5. Record baseline skill/output behavior.
6. Normalize `SKILL.md`.
7. Add the project-map skeleton asset.
8. Add contract validation and the smallest representative output fixtures needed to prove the first slice.
9. Validate generated adapters.
10. Run a cold-read project-map exercise against:
    - a small repository;
    - a monorepo or multi-service fixture;
    - an intentionally stale map.
11. Review and verify.

### Rollback

- Restore `SKILL.md` and the asset inventory together.
- Rebuild generated outputs from canonical source.
- Preserve any recorded baseline or behavior evidence.
- Do not rewrite existing customer project maps during rollback.
- Remove validation only if the prior skill contract is fully restored.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Metadata makes maps bureaucratic | Keep the metadata block short and operational. |
| Path-citation requirements make maps noisy | Require citations for material claims, not every sentence. |
| Inference labels overwhelm readable prose | Label only claims that are not directly supported. |
| Area maps fragment repository understanding | Require root registration and one detailed owner per overlap. |
| Freshness becomes commit-age checking | Use affected-surface triggers, not elapsed time alone. |
| Skill becomes too long | Move only the full output structure into an asset; keep optional depth bounded. |
| Validators overfit natural language | Validate stable metadata, headings, resource maps, and representative fixtures rather than arbitrary prose. |
| Current-state maps drift from future specs | Keep current and planned state explicitly separate. |
| Large repositories trigger excessive reading | Require bounded scope and area maps based on durable boundaries. |

## First-slice boundary

First implementation slice:

```text
frontmatter normalization
workflow-role block
operating modes
map metadata and freshness
evidence classes
root/area map contract
source-rank rules
project-map skeleton asset
minimal skill-validator proof
generated-adapter proof
behavior-preservation evidence
```

Out of scope:

```text
automatic dependency graph generation
runtime tracing
language-specific scanners
historical project-map migration
repository-wide mandatory project-map generation
new CLI scaffolding
remote indexing or telemetry
full project-map fixture suite before concrete drift evidence exists
```

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| `AC-PMAP-001` | `project-map` remains an observation and orientation skill. |
| `AC-PMAP-002` | The skill explicitly prohibits presenting future design as current state. |
| `AC-PMAP-003` | The skill supports create, refresh, area, and audit modes. |
| `AC-PMAP-004` | Produced maps include scope, baseline, coverage, last-reviewed date, and known gaps. |
| `AC-PMAP-005` | Important current-state claims cite repository paths. |
| `AC-PMAP-006` | Inferences are explicitly distinguishable from observations. |
| `AC-PMAP-007` | Unknowns are recorded rather than guessed. |
| `AC-PMAP-008` | Root maps register all area maps. |
| `AC-PMAP-009` | Area maps are based on durable repository boundaries, not one feature request. |
| `AC-PMAP-010` | Plans, proposals, and unimplemented specs are not treated as current implementation evidence. |
| `AC-PMAP-011` | Configured and executed commands are distinguished. |
| `AC-PMAP-012` | Stale or partial maps cannot support unqualified downstream reliance. |
| `AC-PMAP-013` | The full output skeleton is packaged and mapped with `COPY`. |
| `AC-PMAP-014` | The skeleton contains no hidden evidence, routing, or future-design policy. |
| `AC-PMAP-015` | Risks and open questions do not become execution commitments automatically. |
| `AC-PMAP-016` | Existing project maps are not automatically migrated. |
| `AC-PMAP-017` | Generated adapters include the revised skill and skeleton. |
| `AC-PMAP-018` | Representative outputs preserve the existing eleven-section coverage. |
| `AC-PMAP-019` | Refreshes that correct a previously wrong map section include a correction note rather than presenting the issue as ordinary staleness. |

## Open questions

### 1. Should `orientation` become a normalized workflow-role stage?

Resolved direction:

```text
Yes, if the current published-skill contract lacks an appropriate living-reference
or discovery value. Otherwise use the existing contract value with equivalent
meaning rather than adding an unsupported enum.
```

### 2. Should map freshness use a commit SHA, date, or both?

Resolved direction:

```text
Use both when Git is available:
- baseline commit/ref;
- dirty working-tree indicator as <sha>+dirty;
- uncommitted inspected paths when the tree is dirty;
- last-reviewed date.

Use date plus a clearly stated evidence baseline when Git is unavailable.
```

### 3. Should root-map registration of area maps be machine-readable?

Resolved direction:

```text
Use a stable Markdown table in the first slice. Add YAML only if a second
consumer, such as a CI gate or dashboard, appears.
```

### 4. Should all eleven existing sections remain mandatory?

Resolved direction:

```text
Keep the sections structurally present, but allow "Not observed in the mapped
scope" with a rationale. This preserves coverage without forcing invented
content.
```

### 5. Should project-map execute repository commands?

Resolved direction:

```text
Only when execution is needed to answer the orientation question and is safe.
Otherwise record commands as configured, not verified. Never claim execution
success without actual evidence. Read-only inspection commands are allowed;
mutating, network, test-suite, and build-suite commands require user go-ahead.
Record every executed command with its exit code.
```

### 6. When should a repository be split into area maps?

Resolved direction:

```text
Split when there is a durable service, deployment, package, ownership, domain,
or data boundary--not merely because the current feature touches that directory.
Also require roughly more than a screen of root-map content, unless the area has
its own deploy or release lifecycle.
```

### 7. Should produced project maps receive a dedicated validator?

Resolved direction:

```text
Not initially. Validate the skill contract, skeleton, and representative outputs
first. Add a project-map artifact validator only if concrete structural drift
appears in two or more produced maps.
```

### 8. What if a refresh discovers the previous map was wrong, not stale?

Resolved direction:

```text
Do not add a fourth map status in the first slice. Keep status values focused on
the refreshed artifact and require a correction note in the refresh result when
prior map content was incorrect at its recorded baseline.
```

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-23 | Preserve `project-map` as current-state orientation. | Future design belongs to architecture and proposals. | Expand project-map into architecture planning. |
| 2026-06-23 | Add evidence and freshness contracts. | Downstream readers need to know what the map proves and when it applies. | Treat every produced map as implicitly current. |
| 2026-06-23 | Keep one root map as the entry point. | Area maps must not fragment repository orientation. | Allow standalone, unregistered area maps. |
| 2026-06-23 | Add one full skeleton asset. | The output structure is substantial enough to earn a file. | Add many small row assets. |
| 2026-06-23 | Defer automatic graph generation. | Semantic orientation is not equivalent to import-graph extraction. | Build scanners in the same slice. |
| 2026-06-23 | Keep validation incremental. | The first slice should prove the contract and skeleton before building a broad fixture suite. | Treat all PMAP checks as same-slice implementation work. |
| 2026-06-23 | Record correction notes for wrong prior map sections. | Wrong-at-baseline and stale-after-change are different downstream reliance risks. | Add a fourth first-slice freshness status. |

## Next artifacts

```text
proposal-review
spec or skill-contract amendment, if required
spec-review
plan
plan-review
test-spec
implementation
code-review
explain-change
verify
pr
```

If existing published-skill rules already cover metadata, workflow role, assets, and generated parity, a focused test-spec amendment may be sufficient. The evidence, freshness, and root/area map contracts may still justify a dedicated project-map feature spec.

## Follow-on artifacts

- [Project Map Skill Contract](../../specs/project-map.md)

Potential follow-ons after proposal settlement:

- Proposal for automatic dependency and entry-point extraction.
- Proposal for a project-map artifact validator if concrete structural drift appears in two or more produced maps.
- Proposal for runtime-flow evidence collection.
- Proposal for ownership-map integration using CODEOWNERS or repository metadata.
- Proposal for project-map refresh selection based on changed surfaces.

## Readiness

Accepted after clean proposal-review. Follow-on spec created at `specs/project-map.md`.

## Core invariant

```text
A project map is trustworthy only when it says what it covers, what repository
state it describes, which claims are observed, which are inferred, and what
remains unknown.

It describes current repository reality. It does not design the future, replace
source inspection, or become a backlog.
```
