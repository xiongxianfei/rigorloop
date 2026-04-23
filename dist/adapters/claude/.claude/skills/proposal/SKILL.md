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
5. **Context**: relevant repo, product, architecture, or operational background.
6. **Options considered**: summarize at least three options or link to `explore`.
7. **Recommended direction**: selected approach and rationale.
8. **Expected behavior changes**: high-level observable behavior, not detailed requirements.
9. **Architecture impact**: expected components, boundaries, and data flow touched.
10. **Testing and verification strategy**: likely levels of test coverage.
11. **Rollout and rollback**: migration, flags, compatibility, fallback.
12. **Risks and mitigations**: product, technical, operational, security, performance.
13. **Open questions**: what must be resolved before spec or architecture.
14. **Decision log**: date, decision, reason, alternatives rejected.
15. **Next artifacts**: planned spec, architecture, plan, test-spec, or follow-up work while the proposal is active.
16. **Follow-on artifacts**: actual downstream artifacts or terminal disposition after settlement or closeout. If present before any real follow-ons exist, say `None yet`.
17. **Readiness**: truthful next-stage status.

## Decision quality checklist

Before marking accepted or ready for review, verify:

- the problem is not just a solution in disguise;
- the recommended option is compared against alternatives;
- non-goals protect the scope;
- user value is explicit;
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

## Expected output

- proposal file path;
- clear recommended direction;
- alternatives and rationale;
- non-goals and risks;
- open questions;
- readiness statement for `proposal-review` or blocker state.
