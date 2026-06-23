# Learn Session: Markdown Newline Reviewability

## Status

Recorded: 2026-06-23

Session state: recorded

## Frame

Trigger:

The maintainer asked why newline problems kept recurring and reported that a
newline problem was still visible in
`docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/explain-change.md`.

Trigger type:

Explicit maintainer request after a repeated reviewability defect.

Scope:

- `skills/architecture/SKILL.md`
- `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/explain-change.md`
- prior PR feedback about the architecture skill Resource map wrapping
- the branch validation behavior that allowed long logical Markdown lines

Explicit exclusions:

- no new Markdown style policy is made authoritative by this learn session;
- no global formatter, lint rule, or workflow rule is added here;
- no generated adapter output is hand-edited.

Prior learnings reviewed:

- `docs/learn/sessions/2026-06-23-resource-integrity-review-finding-pattern.md`

Session record path:

`docs/learn/sessions/2026-06-23-markdown-newline-reviewability.md`

## Observe

### O1 - The defect was a reviewability problem, not a Markdown parse failure

Evidence:

`git diff --check --` and Markdown-oriented validation can pass while a file
still contains very long logical lines. The visible symptom in review was poor
line wrapping around prose-heavy Markdown content.

Observation:

The defect was not missing semantic content. It was that long source lines and
wide Markdown table rows made review UI rendering hard to read and easy to
misinterpret.

### O2 - The previous fix targeted one visible symptom, not the class

Evidence:

The earlier PR comment focused on the architecture skill Resource map. The same
style problem still existed in dense rationale surfaces such as
`explain-change.md`, especially in wide Markdown tables.

Observation:

The fix was too local. It addressed the reviewed Resource map text but did not
sweep related human-review surfaces for the same long-line shape.

### O3 - Markdown tables are a poor fit for dense rationale content

Evidence:

`explain-change.md` used several tables where each row contained paths,
requirements, rationale, source artifacts, and evidence commands. Those rows
were hundreds of characters long before the fix.

Observation:

Tables work for compact comparisons. They are brittle for prose-heavy rationale
because Markdown table rows cannot be wrapped naturally without hurting source
readability. Wrapped bullet sections are easier to review and maintain.

### O4 - Current validation does not protect this readability boundary

Evidence:

Existing validation checked artifact lifecycle, guide system rules, skill
validation, selected test scopes, and whitespace hygiene. None of those checks
reported the long logical lines as a failure.

Observation:

The validation stack is good at correctness and artifact routing, but it does
not currently enforce reviewable line shape for Markdown. Review caught what
automation did not.

## Root Cause

The root cause is that we treated "newline problem" as a single formatting
mistake instead of a document-shape class:

```text
long logical Markdown line
-> poor PR/review rendering
-> unclear copied text or adjacent UI text
-> repeated review comments
```

The underlying contributors were:

- using dense Markdown tables for prose-heavy explanation;
- fixing only the commented line instead of sweeping related changed Markdown;
- relying on `git diff --check --`, which catches whitespace errors but not
  review readability;
- not having an explicit pre-PR check for long human-facing Markdown lines.

## Best Practices

1. Treat newline complaints as source-shape issues.
   Search for long logical lines in nearby changed Markdown, not only the exact
   reviewed line.

2. Avoid wide tables for prose-heavy rationale.
   Use wrapped bullet sections when cells need paths, decisions, sources,
   evidence, or long explanations.

3. After fixing a formatting review comment, sweep same-class Markdown files.
   At minimum inspect touched skills and change-local rationale artifacts.

4. Remember that `git diff --check --` is not a readability validator.
   It catches trailing whitespace and patch hygiene, not long Markdown lines.

5. If this recurs again, route a confirmed process follow-up to add a lightweight
   Markdown long-line or wide-table reviewability check for human-facing
   artifacts.

## Classify

- O1
  Proposed primary classification: `observation`.
  Final primary classification: `observation`.
  Secondary routes: none.
  Confirmed by: current file inspection.
  Rationale: the defect explains the immediate symptom without changing policy.
- O2
  Proposed primary classification: `process-follow-up`.
  Final primary classification: pending confirmation.
  Secondary routes: possible review checklist or validation guidance.
  Confirmed by: not yet confirmed.
  Rationale: the pattern recurred, but routing needs maintainer confirmation.
- O3
  Proposed primary classification: `durable-lesson`.
  Final primary classification: pending confirmation.
  Secondary routes: possible Markdown authoring guidance.
  Confirmed by: not yet confirmed.
  Rationale: the table-vs-bullet lesson is reusable, but topic updates need
  confirmation.
- O4
  Proposed primary classification: `process-follow-up`.
  Final primary classification: pending confirmation.
  Secondary routes: possible validator or CI selector enhancement.
  Confirmed by: not yet confirmed.
  Rationale: automation could catch this, but learn alone does not authorize new
  policy.

Contributor confirmation status:

The maintainer explicitly confirmed the retrospective trigger. That confirms
recording this session. It does not confirm topic updates, new validation
rules, or workflow policy changes.

## Route

No topic, workflow, skill, or validation-policy updates were made from this
session.

Potential future route, if confirmed:

- add a reviewability check or checklist item for long logical Markdown lines in
  human-facing changed artifacts.

## Follow-ups

None created by this session.
