# Skill Readability and Self-Containment Execution Plan

- Status: active
- Owner: maintainer
- Start date: 2026-05-18
- Last updated: 2026-05-18
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

Implement the approved skill readability and self-containment contract in a safe pilot-first sequence. The pilot updates `proposal` and `proposal-review`, adds focused validation and evidence, proves cold-read and behavior parity, and prepares a follow-on rollout path for the remaining artifact-producing skills without broadening this change into a full skill rewrite.

## Source artifacts

- Proposal: `docs/proposals/2026-05-18-skill-readability-self-containment.md`
- Spec: `specs/skill-readability-contract.md`
- Spec review evidence: `docs/changes/2026-05-18-skill-readability-self-containment/reviews/spec-review-r1.md`
- Architecture: not required; spec-review found no runtime architecture or adapter package format change.
- ADR: not required.
- Test spec: `specs/skill-readability-contract.test.md`
- Related contracts: `specs/skill-contract.md`, `specs/customer-portable-public-skill-evidence.md`

## Context and orientation

Canonical authored skill source lives under `skills/`. Generated adapter output is release/generated output and must not be hand-edited. The current change is contract and skill-surface work: it affects canonical skills, static validation, adapter-generation validation evidence, token measurement evidence, cold-read evidence, behavior-parity fixtures, and lifecycle records.

Likely touched surfaces for this pilot:

- `skills/proposal/SKILL.md`
- `skills/proposal-review/SKILL.md`
- `scripts/test-skill-validator.py`
- `scripts/validate-skills.py` or helper modules it delegates to, only if needed for focused validation
- `scripts/build-skills.py --check` output evidence, not generated skill files
- temporary adapter output generated outside tracked source
- `docs/reports/token-cost/skills/2026-05-18-skill-readability-self-containment.md`
- behavior-parity fixtures under an existing fixture root or a new scoped fixture directory chosen by the test spec
- `docs/changes/2026-05-18-skill-readability-self-containment/`

The full R30 rollout list from the spec remains in scope for the overall contract, but this execution plan implements the pilot pair only. Non-pilot R30 skills are follow-on rollout work after pilot evidence is reviewed; they are not excluded from the contract.

## Non-goals

- Do not change workflow stage order, handoff semantics, review verdict meanings, formal review recording rules, or status vocabulary.
- Do not introduce build-time partials or include mechanisms.
- Do not change adapter packaging, manifest format, or release archive contracts.
- Do not retroactively rewrite legacy adapter archives.
- Do not edit generated adapter output by hand.
- Do not rewrite the full R30 skill set in this pilot change.
- Do not move normative user-facing behavior out of installed skill text into inaccessible repository specs.
- Do not accept token savings or wording reductions that weaken output quality, required-rule coverage, artifact completeness, or cold-read clarity.

## Requirements covered

| Requirement IDs | Planned coverage |
|---|---|
| R1-R10 | Preserve canonical source/generated-output boundaries, quality-first priority, self-containment, project-local evidence, portable defaults, and ambiguity blocking in the pilot pair. |
| R11-R15 | Add workflow role blocks to `proposal` and `proposal-review`, using the closed `stage` enum and two-line summary constraint. |
| R16-R24 | Fence or table closed enums, avoid duplicate enum prose, tabulate long enumerative contracts, deduplicate intra-skill rules where safe, and distinguish workflow-wide from skill-local rules in the pilot pair. |
| R25-R28 | Add fenced output skeletons to `proposal` and `proposal-review` while preserving existing required result/review recording fields. |
| R29-R31 | Implement the pilot pair and record the remaining R30 skills as follow-on rollout work, not exclusions. |
| R32-R35 | Add additive `version` and `schema-version` front matter to the pilot pair only after test-spec confirms compatibility checks. |
| R36-R40 | Add focused static validation for workflow role blocks, output skeletons, forbidden required internal references, and known closed enum placement for the pilot pair. |
| R41-R47 | Record cold-read and behavior-parity evidence for the pilot pair, with `equivalent`, `improvement`, or `regression` classifications. |
| R48-R53 | Record pilot token-cost comparison, apply zero-regression target, five percent tolerance, ten percent hard cap, and decide lint enforcement mode in this plan. |
| R54-R60 | Preserve non-goals and stop conditions for missing blocks, unresolved references, behavior regressions, token hard-cap breaches, and ambiguous rule ownership. |

## Current Handoff Summary

- Current milestone: M3. Cold-read, behavior parity, token comparison, and rollout handoff
- Current milestone state: planned
- Last reviewed milestone: M2. Pilot skill rewrite and generated-output proof
- Review status: clean-with-notes by `code-review-m2-r1`
- Remaining in-scope implementation milestones: M3
- Next stage: implement M3
- Next lifecycle stage after M3 implementation: code-review for M3
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: implementation milestones, code-review, review-resolution closeout if triggered, explain-change, verify, and PR handoff remain incomplete.

## Completed lifecycle handoffs

### Test-spec and validation design

- Stage: test-spec
- Stage state: active test spec created
- Goal: Create the test spec and focused validation design for the pilot before editing pilot skill behavior.
- Requirements: R29-R31, R36-R47, R48-R53
- Files/components likely touched: `specs/skill-readability-contract.test.md`, `docs/changes/2026-05-18-skill-readability-self-containment/change.yaml`, this plan body.
- Dependencies: plan-review approval; approved spec status; clean spec-review evidence.
- Test-spec obligations: map every `MUST` to static validation, cold-read, behavior parity, token-cost measurement, generated adapter validation, or manual review.
- Stage steps: choose behavior-parity fixture paths; define cold-read procedure against installed adapter output; define lint enforcement mode for the pilot as blocking for pilot-touched skills and warning-only for non-pilot skills; define token-cost evidence location; define compatibility check for front matter fields.
- Validation commands: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/skill-readability-contract.md --path specs/skill-readability-contract.test.md --path docs/plans/2026-05-18-skill-readability-self-containment.md --path docs/plan.md`; `python scripts/validate-change-metadata.py docs/changes/2026-05-18-skill-readability-self-containment/change.yaml`; `git diff --check -- specs/skill-readability-contract.test.md docs/plans/2026-05-18-skill-readability-self-containment.md docs/plan.md docs/changes/2026-05-18-skill-readability-self-containment`
- Expected observable result: the test spec is ready for review or approval, and implementation has a concrete proof map before skill rewrites start.
- Risks: test-spec could drift into implementation detail or omit manual proof for cold-read quality.
- Rollback/recovery: revise the test spec before any skill rewrite proceeds; if proof scope becomes too broad, split rollout validation into pilot and follow-on sections.

## Implementation milestones

### M1. Static validator foundations and baseline evidence

- Milestone state: closed
- Goal: Add focused static checks and baseline evidence before rewriting the pilot skill bodies.
- Requirements: R16-R28, R32-R40, R48-R53
- Files/components likely touched: `scripts/test-skill-validator.py`, `scripts/validate-skills.py` or helper modules, baseline token report under `docs/reports/token-cost/skills/2026-05-18-skill-readability-self-containment.md`, optional fixture files chosen by the test spec.
- Dependencies: active test spec exists; no pilot skill rewrite has started.
- Tests to add/update: failing/static checks for missing workflow role block, missing output skeleton, unqualified forbidden internal references, and duplicate known closed enum blocks for `proposal` and `proposal-review`; baseline token measurement for the pilot pair.
- Implementation steps: add focused validator tests first; run them and record expected failure against the current pilot skills where feasible; record baseline token cost for `proposal` and `proposal-review`; keep non-pilot R30 skills warning-only or out of validator enforcement in this milestone.
- Validation commands: `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`; `python scripts/measure-skill-tokens.py`; `python scripts/build-skills.py --check`; `python scripts/validate-change-metadata.py docs/changes/2026-05-18-skill-readability-self-containment/change.yaml`; `git diff --check -- scripts docs/reports/token-cost/skills docs/changes/2026-05-18-skill-readability-self-containment`
- Expected observable result: static checks and baseline evidence exist before the pilot skill rewrite, with failure/pass behavior recorded according to the test spec.
- Commit message: `M1: add skill readability validation foundation`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] hand off to code-review for M1
  - [x] material findings resolved or explicitly dispositioned
  - [x] milestone committed
- Risks: static checks may become semantic prose scoring or accidentally apply to all skills before rollout.
- Rollback/recovery: narrow checks to explicit headings, fields, fenced blocks, known enum markers, and path phrases; defer non-pilot enforcement to follow-on rollout.

### M2. Pilot skill rewrite and generated-output proof

- Milestone state: closed
- Goal: Rewrite `proposal` and `proposal-review` to satisfy the readability contract while preserving normative behavior and generated-output boundaries.
- Requirements: R1-R35, R54-R60
- Files/components likely touched: `skills/proposal/SKILL.md`, `skills/proposal-review/SKILL.md`, validation fixtures if needed, change-local implementation notes.
- Dependencies: M1 closed; baseline token cost recorded; focused static checks available; test spec proof map accepted.
- Tests to add/update: update expected static checks to pass for the pilot pair; add or update fixture assertions for required role blocks, enum blocks, output skeletons, workflow-wide labels, skill-local boundaries, and front matter compatibility.
- Implementation steps: add workflow role blocks; add `version` and `schema-version: skill-readability-v1`; fence closed enums exactly once; convert long enumerative contracts to tables where clearer; add output skeletons near the bottom; label workflow-wide rules; remove duplicate intra-skill rule statements only when the rule remains preserved; run generated skill and temporary adapter validation from canonical source.
- Validation commands: `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`; `python scripts/build-skills.py --check`; `python scripts/build-adapters.py --version <current-or-next-version> --output-dir /tmp/rigorloop-skill-readability-adapters`; `python scripts/validate-adapters.py --root /tmp/rigorloop-skill-readability-adapters --version <current-or-next-version>`; `python scripts/validate-change-metadata.py docs/changes/2026-05-18-skill-readability-self-containment/change.yaml`; `git diff --check -- skills scripts docs/changes/2026-05-18-skill-readability-self-containment`
- Expected observable result: the pilot pair satisfies static readability checks, generated output validates from canonical source, and no generated adapter body is hand-edited.
- Commit message: `M2: rewrite proposal skills for readability`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] hand off to code-review for M2
  - [x] material findings resolved or explicitly dispositioned
  - [x] milestone committed
- Risks: editorial rewrite changes normative proposal or review behavior; front matter fields break a consumer; generated adapter validation version is ambiguous.
- Rollback/recovery: revert only the affected pilot skill body or front matter field; if adapter validation version is ambiguous, block and record the required version decision before continuing.

### M3. Cold-read, behavior parity, token comparison, and rollout handoff

- Milestone state: planned
- Goal: Prove the pilot pair preserves quality and clarity, record token-cost comparison, and prepare follow-on rollout guidance for the remaining R30 skills.
- Requirements: R30-R31, R41-R53, R57-R60
- Files/components likely touched: behavior-parity fixtures and reports, cold-read evidence report, token-cost report, this plan, `docs/changes/2026-05-18-skill-readability-self-containment/change.yaml`, optional `docs/follow-ups.md` only if an unowned cross-change follow-up is needed.
- Dependencies: M2 closed; pilot skills rewritten; generated output validation available.
- Tests to add/update: behavior-parity fixture comparison for `proposal` and `proposal-review`; cold-read installed adapter output check; after-change token measurement and comparison against M1 baseline.
- Implementation steps: build adapter output into a temporary directory; inspect installed `proposal` and `proposal-review` skill text without repository context; run behavior-parity comparison and classify differences as `equivalent`, `improvement`, or `regression`; run after-change token measurement; record any accepted token increase with readability justification; record remaining R30 skill rollout as follow-on work with no exclusions unless specifically justified.
- Validation commands: `python scripts/measure-skill-tokens.py`; `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`; `python scripts/build-skills.py --check`; `python scripts/validate-change-metadata.py docs/changes/2026-05-18-skill-readability-self-containment/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-18-skill-readability-self-containment.md --path docs/plan.md --path specs/skill-readability-contract.md --path docs/changes/2026-05-18-skill-readability-self-containment/change.yaml`; `git diff --check --`
- Expected observable result: no behavior-parity regressions, cold-read evidence passes for the pilot pair, token comparison is within spec thresholds or has recorded allowed rationale, and follow-on rollout ownership is visible.
- Commit message: `M3: record skill readability pilot evidence`
- Milestone closeout:
  - [ ] validation passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] hand off to code-review for M3
  - [ ] material findings resolved or explicitly dispositioned
  - [ ] milestone committed
- Risks: behavior-parity comparison is too subjective; token increase exceeds the hard cap; cold-read finds a dangling internal reference after skill rewrite.
- Rollback/recovery: treat any `regression` as blocking; revise the affected skill and rerun M2/M3 checks; if token hard cap is exceeded, reduce text without breaching quality or revise the spec before rollout.

### Lifecycle closeout

- Milestone state: planned
- Goal: Complete downstream non-implementation gates after all implementation milestones are closed.
- Requirements: all requirements
- Files/components likely touched: `docs/changes/2026-05-18-skill-readability-self-containment/explain-change.md`, optional verify report, this plan, `docs/plan.md`, PR handoff text.
- Dependencies: active test spec exists; M1-M3 closed; all code-review findings resolved; no open review-resolution findings.
- Tests to add/update: no new feature tests; run selected final validation from touched paths.
- Implementation steps: record explain-change; run final verify; update plan and plan index lifecycle state when ready; prepare PR handoff.
- Validation commands: `bash scripts/ci.sh --mode explicit --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path scripts/test-skill-validator.py --path scripts/validate-skills.py --path specs/skill-readability-contract.md --path specs/skill-readability-contract.test.md --path docs/plans/2026-05-18-skill-readability-self-containment.md --path docs/plan.md --path docs/changes/2026-05-18-skill-readability-self-containment`; `python scripts/validate-review-artifacts.py docs/changes/2026-05-18-skill-readability-self-containment`; `git diff --check --`
- Expected observable result: final lifecycle evidence is coherent, plan state is synchronized with `docs/plan.md`, and the branch is ready for PR only after verify passes.
- Commit message: `Close skill readability pilot lifecycle`
- Milestone closeout:
  - [ ] explain-change recorded
  - [ ] final verify passed
  - [ ] plan state synchronized with `docs/plan.md`
  - [ ] PR handoff prepared
- Risks: lifecycle state drifts between plan body and index; final selected CI scope misses a touched validation surface.
- Rollback/recovery: run explicit-path lifecycle validation and selected CI over all touched surfaces; fix plan/index drift before PR handoff.

## Validation plan

- Plan authoring validation: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/skill-readability-contract.md --path specs/skill-readability-contract.test.md --path docs/plans/2026-05-18-skill-readability-self-containment.md --path docs/plan.md --path docs/changes/2026-05-18-skill-readability-self-containment/change.yaml --path docs/changes/2026-05-18-skill-readability-self-containment/review-log.md`; `python scripts/validate-change-metadata.py docs/changes/2026-05-18-skill-readability-self-containment/change.yaml`; `python scripts/validate-review-artifacts.py docs/changes/2026-05-18-skill-readability-self-containment`; `git diff --check -- specs/skill-readability-contract.test.md docs/plans/2026-05-18-skill-readability-self-containment.md docs/plan.md specs/skill-readability-contract.md docs/changes/2026-05-18-skill-readability-self-containment`
- Test-spec validation: artifact lifecycle, change metadata, review artifacts, and diff check passed after creating the active test spec.
- M1 validation: `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, `python scripts/measure-skill-tokens.py`, `python scripts/build-skills.py --check`, metadata validation, and diff check.
- M2 validation: static skill validation, generated skill check, temporary adapter build and validation, metadata validation, and diff check.
- M3 validation: token measurement, behavior-parity evidence, cold-read evidence, static validation, lifecycle validation, metadata validation, and diff check.
- Final validation: selected CI over touched skills, scripts, specs, plans, and change-local artifacts; review artifact validation; lifecycle validation; diff check.

## Risks and recovery

- Risk: the pilot rewrite changes normative behavior. Recovery: behavior-parity comparison blocks rollout; revert or revise only the affected skill text.
- Risk: static validators become broad semantic scoring. Recovery: keep checks focused on headings, fields, fenced blocks, output skeleton markers, and explicit path phrases.
- Risk: cold-read verification becomes subjective. Recovery: require a checklist with named pass/fail items and exact installed adapter output paths.
- Risk: token-cost increase exceeds thresholds. Recovery: reduce wording while preserving quality/clarity or revise the spec before continuing.
- Risk: adding front matter breaks consumers. Recovery: remove or defer `version`/`schema-version` until compatibility is proven.
- Risk: full R30 rollout scope is forgotten after the pilot. Recovery: record follow-on rollout ownership in M3 or `docs/follow-ups.md` if no active plan owns it.

## Dependencies

- `specs/skill-readability-contract.md` must be approved before plan-review relies on it.
- `plan-review` must pass before test-spec or implementation relies on this plan.
- `test-spec` must be active before implementation starts.
- Adapter validation requires choosing the current-or-next adapter version available to `scripts/build-adapters.py` and `scripts/validate-adapters.py`.
- Behavior-parity fixture scope must be defined in the test spec before M2/M3.

## Progress

- 2026-05-18: plan created after clean `spec-review-r1`; spec status settled to `approved`.
- 2026-05-18: `plan-review-r1` found SRSC-PLAN-1; revised the plan so `test-spec` is the next lifecycle handoff and implementation milestones start with static validator foundations.
- 2026-05-18: `plan-review-r2` approved the revised plan with no material findings; next stage is `test-spec`.
- 2026-05-18: `plan-review-r3` reconfirmed the revised plan with no material findings; next stage was `test-spec`.
- 2026-05-18: created active test spec at `specs/skill-readability-contract.test.md`; next stage is implementation M1.
- 2026-05-18: user approved the active test spec; next stage remains implementation M1.
- 2026-05-18: implemented M1 static validator foundations and baseline evidence; next stage is code-review for M1.
- 2026-05-18: `code-review-m1-r1` found no material findings and closed M1; next stage is implementation M2.
- 2026-05-18: implemented M2 pilot rewrite for `proposal` and `proposal-review`; next stage is code-review for M2.
- 2026-05-18: `code-review-m2-r1` found no material findings and closed M2; next stage is implementation M3.

## Decision log

- 2026-05-18: pilot scope is limited to `proposal` and `proposal-review` -> matches R29 and keeps the change reviewable.
- 2026-05-18: non-pilot R30 skills are follow-on rollout work, not exclusions -> preserves the full contract while avoiding a broad first implementation change.
- 2026-05-18: forbidden-path lint is blocking for pilot-touched skills and warning-only for non-pilot skills during this plan -> enforces the pilot without accidentally gating untouched rollout skills.
- 2026-05-18: architecture stage is not required -> spec-review found no runtime architecture or adapter package format change.
- 2026-05-18: test-spec authoring is a lifecycle handoff, not an implementation milestone -> preserves the repository stage sequence `plan-review -> test-spec -> implementation milestone 1`.
- 2026-05-18: M1 readability validation is opt-in on `schema-version: skill-readability-v1` -> lets fixture tests prove the contract before M2 rewrites the pilot skills and prevents current canonical skills from failing before they are in scope.
- 2026-05-18: M2 uses skill front matter `version: "1.0.0"` consistently across the pilot pair -> records the first readability-contract shape version independently from adapter release archive version.
- 2026-05-18: M2 temporary adapter validation uses `v0.1.5` -> matches the tracked `dist/adapters/manifest.yaml` release-support surface after PR #68 merged.

## Surprises and discoveries

- 2026-05-18: existing top-level title validation counted `# ` headings inside fenced output skeletons. M1 adjusted title counting to ignore fenced code blocks so fillable Markdown skeletons can contain headings in later rewrites.
- 2026-05-18: M2 preserved exact prior static-contract phrases in `proposal` and `proposal-review` while moving their operational shape into tables and fenced enum blocks, because existing regression tests still assert those phrases.

## Validation notes

- 2026-05-18: after creating `specs/skill-readability-contract.test.md`, artifact lifecycle validation, change metadata validation, review artifact closeout validation, and diff check passed for the active test spec, plan, plan index, and change-local metadata.
- 2026-05-18: user approval recorded for the active test spec.
- 2026-05-18: test-first run `python scripts/test-skill-validator.py` failed as expected before validator implementation on the new readability fixtures.
- 2026-05-18: `python scripts/test-skill-validator.py` passed after implementing opt-in readability checks.
- 2026-05-18: `python scripts/validate-skills.py` passed for current canonical skills; M1 checks are opt-in until M2 adds `schema-version: skill-readability-v1` to the pilot pair.
- 2026-05-18: `python scripts/measure-skill-tokens.py` passed and established baseline token counts: `proposal` 3189 estimated tokens, `proposal-review` 3255 estimated tokens.
- 2026-05-18: `python scripts/build-skills.py --check` passed using temporary generated output.
- 2026-05-18: M1 handoff validation passed: artifact lifecycle explicit paths, change metadata, review artifact closeout, and `git diff --check --`.
- 2026-05-18: M1 code-review validation passed: `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, `python scripts/build-skills.py --check`, and `python scripts/validate-change-metadata.py docs/changes/2026-05-18-skill-readability-self-containment/change.yaml`.
- 2026-05-18: M2 test-first run `python scripts/test-skill-validator.py -k skill_readability_pilot_pair_opts_into_contract` failed before the pilot rewrite because `proposal` and `proposal-review` lacked `schema-version: skill-readability-v1`, `## Workflow role`, and `## Output skeleton`.
- 2026-05-18: M2 validation passed after the rewrite: `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, `python scripts/build-skills.py --check`, `python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-skill-readability-adapters`, `python scripts/validate-adapters.py --root /tmp/rigorloop-skill-readability-adapters --version v0.1.5`, and `python scripts/validate-change-metadata.py docs/changes/2026-05-18-skill-readability-self-containment/change.yaml`.
- 2026-05-18: M2 handoff validation passed after plan and change-metadata updates: artifact lifecycle explicit paths, review artifact closeout, and `git diff --check --`.
- 2026-05-18: M2 code-review validation passed: `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, `python scripts/build-skills.py --check`, and `python scripts/validate-adapters.py --root /tmp/rigorloop-skill-readability-adapters --version v0.1.5`.

## Outcome and retrospective

- Test spec is active. Keep implementation state in `Current Handoff Summary` until final closeout.

## Readiness

- See `Current Handoff Summary`.

## Risks and follow-ups

- Follow-on rollout must cover the remaining R30 skills after pilot evidence passes, unless a later plan records justified exclusions.
