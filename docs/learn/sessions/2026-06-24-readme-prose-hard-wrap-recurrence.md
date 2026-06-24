# Learn Session: README Prose Hard-Wrap Recurrence

## Status

Recorded: 2026-06-24

Session state: recorded

## Frame

Trigger:

The maintainer explicitly invoked `learn` after the README update for proposal-gated automatic workflow repeatedly split prose across physical source lines, even after a first attempted fix only moved the workflow command into a code block.

Trigger type:

Explicit maintainer request / contributor observation after repeated correction.

Scope:

- Why README prose kept being split into multiple source lines.
- Root cause of the repeated fix miss.
- Best practices for future README and human-facing Markdown prose edits.

Evidence in scope:

- Commit `3c3ad66d` added the README section with mechanically wrapped prose.
- Commit `298a35df` fixed retired route wording but kept mechanically wrapped prose.
- Commit `99980f1e` unwrapped the README prose after maintainer correction.
- Hosted CI failed once on retired route vocabulary and passed after correction.
- Prior learn session `docs/learn/sessions/2026-05-25-documentation-prose-line-wrapping.md`.
- Prior learn session `docs/learn/sessions/2026-06-23-semantic-markdown-line-breaks.md`.
- Topic guidance `docs/learn/topics/documentation-prose.md`.

Explicit exclusions:

- No formatter, markdownlint rule, validator, workflow spec, or skill policy change is made by this session.
- No broad rewrite of README prose outside the newly added proposal-gated automatic workflow section.
- No claim that all Markdown files must use single-line paragraphs.

Prior learnings reviewed:

- `docs/learn/sessions/2026-05-25-documentation-prose-line-wrapping.md`
- `docs/learn/sessions/2026-06-23-semantic-markdown-line-breaks.md`
- `docs/learn/topics/documentation-prose.md`

Session record path:

`docs/learn/sessions/2026-06-24-readme-prose-hard-wrap-recurrence.md`

## Observe

### O1 - The root cause was an unexamined hard-wrap habit

Evidence:

The README section added in `3c3ad66d` split a single paragraph across lines:

```text
For substantive workflow-managed work, the recommended automation boundary is
the proposal gate. Review and improve the proposal manually first; then let the
workflow continue through deterministic authoring and review stages only after
the formal proposal review is clean.
```

The rendered Markdown is acceptable because Markdown treats ordinary newlines inside a paragraph as spaces. The source Markdown was not acceptable to the maintainer because the physical line breaks interrupted the intended prose unit.

Observation:

The root cause was applying a common code/editing convention, hard wrapping prose around a column width, to a human-facing README section where source-line shape matters. The existing learn guidance already says to preserve semantic units and avoid arbitrary mid-sentence wrapping for review-critical prose.

### O2 - The first fix addressed only the command, not the prose convention

Evidence:

The first correction moved `workflow auto-through: plan-review` into a fenced code block. That made the command easier to copy, but left the paragraph and list items hard-wrapped. The maintainer then supplied the paragraph itself as the failing example.

Observation:

The bug was misclassified too narrowly as "the command line is split." The real issue was "a semantic prose unit is split across physical Markdown source lines." Fixing only the obvious command did not address the underlying convention.

### O3 - Current validation does not enforce this source-line convention

Evidence:

`git diff --check -- README.md`, `python scripts/validate-readme.py README.md`, `python scripts/validate-readme.py README.md --vision-markers`, and `python scripts/test-skill-validator.py` passed after the final README correction. Earlier checks also passed with hard-wrapped prose except for the unrelated retired vocabulary failure.

Observation:

This is primarily an authoring/review convention gap, not a syntax or current validator gap. Existing validation catches retired wording and README marker shape, but it does not decide whether a source paragraph should be one physical line or several.

## Root Cause

The repeated split happened because the edit treated Markdown prose like code comments or spec text that should be wrapped near a column limit. That assumption conflicted with the repository's existing documentation-prose guidance: for human-facing README prose, preserve semantic units in source.

The important distinction is:

```text
acceptable semantic source line:
  one complete sentence, list item, table row, command, or other intended unit

problematic hard wrap:
  one prose unit split across multiple physical source lines only because it is visually long
```

The first attempted fix failed because it solved only the visible command wrapping and did not re-check the whole added README section against the semantic-unit rule.

## Best Practices

1. For README and other human-facing Markdown prose, decide whether source shape matters before editing. If the user complains about "one line split into two lines," inspect physical source lines with `nl -ba`, not just rendered Markdown.

2. Preserve semantic units. Keep one complete sentence, list item, table row, or command together unless the Markdown structure itself requires separate lines.

3. Do not apply arbitrary 80-column hard wrapping to public README prose by default. A long line can be correct when it is a complete sentence or other semantic unit.

4. Use structure instead of mid-sentence wrapping. Put commands in fenced code blocks, use bullets for separate steps, and use tables or diagrams for dense lifecycle chains.

5. Before declaring the fix complete, re-read the exact changed section in source form and check every paragraph and list item, not just the line mentioned in the latest correction.

6. Keep current repository vocabulary while editing prose. The correction from `full-feature` to `substantive workflow-managed` was necessary because README is covered by retired-route vocabulary checks.

7. If maintainers want this enforced automatically, route a proposal or validator change. Learn records and topic files explain the practice but do not create authoritative formatting policy by themselves.

## Classify

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | durable-lesson | durable-lesson already captured | existing topic guidance | prior sessions plus current maintainer correction | The durable lesson already exists in `docs/learn/topics/documentation-prose.md`; this session records recurrence rather than duplicating the topic entry. |
| O2 | observation | observation | session record only | maintainer correction and commit sequence | This explains why the immediate fix missed the real problem. |
| O3 | process-follow-up candidate | pending confirmation | possible validator/proposal if maintainers want enforcement | not confirmed | Automation could prevent recurrence, but learn cannot create that policy and no follow-up was explicitly authorized. |

Contributor confirmation status:

The maintainer confirmed the problem and requested root-cause learning. No confirmation was given to update authoritative policy, validators, or topic guidance.

## Route

- Session record created.
- No topic update made because the durable lesson is already captured in `docs/learn/topics/documentation-prose.md`.
- No validator, workflow, skill, spec, or README policy update made from this learn session.

## Follow-ups

- None created.
- Candidate, if explicitly requested later: propose a lightweight README/source-line convention or validator check for selected human-facing Markdown sections.

## Validation

- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/learn/sessions/2026-06-24-readme-prose-hard-wrap-recurrence.md`: passed; no lifecycle-managed artifact files were selected.
- `git diff --check -- docs/learn/sessions/2026-06-24-readme-prose-hard-wrap-recurrence.md`: passed.
- `python scripts/select-validation.py --mode explicit --path docs/learn/sessions/2026-06-24-readme-prose-hard-wrap-recurrence.md`: passed; selected `guide_system.validate`.
- `python scripts/validate-guide-system.py`: passed.
