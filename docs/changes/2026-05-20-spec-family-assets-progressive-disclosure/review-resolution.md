# Review Resolution: Spec-Family Assets Progressive Disclosure

## Summary

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: plan-review-r1
Review closeout: code-review-m1-r1
Review closeout: code-review-m1-r2
Review closeout: code-review-m2-r1
Review closeout: code-review-m2-r2

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `spec-review-r1`, `plan-review-r1`, `code-review-m1-r1`, `code-review-m1-r2`, `code-review-m2-r1`, `code-review-m2-r2`
- Findings resolved: 7
- Unresolved findings: 0
- Final result: Proposal-review R1 requested changes for proof route, per-skill skeleton boundary, generated-output proof boundaries, stricter review-class asset restrictions, and change-local baseline ownership. The proposal was revised to add those controls before downstream plan reliance. Proposal-review R2 approved the proposal with no material findings. Spec-review R1 approved the spec with no material findings. Plan-review R1 approved the execution plan with no material findings. Code-review M1 R1 requested changes for missing generated-output presence coverage in the validator foundation; the finding was accepted and resolved with a reusable generated-output presence helper plus positive and negative tests. Code-review M1 R2 found no blocking or required-change findings. Code-review M2 R1 requested changes for requirement modal parity in `assets/requirement-row.md`; the finding was accepted and resolved by making the requirement row asset preserve the full requirement statement field while keeping modal guidance in `SKILL.md`. Code-review M2 R2 was blocked because no new M2 fix surface existed at that time.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
|---|---|---|---|
| SFA-PR1 | accepted | resolved | Added a proof route requiring a focused test-spec amendment, conditional spec amendment decision, and a plan-named approved route before implementation. |
| SFA-PR2 | accepted | resolved | Added a per-skill skeleton decision for `spec`, `spec-review`, and `test-spec`, with inline fallback if a full skeleton asset hides too much contract surface. |
| SFA-PR3 | accepted | resolved | Added generated-output proof boundaries separating generated mirror proof, temporary adapter archive proof, tracked-tree proof, and explicit stale-debt deferral. |
| SFA-PR4 | accepted | resolved | Added a review-class asset boundary and acceptance criterion limiting `spec-review` assets to structure, labels, placeholders, and short fill hints. |
| SFA-PR5 | accepted | resolved | Added a change-local baseline summary artifact requirement that maps PR #79 structures to planned assets and preserved `SKILL.md` rules. |
| SFA-M1-CR1 | accepted | resolved | Added deterministic generated-output presence coverage without moving full archive generation out of M5. |
| SFA-M2-CR1 | accepted | resolved | Updated `assets/requirement-row.md` to preserve the full requirement statement field and keep modal guidance in `SKILL.md`. |

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
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement M1 fix
Chosen action: Added `mapped_asset_paths_for_skill` and `validate_generated_asset_presence` to `scripts/skill_validation.py`. The helper compares mapped canonical skill asset paths against a supplied generated output root and reports stable errors naming the skill, missing asset path, and generated surface. Added fixture-backed tests proving complete generated skill mirror output passes, generated skill mirror output missing a mapped asset fails, and adapter-shaped output names the generated adapter output surface when a mapped asset is missing.
Rationale: M1 owns the deterministic validator foundation for generated-output presence, while M5 still owns actual generated mirror proof, temporary adapter archive generation, and adapter validation.
Validation target: Validator tests prove generated-output presence coverage without requiring actual archive generation in M1.
Validation evidence: `python scripts/test-skill-validator.py` passed with 141 tests after adding generated-output presence coverage. `python scripts/validate-skills.py`, `git diff --check -- .`, change metadata validation, explicit-path artifact lifecycle validation, and review artifact closeout validation also passed.

### code-review-m1-r2

No material findings.

### code-review-m2-r1

#### SFA-M2-CR1 - `requirement-row.md` narrows the allowed requirement modal verbs

Finding ID: SFA-M2-CR1
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement M2 fix
Chosen action: Updated `skills/spec/assets/requirement-row.md` from `<requirement ID>. The system MUST <testable behavior>.` to `<requirement ID>. <requirement statement>.` Updated the `skills/spec/SKILL.md` resource-map entry to fill the full requirement statement and use modal guidance from `SKILL.md`. Updated baseline and behavior-preservation evidence to record that the asset preserves requirement ID and full requirement statement fields while `SKILL.md` remains authoritative for `MUST`, `MUST NOT`, and `SHOULD ... because ...`.
Rationale: `SFA-M2-CR1` identified a behavior-preservation defect in the asset extraction. The fix keeps the asset structural and avoids duplicating or narrowing modal guidance.
Validation target: M2 validation proves requirement modal parity is restored in the asset and evidence.
Validation evidence: `python scripts/validate-skills.py skills/spec/SKILL.md`, `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, `git diff --check -- .`, change metadata validation, explicit-path artifact lifecycle validation, and review artifact closeout validation passed after the fix.

### code-review-m2-r2

Blocked. No new implementation surface exists after `code-review-m2-r1`;
`SFA-M2-CR1` remains open and M2 remains in `resolution-needed`.
