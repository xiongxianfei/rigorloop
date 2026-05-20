# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Contributor proposal-review
Target: docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md
Status: changes-requested

## Review inputs

- Proposal: `docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md`
- Baseline reference: PR #79, spec-family readability pass
- Prior accepted asset pattern: assets-first pilot for `plan`
- Governing boundaries: `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`

## Result

- Material findings: `SFA-PR1`, `SFA-PR2`, `SFA-PR3`, `SFA-PR4`, `SFA-PR5`
- Recording status: recorded
- Recording blocker: none
- Immediate next stage: proposal revision, then proposal-review rerun
- No automatic downstream handoff: this review does not start spec, test-spec, plan, or implementation.

## Findings

### SFA-PR1 - Proof route is too conditional

Finding ID: SFA-PR1
Severity: major
Evidence: The proposal says to amend `specs/skill-contract.md` only if existing asset rules are insufficient, and to add a test-spec amendment for spec-family asset checks.
Required outcome: Name the approved proof route before implementation.
Safe resolution: Add a `Proof route` section requiring a focused test-spec amendment, making a spec amendment conditional on skill-contract sufficiency, and blocking implementation until the plan names the approved route.

### SFA-PR2 - Per-skill skeleton boundary should be a decision, not an open question

Finding ID: SFA-PR2
Severity: major
Evidence: The proposal asks whether each skill should get a full skeleton asset or only repeated substructure assets while also proposing full skeleton assets for `spec` and `test-spec`, and result/finding assets for `spec-review`.
Required outcome: Record the per-skill skeleton decision explicitly.
Safe resolution: Add a `Per-skill skeleton decision` section: full skeleton asset plus substructure assets for `spec`; result and material-finding assets only for `spec-review`; full skeleton asset plus test-case and coverage-map substructure assets for `test-spec`. Keep the inline fallback if code review finds that a full skeleton asset hides too much contract surface.

### SFA-PR3 - Generated adapter proof must distinguish archive proof, mirror proof, and tracked-tree debt

Finding ID: SFA-PR3
Severity: major
Evidence: The proposal requires generated skill mirrors and generated adapter archives to include all assets. It does not state how to treat known stale tracked expanded adapter layout debt.
Required outcome: Define exact adapter proof requirements and deferral handling.
Safe resolution: Add a `Generated output proof boundary` requiring generated skill mirror proof, temporary generated adapter output proof, adapter validation against temporary generated output, and no hand-edits. Require tracked-tree checks when supported, with explicit deferral for known stale tracked-tree debt.

### SFA-PR4 - `spec-review` assets need a stricter no-hidden-review-guidance rule

Finding ID: SFA-PR4
Severity: major
Evidence: The proposal says `spec-review` assets must not contain review-dimension explanations, severity policy, review judgment, observability/security guidance, or material-finding rules beyond field labels and placeholders, but lacks a review-class-specific check.
Required outcome: Add a review-class asset-specific acceptance criterion.
Safe resolution: Add a `Review-class asset boundary` limiting `spec-review` assets to headings, field labels, placeholders, and short fill hints. Explicitly forbid review-dimension definitions, severity policy, material-finding sufficiency rules, safe-resolution decision rules, recording-status rules, and security/privacy or observability examples.

### SFA-PR5 - Behavior baseline should be summarized change-locally

Finding ID: SFA-PR5
Severity: major
Evidence: The proposal says to use PR #79 as the baseline and lists what must be preserved for `spec`, `spec-review`, and `test-spec`.
Required outcome: Add a baseline summary artifact requirement.
Safe resolution: Require `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/baseline.md` before implementation, mapping PR #79 skill structures to planned assets and identifying which rules, enums, stops, dimensions, coverage obligations, and source locations remain in `SKILL.md`.

## Review dimensions

| Dimension | Result | Notes |
|---|---|---|
| Problem clarity | pass | The proposal clearly follows PR #79 and targets asset extraction only. |
| User value | pass | It reduces common-path skill bodies and proves asset packaging across the family. |
| Option diversity | pass | The proposal compares do-nothing, full resources, constructive-only assets, and all-three with review-skill constraints. |
| Decision rationale | pass | Option 4 follows from family consistency and PR #79 baseline stability. |
| Scope control | concern | Proof route and skeleton decision should be explicit before planning. |
| Architecture awareness | concern | Generated-output proof needs tracked-tree/archive distinction. |
| Testability | concern | Needs stricter review-class asset checks and a baseline summary. |
| Risk honesty | pass | Names hidden behavior, review guidance creep, adapter misses, placeholders, and PR #79 regression. |
| Rollout realism | concern | Milestone split is plausible; proof-route and adapter-validation rules should be tightened. |
| Readiness for plan | changes-requested | Direction is good; revise five areas before planning. |

## Recommended next stage

Revise the proposal to resolve `SFA-PR1`, `SFA-PR2`, `SFA-PR3`, `SFA-PR4`, and `SFA-PR5`, then rerun proposal-review before downstream plan reliance.
