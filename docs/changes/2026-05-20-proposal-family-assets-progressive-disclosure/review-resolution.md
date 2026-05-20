# Proposal-Family Assets Progressive Disclosure Review Resolution

## Summary

Closeout status: open

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: plan-review-r1
Review closeout: code-review-m1-r1

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
Status: open
Owner: implementation agent
Owning stage: implement M1
Chosen action: Pending. Add non-allowlisted proposal-review structural-label rejection and fixture coverage before returning M1 to code review.
Rationale: The approved spec requires explicit structural-label allowlist enforcement for proposal-review assets, not only forbidden-policy phrase detection.
Validation target: `proposal-review` asset validation rejects field labels that are not in `PROPOSAL_REVIEW_ASSET_ALLOWED_FIELD_LABELS` and keeps approved labels passing.
Validation evidence: pending
