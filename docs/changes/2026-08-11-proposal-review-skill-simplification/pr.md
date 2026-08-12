# Pull Request Handoff

| Field | Value |
| --- | --- |
| PR URL | https://github.com/xiongxianfei/rigorloop/pull/137 |
| PR state | open |
| Base branch | main |
| Head branch | proposal/proposal-review-skill-simplification |

## Title

refactor: simplify proposal-review common path

## Summary

- Reduce the ordinary `proposal-review` assembly by 10.2% in words and 9.5% in bytes while preserving universal judgment, materiality, status, isolation, claim, and handoff rules.
- Move durable recording/settlement and specialized proposal gates into two conditionally loaded references with closed triggers and fail-safe resource behavior.
- Keep the existing assets as structural owners and prove semantic, generated, archive, and clean-install integrity without target-agent runtime testing.

## Why

- Ordinary advisory reviews previously loaded formal lifecycle recording, workflow automation, exceptional vision/standing-artifact gates, and broad scope-budget procedure.
- Repeated placement, settlement, and result structures obscured ownership and made exact-string tests accidental prose-policy owners.
- The new package keeps direct advisory review self-sufficient while loading conditional procedure only when current evidence requires it.

## Spec / plan / architecture

- Proposal: `docs/proposals/2026-08-11-proposal-review-skill-simplification.md`
- Spec: `specs/proposal-review-skill-simplification.md`
- Test spec: `specs/proposal-review-skill-simplification.test.md`
- Architecture assessment: `docs/changes/2026-08-11-proposal-review-skill-simplification/architecture-assessment.md` (`architecture-not-required`)
- Plan: `docs/plans/2026-08-11-proposal-review-skill-simplification.md`

## What changed

- Reworked `skills/proposal-review/SKILL.md` around closed recording/automation modes, specialized predicates, four resource assemblies, universal review judgment, and exact resource triggers.
- Added `references/proposal-review-recording-and-settlement.md` for location selection, durable evidence, retry reconciliation, formal settlement, and workflow-managed automated review.
- Added `references/conditional-proposal-gates.md` for vision exceptions, standing-artifact bootstrap, scope-budget review, composition, and ambiguity handling.
- Expanded the result skeleton into one core and four conditional structural groups without moving status or authority policy into assets.
- Updated existing validators and consumers to understand package ownership, and added 21 semantic dispositions, 17 literal dependencies, 25 static scenarios, negative closed-value fixtures, measurements, and package proof.
- Recorded five exact-path selector deferrals for one-change evidence instead of introducing permanent simplicity or fixture-routing infrastructure.

## Tests and verification

- [x] `bash scripts/ci.sh --mode pr --base 27827abc9e7448d0deaa5f16c08bc9d1ce27b5e9 --head HEAD` — current-base PR gate passed.
- [x] `python scripts/select-validation.py --mode pr --base 27827abc9e7448d0deaa5f16c08bc9d1ce27b5e9 --head HEAD` — 12 checks selected, zero blockers, no broad smoke required.
- [x] `python scripts/test-skill-validator.py` — 311 passed, 16 documented skips.
- [x] `python scripts/test-build-skills.py` — 7 passed.
- [x] `python scripts/build-skills.py --check` — passed.
- [x] `python scripts/test-adapter-distribution.py` — passed.
- [x] Trusted `v0.3.6` Codex, Claude, and opencode archive/clean-install proof — passed.
- [x] Formal review closeout — 15 reviews, 7 resolved findings, zero open findings.
- [ ] Hosted CI — the first run exposed and now has a local fix for a case-sensitive incidental prose assertion; the replacement run is pending.

## Requirement coverage

- R1-R8 and R14-R28 → T1-T7, T9-T12 → universal review behavior, closed modes/assemblies, output applicability, missing-resource safety, and claim boundaries in the skill package and focused validator assertions.
- R9-R13 and R16-R17 → T2, T4-T6, T12-T13 → recording location, retry, formal settlement, automation boundaries, and workflow return in the recording reference and static fixtures.
- R18-R24 → T3, T6-T7, T12 → specialized predicates, combined/late gates, ambiguity stops, and non-overriding composition in the gates reference.
- R29-R37 → T8, T10-T15 → rule/literal ledgers, fail-closed fixtures, profile accounting, semantic review, generated/archive/install parity, and bounded architecture assessment.

## Review resolution summary

- Accepted: 7
- Rejected: 0
- Deferred: 0
- Partially accepted: 0
- Needs decision: 0
- Open findings: 0
- Review resolution: `docs/changes/2026-08-11-proposal-review-skill-simplification/review-resolution.md`

## Risks and rollback

- Risk: recorded and specialized assemblies are larger because they load explicit conditional procedure; review resource ownership and trigger boundaries together.
- Risk: the total package grows 35.2% in words while the ordinary path shrinks; the change reports both rather than presenting relocation as deletion.
- Risk: exact parser/package literals can be missed by semantic-only review; the separate literal ledger and regression suite retain those contracts.
- Risk: five change-local evidence paths remain visible owner-deferred registration debt; CMD1 and MP1 remain mandatory.
- Rollback: revert the canonical skill, both references, result asset, validator changes, and change-local evidence together, then regenerate only through existing package tooling.

## Reviewer notes

- Review the boundary between universal judgment in `SKILL.md`, durable side effects in the recording reference, and exceptional judgment in the gates reference first.
- Confirm loading a reference never grants settlement, correction, workflow-continuation, or PR authority.
- Confirm assets remain structural and the M2 correction leaves one canonical formal-settlement owner.
- Hosted CI is not yet observed and must not be inferred from the passing local PR gate.

## Follow-ups

None required for this scoped change.
