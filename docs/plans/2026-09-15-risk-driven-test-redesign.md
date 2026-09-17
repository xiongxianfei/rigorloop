# Risk-driven test redesign delivery plan

## Purpose / big picture

Improve failure detection and maintainability by refactoring oversized fixtures, mixed observation boundaries and weak assertions while retaining the owner-oriented layout and existing Python unittest/Node infrastructure. Begin with a bounded Skill pilot, then Packaging, Release and Selection. Preserve required product proof and independently assess replacement protection before relying on any reduction.

## Current Handoff Summary

No governed change record is selected. This is a portable plan authorized by the user's request to proceed with delivery planning. It does not initialize lifecycle state or authorize implementation. Stage evidence belongs in the existing [refinement evidence](../changes/2026-09-14-design-suitability-review/contract-refinement.md) and associated reviews; current results do not belong in this plan.

## Source artifacts

- Direction: the user's concrete test-redesign proposal, captured in the scope, milestones and preservation rules below; no separate proposal artifact is selected.
- Design: [Validation](../design/engineering/validation.md), especially TEST-SR-01–10/15/16/18, VAL-SR-01/02/11/12/14/15/17–22 and VAL-DEC-09.
- Design assessment: [risk-driven testing Design Review](../changes/2026-09-14-design-suitability-review/reviews/risk-driven-test-design-review.md). Its exact Validation subject is `sha256:200d5859395b87e7999e152f44c7d77a1da7d21d85ba028349f4fdd5eb70ed14`. Later planning authorization comes from the user; this review itself grants no downstream execution permission.
- Retained owners: [Packaging](../design/engineering/packaging.md), [Release](../design/engineering/release/release.md), [Installation](../design/cli/installation.md), [Skill](../design/skill/skill.md) and [Assessment](../design/skill/assessment.md).
- Execution: [CONTRIBUTING](../../CONTRIBUTING.md#validation-scope), the existing selector, executor and suite entrypoints.
- Prior-contract test spec: none. Earlier test/tooling organization plans retain their own scope and are not overwritten or reapproved.

## Context and orientation

Repository tooling tests live in `tests/skill/` and `tests/engineering/{packaging,release,validation}/`; Node tests remain in `packages/rigorloop/test/`. Operational commands live in `scripts/`, with internal implementation under `scripts/lib/`. Inspect these sources directly for this change; the project map is orientation only and does not establish current case discovery or dependency closure.

The supplied archive analysis is a lead, not executed repository evidence: its 934 method declarations exclude generated subcases, imported duplicate discovery and omitted Node tests. The checkout contains package sources missing from the archive. The separately mentioned six-case prototype is not a required input or assumed replacement. Implementation derives fixtures from the actual validator and governing contracts.

Preserve supported aggregate entrypoints and existing TestCase/method selectors during pure module moves. Introduce internal modules only for the group being refactored, following existing release imports or the standard unittest loader. Splitting a multi-fault case may deliberately replace its selector: account for its original detection and partitions in group-level evidence, update every actual consumer, and establish assessed replacements before removing it. Do not keep aliases that cause duplicate execution just to preserve a count.

Every milestone includes its helper imports, copied repositories, direct callers, selection/catalog consumers and normal-loader discovery. Capture actual before/after identities and generated partitions using the existing loader; static declarations alone are insufficient. Required cases must remain reachable once per intended scope, including individual execution and the shared worker budget. Unknown contribution is retained for investigation. Boundary-specific rejection proof observes intended diagnostics at component level and required prohibited effects at the public boundary.

## Non-goals

- No framework migration, new runner or executor, new test lifecycle, per-case ledger, directory taxonomy or deletion quota.
- No semantic-quality automation gate, skill prose rewrite, behavior retirement, new package/release policy or publication.
- No cross-invocation validation cache, shared writable candidate, speed threshold or unmeasured performance claim.
- No unrelated cleanup of the dirty branch, user archive or earlier initiatives.

## Requirements covered

| Requirement or explicit obligation | Allocation and proof |
| --- | --- |
| TEST-SR-01–05/18: meaningful boundary, fixture and oracle | M1–M4; TG-1–4; TG-FINAL-1 |
| TEST-SR-07–10: preservation, replacement and consumers | Every milestone; before/after group rationale and discovery proof; TG-FINAL-1 |
| TEST-SR-15/16: proportional allocation and semantic limits | M1/TG-1; no keyword-based adequacy claim |
| VAL-SR-01/02/17/21/22: independent cases and resource isolation | M1–M4; individual and concurrent execution; TG-FINAL-1 |
| VAL-SR-11/12/14/15/18–20: fresh execution, complete callers, gates and truthful evidence | M1–M4 consumer checks, M4/TG-4 and TG-FINAL-1 |
| DIST-SR-03–06/09/17/18: resource closure, identity and actual installation | M2/TG-2 and TG-FINAL-1 |
| Release approval, candidate and evidence contracts; REL-SR-12–15 | M3/TG-3: binding, rejection, retry and persistence; real public obligations remain owned by Release |
| Existing command/default compatibility | M3/TG-3 if internal import coupling changes; no new public behavior |

## Milestones

### M1. Skill recording-reference pilot

- Milestone kind: implementation.
- Engineering purpose: establish the method on one bounded group before expanding fixture refactors.
- Requirements: TEST-SR-01–05/07–10/15/16/18; VAL-SR-01/02/14/17/21/22.
- Architecture responsibility: Skill structural validation versus semantic Assessment; Validation Criteria and discovery.
- Dependencies: reviewed delivery package and implementation authorization; inspect the actual starting tree and preserve unrelated edits.
- Implementation scope: refactor `ExplicitRecordingGuidanceTests.test_targeted_pilot_reference_selection_and_failures`; assess the bounded semantic-checklist assertion and target-runtime-dependency check. Extract only the relevant contract/CLI/guidance groups, not every Skill class.
- Files/components likely touched: `tests/skill/test-skill-validator.py`, justified `skill_contract_tests.py`, `skill_cli_tests.py`, `skill_guidance_tests.py`, existing consumer expectations and selector paths where affected.
- Required verification: TG-1 — both proposal pilot targets accept valid inputs; independent missing-heading, wrong-trigger, missing-token, missing-resource, escaping-resource, undecodable-resource and wrong-selection defects reject for their intended reason. An unrelated complete resource or appended inline copy cannot rescue the missing selected resource. Retain canonical and real-entrypoint coverage, structural acceptance of ambiguous prose, and intentional byte parity.
- Evidence expectations: fresh valid fixtures before mutation; assert each string mutation changes the intended input; bounded seeded violations fail the protecting assertions and restored code passes. Record exact subjects and limits, not a universal mutation score.
- Implementation steps: capture existing case identities; isolate independent faults; distinguish mechanical resource/byte contracts from incidental wording; exercise the real entrypoint with target executables absent and invocation traps where feasible; reconcile discovery and callers in this slice. If a prose assertion's governing purpose remains unclear, retain it for investigation.
- Validation commands: `python tests/skill/test-skill-validator.py ExplicitRecordingGuidanceTests`; `python tests/skill/test-skill-validator.py`; `python tests/engineering/validation/test-select-validation.py`; `bash scripts/ci.sh --mode explicit --path tests/skill --jobs 4`.
- Expected observable result: independent cases diagnose their intended fault, command behavior has actual runtime observations, and the aggregate/selected suite retains all required protection.
- Completion criteria: replacements established and independently assessed; every affected caller reconciled; full affected suite and selected checks pass without missing or duplicate cases.
- Required evidence: group-level before/after protection rationale, seeded-failure observations, discovery comparison, actual command outcomes and subject applicability.
- Review handoff: independent M1 Code Review of test boundaries, prose dispositions and consumer closure before M2.
- Risks: aggregate imports can change IDs or duplicate classes; a minimal fixture may omit the mechanism.
- Rollback/recovery: restore only this slice's fixtures, tests and consumer edits together from its pre-slice snapshot; retain old protection until the replacement is adequate. Do not reset the surrounding dirty tree.

### M2. Packaging fixtures and product proof

- Milestone kind: implementation.
- Engineering purpose: separate transformation faults from expensive current-product builds while retaining actual artifact and installer boundaries.
- Requirements: TEST-SR-01–05/07–10/18; VAL-SR-01/02/14/17/21/22; DIST-SR-03–06/09/17/18.
- Architecture responsibility: Packaging transformation/integrity and Packaging-to-Installation composition.
- Dependencies: M1 and its required review/corrections.
- Implementation scope: audit repeated optional-discovery, proposal-family, targeted-profile and boundary-first builds. Use one/two-skill fixtures for transformation and negative rules; transfer owner-specific guidance assertions to Skill only with equivalent retained detection. Consolidate only demonstrated equivalent current-candidate builds.
- Files/components likely touched: `tests/engineering/packaging/test-adapter-distribution.py`, justified local fixture helpers, affected Skill groups and selection consumers. Keep package-native tests unless a concrete consumer change requires reconciliation.
- Required verification: TG-2 — independent canonical inventory versus real archive members; correct transforms/resources and metadata; missing/stale resources, hash mismatch, traversal and symlink/type hazards; actual packed CLI installation for Codex and Claude, installed bytes, conflict handling, force replacement, unsafe paths and unrelated-state preservation.
- Evidence expectations: retain `test_distribution_archives_have_independent_complete_resource_inventory` and actual local-archive consumer proof. Expected inventories must not call the producer inventory helper. A passing exit alone cannot establish installed content.
- Implementation steps: identify each repeated build's contribution; establish smaller independent fixtures; keep immutable invocation-local candidate input only where useful; give destructive cases private materializations; reconcile all changed source/helper consumers and case identities immediately. Do not assume a class fixture builds once across case processes.
- Validation commands: `python tests/engineering/packaging/test-adapter-distribution.py`; `python tests/engineering/packaging/test-npm-package-publication.py`; `bash scripts/ci.sh --mode explicit --path tests/engineering/packaging --jobs 4`. Include each additionally changed Skill/implementation path in the explicit selection.
- Expected observable result: smaller rules retain fault sensitivity and both actual product paths still establish resource closure, identity and safe installation.
- Completion criteria: full affected suites and required candidate proof pass; reduced builds have assessed equivalent coverage; discovery and isolation remain complete.
- Required evidence: retained/replacement proof per changed group, actual artifacts/installation results, input identities, command results and limitations.
- Review handoff: independent M2 Code Review including composition and any transferred Skill assertions before M3.
- Risks: fixture simplification hides resource closure defects; a shared candidate leaks mutation; build reduction removes a distinct boundary.
- Rollback/recovery: restore affected groups and consumers together; restore separate product scenarios if equivalence fails. Clean only invocation-owned outputs.

### M3. Release fixtures and focused dependencies

- Milestone kind: implementation.
- Engineering purpose: remove TestCase-as-fixture coupling while preserving approval, execution and real persistence proof.
- Requirements: TEST-SR-01–05/07–10/18; VAL-SR-01/02/14/17/21/22; retained Release candidate/approval/evidence behavior and REL-SR-12–15.
- Architecture responsibility: Release policy, orchestration, candidate identity and evidence persistence; existing Packaging defaults.
- Dependencies: M2 and its required review/corrections; inspect all import/default consumers before production edits.
- Implementation scope: retain existing candidate, coordination, evidence and execution modules and `test-release-transaction.py` aggregate. Extract plain reused fixture builders into `release_fixture_helpers.py`; replace construction of another TestCase plus `setUp()` calls. Isolate focused policy imports from repository packaging metadata when justified.
- Files/components likely touched: release test modules and helpers; narrowly justified `scripts/lib/release/` or `scripts/lib/packaging/` imports/default resolution and their consumers.
- Required verification: TG-3 — exact candidate approval; denied approval/tampering cause no external writes; lost npm response does not republish; failed public smoke preserves actual identity and retry observes it; conflicting public identity is not overwritten; concurrent real-Git evidence writers preserve unrelated data and reject stale updates.
- Evidence expectations: real owned orchestration with external-service fakes, separate real temporary Git persistence, retained actual archive/packed-CLI proof. Historical literals remain when their selected profile requires them. No simulated result proves public availability or permission.
- Implementation steps: extract explicit-input builders; preserve independent state; reproduce focused import coupling in a controlled incomplete tree. For any production dependency change, preserve explicit and default version resolution, metadata failure behavior at the owning operation, command outputs and caller semantics; add focused regression proof and run affected Packaging consumers. If this requires a new public behavior/default policy, return that decision to Design instead of expanding this refactor.
- Validation commands: `python tests/engineering/release/test-release-transaction.py ReleaseApprovalTests`; `python tests/engineering/release/test-release-transaction.py`; `bash scripts/ci.sh --mode explicit --path tests/engineering/release --jobs 4`. Add every changed production/default-consumer path to explicit selection; run the M2 packaging suites when their dependency changes.
- Expected observable result: policy fixtures no longer depend on TestCase lifecycle, focused policy can run without unrelated packaging inputs, and all actual publication/persistence safety observations remain intact.
- Completion criteria: focused and full affected suites pass; runtime compatibility changes are explicitly proved; real Git and retry cases remain reachable and independent.
- Required evidence: fixture/default dependency assessment, command results and exact source/test identities. Compare setup/command measurements only if making a speed claim.
- Review handoff: independent M3 Code Review, including production changes and exact evidence applicability, before M4.
- Risks: lazy defaults change evaluation semantics; policy fixtures erase historical distinctions; fake service success overstates proof.
- Rollback/recovery: restore helper/import and consumer edits as one unit; preserve prior safety cases and failed observations. No publication, evidence-history rewrite or external rollback is part of this slice.

### M4. Selection boundaries and complete consumer reconciliation

- Milestone kind: implementation.
- Engineering purpose: separate routing rules, Git discovery and actual CI execution while checking the combined refactor remains reachable.
- Requirements: TEST-SR-01–05/07–10/18; VAL-SR-01/02/11/12/14/15/17–22.
- Architecture responsibility: Validation selection/execution and all renamed/split suite consumers.
- Dependencies: M1–M3 and required reviews/corrections; earlier milestones have already reconciled their own discovery.
- Implementation scope: split `test-select-validation.py` only by useful responsibility, retaining its aggregate and supported selectors. Keep `EXPECTED_CATALOG` independently specified, including security-relevant command arguments. Remove only the second assertion in each of the four verified adjacent identical pairs. Replace sleep-dependent synthetic overlap observations with the existing real-child rendezvous pattern where needed.
- Files/components likely touched: `tests/engineering/validation/test-select-validation.py`, justified adjacent suite/helper modules, `test-validation-execution.py`, catalog/import consumers and copied repositories.
- Required verification: TG-4 — changed/deleted/renamed/helper paths select surviving consumers; direct, aggregate, individual and concurrent execution agree on required cases. Preserve bounded real overlap, duplicate equivalence, changed basis, failed consumer prerequisites despite shared success, fail-fast, nonzero/unstarted reporting and process-tree cleanup.
- Evidence expectations: independent catalog expectations and normal-loader identities, with explained replacements; actual subprocess/CI stream and exit observations; no replacement scheduler or performance-based rendezvous target.
- Implementation steps: capture discovered scope; split imports without duplicate loading; remove four repeated assertions without deleting their tests; refine timing fixtures; exercise actual selectors and all new helper paths; investigate unexpected losses rather than relabeling them optional.
- Validation commands: `python tests/engineering/validation/test-select-validation.py`; `python tests/engineering/validation/test-validation-execution.py`; `bash scripts/ci.sh --mode explicit --path tests/skill --path tests/engineering/packaging --path tests/engineering/release --path tests/engineering/validation --jobs 4`.
- Expected observable result: complete required case scope runs under the existing worker budget; failures remain visible through each supported caller, and no required case moves to an optional-only command.
- Completion criteria: all affected suites and combined selected scope pass; generated/imported case changes and helper triggers are accounted for; no unresolved isolation or protection gap.
- Required evidence: before/after actual discovery, individual/concurrent outcomes, command/phase results, dependency and replacement rationale.
- Review handoff: independent M4 Code Review followed by the distinct final whole-change checkpoint.
- Risks: aggregate imports silently duplicate or omit cases; shell-string cleanup weakens a security contract; sleeps hide scheduler faults.
- Rollback/recovery: restore split modules and selectors together, restore any lost required case, and retain rendezvous diagnostics for timeout failures.

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: all in-scope implementation milestones and required corrections complete.
- Assessment: fresh independent final whole-change Code Review of the entire delivered diff and cross-milestone interactions, not a summary of milestone approvals.
- Evidence: exact final subjects, retained/replacement protection, reviewer independence, judgments and concern dispositions.
- Successor: distinct final Verify; corrections return to their owner and require affected reassessment.

## Change-level verification

### TG-FINAL-1. Complete protective test portfolio and product composition

- Covers: M1–M4; TEST-SR-01–10/15/16/18; VAL-SR-01/02/11/12/14/15/17–22; retained Packaging/Release obligations above.
- Demonstrate: the current canonical skills flow through real archives and packed CLI installation for both targets; release orchestration and real Git evidence retain their independent proof; all changed test groups remain reachable through supported direct, selected and individual execution. Shared helpers/imports cannot silently narrow another owner's coverage or contaminate concurrent cases.
- Evidence expectations: full affected modules after shared dependency changes; final selected execution across the changed surfaces; actual branch selection without unclassified paths; current package-native consumers when selected. Record generated/imported case scope, actual results, subject/environment applicability and mandatory freshness. Discovery alone is not execution. Reuse earlier results only with affirmative unchanged-basis justification under Assessment; do not blindly rerun unchanged expensive proof or use a result cache.
- Non-applicability: cross-milestone proof is required. Live publication and fresh public smoke are not triggered by this test refactor; their tests and Release obligations remain, and simulated results are never reported as a public release.

## Validation plan

Use the milestone commands as the minimum concrete allocation, expanding explicit paths to every actual changed source/helper/consumer. The existing selector supplies required dependencies and triggers; unknown impact requires investigation. For individual replacements, use the existing aggregate command with its actual `TestCase.method` selector and record the exact command in evidence. Compare normal-loader collections through existing `discover_cases`; do not build another registry.

At final implementation integration run `python scripts/select-validation.py --mode local` to inspect the actual branch scope, then `bash scripts/ci.sh --mode local --jobs 4` for required execution. Apply existing broad-smoke triggers when selected; no release publication command belongs here. Existing unrelated dirty work requires explicit applicability and scope explanation, not a claim that it is part of this redesign.

For this plan's documentation use `python scripts/validate-documentation-prose.py --mode enforce --path docs/plans/2026-09-15-risk-driven-test-redesign.md --path docs/plan.md` and `git diff --check`. Mechanical success does not replace Delivery Review.

## Risks and recovery

Preserve a pre-slice source snapshot and discovered scope outside committed product output. Recovery restores only the slice's edits and its consumers, retaining user work and contradictory evidence. Do not use whole-tree reset or delete the supplied archive. Unknown protection, lost reachability or required shared mutable resources prevent the affected milestone from completing. Missing behavioral authority returns to Design; missing proof allocation returns to Plan.

## Dependencies

Delivery Review must assess the exact plan before implementation reliance. Each milestone depends on the preceding milestone's required independent review and corrections. Replacement proof must be established and assessed before reduced-suite reliance. All implementation/corrections precede fresh whole-change Code Review and distinct Verify. Commit, push, PR, merge and publication remain outside this planning invocation.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-15 | Start with the recording-reference pilot and retain owner-oriented suites. | A bounded group establishes fixture/oracle quality before broader changes. | Framework migration, wholesale splitting by line count, deletion quotas. |
| 2026-09-15 | Reconcile discovery inside every slice and assess the combined result in M4. | No intermediate state may silently lose required execution. | Deferring all catalog/import repair until the last milestone. |
| 2026-09-15 | Treat import/default changes as production compatibility work inside M3. | Fixture cleanup cannot silently change caller behavior. | Fabricating package metadata to hide coupling or changing policy for convenience. |

## Readiness

This plan defines stable delivery intent only. Delivery Review owns its assessment; implementation authorization and later evidence are separate. It does not assert tests passed, milestones completed, branch readiness or final verification.
