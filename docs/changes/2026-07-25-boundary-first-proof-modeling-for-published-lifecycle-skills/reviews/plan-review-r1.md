# Boundary-First Proof Modeling Plan Review R1

Review ID: plan-review-r1
Stage: plan-review
Round: 1
Reviewer: Codex plan-review skill
Target: docs/plans/2026-07-25-boundary-first-proof-modeling.md
Status: changes-requested

## Result

- Skill: plan-review
- Review status: changes-requested
- Material findings: `BFP-PL1`, `BFP-PL2`, `BFP-PL3`
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/plan-review-r1.md
- Review log: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-log.md
- Review resolution: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-resolution.md
- Open blockers: invalid live-state shape, non-executable validation placeholders, and ambiguous baseline-versus-resumption closeout
- Immediate next stage: plan revision

## Review invocation manifest

| Field | Value |
| --- | --- |
| Review target | `docs/plans/2026-07-25-boundary-first-proof-modeling.md` |
| Governing proposal | `docs/proposals/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills.md` |
| Governing specs | `specs/rigorloop-workflow.md` R28-R28z; `specs/skill-contract.md` R56-R56q |
| Architecture | `docs/architecture/system/architecture.md`; `docs/adr/ADR-20260725-boundary-first-proof-modeling.md` |
| Review mode | independent workflow-managed plan review |
| Matching test specs | not yet authored; correctly downstream of plan-review |

## Findings

### BFP-PL1 - The plan's live-state contract is invalid

Finding ID: BFP-PL1
Severity: major
Location: `Status`, `Current Handoff Summary`, and `Readiness`
Evidence: Repository lifecycle validation reports a missing required `Change ID` in the Status block. The handoff initially omitted the exact `Latest review evidence` owner marker and structured review-status grammar, and Readiness repeats `plan-review` even though current routing may appear only in `Current Handoff Summary`.
Required outcome: The plan MUST satisfy the structured active-plan contract and keep live next-stage ownership exclusively in `Current Handoff Summary`.
Safe resolution path: Add the exact Change ID to Status; use the closed handoff fields and reason codes; keep Readiness to `See Current Handoff Summary` plus a non-routing statement.

### BFP-PL2 - Validation is not fully executable under the active adapter contract

Finding ID: BFP-PL2
Severity: major
Location: M4 `Validation commands` and plan-wide `Validation plan`
Evidence: The plan uses bare `python scripts/build-adapters.py --check`, which checks the retired tracked-tree default rather than proving generated v0.1.3+ release output. It also leaves `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` as an ellipsis instead of a runnable command.
Required outcome: Milestone and final validation MUST name executable generated-adapter and lifecycle commands with deterministic version and path inputs.
Safe resolution path: Derive the current adapter version from `dist/adapters/manifest.yaml`, generate to a temporary directory, validate that root and version, and replace the lifecycle ellipsis with the exact touched artifact paths. The matching test specs may add narrower commands but may not weaken these gates.

### BFP-PL3 - Report completion and progressive-disclosure resumption are conflated

Finding ID: BFP-PL3
Severity: major
Location: M4 expected result, Dependencies, and Outcome
Evidence: M4 says a passing capability report proves the complete baseline, while R28o separately requires clean implementation and final code reviews, closed review resolution, and final verification before progressive-disclosure proposal review may resume. The report is produced during implementation and therefore cannot itself prove later review and verification gates.
Required outcome: The plan MUST distinguish a passing R28y report from the complete R28o resumption predicate and identify the post-report gates without creating a cyclic report dependency.
Safe resolution path: Keep report generation in M4 from implementation evidence; close M4 only after its milestone review; require a separate final holistic code review, closed resolution, explain-change, and verify before declaring the R28o dependency satisfied. Do not rewrite the report merely to include its own later review.

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Self-contained context | pass | Owners, files, constraints, and rollout surfaces are named. |
| Source alignment | concern | Milestone scope aligns, but R28y and R28o closeout are conflated. |
| Milestone size | pass | The four slices have cohesive implementation and rollback boundaries. |
| Sequencing | concern | Core and skill sequencing is sound; final baseline sequencing needs clarification. |
| Scope discipline | pass | The plan holds the closed eight-skill slice and excludes publication. |
| Validation quality | block | Adapter and lifecycle commands are not executable as written. |
| TDD readiness | pass | Each milestone starts from named negative and positive proof families. |
| Risk coverage | pass | Normative ownership, semantic review, copied resources, scope, and activation are covered. |
| Architecture alignment | pass | Physical ownership and one-writer report flow match the accepted ADR. |
| Operational readiness | block | Invalid plan state and incomplete commands prevent reliable handoff. |
| Plan maintainability | concern | The structure is strong after live-state fields are normalized. |

## Readiness

The implementation sequence is viable and no upstream proposal, spec, or
architecture revision is required.
Revise the plan for `BFP-PL1` through `BFP-PL3`, validate it, and rerun
plan-review before test-spec authoring.
