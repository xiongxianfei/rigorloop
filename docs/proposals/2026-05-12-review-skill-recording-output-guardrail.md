# Review Skill Recording and Status Output Guardrail

## Status

accepted

## Problem

RigorLoop already has stage-neutral policy for durable material-finding records. `CONSTITUTION.md`, `specs/formal-review-recording.md`, and the accepted Review Skill Material Finding Recording proposal all say that material findings from formal lifecycle reviews must be recorded, including isolated or review-only requests.

The remaining failure mode is execution: a review skill can still report a material finding in final chat output without making the recording action observable and complete. In the documented lapse, `plan-review` reported material finding `PR-001`, but the expected change-local review record did not exist until the maintainer challenged the omission. The first correction then created the review record but omitted `Location`, so the durable record did not fully preserve the finding shape.

This is not only a `plan-review` problem. The same class of omission can occur in any formal lifecycle review skill:

- `proposal-review`
- `spec-review`
- `architecture-review`
- `plan-review`
- `code-review`

The policy exists. The review skills need a sharper output-flow guardrail so a material finding is not treated as fully reported until it is durably recorded or a concrete recording blocker is reported.

A related gap appears after clean approvals. The learn session [Review Approval Status Sync](../learn/sessions/2026-05-12-review-approval-status-sync.md) records that `proposal-review` can return `approved` while the reviewed proposal remains `Status: draft` until someone manually updates it. That leaves chat review status and tracked artifact lifecycle status out of sync even when the review result is clean. Because lifecycle-managed artifacts keep status inside the artifact as the durable source of truth, review skills should either update the corresponding artifact to its next artifact-specific status or report exactly why that status sync is blocked.

## Goals

- Make material-finding recording an explicit output obligation across all formal lifecycle review skills.
- Require complete material-finding shape in durable records, including `Location`.
- Require final review output to report recording status and artifact paths when material findings exist.
- Require approving or clean formal review results to synchronize the reviewed artifact to its next artifact-specific lifecycle status when the status surface is clear.
- Require final review output to report artifact-status sync status when an approving or clean result is returned.
- Preserve isolation semantics: direct and review-only requests do not continue downstream automatically, but still record material findings.
- Keep clean reviews with no material findings lightweight.
- Keep the change skill-focused and aligned with the existing formal review recording spec.
- Avoid adding heavy semantic automation in the first slice.

## Non-goals

- Do not create a new review stage.
- Do not change the review-resolution disposition vocabulary.
- Do not require detailed review files for clean reviews with no material findings and no detailed-record trigger.
- Do not make isolated reviews automatically continue to downstream workflow stages.
- Do not make review skills edit reviewed artifact content beyond the minimal lifecycle-status, readiness, follow-on, or closeout fields needed to make the clean review result durable.
- Do not force a status edit when the reviewed artifact has no clear owned status surface, when multiple lifecycle owners disagree, or when the user forbids edits.
- Do not replace the existing shared `## Isolation and Recording` block.
- Do not introduce semantic validation that decides whether a finding should have been material in the first slice.
- Do not make this only a `plan-review` fix.

## Vision fit

fits the current vision

This proposal strengthens RigorLoop's commitment that review concerns, validation evidence, and lifecycle status are reconstructable from durable tracked artifacts rather than chat history.

## Context

The accepted [Review Skill Material Finding Recording](2026-05-07-review-skill-material-finding-recording.md) proposal and approved [Formal Review Recording](../../specs/formal-review-recording.md) spec already establish the stage-neutral policy:

- formal lifecycle reviews are `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review`;
- isolation controls handoff, not recording;
- material findings require durable change-local review records;
- material findings require `review-resolution.md`;
- clean no-material reviews can remain lightweight when no detailed-record trigger applies.

Those artifacts addressed the policy ambiguity. The new evidence shows an operating-flow ambiguity: agents can still stop at saying what should be recorded instead of creating the required records or reporting why they could not.

The current review skills also vary in how directly their expected output exposes recording status. The guardrail should be common across all formal review skills so a recurrence does not move from `plan-review` to another review stage.

The approval-status sync learn session adds a related direction: a clean approving review should not leave the durable reviewed document in a pre-review status. Current workflow guidance already distinguishes artifact-specific lifecycle vocabulary:

- proposals settle as `accepted`;
- specs and architecture documents settle as `approved`;
- test specs settle as `active`;
- plans use plan-owned readiness and lifecycle state;
- code-review clean outcomes close or advance the review or milestone state in the active plan or required review record rather than changing source code status.

## Initial Intent Preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Add the material-finding recording guardrail | in scope | Goals, Recommended direction |
| Do not limit the fix to `plan-review` | in scope | Problem, Goals, Recommended direction |
| Apply the pattern to all review skills | in scope | Recommended direction, Architecture impact |
| Require complete finding shape including `Location` | in scope | Recommended direction, Expected behavior changes |
| Report recording status in final review output | in scope | Recommended direction, Expected behavior changes |
| Preserve isolated review behavior | in scope | Goals, Non-goals, Expected behavior changes |
| Keep clean reviews lightweight | in scope | Goals, Non-goals |
| Avoid heavy automation first | in scope | Non-goals, Testing and verification strategy |
| On approving or clean review, update the corresponding document directly to its next status | in scope | Goals, Recommended direction, Expected behavior changes |
| Allow manual review/status updates when needed | in scope | Non-goals, Recommended direction |
| Use the approval-status sync learn session as evidence | in scope | Problem, Context, Follow-on artifacts |

## Options Considered

### Option 1: Update only `plan-review`

This addresses the observed lapse directly, but it contradicts the stage-neutral review policy already accepted for the repository. It would leave the same output-flow gap in `proposal-review`, `spec-review`, `architecture-review`, and `code-review`.

### Option 2: Add validator-only enforcement

Validator checks can catch missing phrases or malformed records after edits, but they do not guide the reviewer at the moment a finding is reported. A validator-only fix would still let agents produce incomplete final review output and defer the issue to a later stage.

### Option 3: Add a common recording-status output contract to all formal review skills

This is the recommended option. It keeps the existing artifact model and isolation policy, but makes review completion observable: material findings are either recorded with paths, or blocked with a concrete reason and smallest next action.

### Option 4: Require detailed records for every formal review

This is simple, but too heavy. It would erase the existing proportional path for clean no-material reviews and create low-value change-local artifacts.

### Option 5: Report clean approval but leave artifact status updates manual

This preserves strict review-only isolation, but it keeps the observed drift: chat says the review passed while the tracked artifact remains in a draft or unresolved lifecycle state.

### Option 6: Add artifact-status synchronization for clean approving review outcomes

This is now included in the recommended direction. It keeps review skills from silently claiming lifecycle progress while the tracked artifact still says otherwise. The status update is narrow: it changes only the reviewed artifact's lifecycle/status/readiness/closeout surface, uses artifact-specific vocabulary, and blocks rather than guessing when the status owner is ambiguous.

## Recommended Direction

Choose Option 3 plus Option 6.

Update every formal lifecycle review skill so material-finding recording is part of the required output flow:

- `skills/proposal-review/SKILL.md`
- `skills/spec-review/SKILL.md`
- `skills/architecture-review/SKILL.md`
- `skills/plan-review/SKILL.md`
- `skills/code-review/SKILL.md`

Each review skill should say that when the review produces one or more material findings, the review is not complete until the required durable review artifacts are created or a concrete blocker is reported.

Each review skill should also say that when the review returns an approving or clean outcome, the review is not complete until the reviewed artifact's owned status surface is synchronized to the next artifact-specific state or a concrete status-sync blocker is reported.

Status sync is allowed in workflow-managed reviews and isolated or review-only reviews because it updates the reviewed artifact's own lifecycle surface; it is not downstream continuation. However, explicit user instructions such as "review only, do not modify files" override that default. When edits are forbidden, the review skill should report `Status sync: blocked`, name the intended next status, and state the smallest manual action needed.

The shared operating pattern should include this recording-status contract:

```text
Recording status:
- not-required
- recorded
- blocked
```

Use `not-required` only when there are no material findings and no detailed-record trigger. Use `recorded` when every artifact required by the active recording trigger exists or was updated. Use `blocked` when required recording artifacts cannot be created or updated because the change ID remains ambiguous, repository state is unavailable, the user forbids edits, or another concrete blocker exists.

For material findings, `recorded` requires:

- detailed review record;
- `review-log.md`;
- `review-resolution.md`.

For no-material detailed-record triggers, `recorded` requires:

- detailed review record;
- `review-log.md`.

`review-resolution.md` is required only when material findings exist or another approved review-resolution trigger applies.

When `recorded`, final output should name:

- review record path;
- review-log path;
- review-resolution path when material findings exist.

When `blocked`, final output should name:

- the material Finding IDs;
- the recording blocker;
- the smallest action needed to create the durable record;
- the fact that downstream handoff remains stopped.

Every material finding recorded by a review skill should preserve a complete finding shape:

- Finding ID
- Severity
- Location
- Evidence
- Required outcome
- Safe resolution path, or `needs-decision` rationale

`Location` is required, but it may describe more than an exact line. Valid locations include:

- file path and section;
- file path and line or range, when known;
- artifact and milestone or requirement ID;
- missing expected artifact path;
- review surface plus a "not present" rationale when the issue is an absence.

The location must be specific enough that a future reader can find the affected surface without chat history.

When recording is required, review skills should choose the change ID in this order:

1. active `docs/changes/<change-id>/change.yaml`, when the reviewed work already has a change root;
2. active plan or reviewed artifact metadata, when it names the change ID;
3. user-provided change ID;
4. generated review-recording change ID: `YYYY-MM-DD-<reviewed-artifact-or-topic>-review-recording`.

If the change ID is still ambiguous, use `Recording status: blocked` and state the smallest action needed.

The five formal review skills should use the same concise recording-status block. For this slice, use a shared canonical snippet if the repository already has an accepted shared-skill snippet surface for this kind of block; otherwise copy the same wording into each canonical skill and let static validation check the required heading, vocabulary, and complete finding shape across all five skills.

Expected review output should keep review outcome and recording state separate:

```md
## Result

- Skill:
- Review status:
- Material findings:
- Recording status:
- Recording blocker:
- Status sync:
- Status artifact:
- Status sync blocker:
- Review record:
- Review log:
- Review resolution:
- Open blockers:
- Immediate next stage:
```

`Recording status` is not the review verdict. It reports whether required review-recording artifacts were created, were not required, or are blocked.

`Status sync` is also not the review verdict. It reports whether the reviewed artifact's durable lifecycle/status surface was updated, was not required, or is blocked.

`Recording blocker` is required when `Recording status: blocked`.

`Status sync blocker` is required when `Status sync: blocked`.

Add a separate artifact-status sync contract:

```text
Status sync:
- not-required
- updated
- blocked
```

Use `not-required` when the review outcome is not approving or clean, or when no lifecycle status change is expected for that review result. Use `updated` when the reviewed artifact's owned status surface was updated to the next artifact-specific state. Use `blocked` when the review result is approving or clean but the artifact status could not be updated because the status owner is ambiguous, the artifact lacks an editable status surface, the user forbids edits, repository state is unavailable, or another concrete blocker exists.

For artifact-specific next states, preserve current lifecycle vocabulary unless a later accepted proposal changes it:

| Review skill | Clean or approving review result | Status sync target |
|---|---|---|
| `proposal-review` | `approved` | proposal `Status: accepted` |
| `spec-review` | `approved` | spec `Status: approved` |
| `architecture-review` | `approved` for architecture package | architecture `Status: approved` |
| `architecture-review` | `approved` for ADR | ADR `Status: accepted` or `Status: active`, according to the ADR's existing lifecycle field |
| `plan-review` | `approve` | plan review/readiness section says ready for `test-spec`; `docs/plan.md` index updated only if the index owns active-plan state |
| `code-review` | `clean` or `clean-with-notes` | active plan milestone state updated according to the milestone contract; no source artifact status edit unless the reviewed artifact explicitly owns that state |

If the next status cannot be chosen from this table or an artifact-local lifecycle field, use `Status sync: blocked`.

When `updated`, final output should name the artifact path and the exact status field or section changed.

When `blocked`, final output should name the intended next status, the blocker, and the smallest manual action needed.

The guardrail should fit alongside the existing shared `## Isolation and Recording` block rather than replacing it. The shared block continues to own policy. The new guardrail makes the required action and final output observable.

## Expected Behavior Changes

Before this change, a review skill could report a material finding and only tell the user that records should be created.

After this change, a review skill that reports material findings creates or updates the required durable review artifacts before final output, unless it reports `Recording status: blocked` with a concrete blocker.

Before this change, a durable review record could look complete while missing `Location`.

After this change, review skills treat `Location` as part of the complete material-finding shape.

Before this change, final review output did not consistently expose whether material-finding recording happened.

After this change, formal review output includes recording status and relevant artifact paths or blocker details.

Before this change, a clean approving review could leave the reviewed artifact in `draft`, unresolved, or pre-review state until a later manual edit.

After this change, a clean approving review updates the corresponding artifact to the next artifact-specific status when the status owner is clear, or reports `Status sync: blocked` with the manual action required.

Clean reviews with no material findings remain lightweight and can report `Recording status: not-required` when no detailed-record trigger applies.

No-material detailed-record triggers can report `Recording status: recorded` with a detailed review record and `review-log.md` while omitting `review-resolution.md` unless another approved review-resolution trigger applies.

## Architecture Impact

This is a workflow/review contract, skill-contract, and validation change. It does not require a new runtime component, storage location, review stage, or artifact family.

Expected touched surfaces:

- `specs/formal-review-recording.md` or another focused formal review output contract surface
- `skills/proposal-review/SKILL.md`
- `skills/spec-review/SKILL.md`
- `skills/architecture-review/SKILL.md`
- `skills/plan-review/SKILL.md`
- `skills/code-review/SKILL.md`
- static skill-validator tests for the recording-status output contract
- static skill-validator tests for the artifact-status sync output contract
- generated `.codex/skills/` output after canonical skill edits
- generated public adapter output under `dist/adapters/` after canonical skill edits

The implementation may also update shared templates, lifecycle validation expectations, workflow docs, governance docs, or contributor documentation if that is the smallest way to keep the review skill family consistent.

## Testing and Verification Strategy

Use skill guidance plus static checks in the first slice.

Static skill-validator coverage should confirm that all five formal review skills contain:

- `Recording status`
- `Review status`
- `not-required`
- `recorded`
- `blocked`
- `Status sync`
- `updated`
- `Recording blocker`
- `Status sync blocker`
- `Finding ID`
- `Severity`
- `Location`
- `Evidence`
- `Required outcome`
- `Safe resolution path`
- `review record`
- `review-log.md`
- `review-resolution.md`
- language equivalent to "Do not merely tell the user that these files should be created"
- language explaining that `Recording status` is not the review verdict
- language explaining that `Status sync` is not the review verdict
- language requiring `Recording blocker` when `Recording status: blocked`
- language requiring `Status sync blocker` when `Status sync: blocked`
- the change ID selection order or reference to the shared section that defines it
- artifact-specific next statuses or a reference to the shared section that defines them

Generated output should be refreshed and validated after canonical skill edits.

Lifecycle validation or artifact lifecycle tests should confirm that accepted review results do not leave touched lifecycle-managed artifacts in stale pre-review statuses when the status surface is clear.

Expected validation:

```bash
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version 0.1.1 --check
python scripts/validate-adapters.py --version 0.1.1
git diff --check --
```

Selector-selected CI may add review-artifact or lifecycle checks depending on touched files.

If a formal review skill again reports material findings without `Recording status: recorded` or `Recording status: blocked`, create a follow-up proposal for runtime or output validation. The first slice uses static skill checks only.

## Rollout and Rollback

Rollout:

1. Accept proposal after proposal-review.
2. Add a focused spec amendment for formal review output recording and artifact-status sync.
3. Update all five formal review skills with the recording-status and artifact-status sync output guardrails.
4. Add static skill-validator coverage.
5. Add or update lifecycle validation coverage if existing validators can check clear status-sync cases without semantic review judgment.
6. Regenerate `.codex/skills/` and public adapter output.
7. Run focused validation and selector-selected CI.

Rollback:

- Revert the skill wording, validator checks, and regenerated outputs if the guardrail causes incorrect record creation or conflicts with the approved formal review recording contract.
- Revert artifact-status sync wording or validation if it causes review skills to edit the wrong lifecycle owner or overstep isolated review boundaries.
- Keep any valid review records created under the existing artifact model; the rollback affects guidance, not artifact compatibility.

Execution planning should split implementation into two milestones:

- M1: recording-status guardrail across formal review skills.
- M2: artifact-status sync guardrail for clean or approving outcomes.

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Review skills become repetitive | Use a concise shared pattern and avoid restating the whole formal review recording policy. |
| Agents create records for clean reviews | Keep `not-required` explicit for no-material reviews with no detailed-record trigger. |
| Agents edit files during isolated review when edits are forbidden | Use `blocked` and report the blocker instead of silently skipping recording. |
| Finding shape becomes too rigid | Require only the fields needed to reconstruct a material finding without chat history. |
| The new wording drifts across review skills | Use the same concise wording across the review skill family and add static assertions across all formal review skills. |
| The guardrail duplicates the shared `Isolation and Recording` block | Treat the shared block as policy and this proposal as output-flow guidance. |
| Review skills update the wrong artifact status | Use artifact-specific vocabulary and block when status ownership is ambiguous. |
| Status sync weakens isolated-review behavior | Limit status sync to the reviewed artifact's own lifecycle surface; do not auto-continue to downstream authoring or implementation stages. |
| `approved` review status is confused with proposal `accepted` status | Keep review outcome separate from artifact lifecycle status and preserve artifact-specific vocabulary. |
| The first implementation slice becomes too broad | Split the execution plan into M1 recording-status guardrails and M2 artifact-status sync guardrails. |

## Open Questions

None that block proposal-review.

Implementation may still decide whether the guardrail appears as a single combined status section in each review skill or is integrated into each skill's existing expected-output section, as long as the shared recording-status and artifact-status sync contracts are present and validated consistently.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-05-12 | Broaden the guardrail from `plan-review` to all formal review skills. | The repository policy is stage-neutral and the same output-flow lapse can occur in any formal review stage. | Update only `plan-review`. |
| 2026-05-12 | Keep clean no-material reviews lightweight. | The existing formal review recording contract is proportional and should not create empty records for routine clean reviews. | Require detailed records for every review. |
| 2026-05-12 | Prefer explicit recording status over heavy semantic automation in the first slice. | The immediate gap is skill execution and observable final output, not semantic classification. | Add semantic validator enforcement first. |
| 2026-05-12 | Define `recorded` by the active recording trigger. | No-material detailed-record triggers require a review record and review log but not necessarily `review-resolution.md`. | Treat `recorded` as always requiring `review-resolution.md`. |
| 2026-05-12 | Add deterministic change ID selection before blocking. | Review skills need a consistent change-local path for isolated reviews that lack an existing change root. | Block whenever no change root already exists; invent paths ad hoc. |
| 2026-05-12 | Require flexible but specific `Location` values. | Some material findings are about absent evidence or missing artifacts rather than one line of text. | Require only file-and-line locations; allow missing locations. |
| 2026-05-12 | Treat recurrence as the trigger for runtime or output validation. | Static checks are a proportional first slice, but another omission would prove guidance alone is insufficient. | Add runtime/output validation immediately; never escalate beyond static checks. |
| 2026-05-12 | Add artifact-status sync for approving and clean review outcomes. | The approval-status sync learn session showed that chat review approval can drift from tracked artifact lifecycle status. | Leave status updates manual-only; use one universal `approved` status for all artifact types. |
| 2026-05-12 | Preserve artifact-specific lifecycle vocabulary. | Current workflow guidance uses `accepted` for proposals, `approved` for specs and architecture, and plan-owned lifecycle state for plans. | Rename all approving statuses to `approved`; ignore plan-owned status surfaces. |
| 2026-05-12 | Require a focused spec amendment for the recording/status-sync output contract. | Artifact-status sync is cross-review normative behavior and should not live only in skill prose. | Implement only in skills. |
| 2026-05-12 | Respect explicit no-edit instructions during isolated reviews. | Status sync edits the reviewed artifact even though it is not downstream continuation. | Always edit on isolated approval; never edit during isolated review. |
| 2026-05-12 | Split implementation planning into recording-status and artifact-status milestones. | The combined change touches five review skills, validators, generated output, and lifecycle behavior. | Implement everything as one broad slice. |

## Next Artifacts

- proposal-review
- focused spec amendment for formal review output recording and artifact-status sync
- implementation plan for review skill and validator updates
- skill-validator update
- generated skill and adapter refresh
- explain-change
- verify

## Follow-on Artifacts

- Proposal-review: approved with no material findings.
- Proposal-review R2: changes requested with material findings `RSG-F2` through `RSG-F6`, all accepted and closed after proposal revision.
- Proposal-review R3: approved with no material findings.
- Learn session: [Review Approval Status Sync](../learn/sessions/2026-05-12-review-approval-status-sync.md).

## Readiness

Accepted after proposal-review.

This proposal keeps the existing formal review recording policy and artifact model. It adds output-flow guardrails across all review skills so a material finding is not fully reported until it is durably recorded or recording is explicitly blocked, and a clean approving review does not leave the reviewed artifact's durable status stale when the status owner is clear.
