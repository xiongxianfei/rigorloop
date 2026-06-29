# Test Spec Review R1

Review ID: test-spec-review-r1
Stage: test-spec-review
Round: 1
Reviewer: Codex test-spec-review skill
Target: specs/release-transaction-automation.test.md
Reviewed artifact: specs/release-transaction-automation.test.md
Review date: 2026-06-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Material findings: RTA-TSR1, RTA-TSR2
Immediate next stage: test-spec revision
Implementation handoff: not-allowed
Automatic downstream handoff: none

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: RTA-TSR1, RTA-TSR2
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-29-release-transaction-automation/reviews/test-spec-review-r1.md
- Review log: docs/changes/2026-06-29-release-transaction-automation/review-log.md
- Review resolution: docs/changes/2026-06-29-release-transaction-automation/review-resolution.md#test-spec-review-r1
- Open blockers: RTA-TSR1, RTA-TSR2
- Immediate next stage: test-spec revision
- Implementation handoff: not-allowed
- Stop condition: none

## Review Inputs

- Test spec: specs/release-transaction-automation.test.md
- Approved feature spec: specs/release-transaction-automation.md
- Spec-review evidence: docs/changes/2026-06-29-release-transaction-automation/reviews/spec-review-r1.md
- Approved plan: docs/plans/2026-06-29-release-transaction-automation.md
- Plan-review evidence: docs/changes/2026-06-29-release-transaction-automation/reviews/plan-review-r1.md
- Approved architecture: docs/architecture/system/architecture.md
- ADR: docs/adr/ADR-20260629-release-transaction-profile.md
- Architecture-review evidence: docs/changes/2026-06-29-release-transaction-automation/reviews/architecture-review-r1.md
- Existing command surfaces checked for review-time feasibility: scripts/validate-release.py, scripts/release-verify.sh, scripts/test-adapter-distribution.py, .github/workflows/release.yml

## Findings

### RTA-TSR1

Finding ID: RTA-TSR1
Severity: major
Location: specs/release-transaction-automation.test.md:400; docs/plans/2026-06-29-release-transaction-automation.md:284
Evidence: The active plan says, "Before implementation, test-spec-review must approve the fixture strategy, validation command names, generated-region marker syntax, baseline literal-audit artifact format, and timing file field names." The test spec instead says, "Implementation may choose exact generated-region marker syntax, baseline literal-audit artifact shape, timing field names, and fixture layout within the approved spec and plan boundaries." That defers plan-owned proof decisions past the gate that is supposed to approve them.
Required outcome: The test spec must define, or explicitly constrain with testable compatibility rules, the generated-region marker contract, literal-audit baseline artifact shape, timing evidence field names, and fixture layout enough that M1-M6 implementation can write tests without inventing proof semantics.
Safe resolution path: Revise the test spec to add a concrete proof-contract section for generated regions, literal-audit baseline records, timing evidence schema/field names, and fixture layout. If a detail is intentionally left implementation-selectable, define the closed constraints and the exact tests that will prove any selected implementation satisfies the approved contract, then rerun test-spec-review.
needs-decision rationale: none

### RTA-TSR2

Finding ID: RTA-TSR2
Severity: major
Location: specs/release-transaction-automation.test.md:93-302; docs/plans/2026-06-29-release-transaction-automation.md:103
Evidence: The test spec names many automation locations and command examples, but it does not classify planned validation commands as existing/configured, planned-for-implementation, manual-only, or external/release-owned with milestone ownership. The active plan still names `python scripts/test-release-validation.py`, but review-time command resolution shows that file does not exist; existing adjacent release test/validation surfaces are `scripts/test-adapter-distribution.py`, `scripts/validate-release.py`, and `scripts/release-verify.sh`.
Required outcome: The test spec must provide an implementation-handoff validation command matrix that identifies each command or command family, whether it already exists or is introduced by a milestone, the owning milestone, zero-test or missing-command behavior, safe-mode/dry-run expectations, and the milestone where it becomes required.
Safe resolution path: Revise the test spec to add a command matrix. Replace or classify `python scripts/test-release-validation.py` as a planned command with an owning milestone, or choose an existing command such as `python scripts/test-adapter-distribution.py`/focused new test file with explicit ownership. Include `prepare-release`, `release-preflight`, `close-release-publication`, `validate-release.py`, `release-verify.sh`, lifecycle validators, and CI workflow static checks with clear milestone activation rules, then rerun test-spec-review.
needs-decision rationale: none

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Governing-contract alignment | concern | The proof map mostly follows the approved spec and architecture, but RTA-TSR1 defers plan-required proof-contract details past test-spec-review. |
| Requirement coverage | pass | Requirements `R1` through `R45` map to stable test IDs or manual proof, and no requirement is missing outright. |
| Example coverage | pass | Examples `E1` through `E5` map to stable test IDs covering routine prep, cheap drift, published evidence shape, unavailable public evidence, and special-release handling. |
| Negative and boundary coverage | pass | Edge cases `EC1` through `EC10` are mapped, including invalid profile/package state, unauthorized literals, unreachable remote state, delayed public evidence, invalid archives, multi-root hashes, and override rationale failures. |
| Proof-level adequacy | pass | Unit, integration, e2e, smoke, migration, contract, and manual proof levels are selected according to risk and side-effect boundary. |
| Milestone mapping | concern | Test cases align broadly to M1-M6, but RTA-TSR2 leaves command activation and ownership insufficiently explicit for milestone handoff. |
| Command validity | concern | Existing commands are referenced, but planned commands are not classified and one plan-named command is currently absent without a test-spec owner. |
| Fixture and data design | concern | Fixture categories are representative and network-safe, but RTA-TSR1 leaves fixture layout and schema-sensitive fixture contracts too open for implementation handoff. |
| Manual-proof boundary | pass | Manual proof is bounded to behavior-preservation and reviewability checks, with `RTA-T024` naming the behavior-preservation artifact and pass/fail condition. |
| Observability | pass | Diagnostics are required to name release tag, profile path, literal, file, classification, expected owner, mismatched values, tag conflict, unreachable remote state, and corrective action. |
| Determinism and isolation | pass | Network, npm publication, GitHub release creation, tag pushes, and live public `npx` are excluded from automated tests and replaced by stubs/fixtures. |
| Scope and non-goals | pass | The proof map avoids historical migration, release-gate parallelism, background monitoring, remote caches, hard timing budgets, generated test logic, and real publication. |
| Execution economics | pass | Cheap preflight proof is separated from full release gate and public closeout proof, and expensive/public checks are fixture-backed where appropriate. |
| Traceability | pass | Requirement, example, edge-case, acceptance-criterion, and test IDs are linked consistently enough to identify intended coverage. |
| Implementation handoff | concern | Implementation should not proceed until RTA-TSR1 and RTA-TSR2 are resolved because implementers would otherwise choose proof semantics and validation command ownership themselves. |

## Recommendation

Changes requested. Revise the test spec for RTA-TSR1 and RTA-TSR2, then rerun test-spec-review. No implementation handoff is allowed from this review.
