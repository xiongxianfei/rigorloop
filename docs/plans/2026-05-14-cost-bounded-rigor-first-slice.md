# Cost-Bounded Rigor First Slice Plan

- Status: active
- Owner: maintainers
- Start date: 2026-05-14
- Last updated: 2026-05-14
- Related issue or PR: none yet
- Supersedes: none
- selected_workflow_contract: standard
- broad_smoke_required: false
- broad_smoke_reason: This first slice changes proposal/proposal-review guidance and `docs/workflows.md` evidence guidance. It does not change runtime behavior, release packaging, adapter packaging, validation-selector behavior, broad-smoke triggers, dynamic benchmarks, or hard token gates.

## Purpose / big picture

Implement the approved first slice of cost-bounded rigor so broad proposals classify scope before downstream reliance and agents start from bounded path/state evidence before broad reads.

The change should reduce workflow amplification without weakening formal review, verification, material-finding, release, or full-file-read safety rules.

## Source artifacts

- Proposal: [Cost-Bounded Rigor After Single-Source Skills and Follow-Up Routing](../proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md), accepted.
- Spec: [Cost-Bounded Rigor After Single-Source Skills and Follow-Up Routing](../../specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md), approved after clean spec-review.
- Spec review: [spec-review-r2](../changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/spec-review-r2.md), approved with no material findings.
- Architecture: not required by the spec or spec-review. This slice changes workflow documentation, proposal skill guidance, proposal-review skill guidance, and optional static proof only; it does not alter runtime architecture, APIs, persistence, deployment, security boundaries, or hard-to-reverse data flow.
- Test spec: [Cost-Bounded Rigor After Single-Source Skills and Follow-Up Routing Test Spec](../../specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.test.md), active and maintainer-approved on 2026-05-14.
- Change-local pack: [change.yaml](../changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml), with review records and review-resolution under the same change root.
- Project map: [docs/project-map.md](../project-map.md) exists as a living repository orientation reference. This plan still does not rely on project-map claims for runtime boundaries, persistence, service ownership, or data flow; its implementation orientation remains the accepted proposal, approved spec, current skill files, `docs/workflows.md`, and validation scripts.

## Context and orientation

First-slice implementation surfaces:

- `skills/proposal/SKILL.md` owns proposal authoring guidance and should gain scope-budget trigger, treatment, and table guidance without replacing existing initial-intent preservation.
- `skills/proposal-review/SKILL.md` owns proposal-review guidance and should gain checks for missing or misleading scope-budget classification in broad or multi-workstream proposals.
- `docs/workflows.md` owns the full project-local path, follow-up-routing, and bounded-evidence guide.
- `scripts/test-skill-validator.py` may receive focused static proof for stable guidance terms if needed by the test spec.
- `scripts/validate-skills.py` should remain unchanged unless existing validation ownership requires a structural check.

Affected-surface decisions:

- `CONSTITUTION.md` is intentionally unchanged because this slice does not change source-of-truth order, stage order, lifecycle synchronization, or a governance rule that is not already covered.
- `AGENTS.md` is intentionally unchanged because it already delegates detailed workflow behavior to the constitution, specs, and `docs/workflows.md`.
- `README.md` is not a cost-bounded first-slice behavior surface. Project-map alignment may mention `docs/project-map.md` for repository orientation, but README does not own proposal scope-budget or bounded-evidence guidance.
- `specs/rigorloop-workflow.md` is intentionally unchanged because the approved spec does not change stage order, obligation, handoff, downstream-blocking semantics, or lifecycle state rules.
- `specs/skill-contract.md` is intentionally unchanged because existing token-cost and bounded-evidence contract requirements already cover the needed skill behavior.
- `skills/workflow/SKILL.md` is intentionally unchanged in this first slice unless implementation evidence proves a short local reminder is necessary; `docs/workflows.md` owns the full rule.
- `skills/implement/SKILL.md` and `skills/code-review/SKILL.md` are out of scope unless a later accepted plan explicitly scopes progressive-loading follow-through.
- Generated public adapter skill bodies are intentionally unchanged because `skills/` is the authored source and generated public adapter bodies are release archive output for `v0.1.3` and later.

Validation context:

- Canonical skill source lives under `skills/`.
- When canonical skills change, `python scripts/build-skills.py --check` validates generated local mirror temp output.
- Generated `.codex/skills/` files are local runtime output and must not be treated as authored lifecycle inputs.
- Adapter archive or release validation is not part of this slice unless implementation unexpectedly touches release or adapter packaging surfaces.
- Dynamic token benchmarks are not required for proposal/evidence wording changes; record the no-dynamic-benchmark rationale during explain-change or verification.

## Non-goals

- Do not change validation-selector behavior.
- Do not change broad-smoke triggers.
- Do not add lifecycle token-cost summary artifacts.
- Do not require before/after dynamic benchmark comparison.
- Do not implement the full progressive-loading proposal for high-cost skills.
- Do not edit generated public adapter skill bodies.
- Do not change release validation or adapter packaging.
- Do not move deferred-work ownership into `project-map`.
- Do not weaken formal review, verify, PR, material-finding, release, or full-file-read rules.
- Do not introduce hard token thresholds.
- Do not create a new shared template solely for bounded-evidence wording.

## Requirements covered

| Requirement IDs | Planned implementation surface |
|---|---|
| `R1`, `R2` | Plan/test-spec scope guardrails, affected-surface decisions, and implementation review checklist. |
| `R3`-`R5c` | `skills/proposal/SKILL.md` scope-budget trigger, table, treatment, and definitions. |
| `R6`-`R7b` | `skills/proposal/SKILL.md` follow-up routing and single-authored-skill-source boundaries. |
| `R8`-`R10` | `skills/proposal-review/SKILL.md` checks for broad proposal classification and small-proposal exemption. |
| `R11`-`R11b` | Test-spec/static-proof guardrail that validators do not infer broadness; optional present-table checks only if scoped. |
| `R12`-`R15b` | `docs/workflows.md` bounded-evidence and path-search guidance with do-not-under-read escape. |
| `R16`-`R16b` | Keep full rule in `docs/workflows.md`; avoid a long repeated skill template. |
| `R17` | Implementation review checklist and no removal of safety-critical guidance. |
| `R18`-`R18b` | Validation notes and explain-change rationale for warning-only measurement and no dynamic benchmark. |
| `R19`-`R19b` | This plan, change metadata, and later explain-change record affected-surface updates, unaffected rationales, and deferrals. |

## Current Handoff Summary

- Current milestone: M1. Proposal scope-budget and bounded-evidence guidance
- Current milestone state: closed
- Last reviewed milestone: M1 implementation reviewed in `code-review-r1`
- Review status: code-review completed `clean-with-notes` in `code-review-r1` with no material findings
- Test-spec status: active and maintainer-approved on 2026-05-14
- Remaining in-scope implementation milestones: none
- Verify status: passed on tracked branch tip from a clean temporary worktree
- Next stage: pr
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: PR handoff is still required.

## Milestones

### M1. Proposal scope-budget and bounded-evidence guidance

- Milestone state: closed
- Goal: Add first-slice scope-budget behavior to proposal/proposal-review guidance and strengthen `docs/workflows.md` bounded-evidence path-search guidance while preserving safety-critical escape conditions.
- Requirements: `R1`-`R19b`
- Files/components likely touched:
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `docs/workflows.md`
  - `scripts/test-skill-validator.py`, only for focused static proof named by the test spec
  - `scripts/validate-skills.py`, only if existing skill validation structure needs a narrow check
  - `docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml`
  - this plan body and `docs/plan.md` for lifecycle state updates
- Dependencies:
  - plan-review approval
  - active test spec before implementation
  - no later accepted spec broadening this slice into selector, release, adapter, benchmark, lifecycle-token-summary, or progressive-loading work
- Tests to add/update:
  - test-spec must map each `MUST` to static proof, manual review evidence, or lifecycle validation.
  - Add focused static checks only for stable terms and required boundaries, such as `Scope budget`, treatment values, proposal-review `changes-requested` behavior, no broadness inference, bounded evidence, and do-not-under-read escape.
  - Do not add broad natural-language scoring.
  - Do not add validator inference that fails a proposal solely because no scope-budget table is present.
- Implementation steps:
  - Update `skills/proposal/SKILL.md` with concise scope-budget trigger, table, treatment values, and follow-up/single-source boundaries.
  - Preserve existing `Initial intent preservation` behavior instead of replacing it.
  - Update `skills/proposal-review/SKILL.md` to check broad or multi-workstream proposals for missing/misleading scope-budget classification while allowing small single-decision proposals to omit it.
  - Update `docs/workflows.md` so path/state discovery starts from exact paths, active state, metadata, the artifact-location map, headings, stable IDs, counts, line ranges, and diffs before broad reads.
  - Add the do-not-under-read escape to `docs/workflows.md`.
  - Add or update focused static proof only where the test spec requires it.
  - Run static skill token measurement after skill changes and record that it is diagnostic only.
  - Record why no dynamic benchmark comparison is required for this wording-only slice.
  - Update progress, validation notes, and change metadata.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/select-validation.py --mode explicit --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path docs/workflows.md --path scripts/test-skill-validator.py --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/plan.md`
  - `bash scripts/ci.sh --mode explicit --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path docs/workflows.md --path scripts/test-skill-validator.py --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/plan.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md --path specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/plan.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml`
  - `git diff --check --`
- Expected observable result:
  - proposal guidance tells broad proposal authors when and how to classify work items;
  - proposal-review guidance requests changes for missing or misleading broad-scope classification;
  - small single-decision proposals are not forced into scope-budget ceremony;
  - `docs/workflows.md` is the full bounded-evidence/path-search guide and preserves full-file-read escape conditions;
  - no selector behavior, broad-smoke trigger, release validation, adapter packaging, lifecycle token-cost summary artifact, dynamic benchmark requirement, or progressive-loading implementation changes.
- Commit message: `M1: add cost-bounded proposal and evidence guidance`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - scope-budget guidance could become routine ceremony for small proposals;
  - bounded-evidence wording could be misread as permission to under-read;
  - static checks could become brittle semantic validation;
  - skill wording could duplicate `docs/workflows.md` rather than pointing to it.
- Rollback/recovery:
  - narrow scope-budget language to broad or multi-workstream proposals only;
  - strengthen full-file-read escape wording while preserving bounded-first lookup;
  - remove brittle static checks and rely on review guidance plus test-spec manual proof;
  - move duplicated skill detail back to `docs/workflows.md`.

## Validation plan

Before plan-review:

- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md --path specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/plan.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml`
- `git diff --check -- docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md docs/plan.md specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml`

Before implementation:

- `plan-review` approval.
- Active test spec at `specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.test.md`.

Implementation validation is listed in M1.

Final verification before PR should include:

- review artifact closeout validation;
- change metadata validation;
- artifact lifecycle validation for touched lifecycle artifacts;
- skill validation and generated local mirror temp-output check when canonical skills change;
- selected explicit CI for touched paths;
- final whitespace check;
- explain-change evidence that records no dynamic benchmark was required.

## Risks and recovery

- Risk: The plan expands into validation-budget or lifecycle-token-summary work. Recovery: stop and require a later accepted spec or plan revision before adding those surfaces.
- Risk: Proposal skill wording becomes too long. Recovery: keep treatment definitions concise and route full operating detail through `docs/workflows.md`.
- Risk: Proposal-review becomes a semantic validator. Recovery: keep semantic broadness judgment in review prose and static checks narrow.
- Risk: Existing bounded-extraction wording in `docs/workflows.md` becomes contradictory. Recovery: consolidate the section around one ordered bounded-evidence sequence and preserve full-file-read escapes.
- Risk: Skill changes imply generated public adapter output should be tracked again. Recovery: keep generated public adapter skill bodies out of tracked source and use `build-skills.py --check` plus release-surface guidance.

## Dependencies

- Proposal accepted.
- Spec approved.
- Spec-review approval recorded with no material findings.
- Plan-review approval before test-spec.
- Active test spec before implementation.
- No architecture package required unless plan-review identifies a cross-component design risk.
- No release or adapter packaging validation unless implementation touches release or adapter surfaces.

## Progress

- 2026-05-14: proposal accepted, spec approved after clean spec-review, plan created and indexed.
- 2026-05-14: `plan-review-r1` approved the plan with no material findings; next stage was `test-spec`.
- 2026-05-14: active test spec created; next stage is `implement`.
- 2026-05-14: maintainer approved the active test spec; next stage remains `implement`.
- 2026-05-14: M1 implementation added focused static proof, proposal/proposal-review scope-budget guidance, and `docs/workflows.md` bounded-evidence/path-search guidance. Targeted validation passed; next stage is `code-review`.
- 2026-05-14: `code-review-r1` reviewed M1 implementation commit `dc59864bdc4f36a248be573c551b553c501dd0d6` and returned `clean-with-notes` with no material findings. M1 is closed; next stage is `explain-change`.
- 2026-05-14: `explain-change.md` recorded durable rationale for M1 scope, diff areas, validation evidence, review outcomes, rejected alternatives, and no-dynamic-benchmark rationale. Next stage is `verify`.
- 2026-05-14: final verify passed against tracked branch tip `360ebe8` from clean temporary worktree `/tmp/rigorloop-verify-cost-bounded-360ebe8`. Branch-ready is satisfied for the tracked change pack; next stage is `pr`.

## Decision log

- 2026-05-14: Use one implementation milestone for the first slice. Reason: the approved spec is intentionally narrow and the likely touched implementation surfaces are `skills/proposal`, `skills/proposal-review`, `docs/workflows.md`, and focused static proof.
- 2026-05-14: Treat architecture as not required. Reason: spec-review found no runtime, data-flow, security-boundary, deployment, persistence, or hard-to-reverse design risk.
- 2026-05-14: Do not require dynamic benchmark comparison. Reason: the approved spec changes proposal/evidence wording only and keeps dynamic benchmarks advisory unless a later plan or test spec requires them.
- 2026-05-14: Do not add a standalone `verify-report.md`. Reason: no required manual proof exists; final verification evidence is automated and recorded in this plan, `change.yaml`, and `explain-change.md`.

## Surprises and discoveries

- 2026-05-14: Selected explicit CI included `adapters.drift` and `selector.regression` because canonical skill and workflow guidance changed. No adapter packaging, release validation, selector behavior, dynamic benchmark, or lifecycle token-cost summary behavior changed.

## Validation notes

- 2026-05-14: test-spec stage validation passed:
  - `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md --path specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md --path specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.test.md --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/plan.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md --path specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md --path specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.test.md --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/plan.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml`
  - `python scripts/test-change-metadata-validator.py`
  - `git diff --check -- docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.test.md docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md docs/plan.md docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml`
- 2026-05-14: test-spec approval-state validation passed:
  - `python scripts/select-validation.py --mode explicit --path specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.test.md --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/plan.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.test.md --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/plan.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml`
  - `python scripts/test-change-metadata-validator.py`
  - `git diff --check -- specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.test.md docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md docs/plan.md docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml`
- 2026-05-14: M1 implementation validation passed:
  - `python scripts/test-skill-validator.py SkillValidatorFixtureTests.test_cost_bounded_rigor_m1_proposal_scope_budget_guidance SkillValidatorFixtureTests.test_cost_bounded_rigor_m1_proposal_review_scope_budget_guidance SkillValidatorFixtureTests.test_cost_bounded_rigor_m1_workflows_bounded_evidence_guidance` failed before implementation for the expected missing guidance, then passed after implementation.
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/measure-skill-tokens.py` recorded diagnostic static skill measurement only; no dynamic benchmark comparison was required because this slice changes proposal/evidence wording and no runtime benchmark surface.
  - `python scripts/select-validation.py --mode explicit --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path docs/workflows.md --path scripts/test-skill-validator.py --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/plan.md --path specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.test.md`
  - `bash scripts/ci.sh --mode explicit --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path docs/workflows.md --path scripts/test-skill-validator.py --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/plan.md --path specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.test.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md --path specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md --path specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.test.md --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/plan.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml`
  - `git diff --check -- docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/code-review-r1.md docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/review-log.md docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md docs/plan.md`
- 2026-05-14: `code-review-r1` review-recording validation passed:
  - `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/code-review-r1.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/review-log.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/plan.md`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/plan.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/review-log.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/code-review-r1.md`
  - `python scripts/test-change-metadata-validator.py`
  - `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/code-review-r1.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/review-log.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/plan.md`
- 2026-05-14: explain-change validation passed:
  - `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/explain-change.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/plan.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/explain-change.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/plan.md`
  - `python scripts/test-change-metadata-validator.py`
  - `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/explain-change.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/plan.md`
  - `git diff --check -- docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/explain-change.md docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md docs/plan.md`
- 2026-05-14: final verify passed from clean temporary worktree `/tmp/rigorloop-verify-cost-bounded-360ebe8` to avoid unrelated dirty working-tree changes in `README.md`, `docs/workflows.md`, selector files, and `docs/project-map.md`:
  - `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/explain-change.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/review-log.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/review-resolution.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/code-review-r1.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/plan-review-r1.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/proposal-review-r1.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/proposal-review-r2.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/proposal-review-r3.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/spec-review-r1.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/spec-review-r2.md --path docs/plan.md --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md --path docs/workflows.md --path scripts/test-skill-validator.py --path skills/proposal-review/SKILL.md --path skills/proposal/SKILL.md --path specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md --path specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.test.md`
  - `bash scripts/ci.sh --mode explicit --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/explain-change.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/review-log.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/review-resolution.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/code-review-r1.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/plan-review-r1.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/proposal-review-r1.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/proposal-review-r2.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/proposal-review-r3.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/spec-review-r1.md --path docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/spec-review-r2.md --path docs/plan.md --path docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md --path docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md --path docs/workflows.md --path scripts/test-skill-validator.py --path skills/proposal-review/SKILL.md --path skills/proposal/SKILL.md --path specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md --path specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.test.md`
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording`
  - `git diff --check ef2f0b2..HEAD --`
  - `git status --short`

## Outcome and retrospective

- Keep this section final-only or explicitly historical while the plan is active; do not duplicate the current next stage here.

## Readiness

- See `Current Handoff Summary`.
- M1 implementation is closed after clean code-review, durable rationale is recorded, and final verify passed against the tracked branch tip. Ready for `pr`.
