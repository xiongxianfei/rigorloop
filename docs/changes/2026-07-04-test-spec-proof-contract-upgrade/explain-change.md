# Explain Change: Test-Spec Proof-Contract Upgrade

## Status

Explain-change complete. Final `verify`, branch readiness, PR readiness, and hosted CI status are not claimed by this artifact.

## Summary

This change upgrades the authored `test-spec` skill so future test specs make command ownership, milestone proof timing, and evidence artifacts explicit before implementation begins.

The implementation adds:

- `test-spec` authoring rules for input artifact identities, validation-command ledgers, command IDs, and milestone proof maps;
- packaged row assets for validation commands and milestone proof-map rows;
- representative fixture validation for command ledgers, command classifications, planned-command metadata, milestone proof maps, and raw command references without Command IDs;
- generated-output and behavior-preservation proof showing the revised skill and assets remain reproducible from canonical sources;
- lifecycle review evidence for proposal, spec, plan, test-spec, implementation milestones, review resolution, and code review.

Manual-proof contracts remain out of scope. Existing Manual QA checklist behavior remains unchanged.

## Problem

The accepted proposal identified a recurring authoring gap: a test spec could name commands and manual-style proof obligations without making the command ownership, milestone timing, zero-test behavior, failure behavior, and evidence artifacts reviewable before implementation.

The approved scope narrowed this proposal to command-ledger and milestone-proof-map improvements. Manual-proof contracts were explicitly deferred.

## Decision Trail

| Decision point | Outcome | Source |
| --- | --- | --- |
| Proposal direction | Upgrade `test-spec` and skeleton/assets together so authoring starts from the same proof-contract shape reviewers enforce. | `docs/proposals/2026-07-04-test-spec-proof-contract-upgrade.md`; `proposal-review-r1` |
| Manual-proof scope | Exclude manual-proof contracts and preserve existing Manual QA checklist behavior. | R28, R29 |
| Command ledger | Require a validation-command ledger whenever commands are named or depended on; allow explicit no-command rationale otherwise. | R1-R12 |
| Milestone proof map | Require milestone proof maps for milestone-based plans; allow explicit not-applicable rationale for non-milestone cases. | R15-R20 |
| Test-case fields | Add `Command IDs`, `Evidence artifact`, and `Required by milestone`. | R21, R23 |
| Assets | Add only `assets/validation-command-row.md` and `assets/milestone-proof-row.md`; do not add `assets/manual-proof.md`. | R22-R29 |
| Validation strategy | Start with representative fixture validation, not a full semantic validator for every historical test spec. | R33, R34 |
| Generated proof | Prove generated skills and adapters include the revised skill/assets using repository-owned scripts. | R35 |
| Migration boundary | Do not automatically migrate historical test specs. | R36 |
| Plan milestones | Split implementation into M1 skill/assets, M2 representative validation, and M3 generated-output/preservation proof. | `docs/plans/2026-07-04-test-spec-proof-contract-upgrade.md` |

Architecture was assessed as not required because the work changes authored skill text, assets, validation fixtures, and lifecycle artifacts rather than runtime architecture, data persistence, APIs, or long-lived system boundaries.

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `skills/test-spec/SKILL.md` | Added conditional `Input artifact identities`, `Validation commands`, and `Milestone proof map` guidance; added command classification rules; preserved `test-spec-review` route and claim boundaries. | Make proof ownership explicit during authoring. | R1-R21, R26, R30-R32 | `python scripts/validate-skills.py skills/test-spec/SKILL.md`; code-review-m1-r1 |
| `skills/test-spec/assets/test-spec-skeleton.md` | Added input identity, validation-command, and milestone proof-map sections. | Ensure authors start from the required proof-contract structure. | R13-R20, R22 | `python scripts/test-skill-validator.py -k test_spec`; code-review-m1-r1 |
| `skills/test-spec/assets/test-case.md` | Added `Command IDs`, `Evidence artifact`, and `Required by milestone`. | Test cases must reference stable command IDs when commands are involved. | R21, R23 | T13; `python scripts/test-skill-validator.py -k test_spec_proof_contract` |
| `skills/test-spec/assets/validation-command-row.md` | Added repeated structure for command ledger rows. | Package the row authors must copy for command ID, classification, owner, milestone, failure, zero-test, evidence, and side-effect fields. | R1-R12, R24 | T1-T7; `python scripts/validate-skills.py` |
| `skills/test-spec/assets/milestone-proof-row.md` | Added repeated structure for milestone proof-map rows. | Package the row authors must copy for milestone proof timing and evidence. | R15-R20, R25 | T8, T12; `python scripts/validate-skills.py` |
| `scripts/skill_validation.py` | Added `validate_test_spec_proof_contract_fixture` and closed command classification checks; aligned the allowed `test-spec` asset inventory. | Provide deterministic representative validation without enforcing all historical test specs. | R27, R33, R34 | `python scripts/test-skill-validator.py -k test_spec_proof_contract` |
| `scripts/test-skill-validator.py` | Added positive and negative representative fixtures, including valid `ci-owned` and `release-owned` command rows after review. | Prove command ledger, missing ledger, missing/unknown classification, planned metadata, milestone-map, raw-command, and command-free cases. | T1-T14, TSP-M2-CR1 | code-review-m2-r2 |
| `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/behavior-preservation.md` | Added behavior-preservation matrix for role, status model, review route, Manual QA behavior, no manual-proof asset, generated output, and historical migration boundary. | Prove protected behavior after generated-output checks. | R27-R32, R35, R36; T15-T18 | code-review-m3-r1 |
| `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml` | Recorded artifact paths, validation evidence, review outcomes, and material finding closeout. | Keep change-local metadata synchronized with lifecycle evidence. | Workflow contract | `python scripts/validate-change-metadata.py ...` |
| `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/review-log.md` and `review-resolution.md` | Recorded all formal reviews and closed the single material finding, `TSP-M2-CR1`. | Preserve durable review and resolution evidence. | Review workflow rules | `python scripts/validate-review-artifacts.py --mode structure ...` |
| `docs/changes/.../reviews/*.md` | Added review receipts for proposal, spec, plan, test-spec, and implementation milestones. | Prove lifecycle gates ran and show no remaining material findings. | Workflow contract | code-review-m3-r1 |
| `docs/plans/2026-07-04-test-spec-proof-contract-upgrade.md` and `docs/plan.md` | Tracked milestone progress, validation notes, review state, and handoff from implementation through code review to explain-change. | Keep the active plan as the owner of current lifecycle state. | Plan workflow rules | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` |
| `specs/test-spec-proof-contract-upgrade.md` and `.test.md` | Recorded the approved behavior contract and proof map for this upgrade. | Provide the governing requirements and test IDs used by implementation and review. | Proposal and reviews | `spec-review-r1`, `test-spec-review-r1` |

## Tests Added Or Changed

| Test ID | What it proves | Level | Evidence |
| --- | --- | --- | --- |
| T1-T3 | Skill and assets include the validation-command ledger, command IDs, and closed classifications. | contract/unit | `validate-skills.py`, `test-skill-validator.py -k test_spec` |
| T4 | The closed classification enum includes `ci-owned` and `release-owned`. | unit | M2 review fix added direct positive fixture rows for both. |
| T5-T7 | Planned commands require owner/milestone metadata, zero-test behavior, and side-effect boundaries. | unit | `test_spec_proof_contract` negative fixtures |
| T8 | Milestone proof-map section and row asset exist. | contract | M1 asset validation |
| T9-T13 | Representative negative fixtures fail for missing ledger, missing/unknown classification, incomplete planned command metadata, missing milestone map, and raw command without Command ID. | unit | `python scripts/test-skill-validator.py -k test_spec_proof_contract` |
| T14 | A trivial non-milestone command-free test spec still passes with explicit rationale. | integration | `python scripts/test-skill-validator.py -k test_spec_proof_contract` |
| T15-T16 | Manual-proof asset remains absent, Manual QA behavior remains unchanged, status model and review route are preserved. | contract | `behavior-preservation.md`; `validate-skills.py` |
| T17 | Generated skills and adapter checks include the revised skill and assets. | smoke | `build-skills.py --check`, `test-build-skills.py`, `test-adapter-distribution.py` |
| T18 | Historical test specs are not automatically migrated. | migration | M3 changed-file review and `behavior-preservation.md` |

Representative validation was the appropriate level because the approved proposal explicitly chose targeted proof-contract fixtures first and deferred any full test-spec artifact validator until future drift proves it necessary.

## Validation Evidence Available Before Final Verify

Commands recorded as passing during implementation and review:

- `python scripts/validate-skills.py skills/test-spec/SKILL.md`
- `python scripts/test-skill-validator.py -k test_spec`
- `python scripts/test-skill-validator.py -k test_spec_proof_contract`
- `python scripts/build-skills.py --check`
- `python scripts/test-build-skills.py`
- `python scripts/test-adapter-distribution.py`
- `python scripts/validate-skills.py`
- `python scripts/validate-change-metadata.py docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml`
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-04-test-spec-proof-contract-upgrade`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/test-spec-proof-contract-upgrade.md --path specs/test-spec-proof-contract-upgrade.test.md --path docs/plans/2026-07-04-test-spec-proof-contract-upgrade.md --path docs/plan.md --path docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml --path docs/changes/2026-07-04-test-spec-proof-contract-upgrade/behavior-preservation.md`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/test-spec-proof-contract-upgrade.md --path specs/test-spec-proof-contract-upgrade.test.md --path docs/plans/2026-07-04-test-spec-proof-contract-upgrade.md --path docs/plan.md --path docs/changes/2026-07-04-test-spec-proof-contract-upgrade/change.yaml --path docs/changes/2026-07-04-test-spec-proof-contract-upgrade/behavior-preservation.md --path docs/changes/2026-07-04-test-spec-proof-contract-upgrade/reviews/code-review-m3-r1.md`
- `git diff --check 82c7c049..HEAD`

Hosted CI status is not claimed. Final `verify` has not run.

## Review Resolution Summary

Formal review evidence is recorded in `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/review-log.md`.

Review-resolution closeout is recorded in `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/review-resolution.md`.

Summary:

- Material findings: 1
- Accepted and resolved: 1
- Open findings: 0
- `needs-decision`: 0

The only material finding was `TSP-M2-CR1`, which found that the representative valid fixture did not directly prove `ci-owned` and `release-owned` command classifications. The resolution added both command classifications to the positive fixture, mapped them through command IDs, and reran the targeted validator suite. `code-review-m2-r2` and `code-review-m3-r1` recorded no material findings.

## Alternatives Rejected

| Alternative | Why rejected |
| --- | --- |
| Add manual-proof contracts now. | R28 and R29 keep manual-proof contracts out of scope and preserve existing Manual QA checklist behavior. |
| Make the command ledger mandatory for every test spec with no exception. | The accepted decision requires it when commands are named or depended on, while allowing explicit no-command rationale for command-free specs. |
| Require milestone proof maps for every test spec. | The accepted decision requires milestone proof maps for milestone-based plans and allows not-applicable rationale for one-shot or small changes. |
| Execute validation commands during `test-spec` authoring. | The approved behavior is to inspect known manifests/scripts when feasible but not execute commands during authoring. |
| Build a full semantic validator for all future or historical test specs in this slice. | R33 and R34 call for representative fixture validation first; historical migration and broad enforcement are out of scope. |
| Hand-edit generated public adapter package output. | Generated output must remain reproducible from canonical sources and repository-owned scripts. |

## Scope Control

The change stays inside the approved scope:

- no `skills/test-spec/assets/manual-proof.md`;
- no manual-proof contract requirements;
- no automatic migration of historical test specs;
- no change to the `test-spec` status model;
- no replacement of `test-spec-review`;
- no claim by `test-spec` of implementation completion, validation success, branch readiness, PR readiness, or verification;
- no release publication, network, destructive, or external-state commands.

## Risks And Follow-Ups

Remaining risk before PR handoff:

- Final `verify` still needs to check artifact-code-test coherence and lifecycle state after this explanation is committed.
- This change intentionally starts with representative fixture validation. If future generated test specs still drift from the proof contract, a full artifact validator remains the follow-up path identified by the proposal.
- Branch-level PR readiness is not claimed here; `verify` and `pr` own those later claims.

## Current Handoff

All implementation milestones are closed, the durable explanation is recorded, and the active plan's next stage is `verify`.
