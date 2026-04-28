# Token and Runtime Efficient Scanning

## Status

- accepted

## Problem

RigorLoop contributors and agents often inspect large files, generated artifacts, validation output, and review evidence. Some work requires scanning the same file or output stream multiple times to answer related questions. When each pass dumps broad content back into chat or reruns expensive commands, the workflow pays twice: token usage rises and runtime increases.

The problem is not that agents inspect too much evidence. The problem is that evidence collection is not yet explicit enough about bounded extraction, reuse, and output shape. The project needs practices that preserve correctness, traceability, and reviewability while reducing repeated full-file reads and high-volume command output.

## Goals

- Reduce token usage from file inspection, validation logs, generated output, and repeated evidence collection.
- Reduce runtime spent rescanning the same file or regenerating the same broad output.
- Keep enough source evidence for reviewers to trust conclusions.
- Prefer line-addressed, structured, and reproducible evidence over large pasted excerpts.
- Make repeated scans share an inventory, summary, or parsed representation when feasible.
- Define normal-mode output budgets with explicit verbose escape hatches.
- Give contributors and agents clear guidance for when broad reads are justified.
- Keep the first slice lightweight and compatible with repository-owned scripts.

## Non-goals

- Weakening required verification, review gates, or lifecycle traceability.
- Hiding failures by truncating output before the actionable failure is visible.
- Replacing full-file reads when a full contract review genuinely requires them.
- Adding a long-running indexing service, database, or heavyweight dependency in the first slice.
- Treating output budgets as hard correctness gates before the repository has measured real command behavior.
- Changing validation semantics, selected check coverage, or command exit behavior while shaping output.
- Optimizing model-specific prompt style outside repository-maintained workflow guidance.
- Rewriting existing validators or generators solely for performance without a measured bottleneck.

## Context

`CONSTITUTION.md` says RigorLoop optimizes for reviewability, traceability, and trustworthy automation over speed-by-default. The efficiency change must respect that priority: less output is useful only when it keeps the right evidence available.

`docs/workflows.md` already distinguishes targeted proof from broad smoke through repository-owned validation selection. This proposal applies the same idea to evidence collection and repeated file scanning: start with the smallest reliable extraction, then broaden only when the task needs broader context.

The repository also has generated output and compatibility surfaces. Generated artifacts under `.codex/skills/` and `dist/adapters/` should not become authored scan state. Any durable efficiency guidance should live in canonical workflow content, skills, scripts, or specs, and generated outputs should be refreshed through existing generation commands when canonical skill guidance changes.

## Options considered

### Option 1: Keep broad output and repeated full-file scans as the default

Advantages:

- Simple mental model.
- Low chance of missing nearby context.
- No new guidance, scripts, or conventions.

Disadvantages:

- High token usage for large files and generated output.
- Higher runtime when repeated scans rerun expensive commands.
- Important evidence can be buried in noisy logs.
- Reviewers have less confidence that cited conclusions came from the relevant lines.

### Option 2: Rely on chat discipline only

Advantages:

- Very low implementation cost.
- Encourages better agent behavior immediately.
- No new repository scripts or generated output changes.

Disadvantages:

- Inconsistent between contributors and agents.
- Hard to test or enforce.
- Does not help validators, generators, or other scripts that rescan the same files internally.
- Likely to regress when workflows become more complex.

### Option 3: Add a persistent indexing service or cache layer

Advantages:

- Can make repeated lookup very fast.
- Can support richer semantic or structural queries.
- Useful for very large repositories if maintained carefully.

Disadvantages:

- Adds operational complexity before the bottleneck is proven.
- Creates cache invalidation and portability risks.
- Can conflict with the repository preference for small, reviewable, script-owned mechanisms.
- May make local and hosted validation behavior diverge.

### Option 4: Standardize bounded extraction plus lightweight scan reuse

Advantages:

- Reduces tokens by shaping output before it reaches chat.
- Reduces runtime by parsing or scanning a file once per command or workflow step.
- Keeps evidence line-addressed and reviewable.
- Fits existing repository-owned scripts and workflow guidance.
- Can start as guidance and grow into focused helper behavior only where measured.

Disadvantages:

- Requires contributors and agents to choose extraction scopes deliberately.
- Needs clear escalation rules when a narrow read is not enough.
- Adds small implementation complexity if script-level caching is introduced.

## Recommended direction

Choose Option 4.

RigorLoop should standardize a bounded-extraction workflow for large files, repeated scans, generated output, and validation logs:

1. Start with a file inventory, not file contents. Prefer path lists, sizes, headings, symbols, and matching line numbers before reading full content.
2. Extract evidence at the source. Use path filters, line ranges, counts, stable IDs, and structured output so irrelevant content is never sent back to chat.
3. Build a one-pass local map when repeated inspection is likely. For Markdown, this can be a heading and anchor map. For scripts, this can be functions, classes, imports, and selected matches. For generated output, this should start from manifests and check the filesystem second.
4. Read exact ranges after locating the relevant lines. Prefer small `sed -n` ranges, targeted `rg -n` matches, or structured parser output over broad `cat` output.
5. Reuse parsed content inside scripts. When a validator applies multiple checks to the same file, it should read once, parse once, and run multiple rules against the in-memory representation. The first implementation direction should prefer common parsing helpers for the highest-repeat scripts over a persistent cache.
6. Defer persistent caching until measurement shows cross-command reuse is worth the complexity. If persistent cache reuse is later justified, cache entries should be invalidated by content hash, mtime plus size, or an explicit input digest. Cache output should be local or generated, not a new source of truth.
7. Summarize high-volume output by default. Normal output should be summary-first, failure-focused, diff-focused, and expandable with an explicit `--verbose` or equivalent escape hatch. Command output should report check IDs, affected paths, counts, failing records, and concise failure excerpts. Full logs should stay available through verbose output, files, or reruns when needed.
8. Escalate deliberately. If a targeted read does not answer the question, broaden to neighboring sections, then the whole file, and record why broader context was needed when it matters for review.

Default output budgets should guide normal-mode scripts:

- Routine command output should target no more than 40 lines, with 80 lines as a warning threshold.
- A single excerpt should target no more than 12 lines, with 20 lines as a warning threshold.
- Multi-file summaries should show one summary line per file by default.
- Details should appear only for changed, failing, or explicitly requested files.

Normal-mode output should avoid:

- every parsed field;
- every unchanged file;
- large excerpts by default;
- repeated path lists in multiple sections.

Practical agent-facing best practices:

- Use `rg --files` and targeted `rg -n` before opening files.
- Combine search terms when they answer the same question, rather than scanning the same file once per term.
- Capture line numbers first, then read only the surrounding line ranges needed for evidence.
- Prefer structured command output such as JSON, IDs, or path lists when the script supports it.
- Default to summary and stable ID based reasoning before expanding into prose or raw excerpts.
- Cap routine output and inspect failure-focused excerpts first.
- Keep large raw logs out of chat unless the log itself is the artifact under review.
- Cite files and lines in conclusions instead of pasting long excerpts.
- Parallelize independent reads, but avoid rerunning the same expensive scan in parallel.
- Treat full-file reads as required when the file itself is the review target, when the relevant section cannot be isolated safely, when surrounding context changes the conclusion, when bounded searches disagree, or when a behavior-changing edit depends on understanding the whole source-of-truth artifact.

Practical script-facing best practices:

- Pass changed paths into validators once and share that set across rules.
- Avoid subprocess-per-rule scans of the same file when a single parse can feed all rules.
- Emit concise summaries with stable check IDs and failing paths.
- Add `--json`, `--summary`, or `--failures-only` output modes where high-volume logs are a recurring cost.
- Keep normal-mode output within the stated budgets where practical, and expose `--verbose` for complete detail.
- Use deterministic temporary or cache locations for derived scan state, and keep them out of authored lifecycle artifacts unless explicitly documented as evidence.

## Expected behavior changes

- Contributors and agents begin large-file work with inventories, headings, matches, or structured summaries before reading full content.
- Repeated scans of the same file reuse a local map, parsed representation, or captured line numbers when practical.
- Validation and generation commands favor concise summaries and failure-focused excerpts.
- Normal-mode scripts use summary-first, failure-focused, diff-focused output and provide explicit verbose expansion.
- The first accepted slice includes one small script output-shaping improvement in addition to guidance updates.
- Generated-output scans read manifest evidence first and use filesystem checks as confirmation.
- Important skills include guidance for summary and ID based reasoning plus conditions that require a full-file read.
- Review evidence increasingly cites exact file lines, stable IDs, counts, and affected paths.
- Full-file reads and full logs remain available, but they become escalation steps rather than the default first move.
- Follow-on script changes focus on measured repeated-scan hotspots and shared parsing helpers rather than speculative broad caching.

## Architecture impact

This proposal primarily affects workflow guidance, agent skill guidance, and optional repository-owned helper behavior. It does not require a service, database, network component, or new generated adapter architecture.

Likely follow-on surfaces if the proposal is accepted:

- `docs/workflows.md` for contributor-facing scan and output guidance.
- `AGENTS.md` only if the guidance should become a concise repository default rather than workflow detail.
- Canonical skills under `skills/` so important stage guidance explicitly prefers bounded extraction, summary and ID based reasoning, and full-file-read escalation rules.
- Existing scripts for one first-slice output-shaping improvement, then additional measured repeated reads, repeated subprocess scans, or overly broad output.
- Shared parser helpers for the highest-repeat scripts before any persistent cache is introduced.
- Generated `.codex/skills/` and `dist/adapters/` only through normal generation when canonical skills change.

## Testing and verification strategy

Guidance-only changes can be verified through artifact lifecycle validation and focused documentation review.

If follow-on implementation changes scripts, tests should cover:

- bounded summary output includes the actionable failure and omits unrelated bulk content;
- default output budgets are met or warnings make over-budget normal output visible;
- `--verbose` or equivalent output exposes complete detail when needed;
- the selected first script records before-and-after normal output line counts or byte counts;
- concise failure output preserves check ID, affected path, and actionable failure detail;
- verbose output preserves access to complete diagnostic detail;
- repeated checks over one file share one parsed representation where the code exposes that behavior;
- manifest-first generated-output scans detect missing, extra, or drifted files through a filesystem confirmation step;
- cache or digest invalidation refreshes stale scan state when content changes, if persistent caching is introduced later;
- fallback behavior broadens safely when a path or file type is unclassified;
- failure output includes stable check IDs, paths, and enough context for review.

Runtime improvements should be measured with before-and-after command timings only for scripts that were actually changed. Token reduction should be assessed through output line counts, output byte counts, or representative transcript size rather than subjective impressions.

## Rollout and rollback

Rollout should be incremental:

- Start with documented best practices and any skill guidance that affects agent behavior.
- The first spec should define one reviewable first slice: guidance updates, one named script output-shaping improvement, and any shared parsing helper only when it is needed for that selected script family.
- Add shared parsing helpers for the highest-repeat scripts before persistent caching.
- Add broader script-level output shaping or scan reuse only for repeated, measured pain points.
- Keep broad output available through explicit verbose, debug, or rerun paths.
- Regenerate derived adapter or Codex outputs only when canonical skills change.

Rollback is straightforward for guidance-only changes: revert the documentation or skill guidance. For script-level helpers, rollback by disabling the bounded-output mode, removing helper use, removing cache use if a later slice introduces it, or restoring the previous direct scan path. Because caches should not be authoritative, rollback should not require migration.

## Risks and mitigations

- Risk: Narrow extraction misses important nearby context.
  Mitigation: Define escalation from match to surrounding range to section to full file, and require broader reads when conclusions depend on omitted context.

- Risk: Truncated logs hide the real failure.
  Mitigation: Failure summaries should include check IDs, failing paths, counts, and the actionable failure excerpt, with a verbose rerun path for full logs.

- Risk: Output budgets become brittle style policing.
  Mitigation: Treat budgets as normal-mode targets and warning thresholds, not as hard correctness gates, and keep explicit verbose output available.

- Risk: Cache invalidation creates stale evidence.
  Mitigation: Prefer in-process reuse and shared parsers first. Use content hashes, mtime plus size, or explicit input digests only when cross-command cache reuse is justified later.

- Risk: Efficiency guidance weakens reviewability.
  Mitigation: Keep exact file and line citations as the review-facing evidence, and treat large raw output as available backup rather than primary chat content.

- Risk: Optimization work becomes broader than the measured problem.
  Mitigation: Start with guidance, then require measured hotspots before changing validators, generators, or CI scripts.

## Open questions

No blocking direction questions remain.

Follow-on spec work should still identify the exact first script output-shaping improvement, the highest-repeat scripts that should share parsing helpers first, and the specific important skills that should receive full-file-read escalation guidance.

## Decision log

- 2026-04-27: Draft proposal created. Recommended bounded extraction plus lightweight scan reuse over broad repeated scans, chat-only discipline, or a persistent indexing service because it preserves reviewable evidence while reducing token volume and runtime.
- 2026-04-27: Open direction questions resolved. The first accepted slice should include one small script output-shaping improvement, default output budgets with explicit verbose escape hatches, shared parser helpers before persistent cache work, manifest-first generated-output scanning, and important-skill guidance for summary and ID based reasoning plus full-file-read escalation.
- 2026-04-28: Proposal accepted for spec authoring after proposal review approved the direction and requested only clarifying edits.

## Next artifacts

- `proposal-review` for direction quality and scope challenge.
- If accepted, a focused spec for token and runtime efficient scanning behavior.
- A matching test spec if script behavior, skill behavior, or validation output changes.
- Architecture or ADR only if a persistent cache, shared scan helper, or cross-script indexing boundary is introduced.

## Follow-on artifacts

- [Token and Runtime Efficient Scanning spec](../../specs/token-and-runtime-efficient-scanning.md)

## Readiness

Accepted; may be relied on by downstream spec work.
