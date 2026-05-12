# Review Recording Guardrail and Downstream Status Settlement

## Status

draft

## Problem

RigorLoop already has a stage-neutral policy for recording material review findings. Formal lifecycle review skills say that material findings must be recorded under `docs/changes/<change-id>/reviews/<stage>-r<n>.md`, indexed in `review-log.md`, and resolved in `review-resolution.md`.

However, a real `plan-review` failure showed that the policy is not operationally strong enough in skill output. The review reported material finding `PR-001`, but the required durable review record did not exist until the maintainer challenged the omission. The first correction then created a record that still omitted the `Location` field, meaning the durable record did not fully preserve the material-finding shape.

PR #44 attempted to fix this by adding both review-recording output and artifact-status sync behavior to review skills. That mixed two separate problems:

```text
1. Material-finding recording guardrail.
2. Artifact lifecycle/status settlement.
```

The first problem belongs in review skills. The second problem should be handled by downstream skills before they rely on upstream artifacts.

## Goals

- Keep the material-finding recording guardrail across formal lifecycle review skills.
- Require final review output to expose `Recording status`.
- Require complete material-finding shape, including `Location`.
- Require review record, review log, and review-resolution paths when material findings exist.
- Preserve lightweight clean reviews with no material findings.
- Remove artifact-status sync behavior from review skills.
- Remove downstream status-settlement follow-up references from review skills.
- Move full change-ID selection rules and full `Location` examples to the formal review recording spec or reference.
- Record downstream status settlement as a follow-up direction, not first-slice implementation scope.
- Keep artifacts as the durable source of truth.

## Non-goals

- Do not reopen PR #44.
- Do not make review skills update reviewed artifact lifecycle status by default.
- Do not add artifact-status sync fields to every review skill.
- Do not require detailed review files for clean reviews with no material findings and no detailed-record trigger.
- Do not change review-resolution disposition vocabulary.
- Do not create a new review stage.
- Do not add heavy runtime validation in the first slice.
- Do not duplicate long change-ID or `Location` examples in every skill.
- Do not implement downstream status settlement in the first slice.
- Do not define broad automatic status edits without a later settlement-specific plan.

## Vision fit

fits the current vision

This proposal strengthens RigorLoop's commitment to durable, reviewable evidence while keeping skills concise and project-portable.

## Context

The current `plan-review` skill already states that every material finding requires a durable change-local review record, `review-log.md`, and `review-resolution.md`. It also says isolation does not suppress recording. But its expected output does not require a `Recording status`, review artifact paths, or complete finding-shape proof before the review response ends.

A revised recording-only direction already captured the narrower core: make material-finding recording an explicit output obligation across all formal lifecycle review skills, require `Location`, report recording status and artifact paths, keep isolated review behavior, and keep clean reviews lightweight.

PR #44 went beyond that by adding status-settlement behavior to review skills. That PR is closed and should not be reopened.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Keep `Recording status` output | in scope | Goals, Recommended direction |
| Keep complete material-finding shape including `Location` | in scope | Goals, Review skill contract |
| Keep review record / review-log / review-resolution paths | in scope | Review skill contract |
| Keep blocked recording behavior | in scope | Review skill contract |
| Keep static checks across formal review skills | in scope | Testing and verification strategy |
| Keep generated adapter refresh | in scope | Rollout and rollback |
| Remove artifact-status sync from review skills | in scope | Non-goals, Recommended direction |
| Remove downstream status-settlement references from review skills | in scope | Non-goals, Remove from review skills |
| Move full change-ID selection rule elsewhere | in scope | Move elsewhere |
| Move full `Location` examples elsewhere | in scope | Move elsewhere |
| Add downstream status settlement before reliance | follow-up direction | Follow-up direction: downstream status settlement |
| Keep artifacts as source of truth | in scope | Recommended direction |
| Close and do not reopen PR #44 | in scope | Non-goals, Decision log |

## Options considered

### Option 1: Keep PR #44 behavior

This keeps both review-recording output and review-side artifact-status sync.

Advantages:

- Fixes material-finding recording.
- Attempts to fix stale lifecycle status immediately.

Disadvantages:

- Makes review skill changes long.
- Blurs review and authoring responsibilities.
- Risks violating isolated review or no-edit requests.
- Makes review skills responsible for updating the artifacts they review.
- Encodes a debated status-settlement model before the design is settled.

### Option 2: Keep only review-recording guardrail

Advantages:

- Directly fixes the observed failure.
- Keeps review skills concise.
- Preserves reviewer independence.
- Avoids artifact-status sync scope creep.
- Easier to validate statically.

Disadvantages:

- Does not by itself solve stale upstream artifact status before downstream reliance.

### Option 3: Review-recording guardrail plus downstream status settlement

Advantages:

- Fixes the observed material-finding recording lapse.
- Separates review verdict from artifact lifecycle settlement.
- Keeps review skills independent.
- Ensures downstream skills do not rely on stale artifact statuses.
- Preserves artifact status as the durable source of truth.

Disadvantages:

- Requires updates to downstream skills later.
- Requires a simple precondition check before downstream execution.

## Scope

This proposal has two parts:

```text
Accepted first slice:
  formal review recording output guardrail

Follow-up direction:
  downstream status settlement before reliance
```

The first slice updates only formal review skills, formal review recording reference/spec text, static skill-validator coverage, and generated skill/adapters.

Downstream status settlement is not implemented in the first slice unless a later plan explicitly scopes it as a separate milestone after the recording guardrail is complete.

## Recommended direction

Choose Option 3.

Use this responsibility split:

```text
Review skill:
  records review evidence
  records material findings
  may mention stale lifecycle status as an ordinary finding, concern, or note when it affects the reviewed surface

Downstream skill:
  verifies upstream status before relying
  updates stale status if review evidence is clear
  blocks if not clear

Artifact:
  remains the source of truth
```

Review skills should not include a standardized downstream status-settlement result block, status-sync vocabulary, or follow-up proposal references. If lifecycle status appears stale during review, the review may mention it as an ordinary finding, concern, or note when it affects the reviewed surface, but it does not own settlement by default.

The first implementation slice is recording-only:

- `proposal-review`
- `spec-review`
- `architecture-review`
- `plan-review`
- `code-review`
- formal review recording contract/reference text
- static skill-validator coverage
- generated skill/adapters

It does not update downstream authoring or execution skills for upstream status settlement.

## Formal review recording reference update

The first implementation slice must update the formal review recording contract or a linked reference so it owns:

- full change-ID selection rule
- full `Location` examples
- detailed recording artifact rules

Review skills should contain only the concise recording-status block and point to the project review-recording process.

## Review skill contract

Update all formal lifecycle review skills:

```text
proposal-review
spec-review
architecture-review
plan-review
code-review
```

Each formal review skill should include a short recording-status output contract.

### Recording status

Use exactly one:

```text
not-required
recorded
blocked
```

Definitions:

```text
not-required:
  no material findings and no detailed-record trigger

recorded:
  every artifact required by the active recording trigger exists or was updated

blocked:
  required review-recording artifacts could not be created or updated
```

For material findings, `recorded` requires:

```text
detailed review record
review-log.md
review-resolution.md
```

For no-material detailed-record triggers, `recorded` requires:

```text
detailed review record
review-log.md
```

Do not require an empty `review-resolution.md` for a no-material review event.

### Complete material-finding shape

Every material finding must include:

```text
Finding ID
Severity
Location
Evidence
Required outcome
Safe resolution path, or needs-decision rationale
```

### Final review output

Formal review output should include:

```md
## Result

- Skill:
- Review status:
- Material findings:
- Recording status:
- Recording blocker:
- Review record:
- Review log:
- Review resolution: <path | not-required | blocked>
- Open blockers:
- Immediate next stage:
```

`Recording status` is not the review verdict. It reports whether required review-recording artifacts were created, were not required, or are blocked.

### Concise recording block

Use this short block in each formal review skill:

```md
## Recording status output

`Recording status` is separate from the review verdict.

Use exactly one:

- `not-required`: no material findings and no detailed-record trigger.
- `recorded`: required review-recording artifacts were created or updated.
- `blocked`: required review-recording artifacts could not be created or updated.

For material findings, `recorded` requires a detailed review record, `review-log.md`, and `review-resolution.md`.

For no-material detailed-record triggers, `recorded` requires a detailed review record and `review-log.md`. Do not require an empty `review-resolution.md` for a no-material review event.

If `Recording status: blocked`, include `Recording blocker` and the smallest action needed.

Do not merely tell the user that review artifacts should be created. Create or update them before final output, or report `Recording status: blocked`.

Every material finding must include Finding ID, Severity, Location, Evidence, Required outcome, and Safe resolution path or `needs-decision` rationale.
```

Do not include artifact-status sync in this block.

## Remove from review skills

Remove these concepts from formal review skill changes:

```text
Status settlement recommendation
artifact-status sync
Status sync
Status artifact
Status sync blocker
downstream status settlement follow-up references
long change-ID algorithm duplicated in every skill
long Location examples duplicated in every skill
```

Review skills may mention stale lifecycle status only as a normal review finding, concern, or note when it affects the reviewed surface.

They must not include a standardized `Status settlement recommendation`, `Status sync`, `Status artifact`, or `Status sync blocker` field in this slice.

## Move elsewhere

Move the full change-ID selection rule to:

```text
specs/formal-review-recording.md
```

or a formal review recording reference.

Move full `Location` examples to:

```text
specs/formal-review-recording.md
```

or a formal review recording reference.

Do not duplicate those details in every skill.

## Follow-up direction: downstream status settlement

Downstream skills must not rely on upstream artifacts whose durable status contradicts clear review evidence.

This direction is not implemented in the first slice. A follow-up proposal, plan, or later milestone must define the exact settlement contract before downstream skills are changed.

Before a downstream skill relies on an upstream artifact, it should check:

```text
Is the upstream artifact status settled?
Is there clear approving review evidence?
Are there unresolved material findings?
Is the status update deterministic?
Are edits allowed?
```

If the review result is clear and no unresolved findings remain, the downstream skill may perform minimal lifecycle-status settlement before continuing.

If the settlement is ambiguous, forbidden, or unsafe, the downstream skill must stop and report a blocker.

### Downstream status settlement result

Downstream skills should report:

```md
## Upstream status settlement

- Upstream artifact:
- Review evidence:
- Previous status:
- New status:
- Settlement result: not-needed | updated | blocked
- Settlement blocker:
```

### Examples

If `spec` is about to rely on a proposal:

```text
proposal Status: draft
proposal-review result: approved
open findings: none
```

Then `spec` may update:

```text
proposal Status: accepted
```

before executing.

If findings remain open:

```text
Settlement result: blocked
Reason: proposal-review has unresolved findings
Next stage: review-resolution or proposal revision
```

## Downstream skills affected

This proposal defines the follow-up direction. A later implementation can update these skills as needed:

```text
spec
architecture
plan
test-spec
implement
explain-change
verify
pr
```

Minimum first downstream slice:

```text
spec
architecture
plan
implement
verify
```

because those are most likely to rely on upstream artifact readiness.

### Follow-up questions

- Which downstream skills participate first?
- Which artifact statuses can be settled automatically?
- What review evidence is sufficient?
- What fields may be edited?
- What happens when the user forbids edits?
- What validation proves settlement occurred safely?

## Expected behavior changes

Before:

```text
review skill may say records should be created
but not create them
```

After:

```text
review skill must report Recording status: recorded or blocked
```

Before:

```text
review skills may grow long with status-sync rules
```

After:

```text
review skills stay focused on review evidence and material-finding recording
```

Follow-up direction:

```text
downstream skills should eventually settle stale upstream status before relying, or block
```

## Architecture impact

No runtime architecture change is expected.

This is a skill-contract and workflow-execution improvement. The first slice affects formal review skills, formal review recording reference text, static validation, and generated output.

Affected surfaces may include:

```text
skills/proposal-review/SKILL.md
skills/spec-review/SKILL.md
skills/architecture-review/SKILL.md
skills/plan-review/SKILL.md
skills/code-review/SKILL.md

specs/formal-review-recording.md
scripts/test-skill-validator.py
generated .codex/skills/
generated dist/adapters/
```

Downstream status settlement surfaces are follow-up scope and are intentionally excluded from the first slice.

## Testing and verification strategy

First slice: static skill guidance and generated output validation.

Add static checks that every formal review skill contains:

```text
Recording status
not-required
recorded
blocked
Finding ID
Severity
Location
Evidence
Required outcome
Safe resolution path
review record
review-log.md
review-resolution.md
Do not merely tell the user that review artifacts should be created
```

Also add negative exact field checks that formal review skills do not contain:

```text
- Status settlement recommendation:
- Status sync:
- Status artifact:
- Status sync blocker:
```

Do not fail explanatory prose that says artifact-status sync is out of scope.

For the required formal review recording reference update, validate that the reference owns:

```text
change-ID selection
Location examples
detailed recording artifact rules
```

Suggested validation:

```bash
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version 0.1.1 --check
python scripts/validate-adapters.py --version 0.1.1
git diff --check --
```

If review artifacts are created during implementation:

```bash
python scripts/validate-review-artifacts.py
```

## Rollout and rollback

### Slice 1. Review recording output guardrail

- Update five formal review skills.
- Update the formal review recording contract or linked reference.
- Keep recording block concise.
- Remove artifact-status sync language.
- Add static validator coverage.
- Regenerate public skills/adapters.
- Validate.

### Follow-up. Downstream status settlement

- Define exact settlement rules in a follow-up proposal, plan, or later milestone.
- Identify participating downstream skills.
- Define sufficient review evidence, allowed status fields, no-edit behavior, and validation.
- Update downstream skills only after that scope is approved.

Rollback:

- Revert review-skill recording output changes if they cause incorrect artifact creation or conflict with the approved formal review recording contract.
- Revert downstream settlement wording if it causes unsafe status edits or ambiguous ownership.
- Keep any valid review records created under the existing artifact model.
- Regenerate generated skill and adapter output after any canonical rollback.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Review skills remain too long | Use the concise recording block only |
| Review skills lose material-finding rigor | Preserve complete finding shape |
| Downstream settlement remains unresolved after Slice 1 | Track as follow-up direction with explicit questions |
| Later settlement causes unsafe edits | Require a separate approved contract before downstream skill changes |
| Change-ID selection becomes inconsistent | Move full rule to spec/reference |
| `Location` guidance becomes too verbose | Move examples to spec/reference |
| Generated outputs drift | Regenerate and validate adapters |

## Open questions

- Should the full change-ID and `Location` reference live directly in `specs/formal-review-recording.md` or in a small linked reference file?
- Which downstream status-settlement questions should be answered in a follow-up proposal versus a later implementation plan?

## Decision log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-05-12 | Close PR #44 and restart with narrower scope. | The prior PR mixed review-recording guardrails with artifact-status sync and made skill changes too large. | Keep PR #44 behavior. |
| 2026-05-12 | Keep material-finding recording guardrail. | It directly fixes the observed repeated failure. | Drop the recording guardrail. |
| 2026-05-12 | Remove artifact-status sync from review skills. | Review skills should record verdict and findings, not own artifact settlement by default. | Make review skills update reviewed artifacts. |
| 2026-05-12 | Move downstream status settlement to follow-up direction for relying skills. | Downstream skills should eventually reconcile upstream status before relying, but this first slice must stay recording-only. | Bundle downstream settlement into the first slice. |
| 2026-05-12 | Move long change-ID and `Location` details to formal recording spec/reference. | Avoid duplicating long policy in every review skill. | Copy full rules into every review skill. |

## Next artifacts

- proposal-review
- focused formal review recording spec/reference update
- implementation plan
- skill-validator update
- review skill updates
- generated adapter refresh
- optional downstream status-settlement follow-up proposal
- explain-change
- verify

## Follow-on artifacts

None yet.

## Readiness

Ready for proposal-review.

This proposal narrows the first implementation slice to the actual repeated failure: material findings must be durably recorded or explicitly blocked. It records downstream artifact lifecycle settlement as follow-up direction for the skills that rely on reviewed artifacts.

## Core invariant

```text
Review records evidence.
Downstream settles status before reliance.
Artifacts remain the source of truth.
```
