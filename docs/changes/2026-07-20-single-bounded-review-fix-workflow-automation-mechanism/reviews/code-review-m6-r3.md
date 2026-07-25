# Code Review M6 R3

Review ID: code-review-m6-r3
Stage: code-review
Round: M6 R3
Reviewer: independent same-session context-reset reviewer
Target: M6 correction commit `cdf27205`
Reviewed artifact: M6 correction commit `cdf27205`
Reviewed milestone: M6. Atomic Public Cutover, Legacy Adapters, and Integration Proof
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-25
Recording status: recorded
Material findings: BRF-M6-CR8, BRF-M6-CR9
Immediate next stage: review-resolution M6

## Review context

- Invocation mode: direct isolated milestone rereview
- Independence level: `L1-same-session-context-reset`
- Review surface: commit `cdf27205` against parent `8fadb828`
- Requirement-fidelity gate: applied to `BRF-R019`, `BRF-R023`, `BRF-R043b` through `BRF-R044`, `BRF-R060` through `BRF-R077`, `BRF-R099`, `BRF-R100`, T22, T28, and T30
- Risk tier: elevated
- Automated independent-review gate: not required for this direct isolated invocation
- Context limitation: the reviewer shares the implementation session, intentionally reset to the actual commit, approved specification, active test specification, and current M6 plan, and does not claim blind L2 independence

## Independent risk map

### Affected behavior

- Durable canonical-identity selection and advancement during public resume.
- Repository-backed verification authorization.
- Composed public workflow and deterministic integration proof.

### Highest-impact failure modes

- A public run reaches an authorization boundary but remains durably active.
- A test reports a pause that the canonical state never recorded.
- An ordinary failed stage invocation is mislabeled as interrupted prepared-receipt recovery.
- Status or external-action proof executes outside the declared isolated environment.
- Named T28 scenarios exist only as labels rather than contract-complete workflow traversals.

### Changed boundaries

- `scripts/workflow_automation.py`: public target creation, authorization, and resume.
- `scripts/workflow_automation_state.py`: observed-identity advancement.
- `scripts/test-workflow-automation.py`: T28/T30 public composition proof.

### Expected evidence

- Missing verification authority durably pauses the run with the exact required reason before stage invocation.
- Prepared-receipt interruption resumes against the original receipt and capability after inspecting stage-owned evidence.
- Status, canonical state, receipts, environment, teardown, and external-action counters are observed inside the controlled scenario boundary.
- Each named scenario proves its governing behavior rather than synthesizing the expected result.

### Direct-inspection areas

- `resume_public_run`.
- `coordinate_one_stage` exception and receipt-finalization behavior.
- `test_public_composition_is_deterministic_and_order_independent`.
- Public verification-authorization and canonical-drift regressions.

### Intentionally out-of-scope areas

- Final holistic cross-milestone review.
- `explain-change`, final `verify`, and PR handoff.
- Closed M1-M5 behavior except where M6 exposes it publicly.

### Risk classes

- Applicable: authorization integrity, durable state, interruption recovery, evidence fidelity, deterministic proof, and external-action containment.
- Not applicable: personal-data processing, cryptographic protocol design, accessibility UI, and deployed-service availability.

### Falsifiable questions

- After a verify-target run reaches the verification boundary without authority, is its stored status `paused` with `verification-authorization-required`?
- Does the interruption scenario leave a `prepared` receipt and resume it without silently substituting a new transition?
- Is public status executed under the same sanitized environment and fail-on-call boundaries whose coverage is claimed?
- Do the correction and interruption scenarios enter through public APIs without direct state injection or result synthesis?

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, `review-log.md`, `review-resolution.md`, `change.yaml`, active plan, and plan index
- Open blockers: `BRF-M6-CR8`, `BRF-M6-CR9`
- Next stage: review-resolution M6
- Review status: changes-requested
- Material findings: `BRF-M6-CR8`, `BRF-M6-CR9`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m6-r3.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m6-r3`
- Reviewed milestone: M6. Atomic Public Cutover, Legacy Adapters, and Integration Proof
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M6 resolution and rereview
- Required review-resolution: yes
- Finding IDs: `BRF-M6-CR8`, `BRF-M6-CR9`
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: commit `cdf27205` against parent `8fadb828`.
- Tracked governing branch state: approved specification, approved test specification, approved architecture, accepted ADR, active M6 plan, and recorded R2 resolution.
- Direct proof: a fresh temporary public verify-target run without verification authority raised `public resume requires exactly one matching active parent authorization` while its durable run remained `active`; source inspection showed the T30 test synthesizes a paused result, finalizes its simulated interruption as `failed`, resumes with a new transition ID, and executes status after leaving the environment and external-action trap context.
- Validation evidence challenged: the targeted T30 test and all 70 engine tests pass, demonstrating that the current suite does not detect the durable pause violation or the interruption/status proof substitutions.

## Diff summary

The correction makes public resume select durable observed identities, advances those identities from verified canonical synchronization, and validates verification authority against repository-backed readiness evidence.

It also replaces the previous two-case deterministic fixture with seven named scenarios and compares repeated and reversed results, state, status, environment, teardown, and external-action counters.

## Findings

### BRF-M6-CR8 - Missing verification authority does not durably pause the public run

Finding ID: BRF-M6-CR8
Severity: blocker
Location: `scripts/workflow_automation.py:3544-3559` and `scripts/test-workflow-automation.py:1826-1855`
Evidence: `resume_public_run` rejects a missing matching parent authorization before any pause path. A fresh temporary-repository probe started `$workflow auto: verify` without verification authority, called public resume at `stage="verify"`, received `public resume requires exactly one matching active parent authorization`, and then read the canonical run back as `status: active` with no pause reason. The new deterministic test catches that exception and constructs `{"stage_outcome": "paused", ...}` in local test memory without checking or changing durable state. This violates `BRF-R043e` and lets status/resume continue to describe an active run after the required authorization boundary.
Required outcome: Reaching the verification boundary without verification authority must atomically persist `run.status: paused` and `pause_reason: verification-authorization-required`, report the concrete available basis, and invoke neither `explain-change` nor `verify`.
Safe resolution path: Route the zero-match verification-parent case through one state-adapter pause operation before returning the public result; preserve fail-closed handling for duplicate or malformed parents; add a direct public regression that asserts the stored run, result projection, zero stage invocation, and later `authorize_public_run` reactivation behavior.
needs-decision rationale: none; `BRF-R043e` defines the exact durable result.
auto_fix_class: none

### BRF-M6-CR9 - T28/T30 still substitutes failure/retry and out-of-bound observations for interruption recovery proof

Finding ID: BRF-M6-CR9
Severity: major
Location: `scripts/test-workflow-automation.py:1685-1753`, `scripts/test-workflow-automation.py:1856-1870`, and `scripts/test-workflow-automation.py:1978-1992`
Evidence: The scenario named `interruption` throws inside `invoke_stage`, but production code catches that exception and finalizes `transition-interrupted` as `failed`; the test then starts the successful work under a different `transition-resumed` ID. It therefore proves ordinary failure plus a new transition, not `BRF-R073` through `BRF-R075` evidence-first resume of the original prepared receipt. The correction scenario is installed by `prepare_proposal_correction_transaction`, which directly replaces the store with a preassembled automation transaction before public resume. Finally, the status query and canonical-state read occur after the `patch.dict` sanitized environment and fail-on-call external boundaries have exited, although T30 claims status and complete scenario observation under those controls. The test's names and equality checks are deterministic, but the required composed recovery and isolation behaviors remain unproved.
Required outcome: T28/T30 must exercise a real public prepared-receipt interruption and evidence-first reconciliation against the original transition/capability, enter correction through the supported public state/authorization path, and observe status plus canonical state while the sanitized environment and external-action traps are active.
Safe resolution path: Add an explicit crash seam after prepared-receipt persistence that does not convert the receipt to `failed`; restart through public resume using the same transition key, receipt, and capability and assert reconcile-only or policy-permitted retry behavior. Construct correction authority and findings through public APIs or a documented stage-owned evidence setup rather than replacing unified automation state. Move status/state observation inside the controlled context and assert the stored scenario-specific invariants before comparing repeated and reversed runs.
needs-decision rationale: none; T28, T30, the deterministic fixture contract, and `BRF-R068` through `BRF-R077` already define the required proof.
auto_fix_class: none

## Prior finding reconciliation

| Finding | Result | Evidence |
| --- | --- | --- |
| `BRF-M6-CR5` | resolved | Public resume rejects caller-provided `previously_observed`, loads the durable baseline, pauses on direct canonical mismatch, and has positive completion/handoff identity-advancement regressions. |
| `BRF-M6-CR6` | resolved | Initial and later verification authorization call repository-backed readiness validation and the shaped-hash plus per-prerequisite regressions cover the corrected boundary. |
| `BRF-M6-CR7` | failed-remediation | The seven labels were added, but the interruption scenario is failure/new-transition rather than prepared-receipt resume, correction begins from direct state replacement, missing authority fabricates a paused result, and status is observed outside the declared environment/trap boundary. Residual defects are recorded as `BRF-M6-CR8` and `BRF-M6-CR9`. |

## Requirement-fidelity result

| Contract | Result | Evidence |
| --- | --- | --- |
| `BRF-R019`, `BRF-R023`, `BRF-R044`, `BRF-R100` | pass | Public resume now uses the durable observed-identity baseline and advances it only through verified completion evidence. |
| `BRF-R043b` through `BRF-R043d` | pass | Verification authority is derived from repository-backed closeout evidence rather than shaped hashes. |
| `BRF-R043e` | block | The public missing-authority path raises while leaving the canonical run active. |
| `BRF-R068` through `BRF-R077` / T28 | block | The named interruption case finalizes the original receipt as failed and starts a new transition instead of proving prepared-receipt recovery. |
| T22 / T30 | block | The deterministic fixture synthesizes pause output and performs status/state observation after the controlled environment and external-action traps exit. |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | `BRF-M6-CR8` violates the explicit durable verification-boundary pause contract. |
| Test coverage | block | `BRF-M6-CR9` shows the named T28/T30 cases do not directly prove their stated recovery and isolation behaviors. |
| Edge cases | block | Missing authority and prepared-receipt interruption are named edge cases with incorrect or absent direct proof. |
| Error handling | block | Missing verification authority leaves a resumable active run; stage exceptions are converted to failed receipts and then mislabeled as interruption recovery. |
| Architecture boundaries | concern | The production state write boundary is retained, but the fixture bypasses public setup by replacing unified state. |
| Compatibility | pass | No reviewed change re-enables a legacy writer or removes a required alias. |
| Security/privacy | concern | External-action counters are zero, but status and final state inspection occur outside the fail-on-call boundary whose coverage is claimed. |
| Derived artifact currency | pass | This correction does not hand-edit generated adapter bodies, and the reviewed lifecycle artifacts consistently target R3 before this review. |
| Unrelated changes | pass | The implementation diff is limited to R2 resolution code, tests, and lifecycle evidence. |
| Validation evidence | block | The targeted test and all 70 engine tests pass despite the directly reproduced durable-state violation and proof substitutions. |

## Direct-proof gaps

- No public test proves `run.status: paused` and exact pause reason after missing verification authority.
- No T30 scenario preserves a prepared receipt across an interruption and reconciles or retries the original transition according to its policy.
- No composed correction scenario reaches its transaction setup solely through supported public state and authorization APIs.
- No status/canonical-state observation is performed while the declared environment and external-action controls remain active.

## Milestone handoff

- Reviewed milestone: M6. Atomic Public Cutover, Legacy Adapters, and Integration Proof
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M6-CR8` and `BRF-M6-CR9`
- Remaining in-scope implementation milestones: M6 resolution and rereview
- Next stage: review-resolution M6
- Final closeout readiness: not ready
- Reason: M6 has open material findings; final holistic code review, explain-change, verify, and PR handoff remain pending.

## Isolation

This direct code-review is isolated. It records findings and synchronized lifecycle state but does not apply fixes or start review-resolution automatically.
