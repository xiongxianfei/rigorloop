# Boundary-First Proof Modeling Plan Review R3

Review ID: plan-review-r3
Stage: plan-review
Round: 3
Reviewer: Codex plan-review skill with context-separated reviewer
Target: commit `296cffa5` against `1c620605`
Reviewed artifact: docs/plans/2026-07-25-boundary-first-proof-modeling.md
Status: changes-requested
Review status: changes-requested
Material findings: BFP-PL4, BFP-PL5
Immediate next stage: plan revision
Implementation readiness: not-ready
Test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Initial packet inventory: exact plan diff; approved R13 specs; accepted R4 architecture/ADR; M1 code-review findings; current test specs
Manifest owner: workflow orchestrator

## Result

- Skill: plan-review
- Review status: changes-requested
- Material findings: BFP-PL4, BFP-PL5
- Recording status: recorded
- Recording blocker: none
- Immediate next stage: plan revision
- Implementation readiness: not-ready
- Test-spec readiness: not-ready

## Findings

### BFP-PL4 - Five milestones conflict with the approved R28y phase contract

Finding ID: BFP-PL4
Severity: major

Evidence:

- R28y assigns synthetic proof to M1, fresh upstream behavior to M2,
  downstream preservation to M3, and current aggregation to M4.
- The plan shifted those responsibilities to M1 through M5 and materially
  expanded reviewed M1 scope.

Required outcome:

Preserve reviewed M1 and the approved M1-M4 ownership while keeping runtime
feasibility as a stop before full harness or published-skill mutation.

Safe resolution:

Keep M1 as deterministic finding closure.
Make runtime feasibility a pre-harness M2 promotion gate, implement controlled
harness support within M2, and retain M2 upstream behavior, M3 preservation,
and M4 aggregation.

### BFP-PL5 - Evidence creation and promotion commands are incomplete

Finding ID: BFP-PL5
Severity: major

Evidence:

- The controlled harness pipeline has no exact production command.
- The preservation baseline is not captured before the first participating
  skill mutation.
- Preservation and final report sections do not name exact output paths or
  generation-versus-validation commands.
- Generic M5 file categories are not self-contained boundaries.

Required outcome:

Name exact inputs, outputs, production command, validation-only command,
promotion evidence, and failure stop for every milestone.
Capture the preservation baseline before first skill mutation and keep report
generation separate from report validation.

Safe resolution:

Add controlled fixture generation/validation commands; make baseline creation
the first M2 pre-mutation step; enumerate preservation paths and commands;
name production report generation followed by validation; and require clean
code review before every milestone promotion.

## Prior-Finding Reconciliation

| Finding | Result | Evidence |
| --- | --- | --- |
| BFP-PL1 | resolved | Live-state ownership and plan/index synchronization remain correct. |
| BFP-PL2 | resolved for prior scope | Prior command gaps remain closed; R13 evidence commands require the new correction. |
| BFP-PL3 | resolved | R28y report completion remains distinct from later R28o closeout. |
