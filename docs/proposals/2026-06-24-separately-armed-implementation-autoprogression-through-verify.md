# Separately Armed Implementation Autoprogression Through Verify

## Status

accepted

## Relationship to prior work

The accepted [Proposal-Gated Authoring Autoprogression Through Plan Review](2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md) profile defines the bounded authoring sequence:

```text
proposal gate
-> spec
-> spec-review
-> architecture and architecture-review when required
-> plan
-> plan-review
-> stop
```

This proposal does not widen that profile. It introduces a separately authorized sibling profile:

```text
implementation-through-verify
```

Implementation crosses different risk surfaces than authoring: code execution, dependency mutation, test fixture changes, review-driven corrections, and validation cost. Authorization to continue through authoring must not silently authorize implementation.

## Problem

After a proposal is accepted and the authoring profile produces an approved plan, the remaining lifecycle commonly follows a predictable sequence:

```text
test-spec
-> test-spec settlement
-> implement milestone
-> code-review
-> resolve eligible findings
-> code-review again
-> repeat for remaining milestones
-> explain-change
-> verify
```

Today, the user still has to manually trigger many transitions even when the approved plan already determines the next milestone, validation commands are recorded, the next review round is mandatory, all milestones are clean, and `explain-change` plus `verify` are the required closeout stages.

However, unrestricted implementation autopilot would be unsafe. Findings that appear simple can conceal product, compatibility, workflow, or owner decisions. A review finding whose safe path is "apply this change, or revise the governing spec if legacy behavior should remain" is not auto-fixable because the orchestrator lacks authority to choose the owner's intent.

The central design question is therefore:

```text
Who declared the finding auto-fixable,
under which tracked contract,
and what prevents the loop from expanding beyond that authority?
```

The current workflow also has no separate formal `test-spec-review` stage. The normal chain moves from `test-spec` into implementation. This proposal therefore defines a deterministic test-spec settlement gate rather than adding a new review skill.

## Goals

- Add a change-local, opt-in `implementation-through-verify` profile.
- Require separate user authorization from `authoring-through-plan-review`.
- Automatically author and settle the test spec when its inputs are complete.
- Automatically implement approved plan milestones in order.
- Run a distinct, independent code review after each milestone.
- Permit automatic finding resolution only when the reviewer explicitly classifies the finding as auto-fixable.
- Support bounded `implement -> code-review -> implement fixes -> code-review` loops.
- Stop immediately when a finding requires owner judgment.
- Keep automatic review-driven edits within reviewer-declared paths and approved plan scope.
- Prevent automatic substantive changes to governing artifacts.
- Require unresolved findings to shrink on every automatic correction round.
- Prevent new findings from being chased automatically.
- Automatically run `explain-change` after all implementation milestones and review resolutions close.
- Automatically run final `verify` with fresh actual-run evidence.
- Stop after successful verification and report readiness for the `pr` stage.
- Keep opening, publishing, or externally exposing the PR as an explicit human action.
- Preserve a complete audit trail for every automatic transition and correction.

## Non-goals

- Do not modify or expand `authoring-through-plan-review`.
- Do not infer auto-fixability from severity, wording, file count, or apparent simplicity.
- Do not automatically resolve findings with no explicit auto-fix classification.
- Do not automatically choose between alternative product, compatibility, architecture, or policy outcomes.
- Do not automatically edit proposal, spec, test-spec, architecture, ADR, or substantive plan content in response to code-review findings.
- Do not add a `test-spec-review` skill.
- Do not allow unlimited implementation/review cycles.
- Do not continue when review rounds stop converging.
- Do not automatically fix final verification failures. Automatic verify-failure repair is a permanent non-goal for this profile.
- Do not use cached validation hits as final autoprogression verification evidence.
- Do not open, publish, or update a hosted PR automatically.
- Do not publish packages, deploy software, mutate remote infrastructure, or perform other external-boundary actions.
- Do not run credentialed, destructive, privileged, or unapproved network commands without explicit user authorization.
- Do not operate in an unrelated dirty worktree.
- Do not apply this profile to fast-lane, bugfix, or isolated stage invocations in the first slice.
- Do not run asynchronously or in the background.

## Vision fit

fits the current vision

RigorLoop exists to make AI-assisted work traceable, resumable, reviewable, and safe to continue across agents. This proposal removes low-value routing work while preserving the high-value human boundaries: humans authorize implementation scope, reviewers declare which findings are mechanically safe, the workflow executes only within that recorded authority, and external publication remains human-controlled.

The proposal is falsified if an unclassified finding is automatically fixed, an auto-fix changes a governing artifact, a review loop grows or oscillates instead of converging, a new review finding is automatically chased, review independence collapses into self-approval, verification reuses stale evidence, the workflow opens a PR without explicit authorization, resumption repeats a completed stage, unrelated dirty changes enter the automated diff, or the reason and authority for an automatic fix cannot be reconstructed later.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Automatically run `test-spec` | in scope | Test-spec settlement |
| Automatically approve or settle the test spec | in scope | Test-spec settlement |
| Automatically implement | in scope | Milestone execution |
| Automatically run code review | in scope | Independent review rounds |
| Automatically repeat implement/code-review | in scope | Review-driven correction loop |
| Automatically run `explain-change` | in scope | Closeout phase |
| Automatically run `verify` | in scope | Closeout phase |
| Automatically open a PR | out of scope | PR boundary |
| Automatically fix every finding | rejected option | Reviewer-declared auto-fix classification |
| Preserve safety and reviewability | in scope | Guardrails and audit trail |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Separate implementation profile | core to this proposal | Authoring authorization must not imply code-execution authorization. |
| Test-spec settlement gate | core to this proposal | The repository has no separate formal test-spec-review stage. |
| Milestone implementation sequencing | core to this proposal | Enables automatic implementation flow under the approved plan. |
| Reviewer-declared auto-fix classification | same-slice dependency | The orchestrator must not infer safety. |
| Bounded implementation/review loop | core to this proposal | Required for convergence and safe correction. |
| Independent review contexts | same-slice dependency | Prevents self-approval. |
| Explain-change and verify | core to the final profile | Requested closeout behavior. |
| Fresh actual-run verify evidence | same-slice dependency | Final verification must not rely on stale cache evidence. |
| Automatic PR opening | out of scope | External-boundary action remains human-controlled. |
| Automatic owner-decision resolution | out of scope | Agent lacks authority. |
| Project-wide default profile | separate proposal | Change-local opt-in should prove safe first. |
| Automatic repair after verify failure | out of scope | Post-review edits invalidate final review state; this profile always requires explicit owner direction after verify failure. |

## Context

The standard workflow already establishes:

```text
test-spec
-> implement
-> code-review
-> review-resolution when triggered
-> ci-maintenance when triggered
-> explain-change
-> verify
-> pr
```

For milestone-based plans, the implementation/review segment repeats for each in-scope milestone. The accepted authoring profile intentionally stops after clean `plan-review` and reports `test-spec` next, and the governing workflow spec says additional profiles, including implementation profiles, need separate proposal and spec amendments.

This proposal applies the following safety model:

1. Implementation needs a separately armed profile.
2. Reviewers, not the orchestrator, classify auto-fix eligibility.
3. Every automatic loop is bounded, shrinking, path-local, and free of new findings.
4. Verify may run automatically with fresh evidence, but PR publication remains an explicit human boundary.

The profile is defined as an end state, with phased rollout so the implementation/code-review loop can prove safety before automatic closeout through verify is enabled.

## Options considered

### Option 1: Keep all implementation transitions explicit

Pros:

- Lowest orchestration risk.
- No review-schema changes.

Cons:

- Users remain responsible for deterministic routing.
- Mechanical findings still consume unnecessary attention.

### Option 2: Add unrestricted `auto=true`

Pros:

- Simple interface.
- Maximum automation.

Cons:

- No bounded meaning.
- Encourages inferred auto-fix safety.
- Can silently expand into PR or publication behavior.

Rejected.

### Option 3: Automate only through clean code review

Pros:

- Smaller initial risk surface.
- Proves classification and loop guardrails first.

Cons:

- Still requires manual `explain-change` and `verify`.
- Does not satisfy the full requested experience.

### Option 4: Define `implementation-through-verify`, enable it in phases

Pros:

- Meets the desired end state.
- Keeps one closed profile.
- Preserves separate authorization from authoring.
- Allows the implementation/review loop to prove safety before enabling automatic closeout.
- Stops before external PR effects.

Cons:

- Larger contract and fixture surface.
- Requires review-record schema changes.

Recommended.

### Option 5: Automate through PR opening

Pros:

- Removes the final manual trigger.

Cons:

- Crosses an external boundary.
- Can trigger hosted CI, reviewer notifications, deployment hooks, or publication processes.

Rejected for the first slice.

## Recommended direction

Introduce a closed change-local profile:

```text
off
implementation-through-verify
```

Recommended user-facing request:

```text
auto-through: verify
```

Internal normalized value:

```text
implementation-through-verify
```

The profile uses three persisted rollout phases:

```text
Phase A:
  audit-only transition evaluation

Phase B:
  test-spec settlement
  -> milestone implementation and code-review loops
  -> clean final code review

Phase C:
  explain-change
  -> fresh verify
  -> stop before PR
```

Each profile record includes a persisted rollout phase:

```text
A
B
C
```

The orchestrator refuses transitions outside the persisted phase. Phase A records audit-only decisions and does not execute implementation. Phase B may execute through final clean code review but refuses `explain-change` and `verify` transitions. Phase C may run `explain-change` and `verify` only after durably recorded promotion evidence links to the required Phase B dogfood-cycle audit records and synthetic stop-condition fixture results.

### Profile state model

Use a closed state set:

```text
off
armed
active
paused
completed
cancelled
```

The state records automation policy and execution status. It does not replace the active plan's current-state ownership.

Store `authoring-through-plan-review` and `implementation-through-verify` as independent authorization records with separate keys, timestamps, `authorized_by`, state, phase where applicable, and cancellation data. Revoking or completing one profile does not mutate the other profile's record.

Preferred storage is `docs/changes/<change-id>/change.yaml` under `workflow.autoprogression.implementation_through_verify`; fallback to `docs/changes/<change-id>/workflow-policy.yaml` only when the change-metadata contract rejects policy data. Required fields are `profile`, `phase`, `authorized_by`, `authorized_at`, `state`, and a `cancellation` block when cancelled. The record must persist before activation; write failure pauses the profile.

### Activation gate

The profile may become active only when all of these are true:

- `authoring-through-plan-review` is completed, or the change has a manually authored plan with recorded `plan-review` approval and synchronized plan state.
- `plan-review` is approved and recorded.
- The active plan is internally synchronized.
- Implementation milestones are explicit and ordered.
- Test-spec inputs are complete.
- The user explicitly authorizes `implementation-through-verify`.
- Working tree baseline is recorded.
- Unrelated dirty changes are absent or explicitly excluded.
- Required commands are approved by the plan/test spec.
- No open proposal, spec, architecture, or plan findings remain.
- Artifact placement is unambiguous.
- Workflow-state synchronization passes.

Silence or prior authorization for authoring is not sufficient.

### Test-spec settlement

The profile runs:

```text
test-spec authoring
-> test-spec settlement gate
```

A test spec is settled for implementation only when the artifact exists at the approved path, its status is the repository-approved active or settled value, applicable requirements and acceptance criteria have coverage mapping, required negative and boundary cases are present, uncovered gaps are `none`, no `needs-decision` remains, planned validation commands are named, the test spec does not contradict approved governing artifacts, applicable structural/static validation passes, and workflow-state synchronization passes.

If the test-spec artifact reveals upstream contract ambiguity, the profile pauses and routes to the owning upstream stage. Automatic settlement means the deterministic gate passed; it does not mean the `test-spec` authoring stage reviewed or approved itself.

Settlement evidence records input artifact identities, including hashes or an equivalent durable revision identity for the approved spec, architecture/ADR when present, plan, and test spec. The first milestone's code-review round rechecks those identities against current artifacts before relying on settlement. A mismatch pauses the profile because implementation preconditions may have changed.

### Milestone execution

For each remaining plan milestone, in approved order, the profile confirms dependencies, confirms file and command scope, implements the milestone, runs targeted validation from the approved test spec and plan, synchronizes workflow state, identifies the bounded review surface, invokes independent code review, records the formal review result, closes the milestone if review is clean, or applies the reviewer-declared correction policy.

The profile does not skip ahead because later milestones appear independent. Parallel milestone execution is out of the first slice.

### Reviewer-declared auto-fix classification

Every material code-review finding includes:

```text
auto_fix_class
```

Closed values:

```text
none
mechanical
declared-safe
```

Missing classification behaves as `none`.

`none` is used when owner intent is required, alternatives remain, behavior or compatibility could change, a governing artifact may need revision, the safe path contains a decision branch, affected paths are not bounded, or validation is not deterministic. Behavior: pause immediately.

`mechanical` is used only for enumerated finding kinds whose correction is uniquely determined by tracked artifacts. Candidate eligible kinds are:

```text
formatter-output
lint-autofix
generated-output-refresh
exact-approved-rename
unique-required-field-value
mechanical-state-projection-sync
deterministic-manifest-regeneration
```

The downstream spec should close this enumeration. A mechanical finding also names `auto_fix_kind`, `affected_paths`, deterministic authority, and required validation.

`declared-safe` is a rare reviewer-authorized escape hatch. Required fields are `affected_paths`, `resolution_recipe`, named inputs, named outputs, forbidden paths, acceptance criteria, required validation commands, and a scope-preservation rule. If the recipe changes production code, it includes a test that exercises the changed behavior or cites existing test-spec mappings that already prove the changed behavior. The reviewer affirmatively declares that the recipe contains no owner decision. The orchestrator cannot upgrade `none` to `declared-safe`.

### Governing-artifact boundary

Automatic review-driven fixes cannot substantively edit:

```text
proposal
spec
test-spec
architecture
ADR
plan
constitution
workflow policy
release policy
security policy
```

If such an edit is required, the profile pauses.

The only allowed automated updates within plan or lifecycle surfaces are machine-owned state projections and append-only evidence required by the approved workflow-state contract, such as current handoff projection updates through an approved synchronizer, `docs/plan.md` projection updates, review-log appends, and review-resolution evidence updates.

### Review-driven correction loop

When code review records findings:

```text
if any finding has auto_fix_class=none:
  pause

if every finding is mechanical or declared-safe:
  evaluate loop guardrails
  apply only approved recipes
  rerun required validation
  record resolution evidence
  run a fresh independent code-review round
```

Guardrails:

- Maximum automatic correction rounds per milestone: `3`.
- The across-activation ceiling is the sum of the per-milestone caps, with no extra rounds for long plans.
- Each round reduces the unresolved finding set.
- Any finding ID or finding class not present in the preceding unresolved set pauses the profile. This includes cases where a fresh independent reviewer legitimately discovers a missed issue; new discovery is treated as a human-decision moment rather than more automatic repair authority.
- Correction diffs touch only reviewer-declared affected paths, approved generated outputs derived from those paths, approved workflow-state projections, and required review/evidence records.
- Corrections do not introduce an unplanned component, dependency, public interface, external integration, security boundary, migration, or generated artifact class.
- Substantive governing-artifact edits pause regardless of classification.
- Auto-fix commands come from the approved plan, settled test spec, reviewer-declared recipe, or project-owned deterministic scripts.

### Review independence

Every code-review round is a fresh invocation. The reviewer receives the actual diff, governing proposal/spec/test-spec/architecture/plan, current validation evidence, formal review criteria, and current review target. Prior findings may be used to verify whether they remain, but not to narrow the review to only the requested edit.

Required independence evidence includes review round, reviewed commit or diff, governing artifacts read, validation evidence read, previous findings consulted, and context-reset mode.

Before moving from code review to `explain-change`, the profile requires a full review against the original governing contract, even if the latest round was a targeted rereview.

### Milestone completion

A milestone closes only when targeted validation passes, the latest independent code review is approved or clean, all findings for the milestone are resolved, review-resolution evidence is current, workflow state is synchronized, reviewed diff matches milestone scope, and the commit or review surface is durable.

After a clean non-final milestone, the workflow advances to the next approved milestone. After the final clean milestone, it runs final contract-level code-review confirmation and closes the implementation phase.

### Conditional `ci-maintenance`

If the approved plan or settled test spec triggers CI workflow work, `ci-maintenance` may run automatically as part of the relevant implementation milestone only when the plan explicitly enumerates the CI files in scope. The enumerated CI files also pass a deny-list check for credential handling, deploy targets, hosted-runner privilege changes, and secrets references before automatic CI edits begin. If the CI files are not enumerated, the deny-list check fails, or an unplanned CI infrastructure need appears, the profile pauses because the change may alter external-boundary behavior.

### Explain-change phase

Automatic `explain-change` begins only when all implementation milestones are closed, the latest full code review is clean, all review findings are resolved, review-resolution closeout is current, no unauthorized diff remains, and workflow-state synchronization passes.

The explanation uses the actual final diff, approved proposal, approved spec, settled test spec, architecture and ADRs, plan milestones, review findings and dispositions, and validation evidence available at that point. If the final diff cannot be reconciled with governing artifacts, the profile pauses.

### Verify phase

`verify` may run automatically after `explain-change`, but autoprogression verification uses actual-run evidence. It does not use cache hits as final proof for required test suites, artifact lifecycle validation, review closeout validation, change metadata validation, generated-output checks, security-sensitive validation, or release-sensitive validation. Purely informational sub-check cache hits may be allowed only when the cache entry timestamp is strictly after the activation baseline; default behavior is no cache. Any allowed cache use is recorded with the sub-check name and cache timestamp in the verify audit record.

If verification passes, the profile state becomes `completed`, branch readiness is computed by the workflow-state synchronizer from the recorded verify result and completion evidence, the next stage is `pr`, and human authorization is required. If verification fails, the profile pauses and does not automatically fix the failure. Any source or test correction after a verify failure re-enters `implement -> code-review -> explain-change refresh -> verify` after explicit user direction.

### PR boundary

The profile stops before invoking `pr`. It may report that verification completed, branch-ready evidence is recorded, the PR stage is next, and human authorization is required. It does not open a hosted PR, publish a package, push a branch, trigger deployment, post to external systems, or request human review remotely.

### Pause, cancellation, and resumption

On pause, record last completed stage, current stage, stop reason, finding or blocker IDs, profile round count, files currently changed, required human action, and safe resume point.

User cancellation sets profile state to `cancelled`; no future stage starts automatically and existing artifacts remain intact.

Explicit user resumption is required after `auto_fix_class=none`, owner decision, new finding, non-shrinking loop, round limit, governing-artifact edit need, verify failure, external command requirement, or unrelated dirty state. Before resuming, rerun the workflow-state synchronization gate. Completed milestones and clean review rounds are not repeated unless their underlying inputs changed.

### Audit trail

For every automatic correction round, record profile authorization, activation baseline, milestone, review round, finding IDs, reviewer-recorded classification, auto-fix kind, resolution recipe, affected paths, actual paths changed, before/after unresolved-finding sets, commands run, validation results, review-context reset evidence, and commit or diff identity.

For automatic `explain-change` and `verify`, record evidence inputs, source revision, working-tree state, validation freshness, commands run, transcript or output references, and completion result.

For completion, record that the profile completed at the verify boundary, PR was not opened, and human authorization is required.

## Expected behavior changes

When the profile is off, behavior is unchanged:

```text
test-spec completes
-> report implementation next
-> stop
```

When active for a clean single milestone:

```text
test-spec
-> settlement gate
-> implement M1
-> code-review M1 clean
-> explain-change
-> verify
-> stop before PR
```

When active for multiple clean milestones:

```text
test-spec
-> implement M1
-> code-review M1 clean
-> implement M2
-> code-review M2 clean
-> final full review
-> explain-change
-> verify
-> stop before PR
```

When code review returns a mechanical finding, the profile applies the exact correction, runs required validation, runs a fresh code-review round, and continues only if the review becomes clean without violating loop guardrails.

When code review returns an owner-decision finding, introduces a new finding, stops shrinking, reaches the round cap, or requires a governing-artifact edit, the profile pauses. When final verify fails, the profile pauses and does not repair automatically.

## Architecture impact

| Surface | Impact |
| --- | --- |
| Workflow-stage autoprogression contract | Add separate implementation profile. |
| RigorLoop workflow contract | Define test-spec settlement, milestone loop, and verify stop. |
| Formal review recording | Add reviewer-owned auto-fix classification fields. |
| Material-finding asset | Add classification and deterministic-recipe fields. |
| Workflow skill | Activate, pause, resume, and complete the profile. |
| Test-spec skill | Expose deterministic settlement result. |
| Implement skill | Support bounded milestone execution and reviewer-authorized fixes. |
| Code-review skill | Classify findings and preserve independent review context. |
| Review-resolution | Record automatic recipe execution and disposition. |
| Explain-change | Support profile-driven invocation after final clean review. |
| Verify | Enforce fresh actual-run evidence in auto mode. |
| Workflow-state sync | Validate every transition. |
| Change metadata | Store independent authoring and implementation profile authorization records, phase, state, and audit pointers, not live next-stage ownership. |
| Generated skills/adapters | Rebuild and validate changed canonical skill content. |

This changes orchestration and review-record semantics across multiple stages, so architecture assessment is recommended.

## Testing and verification strategy

The downstream test spec should cover at least:

| Check ID | What is verified |
| --- | --- |
| `ITV-001` | Profile defaults to `off`. |
| `ITV-002` | Authoring-profile authorization does not authorize implementation. |
| `ITV-003` | Unknown profile values fail closed. |
| `ITV-004` | Activation requires approved plan-review. |
| `ITV-005` | Unrelated dirty state blocks activation. |
| `ITV-006` | Test-spec settlement requires complete coverage and no gaps. |
| `ITV-007` | Static repository check confirms no `test-spec-review` skill file or lifecycle stage is added. |
| `ITV-008` | Clean test-spec settlement starts the first milestone. |
| `ITV-009` | Milestones run in approved order. |
| `ITV-010` | Every milestone receives an independent code review. |
| `ITV-011` | Missing `auto_fix_class` behaves as `none`. |
| `ITV-012` | `mechanical` accepts only closed eligible finding kinds. |
| `ITV-013` | `declared-safe` requires a complete deterministic recipe. |
| `ITV-014` | Owner-decision findings pause. |
| `ITV-015` | Governing-artifact edits pause. |
| `ITV-016` | Auto-fix diffs are limited to declared paths. |
| `ITV-017` | Auto-fix cannot introduce a new dependency or component. |
| `ITV-018` | Open findings strictly shrink per round. |
| `ITV-019` | A same-size finding set pauses. |
| `ITV-020` | A new finding pauses. |
| `ITV-021` | The fourth non-clean round for one milestone cannot run automatically. |
| `ITV-022` | Review rounds record context-reset evidence. |
| `ITV-023` | Final full review runs before explain-change. |
| `ITV-024` | All findings close before explain-change. |
| `ITV-025` | Conditional CI changes remain inside reviewed milestone scope. |
| `ITV-026` | Explain-change uses the final reviewed diff. |
| `ITV-027` | Verify uses fresh actual-run evidence. |
| `ITV-028` | Verify failure pauses and does not auto-fix. |
| `ITV-029` | A post-verify edit requires new review and explanation. |
| `ITV-030` | Successful verify completes the profile. |
| `ITV-031` | The profile never opens a PR. |
| `ITV-032` | Cancellation prevents future automatic transitions. |
| `ITV-033` | Resumption does not duplicate closed milestones. |
| `ITV-034` | Every automatic fix is reconstructable from audit records. |
| `ITV-035` | Behavior remains unchanged when the profile is off. |
| `ITV-036` | Phase C transitions are refused unless persisted phase is `C` and promotion evidence is linked. |
| `ITV-037` | Authoring and implementation profile authorizations are stored as separate records. |
| `ITV-038` | First milestone code-review pauses when test-spec settlement input identities changed. |
| `ITV-039` | Automatic CI maintenance pauses unless CI files are enumerated and deny-list checks pass. |

Create `docs/changes/<change-id>/behavior-preservation.md` with a matrix proving that authoring autoprogression, absence of a test-spec-review stage, owner-decision handling, review independence, PR explicitness, fast-lane behavior, bugfix behavior, and profile-off behavior are preserved.

## Rollout and rollback

### Rollout phase A: audit only

Add profile schema and transition evaluation, run simulated chains without executing stages, record what would run/pause/complete, and validate finding classifications and stop conditions.

### Rollout phase B: implementation through clean code review

Enable:

```text
test-spec settlement
-> milestone implementation
-> code-review loop
-> stop after final clean code review
```

Dogfood on at least 10 eligible changes, or for 30 days with at least 10 eligible simulated or real cycles. Promotion criteria are no observed unauthorized auto-fixes, no observed governing-artifact auto-edits, no observed new-finding loops, no observed exceeded round caps, no observed duplicate milestone runs, all reviewer-declared pauses occurring correctly, and a synthetic-fixture audit proving every documented stop condition pauses.

### Rollout phase C: explain-change and verify

After Phase B passes and the persisted profile phase advances to `C` with linked promotion evidence:

```text
final clean code review
-> explain-change
-> fresh verify
-> stop before PR
```

### Rollback

Set profile to `off`, stop automatic stage invocation, preserve produced artifacts and audit records, restore explicit stage triggering, rebuild generated skill outputs if canonical skill guidance is reverted, and keep reviewer classifications in historical findings.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Reviewer over-classifies a finding | Use closed mechanical kinds and mandatory declared-safe recipe fields. |
| Orchestrator infers safety | Missing classification defaults to `none`. |
| Loop oscillates | Enforce shrinking-set and round-limit invariants. |
| Fix creates new defect | Pause on new findings and require independent rereview. |
| Fix expands scope | Enforce affected-path and scope-budget checks. |
| Governing policy changes silently | Hard stop on substantive governing-artifact edits. |
| Review becomes a rubber stamp | Require fresh context plus final full review. |
| Verify uses stale evidence | Require actual-run final verification. |
| Agent edits after verify | Require implementation, review, explanation, and verify replay. |
| Dirty tree contaminates review | Record activation baseline and stop on unrelated diffs. |
| Audit metadata becomes too large | Store structured summaries with links to detailed review and validation evidence. |
| Profile becomes permanent default | Keep first adoption change-local and opt-in. |
| External systems are mutated | Stop before PR and other external actions. |
| Phase gating is documentation only | Persist phase in the profile record and refuse transitions outside the persisted phase. |

## Open questions

| Question | Candidate answer | Where to settle |
| --- | --- | --- |
| What should the profile be called? | `implementation-through-verify`, with user-facing `auto-through: verify`. | Spec |
| Where should authorization be stored? | Prefer `docs/changes/<change-id>/change.yaml` under `workflow.autoprogression.implementation_through_verify`; fallback to `workflow-policy.yaml` only when change metadata rejects policy data. Store it separately from authoring authorization with profile, phase, `authorized_by`, `authorized_at`, state, and cancellation data. | Spec and architecture |
| What is the maximum correction-round count? | `3` is the hard upper bound per milestone in the first slice; project policy may go lower; raising above `3` requires a separate proposal. | Spec |
| Should there be a new `test-spec-review` skill? | No. Use a deterministic settlement gate and track whether unsafe or defective settlements would have been caught by independent review; if that count reaches the threshold set in spec, create a follow-on proposal. | Proposal review and spec |
| May `declared-safe` fixes alter production code? | Yes, only within reviewer-declared paths, deterministic recipe, no governing-artifact changes, no new scope, no owner decisions, and with changed-behavior test proof or cited existing coverage. | Spec and review schema |
| Can final verify use validation-cache hits? | No for sensitive or correctness-bearing checks. Purely informational cache hits may be allowed only when strictly newer than the activation baseline and recorded in the audit trail. | Spec and verify guidance |
| Should verify failure automatically restart implementation? | No. Pause and require explicit resume because reviewed and explained work is no longer current; automatic verify-failure repair is a permanent non-goal for this profile. | Spec |
| Should the profile include PR opening later? | Only through a separate proposal after Phase C produces sufficient evidence under its own promotion criteria, including authentication scope, hosted-CI cost, reviewer notification scope, branch naming, and external mention/PII review. | Follow-on proposal |

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-24 | Add a sibling implementation profile instead of widening authoring. | Implementation needs separate authority and risk controls. | Expand `authoring-through-plan-review`. |
| 2026-06-24 | Use reviewer-declared auto-fix classification. | The orchestrator cannot safely infer owner intent. | Infer from severity or apparent simplicity. |
| 2026-06-24 | Default missing classification to `none`. | Silence fails safe. | Treat unclassified findings as mechanical. |
| 2026-06-24 | Limit automatic correction to three rounds per milestone, with no extra cross-milestone headroom. | Prevents runaway or oscillating loops while preserving long-plan proportionality. | Unlimited iteration; per-activation cap that degrades on long plans. |
| 2026-06-24 | Pause on new findings. | Auto-fix loops should converge rather than discover new work. | Continue chasing new findings. |
| 2026-06-24 | Block substantive governing-artifact edits. | Such edits change the authority under which implementation proceeds. | Allow reviewer-declared spec or plan edits. |
| 2026-06-24 | Use test-spec settlement rather than inventing a review stage. | No current formal test-spec-review stage exists. | Add `test-spec-review` implicitly. |
| 2026-06-24 | Permit automatic explain-change and verify after dogfood promotion. | They are internal evidence stages with deterministic outputs. | Stop permanently at code review. |
| 2026-06-24 | Stop before PR. | PR opening crosses an external boundary. | Full autopilot through PR. |

## Success metrics

Evaluate the first 10 eligible implementation cycles or 30 days:

- zero unauthorized edits;
- zero auto-fixes lacking reviewer classification;
- zero automatic governing-artifact changes;
- zero review loops beyond the configured cap;
- zero PRs opened automatically;
- zero stale-evidence verify passes;
- at least 70% fewer manual "run the next known stage" prompts;
- all pauses attributable to explicit stop conditions.

During Phase A, record the baseline count of manual "run the next known stage" prompts for comparable changes so the 70% reduction target has a measured reference point.

A pause on an owner decision, new finding, or verify failure is correct behavior.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| `AC-ITV-001` | A separate explicit authorization is required after authoring completion. |
| `AC-ITV-002` | The profile is off by default and change-local. |
| `AC-ITV-003` | Test-spec settlement is deterministic and does not invent a review skill. |
| `AC-ITV-004` | Every implementation milestone receives independent code review. |
| `AC-ITV-005` | Reviewers own auto-fix classification. |
| `AC-ITV-006` | Unclassified findings pause. |
| `AC-ITV-007` | Mechanical findings use a closed kind vocabulary. |
| `AC-ITV-008` | Declared-safe findings include a deterministic recipe and bounded paths. |
| `AC-ITV-009` | Governing-artifact changes cannot be automatically applied. |
| `AC-ITV-010` | The open-finding set must shrink every round. |
| `AC-ITV-011` | New findings pause the profile. |
| `AC-ITV-012` | No more than three automatic correction rounds occur per milestone, and the across-activation ceiling is the sum of per-milestone caps. |
| `AC-ITV-013` | Automatic corrections stay within declared scope. |
| `AC-ITV-014` | Review context is reset between implementation and review. |
| `AC-ITV-015` | A full final review precedes explain-change. |
| `AC-ITV-016` | Explain-change uses the final reviewed diff. |
| `AC-ITV-017` | Final verify uses fresh actual-run evidence. |
| `AC-ITV-018` | Verify failure pauses without automatic repair. |
| `AC-ITV-019` | Successful verify completes the profile before PR. |
| `AC-ITV-020` | Opening a PR requires explicit human authorization. |
| `AC-ITV-021` | Resumption is idempotent. |
| `AC-ITV-022` | Every automatic transition and fix is auditable. |
| `AC-ITV-023` | Existing workflow behavior remains unchanged when the profile is off. |
| `AC-ITV-024` | Phase C cannot enable until Phase B promotion criteria pass. |
| `AC-ITV-025` | Phase is persisted in the profile record and transitions outside the persisted phase are refused. |

## Next artifacts

```text
proposal-review
workflow-stage-autoprogression spec amendment
formal review recording / material-finding schema amendment
rigorloop-workflow spec amendment
spec-review
architecture assessment
architecture-review when required
test-spec amendment
plan
plan-review
implementation
code-review
explain-change
verify
pr
```

## Follow-on artifacts

- `proposal-review`: approved in [proposal-review-r1](../changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/reviews/proposal-review-r1.md)

Future proposals may cover automatic verify-failure repair, project-wide default profiles, PR-opening automation with explicit external-action authorization, independent `test-spec-review` if dogfood evidence shows settlement checks are insufficient, and profile analytics or loop-convergence reporting.

## Readiness

Accepted and ready for `spec` under the durably armed `authoring-through-plan-review` profile.

## Core invariant

Implementation automation runs only under separately recorded user authority.

A reviewer, not the orchestrator, declares whether a finding is safe to fix automatically.

Automatic review loops are bounded, shrinking, path-local, independent, and auditable.

The profile may produce fresh verification evidence, but it stops before the external PR boundary.
