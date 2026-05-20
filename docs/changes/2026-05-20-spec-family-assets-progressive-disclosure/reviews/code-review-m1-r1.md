# Code Review M1 R1

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M1. Baseline summary and validator foundation
Reviewed artifact: commit `9bfc927` (`M1: add spec-family asset validation baseline`)
Review date: 2026-05-20
Status: changes-requested
Recording status: recorded

## Scope

Reviewed the M1 implementation slice against the approved spec, active test
spec, active plan, implementation diff, baseline evidence, validator changes,
and recorded validation evidence.

## Review inputs

- Diff: `git show --unified=80 --no-ext-diff --no-renames HEAD -- scripts/skill_validation.py scripts/test-skill-validator.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md docs/plan.md specs/spec-family-assets-progressive-disclosure.md specs/spec-family-assets-progressive-disclosure.test.md`
- Plan: `docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md`
- Spec: `specs/spec-family-assets-progressive-disclosure.md`
- Test spec: `specs/spec-family-assets-progressive-disclosure.test.md`
- Baseline: `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/baseline.md`
- Preservation scaffold: `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/behavior-preservation.md`
- Validation evidence: commit body and `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`

## Diff summary

- Added the accepted proposal, approved spec, active test spec, active plan,
  and prior proposal/spec/plan review records for this change.
- Added `baseline.md` with the proof-route assessment and source-to-asset
  baseline mapping.
- Added `behavior-preservation.md` with M1 scope, proof-route decision, and
  preservation matrix scaffold for M2 through M4.
- Extended `scripts/skill_validation.py` with spec-family asset allowlists and
  checks for approved asset paths, asset-only scope, metadata, statuses,
  placeholders, filler prose, repository-root dependencies, `COPY` entries,
  fill-field wording, no-placeholder instructions, and `spec-review` policy
  prose.
- Extended `scripts/test-skill-validator.py` with temporary spec-family asset
  fixtures and negative cases for asset path, resource-map, metadata, status,
  placeholder, filler, root-dependency, review-policy, and baseline-summary
  checks.
- Updated the plan and plan index to mark M1 `review-requested`.

## Findings

### SFA-M1-CR1 - Major: generated-output presence coverage is missing from the M1 validator foundation

Finding ID: SFA-M1-CR1
Severity: major
Location: `scripts/skill_validation.py`; `scripts/test-skill-validator.py`; `docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md`, M1 steps

Evidence:
The approved spec requires validator or fixture coverage for generated-output
presence:

```text
SFA-R42. The implementation MUST update validator or test fixtures needed to
deterministically check asset mapping, COPY usage, metadata comments, allowed
statuses, placeholder policy, review-class asset boundary, generated-output
presence, and baseline-summary presence.
```

The M1 plan repeats this obligation in the M1 steps: add deterministic checks
for asset mapping, `COPY`, metadata, status values, placeholders,
review-class boundaries, generated-output presence, and baseline-summary
presence.

The implementation adds deterministic checks and tests for the canonical asset
layout/content surfaces and for baseline-summary presence, but no validator
logic or test fixture checks generated skill mirror presence or generated
adapter output presence. The only generated-output coverage remains future
manual/integration proof in M5, which does not satisfy the M1 validator
foundation requirement for generated-output presence coverage.

Problem:
M1 is the validator foundation slice. Without at least a deterministic helper
or fixture-level check for generated-output presence, later milestones can add
canonical assets and still rely on separate manual archive inspection rather
than a repo-owned check that every mapped asset reaches the generated output
surface.

Required outcome:
Add deterministic generated-output presence coverage to the M1 validator
foundation, or revise the approved plan/test-spec through the workflow if the
team intentionally wants to defer that coverage outside M1.

Safe resolution path:
Extend the validator/test foundation with a deterministic generated-output
presence check, such as a helper that compares mapped canonical asset paths
against a supplied generated skill mirror or adapter output root, with positive
and negative tests proving missing generated assets fail. Keep temporary
archive generation and full adapter validation in M5; the M1 fix only needs to
provide the deterministic coverage hook required by `SFA-R42`.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | `SFA-R42` includes generated-output presence in the required validator/test coverage, but M1 does not implement that coverage. |
| Test coverage | block | New tests cover canonical asset layout/content and baseline presence, but no generated-output presence positive or negative case exists. |
| Edge cases | concern | `EC3` and `EC4` are assigned to later generated-output proof, but M1's validator foundation still lacks the deterministic generated-output presence hook required by `SFA-R42`. |
| Error handling | concern | Missing generated assets would not be caught by the new M1 validator checks. |
| Architecture boundaries | pass | No architecture or ADR boundary is changed. |
| Compatibility | pass | No adapter roots, lockfiles, CLI behavior, or release archive trust boundaries are changed. |
| Security/privacy | pass | The validator adds repository-root dependency checks for assets and no secrets or private data are introduced. |
| Derived artifact currency | concern | Generated-output currency is intentionally future milestone work, but deterministic generated-output presence coverage is missing from this validator-foundation slice. |
| Unrelated changes | pass | The diff is scoped to lifecycle artifacts, validator foundation, and review evidence for the approved change. |
| Validation evidence | pass | Recorded commands are relevant and pass, but passing validation does not cover the missing generated-output presence check. |

## Required review-resolution

Yes. `SFA-M1-CR1` must be resolved before M1 can close or M2 can begin.

## Handoff

- Reviewed milestone: M1. Baseline summary and validator foundation
- Review status: changes-requested
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4, M5
- Recommended next stage: review-resolution / implement M1 fix
- Final closeout readiness: not ready
