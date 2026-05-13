# Project Artifact Location Guide and Examples Surface Plan

- Status: active
- Owner: maintainers
- Start date: 2026-05-13
- Last updated: 2026-05-13
- Related proposal: [Project Artifact Location Guide and Examples Surface](../proposals/2026-05-13-project-artifact-location-guide-and-examples-surface.md)
- Supersedes: none

## Purpose / big picture

Implement the approved artifact-location guide and examples surface contract. The change makes `docs/workflows.md` the project-local artifact-location map, keeps exact artifact shapes in specs and schemas, teaches stage skills token-efficient lookup behavior, ensures `docs/examples/**` remains non-lifecycle example content, and records an explicit retained-fixture rationale if `docs/changes/0001-skill-validator/` stays in an active-looking path.

## Source artifacts

- Proposal: [Project Artifact Location Guide and Examples Surface](../proposals/2026-05-13-project-artifact-location-guide-and-examples-surface.md), accepted.
- Spec: [Project Artifact Location Guide and Examples Surface](../../specs/project-artifact-location-guide-and-examples-surface.md), approved.
- Spec-review records: [spec-review-r1](../changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/reviews/spec-review-r1.md), [spec-review-r2](../changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/reviews/spec-review-r2.md).
- Review resolution: [review-resolution.md](../changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/review-resolution.md), closed after `plan-review-r2`.
- Test spec: [Project Artifact Location Guide and Examples Surface Test Spec](../../specs/project-artifact-location-guide-and-examples-surface.test.md), active.
- Architecture: no runtime architecture package expected. This is workflow guidance, skill text, examples routing, and validation work; if planning or review identifies an architecture boundary change, return to `architecture`.
- Project map: absent. No-map rationale: the change touches documented workflow surfaces, canonical skills, generated skill output, and validation scripts that were directly inspected; no repository-wide runtime architecture map is required to sequence this plan.

## Context and orientation

Canonical authored workflow content lives under `docs/`, `specs/`, `skills/`, `schemas/`, `scripts/`, and `templates/`. Canonical skill source is under `skills/<skill>/SKILL.md`; generated public adapter packages under `dist/adapters/` are derived output and must not be hand-edited. Local `.codex/skills/` is ignored runtime state.

The current `docs/workflows.md` already says `docs/examples/**` is not active lifecycle state and retains `docs/changes/0001-skill-validator/` as a rich validator fixture and historical proof pack. It does not yet provide a single `Artifact locations` table with source-rank and schema-disclaimer wording.

Selector routing already has special handling for `docs/examples/**` in `scripts/validation_selection.py`, and tests reference `docs/examples/plans/example-plan.md`. The implementation must preserve that non-lifecycle classification while adding contract coverage for the new token-efficient lookup and retained-fixture behavior.

Likely affected canonical skills:

- `skills/workflow/SKILL.md`
- authoring skills that create artifacts: `proposal`, `spec`, `architecture`, `plan`, `test-spec`, `explain-change`
- review skills that create review records: `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, `code-review`
- downstream handoff skills that locate change-local artifacts when relevant: `verify`, `pr`

Generated skill mirrors and public adapters must be refreshed or checked after canonical skill edits.

## Current Handoff Summary

- Current milestone: downstream closeout after implementation milestones
- Current milestone state: ready-for-explain-change
- Last reviewed milestone: M4. Generated Output Refresh And Final Milestone Review
- Review status: clean code-review for M4 recorded in `code-review-r4`
- Remaining in-scope implementation milestones: none
- Next stage: explain-change
- Final closeout readiness: ready to start downstream closeout; not PR-ready
- Reason final closeout is or is not ready: M1, M2, M3, and M4 are closed after clean code-review; explain-change and verify are not complete, and PR handoff is not prepared.

## Non-goals

- Do not change the standard workflow order.
- Do not redesign formal review recording or review-resolution dispositions.
- Do not make `workflow` author every artifact type.
- Do not make `docs/workflows.md` override approved specs, schemas, architecture artifacts, active plan state, or explicit user paths.
- Do not require public skills to broad-search all authoritative docs solely to discover artifact paths.
- Do not require immediate movement of `docs/changes/0001-skill-validator/` if validator or compatibility coupling remains.
- Do not hand-edit generated public adapter output.

## Requirements covered

- `R1`-`R1d`: `docs/workflows.md` owns the user-facing artifact-location map without becoming a schema authority.
- `R2`-`R2g`: source-rank precedence, explicit path safety, no broad authority scans for path discovery, and stale-map conflict handling.
- `R3`-`R3b`: `workflow` guide create/refresh triggers and non-ownership of every artifact.
- `R4`-`R4c`: required artifact-location rows and conditional review-resolution/verify-report wording.
- `R5`-`R5g`: concise shared stage-skill lookup wording, token-efficient lookup, and generated/public skill portability.
- `R6`-`R6e`: `docs/examples/**` non-lifecycle example routing and formal review example closeout behavior.
- `R7`-`R8a`: retained `docs/changes/0001-skill-validator/` fixture rationale or safe move with references updated.
- `R9`-`R10b`: custom project path preservation and generated-output source-of-truth handling.
- `R11`-`R11d`: repository-owned validation for examples routing, lifecycle behavior, review examples, and retained-fixture outcome.
- `R12`-`R12b`: standard workflow and formal review recording non-regression.

## Milestones

Each in-scope implementation milestone follows the same review handoff:

1. Mark the current milestone `implementing` when implementation starts.
2. After implementation and targeted validation pass, update the plan body, validation notes, change metadata, and Current Handoff Summary.
3. Set the milestone state to `review-requested`, set `Review status` to `code-review requested for M<n>`, and hand off to `code-review`.
4. If the milestone review is clean and no review-resolution work is triggered, set the reviewed milestone to `closed`, update `Last reviewed milestone`, remove it from `Remaining in-scope implementation milestones`, and set `Current milestone` to the next open milestone.
5. If the milestone review has material findings, set the milestone state to `resolution-needed`, keep the finding open through `review-resolution`, and do not move to the next milestone until the finding is resolved and any required re-review passes.
6. After M4's own code-review is clean and any required review-resolution is closed, move to downstream `explain-change`, `verify`, and `pr` gates.

### M1. Workflow Artifact Map And Retained Fixture Rationale

- Milestone state: closed
- Goal: add the project artifact-location map to `docs/workflows.md`, update workflow guidance, and record retained-fixture rationale for `docs/changes/0001-skill-validator/` unless it can move safely.
- Requirements: `R1`-`R4c`, `R6a`, `R7`-`R8a`, `R9`, `R12`-`R12b`
- Files/components likely touched:
  - `docs/workflows.md`
  - `skills/workflow/SKILL.md`
  - `docs/examples/README.md`
  - `docs/changes/0001-skill-validator/**` or `docs/examples/changes/skill-validator/**`
  - `AGENTS.md` only if existing concise guidance becomes contradictory
  - `CONSTITUTION.md` only if governance summary becomes contradictory
  - `docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/change.yaml`
- Dependencies: approved spec and closed spec-review findings.
- Tests to add/update:
  - Test-spec should require checks that `docs/workflows.md` contains the artifact map, source-rank disclaimer, schema disclaimer, and conditional review-resolution/verify-report wording.
  - Test-spec should require proof that the retained fixture either moves with references updated or has durable rationale.
- Implementation steps:
  - Add an `Artifact locations` section to `docs/workflows.md` with required rows and disclaimers.
  - Add source-rank versus lookup-order guidance to `docs/workflows.md`.
  - Update `skills/workflow/SKILL.md` so `workflow` creates or refreshes the guide on the spec-defined triggers, while pointing users to owning stage skills.
  - Decide whether `docs/changes/0001-skill-validator/` can move in this slice by checking references in tests, validators, specs, README, and workflow guidance.
  - If moving is not safe, add durable retained-fixture rationale in a local tracked surface and record the move target.
  - Keep `docs/examples/README.md` aligned with non-normative example wording if it is touched.
- Validation commands:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path skills/workflow/SKILL.md --path docs/examples/README.md --path specs/project-artifact-location-guide-and-examples-surface.md --path docs/plans/2026-05-13-project-artifact-location-guide-and-examples-surface.md --path docs/plan.md --path docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/change.yaml`
  - `git diff --check -- docs/workflows.md skills/workflow/SKILL.md docs/examples docs/changes/0001-skill-validator docs/plans/2026-05-13-project-artifact-location-guide-and-examples-surface.md docs/plan.md docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording`
- Expected observable result: users can find artifact locations in `docs/workflows.md`, `workflow` owns guide refresh behavior, examples remain non-normative, and the skill-validator fixture either moves safely or has explicit retained-fixture rationale.
- Commit message: `M1: add project artifact map and fixture rationale`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - Current Handoff Summary updated to `review-requested` for M1
  - M1 handed off to `code-review`
  - after clean M1 review, M1 marked `closed` and Current Handoff Summary advanced to M2
  - milestone committed
- Risks:
  - `docs/workflows.md` can become too large.
  - Moving `docs/changes/0001-skill-validator/` can break validator fixtures and historical references.
- Rollback/recovery:
  - Keep the table concise and move exact shape detail back to specs if the guide grows too large.
  - Retain `docs/changes/0001-skill-validator/` with rationale if references are too coupled for a safe move.

### M2. Stage Skill Lookup Wording And Static Proof

- Milestone state: closed
- Goal: update canonical stage skills with concise project-guide lookup wording that respects `R2` precedence without encouraging broad spec/schema path scans.
- Requirements: `R2`-`R2g`, `R5`-`R5g`, `R9`-`R10b`, `R12`-`R12b`
- Files/components likely touched:
  - `skills/proposal/SKILL.md`
  - `skills/spec/SKILL.md`
  - `skills/architecture/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/test-spec/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/explain-change/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/pr/SKILL.md`
  - shared templates only if the repo already has an appropriate shared block owner
  - `scripts/test-skill-validator.py`
  - `scripts/validate-skills.py` only if static validation logic belongs there
- Dependencies: M1 artifact-map language stable enough for skills to point to it.
- Tests to add/update:
  - Static checks that affected public skills mention project workflow guide/artifact locations when placement matters.
  - Static checks that public skills discourage broad authoritative-document searches solely to find paths.
  - Static checks that lookup wording includes known governing spec/schema constraints when directly relevant and remains subordinate to source-rank precedence.
  - Existing portability checks should continue to reject RigorLoop-internal validator paths in public skill text.
- Implementation steps:
  - Add concise lookup wording to skills that create or locate lifecycle artifacts.
  - Keep individual skill defaults short and skill-local.
  - Avoid copying the full artifact-location table into every skill.
  - Preserve review-recording exact-shape pointers to `specs/formal-review-recording.md` in repo-owned surfaces while keeping public skill text project-portable where required.
  - Add or update static tests for the exact risk from SR-001: discovery order cannot bypass source-rank precedence and must not cause broad authority scans.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/project-artifact-location-guide-and-examples-surface.md --path docs/plans/2026-05-13-project-artifact-location-guide-and-examples-surface.md --path docs/plan.md --path docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/change.yaml`
  - `git diff --check -- skills scripts docs/plans/2026-05-13-project-artifact-location-guide-and-examples-surface.md docs/plan.md docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording`
- Expected observable result: public skills stay concise, use the project workflow guide as the path index, obey known governing constraints, and static checks protect against reintroducing duplicated path tables or broad search instructions.
- Commit message: `M2: add token-efficient artifact lookup guidance`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - Current Handoff Summary updated to `review-requested` for M2
  - M2 handed off to `code-review`
  - after clean M2 review, M2 marked `closed` and Current Handoff Summary advanced to M3
  - milestone committed
- Risks:
  - Updating too many skills can bloat public skill text.
  - Shared wording can become inconsistent if copied manually.
- Rollback/recovery:
  - Narrow the affected skill set to only skills that actually place artifacts.
  - Use a shared block only if it reduces drift without exposing repository-maintainer internals in public skills.

### M3. Examples Routing And Lifecycle Validation

- Milestone state: closed
- Goal: add repository-owned selector, lifecycle, and review-artifact validation for `docs/examples/**`, retained fixture behavior, and artifact-map lookup invariants.
- Requirements: `R6`-`R8a`, `R11`-`R11d`, acceptance criteria for static/test coverage
- Files/components likely touched:
  - `scripts/validation_selection.py`
  - `scripts/test-select-validation.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `scripts/test-review-artifact-validator.py`
  - `scripts/test-change-metadata-validator.py`
  - `scripts/test-skill-validator.py`
  - `tests/fixtures/**` if new fixtures are needed
  - `docs/examples/**`
  - `docs/changes/0001-skill-validator/**` if retained or moved
- Dependencies: M1 path decisions and M2 skill wording stable.
- Tests to add/update:
  - Selector coverage for `docs/examples/**` as documentation/example content.
  - Lifecycle coverage proving `docs/examples/plans/example-plan.md` is not active plan state.
  - Review-artifact or lifecycle coverage proving `docs/examples/formal-review-recording/**` does not trigger active review closeout.
  - Retained-fixture coverage proving `docs/changes/0001-skill-validator/` either moved safely or carries explicit rationale.
  - Static proof that shared skill lookup wording references source-rank precedence and discourages broad path searches.
- Implementation steps:
  - Inspect current selector classification for `docs/examples/**` and add missing tests before logic changes.
  - Add or update lifecycle tests for plan examples and formal review examples.
  - Add retained-fixture tests or validation checks based on the M1 decision.
  - Ensure test fixtures do not accidentally make `docs/examples/**` active lifecycle state unless explicitly opted in.
  - Update validation command selection if changed paths need new selected-check coverage.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/examples/README.md --path docs/examples/plans/example-plan.md --path specs/project-artifact-location-guide-and-examples-surface.md --path docs/plans/2026-05-13-project-artifact-location-guide-and-examples-surface.md --path docs/plan.md`
  - `git diff --check -- scripts tests docs/examples docs/changes/0001-skill-validator docs/plans/2026-05-13-project-artifact-location-guide-and-examples-surface.md docs/plan.md`
- Expected observable result: repository tests prove examples are not active lifecycle state, formal review examples do not trigger closeout, retained fixture behavior is explicit, and lookup wording is statically protected.
- Commit message: `M3: validate examples routing and lookup invariants`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - Current Handoff Summary updated to `review-requested` for M3
  - M3 handed off to `code-review`
  - after clean M3 review, M3 marked `closed` and Current Handoff Summary advanced to M4
  - milestone committed
- Risks:
  - Existing validators may already partially cover examples, causing duplicate assertions.
  - Retained-fixture validation can become too path-specific.
- Rollback/recovery:
  - Prefer one primary validator/test per invariant and alignment tests only for distinct risk.
  - Keep retained-fixture checks narrow and tied to the approved exception.

### M4. Generated Output Refresh And Final Milestone Review

- Milestone state: closed
- Goal: refresh generated skill and adapter output after canonical skill changes, validate generated output, update lifecycle evidence, and hand off the final implementation milestone to `code-review`.
- Requirements: `R10`-`R10b`, lifecycle closeout requirements, all implementation milestone closeout obligations
- Files/components likely touched:
  - generated skill output under `.codex/skills/` only if local runtime mirror regeneration is intentionally part of the environment and remains untracked
  - `dist/adapters/**`
  - `docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/**`
  - `docs/plans/2026-05-13-project-artifact-location-guide-and-examples-surface.md`
  - `docs/plan.md`
  - final explain-change and verify artifacts if triggered by downstream stages
- Dependencies: M1-M3 closed.
- Tests to add/update: no new tests expected unless generated-output validation reveals missing adapter or manifest coverage.
- Implementation steps:
  - Run canonical skill generation checks.
  - Regenerate or check adapter output for version `0.1.1` after canonical skill edits.
  - Run adapter validation and distribution tests.
  - Update change metadata and plan validation notes with actual commands.
  - Update Current Handoff Summary to `review-requested` for M4 after implementation and targeted validation pass.
  - Hand M4 to `code-review` as its own final implementation milestone.
  - After clean M4 review and any required review-resolution closeout, prepare downstream `explain-change`, `verify`, and `pr` gates.
- Validation commands:
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-13-project-artifact-location-guide-and-examples-surface.md --path specs/project-artifact-location-guide-and-examples-surface.md --path docs/plans/2026-05-13-project-artifact-location-guide-and-examples-surface.md --path docs/plan.md --path docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/change.yaml`
  - `git diff --check -- skills scripts tests docs/workflows.md docs/examples docs/changes/0001-skill-validator dist/adapters docs/plans/2026-05-13-project-artifact-location-guide-and-examples-surface.md docs/plan.md docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording`
- Expected observable result: generated public outputs are current where required, validation passes, change-local evidence is current, and M4 is ready for its own `code-review` handoff.
- Commit message: `M4: refresh generated artifact lookup output`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - Current Handoff Summary updated to `review-requested` for M4
  - M4 handed off to `code-review`
  - after clean M4 review and any required review-resolution closeout, M4 marked `closed` and Current Handoff Summary advanced to `explain-change`
  - milestone committed
- Risks:
  - Generated adapter output may include broad diffs.
  - `.codex/skills/` is ignored local runtime state and should not be treated as tracked release evidence.
- Rollback/recovery:
  - Revert generated output and rerun generation after canonical skill changes are corrected.
  - If adapter validation exposes unrelated baseline debt, record the debt separately and keep this change scoped.

## Validation plan

Run milestone-specific validation first. Before final PR handoff, run targeted validation selected for changed paths through the repository-owned wrapper when the plan or test spec requires it:

```bash
python scripts/select-validation.py --mode explicit --path <changed-path> [...]
bash scripts/ci.sh --mode explicit --path <changed-path> [...]
```

Expected direct validation commands across this plan:

```bash
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/test-select-validation.py
python scripts/test-artifact-lifecycle-validator.py
python scripts/test-review-artifact-validator.py
python scripts/test-change-metadata-validator.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version 0.1.1 --check
python scripts/validate-adapters.py --version 0.1.1
python scripts/test-adapter-distribution.py
python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording
python scripts/validate-change-metadata.py docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/change.yaml
python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-13-project-artifact-location-guide-and-examples-surface.md --path specs/project-artifact-location-guide-and-examples-surface.md --path docs/plans/2026-05-13-project-artifact-location-guide-and-examples-surface.md --path docs/plan.md --path docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/change.yaml
git diff --check --
```

Broad smoke is not planned by default. Add it only if selector output, the test spec, review-resolution, release metadata, or another authoritative trigger requires it.

## Risks and recovery

- Risk: `docs/workflows.md` becomes an under-specified schema surface.
  - Recovery: keep the table to default locations and owning skills; move shape rules back to governing specs or schemas.
- Risk: skill wording grows too much across many public skills.
  - Recovery: use concise shared wording and one skill-local default path line.
- Risk: `docs/changes/0001-skill-validator/` move breaks tests or historical references.
  - Recovery: retain it with explicit rationale and schedule a follow-up move only when coupling is removed.
- Risk: generated output introduces broad adapter diffs.
  - Recovery: review canonical skill diffs first, regenerate deterministically, and validate adapter output before closeout.
- Risk: validation becomes duplicated across selector, lifecycle, review-artifact, and skill tests.
  - Recovery: choose one primary proof for each invariant and keep alignment tests narrow.

## Dependencies

- Approved spec and closed `spec-review` findings.
- Test spec must be authored after this plan passes `plan-review` and before implementation unless the user explicitly invokes isolated implementation.
- Generated output refresh depends on canonical skill changes from M2.
- Final lifecycle closeout depends on all in-scope implementation milestones being implemented, code-reviewed, closed, and review-resolution remaining closed.

## Progress

- [x] 2026-05-13: Proposal accepted after clean `proposal-review-r1`.
- [x] 2026-05-13: Spec drafted and approved after `spec-review-r2`; SR-001 closed.
- [x] 2026-05-13: Plan created and `docs/plan.md` index updated.
- [x] 2026-05-13: Plan revised after `plan-review-r1` PR-001 to require per-milestone `code-review` handoffs.
- [x] 2026-05-13: Plan approved after `plan-review-r2`; PR-001 closed.
- [x] 2026-05-13: Test spec created and activated for implementation.
- [x] 2026-05-13: M1. Workflow Artifact Map And Retained Fixture Rationale closed after clean `code-review-r1`.
- [x] 2026-05-13: M2. Stage Skill Lookup Wording And Static Proof closed after clean `code-review-r2`.
- [x] 2026-05-13: M3. Examples Routing And Lifecycle Validation closed after clean `code-review-r3`.
- [x] 2026-05-13: M4. Generated Output Refresh And Final Milestone Review closed after clean `code-review-r4`.

## Decision log

- 2026-05-13: Use four implementation milestones. Rationale: separates user-facing artifact-map docs, public skill wording, validation proof, and generated-output closeout into reviewable slices.
- 2026-05-13: Do not require architecture before this plan. Rationale: the approved spec defines workflow guidance, skills, examples, and validation behavior with no runtime architecture or data-flow change; return to `architecture` if plan review identifies a boundary decision.
- 2026-05-13: Treat `docs/changes/0001-skill-validator/` movement as an implementation-slice decision. Rationale: the spec allows either safe move with all references updated or retained-fixture rationale when coupling remains.
- 2026-05-13: Keep M1-M4 as separate implementation milestones with per-milestone `code-review` gates. Rationale: the plan is milestone-based and repository workflow requires implementation and code review to repeat for each in-scope implementation milestone.
- 2026-05-13: Retain `docs/changes/0001-skill-validator/` for M1. Rationale: existing specs, docs, validators, and historical references still cite the active-looking path, so this slice records retained-fixture rationale instead of moving it.
- 2026-05-13: Apply concise artifact-placement wording directly to affected canonical public skills for M2. Rationale: this keeps the public behavior explicit now while leaving generated adapter refresh to M4.
- 2026-05-13: Treat M3 as validation-proof-only. Rationale: selector and lifecycle behavior already classified examples correctly; this slice adds repository-owned regression coverage and explicit validation evidence instead of changing runtime validation logic.
- 2026-05-13: Regenerate tracked public adapter output for M4. Rationale: canonical public skill changes from M1 and M2 made the version `0.1.1` adapter output stale; generated output remains derived from canonical `skills/` sources and was refreshed with repository generation scripts.

## Surprises and discoveries

- M1: `docs/examples/README.md`, `AGENTS.md`, and `CONSTITUTION.md` already align with the approved M1 contract and were left unchanged.
- M1: lifecycle validation surfaced stale repository-integration wording in `docs/workflows.md`; it was corrected in the touched workflow guide.
- M2: Current Handoff Summary contained a stale duplicate `Current milestone: M1` line above the M2 state after M1 closeout; this state-sync issue was corrected in the active plan.
- M2: No shared artifact-placement template existed for public skills; the milestone used one concise repeated block and did not copy the artifact-location table into skills.
- M3: Existing selector behavior already classified `docs/examples/**` as examples and selected no lifecycle or review-artifact checks for those paths.
- M3: Existing lifecycle behavior already ignored example paths as active lifecycle artifacts; new tests now cover formal-review examples and the retained fixture rationale.
- M4: `python scripts/build-skills.py --check` passed before adapter regeneration, but `python scripts/build-adapters.py --version 0.1.1 --check` and `python scripts/validate-adapters.py --version 0.1.1` reported 42 stale generated adapter files across Claude, Codex, and opencode. Regenerating adapters resolved the drift.

## Validation notes

- 2026-05-13: Planning validation passed after plan creation, `plan-review-r1` recording, PR-001 plan revision, and `plan-review-r2` recording.
- 2026-05-13: M1 proof-first failure observed: `python scripts/test-skill-validator.py` failed because `docs/workflows.md` lacked the artifact map and source-rank sections, `skills/workflow/SKILL.md` lacked guide refresh trigger wording, and `docs/changes/0001-skill-validator/README.md` did not exist.
- 2026-05-13: M1 validation passed: `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path skills/workflow/SKILL.md --path docs/examples/README.md --path specs/project-artifact-location-guide-and-examples-surface.md --path specs/project-artifact-location-guide-and-examples-surface.test.md --path docs/plans/2026-05-13-project-artifact-location-guide-and-examples-surface.md --path docs/plan.md --path docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/change.yaml`; `python scripts/validate-change-metadata.py docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/change.yaml`; `git diff --check -- docs/workflows.md skills/workflow/SKILL.md docs/examples docs/changes/0001-skill-validator scripts/test-skill-validator.py specs/project-artifact-location-guide-and-examples-surface.test.md docs/plans/2026-05-13-project-artifact-location-guide-and-examples-surface.md docs/plan.md docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording`.
- 2026-05-13: Clean M1 code review recorded in `docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/reviews/code-review-r1.md`; M1 closed and Current Handoff Summary advanced to M2.
- 2026-05-13: M2 proof-first failure observed: `python scripts/test-skill-validator.py` failed for the affected public skills because the shared artifact-placement lookup wording was not present.
- 2026-05-13: M2 validation passed: `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`; `python scripts/validate-change-metadata.py docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/project-artifact-location-guide-and-examples-surface.md --path docs/plans/2026-05-13-project-artifact-location-guide-and-examples-surface.md --path docs/plan.md --path docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/change.yaml`; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording`; `git diff --check -- skills scripts docs/plans/2026-05-13-project-artifact-location-guide-and-examples-surface.md docs/plan.md docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording`.
- 2026-05-13: Clean M2 code review recorded in `docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/reviews/code-review-r2.md`; M2 closed and Current Handoff Summary advanced to M3.
- 2026-05-13: M3 validation-proof tests added for expanded `docs/examples/**` selector coverage, formal-review example lifecycle behavior, retained fixture rationale, and review-artifact non-selection for formal review examples. The added tests passed immediately because the existing implementation already had the required behavior.
- 2026-05-13: M3 validation passed: `python scripts/test-select-validation.py`; `python scripts/test-artifact-lifecycle-validator.py`; `python scripts/test-review-artifact-validator.py`; `python scripts/test-change-metadata-validator.py`; `python scripts/test-skill-validator.py`; `python scripts/select-validation.py --mode explicit --path docs/examples/README.md --path docs/examples/plans/example-plan.md --path docs/examples/formal-review-recording/clean-review-receipt-root.md --path docs/examples/formal-review-recording/material-finding-location-examples.md`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/examples/README.md --path docs/examples/plans/example-plan.md --path docs/examples/formal-review-recording/clean-review-receipt-root.md --path docs/examples/formal-review-recording/material-finding-location-examples.md --path specs/project-artifact-location-guide-and-examples-surface.md --path docs/plans/2026-05-13-project-artifact-location-guide-and-examples-surface.md --path docs/plan.md`; `git diff --check -- scripts tests docs/examples docs/changes/0001-skill-validator docs/plans/2026-05-13-project-artifact-location-guide-and-examples-surface.md docs/plan.md`.
- 2026-05-13: Clean M3 code review recorded in `docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/reviews/code-review-r3.md`; M3 closed and Current Handoff Summary advanced to M4.
- 2026-05-13: M4 proof-first adapter drift observed before regeneration: `python scripts/build-adapters.py --version 0.1.1 --check` failed with 42 stale generated adapter files; `python scripts/validate-adapters.py --version 0.1.1` failed on the same stale generated output.
- 2026-05-13: M4 generated adapter output refreshed with `python scripts/build-adapters.py --version 0.1.1`.
- 2026-05-13: M4 validation passed: `python scripts/build-skills.py --check`; `python scripts/build-adapters.py --version 0.1.1 --check`; `python scripts/validate-adapters.py --version 0.1.1`; `python scripts/test-adapter-distribution.py`; `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`; `python scripts/test-select-validation.py`; `python scripts/test-artifact-lifecycle-validator.py`; `python scripts/test-review-artifact-validator.py`; `python scripts/test-change-metadata-validator.py`; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording`; `python scripts/validate-change-metadata.py docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/change.yaml`.
- 2026-05-13: Clean M4 code review recorded in `docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/reviews/code-review-r4.md`; M4 closed and Current Handoff Summary advanced to `explain-change`.

## Outcome and retrospective

- Pending final closeout. Keep this section final-only while the plan is active.

## Readiness

- See `Current Handoff Summary`.
- Readiness is not Done; implementation milestones are closed and the next stage is `explain-change`.
