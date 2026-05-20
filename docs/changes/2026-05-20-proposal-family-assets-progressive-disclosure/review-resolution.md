# Proposal-Family Assets Progressive Disclosure Review Resolution

## Summary

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: plan-review-r1
Review closeout: code-review-m1-r1
Review closeout: code-review-m1-r2
Review closeout: code-review-m2-r1
Review closeout: code-review-m3-r1
Review closeout: code-review-m3-r2

## Resolution Entries

### proposal-review-r1

## Findings

#### PFA-PR1

Finding ID: PFA-PR1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Revised `Proof route` to require a focused test-spec amendment before implementation, keep a spec amendment conditional on a documented skill-contract gap, and block implementation until the test-spec amendment is approved.
Rationale: The proposal introduces proposal-family-specific asset checks and review-class restrictions, so downstream planning needs a single proof route.
Validation target: Proposal contains an explicit proof route and implementation gate.
Validation evidence: Proposal section `Proof route`.

#### PFA-PR2

Finding ID: PFA-PR2
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Conditional proposal-section boundary`, updated the `proposal` resource-map entry, added preservation-matrix rows for `Initial intent preservation` and `Scope budget`, and added acceptance criteria for trigger-based conditional sections.
Rationale: Moving the proposal skeleton to an asset must not make conditional sections disappear or become mandatory for every proposal.
Validation target: Proposal preserves trigger-based conditional section behavior after skeleton extraction.
Validation evidence: Proposal sections `Conditional proposal-section boundary`, `proposal resource map`, `Behavior preservation boundary`, and `Acceptance criteria`.

#### PFA-PR3

Finding ID: PFA-PR3
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Proposal-review asset validation boundary`, explicit allowed structural labels, forbidden review-policy labels, fixture expectations, and acceptance criteria for deterministic `proposal-review` asset validation.
Rationale: `proposal-review` assets may contain structural fields, but review policy and judgment must remain in `SKILL.md`.
Validation target: Proposal requires deterministic allowlist and forbidden-label checks for `proposal-review` assets.
Validation evidence: Proposal sections `Proposal-review asset validation boundary`, `Testing and verification strategy`, and `Acceptance criteria`.

#### PFA-PR4

Finding ID: PFA-PR4
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Revised `Baseline summary artifact` and `Behavior-parity baseline` to require a pinned source commit or branch point, canonical source paths, source hashes or section hashes, extracted source ranges or stable headings, and conditional section ownership.
Rationale: Behavior preservation evidence must be reviewable against a durable baseline, not a time-dependent current branch state.
Validation target: Proposal defines a pinned baseline identity and uses that baseline for behavior parity.
Validation evidence: Proposal sections `Baseline summary artifact`, `Behavior-parity baseline`, `Acceptance criteria`, and `Decision log`.

## Validation

- Proposal revised to resolve all material findings from `proposal-review-r1`.
- Review log records no open findings for `proposal-review-r1`.
- Downstream planning still requires a proposal-review rerun before reliance.

### proposal-review-r2

No material findings.

### spec-review-r1

No material findings.

### plan-review-r1

No material findings.

### code-review-m1-r1

## Findings

#### PFA-M1-CR1

Finding ID: PFA-M1-CR1
Disposition: accepted
Status: resolved
Owner: implementation agent
Owning stage: implement M1
Chosen action: Updated proposal-review asset validation so field-label-shaped lines must use labels from `PROPOSAL_REVIEW_ASSET_ALLOWED_FIELD_LABELS`. Non-allowlisted structural labels now fail independently of the forbidden-policy regex.
Rationale: The approved spec requires explicit structural-label allowlist enforcement for proposal-review assets, not only forbidden-policy phrase detection.
Validation target: `proposal-review` asset validation rejects field labels that are not in `PROPOSAL_REVIEW_ASSET_ALLOWED_FIELD_LABELS` and keeps approved labels passing.
Validation evidence: Full M1 review-resolution validation passed after the closed-allowlist fix; see command evidence below.

Command evidence:
- `python scripts/test-skill-validator.py` - pass, 151 tests after adding non-allowlisted label regression coverage for `Architecture impact`, `Testability notes`, `Rollout realism`, and `Strategic value`.
- `python scripts/validate-skills.py` - pass.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/change.yaml` - pass.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure` - pass.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-proposal-family-assets-progressive-disclosure.md --path specs/proposal-family-assets-progressive-disclosure.md --path specs/proposal-family-assets-progressive-disclosure.test.md --path docs/plans/2026-05-20-proposal-family-assets-progressive-disclosure.md --path docs/plan.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/baseline.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-resolution.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/proposal-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/proposal-review-r2.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/spec-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/plan-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/code-review-m1-r1.md` - pass.
- `git diff --check --` - pass.

### code-review-m3-r2

No material findings.

Resolution:
Added a closed-allowlist validation path for `proposal-review` asset field labels. Forbidden review-policy wording still fails, approved structural labels still pass, and non-allowlisted field labels now fail with a specific structural-label allowlist error. M1 is returned to `code-review`; M2-M4 remain open and are not ready from this resolution alone.

### code-review-m1-r2

No material findings.

### code-review-m2-r1

No material findings.

### code-review-m3-r1

## Findings

#### PFA-M3-CR1

Finding ID: PFA-M3-CR1
Disposition: accepted
Status: resolved
Owner: implementation agent
Owning stage: implement M3
Chosen action: Restored the pinned `## Result` block shape in `assets/review-result-skeleton.md`, including the literal `- Skill: proposal-review` field, added `Skill` to the proposal-review structural-label allowlist, and added a validator regression test that fails when the result skeleton lacks the baseline heading or `Skill` field.
Rationale: The approved spec requires source-to-asset parity for every extracted structure, and the pinned baseline records `Skill` as part of the review-result field set.
Validation target: M3 validation proves the restored asset validates, the direct regression test fails missing baseline heading/field fixtures, review artifacts close, and lifecycle state returns M3 to code-review rerun.
Validation evidence: Full M3 review-resolution validation passed after the fix; see command evidence below.

Command evidence:
- `python scripts/validate-skills.py skills/proposal-review/SKILL.md` - pass, validated 1 skill file.
- `python scripts/test-skill-validator.py` - pass, 152 tests including `test_proposal_review_result_skeleton_preserves_baseline_result_block`.
- `python scripts/validate-skills.py` - pass, validated 23 skill files.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/change.yaml` - pass.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure` - pass.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` - pass.
- `git diff --check --` - pass.
