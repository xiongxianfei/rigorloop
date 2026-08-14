---
name: project-map
version: "1.0.0"
schema-version: skill-readability-v1
description: Build, refresh, or audit a current-state repository orientation map. Use when architecture, module boundaries, runtime flow, data flow, test layout, CI, ownership, or change placement is unclear. This skill records observed repository structure and bounded inferences; it does not invent future architecture or act as a backlog.
argument-hint: [repository, area, orientation question, or refresh scope]
---

# Project map

Build, refresh, or audit an evidence-bound map of the repository as it exists today. A trustworthy map states its scope and baseline, distinguishes observed facts from inference, exposes unknowns, and never presents intended behavior as current fact.

## Workflow role

- role_name: project-map
- stage: support
- upstream: current repository state, project-local guidance, and the user's orientation question
- downstream: explore, proposal, architecture, workflow, or none
- summary: Create, refresh, or audit a current-state repository map with cited evidence, bounded inference, known gaps, and downstream orientation.
- must_not_claim: future architecture approval, implementation readiness, review approval, validation success, branch readiness, PR readiness, or final lifecycle closeout

`support` is the approved workflow-role stage for this living-reference skill.

## Quick operating guide

Resolve one target, operation, and scope; run the coordination preflight; inspect enough current evidence; then create, refresh, or audit. Use the skeleton for writes and report freshness, limits, blockers, and one next stage.

For blocked cases, use `Stop conditions`. For claim boundaries, use `must_not_claim` in `Workflow role`.

## Resource map

- READ `references/map-maintenance-and-area-coordination.md` for every refresh, every audit, every area scope, and every repository create with coordination evidence. Late coordination discovery changes the loaded assembly to `PMA1-maintenance-or-coordinated`; load this reference before dependent judgment or writes without changing operation or scope.
- COPY `assets/project-map-skeleton.md` when creating or refreshing a root or area project map. Fill: metadata fields, applicable sections, evidence paths, known gaps, evidence-trail entries, and applicable area registration rows. Do not emit unfilled placeholders.

If a required reference is missing, unreadable, escaped from the package, contradictory, or mixed-version, stop before dependent interpretation or mutation. The skill must not reconstruct conditional procedure from memory. An untriggered reference is not required.

## Customer-project orientation

Public skills operate in customer-project mode by default. Treat `AGENTS.md`, `CONSTITUTION.md`, `docs/`, and `specs/` as optional project-local orientation inputs whose absence is normal. Do not search for RigorLoop originals in customer projects. Use `docs/workflows.md` and other project-local guidance when relevant, portable defaults when safe, and block on ambiguity.

## Invocation classification

Classify operation as exactly `create`, `refresh`, or `audit`, and classify map scope as exactly `repository` or `area:<slug>` before broad repository reading.

Resolve the target through this order: explicit user path; current metadata or active workflow context; the `docs/workflows.md` artifact map; portable default; then stop. Defaults are `docs/project-map.md` and `docs/project-map/<area>.md`. `project-map` owns content; workflow guidance owns placement policy.

Apply these target-state rules without implicit reclassification:

- `create` applies only when the resolved target is absent; an existing target stops with an explicit `refresh` requirement.
- `refresh` applies only when the resolved target exists; an absent target stops and routes to `create`.
- A complete rewrite of an existing map is a refresh strategy, never `create`.
- `audit` is always read-only; an absent target produces a `missing-map` finding.
- A correction requested after audit begins a new refresh operation with current target and evidence resolution.

Legacy `create` maps to `create + repository`; legacy `refresh` and `audit` require one scope; legacy `area` requires one operation and `area:<slug>` or stops. New results use `Operation` and `Map scope`, never legacy `Mode`.

## Coordination preflight

Before treating repository creation as uncoordinated, inspect only these known ownership surfaces:

- project-local workflow guidance for customized paths;
- the canonical or configured root-map path;
- the canonical or configured area-map directory;
- existing root registration rows when a root map exists;
- known area-map files in configured locations;
- request-supplied coordination evidence, including proposed areas, parents, overlaps, or missing maps;
- directly referenced project-map paths in the active change context when applicable.

The preflight must not broadly scan the repository merely to prove absence. No known evidence selects uncoordinated behavior. Existing, proposed, missing, or orphaned areas, registrations, parent/child identities, overlaps, or contradictions set `map_coordination_context` true. Unavailable, conflicting, or ambiguous surfaces require reference-owned resolution or stop.

The procedural assemblies are:

- `PMA0-simple-root-create`: `create + repository + coordination=false`; load this file and copy the skeleton when writing.
- `PMA1-maintenance-or-coordinated`: every refresh, every audit, every area scope, and repository create with coordination; load this file plus the conditional reference and copy the skeleton when writing.

Operation and scope form six semantic combinations; assembly selection is separate.

## Map metadata and freshness

Every map begins with `Map metadata` and records Map status, Scope, Baseline, Last reviewed, Coverage, Exclusions, Parent map, and Known gaps. Copy labels and order from the skeleton.

| Status | Meaning |
| --- | --- |
| `current` | Relevant cited surfaces were inspected and no known material gap remains. |
| `partial` | Scope is intentionally bounded or important evidence was unavailable. |
| `stale` | A cited or relied-on surface is known to have materially changed. |

A write does not justify `current`. With Git, record the commit SHA or ref and review date; for inspected uncommitted changes use `<sha>+dirty` and list their paths. Without Git, record the date and inspected archive, workspace, or supplied-path baseline.

## Evidence and confidence

Use these evidence classes:

- observed: supported by inspected repository evidence;
- inferred: a reasonable conclusion not directly declared by inspected source-of-truth evidence;
- unknown: a conclusion the inspected evidence cannot safely support.

Observed material claims cite inspected paths. Label inference and place unknowns under `Open questions`; names alone are insufficient when content could change the conclusion.

Material claim example: "`src/server.ts` registers routes from `src/routes/index.ts`" guides entry-point selection and needs path evidence. Incidental statement example: "This map covers the repository root" needs none.

Call a pattern an observed repository-wide rule only when explicit policy or multiple examples establish it; one example is an observed instance.

Prefer current-state evidence in this order: executable source and runtime configuration; manifests and schemas; tests and CI; current documentation; generated output with a known source; names alone.

Intent artifacts do not prove implementation. When they conflict, describe implementation as current, label intent as planned or expected, and record the discrepancy.

## Commands and runtime evidence

Distinguish a configured command from an executed command run this session. Never claim execution or success without it; record each executed command and exit code.

Read-only inspection may be used for orientation. Mutation, network, test, or build execution requires user go-ahead. State whether flow was statically traced, test-demonstrated, execution-observed, or inferred; static inspection is not runtime observation.

## Root and area maps

The root remains the entry point and summarizes major boundaries, entry points, shared tests and CI, external boundaries, and registered areas. Every area names and links its parent. Create areas only for durable boundaries, roughly screen-length root sections, or distinct deploy, release, ownership, package, domain, or data lifecycles. Detailed coordination belongs to the reference.

## Required output structure

Copy the skeleton as the sole owner of metadata labels, section order, root registration headers, evidence-trail headers, placeholders, and insertion locations. The `Area maps` section applies only to a root with registered areas and is omitted from area maps and uncoordinated roots.

A section without observed content says `Not observed in the mapped scope.` with a rationale. Emit no unfilled placeholders.

## Diagrams

Use Mermaid only to clarify flows or boundaries. Tie nodes to observed components or marked external actors, cite material nodes and edges, label inference, and never present planned components as deployed.

## Downstream reliance and handoff

Downstream skills may use a current map for orientation. They must inspect source directly when it is stale or partial, scope is unreviewed, evidence conflicts, exact architecture or security behavior matters, paths disappeared, or a relied-on claim is inferred or unknown.

Recommend `explore` for uncertainty, `proposal` for direction, `architecture` for future design, `workflow` for routing, or `none`. Isolated invocation never starts it automatically.

## Follow-up boundary

`project-map` may record risks and open questions for orientation.

It does not own deferred execution or act as a backlog.

When a risk needs action, route it through the appropriate owner surface: proposal, plan, learn, review resolution, release evidence, or `docs/follow-ups.md` or another project-local follow-up artifact according to workflow guidance.

## Stop conditions

Stop when target or placement is ambiguous, operation conflicts with target state, evidence cannot support freshness, resources or coordination fail, cited evidence disappeared, a command lacks authority, or work would become future design, backlog, planning, review, verification, branch/PR readiness, or lifecycle closeout.

## Evidence collection efficiency

Use bounded evidence plus summary and stable-ID first reasoning before broad reads. Prefer check IDs, requirement IDs, file paths, counts, line citations, targeted excerpts, and validation summaries.

Do not read every repository file.

## When full-file read is required

Read the full file when the whole file is the review target or map target, bounded searches disagree, relevant sections cannot be isolated safely, surrounding context changes the conclusion, evidence is contradictory or incomplete, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Output skeleton

```md
- Skill: project-map
- Status: <created | updated | audited | blocked>
- Operation: <create | refresh | audit>
- Map scope: <repository | area:<slug>>
- Artifacts changed: <paths or none>
- Freshness result: <current | partial | stale>
- Correction note: <note or none>
- Open blockers: <blockers or none>
- Next stage: <explore | proposal | architecture | workflow | none>
```

## Expected output

Start with the result block, then give the path, orientation or findings, evidence limits, freshness, risks, questions, and next stage. The result describes the invocation; `Map metadata` describes the artifact.
