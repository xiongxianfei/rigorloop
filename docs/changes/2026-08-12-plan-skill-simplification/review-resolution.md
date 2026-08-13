# Review Resolution: Plan Skill Simplification

## Summary

Closeout status: closed

Review closeout: proposal-review-r2

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`
- Findings resolved: 6
- Unresolved findings: 0
- Current result: proposal revised and ready for independent rereview

## Resolution overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| `PLSIM-PR1` | accepted | closed | Execution mode is separate from loading; plan owns no review, automation, or continuation evidence. |
| `PLSIM-PR2` | accepted | closed | Stable completion, evidence, and handoff fields remain while mutable progress moves to change-local state. |
| `PLSIM-PR3` | accepted | closed | Procedural profiles and structural assets now have separate deterministic measurement assemblies. |
| `PLSIM-PR4` | accepted | closed | Governed authority and closed create/revise operations are classified independently. |
| `PLSIM-PR5` | accepted | closed | Plan-owned initialization now binds to clean review-settled plan and review identities. |
| `PLSIM-PR6` | accepted | closed | Milestone migration is read-old/write-new with change-local state as sole active authority. |

## Finding details

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
