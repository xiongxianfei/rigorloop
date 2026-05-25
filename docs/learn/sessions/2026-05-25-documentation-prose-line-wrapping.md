# Learn Session: Documentation Prose Line Wrapping

## Frame

- Trigger: maintainer explicitly invoked `learn` after repeated line-wrapping fixes in README and `VISION.md`.
- Trigger type: contributor observation / explicit maintainer request.
- Scope:
  - reason for awkward line-wrapping issues in adopter-facing prose;
  - best practices for future documentation prose formatting.
- Evidence in scope:
  - commits `8ec095b docs: reflow readme landing copy`, `761a5da docs: reflow vision prose`, and `ec438bf docs: use semantic line breaks in vision`;
  - `README.md` first-screen line-wrap fix;
  - `VISION.md` semantic line-break fix;
  - `docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/verify-report.md` post-PR validation notes;
  - existing learn README and topic index.
- Explicit exclusions:
  - no formatter, markdownlint rule, workflow policy, or validator change in this learn session;
  - no change to README marker-generation semantics.
- Prior learnings reviewed:
  - `docs/learn/README.md`
  - `docs/learn/topics/skill-asset-design.md`
  - search across `docs/learn` for `line`, `wrap`, `semantic`, `Markdown`, and `prose`.
- Session record path: `docs/learn/sessions/2026-05-25-documentation-prose-line-wrapping.md`

## Observe

### O1: Hard wrapping optimized for column width, not reviewer comprehension

Evidence:

- README originally split the first-screen traceability sentence as:
  `proposal` / `to spec`, which separated a meaningful phrase boundary.
- `VISION.md` split sentence fragments such as `that output` / `often disappears`
  and `AI` / `agents` before the final semantic-line-break pass.
- The final VISION fix used one sentence or one natural clause per source line.

The issue was not rendered Markdown. It was source readability. In source review,
line breaks carry visual meaning even when Markdown renders them as spaces.

### O2: Lists embedded in prose are especially fragile under arbitrary wrapping

Evidence:

- Both README and `VISION.md` contain lifecycle chains such as proposal, spec,
  plan, test spec, implementation, review, verification, and PR.
- Arbitrary wrapping made the chains harder to scan and easier to misread,
  especially when one item or transition landed alone on the next line.

Lifecycle chains and value propositions are review-critical copy. They should
prefer sentence boundaries, clause boundaries, or list/table/diagram structures
over mechanical hard wrapping.

### O3: Post-PR prose fixes create avoidable validation churn

Evidence:

- The PR needed multiple follow-up commits for README and `VISION.md` line-wrap
  cleanup.
- Each cleanup also required validation notes in `verify-report.md` and
  `change.yaml`.

This is small but avoidable churn. For adopter-facing prose, source-readability
review should happen before PR handoff.

## Classify

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | durable-lesson | durable-lesson | topic guidance | explicit maintainer `learn` request plus repeated fixes | The pattern recurred across README and `VISION.md`; the semantic-line-break fix is reusable guidance. |
| O2 | durable-lesson | durable-lesson | topic guidance | explicit maintainer `learn` request plus repeated fixes | Lifecycle chains are common in this repository and need source-readable formatting. |
| O3 | observation | observation | session record only | evidence from multiple post-PR cleanup commits | The validation churn is useful context, but not enough by itself to create a new process requirement. |

## Route

- Durable topic guidance added: `docs/learn/topics/documentation-prose.md`.
- No authoritative workflow, spec, validator, or skill update is made here.
- No follow-up proposal is required unless this issue recurs enough to justify
  a formatter or lint rule.

## Durable Lesson

For human-authored documentation prose, optimize source line breaks for review,
not just rendered Markdown.

Use semantic line breaks by default:

- one sentence per line when practical;
- one natural clause per line for long sentences;
- keep paired phrases together, such as `AI agents`, `proposal to spec`, and
  `reviewable in Git`;
- avoid splitting lifecycle chains at confusing points;
- convert dense chains into bullets, tables, or diagrams when source lines get
  too long.

Hard wrapping at an arbitrary column is still acceptable for low-risk prose, but
it should not make adopter-facing claims, lifecycle order, or source-of-truth
statements harder to review.

## Follow-Ups

- None required now.
- Candidate future proposal if the pattern recurs: adopt a lightweight prose
  style note or markdownlint/prettier exception for `VISION.md` and README
  landing prose.

## Validation

- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/learn/sessions/2026-05-25-documentation-prose-line-wrapping.md --path docs/learn/topics/documentation-prose.md`: passed; no lifecycle-managed artifact files were selected.
- `git diff --check --`: passed.
