# Progressive Loading for High-Cost Public Skills Test Spec

## Status

- active

## Related spec and plan

- Spec: [Progressive Loading for High-Cost Public Skills](progressive-loading-high-cost-public-skills.md), approved after clean spec-review.
- Proposal: [Progressive Loading for High-Cost Public Skills](../docs/proposals/2026-05-11-progressive-loading-for-high-cost-public-skills.md), accepted.
- Plan: [Progressive Loading for High-Cost Public Skills](../docs/plans/2026-05-11-progressive-loading-high-cost-public-skills.md), approved by plan-review R2.
- Change metadata: [change.yaml](../docs/changes/2026-05-11-progressive-loading-high-cost-public-skills/change.yaml).
- Architecture: no runtime architecture impact. The approved spec bounds this slice to public skill text, workflow docs, generated output, and benchmark/report evidence.
- Related proof surfaces:
  - `scripts/test-skill-validator.py`
  - `scripts/validate-skills.py`
  - `scripts/measure-skill-tokens.py`
  - `scripts/build-skills.py`
  - `scripts/build-adapters.py`
  - `scripts/validate-adapters.py`
  - `scripts/test-adapter-distribution.py`
  - `scripts/run-token-cost-benchmarks.py`
  - `scripts/validate-token-cost-report.py`
  - `docs/reports/token-cost/releases/v0.1.1.yaml`

## Testing strategy

- Use static validator tests for top-of-skill quick guides, required labels, `implement` handoff inspection wording, section-first reading guidance, and forbidden broad-search guidance.
- Use manual contract review for safety-sensitive prose that should not be reduced to brittle exact wording checks: workflow migration ownership and protected `code-review` contracts.
- Use static skill measurement for before/after token estimates and warning/high-warning justification.
- Use generated-output checks and adapter validation before any dynamic benchmark evidence is accepted.
- Use targeted dynamic benchmark evidence, or the full required core suite when needed for comparable reporting, to prove regenerated public Codex skill behavior.
- Use a durable optimization comparison report as the reviewable before/after evidence surface.
- Use change metadata, review-artifact, lifecycle, and diff checks to keep the non-trivial change traceable.

## Requirement coverage map

| Requirement IDs | Test IDs | Notes |
|---|---|---|
| `R1`, `R1a`-`R1c` | `T1`, `T8`, `T12` | Scope, non-goals, unchanged gates/schema/layout, and generated-output boundaries. |
| `R2`, `R2a`-`R2c` | `T2`, `T6`, `T11` | Quick-guide placement, labels, word-count rationale, and escape-condition preservation. |
| `R3`, `R3a`-`R3c` | `T3` | Handoff-state inspection starts from the active plan and blocks missing state. |
| `R4`, `R4a`-`R4c` | `T4`, `T10` | Workflow detail migration accounting and owner-surface proof. |
| `R5`, `R5a`-`R5c` | `T5`, `T7`, `T12` | `code-review` compression, protected content, no reference split, and later-follow-up boundaries. |
| `R6`, `R6a`-`R6b` | `T6`, `T11` | Section-first reading guidance keeps full-file escape conditions and output-cap discipline. |
| `R7`, `R7a`-`R7b` | `T8`, `T9` | Generated local/public output and adapter validation precede dynamic benchmarks. |
| `R8`, `R8a`-`R8d` | `T7`, `T10` | Static measurement and warning/high-warning rationale. |
| `R9`, `R9a`-`R9c` | `T9`, `T10` | Targeted benchmark rerun, result quality, command output, and full-skill read evidence. |
| `R10`, `R10a`-`R10e` | `T10` | Optimization comparison report fields. |
| `R11`, `R11a`-`R11b` | `T11` | Public portability and allowed internal maintainer surfaces. |
| `R12`, `R12a` | `T1`, `T5`, `T8`, `T9`, `T12` | Existing validation, review, artifact, workflow, determinism, and portability gates remain intact. |

## Example coverage map

| Example | Test IDs | Notes |
|---|---|---|
| `E1` | `T2`, `T6` | `workflow` starts with a usable quick guide and section-first reading guidance. |
| `E2` | `T3` | `implement` starts handoff inspection from `Current Handoff Summary`. |
| `E3` | `T3` | Missing current milestone or next stage stops instead of broad search. |
| `E4` | `T4`, `T10` | Removed or summarized workflow detail has owner-surface accounting. |
| `E5` | `T5` | `code-review` compression preserves safety contracts. |
| `E6` | `T8`, `T9` | Benchmarks run only after generated public skill output is current. |

## Edge case coverage

- Quick-guide placement conflicts with front matter: `T2`.
- Quick-guide brevity conflicts with safety guidance: `T2`, `T5`, `T10`.
- Active plan lacks `Current Handoff Summary`: `T3`.
- Workflow detail has no better owner: `T4`.
- `code-review` template remains large after compression: `T5`, `T7`, `T10`.
- Dynamic benchmark uses stale or repository-local output: `T8`, `T9`.
- Static size improves but result quality fails: `T9`, `T12`.
- Static size remains high but safety guidance is justified: `T7`, `T10`.

## Test cases

### T1. Optimization scope and non-goals remain exact

- Covers: `R1`, `R1a`-`R1c`, `R12`, `R12a`
- Level: integration, manual
- Fixture/setup:
  - `specs/progressive-loading-high-cost-public-skills.md`
  - `docs/plans/2026-05-11-progressive-loading-high-cost-public-skills.md`
  - final diff
- Steps:
  - Assert the implementation changes only the optimized skill set unless a later approved artifact broadens scope.
  - Assert no hard token-size gate, benchmark schema change, adapter package layout change, or workflow order change is introduced.
  - Manually inspect the final diff for unrelated skill rewrites or release-gate changes.
- Expected result:
  - The slice optimizes `workflow`, `implement`, and `code-review` without expanding into a broader workflow or release-policy change.
- Failure proves:
  - The implementation exceeded the approved slice or weakened existing gates.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual final diff review

### T2. Optimized skills contain valid quick operating guides

- Covers: `R2`, `R2a`-`R2c`, `E1`
- Level: integration, manual
- Fixture/setup:
  - `skills/workflow/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert each optimized skill contains `## Quick operating guide` within the first 800 estimated tokens of the skill body.
  - Assert each guide includes `Use this skill to:`, `Read first:`, `Produce:`, `Stop when:`, `Do not claim:`, and `Next stage:`.
  - Assert each quick guide is 250 words or less, or the implementation records a safety rationale.
  - Manually confirm each quick guide preserves correctness and does not tell agents to skip full-file or broader-section reads when escape conditions apply.
- Expected result:
  - Each optimized skill can be used from a compact top section without removing the safety path to fuller reading.
- Failure proves:
  - Progressive loading is not measurable or is unsafe.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual review during M2

### T3. `implement` starts handoff-state inspection from active plan state

- Covers: `R3`, `R3a`-`R3c`, `E2`, `E3`
- Level: integration, manual
- Fixture/setup:
  - `skills/implement/SKILL.md`
  - active plan fixture or text sample with `Current Handoff Summary`
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert `implement` directs handoff-state inspection to start with the active plan's `Current Handoff Summary`.
  - Assert it directs agents next to the current milestone section and validation notes.
  - Assert it forbids using broad searches across docs, specs, skills, generated adapters, historical reviews, or broad `rg` output to infer state before active-plan inspection.
  - Assert missing current milestone or next-stage state is reported as a blocker rather than inferred from broad searches.
- Expected result:
  - `implement-handoff` has a narrow first evidence path and a clear stop condition.
- Failure proves:
  - The highest measured runtime amplification source remains structurally encouraged.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual review during M2

### T4. Workflow detail migration has owner-surface accounting

- Covers: `R4`, `R4a`-`R4c`, `E4`
- Level: manual, contract
- Fixture/setup:
  - before/after `skills/workflow/SKILL.md`
  - `docs/workflows.md`
  - workflow detail migration table in plan, change-local evidence, or optimization report
- Steps:
  - Compare removed or summarized `workflow` topics against the migration table.
  - Assert each safety-relevant removed or summarized topic has a new owner surface and rationale.
  - Assert topics without a better owner remain in `workflow` or have an explicit no-longer-needed rationale.
  - Manually confirm `workflow` still keeps routing, state assessment, stop conditions, claim boundaries, and concise result guidance.
- Expected result:
  - Workflow compression moves detail without deleting safety guidance.
- Failure proves:
  - Token reduction created an unowned workflow safety gap.
- Automation location:
  - manual M2 review checklist
  - `docs/reports/token-cost/optimizations/2026-05-11-progressive-loading-high-cost-skills.md`

### T5. `code-review` preserves protected review contracts

- Covers: `R5`, `R5a`-`R5c`, `E5`
- Level: integration, manual
- Fixture/setup:
  - before/after `skills/code-review/SKILL.md`
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert `code-review` does not split templates into reference files in this slice.
  - Assert static checks or manual review confirm the substance of independent-review mode, mixed-evidence handling, material finding requirements, first-pass status vocabulary, severity vocabulary, isolation and recording rules, detailed review record triggers, milestone-aware review handoff, stop conditions, and result format.
  - Assert any size that remains above target range is justified instead of driving unsafe deletion.
- Expected result:
  - `code-review` becomes more progressively loadable without weakening review rigor.
- Failure proves:
  - Compression removed safety-critical review behavior or prematurely externalized templates.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual M2 review checklist

### T6. Section-first reading guidance preserves escape conditions

- Covers: `R2c`, `R6`, `R6a`, `R6b`, `E1`
- Level: integration, manual
- Fixture/setup:
  - token-cost reading guidance surface updated by this slice
  - optimized skill files
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert guidance directs agents to list headings, read the quick guide, and read specific needed sections before whole-skill reads when the whole skill is not the review target.
  - Assert full-file-read escape conditions remain present or linked to the governing contract.
  - Assert guidance does not imply that output caps make broad reads acceptable as normal first evidence.
- Expected result:
  - The optimization teaches narrow first reads while preserving correctness-driven broad reads.
- Failure proves:
  - The guidance either fails to reduce whole-skill reads or encourages under-reading.
- Automation location:
  - `scripts/test-skill-validator.py`
  - manual review during M1 and M2

### T7. Static token measurement records before/after and justifications

- Covers: `R5c`, `R8`, `R8a`-`R8d`
- Level: smoke, manual
- Fixture/setup:
  - `scripts/measure-skill-tokens.py`
  - baseline `v0.1.1` report
  - updated skill files
  - optimization comparison report
- Steps:
  - Run `python scripts/measure-skill-tokens.py` after optimized skill edits.
  - Record before and after estimated tokens for `workflow`, `implement`, and `code-review`.
  - If `workflow` remains above 5,000 estimated tokens, assert the report explains why remaining guidance is safety-critical or cannot live elsewhere.
  - If `code-review` remains above target range, assert the report explains the preserved safety-critical content and keeps reference-file splitting as a follow-up only.
- Expected result:
  - Static cost changes are visible and any remaining warning/high-warning is justified.
- Failure proves:
  - The implementation cannot demonstrate static token-cost impact or acceptable remaining size.
- Automation location:
  - `scripts/measure-skill-tokens.py`
  - `docs/reports/token-cost/optimizations/2026-05-11-progressive-loading-high-cost-skills.md`

### T8. Generated skill and adapter output is current before benchmarks

- Covers: `R1b`, `R7`, `R7a`, `R7b`, `R11`, `R12a`, `E6`
- Level: integration
- Fixture/setup:
  - canonical skill files under `skills/`
  - generated local skills under `.codex/skills/`
  - public adapters under `dist/adapters/`
- Steps:
  - Run `python scripts/build-skills.py --check`.
  - Run `python scripts/build-adapters.py --version 0.1.1 --check`.
  - Run `python scripts/validate-adapters.py --version 0.1.1`.
  - Run `python scripts/test-adapter-distribution.py`.
  - If check mode reports drift, regenerate from canonical sources and rerun the checks before dynamic benchmarks.
- Expected result:
  - Dynamic benchmarks can only rely on regenerated public Codex skill output.
- Failure proves:
  - Benchmark evidence may measure stale canonical-only or generated output.
- Automation location:
  - `scripts/build-skills.py`
  - `scripts/build-adapters.py`
  - `scripts/validate-adapters.py`
  - `scripts/test-adapter-distribution.py`

### T9. Dynamic benchmarks compare regenerated public Codex skill behavior

- Covers: `R7b`, `R9`, `R9a`-`R9c`, `R12`, `R12a`, `E6`
- Level: e2e, manual
- Fixture/setup:
  - regenerated public Codex adapter skills
  - `benchmarks/token-cost/manifest.yaml`
  - `scripts/run-token-cost-benchmarks.py`
  - baseline `v0.1.1` report
- Steps:
  - Rerun `workflow-route`, `implement-handoff`, `code-review-small`, and `verify-final-pack`, or run the full required core suite when needed for comparable evidence.
  - Confirm the benchmark runner used regenerated public Codex skill output.
  - Record result-quality status for each targeted benchmark.
  - Record largest command output and full-skill read count before and after optimization.
  - Block readiness or record an owner-approved deferral if any targeted result-quality status regresses from `pass` to `fail`.
- Expected result:
  - Runtime behavior is measured against the correct public surface and result quality remains acceptable.
- Failure proves:
  - The optimization cannot claim runtime benefit or safe behavior.
- Automation location:
  - `scripts/run-token-cost-benchmarks.py`
  - `scripts/validate-token-cost-report.py`
  - manual result-quality review

### T10. Optimization comparison report is complete

- Covers: `R4b`, `R8a`-`R8d`, `R9c`, `R10`, `R10a`-`R10e`
- Level: manual, contract
- Fixture/setup:
  - `docs/reports/token-cost/optimizations/2026-05-11-progressive-loading-high-cost-skills.md`
  - baseline `v0.1.1` report
  - static and dynamic evidence from M2-M4
- Steps:
  - Assert the report references the baseline report and names changed skills.
  - Assert it includes static tokens before and after for `workflow`, `implement`, and `code-review`.
  - Assert it includes targeted benchmark results before and after for `workflow-route`, `implement-handoff`, `code-review-small`, and `verify-final-pack`.
  - Assert it includes largest command output before/after, full-skill read count before/after, result-quality status, and remaining warning/high-warning explanations.
  - Assert workflow migration accounting appears in the report or links to the durable owner surface that contains it.
- Expected result:
  - Reviewers have one durable before/after surface for the optimization effect.
- Failure proves:
  - The release review cannot compare cost, safety, and quality impact.
- Automation location:
  - manual report review
  - `git diff --check -- docs/reports/token-cost`

### T11. Public skill wording remains portable and private data stays out

- Covers: `R2c`, `R6a`, `R11`, `R11a`, `R11b`
- Level: integration, manual
- Fixture/setup:
  - updated canonical skills
  - generated public adapter skill output
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert published skill wording does not expose repository-maintainer-only canonical source paths, generated mirror paths, adapter package paths, selector path constraints, drift-check mechanics, shared-block implementation mechanics, or local repository examples.
  - Assert repository-maintainer validation commands and generated-output procedures appear only in internal specs, test specs, plans, contributor docs, or change-local evidence.
  - Manually check public skill text for secrets, credentials, unnecessary machine-local paths, private incident data, and private user data.
- Expected result:
  - Public skills remain project-portable and safe to publish.
- Failure proves:
  - The optimization leaks maintainer-only implementation detail or private data into shipped skills.
- Automation location:
  - `scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - manual public-skill review

### T12. Lifecycle gates and review obligations remain intact

- Covers: `R1b`, `R5`, `R5a`, `R9b`, `R12`, `R12a`
- Level: contract, manual
- Fixture/setup:
  - active plan
  - change-local review artifacts
  - change metadata
  - final diff
- Steps:
  - Assert implementation milestones do not skip code-review, review-resolution when triggered, explain-change, verify, or PR handoff.
  - Assert material findings are recorded and resolved through change-local review artifacts before downstream closeout.
  - Assert `review-resolution.md` is closed only when no open findings remain.
  - Assert final validation includes change metadata, lifecycle, review-artifact closeout, and diff checks.
- Expected result:
  - Token-cost optimization preserves the RigorLoop delivery contract.
- Failure proves:
  - Lower token cost was achieved by weakening reviewability or workflow gates.
- Automation location:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-11-progressive-loading-high-cost-public-skills`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-11-progressive-loading-high-cost-public-skills/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`

## Fixtures and data

- Canonical skill files: `skills/workflow/SKILL.md`, `skills/implement/SKILL.md`, `skills/code-review/SKILL.md`.
- Generated outputs: `.codex/skills/` and `dist/adapters/`.
- Benchmark manifest and prompts: `benchmarks/token-cost/manifest.yaml` and the prompt fixtures for `workflow-route`, `implement-handoff`, `code-review-small`, and `verify-final-pack`.
- Baseline evidence: `docs/reports/token-cost/releases/v0.1.1.yaml` and the current `v0.1.1` Token-Friendliness report.
- Optimization evidence: `docs/reports/token-cost/optimizations/2026-05-11-progressive-loading-high-cost-skills.md`.
- Change-local evidence: `docs/changes/2026-05-11-progressive-loading-high-cost-public-skills/`.

## Mocking/stubbing policy

- Static validator tests may use temporary skill text fixtures for negative cases such as missing quick-guide labels, late quick-guide placement, or missing handoff wording.
- Generated-output checks should use the real generator and adapter validators, not mocked generated trees, when proving final readiness.
- Dynamic benchmark result quality is not mocked for final evidence. If live benchmark execution is unavailable, record the blocker and do not claim dynamic improvement.
- Manual review may summarize benchmark raw output when needed to avoid sensitive local paths, but summaries must preserve failures, result-quality status, largest command output, and full-skill read evidence.

## Migration or compatibility tests

- `T1` proves workflow order, release gates, benchmark schema, and adapter layout do not change.
- `T8` proves generated local and public adapter output remains deterministic derived output.
- `T9` rejects dynamic benchmark evidence that does not use regenerated public Codex skill output.

## Observability verification

- `T7` records static before/after token estimates.
- `T9` records runtime result quality, largest command output, and full-skill read counts.
- `T10` creates the durable optimization comparison report.
- No runtime logs, metrics, traces, or audit events are required.

## Security/privacy verification

- `T11` verifies public skill text does not expose secrets, private data, unnecessary machine-local paths, or maintainer-only implementation details.
- Benchmark evidence may be summarized when raw output would expose sensitive local data, but required review evidence must remain complete enough to evaluate correctness.

## Performance checks

- `T7` checks static token estimates for optimized skills and required justifications.
- `T9` checks dynamic benchmark measurements for the targeted benchmark set.
- Performance targets are warning and evidence targets, not hard token gates.

## Manual QA checklist

- [ ] Quick guides are useful, concise, and safe for common operation.
- [ ] `implement` handoff guidance cannot reasonably encourage broad milestone-state discovery before active-plan inspection.
- [ ] Workflow migration table has no unowned safety topic.
- [ ] `code-review` still contains the protected review contracts.
- [ ] Dynamic benchmark evidence names regenerated public Codex skill output.
- [ ] Optimization report explains every remaining warning or high-warning.

## What not to test

- Do not add a `skill section read` analyzer signal in this slice; that is a follow-up after stable sections exist.
- Do not enforce hard token-size gates; static targets require evidence and justification, not absolute blocking by size alone.
- Do not test every public skill for quick-guide adoption; this slice covers only `workflow`, `implement`, and `code-review`.
- Do not split or test external `code-review` template reference files in this slice.
- Do not automate subjective prose quality scoring beyond stable headings, labels, phrases, and manual review checklists.

## Uncovered gaps

None. Dynamic benchmark availability remains an execution risk, but the spec already defines the required blocker behavior if benchmarks cannot run.

## Next artifacts

- implement M1
- code-review for M1
- review-resolution if triggered

## Follow-on artifacts

None yet.

## Readiness

Active proof surface for M1 proof and execution. The active plan owns the live next-stage handoff.
