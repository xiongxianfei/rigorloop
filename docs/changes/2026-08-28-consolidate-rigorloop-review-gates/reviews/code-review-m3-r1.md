# Code Review M3 R1: Consolidated Workflow Routing

Review ID: code-review-m3-r1
Stage: code-review
Round: r1
Reviewer: Codex independent code-review with fresh-assumption reset
Review date: 2026-08-30
Target: M3 path-bounded implementation in commit `e1a205e86a103c8001509dc111b84c9a5d1b0db7`
Reviewed milestone: M3
Reviewed artifact: consolidated stage routing, package correction routing, automation projection, and downstream authority consumption
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Material findings: CRG-M3-CR1, CRG-M3-CR2

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/reviews/code-review-m3-r1.md`, `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-log.md`, `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-resolution.md`, and the review summary in `change.yaml`
- Open blockers: CRG-M3-CR1 and CRG-M3-CR2
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CRG-M3-CR1, CRG-M3-CR2
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/reviews/code-review-m3-r1.md`
- Review log: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-log.md`
- Review resolution: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-resolution.md`
- Reviewed milestone: M3
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: CRG-M3-CR1, CRG-M3-CR2
- Verify readiness: not-claimed

## Review inputs

- Actual diff: the M3 routing paths in commit `e1a205e86a103c8001509dc111b84c9a5d1b0db7`; the commit also contains already-reviewed M2 closure history, which is outside this M3 judgment.
- Governing authority: CRG-R2 through CRG-R5, CRG-R15, CRG-R21, CRG-R25 through CRG-R29, CRG-R33 through CRG-R42, CRG-T08, CRG-T11, CRG-T12, the accepted package-topology ADR, and M3 of the approved plan.
- Directly inspected implementation: lifecycle stage graph, shared completion decision, read-model package blockers, correction routing, Python automation stage/policy projections, and targeted public tests.
- Additional evidence needed: the Python automation sources were inspected because M3 explicitly owns automation policy/state synchronization; the downstream read fixture was inspected because CRG-T12 requires absence and historical-only authority to block.

## Independent risk map

- Affected behavior: consolidated pre-implementation progression, active automation synchronization, package correction return, and downstream evidence admission.
- Highest-impact failure modes: JavaScript writes an automation stage rejected by the automation engine; Code Review or Verify proceeds without current package authority; a multi-owner package correction grants partial authority.
- Changed boundaries: BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-COMPAT-001, INT-003, INT-007, INT-008.
- Expected evidence: public consolidated-stage automation proof, current-package-required downstream proof, stale/mixed/historical-only rejection, and multi-owner correction proof.
- Intentionally out of scope: M4 published review skills, M5 generated adapters, M6 release cutover, and final holistic review.

## Actual-diff summary

M3 closes the JavaScript lifecycle graph around `design-review` and `delivery-review`, centralizes stage completion, extends package correction routing, and rejects stale or mixed package projections when those projections exist. It does not update the repository's Python automation vocabulary/policy to represent the new stages, and its downstream read model checks package authority only when a package projection is already present.

## Findings

### Finding CRG-M3-CR1

Finding ID: CRG-M3-CR1
Severity: major
Location: `scripts/workflow_automation_policy.py:21-62`, `scripts/workflow_automation_policy.py:577-595`, and the unchanged automation state/routing consumers
Evidence: M3 explicitly requires automation policy/state updates and active automation synchronization. The JavaScript transition mutates `workflow.automation.current_stage`, but `WorkflowStage` and `WorkflowPosition` still contain the retired artifact-review sequence and omit `design-review` and `delivery-review`; `STAGE_POLICIES` likewise routes through `spec-review`, `architecture-review`, `plan-review`, and `test-spec-review`. Direct execution of `WorkflowStage("design-review")` and `WorkflowStage("delivery-review")` raises `ValueError`, so an active automation projection synchronized by the new JavaScript graph cannot be interpreted by the automation engine.
Required outcome: The automation stage and position vocabularies, policies, state transitions, validators, and focused tests must represent the consolidated graph and accept both consolidated review stages while rejecting retired progression.
Safe resolution path: Replace the affected pre-implementation automation policies with `proposal -> proposal-review -> architecture -> spec -> design-review -> plan -> test-spec -> delivery-review -> implement`; update state/validation fixtures; add a public-path test that advances an active automation projection through both consolidated reviews and then resumes it through the Python engine.
needs-decision rationale: none

### Finding CRG-M3-CR2

Finding ID: CRG-M3-CR2
Severity: major
Location: `packages/rigorloop/dist/lib/lifecycle-read.js:256-258` and `packages/rigorloop/test/lifecycle-read.test.js:67-95`
Evidence: M3 and CRG-T12 require Code Review, explanation, Verify, and PR inputs to reject stale, mixed, partial, or historical-only package authority. The read model adds package blockers only when `change.review_packages[kind]` already exists. The public read fixture has no design or delivery package, yet status at `implement` succeeds and `context code-review` advertises `record-review`; therefore absence or legacy-only evidence is accepted rather than blocked. The new downstream regression proves stale and mixed projections only after both packages have been created.
Required outcome: Every M3-owned downstream consumer must require a current approved design package and delivery package, including exact member maps and bound review IDs, and must fail closed when either projection is absent, partial, stale, mixed, or historical-only.
Safe resolution path: Add a downstream package-authority gate shared by status/context and each downstream consumer; activate it for the consolidated contract at the single-cutover boundary without adding hashes or a per-change topology selector; add public regressions for missing packages and historical individual review evidence as well as the existing stale/mixed cases.
needs-decision rationale: none

## Checklist coverage

| Item | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | CRG-M3-CR1 misses the M3 automation contract; CRG-M3-CR2 misses CRG-R41/CRG-R42 downstream authority. |
| Test coverage | block | No Python test enters either consolidated review stage, and no downstream test covers absent or historical-only packages. |
| Edge cases | block | Consolidated automation stages and absent package authority are both outcome-changing unhandled cases. |
| Error handling | concern | Existing stale and mixed package projections fail closed, but missing projections silently bypass the gate. |
| Architecture boundaries | block | JavaScript and Python now encode incompatible active workflow graphs. |
| Compatibility | concern | Retired automation routes remain executable while consolidated routes are unrepresentable; release cutover remains M6 scope. |
| Security/privacy | pass | No credential, network, personal-data, or external authorization surface changes in M3. |
| Derived artifact currency | concern | The JavaScript graph changed while Python policy/state projections remain on the old graph. |
| Unrelated changes | pass | The review is path-bounded to M3; earlier M2 closure content in the commit is excluded. |
| Validation evidence | block | Targeted suites pass, but their fixture selection omits the two failing contract partitions above. |

## Direct proof

```text
python -c 'from scripts.workflow_automation_policy import WorkflowStage; print(WorkflowStage("design-review"))'
=> ValueError: 'design-review' is not a valid WorkflowStage

python -c 'from scripts.workflow_automation_policy import WorkflowStage; print(WorkflowStage("delivery-review"))'
=> ValueError: 'delivery-review' is not a valid WorkflowStage

node --test packages/rigorloop/test/lifecycle-read.test.js packages/rigorloop/test/lifecycle-stage-advance.test.js packages/rigorloop/test/lifecycle-correction-route.test.js
=> 26 passed, 0 failed; inspection shows the success fixtures omit packages and the downstream rejection test covers only existing stale/mixed projections
```

## Handoff

This review is recorded before any correction. M3 remains review-requested and M4 must not start. Resolve CRG-M3-CR1 and CRG-M3-CR2 through the implementation owner, run the named automation and downstream public-path regressions, and return the changed M3 slice for a fresh code review.
