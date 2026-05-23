# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Codex proposal-review
Target: docs/proposals/2026-05-23-release-process-contract.md
Status: approved
Reviewed artifact: docs/proposals/2026-05-23-release-process-contract.md
Review date: 2026-05-23
Recording status: recorded

## Review inputs

- Proposal: `docs/proposals/2026-05-23-release-process-contract.md`
- User-provided review: conversation message on 2026-05-23
- Governance: `CONSTITUTION.md`, `VISION.md`, `docs/workflows.md`
- External sources cited by proposal: npm trusted publishing, provenance, 2FA, and staged publishing documentation

## Result

- Skill: proposal-review
- Review status: approved with observations
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-23-release-process-contract/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-05-23-release-process-contract/review-log.md`
- Review resolution: not-required
- Open blockers: none
- Immediate next stage: isolated stop; next authoring stage is `spec: release process contract` after owner acceptance/status normalization
- No automatic downstream handoff: this review is isolated and does not start spec, test-spec, plan, or implementation work.

## Material Findings

None.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The proposal clearly frames publish as an operation, not a lifecycle change. |
| User value | pass | Repeatable releases, durable evidence, and no per-publish ceremony are concrete maintainer benefits. |
| Option diversity | pass | The proposal compares ad hoc release work, full per-release lifecycle ceremony, standing process contract, and immediate automation. |
| Decision rationale | pass | Option 3 follows from the operating distinction: contract once, execute routine publishes many times. |
| Scope control | pass | Scope budget separates core contract content, first-slice candidates, same-slice dependencies, deferable follow-ups, and separate proposals. |
| Architecture awareness | pass | Release evidence files, CI workflow, package scripts, validators, change metadata, and adapter output are named without changing package behavior in this proposal. |
| Testability | pass | The proposal identifies release checks for version decisions, full gate, generated-output currency, package preview, packed install smoke, registry verification, secret suppression, and failure phases. |
| Risk honesty | pass | Secret leakage, stale generated output, brittle npm auth, missing provenance, wrong dist-tag, bad contents, and post-publish install failure are all named. |
| Rollout realism | pass | The rollout includes spec/test-spec/plan follow-up and a dry-run rehearsal before first real publish. |
| Readiness for spec | pass | Open questions have candidate answers and do not block spec authoring. |

## Scope Preservation Review

Pass.

The proposal visibly preserves the initial goals: create a release-process proposal, avoid per-publish lifecycle over-ceremony, define the process once, preserve release evidence, include npm publish best practices, keep routine publishes operational, distinguish unusual releases, and avoid package behavior changes in this proposal.

## Scope Budget Review

Pass.

The proposal is broad and policy-oriented. The scope budget classifies release-process contract, routine checklist, evidence artifact, version rules, npm policy, CI release workflow, manual fallback, release notes/changelog generation, staged publishing, release CLI, and backport/LTS policy with usable treatment values and reasons.

## Vision Fit Review

Pass.

Root `VISION.md` exists, and the proposal's `Vision fit` section starts with the exact allowed value `fits the current vision`. The direction supports durable evidence for an important project transition without replacing upstream review, CI, or release judgment.

## Standing Artifact Gate Review

Pass.

Root `VISION.md` and `CONSTITUTION.md` exist. The proposal does not bypass a bootstrap gate or source-of-truth gate.

## Observations

### OBS-1: Proposal size and spec-level detail

The proposal is large for a process contract and includes exact evidence-template shape, command snippets, and recovery command blocks. This is not blocking because the content is directionally correct, but the downstream spec should own the precise template and command contract to avoid proposal/spec drift.

Safe downstream resolution: the spec should define the exact release evidence template and command sequences, while the proposal remains the rationale and direction source.

### OBS-2: Release gate language should harden in the spec

The proposal uses softer language such as "should pass the full release gate" for the central safety mechanism. For immutable public artifacts, the spec should make the full gate a hard requirement with only an explicit emergency exception path.

Safe downstream resolution: the spec should state that a release must pass the full gate before publish, except for recorded emergency deferrals with owner approval.

### OBS-3: Generated-output currency should bind to drift checks

The proposal correctly identifies stale generated output as a major release risk, but the spec should name the existing generated-output drift checks or their current equivalents as the proof mechanism.

Safe downstream resolution: the spec should require generated-output drift checks such as `skills.drift`, `adapters.drift`, or current equivalents, and fail the release when generated output differs from canonical source.

## Adversarial Questions

- What proves a routine publish did not need a proposal? The spec should require release evidence to state the release type and whether the publish introduced no new decision.
- Does the release evidence get a selector route? The spec/plan should register `docs/releases/v<version>.md` or the chosen release-evidence class with deterministic selector routing.
- What is the path until trusted publishing CI is configured? The spec should preserve full gate and registry verification even when using manual fallback.

## Recommended Proposal Edits

None required before proposal approval.

Recommended downstream spec refinements:

- Move exact evidence-template shape and command sequences into the spec/test-spec/checklist.
- Make full release gate enforcement hard, with emergency deferral as the explicit recorded exception.
- Bind generated-output currency to drift checks or their current equivalents.
- Require release evidence to state release type and no-new-decision status.
- Register the release-evidence artifact class with deterministic selector routing.
- Preserve full gate and registry verification for manual fallback publishing.

## Recommendation

Approve the proposal direction with observations.

The immediate next authoring stage is `spec: release process contract` after owner acceptance/status normalization. This review is isolated and does not automatically hand off to `spec`, `test-spec`, `plan`, or implementation.
