# Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: commit 187b0b0 M2: validate workflow artifact map drift
Reviewed artifact: commit 187b0b0 M2: validate workflow artifact map drift
Review date: 2026-06-18
Status: changes-requested
Recording status: recorded

## Review inputs

- Diff/review surface: commit `187b0b0` and changed files in the M2 implementation slice.
- Tracked governing branch state: committed M2 branch state on `proposal/workflow-skill-artifact-location-map`.
- Governing artifacts: `specs/workflow-skill-artifact-location-map.md`, `specs/workflow-skill-artifact-location-map.test.md`, and `docs/plans/2026-06-18-workflow-skill-artifact-location-map.md`.
- Validation evidence: M2 validation commands recorded in the active plan and `change.yaml`, including focused workflow-map tests, full skill-validator regression, skill validation, lifecycle validation, selected validation, and selected CI.

## Diff summary

M2 adds workflow artifact-map validation helpers in `scripts/skill_validation.py`, fixture-backed M2 tests in `scripts/test-skill-validator.py`, and lifecycle state updates marking M2 ready for code-review. The validator parses the `Artifact registry` fenced YAML block, checks required fields, checks placement representation shape, compares selected Markdown projections against registry entries, checks workflow skill default path drift, checks first-slice stage-skill contradictions, and exposes an unknown-artifact lookup blocker helper.

## Findings

### WFO-CR1

Finding ID: WFO-CR1
Severity: major
Location: `scripts/skill_validation.py`
Evidence: `specs/workflow-skill-artifact-location-map.md` R15 requires the registry to include architecture records and ADRs, and `specs/workflow-skill-artifact-location-map.test.md` T3 maps R15 to required-entry validation. In `WORKFLOW_ARTIFACT_REQUIRED_REGISTRY_ENTRIES`, the validator requires proposals, specs, test specs, plan surfaces, review/evidence artifacts, PR handoff, and learn sessions, but omits `architecture_record` and `adr`. A direct helper check with those two entries removed from `docs/workflows.md` returned no errors.
Required outcome: The workflow-map validator must fail when `architecture_record` or `adr` is missing from the canonical `artifact_locations` registry.
Safe resolution path: Add `architecture_record` and `adr` to the required registry-entry set, add a targeted regression assertion or fixture that removes those entries and expects artifact-specific missing-entry diagnostics, then rerun the M2 validation set.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | WFO-CR1: R15 requires architecture records and ADRs as required registry entries, but M2 validation does not enforce their presence. |
| Test coverage | block | WFO-CR1: T3 maps R15 to required-entry validation, but the new tests do not remove `architecture_record` or `adr` and assert failure. |
| Edge cases | concern | Duplicate keys, missing owner/trigger, ambiguous placement, stale plan paths, outside-change-pack reviews, and unknown artifact inputs have tests; missing architecture/ADR coverage is the blocking gap. |
| Error handling | pass | Invalid registry shape and unknown artifact lookup return deterministic errors rather than derived paths. |
| Architecture boundaries | pass | The implementation stays in validation helpers, fixture tests, and lifecycle state; it does not redefine runtime architecture or artifact schemas. |
| Compatibility | pass | Plan-body placement remains under `docs/plans/YYYY-MM-DD-slug.md`; no plan files were migrated. |
| Security/privacy | pass | The diff does not introduce secrets, external calls, credential handling, or unsafe logging. |
| Derived artifact currency | pass | Selected CI included skill generation regression after validator changes. |
| Unrelated changes | pass | The diff is scoped to M2 validator/test work plus lifecycle state. |
| Validation evidence | concern | The recorded commands are relevant and passed, but WFO-CR1 shows the targeted assertions are incomplete for R15. |

## No-finding rationale

Not applicable; material finding `WFO-CR1` requires resolution before M2 can close.

## Residual risks

After `WFO-CR1` is fixed, re-review should confirm that required-entry validation covers every artifact type named by R15 and that the new regression fails for the original omission.

## Milestone handoff

- Reviewed milestone: M2
- Review status: changes-requested
- Milestone closeout: resolution-needed
- Required review-resolution: yes
- Remaining implementation milestones: M2 resolution-needed, M3
- Next stage: review-resolution
- Verify readiness: not-claimed
