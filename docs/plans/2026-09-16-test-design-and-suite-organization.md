# Test design adoption and complete suite organization

## Purpose / big picture

Apply the refined Validation Design to the complete test population so contributors can understand, run and maintain each group's protection. Organize mixed responsibilities, make scenario conditions and independent expected results visible, and retain suitable groups. Preserve actual command, filesystem, archive, transaction and recovery observations while changing their test sources.

## Current Handoff Summary

- Owning change record: [test design and suite organization](../changes/2026-09-16-test-design-and-suite-organization/change.json).

Mutable lifecycle state, current milestone state, review status, blockers, routing and closeout readiness live only in this record and its registered records. This plan is stable execution intent, not an assessment or execution report.

## Source artifacts

- Proposal: [refine test design and organize the complete test suite](../proposals/2026-09-16-test-design-and-suite-organization.md).
- Spec: [Validation](../design/engineering/validation.md), particularly TEST-SR-19/20, VAL-SR-32, Test script structure, Complete suite organization and their retained requirements.
- Architecture: Validation's source-composition graph and VAL-DEC-11 within the same model; [System](../design/system.md) retains capability placement. No separate architecture artifact is required.
- Upstream assessment: [Design Review](../changes/2026-09-16-test-design-and-suite-organization/reviews/design-review.json), member `validation`; Delivery Review must inspect its exact current subject and applicability.
- Retained behavior owners: [Skill](../design/skill/skill.md), [CLI](../design/cli/cli.md), [Records](../design/cli/records.md), [Installation](../design/cli/installation.md), [Packaging](../design/engineering/packaging.md) and [Release](../design/engineering/release/release.md). Their existing observations remain required; this plan changes no product behavior.
- Allocation and assessment: [Plan](../design/skill/authoring/plan.md), [Assessment](../design/skill/assessment.md), Constitution and [contributor validation scope](../../CONTRIBUTING.md#validation-scope).
- Prior-contract test spec: none separately applicable. No standalone test specification or permanent case ledger is introduced.

## Context and orientation

The source baseline is `1195dfb261176d500e319662e2ffad5429cb63be`, plus this change's proposal and Validation refinement. Inspect actual sources; project-map currency is not assumed. Python entrypoints live in capability-owned `tests/` directories, Node tests in `packages/rigorloop/test/`, catalog and adapters in `scripts/lib/validation/`, and operational callers in `scripts/` and `.github/workflows/`. Package runtime under `packages/rigorloop/dist/` is an observation subject, not a test source to reorganize.

### Complete population allocation

The table allocates every current authored test module and test-only helper, with recursive fixture and reached-population closure. Paths in the Members column are relative to Root. It identifies scope, not completed protective-value assessment. At each slice, refresh ordinary discovery and inspect imports, generated registration, parameter rows, fixture readers, package scripts, catalog commands and direct/CI/main/broad/release callers. Record additions, renamed identities and justified removals in existing evidence. A new group goes to the owning slice; if it changes a settled slice's order, completion criteria or required evidence, return to Plan and Delivery Review before dependent implementation.

| Allocation | Root | Members and responsibility |
| --- | --- | --- |
| M1 | `tests/skill/` | `SkillValidatorFixtureTests` in `test-skill-validator.py`, including inherited `SkillCliChecks` from `skill_cli_tests.py` and `SkillGuidanceChecks` from `skill_guidance_tests.py`; its constants and fixture methods. Assess every method and named subtest, then separate metadata/readability, resource-map/assets, portable input, installed placement and canonical-guidance responsibilities. |
| M2 | `tests/skill/` | Every remaining class in `test-skill-validator.py`; `skill_contract_tests.py`; `ExplicitRecordingGuidanceTests` in `skill_guidance_tests.py`; `review_independence_skill_phrases.py`. These own recording resources, skill-specific and cross-skill guidance, parity and retained retirement protection. M2 reconciles any support shared with M1. |
| M1–M2 | `tests/fixtures/skills/` | All recursive valid/invalid skill packages, nested assets/references/scripts and generated-output examples. M1 owns readers used by its scenarios; M2 owns the remainder. Shared fixture changes require both consumer groups' proof. Fixture-contained `check.py` and `validate_output.py` are packaged-script inputs, not additional test entrypoints. |
| M3 | `tests/engineering/validation/` | `test-boundary-first-reference.py`, `test-boundary-first-validation.py`, `test-change-metadata-validator.py`, `test-documentation-prose-validator.py`, `test-governed-lifecycle-cli-validator.py`, `test-guide-system-validator.py`, `test-markdown-readability-validator.py`; recursive `fixtures/boundary-first/`. |
| M3 | `tests/fixtures/documentation-prose/` | All recursive pass/fail/warning inputs and any actual readers outside the document suite. |
| M4 | `tests/engineering/validation/` | `test-select-validation.py`, `selection_contract_tests.py`, `selection_git_tests.py`, `selection_cli_tests.py`, `selection_test_helpers.py`, `test-validation-execution.py`; generated Python/Node child-suite strings, copied repositories and all imported or inherited cases. |
| M5 | `tests/engineering/packaging/` | `test-adapter-distribution.py`, `test-npm-package-publication.py`; transformations, manifests, integrity, real archives, packed CLI and installation observations. |
| M5 | `tests/fixtures/adapters/` | All recursive input packages, target-specific examples and transitive resources; reconcile Skill consumers of shared package inputs in the same slice. |
| M6 | `tests/engineering/release/` | `test-release-transaction.py`, `release_candidate_tests.py`, `release_coordination_tests.py`, `release_evidence_tests.py`, `release_execution_tests.py`, `release_fixture_helpers.py`; inline providers, prepared repositories and generated inputs. |
| M6 | `tests/fixtures/release-transaction/` | All profiles, surface inventories, literal-audit inputs and `current-version.json`. The last is also release-generated operational data: preserve its current path and writer contract rather than treating it as an exclusively test-owned fixture. |
| M7 | `packages/rigorloop/test/` | `record-retirement.test.js`; every current `record-store-*.test.js`: adoption, cli, contract, format, interactions, model-examples, persistence, queries, targeted, v3-adoption, v3-contract, v3-mutations, v3-persistence, v3-reads and workflow. |
| M7 | `packages/rigorloop/test/` | `helpers/record-store-launcher.mjs`, `helpers/recording-query-launcher.mjs`, `helpers/record-store-interactions.mjs`, `helpers/v3-fixture.mjs`, `fixtures/recording-interactions/README.md`; include generated scenarios and public fault-injection subprocesses. |
| M3/M4/M7/M8 | `tests/fixtures/rigorloop-records-v3/` | `records.json`, `storage-safety.json` and their transitive consumers. M7 owns package fixture organization; the earliest changing slice owns reconciliation with all current Python and Node readers. Do not relocate a shared root based only on its directory name. |
| M8 | `packages/rigorloop/test/` | `cli.test.js`, `installer-replacement.test.js`, `cli-observability.test.js`, `cli-invocation-observability.test.js`, `result-renderer.test.js`, `workflow-context.test.js`, `fixtures/observability/public-command-output.json`; CLI/installation, rendering, logging and workflow-context populations. |
| Every owning slice; final reconciliation in M8 | Repository and package callers | `scripts/ci.sh`, `scripts/select-validation.py`, `scripts/lib/validation/validation_selection.py`, `validation_execution.py`, `validation_node_adapter.mjs`, package `test` command, `.github/workflows/{ci,release,publish-github-packages}.yml`, release qualification/preparation readers and direct test commands. Include any additional reached source, generated family or helper outside the listed roots; do not silently omit it. |

### Reconcile earlier work

| Earlier allocation | Current source fact and treatment in this plan |
| --- | --- |
| [Directory organization](2026-09-14-validation-test-organization.md) | Capability test roots and imported release groups exist. Retain those locations; assess group quality and actual reachability under M1–M8. Shared fixtures remain where their consumers justify them. Do not repeat directory moves or rewrite the earlier evidence. |
| [Risk-driven redesign](2026-09-15-risk-driven-test-redesign.md) | Recording-reference contract/CLI/guidance modules, selector contract/Git/CLI modules, independent archive observations and `release_fixture_helpers.py` exist. M1/M2 assess the remaining Skill population; M4 preserves the selector split while assessing fixtures/hooks; M5/M6 retain useful archive and release proof. The earlier bounded pilot is not complete-population authority. |
| [Complete skill/support refinement](2026-09-15-refine-skills-and-retire-stale-support.md) | The current checkout has no `scripts/query-change-record.py` or `test-query-change-record.py`; current selector/retirement proof remains an M3/M4/M7 concern. That initiative's skill edits, production-support retirement and broader script audit keep their owner. This initiative assesses all tests and necessary consumers without repeating an absent shim deletion or claiming that initiative complete. |

These facts guide allocation, not inherited approval. Reconcile later overlapping changes against the actual starting tree, retain their history and assess evidence applicability before reuse.

### Common slice method

Each milestone first establishes the actual starting population through C1 below and the source/caller inspection in its allocation. Record coherent groups with governing obligation, intended failure, observation boundary, members/generated families, fixtures/helpers, consumers and a retain/strengthen/consolidate/replace/remove disposition. Explicitly distinguish retained assertions with new placement from improved failure sensitivity. Unknown protection remains present and blocks that group's completion.

Use ordinary functions for fresh fixture data, direct test classes or native Node groups for scenarios, and resource objects only for a real owned lifecycle. A source file can contain several small related roles. Keep supported aggregate filenames. Preserve case selectors on pure moves; intentional class/method/name changes require before/after mappings, meaningful parameter preservation and consumer updates. Do not add discovery aliases that execute a case twice. Existing compatibility mixins may remain with explicit consumer, hook and discovery rationale; they are not the default structure for new groups.

Keep expected outcomes independent of the operation under assessment and faults visible in their cases. New shared mutable inputs must be independently materialized, cleanup registered at acquisition, environment/cwd explicit and resources private. Assess every group in a slice, including unchanged ones; suitable groups need a reasoned retain disposition rather than a rewrite. Before consolidation/removal, establish replacement detection or cite an already explicit behavior-owner retirement, then obtain independent assessment before relying on the reduced population. No newly selected product retirement is authorized.

Every slice reconciles imports, helper/fixture consumers, copied test repositories, catalog arguments and safety bases, path selection, direct/package/CI callers and rerun instructions. Do not blindly refresh a command fingerprint after a move: recheck its observed boundary, hook isolation and nested demand. An actual shared-policy conflict returns to its canonical owner with same-slice generation/validation where applicable; concrete repository structure alone does not require portable skill changes. Production defects discovered during the audit receive bounded correction ownership and any required Design/replan; they are not silently folded into fixture extraction.

## Non-goals

- No new framework, runner, result cache, semantic scoring gate, permanent ledger, file-size rule or test-count target.
- No forced rewrite of suitable groups, universal inheritance hierarchy or generic shared utilities layer.
- No new product behavior, runtime interface, release policy, current installation change or external publication.
- No rewrite of historical plans/reviews, unrelated branch cleanup or automatic completion of overlapping initiatives.

## Requirements covered

| Requirement or retained obligation | Architecture responsibility, allocation and proof |
| --- | --- |
| TEST-SR-19/20; VAL-SR-32 | Behavior modules, scenario/support composition and complete inventory: M1–M8, TG-01–08 and TG-FINAL-01. |
| TEST-SR-01–06/18 | Contract-derived cases, meaningful partitions and independent oracles: every changed/retained group in M1–M8; preserve generated domains and reproduction data where present. |
| TEST-SR-07–10/12/14/17 | Protection-preserving maintenance, fixture ownership and caller closure: common slice method, every milestone and TG-FINAL-01/02. Earlier specific retirement maps are retained context, not new deletion authority. |
| TEST-SR-11/15/16 | Proportionate automated/manual evidence and semantic limits: every independent milestone review; M2 instruction assessment; distinct final whole-change review and Verify. |
| TEST-SR-13; VAL-SR-16 | Contributor adoption and canonical consumer reconciliation: M1 navigation and each affected slice. No new portable criterion is selected; any actual conflict must be reconciled through its owner and applicable generated consumers. |
| VAL-SR-01/02/17/21/22 | Private mutable state, lifecycle ownership and independent execution: every slice; TG-04 checks the runner boundary and TG-FINAL-02 integrates callers. Temporary unknown-safety serial fallback is not completed adoption. |
| VAL-SR-03–10/12/14/15/19/20/27 | Selection, normal discovery, supported filters, worker budgets, failure/timeout/cleanup, deduplication and truthful reruns: M4/TG-04 plus same-slice consumers and TG-FINAL-02. |
| VAL-SR-11/18 | Real execution without result caching and bounded claims: all evidence; no performance improvement is promised. |
| VAL-SR-28 and existing document/reference contracts | Retained current-model/reference/record/prose validation: M3/TG-03. |
| Existing Skill structure/resource/portability obligations | M1/TG-01 and M2/TG-02, at structural, canonical and required real command boundaries. |
| Packaging DIST-SR-03–06/09/17/18; Installation DIST-SR-02/07/08/10–16 | M5/TG-05 and M8/TG-08 preserve actual archives, bundled identity, packed command invocation, containment, destination conflicts and replacement effects. |
| Release profile, candidate, approval, retry and evidence contracts, including REL-SR-12–15/22–24 | M6/TG-06 retains owned orchestration, real local persistence and denied/uncertain-publication observations; fixtures grant no public result or permission. |
| CLI-SR-01–13 and retained Records format/query/targeted mutation obligations | M7/TG-07 preserves actual dispatch, exact bytes, conflict, containment, interruption and recovery; M8/TG-08 preserves observation and workflow-context surfaces. |

VAL-SR-13/23–26/29–31 retain the scopes of their named earlier initiatives. This plan carries their still-required current negative protection through the owning groups; it neither reopens completed retirements nor treats earlier full-inventory judgments as approval of VAL-SR-32.

## Milestones

### M1. Separate the mixed Skill validator group

- Milestone kind: implementation.
- Engineering purpose: establish the common method on the oversized mixed class while leaving other classes reachable through the existing aggregate.
- Requirements: TEST-SR-01–10/12/17–20; VAL-SR-01/02/14/17/32.
- Architecture responsibility: Skill input/resource validation and Validation source composition.
- Dependencies: independent Delivery Review of this exact plan and authorized implementation; current starting population and source snapshot.
- Implementation scope: all M1 members, including the primary class's canonical-guidance methods and inherited cases. Extract cohesive metadata/readability, resource/asset, portable-input and installed-placement groups; give canonical-guidance cases an explicit owner. Reuse/extract only relevant fresh factories and command helpers. Link CONTRIBUTING to the refined authoring sections without duplicating policy.
- Files/components likely touched: `tests/skill/test-skill-validator.py`, its CLI/guidance modules, adjacent behavior/support modules, relevant skill fixtures, contributor link and actual selector/copied-repository consumers.
- Required verification: TG-01 — valid controlled inputs succeed; missing/unknown metadata, wrong resource class, missing/escaped resource, asset mismatch and invalid placement fail for the intended reason. Real CLI cases retain exit/stream/no-unwanted-write observations; no fixture mutation is a no-op.
- Evidence expectations: normal before/after identities and parameter mapping, independent expected-result rationale, cleanup/isolation basis and focused negative detection. Whole Skill suite proof detects effects on still-unmoved M2 classes.
- Implementation steps: assess all M1 groups; extract with minimal dependency direction; strengthen demonstrated weak fixtures/assertions; reconcile supported selectors/imports/consumers; update navigation; perform common slice proof.
- Validation commands: C1; `python tests/skill/test-skill-validator.py`; `python tests/engineering/validation/test-select-validation.py`; C2 for every changed file, including fixtures and CONTRIBUTING.
- Expected observable result: a contributor can locate and run each protected behavior without navigating unrelated scenario bodies; existing aggregate scope remains complete.
- Completion criteria: all M1 groups have supported dispositions; no missing/duplicate or unexplained renamed case/parameter; required direct, individual and selected proof passes; shared consumers remain covered.
- Required evidence: `m1-implementation` and `m1-validation` with exact subjects, actual commands, dispositions and limitations.
- Review handoff: independent M1 Code Review of source responsibilities, negative detection, discovery and consumer closure before M2.
- Risks: inherited cases disappear during extraction; a large generic helper hides the fault or changes the oracle.
- Rollback/recovery: restore the affected scenario/helper/entrypoint/consumer unit from its pre-slice snapshot; keep M2 and unrelated work intact and preserve failed evidence.

### M2. Organize remaining Skill contract and guidance tests

- Milestone kind: implementation.
- Engineering purpose: complete Skill assessment after M1 exposes the reusable local support and aggregate boundary.
- Requirements: TEST-SR-01–05/07–13/15–20; VAL-SR-01/02/14/17/32.
- Architecture responsibility: skill-specific contracts, cross-skill resources and semantic Assessment boundaries.
- Dependencies: M1 review and corrections; refreshed complete Skill discovery.
- Implementation scope: every M2 class/helper/fixture, retaining the recording-reference pilot when adequate. Group by current obligation rather than historical milestone; separate cross-skill shared-resource checks from per-skill cases. Preserve distinct structural and real command protection while documenting limits of wording checks.
- Files/components likely touched: remaining `test-skill-validator.py` bodies, `skill_contract_tests.py`, `skill_guidance_tests.py`, phrase helper, relevant fixtures and newly justified local modules/consumers.
- Required verification: TG-02 — missing/wrong/incomplete/unreadable/escaped selected recording resources reject; unrelated complete resources cannot rescue the selected fault; actual canonical resources and required parity remain covered. Equivalent wording is not presented as an executable semantic verdict.
- Evidence expectations: all remaining Skill dispositions, exact structural obligations for retained phrases, fresh fixtures for meaningful variants, independent inspection of semantic claims and complete shared-consumer proof after M1 support changes.
- Implementation steps: assess each remaining class and subtest family; retain useful pilot structure; move cohesive groups; replace or remove assertions only after established protection; reconcile the complete aggregate and shared constants.
- Validation commands: C1; `python tests/skill/test-skill-validator.py`; `python scripts/validate-skills.py skills`; C2 for all affected paths; rerun affected M1 proof after shared changes.
- Expected observable result: the aggregate exposes complete current Skill groups and each changed scenario has understandable conditions, actions and outcomes.
- Completion criteria: all Skill groups/fixtures have dispositions, uncertain protection is resolved, required proof passes and no instruction-quality claim exceeds its evidence.
- Required evidence: `m2-implementation`, `m2-validation`, and bounded author/reviewer observations of any semantic assertion disposition.
- Review handoff: independent M2 Code Review of the remaining population and M1/M2 interactions before M3.
- Risks: obsolete names are mistaken for obsolete behavior; phrase deletion removes a real structural contract.
- Rollback/recovery: restore affected assertions and fixture/consumer changes until retained protection is established; return missing behavioral authority to Design.

### M3. Assess document, reference and record-validation suites

- Milestone kind: implementation.
- Engineering purpose: assess the independent grammar/reference groups before changing selector/executor fixtures that call them.
- Requirements: TEST-SR-01–10/12/17–20; VAL-SR-01/02/14/17/28/32.
- Architecture responsibility: Validation domain validators and their direct command wrappers.
- Dependencies: M2 review and corrections; current fixture readers, including shared record fixtures, identified.
- Implementation scope: all seven M3 suites and their fixtures. Retain small coherent groups; separate mixed structural/reference/command setup only where needed. Preserve current versus historical classification, missing/unknown input rejection and exact committed-record snapshot observations.
- Files/components likely touched: listed M3 sources, local helpers when justified, boundary/prose fixtures, shared record fixture consumers and catalog routing for new modules.
- Required verification: TG-03 — valid supported models/records pass, missing/unsafe references and malformed/unknown current records reject, absent historical data cannot hide malformed current input, and prose/structural checks report their actual limited scope.
- Evidence expectations: group-level retained or changed rationale; meaningful valid/invalid controls, real filesystem/Git/command boundaries where required; downstream M4/M7/M8 consumers checked for shared fixture changes.
- Implementation steps: inventory groups and generated input variants; assess their obligations; apply only necessary organization/fixture/oracle changes; reconcile shared readers and changed-path selection.
- Validation commands: C1; direct `python tests/engineering/validation/FILE` for each of the seven exact M3 filenames in the allocation; C2 for changed source/fixture/consumer paths. This allocation requires those suites' proof, not merely a passing filename scan.
- Expected observable result: each grammar/reference group remains directly and individually runnable with its distinct accepted/rejected observations.
- Completion criteria: all M3 groups and fixture variants accounted for; required proof passes; no unowned shared-fixture impact.
- Required evidence: `m3-implementation`, `m3-validation`, discovery/parameter comparison and shared-consumer rationale.
- Review handoff: independent M3 Code Review including retained groups and negative observations before M4.
- Risks: oversimplified fixtures mask a different rejection; copied repositories omit new helpers.
- Rollback/recovery: restore fixture, consuming suites and copy/routing lists together; retain the original negative reproduction until the replacement is adequate.

### M4. Refine selector and executor test organization

- Milestone kind: implementation.
- Engineering purpose: preserve the execution machinery's own proof and establish reliable integration for all later suite moves.
- Requirements: TEST-SR-01–10/12/17–20; VAL-SR-01–12/14/15/17/19–22/27/32.
- Architecture responsibility: catalog/selection, Python and Node collection, subprocess execution and reporting.
- Dependencies: M3 review/corrections; all earlier new helper paths already reconciled in their owning slices.
- Implementation scope: all M4 modules and embedded generated child suites. Retain the contract/Git/CLI distinction, assess existing compatibility mixins and reduce hidden fixture coupling using explicit composition when useful. Preserve independent expected catalog definitions, real process overlap, worker budgeting and required direct CI probes.
- Files/components likely touched: selector/executor tests and helpers, copied-tree inputs, catalog path rules/command bases and `.github/workflows/ci.yml` only if a referenced selector changes. No new executor behavior is selected.
- Required verification: TG-04 — added/deleted/renamed/helper paths reach surviving checks; unknown routing never becomes partial success; ordinary and isolated discovery preserve hooks and named Python/Node populations; requested filters run the intended case. Preserve jobs=1 coverage, bounded real overlap, nested allocation, deduplication, failed prerequisites, fail-fast/unstarted reporting, timeout/interrupt cleanup and actionable reruns.
- Evidence expectations: actual subprocess outcomes and controlled rendezvous, not sleep duration as success; complete selector/adapter population mapping; owned-child and resource isolation basis. Negative observation must remain nonzero through the public wrapper.
- Implementation steps: assess all M4 cases/families; refine support and group boundaries; preserve explicit catalog expectations; reconcile helper selection and actual CI probe selectors; run direct and selected execution.
- Validation commands: C1; `python tests/engineering/validation/test-select-validation.py`; `python tests/engineering/validation/test-validation-execution.py`; C3; C2 for actual M4 paths and shared changes.
- Expected observable result: test source changes remain reachable through each declared caller and execution still reports failures and unfinished work truthfully.
- Completion criteria: all M4 groups assessed; direct, individual and bounded execution agree on intended population; real overlap and failure/cleanup proof passes; no unknown isolation remains in completed scope.
- Required evidence: `m4-implementation`, `m4-validation`, explicit compatibility/mixin or replacement rationale, actual emitted rerun verification and nested-budget observations.
- Review handoff: independent M4 Code Review of discovery, wrapper boundaries and cross-slice fixture dependencies before M5.
- Risks: self-derived catalog expectations; test imports perform work; synthetic adapters miss normal-loader behavior.
- Rollback/recovery: restore the source/helper/catalog/caller unit, including former selectors where needed; preserve failed child diagnostics and restore any lost required cases.

### M5. Organize packaging transformation and product proof

- Milestone kind: implementation.
- Engineering purpose: separate bounded transformations from actual artifacts without losing archive and packed-consumer observations.
- Requirements: TEST-SR-01–10/12/17–20; VAL-SR-01/02/14/15/17/32; retained Packaging and Installation requirements in the allocation.
- Architecture responsibility: adapter transforms/inventory, actual archives and packed CLI consumers.
- Dependencies: M4 review/corrections; current canonical Skill sources and packaging fixture consumers identified.
- Implementation scope: all M5 suites and fixtures. Extract cohesive transformation, resource/integrity, command and actual-artifact groups as needed; retain the two supported aggregate entrypoints. Keep independently justified archive membership rather than using producer inventory as its own expected result.
- Files/components likely touched: packaging suites and local support, adapter fixtures, exact catalog subset selectors and publication-workflow test callers. Generated output is produced privately, never hand-authored.
- Required verification: TG-05 — correct target transforms and unknown-target rejection; missing/stale/unexpected/unsafe resource failures; both actual supported archives contain the canonical resource closure under declared transformations; real npm tarball contents and packed binary installs remain observed. A fake non-installing consumer must not pass installation proof.
- Evidence expectations: independent expected inventory, actual archive/tarball inspection, private clean target roots and supported negative partitions; separate transform-level proof from actual product proof.
- Implementation steps: assess every transformation and integration group; extract only cohesive support; reconcile catalog subset arguments and callers; establish changed negative proof before consolidation; execute complete affected artifact observations.
- Validation commands: C1; `python tests/engineering/packaging/test-adapter-distribution.py`; `python tests/engineering/packaging/test-npm-package-publication.py`; C2 for all affected paths.
- Expected observable result: contributors can distinguish transformation, integrity and consumer scenarios, with actual packaging/install protection preserved.
- Completion criteria: every M5 group/fixture has a disposition; actual archive and packed-consumer proof passes; supported subset selections discover their intended cases exactly once.
- Required evidence: `m5-implementation`, `m5-validation`, artifact-boundary and replacement-protection rationale, actual commands and source/environment applicability.
- Review handoff: independent M5 Code Review including oracle independence and preservation of actual product proof before M6.
- Risks: a smaller mock fixture hides omitted resources; changed class names silently break catalog subsets.
- Rollback/recovery: restore the scenario/fixture/subset-caller unit; discard only invocation-owned candidates; keep real artifact cases until replacement protection is assessed.

### M6. Complete release fixture and scenario organization

- Milestone kind: implementation.
- Engineering purpose: clarify local release scenarios while preserving identity, authority and persistence boundaries.
- Requirements: TEST-SR-01–10/12/17–20; VAL-SR-01/02/14/15/17/32; retained Release requirements in the allocation.
- Architecture responsibility: profile/preparation, candidate/approval, provider orchestration, evidence and recovery.
- Dependencies: M5 review/corrections; current shared package/release fixtures identified.
- Implementation scope: all six release modules and recursive fixture inputs. Retain useful existing behavior modules and ordinary factories; extract remaining reusable prepared-repository/timing builders from test classes so one test no longer constructs another test class to borrow setup. Assess imported fakes' ownership without replacing required real Git or archive observations.
- Files/components likely touched: release aggregate, candidate/coordination/evidence/execution modules, fixture helper and consumers. Preserve `current-version.json` writer/location and historical profile grammar.
- Required verification: TG-06 — valid/invalid profile and candidate identity, changed or denied approval with no external write, uncertain publication retry without duplicate publication, conflicting public identity rejection, interrupted local persistence/recovery and concurrent real-Git evidence writers. Ordered recovery steps stay in one private scenario.
- Evidence expectations: actual owned filesystem/process/Git results, explicit deterministic service doubles, private state for each variant and preserved candidate identity across failure; simulated services never prove hosted/public availability.
- Implementation steps: assess complete aggregate and imported groups; replace borrowed test helpers with explicit fixture operations; retain exact historical/current distinctions; reconcile shared consumers; run all affected local release proof.
- Validation commands: C1; `python tests/engineering/release/test-release-transaction.py`; C2 for actual release/helper/fixture paths and any packaging consumers affected.
- Expected observable result: independently runnable release scenarios make approval, external-call intent and persisted recovery state understandable.
- Completion criteria: all M6 groups/fixtures have supported dispositions; complete aggregate and individual execution pass; required real persistence and negative authority observations remain intact.
- Required evidence: `m6-implementation`, `m6-validation`, fixture ownership and actual boundary limitations.
- Review handoff: independent M6 Code Review of identity, retry, cleanup and shared packaging interactions before M7.
- Risks: factory extraction changes fixture identity or historical grammar; fake service success is mistaken for public evidence.
- Rollback/recovery: restore helper/consumer edits together and preserve contradictory results; no external publication or public rollback is performed.

### M7. Assess package Records, transactions and generated families

- Milestone kind: implementation.
- Engineering purpose: organize package-local contract and transaction scenarios before completing CLI/Installation integration.
- Requirements: TEST-SR-01–10/12/17–20; VAL-SR-01/02/14/17/32; CLI-SR-01–13 and retained Records obligations.
- Architecture responsibility: Records representation/query, targeted construction, public dispatch, filesystem transaction and recovery.
- Dependencies: M6 review/corrections; current native Node registration and shared record-fixture consumers identified.
- Implementation scope: all M7 test files, four helpers and fixtures. Retain focused native files where suitable; expand compressed scenarios enough to expose starting state, operation, expected results and cleanup. Keep named generated cases deterministic and mutation variants independent. Separate fixture mechanics from independently justified result expectations.
- Files/components likely touched: `record-store-*.test.js`, `record-retirement.test.js`, package-local helpers and shared record fixtures; Node glob/routing consumers if new files appear.
- Required verification: TG-07 — valid current/retired/unknown formats, complete reads/filtering, targeted versus advanced effects, omitted-byte preservation, exact-subject conflicts, contender exclusion, lost-response retry, unsafe paths, interruption and tampered-recovery rejection. Actual public dispatch and fault-injection child paths remain covered; no-write claims inspect relevant before/after bytes.
- Evidence expectations: named native population and generated family comparison, real isolated files/child processes, stable error meaning and independent invariants. Equality of two production paths alone is insufficient for their shared required outcome.
- Implementation steps: assess each file/group and generated domain; refine setup/action/assert readability and owned helpers; investigate weak or mirrored expectations; establish replacement proof before reduction; reconcile all Python/Node fixture consumers.
- Validation commands: C1; `node --test packages/rigorloop/test/record-retirement.test.js` for its direct catalog scope; `npm --prefix packages/rigorloop test`; C2 for every changed M7 source/helper/fixture path.
- Expected observable result: generated and explicit Records cases expose their protected invariant and remain individually selectable through the native runner.
- Completion criteria: every M7 group and meaningful generated partition assessed; complete package and affected Python consumer proof passes; no hidden mutable sharing or discovery loss.
- Required evidence: `m7-implementation`, `m7-validation`, independent-oracle and actual transaction/recovery boundary rationale.
- Review handoff: independent M7 Code Review covering all M7 groups, generated cases and shared fixture interactions before M8.
- Risks: a shared result builder becomes the oracle; fixture copies are shallow; renamed generated cases disappear from exact selection.
- Rollback/recovery: restore test/helper/fixture and caller changes as one unit; retain old negative scenarios until adequate replacement; never repair product evidence by rewriting historical records.

### M8. Complete CLI/Installation assessment and whole-inventory reconciliation

- Milestone kind: implementation.
- Engineering purpose: finish the remaining package population and reconcile the actual combined result across all earlier slices.
- Requirements: TEST-SR-01–20 as applicable; VAL-SR-01/02/03/12/14/15/17/19–22/27/32; retained CLI/Installation obligations.
- Architecture responsibility: native CLI invocation, observation/renderer/workflow-context, installation and complete execution consumers.
- Dependencies: M7 review/corrections; current dispositions and proof for M1–M7; shared changes trigger affected earlier reassessment.
- Implementation scope: all six M8 test files and observability fixture; necessary remaining navigation/caller fixes; reconciliation of additions, removals, renamed identities, subtest/generated families, fixtures/helpers and alternate callers against the complete allocation. Finish unresolved groups in their owning slice; do not convert them to a deferred follow-up or count a pilot as completion.
- Files/components likely touched: M8 Node files/fixture, local support when useful, contributor navigation and genuinely affected catalog/caller lists. No new workflow decision or Installation behavior.
- Required verification: TG-08 — real CLI args/streams/status and declared observability formats; malformed/unsafe selectors stop before access; trusted local archive installation, default conflicts, force scope, late destination races, partial publication and retry preserve unrelated state. TG-FINAL-01/02 establish whole-population and consumer closure.
- Evidence expectations: fresh complete discovery plus source/caller reconciliation, all group dispositions, independently justified observable outcomes, emitted rerun samples and final changed-set/broad proof with exact applicability limits.
- Implementation steps: assess/refine M8 groups; run affected package/packaging proof; reconcile the final population against baseline and every slice; return any gap to its owner; run final integrated checks and prepare the complete review subject.
- Validation commands: C1; `npm --prefix packages/rigorloop test`; C2 for actual changes; C3 after relevant executor/probe changes; C4 and C5 for final integration. Reuse unaffected prior artifact observations only under the evidence rule below.
- Expected observable result: all included groups have supported dispositions, required proof remains reachable and useful, and no unexplained population remains outside the completed scope.
- Completion criteria: M1–M8 scope and additions accounted for; all affected required proof and integrated groups complete; no unknown protection or unowned correction; final review has exact complete subjects.
- Required evidence: `m8-implementation`, `m8-validation`, `inventory-reconciliation` and integrated proof results in the existing evidence record, with no permanent per-case registry.
- Review handoff: independent M8 Code Review, followed by the separate fresh whole-change checkpoint below.
- Risks: final changes stale earlier evidence; apparent count parity conceals lost variants; uncommitted changes are omitted from a Git-range claim.
- Rollback/recovery: restore only the failed coherent slice and reopen its assessment; keep additions and unresolved protection visible; preserve unrelated work and actual failed results.

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: all eight in-scope implementation milestones and required corrections complete.
- Assessment: fresh independent final whole-change Code Review of the complete delivered engineering change, including Design adoption, plan, test/fixture/consumer changes and cross-milestone interactions. Milestone approvals inform this assessment but do not replace it.
- Evidence: exact final subjects, independent reviewer basis, judgment, complete inventory/protection account and concern dispositions.
- Successor: distinct final Verify; corrections return to their owner and require affected reassessment and an adequate integrated final judgment.

This checkpoint remains required even when a proof group can reuse unaffected evidence. No milestone, collection result or passing command establishes whole-change completion.

## Change-level verification

### TG-FINAL-01. Complete population and useful protection

- Covers: TEST-SR-01–10/12/17–20, VAL-SR-21/22/32 and M1–M8.
- Demonstrate: every baseline and added test/fixture/helper group has a supported disposition; changed identities and meaningful parameters retain their required observations; imported/generated/direct-only populations are accounted for. A source split, aggregate pass or identical case count cannot conceal lost protection.
- Evidence expectations: C1 plus complete source/caller comparison and group-level rationale; required representative negative observations and explicit retained/replacement boundaries; independent review of all group dispositions. Unknown or omitted groups block completion.
- Non-applicability: none. Complete inventory is the selected initiative boundary, not a future maintenance task.

### TG-FINAL-02. Combined discovery, isolation and product consumers

- Covers: TEST-SR-04/05/08–10/19/20, VAL-SR-01–12/14/15/17/19/20/27/32, M1–M8 and retained product owners.
- Demonstrate: direct, selected and package callers still reach required observations; aggregate imports and native registration do not lose or duplicate cases; single-case reruns address the intended scenario; private fixtures remain independent with bounded workers. Actual archives/packed installs, release local orchestration/persistence and Records transactions retain their distinct proof after shared changes.
- Evidence expectations: C2–C5 on the final applicable subject, C1 population comparison, actual rerun samples from each changed entrypoint/helper family, retained or fresh full affected suite results and source/fixture/environment identity. Preserve required main/release caller scope through actual command definitions and their retained fixture tests; if those callers change beyond selector reconciliation, allocate their additional actual proof before implementation reliance.
- Non-applicability: live publication, hosted-success claims and exhaustive repetition of every expensive suite in every scheduling mode are not selected. Existing owner freshness requirements remain effective; simulated services do not replace required public release evidence for a future release.

## Validation plan

Start with the smallest changed scenario, then complete its listed suite and consumer scope. C2 uses actual changed file paths, repeated for all source/helper/fixture/caller changes; do not assume a bare directory is classified. Review emitted check IDs/reasons and unresolved paths before executing. Existing fixtures that verify rejection must actually reach the intended invalid condition. Where strengthening replaces a weak assertion, use a bounded failing-before/passing-after or seeded violation when feasible; otherwise record the exact inspected failure mechanism and execute the relevant proof. A passing reduced suite alone is insufficient.

| ID | Command or procedure | Purpose and timing |
| --- | --- | --- |
| C1 | Run the normal-loader collection procedure below and inspect actual source/caller/parameter families. | Before/after each affected slice and final reconciliation; collection is population evidence, never passing scenario execution. |
| C2 | `python scripts/select-validation.py --mode explicit --path PATH`; `bash scripts/ci.sh --mode explicit --path PATH --jobs 4` with repeated actual file paths. | Same-slice selection, prerequisites, changed helper routing and bounded independent execution; run every required selected check. |
| C3 | `RIGORLOOP_VALIDATION_WORKERS=2 python tests/engineering/validation/test-validation-execution.py ExecutionTests.test_parallel_tasks_actually_overlap_with_bounded_workers CaseAdapterTests.test_normal_and_isolated_fixture_preserve_hooks_population_and_parallelism` | Preserve the real CI overlap observation outside one-worker case allocation. If intentionally renamed, reconcile this allocation and actual CI caller before relying on the replacement. |
| C4 | `python scripts/select-validation.py --mode local`; `bash scripts/ci.sh --mode local --jobs 4`; `git diff --check`; `git diff --cached --check` | Final working-tree selection, execution and whitespace. Stage authoritative new files where preflight requires them; staging is not a commit. |
| C5 | `bash scripts/ci.sh --mode broad-smoke --jobs 4` | One final composed broad run over the actual combined worktree, including full direct product suites and current record checks. Do not use dry-run, stub or skip flags as proof. |
| C6 | `python scripts/validate-documentation-prose.py --mode enforce --path docs/plans/2026-09-16-test-design-and-suite-organization.md --path docs/plan.md`; `node scripts/validate-record-store.mjs docs/changes/2026-09-16-test-design-and-suite-organization/change.json` | Plan/navigation and current record validation at their handoffs. Independent Delivery Review judges semantic allocation. |

C1 reuses the existing adapters, with isolated temporary collection outputs; it creates no new runner or tracked ledger. Execute from the repository root and capture its relevant output in existing evidence. Before narrowing this procedure to an affected slice, establish the complete set and include its actual imported/generated consumers.

```python
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path("scripts").resolve()))
from lib.validation.validation_execution import discover_cases, discover_node_cases

with tempfile.TemporaryDirectory(prefix="suite-collection-") as temporary:
    scratch = Path(temporary)
    for index, path in enumerate(sorted(Path("tests").rglob("test-*.py"))):
        ids = discover_cases(["python", str(path)], scratch / str(index), jobs=1, timeout=300)
        print(json.dumps({"entrypoint": str(path), "ids": ids}))
    groups = discover_node_cases(
        ["npm", "test", "--prefix", "packages/rigorloop"],
        scratch / "node", jobs=1, timeout=300,
    )
    for group in groups:
        path = Path(group["file"]).relative_to(Path.cwd())
        print(json.dumps({"entrypoint": str(path), "ids": group["ids"]}))
```

The glob is a starting entrypoint set, not a complete inventory rule. Compare tracked source definitions, imported mixins/hooks, generated case registration, fixture scripts and actual direct/catalog/package/CI/release callers. Add any newly reached executable entrypoint explicitly to collection through its supported adapter. Python subtest rows require source-level comparison because they are observations inside a containing method, not independent cases. Catalog subsets and emitted reruns require their own targeted collection/execution checks after affected selector changes. Preserve a single-case execution sample from each changed group and execute all newly introduced or substantively changed cases at their required boundary.

This invocation does not authorize commits. If later authorized commits introduce a branch range, add actual `--mode pr --base 1195dfb261176d500e319662e2ffad5429cb63be --head HEAD` selection/execution at the resolved immutable head and validate the exact committed records; retain C4 for any remaining worktree changes. An old HEAD or local pass cannot establish current hosted/main success. Main/release definitions remain caller-audit inputs even when no actual hosted event or release is selected.

Reuse existing passing results only with exact proved scope, unchanged relevant test/helper/fixture/production/environment basis, current authority and no mandatory fresh-execution override. Record the affirmative basis in evidence. C1 final reconciliation and C4/C5 final execution are fresh obligations; no cross-invocation result cache is used. After evidence-only record changes, validate the current record set; additional unchanged expensive suite replays are not required solely by recording.

For manual protective-value/semantic assessment, the implementation author and independent reviewer inspect the exact scoped group, governing obligation, fixture fault, assertion and actual boundary; record performer, subjects, conditions, conclusion and limitations in existing evidence/review. This is necessary because collection and deterministic structure cannot establish readability, requirement relevance or semantic adequacy. Relevant source or contract changes expire the affected judgment; a material uncertainty requires a bounded scenario or return to the owning Design, not an unqualified retain claim.

## Risks and recovery

Preserve an owned pre-slice source/index snapshot or recoverable commit and discovered scope before edits; never restore the whole developer tree. The rollback unit is the affected tests, support, fixtures, aggregate imports and consumers together. Keep failed observations, reviewer findings and unrelated changes intact. Unknown protection, missing consumers or required shared mutable resources block the affected completion. A production incompatibility or new behavioral decision returns to its owner; changed settled milestone allocation requires governed replan and renewed Delivery Review.

## Dependencies

Use existing Python unittest, native Node tests, Node/npm, Git and repository adapters/tools. Execute M1 through M8 in order, with independent milestone review and corrections before the next slice. Same-slice consumer closure applies throughout; M8 does not defer earlier broken intermediate states. Approved-plan initialization may add absent work only after independent Delivery Review of this exact primary plan; Route owns later work state. All implementation and corrections precede fresh whole-change Code Review and distinct Verify. Push, PR, merge and publication retain separate authorization.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-16 | Split Skill and Validation into two reviewable slices each; keep Packaging, Release and two package populations as distinct slices. | Different setup and observation responsibilities permit bounded review while the complete inventory stays allocated. | One whole-suite rewrite; a Skill-only pilot presented as completion; a file-size quota. |
| 2026-09-16 | Retain suitable modules and compatibility entrypoints; justify any selector change explicitly. | Existing organization and supported callers have value, while broad inherited classes may need real responsibility separation. | Mandatory renaming, duplicate discovery aliases, deep inheritance as the default. |
| 2026-09-16 | Require per-slice consumer closure plus final full-population reconciliation and one composed broad run. | Local success cannot prove generated/imported coverage or cross-slice fixture compatibility. | Deferring all caller repairs; repeating every expensive suite in every scheduling mode; count parity as protection proof. |

## Readiness

See the owning change record for current workflow state. The plan requires independent Delivery Review before implementation reliance, independent milestone and whole-change reviews after implementation, and distinct successful Verify for final completion.
