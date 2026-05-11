# Progressive Loading for High-Cost Public Skills

## Status

accepted

## Problem

The `v0.1.1` Token-Friendliness report proves that dynamic runtime benchmarking is useful: it separates static skill size, runtime skill-file reads, command-output amplification, portability, and result quality.

It also exposes four important token-cost drivers:

- `implement-handoff` produced a large broad-search output of 20,738 estimated tokens.
- `workflow` is the largest public skill at 6,674 estimated tokens.
- `code-review` is above the static warning threshold at 4,726 estimated tokens.
- All ten required v2 transition benchmark runs read the active public skill file during runtime.

These warnings are not release blockers in the v2 transition baseline, but they are strong optimization signals.

The current problem is not simply that some skills are long. The deeper problem is that some skills are not progressively loadable enough. Agents often read the whole active public `SKILL.md` file when a short operating section would be enough. In `implement-handoff`, the agent also appears to search broadly for milestone state instead of reading the active plan's `Current Handoff Summary` first.

Without a targeted optimization, future benchmark reports may continue to spend context on broad reads, whole-skill reads, and repeated state discovery.

## Goals

- Reduce runtime amplification for `implement-handoff`.
- Make high-cost public skills easier to use from short targeted sections.
- Add a compact `Quick operating guide` to high-cost public skills.
- Reduce `workflow` public skill size by moving detailed workflow explanation into `docs/workflows.md`.
- Compress `code-review` where safe while preserving safety-critical review guidance.
- Keep all review, material-finding, validation, and milestone-handoff safety rules intact.
- Use dynamic benchmark evidence to compare before and after behavior.
- Avoid broad rewrites of all skills in this slice.

## Non-goals

- Do not remove safety-critical review, validation, or material-finding rules.
- Do not change workflow order.
- Do not change release token-friendliness gates.
- Do not introduce hard token thresholds.
- Do not optimize every skill.
- Do not remove `code-review` independence, mixed-evidence, or material-finding requirements.
- Do not remove `implement` first-pass completeness or milestone handoff requirements.
- Do not hand-edit generated adapter output without regenerating from canonical skills.

## Vision fit

fits the current vision

This proposal improves RigorLoop's public skill usability and release token-friendliness while preserving trustworthy, reviewable AI-assisted delivery.

## Initial Intent Preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Reduce runtime amplification for `implement-handoff`. | in scope | Goals; Implement Optimization; Acceptance Criteria |
| Make high-cost public skills progressively loadable from short targeted sections. | in scope | Goals; Recommended Direction; Progressive Loading Rule |
| Add compact quick operating guides to `workflow`, `implement`, and `code-review`. | in scope | Goals; Progressive Loading Rule; Acceptance Criteria |
| Reduce `workflow` public skill size by moving long-form detail to `docs/workflows.md`. | in scope | Workflow Optimization |
| Compress `code-review` while preserving review rigor. | in scope | Code-Review Optimization; Risks and Mitigations |
| Preserve safety-critical review, validation, material-finding, and handoff rules. | in scope | Goals; Non-goals; Risks and Mitigations |
| Use dynamic benchmark evidence to compare before and after behavior. | in scope | Testing and Verification Strategy; Acceptance Criteria |
| Avoid broad rewrites of all skills in this slice. | in scope | Goals; Non-goals; Rollout |
| Avoid changing token-friendliness release gates or introducing hard thresholds. | out of scope | Non-goals |
| Consider later benchmark signals such as skill-section reads or hard budgets. | deferred follow-up | Policy Decisions; Open Questions |

## Context

The `v0.1.1` Token-Friendliness report measured 54,294 estimated static tokens across 23 skills. It identified `workflow` as a high-warning static-size skill and `code-review` as a warning static-size skill. It also showed that all ten required dynamic runs read the active public skill file and that `implement-handoff` produced a single broad output estimated at 20,738 tokens.

The accepted release Token-Friendliness benchmark spec already defines the report-required release gate, dynamic runtime measurement, analyzer summaries, warning-only early thresholds, and public skill portability checks. This proposal does not change that release contract.

The accepted dynamic benchmark expansion proposal already established the `skill-token-runtime-v2` core suite and result-quality reporting. This proposal uses that measured v2 evidence to choose an optimization slice.

The accepted skill token-cost optimization spec already makes bounded evidence collection part of normalized skill behavior. This proposal narrows the next optimization target to measured high-cost public skill surfaces: `implement`, `workflow`, and `code-review`.

The current `implement` skill contains important safety guidance, but it is long and includes many sections: purpose, inputs, outputs, handoff, claim boundaries, baseline pack, validation layering, first-pass completeness, implementation loop, milestone-aware handoff, TDD rules, scope rules, workflow handoff, plan update requirements, stop conditions, evidence collection efficiency, and expected output.

The current `code-review` skill is also long because it carries independent-review behavior, mixed-evidence handling, edge-case proof rules, review statuses, material findings, review recording, detailed review records, workflow handoff, milestone-aware review handoff, clean review template, and expected output.

The current `workflow` skill is the largest public skill. It carries routing, workflow categories, lifecycle-managed artifacts, standard workflow, manual skill invocation, validation layering, review-resolution contract, review-stage handoff, execution-stage claim ownership, bugfix, review-only invocation, invocation context, traceability, default artifact paths, continuation, stop conditions, and evidence collection.

These skills contain useful safety guidance, but their size and structure encourage whole-skill reads.

This proposal does not rely on `docs/project-map.md`; no project map file was present during proposal authoring.

## Options considered

### Option 1: Shrink all skills aggressively

Advantages:

- largest apparent token reduction;
- simple objective.

Disadvantages:

- risks deleting safety-critical behavior;
- does not target measured runtime amplification;
- may make skills vague;
- may cause more review and handoff errors.

### Option 2: Only reduce static size of `workflow` and `code-review`

Advantages:

- addresses the two largest static warnings;
- easier than runtime behavior work.

Disadvantages:

- does not directly address the `implement-handoff` broad-search spike;
- does not prevent whole-skill reads;
- may optimize the wrong driver if runtime behavior dominates.

### Option 3: Progressive loading for high-cost public skills

Advantages:

- targets both static and dynamic cost;
- preserves safety-critical guidance;
- makes important skills usable from short top sections;
- improves section-targeted reads;
- directly addresses broad state discovery in `implement`;
- produces measurable before and after data.

Disadvantages:

- requires careful editing to avoid weakening contracts;
- may require generated output refresh;
- some runtime cost may remain because agents may still load public skill files.

## Recommended direction

Choose Option 3.

Optimize the measured high-cost public skills using progressive loading:

1. Add a compact `Quick operating guide` near the top of `workflow`, `implement`, and `code-review`.
2. Update `implement` to inspect the active plan's `Current Handoff Summary` before any broad milestone search.
3. Shorten `workflow` by moving detailed workflow explanation to `docs/workflows.md` and keeping the skill focused on routing, state assessment, and guide refresh.
4. Compress `code-review` by reducing repeated policy prose and long examples while preserving safety-critical review rules.
5. Rerun the dynamic benchmark and compare `implement-handoff`, `workflow-route`, `code-review-small`, and overall v2 metrics.

Core invariant:

```text
A token-friendly skill is not just shorter.
It helps the agent do the right narrow read first.
```

## Progressive Loading Rule

Large public skills should be usable from their first screen.

Each high-cost skill should start with:

```md
## Quick operating guide

Use this skill to <one sentence>.

Read first:

- <minimal required artifact>
- <minimal required artifact>

Produce:

- <owned result>

Stop when:

- <top stop condition>

Do not claim:

- <most dangerous downstream claim>

Next stage:

- <normal next stage>
```

Detailed rules may remain later in the skill, but common routing and handoff decisions should not require reading the whole file.

## Quick Operating Guide Contract

For this slice, each optimized skill should contain a `## Quick operating guide` section within the first 800 estimated tokens of the skill body.

The section should include these labeled fields:

- `Use this skill to:`
- `Read first:`
- `Produce:`
- `Stop when:`
- `Do not claim:`
- `Next stage:`

The section should fit within 250 words unless the implementation records a safety rationale.

## Implement Optimization

`implement` should avoid broad repository searches to infer milestone state.

Add a strict handoff inspection rule:

```md
## Handoff inspection budget

When checking milestone readiness or handoff state, start with the active plan's `Current Handoff Summary`.

Do not run broad repository searches to infer milestone state.

Use this order:

1. active plan `Current Handoff Summary`
2. current milestone section
3. validation notes for that milestone
4. review-resolution only when findings exist
5. change metadata only for compact status or artifact pointers

If the active plan does not identify the current milestone or next stage, stop and report the missing state instead of searching broadly.
```

Expected behavior:

- `implement-handoff` reads targeted plan state first.
- `implement` does not search broadly across docs, specs, or skills to infer milestone state.
- If state is missing, the skill stops with a state-owner blocker.

For handoff-state inspection, avoid broad searches such as:

- searching all docs, specs, or skills for milestone names;
- searching generated adapter output;
- searching historical reviews before checking the active plan;
- using broad `rg` output to infer current state.

Allowed first steps:

- read the active plan `Current Handoff Summary`;
- read the current milestone section;
- read validation notes for that milestone.

## Workflow Optimization

`workflow` should become smaller and more operational.

Keep in `workflow`:

- purpose;
- when to use;
- when not to use;
- input lookup;
- route current task;
- create or refresh `docs/workflows.md`;
- stop conditions;
- claim boundaries;
- concise result format.

Move or summarize out of `workflow`:

- full workflow category explanation;
- long review-resolution contract;
- long lifecycle-managed artifact table;
- detailed validation layering;
- bugfix workflow detail;
- long traceability examples;
- detailed default artifact path lists;
- repeated workflow sequence descriptions.

Those details belong in:

- `docs/workflows.md`;
- authoritative specs;
- owning stage skills.

Implementation should record moved or summarized workflow guidance in a migration table:

| Removed or summarized topic | New owner surface | Rationale |
|---|---|---|
| Review-resolution details | `docs/workflows.md` or owning review guidance | Workflow skill should route, not duplicate detailed policy. |
| Lifecycle-managed artifact table | `docs/workflows.md` | Human-readable workflow guide owns the summary. |
| Detailed validation layering | owning validation or verify guidance | Stage-specific proof belongs to owning stages. |

No workflow safety topic should be removed without a new owner surface or an explicit no-longer-needed rationale.

Target:

```text
workflow public skill should move toward 3,000-4,000 estimated tokens,
or justify why remaining size is necessary.
```

Do not introduce a hard `workflow` token-size gate in this slice. A report above 5,000 estimated tokens should require justification explaining which safety-critical guidance remains in the skill and why it cannot live in `docs/workflows.md` or the workflow contract.

Hard gates should not be considered until at least three comparable dynamic reports exist. Even then, a hard gate should target unexplained growth, missing high-warning justification, duplicated long-form lifecycle prose, or portability leakage rather than absolute size alone.

## Code-Review Optimization

`code-review` should remain safety-rich but less repetitive.

Keep:

- independent-review posture;
- inputs to inspect;
- review statuses;
- material finding requirements;
- mixed-evidence handling;
- direct proof for named edge cases;
- milestone-aware handoff;
- stop conditions;
- result format.

Compress:

- repeated review-recording prose;
- long clean-review template;
- repeated workflow order language;
- long lifecycle contract details already owned by workflow docs and specs.

Target:

```text
code-review public skill should move toward 3,500-4,000 estimated tokens,
or justify why remaining size is necessary.
```

Do not split `code-review` templates into reference files in this slice. First add progressive loading, compress repeated prose, remove duplicated workflow policy, shorten the clean-review template, and measure the result. Consider reference files later only if `code-review` remains above roughly 4,000-4,500 estimated tokens, `code-review-small` still reads the whole skill, the clean-review template dominates size, or the same template is duplicated across review skills.

The implementation should preserve the substance of these `code-review` contracts:

- independent-review mode;
- mixed-evidence handling;
- material finding requirements;
- first-pass status vocabulary;
- severity vocabulary;
- isolation and recording rule;
- detailed review record triggers;
- milestone-aware review handoff;
- stop conditions;
- result format.

Compression may shorten wording, but it should not remove these contracts.

## Skill Reading Guidance

Add or reinforce guidance in token-cost documentation:

```text
Do not read a whole SKILL.md when a specific section is enough.

Use this order:

1. list headings
2. read the Quick operating guide
3. read the specific needed section
4. read the whole skill only when the whole skill is the review target
```

The benchmark runner may add a `skill section read` signal later, after progressive-loading guidance and stable section headings exist. The proposed ordering is:

```text
Design section boundaries first.
Measure section reads second.
```

That later signal should distinguish full-skill reads from targeted section reads only when the analyzer can reliably map command ranges to skill headings.

## Expected behavior changes

- `implement-handoff` avoids broad milestone searches when the active plan has a current handoff summary.
- `workflow-route` can route from a shorter top-level operating section.
- `code-review-small` can start from concise review guidance without reading the entire skill.
- Dynamic benchmarks should show smaller or more targeted skill-file reads.
- Static size of `workflow` and possibly `code-review` should decrease or be justified.
- Safety-critical review, verification, and material-finding guidance remains intact.

## Architecture impact

No runtime architecture change is expected.

This is a public skill surface and release benchmark optimization. Affected surfaces may include:

- `skills/workflow/SKILL.md`;
- `skills/implement/SKILL.md`;
- `skills/code-review/SKILL.md`;
- `docs/workflows.md`;
- `docs/learn/topics/token-cost-measurement.md`;
- generated public skill and adapter output after canonical skill changes;
- token-cost benchmark report after rerun.

No change to workflow stage order, release packaging architecture, or adapter layout is expected.

## Testing and verification strategy

Before implementation:

- record current static skill sizes;
- record current dynamic baseline from `v0.1.1`.

After implementation:

```bash
python scripts/measure-skill-tokens.py
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/build-adapters.py --version 0.1.1 --check
python scripts/validate-adapters.py --version 0.1.1
```

Benchmark ordering after canonical skill edits:

1. regenerate generated and public skill output;
2. validate generated output drift;
3. run targeted dynamic benchmarks against the regenerated public Codex skill output.

Dynamic benchmark comparison should use the public skill surface, not stale canonical-only edits.

Rerun targeted dynamic benchmarks:

```text
workflow-route
implement-handoff
code-review-small
verify-final-pack
```

If release benchmark tooling requires the full suite for comparable reporting, run the full required core suite.

Measure:

- static `workflow` estimated tokens;
- static `code-review` estimated tokens;
- `implement-handoff` largest command output;
- full-skill read count;
- repeated read signals;
- `workflow-route` input tokens;
- `code-review-small` input tokens;
- result-quality status.

Record before and after evidence at:

```text
docs/reports/token-cost/optimizations/YYYY-MM-DD-progressive-loading-high-cost-skills.md
```

The optimization comparison report should include:

- baseline report referenced;
- changed skills;
- static tokens before and after for `workflow`, `implement`, and `code-review`;
- targeted benchmark results before and after for `workflow-route`, `implement-handoff`, `code-review-small`, and `verify-final-pack`;
- largest command output before and after;
- full-skill read count before and after;
- result-quality status;
- explanation for any remaining warning or high-warning.

## Acceptance criteria

- `workflow`, `implement`, and `code-review` each include a compact `Quick operating guide`.
- Each `Quick operating guide` appears near the top of the skill and includes the required labels.
- `implement` explicitly starts handoff-state inspection from the active plan's `Current Handoff Summary`.
- `implement` tells agents to stop when milestone state is missing instead of searching broadly.
- `workflow` no longer carries unnecessary long-form workflow detail that belongs in `docs/workflows.md`.
- Workflow detail removed or summarized from `workflow` is accounted for with a new owner surface or an explicit no-longer-needed rationale.
- `code-review` preserves safety-critical review guidance while reducing repeated prose or large templates.
- Public skill portability remains valid.
- Generated public skill output is regenerated and validated after canonical skill edits.
- Targeted dynamic benchmarks run after regenerated public skill output is available.
- Static skill measurement is rerun.
- Targeted dynamic benchmark comparison is recorded in the optimization comparison report.
- No result-quality benchmark regresses from `pass` to `fail`.
- Any remaining high-warning token cost is explained as safety-critical or runtime-base cost.

## Rollout and rollback

Rollout:

1. Accept proposal.
2. Write or update spec/plan only if the skill contract needs a normative change.
3. Optimize `implement` handoff inspection first.
4. Add quick operating guides to `workflow`, `implement`, and `code-review`.
5. Reduce `workflow` long-form detail by moving or summarizing content into `docs/workflows.md`.
6. Compress `code-review` repeated prose while preserving safety rules.
7. Regenerate public skill and adapter output.
8. Run static measurement.
9. Run targeted dynamic benchmarks.
10. Record before and after report.
11. Review and verify.

Rollback:

- restore the prior canonical skill wording if optimization weakens guidance or causes benchmark result quality to fail;
- keep measurement evidence as historical;
- preserve any safe quick-guide improvements;
- do not roll back unrelated benchmark tooling.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Skill becomes too terse. | Preserve safety-critical sections and claim boundaries. |
| Workflow detail is moved but not discoverable. | Ensure `docs/workflows.md` has the moved explanation and `workflow` links to it. |
| Code-review loses material-finding rigor. | Keep material finding, mixed-evidence, and status rules intact. |
| Dynamic benchmark cost does not improve. | Record the result; the cost may be runtime-base or tool behavior, not text size. |
| Generated adapters drift. | Regenerate and run adapter checks. |
| Agent still reads whole skill. | Add section-targeted reading guidance and rerun benchmark to measure. |

## Policy Decisions

- No hard `workflow` token budget after only two comparable reports. Use the 3,000-4,000 estimated-token target range and require justification above high-warning size. Consider hard gates only after at least three comparable reports and only for unexplained growth or missing justification.
- Add a `skill section read` benchmark signal later, after progressive-loading guidance exists and the analyzer can reliably distinguish full-skill reads from targeted section reads.
- Do not split `code-review` templates into reference files in this slice. Compress and measure first; externalize templates only if the measured problem remains.
- Implement this as a focused optimization slice under the existing `skill-token-cost-optimization`, release token-friendliness benchmark, and skill-contract guidance. Add a new spec only if the project introduces normative new token-budget gates, mandatory quick-guide requirements for every skill, a required section-read analyzer signal, mandatory reference-file splitting, or a new release gate.

## Open questions

None blocking proposal-review.

## Decision log

| Date | Decision | Reason |
|---|---|---|
| 2026-05-11 | Target `implement`, `workflow`, and `code-review` first. | The `v0.1.1` report identified `implement-handoff`, `workflow`, and `code-review` as top cost drivers. |
| 2026-05-11 | Use progressive loading instead of broad deletion. | Safety-critical guidance must be preserved. |
| 2026-05-11 | Rerun targeted dynamic benchmarks after optimization. | Dynamic evidence is needed to confirm the real effect. |
| 2026-05-11 | Keep hard token gates out of this slice. | Early warnings should guide optimization, not become hard gates before at least three comparable reports. |
| 2026-05-11 | Defer `skill section read` measurement until sections are stable. | The analyzer needs reliable section boundaries before the signal is meaningful. |
| 2026-05-11 | Keep `code-review` templates in the skill for now. | Compression should be measured before adding reference-file indirection. |
| 2026-05-11 | Treat this as an implementation slice under existing specs. | The proposal changes skill wording and organization, not release gates, workflow order, report schema, or public portability policy. |

## Next artifacts

- progressive-loading implementation slice for skill updates
- static skill measurement
- targeted dynamic benchmark comparison
- generated adapter validation
- explain-change and verify

## Follow-on artifacts

None yet.

## Readiness

Accepted and ready for a progressive-loading implementation plan or slice.

The proposal targets the measured top cost drivers without weakening RigorLoop's safety and review contracts.
