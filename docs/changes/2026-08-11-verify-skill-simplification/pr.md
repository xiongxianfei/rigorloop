# Pull Request Handoff

| Field | Value |
| --- | --- |
| PR URL | https://github.com/xiongxianfei/rigorloop/pull/135 |
| PR state | open |
| Base branch | main |
| Head branch | proposal/verify-skill-simplification |

## Title

refactor: simplify verify skill common path

## Summary

- Reduce the universal `verify` skill from 2,896 to 2,140 words while preserving scoped evidence, review closeout, lifecycle, claim, and handoff rigor.
- Move final branch-readiness aggregation into one conditionally loaded reference; keep the existing boundary-first reference additive and unchanged.
- Preserve canonical/generated/archive/install parity without adding a target-agent runtime, permanent simplicity validator, tokenizer, selector, or result asset.

## Why

- Scoped verification previously loaded final lifecycle, release, and PR-handoff procedure that applied only to branch readiness or governed final verification.
- Repetition obscured ownership between universal evidence truthfulness and final evidence aggregation.
- The new package keeps ordinary verification self-sufficient while loading final-closeout procedure only when its exact outcome requires it.

## Spec / plan / architecture

- Proposal: `docs/proposals/2026-08-11-verify-skill-simplification.md`
- Spec: `specs/verify-skill-simplification.md`
- Test spec: `specs/verify-skill-simplification.test.md`
- Architecture assessment: `docs/changes/2026-08-11-verify-skill-simplification/architecture-assessment.md` (`architecture-not-required`)
- Plan: `docs/plans/2026-08-11-verify-skill-simplification.md`

## What changed

- Reworked `skills/verify/SKILL.md` around three closed outcomes, exact target resolution, four loading profiles, two independent execution modes, universal evidence semantics, and fail-safe resource loading.
- Added `references/branch-readiness-verification.md` as the sole owner of final evidence applicability, aggregation, verdict calculation, and mode-specific completion.
- Added five focused assertions to the existing skill validator plus change-local semantic/literal ledgers, negative fixtures, 17 static scenarios, measurements, and package proof.
- Preserved the parser/package literal `closeout validation passes` after the complete PR gate exposed its exact compatibility requirement.
- Recorded five exact-path owner deferrals for one-change proof artifacts instead of creating permanent selector or validator infrastructure.

## Tests and verification

- [x] `bash scripts/ci.sh --mode pr --base db45673554029473fcd282b4deb740ef3d775f73 --head HEAD` — 26 direct product and governance checks passed.
- [x] `python scripts/select-validation.py --mode pr --base db45673554029473fcd282b4deb740ef3d775f73 --head HEAD` — 12 checks selected, zero blockers, zero unclassified paths, five complete owner-deferred records, no broad smoke required.
- [x] `python scripts/test-review-artifact-validator.py` — 103 passed.
- [x] `python scripts/test-skill-validator.py` — 302 passed, 16 documented skips.
- [x] `python scripts/test-build-skills.py` — seven passed.
- [x] `python scripts/build-skills.py --check` — passed.
- [x] `python scripts/test-adapter-distribution.py` — 150 passed in package proof and exercised again by the PR gate.
- [x] Trusted `v0.3.6` Codex, Claude, and OpenCode archive/clean-install proof — passed.
- [x] Formal review closeout — 15 reviews, four resolved findings, zero open findings.
- [ ] Hosted CI — pending after PR creation.

## Requirement coverage

- R1-R13 → T1-T3, T5, T9, T12 → closed outcomes/targets, execution authority, universal evidence truthfulness, and scoped safety in `skills/verify/SKILL.md`.
- R14-R22 → T4-T5, T9, T12 → final applicability/aggregation, mode-specific completion, resource triggers, and fail-safe loading in the branch-readiness reference and focused validator assertions.
- R23-R29 → T6-T9, T12 → fail-closed rule/literal ledgers, static scenarios, independent semantic review, and deterministic profile accounting.
- R30-R33 → T10-T14 → canonical/generated/archive/install parity, compatibility, bounded architecture assessment, and atomic rollback proof.

## Review resolution summary

- Accepted: 4
- Rejected: 0
- Deferred: 0
- Partially accepted: 0
- Needs decision: 0
- Open findings: 0
- Review resolution: `docs/changes/2026-08-11-verify-skill-simplification/review-resolution.md`

## Risks and rollback

- Risk: the package has one additional mapped resource. Existing mapping, generation, archive, and clean-install checks protect parity.
- Risk: exact parser/package literals can be missed by semantic-only review. The separate literal ledger and repository-wide regression retain these contracts.
- Risk: five change-local evidence paths remain visible owner-deferred registration debt. Their direct CMD1/MP1 proof remains mandatory.
- Rollback: revert the canonical skill, new reference, focused assertions, and change-local evidence together; regenerate only through existing package tooling.

## Reviewer notes

- Review the boundary between item-level evidence truthfulness in `SKILL.md` and final evidence aggregation in the new reference first.
- Confirm resource loading never grants lifecycle-write or PR authority.
- Confirm every profile and the total package shrink; the 30-40% VP0 target was advisory and semantic preservation controlled acceptance.
- Hosted CI is not yet observed and must not be inferred from the passing local gate.

## Follow-ups

None required for this scoped change.
