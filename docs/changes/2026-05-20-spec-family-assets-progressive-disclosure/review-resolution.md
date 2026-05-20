# Review Resolution: Spec-Family Assets Progressive Disclosure

## Summary

Closeout status: open

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: plan-review-r1
Review closeout: code-review-m1-r1

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `spec-review-r1`, `plan-review-r1`, `code-review-m1-r1`
- Findings resolved: 5
- Unresolved findings: 1
- Final result: Proposal-review R1 requested changes for proof route, per-skill skeleton boundary, generated-output proof boundaries, stricter review-class asset restrictions, and change-local baseline ownership. The proposal was revised to add those controls before downstream plan reliance. Proposal-review R2 approved the proposal with no material findings. Spec-review R1 approved the spec with no material findings. Plan-review R1 approved the execution plan with no material findings. Code-review M1 R1 requested changes for missing generated-output presence coverage in the validator foundation.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
|---|---|---|---|
| SFA-PR1 | accepted | resolved | Added a proof route requiring a focused test-spec amendment, conditional spec amendment decision, and a plan-named approved route before implementation. |
| SFA-PR2 | accepted | resolved | Added a per-skill skeleton decision for `spec`, `spec-review`, and `test-spec`, with inline fallback if a full skeleton asset hides too much contract surface. |
| SFA-PR3 | accepted | resolved | Added generated-output proof boundaries separating generated mirror proof, temporary adapter archive proof, tracked-tree proof, and explicit stale-debt deferral. |
| SFA-PR4 | accepted | resolved | Added a review-class asset boundary and acceptance criterion limiting `spec-review` assets to structure, labels, placeholders, and short fill hints. |
| SFA-PR5 | accepted | resolved | Added a change-local baseline summary artifact requirement that maps PR #79 structures to planned assets and preserved `SKILL.md` rules. |
| SFA-M1-CR1 | needs-decision | open | Code-review M1 R1 found that generated-output presence coverage is missing from the M1 validator foundation. |

## Resolution Entries

### proposal-review-r1

#### SFA-PR1 - Proof route is too conditional

Finding ID: SFA-PR1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Proof route` requiring a focused test-spec amendment, making a spec amendment conditional on current skill-contract sufficiency, and blocking implementation until the plan names an approved route.
Rationale: The proposal extends a one-skill asset pilot to three spec-family skills, including a review-class skill, so implementation should not proceed on an implicit proof assumption.
Validation target: Proposal contains an explicit proof route and rollout gate.
Validation evidence: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-resolution.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/reviews/proposal-review-r1.md`; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`; `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`; `git diff --check -- docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`.

#### SFA-PR2 - Per-skill skeleton boundary should be a decision, not an open question

Finding ID: SFA-PR2
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Per-skill skeleton decision` specifying full skeleton assets for `spec` and `test-spec`, result/finding assets only for `spec-review`, and an inline fallback if code review finds hidden contract risk.
Rationale: The skeleton boundary affects `SKILL.md`, assets, resource maps, preservation matrices, and review scope.
Validation target: Proposal no longer leaves the skeleton boundary as an open question.
Validation evidence: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-resolution.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/reviews/proposal-review-r1.md`; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`; `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`; `git diff --check -- docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`.

#### SFA-PR3 - Generated adapter proof must distinguish archive proof, mirror proof, and tracked-tree debt

Finding ID: SFA-PR3
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Generated output proof boundary` requiring generated skill mirror proof, temporary generated adapter proof, adapter validation against temporary generated output, no hand-edits, and explicit deferral for known stale tracked-tree debt.
Rationale: Asset work must prove assets reach generated public output without letting unrelated tracked-tree debt either hide missing archive proof or block valid temporary archive proof.
Validation target: Proposal separates required generated mirror and archive proof from conditional tracked-tree checks.
Validation evidence: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-resolution.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/reviews/proposal-review-r1.md`; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`; `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`; `git diff --check -- docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`.

#### SFA-PR4 - `spec-review` assets need a stricter no-hidden-review-guidance rule

Finding ID: SFA-PR4
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Review-class asset boundary` plus a review-class acceptance criterion limiting `spec-review` assets to headings, field labels, placeholders, and short fill hints.
Rationale: `spec-review` assets sit near a known PR #79 failure mode where presentation-only review-dimension text could read as new obligations.
Validation target: Proposal contains an explicit check preventing review judgment or review-policy prose from accumulating in `spec-review` assets.
Validation evidence: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-resolution.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/reviews/proposal-review-r1.md`; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`; `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`; `git diff --check -- docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`.

#### SFA-PR5 - Behavior baseline should be summarized change-locally

Finding ID: SFA-PR5
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Baseline summary artifact` requiring `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/baseline.md` before implementation.
Rationale: PR #79 remains the authoritative baseline, but reviewers need a concise source-to-asset map for this extraction pass.
Validation target: Proposal requires the baseline summary and defines its per-skill content.
Validation evidence: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-resolution.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/reviews/proposal-review-r1.md`; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`; `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`; `git diff --check -- docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`.

### proposal-review-r2

No material findings.

### spec-review-r1

No material findings.

### plan-review-r1

No material findings.

### code-review-m1-r1

#### SFA-M1-CR1 - Generated-output presence coverage is missing from the M1 validator foundation

Finding ID: SFA-M1-CR1
Disposition: needs-decision
Status: open
Decision owner: implementation owner
Decision needed: Accept the finding and add deterministic generated-output presence coverage to M1, or revise the approved plan/test-spec if generated-output presence coverage is intentionally deferred outside M1.
Owning stage: review-resolution
Stop state: M1 remains `resolution-needed`; M2 must not begin until this finding is dispositioned and resolved or the approved artifacts are revised.
Rationale: The finding is actionable, but implementation has not yet recorded an accepted disposition or fix.
Validation target: Review-resolution records a final disposition and, if accepted, validation proves generated-output presence coverage is implemented.
