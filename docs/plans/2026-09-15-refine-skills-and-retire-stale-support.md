# Complete skill refinement and stale-support retirement

## Purpose / big picture

Make supported skill tasks easier to follow and remove support that no longer serves current behavior. Deliver the complete 19-skill and test/script inventory commitment through four reviewable slices, retaining distinct protection and making the one approved command withdrawal explicit.

## Current Handoff Summary

- Owning change record: [change.json](../changes/2026-09-15-refine-skills-and-retire-stale-support/change.json).

Mutable lifecycle, milestone state, review judgments, blockers and readiness belong to that record and its registered evidence.

## Source artifacts

- Proposal: [complete refinement direction](../proposals/2026-09-15-refine-skills-and-retire-stale-support.md).
- Spec: [Skill](../design/skill/skill.md), [Validation](../design/engineering/validation.md), [CLI](../design/cli/cli.md) and [Delivery Handoff](../design/skill/delivery-handoff.md).
- Architecture: SKL-DEC-09, VAL-DEC-10, CLI-DEC-08 and HAND-DEC-02. CLI-DEC-07 retains its original v2-retirement meaning.
- Prior-contract test spec: none independently required for this scope.
- Upstream evidence: exact `proposal-review` and `design-review-r2` package in the owning registry; the first Design review retains its original judgment and reporter-resolved finding.

## Context and orientation

`skills/` is the only authored skill source. Skill validators and guidance tests currently distinguish inline and selected-reference recording profiles; moving a section without updating every reader can silently disable checks. The query helper is a rejection-only command, but has a catalog entry, fingerprint, selector routing, test fixtures and a published-helper exception. Its withdrawal is one coupled rollback unit. The metadata validation wrapper has current callers and remains supported.

Use current sources directly; project-map currency is not assumed. Inventory baseline is `3c4985f80b242a295116880a5aee9cbbf47b12b0`. Before each slice, reconcile current tracked members, direct runners, imported mixins, generated/parameterized cases and transitive fixtures against the groups below. Additions, renames and removals must have explicit destinations. Final reconciliation includes tracked tests/scripts/support outside these named roots, package script declarations, CI workflows and generator inputs; generated adapter/dist copies are checked against their canonical owners rather than edited. Unknown coverage blocks completion.

### Concrete inventory allocation

M1 owns all complete packages for: proposal, proposal-review, design, design-review, plan, delivery-review, implement, code-review, route, verify, pr, bugfix, ci-maintenance, explore, research, vision, constitution, project-map and learn. This includes every entrypoint, transitive reference, output asset, shared guidance source and selected projection manifest. Other milestones assess the consumers they own; shared edits must identify all affected packages.

The table below enumerates current script/test source members at plan authorship. Paths in a row are relative to its root. Directory fixture rows include all recursive files, including invalid/generated inputs; an empty or skipped discovery result cannot establish coverage. This stable allocation is not a permanent audit ledger or a claim that case-level assessment has occurred.

| Owner | Root | Current members |
| --- | --- | --- |
| M1 | `scripts/` | `lib/validation/skill_validation.py`, `validate-skills.py` |
| M1 | `tests/skill/` | `review_independence_skill_phrases.py`, `skill_cli_tests.py`, `skill_contract_tests.py`, `skill_guidance_tests.py`, `test-skill-validator.py` |
| M2 | `scripts/` | `ci.sh`, `classify-record-store.mjs`, `lib/__init__.py`, `lib/validation/__init__.py`, `lib/validation/boundary_first_reference.py`, `lib/validation/boundary_first_validation.py`, `lib/validation/model_layout.py`, `lib/validation/project_yaml.py`, `lib/validation/record_snapshot_git.mjs`, `lib/validation/record_store_classification.py`, `lib/validation/validation_execution.py`, `lib/validation/validation_node_adapter.mjs`, `lib/validation/validation_selection.py`, `project-boundary-first-reference.py`, `query-change-record.py`, `resources/boundary-first/boundary-first-resources.yaml`, `select-validation.py`, `validate-boundary-first.py`, `validate-change-metadata.py`, `validate-documentation-prose.py`, `validate-governed-lifecycle-cli.py`, `validate-guide-system.py`, `validate-markdown-readability.py`, `validate-readme.py`, `validate-record-store.mjs` |
| M2 | `tests/engineering/validation/` | `fixtures/boundary-first/feature-records/complex.md`, `fixtures/boundary-first/feature-records/minimal.md`, `fixtures/boundary-first/feature-records/semantic-omission.md`, `fixtures/boundary-first/proof-maps/complete.md`, `fixtures/boundary-first/proof-maps/complex-complete.md`, `fixtures/boundary-first/proof-maps/gap.md`, `selection_cli_tests.py`, `selection_contract_tests.py`, `selection_git_tests.py`, `selection_test_helpers.py`, `test-boundary-first-reference.py`, `test-boundary-first-validation.py`, `test-change-metadata-validator.py`, `test-documentation-prose-validator.py`, `test-governed-lifecycle-cli-validator.py`, `test-guide-system-validator.py`, `test-markdown-readability-validator.py`, `test-query-change-record.py`, `test-select-validation.py`, `test-validation-execution.py` |
| M3 | `scripts/` | `build-adapters.py`, `close-release-publication.py`, `lib/packaging/__init__.py`, `lib/packaging/adapter_distribution.py`, `lib/packaging/npm_package_validation.py`, `lib/release/__init__.py`, `lib/release/release_candidate.py`, `lib/release/release_coordination.py`, `lib/release/release_evidence.py`, `lib/release/release_execution.py`, `lib/release/release_provider.py`, `lib/release/release_transaction.py`, `prepare-release.py`, `release-coordinator.py`, `release-preflight.py`, `release-verify.sh`, `release_evidence.py`, `resources/adapter-templates/claude/CLAUDE.md`, `resources/adapter-templates/codex/AGENTS.md`, `validate-adapters.py`, `validate-npm-package.py`, `validate-release.py` |
| M3 | `tests/engineering/packaging/` | `test-adapter-distribution.py`, `test-npm-package-publication.py` |
| M3 | `tests/engineering/release/` | `release_candidate_tests.py`, `release_coordination_tests.py`, `release_evidence_tests.py`, `release_execution_tests.py`, `release_fixture_helpers.py`, `test-release-transaction.py` |
| M4 | `packages/rigorloop/test/` | `cli-invocation-observability.test.js`, `cli-observability.test.js`, `cli.test.js`, `fixtures/observability/public-command-output.json`, `fixtures/recording-interactions/README.md`, `helpers/record-store-interactions.mjs`, `helpers/record-store-launcher.mjs`, `helpers/recording-query-launcher.mjs`, `helpers/v3-fixture.mjs`, `installer-replacement.test.js`, `record-retirement.test.js`, `record-store-adoption.test.js`, `record-store-cli.test.js`, `record-store-contract.test.js`, `record-store-format.test.js`, `record-store-interactions.test.js`, `record-store-model-examples.test.js`, `record-store-persistence.test.js`, `record-store-queries.test.js`, `record-store-targeted.test.js`, `record-store-v3-adoption.test.js`, `record-store-v3-contract.test.js`, `record-store-v3-mutations.test.js`, `record-store-v3-persistence.test.js`, `record-store-v3-reads.test.js`, `record-store-workflow.test.js`, `result-renderer.test.js`, `workflow-context.test.js` |
| M4 | `scripts/` | `build-record-store-schema.mjs` |
| M1 | `tests/fixtures/skills/` | All recursive fixtures and their transitive consumers. |
| M2 | `tests/fixtures/documentation-prose/` | All recursive fixtures and their transitive consumers. |
| M3 | `tests/fixtures/adapters/` | All recursive fixtures and their transitive consumers. |
| M3 | `tests/fixtures/release-transaction/` | All recursive fixtures and their transitive consumers. |
| M4 | `tests/fixtures/rigorloop-records-v3/` | All recursive fixtures and their transitive consumers. |

Each milestone records coherent protected-failure groups, retained/replaced/removed cases and fixtures, actual caller/discovery coverage and reasons. File counts alone are insufficient. Existing plan/evidence/review records carry the account; no mandatory per-function record or new audit tool is introduced.

## Non-goals

- No changes to public skill names, workflow gates, permissions, stored formats or supported runtime behavior beyond the explicitly selected query-helper withdrawal.
- No universal skill layout, length/test-count target, semantic scoring system or performance claim.
- No removal of the active metadata wrapper, feature-spec support or meaningful invalid-input/containment/recovery proof.
- No release, publication, active-environment installation or customer-document conversion.

## Requirements covered

| Requirement or obligation | Allocation | Proof |
| --- | --- | --- |
| SKL-SR-33 and SKL-SR-30/32 | M1 full skill inventory; final reconciliation M4 | TG-01, TG-02, TG-FINAL-01/02 |
| SKL-SR-34/35 | M1 selected entrypoints/resources, descriptions and validators | TG-01/02, TG-FINAL-01/03 |
| HAND-SR-04 with HAND-SR-01–03 | M1 PR body and preserved readiness/mutation boundaries | TG-01/02, TG-FINAL-03 |
| CLI-SR-31 with CLI-SR-02/09/10/11/18/23/28 | M2 obsolete helper withdrawal; M4 retained runtime protection | TG-03/04/06, TG-FINAL-02/03 |
| VAL-SR-29 | M1–M4 complete test/script/fixture population | TG-02/04/05/06, TG-FINAL-02 |
| VAL-SR-30/31 and VAL-SR-27 | M1 resource readers; M2 retired callers/deletion routing/current descriptions | TG-02/03/04, TG-FINAL-02/03 |
| TEST-SR-01–10/12/15/16/18 | Every test maintenance decision; unchanged relevant protection assessed before reuse | All milestone groups and TG-FINAL-02 |
| SKL-SR-09/14/17/20 and package integrity | M1 negative resources; M3 actual archive/install parity | TG-02/05, TG-FINAL-01 |

Model scenarios remain the acceptance basis. Input, authority, composition, failure and late-trigger conditions map to TG-01/02; current/retired/unknown record inputs and preserved state map to TG-03/06; deletion/rename/unknown-path combinations and case discovery map to TG-04; external installed boundaries map to TG-05. Temporal/retry and partial-failure rules remain unchanged and receive semantic preservation assessment plus existing runtime/release protection under TG-05/06. No scenario absence authorizes deletion.

## Milestones

### M1. Refine complete skill guidance with its validators

- Milestone kind: implementation.
- Engineering purpose: keep each changed instruction package and all of its source readers coherent before later support cleanup.
- Requirements: SKL-SR-33–35, HAND-SR-04, VAL-SR-29/31 and retained skill/resource obligations above.
- Architecture responsibility: SKL-DEC-09, HAND-DEC-02; Assessment/Workflow retain semantics and ownership.
- Dependencies: exact approved proposal/Design package and independent Delivery Review of this plan.
- Implementation scope: all 19 complete skill packages and their test population. Refine route, verify, pr, design-review and delivery-review as selected; clarify code-review description and PR asset. Validate retention of the other 13 packages. Route discovered new behavior decisions to Design rather than silently expanding scope.
- Files/components likely touched: the five entrypoints and recording destinations, code-review description, PR body asset, `scripts/lib/validation/skill_validation.py`, `tests/skill/` and affected fixtures/shared sources. Only Verify adds a recording reference; other four reuse selected existing resources.
- Required verification: TG-01 and TG-02 below; interim canonical/archive parity for changed resources.
- Evidence expectations: obligation/destination and supported-reading-path account for changed packages; current complete-package retention rationale for each other skill; meaningful resource faults; all test/mixin/fixture dispositions in M1's allocated population.
- Implementation steps: inspect existing complete packages and readers; establish meaningful missing/wrong/escaped/incomplete-reference counterexamples before extraction; move procedures and reconcile validators/tests together; correct artifact descriptions; assess and consolidate incidental checks only where retained protection is established; run focused then full relevant proof and independent review.
- Validation commands: V1, V2; V7 for changed-skill candidate parity; V8 for actual changed paths.
- Expected observable result: ordinary invocations reach their task before irrelevant recording construction; governed paths still load complete local procedures; PR consumes Verify rationale without inventing Explain-change or standalone ADR output.
- Completion criteria: every M1 population member accounted for, all selected normal/exceptional paths preserved, appropriate commands pass and independent M1 Code Review approves exact package and test-maintenance rationale.
- Required evidence: `m1-implementation`, `m1-validation`, `m1-code-review`, with exact subjects and limitations.
- Review handoff: full affected packages, shared consumers, before/after reading paths and retained/removed test protection, not just shortened entrypoints.
- Optional commit boundary: `M1: Refine skill navigation and current artifact guidance`.
- Risks: heading-dependent validator bypass; missing portable/adopted policy; a shared source change affecting uninspected packages.
- Rollback/recovery: restore each coupled entrypoint/reference/reader/fixture change from the pre-M1 commit; preserve review evidence and rerun affected proof. Do not restore one half of a moved procedure.

### M2. Retire the query shim and assess validation tooling

- Milestone kind: implementation.
- Engineering purpose: withdraw the obsolete interface as one complete source/selector/check change while retaining current validation entrypoints.
- Requirements: CLI-SR-31, VAL-SR-29–31/27, TEST-SR-07–10 and retained CLI safety.
- Architecture responsibility: CLI-DEC-08 and VAL-DEC-10; prior CLI-DEC-07 remains unchanged.
- Dependencies: M1 reviewed; exact Design retirement scope unchanged.
- Implementation scope: remove `scripts/query-change-record.py`, its two exclusive RetiredQueryTests, the named skill existence assertion, catalog/fingerprint/fixture expectations and helper exception. Correct the metadata-wrapper catalog input description. Assess every remaining validation script, test and fixture allocated to M2 and apply justified maintenance under unchanged obligations.
- Files/components likely touched: query script/test; validation selection, skill validator exception and query assertion; selection contract/git/CLI tests and command helpers; other M2 files only when their assessed protective value justifies change.
- Required verification: TG-03 and TG-04; rerun M1 resource checks when the shared skill validator changes.
- Evidence expectations: exact removal-to-owner map, current command absence semantics, actual deleted-path selection, retained record safety and reasoned dispositions for all M2 members.
- Implementation steps: establish replacement selection/negative proof before deleting exclusive expectations; remove the complete shim dependency set; preserve active wrapper behavior; assess actual cases and fixtures across the validation group; run direct and selected proof; return any additional behavioral retirement to Design.
- Validation commands: V2 for shared reader impact, V3, V4, V8; run other affected M2 direct suites from the inventory table using `python PATH` when changed, plus their selector checks.
- Expected observable result: the old path is absent without a product JSON promise; retained current interfaces reject unsupported inputs safely; deleted paths still select meaningful surviving checks and unknown paths remain visible.
- Completion criteria: no active caller launches the removed command, each allocated case/script/fixture has a current disposition, retained failures stay detectable and independent M2 Code Review approves the coupled retirement.
- Required evidence: `m2-implementation`, `m2-validation`, `m2-code-review`.
- Review handoff: complete query/caller deletion diff, selector outputs, retained protection and full M2 population account.
- Optional commit boundary: `M2: Retire obsolete query support and reconcile validation`.
- Risks: empty successful selection, unknown paths masked by known deleted paths, fixture deletion hiding invalid-input protection.
- Rollback/recovery: restore shim, catalog ID/fingerprint, callers and tests as one unit from pre-M2; do not revive a historical YAML decoder. Preserve historical record bytes and assessment identities.

### M3. Refine packaging and release support

- Milestone kind: implementation.
- Engineering purpose: establish complete current package integrity and assess packaging/release support separately from runtime record semantics.
- Requirements: VAL-SR-29/31, TEST-SR-07–10 and retained package/install/release obligations; SKL-SR-33–35 integrated parity.
- Architecture responsibility: existing Packaging, Installation and Release owners; this plan grants no publication authority or new release behavior.
- Dependencies: reviewed M1/M2 so the complete canonical resource and retired-script sets are available.
- Implementation scope: assess all packaging/release tests, fixtures, scripts, libraries, adapter templates and their callers assigned below. Refine stale descriptions or demonstrably redundant checks with preserved obligations; otherwise retain with concrete rationale. A new compatibility or release-policy change returns upstream.
- Files/components likely touched: M3 allocation and consumers; generated files only through existing generators.
- Required verification: TG-05 and TG-FINAL-01.
- Evidence expectations: distinct canonical/archive/install and release transaction/provenance protection; actual fresh candidate identities, complete resource parity and temporary installation results. Record package compatibility and removed-resource observations.
- Implementation steps: inspect each source/helper/fixture group and caller; establish any replacement proof first; apply maintenance; run affected direct suites and fresh supported candidate build/validation; hand off independent source and candidate assessment.
- Validation commands: V5, V6, V7 and V8. Publication tests use their existing isolated test environments; no real publish command is authorized.
- Expected observable result: both supported adapters contain complete current resources, no retired helper/resource dependency and usable target instructions; required release identity/recovery observations remain protected.
- Completion criteria: every M3 member assessed, any changed checks prove retained failures, actual candidates qualify and independent M3 Code Review approves evidence and current artifacts.
- Required evidence: `m3-implementation`, `m3-validation`, `m3-candidate`, `m3-code-review`.
- Review handoff: maintenance rationale, actual archives, transformation/parity results and release proof limits.
- Optional commit boundary: `M3: Refine packaging and release support with preserved protection`.
- Risks: confusing similar boundary checks with redundant proof; mocked release success mistaken for actual publication; stale generated resources.
- Rollback/recovery: restore affected canonical helper/test/template units and rebuild candidates; clean only owned temporary roots after reliance. Do not alter active user installations or public releases.

### M4. Assess package runtime proof and reconcile the complete inventory

- Milestone kind: implementation.
- Engineering purpose: close the remaining runtime test population and all cross-slice inventory gaps before final review; this is implementation/audit work, not a bookkeeping-only closeout.
- Requirements: VAL-SR-29–31, TEST-SR-01–10/12/18, retained CLI-SR-02/09/10/11/18/23/28 and all change-level integration obligations.
- Architecture responsibility: current CLI/Records/Persistence/Installation contracts; behavior remains unchanged apart from the already selected helper path withdrawal.
- Dependencies: reviewed M1–M3 and exact current source/package evidence.
- Implementation scope: every package test, helper, fixture and schema-generation support member; investigate all tracked test/script/fixture/support members outside prior groups and any additions/removals since baseline. Establish justified cleanup or retention; finish any in-scope maintenance before closeout. New behavioral decisions require reviewed Design and affected replan.
- Files/components likely touched: M4 allocation; additional affected consumers explicitly reconciled with their earlier milestone evidence.
- Required verification: TG-06 and all final groups; any edits invalidate affected prior proof until reassessed.
- Evidence expectations: current case-level protection grouped by obligations, generated-domain rationale, actual discovery/caller coverage and complete population reconciliation without unowned remainder.
- Implementation steps: inspect all Node suites and helpers; identify stale/overlapping assertions and preserve useful public-process/identity/recovery boundaries; establish proof before reduction; assess generator dependencies; reconcile baseline-to-final population including CI/package commands; run required integrated checks and independent M4 review.
- Validation commands: V4 for runtime changes, V8, V9 and V10; rerun candidate qualification only if relevant canonical/generator inputs changed since M3.
- Expected observable result: full inventory has evidence-backed dispositions; current unsupported-input, no-mutation, stale-identity, recovery and packaging behavior remain protected through their actual boundaries.
- Completion criteria: no unassessed case/fixture/script/package or unknown removal remains; all changed and integrated proof passes; independent M4 review approves the complete inventory account. Counts alone or unchanged file names cannot satisfy this criterion.
- Required evidence: `m4-implementation`, `m4-validation`, `inventory-reconciliation`, `m4-code-review`.
- Review handoff: complete population reconciliation, grouped protective-value rationale, actual final branch/candidate evidence and impacts on prior approvals.
- Optional commit boundary: `M4: Reconcile runtime proof and complete support inventory`.
- Risks: generated/direct-only populations omitted; reduced discovery mistaken for speed or success; changes to shared helpers invalidate many earlier tests.
- Rollback/recovery: restore affected test/helper/generator units and rerun their real boundaries. Reopen impacted milestone assessment through Route rather than editing old approvals; keep contradictory evidence visible.

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: all four implementation milestones, complete inventory assessment and required corrections independently reviewed.
- Assessment: fresh independent final whole-change Code Review of actual complete diff, all affected Designs, plan, consumer interactions, exact final proof and preservation/retirement decisions.
- Evidence: exact final subjects, nonauthor basis, judgment and owned concern dispositions.
- Successor: distinct final Verify. Corrections return to their owner and require affected reassessment.

Neither a milestone review, successful integrated suite nor a justified unchanged population waives this checkpoint.

## Change-level verification

### Milestone verification groups

| Group | Observable protection and evidence |
| --- | --- |
| TG-01 | Independent nonauthor inspects complete changed skills and bounded ordinary/governed/late-trigger/failure examples. Show route manual versus supported/unsupported automation, Verify scoped versus final with optional Git basis, PR prepare/open and read-only records, and advisory/formal Design/Delivery Review. Missing authority/resources stop before the relevant action; no policy adoption or lifecycle mutation is invented. PR output cites one successful Verify rationale; Code Review description includes milestone and final work. Retained 13 packages receive current complete-package rationale. |
| TG-02 | Missing, wrong, escaped, incomplete or mixed resource selection fails; valid complete package succeeds. Heading removal alone cannot bypass profile/placement checking. Preserve unknown-value ordering, independent resource inventories and each skill test group's distinct structural contribution. Prose quality remains semantic review-owned; automation does not score sentences. |
| TG-03 | Exact old helper is absent and no supported caller executes it. Supported current CLI/record interfaces still reject retired/unknown/malformed input without leaking or mutating source bytes. The metadata wrapper still accepts its current scope and rejects invalid input with existing normalized errors; descriptions match JSON/current-record behavior. |
| TG-04 | Query deletion/rename paths select surviving checks; known deleted plus unknown input does not produce a successful partial selection. Catalog discovery agrees with actual retained runners, including direct-only, mixin and generated cases; removed IDs have no passing aliases. Each M2 test/fixture contribution is retained, replaced or explicitly retired with its owner. |
| TG-05 | Both actual Codex/Claude archives contain exactly the current canonical skill inventory under declared transforms; temporary installs contain complete resources and omit retired ones. Independent package expectations expose missing/stale/unexpected members. Release source/candidate identity, rollback and transaction negative cases retain their distinct observation boundaries. |
| TG-06 | Current public dispatch, transport versus stored-format distinctions, containment, unsupported input, absence of source mutation, exact-subject conflicts and recovery remain protected by actual package tests. Inspect expected-result independence and generated domains; reduce only established redundancy. Final population reconciliation accounts for every baseline and added member and all direct/selected/CI/package callers. |

For semantic TG-01, use registered contributor observations plus independent milestone review with performer, date, exact package subjects, selected inputs/authority, resource path, expected outcome, actual inspection and limits. Inspection is appropriate because text quality cannot be established by phrase matches. If a material uncertainty survives inspection, run a bounded manual scenario and preserve its outcome; do not claim universal agent behavior. A relevant later package/policy change requires reassessment.

### TG-FINAL-01. Complete packaged invocation paths

- Covers: SKL-SR-33–35, HAND-SR-04, M1/M3/M4, canonical-to-installed boundaries.
- Demonstrate: final changed recording paths and PR artifact guidance are present and consistent in both actual candidates, with all 19 skill dispositions and complete resources; no reference to checkout-only authoring paths is necessary.
- Evidence expectations: actual candidate hashes, full canonical resource comparison under declared transforms, temporary clean installs of the five relocated skills plus code-review, independent semantic observations and explicit unchanged-input reuse rationale where applicable.
- Non-applicability: none.

### TG-FINAL-02. Complete protective-value and dependency reconciliation

- Covers: VAL-SR-29–31, CLI-SR-31, TEST-SR-07–10/12, M1–M4.
- Demonstrate: no unassessed script, test, generated case or fixture remains; each removal has its retired obligation or established retained proof; active direct/selected/CI/package callers still exercise required scope. Current malformed/unknown input and historical-data preservation remain protected after deletion.
- Evidence expectations: ordinary grouped inventory evidence, actual before/after discovery and caller inspection, representative negative outcomes and independent review. Avoid a permanent ledger or deletion-count target.
- Non-applicability: none; an unassessed remainder blocks completion.

### TG-FINAL-03. Full branch and authority coherence

- Covers: all changed requirements, approved package/plan and complete original-base diff.
- Demonstrate: exact current engineering passes applicable selected and main gates; changed-path routing includes additions/deletions and owning records. Instruction changes preserve stage boundaries and successful Verify ownership; prior identities, CLI-DEC-07 meaning and reporter-owned finding resolution remain intact.
- Evidence expectations: actual V9/V10 results with immutable base/head, exact committed record validation, final whole-change review followed by distinct Verify. Local results do not imply hosted success or external-action authority.
- Non-applicability: none.

## Validation plan

Use focused cases first where a changed obligation permits a narrower reproduction, then complete the listed required scope. Commands name current repository-owned entrypoints; no new harness is needed. Resolve HEAD and DIR to actual immutable revision and owned temporary path in evidence. `v1.0.0` is a qualification label, not release permission.

| ID | Command | Allocation |
| --- | --- | --- |
| V1 | `python scripts/validate-skills.py skills` | M1 and final canonical integrity. |
| V2 | `python tests/skill/test-skill-validator.py` | M1 full affected skill population; rerun after relevant M2 shared changes. |
| V3 | `python tests/engineering/validation/test-select-validation.py`; `python tests/engineering/validation/test-change-metadata-validator.py`; `python tests/engineering/validation/test-validation-execution.py` | M2 caller/deletion/metadata/execution integration; additional changed M2 suites run directly from the allocation. |
| V4 | `npm --prefix packages/rigorloop test` | M2 retained runtime-boundary proof and M4 package changes; justified unchanged proof may be reused between milestones. |
| V5 | `python tests/engineering/packaging/test-adapter-distribution.py`; `python tests/engineering/packaging/test-npm-package-publication.py` | M3 complete package regressions in existing isolated test environments. |
| V6 | `python tests/engineering/release/test-release-transaction.py` | M3 complete composed release suite and imported groups. |
| V7 | `python scripts/build-adapters.py --version v1.0.0 --output-dir DIR`; `python scripts/validate-adapters.py --version v1.0.0 --adapter-root DIR --clean-install-smoke --skill route --skill verify --skill pr --skill design-review --skill delivery-review --skill code-review` | M1 interim resource boundary; M3 final fresh candidates and TG-FINAL-01. |
| V8 | `bash scripts/ci.sh --mode local`; `bash scripts/ci.sh --mode explicit --path PATH`; `node scripts/validate-record-store.mjs docs/changes/2026-09-15-refine-skills-and-retire-stale-support/change.json`; `git diff --check` | Changed-set checks and current records at each appropriate handoff. Explicit PATH is the actual affected path, repeated when required; local runs need staged new paths when selector rules require them. |
| V9 | `bash scripts/ci.sh --mode pr --base 3c4985f80b242a295116880a5aee9cbbf47b12b0 --head HEAD` | M4/final complete original-base routing and selected proof. |
| V10 | `bash scripts/ci.sh --mode main --base 3c4985f80b242a295116880a5aee9cbbf47b12b0 --head HEAD` | Final full direct product gates and required broad scope for this complete-inventory change. |

Inspect actual runner discovery and dynamic definitions; do not treat a list of filenames or collection count as protective-value assessment. Unchanged audits do not require blind repeated executions: reuse actual passes only with exact unchanged source/helper/fixture/environment and no freshness override. Current-state checks and the final branch/main gates remain required. After attributable evidence-only suffixes, validate the exact committed owning records with `--revision SHA`; changed engineering or contradictory evidence requires affected proof and review again. Hosted CI and release completion are separate claims.

## Risks and recovery

The largest risk is silently weakening coverage while making the tree look cleaner. Establish replacement detection before removing checks, keep unknown protection visible and review the complete group. A real coverage gap returns to its owner; it is not an allowed deferred remainder.

Restore coupled units from the pre-milestone commit if extraction, deletion routing or replacement proof fails. Keep first-pass judgments, findings and failed runs intact. New incompatibilities require Design review and an affected plan revision before implementation reliance. No active installation or remote state needs rollback because none is authorized by this plan.

## Dependencies

Use existing Python, Node/npm, Git, repository scripts, schema/record readers and supported adapter builders. No new runtime dependency is selected. Milestones proceed M1 → M2 → M3 → M4 with independent review between slices; shared consumer changes require reassessing affected earlier proof. Plan work entries may be initialized only after independent Delivery Review approves the exact primary plan; Route owns later state changes.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-15 | Four implementation milestones followed by separate final review and Verify. | Separate package guidance, command withdrawal, release support and runtime proof into coherent review/rollback units while retaining full inventory scope. | A pilot-only closeout drops user goals; one giant cleanup obscures protection and compatibility changes. |
| 2026-09-15 | Enumerate current files and assess actual cases through existing evidence. | Full population coverage and meaningful group rationale are both required. | A permanent audit ledger, count target or filename-only retention does not establish useful protection. |
| 2026-09-15 | Retain metadata wrapper and unproven semantic-checklist guards. | Current callers and omission risks are established; equivalent replacement is not yet proved. | Age or delegation alone cannot justify removal. |

## Readiness

See the owning change record for current workflow state. This plan requires independent Delivery Review before work initialization or implementation; it makes no implementation, final verification or external-handoff claim.
