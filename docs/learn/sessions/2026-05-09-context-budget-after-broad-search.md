# Learn Session: Context Budget After Broad Search

## Frame

- Trigger: contributor asked why the context budget dropped to about 84% after one command.
- Trigger type: contributor observation / workflow-process incident.
- Scope: one proposal authoring turn and the follow-up learn turn.
- Session path: `docs/learn/sessions/2026-05-09-context-budget-after-broad-search.md`
- Evidence in scope:
  - The proposal turn used parallel reads including a broad `rg` over `CONSTITUTION.md`, `docs/workflows.md`, several specs, `docs/plan.md`, and the example plan.
  - The broad workflow/state search returned 511 lines and about 26k output tokens.
  - The follow-up learn search for token/context guidance matched across `docs/learn`, `specs`, `docs/workflows.md`, `CONSTITUTION.md`, `AGENTS.md`, and `skills`, returning 2118 lines and about 93k output tokens.
  - `docs/workflows.md` already contains efficient evidence collection guidance: use bounded extraction first, prefer headings/stable IDs/line citations, keep routine command output around 40 lines, warn at 80 lines, and avoid printing every parsed field or repeated path list.
- Explicit exclusions:
  - No model provider internals are inferred.
  - No claim is made about exact tokenizer accounting beyond observed large tool-output volume.
  - No authoritative workflow, skill, or validator change is made in this session.
- Prior learnings reviewed:
  - Existing learn session inventory was checked.
  - No existing token-budget topic file was found.

## Observe

### O1: The context drop was caused by unbounded evidence collection, not the shell command count

The expensive part was not that a command ran. The expensive part was that the command returned a large amount of text into the conversation context. One `rg` can be cheap when it returns a few line citations, or expensive when it matches thousands of lines across broad directories.

Evidence:

- The proposal turn's broad state search returned 511 lines and about 26k output tokens.
- The learn turn's broad search returned 2118 lines and about 93k output tokens.
- Both searches scanned multiple high-churn text surfaces where many generic words such as `state`, `output`, `context`, and `generated` match frequently.

### O2: The repository already has the right general rule, but the execution violated it

The workflow guidance already says evidence reading should start from summaries, stable IDs, headings, targeted sections, check IDs, file paths, counts, and line citations before broad reads. It also sets normal output budgets and says not to print every large excerpt or repeated path list by default.

Evidence:

- `docs/workflows.md` Efficient Evidence Collection section defines bounded extraction and normal output budgets.
- The broad searches did not apply a low enough line limit, precise enough path scope, or staged count-first approach.

### O3: `max_output_tokens` is a last guard, not a search design

Setting `max_output_tokens` limits the tool response shown back to the agent, but it does not make the query selective. A bad query can still consume a large chunk of usable context before the agent has learned the narrow fact needed.

Evidence:

- The broad searches had output caps, but the returned excerpts were still large enough to materially reduce context.

## Classify

| ID | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | None | Contributor question plus tool-output evidence | The immediate root cause is factual and bounded to this turn. |
| O2 | observation | observation | Candidate process-follow-up: reinforce bounded search behavior in agent practice | Existing workflow guidance and observed violation | Existing authoritative guidance already covers the behavior; this session does not need to create new policy. |
| O3 | observation | observation | None | Tool-output evidence | The lesson affects command design practice more than workflow policy. |

## Route

No derivative artifact was routed from this session.

No topic entry was created because the authoritative guidance already exists in `docs/workflows.md`; the issue was a failure to apply it during evidence collection, not an uncovered workflow rule.

## Best Practices

- Start with `rg --files`, headings, or exact known paths before content search.
- Prefer count-first or filename-first scans for broad questions: `rg -l <pattern> ...`, `rg --count-matches <pattern> ...`, or tight globs before reading matches.
- Search one concept at a time. Avoid broad alternation or generic terms such as `state|output|context|generated` across `specs`, `skills`, and `docs` together.
- Keep first-pass output under the workflow budget: around 40 lines for routine output, with 80 lines as the warning threshold.
- Use precise follow-up reads after locating likely sections: `sed -n '<start>,<end>p' <file>`.
- Treat `max_output_tokens` as a safety rail, not as the main way to control evidence volume.
- Do not run a second broad search after the first broad search proves noisy; narrow immediately.

## No-Learn Rationale

No durable topic guidance was captured because the repository already contains the general bounded-evidence rule. The reusable outcome is operational: apply the existing rule more strictly during proposal, review, and learn sessions.

## Follow-Ups

- No follow-up was created.
- A future proposal or skill update may be warranted only if this recurs despite the existing workflow guidance.
