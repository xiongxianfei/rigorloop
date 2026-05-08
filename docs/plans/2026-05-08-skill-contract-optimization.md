# Skill Contract Optimization Execution Plan

## Status

- active
- Owner: maintainers
- Start date: 2026-05-08
- Last updated: 2026-05-08
- Related issue or PR: none yet
- Supersedes: none
- selected_workflow_contract: refactored
- broad_smoke_required: false
- broad_smoke_reason: This initiative changes workflow-governance Markdown, canonical skill guidance, shared policy templates, static validator checks, generated skill mirrors, and public adapter skill copies. It does not add runtime data flow, storage, network boundaries, deployment behavior, release packaging, schemas, or broad natural-language quality scoring.

## Purpose / Big Picture

Implement the approved skill contract so RigorLoop skills become smaller, claim-safe, summary-first, and handoff-explicit without turning skills into substitute workflow specs.

The first implementation slice normalizes only the highest-risk lifecycle skills:

```text
workflow, plan, implement, code-review, verify, pr, learn
```

The work defines static proof, aligns source-of-truth and contributor summaries, updates canonical skill guidance, introduces stable shared blocks where approved, refreshes generated output, and preserves plan/test/review/verify/PR lifecycle evidence.

## Source Artifacts

- Proposal: [Skill Contract Optimization](../proposals/2026-05-08-skill-contract-optimization.md), accepted after proposal-review R2 on 2026-05-08.
- Spec: [Skill Contract](../../specs/skill-contract.md), approved after clean spec-review on 2026-05-08.
- Architecture: not required. The approved change is workflow guidance, canonical skill wording, static validation, shared text blocks, and generated-output refresh. It does not introduce runtime components, storage, API boundaries, deployment boundaries, or a new validation architecture.
- Test spec: [Skill Contract Test Spec](../../specs/skill-contract.test.md), active after clean plan-review.
- Project map: `docs/project-map.md` is absent. No-map rationale: this plan does not rely on repository-map claims for architecture, runtime flow, data flow, or ownership. Orientation comes from `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, the approved proposal, the approved spec, existing skill files, shared template conventions, and validator/generator scripts.
- Review records: proposal-review R1/R2 are recorded under `docs/changes/2026-05-08-skill-contract-optimization/`; spec-review was clean with no material findings and settled artifact-locally in `specs/skill-contract.md`.

## Context and Orientation

- `specs/skill-contract.md` is the approved source of truth for required skill sections, claim boundaries, output summaries, shared-block handling, generated-output boundaries, evidence-reading guidance, and minimum viable skill rules.
- `specs/rigorloop-workflow.md` remains the source of truth for stage order, stage obligation, handoff, and downstream-blocking semantics.
- `docs/workflows.md` is the short contributor-facing workflow summary and needs only concise skill-contract guidance where affected.
- `AGENTS.md` should stay concise and only carry root reminders that future agents need, such as not creating one-off skills and not treating generated output as source.
- Canonical authored skills live under `skills/`. Generated Codex runtime mirrors under `.codex/skills/` and public adapter package output under `dist/adapters/` must be refreshed through generators, not hand-edited.
- Existing shared review recording guidance lives at `templates/shared/review-isolation-and-recording.md`. This plan may add stable shared blocks for evidence collection and generated-output handling if the test spec confirms the copy-and-check shape.
- The visible workflow stage label is `ci-maintenance`, but the current skill entrypoint remains `skills/ci/SKILL.md`. This first implementation slice does not create `skills/ci-maintenance/SKILL.md`.
- The first implementation slice must not normalize every skill, add broad semantic quality scoring, generate shared blocks into skills, or create a standalone `review-resolution` skill.

## Non-Goals

- Do not change lifecycle stage order.
- Do not replace `specs/rigorloop-workflow.md`.
- Do not normalize every skill in the first implementation slice.
- Do not add a standalone `review-resolution` skill.
- Do not add `skills/ci-maintenance/SKILL.md`.
- Do not add broad natural-language quality scoring.
- Do not generate shared blocks into skills in v1.
- Do not hand-edit generated `.codex/skills/` or `dist/adapters/` output.
- Do not replace proposal, spec, plan, review, verification, explain-change, or PR artifacts with skill prose.
- Do not implement Phase 2, Phase 3, or Phase 4 skill normalization in this first implementation slice.

## Requirements Covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`-`R1d`, `R20`-`R20b` | `specs/skill-contract.md`, `specs/rigorloop-workflow.md`, `docs/workflows.md`, `AGENTS.md`, and static checks for source-of-truth split |
| `R2`-`R2d` | canonical/generated source boundary guidance, generated-output shared block, `scripts/build-skills.py --check`, `scripts/build-adapters.py --version 0.1.1 --check`, and generated output refresh |
| `R3`-`R3c` | first-slice skill section normalization and skill-validator checks for required core sections |
| `R4`-`R7a` | type-specific guidance in first-slice skills where relevant and deferred-phase notes for later skills |
| `R8`-`R8g` | first-slice scope in the test spec, validator assertions, and this plan's milestones |
| `R9`-`R9d` | contributor summary and test-spec coverage for later-phase normalization order, including `ci` as the skill for `ci-maintenance` |
| `R10`-`R10f`, `R18`-`R18d` | do-not-overclaim guidance and narrow positive-first validator checks for `implement`, `code-review`, `verify`, `pr`, `plan`, and `learn` |
| `R11`-`R11c` | compact result output guidance in first-slice skills and static checks for summary-first outputs |
| `R12`-`R12c` | local handoff sections in first-slice skills and links/pointers to workflow spec for full routing |
| `R13`-`R13f` | progress/readiness/closeout/Done wording in `plan`, `implement`, `code-review`, `verify`, `pr`, and `workflow` as applicable |
| `R14`-`R15b` | shared block source files under `templates/shared/`, copied-block guidance, and drift checks for adopted blocks |
| `R16`-`R16c` | evidence-reading guidance and full-file read escalation shared block/copies |
| `R17`-`R17b` | examples guidance in normalized skills and test-spec checks that long examples remain outside skill files |
| `R19`-`R19c` | minimum viable skill guidance in `docs/workflows.md`, `AGENTS.md`, and skill-creator guidance if adopted in scope |

## Immediate Test-Spec Handoff

`plan-review` must approve this plan before implementation starts. After plan-review, create `specs/skill-contract.test.md` to map each approved requirement, example, edge case, compatibility claim, non-goal, and acceptance criterion to concrete proof.

The test spec should require focused static assertions for:

- required core sections in the seven first-slice canonical skills;
- first-slice scope excluding Phase 2/3/4 skill normalization;
- do-not-overclaim wording for `implement`, `code-review`, `verify`, `pr`, `plan`, and `learn`;
- compact `## Result` output or reviewed equivalent in first-slice skills;
- local handoff sections that point to `specs/rigorloop-workflow.md` instead of duplicating the full lifecycle;
- progress/readiness/closeout/Done wording where relevant;
- `ci` as the current skill entrypoint for `ci-maintenance`;
- copied shared blocks for review isolation/recording, evidence collection efficiency, and generated-output handling when adopted;
- generated `.codex/skills/` and adapter output staying derived from canonical skills;
- no broad semantic quality scoring;
- no standalone `review-resolution` skill;
- no `skills/ci-maintenance/SKILL.md`.

## Current Handoff Summary

- Current milestone: M1
- Current milestone state: review-requested
- Last reviewed milestone: M1
- Review status: CR1-F1 fix applied; code-review rerun pending
- Remaining in-scope implementation milestones: M1 review-requested; M2, M3, M4 planned
- Next stage: code-review M1 rerun
- Verify readiness: not ready
- Reason verify is not ready: M1 code-review rerun, implementation milestones M2-M4, generated-output refresh, review-resolution closeout, and final verification remain incomplete.

## Milestones

### M1. Define Skill-Contract Static Proof

- Milestone state: review-requested
- Goal: Add the matching test spec and focused static proof design before changing canonical skill guidance.
- Requirements: `R1`-`R3c`, `R8`-`R20b`.
- Files/components likely touched:
  - `specs/skill-contract.test.md`
  - `scripts/test-skill-validator.py`
  - `specs/skill-contract.md` only for review-approved clarifications
  - `docs/plans/2026-05-08-skill-contract-optimization.md`
  - `docs/changes/2026-05-08-skill-contract-optimization/change.yaml`
- Dependencies:
  - plan-review approval
  - approved `specs/skill-contract.md`
- Tests to design or add:
  - Test-spec cases for required core sections in first-slice skills.
  - Test-spec cases for narrow do-not-overclaim wording and positive required wording.
  - Test-spec cases for shared-block copy/drift when new shared blocks are adopted.
  - Test-spec cases for `ci`/`ci-maintenance` naming split.
  - Test-spec cases that Phase 2/3/4 skills and optional skills are not pulled into first-slice implementation.
  - Test-spec cases that no standalone `review-resolution` or `ci-maintenance` skill path is introduced.
  - Validator assertions may be added in M1 only when they can pass without the later canonical skill edits; checks that require normalization belong with M2 or M3.
- Implementation steps:
  - Create `specs/skill-contract.test.md` from the approved spec.
  - Define the focused validator checks needed for the implementation milestones.
  - Do not leave failing validator assertions committed as M1 closeout evidence.
  - Prefer positive required wording checks before adding narrow forbidden-phrase checks.
  - Avoid broad natural-language quality scoring.
  - Avoid semantic skill-output scoring or runtime workflow simulation.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/select-validation.py --mode explicit --path specs/skill-contract.md --path specs/skill-contract.test.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-08-skill-contract-optimization.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path specs/skill-contract.md --path specs/skill-contract.test.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-08-skill-contract-optimization.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml`
  - `git diff --check -- specs/skill-contract.md specs/skill-contract.test.md scripts/test-skill-validator.py docs/plans/2026-05-08-skill-contract-optimization.md docs/changes/2026-05-08-skill-contract-optimization/change.yaml`
- Expected observable result: the approved skill-contract requirements are mapped to test-spec proof and any committed validator scaffolding passes before canonical first-slice skills are normalized.
- Commit message: `M1: add skill contract proof`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone state updated to `review-requested` before code-review handoff
  - [x] milestone committed
- Risks:
  - Tests may overfit wording and make skill maintenance brittle.
  - Forbidden-phrase checks may block explicit negative guidance.
- Rollback/recovery:
  - Replace brittle exact prose checks with heading, required-term, and narrow forbidden-phrase checks.
  - Narrow any forbidden phrase that catches "Do not ..." style guidance.

### M2. Align Contract Summaries and Shared Blocks

- Milestone state: planned
- Goal: Add concise contributor-facing summaries and stable shared blocks needed by first-slice skill normalization without duplicating full workflow policy.
- Requirements: `R1`-`R2d`, `R12`-`R16c`, `R19`-`R20b`.
- Files/components likely touched:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `templates/shared/review-isolation-and-recording.md`
  - `templates/shared/evidence-collection-efficiency.md`
  - `templates/shared/generated-output-handling.md`
  - `templates/skill.md` or skill-creator guidance only if the approved test spec requires minimum viable skill examples in this slice
  - `scripts/test-skill-validator.py`
  - `docs/plans/2026-05-08-skill-contract-optimization.md`
  - `docs/changes/2026-05-08-skill-contract-optimization/change.yaml`
- Dependencies:
  - M1 static proof in place
- Tests to add/update:
  - Static checks that workflow docs summarize, not override, the skill contract.
  - Static checks for shared-block source files and copied-block drift rules.
  - Static checks that `AGENTS.md` remains concise and does not become a second skill spec.
- Implementation steps:
  - Add a short pointer from `specs/rigorloop-workflow.md` to `specs/skill-contract.md` without moving stage-order semantics.
  - Add concise `docs/workflows.md` summary for skill contract, generated-output handling, shared blocks, and minimum viable skill rule.
  - Add concise `AGENTS.md` reminder only if needed for agent behavior.
  - Create or update shared blocks approved for v1.
  - Keep deferred blocks out of scope unless the test spec identifies a direct contradiction.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/select-validation.py --mode explicit --path specs/skill-contract.md --path specs/skill-contract.test.md --path specs/rigorloop-workflow.md --path docs/workflows.md --path AGENTS.md --path templates/shared/review-isolation-and-recording.md --path templates/shared/evidence-collection-efficiency.md --path templates/shared/generated-output-handling.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-08-skill-contract-optimization.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path specs/skill-contract.md --path specs/skill-contract.test.md --path specs/rigorloop-workflow.md --path docs/workflows.md --path AGENTS.md --path templates/shared/review-isolation-and-recording.md --path templates/shared/evidence-collection-efficiency.md --path templates/shared/generated-output-handling.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-08-skill-contract-optimization.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml`
  - `git diff --check -- specs/skill-contract.md specs/skill-contract.test.md specs/rigorloop-workflow.md docs/workflows.md AGENTS.md templates/shared scripts/test-skill-validator.py docs/plans/2026-05-08-skill-contract-optimization.md docs/changes/2026-05-08-skill-contract-optimization/change.yaml`
- Expected observable result: authoritative and summary surfaces point to the skill contract cleanly, and approved shared blocks have canonical sources before first-slice skill copies.
- Commit message: `M2: align skill contract summaries`
- Milestone closeout:
  - [ ] targeted validation passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone state updated to `review-requested` before code-review handoff
  - [ ] milestone committed
- Risks:
  - `AGENTS.md` or `docs/workflows.md` could duplicate too much spec detail.
  - New shared blocks could drift from the skill copies before generated output refresh.
- Rollback/recovery:
  - Move excess summary detail back to `specs/skill-contract.md`.
  - Keep shared blocks copied and validator-checked rather than generated.

### M3. Normalize First-Slice Canonical Skills

- Milestone state: planned
- Goal: Normalize only the seven first-slice canonical skills to satisfy the required core sections, claim boundaries, summary-first result output, local handoff, evidence-reading, shared-block, and progress/readiness guidance.
- Requirements: `R3`-`R18d`, `R20`-`R20b`.
- Files/components likely touched:
  - `skills/workflow/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/learn/SKILL.md`
  - `scripts/test-skill-validator.py`
  - `docs/plans/2026-05-08-skill-contract-optimization.md`
  - `docs/changes/2026-05-08-skill-contract-optimization/change.yaml`
- Dependencies:
  - M1 static proof in place
  - M2 shared blocks available where adopted
- Tests to add/update:
  - Required core section checks for the seven first-slice skills.
  - Result output checks for summary-first expected output or approved equivalent.
  - Do-not-overclaim wording checks for `implement`, `code-review`, `verify`, `pr`, `plan`, and `learn`.
  - Handoff section checks that point to workflow spec for full routing.
  - Evidence-reading shared-block checks where copied.
- Implementation steps:
  - Normalize `workflow` without changing lifecycle stage order.
  - Normalize `plan` with progress/readiness/closeout/Done distinction and milestone-aware wording preserved.
  - Normalize `implement` so it reports implementation completion/readiness for `code-review`, not review or verify ownership.
  - Normalize `code-review` so it owns review findings and clean-with-notes, not branch or PR readiness.
  - Normalize `verify` so it owns validation proof and branch-ready, not PR body/opening readiness.
  - Normalize `pr` so it links to implementation, review, and verification evidence instead of claiming those proofs independently.
  - Normalize `learn` so lessons route policy changes to authoritative artifacts.
  - Do not touch Phase 2/3/4 skills in this milestone except for shared-block source files already handled by M2.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/select-validation.py --mode explicit --path skills/workflow/SKILL.md --path skills/plan/SKILL.md --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path skills/verify/SKILL.md --path skills/pr/SKILL.md --path skills/learn/SKILL.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-08-skill-contract-optimization.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml`
  - `git diff --check -- skills/workflow/SKILL.md skills/plan/SKILL.md skills/implement/SKILL.md skills/code-review/SKILL.md skills/verify/SKILL.md skills/pr/SKILL.md skills/learn/SKILL.md scripts/test-skill-validator.py docs/plans/2026-05-08-skill-contract-optimization.md docs/changes/2026-05-08-skill-contract-optimization/change.yaml`
- Generated-output checks are M4 closeout gates. If selector output reports generated drift after M3 canonical skill edits, record that as the expected M4 handoff reason rather than claiming verify readiness.
- Expected observable result: seven canonical first-slice skills satisfy the approved skill contract while later-phase skills remain out of scope and generated refresh remains explicitly pending M4.
- Commit message: `M3: normalize first-slice skills`
- Milestone closeout:
  - [ ] targeted validation passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone state updated to `review-requested` before code-review handoff
  - [ ] milestone committed
- Risks:
  - Normalization could bloat skill files instead of sharpening them.
  - Shared block copies could make skills repetitive.
  - Existing useful domain-specific guidance could be lost.
- Rollback/recovery:
  - Preserve behavior-changing local guidance under compact conditional sections.
  - Revert any Phase 2/3/4 skill edits that slip into the first slice.

### M4. Refresh Generated Skill and Adapter Output

- Milestone state: planned
- Goal: Regenerate derived Codex skill mirrors and public adapter skill copies from canonical skills and prove no generated-output drift remains.
- Requirements: `R2`-`R2d`, `R8f`, `R14c`, `R20`-`R20b`.
- Files/components likely touched:
  - `.codex/skills/workflow/SKILL.md`
  - `.codex/skills/plan/SKILL.md`
  - `.codex/skills/implement/SKILL.md`
  - `.codex/skills/code-review/SKILL.md`
  - `.codex/skills/verify/SKILL.md`
  - `.codex/skills/pr/SKILL.md`
  - `.codex/skills/learn/SKILL.md`
  - `dist/adapters/codex/.agents/skills/<skill>/SKILL.md` for each changed first-slice skill
  - `dist/adapters/claude/.claude/skills/<skill>/SKILL.md` for each changed first-slice skill
  - `dist/adapters/opencode/.opencode/skills/<skill>/SKILL.md` for each changed first-slice skill
  - `docs/plans/2026-05-08-skill-contract-optimization.md`
  - `docs/changes/2026-05-08-skill-contract-optimization/change.yaml`
- Dependencies:
  - M3 canonical skill changes complete
- Tests to add/update:
  - No new tests expected unless generated-output validation reveals a selector or adapter coverage gap.
- Implementation steps:
  - Run `python scripts/build-skills.py` to refresh `.codex/skills/`.
  - Run `python scripts/build-adapters.py --version 0.1.1` to refresh public adapter output.
  - Validate generated drift checks.
  - Use concrete generated adapter file paths in selector-driven commands; do not pass `--path dist/adapters`.
- Validation commands:
  - `python scripts/build-skills.py`
  - `python scripts/build-adapters.py --version 0.1.1`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/select-validation.py --mode explicit --path .codex/skills/workflow/SKILL.md --path .codex/skills/plan/SKILL.md --path .codex/skills/implement/SKILL.md --path .codex/skills/code-review/SKILL.md --path .codex/skills/verify/SKILL.md --path .codex/skills/pr/SKILL.md --path .codex/skills/learn/SKILL.md --path dist/adapters/codex/.agents/skills/workflow/SKILL.md --path dist/adapters/codex/.agents/skills/plan/SKILL.md --path dist/adapters/codex/.agents/skills/implement/SKILL.md --path dist/adapters/codex/.agents/skills/code-review/SKILL.md --path dist/adapters/codex/.agents/skills/verify/SKILL.md --path dist/adapters/codex/.agents/skills/pr/SKILL.md --path dist/adapters/codex/.agents/skills/learn/SKILL.md --path dist/adapters/claude/.claude/skills/workflow/SKILL.md --path dist/adapters/claude/.claude/skills/plan/SKILL.md --path dist/adapters/claude/.claude/skills/implement/SKILL.md --path dist/adapters/claude/.claude/skills/code-review/SKILL.md --path dist/adapters/claude/.claude/skills/verify/SKILL.md --path dist/adapters/claude/.claude/skills/pr/SKILL.md --path dist/adapters/claude/.claude/skills/learn/SKILL.md --path dist/adapters/opencode/.opencode/skills/workflow/SKILL.md --path dist/adapters/opencode/.opencode/skills/plan/SKILL.md --path dist/adapters/opencode/.opencode/skills/implement/SKILL.md --path dist/adapters/opencode/.opencode/skills/code-review/SKILL.md --path dist/adapters/opencode/.opencode/skills/verify/SKILL.md --path dist/adapters/opencode/.opencode/skills/pr/SKILL.md --path dist/adapters/opencode/.opencode/skills/learn/SKILL.md --path docs/plans/2026-05-08-skill-contract-optimization.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path .codex/skills/workflow/SKILL.md --path .codex/skills/plan/SKILL.md --path .codex/skills/implement/SKILL.md --path .codex/skills/code-review/SKILL.md --path .codex/skills/verify/SKILL.md --path .codex/skills/pr/SKILL.md --path .codex/skills/learn/SKILL.md --path dist/adapters/codex/.agents/skills/workflow/SKILL.md --path dist/adapters/codex/.agents/skills/plan/SKILL.md --path dist/adapters/codex/.agents/skills/implement/SKILL.md --path dist/adapters/codex/.agents/skills/code-review/SKILL.md --path dist/adapters/codex/.agents/skills/verify/SKILL.md --path dist/adapters/codex/.agents/skills/pr/SKILL.md --path dist/adapters/codex/.agents/skills/learn/SKILL.md --path dist/adapters/claude/.claude/skills/workflow/SKILL.md --path dist/adapters/claude/.claude/skills/plan/SKILL.md --path dist/adapters/claude/.claude/skills/implement/SKILL.md --path dist/adapters/claude/.claude/skills/code-review/SKILL.md --path dist/adapters/claude/.claude/skills/verify/SKILL.md --path dist/adapters/claude/.claude/skills/pr/SKILL.md --path dist/adapters/claude/.claude/skills/learn/SKILL.md --path dist/adapters/opencode/.opencode/skills/workflow/SKILL.md --path dist/adapters/opencode/.opencode/skills/plan/SKILL.md --path dist/adapters/opencode/.opencode/skills/implement/SKILL.md --path dist/adapters/opencode/.opencode/skills/code-review/SKILL.md --path dist/adapters/opencode/.opencode/skills/verify/SKILL.md --path dist/adapters/opencode/.opencode/skills/pr/SKILL.md --path dist/adapters/opencode/.opencode/skills/learn/SKILL.md --path docs/plans/2026-05-08-skill-contract-optimization.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml`
  - `git diff --check -- .codex/skills dist/adapters docs/plans/2026-05-08-skill-contract-optimization.md docs/changes/2026-05-08-skill-contract-optimization/change.yaml`
- Expected observable result: generated local Codex and public adapter skill copies match canonical first-slice skill source, and selector validation uses concrete generated file paths.
- Commit message: `M4: refresh skill contract generated guidance`
- Milestone closeout:
  - [ ] targeted validation passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone state updated to `review-requested` before code-review handoff
  - [ ] milestone committed
- Risks:
  - Adapter selector validation can fail if directory paths are passed instead of concrete files.
  - Generated output can drift after canonical skill edits.
- Rollback/recovery:
  - Re-run generators from canonical skills.
  - Replace unclassified selector paths with concrete generated adapter file paths.

## Lifecycle Closeout

- Lifecycle label: lifecycle-closeout
- Goal: Complete final verification, explanation, PR preparation, and plan lifecycle synchronization after all implementation milestones are closed.
- Requirements: all approved spec requirements after implementation closeout.
- Files/components likely touched:
  - `docs/plan.md`
  - `docs/plans/2026-05-08-skill-contract-optimization.md`
  - `docs/changes/2026-05-08-skill-contract-optimization/change.yaml`
  - `docs/changes/2026-05-08-skill-contract-optimization/explain-change.md`
  - PR body or PR description
- Dependencies:
  - M1-M4 closed
  - code-review clean or required review-resolution closed
  - `verify` passed
- Tests to add/update:
  - No new behavior tests expected unless verification or review identifies a gap.
- Implementation steps:
  - Run selected CI for the full changed path set.
  - Run broad smoke only if selector, plan-review, test spec, or review-resolution requires it.
  - Update explain-change with real diff and validation evidence.
  - Update `docs/plan.md` and this plan body to `done` inside the PR if no true downstream event remains.
  - Prepare PR with accurate source artifacts, changed files, validation, risks, and reviewer notes.
- Validation commands:
  - `python scripts/select-validation.py --mode explicit --path <all changed authored, generated, review, plan, and change-local paths>`
  - `bash scripts/ci.sh --mode explicit --path <all changed authored, generated, review, plan, and change-local paths>`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-skill-contract-optimization`
  - `git diff --check -- <all changed paths>`
  - `rg -n '[[:blank:]]$|\t' <all changed paths>`
  - `bash scripts/ci.sh --mode broad-smoke` only if triggered by selector, plan-review, test spec, review-resolution, or release metadata
- Expected observable result: final artifacts are synchronized, verification evidence is durable, and PR handoff is ready without relying on lifecycle changes after the PR merges.
- Commit message: `M5: close skill contract optimization plan`
- Milestone closeout:
  - [ ] selected validation passed
  - [ ] review-resolution closed if triggered
  - [ ] verify passed
  - [ ] explain-change updated
  - [ ] `docs/plan.md` and this plan body synchronized
  - [ ] PR handoff complete
- Risks:
  - Plan lifecycle state can drift between `docs/plan.md` and this plan body.
  - Final PR text can introduce authoritative references after verification.
- Rollback/recovery:
  - Keep the plan `active` and name a true downstream event only if one remains after PR handoff.
  - Re-run verify if final PR text adds new authoritative artifact references.

## Validation Plan

- Use selector-selected validation first for each milestone's changed paths.
- Use `python scripts/test-skill-validator.py` for skill-contract static proof.
- Use `python scripts/validate-skills.py` for authored skill structure.
- Use `python scripts/build-skills.py --check` and `python scripts/build-adapters.py --version 0.1.1 --check` for generated drift.
- Use `python scripts/validate-adapters.py --version 0.1.1` and `python scripts/test-adapter-distribution.py` after adapter output refresh.
- Use `python scripts/validate-change-metadata.py docs/changes/2026-05-08-skill-contract-optimization/change.yaml` when change metadata changes.
- Use `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-skill-contract-optimization` when review artifacts change or before final handoff.
- Use broad smoke only when triggered by selector, plan-review, test spec, review-resolution, release metadata, or explicit reviewer requirement.

## Risks and Recovery

- Risk: The first implementation slice grows to Phase 2/3/4 skills.
  - Recovery: Revert out-of-scope skill edits and keep first-slice validation scoped to the seven approved skills.
- Risk: Required section normalization bloats skill files.
  - Recovery: Keep core sections concise and move long examples to templates or examples.
- Risk: Forbidden phrase validation becomes brittle.
  - Recovery: Prefer positive required wording and narrow exact forbidden checks.
- Risk: Shared-block copy checks drift.
  - Recovery: Update shared source and copied consumers together, then rerun validator tests.
- Risk: Generated output is hand-edited or stale.
  - Recovery: Regenerate from canonical skills and rerun drift checks.
- Risk: `ci-maintenance` is mistaken for a missing skill directory.
  - Recovery: Preserve `skills/ci/SKILL.md` as the skill entrypoint and document the stage-label split.

## Dependencies

- Plan-review approval before test-spec.
- Matching test spec before implementation.
- No architecture artifact required unless plan-review or spec-review identifies a design boundary not currently present.
- Generated-output refresh depends on canonical skill changes being complete.
- Final verify depends on review-resolution closeout if code-review or other formal review triggers material findings.

## Progress

- [x] Proposal accepted.
- [x] Spec drafted and approved.
- [x] Plan created.
- [x] Plan-review complete.
- [x] Test spec active.
- [x] M1 implementation complete and ready for code-review.
- [x] M1 code-review completed with changes requested.
- [x] M1 CR1-F1 fix implemented and ready for code-review rerun.
- [ ] M1 closed.
- [ ] M2 closed.
- [ ] M3 closed.
- [ ] M4 closed.
- [ ] Code-review clean or review-resolution closed if triggered.
- [ ] Verify passed.
- [ ] Explain-change complete.
- [ ] PR handoff complete.

## Decision Log

- 2026-05-08: Use `specs/skill-contract.md` as the normative skill-contract source. Rationale: keeps skill-contract behavior separate from workflow-routing semantics.
- 2026-05-08: No architecture artifact required. Rationale: first slice changes repository guidance, static validation, and generated outputs without adding runtime or validation architecture.
- 2026-05-08: Keep first implementation slice to seven canonical skills. Rationale: matches accepted proposal and avoids broad normalization churn.
- 2026-05-08: Treat `ci` as the skill entrypoint for `ci-maintenance`. Rationale: existing workflow spec allows the naming split and no `skills/ci-maintenance/` path is approved.
- 2026-05-08: Use an active static/contract test spec rather than runtime workflow simulation. Rationale: approved first slice changes skill guidance, shared blocks, validation, and generated output without adding an executable workflow router.
- 2026-05-08: Limit M1 validator assertions to approved spec/test-spec/plan and path-boundary proof that can pass before canonical skill normalization. Rationale: first-slice skill section and overclaim checks depend on M2/M3 changes and should not be committed red as M1 closeout evidence.

## Surprises and Discoveries

- 2026-05-08: The first M1 validator assertion used a paraphrased `ci`/`ci-maintenance` phrase and failed. The check was narrowed to the exact approved spec wording before closeout.
- 2026-05-08: code-review R1 found that the first-slice test-spec assertion in `scripts/test-skill-validator.py` checks bare skill-name substrings, allowing short names such as `pr` to pass from unrelated words.

## Validation Notes

- 2026-05-08: `bash scripts/ci.sh --mode explicit --path specs/skill-contract.md --path docs/proposals/2026-05-08-skill-contract-optimization.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml --path docs/changes/2026-05-08-skill-contract-optimization/review-log.md --path docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r1.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r2.md` passed before plan creation.
- 2026-05-08: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-skill-contract-optimization` passed before plan creation.
- 2026-05-08: `python scripts/validate-change-metadata.py docs/changes/2026-05-08-skill-contract-optimization/change.yaml` passed before plan creation.
- 2026-05-08: `python scripts/select-validation.py --mode explicit --path specs/skill-contract.md --path docs/plan.md --path docs/plans/2026-05-08-skill-contract-optimization.md --path docs/proposals/2026-05-08-skill-contract-optimization.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml --path docs/changes/2026-05-08-skill-contract-optimization/review-log.md --path docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r1.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r2.md` passed with no unclassified paths.
- 2026-05-08: `python scripts/validate-change-metadata.py docs/changes/2026-05-08-skill-contract-optimization/change.yaml` passed after plan creation.
- 2026-05-08: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-skill-contract-optimization` passed after plan creation.
- 2026-05-08: `bash scripts/ci.sh --mode explicit --path specs/skill-contract.md --path docs/plan.md --path docs/plans/2026-05-08-skill-contract-optimization.md --path docs/proposals/2026-05-08-skill-contract-optimization.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml --path docs/changes/2026-05-08-skill-contract-optimization/review-log.md --path docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r1.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r2.md` passed selected checks.
- 2026-05-08: `git diff --check -- specs/skill-contract.md docs/plan.md docs/plans/2026-05-08-skill-contract-optimization.md docs/proposals/2026-05-08-skill-contract-optimization.md docs/changes/2026-05-08-skill-contract-optimization/change.yaml docs/changes/2026-05-08-skill-contract-optimization/review-log.md docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r1.md docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r2.md` passed.
- 2026-05-08: `rg -n '[[:blank:]]$|\t' specs/skill-contract.md docs/plan.md docs/plans/2026-05-08-skill-contract-optimization.md docs/proposals/2026-05-08-skill-contract-optimization.md docs/changes/2026-05-08-skill-contract-optimization/change.yaml docs/changes/2026-05-08-skill-contract-optimization/review-log.md docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r1.md docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r2.md` found no matches.
- 2026-05-08: `python scripts/select-validation.py --mode explicit --path specs/skill-contract.md --path specs/skill-contract.test.md --path docs/plan.md --path docs/plans/2026-05-08-skill-contract-optimization.md --path docs/proposals/2026-05-08-skill-contract-optimization.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml --path docs/changes/2026-05-08-skill-contract-optimization/review-log.md --path docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r1.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r2.md` passed with no unclassified paths after test-spec creation.
- 2026-05-08: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/skill-contract.md --path specs/skill-contract.test.md --path docs/plan.md --path docs/plans/2026-05-08-skill-contract-optimization.md --path docs/proposals/2026-05-08-skill-contract-optimization.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml --path docs/changes/2026-05-08-skill-contract-optimization/review-log.md --path docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r1.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r2.md` passed after test-spec creation; it reported a non-blocking reviewer-attention warning for pre-existing merge-related wording in an older `docs/plan.md` done entry.
- 2026-05-08: `python scripts/validate-change-metadata.py docs/changes/2026-05-08-skill-contract-optimization/change.yaml` passed after test-spec creation.
- 2026-05-08: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-skill-contract-optimization` passed after test-spec creation.
- 2026-05-08: `bash scripts/ci.sh --mode explicit --path specs/skill-contract.md --path specs/skill-contract.test.md --path docs/plan.md --path docs/plans/2026-05-08-skill-contract-optimization.md --path docs/proposals/2026-05-08-skill-contract-optimization.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml --path docs/changes/2026-05-08-skill-contract-optimization/review-log.md --path docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r1.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r2.md` passed selected checks after test-spec creation.
- 2026-05-08: `git diff --check -- specs/skill-contract.md specs/skill-contract.test.md docs/plan.md docs/plans/2026-05-08-skill-contract-optimization.md docs/proposals/2026-05-08-skill-contract-optimization.md docs/changes/2026-05-08-skill-contract-optimization/change.yaml docs/changes/2026-05-08-skill-contract-optimization/review-log.md docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r1.md docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r2.md` passed after test-spec creation.
- 2026-05-08: `rg -n '[[:blank:]]$|\t' specs/skill-contract.md specs/skill-contract.test.md docs/plan.md docs/plans/2026-05-08-skill-contract-optimization.md docs/proposals/2026-05-08-skill-contract-optimization.md docs/changes/2026-05-08-skill-contract-optimization/change.yaml docs/changes/2026-05-08-skill-contract-optimization/review-log.md docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r1.md docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r2.md` found no matches after test-spec creation.
- 2026-05-08: `python scripts/test-skill-validator.py` failed once because the new `ci`/`ci-maintenance` assertion used paraphrased wording; after narrowing the assertion to the approved spec phrase, `python scripts/test-skill-validator.py` passed 37 tests.
- 2026-05-08: `python scripts/select-validation.py --mode explicit --path specs/skill-contract.md --path specs/skill-contract.test.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-08-skill-contract-optimization.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml` passed with no unclassified paths for M1.
- 2026-05-08: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/skill-contract.md --path specs/skill-contract.test.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-08-skill-contract-optimization.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml` passed for M1.
- 2026-05-08: `python scripts/validate-change-metadata.py docs/changes/2026-05-08-skill-contract-optimization/change.yaml` passed for M1.
- 2026-05-08: `bash scripts/ci.sh --mode explicit --path specs/skill-contract.md --path specs/skill-contract.test.md --path scripts/test-skill-validator.py --path docs/plans/2026-05-08-skill-contract-optimization.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml` passed selected M1 checks: `skills.regression`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- 2026-05-08: `git diff --check -- specs/skill-contract.md specs/skill-contract.test.md scripts/test-skill-validator.py docs/plans/2026-05-08-skill-contract-optimization.md docs/changes/2026-05-08-skill-contract-optimization/change.yaml` passed for M1.
- 2026-05-08: `rg -n '[[:blank:]]$|\t' specs/skill-contract.md specs/skill-contract.test.md scripts/test-skill-validator.py docs/plans/2026-05-08-skill-contract-optimization.md docs/changes/2026-05-08-skill-contract-optimization/change.yaml` found no matches for M1.
- 2026-05-08: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-08-skill-contract-optimization` passed after code-review R1 recorded open finding CR1-F1.
- 2026-05-08: `python scripts/validate-change-metadata.py docs/changes/2026-05-08-skill-contract-optimization/change.yaml` passed after code-review R1.
- 2026-05-08: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml --path docs/changes/2026-05-08-skill-contract-optimization/review-log.md --path docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/code-review-r1.md --path docs/plans/2026-05-08-skill-contract-optimization.md` passed after code-review R1.
- 2026-05-08: `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-08-skill-contract-optimization/review-log.md --path docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/code-review-r1.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml --path docs/plans/2026-05-08-skill-contract-optimization.md` passed selected checks after code-review R1.
- 2026-05-08: `python scripts/test-skill-validator.py` passed 37 tests after tightening the CR1-F1 first-slice assertion to bounded evidence.
- 2026-05-08: `python scripts/select-validation.py --mode explicit --path scripts/test-skill-validator.py --path docs/changes/2026-05-08-skill-contract-optimization/review-log.md --path docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/code-review-r1.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml --path docs/plans/2026-05-08-skill-contract-optimization.md` passed with no unclassified paths after CR1-F1 fix.
- 2026-05-08: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml --path docs/changes/2026-05-08-skill-contract-optimization/review-log.md --path docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/code-review-r1.md --path docs/plans/2026-05-08-skill-contract-optimization.md` passed after CR1-F1 fix.
- 2026-05-08: `bash scripts/ci.sh --mode explicit --path scripts/test-skill-validator.py --path docs/changes/2026-05-08-skill-contract-optimization/review-log.md --path docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/code-review-r1.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml --path docs/plans/2026-05-08-skill-contract-optimization.md` passed selected checks after CR1-F1 fix.
- 2026-05-08: `git diff --check -- scripts/test-skill-validator.py docs/changes/2026-05-08-skill-contract-optimization/review-log.md docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md docs/changes/2026-05-08-skill-contract-optimization/reviews/code-review-r1.md docs/changes/2026-05-08-skill-contract-optimization/change.yaml docs/plans/2026-05-08-skill-contract-optimization.md` passed after CR1-F1 fix.
- 2026-05-08: `rg -n '[[:blank:]]$|\t' scripts/test-skill-validator.py docs/changes/2026-05-08-skill-contract-optimization/review-log.md docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md docs/changes/2026-05-08-skill-contract-optimization/reviews/code-review-r1.md docs/changes/2026-05-08-skill-contract-optimization/change.yaml docs/plans/2026-05-08-skill-contract-optimization.md` found no matches after CR1-F1 fix.

## Outcome and Retrospective

Plan is active. Implementation, review, verification, explanation, and PR handoff remain incomplete.

## Readiness

Status: Active.

Progress: proposal is accepted; spec is approved; plan-review approved the execution plan; test spec is active; M1 implementation is complete; code-review R1 requested changes for CR1-F1; the CR1-F1 fix is implemented.

Readiness: Ready for code-review M1 rerun.

Remaining completion gates: code-review M1 rerun, review-resolution closeout, implementation milestones M2-M4, code-review for each remaining implementation milestone, review-resolution if triggered, verify, explain-change, PR handoff, then Done if no true downstream event remains.

## Risks and Follow-Ups

- Follow up in code-review M1 on whether the passable validator scaffolding is sufficiently narrow and useful before M2/M3 skill normalization.
- Keep broad smoke untriggered unless selector, test spec, review-resolution, release metadata, or explicit reviewer requirement changes that.
