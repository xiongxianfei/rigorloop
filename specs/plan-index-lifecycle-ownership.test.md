# Plan index lifecycle ownership test spec

## Status

- complete

## Related spec and plan

- Spec: `specs/plan-index-lifecycle-ownership.md`
- Related proposal: `docs/proposals/2026-04-20-plan-index-lifecycle-ownership.md`
- Plan: `docs/plans/2026-04-20-plan-index-lifecycle-ownership.md`
- Related workflow and governance surfaces:
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `docs/workflows.md`
  - `specs/rigorloop-workflow.md`
  - `docs/plan.md`
  - `docs/plans/0000-00-00-example-plan.md`
  - `skills/plan/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/learn/SKILL.md`
  - `skills/workflow/SKILL.md`
  - generated `.codex/skills/`

## Testing strategy

- Use manual contract review for contributor-facing workflow and governance guidance because this change is primarily a repository-visible documentation and process contract update.
- Use focused structural scans of tracked files to prove lifecycle-state wording, index placement, and plan-body synchronization.
- Use real canonical skill files plus `python scripts/build-skills.py --check` to prove generated `.codex/skills/` stays synchronized after stage-skill updates.
- Use `python scripts/validate-skills.py` and `bash scripts/ci.sh` as smoke proof that the lifecycle-ownership edits do not break the repository’s existing validation surfaces.
- Prefer real repository files and git-tracked state over mocks, snapshots, or synthetic fixtures.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`, `R2` | `T1`, `T7` | manual, integration | Planned-initiative scope and plan-index-versus-plan-body semantics remain explicit |
| `R3`, `R3a` | `T7`, `T9` | integration, manual | Index placement and one-section-per-plan invariant |
| `R3b`, `R5` | `T3`, `T4`, `T8`, `T9` | manual, integration | Plan-body lifecycle wording matches final lifecycle state |
| `R4` | `T1`, `T2`, `T5`, `T6` | manual, integration | Ownership split across workflow docs and stage skills |
| `R6`, `R6a` | `T3` | manual | Done transition timing and merge-dependent exception |
| `R6b` | `T4` | manual | Blocked and superseded transitions are recorded when decided |
| `R7`, `R7a` | `T5`, `T9` | manual, integration | `verify` blocks stale lifecycle state before PR readiness |
| `R8`, `R8a` | `T1`, `T2`, `T7` | manual, integration | Workflow summary, plan guidance, and skill guidance make ownership discoverable |
| `R9` | `T9` | manual, integration | Migration corrects already-known stale lifecycle state without guessing new state |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T3`, `T8`, `T9` | Done-before-PR closeout is visible in guidance and synchronized plan surfaces |
| `E2` | `T3`, `T9` | Merge-dependent done transition remains an explicit exception |
| `E3` | `T4`, `T9` | Blocked initiative moves out of `Active` when the block is decided |
| `E4` | `T4`, `T7`, `T9` | Superseded initiative moves to `Superseded` in both index and body |
| `E5` | `T6` | `learn` is not treated as lifecycle-state authority |

## Edge case coverage

- A plan may remain `Active` while implementation or review is still intentionally outstanding even if code exists: `T9`
- A merge-dependent `Done` transition may close after merge, but only as an explicit exception rather than the default rule: `T3`, `T9`
- A replaced plan must move to `Superseded` instead of silently remaining active: `T4`, `T7`, `T9`
- A blocked plan must move to `Blocked` without waiting for merge, PR creation, or retrospective work: `T4`, `T9`
- Future automation remains optional and must not become an implied requirement of the initial rule change: `T10`

## Test cases

### T1. Workflow and governance docs expose the lifecycle-ownership model

- Covers: `R1`, `R2`, `R4`, `R8`, `R8a`
- Level: manual
- Fixture/setup:
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `docs/workflows.md`
  - `specs/rigorloop-workflow.md`
- Steps:
  - Review the updated workflow and governance docs.
  - Confirm they describe `docs/plan.md` as an index rather than a plan body.
  - Confirm they describe `implement` as the owner of ongoing plan-body updates during execution.
  - Confirm they describe final lifecycle closeout as the owner of state transitions in both the plan index and plan body.
  - Confirm they describe `verify` as the stage that challenges stale lifecycle state before PR readiness.
- Expected result:
  - A contributor can discover the lifecycle-ownership split without reading chat history.
- Failure proves:
  - The repository still relies on implicit or conflicting guidance for plan lifecycle management.
- Automation location:
  - Manual review during M1.

### T2. Canonical and generated stage skills align with the ownership split

- Covers: `R4`, `R8`, `R8a`
- Level: integration, manual
- Fixture/setup:
  - canonical skill files under `skills/`
  - generated `.codex/skills/`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
- Steps:
  - Review the canonical `plan`, `implement`, `verify`, `pr`, `learn`, and `workflow` skills.
  - Confirm `plan` covers plan creation and startup indexing, not all later lifecycle transitions.
  - Confirm `implement` covers progress, decisions, discoveries, and validation-note updates during execution.
  - Confirm `verify` explicitly treats stale lifecycle state as a readiness blocker when relevant.
  - Confirm `learn` remains retrospective and non-authoritative for lifecycle bookkeeping.
  - Run `python scripts/validate-skills.py`.
  - Run `python scripts/build-skills.py --check`.
- Expected result:
  - Canonical and generated skill guidance reflect the same ownership split and remain structurally valid.
- Failure proves:
  - Runtime guidance still contradicts the workflow and governance docs or generated output drifted from canonical source.
- Automation location:
  - M2 validation.

### T3. Done transition timing and the merge-dependent exception are explicit

- Covers: `R5`, `R6`, `R6a`, `E1`, `E2`, `EC2`
- Level: manual
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `docs/plans/0000-00-00-example-plan.md`
  - `skills/pr/SKILL.md`
  - `skills/verify/SKILL.md`
- Steps:
  - Review the updated docs and skills for done-transition guidance.
  - Confirm they state that when the outcome is known before PR, lifecycle closeout should happen before PR creation.
  - Confirm they state that post-merge closeout is allowed only when merged state is the deciding event for completion.
  - Confirm the post-merge case is clearly presented as an exception, not the default.
- Expected result:
  - Contributors can distinguish normal done closeout from the merge-dependent exception.
- Failure proves:
  - Done-state timing remains ambiguous and contributors could keep active plans stale until an arbitrary later stage.
- Automation location:
  - Manual review during M1 and M2.

### T4. Blocked and superseded transitions are immediate, not deferred

- Covers: `R5`, `R6b`, `E3`, `E4`, `EC3`, `EC4`
- Level: manual
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `docs/plans/0000-00-00-example-plan.md`
  - `skills/verify/SKILL.md`
  - `skills/workflow/SKILL.md`
- Steps:
  - Review the updated workflow and plan-guidance surfaces.
  - Confirm they state that `Blocked` and `Superseded` transitions are recorded as soon as they are decided.
  - Confirm they do not require contributors to wait for PR creation, merge, or retrospective work before updating those states.
- Expected result:
  - Blocked and superseded lifecycle changes are treated as immediate bookkeeping updates in both index and plan body.
- Failure proves:
  - The implementation still leaves a deferral gap for non-done lifecycle transitions.
- Automation location:
  - Manual review during M1, M2, and M3.

### T5. Verify blocks stale lifecycle state and requires lifecycle evidence

- Covers: `R4`, `R7`, `R7a`
- Level: manual
- Fixture/setup:
  - `skills/verify/SKILL.md`
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - plan validation-note conventions in `docs/plans/2026-04-20-plan-index-lifecycle-ownership.md`
- Steps:
  - Review the updated verify guidance and workflow docs.
  - Confirm they explicitly treat stale lifecycle state as blocking PR readiness when relevant.
  - Confirm stale state includes at minimum the mismatches listed in `R7a`.
  - Confirm verification evidence is expected to name the lifecycle-state surfaces reviewed.
- Expected result:
  - `verify` is a concrete gate against stale plan/index drift rather than a vague review suggestion.
- Failure proves:
  - Contributors could still claim PR readiness without reconciling stale lifecycle state.
- Automation location:
  - Manual review during M1 and M2; validation notes review during M3.

### T6. Learn remains retrospective, not bookkeeping authority

- Covers: `R4`, `E5`
- Level: manual
- Fixture/setup:
  - `skills/learn/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `docs/workflows.md`
- Steps:
  - Review `learn` and related workflow guidance.
  - Confirm `learn` is described as retrospective capture of durable lessons.
  - Confirm it is not described as the authoritative owner of lifecycle-state transitions or `docs/plan.md` closeout.
- Expected result:
  - Contributors can use `learn` for retrospectives without treating it as required plan-index bookkeeping.
- Failure proves:
  - The ownership split remains ambiguous and lifecycle closeout could drift into an optional retrospective stage.
- Automation location:
  - Manual review during M2.

### T7. Plan guidance keeps `docs/plan.md` as a one-state lifecycle index

- Covers: `R1`, `R2`, `R3`, `R3a`, `R8`, `R8a`
- Level: integration, manual
- Fixture/setup:
  - `docs/plan.md`
  - `docs/plans/0000-00-00-example-plan.md`
  - `AGENTS.md`
- Steps:
  - Review `docs/plan.md` and confirm it remains an index rather than a plan body.
  - Confirm the example plan teaches contributors to update lifecycle surfaces in the plan body.
  - Run `rg -n "^## (Active|Blocked|Done|Superseded)$" docs/plan.md`.
  - For each currently indexed plan slug, confirm it appears exactly once in `docs/plan.md`.
- Expected result:
  - The plan index remains structurally clear and no indexed plan appears under multiple lifecycle sections.
- Failure proves:
  - The repository still allows index drift or treats `docs/plan.md` as more than a lifecycle index.
- Automation location:
  - M3 validation plus manual review of the example plan.

### T8. Plan bodies do not present done, blocked, or superseded work as still active

- Covers: `R3b`, `R5`, `E1`
- Level: integration, manual
- Fixture/setup:
  - touched plan bodies under `docs/plans/`
  - `docs/plan.md`
- Steps:
  - Review each touched plan body whose lifecycle state is changed by the implementation.
  - Confirm its status line matches the lifecycle state shown in `docs/plan.md`.
  - Confirm its outcome, readiness, and progress wording no longer present the plan as active or in-progress when it is `Done`, `Blocked`, or `Superseded`.
  - Run focused scans for lifecycle wording such as:
    - `rg -n "Status|Outcome and retrospective|Readiness|ready for PR|ready for code-review|complete and now belongs|blocked|superseded" docs/plans/...`
- Expected result:
  - Changed plan bodies no longer present stale active-state wording once lifecycle state changes.
- Failure proves:
  - Index and plan bodies can still disagree about whether an initiative is active.
- Automation location:
  - M3 validation plus manual review of touched plan files.

### T9. Migration corrects already-known stale lifecycle state without over-closing active work

- Covers: `R3`, `R3a`, `R3b`, `R5`, `R7`, `R7a`, `R9`, `E1`, `E2`, `E3`, `E4`, `EC1`
- Level: integration, manual
- Fixture/setup:
  - `docs/plan.md`
  - `docs/plans/2026-04-19-rigorloop-first-release-implementation.md`
  - `docs/plans/2026-04-20-constitution-governance-migration.md`
  - `docs/plans/2026-04-20-plan-index-lifecycle-ownership.md`
- Steps:
  - Compare `docs/plan.md` against each touched concrete plan body.
  - Confirm already-known stale lifecycle state is corrected as part of adoption.
  - Confirm still-active work remains `Active` when verification, review, or closeout is intentionally outstanding.
  - Confirm merge-dependent `Done` handling is recorded explicitly only where it is actually needed.
  - Run the plan-slug uniqueness check named in the active plan.
- Expected result:
  - The migration starts from a truthful lifecycle baseline without guessing new state for active work.
- Failure proves:
  - The change either preserved known stale state or over-corrected into inaccurate historical state.
- Automation location:
  - M3 validation and manual lifecycle comparison.

### T10. No new automation, fake state claims, or heavyweight checks are implied

- Covers: `EC5`
- Level: manual, smoke
- Fixture/setup:
  - updated spec, workflow docs, and skills
  - `bash scripts/ci.sh`
- Steps:
  - Review the updated artifacts and confirm they do not require CI automation or background synchronization to satisfy the lifecycle rule.
  - Confirm they do not claim merge state, CI state, or review completion can be inferred or faked.
  - Run `bash scripts/ci.sh` after the documentation and skill updates are complete.
- Expected result:
  - The change remains lightweight, repo-local, and truthful about what is actually verified.
- Failure proves:
  - The implementation expanded into unapproved automation or introduced workflow claims that the repository cannot honestly support.
- Automation location:
  - M3 validation and final verify smoke pass.

## Fixtures and data

- Real repository workflow and governance files:
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `docs/workflows.md`
  - `specs/rigorloop-workflow.md`
- Real plan surfaces:
  - `docs/plan.md`
  - `docs/plans/0000-00-00-example-plan.md`
  - `docs/plans/2026-04-19-rigorloop-first-release-implementation.md`
  - `docs/plans/2026-04-20-constitution-governance-migration.md`
  - `docs/plans/2026-04-20-plan-index-lifecycle-ownership.md`
- Canonical and generated skill files:
  - `skills/plan/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/learn/SKILL.md`
  - `skills/workflow/SKILL.md`
  - matching generated files under `.codex/skills/`
- Command surfaces:
  - `rg -n ...`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `bash scripts/ci.sh`
  - `git diff --check ...`

## Mocking/stubbing policy

- Do not mock repository files, generated skill output, or plan-index state.
- Do not use snapshots as the primary proof for lifecycle requirements.
- Prefer real tracked files, focused path scans, and existing repo-owned commands over synthetic fixtures.
- If a stale lifecycle state needs demonstration during implementation, use the real tracked before-and-after diff rather than synthetic examples outside the repository artifacts.

## Migration or compatibility tests

- `T3` verifies done-state timing and the merge-dependent exception.
- `T4` verifies immediate handling of blocked and superseded transitions.
- `T8` and `T9` verify lifecycle-state synchronization between `docs/plan.md` and touched plan bodies.
- `T10` verifies the change does not broaden into unapproved automation or fake-state claims.

## Observability verification

- `T5` verifies that `verify` guidance requires lifecycle-state evidence to be named when relevant.
- `T7`, `T8`, and `T9` use focused scans and manual comparison so reviewers can directly inspect lifecycle-state evidence.
- Validation notes in the active plan should name the specific plan-index and plan-body surfaces reviewed during implementation.

## Security/privacy verification

- Review the updated artifacts for fake merge, CI, or review-completion claims.
- Confirm lifecycle bookkeeping remains in tracked repository artifacts rather than chat-only or host-local state.
- Confirm no machine-local paths, usernames, secrets, or debug-only files are introduced while updating docs, plans, or skills.

## Performance checks

- No dedicated performance benchmark is required for this workflow-only change.
- The proof surface should stay limited to lightweight manual review, `rg` path scans, and existing repo-owned validation commands.
- If implementation requires heavier automation or continuous synchronization, return to `spec` or `architecture` before expanding scope.

## Manual QA checklist

- [ ] `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, and `specs/rigorloop-workflow.md` describe the same lifecycle-ownership split.
- [ ] Canonical stage skills and generated `.codex/skills/` agree about who owns `plan`, `implement`, `verify`, final closeout, and `learn`.
- [ ] `docs/plan.md` still reads as an index, not as a plan body.
- [ ] Every indexed plan slug appears exactly once under one lifecycle section in `docs/plan.md`.
- [ ] Touched plan bodies do not present done, blocked, or superseded work as still active.
- [ ] The merge-dependent done path is documented as an exception rather than the default.
- [ ] `verify` guidance treats stale lifecycle state as a readiness blocker.
- [ ] No artifact implies that automation, CI, or `learn` owns lifecycle closeout.

## What not to test

- Do not add new automation or CI enforcement beyond the existing repo-owned command surfaces named in the active plan.
- Do not test hosted PR or branch-protection behavior end to end; this change only defines the repository contract for how contributors must record lifecycle state.
- Do not require exact prose wording where the contract can be satisfied by different but equivalent wording.
- Do not test unrelated workflow, release, schema, or runtime behavior outside the lifecycle-ownership change.
- Do not create synthetic runtime fixtures for plan-state behavior when real tracked repository artifacts provide clearer proof.

## Uncovered gaps

- No uncovered gaps block implementation under the current reviewed spec and active plan.
- If implementation expands into inferred automation, new CI behavior, or a broader redesign of plan structure, return to `spec` or `architecture` before continuing.

## Readiness

This test spec is complete. Its coverage now describes the merged lifecycle-ownership baseline.

No further implementation-stage action is pending for this artifact.
