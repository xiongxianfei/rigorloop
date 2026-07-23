# Code Review: M4 R4 Correction Authority and Review State

Review ID: code-review-m4-r4
Stage: code-review
Round: M4 R4
Reviewer: same-session independent-review reset
Target: M4 correction commit `1980ddc0`
Reviewed artifact: M4 correction commit `1980ddc0`
Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-23
Recording status: recorded
Material findings: BRF-M4-CR7, BRF-M4-CR8, BRF-M4-CR9, BRF-M4-CR10
Immediate next stage: review-resolution

Automated review: no
Review gate outcome: stop
Native review status: changes-requested
Independence level: L0
Reviewer context ID: root-m4-r4-review-reset
Context separation mechanism: The direct formal review used an explicit review-phase reset and inspected the production diff and governing clauses before tests, validation summaries, prior findings, or author resolution claims.
Risk tier: elevated
Risk-tier triggers: Executable correction authority, mutation containment, durable review state, and transactional routing changed.
Risk-tier classifier: Approved review-independence risk-tier contract.
Governing artifacts: `specs/single-bounded-review-fix-workflow-automation.md`; `specs/single-bounded-review-fix-workflow-automation.test.md`; `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md`; approved workflow architecture and ADR.
Formal criteria: Code-review checklist; BRF-R047-R062, BRF-R068-R080, BRF-R087-R090; M4 T10-T12, T24, T26, and MP1 proof.
Initial packet inventory: scripts/workflow_automation.py@1980ddc0#sha256:b52c06a061ecbe3f60d0857e1f1590022b36ee1cdbc90381b34d58e71501b9e8; scripts/workflow_automation_state.py@1980ddc0#sha256:65f096f82ec8c7576fa8ed3a078218014abd8fe1c44296689ee18766c5497d34; scripts/validate_workflow_automation.py@1980ddc0#sha256:6ec22cef33efffc07ed27cc2d8c803059ece273efa2ad6fc421d152cd86d460e; specs/single-bounded-review-fix-workflow-automation.md@1980ddc0#sha256:59241a5e4968a0d6ba60f9772eed56ab8b9e79859a0be1c94e7c77840c724070; specs/single-bounded-review-fix-workflow-automation.test.md@1980ddc0#sha256:e73ac1691966e7f17c1d1342b969681ae660b8a283e2f0130078c564a37e21bd; docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md@1980ddc0#sha256:ba7a474b02b13a2304ebbca3b34a211a92454c52b85a6b2342c48829dd9363d5
Initial packet contains prohibited context: no
Prompt template version: code-review-v1
Initial packet hash: sha256:d69214c6528a2843f81c3273a8b56b27d4a60b99eed102f8b07b5d564336ed56
Manifest owner: direct reviewer
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: `scripts/workflow_automation.py`; `scripts/workflow_automation_state.py`; `scripts/validate_workflow_automation.py`; their changed tests and review evidence
Requirement-fidelity matched path triggers: scripts/*validator*, docs/changes/**/reviews/, docs/changes/**/review-*.md
Requirement-fidelity matched category triggers: autoprogression gates, review-recording contracts, workflow routing contracts, closed enums
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause, property decomposition, production diff, tests, validation evidence, prior findings

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: `BRF-M4-CR7`, `BRF-M4-CR8`, `BRF-M4-CR9`, and `BRF-M4-CR10` block M4 closeout
- Next stage: review-resolution M4
- Review status: changes-requested
- Material findings: `BRF-M4-CR7`, `BRF-M4-CR8`, `BRF-M4-CR9`, `BRF-M4-CR10`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m4-r4.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m4-r4`
- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4 resolution and rereview, M5, M6
- Required review-resolution: yes
- Finding IDs: `BRF-M4-CR7`, `BRF-M4-CR8`, `BRF-M4-CR9`, `BRF-M4-CR10`
- Verify readiness: not-claimed

## Review inputs

- Review surface: commit `1980ddc0` against parent `960d6863`, with production code inspected before changed tests and released validation evidence.
- Tracked governing branch state: commit `1980ddc0`; R4 review evidence was added only after the risk map.
- Governing requirements: BRF-R047-R062, BRF-R068-R080, and BRF-R087-R090.
- Test contract: T10-T12, T24, T26, MP1, and CMD14-CMD20.
- Architecture: stage-owned evidence, sole state writer, prepared receipts, exact effective-capability binding, and fail-closed state validation.
- Prior review and resolution: `code-review-m4-r3.md` and the BRF-M4-CR5/CR6 dispositions, released only after the risk map.

## Blind-first risk map

Affected behavior: Proposal-correction authority derivation from formal review and resolution evidence; proof that proposal correction stayed inside its effective capability; durable proposal-review occurrence, gate, routing, and run-state projection.

Highest-impact failure modes: A correction capability is identity-bound to a reviewed recipe but arbitrary proposal bytes still satisfy completion; mutations not represented by the regular-file snapshot survive while the receipt completes or fails; durable review-result fields validate individually while an impossible outcome, gate, route, or run-state combination remains accepted; a later-target changes-requested occurrence cannot take the specified correction-loop route even when correction authority exists.

Changed boundaries: Formal review evidence to executable correction authority; stage callback to actual-mutation proof; verified review completion to sole-writer durable state; durable review-result state to fail-closed validation.

Evidence expected: Direct proof that the canonical correction recipe constrains the actual proposal mutation; direct proof for callback failure, file creation/deletion, and symlink-like repository mutations; exhaustive outcome/gate/route/run-state consistency tests; exact-target, later-target pause, and later-target correction-loop transactional tests.

Areas requiring direct inspection: Correction-plan parsing and identity binding; proposal-correction callback wrapper and postcondition evaluation; review-result derivation in `finalize_transition`; `latest_review_result` validator consistency checks.

Areas intentionally out of scope: M5 implementation-stage integration; M6 public command and legacy-adapter cutover; external PR, merge, deployment, or destructive Git actions.

Risk classes considered: Authorization containment; partial-failure recovery; durable-state consistency; requirement fidelity; reviewer/corrector separation.

Falsifiable review questions: Can a callback make a proposal change different from the canonical reviewed recipe and still complete? Can a callback mutate a repository entry that the snapshot omits and still complete? Can a callback mutate state and then raise without the escaped mutation being detected? Can an impossible `latest_review_result` combination pass durable-state validation? Can transactional finalization persist correction-loop when a valid correction capability exists?

## Diff summary

The correction binds exact review-log occurrence and formal finding parity,
parses driver-owned classification, rationale, recipe, and a named validation
rule, and hashes those plans into the correction capability.

It also compares regular-file repository snapshots around successful correction
callbacks and atomically derives a fresh proposal-review capability.

Proposal-review finalization now writes review identity, reviewed proposal
identity, outcome, clean-gate state, routing action, and pause reason when
applicable.

Four executable gaps remain: the recorded recipe is not enforced against the
actual proposal mutation; the repository snapshot omits symlink entries and is
not completed on callback failure; durable review-result validation does not
enforce identity or cross-field consistency; and transactional finalization has
no correction-loop route.

## Prior-finding reconciliation

| Prior finding | R4 result | Evidence |
| --- | --- | --- |
| `BRF-M4-CR5` | failed-remediation | Exact occurrence and canonical plan identity are now bound, but the plan does not govern the bytes written, and mutation containment misses failed callbacks and symlink entries. The remaining defects are recorded as `BRF-M4-CR7` and `BRF-M4-CR8`. |
| `BRF-M4-CR6` | failed-remediation | The writer now persists the named fields, but contradictory states pass validation and the composed path cannot persist the required correction-loop route. The remaining defects are recorded as `BRF-M4-CR9` and `BRF-M4-CR10`. |

## Findings

## Finding BRF-M4-CR7

Finding ID: BRF-M4-CR7
Severity: major
Location: `scripts/workflow_automation.py:531-565`, `scripts/workflow_automation.py:939-964`, `scripts/validate_workflow_automation.py:1080-1140`
Evidence: The repository parser binds the canonical recipe text and the validator hashes the resulting plan, but completion never evaluates that recipe. The only supported validation rule is `proposal-identity-changed`, and the coordinator unconditionally passes `deterministic_validation_passed=True` after observing any identity change on the proposal path. A direct probe used the canonical recipe `Append one newline to the reviewed proposal` but appended `UNREVIEWED SEMANTIC CHANGE`; the transition and receipt both completed and fresh rereview authority was activated.
Required outcome: The executable correction must be a deterministic projection of the canonical reviewed recipe, or a stage-owned named validator must prove the exact recipe-specific postcondition before the correction capability is consumed.
Safe resolution path: Replace the descriptive free-text recipe plus generic identity-change rule with a closed executable correction operation or a closed recipe-specific validator carrying immutable inputs and expected outputs. Derive the mutation from that record rather than accepting arbitrary callback bytes, and add positive and wrong-result contrast tests for every supported correction kind.
needs-decision rationale: none; BRF-R062 and BRF-R065 already require deterministic, stage-owned correction and validation.
auto_fix_class: none

## Finding BRF-M4-CR8

Finding ID: BRF-M4-CR8
Severity: major
Location: `scripts/workflow_automation.py:394-404`, `scripts/workflow_automation.py:912-918`, `scripts/workflow_automation.py:1929-1942`
Evidence: `_snapshot_repository_files` explicitly skips symlinks, so creating a repository symlink is absent from both snapshots. A direct probe changed the proposal and created `scripts/escaped-link`; the symlink remained and the transition completed. The wrapper also computes the after-snapshot only when the callback returns. A second probe wrote `scripts/escaped-after-error.py` and raised; the unauthorized file remained while the receipt was merely finalized as `failed`, with no containment result.
Required outcome: Every repository mutation attempted under correction authority must be detected and reconciled against the capability scope on success and failure, including entry-type changes, symlinks, creations, deletions, and callback exceptions.
Safe resolution path: Capture a repository-entry snapshot that includes type and symlink-target identity, compute the after-state in a `finally` path, and fail closed before representing an escaped mutation as a normal failed transition. Prefer executing correction in a bounded temporary worktree or transactional patch application so unauthorized changes can be rejected without leaving them behind. Add direct regressions for symlink creation, file-to-symlink replacement, external symlink targets, and mutate-then-raise behavior.
needs-decision rationale: none; the approved effective-capability and external-action boundaries require complete mutation containment.
auto_fix_class: none

## Finding BRF-M4-CR9

Finding ID: BRF-M4-CR9
Severity: major
Location: `scripts/validate_workflow_automation.py:735-776`; coverage gap in `scripts/test-validate-workflow-automation.py:402-429`
Evidence: The validator requires field presence and closed enum membership, but it does not require non-empty `review_id` or `reviewed_artifact_identity` and does not validate the outcome, clean-gate, routing-action, pause-reason, target, or run-status relationships. A direct probe with empty identities, `outcome: blocked`, `clean_gate: satisfied`, and `routing_action: continue` returned no validation errors. The changed tests exercise unknown enum values only, so impossible known-value combinations remain accepted durable state.
Required outcome: Durable proposal-review state must fail closed unless all identity fields are concrete and the complete outcome/gate/route/pause/run-state projection is valid for the bound structured target.
Safe resolution path: Centralize the proposal-review routing projection in one pure policy function used by finalization and validation. Validate non-empty concrete identities, exact-target versus later-target semantics, clean-gate mapping, pause-reason presence and absence, and compatible run status. Add an exhaustive invalid-combination matrix plus empty-identity regressions.
needs-decision rationale: none; BRF-R047-R058 and BRF-R100 already define the durable consistency contract.
auto_fix_class: none

## Finding BRF-M4-CR10

Finding ID: BRF-M4-CR10
Severity: major
Location: `scripts/workflow_automation_state.py:973-1019`; contrast at `scripts/workflow_automation.py:286-368`; coverage gap in `scripts/test-workflow-automation.py:1332-1380`
Evidence: The pure proposal-review evaluator returns `correction-loop` when a later-target changes-requested review has valid correction authority and remaining budget. The sole writer independently reimplements routing but maps every later-target changes-requested result to `pause` and `proposal-correction-authorization-required`; it receives no correction-capability evidence and has no correction-loop branch. The transactional matrix asserts only exact target, later approved, and later pause, so BRF-R054's authorized branch and the prior finding's required correction-loop persistence are never composed or tested.
Required outcome: The transactional proposal-review path must deterministically persist either `correction-loop` with an exact active correction capability and remaining budget or the specified pause route when authority is absent or invalid.
Safe resolution path: Use the shared proposal-review policy projection during finalization, provide it verifier-owned active correction-capability and budget evidence, bind the chosen capability identity into the transition or atomic handoff, and add transactional positive and negative correction-loop tests. Do not keep a second reduced routing implementation in the state writer.
needs-decision rationale: none; BRF-R054 and the accepted BRF-M4-CR6 resolution explicitly require this route.
auto_fix_class: none

## Requirement fidelity

| Requirement property | Result | Evidence |
| --- | --- | --- |
| BRF-R047 complete concrete durable occurrence | block | Empty identities and contradictory occurrence projections validate. |
| BRF-R048-R050 closed outcome, gate, and route vocabularies | concern | Unknown values fail, but impossible combinations of known values pass. |
| BRF-R051-R058 deterministic exact/later routing | block | The transactional writer cannot persist `correction-loop`, and durable consistency is not validated. |
| BRF-R059 proposal-review capability scope | pass | Proposal-review completion remains review-evidence-only. |
| BRF-R060-R061 distinct review and correction passes | pass | Review and correction remain separate stage invocations. |
| BRF-R062 driver-owned deterministic correction | block | Canonical recipe identity is bound but does not govern the actual proposal bytes. |
| BRF-R065 correction divergence and validation pauses | block | Generic identity change accepts a recipe-mismatched mutation; exception mutations are not reconciled. |
| BRF-R066 historical review and rereview authority | pass with concern | Successful regular-file corrections preserve historical review evidence and derive fresh review authority, but only after incomplete correction proof. |
| BRF-R068-R077 receipt and recovery behavior | concern | Prepared receipts and terminalization work, but failed callbacks can leave unrecorded mutations. |
| BRF-R078-R079 stage authority and policy ownership | block | State finalization duplicates and compresses proposal-review routing policy. |
| BRF-R080 and BRF-R087-R090 isolation/external boundaries | concern | Public and legacy routes remain unchanged, but symlink mutations escape the internal capability boundary. |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | BRF-R047, BRF-R054, BRF-R062, BRF-R065, BRF-R078, and BRF-R100 remain incomplete. |
| Test coverage | block | Focused suites omit recipe-result mismatch, symlink mutation, mutate-then-raise, durable cross-field invalidity, and transactional correction-loop. |
| Edge cases | block | Four direct contrast probes falsify the claimed safety boundary. |
| Error handling | block | A callback exception leaves unauthorized mutation behind while the receipt is only marked failed. |
| Architecture boundaries | block | The sole writer duplicates a reduced policy and mutation containment does not cover all repository entries. |
| Compatibility | pass | M4 remains non-public and public/legacy command surfaces are unchanged. |
| Security/privacy | block | Executable correction authority can write bytes beyond its deterministic plan and leave escaped repository mutations. |
| Derived artifact currency | pass | No generated adapter or public skill output changed. |
| Unrelated changes | pass | The implementation diff is scoped to the M4 corrections and lifecycle evidence. |
| Validation evidence | concern | All focused suites passed while direct adversarial probes reproduced four uncovered defects. |

## Validation and direct proof

- `python scripts/test-workflow-automation.py -k proposal_review` passed 4 tests.
- `python scripts/test-workflow-automation.py -k proposal_correction` passed 6 tests.
- `python scripts/test-validate-workflow-automation.py` passed 54 tests.
- `python scripts/test-workflow-automation-state.py` passed 51 tests.
- Direct recipe-mismatch probe completed the transition and receipt.
- Direct symlink-mutation probe left the symlink and completed the transition.
- Direct mutate-then-raise probe left the escaped file and finalized the receipt as failed.
- Direct contradictory review-result probe returned no validation errors.
- Source and transactional-test inspection confirmed that finalization has no correction-loop branch.

## No-finding rationale

Not applicable; this review has four material findings.

## Residual risks

Rereview must prove recipe-specific correction semantics, complete mutation
containment on success and failure, exhaustive durable review-result
consistency, and the transactional correction-loop branch. M5 and M6 remain out
of scope.

## Milestone handoff

- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M4-CR7`, `BRF-M4-CR8`, `BRF-M4-CR9`, and `BRF-M4-CR10`
- Remaining implementation milestones: M4 resolution and rereview, M5, M6
- Next stage: review-resolution M4
- Final closeout readiness: not ready because M4 has four open material findings and M5-M6 remain unimplemented
- Verify readiness: not-claimed
- Isolation: this direct review performs no automatic downstream handoff
