# Learn Session: Semantic Markdown Line Breaks

## Status

Recorded: 2026-06-23

Session state: recorded

## Frame

Trigger:

The maintainer corrected the prior interpretation of the newline issue: forcing a semantically complete sentence to be split across multiple source lines is not recommended, and the sentence should remain in a normal, natural form.

Trigger type:

Explicit maintainer correction after repeated newline review problems.

Scope:

- `skills/architecture/SKILL.md`
- `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/explain-change.md`
- the reverted commit `c4137f59 Fix markdown reviewability wrapping`
- the corrected follow-up applied in this session

Explicit exclusions:

- no new authoritative Markdown formatting policy is created by this learn session;
- no topic, workflow, skill, or validator rule is updated without confirmation;
- no generated adapter output is hand-edited.

Prior learnings reviewed:

- `docs/learn/sessions/2026-06-23-resource-integrity-review-finding-pattern.md`

Session record path:

`docs/learn/sessions/2026-06-23-semantic-markdown-line-breaks.md`

## Observe

### O1 - The prior fix misread the newline problem

Evidence:

The reverted fix converted complete sentences and table content into visually wrapped source lines and list continuations.
The maintainer explicitly corrected that this was not the desired style.

Observation:

The issue was not that lines were too long.
The issue was that source lines should preserve semantic units: a complete sentence, list item, table row, or command should not be split merely to satisfy visual wrapping.

### O2 - Hard wrapping can make review text less natural

Evidence:

The architecture Resource map sentence was split across multiple source lines in a previous fix attempt, and `explain-change.md` contained prose where individual sentences were hard-wrapped.

Observation:

Hard wrapping inside a sentence creates unnatural source text and can make review comments look like the content itself is broken.
The preferred shape for prose in these artifacts is semantic line breaks, not arbitrary visual line-length wrapping.

### O3 - Existing validation does not distinguish semantic line breaks from hard wraps

Evidence:

`git diff --check --` and selected repository validation passed with hard-wrapped prose.
Those checks validate syntax, contracts, and whitespace hygiene; they do not judge whether line breaks preserve sentence boundaries.

Observation:

The recurring newline problem is a human-authoring convention gap, not a validator failure in the current contract.

## Root Cause

The root cause was applying a generic Markdown hard-wrap habit to human-facing workflow artifacts without confirming the repository's intended source-line convention.

The correct distinction is:

```text
semantic line:
  one complete sentence, list item, table row, or command unit

bad hard wrap:
  one sentence split across multiple source lines only because it is visually long
```

The earlier response compounded the issue by treating long lines as the defect and creating more mid-sentence line breaks.

## Best Practices

1. Preserve semantic units in Markdown source.
   Keep a complete sentence, Resource map instruction, table row, or command unit together unless the structure itself requires separate lines.

2. Do not "fix" newline review comments by hard-wrapping prose.
   First identify whether the problem is missing separation between semantic units or an unwanted split inside one unit.

3. Use line breaks between sentences or list items, not inside a sentence.
   This keeps source text natural while still making diffs reviewable at semantic boundaries.

4. Treat long-line scans as diagnostic only.
   A long line is not automatically wrong when it is a complete semantic unit.

5. If this convention should become enforced, route it to an authoritative artifact or validator proposal.
   Do not encode it as policy from this learn session alone.

## Classify

- O1
  Proposed primary classification: `observation`.
  Final primary classification: `observation`.
  Secondary routes: none.
  Confirmed by: maintainer correction and reverted commit.
  Rationale: this records the immediate misunderstanding.
- O2
  Proposed primary classification: `durable-lesson`.
  Final primary classification: pending confirmation.
  Secondary routes: possible Markdown authoring guidance.
  Confirmed by: not yet confirmed.
  Rationale: the pattern has recurred, but routing needs explicit confirmation.
- O3
  Proposed primary classification: `process-follow-up`.
  Final primary classification: pending confirmation.
  Secondary routes: possible validator or review checklist proposal.
  Confirmed by: not yet confirmed.
  Rationale: automation could help, but learn alone cannot create the rule.

Contributor confirmation status:

The maintainer confirmed the correction and retrospective trigger.
That confirms recording this session, but not topic updates or authoritative policy changes.

## Route

No topic, workflow, skill, or validation-policy updates were made from this session.

Potential future route, if confirmed:

- add Markdown authoring guidance for semantic line breaks in human-facing artifacts.

## Follow-ups

None created by this session.
