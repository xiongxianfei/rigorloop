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

## Upstream status settlement

In workflow-managed downstream execution, before relying on a proposal, check whether its tracked status matches clear formal review evidence.

Do not run upstream status settlement for review-only, no-edit, or manual inspection requests. Those requests remain isolated.

During normal workflow-managed downstream execution, do not ask whether edits are allowed; the downstream invocation permits minimal settlement.

Settle only lifecycle/status/readiness/follow-on/closeout metadata. Do not rewrite substantive artifact content.

The clear review evidence check requires:

- durable formal review evidence for the upstream artifact;
- an approving or clean review outcome;
- no later contradictory review record;
- no open findings in `review-log.md` when present;
- closed `review-resolution.md` for material findings when required;
- an explicit settlement mapping for this skill.

Mapping for this skill:

- proposal-review approved with no unresolved material findings -> proposal `Status: accepted`.

If review evidence is missing, contradictory, unresolved, or the status surface is absent, block instead of guessing.

If the artifact type, lifecycle field, next status, or target status is unknown or unmapped, block instead of inferring a settlement.

Report `## Upstream status settlement` when settlement was updated, blocked, or stale status was detected:

```md
## Upstream status settlement

- Upstream artifact:
- Review evidence:
- Previous status:
- New status:
- Settlement result: <settlement result>
- Settlement blocker:
```

For blocked settlement with a deterministic target, report that intended target in `New status`. For blocked settlement with no deterministic target, report `New status: not-applicable`. `Settlement blocker` is required for blocked settlement and must distinguish a known target blocked by evidence/state from an unknown target blocked by missing mapping or lifecycle vocabulary.

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

- COPY `assets/spec-skeleton.md` when creating or fully rewriting a feature spec.
  Fill: spec title, required-section structures, examples, requirements, acceptance criteria, next artifacts, follow-on artifacts, and readiness.
  Do not emit unfilled placeholders.
- COPY `assets/requirement-row.md` when adding each normative requirement.
  Fill: requirement ID and full requirement statement.
  Use the requirement modal guidance in this skill when writing the statement.
  Do not emit unfilled placeholders.
- COPY `assets/acceptance-criterion-row.md` when adding each acceptance criterion.
  Fill: criterion ID and observable outcome.
  Do not emit unfilled placeholders.
- COPY `assets/decision-log-row.md` when recording a durable spec decision.
  Fill: date, decision, reason, and alternatives rejected.
  Do not emit unfilled placeholders.

## Required sections

Include these sections:

| Section | Requirement |
| --- | --- |
| Status | Required section. |
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

## Closed enums

Spec status:

```text
draft
approved
abandoned
superseded
archived
```

Settlement result:

```text
updated
blocked
not-needed
```

## Rules

- Do not bury requirements in prose.
- Do not use vague words such as “fast,” “intuitive,” or “robust” without measurable criteria.
- Do not specify internal class names, functions, or file paths unless they are externally observable contracts.
- Do not skip failure behavior.
- Do not skip compatibility expectations.
- Do not invent requirements that the proposal excludes.
- Do not use `reviewed` as a durable spec status. Once the review outcome is relied on, normalize the tracked spec to `approved` or the appropriate terminal state.
- Preserve `Next artifacts` as planning history. Use `Follow-on artifacts` for actual downstream artifacts, replacement, or terminal closeout.
- If a spec is superseded, identify the replacement with `superseded_by` or equivalent labeled text.
- If the behavior is too unclear to specify, return to `explore`, `research`, or `proposal`.

## Workflow handoff behavior

In a workflow-managed flow, successful `spec` completion hands off to `spec-review` when that review is next. If blockers prevent review-quality contract writing, stop and report them. This v1 contract does not imply `spec-review -> architecture` or `spec-review -> test-spec`; review-to-next-authoring transitions remain out of scope unless later approved.

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
Use `assets/requirement-row.md`, `assets/acceptance-criterion-row.md`,
and `assets/decision-log-row.md` for repeated rows when applicable.
Do not emit unfilled placeholders.
```

## Expected output

Use the `## Output skeleton` guidance and `assets/spec-skeleton.md` structure. Include the spec path, examples first, requirement IDs, edge cases, non-goals, acceptance criteria, ambiguities, and readiness for `spec-review` or blocker state.
