# Code Review: M4 R3 Canonical Authoring Correction

Review ID: code-review-m4-r3
Stage: code-review
Round: M4 R3
Reviewer: independent blind-review context
Target: M4 correction commit `6404b7b7`
Reviewed artifact: M4 correction commit `6404b7b7`
Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-23
Recording status: recorded
Material findings: BRF-M4-CR5, BRF-M4-CR6
Immediate next stage: review-resolution

Automated review: yes
Review gate outcome: stop
Native review status: changes-requested
Independence level: L2
Reviewer context ID: m3-r5-blind-review-reused-as-m4-r3
Context separation mechanism: A separate existing reviewer context received a neutral packet, recorded the blind-first risk map, and stopped before validation summaries or prior findings were released.
Risk tier: elevated
Risk-tier triggers: Authorization, review independence, durable state, parser ownership, mutation scope, and transaction recovery changed.
Risk-tier classifier: Approved review-independence risk-tier contract.
Governing artifacts: `specs/single-bounded-review-fix-workflow-automation.md`; `specs/single-bounded-review-fix-workflow-automation.test.md`; `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md`; approved workflow architecture and ADR.
Formal criteria: Code-review checklist; BRF-R047-R062, BRF-R068-R080, BRF-R087-R090; M4 T10-T12, T24, T26, and MP1 proof.
Initial packet inventory: scripts/workflow_automation.py@6404b7b7#sha256:cc5d6254197104adc004d037d5bf720c46637c5ea7e44ea98d6653b67036c9e9; scripts/workflow_automation_state.py@6404b7b7#sha256:c0148dfd56966fc87ec7e880b79122529a6a82d13e8c011bca09adf37b89d19b; scripts/validate_workflow_automation.py@6404b7b7#sha256:39ecf9b56468222240b050824dd96de77a6f60f6cbdce555055f02bdf7ec8dd0; specs/single-bounded-review-fix-workflow-automation.md@6404b7b7#sha256:59241a5e4968a0d6ba60f9772eed56ab8b9e79859a0be1c94e7c77840c724070; specs/single-bounded-review-fix-workflow-automation.test.md@6404b7b7#sha256:e73ac1691966e7f17c1d1342b969681ae660b8a283e2f0130078c564a37e21bd; docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md@6404b7b7#sha256:be4f640fcad07ee568f22e52bd93bf2a2581d9b42ccf9aaf47b9ce5e53922c02
Initial packet contains prohibited context: no
Prompt template version: code-review-v1
Initial packet hash: sha256:c274c62dd06f1c797af9358718199a395d2efbb9a98d3b5b9e7d7a6293a37c1f
Manifest owner: workflow orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: `scripts/workflow_automation.py`; `scripts/workflow_automation_state.py`; `scripts/validate_workflow_automation.py`; their changed tests and review evidence
Requirement-fidelity matched path triggers: scripts/*validator*, docs/changes/**/reviews/, docs/changes/**/review-*.md
Requirement-fidelity matched category triggers: autoprogression gates, artifact lifecycle validators, closed enums
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause, property decomposition, production diff, tests, validation evidence, prior findings

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: `BRF-M4-CR5` and `BRF-M4-CR6` block M4 closeout
- Next stage: review-resolution M4
- Review status: changes-requested
- Material findings: `BRF-M4-CR5`, `BRF-M4-CR6`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/code-review-m4-r3.md`
- Review log: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md`
- Review resolution: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md#code-review-m4-r3`
- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4 resolution and rereview, M5, M6
- Required review-resolution: yes
- Finding IDs: `BRF-M4-CR5`, `BRF-M4-CR6`
- Verify readiness: not-claimed

## Review inputs

- Review surface: commit `6404b7b7` against parent `6ebf2ec4`, with production code inspected before changed tests and released validation evidence.
- Tracked governing branch state: commit `6404b7b7`; R3 review evidence was added only after the verdict.
- Governing requirements: BRF-R047-R062, BRF-R068-R080, and BRF-R087-R090.
- Test contract: T10-T12, T24, T26, MP1, and CMD14-CMD20.
- Architecture: stage-owned evidence, sole state writer, prepared receipts, exact effective-capability binding, and capability-stable recovery.
- Prior review and resolution: `code-review-m4-r2.md` and the BRF-M4-CR3/CR4 dispositions, released only after the risk map.

## Blind-first risk map

Affected behavior: Proposal-review occurrence and clean-gate routing; canonical proposal-correction authority; post-correction convergence; non-public authoring progression; stage-native completion and recovery; atomic capability consumption and rereview activation; failure pause and invalidation.

Highest-impact failure modes: Proposal mutation without current driver-owned authority; caller-selected validation or changed paths; stale review reuse; scope expansion during correction; partial or unrecoverable post-mutation state; incomplete review occurrence persistence; premature public reachability.

Changed boundaries: Canonical review parser to correction authority; review log and resolution to effective capability; stage callback to completion verifier; verified facts to routing; post-completion derivation to the sole state writer; mutated proposal to paused state.

Evidence expected: Complete outcome and target matrices; canonical occurrence, classification, budget, path, and validation contrasts; atomic capability handoff proof; post-mutation failure injection; stage-native recovery; public-isolation proof; complete durable proposal-review occurrence assertions.

Areas requiring direct inspection: `evaluate_proposal_review`; `_load_proposal_correction_repository_evidence`; `resolve_proposal_correction_authority`; `evaluate_proposal_correction`; `coordinate_non_public_authoring_stage`; `coordinate_one_stage`; `verify_transition_completion`; `finalize_transition`; correction validation and tests.

Areas intentionally out of scope: M5 implementation and verification integration; M6 public cutover and legacy retirement; generated adapters; PR, release, deployment, merge, credentials, and external actions.

Risk classes considered: Authorization and least privilege; review independence; durable-state atomicity; recovery; filesystem containment and TOCTOU; parser trust; closed vocabularies; scope and budget enforcement; compatibility isolation; auditability.

Falsifiable review questions: Can the wrong review round authorize correction? Can caller classifications or an always-true validator substitute for stage-owned evidence? Can undeclared file mutation survive completion? Is the old review unusable as the new gate? Is fresh authority bounded and atomic? Is the complete proposal-review occurrence/gate/route projection durable? Can any public or isolated route enter the harness?

## Diff summary

The correction makes completed recovery stage-semantic, carries verifier-derived facts into routing, parses current review and resolution evidence, validates persisted correction budgets, reevaluates post-mutation convergence, and atomically consumes correction authority while activating fresh proposal-review authority.

The changed tests add stage-family recovery, budget and classification contrasts, canonical evidence fixtures, post-mutation failure cases, and atomic state transitions.

Two executable gaps remain: correction classification, validation, and changed-path evidence can still be substituted by the caller, and the complete proposal-review occurrence/gate/route record required by BRF-R047 is never persisted.

## Prior-finding reconciliation

| Prior finding | R3 result | Evidence |
| --- | --- | --- |
| `BRF-M4-CR3` | resolved | Completed recovery now compares stage-generic normalized proof, retains review-log drift diagnostics only for formal review proof, and routes from verifier-derived stage facts. |
| `BRF-M4-CR4` | failed-remediation | Post-mutation convergence and capability finalization improved, but exact occurrence, driver classification, deterministic validation, and actual changed paths remain caller-substitutable, as recorded in `BRF-M4-CR5`. |

## Findings

## Finding BRF-M4-CR5

Finding ID: BRF-M4-CR5
Severity: major
Location: `scripts/workflow_automation.py:456-589`, `scripts/workflow_automation.py:805-904`, `scripts/test-workflow-automation.py:139-206`, `scripts/test-workflow-automation.py:1962-2005`
Evidence: Canonical review-log matching checks review ID, stage, status, and path but omits the review round and material-finding parity; changing `Round: r1` to `r2` still returns correction authority. Persisted classifications are checked only against their own hash and are not compared with driver-owned classification evidence in `review-resolution.md`; the positive resolution fixture contains no driver classification while a separately persisted `mechanical` value authorizes correction. Deterministic validation is an unbound caller callback, and an always-true callback completes correction and activates rereview authority. A caller also supplies `affected_paths`; a direct probe mutated an undeclared file outside the proposal scope while reporting only the proposal path, and the receipt still completed. The positive correction callback edits `review-resolution.md` and `review-log.md` even though the proposal-correction policy permits only `proposal-content`.
Required outcome: Correction must derive the exact review occurrence, driver classification, deterministic validation, and complete changed-path set from current stage-owned evidence. No mutation outside the effective capability may occur.
Safe resolution path: Require exact review round plus review-log material/open-finding parity; bind driver classification and its rationale or recipe to canonical review-resolution evidence; replace the arbitrary validator callback with named identity-bound validation evidence; compare actual repository changes with capability roots and mutation categories; and move review-log or resolution mutation into separately authorized stage work.
needs-decision rationale: none; the approved authority, stage-ownership, and mutation-scope contracts already require fail-closed correction.
auto_fix_class: none

## Finding BRF-M4-CR6

Finding ID: BRF-M4-CR6
Severity: major
Location: `scripts/workflow_automation_state.py:487-493`, `scripts/workflow_automation.py:701-761`, `scripts/workflow_automation.py:919-939`, `scripts/validate_workflow_automation.py:732-775`; coverage gap in `scripts/test-workflow-automation.py`
Evidence: BRF-R047 requires a proposal-review occurrence to record review ID, reviewed proposal identity, outcome, occurrence-recorded state, clean-gate state, routing action, and pause reason when applicable. Verified completion facts contain only review ID and outcome. The route helper substitutes placeholder review ID and proposal identity, the composed result carries only generic route status, next stage, and pause reason, and the coordinator never writes the validator-supported `workflow.automation.latest_review_result`. Transactional tests assert route status and verified outcome but not the complete durable occurrence projection.
Required outcome: Atomically persist the complete verifier-derived BRF-R047 occurrence, gate, and routing projection for the actual structured target. Exact-target, correction-loop, blocked, and inconclusive paths must retain their gate and pause state durably.
Safe resolution path: Derive the complete proposal-review result from `VerifiedCompletion` and the bound target, persist it through the sole writer with receipt finalization or another atomic transition, remove placeholder identities, and add transactional four-outcome exact-versus-later assertions.
needs-decision rationale: none; BRF-R047 and the existing durable result schema determine the required shape.
auto_fix_class: none

## Requirement fidelity

| Requirement property | Result | Evidence |
| --- | --- | --- |
| BRF-R047 complete durable review occurrence, gate, route, and pause record | block | The coordinator never persists `latest_review_result`; verified facts and route output omit required fields. |
| BRF-R048-R050 closed outcome, gate, and routing vocabularies | pass | Closed values remain validated and helper-level matrices reject unknown values. |
| BRF-R051-R058 approval, exact-target, blocked, inconclusive, and stale-review routing | concern | Helper-level decisions route correctly, but the required durable state is incomplete. |
| BRF-R059 review capability excludes proposal mutation | pass | Proposal-review completion remains review-evidence-only. |
| BRF-R060-R061 distinct review and mutation ownership | block | Proposal correction mutates review evidence under proposal-content-only authority. |
| BRF-R062 driver-owned deterministic correction | block | Classification, validation, and changed-path evidence remain caller-selected. |
| BRF-R068-R077 receipt and recovery behavior | pass | The previously defective M4 stage families now recover from current normalized proof. |
| BRF-R078-R079 stage-owned authority and policy scope | block | Caller-supplied validation and undeclared mutation bypass stage-owned scope. |
| BRF-R080 and BRF-R087-R090 internal-only routing and external boundary | pass | Public and legacy routes remain unchanged; no external action surface changed. |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | BRF-R047, BRF-R060-R062, and BRF-R078 remain incomplete. |
| Test coverage | block | The suites omit wrong-round, canonical driver-classification, always-true validator, undeclared mutation, and durable occurrence assertions. |
| Edge cases | block | Direct counterexamples pass through the current correction boundary. |
| Error handling | concern | Post-mutation failures pause, but caller-selected evidence can prevent the failure from being detected. |
| Architecture boundaries | block | Stage-owned evidence and correction mutation categories are bypassed. |
| Compatibility | pass | M4 remains non-public and legacy behavior is unchanged. |
| Security/privacy | block | Executable correction authority and mutation scope remain substitutable. |
| Derived artifact currency | pass | No generated or public adapter output changed. |
| Unrelated changes | pass | The diff is scoped to M4 runtime, tests, and required lifecycle evidence. |
| Validation evidence | concern | Reported and rerun suites pass despite direct counterexamples. |

## Validation and direct proof

- Independently reran CMD15-CMD20: 3 proposal-review, 4 proposal-correction, 4 authoring, 4 non-public, 103 review-artifact, and 259 skill-validator tests passed.
- Independently reran 51 state/recovery and 54 automation-validator tests.
- Completed-recovery and identity-stable-routing focused cases passed.
- Direct wrong-round correction evidence still returned executable authority.
- Direct always-true validation completed correction and activated rereview authority.
- Direct undeclared mutation outside proposal scope survived completion.
- The released 12-check broad-smoke result was challenged but not independently rerun.
- `git diff --check 6ebf2ec4..6404b7b7` passed.

## No-finding rationale

Not applicable; this review has two material findings.

## Residual risks

Rereview should prove exact occurrence parity, repository-owned classification and validation evidence, complete mutation-set containment, atomic durable review-result recording, and all four proposal-review outcomes through the composed transactional path. M5 and M6 remain out of scope.

## Milestone handoff

- Reviewed milestone: M4. Authoring, Proposal Review, and Correction Integration
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `BRF-M4-CR5` and `BRF-M4-CR6`
- Remaining implementation milestones: M4 resolution and rereview, M5, M6
- Next stage: review-resolution M4
- Final closeout readiness: not ready because M4 has two open material findings and M5-M6 remain unimplemented
- Verify readiness: not-claimed
