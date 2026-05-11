# Plan Review R1

Review ID: plan-review-r1
Stage: plan-review
Round: 1
Reviewer: Contributor plan-review
Target: docs/plans/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md
Status: revise

## Review inputs

- Plan: `docs/plans/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md`
- Spec: `specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.md`
- Architecture: `docs/architecture/system/architecture.md`
- Architecture review: `docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/reviews/architecture-review-r1.md`
- Existing release benchmark test spec: `specs/release-token-friendliness-benchmark-for-skills.test.md`
- Governance: `AGENTS.md`, `CONSTITUTION.md`, `docs/workflows.md`

## Findings

### EDTF-PL1 - Test-spec is modeled as an implementation milestone

Finding ID: EDTF-PL1
Severity: material
Status: open

Evidence: The plan's `Current Handoff Summary` lists `M1. Test spec for v2 benchmark expansion` as the current milestone and includes `M1` in the remaining in-scope implementation milestones. The M1 section creates `specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.test.md`, which is the workflow `test-spec` stage rather than an implementation slice.

Problem: The plan collapses the next mandatory authoring stage into the implementation milestone loop. That makes downstream routing ambiguous: after plan-review, the immediate next stage should be `test-spec`, while implementation milestones should start only after the test spec is active.

Required outcome: Separate the `test-spec` gate from implementation milestones.

Safe resolution: Move test-spec authoring out of the implementation milestone list and into the plan's handoff/dependency section. Rename the first implementation milestone to the first code/fixture change, such as manifest and required core prompt fixtures. Update `Current Handoff Summary` so the immediate next stage after plan-review is `test-spec`, and the remaining in-scope implementation milestones start after test-spec is complete.

### EDTF-PL2 - M5 release validation command is sequenced before v2 report evidence exists

Finding ID: EDTF-PL2
Severity: material
Status: open

Evidence: M5 validates release integration with `python scripts/validate-release.py --version v0.1.1`, but M6 is the milestone that preserves pre-transition v1 evidence and writes the v2 `v0.1.1` report metadata. M5 therefore may run release validation against pre-v2 or incomplete release metadata.

Problem: The plan includes a real release validation command at a point where the release evidence it needs is intentionally not created yet. That can force either premature report work into M5 or a failing validation command that does not reflect M5's actual integration scope.

Required outcome: M5 validation must prove release-validation delegation and required benchmark context behavior without depending on final v2 report evidence that belongs to M6.

Safe resolution: In M5, use focused tests and fixtures to prove release validation context generation, token-cost validator delegation, changed-skill benchmark requirements, and invalid governed metadata blocking. Move the real `python scripts/validate-release.py --version v0.1.1` command to M6 after the v2 report metadata exists.

## Review dimensions

| Dimension | Result | Notes |
|---|---|---|
| Self-contained context | pass | Source artifacts, current v1 surfaces, and constraints are clearly listed. |
| Source alignment | pass | Milestones trace to approved spec and architecture surfaces. |
| Milestone size | concern | M1 is not an implementation milestone; it is the `test-spec` workflow stage. |
| Sequencing | block | M1 and M5 have sequencing issues that would make downstream handoff or validation ambiguous. |
| Scope discipline | pass | Non-goals are protected. |
| Validation quality | concern | Most commands are concrete, but M5 includes a release command before its required report evidence exists. |
| TDD readiness | concern | Test-spec coverage is identified, but it is placed inside the milestone loop instead of as the next workflow stage. |
| Risk coverage | pass | Rollback and recovery are recorded for v2 report preservation, context generation, and fixture complexity. |
| Architecture alignment | pass | Plan follows architecture-review R1 and does not require unnecessary ADR or diagram work. |
| Operational readiness | concern | Release validation integration is planned, but the real release command should wait for M6 evidence. |
| Plan maintainability | pass | Current handoff, progress, decision log, surprises, and validation notes are present. |

## Outcome

Verdict: revise

Immediate next repository stage: plan

Eventual test-spec readiness: not-ready until EDTF-PL1 and EDTF-PL2 are resolved and plan-review is rerun.

Stop condition: Revise the plan sequencing and M5 validation scope before starting `test-spec` or implementation.
