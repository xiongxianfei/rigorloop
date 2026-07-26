# Boundary-First Proof Modeling Test-Spec Review R1

Review ID: test-spec-review-r1
Stage: test-spec-review
Round: 1
Reviewer: Codex test-spec-review skill
Target: specs/rigorloop-workflow.test.md
Status: changes-requested
Review status: changes-requested
Material findings: BFP-TSR1, BFP-TSR2
Immediate next stage: test-spec revision
Implementation handoff: not-allowed
Stop condition: test-spec review findings remain open

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: `BFP-TSR1`, `BFP-TSR2`
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/test-spec-review-r1.md
- Review log: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-log.md
- Review resolution: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-resolution.md
- Open blockers: premature report-command gate and incomplete manual-proof contracts
- Immediate next stage: test-spec revision
- Implementation handoff: not-allowed
- Stop condition: test-spec review findings remain open

## Reviewed proof surfaces

- `specs/rigorloop-workflow.test.md` R28-R28z proof map
- `specs/skill-contract.test.md` R56-R56q proof map
- `docs/plans/2026-07-25-boundary-first-proof-modeling.md`
- approved specs, architecture, ADR, spec-review R2, and plan-review R2

## Finding BFP-TSR1

Finding ID: BFP-TSR1
Severity: major
Location: `specs/rigorloop-workflow.test.md`, CMD-BFP-2 and M1 milestone proof row
Evidence: CMD-BFP-2 invokes `validate-boundary-proof.py` against the canonical `boundary-capability-baseline.md`, while the plan and test spec intentionally defer creation of that report until M4. The command is nevertheless marked first-required in M1 and listed as an M1 closeout gate. A correct M1 implementation would therefore fail because the required artifact must not exist yet.
Required outcome: M1 MUST prove report parsing and aggregation through synthetic fixtures without requiring the canonical M4 report path; canonical report validation MUST first become mandatory in M4.
Safe resolution path: Change CMD-BFP-2 ownership and first-required milestone to M4, remove it from M1, and keep T46's M1 coverage on CMD-BFP-1 synthetic report fixtures. Retain CMD-BFP-2 for M4 canonical serialization and validation.
needs-decision rationale: none

## Finding BFP-TSR2

Finding ID: BFP-TSR2
Severity: major
Location: both test specs, Boundary-first proof map and Manual QA checklist
Evidence: Hybrid proof rows reference seven stable manual procedure IDs, but each procedure is only a one-sentence instruction. The governing test-spec-review contract requires an automation rationale, exact steps, required environment, evidence artifact, pass condition, failure condition, and owning stage for every manual proof.
Required outcome: Every referenced manual procedure ID MUST resolve to a complete, bounded, executable manual-proof contract.
Safe resolution path: Add one structured manual-procedure table or blocks to each test spec containing all required fields. Keep judgment limited to semantic authority, composed paths, evidence adequacy, stage behavior, and capability preservation; do not convert those judgments into natural-language scoring.
needs-decision rationale: none

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Governing-contract alignment | pass | The proof maps operationalize the approved specs without changing behavior. |
| Requirement coverage | pass | R28-R28z and R56-R56q are completely mapped. |
| Example coverage | pass | The scoped amendments use normative boundary and interaction records; retained examples outside scope remain grandfathered. |
| Negative and boundary coverage | pass | Unknown, stale, partial, interruption, composition, migration, outcome, and overclaim cases are explicit. |
| Proof-level adequacy | concern | Automated levels are appropriate; manual procedures are under-specified. |
| Milestone mapping | block | M1 requires an artifact intentionally created only in M4. |
| Command validity | concern | Command ownership is named, but CMD-BFP-2 is required at the wrong gate. |
| Fixture and data design | pass | Eight frozen incidents, negative records, and a compact simple fixture are deterministic and repository-local. |
| Manual-proof boundary | block | Manual IDs do not yet define evidence and pass/fail contracts. |
| Observability | pass | Stable requirement, boundary, fixture, test, and command IDs identify failures. |
| Determinism and isolation | pass | Tests avoid network, time, randomness, and shared external state. |
| Scope and non-goals | pass | Exactly eight skills are covered; no lifecycle stage or release action is added. |
| Execution economics | pass | Focused checks precede adapter and release-unit proof. |
| Traceability | pass | Requirement, boundary, interaction, test, fixture, command, and milestone links are explicit. |
| Implementation handoff | block | The two local proof-contract defects must be corrected and rereviewed. |
