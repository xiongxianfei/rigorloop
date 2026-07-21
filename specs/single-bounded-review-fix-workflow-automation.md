# Single Bounded Review-Fix Workflow Automation

## Status

approved

## Related proposal

- [Single Bounded Review-Fix Workflow Automation Mechanism](../docs/proposals/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism.md)
- [Approved proposal-review R4](../docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/proposal-review-r4.md)

This spec amends the automation behavior described by:

- [RigorLoop Workflow](rigorloop-workflow.md);
- [Workflow Stage Autoprogression](workflow-stage-autoprogression.md);
- [Review-Fix Autoprogression](review-fix-autoprogression.md);
- [Review Finding Resolution Contract](review-finding-resolution-contract.md).

Those specs retain ownership of unrelated workflow ordering, manual-invocation isolation, review-record shape, finding completeness, correction classification, and verification behavior.

### Normative ownership

This spec is the sole normative owner of persisted workflow-automation mechanisms, commands, targets, run state, authorization, effective capabilities, automatic transition recovery, and legacy automation adapters after approval.

| Contract | Retained normative ownership |
| --- | --- |
| This spec | All writable workflow automation and compatibility projection into that automation. |
| `specs/workflow-stage-autoprogression.md` | General lifecycle continuation and stage ordering that does not define a separately writable automation mechanism. |
| `specs/rigorloop-workflow.md` | Repository lifecycle, artifact ordering, canonical workflow-state ownership, and isolated or manual workflow behavior. |
| `specs/review-finding-resolution-contract.md` | Reviewer-owned finding classification, finding completeness, and review-resolution semantics. |
| `specs/review-fix-autoprogression.md` | Historical compatibility meaning only after this spec is approved; no independent live authority. |

Historical automation requirements remain readable through the closed disposition registry in this spec.
They are not parallel normative implementations.

## Goal and context

RigorLoop currently exposes three separately persisted workflow automation mechanisms.
This spec replaces new writes to those mechanisms with one target-driven `bounded-review-fix` mechanism while preserving their safety boundaries.

The contract separates the user's requested target from executable authority.
It also separates durable maximum consent from a stage-specific capability, recorded review occurrence from clean-gate satisfaction, automation evidence from canonical workflow position, and workflow automation from external actions.

## Glossary

- `bounded-review-fix`: the only mechanism identifier permitted for newly authorized workflow automation runs.
- `automation run`: the durable change-local record that coordinates one requested structured target, its authorizations, effective capabilities, receipts, and status.
- `structured target`: the requested stopping boundary expressed as stage, occurrence, binding identity, and completion predicate.
- `bounded parent authorization`: durable user consent defining the maximum authority available inside one risk class; it is not executable mutation authority.
- `effective capability`: executable authority for one stage occurrence, derived from one active parent authorization and bound to current stage-appropriate evidence.
- `stage-appropriate basis`: the artifact, review, plan, command, workflow-state, or other identities required by the stage policy at the time a capability is derived.
- `authorization class`: one of `authoring`, `implementation`, or `verification`.
- `capability kind`: a closed stage-policy value identifying the operation an effective capability may execute.
- `canonical workflow position`: the current workflow position derived from authoritative artifacts before a plan exists and owned by the active plan after the ownership handoff.
- `transition receipt`: a write-ahead record for one attempted automatic stage transition.
- `review occurrence`: durable evidence that one formal review ran against one exact artifact identity and produced one closed outcome.
- `clean gate`: the approval fact that permits downstream reliance on a reviewed artifact.
- `legacy automation record`: an existing `authoring-through-plan-review`, legacy `bounded-review-fix`, or `implementation-through-verify` record created before cutover.
- `external action`: PR opening, push, publication, release, deployment, merge, destructive Git operation, or another mutation outside the repository-local workflow artifacts authorized by this spec.
- `lifecycle continuation`: entry into an already-mandatory adjacent workflow stage without a persisted automation run; it remains governed by the general workflow contracts and is not a second writable automation mechanism.

## Examples first

### Example E1: proposal review before proposal approval

Given a tracked proposal has status `under review`
And an active authoring parent authorization permits `proposal-review`
When the engine derives a proposal-review capability from the exact proposal identity
Then it may invoke `proposal-review` and write change-local review evidence
And it may not edit the proposal or create downstream authoring artifacts under that capability.

### Example E2: later target pauses at a risk boundary

Given a run targets final `verify`
And it has active authoring authority but no implementation authorization
When authoring stages through approved `test-spec-review` complete
Then the run pauses before implementation
And it reports the missing implementation authorization without changing the target.

### Example E3: proposal findings enter bounded correction

Given proposal review records `changes-requested`
And the parent authorization permits proposal correction
And the findings are deterministically eligible and inside the remaining budget
When the engine derives a correction capability
Then it applies only the accepted bounded corrections
And it invalidates the prior review as gate evidence after the proposal identity changes
And it derives a new proposal-review capability before rereview.

### Example E4: inconclusive review pauses

Given proposal review records `inconclusive` against the current proposal identity
When the review occurrence is persisted
Then the clean gate is `not-satisfied`
And the run pauses with reason `proposal-review-inconclusive`
And it does not rerun the review until material evidence changes.

### Example E5: milestone target remains bound

Given the structured target is `code-review@M2`
When M2 implementation and its required validation complete
Then the run invokes milestone-local code review for M2
And target completion cannot silently rebind to M3 after interruption or resume.

### Example E6: interrupted transition reconciles

Given a prepared receipt exists for `implement@M2`
And the stage completed its authoritative outputs before receipt finalization was interrupted
When the run resumes
Then it reconciles the completion evidence and canonical plan state
And it does not rerun implementation.

### Example E7: active legacy state migrates once

Given an active `implementation-through-verify` record exists at cutover
When the user explicitly authorizes a mutating resume
Then the system writes one unified run and one migration receipt
And the legacy record becomes read-only for that change.

### Example E8: direct review remains isolated

Given no workflow automation command or workflow-managed continuation context exists
When the user directly invokes `proposal-review`
Then the review records its formal evidence
And it does not create, resume, or advance an automation run.

### Example E9: repeated target binds before persistence

Given the active plan identifies M2 as the unique current in-scope implementation milestone
When the user runs `$workflow auto: code-review`
Then the engine persists `code-review@M2` with the current plan identity
And resume never rebinds that target to M3.

### Example E10: cancellation has one durable result

Given an active run has active parent authorizations and effective capabilities
When the user runs `$workflow auto: off`
Then the run becomes `cancelled`
And active parents become `revoked`
And active capabilities become `invalidated`
And prior receipts and evidence remain durable.

### Example E11: verify target precedes verification consent

Given planning and test-spec gates are approved but implementation is not complete
When the user selects final `verify` as the target
Then the target may be persisted
And verification authorization remains absent
And the run pauses with `verification-authorization-required` when it reaches that boundary.

### Example E12: legacy verify alias uses the unified writer

Given implementation basis is concrete but verification basis does not yet exist
When the user runs `workflow auto-through: verify`
Then the adapter persists a unified final `verify` target and implementation authorization only
And it writes no legacy profile state
And later pauses before verification authorization is required.

## Requirements

### Mechanism and command contract

BRF-R001. Newly authorized workflow automation MUST persist exactly one writable mechanism value: `bounded-review-fix`.

BRF-R002. Newly authorized automation MUST persist under the neutral `workflow.automation` namespace rather than creating new `workflow.autoprogression` profile state.

BRF-R003. A change MUST have at most one active writable automation run.

BRF-R003a. After this spec is approved, it MUST be the sole normative owner of persisted workflow-automation mechanisms and automatic execution authority.

BRF-R003b. General lifecycle and finding-resolution specs MAY retain stage ordering, isolation, review, classification, and evidence contracts, but MUST reference this spec rather than define another writable automation mechanism.

BRF-R003c. A fully retired automation spec MUST identify this spec as its `superseded_by` target and MUST NOT remain a current authority for execution or writes.

BRF-R003d. General workflow-managed lifecycle continuation without a persisted automation run MUST remain governed by the lifecycle specs and MUST NOT create mechanism, run, parent-authorization, capability, or receipt state by implication.

BRF-R004. The system MUST support `$workflow auto: <target-stage>`, `$workflow auto: status`, and `$workflow auto: off` as public command forms for the unified mechanism.

BRF-R005. Existing supported public aliases MUST remain compatibility adapters throughout the migration window, and every alias MUST resolve to the structured target and risk-scoped authorization result defined by this spec before new state is persisted.

BRF-R006. `$workflow auto: status` MUST be read-only and report the current target, authorization boundary, canonical position source, in-flight transition, pause or stop reason, and latest evidence identities.

BRF-R007. `$workflow auto: off` MUST durably produce terminal `run.status: cancelled` before reporting cancellation complete.

BRF-R007a. Cancellation MUST stop scheduling new transitions and, when a prepared transition exists, reconcile stage-owned evidence before finalizing cancellation.

BRF-R007b. Cancellation MUST revoke every active parent authorization with reason `run-cancelled`, invalidate every active effective capability with reason `parent-revoked`, and preserve all prior receipts and evidence.

BRF-R007c. `off` on a cancelled run MUST be an idempotent no-op that reports `cancelled`; `off` with no active run MUST perform no mutation and report `no-active-run`; and `off` on a completed run MUST perform no mutation and report `already-completed`.

BRF-R008. Unknown mechanism, command, target, status, authorization class, capability kind, occurrence kind, review outcome, receipt status, retry policy, or policy version MUST fail closed before mutation.

### Durable-state vocabularies

BRF-R008a. Automation-run status MUST be closed to `active`, `paused`, `completed`, and `cancelled`.

BRF-R008b. A new run MUST enter `active`; `active` MAY transition only to `paused`, `completed`, or `cancelled`; `paused` MAY transition only to `active` or `cancelled`; and `completed` and `cancelled` MUST be terminal.

BRF-R008c. Resuming a terminal run MUST fail closed; a new target after terminal completion or cancellation MUST use a new run ID.

BRF-R008d. Parent-authorization status MUST be closed to `active`, `revoked`, and `invalidated`; a new parent MUST enter `active`; and an active parent MAY transition only to terminal `revoked` or terminal `invalidated`.

BRF-R008e. Effective-capability status MUST be closed to `active`, `consumed`, and `invalidated`; a derived capability MUST enter `active`; and an active capability MAY transition only to terminal `consumed` or terminal `invalidated`.

BRF-R008f. Pause MUST be represented only by `run.status: paused`; parent authorizations and effective capabilities MUST NOT use a paused status.

BRF-R008g. Capability kind MUST be closed to `proposal-review`, `proposal-correction`, `post-proposal-authoring`, `implementation`, `implementation-correction`, and `verification`.

BRF-R008h. `proposal-review` MUST bind to proposal review; `proposal-correction` to eligible proposal correction and rereview preparation; `post-proposal-authoring` to `spec` through `test-spec-review` including architecture assessment; `implementation` to implementation, milestone review, final holistic review, and in-scope CI maintenance; `implementation-correction` to eligible code-review correction; and `verification` to `explain-change` and `verify`.

BRF-R008i. Unknown values and transitions absent from these tables MUST fail closed before mutation.

BRF-R008j. A capability MUST become `consumed` only after its bound stage operation completes and the transition receipt is finalized, and a consumed capability MUST NOT authorize another invocation.

### Structured target

BRF-R009. A persisted target MUST contain a closed stage, occurrence identity, binding time, and completion predicate.

BRF-R010. Public target stages MUST be closed to `proposal-review`, `spec`, `spec-review`, `architecture`, `architecture-review`, `plan`, `plan-review`, `test-spec`, `test-spec-review`, `implement`, `code-review`, and `verify`.

BRF-R011. Target occurrence kinds MUST be closed to `singleton`, `milestone`, and `final`.

BRF-R012. `implement` and `code-review` targets MUST bind a milestone ID when their occurrence kind is `milestone`.

BRF-R013. A resumed target MUST retain its original occurrence identity and MUST NOT silently bind to a later milestone or review.

BRF-R014. A requested target MUST NOT imply authorization to cross an intervening risk-class boundary.

BRF-R015. Reaching a target MUST NOT skip its prerequisites, formal reviews, required review resolution, or canonical-state synchronization.

BRF-R016. When architecture is not required, a later target MUST record architecture as `not-applicable` and continue, while an explicit `architecture` or `architecture-review` target MUST stop with `target-not-applicable`.

BRF-R017. Ambiguous architecture applicability MUST pause for owner decision.

### Stage-to-occurrence compatibility

BRF-R017a. Every public target stage MUST resolve to exactly one permitted occurrence kind and completion predicate before automation-run or authorization state is persisted.

| Public target | Required occurrence | Additional identity | Completion predicate |
| --- | --- | --- | --- |
| `proposal-review` | `singleton` | none | Formal review occurrence recorded for the bound proposal identity. |
| `spec` | `singleton` | none | Spec artifact reaches its required authored state. |
| `spec-review` | `singleton` | none | Formal spec-review occurrence recorded; only approval satisfies its clean gate. |
| `architecture` | `singleton` | none | Required architecture artifact completes, or the explicit target returns `target-not-applicable`. |
| `architecture-review` | `singleton` | none | Required review occurrence completes, or the explicit target returns `target-not-applicable`. |
| `plan` | `singleton` | none | Valid active plan with `Current Handoff Summary` is established. |
| `plan-review` | `singleton` | none | Formal plan-review occurrence is recorded; only approval satisfies its clean gate. |
| `test-spec` | `singleton` | none | Active test spec exists against current upstream identities. |
| `test-spec-review` | `singleton` | none | Formal review occurrence is recorded; only approval permits implementation handoff. |
| `implement` | `milestone` | `milestone_id`, plan identity | Bound implementation exists, required validation passes, and plan state is `review-requested`. |
| `code-review` | `milestone` | `milestone_id`, plan identity | Bound review is approved, required resolution is closed, and the plan closes or advances the milestone. |
| `verify` | `final` | none | All milestones and final-review obligations are closed, explanation is current, and fresh verification passes. |

BRF-R017b. `$workflow auto: implement` and `$workflow auto: code-review` MUST require a structurally valid active plan and MUST bind the unique current nonterminal in-scope implementation milestone from its authoritative `Current Handoff Summary`.

BRF-R017c. Repeated-stage target persistence MUST include the milestone ID and current plan identity.

BRF-R017d. A missing active plan, missing current milestone, terminal or out-of-scope milestone, or more than one plausible milestone MUST prevent target and authorization persistence and MUST report an exact binding diagnostic.

BRF-R017e. `implement` or `code-review` with `singleton` or `final`, `verify` with `singleton` or `milestone`, and any singleton stage with `milestone` or `final` MUST fail closed before persistence.

BRF-R017f. Ambiguous repeated-stage binding MUST report `cannot bind <stage> target: active plan does not identify exactly one current in-scope implementation milestone`, substituting the requested stage without changing the rest of the diagnostic.

### Canonical workflow position

BRF-R018. Before a valid active plan exists, the engine MUST derive workflow position from authoritative artifact existence and status, current formal reviews, review-resolution state, architecture applicability, and the closed transition registry.

BRF-R019. Multiple plausible pre-plan positions, stale review evidence, or contradictory artifact identities MUST pause the run.

BRF-R020. Once a structurally valid active plan with a valid `Current Handoff Summary` exists, that summary MUST own current milestone, milestone state, review state, remaining milestones, next stage, and final-closeout readiness.

BRF-R021. The plan-creation transition MUST record the pre-plan evidence identities and validated plan identity that establish the ownership handoff.

BRF-R022. Automation metadata MUST NOT persist an independent authoritative `current_stage` or `next_stage` cursor.

BRF-R023. A mismatch between automation-observed identities and canonical workflow state MUST pause before another transition.

### Bounded parent authorization

BRF-R024. A bounded parent authorization MUST record authorization ID, authorization class, policy version, change ID, authorizer, authorization time, maximum structured target, allowed capability kinds, maximum path roots, maximum mutation categories, applicable correction budget, status, revocation state, and invalidation behavior.

BRF-R025. Parent authorization classes MUST be closed to `authoring`, `implementation`, and `verification`.

BRF-R026. A parent authorization MUST define maximum consent only and MUST NOT directly authorize stage execution or mutation.

BRF-R027. Authoring authorization MUST NOT imply implementation or verification authorization.

BRF-R028. Implementation authorization MUST NOT imply verification authorization.

BRF-R029. External actions MUST be represented as `prohibited` and MUST NOT be a grantable authorization class under this spec.

BRF-R030. User revocation, cancellation, supersession, change-identity mismatch, scope narrowing, or incompatible policy change MUST pause or invalidate all effective capabilities derived from the affected parent authorization.

BRF-R031. A parent authorization alone attempting execution or mutation MUST fail closed.

### Effective capability

BRF-R032. Only an active effective capability MAY authorize one concrete stage occurrence.

BRF-R033. Every effective capability MUST record capability ID, capability kind, parent authorization ID, policy version, change ID, stage and occurrence, stage-appropriate basis identities, actual path and mutation scope, derivation time, status, and invalidation behavior.

BRF-R034. An effective capability MUST derive from one existing active non-revoked parent authorization with a compatible policy version.

BRF-R035. A capability kind, stage occurrence, target, path root, mutation category, correction budget, and risk class MUST be a subset of its parent authorization.

BRF-R036. A capability missing its parent, using a stale parent identity, exceeding parent scope, or crossing authorization class MUST fail closed.

BRF-R037. A capability basis MUST contain every identity required by its stage policy and MUST be current when the transition begins.

BRF-R038. Review identities MUST be required only when the stage-policy basis can legitimately require an existing review.

BRF-R039. Proposal-review capability basis MUST include the exact proposal identity, standing-gate identity, review-policy identity, structured target, and review-evidence roots; it MUST NOT require an earlier proposal-review identity.

BRF-R040. Proposal-correction capability basis MUST include the exact reviewed proposal identity, review record, bounded accepted finding set, classifier policy, correction budget, and affected proposal roots.

BRF-R041. Post-proposal authoring capability basis MUST include the exact proposal identity, latest approved applicable proposal-review identity, closed required review resolution, and concrete stage scope.

BRF-R042. Implementation capability basis MUST include the approved plan and plan-review identities, active test spec and approved test-spec-review identities, milestone occurrence, affected paths, mutation categories, and validation-command identity.

BRF-R043. Verification capability basis MUST include closed implementation milestones, clean final holistic code-review identity, valid promotion evidence, current explanation inputs, and concrete branch-state verification inputs.

BRF-R043a. A run MAY persist a final `verify` target before verification authorization exists; that target MUST NOT be interpreted as verification consent.

BRF-R043b. A verification parent authorization and verification capability MUST NOT be persisted from future-contingent consent.

BRF-R043c. Verification parent authorization MAY be created only when all implementation milestones and milestone review-resolution obligations are closed, final holistic code review is clean, promotion evidence is valid, current explanation inputs and branch-state verification inputs are concrete, and verification command and evidence identities are known.

BRF-R043d. One interaction MAY create implementation and verification parent authorizations only when the complete bases for both already exist and validate independently during that interaction.

BRF-R043e. A run that reaches the verification boundary without verification authorization MUST set `run.status: paused`, use stop reason `verification-authorization-required`, and report the concrete basis available for approval without invoking `explain-change` or `verify`.

BRF-R044. A changed basis artifact, stale required review, changed finding set, changed occurrence, expanded required scope, changed validation-command identity, or canonical-state mismatch MUST pause or invalidate the affected capability.

BRF-R045. The engine MUST create a new capability rather than mutate an existing capability into materially different scope.

BRF-R046. No conflicting active capability or in-flight transition MAY exist for the same change and stage occurrence.

### Proposal-review occurrence and gate semantics

BRF-R047. A proposal-review occurrence MUST record review ID, reviewed proposal identity, one closed outcome, occurrence-recorded state, clean-gate state, routing action, and pause reason when paused.

BRF-R048. Proposal-review outcomes MUST be closed to `approved`, `changes-requested`, `blocked`, and `inconclusive`.

BRF-R049. Clean-gate state MUST be closed to `satisfied` and `not-satisfied`.

BRF-R050. Routing action MUST be closed to `continue`, `correction-loop`, `stop-at-target`, `pause`, and `fail-closed`.

BRF-R051. `approved` MUST record the occurrence and satisfy the clean proposal gate.

BRF-R052. `changes-requested` MUST record the occurrence and MUST NOT satisfy the clean proposal gate.

BRF-R053. For an exact `proposal-review` target, `changes-requested` MUST stop at the target with findings and clean-gate state `not-satisfied`.

BRF-R054. For a later target, `changes-requested` MAY enter correction only with an active correction capability and remaining correction budget; otherwise it MUST pause.

BRF-R055. `blocked` and `inconclusive` MUST record the occurrence, leave the clean gate unsatisfied, and pause without downstream continuation.

BRF-R056. An inconclusive review MUST NOT rerun without a material proposal, policy, standing-gate, or evidence change.

BRF-R057. An unknown review outcome MUST fail closed and MUST NOT count as a valid occurrence.

BRF-R058. A later target MUST NOT continue unless the latest applicable review of the current proposal identity is `approved`.

BRF-R059. Proposal-review capability scope MUST permit only review invocation and change-local review-evidence mutation and MUST prohibit proposal-content, downstream-authoring, implementation, verification, and external-action mutation.

### Review correction policy

BRF-R060. Review stages MUST remain distinct invocations that review tracked artifacts, use their formal criteria, and record results before correction or continuation.

BRF-R061. A review skill MUST NOT edit the artifact it is reviewing in the same review pass.

BRF-R062. Proposal-side correction eligibility MUST remain driver-owned and deterministic under the existing review-fix safety classifications and budgets unless a later approved spec changes that policy.

BRF-R063. Implementation correction eligibility MUST remain reviewer-owned through `auto_fix_class` and its existing required fields.

BRF-R064. Missing implementation `auto_fix_class` MUST be treated as `none`.

BRF-R065. Automatic correction MUST pause on owner decision, new finding ID or class, non-shrinking unresolved set, exhausted budget, scope expansion, stale evidence, or missing deterministic validation.

BRF-R066. Proposal mutation after review MUST preserve the historical occurrence, make the prior review stale for gate purposes, and require a new proposal-review capability and rereview.

BRF-R067. Verification failure MUST pause without automatic repair.

### Transition transaction and resume

BRF-R068. Before any stage mutation, the engine MUST compute a deterministic transition key and persist a prepared transition receipt.

BRF-R069. A receipt MUST record transition ID, transition key, policy version, run ID, change ID, canonical from-position, target, effective capability ID, input identities, expected postcondition, status, outputs, and canonical-sync status.

BRF-R070. Receipt status MUST be closed to `prepared`, `completed`, `failed`, `paused`, and `cancelled`.

BRF-R071. Every stage policy MUST declare one retry policy from `idempotent-retry`, `reconcile-only`, and `manual-recovery`.

BRF-R072. At most one transition MAY be in flight for one change.

BRF-R073. Resume MUST inspect stage-owned completion evidence before retrying a prepared transition.

BRF-R074. A prepared transition with valid completion evidence MUST reconcile outputs and canonical state without rerunning the stage.

BRF-R075. A prepared transition without completion evidence MAY retry only when its policy is `idempotent-retry`; other retry policies MUST pause or require manual recovery.

BRF-R076. A completed receipt whose canonical state or output identity no longer matches MUST pause for explicit reconciliation.

BRF-R077. Multiple in-flight transitions, unknown receipt state, unknown policy version, or partial output without valid completion evidence MUST fail closed.

### Stage routing and completion

BRF-R078. The mechanism MUST coordinate stage-owning skills and MUST NOT replace their artifact, review, classification, or verification authority.

BRF-R079. The stage-policy registry MUST be closed and define predecessor, applicability, required authorization class, capability kind, owning skill, permitted mutation category, required input identities, completion evidence, retry policy, next-stage calculation, correction policy, and stop behavior for every automatable stage.

BRF-R080. Internal support stages MAY include `proposal`, `architecture-assessment`, `review-resolution`, `ci-maintenance`, `explain-change`, and `final-holistic-code-review`, but they MUST NOT become public targets under this spec.

BRF-R081. `implement@M<n>` MUST complete only when the named milestone implementation exists, milestone validation passes, and the active plan records that milestone as `review-requested`.

BRF-R082. `implement@M<n>` completion MUST NOT imply code-review approval.

BRF-R083. `code-review@M<n>` MUST complete only when the named milestone-local review is approved, required review resolution is closed, and the active plan closes or advances that milestone according to plan policy.

BRF-R084. Every implementation milestone MUST execute in approved plan order and receive independent milestone-local code review before closing.

BRF-R085. Final verification MUST require all implementation milestones closed, final holistic code review clean, current `explain-change`, and fresh verification evidence.

BRF-R086. Successful `verify` MUST stop before `pr` and report `pr` as the next stage without opening it.

### Isolation and external boundary

BRF-R087. Direct individual-skill and review-only invocations MUST remain isolated unless the user explicitly invokes workflow automation or an approved workflow-managed continuation applies.

BRF-R088. Isolation MUST NOT suppress required formal review recording.

BRF-R089. Bugfix invocations MUST remain explicit-step unless a higher-priority approved artifact broadens them.

BRF-R090. The mechanism MUST NOT automatically open a PR, push, publish, release, deploy, merge, perform destructive Git operations, access credentials, or mutate an external system.

### Compatibility and migration

BRF-R091. Migration MUST use dual-read, single-write behavior: legacy records remain readable, while new authorizations write only the unified format.

BRF-R092. Terminal legacy records MUST remain readable indefinitely and MUST NOT be rewritten merely because they are read.

BRF-R093. An active legacy record MAY migrate only on the first explicitly authorized mutating resume.

BRF-R094. Migration MUST write a receipt containing source mechanism, source-record identity, migration time, unified run ID, and projection result.

BRF-R095. After successful migration, the legacy record MUST be read-only for that change.

BRF-R096. Mixed writable legacy and unified state MUST fail closed.

BRF-R097. Active legacy-resume support MAY be removed only after a repository audit finds no active legacy records remaining.

BRF-R098. Rollback MUST stop creation and automatic continuation of unified runs, preserve durable evidence, and return affected work to explicit stage invocation without manufacturing retired profile records.

### Legacy command adapters

BRF-R098a. Supported legacy public command forms MUST remain available throughout the dual-read, single-write migration window, and adapters MUST write only unified `workflow.automation` state.

| Legacy command | Unified target or action | Authorization result |
| --- | --- | --- |
| `workflow auto-through: plan-review` | `plan-review` with `singleton` occurrence | Create bounded authoring parent authorization through `plan-review`; create no implementation or verification authority. |
| `workflow auto-through: verify` | `verify` with `final` occurrence | Create only the currently basis-valid risk-class authorization; never persist future-contingent verification authority. |
| `workflow auto-through: status` | Read unified status | Project legacy-only state read-only and do not migrate. |
| `workflow auto-through: off` | Unified cancellation | For legacy-only active state, project once, write a migration receipt, write the unified run directly as cancelled, and make legacy state read-only. |
| Unknown legacy form | none | Fail closed and report the supported forms and migration guidance. |

BRF-R098b. The `auto-through: verify` adapter MUST persist the final target, MUST create implementation authorization only when its basis is concrete, MUST create verification authorization only when its complete basis is concrete, MUST NOT infer authoring authority, and MUST pause at the first unauthorized boundary.

BRF-R098c. Legacy status projection MUST be side-effect free; legacy cancellation MUST use the unified writer and MUST NOT update legacy profile state.

BRF-R098d. Alias removal or semantic narrowing MUST require a separate approved compatibility change that proves no active legacy run remains, defines removal behavior, updates public skills and adapters, and adds removal regressions.

### Observability and validation

BRF-R099. Every run result MUST report mechanism, structured target, canonical position source, active parent authorization class, effective capability kind, stage outcome, review and clean-gate state when applicable, transitions attempted, fixes applied, human decisions required, artifacts changed, pause or stop reason, and next action.

BRF-R100. Durable status and resume evaluation MUST rely on tracked identities and receipts rather than hidden chat state.

BRF-R101. Validators MUST reject unknown closed-vocabulary values before evaluating cross-field consistency.

BRF-R102. Every new closed-vocabulary validator MUST include an unknown-value regression.

## Inputs and outputs

Inputs:

- Public workflow commands and compatibility aliases.
- Change identity and tracked workflow artifacts.
- Formal review records and review-resolution state.
- Active plan `Current Handoff Summary` after plan ownership begins.
- Bounded parent authorizations.
- Stage-policy definitions and policy version.
- Approved validation commands and branch-state inputs where applicable.

Outputs:

- One `workflow.automation` run using `mechanism: bounded-review-fix`.
- Structured target and run status.
- Parent authorization and effective capability records.
- Prepared and finalized transition receipts.
- Migration receipts when legacy active state is resumed.
- Formal review and correction evidence from stage-owning skills.
- User-visible status, pause, cancellation, completion, and next-action reporting.

## State and invariants

1. One change has at most one active writable automation run.
2. The requested target and current executable authority are independent.
3. Parent authorization is maximum consent and never executable mutation authority.
4. Effective capability equals valid parent identity plus complete stage-appropriate basis plus actual scope no broader than the parent.
5. Capability derivation never crosses an authorization class.
6. Automation metadata never owns the canonical workflow cursor.
7. Review occurrence and clean-gate satisfaction are independent facts.
8. Only an approved review of the current artifact identity satisfies its clean gate.
9. One change has at most one in-flight transition.
10. Review and correction remain separate stage operations.
11. External actions remain prohibited.
12. New writes use one mechanism; compatibility reads do not create a second writer.
13. Only the automation run owns pause state.
14. Completed and cancelled runs, revoked and invalidated parents, and consumed and invalidated capabilities are terminal.
15. Every effective capability is single-use and becomes consumed after its bound transition completes.
16. A final verify target is destination state, not verification authorization.
17. Every public target has exactly one permitted occurrence kind.
18. One active spec owns writable workflow automation; lifecycle ordering and reviewer-owned finding semantics remain separate contracts.
19. Absence from the closed affected-selector registry is never interpreted as a migration disposition.

## Error and boundary behavior

| Condition | Required behavior |
| --- | --- |
| Unknown closed value | Fail closed before consistency evaluation or mutation. |
| Incompatible stage and occurrence | Fail closed before target or authorization persistence. |
| Repeated target lacks one unique current milestone | Do not persist target or authority; report the exact plan-state ambiguity. |
| Missing or revoked parent authorization | Pause or fail closed before capability use. |
| Missing, stale, or over-scoped capability | Pause or fail closed and report the exact mismatch. |
| Multiple plausible pre-plan positions | Pause without choosing a cursor. |
| Automation and active-plan state disagree | Pause for state reconciliation. |
| Proposal review is `changes-requested` | Stop at exact review target, or enter bounded correction for a later target only with valid capability and budget. |
| Proposal review is `blocked` or `inconclusive` | Record the occurrence and pause with clean gate unsatisfied. |
| Inconclusive review has no new evidence | Remain paused; do not spin. |
| Architecture target is not applicable | Stop with `target-not-applicable`. |
| Capability basis changes | Invalidate or pause the capability; do not mutate its scope. |
| Verification target exists before verification authority | Preserve the target; pause at the verification boundary with `verification-authorization-required`. |
| Prepared receipt has completion evidence | Reconcile; do not rerun. |
| Prepared receipt lacks completion evidence | Follow the declared retry policy. |
| Verify fails | Pause without repair. |
| External action would be required | Stop before the action and report the explicit next stage. |
| `off` with prepared transition | Reconcile stage-owned evidence, then cancel, revoke parents, and invalidate capabilities. |

## Compatibility and migration

### Cross-spec disposition contract

Every affected same-rank requirement and acceptance surface is classified as `superseded`, `preserved-unchanged`, or `preserved-rebound`.
Each comma-separated identifier below is individually assigned the row's disposition.
`preserved-rebound` means the behavior remains mandatory with the named unified subject and does not keep a retired profile writable.
The tables below form the closed affected-selector registry.
A selector absent from this registry is outside this amendment; absence is not a migration disposition.
Open-ended defaults, prose wildcards, and identifier ranges cannot establish precedence.
Every source selector in the registry MUST be unique within its source artifact.

#### `specs/workflow-stage-autoprogression.md`

| Exact identifiers | Disposition | Unified subject or replacement |
| --- | --- | --- |
| `R2b`, `R2g` | `preserved-rebound` | Unified workflow-managed run and applicable target/capability policy. |
| `R2b1` | `preserved-unchanged` | Standard workflow-managed lifecycle continuation; it creates no persisted automation mechanism by implication. |
| `R2h`, `R2j` | `superseded` | `BRF-R001`-`BRF-R005` and `BRF-R098a`-`BRF-R098d`. |
| `R2i`, `R2k`, `R2l`, `R2m`, `R2n` | `preserved-rebound` | Unified run validation and authoring parent/capability activation. |
| `R2o`, `R2p` | `superseded` | Structured target routing through `BRF-R009`-`BRF-R017e`; external boundaries remain governed by `BRF-R090`. |
| `R2q`, `R2r`, `R2s`, `R2t` | `preserved-rebound` | Target completion, parent-authorization persistence, and canonical-state ownership. |
| `R2u`, `R2v` | `superseded` | One extensible mechanism replaces future profile creation. |
| `R2w`, `R2x`, `R2y`, `R2z`, `R2aa`, `R2ab` | `preserved-rebound` | Unified post-proposal-authoring stage policy and architecture assessment. |
| `R2ac`, `R2ad` | `preserved-rebound` | Every unified formal-review stage policy. |
| `R2ae`, `R2af` | `preserved-rebound` | Unified run pause and reporting behavior. |
| `R2ag` | `superseded` | Deterministic unified cancellation under `BRF-R007`-`BRF-R008f`. |
| `R2ah` | `preserved-rebound` | Explicit unified run resume after re-evaluation. |
| `R2ai` | `superseded` | Target-aware stage registry and stage-specific budgets replace the six-slot profile budget. |
| `R2aj`, `R2ak`, `R2al` | `preserved-rebound` | Unified rereview budget, preflight, and evidence-first resume policy. |
| `R2am`, `R2an`, `R2ao` | `superseded` | Single mechanism and mandatory alias mapping. |
| `R2ap`, `R2aq` | `preserved-rebound` | Separate authoring, implementation, and verification parent authorizations. |
| `R2ar` | `superseded` | Unified parent authorization and capability records replace the separate profile key/state. |
| `R2as` | `preserved-rebound` | Unified implementation capability basis and activation preflight. |
| `R2at`, `R2au`, `R2av`, `R2aw`, `R2ax` | `preserved-rebound` | Legacy phase compatibility projection only; phases do not govern new unified runs. |
| `R2ay`, `R2az`, `R2ba`, `R2bb`, `R2bc`, `R2bd`, `R2be`, `R2bf`, `R2bg`, `R2bh`, `R2bi`, `R2bj`, `R2bk`, `R2bl`, `R2bm`, `R2bn`, `R2bo`, `R2bp`, `R2bq`, `R2br`, `R2bs`, `R2bt`, `R2bu`, `R2bv`, `R2bw`, `R2bx`, `R2by`, `R2bz` | `preserved-rebound` | Unified implementation, implementation-correction, final-review, verification, and run-completion policies. |

The following non-requirement surfaces receive exact selectors in this amendment:

| Selector and exact legacy surface | Disposition | Unified subject |
| --- | --- | --- |
| `WSA-INPUT-1`: user authorization for `auto-through: plan-review` | `preserved-rebound` | Legacy adapter to authoring authorization. |
| `WSA-INPUT-2`: user authorization for `auto-through: verify` | `preserved-rebound` | Legacy adapter to final target and basis-valid authorization only. |
| `WSA-INPUT-3`: durable authoring-profile policy record | `superseded` | Parent authorizations and capabilities. |
| `WSA-INPUT-4`: implementation profile policy, phase, state, and baseline | `preserved-rebound` | Read-only legacy projection and unified migration receipt. |
| `WSA-OUTPUT-1`: profile state `off`, armed, active, paused, or completed | `superseded` | Closed unified run, parent, and capability states. |
| `WSA-STATE-1` | `superseded` | One unified mechanism replaces exclusive review-to-authoring profile ownership. |
| `WSA-STATE-2`, `WSA-STATE-3`, `WSA-STATE-4` | `preserved-rebound` | Exact plan-review target completion, separate implementation authority, and external-action prohibition. |
| `WSA-ERROR-1`: phase-boundary refusal | `preserved-rebound` | Legacy projection only. |
| `WSA-ERROR-2`: cancellation persistence failure | `preserved-rebound` | Prepared-transition reconciliation and unified cancellation failure handling. |
| `WSA-COMPAT-1`, `WSA-COMPAT-2`, `WSA-COMPAT-3` | `preserved-rebound` | Dual-read projection; new authorization always uses the unified writer. |
| `WSA-OBS-1`: profile-managed pause output | `preserved-rebound` | Unified run status output. |
| `WSA-SEC-1`, `WSA-SEC-2`: retired-profile external-action prohibitions | `preserved-rebound` | `BRF-R090`. |
| `WSA-EC30`, `WSA-EC32`, `WSA-EC33`, `WSA-EC34` | `preserved-rebound` | Unified cancellation, authorization boundary, and legacy phase projection fixtures. |
| `WSA-AC-A1`, `WSA-AC-A9`, `WSA-AC-I1` | `superseded` | Retired profile identity and old `off` state are replaced by the unified mechanism and closed run states. |
| `WSA-AC-A2`, `WSA-AC-A3`, `WSA-AC-A4`, `WSA-AC-A5`, `WSA-AC-A6`, `WSA-AC-A7`, `WSA-AC-A8`, `WSA-AC-A10`, `WSA-AC-A11`, `WSA-AC-A12` | `preserved-rebound` | Unified authoring authorization, gates, assessment, review, pause, target completion, isolation, resume, and persistence. |
| `WSA-AC-I2`, `WSA-AC-I3`, `WSA-AC-I4`, `WSA-AC-I5`, `WSA-AC-I6`, `WSA-AC-I7`, `WSA-AC-I8` | `preserved-rebound` | Legacy phase projection plus unified settlement, correction, final review, verification, and stop-before-PR behavior. |

#### `specs/rigorloop-workflow.md`

| Exact identifiers | Disposition | Unified subject or replacement |
| --- | --- | --- |
| `R7e` | `preserved-rebound` | Unified workflow-managed target/capability continuation. |
| `R7ea`, `R7ec` | `superseded` | Single mechanism and mandatory legacy-command adapters. |
| `R7eb`, `R7ed`, `R7ee`, `R7ef`, `R7eg` | `preserved-rebound` | Unified unknown-value rejection and authoring authorization/gate separation. |
| `R7eh` | `superseded` | Structured target path may continue through `test-spec-review`. |
| `R7ei` | `preserved-rebound` | Exact `plan-review` target completion. |
| `R7ej` | `superseded` | Unified authoring scope may include test-spec stages; external prohibitions remain preserved by `BRF-R090`. |
| `R7ek`, `R7el`, `R7em`, `R7en` | `preserved-rebound` | Unified authoring stage policies, formal reviews, architecture assessment, and pause rules. |
| `R7eo`, `R7ep` | `superseded` | Unified cancellation and target-aware stage policy replace `off` and six-slot profile budget. |
| `R7eq`, `R7er` | `preserved-rebound` | Unified rereview scope, durable authorization, and canonical-state ownership. |
| `R7es` | `superseded` | Future automation extends the single mechanism rather than adding profiles. |
| `R7et`, `R7eu` | `preserved-rebound` | Separate implementation authority and concrete implementation basis. |
| `R7ev`, `R7ew` | `preserved-rebound` | Legacy phase compatibility projection only. |
| `R7ex`, `R7ey`, `R7ez`, `R7faa`, `R7fab`, `R7fac`, `R7fad` | `preserved-rebound` | Unified settlement, implementation, correction, final-review, verification, and stop-before-PR policies. |

| Selector and exact legacy surface | Disposition | Unified subject |
| --- | --- | --- |
| `RLW-INPUT-1`: durable authorization result for `authoring-through-plan-review` | `superseded` | Unified parent authorization and capability persistence. |
| `RLW-INPUT-2`: profile state and authoring autoprogression audit evidence | `superseded` | Unified run status and receipts. |
| `RLW-STATE-1` | `superseded` | Unified run and capability records replace distinct profile state. |
| `RLW-STATE-2` | `preserved-rebound` | Exact `plan-review` target completion and authoring boundary. |
| `RLW-ERROR-1`: unknown or contradictory profile-state pause | `preserved-rebound` | Unified closed vocabularies and fail-closed transitions. |
| `RLW-COMPAT-1`: compatibility through explicit authoring profile | `superseded` | Mandatory adapters plus unified writer. |
| `RLW-EC50`: clean plan-review profile completion | `preserved-rebound` | Exact `plan-review` target completion. |
| `RLW-AC-A1`, `RLW-AC-A2`, `RLW-AC-A9` | `superseded` | Unified states, alias mapping, and single-mechanism extension replace the retired profile assertions. |
| `RLW-AC-A3`, `RLW-AC-A4`, `RLW-AC-A5`, `RLW-AC-A6`, `RLW-AC-A7`, `RLW-AC-A8` | `preserved-rebound` | Unified gate separation, isolation, architecture assessment, target completion, canonical ownership, and durable authorization. |

#### `specs/review-fix-autoprogression.md`

| Exact identifiers | Disposition | Unified subject or replacement |
| --- | --- | --- |
| `R1`, `R2`, `R3` | `preserved-rebound` | Unified `auto`, status, and cancellation commands. |
| `R4`, `R5`, `R6`, `R7`, `R8`, `R9` | `superseded` | Neutral namespace, structured targets, and closed unified states. |
| `R9a` | `preserved-rebound` | Stage-appropriate capability preflight. |
| `R9b` | `superseded` | Non-circular proposal-review bootstrap capability. |
| `R9c`, `R9d`, `R9e` | `preserved-rebound` | Capability activation, direct-review isolation, and fail-closed state. |
| `R9f` | `superseded` | Unified cancellation and run terminal transitions. |
| `R10` | `preserved-unchanged` | Direct invocations do not create automation state. |
| `R11`, `R12` | `superseded` | Unified target path extends through final verify while preserving external boundaries. |
| `R13`, `R14`, `R15`, `R16`, `R17`, `R18`, `R19`, `R20`, `R21`, `R22`, `R22a`, `R22b`, `R22c`, `R22d`, `R22e`, `R22f`, `R22g`, `R23`, `R24`, `R25`, `R26`, `R27`, `R28`, `R29`, `R30`, `R31`, `R32`, `R33`, `R34`, `R35`, `R36`, `R37`, `R38` | `preserved-rebound` | Unified proposal-side preflight, stage ownership, assessment, correction classification, budgets, rereview, and evidence. |
| `R39` | `superseded` | Closed unified run and cancellation transitions. |
| `R40`, `R41`, `R42`, `R43` | `preserved-rebound` | Unified explicit resume, reporting, vocabulary validation, and consistency validation. |
| `R44` | `superseded` | This approved amendment changes both retired profiles. |
| `R45` | `preserved-rebound` | Unified feature rollout must pass its complete acceptance contract before exposure. |

| Selector and exact legacy surface | Disposition | Unified subject |
| --- | --- | --- |
| `RFA-INPUT-1`: `$workflow auto` command forms | `preserved-rebound` | Unified command contract. |
| `RFA-OUTPUT-1`: updated `workflow.autoprogression.review_fix` state | `superseded` | `workflow.automation`. |
| `RFA-STATE-1`: review-fix authorization lives only under legacy namespace | `superseded` | Neutral unified namespace. |
| `RFA-COMPAT-1`: additive profile and unchanged retired profiles | `superseded` | Single writer plus mandatory adapters. |
| `RFA-COMPAT-2`: missing legacy state means unarmed with no migration | `preserved-rebound` | Read-only legacy interpretation; mutation migrates once. |
| `AC1`, `AC3`, `AC5`, `AC16`, `AC19`, `AC24` | `superseded` | Expanded target enum, deterministic cancellation, neutral namespace, non-circular proposal review, unified terminal state, and retired-profile behavior. |
| `AC2`, `AC4`, `AC6`, `AC7`, `AC8`, `AC9`, `AC10`, `AC11`, `AC12`, `AC13`, `AC14`, `AC15`, `AC17`, `AC18`, `AC20`, `AC21`, `AC22`, `AC23`, `AC25`, `AC26` | `preserved-rebound` | Matching unified status, isolation, review, correction, validation, assessment, rollout, and reporting policies. |

#### `specs/review-finding-resolution-contract.md`

| Exact identifiers | Disposition | Unified subject or replacement |
| --- | --- | --- |
| `R1e` | `preserved-rebound` | Unified implementation and implementation-correction capabilities. |
| `R1f`, `R1g`, `R1h`, `R1i`, `R1j`, `R1k`, `R1l` | `preserved-unchanged` | Reviewer-owned correction vocabulary and required fields. |
| `RFR-AC-IMPLEMENTATION-1`: implementation-profile mechanical-field acceptance surface | `preserved-rebound` | Unified implementation-correction capability. |
| `RFR-AC-IMPLEMENTATION-2`: implementation-profile declared-safe-field acceptance surface | `preserved-rebound` | Unified implementation-correction capability. |

BRF-R098e. A repository-owned static check MUST reject an affected legacy requirement or acceptance selector with no disposition, duplicate dispositions, a preserved rule that leaves a retired profile as its only live subject, a superseded rule cited as current authority, an acceptance criterion requiring a retired writer, or an open-ended prose range used as normative precedence.

BRF-R098f. The exact ledger and the four affected specs' unified-amendment notices MUST remain consistent.

BRF-R098g. The static check MUST reject duplicate source selectors before it evaluates disposition consistency.

BRF-R098h. The static check MUST treat the selectors enumerated by this registry as its complete affected set and MUST NOT infer a disposition for an absent selector.

BRF-R098i. Approval settlement MUST normalize `specs/review-fix-autoprogression.md` to `superseded`, record this spec as `superseded_by`, and leave the other three affected specs active only for their retained ownership boundaries.

Legacy phase projection is:

| Legacy phase | Unified compatibility interpretation |
| --- | --- |
| `A` | Audit evaluation only; no executable capability. |
| `B` | Implementation authorization and capabilities through final clean code review, excluding explanation and verify. |
| `C` | Verification capability only when existing promotion evidence remains valid. |

Public command removal or semantic narrowing requires the separate compatibility change defined by `BRF-R098d`.

## Observability

Durable observability consists of the automation run, parent authorizations, effective capabilities, transition receipts, migration receipts, formal review records, review-resolution evidence, canonical plan state, and validation identities.

Status output must distinguish:

- requested target;
- canonical position and its source;
- maximum authorized boundary;
- currently executable capability;
- latest completed and in-flight transition;
- review occurrence and clean-gate state;
- pause, cancellation, or completion reason;
- next required user decision or stage.

Hosted CI status must not be reported as passed unless observed.
Local validation reporting must name commands actually run.

## Security and privacy

- Authorization must be explicit, durable, change-local, and attributable.
- Session-only intent must not authorize a resumed mutation after chat context is lost.
- Parent and capability scope must use path and mutation-category allowlists.
- External actions, credential access, and destructive operations are prohibited.
- Automation records must not store secrets, credentials, private keys, or unnecessary personal data.
- User-visible diagnostics should report identities and reason codes without exposing secret file content.

## Accessibility and UX

The command and status surface is text-based.
Outputs must use stable stage names, exact invalid values, allowed closed values, and actionable pause reasons.
Status must distinguish target reached, clean gate satisfied, paused, cancelled, and authorization required rather than collapsing them into a generic success or failure.

## Performance expectations

- Canonical-state, authorization, capability, and receipt preflight must occur before expensive stage work.
- Resume must reuse valid completion evidence rather than repeating completed stages.
- Status must not invoke authoring, review, implementation, or validation stages.
- Correction budgets bound repeat cycles and file churn according to the preserved stage-specific policies.
- No background scheduler or hosted runtime is introduced.

## Edge cases

EC1. A proposal-review capability has an exact proposal identity but no review identity: it is valid when all other stage-basis fields exist.

EC2. A proposal-correction capability lacks its review identity: capability derivation fails closed.

EC3. An authoring parent attempts to derive implementation: derivation fails closed.

EC4. A revoked parent still has an active child: the child is invalidated before use.

EC5. A capability requires a new path root: the old capability is not expanded; a new capability and possibly new parent authorization are required.

EC6. Proposal review records `changes-requested` for an exact review target: the occurrence is reached, the gate remains unsatisfied, findings are reported, and no downstream stage runs.

EC7. Proposal review records `inconclusive` twice with unchanged evidence: the second run is not invoked automatically.

EC8. A proposal changes after approval: the old review remains historical but cannot satisfy the current proposal gate.

EC9. `code-review@M2` resumes after M2 closes and M3 becomes current: the target remains M2 and does not rebind.

EC10. A prepared receipt exists and outputs are partial: path existence alone is not completion evidence.

EC11. Both legacy and unified records are writable: the run fails closed until one writer is established.

EC12. A legacy record is read for status only: no migration receipt or unified state is written.

EC13. Architecture is not required while the explicit target is `architecture-review`: the run returns `target-not-applicable`.

EC14. Verification fails after implementation closeout: the run pauses and does not repair, reopen PR, or mutate implementation automatically.

EC15. `$workflow auto: implement` sees M2 as the unique current milestone: the engine persists `implement@M2` and the current plan identity.

EC16. `$workflow auto: code-review` has no active plan or sees two plausible milestones: target and authorization persistence do not occur.

EC17. A persisted `code-review@M2` resumes after the plan advances to M3: the target remains M2.

EC18. An invalid pair such as `implement + singleton` or `verify + milestone` fails before persistence.

EC19. A completed run is requested to resume: it remains terminal and a new target requires a new run ID.

EC20. `off` is invoked on an active run with a prepared transition: the engine reconciles evidence before recording cancellation and authority invalidation.

EC21. A final verify target is selected before implementation: the target persists but verification authorization does not.

EC22. Legacy `auto-through: status` reads legacy-only state: projection is side-effect free.

EC23. Legacy `auto-through: off` encounters active legacy-only state: one unified cancelled run and migration receipt are written, and the legacy record becomes read-only.

EC24. A cross-spec disposition is missing, duplicated, or leaves a retired writer as the only live subject: static validation fails.

EC25. Two requirements in one source artifact use the same selector: validation fails before ledger consistency is evaluated.

EC26. A selector is absent from the affected-selector registry: the amendment makes no precedence claim about that selector and does not silently classify it as preserved.

## Non-goals

- Renaming or immediately removing every compatibility command.
- Automatic PR opening, push, publication, release, deploy, merge, or destructive Git operation.
- Repository-wide default automation.
- Background, asynchronous, or hosted workflow execution.
- One blanket proposal-to-verify authorization.
- Automation-owned canonical workflow position.
- Review skills editing their reviewed artifacts.
- Generic replacement of stage-specific correction classification.
- Automatic repair after verification failure.
- Rewriting terminal historical automation records.
- Expanding manual skill or bugfix invocations by default.

## Acceptance criteria

Required proof cases:

| Proof case | Expected result |
| --- | --- |
| `$workflow auto: implement` with unique current M2 | Persist `implement@M2`. |
| `$workflow auto: code-review` without active plan | Fail before persistence. |
| Repeated-stage command with two plausible milestones | Fail before persistence. |
| Resume `code-review@M2` after plan advances to M3 | Remain bound to M2. |
| `implement + singleton` | Fail closed. |
| Unknown run status | Fail closed before consistency checks. |
| Illegal `completed -> active` transition | Fail closed. |
| `off` on active run | Reconcile, cancel, revoke parents, and invalidate capabilities. |
| Early final verify target | Persist target without verification authority. |
| Early verification authorization | Reject. |
| Verification authorization after complete basis exists | Accept. |
| Legacy `auto-through: plan-review` | Use unified singleton authoring mapping. |
| Legacy `auto-through: verify` before verification basis | Persist final target without verification authorization and later pause. |
| Legacy status | Read-only projection. |
| Legacy off | Unified cancellation with migration receipt and no legacy write. |
| Unclassified legacy requirement | Static check fails. |
| Preserved rule exclusively names retired writer | Static check fails. |
| Duplicate source selector | Static check fails before disposition evaluation. |
| Selector absent from affected registry | No implicit disposition is produced. |

| ID | Criterion |
| --- | --- |
| BRF-AC001 | New authorization writes only `workflow.automation` with `mechanism: bounded-review-fix`. |
| BRF-AC002 | Public targets are closed, structured, occurrence-bound, and independent from current authority. |
| BRF-AC003 | Pre-plan position derives from authoritative evidence and ownership hands to the validated active plan without an automation-owned cursor. |
| BRF-AC004 | Every parent authorization records stable identity, class, policy, change, authorizer, maximum target and scope, revocation, and invalidation. |
| BRF-AC005 | Parent authorization alone cannot execute or mutate. |
| BRF-AC006 | Every effective capability binds its parent, kind, stage occurrence, complete stage basis, actual subset scope, and invalidation. |
| BRF-AC007 | Review identities are required only by stage policies where an applicable review can already exist. |
| BRF-AC008 | Capability derivation cannot exceed parent target, paths, categories, budget, or risk class. |
| BRF-AC009 | Parent revocation and invalidation propagate to derived capabilities. |
| BRF-AC010 | Proposal review can run before approval with review-evidence-only mutation authority. |
| BRF-AC011 | Proposal review, proposal correction, and post-proposal authoring use separate capabilities. |
| BRF-AC012 | Review occurrence and clean-gate satisfaction are stored separately. |
| BRF-AC013 | All four proposal-review outcomes have deterministic exact-target and later-target routing; only `approved` satisfies the gate. |
| BRF-AC014 | Unknown review outcomes fail closed and inconclusive review does not spin without new evidence. |
| BRF-AC015 | Every mutating transition writes a prepared receipt before stage invocation. |
| BRF-AC016 | Resume reconciles valid completion evidence before considering retry. |
| BRF-AC017 | Repeated stage targets cannot rebind to another milestone occurrence. |
| BRF-AC018 | Every implementation milestone runs in plan order and receives independent code review. |
| BRF-AC019 | Proposal-side and implementation-side correction ownership and budgets remain distinct. |
| BRF-AC020 | Verify requires final closeout evidence, pauses without repair on failure, and stops before PR on success. |
| BRF-AC021 | Direct individual-skill invocations remain isolated while formal review recording remains mandatory. |
| BRF-AC022 | External actions remain prohibited to the mechanism. |
| BRF-AC023 | Migration is dual-read, single-write, one-way on first mutating resume, and side-effect free on reads. |
| BRF-AC024 | Unknown closed values fail before consistency checks and have direct regression coverage. |
| BRF-AC025 | Status output distinguishes target, canonical position, parent boundary, effective capability, transition state, clean gate, stop reason, and next action. |
| BRF-AC026 | Compatibility adapters preserve historical command meaning without creating legacy writes for new authorization. |
| AC-BRF-SR1-1 | Every public stage has exactly one permitted occurrence kind. |
| AC-BRF-SR1-2 | `implement` and `code-review` bind one milestone ID before persistence. |
| AC-BRF-SR1-3 | Missing or ambiguous current milestone prevents target and authorization persistence. |
| AC-BRF-SR1-4 | Resumed repeated-stage targets cannot rebind to another milestone. |
| AC-BRF-SR1-5 | Invalid stage and occurrence pairs fail closed. |
| AC-BRF-SR2-1 | Run, parent-authorization, and capability statuses use separate closed enums. |
| AC-BRF-SR2-2 | Only the run may use `paused`. |
| AC-BRF-SR2-3 | Every durable status enum has an exhaustive legal-transition table. |
| AC-BRF-SR2-4 | `$workflow auto: off` produces terminal `run.status: cancelled`. |
| AC-BRF-SR2-5 | Cancellation revokes active parents and invalidates active capabilities after transition reconciliation. |
| AC-BRF-SR2-6 | Unknown values and illegal transitions fail closed. |
| AC-BRF-SR3-1 | A final verify target can exist without verification authorization. |
| AC-BRF-SR3-2 | Future-contingent verification parent authorization is forbidden. |
| AC-BRF-SR3-3 | Verification authorization requires complete concrete basis identities. |
| AC-BRF-SR3-4 | Missing verification authority pauses at the verification boundary. |
| AC-BRF-SR3-5 | One interaction grants implementation and verification only when both bases already validate. |
| AC-BRF-SR4-1 | Legacy aliases remain mandatory throughout the migration window. |
| AC-BRF-SR4-2 | `auto-through: plan-review` maps to a singleton plan-review target and authoring authority only. |
| AC-BRF-SR4-3 | `auto-through: verify` never creates future-contingent verification authority. |
| AC-BRF-SR4-4 | Legacy status is a side-effect-free unified projection. |
| AC-BRF-SR4-5 | Legacy off produces a unified cancelled run and no legacy write. |
| AC-BRF-SR4-6 | Alias removal requires a separate approved compatibility change. |
| AC-BRF-SR5-1 | Every affected legacy requirement and acceptance selector has exactly one exact disposition. |
| AC-BRF-SR5-2 | No preserved rule leaves a retired profile as its live exclusive subject. |
| AC-BRF-SR5-3 | No new write uses a retired profile. |
| AC-BRF-SR5-4 | Static validation detects unclassified, duplicate, ambiguous, and contradictory dispositions. |
| AC-BRF-SR5-5 | The exact ledger and affected-spec amendment notices remain consistent. |
| AC-BRF-SR6-1 | Every selector in an affected source artifact is unique before disposition validation begins. |
| AC-BRF-SR6-2 | The affected-selector registry is closed and absence never implies `preserved-unchanged`. |
| AC-BRF-SR6-3 | The unified spec is the only active owner of writable workflow automation after approval settlement. |
| AC-BRF-SR6-4 | The retired review-fix spec records this spec as its replacement, while lifecycle and finding-resolution specs retain only their explicitly stated ownership. |

## Open questions

None.

## Next artifacts

- `spec-review`
- Architecture assessment with expected result `architecture-required`
- Architecture package update and superseding ADR
- `architecture-review`
- Execution plan and `plan-review`
- Matching test specification and `test-spec-review`

## Follow-on artifacts

- Co-amended [Workflow Stage Autoprogression](workflow-stage-autoprogression.md)
- Co-amended [RigorLoop Workflow](rigorloop-workflow.md)
- Co-amended [Review-Fix Autoprogression](review-fix-autoprogression.md)
- Co-amended [Review Finding Resolution Contract](review-finding-resolution-contract.md)
- Co-amended [Workflow Stage Autoprogression test spec](workflow-stage-autoprogression.test.md)
- Approved [spec-review R4](../docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/spec-review-r4.md)

## Readiness

The contract is approved and ready for architecture.
Architecture assessment result: `architecture-required`.
