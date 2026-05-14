# Cost-Bounded Rigor M3 Validation-Budget Guidance Plan

- Status: active
- Owner: maintainers
- Start date: 2026-05-14
- Last updated: 2026-05-14
- Related issue or PR: none yet
- Supersedes: none
- selected_workflow_contract: standard
- broad_smoke_required: false
- broad_smoke_reason: The planned slice is validation-budget guidance and static proof. It should not change release behavior, adapter packaging, lifecycle token-cost summaries, dynamic benchmark requirements, hard token gates, or broad-smoke triggers unless a later approved test spec explicitly broadens the scope.

## Purpose / big picture

Plan the M3 cost-bounded-rigor slice after PR #55 merged the M2 selected skill reminders.

The approved M3 spec defines validation-budget behavior: stages should validate the smallest sufficient surface that proves the current change while preserving mandatory broad-smoke, release, review-resolution, test-spec, active-plan, and selector triggers.

This plan keeps the implementation narrow. The intended first implementation milestone audits the current owner surfaces, updates only the smallest guidance or static proof needed, and records no-change rationale for surfaces that already satisfy the approved M3 contract.

## Source artifacts

- Proposal: [Cost-Bounded Rigor After Single-Source Skills and Follow-Up Routing](../proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md), accepted. The rollout names M3 as validation-budget guidance.
- M3 spec: [Cost-Bounded Rigor M3 Validation-Budget Guidance](../../specs/cost-bounded-rigor-m3-validation-budget-guidance.md), approved after clean [spec-review-r1](../changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/reviews/spec-review-r1.md).
- Current test spec: [Cost-Bounded Rigor M3 Validation-Budget Guidance Test Spec](../../specs/cost-bounded-rigor-m3-validation-budget-guidance.test.md), active and maintainer-approved by direct request on 2026-05-14.
- Architecture: not required. `spec-review-r1` found no runtime architecture, persistence, external API, security-boundary, release packaging, adapter packaging, or hard-to-reverse design change.
- Completed M2 plan: [Cost-Bounded Rigor M2 Selected Skill Reminders](2026-05-14-cost-bounded-rigor-m2-selected-skill-reminders.md), done after merged PR #55.
- Change-local pack: [docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance](../changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/) records M3 spec and review evidence.
- Project map: [docs/project-map.md](../project-map.md) orients the repository layout. This plan relies on direct source inspection for touched workflow and validation surfaces.

## Context and orientation

Current validation behavior is split across:

- `docs/workflows.md`, which owns contributor-facing validation guidance and already says selector-selected targeted proof is the first layer and broad smoke is trigger-driven;
- `scripts/validation_selection.py`, `scripts/select-validation.py`, and `scripts/ci.sh`, which own executable check selection and wrapper execution;
- `scripts/test-select-validation.py`, which owns selector and workflow-routing regression proof, including existing validation-layering expectations;
- stage skills such as `workflow`, `implement`, and `verify`, which already contain concise targeted-validation and broad-smoke reminders;
- active plans, test specs, review-resolution records, and release metadata, which can require stronger validation for a specific change.

M3 should not turn this into a broad rewrite. Implementation should first audit these owner surfaces, then either record no-change rationale or add the smallest missing owner-surface guidance and static proof.

## Non-goals

- Do not implement lifecycle token-cost summaries.
- Do not add hard token gates.
- Do not change release validation or adapter packaging.
- Do not reintroduce tracked generated public adapter skill bodies.
- Do not require dynamic benchmark comparison.
- Do not implement progressive-loading follow-through.
- Do not rewrite every stage skill.
- Do not weaken formal review, review-resolution, verify, PR, material-finding, release, generated-output, or broad-smoke rules.
- Do not make skill prose the executable source of truth for selected checks.
- Do not change selector behavior unless the approved M3 test spec explicitly requires selector regression coverage for a focused behavior gap.

## Requirements covered

| Requirement IDs | Planned implementation surface |
|---|---|
| `R1`-`R4` | `docs/workflows.md` guidance or no-change rationale, plus validation-layering static proof. |
| `R5`-`R7` | Owner-surface audit; `docs/workflows.md` and proof updates only where needed. |
| `R8`-`R10` | Explicit selector-behavior decision: unchanged with rationale unless the M3 test spec broadens scope. |
| `R11`-`R13` | Stage-skill audit and no-change rationale; no `implement`, `code-review`, or `verify` edits planned in the first milestone. |
| `R14`-`R16` | Scope guardrails in plan, test spec, implementation review, and final validation. |
| `R17`-`R18` | Plan/test-spec/verify evidence for explicit-path or wrapper-selected validation and trigger matching. |
| `R19` | Tracked no-change rationale for owner surfaces that already satisfy the contract. |

## Current Handoff Summary

- Current milestone: M1. Owner-surface audit and minimal validation-budget guidance
- Current milestone state: closed
- Last reviewed milestone: M1. Owner-surface audit and minimal validation-budget guidance
- Review status: `code-review-m1-r1` clean-with-notes, no material findings
- Remaining in-scope implementation milestones: none
- Next stage: pr
- Final closeout readiness: ready for PR handoff, not final Done
- Reason final closeout is or is not ready: M1 implementation, code-review, explain-change, and local final verify are complete. The branch is ready for PR handoff, but the PR stage is not complete and hosted CI has not been observed.

## Milestones

### M0. Plan creation and spec status settlement

- Milestone state: closed
- Goal: Normalize the cleanly reviewed M3 spec to approved, create the active M3 plan, and register it in `docs/plan.md`.
- Requirements: M3 spec `R1`-`R19` as planning source; spec-review clean approval before reliance.
- Files/components likely touched:
  - `specs/cost-bounded-rigor-m3-validation-budget-guidance.md`
  - `docs/plans/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance.md`
  - `docs/plan.md`
  - `docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/change.yaml`
- Dependencies:
  - accepted proposal;
  - merged M2 PR #55;
  - clean `spec-review-r1`;
  - no material spec-review findings.
- Tests to add/update:
  - none during plan creation.
- Implementation steps:
  - Normalize the M3 spec status from `draft` to `approved`.
  - Create this plan.
  - Add the active M3 plan entry to `docs/plan.md`.
  - Update change metadata with plan and validation evidence.
- Validation commands:
  - `python scripts/select-validation.py --mode explicit --path specs/cost-bounded-rigor-m3-validation-budget-guidance.md --path docs/plans/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance.md --path docs/plan.md --path docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/change.yaml --path docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/review-log.md --path docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/reviews/spec-review-r1.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/cost-bounded-rigor-m3-validation-budget-guidance.md --path docs/plans/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance.md --path docs/plan.md --path docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/change.yaml --path docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/review-log.md --path docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/reviews/spec-review-r1.md`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path specs/cost-bounded-rigor-m3-validation-budget-guidance.md --path docs/plans/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance.md --path docs/plan.md --path docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/change.yaml --path docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/review-log.md --path docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/reviews/spec-review-r1.md`
  - `git diff --check --`
- Expected observable result: The M3 spec is approved, this plan is active, `docs/plan.md` points to it, and the next stage is `plan-review`.
- Commit message: `Plan M3 validation-budget guidance`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed, when this planning commit is created
- Risks:
  - planning could accidentally authorize selector behavior changes before test-spec proof exists;
  - stale spec status could block downstream reliance.
- Rollback/recovery:
  - revert plan index and plan body if plan-review rejects the plan shape;
  - return the spec to `draft` only if review evidence is invalidated by a later formal review.

### M1. Owner-surface audit and minimal validation-budget guidance

- Milestone state: closed
- Goal: Implement the smallest guidance or static-proof update needed for M3 validation-budget behavior, after auditing owner surfaces.
- Requirements: M3 spec `R1`-`R19`.
- Files/components likely touched:
  - `docs/workflows.md`
  - `scripts/test-select-validation.py`
  - `docs/plans/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance.md`
  - `docs/plan.md`
  - `docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/change.yaml`
- Files/components explicitly not planned for M1 unless the approved test spec requires plan revision first:
  - `scripts/validation_selection.py`
  - `scripts/select-validation.py`
  - `scripts/ci.sh`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - release and adapter packaging surfaces
- Dependencies:
  - M0 closed;
  - plan-review approval for this plan;
  - active M3 test spec before implementation;
  - no later accepted artifact broadening M3 into lifecycle token-cost reporting, release packaging, adapter packaging, dynamic benchmarks, hard token gates, or progressive-loading work.
- Tests to add/update:
  - Add or update static proof in `scripts/test-select-validation.py` if `docs/workflows.md` wording changes or if the test spec requires static proof for owner-surface split.
  - Add selector regression tests only if the approved test spec explicitly authorizes selector behavior changes.
  - Do not add brittle exact-sentence checks when stable behavior cues are sufficient.
- Implementation steps:
  - Audit `docs/workflows.md`, validation selector behavior, wrapper behavior, and validation-related stage skill reminders against M3 `R1`-`R19`.
  - Record each owner surface as edited, unchanged with rationale, or deferred with owner/slice.
  - If needed, add a concise validation-budget ownership or targeted-validation clarification to `docs/workflows.md`.
  - Keep selector behavior unchanged unless the active M3 test spec requires a focused selector change.
  - Keep stage skills unchanged unless the active M3 test spec identifies a direct contradiction or missing local cue and this plan is revised to include that surface.
  - Update focused static proof and lifecycle evidence.
  - Record why broad smoke is or is not required for this implementation.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path scripts/test-select-validation.py --path docs/plans/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance.md --path docs/plan.md --path docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path docs/workflows.md --path scripts/test-select-validation.py --path docs/plans/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance.md --path docs/plan.md --path docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/cost-bounded-rigor-m3-validation-budget-guidance.md --path docs/plans/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance.md --path docs/plan.md --path docs/workflows.md --path docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/change.yaml`
  - `git diff --check --`
- Expected observable result:
  - M3 owner-surface decisions are tracked;
  - `docs/workflows.md` either already satisfies or gains the minimal validation-budget guidance needed;
  - static proof protects the targeted-validation and broad-smoke trigger contract without changing selector behavior;
  - no release, adapter, token-cost, dynamic benchmark, hard-token-gate, or progressive-loading scope is added.
- Commit message: `M1: add validation-budget guidance`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed, when this implementation commit is created
- Risks:
  - static proof could become brittle by freezing exact prose;
  - guidance could imply broad smoke is optional when an authoritative trigger requires it;
  - implementation could drift into selector behavior without test-spec authority.
- Rollback/recovery:
  - reduce static proof to stable behavior cues;
  - restore stronger trigger wording if review finds under-validation risk;
  - split selector behavior changes into a plan revision or later slice with selector regression coverage.

## Validation plan

Before implementation:

- M3 spec is approved.
- This plan is reviewed by `plan-review`.
- An active M3 test spec is created and approved or otherwise ready according to workflow state.

During implementation:

- Run focused static proof first where feasible.
- Run selector-selected validation for changed paths through `scripts/select-validation.py` and `bash scripts/ci.sh --mode explicit`.
- Run broad smoke only if the active plan, test spec, review-resolution, release metadata, selector mode, or explicit flag requires it.

Final closeout:

- Run `code-review`.
- Resolve material findings through `review-resolution` if triggered.
- Record `explain-change`.
- Run `verify` to check that actual validation evidence matches plan, test spec, review-resolution, and release metadata triggers.
- Use `pr` only after verify establishes branch readiness.

## Risks and recovery

- Risk: M3 duplicates existing validation-layering guidance. Recovery: record no-change rationale and avoid wording churn.
- Risk: M3 weakens broad-smoke or release validation by overemphasizing targeted checks. Recovery: preserve trigger wording and add review/test coverage for broad-smoke triggers.
- Risk: M3 silently changes selector behavior. Recovery: require explicit plan/test-spec scope and selector regression tests before executable selector changes.
- Risk: dirty worktree guidance is misread as permission to skip lifecycle validation. Recovery: keep explicit-path and wrapper-selected validation requirements visible.

## Dependencies

- PR #55 merged M2 selected skill reminders.
- M3 spec approved by clean `spec-review-r1`.
- Plan-review approved this plan in `plan-review-r1`.
- Active test spec exists and must be followed during implementation.

## Progress

- 2026-05-14: PR #55 merged M2 selected skill reminders.
- 2026-05-14: M3 spec drafted at `specs/cost-bounded-rigor-m3-validation-budget-guidance.md`.
- 2026-05-14: clean `spec-review-r1` recorded with no material findings.
- 2026-05-14: M3 spec status normalized to `approved`; active M3 plan created; next stage is `plan-review`.
- 2026-05-14: clean `plan-review-r1` recorded with no material findings; active M3 test spec created at `specs/cost-bounded-rigor-m3-validation-budget-guidance.test.md`; next stage is `implement`.
- 2026-05-14: active M3 test spec maintainer-approved by direct user request; next stage remains `implement`.
- 2026-05-14: M1 implementation started with static proof for validation owner-surface wording before editing `docs/workflows.md`.
- 2026-05-14: M1 implementation added validation owner-surface guidance to `docs/workflows.md`, updated stable static proof in `scripts/test-select-validation.py`, recorded owner-surface rationale, and is ready for `code-review`.
- 2026-05-14: clean `code-review-m1-r1` recorded with no material findings; M1 is closed and next stage is `explain-change`.
- 2026-05-14: Explain-change recorded at `docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/explain-change.md`; next stage is `verify`.
- 2026-05-14: Final local verify passed over the full changed artifact set, including selected CI, closeout-mode review validation, direct selector regression proof, artifact lifecycle validation, change metadata validation, and `git diff --check --`; branch is ready for PR handoff and next stage is `pr`.

## Decision log

- 2026-05-14: Keep M3 guidance-first and selector-preserving unless test-spec explicitly broadens scope. Reason: current selector behavior already supports targeted validation, broad-smoke source attribution, and trigger detection; unnecessary executable changes would increase risk.
- 2026-05-14: Do not plan edits to `implement`, `code-review`, or `verify` in M1. Reason: current skills already contain targeted-validation and broad-smoke reminders, and M3 `R13` requires a specific plan-scoped gap before editing those skills.
- 2026-05-14: Use `scripts/test-select-validation.py` as the likely static proof surface for workflow validation guidance. Reason: it already owns validation-layering and selector workflow-routing proof.
- 2026-05-14: Do not require dynamic benchmark comparison or release/adapter validation for M3 test proof. Reason: the active test spec keeps this slice guidance/static-proof focused unless a later approved artifact broadens scope.
- 2026-05-14: Keep selector behavior unchanged for M1. Reason: the implementation is guidance-only, and `scripts/test-select-validation.py` proved owner-surface wording and existing broad-smoke trigger behavior without changing selected-check coverage.

## M1 Owner-Surface Audit

| Surface | Outcome | Rationale |
|---|---|---|
| `docs/workflows.md` | edited | Added the validation owner-surface split and guidance-only guardrail required by M3 `R5`-`R7`. |
| `scripts/test-select-validation.py` | edited | Added stable static cues for the owner-surface split without freezing a full exact sentence. |
| `scripts/validation_selection.py` | unaffected with rationale | Selector behavior already supports targeted validation, broad-smoke source attribution, unclassified-path blocking, and explicit-path validation. M1 does not change executable check selection. |
| `scripts/select-validation.py` | unaffected with rationale | CLI wrapper behavior remains aligned with current selector behavior; M1 adds guidance only. |
| `scripts/ci.sh` | unaffected with rationale | CI wrapper behavior and command exit semantics remain unchanged; selected CI still executes the selected checks. |
| `skills/workflow/SKILL.md` | unaffected with rationale | Existing wording already contains concise targeted-proof, broad-smoke, manual-proof, and source-attribution reminders. |
| `skills/implement/SKILL.md` | unaffected with rationale | Existing wording already tells implementation to inspect selected checks, run targeted proof, and run broad validation only when an authoritative trigger requires it. |
| `skills/code-review/SKILL.md` | unaffected with rationale | Existing wording already checks targeted proof, broad smoke, selected checks, and direct proof without needing a full validation-budget rule. |
| `skills/verify/SKILL.md` | unaffected with rationale | Existing wording already requires verify to check targeted proof, broad validation triggers, release metadata, and `broad_smoke_required` evidence. |
| Release, adapter, generated-output, token-cost, and progressive-loading surfaces | unaffected with rationale | M3 M1 does not touch release or adapter packaging, generated public adapter output, lifecycle token-cost summaries, dynamic benchmarks, hard token gates, or progressive-loading work. |

## Surprises and discoveries

- Existing `docs/workflows.md`, `workflow`, `implement`, and `verify` surfaces already contain targeted-validation and broad-smoke guidance; M3 likely needs ownership clarification and proof rather than broad new behavior.
- Selector behavior and CI wrapper behavior did not need executable changes; the selected path validation for this diff keeps `broad_smoke_required` false.

## Validation notes

- 2026-05-14: Plan creation validation passed after spec status settlement and plan-index update: `python scripts/select-validation.py --mode explicit ...`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance`, `python scripts/validate-change-metadata.py docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/change.yaml`, `bash scripts/ci.sh --mode explicit ...`, and `git diff --check --`.
- 2026-05-14: Test-spec authoring validation passed after creating the active M3 test spec and syncing lifecycle state: selected validation, review-artifact closeout, change metadata validation, artifact lifecycle validation, selected CI, and `git diff --check --`.
- 2026-05-14: Test-spec approval validation passed after recording direct maintainer approval and syncing lifecycle state: selected validation, artifact lifecycle validation, change metadata validation, selected CI, and `git diff --check --`.
- 2026-05-14: M1 red/green proof: `python scripts/test-select-validation.py ValidationSelectionTests.test_workflow_guidance_aligns_with_validation_layering_contract` failed before `docs/workflows.md` gained the owner-surface terms, then passed after the guidance edit.
- 2026-05-14: M1 selector regression passed: `python scripts/test-select-validation.py`.
- 2026-05-14: M1 selected validation passed for `docs/workflows.md`, `scripts/test-select-validation.py`, this plan, `docs/plan.md`, and change metadata. Selected checks were `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`; `broad_smoke_required` was false.
- 2026-05-14: M1 code-review recorded `clean-with-notes` with no material findings. Final closeout validation remains pending for `explain-change` and `verify`.
- 2026-05-14: M1 code-review recording validation passed: selected review-artifact/lifecycle/change-metadata checks, `python scripts/validate-review-artifacts.py --mode closeout ...`, change metadata validation, artifact lifecycle validation, selected CI, and `git diff --check --`.
- 2026-05-14: Explain-change validation passed after creating the durable rationale artifact: selected lifecycle and change-metadata checks, selected CI, and `git diff --check --`.
- 2026-05-14: Final verify selected CI passed over the full changed artifact set. Selected check IDs were `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`; `broad_smoke_required` was false.
- 2026-05-14: Final verify support checks passed: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance`, `python scripts/test-select-validation.py` (61 tests), `python scripts/validate-change-metadata.py docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/change.yaml`, artifact lifecycle validation for the full changed artifact set, and `git diff --check --`. Hosted CI was not observed.

## Outcome and retrospective

- Branch-ready for PR handoff after local final verify. The PR stage and hosted CI observation remain outside this verify result.

## Readiness

- See `Current Handoff Summary`.
- Ready for `pr`, not final lifecycle Done.
