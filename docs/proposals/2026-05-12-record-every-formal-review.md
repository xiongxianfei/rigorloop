# Record Every Formal Review

## Status

- accepted

## Problem

Formal review evidence is currently split between detailed durable records for material findings and lightweight handling for clean reviews. That keeps clean reviews cheap, but it can leave a formal review without a dedicated review evidence file. Later work then has to infer whether a formal review happened, what scope was checked, and whether the result was clean.

The workflow needs one simple rule: every formal review leaves a durable review file, while clean reviews remain intentionally lightweight.

## Goals

- Record every formal lifecycle review invocation in a durable review file.
- Keep reviews with no material findings lightweight and low-friction.
- Preserve detailed finding and resolution handling for material findings and blocking outcomes.
- Make formal review output unambiguous: the review evidence was recorded or recording was blocked.
- Keep public review skills concise by centralizing reusable details, templates, and examples.
- Keep review evidence separate from downstream lifecycle/status settlement.

## Non-goals

- Redesign the full workflow stage model.
- Add or rename review stages.
- Add a dedicated PR-review stage.
- Require empty resolution files for clean reviews with no findings.
- Move downstream lifecycle/status settlement into review skills.
- Define implementation milestones in this proposal.
- Backfill durable review files for old clean reviews unless a later change explicitly needs them.

## Vision fit

fits the current vision

This proposal strengthens RigorLoop's Git-first reviewability by ensuring reviewers can reconstruct formal review scope and outcome from tracked artifacts without relying on chat history.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Record all reviews, including reviews with no findings | in scope | Goals, Recommended direction, Expected behavior changes |
| Keep no-finding reviews lightweight | in scope | Goals, Recommended direction, Risks and mitigations |
| Keep skill wording simple and concise | in scope | Goals, Recommended direction, Architecture impact |
| Avoid expanding review skills into downstream status settlement | in scope | Non-goals, Recommended direction, Architecture impact |

## Context

`VISION.md` says RigorLoop should make a representative change's purpose, requirements, design constraints, tests, validation evidence, and review concerns reconstructable from tracked artifacts without chat history. Clean formal reviews that leave no durable review file weaken that promise.

The current formal-review-recording spec already requires durable recording for material findings and complete material-finding shape, including a stable location, evidence, required outcome, and safe resolution path. It also distinguishes recording from handoff isolation.

The existing clean-review policy favors lightweight treatment when no detailed-record trigger applies. The proposed change keeps the lightweight goal but moves from artifact-local-only clean handling to a durable review-receipt model for every formal lifecycle review.

The current handoff direction for review recording is to keep the change recording-only, retain recording status and blocked-recording behavior, preserve complete material-finding shape, avoid artifact-status synchronization fields in review skills, and centralize long reusable rules outside individual skills.

This proposal amends the accepted formal-review-recording direction. It does not replace the existing material-finding and review-resolution model.

## Relationship to existing clean-review settlement

This proposal intentionally amends the current material-triggered clean-review settlement model.

Before this change, clean formal reviews with no material findings could settle artifact-locally when no detailed-record trigger applied.

After this change, every formal lifecycle review creates a lightweight review receipt. Clean receipts do not require `review-resolution.md`.

Artifact-local lifecycle/status settlement remains required when the reviewed artifact status changes. The review receipt proves the review happened; it does not replace artifact status settlement.

## Options considered

### Option 1: Keep the current material-triggered model

Clean reviews continue to avoid dedicated review files unless another detailed-record trigger applies.

This minimizes file creation, but it keeps an ambiguity gap for formal reviews that completed cleanly. It also makes review evidence less uniform across stages.

### Option 2: Require full detailed review records for every review

Every formal review would use the same detailed record, log, and resolution structure regardless of outcome.

This maximizes uniformity, but it creates unnecessary boilerplate for clean reviews and increases the token/runtime cost of routine review work.

### Option 3: Require a lightweight review receipt for every formal review

Every formal review creates a durable review file. Clean reviews use a short receipt. Reviews with material findings or blocking outcomes expand into detailed records and disposition tracking.

This is the recommended option because it provides consistent durable evidence without turning clean reviews into heavy process artifacts.

### Option 4: Store clean review evidence only in the reviewed artifact

A reviewed artifact would record that review passed, with no dedicated review file for clean outcomes.

This remains useful as artifact-local lifecycle history, but it is weaker as a uniform review-evidence model because review scope, round, reviewer, and record status are not consistently discoverable.

## Recommended direction

Adopt a two-tier review evidence model.

This rule applies when a supported formal lifecycle review skill is invoked to produce a lifecycle review result for a tracked artifact:

- `proposal-review`
- `spec-review`
- `architecture-review`
- `plan-review`
- `code-review`

The rule does not apply to casual critique, exploratory comments, informal readiness discussion, or review-like chat that does not return a formal review status.

When the user asks for a formal review skill result, the review is formal even if the request is isolated or review-only.

Every formal lifecycle review creates or updates a durable review file under the selected change-local review path, for example:

```text
docs/changes/<change-id>/reviews/<stage>-r<n>.md
```

For a clean review with no material findings, the file is a lightweight review receipt. It records only the essentials:

```md
# <Stage> Review r<n>

## Review metadata

- Review stage: <stage>
- Review round: r<n>
- Reviewed artifact: <path>
- Review date: <YYYY-MM-DD>
- Reviewer: <agent or role>
- Recording status: recorded

## Outcome

- Review status: approved | accepted | clean | equivalent stage outcome
- Material findings: none
- Blocking findings: none

## Scope checked

- <short reviewed-scope bullets>

## Notes

- Clean formal review completed with no material findings.
```

For a review with material findings or a blocking stage-owned outcome, the review file includes the complete detailed finding shape:

```md
## Findings

### F1: <finding title>

- Severity: material | block
- Location: <path and precise section/line/context>
- Evidence: <bounded evidence>
- Required outcome: <required change or decision>
- Safe resolution path: <fix path>
```

The `review-log.md` file indexes every formal review receipt, including clean receipts. The `review-resolution.md` file is required only when findings or blocking outcomes require disposition. Clean reviews do not create empty resolution files.

Formal review outputs report review recording as `recorded` or `blocked` for formal lifecycle reviews. The existing `not-required` value is reserved for non-formal review-like requests outside this proposal's scope.

A clean review receipt proves the review happened. It does not by itself settle the reviewed artifact's lifecycle status. When a clean review changes the reviewed artifact's lifecycle state, artifact-local status settlement or downstream status settlement still updates the artifact or reports a blocker.

When a formal review receipt is required, choose the change ID in this order:

1. existing active `docs/changes/<change-id>/change.yaml`;
2. active plan or reviewed artifact metadata naming a change ID;
3. user-provided change ID;
4. generated receipt change ID:

   ```text
   YYYY-MM-DD-<reviewed-artifact-or-topic>-review-recording
   ```

If the change ID remains ambiguous, the review output reports `Recording status: blocked` and names the smallest action needed to record the review.

Every formal review receipt is indexed in `review-log.md` with a minimal entry containing:

- review ID;
- stage;
- round;
- reviewed artifact;
- review record path;
- review status;
- material findings count;
- recording status.

Clean receipts use `material findings count: 0`.

Example:

```md
| Review ID | Stage | Round | Reviewed artifact | Record | Status | Material findings | Recording |
|---|---|---:|---|---|---|---:|---|
| spec-review-r1 | spec-review | 1 | `specs/example.md` | `reviews/spec-review-r1.md` | approved | 0 | recorded |
```

Clean receipts should remain short. The target is under 300 words unless the reviewer records a reason. Clean receipts do not include full detailed checklist prose unless a detailed-record trigger applies.

The full change-ID selection rule, minimal required receipt shape, detailed finding shape, `review-log.md` indexing rule, and blocked-recording behavior should live in `specs/formal-review-recording.md`. Filled examples should live under `docs/examples/formal-review-recording/`.

Use a strict role split:

```text
specs/formal-review-recording.md = normative shared receipt contract
docs/examples/formal-review-recording/ = non-normative filled examples
```

Individual public review skills should state the obligation briefly and point to the central rule rather than duplicating long algorithms or full receipt templates.

## Expected behavior changes

- A clean formal review now creates a lightweight durable review receipt instead of relying only on local artifact text.
- A clean formal review is indexed in `review-log.md`.
- A clean formal review does not create an empty `review-resolution.md`.
- A clean formal review receipt does not replace artifact-local lifecycle/status settlement.
- A material-finding review still records complete finding details and requires disposition tracking.
- A formal review that cannot create or update required review evidence reports recording as blocked and names the smallest action needed.
- Review skills become simpler: record every formal review, use a lightweight receipt when clean, use detailed finding records when needed.

## Architecture impact

This change affects the review-recording contract and the public review skills that invoke it.

Expected touched areas:

- `specs/formal-review-recording.md` for the normative rule and reusable templates.
- Formal lifecycle review skills such as `proposal-review`, `spec-review`, `plan-review`, `architecture-review`, and `code-review`.
- Any future `test-spec-review` skill if it is added to the formal lifecycle review model by a separate approved change.
- Review artifact validation, especially checks for review receipt fields and `review-log.md` indexing.
- Generated adapter outputs after canonical skill edits.
- Optional examples under `docs/examples/formal-review-recording/` to keep skill files concise.

The boundary remains narrow: review skills record review evidence and findings; downstream lifecycle/status settlement stays outside this proposal.

## Testing and verification strategy

Verification should cover both policy text and generated outputs.

Likely checks:

- Static validation that formal review skills no longer describe clean formal reviews as having no durable review file.
- Static validation that formal review outputs use `recorded` or `blocked` for formal lifecycle reviews.
- Validation that the formal review recording spec defines the minimal clean receipt contract.
- Fixture validation for a clean review receipt with no material findings.
- Fixture validation for a material-finding review record with complete finding shape.
- Fixture or example validation that filled examples stay under `docs/examples/formal-review-recording/` and are not treated as normative authority.
- Validation that `review-log.md` can index clean receipts and detailed records.
- Validation that clean receipts do not require empty `review-resolution.md` files.
- Validation that clean receipts do not satisfy artifact-local lifecycle/status settlement by themselves.
- Validation that clean receipt fixtures stay concise and avoid detailed checklist prose.
- Adapter build/check validation after canonical skill updates.

## Rollout and rollback

Rollout should be incremental:

1. Update the central formal review recording spec.
2. Add or update review artifact validation fixtures for clean receipts and log indexing.
3. Update `plan-review` and `spec-review` first, because recent review evidence gaps surfaced there.
4. Update `proposal-review`, `architecture-review`, and `code-review`.
5. Regenerate adapter outputs.
6. Apply the new rule prospectively to new formal reviews.

No broad backfill is required for old clean reviews unless an active change needs durable evidence for continued work.

Rollback is straightforward: revert the spec and skill wording to the prior material-triggered model. Review receipts created during rollout remain harmless historical evidence and do not require removal.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Clean reviews become boilerplate-heavy | Use a short receipt template with only essential fields. |
| Review directories become noisy | Keep `review-log.md` as the discoverability surface and make receipt names predictable. |
| Skills become longer | Move reusable algorithms and examples into the central spec and example docs. |
| Casual review-like feedback is over-recorded | Scope the rule to formal lifecycle review skill invocations. |
| Receipts are mistaken for lifecycle settlement | State that receipts prove review occurrence only; artifact-local or downstream status settlement remains required. |
| Clean isolated reviews lack a change ID | Use the deterministic change-ID selection rule and report blocked recording when ambiguity remains. |
| Validation becomes too strict too early | Start with minimal required fields and add stricter checks only after fixtures stabilize. |
| Existing `not-required` status semantics conflict with the new rule | Reserve `not-required` for non-formal review-like requests only. |

## Open questions

None.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-05-12 | Draft proposal to record every formal review with lightweight clean receipts | Maintainer direction favors durable evidence for all formal reviews while preserving low-friction clean reviews | Material-triggered-only records; full detailed records for every review; artifact-local-only clean evidence |
| 2026-05-12 | Treat this as an amendment to the accepted formal-review-recording contract | The current approved spec allows clean required reviews to remain artifact-local, so this proposal must change that contract explicitly | Silent implementation drift from the existing spec |
| 2026-05-12 | Reserve `not-required` for non-formal review-like requests | Every formal lifecycle review must either record a receipt or report blocked recording | Keeping `not-required` as a formal review status |
| 2026-05-12 | Scope first implementation to `plan-review` and `spec-review` after central spec and fixtures | Recent evidence gaps surfaced in those stages and they exercise both planning and contract review behavior | Updating all review skills before validator fixtures exist |
| 2026-05-12 | Put the minimal clean receipt contract in `specs/formal-review-recording.md` and filled examples under `docs/examples/formal-review-recording/` | Validators, test specs, and skills need one normative rule while examples should remain illustrative | Spec-only long examples; examples-only receipt contract; duplicating full templates in each review skill |
| 2026-05-12 | Accepted proposal for spec drafting | Maintainer approved the proposal and requested spec creation | Keeping proposal in draft after downstream reliance |

## Next artifacts

- Proposal-review of this proposal.
- Spec update to `specs/formal-review-recording.md`.
- Filled examples under `docs/examples/formal-review-recording/`.
- Skill updates for formal lifecycle review skills.
- Review artifact validation fixtures and checks.
- Generated adapter refresh after canonical skill edits.

## Follow-on artifacts

- Spec update: [Formal Review Recording](../../specs/formal-review-recording.md)

## Readiness

Accepted for spec drafting.
