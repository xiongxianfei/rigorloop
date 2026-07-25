# Code Review M6 R2

Review ID: code-review-m6-r2
Stage: code-review
Round: M6 R2
Reviewer: independent same-session context-reset reviewer
Target: M6 correction commit `8fadb828`
Reviewed artifact: M6 correction commit `8fadb828`
Reviewed milestone: M6. Atomic Public Cutover, Legacy Adapters, and Integration Proof
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-24
Recording status: recorded
Material findings: BRF-M6-CR5, BRF-M6-CR6, BRF-M6-CR7
Immediate next stage: review-resolution M6

## Review context

- Invocation mode: direct isolated milestone rereview
- Independence level: `L1-same-session-context-reset`
- Review surface: commit `8fadb828` against parent `02c3bc79`
- Requirement-fidelity gate: applied to `BRF-R023`, `BRF-R037`, `BRF-R043b` through `BRF-R043e`, `BRF-R044`, `BRF-R060` through `BRF-R067`, `BRF-R098a` through `BRF-R100`, T22, T28, and T30
- Risk tier: elevated
- Automated independent-review gate: not required for this direct isolated invocation
- Context limitation: the reviewer shares the implementation session, intentionally reset to the actual commit, approved specification, active test specification, and current M6 plan, and does not claim blind L2 independence

## Independent risk map

### Affected behavior

- Independent affected-selector validation.
- Atomic legacy migration and cancellation.
- Public status and result evidence.
- Public authorization and persisted-target resume.
- Bounded correction and verification routing.
- Deterministic composed-engine proof.

### Highest-impact failure modes

- A public resume mutates after canonical evidence changes from the identities observed by the run.
- Verification consent is persisted before closeout evidence is independently valid.
- Focused tests are presented as T28/T30 proof while required composed scenarios remain absent.
- Cancellation or migration exposes a nonterminal intermediate state.
- Result projection loses durable receipt or artifact evidence.

### Changed boundaries

- `scripts/workflow_automation.py`: public authorization, resume, control, and result paths.
- `scripts/workflow_automation_state.py`: legacy cancellation and status projection.
- `scripts/validate_workflow_automation.py`: closed affected-selector registry.
- Workflow automation regression suites and lifecycle evidence.

### Expected evidence

- Public resume compares current canonical evidence with the run's persisted observed identities before mutation.
- Verification authorization re-reads and validates all repository-backed closeout prerequisites before persisting or reactivating a run.
- T28 and T30 execute their complete declared scenario sets through the public composition.
- Repeated and reversed runs compare receipts, state, status, teardown, and external-action trap counts.

### Direct-inspection areas

- `authorize_public_run`.
- `resume_public_run` and `coordinate_one_stage`.
- `test_public_composition_is_deterministic_and_order_independent`.
- Verification-authorization and public-resume tests.
- R1 finding resolutions and proof claims.

### Intentionally out-of-scope areas

- Final holistic cross-milestone review.
- `explain-change`, final `verify`, and PR handoff.
- Closed M1-M5 behavior except where M6 exposes it publicly.

### Risk classes

- Applicable: authorization integrity, canonical-state drift, interruption recovery, migration, observability, deterministic proof, and external-action containment.
- Not applicable: personal-data processing, cryptographic protocol design, accessibility UI, and deployed-service availability.

### Falsifiable questions

- Can public resume complete after every canonical identity observed at run creation changes?
- Can verification authorization be persisted from six syntactically complete but nonexistent identities?
- Does T30 run transaction, interruption, migration, status, and final-success scenarios twice and in reverse order?
- Do active and terminal legacy cancellation remain one-write and byte-preserving?
- Does deleting an exact affected-selector row fail independently?

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, `review-log.md`, `review-resolution.md`, `change.yaml`, active plan, and plan index
- Open blockers: `BRF-M6-CR5`, `BRF-M6-CR6`, `BRF-M6-CR7`
- Next stage: review-resolution M6
- Review status: changes-requested
- Material findings: `BRF-M6-CR5`, `BRF-M6-CR6`, `BRF-M6-CR7`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m6-r2.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m6-r2`
- Reviewed milestone: M6. Atomic Public Cutover, Legacy Adapters, and Integration Proof
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M6 resolution and rereview
- Required review-resolution: yes
- Finding IDs: `BRF-M6-CR5`, `BRF-M6-CR6`, `BRF-M6-CR7`
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: commit `8fadb828` against parent `02c3bc79`.
- Tracked governing branch state: approved specification, approved test specification, approved architecture, accepted ADR, active M6 plan, and recorded R1 resolution.
- Direct proof: a temporary public run accepted changed proposal and proposal-review identities, completed `spec`, and retained the old `observed_identities`; source/test inspection proved verification authorization accepts arbitrary complete strings and T30 declares only two scenarios.
- Validation evidence challenged: 67 engine, 68 validator, 60 state, and 16 policy tests plus the recorded selected-CI and broad-smoke evidence.

## Diff summary

The correction adds an independent cross-spec selector registry, one-write legacy cancellation, richer public result projection, explicit risk-class authorization, and a public persisted-target resume entry point.

It also redirects existing authoring, correction, implementation, review, and verification tests through the public resume entry point and adds one repeated/reversed-order test containing authoring/status and legacy-cancellation scenarios.

## Findings

### BRF-M6-CR7 - Composed determinism proof remains incomplete

Finding ID: BRF-M6-CR7
Severity: major
Location: `scripts/test-workflow-automation.py:1146-1295`
Evidence: The R1 required outcome explicitly requires clean, correction, interruption, cancellation, migration, missing-authority, and final-success public flows plus T30's repeated/reversed composed comparison. The new deterministic test declares only `("authoring", "legacy-cancel")`. It contains no prepared-receipt interruption/resume, no final-success verify, no missing-authority boundary, no correction scenario, no sanitized-environment or teardown assertion, and no external-action trap counter. Separate one-pass tests routed through `resume_public_run` do not satisfy T30's requirement that composed transaction, interruption, migration, status, and final-success scenarios each run twice and in reversed declared order. This is a failed remediation of the R1 finding.
Required outcome: Execute every T28 scenario through the public composition and make T30 repeat and reverse the complete composed transaction, interruption, migration, status, and final-success set while comparing canonical state, receipts, result/status output, teardown, and external-action counts.
Safe resolution path: Build reusable fresh-root scenario drivers for clean, correction, interrupted-receipt resume, unified cancellation, legacy migration, missing authority, and final verify. Run the fixed-input scenario registry twice and in reverse, normalize only declared nondeterministic fields, assert exact state/evidence equivalence and teardown, and trap/count every prohibited external boundary.
needs-decision rationale: none; the approved test specification and prior accepted finding already define the required proof.
auto_fix_class: none

### BRF-M6-CR5 - Public resume ignores persisted observed identities

Finding ID: BRF-M6-CR5
Severity: blocker
Location: `scripts/workflow_automation.py:3471-3569` and `scripts/workflow_automation.py:4239-4318`
Evidence: `start_public_run` persists `observed_identities`, but `resume_public_run` neither loads them nor supplies them as `previously_observed`. `coordinate_one_stage` compares canonical evidence only when the caller voluntarily provides that argument. A temporary-repository probe started a `spec` target with proposal/review identities `p1/r1`, resumed with `p2/r2`, completed the spec transition, and left persisted `observed_identities` at `p1/r1`. The mechanism therefore mutated after a canonical-state mismatch instead of pausing, violating `BRF-R023`, `BRF-R044`, and `BRF-R100`.
Required outcome: Every public resume must bind re-evaluated canonical state to the identities durably observed by the run and pause before capability derivation, receipt preparation, or stage mutation when they disagree, while allowing only explicitly defined ownership-handoff or completed-transition identity advancement.
Safe resolution path: Make `resume_public_run` obtain the persisted observed-identity baseline from the validated state snapshot and pass it through a single state-aware canonical comparison/update policy. Add public pre-plan and active-plan drift regressions that assert zero capability, receipt, artifact, and state mutation on mismatch, plus positive tests for explicitly permitted post-transition identity advancement.
needs-decision rationale: none; the approved canonical-state and resume contracts already require the pause.
auto_fix_class: none

### BRF-M6-CR6 - Verification authorization trusts shaped hashes

Finding ID: BRF-M6-CR6
Severity: blocker
Location: `scripts/workflow_automation.py:3419-3438` and `scripts/test-workflow-automation.py:878-915`
Evidence: `authorize_public_run` treats verification authority as valid when all six fields are merely nonempty strings. It receives neither repository evidence paths nor an active plan/current-code provider and performs no semantic or identity validation. The positive test uses arbitrary values such as `sha256:closed` and `sha256:final-review`, persists a verification parent, and reactivates the paused run. That directly contradicts `BRF-R043b` through `BRF-R043d`, which allow verification parent authorization only after closed milestones, clean final review, valid promotion, current explanation and branch inputs, and known verification evidence independently validate.
Required outcome: Verification parent authorization must remain absent and the run paused until the complete repository-backed verification basis is independently re-read, identity-matched, and semantically valid at the authorization interaction.
Safe resolution path: Require repository root plus the same canonical basis-path and code-state inputs used by verification readiness; call the repository-backed readiness resolver before parent persistence; bind the validated identity projection into the parent; reject missing, stale, forged, or semantically non-clean evidence without reactivating the run. Replace the arbitrary-hash positive test with real temporary artifacts and add negative tests for each prerequisite.
needs-decision rationale: none; the approved verification-authorization timing contract is explicit.
auto_fix_class: none

## Prior finding reconciliation

| Finding | Result | Evidence |
| --- | --- | --- |
| `BRF-M6-CR1` | resolved | The validator now compares the parsed ledger with `CROSS_SPEC_AFFECTED_SELECTORS`; deleting `R1e` is covered by an independent temporary-repository regression. |
| `BRF-M6-CR2` | resolved | Active legacy off uses one state-adapter replacement, the old second write is trapped, and terminal completed state is byte-preserving. |
| `BRF-M6-CR3` | resolved | Public result projection now contains persisted canonical provenance, receipt history, fixes, decisions, and changed artifacts with active/completed/migrated coverage. |
| `BRF-M6-CR4` | failed-remediation | Public wrappers and correction authority exist, but the required T28/T30 complete composed proof remains compressed to two deterministic scenarios. |

## Requirement-fidelity result

| Contract | Result | Evidence |
| --- | --- | --- |
| `BRF-R023`, `BRF-R044`, `BRF-R100` | block | Public resume ignores the run's durable observed-identity baseline and accepts complete canonical drift. |
| `BRF-R043b` through `BRF-R043e` | block | Verification authorization validates field shape, not repository-backed prerequisite truth. |
| `BRF-R060` through `BRF-R067` / T28 | concern | Individual public coordinator tests exist, but no one end-to-end scenario fixture proves the complete bounded workflow. |
| `BRF-R098a` through `BRF-R098h` | pass | Independent selector completeness and one-write active/terminal legacy cancellation are directly covered. |
| `BRF-R099` / T22 | pass | Public results project the required durable fields for the covered active, completed, and migrated states. |
| T30 | block | The repeated/reversed registry contains only authoring and legacy cancellation and omits interruption and final success. |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | `BRF-M6-CR5` and `BRF-M6-CR6` violate explicit MUST-level canonical-state and verification-authorization contracts. |
| Test coverage | block | `BRF-M6-CR7` records the residual T28/T30 scenario compression; the existing verification-authorization positive test codifies the unsafe behavior. |
| Edge cases | block | Canonical drift and forged-but-shaped verification basis are accepted; deterministic interruption/final-success proof is absent. |
| Error handling | block | Public resume and authorization continue where the contract requires a pause. |
| Architecture boundaries | concern | The sole state writer is retained, but public orchestration bypasses repository-backed state and verification evaluators at two decision boundaries. |
| Compatibility | pass | R1 legacy active and terminal cancellation defects are corrected without restoring a legacy writer. |
| Security/privacy | block | Verification authority is an authorization-integrity boundary and currently accepts unverified caller assertions. No secret leakage was observed. |
| Derived artifact currency | pass | This correction does not edit canonical skill content or generated adapter output. |
| Unrelated changes | pass | The diff is scoped to R1 correction, tests, and lifecycle evidence. |
| Validation evidence | block for adequacy | Focused suites pass, but direct probes and test-spec comparison expose untested unsafe behavior and missing required scenarios. |

## Validation challenge

- `python scripts/test-workflow-automation.py`: 67 tests passed.
- `python scripts/test-validate-workflow-automation.py`: 68 tests passed.
- `python scripts/test-workflow-automation-state.py`: 60 tests passed.
- `python scripts/test-workflow-automation-policy.py`: 16 tests passed.
- The recorded 12-check selected CI and 12-check broad-smoke results are credible for the commands run.
- Passing results do not cover persisted-observed-identity enforcement or repository-backed authorization-time verification readiness.
- T30's committed two-scenario registry is not the scenario set required by the approved test specification.

## Direct-proof gaps

- No public-resume regression binds current canonical evidence to the run's persisted observed identities.
- No verification-authorization test re-reads real closeout artifacts before parent persistence.
- No T30 registry includes interruption/resume or final-success verification.
- No T30 assertion compares external-action trap counts, sanitized environment, or fixture teardown.

## Milestone handoff

- Reviewed milestone: M6. Atomic Public Cutover, Legacy Adapters, and Integration Proof
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes; `BRF-M6-CR5`, `BRF-M6-CR6`, and `BRF-M6-CR7`
- Remaining in-scope implementation milestones: M6 resolution and rereview
- Next stage: review-resolution M6
- Final closeout readiness: not ready; M6 findings, M6 rereview, final holistic review, explanation, verification, and PR handoff remain

This direct review is isolated. It records the findings but does not begin correction automatically.
