# Progressive Loading for High-Cost Public Skills

## Status

approved

## Related proposal

- [Progressive Loading for High-Cost Public Skills](../docs/proposals/2026-05-11-progressive-loading-for-high-cost-public-skills.md), accepted.

## Goal and context

This spec defines the contract for optimizing the measured high-cost public skills `workflow`, `implement`, and `code-review` so agents can start from a short operating section, avoid broad handoff-state discovery, and preserve review and validation safety guidance.

The `v0.1.1` Token-Friendliness report identified `implement-handoff` command-output amplification, large static `workflow` and `code-review` skill sizes, and runtime reads of active public skill files across all ten required v2 transition benchmarks. This change uses that evidence to optimize the highest-cost skill surfaces without changing workflow order, release gates, benchmark schema, or public adapter layout.

This spec is governed by the accepted `skill-token-cost-optimization` spec, the release Token-Friendliness benchmark specs, and the skill contract. It narrows the implementation slice to progressive loading for three measured public skills.

## Glossary

- `optimized skill`: one of `workflow`, `implement`, or `code-review` in this implementation slice.
- `Quick operating guide`: a short top-of-skill section that gives the minimum operating path for common use.
- `high-cost public skill`: a public skill whose static size or benchmark runtime behavior produced a warning or high-warning in the `v0.1.1` Token-Friendliness report.
- `handoff-state inspection`: reading artifact state to determine the current milestone, next stage, or readiness for downstream handoff.
- `broad milestone search`: a broad repository search that tries to infer current milestone or handoff state before reading the active plan's `Current Handoff Summary`.
- `workflow detail migration table`: an implementation accounting table that records where removed or summarized `workflow` skill guidance now lives.
- `optimization comparison report`: a durable before and after report for this optimization slice.
- `public Codex skill output`: generated Codex adapter skill text under the public adapter surface measured by dynamic benchmarks.
- `safety-critical review guidance`: code-review guidance whose removal could weaken independent review, finding recording, material-finding disposition, milestone handoff, or result claims.

## Examples first

### Example E1: quick guide enables a narrow first read

Given an agent invokes `workflow`
When it opens the public `workflow` skill
Then the first screen contains `## Quick operating guide`
And the guide includes `Use this skill to:`, `Read first:`, `Produce:`, `Stop when:`, `Do not claim:`, and `Next stage:`
And the agent can route the normal task without reading a long lifecycle-policy section first.

### Example E2: implement handoff starts from the active plan

Given an agent is checking implementation handoff readiness
When the active plan has a `Current Handoff Summary`
Then `implement` guidance directs the agent to read that summary first
And it does not direct the agent to search all docs, specs, skills, generated adapters, or historical reviews to infer current state.

### Example E3: missing handoff state stops instead of broad search

Given an active plan does not identify the current milestone or next stage
When `implement` is checking milestone readiness
Then the skill directs the agent to report the missing state as a blocker
And it does not instruct the agent to infer the state from broad repository search output.

### Example E4: workflow details move with ownership

Given `workflow` skill text summarizes review-resolution detail
When implementation removes the long detail from the skill
Then the workflow detail migration table records the removed topic, the new owner surface, and the rationale
And no safety topic disappears without a new owner surface or explicit no-longer-needed rationale.

### Example E5: code-review compression preserves safety contracts

Given `code-review` repeated prose is compressed
When the updated skill is reviewed
Then independent-review mode, mixed-evidence handling, material finding requirements, status and severity vocabulary, isolation and recording rules, detailed review record triggers, milestone-aware handoff, stop conditions, and result format remain substantively present.

### Example E6: benchmarks measure regenerated public skills

Given canonical skill text has changed
When targeted dynamic benchmarks are rerun
Then generated public skill output has already been regenerated and validated
And the benchmark runner measures the regenerated public Codex skill surface rather than stale canonical-only edits.

## Requirements

R1. The implementation MUST optimize only the `workflow`, `implement`, and `code-review` public skills in this slice unless a later approved artifact broadens the scope.

R1a. The implementation MUST NOT optimize every skill as part of this slice.

R1b. The implementation MUST NOT change workflow stage order, release token-friendliness gates, benchmark report schema, or adapter package layout.

R1c. The implementation MUST NOT introduce hard token-size gates.

R2. Each optimized skill MUST contain a `## Quick operating guide` section within the first 800 estimated tokens of the skill body.

R2a. Each `## Quick operating guide` section MUST include the labeled fields `Use this skill to:`, `Read first:`, `Produce:`, `Stop when:`, `Do not claim:`, and `Next stage:`.

R2b. Each `## Quick operating guide` section SHOULD fit within 250 words unless the implementation records a safety rationale for exceeding that length.

R2c. The quick guide MUST preserve correctness and MUST NOT tell agents to skip full-file or broader-section reads when full-file-read escape conditions apply.

R3. `implement` MUST direct handoff-state inspection to start with the active plan's `Current Handoff Summary`.

R3a. After the `Current Handoff Summary`, `implement` MUST direct agents to inspect the current milestone section and that milestone's validation notes before broader handoff-state surfaces.

R3b. `implement` MUST NOT direct agents to infer handoff state by searching all docs, specs, skills, generated adapter output, historical reviews, or broad `rg` output before checking active plan state.

R3c. If the active plan does not identify the current milestone or next stage, `implement` MUST direct agents to stop and report the missing state instead of searching broadly to infer it.

R4. `workflow` MUST keep common routing, state assessment, stop conditions, claim boundaries, and concise result guidance in the public skill.

R4a. `workflow` SHOULD move or summarize long-form workflow category explanation, review-resolution detail, lifecycle-managed artifact tables, validation-layering detail, bugfix detail, long traceability examples, default artifact path lists, and repeated workflow sequence prose when equivalent guidance has a clearer owner surface.

R4b. Whenever `workflow` removes or summarizes safety-relevant guidance, the implementation MUST record a workflow detail migration table with removed or summarized topic, new owner surface, and rationale.

R4c. Workflow safety topics MUST NOT be removed without a new owner surface or explicit no-longer-needed rationale.

R5. `code-review` MAY compress repeated prose, long templates, repeated workflow order language, and lifecycle detail already owned by workflow docs or specs.

R5a. `code-review` MUST preserve the substance of independent-review mode, mixed-evidence handling, material finding requirements, first-pass status vocabulary, severity vocabulary, isolation and recording rules, detailed review record triggers, milestone-aware review handoff, stop conditions, and result format.

R5b. `code-review` MUST NOT split templates into reference files in this slice.

R5c. The implementation MAY propose later reference files only if post-optimization evidence shows `code-review` remains above the warning range, still causes whole-skill reads in `code-review-small`, has a clean-review template that dominates size, or duplicates templates across review skills.

R6. Token-cost reading guidance MUST direct agents to prefer heading lists, quick guides, and specific needed sections before whole-skill reads when the whole skill is not the review target.

R6a. Token-cost reading guidance MUST preserve full-file-read escape conditions from the skill-token-cost optimization contract.

R6b. The implementation MUST NOT imply that output caps make broad reads acceptable as the normal first evidence step.

R7. Canonical skill changes MUST be regenerated into generated local and public adapter output before targeted dynamic benchmarks are run.

R7a. Generated output drift validation MUST run before targeted dynamic benchmarks.

R7b. Targeted dynamic benchmarks MUST measure regenerated public Codex skill output, not stale canonical-only edits or repository-local generated mirrors.

R8. The implementation MUST run static skill measurement after the optimized skill changes.

R8a. Static measurement evidence MUST include estimated tokens for `workflow`, `implement`, and `code-review` before and after the optimization.

R8b. Static `workflow` SHOULD target 3,000-4,000 estimated tokens after optimization, but exceeding that range MUST NOT block readiness by itself.

R8c. Static `workflow` above 5,000 estimated tokens after optimization MUST include a justification explaining which safety-critical guidance remains in the skill and why it cannot live in `docs/workflows.md`, an authoritative spec, or owning stage guidance.

R8d. Static `code-review` SHOULD target 3,500-4,000 estimated tokens after optimization, but exceeding that range MUST NOT block readiness by itself when safety-critical guidance justifies the size.

R9. The implementation MUST rerun targeted dynamic benchmarks for `workflow-route`, `implement-handoff`, `code-review-small`, and `verify-final-pack`, unless the plan records that the full required core suite is needed for comparable evidence.

R9a. Dynamic benchmark evidence MUST include result-quality status for each rerun targeted benchmark.

R9b. No targeted benchmark result-quality status MAY regress from `pass` to `fail` without blocking readiness or recording an owner-approved deferral.

R9c. Dynamic benchmark evidence MUST record largest command output and full-skill read count before and after optimization.

R10. The implementation MUST create an optimization comparison report at `docs/reports/token-cost/optimizations/YYYY-MM-DD-progressive-loading-high-cost-skills.md`.

R10a. The optimization comparison report MUST reference the baseline report.

R10b. The optimization comparison report MUST name changed skills.

R10c. The optimization comparison report MUST include static tokens before and after for `workflow`, `implement`, and `code-review`.

R10d. The optimization comparison report MUST include targeted benchmark results before and after for `workflow-route`, `implement-handoff`, `code-review-small`, and `verify-final-pack`.

R10e. The optimization comparison report MUST include largest command output before and after, full-skill read count before and after, result-quality status, and explanations for any remaining warning or high-warning.

R11. Public skill wording MUST remain project-portable.

R11a. Published skill text MUST NOT expose repository-maintainer-only source paths, generated mirror paths, adapter package paths, selector path constraints, drift-check mechanics, shared-block implementation mechanics, or local repository examples.

R11b. Repository-maintainer validation commands and generated-output procedures MAY appear in the spec, test spec, plan, contributor docs, or change-local evidence.

R12. The implementation MUST preserve existing required validation coverage, review obligations, artifact obligations, and workflow gates.

R12a. Optimizing token cost MUST NOT reduce correctness, reviewability, generated-output determinism, or public adapter portability.

## Inputs and outputs

Inputs:

- accepted progressive-loading proposal;
- approved skill token-cost optimization spec;
- approved release Token-Friendliness benchmark specs;
- current `v0.1.1` Token-Friendliness report and analyzer summaries;
- canonical `workflow`, `implement`, and `code-review` skill text;
- `docs/workflows.md` and owning stage skills or specs for migrated guidance;
- generated local and public adapter output after regeneration.

Outputs:

- updated canonical `workflow`, `implement`, and `code-review` skill text;
- updated `docs/workflows.md` or other owner surfaces when workflow guidance moves;
- workflow detail migration table in the implementation plan, change artifact, or optimization report;
- regenerated generated local and public adapter output;
- static skill measurement evidence;
- targeted dynamic benchmark evidence;
- optimization comparison report.

## State and invariants

- Workflow stage order remains unchanged.
- Release token-friendliness gates remain unchanged.
- Benchmark schema remains unchanged.
- Adapter package layout remains unchanged.
- `workflow`, `implement`, and `code-review` remain public skills.
- Correctness outranks token savings.
- Full-file-read escape conditions remain available.
- Generated local skill output and public adapter output remain deterministic derived artifacts.
- `docs/workflows.md` remains an operating guide subordinate to approved specs and the constitution.

## Error and boundary behavior

- If a quick guide cannot fit within 250 words without weakening safety guidance, the implementation records a safety rationale and preserves safety guidance.
- If moved workflow content has no clear owner surface, the implementation keeps it in `workflow` or records an explicit no-longer-needed rationale before removing it.
- If handoff state is missing from the active plan, `implement` guidance treats that as a state-owner blocker rather than encouraging broad inference.
- If targeted dynamic benchmarks cannot run, the implementation records the blocker, owner, environment, and follow-up; readiness cannot claim improved dynamic behavior from static evidence alone.
- If generated public skill output is stale, dynamic benchmark results are invalid for this slice until generated output is regenerated and validated.
- If benchmark cost does not improve, the optimization comparison report records the result and explains whether the remaining cost is safety-critical, runtime-base, fixture-driven, or tool-behavior-driven.

## Compatibility and migration

- Existing historical reports and analyzer summaries remain valid.
- Existing release Token-Friendliness report requirements remain valid.
- Existing dynamic benchmark warnings remain warning-only unless a later approved spec changes release gates.
- Existing downstream users may still read full skills; progressive loading adds a narrow first path and does not remove the ability to read detailed guidance.
- Rollback may restore prior canonical skill wording, regenerate derived output, and preserve the optimization comparison report as historical evidence.

## Observability

- Validation evidence should identify quick-guide presence, required labels, and placement for each optimized skill.
- Validation evidence should identify generated-output drift checks and adapter validation.
- Benchmark evidence should identify the public skill source measured by the runner.
- The optimization comparison report is the durable observability surface for before and after token cost, command-output amplification, full-skill reads, and result quality.
- No runtime logs, metrics, traces, or audit events are required.

## Security and privacy

- Public skill text MUST remain free of secrets, credentials, tokens, private keys, private incident data, unnecessary machine-local paths, and private user data.
- Benchmark evidence that would expose sensitive local paths or raw output MAY be summarized when the summary preserves required review evidence.
- Summary-first reporting MUST NOT hide failures needed to evaluate result quality or validation readiness.

## Accessibility and UX

No UI behavior is changed.

The user-facing skill experience should improve by placing the common operating path near the top of each optimized public skill and making the first read shorter and more predictable.

## Performance expectations

- The optimized skills should reduce static size or justify remaining warning/high-warning size.
- `implement-handoff` should reduce largest command-output amplification or explain why the remaining output is unavoidable.
- `workflow-route` and `code-review-small` should be able to start from quick-guide guidance without requiring long whole-skill reads for common routing or review setup.
- Performance expectations are evidence targets, not hard release gates in this slice.

## Edge cases

E1. Quick-guide placement conflicts with existing front matter.
Expected behavior: front matter remains valid, and the quick guide appears within the first 800 estimated tokens of the skill body.

E2. Quick-guide brevity conflicts with safety guidance.
Expected behavior: safety guidance wins, and the implementation records a safety rationale for exceeding 250 words.

E3. Active plan lacks `Current Handoff Summary`.
Expected behavior: `implement` reports missing handoff state instead of using broad repository searches to infer it.

E4. Workflow detail has no better owner.
Expected behavior: keep the detail in `workflow` or record a no-longer-needed rationale before removal.

E5. Code-review template remains large after compression.
Expected behavior: keep the template in the skill for this slice and record size justification; reference-file splitting remains a follow-up.

E6. Dynamic benchmark reads the repository-local mirror or stale public adapter output.
Expected behavior: reject that benchmark evidence for this slice and rerun after public adapter regeneration and validation.

E7. Static size improves but result quality fails.
Expected behavior: block readiness or restore safe guidance; token savings do not justify result-quality regression.

E8. Static size remains high but safety guidance is justified.
Expected behavior: record the justification and do not treat absolute size alone as a hard gate.

## Non-goals

- Do not optimize every skill.
- Do not introduce hard token-size gates.
- Do not change release token-friendliness gates.
- Do not change benchmark report schema.
- Do not add a required `skill section read` analyzer signal in this slice.
- Do not split `code-review` templates into reference files in this slice.
- Do not remove safety-critical review, validation, material-finding, or milestone-handoff guidance.
- Do not change workflow order.
- Do not hand-edit generated adapter output without regeneration.

## Acceptance criteria

- `workflow`, `implement`, and `code-review` each contain `## Quick operating guide` within the first 800 estimated tokens of the skill body.
- Each quick guide contains all required labels.
- `implement` directs agents to start handoff-state inspection from active plan `Current Handoff Summary`.
- `implement` includes guidance to stop when milestone or next-stage state is missing.
- `implement` does not direct agents to infer handoff state from broad repository searches before active plan inspection.
- Workflow detail removed or summarized from `workflow` is accounted for with a new owner surface or explicit no-longer-needed rationale.
- `code-review` preserves all protected safety-critical review contracts.
- Generated local and public adapter output is regenerated or checked and validated before targeted dynamic benchmarks.
- Static skill measurement records before and after tokens for `workflow`, `implement`, and `code-review`.
- Targeted dynamic benchmarks run against regenerated public Codex skill output for `workflow-route`, `implement-handoff`, `code-review-small`, and `verify-final-pack`, or the full required core suite runs with those benchmarks included.
- The optimization comparison report exists and includes all required comparison fields.
- No targeted benchmark result-quality status regresses from `pass` to `fail`.
- Any remaining warning or high-warning token cost is explained.

## Open questions

None.

## Next artifacts

- plan or implementation slice
- test-spec
- implementation
- code-review
- explain-change
- verify

## Follow-on artifacts

None yet.

## Readiness

Approved after clean spec-review and ready for planning.
