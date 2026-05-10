# Review Resolution: Token Cost Measurement Baseline and Proposal Scope Preservation

## Summary

Closeout status: open

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: architecture-review-r1
Review closeout: plan-review-r1
Review closeout: code-review-m3-r1

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `spec-review-r1`, `architecture-review-r1`, `plan-review-r1`, `code-review-m3-r1`
- Findings resolved: 1
- Unresolved findings: 1
- Current result: proposal-review R1 requested revision for one material finding. The proposal now makes focused spec authoring mandatory before execution planning or implementation relies on the contributor-visible workflow and skill behavior change. Proposal-review R2 approved the revised proposal with no material findings. Spec-review R1 approved the spec with no material findings. Architecture-review R1 approved the canonical architecture update with no material findings. Plan-review R1 approved the active plan with no material findings. Code-review M3 R1 requested one fix for proposal-review expected-output alignment before M3 can close.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
|---|---|---|---|
| TCSP-PR1-F1 | accepted | resolved | Proposal replaced optional spec/plan wording with required focused spec before implementation planning. |
| TCSP-CR-M3-F1 | accepted | open | Proposal-review expected output must include or map `changes-requested` for silent-narrowing findings before M3 returns to code-review. |

## Resolution Entries

### proposal-review-r1

#### TCSP-PR1-F1 - Downstream artifact wording makes spec optional

Finding ID: TCSP-PR1-F1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Chosen action: Replaced "focused spec or implementation plan" with "focused spec, then implementation plan if the accepted spec requires one" in `Rollout and rollback` and `Next artifacts`, and updated `Readiness` to route through proposal revision, proposal-review, and then spec once accepted.
Rationale: The proposal affects contributor-visible skill behavior, proposal-review behavior, validation expectations, and new measurement scripts. Under the repository's spec-driven rules, behavior-changing and workflow-governance changes need an approved spec before implementation relies on them.
Validation target: Proposal `Rollout and rollback`, `Next artifacts`, and `Readiness` should make focused spec authoring the required next authoring stage before execution planning or implementation.
Validation evidence: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation`, `python scripts/validate-change-metadata.py docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation/change.yaml`, and `git diff --check -- docs/proposals/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md docs/changes/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation` passed after the proposal revision.

### proposal-review-r2

No material findings.

### spec-review-r1

No material findings.

### architecture-review-r1

No material findings.

### plan-review-r1

No material findings.

### code-review-m3-r1

#### TCSP-CR-M3-F1 - Proposal-review expected output still omits `changes-requested`

Finding ID: TCSP-CR-M3-F1
Disposition: accepted
Status: open
Owner: implement
Owning stage: review-resolution
Decision owner: implement
Chosen action: Pending. Update `skills/proposal-review/SKILL.md` so the expected output includes or explicitly maps `changes-requested` for scope-preservation failures, and update static validator coverage for that output contract alignment.
Rationale: The approved spec requires proposal-review to return `changes-requested` for silent-narrowing failures. The M3 skill update adds those rules but leaves the normal expected verdict list as `approve`, `revise`, or `rethink`, creating an inconsistent public skill contract.
Validation target: `skills/proposal-review/SKILL.md` expected output aligns with R8b-R8e, `scripts/test-skill-validator.py` directly protects that alignment, and M3 validation passes before the milestone returns to code-review.
Validation evidence: Pending review-resolution implementation.
