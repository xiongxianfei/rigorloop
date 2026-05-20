# Review Resolution: Test-Spec Contract Normalization

## Summary

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: plan-review-r1
Review closeout: code-review-m2-r1
Review closeout: code-review-m3-r1

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `spec-review-r1`, `plan-review-r1`, `code-review-m2-r1`, `code-review-m3-r1`
- Findings resolved: 4
- Unresolved findings: 0
- Final result: proposal-review requested changes in R1 for baseline audit evidence, preservation proof, amendment sequencing, and generated adapter validation. The proposal was revised to add those controls, R2 approved the proposal with no material findings, spec-review R1 approved the skill-contract amendment with no material findings, plan-review R1 approved the execution plan with no material findings, code-review M2 R1 closed M2 with no material findings, and code-review M3 R1 closed all implementation milestones with no material findings.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
|---|---|---|---|
| TSCN-PR1 | accepted | resolved | Added a baseline compliance audit with concrete evidence for `spec`, `spec-review`, and `test-spec`. |
| TSCN-PR2 | accepted | resolved | Added content-preservation proof requirements and acceptance criteria for moved and skeletonized content. |
| TSCN-PR3 | accepted | resolved | Added amendment sequencing that blocks implementation until the plan names an approved proof route. |
| TSCN-PR4 | accepted | resolved | Added a generated adapter output boundary requiring rebuild or validation unless explicitly deferred in the plan. |

## Resolution Entries

### proposal-review-r1

#### TSCN-PR1 - Baseline audit evidence is not durable enough

Finding ID: TSCN-PR1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Baseline compliance audit` to the proposal with evidence for `spec`, `spec-review`, and `test-spec` across front matter, Workflow role, output skeleton, and stop-condition surfacing.
Rationale: Downstream reviewers need durable evidence for why the proposal touches only `test-spec`.
Validation target: Proposal includes baseline audit evidence and keeps `spec` and `spec-review` out of scope.
Validation evidence: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-test-spec-contract-normalization.md --path docs/changes/2026-05-20-test-spec-contract-normalization/change.yaml --path docs/changes/2026-05-20-test-spec-contract-normalization/review-log.md --path docs/changes/2026-05-20-test-spec-contract-normalization/review-resolution.md --path docs/changes/2026-05-20-test-spec-contract-normalization/reviews/proposal-review-r1.md` passed; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-test-spec-contract-normalization` passed; `git diff --check -- docs/proposals/2026-05-20-test-spec-contract-normalization.md docs/changes/2026-05-20-test-spec-contract-normalization` passed.

### proposal-review-r2

No material findings.

### spec-review-r1

No material findings.

### plan-review-r1

No material findings.

### code-review-m2-r1

No material findings.

### code-review-m3-r1

No material findings.

#### TSCN-PR2 - Preservation proof is too general for stop-condition promotion and skeleton creation

Finding ID: TSCN-PR2
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Content-preservation proof`, including a source-to-destination preservation matrix and acceptance criteria for stop conditions, required sections, test-case format, and coverage-map obligations.
Rationale: A no-behavior-change proposal needs concrete proof for behavior-significant moved or skeletonized content.
Validation target: Proposal requires a preservation matrix before `code-review` and states that structural validation alone is insufficient.
Validation evidence: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-test-spec-contract-normalization.md --path docs/changes/2026-05-20-test-spec-contract-normalization/change.yaml --path docs/changes/2026-05-20-test-spec-contract-normalization/review-log.md --path docs/changes/2026-05-20-test-spec-contract-normalization/review-resolution.md --path docs/changes/2026-05-20-test-spec-contract-normalization/reviews/proposal-review-r1.md` passed; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-test-spec-contract-normalization` passed; `git diff --check -- docs/proposals/2026-05-20-test-spec-contract-normalization.md docs/changes/2026-05-20-test-spec-contract-normalization` passed.

#### TSCN-PR3 - Amendment sequencing is ambiguous

Finding ID: TSCN-PR3
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Amendment sequencing`, requiring the plan to name one approved proof route before implementation begins, and revised Rollout and Next artifacts accordingly.
Rationale: Implementation should not begin until the proof route is explicit and approved.
Validation target: Proposal names the three allowed routes and no longer implies unconditional `spec-review`.
Validation evidence: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-test-spec-contract-normalization.md --path docs/changes/2026-05-20-test-spec-contract-normalization/change.yaml --path docs/changes/2026-05-20-test-spec-contract-normalization/review-log.md --path docs/changes/2026-05-20-test-spec-contract-normalization/review-resolution.md --path docs/changes/2026-05-20-test-spec-contract-normalization/reviews/proposal-review-r1.md` passed; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-test-spec-contract-normalization` passed; `git diff --check -- docs/proposals/2026-05-20-test-spec-contract-normalization.md docs/changes/2026-05-20-test-spec-contract-normalization` passed.

#### TSCN-PR4 - Generated adapter validation is too conditional

Finding ID: TSCN-PR4
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Generated adapter output boundary`, requiring current generated adapter output to be rebuilt or validated from canonical `skills/` when `skills/test-spec/SKILL.md` changes, unless the plan records an explicit deferral with rationale.
Rationale: The proposal should distinguish legacy archive non-rewrite from current generated output currency.
Validation target: Proposal names candidate generated-output validation commands and keeps generated adapter skill bodies non-authored.
Validation evidence: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-test-spec-contract-normalization.md --path docs/changes/2026-05-20-test-spec-contract-normalization/change.yaml --path docs/changes/2026-05-20-test-spec-contract-normalization/review-log.md --path docs/changes/2026-05-20-test-spec-contract-normalization/review-resolution.md --path docs/changes/2026-05-20-test-spec-contract-normalization/reviews/proposal-review-r1.md` passed; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-test-spec-contract-normalization` passed; `git diff --check -- docs/proposals/2026-05-20-test-spec-contract-normalization.md docs/changes/2026-05-20-test-spec-contract-normalization` passed.
