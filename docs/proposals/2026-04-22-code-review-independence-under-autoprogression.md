# Code Review Independence Under Autoprogression

## Status

- accepted

## Problem

When `code-review` is triggered automatically after `implement`, it can behave like implementation self-approval.

The risk is not that every review must produce many comments. The risk is that the workflow may accept an unsupported clean result.

A credible review outcome must be grounded in the actual diff, upstream artifacts, checklist coverage, and validation evidence.

This proposal improves review credibility by requiring independent-review mode, evidence-backed clean results, and explicit `inconclusive` status when the reviewer cannot inspect enough evidence.

## Goals

- Preserve automatic `implement -> code-review` handoff for normal full-feature flow.
- Restore trust that `code-review` is an independent gate rather than a continuation of implementation.
- Make zero-finding reviews credible by requiring clearer review scope and evidence.
- Keep actionable review findings visible before any automatic fix loop begins.
- Preserve the existing `review-resolution` loop for straightforward fixes.

## Non-goals

- Reverting workflow autoprogression broadly.
- Removing `code-review`, `review-resolution`, or `verify`.
- Requiring a human reviewer for every non-trivial change.
- Replacing review with lint, tests, or verification alone.
- Designing a full orchestration subsystem or model-specific reviewer runtime in this same change.
- Treating every clean review result as suspicious by default.

## Context

- `specs/workflow-stage-autoprogression.md` intentionally keeps `code-review` as a real gate and says autoprogression must not weaken it.
- `skills/code-review/SKILL.md` already says the reviewer should work with fresh eyes and prefer a fresh session or intentional assumption reset.
- Current guidance does not yet make that independence operational enough when `code-review` starts immediately after `implement` in the same workflow-managed completion flow.
- The settled direction for this slice is narrower than hard session isolation:
  - independent-review mode is required;
  - fresh session, separate reviewer, or separate agent is recommended when available;
  - hard fresh-session enforcement is out of scope.
- The problem surfaced through direct user feedback: once auto-triggered, reviews now often appear much cleaner than before, which reduces confidence in the gate if the result is not backed by visible evidence.
- The repository already has a `review-resolution` loop for fixable findings. What is missing is a stronger boundary around the first independent review pass, not another downstream stage.

## Options considered

### Option 1: Return to manual user-triggered `code-review`

- Advantages:
  - restores a visible pause between implementation and review
  - may reduce perceived continuity between authoring and review
- Disadvantages:
  - reintroduces the routing friction that autoprogression was meant to remove
  - does not guarantee a more independent review by itself
  - makes the user manually trigger a stage the workflow already knows is required

### Option 2: Keep the current autoprogression model and accept cleaner reviews as normal

- Advantages:
  - no workflow changes
  - lowest short-term cost
- Disadvantages:
  - leaves the trust problem unresolved
  - makes it hard to distinguish genuinely strong implementation from review contamination
  - risks turning `code-review` into a nominal gate

### Option 3: Keep autoprogression, but require an explicit independent first-pass review protocol

- Advantages:
  - preserves workflow momentum
  - addresses the actual issue, which is review independence rather than stage order
  - keeps review findings and zero-finding verdicts legible and auditable
  - fits the current workflow model and `review-resolution` loop
- Disadvantages:
  - adds discipline and wording requirements to the review stage
  - may slightly increase review latency for some changes

### Option 4: Add mandatory second-pass or human review for all non-trivial changes

- Advantages:
  - strongest independence guarantee
  - easiest to explain conceptually
- Disadvantages:
  - too heavy for ordinary repository flow
  - increases cost and cycle time for every change
  - solves a subset of the problem by forcing more reviewers rather than improving the normal gate

## Recommended direction

Choose Option 3.

The repository should keep `implement -> code-review` autoprogression, but require independent-review mode for the first `code-review` pass and require a first-pass review record before any review-driven fixes begin.

The core best practices are:

- Separate implementation context from review context.
  - independent-review mode is required for autoprogressed `code-review`;
  - `code-review` should start from the actual diff, upstream artifacts, checklist coverage, and validation evidence, not from remembered implementation reasoning alone;
  - a fresh session, separate reviewer, or separate agent is recommended when available, but this slice does not require hard session-boundary enforcement.
- Make the first review pass record findings before making fixes.
  - `code-review` MUST produce a first-pass review record before any review fixes are applied;
  - the first-pass review record includes review status, review inputs, diff summary, findings, checklist coverage, no-finding rationale when there are no findings, and the recommended next stage.
- Preserve the existing automatic fix loop where it already fits.
  - in a workflow-managed run, fixable findings should automatically enter `review-resolution` when no stop condition applies;
  - this is not a new user decision gate;
  - surfacing findings first means the findings are visible before fixes begin, not that the workflow pauses for approval.
- Make zero-finding reviews explain what was checked.
  - a clean review is valid only when it includes checklist coverage and no-finding rationale;
  - "approve, no findings" without scope or evidence is too weak when the review immediately follows implementation;
  - if the reviewer cannot inspect the required evidence, the result should be `inconclusive`, not a clean pass.
- Use the repository's existing sensitive change classes when stronger review coverage is needed.
  - changes affecting security-sensitive behavior, workflow order or stage policy, CI behavior, schemas, architecture boundaries, or compatibility-sensitive contributor expectations should receive stricter explicit coverage instead of a bare clean result.
- Preserve the current stop condition for real decisions.
  - If review reveals a design, scope, or spec question, the workflow should stop and surface that decision instead of silently fixing forward.

This direction treats the real problem as review contamination, not autoprogression itself. The repository should optimize for:

- automatic routing between stages; and
- independent judgment inside review stages.

Those are compatible if the review contract is explicit enough.

Status behavior for the first-pass review record should be:

| Code-review result | Workflow-managed behavior |
| --- | --- |
| `clean-with-notes` | continue to `verify` |
| `changes-requested` | continue to `review-resolution` |
| `blocked` | stop and report the blocker |
| `inconclusive` | stop and report missing evidence |
| review-only or isolated request | stop after review findings |

Issues that are clearly fixable under current approved scope belong in `changes-requested`, not `blocked`.

## Expected behavior changes

- Automatic `implement -> code-review` handoff remains in place for workflow-managed full-feature execution.
- The first `code-review` pass becomes explicitly independent in posture and must produce a first-pass review record before fixes begin.
- Review findings are surfaced before the workflow enters `review-resolution`, but workflow-managed runs still continue automatically when the findings are fixable and no stop condition applies.
- Zero-finding reviews include clearer evidence about what was reviewed and why the gate passed.
- `inconclusive` becomes an explicit outcome when the reviewer cannot inspect enough evidence to produce a credible result.
- Changes in the repository's existing sensitive change classes receive more explicit review coverage instead of the same lightweight closeout used for small safe diffs.

## Architecture impact

This is primarily a workflow-contract and skill-guidance change, not a runtime architecture change.

Likely touched surfaces:

- `specs/workflow-stage-autoprogression.md` or a focused follow-up spec if the repository wants the review-independence rules isolated
- `docs/workflows.md`
- `skills/code-review/SKILL.md`
- possibly `skills/workflow/SKILL.md`, `skills/implement/SKILL.md`, and any review-resolution guidance that currently blurs the first-pass review boundary
- regenerated `.codex/skills/` output if canonical `skills/` change

No new storage, service boundary, repository automation subsystem, or hard session-enforcement mechanism should be necessary for the first slice.

## Testing and verification strategy

- Write a focused spec that defines the independent first-pass review expectations and the boundary between `code-review` and `review-resolution`.
- Add a matching test spec that covers:
  - auto-handoff into `code-review` still occurring;
  - first-pass findings being reported before fixes;
  - zero-finding reviews requiring explicit scope/evidence language;
  - `inconclusive` when required evidence is missing;
  - sensitive change classes requiring stronger review coverage;
  - design-choice findings stopping instead of auto-fixing forward.
- Use document and skill review to confirm the canonical workflow, `code-review`, and related stage skills say the same thing.
- Run the repository's artifact lifecycle validation on the touched proposal/spec/test-spec surfaces once follow-on artifacts exist.

## Rollout and rollback

Rollout:

- settle the direction in proposal review;
- write a narrow follow-up spec for review independence under autoprogression;
- update the affected workflow and skill surfaces;
- regenerate `.codex/skills/`;
- validate the changed artifact set with repo-owned checks.

Rollback:

- revert the review-independence wording if it proves unworkable;
- keep the broader autoprogression contract unless the repository later decides the routing change itself was the real problem.

## Risks and mitigations

- Risk: the repository adds ceremony but still does not improve review quality.
  - Mitigation: make the first-pass behavior concrete enough to observe in outputs, especially for zero-finding reviews.
- Risk: reviewers treat "fresh eyes" as aspirational wording rather than an operational rule.
  - Mitigation: define explicit first-pass expectations and output shape in the governing spec and skill text.
- Risk: latency increases enough that contributors work around review.
  - Mitigation: keep the change focused on the first-pass boundary instead of adding universal second-review requirements.
- Risk: users interpret this proposal as distrust of every clean review.
  - Mitigation: state clearly that clean reviews remain valid when the review scope and evidence are credible.
- Risk: the change broadens into model-specific orchestration assumptions.
  - Mitigation: define the contract in workflow terms such as independent-review mode, evidence-backed clean results, first-pass review record, and explicit findings, not in terms of any one tool implementation.

## Open questions

- None.

## Decision log

- 2026-04-22: Rejected reverting to manual `code-review` invocation as the preferred direction. Reason: the main issue is review independence, not stage routing.
- 2026-04-22: Rejected leaving the current behavior unchanged. Reason: user trust in the review gate has already been weakened.
- 2026-04-22: Chose explicit first-pass review independence under autoprogression as the leading direction. Reason: it preserves workflow momentum while restoring the credibility of the review gate.
- 2026-04-22: Rejected mandatory second-pass or human review for every non-trivial change as the default. Reason: it is heavier than needed for the repository's normal path.
- 2026-04-22: Settled that independent-review mode is required, but hard fresh-session enforcement is out of scope. Reason: the credibility problem is review grounding and observable first-pass evidence, not mandatory session isolation.
- 2026-04-22: Settled that first-pass review findings are surfaced before fixes, but workflow-managed fixable findings still auto-enter `review-resolution` when no stop condition applies. Reason: the repository needs visible review evidence without reintroducing a new user confirmation gate.
- 2026-04-22: Settled that clean reviews do not require positive notes. Reason: checklist coverage plus no-finding rationale is required for a valid clean review, while positive notes remain optional and should be used only when they provide specific evidence-backed value.

## Next artifacts

- focused spec for code-review independence under autoprogression
- matching test spec
- plan if no separate architecture artifact becomes necessary
- architecture only if the follow-up broadens beyond workflow and skill guidance

## Follow-on artifacts

- `specs/code-review-independence-under-autoprogression.md`
- `specs/code-review-independence-under-autoprogression.test.md`
- `docs/plans/2026-04-22-code-review-independence-under-autoprogression.md`

## Readiness

- This proposal is accepted.
- The focused follow-on spec, active test spec, and active plan now exist.
- No further `proposal-review` action is pending.
