# Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: r1
Reviewer: Codex code-review skill
Target: M2. Implement the inactive v2 lifecycle and plan-centered package
Reviewed artifact: commit `e4b5ba8b` (`M2: add inactive plan-centered lifecycle`)
Review date: 2026-08-31
Status: changes-requested
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-08-31-retire-standalone-test-spec-stage/reviews/code-review-m2-r1.md`, `docs/changes/2026-08-31-retire-standalone-test-spec-stage/review-log.md`, and `docs/changes/2026-08-31-retire-standalone-test-spec-stage/review-resolution.md`
- Open blockers: `RTS-M2-CR1`, `RTS-M2-CR2`
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: `RTS-M2-CR1`, `RTS-M2-CR2`
- Recording status: recorded
- Recording blocker: none; the durable review surfaces record the non-clean result while M2 remains review-requested
- Review record: `docs/changes/2026-08-31-retire-standalone-test-spec-stage/reviews/code-review-m2-r1.md`
- Review log: `docs/changes/2026-08-31-retire-standalone-test-spec-stage/review-log.md`
- Review resolution: `docs/changes/2026-08-31-retire-standalone-test-spec-stage/review-resolution.md`
- Reviewed milestone: M2. Implement the inactive v2 lifecycle and plan-centered package
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4, M5
- Required review-resolution: yes
- Finding IDs: `RTS-M2-CR1`, `RTS-M2-CR2`
- Verify readiness: not-claimed

## Scope

Reviewed the exact M2 implementation commit against the approved Design and Delivery packages, M2 allocation, matching legacy-path test specification, implementation evidence, and direct contract-path probes. This first-pass review records findings without modifying the reviewed implementation or advancing lifecycle routing.

## Review inputs

- Diff/review surface: commit `e4b5ba8be7e1c77f174fbeee6c781b9800d249e0`
- Tracked governing branch state and review-requested handoff: commit `24f055b8207fed898c28b1c4493727552b494a39`
- Approved Design package: `design-review-r2`
- Approved Delivery package: `delivery-review-r3`
- Primary architecture: `docs/architecture/2026-08-31-retire-standalone-test-spec-stage.md`
- Specification: `specs/retire-standalone-test-spec-stage.md`
- Plan: `docs/plans/2026-08-31-retire-standalone-test-spec-stage.md`, approved identity `sha256:727b5a71f1d5ce001876cde59f195536c9671b4743e50a70ef95cf437ccc9938`
- Legacy-path test specification: `specs/retire-standalone-test-spec-stage.test.md`
- Implementation evidence: `docs/changes/2026-08-31-retire-standalone-test-spec-stage/evidence/m2-dual-lifecycle.md`
- Relevant requirements and acceptance criteria: `RTS-R1`, `RTS-R2`, `RTS-R13` through `RTS-R16`, `RTS-R18`, `RTS-R19`, `RTS-R21` through `RTS-R24`, `RTS-AC1`, `RTS-AC4`, `RTS-AC7`, `RTS-AC8`, `RTS-AC11`
- Relevant boundaries and interactions: `BND-INPUT-001`, `BND-STATE-001`, `BND-AUTH-001`, `BND-COMPOSE-001`, `BND-TEMPORAL-001`, `BND-RECOVERY-001`, `BND-COMPAT-001`, `INT-001`, `INT-002`, `INT-004`, `INT-005`
- Recorded implementation validation: CMD-01 passed 189 Node tests; CMD-02 passed 310 Node tests with 2 pre-existing skips; CMD-03 passed 77 Python tests; CMD-04 passed 166 Python tests; CMD-05 passed 77 workflow-automation, 18 policy, and 69 state tests; CMD-06 passed 109 Python tests

## Actual-diff summary

- Added contract-keyed Node lifecycle graphs, artifact kinds, package composition, correction routing, context projection, and mutation behavior for inactive v2 while retaining v1.
- Added Python metadata, artifact-lifecycle, review-artifact, workflow-policy, workflow-state, and schema handling for v2.
- Added focused tests for direct Node `plan -> delivery-review`, plan-only package membership, retired test-spec rejection, plan correction routing, v1 compatibility, and selected Python v2 projections.
- Left central Python transition evaluation and public/coordinated authoring entrypoints on their v1 defaults, and made the review-artifact validator assume the primary plan artifact ID is literally `plan`.

## Material findings

## Finding RTS-M2-CR1

Finding ID: RTS-M2-CR1
Severity: major
Location: `scripts/workflow_automation_policy.py:1003`; `scripts/workflow_automation.py:1925`; `scripts/workflow_automation.py:2165`; `scripts/workflow_automation.py:2708`; `scripts/workflow_automation.py:2841`; `scripts/validate_workflow_automation.py:1110`
Evidence: M2 creates `V2_TRANSITION_RULES`, and the narrow `evaluate_non_public_authoring_route(..., lifecycle_contract=v2)` helper returns `delivery-review` after `plan`. The central `evaluate_transition`, however, still reads only the v1 `TRANSITION_RULES_BY_OPERATION` map and accepts no contract discriminator. A direct probe confirmed that a v2 `plan -> delivery-review` rule exists while `evaluate_transition` rejects that exact transition with `transition: no rule permits operation toward target`. The coordinated authoring path calls the narrow helper without forwarding a contract, the public command/route/target-resolution entrypoints normalize with the v1 default, and the automation validator calls `can_operation_fit_target` and `evaluate_transition` without contract context. The green tests exercise the isolated helper and registry projection, not a complete contract-selected automation transaction. This contradicts M2's required executable v2 route and the completion criterion that runtime and repository-owned paths pass the closed graph matrix.
Required outcome: make contract selection flow through the central transition evaluator, automation validation, target binding/resolution, public and non-public coordination, and post-completion routing so an explicit v2 record can traverse `plan -> delivery-review` while v1 remains unchanged and unknown contracts fail before transition consistency checks.
Safe resolution path: add a contract parameter or contract-bearing transition context at the central evaluator boundary; derive and forward the owning change's classified contract through coordinator, public target, and validator calls; add transaction-level v2 tests that exercise binding, capability/receipt validation, completion, and post-completion routing rather than only the helper; rerun CMD-05 and the relevant metadata/contract checks.
needs-decision rationale: none; this is a bounded completion of the already-approved M2 contract-keyed automation path.

## Finding RTS-M2-CR2

Finding ID: RTS-M2-CR2
Severity: major
Location: `scripts/review_artifact_validation.py:930`
Evidence: the v2 review-artifact rule compares parsed member IDs to the literal list `["plan"]`. Artifact IDs are stable identities, not artifact kinds; the Node package engine, metadata semantics, and workflow-state verifier correctly derive the exact primary plan's actual artifact ID. A direct validator fixture with one valid v2 primary plan member named `primary-plan=docs/plans/example.md` was rejected solely with `v2 Delivery Review package members must contain exactly plan`. This creates cross-validator disagreement and blocks a valid exact-primary-plan Delivery Review record under `RTS-R13` and `RTS-R18`. The new regression hardcodes `plan`, so it does not cover identity-independent primary-plan membership.
Required outcome: validate the v2 review record against the owning change's exact single primary-plan artifact ID and path, rejecting missing, extra, wrong-kind, wrong-role, and test-spec members without requiring the ID string `plan`.
Safe resolution path: load the owning change's artifact-state map through the existing bounded metadata reader, derive the one primary plan member, compare the parsed `artifact-id=path` map exactly, and add positive coverage for a nonliteral plan ID plus negative coverage for an extra or substituted member; rerun CMD-06 and CMD-03.
needs-decision rationale: none; artifact identity independence and exact primary-plan membership are already established by the approved contract.

## Checklist coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | block | The Node lifecycle path satisfies the v2 graph, but the central Python automation path cannot select it and a valid exact-primary-plan review identity can be rejected. |
| Test coverage | block | Focused tests cover the narrow v2 helpers and literal `plan` fixture; they omit a complete automation transaction and a nonliteral primary-plan ID. |
| Edge cases | block | Contract propagation across coordination/validation and artifact-ID-versus-kind identity are unproved and directly fail. |
| Error handling | concern | Unknown contract helpers fail closed, but defaulted downstream calls can silently select v1 when contract context is omitted. |
| Architecture boundaries | block | The contract discriminator does not reach every workflow-automation decision boundary required by M2. |
| Compatibility | pass | Reviewed Node and Python defaults retain v1 behavior, and no activation or migration was introduced. |
| Security/privacy | pass | No secrets, credentials, external calls, or new sensitive-data handling were introduced. |
| Derived artifact currency | pass | No public skill or adapter publication is allocated to M2; the compatibility fixture was refreshed through the repository-owned update path. |
| Unrelated changes | pass | The implementation diff is scoped to M2 lifecycle/runtime/validation work and its evidence. The user-owned untracked `packages/rigorloop/node_modules/` remains outside the review. |
| Validation evidence | concern | All named suites pass, but direct probes expose two contract cases missing from those suites. |

## No-finding rationale

Not applicable. Material findings `RTS-M2-CR1` and `RTS-M2-CR2` require resolution and rereview before M2 can close.

## Direct proof and residual risk

- A direct policy probe showed `v2_rule_exists=True` and `evaluate_transition_allowed=False` for `WorkflowPosition.PLAN -> WorkflowStage.DELIVERY_REVIEW`, with the central evaluator returning `transition: no rule permits operation toward target`.
- A direct review-validator fixture showed that `primary-plan=docs/plans/example.md` is rejected solely because the ID is not literally `plan`, despite representing the exact primary plan.
- The existing focused suites remain useful regression evidence for Node graph/package behavior and v1 compatibility, but they do not override these direct failures.
- Rereview should focus on end-to-end contract propagation, fail-closed unknown contract handling at every new parameter, v1 behavior compatibility, and exact member identity agreement across Node and Python validators.

## Handoff

- Reviewed milestone: M2. Implement the inactive v2 lifecycle and plan-centered package
- Review status: changes-requested
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4, M5
- Required review-resolution: yes
- No automatic downstream handoff: this first-pass review stops before correction or M3.
- Recommended next stage: resolve `RTS-M2-CR1` and `RTS-M2-CR2`, return M2 to implementation for bounded corrections, rerun the exact M2 validation commands, and perform code-review again.
- Final closeout readiness: not ready; M2 has two open material findings and M3-M5 remain unstarted.
