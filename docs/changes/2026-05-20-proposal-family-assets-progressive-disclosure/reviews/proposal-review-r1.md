# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Contributor proposal-review
Target: docs/proposals/2026-05-20-proposal-family-assets-progressive-disclosure.md
Status: changes-requested

## Review inputs

- Proposal: `docs/proposals/2026-05-20-proposal-family-assets-progressive-disclosure.md`
- User-supplied proposal-review result in chat on 2026-05-20
- Governing boundaries: `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`

## Result

- Material findings: `PFA-PR1`, `PFA-PR2`, `PFA-PR3`, `PFA-PR4`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-log.md`
- Review resolution: `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-resolution.md`
- Open blockers: proof-route finalization, conditional proposal-section preservation, review-class asset validator boundary, durable baseline identity
- Immediate next stage: proposal revision, then test-spec amendment / plan as clarified
- No automatic downstream handoff: this review does not start spec, test-spec, plan, or implementation.

## Findings

### PFA-PR1 - Proof route remains conditional even though open questions are declared closed

Finding ID: PFA-PR1
Severity: major
Location: `Proof route`, `Next artifacts`, `Open questions`
Evidence: The proposal left the focused test-spec amendment conditional while also saying there were no open questions for proposal-review.
Required outcome: Make the proof route explicit before planning.
Safe resolution: Require a focused test-spec amendment before implementation, keep the spec amendment conditional on a documented skill-contract gap, and block implementation until the test-spec amendment is approved.

### PFA-PR2 - Conditional proposal sections are not explicitly preserved when the full skeleton moves to `assets/`

Finding ID: PFA-PR2
Severity: major
Location: `proposal` proposed asset layout, `proposal` resource map, `Behavior preservation boundary`
Evidence: The proposal resource-map entry listed core proposal sections but did not explicitly preserve trigger-based sections such as `Initial intent preservation` and `Scope budget`.
Required outcome: Define how conditional proposal sections are represented after extraction.
Safe resolution: Add a conditional proposal-section boundary, update the `proposal` resource-map entry, and add preservation-matrix rows for conditional sections.

### PFA-PR3 - `proposal-review` needs an explicit review-class asset validator boundary

Finding ID: PFA-PR3
Severity: major
Location: `Review-class asset boundary`, `Testing and verification strategy`, `Acceptance criteria`
Evidence: The proposal forbade hidden review-policy guidance but did not require deterministic allowed structural labels and forbidden policy labels for `proposal-review` assets.
Required outcome: Add deterministic review-class asset checks for `proposal-review`.
Safe resolution: Add a proposal-review asset validation boundary with a structural-label allowlist, forbidden review-policy labels, and positive/negative fixture expectations.

### PFA-PR4 - Baseline identity should be pinned, not described as "current canonical skill state"

Finding ID: PFA-PR4
Severity: major
Location: `Baseline summary artifact`, `Behavior-parity baseline`, `Rollout and rollback`
Evidence: The proposal used "current canonical skill state" as the behavior baseline, which is ambiguous across branches and time.
Required outcome: Pin the baseline to a durable source.
Safe resolution: Require the baseline artifact to record source commit or branch point, canonical source paths, source hashes or section hashes, extracted source ranges or stable headings, and conditional sections governed by `SKILL.md`.

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Clear problem: proposal-family skills carry large inline structures that can be packaged as assets. |
| User value | pass | Better common-path readability for two high-visibility published skills. |
| Option diversity | pass | Options compare do-nothing, full resource rollout, proposal-only, and both-skills assets. |
| Decision rationale | pass | Option 4 is justified: both skills get assets, but review-class assets stay narrow. |
| Scope control | concern | Strong non-goals, but proof route and conditional section handling needed tightening. |
| Architecture awareness | pass | Adapter roots, lockfiles, CLI, generated output, and canonical source boundaries are addressed. |
| Testability | concern | Needed deterministic proposal-review asset validation and pinned baseline evidence. |
| Risk honesty | pass | Names hidden behavior, review guidance creep, missing assets, placeholder leakage, and tiny-asset ceremony. |
| Rollout realism | concern | Milestone split is plausible, but baseline and proof route needed finalization before planning. |
| Readiness for plan | changes-requested | Direction is good; revise four issues before plan approval. |

## Scope-preservation result

Pass.

The proposal preserves the initial request to add assets-only progressive disclosure for `proposal` and `proposal-review`, preserve current behavior, keep rules in `SKILL.md`, validate generated adapter output, and avoid tiny asset formalism.

## Recommended next stage

Revise the proposal to resolve `PFA-PR1`, `PFA-PR2`, `PFA-PR3`, and `PFA-PR4`, then rerun proposal-review before downstream plan reliance.
