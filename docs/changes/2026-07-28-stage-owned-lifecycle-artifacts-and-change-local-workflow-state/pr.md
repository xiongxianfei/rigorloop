# Pull Request Handoff

| Field | Value |
| --- | --- |
| PR URL | https://github.com/xiongxianfei/rigorloop/pull/127 |
| PR state | open |
| Base branch | main |
| Head branch | stage-owned-lifecycle-artifacts |

## Title

feat: enforce stage-owned lifecycle state

## Summary

- Make governed proposal, spec, architecture, ADR, plan, and test-spec content stable while their mutable lifecycle state lives in the owning `change.yaml`.
- Keep authoring and matching review skills as peers with fixed write boundaries.
- Preserve one target-driven automation flow without profiles, capabilities, selector parameters, hashes, or upstream write-back.
- Add prospective migration, generated adapter parity, and deterministic validation for the new state contract.

## Why

Downstream automation could previously rewrite upstream artifacts or status fields, invalidating approved content and creating recursive regeneration.

The new model separates discovery, content ownership, review settlement, and workflow routing while preserving automatic continuation through a selected target.

## Spec / plan / architecture

- Proposal:
  `docs/proposals/2026-07-28-approved-specification-baselines-and-controlled-amendment-workflow.md`
- Spec:
  `specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md`
- Test spec:
  `specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.test.md`
- Architecture:
  `docs/architecture/system/architecture.md`
- ADR:
  `docs/adr/ADR-20260729-stage-owned-change-local-lifecycle-state.md`
- Plan:
  `docs/plans/2026-07-29-stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md`

## What changed

- Updated canonical published skills and assets with stage-owned outputs, upstream read-only boundaries, peer-review settlement, route-back, and independent-invocation behavior.
- Added the `stage-owned-change-local-v1` artifact, workflow, milestone, blocker, review, and automation state contract to the existing metadata path.
- Added bounded atomic state persistence and prospective migration while leaving historical reads side-effect free.
- Updated generated adapter and guide/selector projections to follow the new contract without adding another public mechanism.
- Recorded milestone reviews, review resolutions, behavior preservation, final rationale, and verification evidence.

## Tests and verification

- [x] `python scripts/test-skill-validator.py` — 269 passed; 17 explicitly superseded historical projections skipped.
- [x] `python scripts/test-change-metadata-validator.py` — 61 passed.
- [x] `python scripts/test-workflow-automation-state.py` — 65 passed.
- [x] `python scripts/test-adapter-distribution.py` — 133 passed.
- [x] `python scripts/test-select-validation.py` — 136 passed.
- [x] `python scripts/test-guide-system-validator.py` — 10 passed.
- [x] `bash scripts/ci.sh --mode pr --base f73c0f622d248f54708c580b92e1d4193da4a3e2 --head HEAD` — 20 selected checks passed; broad smoke passed in 432.15 seconds.
- [ ] Hosted CI — pending after PR creation.

## Requirement coverage

- SLA-R001–R041 → change-local lifecycle shape, transition authority, metadata semantics, and state-adapter tests.
- SLA-R042–R047 → downstream route-back and read-only published-skill tests.
- SLA-R048–R064a → single-target workflow scenarios and activation tests.
- SLA-R065–R074e → migration, compatibility, generated parity, and boundary-first evidence.
- AC-SLA-001–035 → approved T1–T26 proof map and final PR-mode verification.

## Review resolution summary

- Accepted: 24
- Rejected: 0
- Deferred: 0
- Partially accepted: 0
- Needs decision: 0
- Review resolution:
  `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/review-resolution.md`

## Risks and rollback

- Risk: legacy and current state could be mixed.
  The validator rejects mixed writers; historical reads remain unchanged.
- Risk: canonical and generated published skills could diverge.
  Temporary generation, adapter distribution, and broad smoke prove parity.
- Rollback: revert the M6 activation default while preserving stage-owned skill boundaries and recorded evidence; return to explicit invocation without restoring upstream write-back.

## Reviewer notes

- Review canonical published skill clarity first, especially peer review and downstream route-back boundaries.
- Review `change_metadata_semantics.py` for closed-vocabulary and settlement consistency behavior.
- Review `StageOwnedChangeStateStore` for atomic replacement, optimistic identity checks, and migration containment.
- Confirm the two CI-maintenance corrections reuse existing checks rather than creating per-file selectors.

## Follow-ups

None required for this PR.

Historical changes are intentionally not mass-migrated.
