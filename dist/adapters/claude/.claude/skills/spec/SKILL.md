---
name: spec
description: >
  Write a contract-level feature specification before execution planning or implementation. Use for changes that affect externally observable behavior, APIs, UI, config, data contracts, error behavior, compatibility, security, or safety-sensitive logic.
---

# Feature spec authoring

You are writing the behavioral contract for the change.

The spec defines **what the system must do** and **how the behavior will be observed**. It should avoid unnecessary internal implementation detail.

## Inputs to read

Read, if present:

- `AGENTS.md`
- `CONSTITUTION.md`
- accepted proposal or issue
- exploration and research artifacts
- `docs/project-map.md`
- related specs
- related architecture docs or ADRs
- existing interfaces, schemas, APIs, UI flows, config, or data contracts

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
- Settlement result: updated | blocked | not-needed
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

Do not broad-search authoritative documents just to find paths. Use `docs/workflows.md` as the path index, and consult specs or schemas only when they govern exact shape, placement, or a detected conflict.

## Required sections

1. **Status**: draft, approved, abandoned, superseded, archived.
2. **Related proposal**: link to proposal or issue.
3. **Goal and context**: what behavior is being defined and why.
4. **Glossary**: domain terms that affect interpretation.
5. **Examples first**: concrete before abstract.
6. **Requirements**: stable IDs with normative language.
7. **Inputs and outputs**: user input, API input, config, data, events, responses.
8. **State and invariants**: what must remain true.
9. **Error and boundary behavior**: invalid input, partial failure, timeouts, permissions, empty states.
10. **Compatibility and migration**: old clients, old data, flags, deprecation, rollback.
11. **Observability**: logs, metrics, traces, audit events, user-visible status.
12. **Security and privacy**: auth, authorization, secrets, data exposure, abuse cases.
13. **Accessibility and UX** when UI is involved.
14. **Performance expectations** when user or system behavior depends on them.
15. **Edge cases**: explicit, numbered cases.
16. **Non-goals**: behaviors intentionally not covered.
17. **Acceptance criteria**: observable outcomes that can be verified.
18. **Open questions**: only if they do not invalidate the spec.
19. **Next artifacts**: planned next steps while the spec is active.
20. **Follow-on artifacts**: actual downstream artifacts or terminal disposition. If present before any real follow-ons exist, say `None yet`.
21. **Readiness**: truthful next-stage or settled-state wording.

## Requirement format

Use stable requirement IDs:

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
- Do not use `reviewed` as a durable spec status. Once the review outcome is relied on, normalize the tracked spec to `approved` or the appropriate terminal state.
- Preserve `Next artifacts` as planning history. Use `Follow-on artifacts` for actual downstream artifacts, replacement, or terminal closeout.
- If a spec is superseded, identify the replacement with `superseded_by` or equivalent labeled text.
- If the behavior is too unclear to specify, return to `explore`, `research`, or `proposal`.

## Workflow handoff behavior

- In a workflow-managed flow, successful `spec` completion hands off to `spec-review` when that review is the next mandatory or triggered downstream stage.
- If the spec still has blockers that prevent review-quality contract writing, stop and report the blocker instead of implying `spec-review` can proceed.
- This v1 contract does not imply `spec-review -> architecture` or `spec-review -> test-spec`; review-to-next-authoring transitions remain outside the autoprogression boundary unless a later approved change adds them.

## Evidence collection efficiency

Use bounded evidence before broad reads or raw excerpts.
Use summary and stable-ID first reasoning before broad reads or raw excerpts.
Prefer check IDs, requirement IDs, test IDs, file paths, counts, line citations, matching line numbers, diffs, and targeted excerpts when inspecting large files, generated output, validation logs, or repeated scans.
Output caps are safety rails, not evidence-selection strategy.
Validation summaries must not change selected check coverage, command exit behavior, failure detection, or required validation evidence.
Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

- spec file path;
- examples first;
- requirement IDs with normative language;
- explicit edge cases, non-goals, and acceptance criteria;
- uncovered ambiguities;
- readiness statement for `spec-review` or blocker state.
