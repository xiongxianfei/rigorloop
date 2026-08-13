# Plan Skill Simplification Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: r1
Reviewer: Codex independent code-review context
Target: implementation commit `5c60984b`
Reviewed artifact: commit `5c60984b`
Reviewed milestone: M2
Review date: 2026-08-13
Status: changes-requested
Review status: changes-requested
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: review record, invocation manifest, review log, review resolution, and lifecycle state
- Open blockers: PLSIM-CR1, PLSIM-CR2
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: PLSIM-CR1, PLSIM-CR2
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-12-plan-skill-simplification/reviews/code-review-m2-r1.md`
- Review log: `docs/changes/2026-08-12-plan-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-12-plan-skill-simplification/review-resolution.md#code-review-m2-r1`
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3
- Required review-resolution: yes
- Finding IDs: PLSIM-CR1, PLSIM-CR2
- Verify readiness: not-claimed

## Review boundary

The review inspected `702e5940..5c60984b`, the approved skill and lifecycle requirements, M2 plan and test-spec obligations, the complete canonical plan package, ledgers, fixtures, focused tests, and recorded size evidence. Package ownership and measured profile reduction are sound, but deterministic identity wording and invalid-fixture proof are incomplete.

## Finding PLSIM-CR1

Finding ID: PLSIM-CR1
Severity: major
Location: `skills/plan/references/governed-plan-authoring.md`, create and initialize operations
Evidence: PSIM-R011 and PSIM-R012 define stable artifact identity as artifact ID, kind, role, and normalized path and reviewed revision identity as review ID, round, record path, reviewed artifact path, and repository revision. The reference compresses these to “one stable plan tuple” and “review identity and revision,” which does not tell a governed invocation which fields are mandatory.
Required outcome: Restore the exact stable-artifact and reviewed-revision fields in the governed procedure while keeping both `PL0` and `PL1` below baseline.
Safe resolution path: Name both approved tuples explicitly, rerun the profile measurements and complete M2 validator set, and update M2 evidence.
needs-decision rationale: none

## Finding PLSIM-CR2

Finding ID: PLSIM-CR2
Severity: major
Location: `scripts/test-skill-validator.py`, `PlanSkillSimplificationContractTests.test_plan_simplification_inventories_and_scenarios_fail_closed`
Evidence: T7 requires unknown disposition, unknown classification, duplicate ID, missing field, and inconsistent destination fixtures to pass through a deterministic change-local validation path with closed vocabulary checked first. The implementation supplies only two unknown-value fixtures and merely asserts that their values are absent from local sets; it does not exercise duplicate, missing-field, destination consistency, or validation ordering.
Required outcome: Add a deterministic change-local ledger validation helper and fixtures proving unknown values fail before consistency, while duplicate IDs, missing fields, and inconsistent destinations also fail.
Safe resolution path: Keep the helper inside the existing test suite rather than adding a validator family, add the missing fixtures, and rerun CMD7.
needs-decision rationale: none

## Handoff

M2 remains open. Resolve both accepted findings, record validation evidence, and rerun code-review at a strictly later round.
