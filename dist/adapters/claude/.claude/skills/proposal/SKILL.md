---
name: proposal
description: >
  Create a decision-oriented change proposal before writing a feature spec or execution plan. Use after exploration has produced options or when the intended direction is clear enough to evaluate scope, value, risks, and non-goals.
---

# Change proposal

You are turning exploration into a concrete, reviewable direction.

A proposal answers “why this change, why now, and why this approach?” It does not define every requirement and it does not prescribe every implementation task.

## Inputs to read

Read, if present:

- `AGENTS.md`
- `CONSTITUTION.md`
- `docs/project-map.md`
- relevant exploration artifact
- relevant research artifact
- related specs
- related architecture docs or ADRs
- related issues, incidents, or user feedback
- root `vision.md` when present

## Output path

Prefer:

```text
docs/proposals/YYYY-MM-DD-slug.md
```

Do not overwrite an older proposal for a new initiative.

## Required sections

1. **Status**: draft, under review, accepted, rejected, abandoned, superseded, archived.
2. **Problem**: the user or system problem being solved.
3. **Goals**: outcomes the change should produce.
4. **Non-goals**: explicitly out-of-scope work.
5. **Vision fit**: relationship to root `vision.md`.
6. **Context**: relevant repo, product, architecture, or operational background.
7. **Options considered**: summarize at least three options or link to `explore`.
8. **Recommended direction**: selected approach and rationale.
9. **Expected behavior changes**: high-level observable behavior, not detailed requirements.
10. **Architecture impact**: expected components, boundaries, and data flow touched.
11. **Testing and verification strategy**: likely levels of test coverage.
12. **Rollout and rollback**: migration, flags, compatibility, fallback.
13. **Risks and mitigations**: product, technical, operational, security, performance.
14. **Open questions**: what must be resolved before spec or architecture.
15. **Decision log**: date, decision, reason, alternatives rejected.
16. **Next artifacts**: planned spec, architecture, plan, test-spec, or follow-up work while the proposal is active.
17. **Follow-on artifacts**: actual downstream artifacts or terminal disposition after settlement or closeout. If present before any real follow-ons exist, say `None yet`.
18. **Readiness**: truthful next-stage status.

## Vision fit

Include `Vision fit` in new or substantively revised proposals after the vision spec is adopted.

The section states exactly one of:

- `fits the current vision`
- `may conflict with the current vision`
- `intentionally proposes a vision revision`
- `no vision exists yet`

When root `vision.md` is absent, proposals must use the exact `Vision fit` value `no vision exists yet`. If root `vision.md` exists, choose one of the current-vision outcomes and do not use `no vision exists yet`.

A proposal must not silently redefine project vision outside the `Vision fit` section and normal proposal rationale.

Legacy proposals are not invalid solely because they lack `Vision fit`; add it only when the proposal is new or substantively revised after adoption.

## Decision quality checklist

Before marking accepted or ready for review, verify:

- the problem is not just a solution in disguise;
- the recommended option is compared against alternatives;
- non-goals protect the scope;
- user value is explicit;
- `Vision fit` is present and consistent with root `vision.md` when required;
- architecture impact is acknowledged;
- testing and verification are plausible;
- risks are specific enough to act on;
- open questions do not block writing a spec.

## Rules

- Do not write implementation milestones here.
- Do not use normative `MUST` requirements here unless quoting a known constraint.
- Do not hide major tradeoffs.
- Do not skip the rejected alternatives.
- Do not claim a proposal is accepted unless the user or project process accepts it.
- Do not treat `under review` as a durable relied-on state once downstream work is using the proposal. Normalize accepted proposals to `accepted`.
- Preserve `Next artifacts` as planning history. Use `Follow-on artifacts` or equivalent closeout text for actual downstream artifacts or final disposition.
- If a proposal is superseded, identify the replacement with `superseded_by` or equivalent labeled text.

## Workflow handoff behavior

- In a workflow-managed flow, successful `proposal` completion hands off to `proposal-review` when that review is the next required or default downstream stage.
- If open questions or direction gaps still block review, stop and report the blocker instead of implying that `proposal-review` can proceed.
- This v1 contract does not imply `proposal-review -> spec`; review-to-next-authoring transitions remain outside the autoprogression boundary unless a later approved change adds them.

## Evidence collection efficiency

Use summary and stable-ID first reasoning before broad reads or raw excerpts. Prefer check IDs, requirement IDs, test IDs, file paths, counts, and line citations when inspecting large files, repeated scans, generated output, or validation output. Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

- proposal file path;
- clear recommended direction;
- alternatives and rationale;
- non-goals and risks;
- open questions;
- readiness statement for `proposal-review` or blocker state.
