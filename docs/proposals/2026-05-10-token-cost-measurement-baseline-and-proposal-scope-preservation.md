# Token Cost Measurement Baseline and Proposal Skill Scope Preservation

## Status

accepted

## Problem

RigorLoop recently attempted to optimize skill token usage. The original user intent included:

- static skill cost measurement
- runtime tool-output amplification measurement
- Codex JSONL session cost measurement
- identifying the largest cost drivers before optimizing skill text
- improving skill token-friendliness

The accepted proposal, spec, and plan narrowed the work into skill guidance and bounded evidence collection. That slice was useful, but it did not preserve the measurement-baseline work as in scope, out of scope, rejected, open, or deferred.

This created a process problem: proposal authoring narrowed the user's broad intent without making the narrowing explicit enough for proposal-review to catch.

The repository now needs both:

1. a token-cost measurement baseline; and
2. a proposal-skill improvement that prevents silent scope loss.

## Goals

### Measurement Goals

- Add a static skill token measurement report.
- Add Codex JSONL session-cost analysis.
- Add command/tool-output amplification reporting.
- Identify the top measured cost drivers before future skill optimization.
- Keep token budget enforcement as warnings first, not hard CI failures.

### Proposal-Skill Goals

- Require proposal authoring to preserve every initial user goal as in scope, out of scope, deferred, rejected, or open.
- Add an `Initial intent preservation` section or equivalent table for broad requests.
- Update proposal-review to check for silent narrowing.
- Make proposal narrowing reviewable without making proposal-review rewrite the proposal.

## Initial Intent Preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Measure static skill cost. | in scope | Measurement Goals; Workstream A |
| Measure runtime tool-output amplification. | in scope | Measurement Goals; Workstream A |
| Measure Codex session cost from exported JSONL. | in scope | Measurement Goals; Workstream A |
| Identify the largest cost drivers before optimizing skill text. | in scope | Measurement Goals; Workstream A; Rollout |
| Make public skills more token-friendly without removing safety-critical guidance. | in scope | Proposal-Skill Goals; Expected Behavior Changes |
| Prefer bounded evidence collection over broad reads. | in scope | Workstream A; Testing and Verification Strategy |
| Keep the first implementation lightweight and reviewable. | in scope | Rollout; Risks and Mitigations |
| Avoid adding complex telemetry infrastructure before simpler local measurement exists. | out of scope | Non-goals |
| Prevent future proposals from silently dropping parts of broad user requests. | in scope | Proposal-Skill Goals; Workstream B |
| Add hard token-budget CI gates. | deferred follow-up | Non-goals; Decision Log; Rollout |

## Non-goals

- Do not reopen PR #39.
- Do not treat PR #39 as failed solely because it was narrower.
- Do not add hard token-budget CI gates in the first slice.
- Do not add hosted telemetry infrastructure.
- Do not rewrite all skills in this proposal.
- Do not make proposal-review responsible for editing proposals directly.
- Do not weaken proposal's right to narrow scope; require only that narrowing is explicit.

## Vision fit

fits the current vision

This proposal supports RigorLoop's commitment to trustworthy, reviewable AI-assisted delivery by making proposal scope decisions explicit and token optimization evidence-based.

## Context

A recent learn session found that the skill-token optimization work narrowed from measurement plus optimization into skill guidance changes. The missing measurement track was not preserved in the accepted proposal's requirements or follow-up artifacts. See `docs/learn/sessions/2026-05-10-skill-token-measurement-scope-narrowing.md`.

The accepted token-cost optimization proposal identifies broad reads and large command output as delivery cost drivers, but it focuses on evidence collection guidance rather than establishing a complete measurement baseline. See `docs/proposals/2026-05-09-skill-token-cost-optimization.md`.

The implemented work from PR #39 remains valid as a bounded evidence guidance slice. This proposal adds the missing measurement track and proposal-scope preservation guardrail instead of retroactively expanding PR #39.

## Options considered

### Option 1: Only create a measurement-baseline proposal

Advantages:

- Recovers the missing measurement work.
- Keeps scope focused on scripts and reports.

Disadvantages:

- Does not prevent the same scope-loss problem in future proposals.
- Treats the symptom, not the authoring cause.

### Option 2: Only optimize the proposal skill

Advantages:

- Prevents future silent narrowing.
- Smaller change.

Disadvantages:

- Does not recover the missing measurement baseline.
- Still leaves token-cost optimization without evidence.

### Option 3: Combine measurement baseline and proposal-skill scope preservation

Advantages:

- Fixes the missing measurement work.
- Fixes the process that caused the measurement work to disappear.
- Keeps the scope coherent because both issues came from the same incident.
- Gives proposal-review an observable scope-preservation surface.

Disadvantages:

- Larger than either single-purpose proposal.
- Requires careful separation into two workstreams.

## Recommended direction

Choose Option 3.

Create one proposal with two workstreams:

1. Token Cost Measurement Baseline
2. Proposal Skill Scope Preservation

The proposal should not reopen PR #39. PR #39 remains a valid bounded-evidence guidance slice.

This proposal adds the missing measurement baseline and improves the proposal and proposal-review skills to prevent future silent narrowing.

## Workstream A: Token Cost Measurement Baseline

Add lightweight local scripts:

- `scripts/measure-skill-tokens.py`
- `scripts/analyze-codex-jsonl.py`
- optional later: `scripts/measure-command-output.py`, only if live command wrapping becomes useful

The first slice should report:

- static skill size
- estimated token count
- largest skill sections
- internal-path leakage in public skills
- session token usage from a Codex JSONL export when present
- tool calls
- command output lines, bytes, and estimated tokens
- largest command outputs
- broad searches and full-file reads
- high `max_output_tokens` values
- repeated file reads

The first slice should warn, not fail, on token budgets.

Command-output amplification should start inside `scripts/analyze-codex-jsonl.py` because the immediate evidence source is an exported Codex session. Add a separate `scripts/measure-command-output.py` later only if the project needs live command wrapping for local shell command budgeting, validator output measurement, pre-commit checks, or command wrappers around tools such as `rg`, `sed`, or `git diff`.

The first baseline report should be stored under:

```text
docs/reports/token-cost/YYYY-MM-DD-baseline.md
```

When the baseline report is produced by a change, the change-local artifacts should link to the durable report instead of duplicating it.

Recommended report shape:

```md
# Token Cost Baseline: YYYY-MM-DD

## Summary

- Benchmark source:
- Model/tool:
- Prompt:
- Repository state:
- Total input tokens:
- Cached input tokens:
- Output tokens:
- Reasoning output tokens:
- Largest cost driver:
- Recommended next optimization:

## Static skill cost

| Skill | Estimated tokens | Status |
|---|---:|---|

## Codex session cost

| Metric | Value |
|---|---:|
| Input tokens | |
| Cached input tokens | |
| Output tokens | |
| Reasoning output tokens | |

## Tool-output amplification

| Command / event | Lines | Estimated tokens | Notes |
|---|---:|---:|---|

## Top cost drivers

| Rank | Cost driver | Evidence | Suggested action |
|---:|---|---|---|

## Comparison to previous report

| Metric | Previous | Current | Change |
|---|---:|---:|---:|

## Conclusions

- <finding>
- <finding>

## Next actions

- <action>
```

## Workstream B: Proposal Skill Scope Preservation

Update `skills/proposal/SKILL.md` so broad user requests are preserved.

For broad or multi-part user requests, the proposal should include:

```md
## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| <goal> | in scope / out of scope / deferred follow-up / rejected option / open question | <section> |
```

Every initial user goal should be visible in the proposal.

Allowed treatments:

- `in scope`
- `out of scope`
- `deferred follow-up`
- `rejected option`
- `open question`

If a goal is deferred, it should appear in `Next artifacts`, `Follow-on artifacts`, or a named follow-up.

If a goal is rejected, it should appear in `Options considered` or `Decision log`.

If a goal is out of scope, it should appear in `Non-goals`.

## Proposal-review impact

Update `proposal-review` to check scope preservation.

Proposal-review should return `changes-requested` if:

- a user goal from the initial request disappears;
- a deferred goal has no follow-up;
- a rejected goal has no rationale;
- the proposal narrows scope but does not say why.

Proposal-review does not rewrite the proposal. It requests revision.

## Expected behavior changes

- Broad user requests are not silently narrowed.
- Missing goals become visible during proposal-review.
- Token-cost optimization becomes evidence-based.
- Future optimization proposals can cite measured cost drivers.
- PR #39 remains a completed guidance slice rather than being retroactively expanded.

## Architecture impact

No runtime architecture change.

Affected surfaces may include:

- `skills/proposal/SKILL.md`
- `skills/proposal-review/SKILL.md`
- `scripts/measure-skill-tokens.py`
- `scripts/analyze-codex-jsonl.py`
- generated public skill/adapters, if canonical skills change
- `docs/workflows.md`, if it summarizes proposal-scope preservation
- `AGENTS.md`, if it summarizes proposal/review expectations

## Testing and verification strategy

Required checks:

```bash
python scripts/measure-skill-tokens.py
python scripts/analyze-codex-jsonl.py codex-bench.jsonl
python scripts/validate-skills.py
python scripts/test-skill-validator.py
python scripts/build-adapters.py --check
python scripts/validate-adapters.py
git diff --check --
```

For ordinary pre-release skill wording changes, adapter validation should use unversioned commands:

```bash
python scripts/build-adapters.py --check
python scripts/validate-adapters.py
```

If adapter release metadata or manifest versioning is touched, or if the repository's adapter scripts require a version, use the active planned adapter version:

```bash
python scripts/build-adapters.py --version <active-version> --check
python scripts/validate-adapters.py --version <active-version>
```

The plan should record the version source when using a pinned version, such as release plan, package metadata, manifest metadata, or active RC metadata.

Add static skill-validator checks that:

- proposal skill contains `Initial intent preservation`
- proposal skill requires every initial goal to be classified
- proposal-review checks for silent narrowing
- proposal-review requests revision when initial goals disappear

## Rollout and rollback

Rollout:

1. Accept proposal.
2. Write focused spec, then implementation plan if the accepted spec requires one.
3. Add measurement scripts.
4. Update proposal and proposal-review skills.
5. Regenerate generated skills and adapters.
6. Run measurement on an available Codex JSONL export such as `codex-bench.jsonl`.
7. Produce the first token-cost baseline report under `docs/reports/token-cost/`.
8. Use the report to decide the next optimization slice.

Rollback:

- Revert skill guidance changes if proposal/proposal-review behavior becomes too heavy.
- Keep measurement scripts warning-only until baseline quality is trusted.
- Remove or defer optional command-output measurement if Codex JSONL analysis already provides enough evidence for the first slice.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Proposal skill becomes too heavy. | Use a small table only for broad or multi-part requests. |
| Proposal-review becomes too intrusive. | It requests revision; it does not rewrite the proposal. |
| Token estimates are approximate. | Treat them as warnings and baseline evidence, not hard gates. |
| Measurement scripts add maintenance. | Keep them dependency-light and defensive. |
| Future proposals over-preserve scope and become too broad. | Proposal may still narrow, but narrowing must be explicit. |

## Open questions

None.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-05-10 | Combine token measurement baseline with proposal-skill scope preservation. | The same incident exposed both missing measurement and silent narrowing. | Measurement-only proposal; proposal-skill-only proposal. |
| 2026-05-10 | Do not reopen PR #39. | It is a valid bounded-evidence guidance slice. | Retroactively expanding or relitigating the merged PR. |
| 2026-05-10 | Add initial intent preservation to proposal authoring. | Prevents future user goals from disappearing silently. | Relying on proposal-review inference alone. |
| 2026-05-10 | Keep token budget enforcement warning-only in the first slice. | Need baselines before hard gates. | Hard token-budget CI gates in the first slice. |
| 2026-05-10 | Start command-output amplification inside `scripts/analyze-codex-jsonl.py`. | The immediate evidence source is already a recorded Codex session, so one analyzer can explain session cost and drivers together. | Adding a separate live command wrapper in the first slice. |
| 2026-05-10 | Store baseline reports under `docs/reports/token-cost/`. | Token-cost baselines need a durable longitudinal location and change-local artifacts can link to them. | Storing the baseline only under `docs/changes/<change-id>/`. |
| 2026-05-10 | Use unversioned adapter validation by default. | Ordinary skill wording changes need sync and structure validation, not release semantics. | Pinning an arbitrary future adapter version. |

## Next artifacts

- proposal-review
- focused spec, then implementation plan if the accepted spec requires one
- measurement scripts
- proposal/proposal-review skill updates
- generated output refresh
- first token-cost baseline report under `docs/reports/token-cost/`

## Follow-on artifacts

- Spec: `specs/token-cost-measurement-baseline-and-proposal-scope-preservation.md`

## Readiness

Accepted.

The current downstream review target is `specs/token-cost-measurement-baseline-and-proposal-scope-preservation.md`.

The proposal has a clear direction: recover the missing measurement baseline and optimize the proposal skill so future broad requests are not silently narrowed.
