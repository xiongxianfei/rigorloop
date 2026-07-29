<!-- Template: spec-skeleton-v1 -->
<!-- Skill: spec -->
<!-- Template status: normative -->

# Stage-Owned Lifecycle Artifacts and Change-Local Workflow State

## Status

draft

## Related proposal

- [Stage-Owned Lifecycle Artifacts and Change-Local Workflow State](../docs/proposals/2026-07-28-approved-specification-baselines-and-controlled-amendment-workflow.md)
- [Approved proposal-review R4](../docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/proposal-review-r4.md)

## Goal and context

RigorLoop lifecycle artifacts currently mix settled intent with mutable status,
execution progress, and workflow routing.
That lets a downstream stage change an upstream file and can make the file
differ from the revision its review assessed.

This specification introduces a prospective lifecycle contract in which:

- governed artifact content remains owned by its authoring stage;
- artifact lifecycle state lives in the change record;
- authoring and review peers have closed transitions on their matching
  artifact-state entry;
- independently invoked review skills record evidence and settle their matching
  state without changing workflow routing;
- `workflow` owns current routing state and does not settle artifact approval;
  and
- one `$workflow auto: <target>` command selects the complete repository-local
  automation boundary without another authorization layer; and
- `boundary-first-v1` owns the input, lifecycle, authority, composition,
  temporal, recovery, compatibility, and environment proof boundaries.

The contract deliberately avoids content hashes, write interception,
protected-path infrastructure, revision snapshots, and a formal specification
amendment subsystem.

## Glossary

- `governed change`: a current or resumed nonterminal change whose
  `change.yaml` declares
  `lifecycle_contract: stage-owned-change-local-v1`.
- `governed artifact`: a proposal, feature spec, architecture document, ADR,
  plan, or test spec registered in a governed change's `artifact_states`.
- `artifact ID`: a stable change-local identifier matching
  `[a-z][a-z0-9-]*`.
- `artifact-state entry`: the change-local registry entry for one governed
  artifact, keyed by artifact ID rather than artifact kind.
- `authoring transition`: the matching authoring skill's transition of its
  artifact state to `authoring` before content mutation and then to
  `review-required` after authoring completion.
- `settlement transition`: the matching review skill's evidence-backed
  transition to a settled, revision-required, or blocked state.
- `routing state`: the current lifecycle stage, next stage, blocker, and
  evidence pointers stored in `workflow_state`.
- `review evidence`: the durable formal review record and indexed finding
  closeout required by the review-recording contract.
- `automation target`: the durable user-selected repository-local lifecycle
  boundary for one workflow-managed run.
- `boundary record`: the requirement-owned applicability, partition,
  interaction, outcome, and example map consumed unchanged by test-spec.
- `historical change`: an untouched pre-adoption record that remains readable
  evidence but cannot receive new lifecycle state under a retired model.

## Examples first

### Example E1: independent proposal review settles change-local state

Given a governed change registers a proposal as `review-required`
And no workflow automation run is active
When `proposal-review` records an approved review with no open findings
Then it changes only the proposal entry to `accepted`
And records the review ID and review-record path
And it does not edit the proposal or `workflow_state`.

### Example E2: review requests revision

Given a governed spec is `review-required`
When `spec-review` records `changes-requested`
Then it changes only the spec entry to `revision-required`
And workflow-managed execution routes to `spec`
And an isolated review stops after settlement.

### Example E3: author invalidates settlement before revision

Given a proposal entry is `accepted`
When the proposal author begins a substantive revision
Then `proposal` first changes its matching entry to `authoring`
And it changes the entry to `review-required` only after the revision and
authoring evidence are complete
And the earlier review remains historical evidence
And downstream reliance stops until a fresh proposal review settles the entry.

### Example E4: workflow never approves an artifact

Given `spec-review` has recorded approved evidence but settlement was
interrupted
When workflow evaluates the next route
Then it pauses on incomplete settlement
And it does not write `approved` on behalf of `spec-review`.

### Example E5: workflow-managed review continues

Given a governed change has a current target later than `proposal-review`
When proposal review records evidence and settles the proposal as `accepted`
Then workflow updates `workflow_state`
And continues to `spec` when no other stop condition exists.

### Example E6: one command selects the repository-local target

Given a governed change has an accepted proposal
When the user invokes `$workflow auto: verify`
Then the run records `verify` as its automation target
And it does not request another public authorization parameter at authoring,
implementation, or verification boundaries
And every stage still obeys its fixed write-ownership boundary.

### Example E7: a target does not pre-set future state

Given a final `verify` target exists before a plan or implementation exists
When the run is persisted
Then future stages are not marked complete or ready
And workflow invokes each stage only after its current prerequisites validate.

### Example E8: external action remains prohibited

Given an automated run reaches successful final verification
When the target completion predicate is satisfied
Then the run stops and reports `pr` as the next stage
And it does not open a PR, push, merge, publish, release, or deploy.

### Example E9: downstream plan defect routes to its owner

Given implementation discovers that an active plan is contradictory
When implementation records the defect
Then implementation does not edit the plan
And workflow routes to `plan`
And `plan` marks its matching state `authoring` before revision.

### Example E10: historical change is read-only until resumed

Given a historical change predates `stage-owned-change-local-v1`
When a lifecycle stage reads it without resuming work
Then the existing artifact-local and plan-owned values remain historical
evidence
And no migration occurs merely because the change was read
But any resumed nonterminal work must migrate before its next lifecycle
mutation.

### Example E11: multiple ADRs have unambiguous state

Given one change registers `adr-storage` and `adr-auth` with kind `adr`
When `architecture-review` reviews only `adr-auth`
Then the review record and settlement name artifact ID `adr-auth`
And the state of `adr-storage` is unchanged.

### Example E12: interrupted authoring cannot be reviewed

Given a spec is `approved`
When `spec` enters `authoring` and the invocation stops before completion
Then the spec remains unsettled in `authoring`
And `spec-review` must refuse settlement until `spec` records authoring
completion and transitions it to `review-required`.

### Example E13: milestone resume uses change-local planned work

Given plan `main-plan` defines milestones M1, M2, and M3
And M1 is closed and M2 is `resolution-needed`
When workflow resumes
Then `workflow_state.planned_work.current_milestone` is M2
And `remaining_implementation_milestones` is `[M2, M3]`
And the latest review reference and final-closeout reasons determine the next
legal route without reading mutable status from the plan.

## Requirements

### Activation and normative ownership

SLA-R001. Every new workflow-managed change and every pre-adoption nonterminal
change before resumed lifecycle mutation MUST record the exact top-level
contract-version value:

```yaml
lifecycle_contract: stage-owned-change-local-v1
```

SLA-R002. A change containing the contract-version marker MUST use this specification
as the sole normative owner of governed artifact-state placement,
transition-scoped lifecycle authority, current routing-state placement, and
automation-target semantics.

SLA-R003. A pre-adoption change without the contract-version marker MUST be
read-only historical evidence unless it is migrated before resumed
nonterminal work.

SLA-R004. Reading a historical change MUST NOT add the contract-version marker
or mutate lifecycle state.
The first resumed lifecycle mutation MUST create or validate the current
change-local record before any stage writes.

### Change-local state shape

SLA-R005. A governed `change.yaml` MUST contain exactly one
`artifact_states` mapping and exactly one `workflow_state` mapping.

SLA-R005a. `artifact_states` MUST be keyed by stable artifact IDs matching
`[a-z][a-z0-9-]*`.

SLA-R005b. Artifact IDs and registered artifact paths MUST each be unique
within one governed change.

SLA-R006. Each artifact-state entry MUST contain exactly:

- `kind`;
- `path`;
- `role`;
- `lifecycle_state`;
- `authoring_evidence` when `lifecycle_state` is `authoring` or
  `review-required`;
- `review` when the current state was produced by review settlement; and
- `replacement_artifact_id` when `lifecycle_state` is `superseded`.

SLA-R006a. Registered artifact kinds MUST be closed to `proposal`, `spec`,
`architecture`, `adr`, `plan`, and `test-spec`.

SLA-R006b. Artifact role MUST be closed to `primary` and `supporting`.

SLA-R006c. At most one artifact of each kind MAY have role `primary`; multiple
artifacts of the same kind MAY have role `supporting`.

SLA-R007. `path`, review-record paths, authoring-evidence paths, and
replacement paths MUST be normalized repository-relative paths without `..`.

SLA-R007a. A `superseded` entry's `replacement_artifact_id` MUST resolve to a
different registered artifact whose path is also the replacement pointer
recorded by the owning closeout evidence.

SLA-R008. A present `review` mapping MUST contain exactly:

- `id`;
- `artifact_id`;
- `outcome`; and
- `record`;
- `round`; and
- `adr_settlement` only for an approved ADR review.

SLA-R009. `review.outcome` MUST be closed to `approved`,
`changes-requested`, `blocked`, and `inconclusive`.

SLA-R009a. `review.round` MUST match `r[1-9][0-9]*`.

SLA-R009b. `review.adr_settlement` MUST be exactly `accepted` or `active` and
MUST be absent for non-ADR reviews and non-approved ADR outcomes.

SLA-R010. The shared artifact-state vocabulary MUST be closed to:

```text
authoring
review-required
revision-required
accepted
approved
active
blocked
deprecated
superseded
abandoned
archived
```

SLA-R011. Artifact-specific valid current states MUST be:

| Artifact | Authoring and review-needed states | Settled states | Terminal or historical states |
| --- | --- | --- | --- |
| `proposal` | `authoring`, `review-required`, `revision-required`, `blocked` | `accepted` | `superseded`, `abandoned`, `archived` |
| `spec` | `authoring`, `review-required`, `revision-required`, `blocked` | `approved` | `superseded`, `abandoned`, `archived` |
| `architecture` | `authoring`, `review-required`, `revision-required`, `blocked` | `approved` | `superseded`, `abandoned`, `archived` |
| `adr` | `authoring`, `review-required`, `revision-required`, `blocked` | `accepted`, `active` | `deprecated`, `superseded`, `abandoned`, `archived` |
| `plan` | `authoring`, `review-required`, `revision-required`, `blocked` | `active` | `superseded`, `abandoned`, `archived` |
| `test-spec` | `authoring`, `review-required`, `revision-required`, `blocked` | `active` | `superseded`, `abandoned`, `archived` |

SLA-R012. Unknown artifact kinds, lifecycle states, review outcomes, or
artifact-state combinations MUST fail closed before routing or settlement.

SLA-R012a. Legal nonterminal artifact transitions MUST be closed to:

```text
missing -> authoring
authoring -> review-required
review-required -> accepted | approved | active
review-required -> revision-required | blocked
revision-required -> authoring
blocked -> authoring
accepted | approved | active -> authoring
```

SLA-R012b. Legal closeout and historical transitions MUST be exactly:

```text
authoring | review-required | revision-required | blocked -> abandoned
accepted | approved | active | deprecated -> archived
authoring | review-required | revision-required | blocked |
accepted | approved | active | deprecated -> superseded
accepted | active -> deprecated
```

SLA-R012c. `accepted | active -> deprecated` MUST apply only to ADRs.
`superseded`, `abandoned`, and `archived` MUST be terminal.
`deprecated` MAY transition only to `archived` or `superseded`.
A transition absent from SLA-R012a or SLA-R012b MUST fail closed.

### Governed artifact content

SLA-R013. A governed artifact MUST contain one stable pointer to its owning
change record.

SLA-R014. A governed artifact MUST NOT contain mutable lifecycle status,
current stage, next stage, execution progress, current review result, or current
blocker fields.

SLA-R015. Artifact content MAY preserve stable intent, planned next artifacts,
decision history, non-current examples, and explicitly historical evidence.

SLA-R016. `docs/plan.md` MUST be navigation to plan bodies and change records,
not an active, blocked, or current-status registry for governed changes.

SLA-R017. Governed plans MUST contain stable execution intent, including scope,
sequence, dependencies, validation strategy, recovery, and milestone
definitions, but MUST NOT own current milestone progress, current review
status, blockers, next stage, or final-closeout readiness.

### Authoring transition authority

SLA-R018. The matching authoring skill MUST create or change only its named
artifact-ID entry to `authoring` before it creates or substantively revises
governed content.

SLA-R019. The transition to `authoring` MUST remove the current `review`
mapping and record `authoring_evidence` containing exactly one repository-
relative authoring record path.

SLA-R019a. After governed content and its authoring record are complete, the
matching authoring skill MUST transition the same entry from `authoring` to
`review-required`.

SLA-R019b. An authoring record MUST name the artifact ID, artifact path,
authoring stage, completion status, and resulting review-request path.

SLA-R019c. Authoring completion status MUST be exactly `complete`; absent,
unknown, or non-complete authoring evidence MUST leave the artifact in
`authoring`.

SLA-R020. An authoring skill MUST NOT write a settled lifecycle state, review
evidence, another artifact-state entry, or `workflow_state`.

SLA-R021. A formatting-, typo-, heading-, ordering-, or link-only correction
MAY preserve settlement only when the governing review skill's staleness
contract classifies the change as non-substantive.

SLA-R021a. The matching authoring skill MAY transition its artifact to
`abandoned` or `archived` only with stage-owned closeout evidence.

SLA-R021b. After a replacement artifact is settled, its matching authoring
skill MUST perform a separate closeout operation targeting the replaced
artifact.
That operation MAY transition only the replaced artifact's entry to
`superseded` and MUST record the replacement artifact ID and closeout evidence.

SLA-R021c. An ADR transition to `deprecated` MUST be owned by
`architecture-review` and supported by durable review evidence.

### Review settlement authority

SLA-R022. A matching formal review skill MUST write required durable review
evidence before changing its artifact-state entry.

SLA-R023. A review skill MUST settle only the artifact-ID entry named by its
review evidence and MUST accept settlement only from `review-required`.

SLA-R024. An approved review with no open material findings and required
review-resolution closed MUST map as follows:

| Review stage | Artifact | Settled state |
| --- | --- | --- |
| `proposal-review` | `proposal` | `accepted` |
| `spec-review` | `spec` | `approved` |
| `architecture-review` | `architecture` | `approved` |
| `architecture-review` | `adr` | the exact `review.adr_settlement` value |
| `plan-review` | `plan` | `active` |
| `test-spec-review` | `test-spec` | `active` |

SLA-R025. A review outcome of `changes-requested` MUST map the matching entry to
`revision-required`.

SLA-R026. A review outcome of `blocked` or `inconclusive` MUST map the matching
entry to `blocked`.

SLA-R027. A review skill MUST NOT edit its reviewed artifact, another
artifact-state entry, or `workflow_state`.

SLA-R028. An independently invoked review MUST record its evidence, settle its
matching artifact state, and stop without creating, resuming, or advancing
workflow automation.

SLA-R029. A workflow-managed review MUST use the same evidence and settlement
sequence as an independent review.

SLA-R030. Repeating settlement with the same review ID, artifact path, outcome,
review-record path, round, and ADR settlement value MUST be idempotent.

SLA-R031. Reusing a review ID with different settlement inputs MUST fail closed.

SLA-R032. If review evidence exists but settlement is incomplete, retrying the
same review MUST reconcile the matching artifact-state entry without rerunning
the review.

SLA-R033. Workflow MUST pause on incomplete review settlement and MUST NOT
settle on the review skill's behalf.

### Workflow routing authority

SLA-R034. `workflow_state` MUST be the sole owner of current routing for a
governed change.

SLA-R035. `workflow_state` MUST contain exactly:

- `lifecycle_state`;
- `current_stage`;
- `next_stage`;
- `blocker`; and
- `evidence`; and
- `planned_work`, present exactly when a primary plan is registered.

SLA-R036. `workflow_state.lifecycle_state` MUST be closed to `active`, `paused`,
`completed`, and `cancelled`.

SLA-R037. `current_stage` and `next_stage` MUST use exactly one value from:

```text
explore
research
proposal
proposal-review
spec
spec-review
architecture-assessment
architecture
architecture-review
plan
plan-review
test-spec
test-spec-review
implement
code-review
review-resolution
ci-maintenance
final-holistic-code-review
explain-change
verify
pr
learn
none
```

SLA-R037a. `blocker` MUST be either `null` or a mapping containing exactly
`code` and `evidence`.

SLA-R037b. Blocker code MUST be closed to:

```text
owner-decision
review-findings-open
authoring-in-progress
incomplete-settlement
stale-evidence
scope-expansion
validation-failed
tooling-unavailable
external-action-prohibited
cancelled
```

SLA-R037c. Every `evidence` field in this contract MUST be a list of unique,
normalized repository-relative paths; `blocker.evidence` MUST be non-empty
when `blocker` is not `null`.

SLA-R037d. `workflow_state.planned_work` MUST contain exactly:

- `plan_artifact_id`;
- `current_milestone`;
- `milestones`;
- `remaining_implementation_milestones`;
- `latest_review`; and
- `final_closeout`.

SLA-R037e. `plan_artifact_id` MUST resolve to the primary registered plan.

SLA-R037f. `milestones` MUST be keyed by IDs matching `M[1-9][0-9]*`, preserve
the plan-defined order, and contain exactly `kind` and `state` per entry.

SLA-R037g. Milestone kind MUST be `implementation` or `lifecycle-closeout`.
Milestone state MUST be `planned`, `implementing`, `review-requested`,
`resolution-needed`, or `closed`.

SLA-R037h. Legal milestone transitions MUST be exactly:

```text
planned -> implementing
implementing -> review-requested
review-requested -> closed
review-requested -> resolution-needed
resolution-needed -> review-requested
resolution-needed -> closed
```

SLA-R037i. `current_milestone` MUST be `none` only when no nonterminal
milestone remains; otherwise it MUST name the first nonterminal milestone in
plan order.

SLA-R037j. `remaining_implementation_milestones` MUST equal the ordered IDs of
all non-closed `implementation` milestones.

SLA-R037k. `latest_review` MUST contain exactly `status`, `stage`, `round`,
`artifact_id`, `occurrence`, `milestone_id`, and `evidence`; status MUST be
`not-started`, `not-required`, `review-requested`, `approved`,
`changes-requested`, `blocked`, or `inconclusive`; stage MUST be a formal
review stage from SLA-R037 or `none`; round MUST be `none` or match
`r[1-9][0-9]*`; and occurrence MUST be `singleton`, `milestone`, `final`, or
`none`.

SLA-R037l. `not-started` and `not-required` latest reviews MUST use
`stage: none`, `round: none`, `artifact_id: none`, `occurrence: none`,
`milestone_id: none`, and empty evidence.
Every other latest review MUST name a registered artifact ID, review stage,
positive round, occurrence, and non-empty evidence.
A milestone occurrence MUST name the current milestone ID; singleton and final
occurrences MUST use `milestone_id: none`.

SLA-R037la. When `current_milestone` advances, `latest_review` MUST reset to
`not-started` for the new milestone until review is requested.
Prior milestone reviews remain stage-owned historical evidence and MUST NOT
remain the current `latest_review`.

SLA-R037m. `final_closeout` MUST contain exactly `readiness`, `reasons`, and
`evidence`; readiness MUST be `ready` or `not-ready`.

SLA-R037n. Final-closeout reasons MUST be unique, appear in this normative
order, and be closed to:

```text
ready
lifecycle-gates-open
implementation-milestones-open
milestone-review-pending
review-findings-open
explain-change-pending
verify-pending
pr-handoff-pending
plan-index-sync-pending
external-completion-event-pending
```

SLA-R037o. `ready` readiness MUST use the sole reason `ready`; `not-ready`
readiness MUST use one or more non-`ready` reasons.

SLA-R037oa. `final_closeout.readiness` MUST be derived as a conjunction of
positive stage-owned evidence.
It MAY be `ready` only when every implementation milestone is closed, required
review resolution is closed, final holistic code review is approved,
explain-change is current, final verify passes, required plan-index sync is
complete, PR handoff is complete, and any required external completion event
has occurred.

SLA-R037ob. For each unsatisfied applicable gate in SLA-R037oa,
`final_closeout.reasons` MUST contain its matching non-`ready` reason from
SLA-R037n and `final_closeout.evidence` MUST point to the stage-owned evidence
that establishes the current stop state.
Absent, stale, contradictory, or unparseable evidence MUST produce
`not-ready`, never `ready`.

SLA-R037p. Repeated `implement` and `code-review` occurrences MUST bind the
current milestone ID, primary plan artifact ID, and current planned-work
evidence before execution or resume.

SLA-R038. `workflow` MUST update `workflow_state` only from current governed
artifact state and stage-owned evidence.

SLA-R039. `workflow` MUST NOT write artifact settlement, review outcomes,
governed artifact content, finding dispositions, or verification conclusions.

SLA-R040. A forward route that depends on an artifact MUST require that
artifact's current settled state and matching review evidence.

SLA-R041. `workflow_state` MUST NOT duplicate full findings, rationale,
validation output, or stage history; it MUST point to their owning evidence.

### Downstream challenge and correction

SLA-R042. A downstream stage that discovers an upstream defect MUST record the
problem in its own evidence and MUST NOT edit the upstream artifact or its
artifact-state entry.

SLA-R043. A blocking upstream defect MUST pause forward routing.

SLA-R044. Workflow MUST route an accepted upstream defect to the artifact's
matching authoring stage.

SLA-R045. Before revision, the authoring stage MUST perform the
`authoring` transition defined by SLA-R018.

SLA-R046. After a substantive revision, the matching review MUST run again
before downstream reliance resumes.

SLA-R047. After fresh settlement, workflow MUST conservatively rerun stages
after the revised artifact unless a later approved contract introduces
selective reuse.

### Target-bound workflow automation

SLA-R048. `$workflow auto: <target-stage>` on a governed change MUST store one
structured target at `workflow.automation.target`.

SLA-R048a. The selected target MUST be the complete public authorization
boundary for repository-local continuation through that stage.

SLA-R049. `workflow.automation` MUST contain exactly:

- `mechanism`;
- `target`;
- `status`;
- `current_stage`;
- `stop_reason`; and
- `evidence`.

`mechanism` MUST be exactly `bounded-review-fix`.
`current_stage` MUST use SLA-R037.
`stop_reason` MUST be `null` while active and a non-empty reason code while
paused, completed, or cancelled.
`evidence` MUST follow SLA-R037c.

SLA-R050. Automation status MUST be closed to `active`, `paused`, `completed`,
and `cancelled`.

Legal automation transitions MUST be exactly:

```text
active -> paused
active -> completed
active -> cancelled
paused -> active
paused -> cancelled
```

SLA-R050a. A completed or cancelled run MUST NOT return to `active`; a new
user invocation creates a new run occurrence.

SLA-R050b. The target MUST retain the structured stage, occurrence, binding,
and completion-predicate contract of the existing automation specification.

SLA-R051. The selected target MUST be sufficient user consent for
repository-local authoring, implementation, review, explanation, and
verification stages that are prerequisites of or equal to that target.

SLA-R052. Workflow MUST NOT request, persist, derive, or require another public
authorization, capability, activation selector, or risk-class parameter solely
because execution reaches a later stage.

SLA-R053. The selected target MUST NOT expand any stage's write authority
beyond SLA-R074.

SLA-R054. Before invoking a stage, workflow MUST validate its current
prerequisites, target position, and fixed write boundary.

SLA-R055. Workflow MUST NOT mark a future stage ready, complete, or settled
before current stage-owned evidence supports that transition.

SLA-R056. After a stage records its owned output, workflow MUST record only the
corresponding routing or planned-work transition.

SLA-R057. Repeated stage occurrences MUST bind the current artifact or
milestone identity and MUST NOT silently rebind on resume.

SLA-R058. Direct individual-skill invocation MUST remain isolated unless the
user selected a workflow automation target.

SLA-R059. Missing a retired authorization, capability, profile, or selector
record MUST NOT pause a governed run.

SLA-R060. Automation MUST pause on a real owner decision, material unresolved
finding, scope or path expansion, stale or contradictory evidence, invalid
transition, failed or inconclusive validation, cancellation, missing required
tooling, or external or destructive action.

SLA-R061. Automation MUST NOT open a PR, push, publish, release, deploy, merge,
perform destructive Git operations, access credentials, or mutate an external
system.

SLA-R062. Successful final verification MUST complete the target, stop the
automation run, and report `pr` as the next stage without invoking it.

SLA-R063. `$workflow auto: status` MUST remain read-only.

SLA-R064. `$workflow auto: off` MUST cancel the run, preserve transition
evidence, and stop new scheduling.

SLA-R064a. Unknown automation statuses, transitions, or structured-target
values MUST fail closed before mutation.

### Compatibility and proof boundary

SLA-R065. Existing nonterminal automation runs created before adoption MUST
migrate to the current change-local contract before any continuation or state
mutation.

SLA-R066. Migration MUST preserve the structured target, completed transition
evidence, current stop reason, and external-action prohibition.

SLA-R067. One governed change MUST NOT mix artifact-local status, plan-owned
live routing, or separate risk-class consent with the new state model.

SLA-R068. Historical artifacts and changes MUST NOT be mass-migrated.

SLA-R069. Implementation of this contract MUST NOT require content hashes,
protected-path manifests, write interception, immutable snapshots, or a hosted
state service.

SLA-R070. Repository validation MUST check state shape, closed vocabularies,
legal transitions, review-evidence settlement consistency, routing
consistency, contract-version consistency, and generated-adapter parity.
These checks support the published-skill contract and MUST NOT become a second
normative workflow.

SLA-R071. Deterministic validation MUST NOT claim to prove which skill process
physically wrote a file.

SLA-R072. Published skill guidance MUST declare owned artifact outputs,
matching artifact-state transitions, read-only inputs, independent-invocation
behavior, and route-back behavior.

SLA-R073. Generated public adapters MUST be rebuilt from canonical skill
sources and MUST preserve the same transition and isolation guidance.

SLA-R074. Unknown closed-vocabulary values MUST fail before consistency checks
and MUST have direct unknown-value regression coverage.

## Published-skill ownership and compatibility

The public behavior is the stage contract below.
Repository scripts may check its structured state, but scripts do not define
stage ownership.

| Published skill group | Writable outputs | Read-only inputs | Required route-back behavior |
| --- | --- | --- | --- |
| `workflow` | `workflow_state`, the selected automation target, and transition receipts | governed artifacts, artifact settlement, and stage-owned evidence | Pause and route to the owning stage; never repair content or manufacture settlement. |
| `proposal`, `spec`, `architecture`, `plan`, `test-spec` | their own governed artifact, matching authoring evidence, and only their matching `artifact_states` entry for `authoring`, `review-required`, or owned closeout | every other governed artifact and state entry | Record the authoring transition before revision and request fresh peer review after completion. |
| `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, `test-spec-review` | their own review evidence and only the reviewed artifact's matching settlement transition | the reviewed artifact, every other governed artifact, and `workflow_state` | Record findings or settlement and stop when isolated; never revise reviewed content or advance routing. |
| `implement` | implementation, tests, and implementation evidence | governed artifacts, artifact settlement, and `workflow_state` | Record an upstream challenge and stop; never update plan or other upstream content. |
| `code-review` | implementation-review evidence | implementation and all governing artifacts | Record findings and stop or hand back to `implement`; never repair implementation or upstream artifacts. |
| `explain-change`, `verify`, `learn` | their own stage evidence | governed artifacts, artifact settlement, and `workflow_state` | Report mismatch, blocker, or lesson to its owner; never make normative or lifecycle corrections. |
| `pr` | PR handoff evidence and an explicitly authorized PR action | governed artifacts, artifact settlement, and `workflow_state` | Report not-ready and stop; never repair lifecycle state or governing content. |
| every other published skill | only the outputs declared by its own contract | governed artifacts and state owned by another stage | Route a required correction to the declared owner; never infer write authority from workflow position. |

SLA-R074a. Every published skill MUST state its writable outputs,
read-only inputs, independent-invocation behavior, and route-back behavior
consistently with this table.

SLA-R074b. Generated public adapters MUST preserve the canonical published
skill behavior without adding a downstream write to a governed artifact,
another artifact's state, or workflow routing.

SLA-R074c. For a governed change, this specification replaces earlier
requirements only for these closed subjects:

| Source specification | Replaced subject for governed changes | Retained behavior |
| --- | --- | --- |
| `artifact-status-lifecycle-ownership.md` | lifecycle-state storage inside governed artifacts and downstream normalization of that state | lifecycle meanings, terminal history, staleness detection, and explicit replacement evidence |
| `single-source-of-workflow-state.md` | active-plan and `docs/plan.md` ownership of current milestone, review, blocker, next-stage, and closeout state | milestone ordering, review evidence, closeout gates, portability, and historical plan intent |
| `rigorloop-workflow.md` | instructions that let a peer or downstream stage update reviewed content, plan progress, artifact settlement outside its matching transition, or request another public authorization inside one target | lifecycle order, formal review gates, isolation, correction budgets, and stop conditions |
| `single-bounded-review-fix-workflow-automation.md` | additional authorization, capability, activation-selector, profile, and selector-ledger mechanisms | structured targets, occurrence binding, review independence, bounded correction, evidence-first resume, historical reads, and external-action prohibitions |
| `formal-review-recording.md` | artifact-local lifecycle settlement and requirements that keep mutable status in reviewed artifacts or plans | formal review receipts, detailed finding records, review-log indexing, and review-resolution obligations |
| `downstream-status-settlement-before-reliance.md` | every permission or requirement for a downstream stage to edit upstream lifecycle, readiness, follow-on, or closeout metadata | clear-review-evidence checks, fail-closed reliance, and blocking on contradictory or unresolved evidence |
| `proposal-family-assets-progressive-disclosure.md` | proposal-status sections, values, and asset-shape preservation requirements | proposal-family asset packaging, progressive disclosure, Vision fit, scope preservation, review dimensions, and recording behavior |
| `spec-family-assets-progressive-disclosure.md` | embedded spec-status sections, proposal-status settlement gates, and active-plan handoff ownership | spec-family asset packaging, progressive disclosure, boundary guidance, and evidence-access behavior |
| `review-finding-resolution-contract.md` | artifact-local settlement and clean-review settlement through proposal status or decision-log mutation | material-finding shape, review logging, dispositions, resolution closeout, and referential integrity |
| `review-skill-family-consistency-parser-owned-finding-shape.md` | downstream reliance on embedded proposal status | review-family consistency, parser-owned finding shape, asset policy, and formal review evidence requirements |
| `stage-evidence-access-contracts-for-cost-bounded-rigor.md` | accepted proposal status settlement as an output or acceptance criterion | bounded evidence access, escalation rules, and contributor-visible evidence reporting |
| `stop-tracking-generated-public-adapter-skill-bodies.md` | accepted proposal status settlement as a downstream-reliance prerequisite | canonical skill-source ownership, adapter archive installation, release metadata, and generated-output policy |
| `workflow-stage-autoprogression.md` | artifact-local status gates and separately armed authoring or implementation profiles | stage ordering, review gates, bounded correction, resume safety, test-spec proof requirements, and stop-before-PR behavior |
| `change-record-catalog-registration-and-bounded-read-model.md` | active-plan `Current Handoff Summary` as the current live-state source | change-record registration, bounded artifact discovery, evidence pointers, and historical reads |
| `cost-bounded-rigor-m5-progressive-loading-follow-through.md` | active-plan handoff state as the first implementation-state read | progressive loading, quick operating guides, bounded evidence, and full-read escape conditions |
| `learn-artifact-model.md` | routing mutable process follow-ups into the active plan | learn session and topic ownership, classification, deduplication, and routing to an owning surface |
| `milestone-aware-review-handoff.md` | code-review requirements to update or require updates to active-plan milestone and handoff state | milestone identity, review outcomes, finding resolution, and next-milestone sequencing |
| `plan-index-lifecycle-ownership.md` | plan-body and plan-index ownership of mutable lifecycle, progress, blocker, and closeout state | stable plan navigation, historical plan preservation, archive link integrity, and bounded index presentation |
| `progressive-loading-high-cost-public-skills.md` | active-plan `Current Handoff Summary` as the authoritative handoff-state source | progressive evidence loading, token-cost controls, quick guides, and safety escape conditions |
| `release-process-contract.md` | release-stage updates to active-plan lifecycle or handoff state | release evidence, safety gates, rollback, registry verification, and transactional release behavior |
| `skill-contract.md` | artifact-local lifecycle settlement, embedded mutable status requirements, and current-handoff templates that duplicate change-local state | normalized skill structure, resource and asset integrity, claim boundaries, portability, and generated-adapter parity |
| `workflow-skill-artifact-location-map.md` | plan bodies and `docs/plan.md` as mutable lifecycle-state or current-routing owners | artifact placement, change-root mapping, review-record locations, portable defaults, and workflow-guide ownership |
| `cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md` | current-handoff or active-plan state as the first current-state source and active-plan ownership of implementation handoff | bounded evidence order, escalation, follow-up classification, and cost controls |
| `cost-bounded-rigor-m2-selected-skill-reminders.md` | implementation recording mutable rationale or validation evidence in the active plan | selected-skill reminders, no-change rationale, and contributor-visible evidence requirements |
| `cost-bounded-rigor-m4-lifecycle-token-cost-summary.md` | mutable summary triggers, decisions, or follow-ups owned by the active plan | lifecycle token-cost summaries, trigger classification, report shape, and evidence limits |
| `follow-up-ownership-and-deferred-work-register.md` | current-change execution or learn follow-ups being written to the active plan | cross-change follow-up admission, ownership fields, deduplication, and terminal dispositions |
| `guide-system-source-of-truth-alignment.md` | `docs/plan.md` as a mutable live-work index | guide-surface classification, navigation, source-rank reporting, and bounded presentation |
| `implement-first-attempt-correctness.md` | implementation writing rationale, progress, or alignment state into the active plan body | same-slice completeness, first-pass proof, validation selection, and aligned-surface auditing |
| `installed-skill-artifact-placement-contract.md` | lifecycle state and milestone progress being placed in `docs/plan.md` or the plan body | artifact-type distinctions, path discovery, portable defaults, and placement diagnostics |
| `project-artifact-location-guide-and-examples-surface.md` | active-plan metadata as current lifecycle authority or a higher-ranked mutable path source | artifact-location guidance, example isolation, path lookup, and generated-surface validation |
| `release-transaction-automation.md` | active-plan `Current Handoff Summary` as the next workflow-action owner | transactional release stages, evidence, safety checks, rollback, and stop conditions |
| `test-spec-review-gate.md` | active-plan ownership of current workflow state | proof-map review, implementation handoff gating, coverage, and review evidence |

SLA-R074d. A requirement outside the replaced subjects in SLA-R074c
MUST remain authoritative.
Each source specification MUST carry one reciprocal notice naming this
specification, the contract-version marker, its replaced subject, and its
retained behavior.
`CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` MUST assign lifecycle
state, routing, and stage write authority consistently with this specification.
Approval MUST fail when a notice is missing or contradicts SLA-R074c.

SLA-R074e. A matching test specification whose proof expectations rely on a
replaced subject in SLA-R074c MUST be treated as stale.
It MUST be revised and pass `test-spec-review` before implementation relies on
that proof map.
Historical test evidence remains unchanged.

SLA-R075. This specification MUST use the `boundary-first-v1` record below and
MUST keep its eight core dimensions, owned boundary definitions, selected
interactions, and example classifications structurally valid and semantically
current.
While repository boundary-first activation remains `pending`, this draft MUST
NOT record the `boundary_contract: boundary-first-v1` activation marker.

SLA-R076. The matching test specification MUST consume the exact boundary and
interaction IDs below and MUST record direct proof or a blocking gap for every
applicable boundary and selected interaction.

SLA-R077. Examples MUST remain illustrations of requirement-owned behavior and
MUST NOT create a boundary, invariant, transition, or outcome.

## Boundary model

Boundary model version: boundary-first-v1

Boundary model scope: every requirement defined in this specification,
`SLA-R001` through `SLA-R077`, including the defined suffixed requirements.

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | SLA-R001, SLA-R005, SLA-R048, SLA-R064a | BND-INPUT-001 | - |
| state-lifecycle | applicable | SLA-R012a, SLA-R012b, SLA-R035, SLA-R037h, SLA-R037k, SLA-R037oa, SLA-R050, SLA-R057 | BND-STATE-001 | - |
| identity-authority | applicable | SLA-R020, SLA-R023, SLA-R027, SLA-R034, SLA-R039, SLA-R042, SLA-R053, SLA-R054 | BND-AUTH-001 | - |
| composition-path | applicable | SLA-R028, SLA-R029, SLA-R033, SLA-R044, SLA-R046, SLA-R063, SLA-R064, SLA-R072, SLA-R074b | BND-COMPOSE-001 | - |
| temporal-retry | applicable | SLA-R019a, SLA-R030, SLA-R031, SLA-R032, SLA-R037la, SLA-R050a, SLA-R057, SLA-R058 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | SLA-R025, SLA-R026, SLA-R043, SLA-R044, SLA-R047, SLA-R060, SLA-R062, SLA-R064 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | SLA-R003, SLA-R004, SLA-R065, SLA-R067, SLA-R068, SLA-R074a, SLA-R074c, SLA-R074d, SLA-R074e | BND-COMPAT-001 | - |
| external-environment | applicable | SLA-R007, SLA-R037c, SLA-R061, SLA-R069, SLA-R071 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | SLA-R001, SLA-R005, SLA-R048, SLA-R064a | exact contract-version marker; valid registry and target command; absent, malformed, additional, unknown, conflicting, or path-escaping input | Reading historical work does not mutate it, resumed nonterminal work uses the current contract, identifiers remain unique, and unknown input never widens authority. | Valid current input proceeds; historical reads remain read-only; every invalid or unmigrated mutation fails before writing. | SLA-R001 |
| BND-STATE-001 | state-lifecycle | SLA-R012a, SLA-R012b, SLA-R035, SLA-R037h, SLA-R037k, SLA-R037oa, SLA-R050, SLA-R057 | artifact, workflow, milestone, review occurrence, closeout, and automation-run legal transitions; every absent transition is illegal | Authoring is not review-ready, current review matches its occurrence, readiness needs positive evidence, and terminal state does not reopen. | Legal transitions commit; stale, incomplete, illegal, or contradictory state pauses or fails closed. | SLA-R012a |
| BND-AUTH-001 | identity-authority | SLA-R020, SLA-R023, SLA-R027, SLA-R034, SLA-R039, SLA-R042, SLA-R053, SLA-R054 | authoring owner; review peer; workflow router; downstream challenger; automation target | Each actor changes only its owned surface, and the target never expands stage authority. | Owned bounded mutation succeeds; cross-owner, stale, substituted, or expanded authority pauses or fails. | SLA-R020 |
| BND-COMPOSE-001 | composition-path | SLA-R028, SLA-R029, SLA-R033, SLA-R044, SLA-R046, SLA-R063, SLA-R064, SLA-R072, SLA-R074b | isolated and managed review; owner route-back; rereview; status and off aliases; canonical skills; adapters; reciprocal notices | Review never advances routing, workflow never manufactures settlement, and projected surfaces point to one exact contract. | Isolated review stops; managed routing resumes only after settlement; drift or conflicting authority blocks current-contract use. | SLA-R028 |
| BND-TEMPORAL-001 | temporal-retry | SLA-R019a, SLA-R030, SLA-R031, SLA-R032, SLA-R037la, SLA-R050a, SLA-R057, SLA-R058 | interrupted authoring or settlement; identical retry; conflicting reuse; milestone advance; terminal automation run; isolated invocation | Partial authoring is not review-ready, review IDs do not change meaning, and occurrence identity does not silently rebind. | Completed evidence reconciles; incomplete or changed evidence pauses; a terminal run needs a new invocation. | SLA-R030 |
| BND-RECOVERY-001 | failure-recovery | SLA-R025, SLA-R026, SLA-R043, SLA-R044, SLA-R047, SLA-R060, SLA-R062, SLA-R064 | revision request; blocked review; upstream defect; validation or verification failure; missing tooling; cancellation; conservative replay | Failure preserves evidence, never grants automatic repair or external action, and returns content changes to the owning stage. | Workflow pauses or cancels durably, routes to the owner when correctable, and resumes only after required settlement. | SLA-R060 |
| BND-COMPAT-001 | compatibility-migration | SLA-R003, SLA-R004, SLA-R065, SLA-R067, SLA-R068, SLA-R074a, SLA-R074c, SLA-R074d, SLA-R074e | historical read; resumed pre-adoption work; required migration; mixed writable state; rollback; closed replaced subjects; stale dependent proof maps | Historical records are read-only, resumed nonterminal work uses one current writer, every affected source names the same closed subject boundary, and stale proof is not reused. | Historical reads remain valid; resumed work migrates first; missing notices, stale test specs, stale governance, or mixed authority block downstream reliance. | SLA-R065 |
| BND-ENV-001 | external-environment | SLA-R007, SLA-R037c, SLA-R061, SLA-R069, SLA-R071 | valid repository-relative path; escaping or expanded path; local mutation; external, credential, destructive Git, hosted, hash, interception, or attribution boundary | Automation stays repository-local, external actions remain prohibited, and deterministic validation does not overclaim writer identity. | In-scope local work may proceed; expanded, destructive, external, or unsupported proof requests pause or fail. | SLA-R061 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | SLA-R018, SLA-R019a, SLA-R023, SLA-R027 | BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001 | Independent review observes an artifact while its owner is partway through revision. | State remains authoring; review refuses settlement; only completed authoring may request review. |
| INT-002 | SLA-R022, SLA-R028, SLA-R032, SLA-R033, SLA-R038 | BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001 | Review evidence is durable but peer settlement or workflow routing is interrupted. | The same review reconciles settlement idempotently; workflow waits and never writes approval. |
| INT-003 | SLA-R037i, SLA-R037j, SLA-R037k, SLA-R037l, SLA-R037la, SLA-R037oa, SLA-R037ob, SLA-R037p | BND-STATE-001, BND-TEMPORAL-001 | A prior milestone review is mistaken for the current occurrence or final readiness is asserted from incomplete gates. | Current review binds the exact artifact and milestone occurrence; stale evidence yields not-ready and pauses resume. |
| INT-004 | SLA-R050b, SLA-R051, SLA-R052, SLA-R053, SLA-R054, SLA-R055, SLA-R058 | BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-ENV-001 | A future stage is inferred complete or receives wider writes merely because it is before the selected target. | Workflow validates current prerequisites; stage ownership remains fixed; no additional authorization layer or future completion is persisted. |
| INT-005 | SLA-R065, SLA-R066, SLA-R067, SLA-R074a, SLA-R074b, SLA-R074c, SLA-R074d, SLA-R074e | BND-COMPAT-001, BND-COMPOSE-001 | A retired writer and the governed writer both claim current authority, or a stale proof map still expects the retired writer. | Reciprocal notices and contract-version checks establish one writer; mixed writable state and stale downstream proof fail closed. |
| INT-006 | SLA-R060, SLA-R061, SLA-R062, SLA-R063, SLA-R064 | BND-RECOVERY-001, BND-ENV-001 | Final verification or cancellation is treated as authority to repair, open a PR, or mutate an external system. | Failure pauses without repair; success completes before PR; cancellation invalidates authority; status remains read-only. |
| INT-007 | SLA-R042, SLA-R043, SLA-R044, SLA-R045, SLA-R046, SLA-R047 | BND-AUTH-001, BND-COMPOSE-001, BND-RECOVERY-001 | A downstream stage discovers an upstream defect and writes back directly. | Downstream records evidence and pauses; workflow routes to the owner; authoring and fresh review precede conservative replay. |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | SLA-R028 | BND-COMPOSE-001 | - | - |
| E2 | illustration | SLA-R025, SLA-R044 | BND-RECOVERY-001 | - | - |
| E3 | illustration | SLA-R019a | BND-TEMPORAL-001 | - | - |
| E4 | illustration | SLA-R032 | BND-TEMPORAL-001 | - | - |
| E5 | illustration | SLA-R029, SLA-R044 | BND-COMPOSE-001 | - | - |
| E6 | illustration | SLA-R053, SLA-R054 | BND-AUTH-001 | - | - |
| E7 | illustration | SLA-R057, SLA-R058 | BND-TEMPORAL-001 | - | - |
| E8 | illustration | SLA-R061 | BND-ENV-001 | - | - |
| E9 | illustration | SLA-R043, SLA-R044 | BND-RECOVERY-001 | - | - |
| E10 | illustration | SLA-R003, SLA-R004, SLA-R068 | BND-COMPAT-001 | - | - |
| E11 | illustration | SLA-R005 | BND-INPUT-001 | - | - |
| E12 | illustration | SLA-R019a, SLA-R032 | BND-TEMPORAL-001 | - | - |
| E13 | illustration | SLA-R037k, SLA-R037oa | BND-STATE-001 | - | - |

## Inputs and outputs

### Inputs

- accepted proposal and approved proposal-review evidence;
- governed `docs/changes/<change-id>/change.yaml`;
- governed artifact paths and their stable change-record pointers;
- formal review records, review log, and review-resolution evidence;
- stage-owned authoring, implementation, review, verification, and learn
  evidence;
- structured workflow target;
- current repository paths, validation commands, and branch-state evidence.

### Outputs

- change-local artifact lifecycle state;
- change-local current workflow routing state;
- durable review settlement linked to formal evidence;
- authoring invalidation before governed content revision;
- transition receipts and actionable pause reasons;
- exact boundary and interaction IDs for downstream proof mapping;
- PR-visible links to review, resolution, verification, and learn evidence.

## State and invariants

The following invariants apply to governed changes:

```text
governed artifact content has one authoring owner
artifact lifecycle state has transition-scoped peer ownership
artifact IDs and paths are unique within one change
authoring state is distinct from review readiness
review evidence precedes review settlement
workflow routing never manufactures artifact approval
independent review settlement never advances workflow routing
forward routing requires settled upstream artifacts
substantive author revision invalidates settlement before content changes
planned-work live state has one change-local owner
one automation target bounds repository-local work through its target
each stage keeps the same fixed write boundary in manual and automated use
external actions remain prohibited
examples illustrate requirement-owned boundaries and never create behavior
```

Exactly one current artifact-state entry may exist for one artifact ID.
Multiple artifact IDs may share a kind, but not a path.
Exactly one `workflow_state` may exist for one governed change.
At most one writable workflow automation run may be active.

## Error and boundary behavior

- Missing contract-version metadata on a new or resumed nonterminal change
  fails closed and reports the expected marker.
- A missing, invalid, or duplicate artifact ID or path fails closed.
- Two primary artifacts of one kind fail closed.
- A review naming an artifact path but not its registered artifact ID fails
  closed.
- A review invoked while the artifact is `authoring` refuses settlement.
- A settlement whose review ID, outcome, record, or open-finding state does not
  match formal evidence fails closed.
- A review that attempts to settle another artifact ID is incomplete and
  must not report settlement success.
- A workflow route that depends on `review-required`, `revision-required`, or
  `authoring`, or `blocked` state pauses and names the artifact ID.
- A substantive authoring edit that begins while the matching state remains
  settled is a lifecycle violation and blocks downstream reliance when
  detected.
- An interrupted review after evidence but before settlement resumes through
  idempotent settlement reconciliation.
- An interrupted review before durable evidence does not settle.
- A selected target never expands a stage's fixed write boundary.
- A future stage is not marked ready or complete before its prerequisites and
  owned evidence exist.
- Inconsistent current milestone, remaining milestone list, review reference,
  or final-closeout reasons fail before resume.
- Failed final verification pauses without automatic repair.
- Unknown values fail closed before state-consistency evaluation.

## Compatibility and migration

Activation is prospective.
A repository enables the new model only after the complete schema, workflow,
skill, validation, and adapter slice is reviewed.

Historical changes remain readable and unchanged.
Resumed nonterminal work migrates before its first lifecycle mutation.
Read-only inspection does not migrate.

Migration records the historical policy, run ID, target, current evidence,
completed receipts, and projection result.
After migration, the historical automation record and artifact-local status
remain historical and read-only for that change.

Rollback disables automatic continuation, preserves change-local state and
evidence, and returns affected work to explicit stage invocation under the
same ownership boundaries.
Rollback does not restore downstream write access to upstream artifacts or
erase truthful lifecycle history.

## Observability

Status output for a governed run must show:

- contract version;
- structured target;
- automation target and status;
- current workflow stage and next stage;
- current artifact states and their review IDs;
- latest completed and in-flight transition;
- pause or completion reason; and
- next required stage or owner decision.

Reviewers must be able to follow links from `change.yaml` to governed
artifacts, formal reviews, finding resolution, validation evidence,
verification evidence, and relevant learn records.

Hosted CI must not be reported as passed unless observed.
Local validation reporting must name the commands actually run.

## Security and privacy

- The selected target covers repository-local work only and never expands
  stage write ownership.
- External actions, destructive Git, credential access, and hosted mutations
  remain prohibited.
- Change records and status output must not store secrets, credentials,
  private keys, or unnecessary personal data.
- Diagnostics should report paths, IDs, closed values, and reason codes
  without printing secret file content.
- No hosted control plane or background scheduler is introduced.

## Accessibility and UX

The interface is text based.
Diagnostics must name the invalid value, allowed values, affected artifact or
stage, and smallest recovery action.

Status output must distinguish:

- artifact settled;
- artifact revision required;
- workflow paused;
- target reached;
- validation failed;
- owner decision required; and
- external action prohibited.

## Performance expectations

- State and evidence preflight must occur before expensive stage work.
- Status reads must not invoke lifecycle stages or mutate historical changes.
- State validation should be linear in the bounded change record and linked
  review indexes.
- Resume should reconcile valid completed evidence rather than repeat stage
  work.
- No background polling, hosted runtime, or repository-wide content hashing is
  required.

## Edge cases

EC1. An independent approved review settles artifact state but leaves
`workflow_state` unchanged.

EC2. An independent changes-requested review settles `revision-required` and
does not invoke the authoring skill.

EC3. An author starts revision after acceptance; state becomes `authoring`
before content changes and becomes `review-required` only after complete
authoring evidence exists.

EC4. Review evidence is durable but settlement is missing; the same review ID
reconciles settlement without another review.

EC5. The same review ID appears with a different outcome or record path;
settlement fails closed.

EC6. Workflow sees approved review evidence but `review-required` state;
workflow pauses instead of approving.

EC7. A plan remains stable while implementation evidence reports progress in
the change root.

EC8. A test spec remains `active` while proof work is current and becomes
`archived`, `superseded`, or `abandoned` through its owning closeout
transition.

EC9. `$workflow auto: verify` is invoked before implementation exists; target
is active but no future stage is marked ready or complete.

EC10. Verification prerequisites become concrete later; workflow invokes
verification without another public authorization parameter.

EC11. Work needed to reach the target exceeds the accepted change scope;
automation pauses for an owner decision.

EC12. Final verify passes; the run completes before PR.

EC13. Final verify fails; the run pauses without repairing implementation.

EC14. A historical change is read after rollout; no migration write
occurs.

EC15. Pre-adoption nonterminal work resumes; one migration record is written
before any lifecycle continuation.

EC16. A downstream skill edits an upstream artifact; review may detect the
unexpected diff, but deterministic validation does not claim actor
attribution.

EC17. An unknown artifact state appears with otherwise consistent evidence;
validation rejects the unknown value first.

EC18. A change registers two ADRs; both remain valid because unique artifact
IDs and paths distinguish them.

EC19. Two entries use the same path or one kind has two primary entries;
validation fails.

EC20. An interrupted authoring invocation leaves state `authoring`; review
cannot settle it.

EC21. Planned work names M2 as current while M1 remains nonterminal;
validation rejects the inconsistent ordering.

EC22. Automation records an unknown target or run status; validation fails
before mutation.

EC23. A canonical published skill retains an instruction to update an upstream
artifact or requests another public authorization inside an existing target;
skill review blocks publication until the ownership table is restored.

EC24. A boundary-first core dimension is absent, duplicated, or uses an
unknown applicability value; structural validation fails and semantic review
does not infer the missing boundary.

EC25. An example or test proposes behavior not owned by its cited requirement
and boundary; the gap routes to spec revision instead of becoming normative
through the example.

## Non-goals

- Content hashes or blob identities.
- Protected-path manifests or file-write interception.
- Copy-on-write artifact revisions or immutable snapshots.
- A specification issue or amendment state machine.
- Selective reuse of downstream artifacts after upstream revision.
- A hosted workflow-state service or database.
- Background autonomous execution.
- Automatic PR opening, push, publication, release, deployment, or merge.
- Automatic repair after verification failure.
- Migration of every historical change.
- Deterministic attribution of an arbitrary file write to one skill process.
- Making learn evidence normative over the current solution.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| `AC-SLA-001` | Every new or resumed nonterminal change records the exact lifecycle contract-version marker. |
| `AC-SLA-002` | Historical changes remain readable without mutation, and resumed work migrates before writing. |
| `AC-SLA-003` | Governed artifacts contain a stable change-record pointer and no mutable lifecycle or routing state. |
| `AC-SLA-004` | Unique stable artifact IDs support multiple artifacts of one kind, and all state combinations use closed vocabularies. |
| `AC-SLA-005` | Authoring marks only its matching artifact `authoring` before mutation and `review-required` only after completion evidence. |
| `AC-SLA-006` | Review evidence is durable before settlement. |
| `AC-SLA-007` | Each review stage settles only its matching artifact state. |
| `AC-SLA-008` | Independent review settlement leaves `workflow_state` and automation unchanged. |
| `AC-SLA-009` | Approved review outcomes map to the correct artifact-specific settled state. |
| `AC-SLA-010` | Non-approved outcomes map deterministically to `revision-required` or `blocked`. |
| `AC-SLA-011` | Same-review settlement retry is idempotent and conflicting reuse fails closed. |
| `AC-SLA-012` | Workflow pauses on incomplete settlement instead of manufacturing approval. |
| `AC-SLA-013` | `workflow_state` is the sole routing and planned-work live-state owner for governed changes. |
| `AC-SLA-014` | Plans and `docs/plan.md` do not carry mutable current workflow state for governed changes. |
| `AC-SLA-015` | Downstream stages record challenges without editing upstream artifacts or state. |
| `AC-SLA-016` | Substantive owner revision requires fresh review and conservative downstream replay. |
| `AC-SLA-017` | One auto target is the complete repository-local automation boundary through that target. |
| `AC-SLA-018` | No additional public authorization parameter is required at internal risk-class boundaries. |
| `AC-SLA-019` | The automation target never expands fixed stage write ownership. |
| `AC-SLA-020` | Future stages are not marked ready or complete before their prerequisites and evidence exist. |
| `AC-SLA-021` | Real decisions, scope expansion, stale evidence, failed validation, and external actions pause automation. |
| `AC-SLA-022` | Successful verify completes before PR and failed verify pauses without repair. |
| `AC-SLA-023` | Migration is prospective, explicit, one-way, and preserves evidence. |
| `AC-SLA-024` | State validation proves semantic consistency without claiming writer attribution. |
| `AC-SLA-025` | Unknown closed values fail before consistency checks and have regression coverage. |
| `AC-SLA-026` | Canonical skills and generated adapters contain aligned ownership and isolation guidance. |
| `AC-SLA-027` | Closed subject-level co-amendment notices prevent conflicting current authorities without cataloguing unchanged requirements. |
| `AC-SLA-028` | Terminal artifact transitions require closeout evidence, and superseded artifacts identify their replacement. |
| `AC-SLA-029` | Review settlement is permitted only from `review-required`; interrupted authoring remains unreviewable. |
| `AC-SLA-030` | Planned-work milestone, review, remaining-work, and closeout schemas support deterministic bind and resume. |
| `AC-SLA-031` | Automation target and status use one closed schema and legal transitions. |
| `AC-SLA-032` | Canonical published skills, reciprocal notices, and generated adapters agree on the ownership table and closed replaced subjects. |
| `AC-SLA-033` | The boundary-first record classifies all eight core dimensions exactly once and defines every cited boundary exactly once. |
| `AC-SLA-034` | Every example is requirement-owned, every selected interaction follows from defined boundaries, and the test spec maps each boundary and interaction to proof or a blocking gap. |
| `AC-SLA-035` | Test specifications that rely on a replaced status or settlement subject are revised and reviewed before implementation relies on them. |

## Open questions

None.

## Next artifacts

- `spec-review`
- architecture assessment with expected result `architecture-required`
- architecture and ADR updates
- `architecture-review`
- execution plan and `plan-review`
- matching test specification and `test-spec-review`

## Follow-on artifacts

None yet

## Readiness

Ready for `spec-review`.

This boundary-first draft does not activate the new lifecycle model, amend the
current automation runtime, authorize implementation, or claim downstream
readiness.
