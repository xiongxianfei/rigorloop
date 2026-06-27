# Test Spec Review R1: Validation Runtime Follow-Through

Review ID: test-spec-review-r1
Stage: test-spec-review
Round: 1
Reviewer: Codex test-spec-review skill
Target: specs/validation-runtime-follow-through.test.md
Reviewed artifact: specs/validation-runtime-follow-through.test.md
Review date: 2026-06-26
Recording status: recorded
Status: changes-requested
Material findings: TSR1-F1
Review status: changes-requested
Immediate next stage: review-resolution
Implementation handoff: not-allowed

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: TSR1-F1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/test-spec-review-r1.md
- Review log: docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/review-log.md
- Review resolution: docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/review-resolution.md#test-spec-review-r1
- Open blockers: TSR1-F1
- Immediate next stage: review-resolution
- Implementation handoff: not-allowed
- Stop condition: material proof-map finding requires review-resolution before implementation

## Review Inputs

- Test spec: `specs/validation-runtime-follow-through.test.md`
- Approved feature spec: `specs/validation-runtime-follow-through.md`
- Spec-review evidence: `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/spec-review-r1.md`
- Approved plan: `docs/plans/2026-06-26-preflight-first-validation-runtime-optimization.md`
- Plan-review evidence: `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/plan-review-r1.md`
- Architecture/ADR: not required for this slice unless scope expands into persistent workers, shared/remote cache, cross-process protocol, or broad validator composition.
- Review skill rule: `.agents/skills/test-spec-review/SKILL.md`

## Findings

## Finding TSR1-F1

Finding ID: TSR1-F1
Severity: major
Location: `specs/validation-runtime-follow-through.test.md:103`, `specs/validation-runtime-follow-through.test.md:252`
Evidence: Test case `T3` is marked `Level: manual` and asks the implementer to profile `selector.regression`, record dominant contributors or limitations, and record a timeout or follow-up decision. The manual QA checklist also asks reviewers to confirm the selector profile exists. The test-spec-review contract requires manual proof to name a stable ID, automation rationale, exact steps, required environment, evidence artifact, pass condition, failure condition, and owning stage. The current manual proof names a test ID and evidence artifact, but it does not define the required environment, automation rationale, exact profiling steps, pass/fail criteria for profile adequacy, or owning stage.
Required outcome: Manual proof for selector-regression profiling must be made auditable before implementation handoff, or converted to an automated/fixture-backed proof.
Safe resolution path: Revise `specs/validation-runtime-follow-through.test.md` to add a structured manual proof case for selector-regression profiling, or expand `T3` with the missing fields: stable manual proof ID, automation rationale, exact profiling steps, required environment, evidence artifact, pass condition, failure condition, owner role, and owning stage. Link that proof from R6/R11 coverage and the manual QA checklist, then rerun `test-spec-review`.
needs-decision rationale: none

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Governing-contract alignment | pass | The test spec operationalizes the approved follow-through spec and active plan without changing product direction or scope. |
| Requirement coverage | pass | Requirements R1-R25 are mapped to test IDs or manual/contract proof. |
| Example coverage | pass | Examples E1-E5 map to stable test IDs. |
| Negative and boundary coverage | pass | The proof map covers missing routes, diagnostic broad-smoke after blockers, unsafe selector optimization, low-confidence broad-smoke classification, cache-status misuse, and composition sprawl. |
| Proof-level adequacy | concern | Most behavior is assigned to integration or contract proof, but the selector-regression profile proof remains manual without enough procedure detail. |
| Milestone mapping | pass | M1-M3 map to the appropriate test IDs and match the approved plan sequence. |
| Command validity | pass | Referenced repository scripts exist; planned evidence artifacts are owned by the active plan milestones. |
| Fixture and data design | pass | The fixture strategy uses temporary repositories, fixture workspaces, and existing selector/CI test surfaces without network-dependent tests. |
| Manual-proof boundary | block | Manual selector-profile proof is not exact, owned, evidenced, and bounded enough for implementation handoff. |
| Observability | pass | Evidence artifacts and diagnostics are named for baseline, selector profile, selector preservation, missing-route blockers, and broad-smoke classification. |
| Determinism and isolation | pass | The test spec avoids network-dependent tests and scopes broad-smoke expensive behavior to stubs or evidence artifacts where appropriate. |
| Scope and non-goals | pass | The proof map avoids broad-smoke parallelism, cache reuse, broad validator composition, and fixed runtime targets. |
| Execution economics | pass | Focused selected checks, broad-smoke boundary cost, and final verify evidence are kept distinct. |
| Traceability | pass | Requirements, examples, edge cases, milestones, and test IDs are consistently linked. |
| Implementation handoff | block | Implementation would have to infer the required selector-profile manual proof procedure. |

## Exact Proof-Map Gap

- `T3` needs a structured manual proof case or equivalent expanded fields for selector-regression profiling: automation rationale, exact steps, required environment, evidence artifact, pass condition, failure condition, owner role, and owning stage.

## Handoff

No automatic downstream handoff is performed. `TSR1-F1` must be dispositioned in review-resolution and the test spec must be revised or otherwise resolved before implementation can rely on this proof map.
