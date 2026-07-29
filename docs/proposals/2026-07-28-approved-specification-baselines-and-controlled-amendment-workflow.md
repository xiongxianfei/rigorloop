<!-- Template: proposal-skeleton-v1 -->
<!-- Skill: proposal -->
<!-- Template status: normative -->

# Stage-Owned Lifecycle Artifacts and Change-Local Workflow State

## Status

accepted

## Problem

RigorLoop automation sometimes writes progress, status, review settlement, or
handoff information into an artifact created by an earlier stage. For example,
implementation may update an approved plan, or a review stage may update the
artifact it reviewed.

This causes two problems:

```text
approved artifact changes after review
-> the review no longer describes the reviewed file
```

```text
current workflow state is copied into several artifacts
-> transitions update only some copies
-> the repository reports contradictory state
```

The published skills need a small, portable ownership contract. They do not
need document hashing, protected-path infrastructure, write interception, or a
formal amendment system.

## Goals

- Treat every authoring skill and its review skill as peer stages.
- Give each stage exclusive write ownership of the artifacts it creates.
- Prevent downstream automation from editing upstream artifacts.
- Keep approved plans and other approved artifacts free of execution progress.
- Give each activated artifact a stable pointer to its owning change record.
- Store artifact lifecycle state and current workflow state only in
  `docs/changes/<change-id>/change.yaml`.
- Let each review peer settle only the matching artifact lifecycle field after
  it records its review.
- Let each authoring peer mark only its matching artifact state as requiring
  review before it creates or revises governed content.
- Let `workflow` own routing fields without settling or invalidating artifact
  lifecycle state.
- Route an upstream problem back to the owning authoring stage.
- Require a fresh peer review after an owning stage revises its artifact.
- Make review, resolution, verification, and learn evidence visible to the PR
  reviewer without letting those stages rewrite governing artifacts.
- Let `$workflow auto: <target>` express one bounded repository-local
  continuation intent without requiring another public authorization
  parameter at each internal risk boundary.

## Non-goals

- Do not make approved artifacts permanently unchangeable by their owners.
- Do not add hashes, blob identities, protected-path manifests, or file-write
  interception.
- Do not create copy-on-write revision files or immutable snapshots.
- Do not introduce specification issue and amendment state machines.
- Do not infer which downstream artifacts can be safely reused after an
  upstream revision.
- Do not promise selective downstream reuse as follow-up work.
- Do not turn `change.yaml` into an event log or evidence store.
- Do not make `learn` authoritative over the current solution.
- Do not let review peers update routing, revise reviewed content, or settle
  another artifact's state.
- Do not make an automation target authorize PR creation, push, merge,
  release, deployment, credential access, destructive Git, or external-system
  mutation.
- Do not add a hosted workflow-state service.
- Do not migrate all historical changes.

## Vision fit

fits the current vision

Stage-owned artifacts preserve reviewability. A single change-local state
surface with transition-scoped authority improves traceability and resumability
without adding repository-specific enforcement machinery to published skills.

## Initial intent preservation

| Initial intent | Treatment | Where recorded |
| --- | --- | --- |
| Approved documents are not changed downstream | in scope | Recommended Direction |
| Authoring and review skills are peers | in scope | Peer-stage ownership |
| Review stages do not edit reviewed artifacts | in scope | Peer-stage ownership |
| `docs/plan.md` does not carry current status | in scope | Plan policy |
| Current status lives under the change root | in scope | Change-local lifecycle and workflow state |
| Review approves and settles lifecycle status | in scope | Review-owned settlement |
| Review settlement lives under the change root | in scope | Change-local lifecycle and workflow state |
| Upstream defects can still be corrected safely | in scope | Upstream correction |
| PR reviewers can see learn evidence | in scope | PR and learn boundary |
| Automation continues to its selected repository-local target without another public parameter | in scope | Automation continuation |
| Verify documents with content hashes | rejected option | Non-goals |
| Add a formal amendment mechanism | rejected option | Non-goals |
| Reopen only semantically affected artifacts | out of scope | Non-goals, Scope Budget |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Peer-stage write ownership | core to this proposal | It prevents downstream write-back. |
| Change-local artifact and workflow state | core to this proposal | Lifecycle and routing state need explicit field owners. |
| Review-owned artifact settlement | core to this proposal | A review peer should complete its own gate without editing its target. |
| Upstream correction routing | core to this proposal | Incorrect authority still needs a safe correction path. |
| Fresh review after revision | core to this proposal | An old review cannot settle revised content. |
| PR-visible evidence | core to this proposal | Reviewers need the actual decision and proof trail. |
| Target-bound repository-local automation consent | core to this proposal | Automation should not stop for a redundant public authorization prompt. |
| Governance and workflow updates | same-slice dependency | Current rules assign live state to plans and permit downstream updates. |
| Bounded-review-fix automation spec amendment | same-slice dependency | The current approved spec separates target selection from executable authority. |
| Published-skill updates | same-slice dependency | Stage behavior must use the same ownership rule. |
| Basic state-schema validation | same-slice dependency | Closed states, legal transitions, and evidence consistency prevent ambiguous routing. |
| Historical migration | out of scope | Prospective adoption is sufficient. |
| Hash or protected-path enforcement | out of scope | It is too repository-specific for the published skills. |
| Formal issue and amendment records | out of scope | Normal stage evidence and routing are sufficient initially. |
| Selective downstream reuse | out of scope | Conservative replay keeps the first version simple. |

## Context

Current governance assigns live execution state to an active plan and requires
updates to `docs/plan.md`. Some skills also settle status in artifacts owned by
earlier stages.

This proposal replaces that model:

```text
approved artifacts:
  settled intent

change.yaml:
  artifact lifecycle state and current workflow state

stage-owned evidence:
  findings, progress, decisions, and proof
```

The change therefore requires coordinated updates to the constitution,
workflow contract, and affected skills. It does not require runtime document
protection infrastructure.

## Options Considered

### Option 1: Continue downstream status updates

This keeps current plan and index behavior.

Rejected because status is still part of an upstream file, and a downstream
write makes ownership and review boundaries unclear.

### Option 2: Allow metadata-only upstream edits

Downstream stages could change status and handoff fields but not normative
content.

Rejected because metadata changes can alter lifecycle meaning and still make
the reviewed file differ from the approved file.

### Option 3: Use stage ownership and transition-scoped change-local state

Every stage writes only its own artifacts.
Each authoring peer marks only its matching artifact state as requiring review
when it creates or revises governed content.
Each review peer records its verdict and settles only the matching artifact
state in `change.yaml`.
`workflow` updates only routing state.

Recommended because it is simple, portable, and sufficient for published
skills.

### Option 4: Enforce document identities and protected paths

Automation could calculate hashes and reject writes to registered paths.

Rejected because the operational cost and published-skill complexity are not
justified.
The first version deliberately provides guidance-and-review assurance rather
than deterministic write attribution.

## Recommended Direction

Adopt Option 3.

Use five rules:

```text
1. A stage writes only the artifacts it owns and its explicitly assigned
   transition on the matching artifact-state entry.

2. An authoring peer marks only its matching artifact state as review-required
   before revising settled content.

3. A review peer settles only its matching artifact state after recording
   review evidence.

4. Workflow owns routing state and never settles artifact lifecycle state.

5. A downstream problem is routed to the upstream owner; it is never fixed by
   downstream write-back.
```

### Peer-stage ownership

An authoring skill and its review skill are peers:

| Peer | Owns | Treats as read-only |
| --- | --- | --- |
| `proposal` | Proposal content | Proposal-review evidence |
| `proposal-review` | Proposal-review evidence | Proposal |
| `spec` | Specification content | Spec-review evidence |
| `spec-review` | Spec-review evidence | Specification |
| `architecture` | Architecture and ADR content | Architecture-review evidence |
| `architecture-review` | Architecture-review evidence | Architecture and ADRs |
| `plan` | Plan content | Plan-review evidence |
| `plan-review` | Plan-review evidence | Plan |
| `test-spec` | Test-specification content | Test-spec-review evidence |
| `test-spec-review` | Test-spec-review evidence | Test specification |
| `implement` | Code, tests, and implementation evidence | Code-review evidence |
| `code-review` | Code-review evidence | Implementation outputs |

The same rule applies to later stages:

- `review-resolution` owns disposition evidence;
- `explain-change` owns change rationale;
- `verify` owns verification evidence;
- `learn` owns retrospective evidence; and
- `pr` owns the PR handoff.

None of these stages repairs another stage's artifact.

### Change-local lifecycle and workflow state

After activation, lifecycle-managed artifacts do not contain mutable status
fields.
At creation, each artifact records a stable change ID or lifecycle-record path
so a reader can find its current state without relying on repository search.
That pointer does not mirror the state and does not change during normal
lifecycle transitions.

`docs/changes/<change-id>/change.yaml` contains both settled artifact state and
the small current workflow snapshot.
For example:

```yaml
artifact_states:
  proposal:
    lifecycle_state: accepted
    review: proposal-review-r1

workflow_state:
  lifecycle_state: active
  current_stage: implement
  next_stage: code-review
  blocker: none
  evidence:
    - docs/changes/2026-07-28-example/implementation-m1.md
```

The review peer records only its verdict.
It does not change the reviewed artifact.
After recording durable review evidence, it updates only the matching
`artifact_states.<artifact>` entry.
`workflow` separately updates `workflow_state` and continues or pauses from
the settled result.

Ownership is transition-scoped because `change.yaml` is shared:

| Writer | Writable surface | Prohibited surface |
| --- | --- | --- |
| Authoring peer | Its authored artifact, owned evidence, and its matching state transition to `review-required` | Review evidence, settled approval state, other artifact states, workflow routing |
| Review peer | Its review evidence and evidence-backed settlement of its matching artifact state | Reviewed content, other artifact states, workflow routing |
| `workflow` | `workflow_state` | Artifact lifecycle state, reviewed content, review verdicts |
| Later stages | Their own evidence | Upstream artifacts, upstream settlement, workflow routing |

Review settlement uses an artifact-specific mapping:

| Review result | Proposal | Spec | Architecture | Plan | Test spec |
| --- | --- | --- | --- | --- | --- |
| `approved` | `accepted` | `approved` | `approved` | `active` | `active` |
| `changes-requested` | `revision-required` | `revision-required` | `revision-required` | `revision-required` | `revision-required` |
| `blocked` or `inconclusive` | `blocked` | `blocked` | `blocked` | `blocked` | `blocked` |

The review record preserves the exact review outcome, so the artifact state
does not need to duplicate every review vocabulary.
Unknown artifact kinds, review outcomes, lifecycle states, or transitions fail
closed.

Settlement order is fixed:

This produces a finite settlement sequence:

```text
authoring peer writes content
-> review peer records verdict
-> review peer verifies required finding closeout
-> review peer settles only the matching artifact state
-> workflow records routing
-> workflow routes forward
```

The evidence write precedes settlement.
If settlement is interrupted, retrying the same review reconciles its matching
state from the recorded evidence instead of rerunning or inventing a verdict.
Workflow detects incomplete settlement and pauses; it does not settle on the
review peer's behalf.
Repeating settlement with the same review ID is idempotent.

A later owner revision leaves the earlier review as historical evidence.
Workflow records the route to the owning authoring stage.
Before changing settled content, the authoring peer changes only its matching
artifact state to `review-required`.
The owner then revises the artifact, and fresh review is required before
downstream reliance.

An independently invoked review follows the same settlement sequence:

```text
review target
-> write durable review evidence
-> settle matching artifact state in change.yaml
-> stop without changing workflow_state
```

When workflow automation invoked the review, workflow reads the settled state,
updates routing, and continues.

`change.yaml` does not duplicate full findings, rationale, command output, or
history. Git and the linked stage-owned artifacts preserve that evidence.

This proposal itself retains its embedded `Status` while it is governed by the
current pre-activation contract.
Prospective activation removes embedded mutable status from newly governed
artifacts; historical artifacts are not rewritten.

### Plan policy

An approved plan records stable execution intent:

- scope;
- sequence;
- dependencies;
- validation strategy;
- recovery approach; and
- milestone definitions.

Implementation progress, current milestone, review status, blockers,
validation results, and next stage belong in change-local state or
stage-owned evidence. Implementation does not write them into the approved
plan.

`docs/plan.md` becomes static navigation rather than a current-work registry:

```md
# Plan navigation

- Approved plans: `docs/plans/`
- Current state: `docs/changes/<change-id>/change.yaml`
```

If a current-work list is useful, a repository command may generate an
untracked view from `change.yaml` files. The generated view is not another
state owner.

### Upstream correction

When a downstream stage finds an upstream problem, it records the problem in
its own evidence and stops if the problem blocks safe or truthful progress.
`workflow` records the blocker and routes the issue to the upstream owner.

The owner chooses one of three outcomes:

| Outcome | Action |
| --- | --- |
| Downstream defect | Keep the upstream artifact unchanged and fix the consumer. |
| Deferred improvement | Keep the current artifact and create follow-up work. |
| Upstream defect | Route to the owning authoring stage for revision and fresh peer review. |

The owning authoring stage revises its canonical artifact. Git preserves the
previous reviewed revision; no separate snapshot or content hash is required.

After fresh approval, the simple first version resumes from the stage after
the revised artifact and reruns later stages.
Selective downstream reuse is outside this proposal.

### Automation continuation

`$workflow auto: <target>` is the user's bounded consent to perform the
repository-local stages required to reach that target for the selected change.
It is not blanket authority outside the repository.

The workflow still derives one stage-scoped internal capability only when the
stage's concrete inputs, paths, and review basis exist.
The capability remains single-use and fails closed on stale evidence, expanded
scope, an owner decision, or an invalid transition.
The simplification is public: the user does not provide another authorization
parameter or repeat the same consent at authoring, implementation, and
verification boundaries.

For example:

```text
$workflow auto: verify
-> proposal-review records evidence and settles proposal state
-> workflow derives the next basis-complete repository-local capability
-> spec and later required stages continue
-> verify runs when its concrete basis exists
-> workflow stops before pr
```

The command does not create future stage capabilities early.
It records target-bound consent once and derives each capability just in time.
Automation pauses only for a real owner decision, material unresolved finding,
scope or path expansion, stale or contradictory evidence, failed or
inconclusive validation, cancellation, or an external or destructive action.

This intentionally amends the approved bounded-review-fix contract that
currently treats target selection as separate from risk-class authorization.
The downstream spec must update that normative owner and its compatibility
adapters; skill text alone cannot make this change.

### PR and learn boundary

The PR handoff links the current `change.yaml` state and relevant stage-owned
evidence, including review findings, resolutions, verification, and learn
records.

A PR reviewer may use learn evidence to request a revision. That request is
routed to the stage that owns the affected solution artifact, followed by the
normal peer review. `learn` does not edit the solution, approve the revision,
or advance workflow state.

## Expected Behavior Changes

- Approved artifacts are stable inputs to downstream automation.
- Review skills record verdicts without editing their review targets.
- Review skills settle only their matching artifact lifecycle state after
  review evidence is durable.
- Downstream stages no longer update status in plans or other upstream files.
- Activated artifacts no longer contain mutable lifecycle status.
- `change.yaml` is the only artifact-lifecycle and workflow-state owner.
- Authoring peers own matching transitions to `review-required`, review peers
  own evidence-backed settlement, and `workflow` owns routing.
- Plans retain approved intent rather than becoming execution journals.
- Upstream defects return to their owning authoring stage.
- Revised artifacts receive fresh peer review.
- PR reviewers can inspect linked learn evidence and request owner-routed
  changes.
- `$workflow auto: <target>` continues through basis-complete repository-local
  stages without another public authorization parameter.
- Published skills remain portable and contain no hashing or file-protection
  mechanism.

## Architecture Impact

An architecture assessment is recommended because the proposal changes
workflow state ownership, but no runtime service or document-protection design
is expected.

| Surface | Expected impact |
| --- | --- |
| Constitution | Replace plan-owned live state and downstream settlement rules. |
| Workflow specification | Define stage ownership, routing, and transition-scoped `change.yaml` ownership. |
| Bounded-review-fix specification | Make one target command sufficient consent for just-in-time repository-local capabilities. |
| Change metadata | Add small `artifact_states` and `workflow_state` blocks. |
| Artifact templates | Replace mutable status with a stable change-record pointer after activation. |
| Plans and `docs/plan.md` | Remove mutable workflow-state responsibility. |
| Stage and review skills | Declare owned outputs and read-only inputs. |
| PR handoff | Link current state and stage-owned evidence. |
| Generated adapters | Rebuild from canonical skill sources. |
| Runtime deployment | No change. |

## Testing and Verification Strategy

The downstream specification and test specification should cover these
behavioral cases:

| Scenario | Expected behavior |
| --- | --- |
| Review requests a proposal change | Review records a finding; workflow routes to proposal. |
| Reader opens an activated artifact | Its stable pointer resolves to the authoritative change record. |
| Implementation discovers a plan defect | Implementation records and reports it; plan remains unchanged. |
| Implementation reports progress | Evidence is written under the change root, not into the plan. |
| Review approves an artifact | Review records evidence, then settles only its matching state field. |
| Review requests changes | Review records evidence, sets the matching state to `revision-required`, and workflow routes to the owner. |
| Review settlement is retried | The same review ID produces an idempotent matching state. |
| Settlement contradicts review evidence | State consistency validation fails closed. |
| An isolated review settles an artifact | It updates only the matching artifact state and stops without changing `workflow_state`. |
| A non-review stage completes | It writes owned evidence; workflow updates routing only. |
| An owning stage revises an approved artifact | It first marks its matching state `review-required`; the prior review becomes historical and peer review repeats. |
| `$workflow auto: verify` starts before later bases exist | Target-bound consent persists; stage capabilities are derived just in time without another public parameter. |
| Automation reaches a real decision or external boundary | It pauses without widening authority. |
| Learn identifies a solution defect during PR review | The owning solution stage revises; learn remains unchanged evidence. |
| PR handoff is prepared | It links current state, reviews, resolutions, verification, and relevant learn evidence. |
| Historical change lacks the new state block | It remains valid unless explicitly migrated. |

Canonical skill validation should check that published skills declare their
owned outputs, read-only inputs, matching settlement field, and route-back
behavior.
Generated adapter parity should prove that the same guidance is shipped.
State validation should reject unknown artifacts, outcomes, states,
illegal transitions, settlement without matching review evidence, and forward
routing without a settled artifact state.

Review and verification may flag unexpected upstream changes visible in the
actual diff, but a final diff does not attribute a write to a specific stage.
The first version therefore claims guidance-and-review assurance, not
deterministic enforcement.
No content hash, path-protection validator, or stage-write interception is
required.

## Rollout and Rollback

Adopt the rule prospectively for new changes.
Update governance, lifecycle templates, change metadata, workflow, canonical
skills, and generated adapters together so published guidance does not
describe mixed ownership.

Existing active changes may finish under the old contract or opt into a
documented one-time migration. One change should not mix the two state models.

If rollback is required:

- stop automated progression for changes using the new state model;
- preserve `change.yaml` and all stage-owned evidence;
- return routing to explicit human control; and
- do not grant downstream stages permission to rewrite upstream artifacts.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Skills accidentally retain old write-back instructions. | Update canonical skills together and validate generated adapter parity. |
| `change.yaml` becomes another large artifact. | Keep only the current snapshot and evidence links. |
| Multiple skills write one YAML file. | Assign closed transition authority, require evidence-first settlement, and validate semantic state consistency. |
| Review settlement and routing diverge after interruption. | Make same-review settlement idempotent; workflow pauses until the review peer completes settlement. |
| Contributors lose progress detail from plans. | Link stage-owned progress evidence from `change.yaml`. |
| Removing embedded status harms standalone discoverability. | Put one stable change-record pointer in each activated artifact. |
| Conservative replay repeats unaffected work. | Accept the extra work as the explicit simplicity tradeoff for v1. |
| Guidance does not mechanically prevent every write. | Keep ownership explicit, surface unexpected upstream diffs in review, and avoid claiming deterministic enforcement. |
| A blocking upstream defect is ignored. | Require the discovering stage to stop and route through workflow. |
| Learn becomes an informal change authority. | Route reviewer requests to the owning authoring and review peers. |
| Historical changes fail new expectations. | Activate prospectively without mass migration. |
| One target command is mistaken for external authority. | Limit it to the selected change and repository-local target; stop before PR and all external or destructive actions. |

## Open Questions

None block proposal review.

The downstream specification should settle:

- the minimal `workflow_state` fields and closed values;
- the minimal `artifact_states` fields and artifact-specific settled values;
- the allowed workflow transitions;
- the exact transition registry and evidence-first reconciliation rule;
- the target-bound consent record and just-in-time capability derivation rules;
- the names and locations of stage-owned execution evidence; and
- the prospective activation marker and template migration.

These details must not introduce a document identity or write-protection
mechanism.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-07-28 | Treat authoring and review skills as peers. | Each peer needs independent evidence ownership. | Review editing its target. |
| 2026-07-28 | Prohibit downstream writes to upstream artifacts, including status. | Metadata write-back still changes reviewed authority. | Metadata-only edits. |
| 2026-07-28 | Put artifact lifecycle state and current workflow state only in `change.yaml`. | One location avoids contradictory projections and status settlement loops. | Artifact-, plan-, or distributed state. |
| 2026-07-28 | Give review peers matching artifact-state settlement authority and give `workflow` routing authority. | Transition-scoped ownership lets an independent review complete its gate without editing its target or letting workflow reinterpret the verdict. | Workflow settling every artifact; every stage updating arbitrary state. |
| 2026-07-28 | Let an authoring peer mark its matching artifact state `review-required` before revision. | Independent authoring must invalidate prior settlement before changing governed content. | Workflow invalidation; leaving settled state current during revision. |
| 2026-07-28 | Move artifact lifecycle status to `change.yaml`. | Review can approve without editing its target or creating a status-settlement loop. | Review-owned or author-settled embedded status. |
| 2026-07-28 | Keep one stable change-record pointer in each activated artifact. | Readers need discoverability without a second mutable state owner. | Embedded mirrored status; repository search only. |
| 2026-07-28 | Route upstream correction to its authoring owner and peer review. | Correction remains possible without violating ownership. | Downstream repair. |
| 2026-07-28 | Make v1 a guidance-and-review contract. | Portable skills cannot attribute writes from a final diff without extra machinery. | Deterministic stage-write enforcement. |
| 2026-07-28 | Exclude selective downstream reuse. | Conservative replay avoids dependency-analysis machinery and unowned follow-up work. | Deferred selective-reuse proposal. |
| 2026-07-28 | Keep learn visible but non-authoritative. | Reviewers can use lessons without letting learn rewrite the solution. | Learn-owned revisions. |
| 2026-07-28 | Treat `$workflow auto: <target>` as bounded repository-local continuation consent. | Just-in-time internal capabilities preserve scope checks without another public authorization parameter or redundant stop. | Separate public authorization prompts at each risk boundary; blanket external authority. |

## Next Artifacts

```text
proposal-review
-> stage ownership and change-local workflow-state specification
-> bounded-review-fix automation contract amendment
-> spec-review
-> architecture assessment
-> architecture and architecture-review when required by the assessment
-> plan
-> plan-review
-> test-spec
-> test-spec-review
-> implementation and code-review
-> explain-change
-> verify
-> pr
```

## Follow-on Artifacts

- [Stage-Owned Lifecycle Artifacts and Change-Local Workflow State specification](../../specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md)

## Readiness

Accepted by `proposal-review-r4`.
Ready for specification authoring.

The proposal now defines transition-scoped authoring and review state,
workflow-owned routing, and target-bound repository-local continuation without content
hashes, protected paths, snapshots, a formal amendment workflow, or another
public authorization parameter.
