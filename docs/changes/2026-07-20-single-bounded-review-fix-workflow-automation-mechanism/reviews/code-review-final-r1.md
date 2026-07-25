# Final Holistic Code Review R1

Review ID: code-review-final-r1
Stage: code-review
Round: Final R1
Reviewer: independent same-session context-reset reviewer
Target: complete branch diff `52bdcbb329897225c22a593b8e04541409e2d315..962bdc4a`
Reviewed artifact: complete M1-M6 implementation and lifecycle diff through commit `962bdc4a`
Reviewed milestone: Final holistic M1-M6 closeout
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-25
Recording status: recorded
Material findings: BRF-FH-CR1
Immediate next stage: review-resolution

## Review context

- Invocation mode: direct isolated final holistic review
- Independence level: `L1-same-session-context-reset`
- Review surface: all 125 changed files and 43,434 added lines in the merge-base range `52bdcbb329897225c22a593b8e04541409e2d315..962bdc4a`
- Requirement-fidelity gate: applied across the approved unified automation spec, approved test spec, accepted architecture and ADR, active M1-M6 plan, and all recorded review resolutions
- Risk tier: elevated
- Automated independent-review gate: not required for this direct isolated invocation
- Context limitation: the reviewer shares the implementation session, intentionally reset to the complete governing contract and branch diff before challenging final validation selection, and does not claim blind L2 independence

## Independent risk map

### Affected behavior

- One writable target-driven automation mechanism from proposal review through verification.
- Canonical change-local state, structured targets, risk-scoped authority, and prepared-transition recovery.
- Proposal and implementation correction loops, milestone review, final review, and verification boundaries.
- Legacy dual-read/single-write adapters and cancellation.
- Public workflow guidance, schemas, validators, generated adapter sources, and repository validation selection.

### Highest-impact failure modes

- A source change bypasses the regression suite that proves its security or authority boundary.
- Recovery repeats or skips a stage-owned mutation.
- Parent authorization is mistaken for executable capability.
- Automation state becomes a competing owner of plan or review truth.
- Legacy adapters revive a retired writer.
- Verification or public orchestration crosses the PR or external-action boundary.

### Changed boundaries

- `scripts/workflow_automation.py`, `scripts/workflow_automation_policy.py`, `scripts/workflow_automation_state.py`, and `scripts/validate_workflow_automation.py`.
- `scripts/workflow_code_state.py`, which supplies the canonical Git-backed final-code identity used at verification.
- `scripts/validation_selection.py`, which routes changed paths into repository-owned proof.
- `schemas/change.schema.json`, lifecycle and review validators, canonical workflow skills, specs, architecture, ADRs, and change-local evidence.

### Expected evidence

- Every changed automation module deterministically selects all proof required for its boundary.
- Closed vocabularies fail before consistency checks.
- Prepared-transition recovery preserves exact capability and receipt identity without replay.
- Risk-class boundaries remain separate and verification authority is never future-contingent.
- Public and legacy commands write only unified state and stop before PR or external action.
- Generated or derived public guidance is current with canonical skill sources.

### Direct-inspection areas

- The complete changed-path map and module ownership boundaries.
- Workflow-automation validation catalog, category expansion, and path classifier.
- Dedicated code-state provider and its 12 regression tests.
- Full automation engine, state, policy, validator, and selector suites.
- Active-plan handoff, review-resolution closeout, and final validation commands.

### Intentionally out-of-scope areas

- Final `explain-change`, final verification, and PR preparation.
- Network, publication, deployment, merge, or other external actions.
- Unrelated baseline repository changes outside the merge-base range.

### Risk classes

- Applicable: authorization integrity, durable recovery, canonical-state ownership, Git trust boundary, migration compatibility, validation selection, generated-output currency, and external-action containment.
- Not applicable: personal-data processing, cryptographic protocol design, accessibility UI, and deployed-service availability.

### Falsifiable questions

- Does every changed workflow-automation source or regression path produce deterministic selected-CI coverage?
- Does the canonical code-state provider select its dedicated adversarial Git regression suite?
- Do the complete engine, state, policy, validator, and selector suites remain green?
- Can a final verification boundary be changed without selecting the tests that prove additions, deletions, renames, dirty files, untracked files, and command containment?
- Are all prior material findings durably closed before final review?

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, `review-log.md`, `review-resolution.md`, `change.yaml`, active plan, and plan index
- Open blockers: `BRF-FH-CR1`
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: `BRF-FH-CR1`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-final-r1.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-final-r1`
- Reviewed milestone: Final holistic M1-M6 closeout
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M6 final-holistic resolution and rereview
- Required review-resolution: yes
- Finding IDs: `BRF-FH-CR1`
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: complete branch range `52bdcbb329897225c22a593b8e04541409e2d315..962bdc4a`.
- Tracked governing branch state: approved specification and test specification, approved architecture, accepted ADR, active plan with M1-M6 closed, and closed resolution for the prior 103 material findings.
- Direct proof: explicit-path selected CI for `scripts/workflow_code_state.py` and `scripts/test-workflow-code-state.py`.
- Validation evidence challenged: complete engine, state, code-state, validator, and selector regression suites plus recorded milestone-selected and broad-smoke evidence.

## Diff summary

The branch replaces three writable automation profiles with one target-driven `bounded-review-fix` mechanism, one typed policy projection, one canonical state writer, and one public command surface.

Across M1-M6 it adds closed state and authority contracts, write-ahead recovery, canonical position and repeated-target binding, proposal and implementation review/correction integration, Git-backed final-code identity, verification containment, legacy adapters, public guidance, cross-spec validation, and repository-selected proof.

The final public-cutover selector registers the engine, policy, state, and validator modules as one `workflow-automation` category. It does not register the code-state provider or its dedicated regression suite.

## Findings

### BRF-FH-CR1 — The canonical code-state boundary is omitted from selected-CI routing

Finding ID: BRF-FH-CR1
Severity: major
Location: `scripts/validation_selection.py:117-136`, `scripts/validation_selection.py:1650-1661`, `scripts/validation_selection.py:2158-2168`, and `scripts/test-select-validation.py:73-76`
Evidence: The `workflow-automation` check catalog contains only engine, policy, state, and validator regressions, and the path classifier contains only those four source/test pairs. Running `bash scripts/ci.sh --mode explicit --path scripts/workflow_code_state.py --path scripts/test-workflow-code-state.py` exits 2 and reports `manual-routing-required` for both paths. The dedicated `python scripts/test-workflow-code-state.py` suite passes all 12 tests, but no deterministic selector check invokes it. This contradicts the active plan decision at `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md:661` that every workflow-automation module routes through one complete selected-CI category and leaves future edits to the Git-backed verification trust boundary without their dedicated proof.
Required outcome: Both code-state paths must resolve deterministically to the workflow-automation validation category, and that category must select the dedicated code-state regression suite together with the existing complete automation proof.
Safe resolution path: Add a stable `workflow_automation.code_state_regression` catalog entry for `python scripts/test-workflow-code-state.py`, include it in the `workflow-automation` category, classify both code-state source/test paths, add exact selector regressions for both paths and the complete check set, update the plan/test-spec selected-CI path contract where it is enumerated, and rerun the dedicated suite, all changed automation-path selection, selected CI, and required broad smoke.
needs-decision rationale: none; the approved plan already chooses complete deterministic workflow-automation selection.
auto_fix_class: none

## Cross-milestone interaction coverage

| Milestone | Holistic result | Evidence |
| --- | --- | --- |
| M1 state/policy | pass | Complete policy, state, schema, and fail-closed validation boundaries remain represented in dedicated suites. |
| M2 recovery/migration | pass | State and engine suites retain write-ahead, reconciliation, cancellation, and one-way migration proof. |
| M3 target/canonical position | pass | Engine and lifecycle evidence cover structured target binding, canonical position, and capability evaluation. |
| M4 authoring/proposal review | pass | Engine, review-artifact, and lifecycle proof cover proposal review occurrence, correction, rereview, and authoring continuation. |
| M5 implementation/verification | block | The canonical Git-backed code-state provider has direct tests but no deterministic selected-CI route. |
| M6 public cutover | block | The final selector category claims complete automation proof while omitting the M5 code-state boundary and its regression suite. |

## Prior-finding reconciliation

All 103 material findings recorded before this review remain resolved in the current tracked review-resolution state. `BRF-FH-CR1` is a new cross-milestone integration finding discovered by challenging final validation selection rather than a reopened or failed-remediation finding.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | Runtime behavior aligns with the approved mechanism, but durable proof routing is incomplete for a verification trust boundary. |
| Test coverage | block | Twelve dedicated code-state tests exist and pass, but selected CI cannot reach them from either owning path. |
| Edge cases | concern | The dedicated suite covers Git additions, modifications, deletions, renames, dirty state, untracked state, and command containment; future changes can bypass it. |
| Error handling | pass | Unknown script paths fail closed as manual routing; the defect is that known in-scope paths remain unknown. |
| Architecture boundaries | block | `workflow_code_state.py` is part of the executable verification boundary but is absent from the declared complete automation proof category. |
| Compatibility | pass | No contradictory legacy adapter or retired-writer behavior was found in the holistic pass. |
| Security/privacy | block | The omitted suite protects the exact Git command and final-code identity boundary used before verification authorization. |
| Derived artifact currency | pass | Canonical skills and tracked public documentation align; generated adapter bodies remain untracked release output. |
| Unrelated changes | pass | The complete branch diff remains within the accepted automation consolidation and required lifecycle evidence. |
| Validation evidence | block for adequacy | Engine 73, state 60, code-state 12, validator 68, and selector 133 tests pass, but explicit selection of the code-state paths deterministically blocks. |

## Validation challenge

- `python scripts/test-workflow-automation.py`: 73 tests passed.
- `python scripts/test-workflow-automation-state.py`: 60 tests passed.
- `python scripts/test-workflow-code-state.py`: 12 tests passed.
- `python scripts/test-validate-workflow-automation.py`: 68 tests passed.
- `python scripts/test-select-validation.py`: 133 tests passed.
- `bash scripts/ci.sh --mode explicit --path scripts/workflow_code_state.py --path scripts/test-workflow-code-state.py`: exited 2 with `manual-routing-required` for both paths.
- Passing dedicated and selector suites do not prove integration when no selector fixture names either code-state path.

## Direct-proof gaps

- No selector regression maps `scripts/workflow_code_state.py` to the `workflow-automation` category.
- No selector regression maps `scripts/test-workflow-code-state.py` to the `workflow-automation` category.
- No workflow-automation category assertion includes the code-state regression command.
- The plan's exact selected-CI command omits both code-state paths, so the final-cutover proof does not reveal the missing registration.

## Final closeout handoff

- Reviewed milestone: Final holistic M1-M6 closeout
- Review status: changes-requested
- Implementation milestone state after review: M6 is resolution-needed; M1-M5 remain closed
- Required review-resolution: yes; `BRF-FH-CR1`
- Remaining in-scope implementation milestones: M6 final-holistic resolution and rereview
- Next stage: review-resolution
- Final closeout readiness: not ready; one final holistic finding, rereview, explanation, verification, and PR handoff remain

This direct review is isolated. It records the finding but does not begin correction automatically.
