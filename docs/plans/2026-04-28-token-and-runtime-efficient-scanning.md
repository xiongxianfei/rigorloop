# Token and Runtime Efficient Scanning Execution Plan

- Status: done
- Owner: maintainers
- Start date: 2026-04-28
- Last updated: 2026-04-28
- Related issue or PR: none yet
- Supersedes: none

## Goal

Implement the approved token and runtime efficient scanning contract in small, reviewable slices while preserving validation semantics, generated-output correctness, and contributor-visible traceability.

## Why now

The accepted proposal and approved spec define the first slice: guidance updates, one named script output-shaping improvement, manifest-first generated-output inspection, and explicit full-file-read escalation guidance for scan-sensitive skills. Planning is needed before `test-spec` and implementation because the work touches workflow documentation, canonical skills, generated surfaces, and adapter drift checking.

## Source artifacts

- Proposal: [Token and Runtime Efficient Scanning](../proposals/2026-04-27-token-and-runtime-efficient-scanning.md)
- Spec: [Token and Runtime Efficient Scanning](../../specs/token-and-runtime-efficient-scanning.md)
- Architecture: not required for the first slice because the approved behavior does not introduce a persistent cache, service, database, new dependency, or cross-validation-family parser boundary. Revisit architecture if implementation expands shared parsing beyond the adapter drift script family.
- Test spec: [Token and Runtime Efficient Scanning test spec](../../specs/token-and-runtime-efficient-scanning.test.md)
- Relevant workflow guidance: [docs/workflows.md](../workflows.md)

## Scope

### In scope

- Add bounded extraction, output budget, verbose expansion, and full-file-read escalation guidance to contributor-visible workflow documentation.
- Update every first-slice scan-sensitive canonical skill named by the spec to prefer summary or stable ID based reasoning and to state when full-file reads are required.
- Refresh generated `.codex/skills/` and public adapter package output only through existing generation commands after canonical skill edits.
- Shape normal output for `python scripts/build-adapters.py --version <version> --check`.
- Add `python scripts/build-adapters.py --version <version> --check --verbose`.
- Classify every adapter drift failure entry as `missing`, `stale`, `unexpected`, `canonical-source-error`, or `manifest-error`.
- Read `dist/adapters/manifest.yaml` first for adapter generated-output coverage inspection, then confirm required filesystem state.
- Reuse or add only in-process helpers needed by the adapter drift script family.
- Record before-and-after output line or byte counts for representative clean and drift cases.

### Out of scope

- Weakening validation, review gates, lifecycle traceability, selected check coverage, or command exit behavior.
- Replacing full-file reads when a full contract review requires them.
- Adding a persistent cache, long-running indexing service, database, external dependency, or cross-command cache.
- Rewriting unrelated validators or generators solely for performance.
- Changing hosted CI behavior except through existing repository-owned commands.
- Making output budgets hard correctness failures.

## Context and orientation

- `docs/workflows.md` is the contributor-facing operational surface for evidence collection and validation-output guidance.
- Canonical skills live under `skills/`; generated Codex runtime skills under `.codex/skills/` and public adapter packages under `dist/adapters/` must not be hand-edited.
- The first-slice scan-sensitive canonical skills are `architecture`, `architecture-review`, `bugfix`, `ci`, `code-review`, `explain-change`, `implement`, `plan`, `plan-review`, `pr`, `project-map`, `proposal`, `proposal-review`, `research`, `spec`, `spec-review`, `test-spec`, `verify`, and `workflow`.
- `scripts/build-adapters.py` is the CLI entrypoint for syncing and checking generated adapter output.
- `scripts/adapter_distribution.py` currently computes expected adapter files, reads existing generated files, validates canonical skill sources, parses adapter manifests, and returns drift as plain strings.
- `scripts/test-adapter-distribution.py` is the primary test surface for adapter generation, drift, manifest parsing, release verification, and generated-output validation behavior.
- `scripts/validation_selection.py` owns the `adapters.drift` selected-check command that currently calls `python scripts/build-adapters.py --version <adapter-version> --check`.
- Existing manifest parsing helpers should be reused before new parser code is added. Any new helper introduced by this plan must stay in-process and scoped to the selected script family unless a later architecture artifact approves a broader boundary.

## Constraints

- Preserve current pass/fail semantics and exit behavior for clean checks, drift failures, and invalid inputs.
- Keep normal-mode output summary-first, failure-focused, diff-focused where applicable, and expandable with `--verbose`.
- Target no more than 40 routine normal-mode lines and warn if unavoidable output exceeds 80 lines.
- Avoid large excerpts and repeated path lists by default.
- Keep complete diagnostic detail available through verbose mode.
- Do not add external dependencies.
- Do not hand-edit generated `.codex/skills/` or `dist/adapters/` output.

## Validation command types

This plan uses two validation command types:

- Pass-gate commands are expected to succeed as written and are required for milestone completion.
- Selector inspection / manual-routing proofs are used to prove selector behavior for unsupported or intentionally unclassified paths. A blocked selector result is expected and does not fail the milestone when the plan records the direct manual route that will be used instead.

## Requirements covered

- M1 covers R1-R6, R10-R15, R34-R36, EC8, EC9, EC12, AC1, and AC2.
- M2 covers R7-R18, R19-R19c for generated-output and canonical-source entries, R20-R23 for non-manifest drift output, R24-R26 for non-manifest collected entries, R30-R33, R37, EC1-EC4, EC10, EC11, EC13, AC3-AC5, AC7-AC9, and generated-output plus canonical-source portions of AC10. M2 does not claim manifest-error coverage.
- M3 covers manifest-first collection and manifest-error behavior: R19a, R19d, R22, R24, R27-R33, R37, EC5-EC7, EC14, AC6, AC8, AC9, and the manifest-error portion of AC10.
- M4 covers R14, R20, R25, R34-R37, EC11, EC12, and AC11 through generated-output, selector, artifact-lifecycle, and broad-smoke validation.

## Milestones

### M1. Add bounded extraction and skill guidance

- Goal: Update authoritative workflow guidance and first-slice scan-sensitive skills so contributors and agents default to bounded extraction, stable IDs, concise summaries, and explicit full-file-read escalation rules.
- Requirements: R1-R6, R10-R15, R34-R36, EC8, EC9, EC12, AC1, AC2.
- Files/components likely touched: `docs/workflows.md`; the first-slice canonical `skills/*/SKILL.md` files named in the spec; generated `.codex/skills/`; generated `dist/adapters/`; possibly `AGENTS.md` only if a concise pointer is needed after reviewing the workflow guidance.
- Dependencies: approved spec; no architecture required unless guidance introduces a new parser or cache boundary.
- Tests to add/update: skill validator expectations if existing rules need to recognize the new required guidance; generated skill and adapter drift checks.
- Implementation steps:
  - Add a bounded extraction section to `docs/workflows.md` covering inventories, stable IDs, line-number searches, exact ranges, output budgets, verbose escape hatches, and full-file-read escalation.
  - Update each named canonical skill with summary or ID based reasoning guidance and a short "when full-file read is required" rule.
  - Keep skill wording concise and stage-local; do not add unrelated workflow order changes.
  - Run existing generators to refresh `.codex/skills/` and `dist/adapters/` after canonical skill edits.
  - Record any intentionally unchanged governance surface with rationale in this plan or change-local artifacts.
- Validation commands:
  - Pass-gate commands:
    - `python scripts/validate-skills.py`
    - `python scripts/test-skill-validator.py`
    - `python scripts/test-select-validation.py`
    - `python scripts/build-skills.py --check`
    - `python scripts/build-adapters.py --version 0.1.1 --check`
    - `python scripts/validate-adapters.py --version 0.1.1`
- Expected observable result: workflow and skill guidance direct bounded extraction first, name full-file-read escalation conditions, and generated skill/adapter outputs are synchronized through repository-owned generators.
- Commit message: `M1: add bounded extraction guidance`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks: repeated wording across skills could drift or become too broad.
- Rollback/recovery: revert canonical guidance edits and regenerate derived outputs.

### M2. Shape adapter drift check output

- Goal: Implement normal and verbose output for `build-adapters.py --check` without changing adapter drift semantics or exit codes.
- Requirements: R7-R18, R19-R19c for generated-output and canonical-source entries, R20-R23 for non-manifest drift output, R24-R26 for non-manifest collected entries, R30-R33, R37, EC1-EC4, EC10, EC11, EC13, AC3-AC5, AC7-AC9, and generated-output plus canonical-source portions of AC10. Manifest-error collection, validation, and regression tests are owned by M3 unless manifest-first collection is implemented in this milestone.
- Files/components likely touched: `scripts/build-adapters.py`, `scripts/adapter_distribution.py`, `scripts/test-adapter-distribution.py`, and any selector or release tests that assert command text.
- Dependencies: M1 may run independently, but M2 must preserve the existing `adapters.drift` command identity used by validation selection.
- Tests to add/update:
  - clean check normal output includes `adapters.drift`, requested version, output root, concise success status, and no unchanged file list;
  - drift normal output includes category counts, displayed failure category, affected path, actionable detail, and verbose rerun instruction when failures are omitted;
  - verbose check output includes every collected generated-output and canonical-source failure entry deterministically;
  - success, drift failure, and invalid input exit codes remain equivalent to pre-output-shaping behavior;
  - generated-output failures are categorized as `missing`, `stale`, or `unexpected`;
  - canonical-source failures are categorized as `canonical-source-error`;
  - output line or byte count evidence exists for representative clean and drift cases.
- Implementation steps:
  - Add a structured in-process adapter drift entry representation with category, affected path, and detail while preserving or bridging existing string-based helpers where that keeps tests and callers stable.
  - Add a formatter for normal output that starts with `adapters.drift`, version, output root, status, and category counts before displayed failure records.
  - Bound displayed normal failure records so routine output targets 40 lines and emits an over-budget warning if unavoidable output exceeds 80 lines.
  - Add a verbose formatter that renders every collected failure entry from the same drift collection result.
  - Add `--verbose` to `build-adapters.py` for `--check`; reject or clearly fail `--verbose` without `--check` if it has no meaningful behavior.
  - Add test evidence that computes or records the legacy one-line-per-entry baseline and the new shaped normal output size for clean and drift examples.
- Validation commands:
  - Pass-gate commands:
    - `python scripts/test-adapter-distribution.py`
    - `python scripts/build-adapters.py --version 0.1.1 --check`
    - `python scripts/build-adapters.py --version 0.1.1 --check --verbose`
    - `python scripts/validate-adapters.py --version 0.1.1`
    - `python scripts/test-select-validation.py` if `scripts/validation_selection.py` changes
  - Selector inspection proof:
    - `python scripts/select-validation.py --mode explicit --path scripts/build-adapters.py --path scripts/adapter_distribution.py --path scripts/test-adapter-distribution.py --path scripts/validation_selection.py`
    - Expected selector result: `scripts/test-adapter-distribution.py` routes through the adapter check family; unsupported or intentionally unclassified script paths still require manual-routing proof.
- Expected observable result: normal adapter drift checks are concise and failure-focused; verbose checks expose full diagnostic detail; exit behavior and selected-check identity remain unchanged.
- Commit message: `M2: shape adapter drift output`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks: summarization could hide the actionable failure, or internal return-type changes could break callers.
- Rollback/recovery: keep the structured collector separable from validation logic so the CLI formatter can be reverted to the prior one-entry-per-line output without changing drift detection.

### M3. Add manifest-first adapter inspection

- Goal: Make adapter generated-output coverage inspection read `dist/adapters/manifest.yaml` first when available, then use canonical sources and filesystem checks to prove missing, stale, unexpected, or drifted files.
- Requirements: R19a, R19d, R22, R24, R27-R33, R37, EC5-EC7, EC14, AC6, AC8, AC9, and the manifest-error portion of AC10.
- Files/components likely touched: `scripts/adapter_distribution.py`, `scripts/test-adapter-distribution.py`, and generated adapter validation tests if manifest consistency assertions need to move earlier.
- Dependencies: M2 structured drift entries should exist so manifest errors can be categorized and formatted consistently.
- Tests to add/update:
  - manifest is parsed before filesystem coverage confirmation when it exists;
  - malformed, missing, inconsistent, or contract-mismatched manifest conditions produce `manifest-error`;
  - normal output for manifest failures includes `manifest-error`, affected manifest path, and actionable detail;
  - verbose output includes complete manifest failure entries deterministically;
  - manifest evidence does not replace canonical source and filesystem drift checks;
  - missing, stale, and unexpected generated-output categories still apply to non-manifest generated files.
- Implementation steps:
  - Reuse existing `parse_manifest_yaml` for manifest reads.
  - Add a small helper for reading and validating generated adapter manifest inventory before broad filesystem traversal where coverage inspection needs the manifest.
  - Continue building expected files from canonical skills, templates, and generator code.
  - Continue confirming generated-output state against the filesystem after manifest inspection.
  - Keep all helper state in process and discard it after the command invocation.
- Validation commands:
  - Pass-gate commands:
    - `python scripts/test-adapter-distribution.py`
    - `python scripts/build-adapters.py --version 0.1.1 --check`
    - `python scripts/build-adapters.py --version 0.1.1 --check --verbose`
    - `python scripts/validate-adapters.py --version 0.1.1`
- Expected observable result: adapter coverage checks use manifest inventory first without making the manifest authoritative over canonical sources or filesystem proof.
- Commit message: `M3: inspect adapter manifest before filesystem confirmation`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks: treating manifest mismatch as drift could double-report failures or mask stale generated files.
- Rollback/recovery: isolate manifest-first inventory as a pre-check that can be disabled while preserving canonical expected-file and filesystem comparison behavior.

### M4. Align generated output, lifecycle artifacts, and final validation

- Goal: Close the implementation slice with generated outputs synchronized, change-local evidence recorded, lifecycle artifacts consistent, and repository validation run through the approved proof path.
- Requirements: R14, R20, R25, R34-R37, EC11, EC12, AC5, AC9, AC11.
- Files/components likely touched: `docs/changes/token-and-runtime-efficient-scanning/change.yaml`, `docs/changes/token-and-runtime-efficient-scanning/explain-change.md`, this plan, `docs/plan.md`, generated `.codex/skills/`, generated `dist/adapters/`, and any release metadata validation references affected by generated adapter output.
- Dependencies: M1-M3 complete; `test-spec` active before implementation starts.
- Tests to add/update: no new behavior tests unless final validation exposes gaps; update test spec traceability if implementation changes the planned test names.
- Implementation steps:
  - Regenerate derived skills and public adapter output from canonical sources.
  - Record before-and-after output-size evidence and validation results in the plan validation notes or change-local artifacts.
  - Use selector-selected explicit validation for touched paths before broad smoke.
  - Run structural checks required for skills, adapters, release metadata, and artifact lifecycle.
  - Run broad smoke before final PR readiness because the completed implementation will span workflow guidance, canonical skills, generated adapters, and repository-owned validation behavior.
  - Update `docs/plan.md` and this plan body together when the initiative lifecycle state changes.
- Validation commands:
  - Pass-gate commands:
    - `python scripts/validate-skills.py`
    - `python scripts/test-skill-validator.py`
    - `python scripts/test-select-validation.py`
    - `python scripts/build-skills.py --check`
    - `python scripts/test-adapter-distribution.py`
    - `python scripts/build-adapters.py --version 0.1.1 --check`
    - `python scripts/build-adapters.py --version 0.1.1 --check --verbose`
    - `python scripts/validate-adapters.py --version 0.1.1`
    - `python scripts/validate-release.py --version v0.1.1`
    - `python scripts/test-artifact-lifecycle-validator.py`
    - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-27-token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.test.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/plan.md`
    - `bash scripts/ci.sh --mode broad-smoke`
  - Selector inspection proof:
    - `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path skills/architecture/SKILL.md --path skills/architecture-review/SKILL.md --path skills/bugfix/SKILL.md --path skills/ci/SKILL.md --path skills/code-review/SKILL.md --path skills/explain-change/SKILL.md --path skills/implement/SKILL.md --path skills/plan/SKILL.md --path skills/plan-review/SKILL.md --path skills/pr/SKILL.md --path skills/project-map/SKILL.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path skills/research/SKILL.md --path skills/spec/SKILL.md --path skills/spec-review/SKILL.md --path skills/test-spec/SKILL.md --path skills/verify/SKILL.md --path skills/workflow/SKILL.md --path scripts/build-adapters.py --path scripts/adapter_distribution.py --path scripts/test-adapter-distribution.py --path specs/token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.test.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/plan.md`
    - Expected selector result: `scripts/test-adapter-distribution.py` routes through the adapter check family; unsupported or intentionally unclassified paths still require manual-routing proof. Do not pass directory path `skills`; pass each changed canonical `skills/<name>/SKILL.md` path explicitly.
- Expected observable result: generated outputs are synchronized, lifecycle artifacts are consistent, and validation evidence supports handoff to `code-review`, `verify`, `explain-change`, and `pr`.
- Commit message: `M4: validate token efficient scanning slice`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks: broad validation may expose unrelated baseline debt.
- Rollback/recovery: keep unrelated debt separate; if generated drift appears, rerun the generator from canonical sources or revert the canonical edit that caused the drift.

## Validation plan

- Before implementation, run artifact lifecycle validation for the accepted proposal, approved spec, this plan, and `docs/plan.md`.
- After `plan-review`, create a test spec that maps every spec MUST and acceptance criterion to concrete tests or validation evidence before editing production behavior.
- For each milestone, run the validation commands named in that milestone before advancing.
- Treat pass-gate commands as required milestone completion gates.
- Treat selector inspection / manual-routing proofs as evidence about selector behavior; a blocked selector result is acceptable only when it matches the expected unsupported path and the direct manual pass-gate command is recorded.
- Use selector-selected explicit validation for supported touched paths before final broad smoke, and use direct pass-gate commands for unsupported or intentionally manual-routed paths.
- Run broad smoke before final PR readiness because the completed implementation will span workflow guidance, canonical skills, generated adapters, and repository-owned validation behavior.
- Record all commands actually run in this plan's validation notes or change-local artifacts.

## Risks and recovery

- Concise output could hide actionable failures. Mitigation: normal output must include check ID, category, affected path, counts, actionable detail for displayed failures, omitted counts, and a verbose rerun path.
- Output shaping could accidentally alter pass/fail behavior. Mitigation: tests must cover exit-code equivalence and selector wrapper behavior.
- Manifest-first inspection could imply that the manifest is authoritative. Mitigation: keep canonical source generation and filesystem confirmation in the drift proof path.
- Updating many skills could introduce inconsistent wording. Mitigation: use one concise reusable rule shape and validate canonical/generated skill surfaces.
- New helpers could expand into an unreviewed parser boundary. Mitigation: keep helpers in-process and adapter-family scoped; require architecture before broadening.
- Generated outputs could be hand-edited by mistake. Mitigation: use generators only and prove with build/check commands.
- Broad smoke may surface unrelated baseline failures. Mitigation: record unrelated debt separately and do not claim it as caused or fixed by this initiative without evidence.

## Dependencies

- The proposal is accepted and the spec is approved.
- `plan-review` must pass before `test-spec`.
- `test-spec` must be active before implementation.
- Architecture remains unnecessary unless implementation introduces a persistent cache, new external dependency, service, database, or cross-validation-family parser boundary.
- Generated output refresh depends on existing `build-skills.py` and `build-adapters.py` commands.
- Final PR readiness depends on completed `code-review`, `verify`, and downstream lifecycle stages.

## Progress

- [x] 2026-04-28: plan created from approved proposal and spec.
- [x] 2026-04-28: plan revised after `plan-review` findings to distinguish validation command types and move manifest-error ownership to M3.
- [x] 2026-04-28: `plan-review` approved the concrete execution sequence.
- [x] 2026-04-28: `specs/token-and-runtime-efficient-scanning.test.md` created and activated.
- [x] 2026-04-28: M1 completed bounded extraction workflow guidance, first-slice scan-sensitive skill guidance, generated skill and adapter refresh, change-local baseline pack, and targeted validation.
- [x] 2026-04-28: M2 completed structured adapter drift entries, summary-first normal output, complete verbose output, output-size evidence, and targeted adapter validation without implementing manifest-first collection.
- [x] 2026-04-28: M3 completed manifest-first adapter drift inspection, `manifest-error` entries for missing/malformed/inconsistent/mismatched manifests, and filesystem confirmation after manifest inspection.
- [x] 2026-04-28: M4 completed generated-output regeneration, selector/manual-route proof, release validation, artifact-lifecycle validation, and broad-smoke validation.
- [x] 2026-04-28: first-pass `code-review` returned `clean-with-notes` with no blocking or required-change findings and recommended `verify` as the next stage.
- [x] 2026-04-28: post-review lifecycle bookkeeping synchronized the spec, test spec, active plan, plan index, and change-local pack so tracked readiness points to `verify`.
- [x] 2026-04-28: `verify` passed with verdict `ready`; branch-ready is satisfied, and the next stage is `explain-change`.
- [x] 2026-04-28: `explain-change` completed the durable problem-to-diff rationale and PR handoff summary.
- [x] 2026-04-28: PR handoff prepared. Lifecycle state is closed in this plan body and `docs/plan.md`.
- [x] Final lifecycle closeout completed in both this plan and `docs/plan.md`.

## Decision log

- 2026-04-28: Use `python scripts/build-adapters.py --version <version> --check` as the named first output-shaped script because the approved spec identifies it and the current CLI prints one line per drift entry.
- 2026-04-28: No separate architecture artifact is required for the first slice because helper work stays in-process, adapter-family scoped, dependency-free, and non-persistent.
- 2026-04-28: Keep generated outputs as derived surfaces and refresh them only through `build-skills.py` and `build-adapters.py`.
- 2026-04-28: Include broad smoke in final validation because the planned work spans workflow guidance, canonical skills, generated adapters, and repository-owned validation behavior.
- 2026-04-28: M2 owns generated-output failure categories and `canonical-source-error`; M3 owns manifest-first collection and therefore `manifest-error` collection, validation, and regression tests.
- 2026-04-28: M1 left `AGENTS.md`, `CONSTITUTION.md`, `specs/rigorloop-workflow.md`, and adapter drift logic unchanged with rationale recorded in `docs/changes/token-and-runtime-efficient-scanning/explain-change.md`.
- 2026-04-28: M2 preserves `collect_adapter_drift` as the string-returning compatibility API and adds `collect_adapter_drift_entries` for structured formatter and category tests.
- 2026-04-28: M2 keeps `manifest-error` as a reserved category in formatter counts so the full taxonomy is visible, but actual manifest-first collection and manifest-error regression coverage remain M3 work.
- 2026-04-28: M3 uses a scoped in-process manifest inspection helper in the adapter drift family instead of a persistent cache or cross-command parser boundary.
- 2026-04-28: M3 reports manifest contract failures as `manifest-error` entries and skips a duplicate ordinary `missing` or `stale` entry for `manifest.yaml`; non-manifest generated files still use `missing`, `stale`, and `unexpected`.
- 2026-04-28: M4 leaves the initiative active in `docs/plan.md` until downstream `code-review` and `verify` complete; the implementation state is ready for `code-review`, not PR-ready.
- 2026-04-28: After clean first-pass `code-review`, keep the initiative active until `verify` and downstream explanation/PR handoff complete; the implementation state is ready for `verify`, not PR-ready.
- 2026-04-28: After `verify`, keep the initiative active until `explain-change` and PR handoff complete; the branch is `branch-ready`, while `pr-body-ready` and `pr-open-ready` remain owned by later stages.
- 2026-04-28: After direct `explain-change`, stop before `pr` while marking the explanation and PR handoff rationale complete; PR body readiness and PR opening remain owned by the `pr` stage.
- 2026-04-28: During `pr`, close the plan as done before opening the pull request because M1-M4, code-review, verify, explain-change, and PR handoff readiness are complete before merge.

## Surprises and discoveries

- 2026-04-28: M4 broad smoke passed while reporting unrelated baseline warnings for older draft proposal files; those warnings are outside this change and did not block the related artifact lifecycle validation.

## Validation notes

- 2026-04-28: `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-04-27-token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/plan.md` selected `artifact_lifecycle.validate` only; broad smoke was not required for this planning-only change.
- 2026-04-28: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-27-token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/plan.md` passed, reporting `validated 2 artifact files in explicit-paths mode`.
- 2026-04-28: before the PR-stage selector repair, `python scripts/select-validation.py --mode explicit --path scripts/build-adapters.py --path scripts/adapter_distribution.py --path scripts/test-adapter-distribution.py --path scripts/validation_selection.py` blocked only on `scripts/test-adapter-distribution.py` as `manual-routing-required`; the plan recorded `python scripts/test-adapter-distribution.py` as the manual pass-gate route.
- 2026-04-28: before the PR-stage selector repair, the M4 selector inspection with concrete `skills/<name>/SKILL.md` paths had no unclassified `skills` directory path and blocked only on `scripts/test-adapter-distribution.py` as `manual-routing-required`; the plan recorded the direct manual route.
- 2026-04-28: after plan-review revision, `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-04-27-token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/plan.md` selected `artifact_lifecycle.validate` only.
- 2026-04-28: after plan-review revision, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-27-token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/plan.md` passed, reporting `validated 2 artifact files in explicit-paths mode`.
- 2026-04-28: after test-spec activation, `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-04-27-token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.test.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/plan.md` selected `artifact_lifecycle.validate` only; broad smoke was not required for this artifact-only change.
- 2026-04-28: after test-spec activation, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-27-token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.test.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/plan.md` passed, reporting `validated 3 artifact files in explicit-paths mode`.
- 2026-04-28: M1 TDD proof: `python scripts/test-skill-validator.py` failed before implementation with expected failures for missing bounded extraction workflow terms and missing summary/stable-ID plus full-file-read guidance in the 19 first-slice scan-sensitive skills.
- 2026-04-28: M1 generation commands passed: `python scripts/build-skills.py` and `python scripts/build-adapters.py --version 0.1.1`.
- 2026-04-28: M1 pass-gate commands passed: `python scripts/validate-skills.py`; `python scripts/test-skill-validator.py`; `python scripts/test-select-validation.py`; `python scripts/build-skills.py --check`; `python scripts/build-adapters.py --version 0.1.1 --check`; `python scripts/validate-adapters.py --version 0.1.1`.
- 2026-04-28: M1 change metadata passed: `python scripts/validate-change-metadata.py docs/changes/token-and-runtime-efficient-scanning/change.yaml`.
- 2026-04-28: M1 selector inspection passed for `docs/workflows.md`, `scripts/test-skill-validator.py`, the 19 concrete `skills/<name>/SKILL.md` paths, the change-local pack, and lifecycle artifacts. It selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.drift`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`; broad smoke was not required and there were no blocking results.
- 2026-04-28: M1 explicit CI wrapper passed for the same authored path set, executing the selected checks listed above.
- 2026-04-28: after M1 plan and change-local updates, `python scripts/validate-change-metadata.py docs/changes/token-and-runtime-efficient-scanning/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/token-and-runtime-efficient-scanning/change.yaml --path docs/changes/token-and-runtime-efficient-scanning/explain-change.md --path docs/plan.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/proposals/2026-04-27-token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.test.md`, and `git diff --check -- .` passed.
- 2026-04-28: M2 TDD proof: `python scripts/test-adapter-distribution.py` failed before implementation because the new tests imported missing structured drift entry and formatter helpers.
- 2026-04-28: M2 adapter regression passed: `python scripts/test-adapter-distribution.py` ran 54 tests successfully after implementing structured drift entries, normal and verbose formatters, no-cache proof, output-size evidence, and CLI compatibility coverage.
- 2026-04-28: M2 pass-gate commands passed: `python scripts/build-adapters.py --version 0.1.1 --check`; `python scripts/build-adapters.py --version 0.1.1 --check --verbose`; `python scripts/validate-adapters.py --version 0.1.1`; `python scripts/test-select-validation.py`.
- 2026-04-28: M2 invalid verbose boundary proof passed: `python scripts/build-adapters.py --version 0.1.1 --verbose` failed as expected with exit code 2 and `--verbose is only supported with --check`.
- 2026-04-28: M2 selector inspection `python scripts/select-validation.py --mode explicit --path scripts/build-adapters.py --path scripts/adapter_distribution.py --path scripts/test-adapter-distribution.py --path scripts/validation_selection.py` originally returned a blocked/manual-routing result for `scripts/test-adapter-distribution.py`, selected `adapters.regression`, `adapters.drift`, `adapters.validate`, and `selector.regression`, and did not require broad smoke. The manual route `python scripts/test-adapter-distribution.py` passed.
- 2026-04-28: M2 output-size evidence recorded representative clean normal output as legacy 1 line and shaped 4 lines, and representative many-drift normal output as legacy 35 lines and shaped 26 lines.
- 2026-04-28: after M2 plan and change-local updates, `python scripts/validate-change-metadata.py docs/changes/token-and-runtime-efficient-scanning/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/token-and-runtime-efficient-scanning/change.yaml --path docs/changes/token-and-runtime-efficient-scanning/explain-change.md --path docs/plan.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/proposals/2026-04-27-token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.test.md`, and `git diff --check -- .` passed.
- 2026-04-28: M3 TDD proof: `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_adapter_drift_entries_classify_generated_output_failures AdapterDistributionTests.test_manifest_first_inspection_precedes_filesystem_confirmation AdapterDistributionTests.test_manifest_errors_are_structured_and_displayed_completely` failed before implementation because the manifest-first helper and `manifest-error` drift entries were not implemented.
- 2026-04-28: M3 narrow tests passed after implementation for generated-output failure classification, manifest-before-filesystem call order, and manifest-error normal/verbose output.
- 2026-04-28: M3 adapter regression passed: `python scripts/test-adapter-distribution.py` ran 56 tests successfully.
- 2026-04-28: M3 pass-gate commands passed: `python scripts/build-adapters.py --version 0.1.1 --check`; `python scripts/build-adapters.py --version 0.1.1 --check --verbose`; `python scripts/validate-adapters.py --version 0.1.1`.
- 2026-04-28: M3 selector inspection `python scripts/select-validation.py --mode explicit --path scripts/adapter_distribution.py --path scripts/test-adapter-distribution.py --path docs/changes/token-and-runtime-efficient-scanning/change.yaml --path docs/changes/token-and-runtime-efficient-scanning/explain-change.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md` originally returned a blocked/manual-routing result for `scripts/test-adapter-distribution.py`, selected `adapters.regression`, `adapters.drift`, `adapters.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`, and did not require broad smoke. The direct manual route `python scripts/test-adapter-distribution.py` passed.
- 2026-04-28: M3 selected support checks passed: `python scripts/test-select-validation.py`; `python scripts/test-change-metadata-validator.py`; `python scripts/validate-change-metadata.py docs/changes/token-and-runtime-efficient-scanning/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/token-and-runtime-efficient-scanning/change.yaml --path docs/changes/token-and-runtime-efficient-scanning/explain-change.md --path docs/plan.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/proposals/2026-04-27-token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.test.md`; `git diff --check -- .`.
- 2026-04-28: M4 regenerated derived outputs with `python scripts/build-skills.py` and `python scripts/build-adapters.py --version 0.1.1`; no generated diff remained.
- 2026-04-28: M4 selector inspection `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path skills/architecture/SKILL.md --path skills/architecture-review/SKILL.md --path skills/bugfix/SKILL.md --path skills/ci/SKILL.md --path skills/code-review/SKILL.md --path skills/explain-change/SKILL.md --path skills/implement/SKILL.md --path skills/plan/SKILL.md --path skills/plan-review/SKILL.md --path skills/pr/SKILL.md --path skills/project-map/SKILL.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path skills/research/SKILL.md --path skills/spec/SKILL.md --path skills/spec-review/SKILL.md --path skills/test-spec/SKILL.md --path skills/verify/SKILL.md --path skills/workflow/SKILL.md --path scripts/build-adapters.py --path scripts/adapter_distribution.py --path scripts/test-adapter-distribution.py --path specs/token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.test.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/plan.md` originally returned a blocked/manual-routing result for `scripts/test-adapter-distribution.py`, selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `artifact_lifecycle.validate`, and `selector.regression`, and did not require broad smoke. The direct manual route is the M4 pass-gate `python scripts/test-adapter-distribution.py`.
- 2026-04-28: M4 supported explicit CI originally passed with `bash scripts/ci.sh --mode explicit` on the same concrete path set minus `scripts/test-adapter-distribution.py`, executing `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `artifact_lifecycle.validate`, and `selector.regression`.
- 2026-04-28: M4 remaining pass gates passed: `python scripts/build-adapters.py --version 0.1.1 --check --verbose`; `python scripts/validate-release.py --version v0.1.1`; `python scripts/test-artifact-lifecycle-validator.py`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-27-token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.test.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/plan.md`.
- 2026-04-28: M4 broad smoke passed: `bash scripts/ci.sh --mode broad-smoke`.
- 2026-04-28: after M4 artifact updates, `bash scripts/ci.sh --mode explicit --path docs/changes/token-and-runtime-efficient-scanning/change.yaml --path docs/changes/token-and-runtime-efficient-scanning/explain-change.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/plan.md` passed, selecting `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`; `git diff --check -- .` passed.
- 2026-04-28: first-pass `code-review` record for `c929147..618c4f5`.
  - Review status: `clean-with-notes`
  - Findings: no blocking or required-change findings.
  - Checklist coverage: pass for spec alignment, test coverage, edge cases, error handling, architecture boundaries, compatibility, security/privacy, generated output drift, unrelated changes, and validation evidence.
  - Residual risks: final `verify`, downstream explanation/PR handoff, and lifecycle closeout remained pending; broad-smoke warnings were unrelated baseline warnings for older draft proposal files.
  - Recommended next stage: `verify`
- 2026-04-28: post-code-review lifecycle sync updated tracked readiness and validated with:
  - `python scripts/select-validation.py --mode explicit --path docs/changes/token-and-runtime-efficient-scanning/change.yaml --path docs/changes/token-and-runtime-efficient-scanning/explain-change.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/plan.md --path specs/token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.test.md`
  - `bash scripts/ci.sh --mode explicit --path docs/changes/token-and-runtime-efficient-scanning/change.yaml --path docs/changes/token-and-runtime-efficient-scanning/explain-change.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/plan.md --path specs/token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.test.md`
  - `python scripts/validate-change-metadata.py docs/changes/token-and-runtime-efficient-scanning/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/token-and-runtime-efficient-scanning/change.yaml --path docs/changes/token-and-runtime-efficient-scanning/explain-change.md --path docs/plan.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/proposals/2026-04-27-token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.test.md`
  - `git diff --check -- .`
  - Result: passed.
- 2026-04-28: `verify` passed on the complete implementation plus post-review lifecycle bookkeeping.
  - Verification verdict: `ready`
  - Traceability:
    - `R1`-`R6`, `R34`, `R35` -> `T1`, `T2`, `T16` -> `docs/workflows.md`, canonical `skills/`, generated `.codex/skills/`, public adapter packages -> workflow guidance, skill guidance, skill validation, and generated-output drift checks -> pass
    - `R7`-`R15`, `R21`-`R26` -> `T4`, `T5`, `T6`, `T8`, `T9`, `T12` -> `scripts/build-adapters.py`, `scripts/adapter_distribution.py`, `scripts/test-adapter-distribution.py` -> summary-first normal output, bounded failure output, complete verbose output, and output-size evidence -> pass
    - `R16`-`R20`, `R19a`-`R19d` -> `T4`, `T7`, `T10`, `T12`, `T14`, `T16` -> adapter drift entry collection, CLI check mode, and selector/CI proof -> command identity, exit-code compatibility, and failure taxonomy -> pass
    - `R27`-`R33` -> `T11`, `T12`, `T13` -> manifest-first adapter inspection helpers and adapter tests -> manifest-before-filesystem behavior, filesystem confirmation, no persistent cache, and no new dependency -> pass
    - `R36`, `R37`, `AC1`-`AC11` -> `T3`, `T13`, `T15`, `T16` -> generated skills/adapters, release metadata, lifecycle artifacts, and broad smoke -> generated-output alignment, release validation, privacy boundary, and lifecycle validation -> pass
  - Validation commands:
    - `python scripts/validate-skills.py`
    - `python scripts/test-skill-validator.py`
    - `python scripts/test-adapter-distribution.py`
    - `python scripts/build-skills.py --check`
    - `python scripts/build-adapters.py --version 0.1.1 --check`
    - `python scripts/build-adapters.py --version 0.1.1 --check --verbose`
    - `python scripts/validate-adapters.py --version 0.1.1`
    - `python scripts/validate-release.py --version v0.1.1`
    - `python scripts/test-select-validation.py`
    - `python scripts/test-change-metadata-validator.py`
    - `python scripts/test-artifact-lifecycle-validator.py`
    - `python scripts/select-validation.py --mode explicit --path docs/changes/token-and-runtime-efficient-scanning/change.yaml --path docs/changes/token-and-runtime-efficient-scanning/explain-change.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/plan.md --path specs/token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.test.md`
    - `bash scripts/ci.sh --mode explicit --path docs/changes/token-and-runtime-efficient-scanning/change.yaml --path docs/changes/token-and-runtime-efficient-scanning/explain-change.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/plan.md --path specs/token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.test.md`
    - `python scripts/validate-change-metadata.py docs/changes/token-and-runtime-efficient-scanning/change.yaml`
    - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/token-and-runtime-efficient-scanning/change.yaml --path docs/changes/token-and-runtime-efficient-scanning/explain-change.md --path docs/plan.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/proposals/2026-04-27-token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.test.md`
    - `bash scripts/ci.sh --mode broad-smoke`
    - `git diff --check -- .`
  - CI status: local repo-owned broad smoke passed. Hosted CI has not been observed from this environment.
  - Artifact drift: none blocking. `docs/plan.md` and this plan body both keep the initiative active while moving the next stage from `verify` to `explain-change`.
  - Warnings: broad smoke reported unrelated baseline lifecycle warnings for older draft proposal files outside this change.
- 2026-04-28: `explain-change` completed the durable explanation artifact.
  - Artifact: `docs/changes/token-and-runtime-efficient-scanning/explain-change.md`
  - Added required sections for the original problem, review-resolution summary, alternatives rejected, risks/follow-ups, and PR handoff readiness.
  - Next stage: `pr`
- 2026-04-28: PR handoff lifecycle closeout completed in this plan and `docs/plan.md`.
  - `docs/changes/token-and-runtime-efficient-scanning/change.yaml` records `review.status: pr handoff ready`.
- 2026-04-28: PR handoff validation completed.
  - `python scripts/validate-change-metadata.py docs/changes/token-and-runtime-efficient-scanning/change.yaml` passed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/token-and-runtime-efficient-scanning/change.yaml --path docs/changes/token-and-runtime-efficient-scanning/explain-change.md --path docs/plan.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/proposals/2026-04-27-token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.test.md` passed.
  - `bash scripts/ci.sh --mode explicit --path docs/changes/token-and-runtime-efficient-scanning/change.yaml --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/plan.md` passed.
  - `bash scripts/ci.sh --mode pr --base origin/main --head HEAD` originally returned the selector v1 manual-routing block for `scripts/test-adapter-distribution.py`; the PR-stage CI repair below replaced that boundary with deterministic adapter-check routing.
  - `git diff --check -- .` passed.
- 2026-04-28: PR-stage CI repair classified `scripts/test-adapter-distribution.py` as adapter-owned in `scripts/validation_selection.py` and added explicit plus PR-mode selector regression coverage in `scripts/test-select-validation.py`.
- 2026-04-28: PR-stage CI repair validation passed: `python scripts/test-select-validation.py`; `python scripts/select-validation.py --mode explicit --path scripts/build-adapters.py --path scripts/adapter_distribution.py --path scripts/test-adapter-distribution.py --path scripts/validation_selection.py`; `bash scripts/ci.sh --mode explicit --path scripts/test-adapter-distribution.py`; and `bash scripts/ci.sh --mode pr --base origin/main --head HEAD`. The repaired PR-mode wrapper selected adapter checks with no blocking results.

## Outcome and retrospective

- Done. M1-M4 implementation milestones, first-pass `code-review`, `verify`, `explain-change`, and PR handoff readiness are complete.
- PR-stage lesson: the PR stage took longer than expected because local and hosted PR-mode CI use `bash scripts/ci.sh --mode pr`; the earlier manual-routing proof for `scripts/test-adapter-distribution.py` was valid milestone evidence but did not make hosted PR CI pass. This branch now classifies `scripts/test-adapter-distribution.py` as adapter-owned so PR-mode CI selects `adapters.regression`, `adapters.drift`, and `adapters.validate` deterministically.
- Review-record lesson: this slice had a clean first-pass `code-review` with no material findings, so the review outcome belongs in the plan and change metadata rather than a `review-resolution.md` closeout. A standalone review-resolution artifact is required only when material findings or non-final dispositions exist.

## Readiness

- Immediate next repository stage: `pr`.
- Next implementation milestone: none.

## Risks and follow-ups

- Persistent cache behavior remains a future initiative and requires measurement plus an updated or superseding spec before implementation.
- Broader parser helpers outside the adapter drift family require architecture review before adoption.
- Follow-up closed in PR-stage CI repair: selector v1 now classifies `scripts/test-adapter-distribution.py` for PR-mode changes through the adapter check family.
