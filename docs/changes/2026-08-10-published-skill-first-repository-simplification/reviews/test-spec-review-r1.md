# Published-Skill-First Repository Simplification Test-Spec Review R1

Review ID: test-spec-review-r1
Stage: test-spec-review
Round: 1
Reviewer: Codex independent test-spec-review context
Target: `specs/published-skill-first-repository-simplification.test.md`
Reviewed artifact: `specs/published-skill-first-repository-simplification.test.md`
Review date: 2026-08-10
Status: changes-requested
Review status: changes-requested
Recording status: recorded
Material findings: PSR-TSR1-001, PSR-TSR1-002
Immediate next stage: review-resolution
Implementation handoff: not-allowed
Automatic downstream handoff: none; bounded workflow target reached

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: PSR-TSR1-001, PSR-TSR1-002
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-10-published-skill-first-repository-simplification/reviews/test-spec-review-r1.md`
- Review log: `docs/changes/2026-08-10-published-skill-first-repository-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-10-published-skill-first-repository-simplification/review-resolution.md#test-spec-review-r1`
- Open blockers: PSR-TSR1-001, PSR-TSR1-002
- Immediate next stage: review-resolution
- Implementation handoff: not-allowed
- Stop condition: bounded automation target reached with two material proof-map findings

## Review inputs

- Corrected approved feature spec and `spec-review-r2`.
- Approved canonical architecture, accepted ADR, and `architecture-review-r2`.
- Approved execution plan and `plan-review-r1`.
- Active test-spec candidate and authoring evidence.
- Existing skill, adapter, release, lifecycle, review, selector, and package test surfaces for command feasibility.
- `boundary-first-v1` compact core and proof guidance.

## Findings

## Finding PSR-TSR1-001

Finding ID: PSR-TSR1-001
Severity: major
Location: `specs/published-skill-first-repository-simplification.test.md`, Input artifact identities
Evidence: The feature-spec identity row cites `spec-review-r1`, but the owning change record identifies `spec-review-r2` as the current approving review after the boundary-record correction. Implementation and first-milestone code review are required to rely on current input identities; the recorded identity is stale.
Required outcome: The test spec must identify `spec-review-r2` and its review record as the current feature-spec approval before implementation handoff.
Safe resolution path: Revise only the feature-spec input-identity row and authoring evidence to cite `spec-review-r2`, confirm the reviewed requirement and proof IDs remain unchanged, then rerun `test-spec-review`.
needs-decision rationale: none

## Finding PSR-TSR1-002

Finding ID: PSR-TSR1-002
Severity: major
Location: `specs/published-skill-first-repository-simplification.test.md`, T3 and Manual QA checklist MP1
Evidence: MP1 has a stable ID and checklist, while T3 supplies a fixture, expected result, failure claim, and evidence path. The manual-proof contract nevertheless does not explicitly name its automation rationale, required environment, owning stage and role, auditable pass condition, or auditable failure condition in one procedure. The review contract requires those fields so implementation does not infer how semantic review evidence closes M2.
Required outcome: MP1 must become an explicit, auditable manual proof procedure with automation rationale, owner role, owning stage, required environment, exact steps, evidence artifact, pass condition, failure condition, and rerun condition.
Safe resolution path: Add a structured manual-proof case for MP1, link T3 and the M2 milestone row to it, preserve semantic review as judgment rather than a validator, then rerun `test-spec-review`.
needs-decision rationale: none

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Governing-contract alignment | concern | Behavior aligns, but the feature-spec review identity is stale after R2. |
| Requirement coverage | pass | R1-R29 all map to stable automated or manual proof. |
| Example coverage | pass | E1-E8 map to stable test cases. |
| Negative and boundary coverage | pass | Valid, invalid, missing, extra, stale, unknown, conflicting, partial, rollback, compatibility, and external exclusions are represented. |
| Proof-level adequacy | concern | Automated levels are proportionate; MP1 lacks a complete manual procedure contract. |
| Milestone mapping | pass | M1-M6 each have tests, commands, evidence, review timing, and recovery intent. |
| Command validity | pass | Existing commands resolve or planned commands name owner, milestone, failure, zero-test, and safety behavior. Placeholder operands are explicitly non-literal fixture bindings. |
| Fixture and data design | pass | Fixtures are local, temporary, isolated, representative, and non-publishing. |
| Manual-proof boundary | block | MP1 is justified but not fully explicit, owned, and auditable. |
| Observability | pass | Gate and retirement failures name owner, artifact, invariant, result, and repair. |
| Determinism and isolation | pass | Network, publication, credentials, target runtimes, prompts, and model evidence are excluded. |
| Scope and non-goals | pass | The proof map does not reintroduce target-runtime certification or a new validation subsystem. |
| Execution economics | pass | Focused milestone checks remain separate from final CI and local release proof. |
| Traceability | block | The current feature-spec approval record is not linked. |
| Implementation handoff | block | Implementation would have to infer the current input approval and MP1 closeout contract. |

## Handoff

No implementation handoff is allowed.
Both findings have safe proof-map corrections and require review-resolution, test-spec revision, and a new formal test-spec review before implementation may begin.
