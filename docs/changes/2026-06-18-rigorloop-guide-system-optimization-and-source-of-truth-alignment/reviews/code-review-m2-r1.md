# Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: commit `89e5dbf`
Reviewed artifact: M2. Cross-guide validation
Review date: 2026-06-18
Recording status: recorded
Status: changes-requested

## Review Inputs

- Diff/review surface: `89e5dbf M2: validate guide system drift`
- Tracked governing branch state: committed M2 implementation plus accepted proposal, approved spec, approved test spec, active plan, and prior review records.
- Governing spec: `specs/guide-system-source-of-truth-alignment.md`
- Test spec: `specs/guide-system-source-of-truth-alignment.test.md`
- Plan: `docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md`
- Validation evidence: M2 validation entries in `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml`; reviewer reran `python scripts/test-guide-system-validator.py`, `python scripts/validate-guide-system.py`, and `python scripts/test-select-validation.py`.

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/reviews/code-review-m2-r1.md`, `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/review-log.md`, `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/review-resolution.md`, `docs/plans/2026-06-18-guide-system-source-of-truth-alignment.md`, `docs/plan.md`, `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/change.yaml`
- Open blockers: none
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: `GUIDE-CR1`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/reviews/code-review-m2-r1.md`
- Review log: `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/review-log.md`
- Review resolution: `docs/changes/2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment/review-resolution.md`
- Reviewed milestone: M2. Cross-guide validation
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2 resolution-needed, M3
- Required review-resolution: yes
- Finding IDs: `GUIDE-CR1`
- Verify readiness: not-claimed

## Diff Summary

M2 adds `scripts/validate-guide-system.py`, adds fixture-backed guide-system validator tests, registers `guide_system.regression` and `guide_system.validate` in selected validation, routes guide surfaces through the new checks, and synchronizes plan and change metadata to request M2 review.

## Findings

### GUIDE-CR1

Finding ID: GUIDE-CR1
Severity: major
Location: `scripts/validate-guide-system.py:114`
Evidence: `specs/guide-system-source-of-truth-alignment.md` R42 requires guide-system validation to preserve the workflow-map validator's canonical-registry/table consistency checks rather than duplicating them as a second contract. `specs/guide-system-source-of-truth-alignment.test.md` GST-008 requires workflow-map registry/table consistency to remain owned by the workflow-map validator or a composed validator call. The implementation adds separate `GUIDE-008` registry checks in `scripts/validate-guide-system.py:114-128`, but the existing workflow-map validator at `scripts/skill_validation.py:988-1058` already parses the same registry and validates required entries, required fields, placement representations, plan/review paths, and Markdown table projection consistency. The new guide validator does not call that owner and instead creates a partial second registry contract.
Required outcome: Guide-system validation must not own an incomplete duplicate workflow-map registry contract. It must either compose/call the existing workflow-map validator for registry/table consistency or limit its own checks to guide-system ownership boundaries while ensuring the workflow-map validator remains selected where registry/table consistency is required.
Safe resolution path: Refactor `GUIDE-008` so it delegates registry/table consistency to `skill_validation.validate_workflow_artifact_map_contract` or removes partial registry-entry validation and adds selector/test coverage that runs the workflow-map validator when `docs/workflows.md` registry/table consistency is in scope. Add a regression proving a registry/table mismatch is caught by the owning workflow-map validator, then rerun guide-system, selector, skill-validator/workflow-map, lifecycle, metadata, and selected CI checks for M2.
needs-decision rationale: none

## Checklist Coverage

| Check | Verdict | Evidence |
| --- | --- | --- |
| Spec alignment | block | `GUIDE-CR1`: R42 requires preserving the workflow-map validator boundary, but M2 adds partial registry checks in the guide validator instead of composing or selecting the owner. |
| Test coverage | concern | `scripts/test-guide-system-validator.py` covers the new partial `GUIDE-008` duplicate-registry check, but no M2 regression proves guide-system validation composes or selects the existing workflow-map registry/table validator for mismatches. |
| Edge cases | concern | Broken guide links, missing workflow guide ownership, project-map scope, plan-index bloat, learn-session live authority, and stage-skill plan path contradictions have direct tests; registry/table mismatch ownership remains the blocking gap. |
| Error handling | pass | The new validator reports stable `GUIDE-*` IDs and exits nonzero on failures. |
| Architecture boundaries | concern | The dedicated validator boundary is allowed by R32, but `GUIDE-CR1` crosses into workflow-map registry ownership. |
| Compatibility | pass | No lifecycle stage order, artifact schema, generated adapter output, or historical migration changed in the M2 diff. |
| Security/privacy | pass | The diff is local validation and documentation state only; it adds no network calls, credentials, secret handling, or private runtime logging. |
| Derived artifact currency | pass | No canonical skill files or generated public adapter outputs changed in M2. |
| Unrelated changes | pass | The diff is scoped to guide validation, selector routing, small guide wording needed for deterministic validation, and lifecycle handoff artifacts. |
| Validation evidence | concern | Recorded and reviewer-run validation commands are relevant and passing, but they do not prove the R42 ownership boundary because the new guide validator is checking registry details itself. |

## No-Finding Rationale

Not applicable. Material finding `GUIDE-CR1` requires resolution before M2 can close.

## Residual Risks

After `GUIDE-CR1` is fixed, re-review should confirm that guide-system validation still checks guide ownership concerns while workflow-map registry/table consistency remains owned by the existing workflow-map validator.

## Handoff

- Reviewed milestone: M2. Cross-guide validation
- Review status: changes-requested
- Milestone closeout: resolution-needed
- Required review-resolution: yes
- Remaining implementation milestones: M2 resolution-needed, M3
- Next stage: review-resolution
- Verify readiness: not-claimed
