# Workflow Skill Simplification Test-Spec Review R1

Review ID: test-spec-review-r1
Stage: test-spec-review
Round: r1
Reviewer: Codex independent test-spec-review context
Target: `specs/workflow-skill-simplification.test.md`
Reviewed artifact: complete R1 proof-map revision
Review date: 2026-08-11
Status: changes-requested
Material findings: WFSIM-TR1, WFSIM-TR2
Review status: changes-requested
Immediate next stage: test-spec revision
Implementation handoff: not-allowed
Recording status: recorded

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: WFSIM-TR1, WFSIM-TR2
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-11-workflow-skill-simplification/reviews/test-spec-review-r1.md`
- Review log: `docs/changes/2026-08-11-workflow-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-11-workflow-skill-simplification/review-resolution.md#test-spec-review-r1`
- Open blockers: WFSIM-TR1, WFSIM-TR2
- Immediate next stage: test-spec revision
- Implementation handoff: not-allowed
- Stop condition: implementation waits for corrected executable proof and bounded manual procedures

## Findings

## Finding WFSIM-TR1

Finding ID: WFSIM-TR1
Severity: material
Location: `specs/workflow-skill-simplification.test.md`, Validation commands, CMD1
Evidence: CMD1 is the literal placeholder `python -c '<change-local ledger and scenario contract proof recorded verbatim in M1 evidence>'`. M1 and PRF-001, PRF-002, PRF-003, PRF-005, PRF-006, PRF-009 through PRF-011, PRF-013, and PRF-015 rely on it. A placeholder cannot establish required fields, closed-vocabulary rejection, unique IDs, exact scenario identity, or zero-proof behavior.
Required outcome: Replace CMD1 with one executable deterministic standard-library command that validates both ledgers, the full required scenario identity set, required/forbidden outcomes, uniqueness, and explicit unknown-value rejection.
Safe resolution path: Adapt the repository's existing implement-simplification ledger command to workflow's closed dispositions, literal classes, required fields, and scenario names. Keep it change-local and model-free; do not create a permanent validator.
needs-decision rationale: none

## Finding WFSIM-TR2

Finding ID: WFSIM-TR2
Severity: material
Location: `specs/workflow-skill-simplification.test.md`, Manual QA checklist, MP1 and MP2
Evidence: Both procedures name inputs, steps, evidence, and a pass statement, but neither states why automation is insufficient, the required environment, the owning stage, or an explicit failure condition. Those fields are mandatory for manual proof relied on by hybrid PRF rows and M1/M3 closeout.
Required outcome: Give MP1 and MP2 an automation rationale, required environment, owner/owning stage, exact failure condition, and retain their evidence and pass conditions.
Safe resolution path: Add bounded fields to each existing procedure without expanding manual proof scope or replacing deterministic commands.
needs-decision rationale: none

All requirements, examples, boundaries, interactions, negative outcomes, milestone mappings, and package proof surfaces are otherwise represented. Structural boundary validation passes, but structural validity cannot substitute for executable or bounded proof.
