# Proposal Review R2

Review ID: proposal-review-r2
Stage: proposal-review
Round: 2
Reviewer: Maintainer proposal-review
Target: docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md
Status: changes-requested

## Review inputs

- Proposal: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`
- Learn session: `docs/learn/sessions/2026-05-12-review-approval-status-sync.md`
- Governing policy: `CONSTITUTION.md`
- Related workflow guidance: `docs/workflows.md`

## Findings

### RSG-F2: Artifact-status sync is new normative behavior and should not be skill-only

Finding ID: RSG-F2
Severity: major
Location: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`, Next Artifacts
Evidence: The proposal adds a cross-review-skill requirement that clean or approving formal review results synchronize the reviewed artifact to its next artifact-specific lifecycle status or report `Status sync: blocked`, but `Next Artifacts` makes a spec amendment conditional.
Required outcome: Make the status-sync rule normative in the appropriate workflow/review contract, not only in the five skills.
Safe resolution: Change `Next Artifacts` to require a focused spec amendment for formal review output recording and artifact-status sync.

### RSG-F3: Status sync needs an explicit edit-permission rule for isolated/review-only requests

Finding ID: RSG-F3
Severity: major
Location: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`, Recommended Direction and Non-goals
Evidence: The proposal says direct and review-only requests do not continue downstream automatically, while also requiring clean approving reviews to update the reviewed artifact's owned status surface when clear. Status sync is not downstream continuation, but it is still an artifact edit.
Required outcome: Define when review skills may update status surfaces and when they must report `Status sync: blocked`.
Safe resolution: State that review skills update status surfaces during workflow-managed reviews and isolated reviews unless the user explicitly forbids edits; explicit no-edit instructions require `Status sync: blocked` with the manual action needed.

### RSG-F4: Artifact-specific status table needs tighter status values

Finding ID: RSG-F4
Severity: major
Location: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`, artifact-specific next-state table
Evidence: The proposal table allows architecture or ADR status to `approved`, `accepted`, or `active` according to vocabulary and describes plan/code-review updates broadly. Implementers need testable allowed next states or clear block behavior.
Required outcome: Make the status sync table testable.
Safe resolution: Replace the broad table with stricter mappings for proposal, spec, architecture package, ADR, plan, and code-review. Add a rule to use `Status sync: blocked` if the next status cannot be chosen from the table or an artifact-local lifecycle field.

### RSG-F5: `blocked` semantics should distinguish recording blocked from status-sync blocked

Finding ID: RSG-F5
Severity: major
Location: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`, result shape
Evidence: The proposal introduces `Recording status` and `Status sync`, both with `blocked`, while final output has only generic `Open blockers`.
Required outcome: Define separate blocker fields.
Safe resolution: Add `Recording blocker` and `Status sync blocker` result fields. Require `Recording blocker` when `Recording status: blocked` and `Status sync blocker` when `Status sync: blocked`.

### RSG-F6: First implementation may be too broad

Finding ID: RSG-F6
Severity: concern
Location: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`, Rollout
Evidence: The rollout includes all five formal review skills, static validator checks, possible lifecycle validation, generated skill mirrors, adapters, and possible shared templates or governance/docs updates.
Required outcome: Keep the implementation reviewable.
Safe resolution: Split the execution plan into two milestones: M1 recording-status guardrail across formal review skills, and M2 artifact-status sync guardrail for clean or approving outcomes.

## Review dimensions

| Dimension | Result | Notes |
|---|---|---|
| Problem clarity | pass | The added status-sync problem is real and connected to the learn session. |
| Scope control | concern | The status-sync addition needs a normative spec owner and milestone split. |
| Architecture awareness | concern | The proposal names lifecycle surfaces but needs tighter status ownership and edit-permission rules. |
| Testability | concern | The status table and blocker fields need to be more testable. |
| Readiness for spec | concern | Ready after the findings above are resolved in the proposal. |

## Recommended next stage

Verdict: changes requested before implementation.

Immediate next repository stage: proposal revision and proposal-review rerun.

Downstream implementation readiness: blocked until the revised proposal requires the spec amendment and tightens status-sync behavior.
