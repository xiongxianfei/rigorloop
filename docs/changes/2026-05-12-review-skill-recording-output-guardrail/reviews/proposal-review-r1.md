# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Maintainer proposal-review
Target: docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md
Status: changes-requested

## Review inputs

- Proposal: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`
- Governing policy: `CONSTITUTION.md`
- Related spec: `specs/formal-review-recording.md`
- Related proposal: `docs/proposals/2026-05-07-review-skill-material-finding-recording.md`

## Findings

### RSG1: `recorded` is defined too narrowly for no-material detailed-record triggers

Finding ID: RSG1
Severity: major
Location: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`, Recommended Direction, recording-status definition
Evidence: The proposal defines `recorded` as requiring the review record, review log, and review-resolution artifacts, but the approved formal review recording contract allows no-material detailed-record triggers that require a detailed review record and `review-log.md` without an empty `review-resolution.md`.
Required outcome: Define `recorded` as every artifact required by the active recording trigger, not always `review-resolution.md`.
Safe resolution: Add separate artifact requirements for material findings and no-material detailed-record triggers, and restate that `review-resolution.md` is required only for material findings or another approved review-resolution trigger.

### RSG2: Change-id selection is underspecified

Finding ID: RSG2
Severity: major
Location: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`, Recommended Direction, required recording artifact paths
Evidence: The proposal requires creating or updating `docs/changes/<change-id>/...` artifacts but only says to block when the change ID is unknown. Isolated review requests often lack a preexisting change root, so review skills need deterministic change ID selection before blocking.
Required outcome: Add a simple change ID source rule.
Safe resolution: Choose the change ID from an active change root, active plan or reviewed artifact metadata, user-provided change ID, or generated `YYYY-MM-DD-<reviewed-artifact-or-topic>-review-recording`; block only when still ambiguous.

### RSG3: `Location` should be required but flexible

Finding ID: RSG3
Severity: major
Location: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`, Recommended Direction, complete material-finding shape
Evidence: The proposal requires `Location`, which is correct, but findings may concern a missing artifact, absent evidence, missing handoff, milestone region, or requirement rather than one exact file line.
Required outcome: Define what counts as a valid `Location`.
Safe resolution: Allow file and section, file and line or range, artifact and milestone or requirement ID, missing expected artifact path, or review surface plus "not present" rationale, as long as the location is specific enough for a future reader to find the affected surface without chat history.

### RSG4: The proposal should choose shared wording versus duplicated wording

Finding ID: RSG4
Severity: major
Location: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`, Open Questions, shared wording strategy
Evidence: The proposal leaves open whether the recording-status wording should live in a shared template or be statically checked across five review skills. Leaving this unresolved would make implementation guess.
Required outcome: Decide the first-slice strategy.
Safe resolution: Use the same concise recording-status block across all five formal review skills. If a shared template source is already accepted for skill snippets, place the block there and compare copied skill text against it; otherwise use exact copied wording plus static coverage.

### RSG5: Expected output should distinguish review status from recording status

Finding ID: RSG5
Severity: concern
Location: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`, Recommended Direction and Expected Behavior Changes
Evidence: Review skills have stage-specific review statuses. Without a distinction, agents could treat `recorded` as the review outcome rather than artifact-recording state.
Required outcome: Clarify that `Recording status` is not the review verdict.
Safe resolution: Use a result shape with both `Review status` and `Recording status`, and state that recording status only reports whether required review-recording artifacts were created, not required, or blocked.

### RSG6: Static checks alone may not prevent recurrence

Finding ID: RSG6
Severity: concern
Location: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`, Testing and Verification Strategy
Evidence: The existing `plan-review` skill already contained recording policy, yet an agent still failed to create the record. Static checks prove wording exists but do not verify runtime review output.
Required outcome: Add a later escalation trigger.
Safe resolution: State that if a formal review again reports material findings without `Recording status: recorded` or `Recording status: blocked`, the project should create a follow-up proposal for runtime or output validation.

## Review dimensions

| Dimension | Result | Notes |
|---|---|---|
| Problem framing | pass | The proposal identifies execution flow rather than re-litigating existing policy. |
| Scope | concern | The stage-neutral scope is right, but the recording-status contract needs precision before implementation. |
| Source alignment | concern | The current `recorded` definition could conflict with the no-empty-resolution boundary in the formal review recording spec. |
| Testability | concern | Static checks are appropriate for v1, but the proposal needs clearer wording strategy and escalation criteria. |
| Workflow safety | concern | Change ID selection and flexible `Location` rules are needed to make recording reliable. |

## Recommended next stage

Verdict: changes requested before implementation.

Immediate next repository stage: proposal revision and proposal-review rerun.

Downstream implementation readiness: not ready until the recording-status contract is precise enough for implementation and static validation.
