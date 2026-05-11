# Learn Session: Dynamic Token Cost Root Cause

## Frame

- Trigger: maintainer asked what root cause explains the `v0.1.1` Token-Friendliness warning results and what best practices should solve them.
- Trigger type: explicit maintainer request / contributor observation after dynamic release benchmark execution.
- Scope: first release Token-Friendliness report, sanitized analyzer summaries, prior token-cost learn sessions, and the public skill surfaces named by the warnings.
- Session path: `docs/learn/sessions/2026-05-11-dynamic-token-cost-root-cause.md`
- Evidence in scope:
  - `docs/reports/token-cost/releases/v0.1.1.md`
  - `docs/reports/token-cost/releases/v0.1.1.yaml`
  - `docs/reports/token-cost/runs/v0.1.1/*.analysis.yaml`
  - `skills/workflow/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `docs/learn/sessions/2026-05-09-context-budget-after-broad-search.md`
  - `docs/learn/sessions/2026-05-10-skill-token-measurement-scope-narrowing.md`
- Explicit exclusions:
  - No claim is made that the `v0.1.1` warnings are release blockers; the release metadata records them as warning-only.
  - No safety-critical skill guidance is removed or recommended for removal solely to reduce tokens.
  - No exact tokenizer internals are inferred beyond the measured report fields.
- Prior learnings reviewed:
  - `docs/learn/sessions/2026-05-09-context-budget-after-broad-search.md`
  - `docs/learn/sessions/2026-05-10-skill-token-measurement-scope-narrowing.md`
  - `docs/learn/topics/plan-lifecycle-closeout.md`

## Observe

### O1: Static size warnings identify large public skills, but they do not explain the whole runtime cost

`workflow` is the largest public skill at 6,674 estimated tokens and exceeds the high-warning threshold. `code-review` is 4,726 estimated tokens and exceeds the warning threshold. These are real static costs, but static size alone does not explain the dynamic pattern because every benchmark also had runtime skill-file reads and large input-token totals.

Evidence:

- `docs/reports/token-cost/releases/v0.1.1.md` records 54,294 estimated static tokens across 23 skills.
- The same report identifies `workflow` at 6,674 estimated tokens and `code-review` at 4,726 estimated tokens.
- The release metadata records static warnings for `workflow` and `code-review`.

Root cause:

- These skills aggregate broad lifecycle responsibility. `workflow` carries routing, lifecycle ownership, artifact paths, continuation behavior, validation layering, review-resolution semantics, evidence collection, and output shape. `code-review` carries review independence, material finding rules, recording rules, severity, milestone handoff, closeout, evidence collection, and templates.
- The size is structural: one public skill contains multiple safety and workflow contracts so a runtime that loads or reads the whole skill pays for all of that guidance even when a prompt only needs a narrow subset.

### O2: The confirmed full-file reads are the dynamic behavior that static measurement would miss

The corrected analyzer summaries found one confirmed skill-file read in every dynamic benchmark. The report's command-output table shows each benchmark reading the installed public skill file from the temporary fixture.

Evidence:

- `docs/reports/token-cost/releases/v0.1.1.yaml` summary records `full_file_read_count: 7`.
- Each tracked analyzer summary records `full_file_read.result: confirmed`.
- Largest observed single command output was the public `workflow/SKILL.md` read at 4,071 estimated tokens.

Root cause:

- The runtime benchmark triggered the expected skill, then the agent read the installed public `SKILL.md` using a broad leading range such as `sed -n '1,220p'`.
- That behavior is not visible from static file size alone. Static measurement says how large the skill is; dynamic measurement shows whether the agent actually loads or prints it during ordinary use.

### O3: `verify-final-pack` crossed the dynamic input warning because dynamic input compounds multiple context sources

`verify-final-pack` recorded 77,019 input tokens, above the initial 75,000 warning threshold. Its largest command output was the `verify/SKILL.md` read at 3,515 estimated tokens, and its total command-output estimate was 5,893 tokens. That is material, but it is not large enough by itself to explain the whole input-token total.

Evidence:

- `verify-final-pack` input tokens: 77,019.
- `verify-final-pack` cached input tokens: 66,560.
- `verify-final-pack` total estimated command-output tokens: 5,893.
- `verify-final-pack` largest event: public `verify/SKILL.md` command execution at 220 lines and 3,515 estimated tokens.
- The report also records broad search count 2 for this benchmark.

Root cause:

- Dynamic input tokens include the prompt, runtime instructions, loaded skill content, fixture context, prior tool results, and other session context. Command output is one driver, not the only driver.
- The high cached-input count suggests a large reusable context base. The incremental cost is still worth measuring because skill-file reads, broad searches, and fixture reads determine how much extra context each benchmark adds.

### O4: The warning result proves the benchmark's value because it separates four different optimization targets

The warning set points to different levers:

- static skill size: `workflow` and `code-review`;
- runtime loading behavior: confirmed skill-file reads in all seven runs;
- benchmark/session context: `verify-final-pack` input tokens;
- command-output amplification: largest observed single output at 4,071 estimated tokens, below the current 8,000 command-output warning threshold.

Evidence:

- The release gate status is `warning`, not `blocked`.
- The report lists static size, dynamic benchmark, command-output amplification, portability, comparison, and top cost drivers separately.

Root cause:

- Token cost is multi-factor. A single static size metric would over-focus on deleting skill text; a single dynamic total would hide whether the cost came from skill size, command output, broad searches, or the runtime context base.

## Classify

| ID | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | durable-lesson | durable-lesson | Topic entry | Maintainer prompt plus `v0.1.1` report evidence | Large public skills are a real static cost, but their optimization must preserve safety-critical guidance and be guided by runtime evidence. |
| O2 | durable-lesson | durable-lesson | Topic entry | Maintainer prompt plus seven analyzer summaries | Dynamic checks are necessary because they expose runtime skill-file reads that static measurement cannot show. |
| O3 | observation | observation | Candidate future optimization slice | Token-cost report evidence | `verify-final-pack` is a measured warning, but one baseline is not enough to define a hard optimization target. |
| O4 | durable-lesson | durable-lesson | Topic entry | Maintainer prompt plus report structure and warnings | Separate static size, runtime reads, command output, and context-base effects before choosing an optimization. |

## Route

- Added topic entry: `docs/learn/topics/token-cost-measurement.md`
- No authoritative workflow, spec, architecture, or skill behavior change was made in this session.
- The release Token-Friendliness benchmark contract already owns the policy that every public release should produce static and dynamic evidence.

## Answer

The root cause is not one oversized file alone. It is a compound token-cost pattern:

1. Some public skills are structurally large because they bundle broad lifecycle and safety contracts.
2. The runtime benchmark showed agents read installed public skill files during ordinary skill use.
3. Dynamic input tokens include more than command output: prompt, runtime instructions, loaded skills, fixture context, cached context, and tool results all contribute.
4. The analyzer separated command-output amplification from total dynamic input, proving that static size and runtime behavior must both be measured.

The warnings therefore prove the necessity of dynamic checks: static measurement found `workflow` and `code-review` size risk, but only dynamic measurement found confirmed runtime skill-file reads in every benchmark and the `verify-final-pack` input-token warning.

## Best Practices

- Measure before optimizing. Keep static size, dynamic input, command-output amplification, broad searches, full-file reads, repeated reads, and portability as separate evidence categories.
- Optimize the largest repeated cost driver first. For this baseline, candidate follow-ups are `workflow` static size, repeated whole-skill reads, and `verify-final-pack` dynamic input if the pattern recurs.
- Do not delete safety-critical guidance just to reduce tokens. Split, summarize, or move guidance only when an authoritative artifact or existing skill contract can own the detail safely.
- Design skills for progressive loading: concise triggers, concise result shape, short routing guidance up front, and deeper guidance behind targeted sections.
- Avoid whole-skill reads when a specific section is enough. Use headings, IDs, and bounded excerpts before printing a full `SKILL.md`.
- Keep benchmark prompts and fixtures small, stable, and user-like so broad reads are obvious and comparable.
- Treat `cached_input_tokens` and command-output tokens differently. Cached input can show a large runtime base; command-output estimates show what tool behavior added.
- Use warnings as prioritization evidence until enough comparable reports exist. One baseline should guide the next optimization slice, not define a hard blocker.

## Follow-Ups

- Candidate follow-up: create a focused optimization proposal for reducing `workflow` skill static size and runtime whole-skill reads after another comparable report or maintainer prioritization.
- Candidate follow-up: inspect `verify-final-pack` again after the next release report; optimize only if the dynamic input warning repeats or grows.
- No immediate authoritative artifact update is required because the release benchmark spec and report already encode the need for both static and dynamic measurement.
