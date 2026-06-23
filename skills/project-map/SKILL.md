---
name: project-map
version: "1.0.0"
schema-version: skill-readability-v1
description: Build, refresh, or audit a current-state repository orientation map. Use when architecture, module boundaries, runtime flow, data flow, test layout, CI, ownership, or change placement is unclear. This skill records observed repository structure and bounded inferences; it does not invent future architecture or act as a backlog.
argument-hint: [repository, area, orientation question, or refresh scope]
---

# Project map

Build, refresh, or audit an evidence-bound map of the repository as it exists today.

This skill is for current-state orientation. It must not design future architecture, approve future architecture, claim implementation readiness, claim review approval, claim validation success, claim branch readiness, claim PR readiness, or claim final lifecycle closeout.

## Workflow role

- role_name: project-map
- stage: support
- upstream: current repository state, project-local guidance, and the user's orientation question
- downstream: explore, proposal, architecture, workflow, or none
- summary: Create, refresh, or audit a current-state repository map with cited evidence, bounded inference, known gaps, and downstream orientation.
- must_not_claim: future architecture approval, implementation readiness, review approval, validation success, branch readiness, PR readiness, or final lifecycle closeout

## Quick operating guide

Use this skill to: create, refresh, or audit a root or area project map that orients future work.

Read first:

- the user's requested repository, area, refresh, or audit scope;
- any existing root or area project map in scope;
- project-local guidance when present and relevant;
- source, runtime configuration, manifests, schemas, tests, CI, deployment, infrastructure, and generated output needed for material claims.

Produce:

- a project-map artifact or audit result;
- cited evidence for material current-state claims;
- visible labels for inference and unknowns;
- freshness metadata, known gaps, correction notes when needed, and a next-stage recommendation.

Stop when:

- artifact placement is ambiguous after the lookup order;
- required evidence is unavailable for a `current` status;
- overlapping maps contradict each other;
- the requested command would mutate state, hit the network, or run a test/build suite without user go-ahead.

Do not claim:

- future design approval, implementation readiness, review approval, validation success, branch readiness, PR readiness, or final lifecycle closeout.

Next stage:

- `explore`, `proposal`, `architecture`, `workflow`, or `none`.

## Resource map

- COPY `assets/project-map-skeleton.md` when creating a new root or area project map.
  Fill: metadata fields, applicable sections, evidence paths, known gaps, correction notes, evidence-trail entries, and area registration fields.
  Do not emit unfilled placeholders.

## Customer-project orientation

Public skills operate in customer-project mode by default.

`project-map` reads project-local repository artifacts for orientation. Treat `AGENTS.md`, `CONSTITUTION.md`, `docs/`, and `specs/` as optional project-local orientation inputs whose absence is normal. Do not search for RigorLoop originals in customer projects.

Use `docs/workflows.md` and other project-local guidance when present and relevant. Use portable defaults where safe, and block on ambiguity when no safe local guidance or default exists.

## Operating modes

Classify the invocation before broad repository reading.

- `create`: use when no suitable map exists for the requested scope; create a root map or approved area map.
- `refresh`: use when a map exists but relevant repository state changed; update affected sections and metadata.
- `area`: use when the requested scope is a durable subsystem, package group, service, application, data platform, infrastructure subsystem, ownership area, or domain.
- `audit`: use when the user asks whether a map is current, partial, stale, incomplete, contradictory, or safe to rely on; report drift and do not rewrite artifacts unless requested.

State the selected mode in the result.

## Artifact placement

Use project-local workflow guidance when present.

Lookup order:

1. explicit user path;
2. current artifact metadata or active workflow context;
3. `docs/workflows.md` project-local artifact map when present;
4. portable default;
5. block on unresolved ambiguity.

Portable defaults:

```text
docs/project-map.md
docs/project-map/<area>.md
```

`project-map` owns map content. Workflow guidance owns project-local placement policy.

## Map metadata and freshness

Every root or area map begins with `Map metadata` and records:

- Map status
- Scope
- Baseline
- Last reviewed
- Coverage
- Exclusions
- Parent map
- Known gaps

Status meanings:

| Status | Meaning |
| --- | --- |
| `current` | Relevant cited surfaces were inspected and no known material gap remains. |
| `partial` | Scope is intentionally bounded or important evidence was unavailable. |
| `stale` | A cited or relied-on surface is known to have materially changed. |

A map must not claim `current` merely because the skill produced or refreshed a document.

When Git is available, record the baseline commit SHA or ref and the last-reviewed date. If inspected files include uncommitted changes, record `<sha>+dirty` and list the inspected uncommitted paths. When Git is unavailable, record the last-reviewed date plus a clear evidence baseline such as inspected archive, workspace, or supplied path set.

Refresh affected maps when changes modify top-level or package boundaries, runtime entry points, public module interfaces, service-to-service calls, storage models, schemas, migrations, build or package manifests, test layout or commands, CI, release, deployment, infrastructure configuration, generated-source ownership, ownership boundaries, external integrations, or files cited by the map in a way that changes the map conclusion.

Unrelated repository changes do not automatically make every map stale.

If a refresh discovers that a previous map claim was wrong at its recorded baseline, include a correction note in the result. Name the affected section, corrected claim, and evidence path. Do not introduce a fourth map status.

## Evidence and confidence

Use these evidence classes:

- observed: supported by inspected repository evidence;
- inferred: a reasonable conclusion not directly declared by inspected source-of-truth evidence;
- unknown: a conclusion the inspected evidence cannot safely support.

Observed claims cite inspected repository paths. Inferences are visibly labeled as inference. Unknowns go under `Open questions` rather than being guessed.

Material current-state claims cite at least one repository path. Directory names alone are not sufficient evidence for a material claim when file content could change the conclusion.

Material claim example: "`src/server.ts` creates the HTTP server and registers routes from `src/routes/index.ts`" is material because a downstream agent could use it to choose an entry point, trust a runtime boundary, or select source files for change placement.

Material claim example: "`packages/domain/` has no imports from delivery packages in the inspected files `packages/domain/order.ts` and `packages/api/routes.ts`" is material because it supports a boundary or architecture-rule conclusion.

Incidental statement example: "This map covers the repository root" is incidental and does not need a path citation because it does not justify a code, boundary, test, runtime, data-flow, or downstream reliance decision.

Present an observed architecture rule only when an explicit project rule states it or multiple independent examples consistently demonstrate it. A single example is an observed instance, not a repository-wide rule.

For current-state claims, prefer evidence in this order:

1. executable source and runtime configuration;
2. build/package manifests and schemas;
3. tests and CI workflows;
4. explicit current-state project documentation;
5. generated output with a known canonical source;
6. directory and file names alone.

Proposals, specs, architecture plans, ADRs, and execution plans describe intent. They do not prove that intended behavior exists in current implementation. When intent artifacts conflict with implementation, describe implementation as current state, cite the intent artifact only as planned or expected state, and record the discrepancy as a risk or open question.

## Commands and runtime evidence

Distinguish configured commands from executed commands.

- configured command: found in a manifest, workflow, script, or documented configuration;
- executed command: actually run during the mapping session.

Do not state that a configured command works, passes, or was executed unless it was actually run. Record every executed command with its exit code in the map's evidence trail or equivalent evidence section.

Read-only inspection commands such as `git log`, `ls`, test discovery commands, `--dry-run`, and `--help` may be run when useful for orientation. Commands that mutate state, hit the network, or run an actual test or build suite require user go-ahead before execution.

For runtime flow and data flow, state whether the flow was statically traced, demonstrated by tests, observed through execution, or partially inferred. Do not imply runtime observation when only static source inspection occurred.

## Root and area maps

When any area map exists, the root map remains the repository-level entry point.

The root map includes repository-wide overview, major boundaries, major entry points, shared test and CI surfaces, external boundaries, links to area maps, and a scope/freshness summary for each area map.

Every area map is linked from the root map. Use this stable Markdown registration table:

| Area | Map | Scope | Baseline | Freshness | Known gaps |
| --- | --- | --- | --- | --- | --- |

An area map names its parent map. Use area maps only for durable repository boundaries, not merely because one current feature touches a directory. Do not create an area map until the root-map section for that area would exceed roughly one screen of content, unless the area has its own deploy, release, ownership, package, domain, or data lifecycle.

When two maps overlap, each map names the overlap, one map owns the detailed description, and the other links rather than duplicates. Contradictions between overlapping maps block a clean refresh result.

## Required output structure

Root and area maps include these structural sections:

- Map metadata
- Purpose and scope
- System overview
- Repository layout
- Runtime flow
- Data flow
- External boundaries
- Test map
- CI and release map
- Architecture rules observed
- Risk areas
- Open questions

Root maps should include `Area maps` when area maps exist.

A required section with no applicable observed content says `Not observed in the mapped scope.` and includes a short rationale.

## Diagrams

Use Mermaid only when it clarifies runtime flow, data flow, module or service boundaries, deployment boundaries, or external integrations.

Every node corresponds to an observed repository component or an explicitly marked external actor. Cite supporting files for material nodes or edges. Label inferred edges as inferred.

Do not include decorative layers or present planned components as deployed. Keep detailed area diagrams in the owning area map rather than the root map.

## Downstream reliance and handoff

Downstream skills may use a current map to locate likely modules and entry points, find tests and CI, identify known boundaries, decide which source files need direct inspection, and recognize known gaps.

Downstream skills must inspect source directly when the relevant map is stale or partial, the change crosses an unreviewed area, map evidence conflicts with current code, architecture or security decisions depend on exact behavior, cited paths no longer exist, or the relevant claim is inferred or unknown.

Recommend the next stage from:

| Finding | Next stage |
| --- | --- |
| Problem or options are unclear | `explore` |
| A direction decision is needed | `proposal` |
| Current boundaries are clear enough for future design | `architecture` |
| Workflow placement or routing is unclear | `workflow` |
| No downstream action requested | `none` |

Do not automatically start a downstream stage during an isolated invocation.

## Follow-up boundary

`project-map` may record risks and open questions for orientation.

It does not own deferred execution or act as a backlog.

When a risk needs action, route it to `proposal`, `plan`, `learn`, review-resolution, release evidence, or `docs/follow-ups.md` through the workflow guide.

`project-map` may record unclear ownership, fragile coupling, missing tests, undocumented boundaries, stale documentation, or unverified runtime assumptions as orientation evidence.

Risks and open questions do not become execution commitments automatically. Route actionable follow-up work through the appropriate owner surface, such as proposal, plan, learn, review resolution, release evidence, or a project-local follow-up artifact according to project workflow guidance.

## Stop conditions

Stop and report a blocked result when:

- artifact placement remains ambiguous after the lookup order;
- evidence is insufficient for the requested freshness claim;
- overlapping maps contradict each other;
- a cited path no longer exists and the relevant claim cannot be refreshed;
- the user requests mutating, network, build, or test execution without go-ahead;
- the requested work would turn the map into future design, backlog, implementation planning, review approval, verification, branch readiness, PR readiness, or final lifecycle closeout.

## Evidence collection efficiency

Use summary and stable-ID first reasoning before broad reads or raw excerpts.

Use bounded evidence before broad reads. Prefer check IDs, requirement IDs, test IDs, file paths, counts, line citations, summaries, stable IDs, path inventories, matching line numbers, targeted excerpts, file counts, and validation summaries before broad scans or raw excerpts. Read exact ranges after locating relevant lines, then expand only when narrower evidence is insufficient.

Do not read every repository file. Read enough source, configuration, schemas, tests, CI, and current-state documentation to support the mapped scope and the material claims you write.

## When full-file read is required

Read the full file when the whole file is the review target or map target, relevant sections cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree, bounded evidence is contradictory or incomplete, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Output skeleton

```md
- Skill: project-map
- Status: <created | updated | audited | blocked>
- Mode: <create | refresh | area | audit>
- Map scope: <repository | area:slug>
- Artifacts changed: <paths or none>
- Freshness result: <current | partial | stale>
- Correction note: <note or none>
- Open blockers: <blockers or none>
- Next stage: <explore | proposal | architecture | workflow | none>
```

## Expected output

Start with:

```md
## Result

- Skill: project-map
- Status: <created | updated | audited | blocked>
- Mode: <create | refresh | area | audit>
- Map scope: <repository | area:slug>
- Artifacts changed: <paths or none>
- Freshness result: <current | partial | stale>
- Correction note: <note or none>
- Open blockers: <blockers or none>
- Next stage: <explore | proposal | architecture | workflow | none>
```

Then include the created, refreshed, or audited map path; concise repository orientation; evidence classes; cited material claims; freshness metadata; risks and open questions; and the immediate next stage. Do not claim review approval, validation success, branch readiness, PR readiness, final lifecycle closeout, or future architecture approval.
