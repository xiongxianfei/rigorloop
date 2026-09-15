# Validation test organization

## Purpose / big picture

Separate repository test sources from operational scripts, group them by current capability ownership, and preserve actual test discovery, failure detection and execution. Apply proportionate evidence under Validation TEST-SR-15/16 without introducing a semantic harness or blanket test deletion.

## Current Handoff Summary

- Owning change record: none selected; this is a scoped portable plan under the user's explicit refactor authorization on `refactor/validation-organization`.
- Authoring and review evidence: [existing refinement record](../changes/2026-09-14-design-suitability-review/contract-refinement.md) and its reviews. No lifecycle state or historical approval is manufactured by this plan.

## Source artifacts

- Proposal: no separate artifact; selected direction and authorization are recorded in the existing refinement record and independent Design Review.
- Spec and Architecture: [Validation](../design/engineering/validation.md) and [System](../design/system.md), exact subjects in the [independent Design Review](../changes/2026-09-14-design-suitability-review/reviews/validation-refactor-design-review.md).
- Prior-contract test spec: none additionally selected. Existing Validation execution/protection obligations and package/release requirements remain applicable.
- Review and allocation authority: [Assessment](../design/skill/assessment.md), [Plan](../design/skill/authoring/plan.md) and Constitution.

## Context and orientation

The current catalog is `scripts/validation_selection.py`; `scripts/validation_execution.py` adapts normal Python loaders and native Node discovery and emits rerun commands. `scripts/ci.sh` remains the contributor entrypoint. Python tests commonly derive the root with `Path(__file__).parents[1]`, import production modules as siblings, and use `with_name` to locate validators. These assumptions must be corrected with their source moves. Four release support modules are imported by the main release entrypoint; they are part of its discovered population, not standalone catalog commands.

The branch includes prior uncommitted work. Preserve it, use a pre-migration content/index backup for recovery, and distinguish the new migration diff from that baseline. Earlier cleanup plans are context, not authority to rewrite their records or claim their completion. This plan neither commits the accumulated branch nor publishes it.

### Concrete source destinations

Keep existing filenames to avoid unnecessary renaming. Each source below begins under `scripts/`.

| Sources | Destination directory | Milestone |
| --- | --- | --- |
| `test-boundary-first-reference.py`, `test-boundary-first-validation.py`, `test-change-metadata-validator.py`, `test-documentation-prose-validator.py`, `test-governed-lifecycle-cli-validator.py`, `test-guide-system-validator.py`, `test-markdown-readability-validator.py`, `test-query-change-record.py`, `test-select-validation.py`, `test-validation-execution.py` | `tests/engineering/validation/` | M1 |
| `test-skill-validator.py`, test-only `review_independence_skill_phrases.py` | `tests/skill/` | M2 |
| `test-adapter-distribution.py`, `test-npm-package-publication.py` | `tests/engineering/packaging/` | M2 |
| `test-release-transaction.py`, `release_candidate_tests.py`, `release_coordination_tests.py`, `release_evidence_tests.py`, `release_execution_tests.py` | `tests/engineering/release/` | M2 |

Exclusive fixtures move beside their owning group after checking actual readers. Begin with `scripts/fixtures/boundary-first/` to `tests/engineering/validation/fixtures/boundary-first/`. Audit `tests/fixtures/documentation-prose`, `skills` and `adapters` for exclusive versus cross-group consumers; move exclusive roots to the corresponding group's `fixtures/<capability>/`, and retain genuinely shared roots with an explicit consumer rationale in evidence. Shared record fixtures remain `tests/fixtures/rigorloop-records-v3/` because metadata, lifecycle and selector groups consume them. Release fixture inputs are shared across the main suite, imported support modules and selector tests; retain their capability-owned shared root for this migration.

`tests/fixtures/release-transaction/current-version.json` is a release-generated resource: `release_transaction._plan_current_version_fixture` writes it and `release_candidate` includes it in its source-change allowlist. Preserve that location, content contract and release behavior. It is not an exclusive static test fixture or test-only helper. Changing that release interface would require its owning Design and separate allocation.

## Non-goals

- No new runner, catalog, schema, semantic harness, test-count target or public skill.
- No case removal or assertion weakening solely to simplify migration. Distinct scope-preserving test consolidation needs its own justified assessment.
- No package test relocation, release permission change, external publication, branch-wide cleanup or historical evidence rewrite.

## Requirements covered

| Requirement basis | Allocation |
| --- | --- |
| TEST-SR-01–06, TEST-SR-15/16 | Both milestones retain group-level obligation/outcome descriptions and actual assertions; review assesses semantic claims without inventing agent compliance evidence. Manual scenarios are conditional on material uncertainty. |
| TEST-SR-07–10, TEST-SR-17, VAL-SR-26–28 | TG-1/2/3: complete move maps, consumers, rename/deletion selection, discovery preservation and negative sensitivity. No removal disposition is inferred from this plan. |
| TEST-SR-11–14 | Independent milestone and final reviews, change-level evidence and explicit applicability; existing checks and required freshness remain. |
| VAL-SR-01/02/05/07/10/17/18/21/22 | TG-1/2/3: independently materialized fixtures, single-case and bounded concurrent execution, ordinary loader parity and subprocess cleanup protection. |
| VAL-SR-03/04/06/08/09/12/14/19/20 | TG-1/3: current catalog/selector/executor behavior, no missing routes or fabricated passes, preserved prerequisites and canonical check composition. |
| System source layout; VAL-DEC-09 | M1/M2 source ownership and retained package locality. No public behavior or retired capability is reintroduced. |

Both milestones cover the applicable Validation Composition/path, Compatibility/migration, Failure/recovery and External/environment scenarios. Input-domain and State/lifecycle scenarios apply to rename/deletion routing and incomplete discovery. Identity/authority applies to bounded evidence claims and review; Temporal/retry applies to isolation, repeated actual execution and preservation of existing scheduler protection.

## Milestones

### M1. Move validation-tool tests with their discovery and callers

- Milestone kind: implementation.
- Engineering purpose: establish the new repository test root while preserving a runnable catalog and unchanged product tooling.
- Requirements: TEST-SR-01–12, TEST-SR-15–17 and the VAL-SR execution/selection requirements mapped above.
- Architecture responsibility: Validation source layout, catalog, selector and existing Python adapter.
- Dependencies: independently assessed Design package and independent Delivery Review of this plan.
- Implementation scope: the ten Validation suites, their exclusive fixtures, imports/root discovery, catalog paths/routing, actual workflow/direct callers and current documentation links. Other suites continue at existing locations until M2.
- Files/components likely touched: `scripts/validation_selection.py`, moved suites, exclusive fixtures, `.github/workflows/ci.yml`, existing executor only if a demonstrated adapter assumption requires correction, and current references in `docs/design/cli/cli.md`.
- Required verification: TG-1 — ordinary discovery before/after, direct suite and single-case execution, selector routing on both sides of moves, unchanged isolation and representative invalid-input detection.
- Evidence expectations: map each old entrypoint to its new entrypoint and actual discovered case IDs; list intentional new regression cases separately. Compare generated/imported populations, not AST method counts. Record exact commands and failures.
- Implementation steps: capture a recoverable migration baseline; establish selector regression proof before path changes; move each source/fixture with its readers; repair explicit root/script imports; reconcile workflow commands; demonstrate no required case loss. Retain old-path change classification to select current consumers without runnable alias scripts.
- Validation commands: `python tests/engineering/validation/test-select-validation.py`; `python tests/engineering/validation/test-validation-execution.py`; direct invocation of each moved suite; focused class/case invocation for representative fixture and path failures; `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path tests/engineering/validation --path .github/workflows/ci.yml`. If directory inputs are not classified, pass the exact moved files with repeated `--path` flags rather than inventing a blanket routing exemption.
- Expected observable result: old and new path changes select current commands, ordinary loader discovery retains every baseline case, negative inputs still fail, and a reported rerun command executes the intended case.
- Completion criteria: all ten entrypoints and required fixture consumers work from their new paths; counterpart suites still work from old paths; no unknown moved path or skipped case is hidden.
- Required evidence: baseline/discovery comparison, targeted and selected results, source/fixture consumer map, exact migrated subjects and limitations in the existing refinement evidence.
- Review handoff: independent Code Review of M1's complete source/caller/fixture slice, including any CI changes under CI-maintenance guidance.
- Risks: nested root calculations, sibling imports and selector fall-through may silently lose or misroute proof.
- Rollback/recovery: restore the captured M1 source/fixture/caller bytes and index state coherently, preserving pre-existing user edits; rerun the original entrypoints before further migration. Do not reset the branch.

### M2. Move Skill, Packaging and Release tests and reconcile navigation

- Milestone kind: implementation.
- Engineering purpose: complete repository test placement after the new validation root and selection rules are established.
- Requirements: TEST-SR-01–12, TEST-SR-15–17 and mapped VAL-SR preservation/isolation requirements.
- Architecture responsibility: Skill contracts, Engineering Packaging/Release test ownership and Validation's shared execution path.
- Dependencies: M1 complete and independently reviewed; no unresolved M1 loss of protection.
- Implementation scope: remaining four entrypoints, four imported release modules, the Skill test-only phrase helper, assessed exclusive fixtures and catalog/current caller references. Package-native test location and release-owned generated fixture stay unchanged.
- Files/components likely touched: source map above, `scripts/validation_selection.py`, `.github/workflows/publish-github-packages.yml`, current Skill documentation references, `CONTRIBUTING.md` and the test-layout section of `docs/project-map.md` after direct-source inspection.
- Required verification: TG-2 — ordinary full release discovery includes imported/dynamic cases; skill resource and archive integrity assertions still execute; actual npm packaging tests run; shared/release-generated fixtures retain their consumers and unchanged semantics.
- Evidence expectations: exact before/after discovered IDs, runtime/test-only helper disposition and fixture consumer map, current commands and output, independently reviewed claim limits. No execution of hosted publication is implied by local fixtures.
- Implementation steps: move coherent suites and helpers with imports; replace same-directory validator lookup with explicit production script paths; reconcile production catalog and workflow callers; update current navigation; validate skill/package/release ordinary paths. Retain existing assertions except independently justified corrections needed to observe the same contract from a new location.
- Validation commands: `python tests/skill/test-skill-validator.py`; `python tests/engineering/packaging/test-adapter-distribution.py`; `python tests/engineering/packaging/test-npm-package-publication.py`; `python tests/engineering/release/test-release-transaction.py`; `bash scripts/ci.sh --mode local --broad-smoke --jobs 4`; `git diff --check`. When the combined selected run executes a required suite completely, retain its actual result instead of redundantly repeating the direct command without a new concern.
- Expected observable result: all 14 Python entrypoints and four release support modules remain discoverable at owned locations, package tests remain colocated, candidate/archive checks exercise actual outputs, and no production code newly depends on test-only helpers.
- Completion criteria: complete source map adopted, current callers no longer launch old test paths, shared fixture exceptions justified, ordinary selected/broad execution preserves all required cases and failures, navigation describes observed layout.
- Required evidence: TG-2 results and discovery mapping, reviewed final source identities, maintained protection and any material limits.
- Review handoff: independent Code Review of M2 and interactions with M1.
- Risks: release support imports, copied repository fixture builders and explicit Git staging lists can omit moved test sources.
- Rollback/recovery: restore M2 tests, helpers, fixtures and callers together to the pre-M2 baseline, retaining valid M1 work. Preserve the release-generated fixture path and do not amend historical release records.

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: all in-scope implementation milestones and required corrections complete.
- Assessment: fresh independent final whole-change Code Review of the delivered migration and cross-milestone interactions, distinguishing preserved pre-existing changes from this scope.
- Evidence: exact final subjects, separate reviewer basis, judgment and concern dispositions.
- Successor: distinct final Verify of this scope; corrections return to their owner and require appropriate reassessment. No branch-wide or formal lifecycle completion is inferred from this portable plan.

## Change-level verification

### TG-3. Complete source relocation preserves actual protection

- Covers: M1/M2, TEST-SR-04/05/08/10/12/17, VAL-SR-01/03/04/05/17/21/22/27/28 and the combined suite-plus-fixture migration hazard.
- Demonstrate: normal discovery from all 14 entrypoints preserves the baseline case set including imported/generated release tests; ordinary package-native discovery is unaffected; local changed-set routing includes deletions and new paths; a representative moved fixture's intended violation is detected; direct and selected execution retain the same cases, resource isolation and honest diagnostics.
- Evidence expectations: use the existing executor's normal-loader collection before and after; collection is inventory, not passing execution. Capture actual results through current commands. Compare at least one single-worker and bounded-worker representative slice using the same inputs and case scope. Existing executor regressions protect general scheduler behavior; do not rerun all expensive suites twice solely to compare worker counts.
- Non-applicability: hosted PR/release execution and external semantic-agent certification are outside this local source migration; existing semantic review handles instruction and evidence claims. These limits do not waive final independent Code Review or Verify.

## Validation plan

- First run the smallest relevant moved-suite/selection checks; then complete the appropriate milestone and combined local/broad scope above. Required broad validation also preserves the applicable accumulated integration-plan trigger without claiming that unrelated initiative is complete.
- Use real normal-loader discovery and retain case identities; counts alone cannot show equivalence. Replay a representative emitted rerun command and a negative fixture after relocation.
- Inspect actual changed paths, live source/doc/workflow references and fixture readers. Historical plans, results and rejected-format fixtures retain their original meaning; do not bulk-replace every old string in the repository.
- Run prose/link validation for updated current documentation and `git diff --check` after evidence recording. No new formatting tests or mandatory per-case ledger are required.

## Risks and recovery

Preserve an exact pre-migration working-tree/index backup before edits because this branch contains prior uncommitted work. A missing case, unclassified moved path, changed package observation or released-fixture interface blocks its slice; restore the coherent source/caller group or correct it with fresh proof. Do not make a failure disappear by skipping cases, widening arbitrary path acceptance or changing expected outputs without governing authority.

## Dependencies

Independent Design Review supplies scoped engineering assessment; independent Delivery Review must assess this exact plan before implementation. M2 depends on M1's reviewed working catalog and source root. Final review depends on both milestones and all corrections; final Verify follows that review. No external action or historical record migration is authorized by this plan.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-14 | Move Validation first, then the remaining capability suites with their consumers | Provides two coherent reviewable states and keeps the shared selector path runnable. | An unreviewable bulk move or leaving callable compatibility copies indefinitely. |
| 2026-09-14 | Preserve filenames, cases and genuinely shared fixtures | Changes placement without confusing name churn with improved protection. | A deletion quota, speculative per-model folders or blanket fixture relocation. |
| 2026-09-14 | Retain the release-generated current-version fixture contract | Production release preparation owns this path and source whitelist. | Treating it as exclusive test data and silently altering release preparation. |

## Readiness

This is stable execution intent. Current independent assessments and actual results belong in the existing review/evidence surfaces; authoring this plan does not approve it, initialize lifecycle state or complete implementation.
