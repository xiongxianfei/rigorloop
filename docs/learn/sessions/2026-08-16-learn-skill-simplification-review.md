# Learn Session: Learn Skill Simplification Review

## Status

- Session outcome: observations recorded
- Contributor confirmation: pending
- Topic updates: none
- Derivative routing: none

## Frame

- Trigger: explicit invocation of `learn` after a proposal rereview requested further changes to the learn-skill simplification proposal.
- Trigger type: explicit maintainer request / repeated proposal-review findings.
- Scope:
  - `docs/proposals/2026-08-16-learn-skill-simplification.md`
  - the user-provided rereview result covering `LRNSIM-PR1`, `LRNSIM-PR2`, and `LRNSIM-PR3`
  - `skills/learn/SKILL.md`
  - `specs/learn-artifact-model.md`
  - directly relevant prior learn guidance about progressive loading, skill asset design, token-measurement scope, and repeated review findings
- Session record path: `docs/learn/sessions/2026-08-16-learn-skill-simplification-review.md`
- Evidence in scope:
  - the current proposal revision at commit `24cdadda`
  - the current canonical learn skill
  - requirements R2, R8-R25a, R31-R35, and R44 of the approved learn artifact model
  - the current user-provided proposal rereview, which is not treated as a substitute for a formal recorded proposal-review artifact
  - `docs/learn/topics/skill-asset-design.md`
  - `docs/learn/sessions/2026-05-11-progressive-loading-high-cost-skills.md`
  - `docs/learn/sessions/2026-05-09-review-finding-volume-root-cause.md`
  - `docs/learn/sessions/2026-05-10-skill-token-measurement-scope-narrowing.md`
- Explicit exclusions:
  - This session does not revise the proposal or settle its review status.
  - This session does not approve the rereview's recommended operations or persistence model.
  - This session does not update topic guidance without contributor confirmation.
  - This session does not create a new schema, transaction artifact, reconciliation engine, template, or workflow stage.
- Prior learnings reviewed:
  - Packaged resources should earn their files through a real activation boundary or substantial repeated structure.
  - Optimization scope and measurement profiles should be supported by actual usage evidence rather than an artificial path.
  - Repeated review findings often indicate that the selected model or vocabulary has not stabilized before downstream detail is added.

## Observe

### O1: The lightweight trigger-assessment profile is not yet supported by an observed caller

The current proposal retains `assess-learn-trigger` but makes its existence conditional on a later inventory. The rereview correctly identifies that a public operation and measured profile should not be designed first and justified afterward.

Evidence:

- The approved workflow says a trigger-owning surface may close a trigger before a learn session runs.
- The current learn skill describes this closeout but does not identify a repository-owned caller that invokes `learn` solely to make the decision.
- The proposal explicitly says LR0 should be removed if later evidence finds no caller.

Observation:

The simpler first-version direction is to inventory current callers before preserving the operation. If no caller exists, trigger-owning stages decide whether to invoke `$learn`, and every actual learn invocation begins a recorded session.

### O2: Exact phase recovery risks turning a Markdown retrospective into a transaction engine

The rereview requests durable prepared state, closed phase values, contributor-confirmation progress, prepared topic effects, and idempotent side-effect identities. Those fields would make crash recovery more explicit, but they also expand the proposal from package simplification into a persistent session execution protocol.

Evidence:

- The approved learn contract requires a tracked session once `Frame` begins but does not currently define a separate transaction artifact or machine-owned phase state.
- The proposal's non-goals reject scripts, templates, a schema owner, and an executable learning engine.
- The rereview says architecture is required if the existing session record cannot carry this recovery model.

Observation:

The first version should distinguish ordinary safe file handling from workflow-grade crash recovery. It can resolve a unique absent session path, write the complete session record in bounded edits, and stop on an occupied or concurrently changed path. It should not promise exact resume after arbitrary interruption unless repository evidence shows that this is a real requirement and the architecture owns the resulting state model.

### O3: Route reconciliation would make learn an ongoing settlement tracker

The rereview proposes `reconcile-learn-routes`, stable route IDs, per-route states, aggregate derivation, and later mutation of the session record after destination owners act. This closes a traceability gap, but it changes a historical retrospective record into a continuing cross-stage settlement ledger.

Evidence:

- The approved model makes the session record the historical thread and action-owning artifacts authoritative for behavior changes.
- The current learn skill routes derivative work through owners and does not claim workflow continuation or lifecycle state.
- `workflow` owns routing, while the destination skill owns its artifact and review gates.
- The proposal's central goal is a smaller judgment-oriented skill, not a new cross-stage reconciliation owner.

Observation:

The simpler boundary is to record the owner-bound route and any destination identity that already exists during the session, then stop. Later owner work remains authoritative in its own surface. If durable backlink completion is genuinely required, it should be proposed as a separate workflow or traceability capability rather than hidden inside a learn-skill simplification.

### O4: The repeated findings point to scope expansion, not merely missing detail

The first review asked for read-only trigger ownership, mandatory route semantics, and safe session identity. The revised proposal addressed those issues. The next rereview asks for caller envelopes, durable phase progress, per-effect retry state, a third reconciliation operation, and aggregate route settlement derivation.

Evidence:

- The proposal began as a content-package and progressive-disclosure refactor.
- The requested recovery and reconciliation model introduces behavior and state beyond the current published skill.
- Prior learn evidence shows that repeated review rounds often continue when the fundamental model has not been narrowed before detailed contracts are added.

Observation:

The proposal should explicitly choose between two initiatives:

1. a bounded learn-package simplification that preserves current behavior and fails closed on ambiguous interruption or later route state; or
2. a broader learn-session transaction and reconciliation redesign requiring architecture assessment and its own value case.

Combining both makes the simplification harder to justify and more expensive to implement and review.

## Classify

| ID | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | pending confirmation | Candidate proposal revision: remove `assess-learn-trigger` unless an actual caller is found | Pending contributor confirmation | The current evidence questions the operation but does not yet include a complete caller inventory. |
| O2 | direction | pending confirmation | Candidate proposal revision: use fail-closed whole-record writes and defer resumable phase transactions | Pending contributor confirmation | Selecting transaction-grade recovery would materially broaden the proposal and may require architecture. |
| O3 | direction | pending confirmation | Candidate proposal revision: omit `reconcile-learn-routes` from the simplification | Pending contributor confirmation | Reconciliation is a distinct continuing ownership capability, not obviously part of package simplification. |
| O4 | observation | pending confirmation | Candidate scope split if transaction and reconciliation behavior is still desired | Pending contributor confirmation | The review sequence provides evidence of expanding scope, but the contributor should choose the direction. |

## Route

No topic update or derivative artifact mutation was performed.

Contributor confirmation is required before revising the proposal or creating a separate transaction/reconciliation proposal. The current candidate direction is:

```text
first version:
  simplify the package
  preserve recorded sessions and topic ownership
  remove unproven trigger-assessment operation
  fail closed on session collision or interruption ambiguity
  record owner-bound routes without later learn-owned settlement tracking

separate future proposal, only if evidence justifies it:
  resumable phase transactions
  idempotent multi-file effects
  route reconciliation
```

## No Durable Lesson Rationale

The observations are evidence-bound and potentially reusable, but they propose a change in scope and architecture posture for an active proposal. They remain candidate `direction` classifications until the contributor confirms or adjusts them. A topic file would be inappropriate because the active proposal and any later architecture decision are the authoritative surfaces.

## Validation Evidence

- `git diff --check`

## Follow-Ups

- Pending contributor confirmation: whether to adopt the bounded first-version direction above.
- No proposal revision, topic update, workflow change, or architecture artifact was created by this session.
