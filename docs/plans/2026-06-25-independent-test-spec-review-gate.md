# Independent Test-Spec-Review Gate Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Owner: maintainers
- Start date: 2026-06-25
- Last updated: 2026-06-25
- Change ID: 2026-06-25-independent-test-spec-review-gate
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

Implement the approved independent `test-spec-review` gate so formal workflow-managed test specs receive proof-map adequacy review before implementation begins.

The plan sequences the workflow/spec contract, canonical skill and asset additions, validator support, generated adapter proof, and lifecycle evidence without starting implementation before `plan-review` and `test-spec`.

## Source artifacts

- Proposal: [docs/proposals/2026-06-25-independent-test-spec-review-gate.md](../proposals/2026-06-25-independent-test-spec-review-gate.md)
- Spec: [specs/test-spec-review-gate.md](../../specs/test-spec-review-gate.md)
- Architecture: [docs/architecture/2026-06-25-independent-test-spec-review-gate.md](../architecture/2026-06-25-independent-test-spec-review-gate.md)
- ADR: [docs/adr/ADR-20260625-independent-test-spec-review-gate.md](../adr/ADR-20260625-independent-test-spec-review-gate.md)
- Test spec: [specs/test-spec-review-gate.test.md](../../specs/test-spec-review-gate.test.md)
- Change metadata: [docs/changes/2026-06-25-independent-test-spec-review-gate/change.yaml](../changes/2026-06-25-independent-test-spec-review-gate/change.yaml)

## Context and orientation

The change affects repository workflow infrastructure, not product runtime code. Likely implementation surfaces include:

- `specs/rigorloop-workflow.md` and matching test spec;
- `specs/skill-contract.md` and matching test spec if the new skill/assets require a skill-contract amendment;
- `docs/workflows.md` and possibly `AGENTS.md`;
- `skills/test-spec/SKILL.md`, `skills/implement/SKILL.md`, `skills/workflow/SKILL.md`, and new `skills/test-spec-review/`;
- `scripts/validate-review-artifacts.py`, review-artifact parser code, change-metadata/lifecycle validators, skill validators, and fixtures;
- generated or release-package validation surfaces for supported adapters.

Generated public adapter skill bodies are not authored source and must not be hand-edited.

## Non-goals

- Do not implement historical test-spec migration.
- Do not add automated semantic scoring.
- Do not require a different model or vendor for this review stage.
- Do not execute final validation during `test-spec-review`.
- Do not redesign `code-review` or `verify`.
- Do not start `test-spec` or implementation as part of this authoring-through-plan-review profile.

## Requirements covered

- R1-R4: M1
- R5-R12: M1, M3
- R13-R18: M2, M3
- R19-R21: M1, M3
- R22-R24: M2, M3
- R25-R26: M2
- R27: M3
- R28: M3

## Current Handoff Summary

- Current milestone: M3. Validators, fixtures, generated package proof, and representative evidence
- Current milestone state: closed
- Latest review evidence: code-review-r3
- Last reviewed milestone: M3. Validators, fixtures, generated package proof, and representative evidence
- Review status: approved; stage=code-review; round=r3
- Remaining in-scope implementation milestones: none
- Next stage: pr
- Final closeout readiness: ready
- Reason final closeout is or is not ready: ready — local verify complete; PR handoff remains.

## Milestones

### M1. Workflow and contract baseline

- Milestone state: closed
- Requirements: R1-R12, R19-R21
- Deliverable: workflow/spec amendments define stage order, test-spec `active` preservation, result enums, handoff mapping, staleness, upstream revision routing, and implementation eligibility.
- Likely files: `specs/rigorloop-workflow.md`, `specs/rigorloop-workflow.test.md`, `docs/workflows.md`, `AGENTS.md` if affected, change-local behavior-preservation evidence.
- Validation:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
  - targeted workflow/spec static checks added or updated in repo-owned tests
- Implementation handoff:
  - [x] targeted validation passed
  - [x] hand off to code-review for M1
- Review closeout:
  - [x] code-review completed
  - [x] material findings resolved or explicitly dispositioned
  - [x] lifecycle handoff updated before starting the next implementation milestone
- Milestone commit message: `M1: add test-spec-review workflow contract`

### M2. Canonical skill and review assets

- Milestone state: closed
- Requirements: R13-R18, R22-R26
- Deliverable: add `skills/test-spec-review/SKILL.md`, result and material-finding assets, update `test-spec`, `implement`, and workflow-facing skill wording.
- Likely files: `skills/test-spec-review/SKILL.md`, `skills/test-spec-review/assets/review-result-skeleton.md`, `skills/test-spec-review/assets/material-finding.md`, `skills/test-spec/SKILL.md`, `skills/implement/SKILL.md`, `skills/workflow/SKILL.md`.
- Validation:
  - `python scripts/test-skill-validator.py`
  - targeted skill phrase/resource-map checks
- Implementation handoff:
  - [x] targeted validation passed
  - [x] hand off to code-review for M2
- Review closeout:
  - [x] code-review completed
  - [x] material findings resolved or explicitly dispositioned
  - [x] lifecycle handoff updated before starting the next implementation milestone
- Milestone commit message: `M2: add test-spec-review skill`

### M3. Validators, fixtures, generated package proof, and representative evidence

- Milestone state: closed
- Requirements: R5-R12, R19-R23, R27-R28
- Deliverable: validator recognition for the new stage and result fields, unknown-value regression tests, formal review placement checks, stale-review fixture coverage where feasible, generated adapter inclusion proof, and representative review fixtures.
- Likely files: `scripts/`, `tests/fixtures/`, `dist/adapters/README.md` or manifest support surface if needed, change-local behavior-preservation evidence, generated package proof reports.
- Validation:
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-25-independent-test-spec-review-gate`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-25-independent-test-spec-review-gate/change.yaml`
  - targeted validator unit tests
  - adapter generation/package validation command named by the test spec
- Implementation handoff:
  - [x] targeted validation passed
  - [x] hand off to code-review for M3
- Review closeout:
  - [x] code-review completed
  - [x] material findings resolved or explicitly dispositioned
  - [x] lifecycle handoff updated before final lifecycle closeout
- Milestone commit message: `M3: validate test-spec-review lifecycle evidence`

## Validation plan

- `python scripts/validate-change-metadata.py docs/changes/2026-06-25-independent-test-spec-review-gate/change.yaml`: validate change metadata and autoprogression authorization shape.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-25-independent-test-spec-review-gate`: validate formal review records and review log.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-25-independent-test-spec-review-gate.md --path specs/test-spec-review-gate.md --path docs/architecture/2026-06-25-independent-test-spec-review-gate.md --path docs/adr/ADR-20260625-independent-test-spec-review-gate.md --path docs/plans/2026-06-25-independent-test-spec-review-gate.md --path docs/plan.md --path docs/changes/2026-06-25-independent-test-spec-review-gate/change.yaml --path docs/changes/2026-06-25-independent-test-spec-review-gate/review-log.md`: validate lifecycle-managed artifacts touched by the authoring stages.
- `git diff --check -- docs/proposals/2026-06-25-independent-test-spec-review-gate.md specs/test-spec-review-gate.md docs/architecture/2026-06-25-independent-test-spec-review-gate.md docs/adr/ADR-20260625-independent-test-spec-review-gate.md docs/plans/2026-06-25-independent-test-spec-review-gate.md docs/plan.md docs/changes/2026-06-25-independent-test-spec-review-gate`: whitespace sanity check.
- Test-spec stage refined milestone-specific validator and adapter commands in `specs/test-spec-review-gate.test.md`.

## Risks and recovery

- Risk: The new gate duplicates `spec-review`, `plan-review`, `code-review`, or `verify`.
  - Recovery: Keep review dimensions proof-map-only and preserve downstream review backstops in skill and validator checks.
- Risk: Staleness detection is under-specified.
  - Recovery: First slice uses tracked review/change evidence and explicit substantive-change categories; route hash/fingerprint work to a follow-on proposal if needed.
- Risk: Generated adapter packaging drifts.
  - Recovery: Use normal generation and package validation; do not hand-edit generated public adapter bodies.
- Risk: Implementation starts after `test-spec` without the new review evidence.
  - Recovery: Add implement-skill gate wording and validator/fixture proof before implementation milestones close.

## Dependencies

- Accepted proposal and approved spec.
- Approved architecture record and ADR.
- Clean plan-review before `test-spec`.
- Test-spec before implementation.
- Existing review-family recording and validator patterns.

## Progress

- 2026-06-25: Proposal authored, proposal-review approved, spec authored and approved, architecture assessment recorded as required, architecture and ADR authored and approved, plan authored and plan-review approved.
- 2026-06-25: Test spec authored as the active proof-planning surface; next stage is `implement M1`.
- 2026-06-25: M1 implemented workflow/spec contract baseline, review-artifact validator recognition for `test-spec-review`, result-field closed-vocabulary checks, workflow summary/root guidance updates, and behavior-preservation evidence; next stage is `code-review M1`.
- 2026-06-25: M1 code-review completed clean with no material findings; M1 is closed and next stage is `implement M2`.
- 2026-06-25: M2 added canonical `test-spec-review` skill/assets, updated adjacent `test-spec`, `implement`, and `workflow` routing, and extended review-family skill validation; next stage is `code-review M2`.
- 2026-06-25: M2 code-review completed clean with no material findings; M2 is closed and next stage is `implement M3`.
- 2026-06-25: M3 added lifecycle review-stage recognition for `test-spec-review`, adapter manifest inclusion for the new skill, generated-adapter validation proof, `v`-prefixed adapter version alias handling, and v0.1.5 release-metadata alignment for alias smoke evidence; next stage is `code-review M3`.
- 2026-06-25: M3 code-review completed clean with no material findings; all implementation milestones are closed and next stage is `explain-change`.
- 2026-06-25: Explain-change recorded durable change rationale; next stage is `verify`.
- 2026-06-25: Final verify passed; next stage is `pr`.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-25 | Split implementation into three milestones. | Keeps workflow contract, skill assets, and validators/generated proof reviewable. | One large implementation slice. |
| 2026-06-25 | Defer test-spec authoring until after plan-review. | The current autoprogression profile stops after clean plan-review. | Continue into test-spec under `auto-through: plan-review`. |

## Surprises and discoveries

- 2026-06-25: Regenerating adapter metadata for `v0.1.5` exposed that adapter version parsing did not treat `v`-prefixed release tags as semver for OpenCode command aliases. M3 fixed the parser and added a regression before recording generated package proof.

## Validation notes

- 2026-06-25: Test-spec authoring validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-25-independent-test-spec-review-gate/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-25-independent-test-spec-review-gate`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-25-independent-test-spec-review-gate.md --path specs/test-spec-review-gate.md --path specs/test-spec-review-gate.test.md --path docs/architecture/2026-06-25-independent-test-spec-review-gate.md --path docs/adr/ADR-20260625-independent-test-spec-review-gate.md --path docs/plans/2026-06-25-independent-test-spec-review-gate.md --path docs/plan.md --path docs/changes/2026-06-25-independent-test-spec-review-gate/change.yaml --path docs/changes/2026-06-25-independent-test-spec-review-gate/review-log.md --path docs/changes/2026-06-25-independent-test-spec-review-gate/reviews/proposal-review-r1.md --path docs/changes/2026-06-25-independent-test-spec-review-gate/reviews/spec-review-r1.md --path docs/changes/2026-06-25-independent-test-spec-review-gate/reviews/architecture-review-r1.md --path docs/changes/2026-06-25-independent-test-spec-review-gate/reviews/plan-review-r1.md --path docs/changes/2026-06-25-independent-test-spec-review-gate/reviews/plan-review-r2.md`
  - `git diff --check -- docs/proposals/2026-06-25-independent-test-spec-review-gate.md specs/test-spec-review-gate.md specs/test-spec-review-gate.test.md docs/architecture/2026-06-25-independent-test-spec-review-gate.md docs/adr/ADR-20260625-independent-test-spec-review-gate.md docs/plans/2026-06-25-independent-test-spec-review-gate.md docs/plan.md docs/changes/2026-06-25-independent-test-spec-review-gate`
- 2026-06-25: M1 implementation validation passed:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-skill-validator.py -k implementation_through_verify_behavior_preservation_covers_acceptance_and_itv_checks`
  - `python scripts/test-skill-validator.py -k test_test_spec_review_gate_workflow_baseline_surfaces_are_declared`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-25-independent-test-spec-review-gate`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-25-independent-test-spec-review-gate/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-25-independent-test-spec-review-gate.md --path specs/test-spec-review-gate.md --path specs/test-spec-review-gate.test.md --path docs/architecture/2026-06-25-independent-test-spec-review-gate.md --path docs/adr/ADR-20260625-independent-test-spec-review-gate.md --path docs/plans/2026-06-25-independent-test-spec-review-gate.md --path docs/plan.md --path docs/changes/2026-06-25-independent-test-spec-review-gate/change.yaml --path docs/changes/2026-06-25-independent-test-spec-review-gate/review-log.md --path docs/changes/2026-06-25-independent-test-spec-review-gate/reviews/proposal-review-r1.md --path docs/changes/2026-06-25-independent-test-spec-review-gate/reviews/spec-review-r1.md --path docs/changes/2026-06-25-independent-test-spec-review-gate/reviews/architecture-review-r1.md --path docs/changes/2026-06-25-independent-test-spec-review-gate/reviews/plan-review-r1.md --path docs/changes/2026-06-25-independent-test-spec-review-gate/reviews/plan-review-r2.md`
  - `git diff --check -- AGENTS.md docs/workflows.md specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md scripts/review_artifact_validation.py scripts/test-review-artifact-validator.py scripts/test-skill-validator.py docs/changes/2026-06-25-independent-test-spec-review-gate/change.yaml`
- 2026-06-25: M2 implementation validation passed:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py -k test_test_spec_review`
  - `python scripts/test-skill-validator.py`
  - `git diff --check -- skills/test-spec-review skills/test-spec/SKILL.md skills/implement/SKILL.md skills/workflow/SKILL.md scripts/skill_validation.py scripts/test-skill-validator.py`
- 2026-06-25: M3 implementation validation passed:
  - `python scripts/test-artifact-lifecycle-validator.py -k workflow_state_owner_review_status_cases`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_manifest_records_opencode_command_aliases_for_v_prefixed_releases AdapterDistributionTests.test_adapter_manifest_remains_metadata_only AdapterDistributionTests.test_generated_adapter_archives_are_not_committed`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version v0.1.5 --check`
  - `python scripts/validate-adapters.py --version v0.1.5`
  - `python scripts/validate-release-ci.py --version v0.1.5`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-25-independent-test-spec-review-gate/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-25-independent-test-spec-review-gate`

## Outcome and retrospective

- Final verify passed locally. PR handoff remains.

## Readiness

- See `Current Handoff Summary`.
- Lifecycle routing is owned by `Current Handoff Summary`.
