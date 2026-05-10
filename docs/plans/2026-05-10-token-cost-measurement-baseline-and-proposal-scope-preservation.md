# Token Cost Measurement Baseline and Proposal Scope Preservation

- Status: active
- Owner: Codex
- Start date: 2026-05-10
- Last updated: 2026-05-10
- Related issue or PR: none yet
- Supersedes: none

## Purpose / Big Picture

This plan implements the approved token-cost measurement baseline and proposal scope-preservation contract in small, reviewable slices.

The change has two connected outcomes:

- make token-cost optimization evidence-based through local measurement scripts and a durable baseline report;
- prevent future proposals from silently dropping parts of a user's initial request by updating proposal/proposal-review guidance and validation.

## Source Artifacts

- Proposal: `docs/proposals/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md`
- Spec: `specs/token-cost-measurement-baseline-and-proposal-scope-preservation.md`
- Architecture: `docs/architecture/system/architecture.md`
- Proposal review: `docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/reviews/proposal-review-r2.md`
- Spec review: `docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/reviews/spec-review-r1.md`
- Architecture review: `docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/reviews/architecture-review-r1.md`
- Test spec: `specs/token-cost-measurement-baseline-and-proposal-scope-preservation.test.md`
- Change metadata: `docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`

## Context and Orientation

Likely implementation surfaces:

- measurement scripts under `scripts/`
- script tests in existing repository-owned test files or new focused test files under `scripts/`
- canonical skill sources:
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
- skill validation surfaces:
  - `scripts/skill_validation.py`
  - `scripts/validate-skills.py`
  - `scripts/test-skill-validator.py`
- generated skill mirrors and public adapter output:
  - `.codex/skills/`
  - `dist/adapters/`
- durable report output:
  - `docs/reports/token-cost/2026-05-10-baseline.md`
- change-local evidence:
  - `docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/`

Constraints:

- Do not hand-edit `.codex/skills/` or `dist/adapters/`; regenerate them from canonical sources.
- Do not add hosted telemetry or network-dependent measurement.
- Do not add hard token-budget CI gates in this slice.
- Do not add a live command wrapper in this slice.
- The current repository adapter validation command requires `--version`; use `0.1.1` unless a later approved release artifact changes the active version.
- Public skill text must remain project-portable and must not expose repository-maintainer-only paths or adapter mechanics.

## Non-goals

- Do not reopen PR #39.
- Do not add hosted telemetry infrastructure.
- Do not add hard token-budget CI gates in the first slice.
- Do not add `scripts/measure-command-output.py` in the first slice.
- Do not rewrite all skills.
- Do not make proposal-review responsible for editing proposals directly.
- Do not replace required validation, review, or workflow gates with token-cost measurement.
- Do not require downstream public skill users to know this repository's internal generated-output or adapter paths.

## Requirements Covered

| Requirement | Planned coverage |
|---|---|
| R1, R1a-R1e | M1 static skill measurement script and tests |
| R2, R2a-R2f | M1 Codex JSONL analyzer and tests |
| R3, R3a-R3b | M1 analyzer scope and M3/M5 non-goal checks |
| R4, R4a-R4d | M2 baseline report and change-local links |
| R5, R5a-R5c | M1 warning-only measurement behavior and tests |
| R6, R6a-R6e | M3 proposal skill guidance |
| R7, R7a-R7e | M3 proposal skill guidance and validator checks |
| R8, R8a-R8f | M3 proposal-review guidance and validator checks |
| R9, R9a-R9b | M3 public skill wording review and M4 generated output validation |
| R10, R10a-R10e | M3 static validation and tests |
| R11, R11a-R11d | M4 generated skill and adapter drift/validation |
| R12, R12a-R12b | M2/M5 change evidence and plan scope |
| AC1-AC2 | M1 direct script proof |
| AC3 | M2 report proof |
| AC4-AC6 | M3 skill and validator proof |
| AC7 | M4 generated output and adapter proof |
| AC8 | M1/M5 warning-only proof |

## Current Handoff Summary

- Current milestone: M3. Proposal scope preservation skill and validator updates
- Current milestone state: review-resolution
- Last reviewed milestone: M2. Durable baseline report and change evidence
- Review status: M3 code-review R1 changes-requested with TCSP-CR-M3-F1 open
- Remaining in-scope implementation milestones: M3, M4
- Next stage: review-resolution / implement M3 fix
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: M3 has an open code-review finding, M4 has not started, final lifecycle closeout has not run, and PR handoff is not prepared.

## Milestones

### M1. Measurement Scripts and Parser Tests

- Milestone state: closed
- Goal: Add local measurement commands for static skill cost and Codex JSONL session/tool-output amplification.
- Requirements: R1, R1a-R1e, R2, R2a-R2f, R3, R3a-R3b, R5, R5a-R5b, AC1, AC2, AC8
- Files/components likely touched:
  - `scripts/measure-skill-tokens.py`
  - `scripts/analyze-codex-jsonl.py`
  - focused script tests under `scripts/`
- Dependencies:
  - Approved spec and architecture-review R1.
  - Test spec should define fixture shapes before implementation.
- Tests to add/update:
  - Static skill measurement covers path, byte size, line count, estimated tokens, warnings, no-network behavior, no skills found.
  - JSONL analyzer covers token usage present, usage absent, unknown event shapes, malformed JSONL, missing file, largest outputs, broad reads, high output caps, repeated reads, and no command-output events.
- Implementation steps:
  - Add dependency-light token estimate helper.
  - Add static skill scanner for canonical skill files.
  - Add JSONL streaming parser with conservative event extraction.
  - Add warning-only budget behavior with successful exit for threshold warnings.
  - Add focused tests and fixtures.
- Validation commands:
  - `python scripts/test-token-cost-measurement.py`
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/analyze-codex-jsonl.py <test-fixture-or-export>.jsonl`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`
  - `git diff --check -- scripts docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation`
- Expected observable result: Contributors can run local commands that summarize static skill cost and Codex JSONL tool-output amplification without telemetry or hard budget gates.
- Commit message: `M1: add token cost measurement commands`
- Implementation handoff:
  - [x] targeted validation passed
  - [x] hand off to code-review for M1
- Review closeout:
  - [x] code-review completed
  - [x] material findings resolved or explicitly dispositioned
  - [x] milestone state updated before starting the next implementation milestone
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - Codex JSONL export shapes may vary.
  - Token estimates may be approximate.
- Rollback/recovery:
  - Revert the new scripts and tests; no data migration is involved.
  - Keep unknown JSONL event handling defensive rather than shape-specific.

### M2. Durable Baseline Report and Change Evidence

- Milestone state: closed
- Goal: Produce the first token-cost baseline report and link it from change-local evidence.
- Requirements: R4, R4a-R4d, R12, R12a-R12b, AC3
- Files/components likely touched:
  - `docs/reports/token-cost/2026-05-10-baseline.md`
  - `docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`
  - optional durable reasoning evidence under `docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/`
- Dependencies:
  - M1 measurement scripts closed after code-review.
  - A usable fixture or local Codex JSONL export exists, or the report records unavailable session-token evidence with rationale.
- Tests to add/update:
  - Report shape is checked manually against the spec and by lifecycle/change metadata validation.
  - If practical, add a lightweight report-presence or report-heading test.
- Implementation steps:
  - Run static measurement.
  - Run JSONL analysis against the available benchmark source or fixture.
  - Write baseline report with summary, static skill cost, session cost, tool-output amplification, top cost drivers, comparison, conclusions, and next actions.
  - Link the report from change-local evidence.
- Validation commands:
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/analyze-codex-jsonl.py <test-fixture-or-export>.jsonl`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/reports/token-cost/2026-05-10-baseline.md --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`
  - `git diff --check -- docs/reports/token-cost docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation`
- Expected observable result: A durable first baseline exists under `docs/reports/token-cost/` and change-local artifacts link to it.
- Commit message: `M2: record token cost baseline report`
- Implementation handoff:
  - [x] targeted validation passed
  - [x] hand off to code-review for M2
- Review closeout:
  - [x] code-review completed
  - [x] material findings resolved or explicitly dispositioned
  - [x] milestone state updated before starting the next implementation milestone
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - The first report may be based on a fixture rather than a full real session export.
  - Raw transcript content could be over-quoted.
- Rollback/recovery:
  - Revert the report and links.
  - Replace raw output with summarized evidence if review finds excessive transcript exposure.

### M3. Proposal Scope Preservation Skill and Validator Updates

- Milestone state: review-resolution
- Goal: Update proposal/proposal-review behavior and static validation for initial intent preservation.
- Requirements: R6, R6a-R6e, R7, R7a-R7e, R8, R8a-R8f, R9, R9a-R9b, R10, R10a-R10e, AC4, AC5, AC6
- Files/components likely touched:
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`
  - `scripts/validate-skills.py` if needed
- Dependencies:
  - M1 and M2 closed after code-review so measurement/reporting context is stable.
  - Public skill wording must stay project-portable.
- Tests to add/update:
  - Proposal skill contains `Initial intent preservation` or equivalent scope-preservation guidance.
  - Proposal skill requires every initial user goal to be classified.
  - Proposal-review checks for silent narrowing.
  - Proposal-review requests revision when initial goals disappear.
  - Validator checks are narrow section/phrase/stable-ID checks.
- Implementation steps:
  - Add concise proposal skill scope preservation guidance.
  - Add proposal-review scope preservation review guidance.
  - Add focused static validation checks.
  - Add regression tests for the checks.
  - Run public portability checks and revise wording if needed.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`
  - `git diff --check -- skills/proposal/SKILL.md skills/proposal-review/SKILL.md scripts/skill_validation.py scripts/test-skill-validator.py docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation`
- Expected observable result: Proposal authoring preserves initial goals, proposal-review rejects silent narrowing, and validator tests protect the behavior.
- Commit message: `M3: preserve initial proposal intent`
- Implementation handoff:
  - [x] targeted validation passed
  - [x] hand off to code-review for M3
- Review closeout:
  - [x] code-review completed
  - [ ] material findings resolved or explicitly dispositioned
  - [x] milestone state updated before starting the next implementation milestone
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - Skill text could become too heavy.
  - Validator checks could become brittle prose scoring.
- Rollback/recovery:
  - Revert the skill and validator edits.
  - Replace broad prose checks with narrower stable-phrase checks.

### M4. Generated Skill and Adapter Refresh

- Milestone state: planned
- Goal: Regenerate derived Codex skill mirrors and public adapter output after canonical skill changes.
- Requirements: R11, R11a-R11d, AC7
- Files/components likely touched:
  - `.codex/skills/proposal/SKILL.md`
  - `.codex/skills/proposal-review/SKILL.md`
  - `dist/adapters/**/skills/proposal/SKILL.md`
  - `dist/adapters/**/skills/proposal-review/SKILL.md`
  - generated adapter manifests if the generator changes them
- Dependencies:
  - M3 canonical skill updates closed after code-review.
  - M3 code-review finding TCSP-CR-M3-F1 resolved and M3 closed.
  - Use adapter version `0.1.1`; source is current repository adapter command default and validation requirement.
- Tests to add/update:
  - Generated skill drift check.
  - Adapter drift check.
  - Adapter validation.
  - Adapter distribution tests if generated adapter output changes.
- Implementation steps:
  - Run the skill generator, if M3 changed canonical skills.
  - Run the adapter generator, if M3 changed public skill text.
  - Inspect generated diffs for source-path or maintainer-detail leakage.
  - Record validation evidence.
- Validation commands:
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`
  - `git diff --check -- .codex/skills dist/adapters docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation`
- Expected observable result: Derived skill mirrors and public adapters match canonical proposal/proposal-review skill behavior and validate for adapter version `0.1.1`.
- Commit message: `M4: refresh generated scope preservation skills`
- Implementation handoff:
  - [ ] targeted validation passed
  - [ ] hand off to code-review for M4
- Review closeout:
  - [ ] code-review completed
  - [ ] material findings resolved or explicitly dispositioned
  - [ ] milestone state updated before starting final lifecycle closeout
- Milestone closeout:
  - [ ] validation passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks:
  - Generated output may be stale if generation is skipped.
  - Adapter validation may fail if version source changes before implementation.
- Rollback/recovery:
  - Regenerate from canonical sources.
  - If version changes, update the plan with the active version source before rerunning validation.

### M5. Final Lifecycle Closeout

- Milestone state: planned
- Milestone type: lifecycle-closeout
- Goal: Complete final evidence, verification, plan/index state synchronization, and PR handoff only after M1-M4 each pass their milestone review loop.
- Requirements: all requirements, with emphasis on change evidence, lifecycle state, final validation, and PR readiness.
- Files/components likely touched:
  - `docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/explain-change.md`
  - `docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`
  - `docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md`
  - `docs/plan.md`
- Dependencies:
  - M1-M4 milestone states are `closed`.
  - All material findings are resolved or explicitly dispositioned.
  - Review-resolution closeout is closed.
  - Test spec is active and covered.
- Tests to add/update:
  - None expected beyond final validation and any review-requested proof.
- Implementation steps:
  - Write durable explain-change evidence.
  - Run final selected validation and any required broad smoke if triggered.
  - Synchronize this plan and `docs/plan.md` lifecycle state before PR handoff.
  - Prepare PR summary after final verification.
- Validation commands:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md --path docs/proposals/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md --path specs/token-cost-measurement-baseline-and-proposal-scope-preservation.md --path specs/token-cost-measurement-baseline-and-proposal-scope-preservation.test.md --path docs/architecture/system/architecture.md --path docs/reports/token-cost/2026-05-10-baseline.md --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`
  - `git diff --check -- .`
- Expected observable result: All implementation milestones are closed, final validation evidence is recorded, lifecycle state is synchronized, and the branch is ready for PR preparation.
- Commit message: `M5: close token cost baseline lifecycle`
- Implementation handoff:
  - [ ] final validation passed
  - [ ] hand off to code-review for M5 if final evidence changes require review
- Review closeout:
  - [ ] code-review completed if triggered
  - [ ] material findings resolved or explicitly dispositioned
  - [ ] lifecycle state updated before verify/PR
- Milestone closeout:
  - [ ] final validation passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks:
  - Final lifecycle state could drift between `docs/plan.md`, this plan, and change metadata.
  - PR handoff could cite stale validation.
- Rollback/recovery:
  - Return the plan to `active` and name the unresolved gate.
  - Rerun lifecycle and review-artifact validation after any state correction.

## Validation Plan

Milestone validation is listed inside each milestone. The expected final validation family includes:

```bash
python scripts/test-token-cost-measurement.py
python scripts/measure-skill-tokens.py
python scripts/analyze-codex-jsonl.py <test-fixture-or-export>.jsonl
python scripts/validate-skills.py
python scripts/test-skill-validator.py
python scripts/build-skills.py --check
python scripts/test-adapter-distribution.py
python scripts/build-adapters.py --version 0.1.1 --check
python scripts/validate-adapters.py --version 0.1.1
python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation
python scripts/validate-change-metadata.py docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml
python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md --path docs/proposals/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md --path specs/token-cost-measurement-baseline-and-proposal-scope-preservation.md --path specs/token-cost-measurement-baseline-and-proposal-scope-preservation.test.md --path docs/architecture/system/architecture.md --path docs/reports/token-cost/2026-05-10-baseline.md --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml
git diff --check -- .
```

Use selector-selected CI once changed paths are known:

```bash
python scripts/select-validation.py --mode explicit --path <changed-path>...
bash scripts/ci.sh --mode explicit --path <changed-path>...
```

## Risks and Recovery

- JSONL shape uncertainty: keep parsing defensive, report unknown shapes, and cover malformed input in tests.
- Approximate token estimates: label estimates and keep thresholds warning-only.
- Public skill leakage: keep maintainer-only commands in specs/plans/tests/change evidence, not shipped skill text.
- Generated-output drift: regenerate from canonical sources and verify with drift checks.
- Lifecycle drift: update `Current Handoff Summary`, milestone states, `change.yaml`, `review-log.md`, `review-resolution.md`, and `docs/plan.md` before claiming downstream readiness.

## Dependencies

- Proposal status is `accepted`.
- Spec status is `approved`.
- Canonical architecture update is approved by architecture-review R1.
- Plan-review R1 approved this plan.
- Test spec is active and must guide implementation.
- M1-M4 must each complete implementation handoff, code-review, and review closeout before M5 final lifecycle closeout.
- Adapter validation uses version `0.1.1` because `scripts/validate-adapters.py` requires `--version` in this repository.

## Progress

- 2026-05-10: plan created after proposal-review R2, spec-review R1, and architecture-review R1 approval.
- 2026-05-10: test spec created and activated after plan-review R1 approval; M1 is ready to start implementation.
- 2026-05-10: M1 implementation started for static skill measurement and Codex JSONL session analysis.
- 2026-05-10: M1 added static skill measurement, Codex JSONL session analysis, focused parser tests, a small JSONL fixture, and change-local explanation evidence. M1 is ready for code-review.
- 2026-05-10: M1 code-review completed clean-with-notes with no material findings; M1 is closed and the plan is active for M2.
- 2026-05-10: M2 implementation started for durable baseline report and change-local links.
- 2026-05-10: M2 added the first durable token-cost baseline report, change-local report links, and a lightweight report-shape regression test. M2 is ready for code-review.
- 2026-05-10: M2 code-review completed clean-with-notes with no material findings; M2 is closed and the plan is active for M3.
- 2026-05-10: M3 implementation started for proposal/proposal-review scope preservation guidance and validator coverage.
- 2026-05-10: M3 added proposal/proposal-review scope preservation guidance and narrow static validator coverage. M3 is ready for code-review.
- 2026-05-10: M3 code-review R1 requested changes for TCSP-CR-M3-F1. M3 is in review-resolution; do not start M4 until the finding is resolved, targeted validation passes, and M3 returns to code-review.

## Decision Log

- 2026-05-10: split implementation into measurement scripts, baseline report/evidence, skill/validator updates, generated output refresh, and final lifecycle closeout -> keeps each review loop focused and prevents generated-output churn from mixing with hand-authored behavior changes.
- 2026-05-10: use adapter version `0.1.1` for adapter drift and validation -> `validate-adapters.py` currently requires `--version`, and `build-adapters.py` defaults to `0.1.1`.
- 2026-05-10: keep M5 as lifecycle-closeout only -> final closeout must wait until M1-M4 are closed through their milestone review loops.
- 2026-05-10: manually route M1 script and fixture validation because `scripts/select-validation.py` currently classifies the new token-cost scripts as `script-unsupported` and the token-cost fixture path as unclassified; direct script tests and commands are the authoritative M1 proof.
- 2026-05-10: manually route M2 report validation because `scripts/select-validation.py` currently leaves `docs/reports/token-cost/2026-05-10-baseline.md` unclassified and the updated script test as `script-unsupported`; direct report-shape tests, lifecycle validation, and change metadata validation are the authoritative M2 proof.
- 2026-05-10: keep M3 validator coverage as exact section and phrase checks -> satisfies R10 without broad semantic scoring.
- 2026-05-10: leave generated Codex skill mirror and public adapter refresh to M4 -> M3 changes canonical skill text only, while M4 owns `.codex/skills/` and `dist/adapters/` updates after M3 code-review.

## Surprises and Discoveries

- none yet

## Validation Notes

- Test spec authoring validation passed:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md --path docs/proposals/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md --path specs/token-cost-measurement-baseline-and-proposal-scope-preservation.md --path specs/token-cost-measurement-baseline-and-proposal-scope-preservation.test.md --path docs/architecture/system/architecture.md --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/review-log.md --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/review-resolution.md`
  - `git diff --check -- specs/token-cost-measurement-baseline-and-proposal-scope-preservation.test.md specs/token-cost-measurement-baseline-and-proposal-scope-preservation.md docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation`
- Lifecycle validation still reports the pre-existing unrelated `docs/plan.md` line 20 lifecycle-language warning.
- M1 implementation validation passed:
  - `python scripts/test-token-cost-measurement.py`
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/analyze-codex-jsonl.py tests/fixtures/token-cost/sample-codex-session.jsonl`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/select-validation.py --mode explicit --path scripts/measure-skill-tokens.py --path scripts/analyze-codex-jsonl.py --path scripts/test-token-cost-measurement.py --path tests/fixtures/token-cost/sample-codex-session.jsonl --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml --path docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/explain-change.md`
  - Selector result: blocked only for manual routing of `script-unsupported` paths and the unclassified token-cost fixture; selected checks were artifact lifecycle, change metadata regression, and change metadata validation.
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md --path docs/proposals/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md --path specs/token-cost-measurement-baseline-and-proposal-scope-preservation.md --path specs/token-cost-measurement-baseline-and-proposal-scope-preservation.test.md --path docs/architecture/system/architecture.md --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/review-log.md --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/review-resolution.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/explain-change.md --path docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md`
  - `git diff --check -- scripts tests/fixtures/token-cost docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md specs/token-cost-measurement-baseline-and-proposal-scope-preservation.test.md specs/token-cost-measurement-baseline-and-proposal-scope-preservation.md`
- M2 implementation validation passed:
  - `python scripts/test-token-cost-measurement.py`
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/analyze-codex-jsonl.py tests/fixtures/token-cost/sample-codex-session.jsonl`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/reports/token-cost/2026-05-10-baseline.md --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`
  - `python scripts/select-validation.py --mode explicit --path docs/reports/token-cost/2026-05-10-baseline.md --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/explain-change.md --path scripts/test-token-cost-measurement.py --path docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md`
  - Selector result: blocked only for manual routing of the unclassified token-cost report and `script-unsupported` test path; selected checks were artifact lifecycle, change metadata regression, and change metadata validation.
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/explain-change.md --path docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation`
  - `git diff --check -- docs/reports/token-cost docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation scripts/test-token-cost-measurement.py docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md`
- M2 code-review validation rerun passed:
  - `python scripts/test-token-cost-measurement.py`
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/analyze-codex-jsonl.py tests/fixtures/token-cost/sample-codex-session.jsonl`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/reports/token-cost/2026-05-10-baseline.md --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/explain-change.md --path docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md`
  - `git diff --check -- HEAD~1..HEAD`
- M3 implementation validation passed:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/select-validation.py --mode explicit --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path scripts/test-skill-validator.py --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/explain-change.md --path docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md`
  - Selector result: selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.drift`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`; no blocking results.
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/explain-change.md --path docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md --path skills/proposal-review/SKILL.md --path skills/proposal/SKILL.md`
  - `python scripts/build-skills.py --check` failed with stale generated proposal/proposal-review skill mirrors; this is expected until M4 generated output refresh.
  - `python scripts/build-adapters.py --version 0.1.1 --check` failed with stale generated proposal/proposal-review adapter files; this is expected until M4 generated output refresh.
  - `git diff --check -- skills/proposal/SKILL.md skills/proposal-review/SKILL.md scripts/test-skill-validator.py docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md`
- M3 code-review R1 validation rerun completed:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/explain-change.md --path docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md --path skills/proposal-review/SKILL.md --path skills/proposal/SKILL.md`
  - `git diff --check -- HEAD~1..HEAD`
  - `python scripts/build-skills.py --check` failed with stale generated proposal/proposal-review skill mirrors; this remains expected M4 scope.
  - `python scripts/build-adapters.py --version 0.1.1 --check` failed with stale generated proposal/proposal-review adapter files; this remains expected M4 scope.
- M3 code-review R1 recording validation passed:
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/review-log.md --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/review-resolution.md --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/reviews/code-review-m3-r1.md --path docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md`
  - `git diff --check -- docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md`
- M1 code-review validation rerun passed:
  - `python scripts/test-token-cost-measurement.py`
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/analyze-codex-jsonl.py tests/fixtures/token-cost/sample-codex-session.jsonl`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml --path docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/explain-change.md --path docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md`
  - `git diff --check -- HEAD~1..HEAD`

## Outcome and Retrospective

- Pending. This plan remains active until all implementation milestones, review loops, final validation, and PR handoff gates are complete.

## Readiness

- See `Current Handoff Summary`.
- This plan is in M3 review-resolution. Return M3 to code-review only after TCSP-CR-M3-F1 is fixed, targeted validation passes, and the milestone state is updated to review-requested.

## Remaining Completion Gates

- M3 review-resolution and code-review closeout
- M4 implementation and code-review closeout
- M5 lifecycle closeout
- explain-change
- verify
- PR handoff
