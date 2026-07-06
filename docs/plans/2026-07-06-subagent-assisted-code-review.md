# Subagent-Assisted Code Review

## Status

Plan lifecycle state: active
Terminal disposition: none

- Owner: maintainers
- Change ID: 2026-07-06-subagent-assisted-code-review
- Start date: 2026-07-06
- Last updated: 2026-07-06
- Related issue or PR: none yet
- Supersedes: none

## Goal

Implement the approved subagent-assisted code review contract while preserving direct code review, single reviewer-of-record authority, existing review-resolution behavior, and existing verify and PR readiness boundaries.

## Why now

Broad RigorLoop changes increasingly span workflow policy, validators, generated output, release packaging, and public skill behavior.
The approved proposal and spec define a bounded way to widen review coverage without fragmenting lifecycle authority.

## Scope

### In scope

- Update canonical `code-review` skill guidance and assets for subagent selection, packet shape, aggregation, coverage recording, and advisory import behavior.
- Add validation and fixture coverage for closed role vocabulary, packet schema, malformed or missing packets, unknown statuses, deduplication, conflict handling, and coverage records.
- Prove generated skill and adapter packaging stays aligned through existing repository-owned generation and validation commands.
- Keep direct code review without subagents available.
- Keep review-resolution, verify, and PR readiness boundaries unchanged.

### Out of scope

- Implementing runtime subagent orchestration as a new service.
- Persisting raw subagent packet files in the first slice.
- Packaging Claude custom subagent configs for every role.
- Making Codex or GitHub review mandatory for every PR.
- Running subagents in parallel.
- Auto-applying code-review findings.
- Hand-editing generated adapter output.

## Constraints

- `skills/` is the only authored skill source.
- Generated public adapter skill bodies must not be hand-edited.
- Existing direct code-review behavior must remain valid.
- Unknown closed-vocabulary values must fail closed and have regression coverage.
- Formal review records must remain canonical lifecycle evidence.
- Implementation must not proceed until this plan has an approved recorded plan-review and the matching test spec has approved recorded test-spec-review.

## Source artifacts

- Proposal: `docs/proposals/2026-07-06-subagent-assisted-code-review.md`
- Proposal review: `docs/changes/2026-07-06-subagent-assisted-code-review/reviews/proposal-review-r1.md`
- Spec: `specs/subagent-assisted-code-review.md`
- Spec review: `docs/changes/2026-07-06-subagent-assisted-code-review/reviews/spec-review-r1.md`
- Architecture assessment: `docs/changes/2026-07-06-subagent-assisted-code-review/architecture-assessment.md`
- Test spec: `specs/subagent-assisted-code-review.test.md`

## Context and orientation

The likely authored surfaces are `skills/code-review/SKILL.md`, `skills/code-review/assets/`, review-artifact validators, skill validators, test fixtures, adapter-generation tests, and workflow guidance when affected.

The approved first slice is contract and validation work inside existing repository boundaries.
It does not introduce a persistent packet store, new runtime orchestrator, external review service, or target-native subagent configuration generator.

## Requirements covered

| Requirement | Plan coverage |
|---|---|
| R1-R2 | M1 direct-review preservation and reviewer-of-record guidance |
| R3-R5 | M1 role vocabulary and selection rules, M2 closed-vocabulary validation |
| R6-R8 | M1 packet contract guidance, M2 packet validation fixtures |
| R9-R12 | M1 aggregation and coverage guidance, M2 aggregation validation fixtures |
| R13-R14 | M1 lifecycle boundary and advisory import guidance, M2 validation fixtures |
| R15-R18 | M1 first-slice boundaries, M3 generated output and adapter proof |
| AC1-AC16 | M1-M3 plus test-spec and review evidence |

## Current Handoff Summary

- Current milestone: M2. Validation and fixtures
- Current milestone state: planned
- Latest review evidence: code-review-m1-r1
- Last reviewed milestone: M1. Code-review contract and assets
- Review status: approved; stage=code-review; round=r1
- Remaining in-scope implementation milestones: M2, M3
- Next stage: implement M2
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: implementation-milestones-open, milestone-review-pending, explain-change-pending, verify-pending, pr-handoff-pending — implementation milestones M1-M3, code-review, explain-change, verify, and PR handoff remain.

## Milestones

### M1. Code-review contract and assets

- Milestone state: closed
- Deliverable: update `code-review` guidance and assets for reviewer-of-record invariants, specialist selection, bounded input packets, structured advisory packets, aggregation, coverage recording, advisory external review import, and first-slice non-goals.
- Requirements: R1-R18, AC1-AC16.
- Expected files: `skills/code-review/SKILL.md`, `skills/code-review/assets/` when needed, affected docs when required.
- Validation: `python scripts/validate-skills.py skills/code-review/SKILL.md`; targeted validator tests named by the test spec.
- Implementation handoff:
  - [x] targeted validation passed
  - [x] plan progress and validation notes updated
  - [x] hand off to code-review for M1
- Review closeout:
  - [x] code-review completed
  - [x] material findings resolved or explicitly dispositioned
  - [x] current handoff updated before starting M2
- Milestone commit message: `M1: add subagent-assisted code-review contract`

### M2. Validation and fixtures

- Milestone state: planned
- Deliverable: add repository-owned validation and fixtures for role vocabulary, packet schema, unknown values, malformed packets, missing coverage, dedupe, conflict decisions, low-evidence non-promotion, coverage records, and advisory import summaries.
- Requirements: R3-R14, AC3-AC14.
- Expected files: validator scripts, validator tests, fixtures, and review-artifact validation tests as identified by the test spec.
- Validation: targeted validator regression commands named by the test spec; `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-06-subagent-assisted-code-review` when review artifacts change.
- Implementation handoff:
  - [ ] targeted validation passed
  - [ ] plan progress and validation notes updated
  - [ ] hand off to code-review for M2
- Review closeout:
  - [ ] code-review completed
  - [ ] material findings resolved or explicitly dispositioned
  - [ ] current handoff updated before starting M3
- Milestone commit message: `M2: validate subagent review packets and coverage`

### M3. Generated output and adapter proof

- Milestone state: planned
- Deliverable: prove generated skills and adapter artifacts include the updated canonical code-review skill and assets through repository-owned generation and validation, without hand-editing generated output.
- Requirements: R13-R18, AC12-AC16.
- Expected files: generated-output tests or adapter distribution tests when needed; change-local behavior-preservation evidence.
- Validation: `python scripts/build-skills.py --check`; relevant adapter generation or distribution tests named by the test spec; `python scripts/validate-skills.py`.
- Implementation handoff:
  - [ ] targeted validation passed
  - [ ] behavior-preservation evidence recorded when needed
  - [ ] plan progress and validation notes updated
  - [ ] hand off to code-review for M3
- Review closeout:
  - [ ] code-review completed
  - [ ] material findings resolved or explicitly dispositioned
  - [ ] current handoff updated before final closeout
- Milestone commit message: `M3: prove subagent review packaging alignment`

## Validation plan

- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-07-06-subagent-assisted-code-review.md --path specs/subagent-assisted-code-review.md --path docs/plans/2026-07-06-subagent-assisted-code-review.md --path docs/plan.md --path docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml`: lifecycle artifact status and readiness.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-06-subagent-assisted-code-review`: review-record structure.
- `python scripts/validate-change-metadata.py docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml`: change metadata.
- `python scripts/validate-skills.py skills/code-review/SKILL.md`: skill syntax and asset references.
- Targeted validator regression commands from the test spec for closed vocabulary, packet schema, coverage section, aggregation, and advisory import behavior.
- Generated-output and adapter tests named by the test spec after M3.

## Risks and recovery

- Risk: subagent guidance becomes noisy and weakens review focus.
  - Recovery: keep material-promotion rules evidence-bound and preserve direct review.
- Risk: validation overfits to one packet shape and blocks useful target-native advisory output.
  - Recovery: keep advisory import separate from canonical packet validation and specify source, scope, and limitations.
- Risk: generated adapter output drifts from canonical skill source.
  - Recovery: rely on existing build and adapter validation commands, not hand edits.
- Risk: first slice expands into runtime orchestration or persistence.
  - Recovery: route expansion back to architecture and proposal/spec amendment before implementation.

## Dependencies

- Accepted proposal and approved spec are present.
- Architecture assessment records architecture-not-required for the first slice.
- Test spec must be authored and approved before implementation.
- Existing validators and adapter-generation scripts remain the preferred proof surfaces.

## Progress

- 2026-07-06: proposal authored, proposal-review approved, proposal accepted, spec authored, spec-review approved, architecture assessment recorded, and execution plan created.
- 2026-07-06: plan-review R1 approved the execution plan with no material findings.
- 2026-07-06: test spec authored and ready for test-spec-review.
- 2026-07-06: test-spec-review R1 approved the proof map with no material findings; workflow auto target reached.
- 2026-07-06: M1 implementation started; focused static proof for subagent-assisted code-review guidance now fails before the skill contract update.
- 2026-07-06: M1 implementation added the subagent-assisted code-review contract to `skills/code-review/SKILL.md` and focused static proof in `scripts/test-skill-validator.py`.
- 2026-07-06: M1 targeted validation passed and the milestone is ready for `code-review`.
- 2026-07-06: code-review M1 R1 completed clean-with-notes with no material findings; M1 closed and workflow routed to `implement M2`.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-07-06 | Split implementation into code-review contract, validation fixtures, and generated-output proof. | This keeps behavior, validation, and packaging reviewable while preserving direct review. | One large implementation milestone. |
| 2026-07-06 | Defer persistent packet files and parallel execution. | The approved first slice records summarized coverage and needs deterministic validation first. | Building storage or parallel orchestration immediately. |
| 2026-07-06 | Keep code-review result assets unchanged in M1. | The new coverage table is optional review-record guidance for subagent-assisted mode, not a parser-owned result field. | Adding new skeleton fields before review-artifact validation exists. |

## Surprises and discoveries

- None yet.
- No new `skills/code-review/assets/` file was needed for M1; the existing parser-owned result and material-finding assets remain valid.

## Validation notes

- Plan-review R1 approved the plan with no material findings.
- Test spec authored with validation command ledger and milestone proof map.
- Test-spec-review R1 approved the proof map with implementation handoff allowed.
- M1 failing proof before implementation: `python scripts/test-skill-validator.py -k subagent_code_review` failed because the code-review skill lacked the new subagent-assisted contract terms.
- M1 validation passed: `python scripts/test-skill-validator.py -k subagent_code_review`.
- M1 validation passed: `python scripts/validate-skills.py skills/code-review/SKILL.md`.
- Code-review M1 R1 reviewer rerun passed: `python scripts/test-skill-validator.py -k subagent_code_review`.
- Code-review M1 R1 reviewer rerun passed: `python scripts/validate-skills.py skills/code-review/SKILL.md`.
- Code-review M1 R1 reviewer rerun passed: `python scripts/validate-change-metadata.py docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml`.

## Outcome and retrospective

- Pending.

## Readiness

- See `Current Handoff Summary`.
- Lifecycle routing is owned by `Current Handoff Summary`.
- M2 implementation may begin after clean M1 code-review.

## Risks and follow-ups

- Revisit architecture if implementation introduces persistent packet files, reusable orchestration, target-native config generation, new dependencies, or external review-service integration.
