# Review Resolution: Plan Skill Simplification

## Summary

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: proposal-review-r3
Review closeout: proposal-review-r4
Review closeout: spec-review-r1
Review closeout: architecture-review-r1
Review closeout: spec-review-r2
Review closeout: plan-review-r1
Review closeout: test-spec-review-r1
Review closeout: code-review-m1-r1
Review closeout: code-review-m2-r1
Review closeout: code-review-m2-r2
Review closeout: code-review-m3-r1
Review closeout: code-review-final-r1
Review closeout: code-review-final-r2

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `proposal-review-r3`, `proposal-review-r4`
- Findings resolved: 11
- Unresolved findings: 0
- Current result: M2 implementation approved

## Resolution overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| `PLSIM-PR1` | accepted | closed | Execution mode is separate from loading; plan owns no review, automation, or continuation evidence. |
| `PLSIM-PR2` | accepted | closed | Stable completion, evidence, and handoff fields remain while mutable progress moves to change-local state. |
| `PLSIM-PR3` | accepted | closed | Procedural profiles and structural assets now have separate deterministic measurement assemblies. |
| `PLSIM-PR4` | accepted | closed | Governed authority and closed create/revise operations are classified independently. |
| `PLSIM-PR5` | accepted | closed | Plan-owned initialization now binds to clean review-settled plan and review identities. |
| `PLSIM-PR6` | accepted | closed | Milestone migration is read-old/write-new with change-local state as sole active authority. |
| `PLSIM-PR7` | accepted | closed | Clean review evidence, plan-owned initialization, and identical settlement retry now form one closed transaction. |
| `PLSIM-PR8` | accepted | closed | Stable artifact metadata and existing review revision evidence define identity without hashes. |
| `PLSIM-PR9` | accepted | closed | Canonical architecture updates and a narrow successor ADR are required in this change. |
| `PLSIM-CR1` | accepted | closed | Exact stable-artifact and reviewed-revision identity fields were restored without losing profile reduction. |
| `PLSIM-CR2` | accepted | closed | The invalid-ledger proof now covers vocabulary ordering, duplicates, missing fields, and destination consistency. |

## Finding details

### code-review-final-r2

No material findings. The focused final rereview approved eight exact owner deferrals, retained direct proof, unchanged selector policy, and refreshed rationale.

### code-review-final-r1

No material findings. The final holistic review approved the coherent M1-M3 implementation, closed review history, semantic preservation, and complete package proof.

### code-review-m3-r1

No material findings. The clean milestone review approved the profile measurements, semantic preservation evidence, boundary proof, and canonical-through-installed package parity.

### code-review-m2-r2

No material findings. The clean rereview confirmed both M2 findings are closed, both procedural profiles remain below baseline, and the complete skill suite passes.

### code-review-m1-r1

No material findings. The clean milestone review approved the evidence-first initialization, state-authority migration, compatibility boundary, and direct deterministic proof.

### architecture-review-r1

No material findings. The clean review approved the canonical architecture update and accepted the successor ADR.

### spec-review-r2

No material findings. The clean rereview approved the corrected example ownership metadata without changing the feature contract.

### plan-review-r1

No material findings. The clean review approved the three-milestone execution plan and its explicit bootstrap compatibility boundary.

### test-spec-review-r1

No material findings. The clean review approved the complete deterministic proof map and allowed implementation handoff without starting implementation.

### spec-review-r1

No material findings. The clean review approved `specs/plan-skill-simplification.md` and routed to required architecture work.

### proposal-review-r4

No material findings. The clean rereview approved the proposal at commit `996f1517` and confirmed closure of `PLSIM-PR7`, `PLSIM-PR8`, and `PLSIM-PR9`.

### proposal-review-r1

#### PLSIM-PR1

Finding ID: PLSIM-PR1
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close the execution-authority and cross-stage ownership model.
Chosen action: Separate execution authority from resource loading and restrict the governed reference to plan-owned authoring through the review-required handoff.
Rationale: The package shape remains viable, but plan must not own automation receipts or plan-review completion behavior.
Required outcome: Restrict the governed reference to plan-owned authoring and normal review-required handoff.
Safe resolution path: Adopt the authority correction in `proposal-review-r1` and validate it with static manual and automated scenarios.
Validation target: revised reference ownership, execution-authority, handoff, and acceptance sections plus independent proposal rereview.
Validation evidence: `evidence/proposal-revision-r1.md`; revised Invocation classification, Governed reference ownership, Expected Behavior Changes, Testing and Verification Strategy, and Decision Log sections.

#### PLSIM-PR2

Finding ID: PLSIM-PR2
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Define stable milestone completion structure without mutable progress.
Chosen action: Retain stable completion criteria, required evidence, review handoff, and milestone kind while removing mutable state and execution-progress fields.
Rationale: Mutable state must leave the plan, but stable completion, proof, and review handoff criteria must remain explicit.
Required outcome: Close the replacement milestone field groups and lifecycle-closeout distinction.
Safe resolution path: Adopt the stable completion group recommended by `proposal-review-r1` and reconcile it with the existing asset contract.
Validation target: revised asset ownership, migration, parity, and static fixture sections plus independent proposal rereview.
Validation evidence: `evidence/proposal-revision-r1.md`; revised Asset ownership and milestone-state migration, Expected Behavior Changes, Testing and Verification Strategy, Risks and Mitigations, and Decision Log sections.

#### PLSIM-PR3

Finding ID: PLSIM-PR3
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Define deterministic procedural profile and asset measurement assemblies.
Chosen action: Measure exact procedural assemblies without assets and report assets through fixed separate structural measurements.
Rationale: Variable asset applicability and milestone counts currently make the primary reduction gate non-repeatable.
Required outcome: Separate reference-loaded context from output-structure resource measurements.
Safe resolution path: Adopt the measurement convention recommended by `proposal-review-r1`.
Validation target: revised profile, measurement, acceptance, and evidence sections plus independent proposal rereview.
Validation evidence: `evidence/proposal-revision-r1.md`; revised Invocation classification, Simplification measurement, Testing and Verification Strategy, Risks and Mitigations, and Decision Log sections.

### proposal-review-r2

#### PLSIM-PR4

Finding ID: PLSIM-PR4
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Separate governed change authority from plan artifact existence and operation.
Chosen action: Separate governed authority from create/revise operation and close file, entry, path, identity, conflict, and creation order.
Rationale: A new governed plan cannot require the identity it is meant to create.
Required outcome: Close create, revise, asymmetry, mismatch, and ambiguity behavior.
Safe resolution path: Adopt the operation model in `proposal-review-r2` and validate it through static fixtures.
Validation target: revised classification, governed procedure, failure, and acceptance sections plus independent rereview.
Validation evidence: `evidence/proposal-revision-r2.md`; revised Invocation classification, Governed reference ownership, Testing and Verification Strategy, Risks and Mitigations, and Decision Log sections.

#### PLSIM-PR5

Finding ID: PLSIM-PR5
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Settle when and from which identity live `planned_work` is initialized.
Chosen action: Move initialization after clean plan-review settlement, bind it to approved identities, and route later baseline changes to governed replan or migration.
Rationale: Pre-review initialization and immutable later state conflict with review-driven revisions.
Required outcome: Bind initialization to approved plan and review evidence and define later replan behavior.
Safe resolution path: Adopt post-approval initialization and direct contract amendment.
Validation target: revised lifecycle ownership, initialization, replan, testing, and rollout sections plus independent rereview.
Validation evidence: `evidence/proposal-revision-r2.md`; revised Context, Universal ownership, Governed reference ownership, Plan baseline settlement and replan, Expected Behavior Changes, Rollout and Rollback, and Decision Log sections.

#### PLSIM-PR6

Finding ID: PLSIM-PR6
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Define old/new milestone-format activation, precedence, and migration failures.
Chosen action: Adopt lifecycle-marker-based read-old/write-new compatibility, preserve historical plans, and block incomplete or conflicting active legacy state.
Rationale: Current consumers cannot migrate safely without a read-old/write-new boundary.
Required outcome: Close writer, reader, authority, active legacy, historical, conflict, and reverse-synchronization behavior.
Safe resolution path: Adopt the compatibility matrix in `proposal-review-r2`.
Validation target: revised compatibility, parser migration, rollout, rollback, and fixture sections plus independent rereview.
Validation evidence: `evidence/proposal-revision-r2.md`; revised Asset ownership, Milestone-format compatibility, Testing and Verification Strategy, Rollout and Rollback, Risks and Mitigations, and Decision Log sections.

### proposal-review-r3

#### PLSIM-PR7

Finding ID: PLSIM-PR7
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Define the evidence-first initialization and settlement transaction.
Chosen action: Add `initialize-approved-plan`, legal temporary states, clean evidence before initialization, and identical settlement retry without rerunning judgment.
Rationale: The current primary-plan/planned-work invariant does not permit the proposed intermediate states.
Required outcome: Close legal combinations, invocation ownership, retry, failure, and routing behavior.
Safe resolution path: Adopt the two-phase review evidence, plan initialization, and settlement retry model in `proposal-review-r3`.
Validation target: revised state sequence, schema amendment, direct/workflow-managed behavior, failure, and tests plus independent rereview.
Validation evidence: `evidence/proposal-revision-r3.md`; revised Invocation classification, Governed reference ownership, Architecture Impact, Testing and Verification Strategy, Rollout and Rollback, Risks and Mitigations, and Decision Log sections.

#### PLSIM-PR8

Finding ID: PLSIM-PR8
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Select the stable artifact and reviewed revision identity model.
Chosen action: Use the stable artifact tuple and durable review revision evidence, with no governed-document hash or `content_identity` field.
Rationale: The proposal's undefined content identity could silently introduce a rejected hash or schema field.
Required outcome: Define identity through existing artifact and review evidence or explicitly amend architecture.
Safe resolution path: Use artifact ID/kind/role/path plus review record and reviewed commit, without a new content hash.
Validation target: revised creation, revision, initialization, compatibility, and architecture sections plus independent rereview.
Validation evidence: `evidence/proposal-revision-r3.md`; revised Invocation classification, Governed reference ownership, Architecture Impact, Testing and Verification Strategy, Risks and Mitigations, and Decision Log sections.

#### PLSIM-PR9

Finding ID: PLSIM-PR9
Disposition: accepted
Status: closed
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Correct the architecture disposition for the selected lifecycle-order change.
Chosen action: Require canonical architecture updates and a narrow successor ADR while preserving mutable architecture assessment status and pointers in the owning change record.
Rationale: Current architecture and ADR text explicitly owns the ordering and no-hash decision being changed or relied upon.
Required outcome: Require canonical architecture and ADR amendment or successor work.
Safe resolution path: Replace `architecture-not-required` expectation with architecture-update-required and enumerate affected decision surfaces.
Validation target: revised Architecture Impact, scope budget, rollout, and decision log plus independent rereview.
Validation evidence: `evidence/proposal-revision-r3.md`; revised Scope Budget, Architecture Impact, Testing and Verification Strategy, Rollout and Rollback, Risks and Mitigations, Next Artifacts, and Decision Log sections.

### code-review-m2-r1

#### PLSIM-CR1

Finding ID: PLSIM-CR1
Disposition: accepted
Status: closed
Owner: implement
Owning stage: implement
Decision owner: implement
Decision needed: Restore deterministic identity fields removed by over-compression.
Chosen action: Name the stable artifact and reviewed revision tuples explicitly in the governed reference.
Rationale: Governed procedure must remain executable without inferring mandatory identity fields.
Required outcome: Exact approved identity fields remain explicit while both loaded profiles stay below baseline.
Safe resolution path: Amend the reference, measure profiles, rerun CMD6-CMD9, and rereview.
Validation target: PSIM-R011, PSIM-R012, T7, T8, and profile evidence.
Validation evidence: `skills/plan/references/governed-plan-authoring.md` names both exact approved identity tuples; `evidence/m2-plan-package.md` records reduced PL0 and PL1 profiles; CMD6-CMD9 passed after correction.

#### PLSIM-CR2

Finding ID: PLSIM-CR2
Disposition: accepted
Status: closed
Owner: implement
Owning stage: implement
Decision owner: implement
Decision needed: Complete the deterministic invalid-ledger proof required by T7.
Chosen action: Add a change-local validation helper and fixtures for unknown-first, duplicate-ID, missing-field, and inconsistent-destination failures.
Rationale: Asserting that two values are outside local sets does not exercise the required failure path or validation order.
Required outcome: Every named invalid fixture fails for its intended reason and unknown vocabulary is checked before consistency.
Safe resolution path: Extend the existing focused test without adding a permanent validator family.
Validation target: T7 and CMD7.
Validation evidence: Five invalid fixtures exercise unknown dispositions, unknown classifications, duplicate IDs, missing fields, and inconsistent destinations through `_validate_ledger`; CMD7 passed with 317 tests and 16 skips.
