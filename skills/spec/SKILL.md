---
name: spec
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Write or amend a contract-level feature spec before architecture, planning, test planning, or implementation. Use when accepted direction or requested behavior must become requirements for observable behavior, APIs, UI, config, data contracts, errors, compatibility, security, privacy, accessibility, performance, or safety-sensitive logic. Use spec-review to review a spec; use proposal, architecture, plan, test-spec, implement, verify, or pr for those stages.
argument-hint: [proposal path, feature name, behavior request, or issue number]
---

# Feature spec authoring

You are writing the behavioral contract for the change.

The spec defines **what the system must do** and **how the behavior will be observed**. It should avoid unnecessary internal implementation detail.

## Workflow role

- role_name: spec
- stage: authoring
- upstream: accepted proposal, approved direction, behavior request, issue, exploration, or research
- downstream: spec-review
- summary: Author or amend the feature spec recording observable behavior, requirements, examples, edge cases, acceptance criteria, and readiness.
- must_not_claim: spec-review approval, architecture readiness, plan readiness, implementation readiness, verification, branch readiness, or PR readiness.

## Project-local evidence

Public skills operate in customer-project mode by default.

Use project-local artifacts when present and relevant: `AGENTS.md`, `CONSTITUTION.md`, accepted proposals, issues, exploration or research, `docs/project-map.md`, `docs/workflows.md`, related local specs, architecture records, ADRs, interfaces, schemas, APIs, UI flows, config, and data contracts.

Do not require RigorLoop repository-internal specs, docs, reports, follow-up files, or governance files in customer projects. Use portable defaults where safe, and block on ambiguity when no safe local guidance or default exists.

## Inputs to read

Read the smallest relevant set from project-local instructions, accepted proposal or issue, exploration or research, project map, related specs, architecture docs or ADRs, and existing interfaces, schemas, APIs, UI flows, config, or data contracts.

A concrete execution plan is not required before writing the spec. In this workflow, the spec normally comes before the execution plan.

## Upstream settlement check

Before relying on a proposal, read its matching `change.yaml` artifact entry and formal review evidence.
Require an `accepted` settlement, no later contradictory review, no open findings, and closed review resolution when required.

Treat the proposal and its lifecycle state as read-only.
Do not normalize status in the proposal or settle its change-local entry.
If settlement is missing or contradictory, record the blocker and route to `proposal-review`.

## Change-record authoring transition

For a governed change, read the complete `change.yaml` before writing.
Require `lifecycle_contract: stage-owned-change-local-v1`; route a missing marker to `workflow` for creation or migration instead of inventing state.
Resolve exactly one spec entry by artifact ID, `kind`, and normalized `path`.
For a new spec, create only that entry with a unique stable ID, `kind: spec`, normalized path, and explicit role. Before creating or substantively revising the spec, set only that entry to `authoring`, remove any prior `review`, and set `authoring_evidence` to the spec-authoring record path. After the spec and authoring record are complete, set the same entry to `review-required`.
Preserve every other entry and `workflow_state`. Stop on an ambiguous entry, illegal transition, or failed available change-metadata validation.

## Output path

Prefer:

```text
specs/slug.md
```

Do not overwrite unrelated specs. If changing an existing behavior, update the existing spec and preserve history through changelog notes when useful.

## Artifact placement

Use the project workflow guide for artifact locations when placement matters.

Lookup order:

1. explicit user path or change ID;
2. active plan, change metadata, reviewed artifact path, or current artifact metadata;
3. known governing spec or schema constraint when directly relevant;
4. `docs/workflows.md` artifact-location table;
5. this skill's portable default path;
6. block on ambiguity.

This discovery order is subordinate to the source-rank rule in `docs/workflows.md` when sources conflict.

Do not broad-search authoritative documents just to find paths. Use `docs/workflows.md` as the path index when project-local, and consult specs or schemas only when they govern exact shape, placement, or a detected conflict.

## Resource map

- READ `references/boundary-first-method-v1.md` when a behavior contract is governed by `boundary-first-v1`.
- READ `references/boundary-first-feature-authoring-v1.md` when authoring or revising the formal feature boundary record.
- COPY `assets/spec-skeleton.md` when creating or fully rewriting a feature spec.
  Fill: spec title, required-section structures, examples, requirements, acceptance criteria, next artifacts, follow-on artifacts, and readiness.
  Do not emit unfilled placeholders.

## Boundary-first method

Run this compact scan before any stage-owned decision that can change observable behavior, and whenever the input cites an active boundary contract or stable boundary, interaction, or proof ID. Do not wait for the user to name the method.

1. Which inputs or actors can change the outcome?
2. Which state or timing conditions can change the outcome?
3. Which public, sibling, helper, or alternate path can change the outcome?
4. Which failure, retry, recovery, compatibility, or external condition can change the outcome?

If the work is non-behavioral, cites no active boundary identity, and the scan finds no outcome-changing condition, continue under the ordinary stage contract. The scan alone does not create a formal record, ID, proof map, artifact, or user-visible scenario inventory.

Start with the exact approved rows cited for the current decision. Expand approved context only when an ID or outcome is missing, stale, unknown, ambiguous, conflicting, escaped, or insufficient to explain observed behavior. A new or changed normative outcome routes to `spec`; a proof-only gap routes to `test-spec`. Downstream stages do not redefine or rename upstream IDs.

Add a scenario only for a distinct outcome or material authority, trust, state, timing, recovery, path, compatibility, external-dependency, incident, or regression hazard. Stop when every applicable boundary and selected interaction has direct proof; do not build a Cartesian inventory.

Capability state controls formal adoption: `pending` never claims active adoption; after activation, new behavior-changing specs adopt automatically, grandfathered non-substantive revisions remain valid, and `spec-review` must block an undecidable substantive-revision classification. Explain concisely when a formal record is created or an upstream gap blocks progress; do not request redundant consent for contract-required adoption. Structural validation cannot author, repair, or approve semantic content.

Author the normative applicability, boundary, interaction, and example-ownership record.

Use the shared reference for the closed record shape while keeping feature behavior and stage policy in the spec. Stop spec authoring and route the gap upstream when the governing requirements cannot own an applicable boundary, an example would be the only source of behavior, or applicability cannot be decided safely.

## Generated Markdown readability

When this skill creates or updates generated or generator-shaped Markdown:

- Write ordinary prose as normal Markdown paragraphs. Do not split a sentence across physical source lines merely for wrapping or clause separation; multiple sentences may remain in one paragraph.
- Preserve stable IDs for requirements, findings, commands, milestones, and evidence; use tables for repeated mappings.
- Keep commands fenced or table-owned when they carry proof.
- Diagrams are optional. Use them only when they reduce cognitive load and map to real artifacts, stages, components, actors, or states.
- Do not require manual-proof contracts from this readability guidance alone; use governing project rules when manual proof is otherwise required.

## Required sections

Include these sections:

| Section | Requirement |
| --- | --- |
| Owning change record | Required stable pointer for governed work. |
| Related proposal | Required section. |
| Goal and context | Required section. |
| Glossary | Required section. |
| Examples first | Required section. |
| Requirements | Required section. |
| Inputs and outputs | Required section. |
| State and invariants | Required section. |
| Error and boundary behavior | Required section. |
| Compatibility and migration | Required section. |
| Observability | Required section. |
| Security and privacy | Required section. |
| Accessibility and UX | Required section. |
| Performance expectations | Required section. |
| Edge cases | Required section. |
| Non-goals | Required section. |
| Acceptance criteria | Required section. |
| Open questions | Required section. |
| Next artifacts | Required section. |
| Follow-on artifacts | Required section. |
| Readiness | Required section. |

Use `None`, `not applicable`, or a short rationale for sections that do not apply. `Follow-on artifacts`, when present before real follow-ons exist, says `None yet`.

## Requirement format

Use stable, testable requirement IDs:

```text
R1. The system MUST ...
R2. The API MUST NOT ...
R3. The UI SHOULD ... because ...
```

Every `MUST` must be testable or explicitly justified as manually verifiable.

## Example format

Prefer concrete examples:

```text
Example E1: valid input creates a record
Given ...
When ...
Then ...
```

## Rules

- Do not bury requirements in prose.
- Do not use vague words such as “fast,” “intuitive,” or “robust” without measurable criteria.
- Do not specify internal class names, functions, or file paths unless they are externally observable contracts.
- Do not skip failure behavior.
- Do not skip compatibility expectations.
- Do not invent requirements that the proposal excludes.
- Do not write review settlement into the spec.
  The matching `spec-review` records settlement in `change.yaml`.
- Preserve `Next artifacts` as planning history. Use `Follow-on artifacts` for actual downstream artifacts, replacement, or terminal closeout.
- If a spec is superseded, identify the replacement with `superseded_by` or equivalent labeled text.
- If the behavior is too unclear to specify, return to `explore`, `research`, or `proposal`.

## Workflow handoff behavior

In a workflow-managed flow, successful `spec` completion hands off to `spec-review` when that review is next. If blockers prevent review-quality contract writing, stop and report them. This v1 contract does not imply `spec-review -> architecture` or `spec-review -> test-spec`; review-to-next-authoring transitions remain out of scope unless later approved.

Only an explicitly authorized workflow-managed `bounded-review-fix` run can continue after the matching `spec-review`, and that continuation depends on a clean recorded review, recorded architecture assessment, a current authoring capability, and no stop condition.

## Evidence collection efficiency

Use bounded evidence before broad reads or raw excerpts.
Use summary and stable-ID first reasoning before broad reads or raw excerpts.
Prefer check IDs, requirement IDs, test IDs, file paths, counts, line citations, matching line numbers, diffs, and targeted excerpts when inspecting large files, generated output, validation logs, or repeated scans.
Output caps are safety rails, not evidence-selection strategy.
Validation summaries must not change selected check coverage, command exit behavior, failure detection, or required validation evidence.
Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Output skeleton

```md
COPY `assets/spec-skeleton.md` for <spec path>.
Fill every section named in Required sections.
Do not emit unfilled placeholders.
```

## Expected output

Use the `## Output skeleton` guidance and `assets/spec-skeleton.md` structure. Include the spec path, examples first, requirement IDs, edge cases, non-goals, acceptance criteria, ambiguities, and readiness for `spec-review` or blocker state.
