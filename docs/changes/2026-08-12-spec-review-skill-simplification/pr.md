# Pull Request Handoff

| Field | Value |
| --- | --- |
| PR URL | Pending creation |
| PR state | pending |
| Base branch | main |
| Head branch | proposal/spec-review-skill-simplification |

## Title

refactor: simplify spec-review common path

## Summary

- Reduce the isolated formal `spec-review` profile from 2,328 to 2,143 words and from 17,407 to 16,248 UTF-8 bytes while preserving review judgment, recording, statuses, stops, claims, and handoff authority.
- Move exact governed settlement and workflow-managed automation into one conditionally loaded reference while keeping isolated formal judgment and recording self-sufficient.
- Preserve canonical, generated, archive, and installed package integrity without adding a target-agent runtime, permanent simplicity validator, tokenizer, selector class, or new output asset.

## Why

- Isolated formal reviews previously loaded governed settlement and automation procedure they could not use.
- Repeated orientation, routing, recording, settlement, boundary, and output guidance obscured ownership and increased drift risk.
- The revised package makes the common path easier to scan while loading governed procedure only after exact same-change authority is established.

## Spec / plan / architecture

- Proposal: `docs/proposals/2026-08-12-spec-review-skill-simplification.md`
- Spec: `specs/spec-review-skill-simplification.md`
- Test spec: `specs/spec-review-skill-simplification.test.md`
- Architecture assessment: `docs/changes/2026-08-12-spec-review-skill-simplification/architecture-assessment.md` (`architecture-not-required`)
- Plan: `docs/plans/2026-08-12-spec-review-skill-simplification.md`

## What changed

- Reworked `skills/spec-review/SKILL.md` around formal classification, universal review judgment, isolated recording, status, stops, claims, resource failure, and bounded handoff.
- Added `references/governed-spec-review-settlement.md` as the sole conditional owner for matching-entry settlement and workflow-managed automation.
- Expanded `review-result-skeleton.md` with closed recording, governed-settlement, boundary-review, and automated-review structural groups without moving policy into the asset.
- Migrated validator consumers to the complete package and added focused tests for profiles, authority separation, record-first settlement, asset structure, and resource availability.
- Added 18-rule and 18-literal preservation ledgers, 17 static scenarios, negative closed-vocabulary fixtures, profile measurements, semantic review, and package-chain proof.
- Recorded five exact-path owner deferrals for one-change proof artifacts instead of creating permanent selector or validator infrastructure.

## Tests and verification

- [x] `bash scripts/ci.sh --mode pr --base 72221718 --head HEAD` — 26 direct product and governance checks passed at post-review head `478be032`.
- [x] `python scripts/select-validation.py --mode pr --base 72221718 --head HEAD` — 12 checks selected, zero blockers, five complete owner-deferred records, no broad smoke required.
- [x] CMD1 ledger and scenario proof — 18 rules, 18 literals, 17 scenarios; unknown values rejected first.
- [x] `python scripts/test-skill-validator.py` — 313 passed, 16 documented skips.
- [x] `python scripts/test-build-skills.py` — seven passed.
- [x] `python scripts/build-skills.py --check` — passed.
- [x] `python scripts/test-adapter-distribution.py` — 150 passed in M3 package proof.
- [x] Fresh Codex, Claude, and OpenCode archive and selected clean-install proof — passed.
- [x] Formal review structure — 21 reviews, 14 resolved findings, zero open findings.
- [ ] Hosted CI — pending after PR creation.

## Requirement coverage

- R1-R19, R26-R32 → T1-T5, T9-T13 → formal classification, universal judgment and recording, exact profiles, assets, stops, claims, and handoff in `SKILL.md` and focused assertions.
- R20-R25 → T2-T5, T12-T13 → exact governed authority, conditional reference loading, record-first matching-entry settlement, and workflow-managed automation boundaries.
- R33-R40 → T6-T9, T14, MP0-MP1 → semantic and literal ledgers, static scenarios, readability proof, independent semantic review, and honest profile accounting.
- R41-R45 → T10-T14 → canonical, generated, archive, installed, boundary, compatibility, and rollback proof.

## Review resolution summary

- Accepted: 14
- Rejected: 0
- Deferred: 0
- Partially accepted: 0
- Needs decision: 0
- Open findings: 0
- Review resolution: `docs/changes/2026-08-12-spec-review-skill-simplification/review-resolution.md`

## Risks and rollback

- Risk: governed assemblies grow because the conditional procedure is now complete and explicit. Keep the reference conditional and prevent cross-owner duplication.
- Risk: the package has one additional mapped reference. Existing mapping, generation, archive, and clean-install checks protect parity.
- Risk: exact normative and parser literals can drift. Separate literal evidence and package-aware regression tests retain those contracts.
- Risk: five change-local evidence paths remain visible owner-deferred registration debt. Their direct CMD1 and MP1 proof remains mandatory.
- Rollback: revert the canonical skill, new reference, asset changes, validator consumer migration, focused tests, and change-local evidence together; regenerate only through existing package tooling.

## Reviewer notes

- Review the boundary between universal formal review and recording in `SKILL.md` and governed settlement and automation in the new reference first.
- Confirm the reference loads only after exact governed authority and that settlement still waits for successful durable recording.
- Confirm the result asset owns layout only and boundary references retain their existing activation and identity.
- The advisory reduction range did not override semantic preservation; the achieved isolated-profile reduction is 7.95% by words and 6.66% by bytes.
- Hosted CI is not yet observed and must not be inferred from the passing local gate.

## Follow-ups

None required for this scoped change.
