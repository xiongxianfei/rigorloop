# Pull Request Handoff

| Field | Value |
| --- | --- |
| PR URL | https://github.com/xiongxianfei/rigorloop/pull/136 |
| PR state | open |
| Base branch | main |
| Head branch | proposal/test-spec-review-skill-simplification |

## Title

refactor: simplify test-spec-review common path

## Summary

- Reduce the ordinary `test-spec-review` profile from 2,722 to 2,136 words while preserving proof quality, statuses, stops, claims, and handoff authority.
- Move durable recording and formal-only settlement into one conditionally loaded reference while keeping boundary-first resources additive and unchanged.
- Preserve canonical, generated, archive, and installed package integrity without adding a target-agent runtime, permanent simplicity validator, tokenizer, selector, or result asset.

## Why

- Advisory review previously loaded formal change-record, review-log, and settlement procedure it did not always use.
- Repeated quick-guide, routing, stop, recording, finding, and output descriptions obscured the owner of important rules.
- The new package keeps ordinary review self-sufficient while loading recording procedure only when exact evidence triggers it.

## Spec / plan / architecture

- Proposal: `docs/proposals/2026-08-11-test-spec-review-skill-simplification.md`
- Spec: `specs/test-spec-review-skill-simplification.md`
- Test spec: `specs/test-spec-review-skill-simplification.test.md`
- Architecture assessment: `docs/changes/2026-08-11-test-spec-review-skill-simplification/architecture-assessment.md` (`architecture-not-required`)
- Plan: `docs/plans/2026-08-11-test-spec-review-skill-simplification.md`

## What changed

- Reworked `skills/test-spec-review/SKILL.md` around closed lifecycle and handoff classification, universal proof review, status, staleness, stops, findings, claims, resource failure, and bounded handoff.
- Added `references/test-spec-review-recording-and-settlement.md` with one shared recording procedure and one separately gated formal settlement procedure.
- Migrated installed placement validation to inspect the complete package and added six focused simplification contract tests.
- Added 19-rule and 16-literal preservation ledgers, 16 static scenarios, negative closed-vocabulary fixtures, profile measurements, semantic review, and package-chain proof.
- Recorded five exact-path owner deferrals for one-change proof artifacts instead of creating permanent selector or validator infrastructure.

## Tests and verification

- [x] `bash scripts/ci.sh --mode pr --base 9b0cd7d4 --head HEAD` — 26 direct product and governance checks passed at final review head `151f0c2a`.
- [x] `python scripts/select-validation.py --mode pr --base 9b0cd7d4 --head HEAD` — 11 checks selected, zero blockers, five complete owner-deferred records, no broad smoke required.
- [x] CMD1 ledger/scenario proof — 19 rules, 16 literals, 16 scenarios; unknown values rejected first.
- [x] `python scripts/test-skill-validator.py` — 308 passed, 16 documented skips.
- [x] `python scripts/test-build-skills.py` — seven passed.
- [x] `python scripts/build-skills.py --check` — passed.
- [x] `python scripts/test-adapter-distribution.py` — 150 passed in package proof.
- [x] Trusted `v0.3.6` Codex, Claude, and OpenCode archive/clean-install proof — passed.
- [x] Formal review closeout — 15 reviews, six resolved findings, zero open findings.
- [ ] Hosted CI — pending after PR creation.

## Requirement coverage

- R1-R9, R19-R24, R34-R39 → T1, T3-T5, T9, T12-T16 → closed classification, universal proof/status/claim safety, exact resources, and bounded handoff in `SKILL.md` and focused assertions.
- R10-R18 → T1-T5, T12, T14-T16 → additive recording, formal-only settlement, blocked-recording behavior, and record-first matching-entry updates in the new reference.
- R25-R30, R35, R38 → T6-T9, T12, MP0-MP1 → semantic/literal ledgers, static scenarios, readability proof, independent semantic review, and honest profile accounting.
- R31-R33, R37-R38 → T10-T14 → canonical/generated/archive/install parity, selected clean installs, compatibility, and atomic rollback proof.

## Review resolution summary

- Accepted: 6
- Rejected: 0
- Deferred: 0
- Partially accepted: 0
- Needs decision: 0
- Open findings: 0
- Review resolution: `docs/changes/2026-08-11-test-spec-review-skill-simplification/review-resolution.md`

## Risks and rollback

- Risk: formal profiles grow slightly because the conditional recording procedure is now complete and explicit. Keep the reference conditional and prevent cross-owner duplication.
- Risk: the package has one additional mapped reference. Existing mapping, generation, archive, and clean-install checks protect parity.
- Risk: exact parser/package literals can drift. The separate literal ledger and package-aware regression tests retain those contracts.
- Risk: five change-local evidence paths remain visible owner-deferred registration debt. Their direct CMD1 and MP1 proof remains mandatory.
- Rollback: revert the canonical skill, new reference, validator consumer migration, focused tests, and change-local evidence together; regenerate only through existing package tooling.

## Reviewer notes

- Review the boundary between universal advisory proof judgment in `SKILL.md` and recording/formal settlement in the new reference first.
- Confirm recording never changes verdict, lifecycle mode, handoff mode, or workflow routing authority.
- Confirm boundary references and structural assets remain unchanged and are loaded only by exact triggers.
- The 30-40% ordinary-profile target was advisory: the achieved reduction is 21.53% by words and 18.53% by bytes because universal safety remained inline.
- Hosted CI is not yet observed and must not be inferred from the passing local gate.

## Follow-ups

None required for this scoped change.
