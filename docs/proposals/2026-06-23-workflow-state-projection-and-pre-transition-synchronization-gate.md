# Workflow-State Projection and Pre-Transition Synchronization Gate

## Status

accepted

## Problem

RigorLoop already has a single-source workflow-state contract: for planned initiatives, the active plan's `Current Handoff Summary` owns live state. PR #38 merged that ownership direction through the Single Source of Workflow State initiative.

The remaining problem is enforcement. Mutable lifecycle facts are still copied manually into projections, summaries, evidence records, and narrative sections. A stage transition can update the owner while leaving `Readiness`, `docs/plan.md`, change metadata, review evidence, or milestone sections stale until a reviewer catches the contradiction.

Recurring drift has included:

- `Current Handoff Summary` moving to review resolution while `Readiness` still routed to code review.
- partial fixes that updated the active plan but left change metadata or review evidence stale.
- milestone body state diverging from the owner state.
- stale review-round or next-stage wording surviving in live-state surfaces.

This is a tooling and artifact-role problem, not primarily a contributor-discipline problem. The owner exists, but projections and evidence surfaces are still synchronized by hand.

## Goals

- Preserve `Current Handoff Summary` as the sole owner of live planned-initiative state.
- Define one owner for every other mutable readiness or evidence fact.
- Classify related artifacts as owner, projection, pointer, ledger, or evidence.
- Eliminate narrative restatement of live state outside the owner.
- Make `Readiness` a stable pointer instead of a second next-stage statement.
- Make `docs/plan.md` a mechanically comparable projection.
- Treat the active milestone's `Milestone state` as a projection of the owner.
- Add a pre-transition state-sync gate before downstream readiness claims.
- Add deterministic cross-surface validation for owner/projection/evidence agreement.
- Detect stale prior-stage wording in bounded live-state surfaces before handoff.
- Validate review summaries against review-log and review-resolution state.
- Bind the synchronization gate to the stage handoff path so a failed gate blocks downstream stage claims.
- Preserve append-only history and durable evidence.
- Keep historical plans and completed review records valid.

## Non-goals

- Do not change the standard workflow stage order.
- Do not make `docs/plan.md` the live-state owner.
- Do not make `change.yaml` the live next-stage owner.
- Do not derive current next stage from `review-log.md` or `review-resolution.md`.
- Do not remove review logs, review resolutions, progress history, or validation evidence.
- Do not rewrite historical plans solely to adopt the new format.
- Do not parse arbitrary prose to infer lifecycle state.
- Do not make raw whole-repository grep authoritative.
- Do not let automatic synchronization alter review findings or dispositions.
- Do not let automatic synchronization claim validation, branch readiness, or PR readiness.
- Do not replace `verify` ownership of branch readiness or `pr` ownership of PR readiness.
- Do not add a hosted workflow service, database, or external control plane.
- Do not hand-edit generated skill or adapter output.

## Vision fit

fits the current vision

RigorLoop depends on repository artifacts being sufficient to resume and review work without reconstructing state from chat. That promise is weakened when several files claim different current stages.

This proposal strengthens traceability by enforcing a narrower rule: write live state once, project it mechanically, record history append-only, record evidence under its owning stage, and validate synchronization before transition.

## Context

This is a follow-up hardening slice to [Single Source of Workflow State](2026-05-09-single-source-of-workflow-state.md), not a new workflow-state ownership decision.

The current constitution already says the active plan `Current Handoff Summary` owns live state and that state-changing handoffs perform a state-sync check before downstream readiness is claimed. The approved single-source spec defines the same owner boundary and intentionally avoided broad semantic validators in its first implementation slice.

The next step is to make the remaining repeated values mechanical and to fail transitions before review or downstream handoff when surfaces contradict the owner.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| One owner per volatile fact | in scope | Fact ownership matrix |
| `Current Handoff Summary` owns live plan state | in scope | Recommended direction |
| Replace duplicated prose with references | in scope | Pointer and projection contracts |
| Classify artifact roles | in scope | Artifact-role model |
| Make mirrors mechanical | in scope | Mechanical projection contracts |
| Add pre-transition checklist | in scope | Pre-transition synchronization gate |
| Automate cross-surface invariants | in scope | Cross-surface validator |
| Scan for stale stage tokens | in scope | Stale-token detection |
| Preserve ledgers and evidence | in scope | Artifact-role model |
| Avoid relying on discipline alone | in scope | Recommended direction |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| State ownership matrix | core to this proposal | Validation needs one owner per mutable fact. |
| Exact `Current Handoff Summary` schema | core to this proposal | The live owner must be deterministically parseable. |
| `docs/plan.md` projection normalization | core to this proposal | The plan index currently mirrors live state. |
| Active milestone-state projection check | core to this proposal | This is a recurring drift surface. |
| Readiness pointer rule | core to this proposal | Narrative readiness duplication has repeatedly drifted. |
| Review evidence consistency | core to this proposal | Open findings should block incompatible state. |
| Pre-transition validator | core to this proposal | This is the highest-leverage enforcement point. |
| Bounded stale-token check | core to this proposal | It detects adjacent live-state drift without corrupting history. |
| Workflow and directly affected skill guidance | same-slice dependency | The gate needs to run at actual transition points. |
| Active/blocked plan migration audit | core to this proposal | Baseline audit on 2026-06-23 found 2 active entries and 0 blocked entries in `docs/plan.md`; the first slice should size and normalize that bounded set before enforcement. |
| Automatic projection writer | deferable follow-up | Useful after the read-only validation contract is stable. |
| Historical plan migration | out of scope | Historical artifacts are evidence, not live state. |
| New change-metadata schema | first-slice candidate | Add only if current compact fields cannot express derived summaries. |

## Options Considered

### Option 1: Keep manual synchronization with clearer guidance

This keeps the current single-source owner and relies on agents to update all affected surfaces by checklist.

Advantages:

- No new parser or validator complexity.
- No migration pressure on active artifacts.
- Lowest immediate implementation cost.

Disadvantages:

- Repeats the failure mode that prompted this proposal.
- Review remains the first reliable synchronization check.
- Narrative mirrors stay difficult to compare.

### Option 2: Add a broad semantic validator across workflow artifacts

This attempts to infer state from plan prose, change metadata, review records, and other artifacts.

Advantages:

- Could catch many drift cases.
- Requires less artifact format normalization up front.

Disadvantages:

- Risks false positives from historical ledgers.
- Encourages arbitrary-prose inference instead of a stable contract.
- Makes validators responsible for deciding which duplicated claim is authoritative.

### Option 3: Define owner/projection/pointer/ledger/evidence roles and validate bounded fields

This keeps `Current Handoff Summary` as owner, makes repeated live-state values mechanical projections, and validates only structured fields and bounded live-state surfaces.

Advantages:

- Reinforces the existing ownership model instead of replacing it.
- Avoids parsing arbitrary prose.
- Preserves historical review and progress text.
- Fails incomplete transitions before review handoff.
- Creates a stable base for a later projection writer.

Disadvantages:

- Requires normalizing active and blocked plan projections.
- Requires parser and fixture work.
- Requires affected stage guidance to call the gate consistently.

## Recommended Direction

Choose Option 3.

Amend the existing Single Source of Workflow State contract so it distinguishes five artifact roles:

| Role | Meaning |
| --- | --- |
| Owner | Authoritative source for one mutable fact. |
| Projection | Compact, mechanically comparable mirror of owner state. |
| Pointer | Reference to the owner without restating live state. |
| Ledger | Append-only or event-oriented history. |
| Evidence | Stage-owned proof of a bounded outcome. |

For planned initiatives, the active plan `Current Handoff Summary` remains the owner of:

- current milestone;
- current milestone state;
- current review status;
- remaining in-scope implementation milestones;
- next stage;
- final-closeout readiness;
- reason final closeout is or is not ready.

No other artifact should independently own those facts.

`Last reviewed milestone` should be derived from formal review evidence instead of stored as a second live fact. The handoff summary may include a pointer to latest review evidence, but it should not own a separately maintained last-reviewed milestone value.

The first-slice projections should be:

- the active or blocked row in `docs/plan.md`;
- the current milestone's `Milestone state` field.

The active plan `Readiness` section should become a pointer:

```md
## Readiness

See `Current Handoff Summary` for current milestone, next stage, and
final-closeout readiness.

Readiness is not Done.
```

## Fact Ownership Matrix

| Fact | Owner | Allowed projections or evidence |
| --- | --- | --- |
| Current milestone | `Current Handoff Summary` | `docs/plan.md`, milestone heading |
| Current milestone state | `Current Handoff Summary` | active milestone `Milestone state` |
| Current review status | `Current Handoff Summary` | compact `change.yaml` review summary |
| Last reviewed milestone | formal review evidence and `review-log.md` | `Current Handoff Summary` may point to latest review evidence |
| Next stage | `Current Handoff Summary` | one normalized `docs/plan.md` field |
| Final-closeout readiness | `Current Handoff Summary` | no narrative mirror |
| Milestone history | `Progress` | review records and commits |
| Review event status | owning review record | `review-log.md` |
| Finding disposition | `review-resolution.md` | compact unresolved count in `change.yaml` |
| Validation result | owning validation evidence | `change.yaml` validation event |
| Branch readiness | `verify` | PR may cite it |
| PR body/open readiness | `pr` | PR artifact |
| Final rationale | `explain-change` | change metadata pointer |

## Canonical Current Handoff Summary

Use stable keys:

```md
## Current Handoff Summary

- Current milestone: <milestone or lifecycle gate>
- Current milestone state: <planned | implementing | review-requested | resolution-needed | closed>
- Latest review evidence: <review-log pointer, review record pointer, or none>
- Review status: <review-stage> <round-or-none> <status>
- Remaining in-scope implementation milestones: <ordered list or none>
- Next stage: <normalized stage and optional bounded target>
- Final closeout readiness: <ready | not ready>
- Reason final closeout is or is not ready: <reason-code> - <bounded detail>
```

The downstream spec should settle exact enums. Candidate `Review status` values should be enum-like, such as `not-run`, `requested`, `clean`, `changes-requested`, `resolved-pending-rereview`, and `blocked`. Candidate final-closeout reason codes should distinguish open implementation milestone, open review finding, missing final rationale, missing verify evidence, missing PR handoff, blocked external event, and ready.

The validator should parse only the heading, exact bullet labels, and field values. Missing, duplicated, or unparseable required fields should fail closed. Stale-token fixtures should exercise both `Review status` and the final-closeout reason field, because those fields are the highest-risk bounded text remaining in the owner.

## Mechanical Projection Contracts

Normalize active and blocked entries in `docs/plan.md` to a stable Markdown table:

```md
| Plan | State | Next stage | Change ID |
| --- | --- | --- | --- |
| [<title>](plans/<plan>.md) | active | <normalized value> | `<change-id>` |
```

The validator should compare `State`, `Next stage`, and `Change ID` against the active plan owner. It should not compare descriptive title wording. The table avoids delimiter ambiguity in list-row `key: value` parsing and gives reviewers one deterministic projection unit per plan.

For the current milestone, `Milestones/<current milestone>/Milestone state` should match `Current Handoff Summary/Current milestone state`. Closed previous milestones remain historical and are not rewritten.

The validator should reject current stage, review-round, or next-stage restatement in `Readiness`, while accepting a pointer to `Current Handoff Summary` and stable explanatory text such as `Readiness is not Done`.

## Pre-Transition Synchronization Gate

Run the synchronization gate after stage-owned evidence is updated and before downstream readiness is claimed, review is requested, `verify` runs, or PR handoff starts.

For every lifecycle transition:

1. Update `Current Handoff Summary`.
2. Update the active milestone-state projection.
3. Update the `docs/plan.md` projection.
4. Keep `Readiness` as a pointer.
5. Append dated `Progress` history.
6. Append the formal review event to `review-log.md`, when applicable.
7. Update finding dispositions and closeout in `review-resolution.md`, when applicable.
8. Update compact review/validation summaries and evidence pointers in `change.yaml`.
9. Run cross-surface state validation.
10. Run bounded stale-token detection.
11. Claim readiness for the next stage only after the gate passes.

A partial transition remains blocked until synchronization is complete.

## Enforcement Binding

The gate is a binding precondition, not advisory guidance.

First-slice enforcement should bind at three layers:

- stage skills treat a failing state-sync validator as a blocker for the next-stage handoff sentence;
- `verify` treats a failing state-sync validator as blocking branch readiness for touched, referenced, active, or blocked workflow-state artifacts;
- CI or repository-owned validation runs the same artifact-lifecycle state-sync mode for PRs that touch active plans, `docs/plan.md`, change metadata, review artifacts, workflow guidance, or the state-sync validator.

The proposal does not require a local pre-commit hook in the first slice. A hook may be added as a contributor convenience later, but it should not be the only enforcement point because hooks are optional in many contributor environments.

On gate failure, the agent should leave no silent partial transition. It should either revert its own in-progress owner/projection edits before handing back or record the failure as the current blocker and make the next action re-running the gate and resolving the named inconsistency.

## Cross-Surface Validator

Implement lifecycle-state synchronization inside the artifact-lifecycle validation boundary instead of creating a competing workflow-state contract.

Recommended structure:

```text
scripts/lifecycle_state_sync.py
scripts/validate-artifact-lifecycle.py
scripts/test-artifact-lifecycle-validator.py
```

A dedicated top-level command is acceptable only as a thin wrapper around the shared parser and comparison module.

For a planned initiative, validation inputs should include:

- active plan body;
- `docs/plan.md`;
- `change.yaml`;
- `review-log.md`, when present;
- `review-resolution.md`, when present or required;
- latest relevant review record.

Core invariants:

- owner fields parse exactly once;
- active milestone exists;
- active milestone state matches owner;
- `docs/plan.md` table row exists exactly once;
- `docs/plan.md` projection matches owner;
- `Readiness` does not restate live next stage;
- open material findings are consistent across log, resolution, and metadata;
- `resolution-needed` is used when accepted material findings remain open;
- `review-requested` is not used while required dispositions remain unresolved;
- a closed milestone is not the current `resolution-needed` milestone;
- final-closeout readiness is `not ready` while milestones or findings remain open.

## Review Consistency Contract

This proposal uses the repository's existing review contract for materiality. A material finding is a formal lifecycle review finding that requires durable detailed review evidence and disposition tracking before it can drive fixes or downstream routing. The downstream spec amendment should define the exact mapping from review-record fields, severity labels, and dispositions to `material`, `open`, and `closed`.

If formal review evidence contains unresolved material findings, the owner state should remain:

```text
Current milestone state: resolution-needed
Final closeout readiness: not ready
```

The next stage should be a bounded resolution route rather than a downstream lifecycle gate.

A finding counts as closed only when review-log indexes it, review-resolution records final disposition, the required corrective action or accepted exception is present, required validation evidence is recorded, and no later review reopens it.

`change.yaml` may contain derived fields such as review status summary, unresolved finding count, latest validation state, and artifact pointers. The validator should derive expected values from review artifacts and reject mismatches. It should not derive the live next stage from `change.yaml`.

## Stale-Token Detection

Historical ledgers legitimately contain old stage names and review rounds. A whole-repository ban would corrupt or falsely reject history.

Before readiness handoff, stale-token detection should:

1. Capture the previous owner state.
2. Derive tokens that should no longer appear as live claims.
3. Scan only `Current Handoff Summary`, the active milestone-state block, `Readiness`, the current `docs/plan.md` row, compact live-state fields in `change.yaml`, and changed current-state lines.
4. Exclude ledgers and historical review evidence.
5. Report stale tokens with path, line, expected owner value, and replacement.

Candidate stale tokens include old next stage, old milestone state, old review round, old review result, old final-readiness value, and retired lifecycle labels. Raw `rg` remains useful as a diagnostic, but parser-scoped checking owns the gate decision.

## Optional Projection Writer

After the read-only contract is stable, add a dry-run writer:

```bash
python scripts/sync-workflow-state.py \
  --plan docs/plans/<plan>.md \
  --write-projections
```

It may update only:

- `docs/plan.md` projection;
- current milestone-state projection;
- `Readiness` pointer shape.

It should not modify review logs, review resolutions, review records, validation evidence, finding dispositions, verify evidence, or PR evidence.

The validator remains authoritative even if the writer exists. Writer tests should use hand-authored golden fixtures for before/after projection edits, not only "writer output passes validator", so the writer cannot satisfy the parser while losing intended human meaning.

## Expected Behavior Changes

- Lifecycle-state transitions fail earlier when surfaces disagree.
- `Readiness` stops repeating current stage details.
- `docs/plan.md` table rows become deterministic projections.
- Review-log and review-resolution remain historical or evidence surfaces.
- Current milestone state cannot drift from the handoff owner.
- Open review findings block incompatible readiness automatically.
- Historical evidence remains intact.
- Stage ownership and workflow order remain unchanged.

Success metric: after rollout, state-drift findings in proposal-review, plan-review, code-review, verify, and PR handoff for active/blocked workflow-state transitions should drop to zero for the next 10 formal reviews or the next 30 calendar days, whichever produces more evidence. If review cadence is slow, a partial window with zero findings at 30 days is still a positive signal, but any drift finding in that window should be treated as either a validator coverage gap or a transition-binding gap.

## Architecture Impact

| Surface | Impact |
| --- | --- |
| Active plan contract | Clarify owner and projections. |
| Plan skeleton/assets | Replace narrative readiness with pointer text. |
| `docs/plan.md` format | Normalize active/blocked projection fields. |
| Workflow skill | Require pre-transition synchronization gate. |
| Plan, implement, and review-resolution skills | Add transition responsibilities. |
| Artifact lifecycle validator | Add cross-surface semantic checks. |
| Change metadata validation | Reuse or expose compact derived review fields. |
| Review artifacts | No schema change unless current summaries are insufficient. |
| Generated skills/adapters | Rebuild if canonical skill text changes. |
| Runtime application | No change. |

No new service, storage, network, deployment, or security boundary is introduced.

## Testing and Verification Strategy

| Check ID | What is verified |
| --- | --- |
| `WSS-001` | `Current Handoff Summary` is the only live planned-state owner. |
| `WSS-002` | Missing or duplicate owner fields fail. |
| `WSS-003` | Current milestone state matches the milestone projection. |
| `WSS-004` | `docs/plan.md` state matches the owner. |
| `WSS-005` | `docs/plan.md` next stage matches the owner exactly. |
| `WSS-006` | `Readiness` points to the owner and does not restate a live stage. |
| `WSS-007` | Fixture pair proves historical stage tokens are allowed in `Progress` and `review-log.md` while the same stale tokens are rejected in `Current Handoff Summary`, `Readiness`, and the `docs/plan.md` projection row. |
| `WSS-008` | Open material findings force `resolution-needed`. |
| `WSS-009` | Open findings force final-closeout readiness to `not ready`. |
| `WSS-010` | Resolved findings plus validation permit `review-requested`. |
| `WSS-010a` | `resolved-pending-rereview` does not permit downstream gates until a clean rereview closes the review loop. |
| `WSS-011` | `change.yaml` unresolved counts match review evidence. |
| `WSS-012` | A stale current review round is detected. |
| `WSS-012a` | Fixture pair proves stale review status and final-closeout reason text are detected inside bounded owner fields while valid bounded text is accepted. |
| `WSS-013` | Historical review-round references are not falsely rejected. |
| `WSS-014` | Clean non-final review closes the old milestone and routes to the next. |
| `WSS-015` | Final milestone closeout still routes through explain-change, verify, and PR. |
| `WSS-016` | Branch readiness remains owned by verify. |
| `WSS-017` | PR readiness remains owned by PR. |
| `WSS-018` | Projection writer, if added, cannot modify ledger or evidence files. |

Create `docs/changes/<change-id>/behavior-preservation.md` with a matrix proving that workflow stage order, current state ownership, plan index role, review log role, review-resolution role, change metadata role, verify ownership, PR ownership, and historical-plan validity are preserved.

## Rollout and Rollback

Rollout:

1. Audit active and blocked plans for live-state duplication.
2. Amend the existing Single Source of Workflow State contract instead of creating a competing ownership spec.
3. Add test-spec coverage for owner/projection/ledger/evidence semantics.
4. Normalize the plan skeleton and current example plan.
5. Add cross-surface parser and validator fixtures.
6. Add pre-transition validation to workflow-managed handoff guidance.
7. Apply the contract to active and blocked plans.
8. Update only directly affected canonical skills.
9. Rebuild and validate generated skills/adapters when needed.
10. Run cold transition exercises for implementation to review, changes requested to resolution, resolution to re-review, clean milestone to next milestone, and final closeout to verify and PR.

Rollback:

- Restore the prior plan/index formatting together.
- Keep append-only review and progress history unchanged.
- Remove the new enforcement mode if it produces unresolved false positives.
- Do not restore competing live-state ownership.
- Preserve fixture evidence and review findings.
- Do not automatically rewrite historical plans during rollback.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Validator overfits narrative prose | Parse exact fields and bounded sections only. |
| Historical stage tokens trigger false positives | Exclude ledgers and review history from live-state scans. |
| `docs/plan.md` becomes overly machine-oriented | Keep human-readable links and compact exact fields. |
| Change metadata becomes a second owner | Treat fields as derived evidence only. |
| Automatic writer changes evidence | Restrict writer to projections and default to dry-run. |
| Transition checklist adds ceremony | Invoke one validator command instead of relying on manual inspection. |
| Legacy plans cannot satisfy new structure | Enforce active/blocked or newly transitioned plans initially. |
| Review evidence is ambiguous | Fail closed and require stage-owned correction. |

## Open Questions

1. Should `docs/plan.md` use one-line list rows or a Markdown table?

   Answer: start with a Markdown table for active and blocked projections. It is more robust for deterministic parsing than semicolon-delimited list rows and still remains readable. The spec amendment should fix exact column order and labels so independently authored projections collide identically.

2. Should a projection writer ship in the first slice?

   Answer: start with a read-only validator and stable contract. Add `--write-projections` after fixtures prove deterministic edits.

3. Should `change.yaml` store current next stage?

   Answer: no. It may store derived review and validation summaries, but the active plan remains the only owner of planned-initiative next stage. The spec amendment should state that validator-recognized `change.yaml` next-stage-like fields are derived-only and that direct authoring of live next-stage authority in `change.yaml` is rejected.

4. Should stale-token checking use raw grep?

   Answer: use parser-scoped checking as the gate. Use raw grep only as a diagnostic or reviewer aid.

5. Which plans should be subject to immediate enforcement?

   Answer: active and blocked plans, plus any plan whose lifecycle state changes after the contract lands. Done and archived plans remain historical. Reopening an archived plan back to active is a lifecycle state change and should place that plan under enforcement.

6. Should cross-surface validation be a new command?

   Answer: prefer a reusable state-sync module composed through `validate-artifact-lifecycle.py`. Add a separate command only as a thin wrapper; it should reuse the same parser and comparison module, not implement independent lifecycle-state parsing.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-23 | Treat this as follow-up hardening to Single Source of Workflow State. | Ownership already landed and PR #38 merged. | Create another competing state-ownership proposal. |
| 2026-06-23 | Keep `Current Handoff Summary` as owner. | It already contains the complete live-state field set. | Move ownership to change metadata or plan index. |
| 2026-06-23 | Make `Readiness` a pointer. | Narrative next-stage mirrors repeatedly drifted. | Continue manually synchronizing readiness prose. |
| 2026-06-23 | Derive last-reviewed milestone from review evidence. | Storing it in the owner duplicates ledger facts. | Keep `Last reviewed milestone` as an independently maintained handoff-summary field. |
| 2026-06-23 | Use a `docs/plan.md` table projection. | Table cells are less ambiguous than semicolon-delimited list rows. | Start with one-line `key: value` list rows. |
| 2026-06-23 | Bind the gate through stage handoff, verify, and CI validation. | An advisory checklist alone repeats the manual synchronization failure mode. | Rely only on agent discipline or optional hooks. |
| 2026-06-23 | Validate before transition. | Review-time detection is too late. | Depend on reviewers to find drift. |
| 2026-06-23 | Keep `change.yaml` next-stage-like data derived-only. | Direct live next-stage authoring in metadata would create a second owner. | Store current next stage directly in `change.yaml`. |
| 2026-06-23 | Treat reopened archived plans as newly enforced. | Reopening is a lifecycle state change, so stale historical formatting becomes live risk. | Leave reopened plans outside the gate until another transition. |
| 2026-06-23 | Scope stale-token checks to live surfaces. | Historical evidence should preserve prior stage names. | Whole-repository token bans. |
| 2026-06-23 | Defer automatic projection writing until the parser contract is stable. | Incorrect automatic edits are riskier than a failing validator. | Start with broad automatic rewriting. |

## Next Artifacts

```text
proposal-review
single-source workflow-state spec amendment
spec-review
test-spec amendment
plan
plan-review
implementation
code-review
explain-change
verify
pr
```

Architecture is not expected to be required because this changes repository workflow contracts, Markdown projections, and validation tooling without changing runtime services, persistence, deployment, or external APIs.

## Follow-on Artifacts

- Proposal-review: `docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/reviews/proposal-review-r1.md`
- Spec amendment: `specs/single-source-of-workflow-state.md`

## Readiness

Accepted after `proposal-review-r1`.

Spec amendment is in progress in `specs/single-source-of-workflow-state.md`.

## Core Invariant

A mutable lifecycle fact has one owner.

Every repeated current-state value is a mechanical projection, not a narrative copy.

Ledgers preserve history. Evidence proves bounded outcomes. Neither controls the live next stage.

No lifecycle transition is ready until owner, projections, ledgers, evidence, and derived summaries agree.
