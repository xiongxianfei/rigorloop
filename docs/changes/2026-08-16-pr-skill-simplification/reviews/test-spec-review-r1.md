# Test-Spec Review R1: PR Skill Simplification

Review ID: test-spec-review-r1
Stage: test-spec-review
Round: r1
Reviewer: Codex independent test-spec-review context reset to proof map and governing artifacts
Target: `specs/pr-skill-simplification.test.md`
Reviewed artifact: commit `f15da7e7`, sha256 `523f3cda6d236e1d2e9a0a708f97e73919d7679186e740dece42122c7db772d4`
Review date: 2026-08-16
Status: changes-requested
Review status: changes-requested
Material findings: TSPRSIM-TSR1
Recording status: recorded
Immediate next stage: test-spec revision
Implementation handoff: not-allowed

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: TSPRSIM-TSR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-16-pr-skill-simplification/reviews/test-spec-review-r1.md`
- Review log: `docs/changes/2026-08-16-pr-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-16-pr-skill-simplification/review-resolution.md`
- Open blockers: M1 preservation proof lacks one exact executable command in the command ledger
- Immediate next stage: test-spec revision
- Implementation handoff: not-allowed
- Stop condition: bounded proof-map correction and independent rereview required

## Findings

## Finding TSPRSIM-TSR1

Finding ID: TSPRSIM-TSR1
Severity: major
Location: `specs/pr-skill-simplification.test.md`, Validation commands, M1 milestone row, and T-PR-018
Evidence: M1 requires a “standard-library ledger and fixture command,” but the validation-command ledger defines no command ID or exact command for it. The milestone row and T-PR-018 therefore depend on prose rather than an executable, owned validation contract.
Required outcome: Add one exact planned-for-implementation command for M1 ledger, fixture, unknown-value, and baseline validation and reference its command ID from T-PR-018 and the M1 milestone proof row.
Safe resolution path: Add a change-local standard-library validator command with closed failure and zero-test behavior, update the two mappings, rerun boundary validation, and independently rereview the complete proof map.
needs-decision rationale: none

## Review assessment

The proof map otherwise traces all 49 requirements, eight examples, ten edge cases, eight boundaries, and eight interactions to deterministic cases and repository-owned commands. It correctly excludes live PR and target-agent execution, models external state locally, distinguishes producer/consumer verification evidence, and places package proof in M3. The missing M1 command is bounded and does not require upstream behavior or plan changes.

## Claim limitations

This result does not authorize implementation or claim that any command has run, any package has been built, verification passed, the branch is ready, or a PR is ready.
