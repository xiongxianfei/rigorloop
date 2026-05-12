# Review Recording Guardrail and Downstream Status Settlement

## Status

accepted

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
- Keep normative change-ID and `Location` rules in the formal review recording spec or reference.
- Move full change-ID, `Location`, plan, and shipped change-pack examples under `docs/examples/` where practical.
- Record downstream status settlement as the follow-up model, not first-slice implementation scope.
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
- Do not treat `docs/examples/**` as active lifecycle state.
- Do not move example fixtures without updating all validator and selector references in the same slice.

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
| Move full change-ID selection rule elsewhere | in scope | Move examples elsewhere |
| Move full `Location` examples elsewhere | in scope | Move examples elsewhere |
| Put examples under `docs/examples/` | in scope | Move examples elsewhere, Examples cleanup acceptance criteria |
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
  formal review recording output guardrail and examples cleanup

Follow-up direction:
  downstream status settlement before reliance
```

The first slice updates formal review skills, formal review recording reference/spec text, docs examples surfaces, static skill-validator coverage, and generated skill/adapters.

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

The first implementation slice is limited to review recording and examples cleanup:

- `proposal-review`
- `spec-review`
- `architecture-review`
- `plan-review`
- `code-review`
- formal review recording contract/reference text
- `docs/examples/` cleanup
- static skill-validator coverage
- generated skill/adapters

It does not update downstream authoring or execution skills for upstream status settlement.

## Formal review recording reference update

The first implementation slice must update the formal review recording contract or a linked reference so it owns the normative rules for:

- full change-ID selection rule
- required `Location` behavior
- detailed recording artifact rules

Full examples should live under `docs/examples/formal-review-recording/` instead of every skill or active lifecycle directories.

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

## Move examples elsewhere

Normative rules remain in:

```text
specs/formal-review-recording.md
```

or a linked formal review recording reference.

Examples move to:

```text
docs/examples/
```

Planned example surfaces:

- `docs/examples/README.md`
- `docs/examples/formal-review-recording/change-id-selection-examples.md`
- `docs/examples/formal-review-recording/material-finding-location-examples.md`
- `docs/examples/plans/example-plan.md`
- `docs/examples/changes/skill-validator/`

Examples are non-normative and must not be treated as active lifecycle artifacts.

Do not duplicate those details in every skill.

## Follow-up direction: downstream status settlement

Downstream skills must not rely on stale upstream artifact status.

This direction is not implemented in the first slice. A follow-up proposal, plan, or later milestone must define the exact settlement contract before downstream skills are changed.

Downstream skill execution implies minimal upstream lifecycle-status settlement is allowed. Review-only or manual inspection requests remain isolated; this rule applies when a downstream authoring or execution skill is actually running and needs to rely on upstream artifacts.

Before a downstream skill relies on an upstream artifact, it should check:

```text
upstream artifact path
review evidence
unresolved material findings
current artifact status
expected settled status
```

If review evidence is clear, final, and has no unresolved material findings, the downstream skill updates the minimal lifecycle/status fields and continues.

If the evidence is unclear, contradictory, missing, or has unresolved material findings, the downstream skill blocks.

Allowed edits are limited to lifecycle/status surfaces:

- `Status`
- readiness
- follow-on artifacts
- closeout or lifecycle metadata

Downstream settlement must not rewrite substantive artifact content.

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

This is a skill-contract and workflow-execution improvement. The first slice affects formal review skills, formal review recording reference text, examples, static validation, and generated output.

Affected surfaces may include:

```text
skills/proposal-review/SKILL.md
skills/spec-review/SKILL.md
skills/architecture-review/SKILL.md
skills/plan-review/SKILL.md
skills/code-review/SKILL.md

specs/formal-review-recording.md
docs/examples/README.md
docs/examples/formal-review-recording/
docs/examples/plans/example-plan.md
docs/examples/changes/skill-validator/
docs/plans/0000-00-00-example-plan.md
docs/changes/0001-skill-validator/
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
Location rule
detailed recording artifact rules
```

Examples cleanup acceptance criteria:

- `docs/examples/README.md` exists and states examples are non-normative.
- `docs/plans/0000-00-00-example-plan.md` is moved to `docs/examples/plans/example-plan.md`.
- `docs/changes/0001-skill-validator/` is moved to `docs/examples/changes/skill-validator/`, or retained with explicit rationale if validator coupling makes it a separate slice.
- Tests and validators that reference moved examples are updated.
- `docs/examples/**` is routed or ignored consistently by selector/lifecycle validation.

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

### Slice 1. Review recording output guardrail and examples cleanup

- Update five formal review skills.
- Update the formal review recording contract or linked reference.
- Add `docs/examples/README.md`.
- Move the example plan to `docs/examples/plans/example-plan.md`.
- Move the shipped example change pack to `docs/examples/changes/skill-validator/`, or retain it with explicit rationale if validator coupling makes that a separate slice.
- Keep recording block concise.
- Remove artifact-status sync language.
- Add static validator coverage.
- Update tests, validators, and selectors that reference moved examples.
- Regenerate public skills/adapters.
- Validate.

### Follow-up. Downstream status settlement

- Define exact settlement rules in a follow-up proposal, plan, or later milestone.
- Identify participating downstream skills.
- Define sufficient review evidence, allowed lifecycle/status fields, blocking behavior, and validation.
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
| Example move breaks validator fixtures | Move examples only when references are updated in the same slice, or retain with explicit rationale |
| `docs/examples/**` is mistaken for active lifecycle state | Document examples as non-normative and update selector/lifecycle handling |
| Downstream settlement remains unresolved after Slice 1 | Track as follow-up direction with explicit questions |
| Later settlement causes unsafe edits | Require a separate approved contract before downstream skill changes |
| Change-ID selection becomes inconsistent | Move full rule to spec/reference |
| `Location` guidance becomes too verbose | Keep normative rule in spec/reference and examples in `docs/examples/` |
| Generated outputs drift | Regenerate and validate adapters |

## Open questions

- Should the full change-ID and `Location` rules live directly in `specs/formal-review-recording.md` or in a small linked reference file?
- Should `docs/changes/0001-skill-validator/` move in Slice 1 or be retained temporarily with explicit fixture-coupling rationale?
- Which downstream status-settlement questions should be answered in a follow-up proposal versus a later implementation plan?

## Decision log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-05-12 | Close PR #44 and restart with narrower scope. | The prior PR mixed review-recording guardrails with artifact-status sync and made skill changes too large. | Keep PR #44 behavior. |
| 2026-05-12 | Keep material-finding recording guardrail. | It directly fixes the observed repeated failure. | Drop the recording guardrail. |
| 2026-05-12 | Remove artifact-status sync from review skills. | Review skills should record verdict and findings, not own artifact settlement by default. | Make review skills update reviewed artifacts. |
| 2026-05-12 | Move downstream status settlement to follow-up direction for relying skills. | Downstream skills should eventually reconcile upstream status before relying, but this first slice must stay recording-only. | Bundle downstream settlement into the first slice. |
| 2026-05-12 | Keep normative change-ID and `Location` rules in formal recording spec/reference and examples under `docs/examples/`. | Avoid duplicating long policy in every review skill and avoid active lifecycle directories for examples. | Copy full rules into every review skill or keep examples in active lifecycle directories. |

## Next artifacts

- focused formal review recording spec/reference update
- examples cleanup
- implementation plan
- skill-validator update
- review skill updates
- generated adapter refresh
- optional downstream status-settlement follow-up proposal
- explain-change
- verify

## Follow-on artifacts

- Proposal-review: approved on 2026-05-12 with no material findings.
- Spec amendment: [Formal Review Recording](../../specs/formal-review-recording.md), drafted for review recording output guardrail and examples cleanup.
- Test spec amendment: [Formal Review Recording Test Spec](../../specs/formal-review-recording.test.md), drafted for the same amendment.

## Readiness

Accepted. The focused spec and test-spec amendments now carry the next review gate for this change.

This proposal narrows the first implementation slice to the actual repeated failure: material findings must be durably recorded or explicitly blocked, while moving examples out of active lifecycle directories. It records downstream artifact lifecycle settlement as follow-up direction for the skills that rely on reviewed artifacts.

## Core invariant

```text
Review records evidence.
Examples are not active lifecycle state.
Downstream execution may settle upstream status before reliance.
Artifacts remain the source of truth.
```
