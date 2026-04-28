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

## Output path

Prefer:

```text
specs/slug.md
```

Do not overwrite unrelated specs. If changing an existing behavior, update the existing spec and preserve history through changelog notes when useful.

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

- In a workflow-managed flow, successful `spec` completion hands off to `spec-review` when that review is the next required or default downstream stage.
- If the spec still has blockers that prevent review-quality contract writing, stop and report the blocker instead of implying `spec-review` can proceed.
- This v1 contract does not imply `spec-review -> architecture` or `spec-review -> test-spec`; review-to-next-authoring transitions remain outside the autoprogression boundary unless a later approved change adds them.

## Evidence collection efficiency

Use summary and stable-ID first reasoning before broad reads or raw excerpts. Prefer check IDs, requirement IDs, test IDs, file paths, counts, and line citations when inspecting large files, repeated scans, generated output, or validation output. Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

- spec file path;
- examples first;
- requirement IDs with normative language;
- explicit edge cases, non-goals, and acceptance criteria;
- uncovered ambiguities;
- readiness statement for `spec-review` or blocker state.
