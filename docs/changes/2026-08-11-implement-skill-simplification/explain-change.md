# Implement Skill Simplification Explain Change

## Summary

This change makes the published `implement` skill substantially smaller for isolated and ordinary planned work while preserving its authority, test-first practice, completeness, validation, stop, claim, milestone, correction, and review-handoff contracts.

The universal `SKILL.md` shrinks from 3,338 to 2,187 words. A completed isolated profile falls 28.52% by words and 26.30% by bytes; a planned profile falls 15.31% and 12.57%. The fully armed profile grows 0.99% by words because it alone now loads explicit independent-review and bounded-correction procedure. Total package growth is reported separately at 0.79% by words and 4.17% by bytes.

## Problem and decision

The prior skill loaded planned-milestone and armed-automation procedure for every implementation request and repeated orientation, handoff, and result structure. Deleting prose or optimizing only the main file could weaken universal behavior or hide moved maintenance cost.

The accepted design keeps a self-sufficient universal contract, adds one planned procedure reference and one automation procedure reference with exact identity-bound triggers, and makes one policy-free asset the sole result-layout owner. The existing package architecture already supports mapped resources, so the recorded assessment is `architecture-not-required`.

## Diff rationale

| Area | Change | Why | Contract and proof |
| --- | --- | --- | --- |
| `skills/implement/SKILL.md` | Consolidated universal authority, profiles, proof-first execution, completeness, validation, stops, claims, handoff, boundary method, and resource triggers. | Keeps `IP0-isolated` complete while removing conditional procedure and duplicate result structure. | R1-R7, R31; T1-T2, T9, T12; M2 review R2. |
| Planned reference | Added milestone inspection, baseline/change pack, execution, commit, review handoff, and accepted correction return. | Ordinary planned work needs these steps; isolated work does not. | R8-R9; T3; package and semantic proof. |
| Automation reference | Added armed authority, neutral review packet, fidelity routing, bounded correction/rereview, and promotion/pause procedure. | Only durable automation for the same current planned milestone should load this path. | R10-R12; T4; final holistic review. |
| Result asset | Added core, planned, and armed structural groups with omission rules. | Gives every profile one structural owner without turning the asset into a policy owner. | R13-R15; T5. |
| Skill-validator tests | Added focused profile/resource/ownership assertions and redirected existing automation and result consumers to mapped owners. | Proves the package contract without executing a model; preserves genuine literals while removing incidental prose ownership. | R19-R22, R28-R31; 291-test suite. |
| Rule and literal ledgers | Recorded 24 semantic rules, 18 literal dependencies, closed treatments, destinations, and negative fixtures. | Prevents silent semantic loss and distinguishes contracts from accidental test wording. | R16-R22; CMD1 and MP0/MP1. |
| Measurements and package evidence | Recorded per-profile and total-package words/bytes plus canonical, generated, archive, and installed parity. | Makes relocation and armed-profile cost visible rather than presenting file movement as deletion. | R23-R30, R33; M3 review. |
| Test-spec CMD7 | Replaced an untrusted synthetic version with immutable trusted fixture `v0.3.6` after the original command failed closed. | Clean-install proof requires a version present in the release-metadata trust root. | Test-spec revision and review R2; corrected CMD7. |
| Selector routing debt | Recorded complete owner-approved deferrals for the two one-change ledgers and three static fixtures. | Keeps non-recurring evidence visible and blocked from generic routing without creating permanent simplicity infrastructure. | Existing owner-deferral contract; CMD1, MP0, MP1, and final selector rerun. |

## Test-first and review corrections

The focused M2 package assertion first failed because the planned reference did not exist, then passed after implementation. The complete validator run exposed compatibility-sensitive shared contracts; those stayed inline, while automation and result consumers moved to their new owners.

M2 code review found two mechanical defects: trailing whitespace contradicted the recorded diff-check result, and an unrelated code-review assertion had changed. Both findings were recorded, accepted, corrected on named paths, validated, and independently rereviewed before M3.

The original CMD7 built archives but all clean installs stopped before mutation with `metadata-trust-root-unavailable`. The test-spec owner changed only the fixture identity and cleanup wrapper, test-spec-review R2 approved it, and the trusted rerun validated all three adapters.

## Validation evidence before final verify

- CMD1: 24 rules, 18 literals, eleven scenarios, unknown values rejected.
- Canonical skill validation passed.
- `scripts/test-skill-validator.py`: 291 tests passed, 16 governed skips.
- `scripts/test-build-skills.py`: seven tests passed.
- Generated skill checking passed in a temporary tree.
- `scripts/test-adapter-distribution.py`: 150 tests passed.
- Trusted `v0.3.6` CMD7 validated Codex, Claude, and opencode archives and clean installed `implement` packages.
- Boundary-first, lifecycle metadata, and review-artifact structure validation passed.
- No target agent, network call, publication, or new permanent simplicity validator was used.

## Alternatives rejected

- Inline-only deduplication would keep planned and automation procedure on every path.
- One combined conditional reference would make ordinary planned work load armed-review procedure.
- Several small fragments would increase trigger and packaging complexity.
- A generic checklist would weaken lifecycle and claim boundaries.
- A mandatory percentage or permanent size validator would make prose length a policy owner.
- Runtime prompt journeys or transcript grading would test model behavior rather than the published package contract.

## Scope and residual risk

No new runtime, persistent state, dependency, service, lifecycle owner, validator family, scheduler, or release publication was introduced. Canonical authorship remains under `skills/`; generated adapters remain derived.

The selector deferrals are exact-path repository-maintainer decisions. They do not waive CMD1, MP0, MP1, or focused literal-consumer proof and do not create a generic evidence bypass.

The package now has more files, so exact Resource-map triggers and package parity remain important drift controls. Token estimates are advisory only. PR preparation remains outside the armed workflow target.

## Readiness

All implementation milestones, finding resolutions, the corrected test-spec review, and final holistic code review are closed. This explanation is current for reviewed commit `8404313c` and is ready for final `verify`; it does not claim branch or PR readiness before verification runs.
