# Independent parallel tests and architecture-view adoption

## Purpose / big picture

Deliver the reviewed architecture-authoring convention and simplified validation design together: portable skills produce understandable model views, each repository model has the supporting views it needs, required checks execute once per canonical ID within a run, and every retained automated test case is independently runnable and parallel-capable. Reduce duplicate protection only after its replacement is established; measure actual costs without a speed target.

## Current Handoff Summary

- Owning change record: [independent parallel tests](../changes/2026-09-13-independent-parallel-tests/change.json).

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: [independent parallel tests](../proposals/2026-09-13-independent-parallel-tests.md).
- Spec: owning living Designs, particularly [Validation](../design/engineering/validation.md), [Design](../design/skill/authoring/design.md) and [System](../design/system.md). The complete reviewed twelve-model set is linked by the owning change record.
- Architecture: the same living Designs own architecture; [Engineering](../design/engineering/engineering.md), [Skill](../design/skill/skill.md), [CLI](../design/cli/cli.md), their children and their boundary scenarios retain their detailed contracts.
- Prior-contract test spec: only the explicitly retained obligations in [published-skill-first simplification](../../specs/published-skill-first-repository-simplification.md) and its [test spec](../../specs/published-skill-first-repository-simplification.test.md), as allocated by Validation's current maintenance map. Historical retired validation specifications are not operational proof recipes.

## Context and orientation

The planning source snapshot has 83 catalog entries, 26 `scripts/test-*.py` entrypoints and 22 `packages/rigorloop/test/*.test.js` files. These are allocation counts, not discovered-case counts or independence evidence. The file groups below exhaust that inspected entrypoint inventory. Implementation reconciles dynamic discovery, custom loaders, nested invocations, package scripts, `scripts/ci.sh`, `scripts/release-verify.sh` and `.github/workflows/` against it; newly discovered or added cases join their owning group before closeout. Fixture programs executed by these tests remain within their parent case's resource/proof scope rather than becoming duplicate top-level tests.

Use `scripts/validation_selection.py` for the authoritative catalog and `scripts/validation_execution.py` for the existing scheduler, Python case adapter, composition and reports. The inspected `expand_cases` implementation currently expands Python unittest entries; the declared `node-test` unit does not establish complete Node case expansion. M6 must demonstrate actual native selection, hook completeness and isolated case execution rather than claim file-level concurrency proves case independence.

`validation_execution.regression` and `broad_smoke.validation_execution.regression` currently invoke the same complete executor suite. Three executor tests additionally repeat normal, single-worker and reversed-parallel execution of entire production suites. M3 replaces unnecessary repetition with focused detection and small real integrations, retaining full migration observations only where needed for adoption. The initial selector/lifecycle/metadata adoption remains protected.

The project map describes stale record-format and legacy architecture facts; this plan does not rely on it. Current Designs, CLI context, catalog, wrappers and actual test source provide the bounded orientation. No new project-map rewrite is allocated here. Prior cache/source/script retirement is completed original adoption, not a new cleanup milestone.

## Non-goals

- No validation cache, runtime equivalence inference, input-fingerprint matching, new public runner, distributed CI, permanent test ledger or benchmark service.
- No weakening of required checks, skips disguised as success, permanent unassessed serial exceptions or deletion based on names, counts or runtime alone.
- No record migration, historical evidence rewrite, product-feature change, live publication or deployment. Push and PR remain separately authorized external handoff.
- No universal graph-layout metric or claim that a keyword check proves architecture quality. Retained legacy document formats are not converted by installing the skill.

## Requirements covered

| Governing obligation | Allocation and proof |
| --- | --- |
| Design DES-SR-02–12, DES-SR-15/16/18/19/22; Skill SKL-SR-01–15 | M1 / TG-01 publishes portable, complete authoring/review guidance and preserves conditional loading, examples and packaging. M2 / TG-02 applies the view contract without competing authority. Historical invocation-retirement work is not reopened. |
| System SYS-SR-01–11; Engineering parent/child composition and reviewed overview decisions | M2 / TG-02 preserves products, complete hierarchy, nearest-parent ownership, whole-system flow and actual model interfaces. All twelve current model requirement/scenario tables remain the semantic basis for their views. |
| Validation VAL-SR-01–10, VAL-SR-12/14/15/17/19/20 | M3 / TG-03 establishes canonical selection, gating, trusted commands, dependencies, bounded resources, complete outcomes and cleanup. M4–M6 apply that machinery to remaining cases. |
| Validation VAL-SR-21/22; TEST-SR-01–14 | M3–M6 / TG-03–06 exhaust the retained case inventory through protection-preserving consolidation and isolated execution. M7 / TG-07 reconciles all actual callers and inventory deltas. |
| Validation VAL-SR-11/13/16/18 | M3–M7 preserve no-cache behavior, scoped source/consumer reconciliation, coherent adoption and truthful measurements. Already completed original source/cache retirement is a retained invariant, not repeated implementation. |
| Retained simplification R14/R17–20/R22/R25 and applicable test intent | M1, M4 and M7 establish current skill/package consumer coverage under Validation's maintenance allocation; retained R15/R16/R21 authority boundaries and required negative/regression proof remain. No second maintenance ledger or irrelevant compulsory duplicate comparison is added. |
| Workflow, Assessment, Records, Installation, Packaging and Release owned scenarios | M2 preserves view meanings; M4–M6 preserve actual product detection, permissions, fixture invariants and observation boundaries while changing tests and scheduling. Semantic gaps route to the owning Design. |
| RC-SR shared assessment/reliance and final-closeout policy | Every milestone receives independent Code Review; changed Design subjects receive Design Review as applicable. Fresh whole-change Code Review follows all implementation/corrections and precedes distinct final Verify. |

The eight model boundary dimensions map as follows: input domain and composition/path to TG-01–07; state/lifecycle and identity/authority to TG-01/03–07; temporal/retry and failure/recovery to TG-03–07; compatibility/migration to TG-01–07; external/environment to TG-01/03–07. M2 checks every affected model's own scenario rows against its views, including meaningful non-applicability. Implementation may derive additional cases for distinct hazards; these groups are not an exhaustive test whitelist.

## Milestones


### M1. Portable architecture authoring and review guidance

- Milestone kind: implementation.
- Engineering purpose: Publish the already reviewed Design method as one coherent skill-resource slice.
- Requirements: DES-SR-02–12/15/16/18/19/22; SKL-SR-01–15.
- Architecture responsibility: Design method, Skill content invariants and independent Assessment.
- Dependencies: Approved exact Design and this Delivery package.
- Implementation scope: Update design entry guidance, model-authoring, technical-design, system-composition, design skeleton, a portable worked example and affected design-review guidance. Replace unconditional optional-diagram guidance only for the selected living-model contract; retain legacy applicability and portable/governed recording boundaries.
- Files/components likely touched: `skills/design/SKILL.md`, `skills/design/references/{model-authoring,technical-design,system-composition}.md`, `skills/design/assets/design-skeleton.md`, one indexed skill-local example; actual affected `skills/design-review/` resources; existing skill/adapter validators and tests only where their protection requires it.
- Required verification: TG-01 — Required overview; reasoned necessity for all four views; every necessary view drawn; ownership/reference coherence; conditional loading and portable packaged completeness. Negative examples include a missing necessary runtime view, ambiguous owner and duplicate detailed authority.
- Evidence expectations: Inspect emitted examples for a small leaf and a composed subsystem using only candidate-packaged guidance plus synthetic project context. Independent reviewers record exact guidance/output identities and reasons for acceptance/rejection. Rendering/structural checks supplement this semantic exercise; no deterministic target-agent correctness claim.
- Implementation steps: Update focused protection for changed guidance and complete example expectations, then canonical content; generate supported candidate archives outside source/active roots and check exact resource parity. Scope governance/navigation consumers by actual changed references; retain an evidence-backed unaffected disposition for unchanged Constitution, AGENTS and CLI context.
- Validation commands: `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`; `python scripts/test-adapter-distribution.py`; prose checks for exact touched Markdown paths.
- Expected observable result: Installed candidate guidance can explain and illustrate the required views without internal repository documents or internal requirement IDs.
- Completion criteria: All triggered resources and transitive examples are complete in supported packages; reviewer exercises distinguish coherent and defective graphs; no public skill depends on this checkout.
- Required evidence: Guidance and example inspection, exact package identities, executed regression results and scoped consumer dispositions.
- Review handoff: Full skill/resource/example diff, supported package parity and semantic exercise evidence; independent Code Review.
- Optional commit boundary: `M1: Portable architecture authoring and review guidance`.
- Risks: Missing transitive guidance or confusing graph presence with adequacy.
- Rollback/recovery: Restore the canonical guidance/example/test slice together and regenerate candidates; never repair installed output as the source.


### M2. Necessary supporting views for all repository models

- Milestone kind: implementation.
- Engineering purpose: Apply the approved view convention without inventing submodels or duplicating detailed authority.
- Requirements: DES-SR-05/07/08/09/12/16/22; SYS-SR-10/11 and each model-owned scenario table.
- Architecture responsibility: Design authorship and each parent/child model owner.
- Dependencies: M1 guidance available; current approved twelve overviews retained.
- Implementation scope: Evaluate Context, Building Block, Runtime and Deployment for each of the twelve declared models, record reasons and owned detail links, and draw every necessary view. Preserve the selected Validation overview and full System hierarchy/end-to-end flow. Reconcile the Design model's embedded illustrative model with its explicitly declared complete/excerpt scope.
- Files/components likely touched: All twelve paths in `scripts/model_layout.py:PROJECT_MODEL_PATHS`; affected model-owned examples, including the embedded Design example. No separate design copy or new normative model required.
- Required verification: TG-02 — All twelve have a required overview and four justified necessity dispositions; necessary supporting diagrams resolve to one owner and agree with contracts, external boundaries, parent composition, normal behavior and significant failure scenarios.
- Evidence expectations: Exact subject list, per-model view dispositions and links, rendered changed diagrams, scenario walkthroughs and counterexamples. A model with a necessary absent view cannot be accepted; an unnecessary view has a bounded reason.
- Implementation steps: Use the Design authoring owner for model changes. Select the smallest meaningful views, reuse owned diagrams by reference, reconcile cross-model effects, and obtain refreshed independent Design Review of changed models and examples before downstream reliance. Code Review of delivered documentation remains distinct.
- Validation commands: `python scripts/validate-boundary-first.py --check` with one `--path` per declared model; prose checks with the same explicit files; render each changed Mermaid source and inspect links.
- Expected observable result: Readers can navigate overview to necessary context, structure, interactions and deployment detail without contradictory ownership.
- Completion criteria: All twelve and affected examples are assessed; every necessary view exists; exact changed package independently Design-reviewed.
- Required evidence: View dispositions, render/link observations, semantic scenario assessment, current Design Review and implementation review evidence.
- Review handoff: All affected view/model/example subjects and interactions to Design Review, then independent Code Review of the delivered documentation slice.
- Optional commit boundary: `M2: Necessary supporting views for all repository models`.
- Risks: Artificial diagrams or a model move silently retargeting historical judgments.
- Rollback/recovery: Restore the affected views/links together; preserve old identities and request assessment for revised subjects.


### M3. Canonical execution and focused executor protection

- Milestone kind: implementation.
- Engineering purpose: Remove repeated scheduling and excessive executor comparisons before expanding case adoption.
- Requirements: VAL-SR-01–12/14/15/17/19/20/21/22; TEST-SR-01–14.
- Architecture responsibility: Validation catalog, selection, executor and reports.
- Dependencies: M1 and M2 reviewed; no new public execution interface.
- Implementation scope: Compose focused F then required B minus F by canonical ID within one invocation. Consolidate known identical catalog entries only after checking commands, preparation, configuration and required observation points. Retire the duplicate executor ID and reconcile callers. Preserve one existing plan/result model and report shape. Refine executor cases and retain already adopted selector/lifecycle/metadata isolation.
- Files/components likely touched: `scripts/validation_selection.py`, `scripts/validation_execution.py`, `scripts/select-validation.py`, `scripts/ci.sh`; `scripts/test-{validation-execution,select-validation,artifact-lifecycle-validator,change-metadata-validator}.py`; associated fixtures and actual report consumers.
- Required verification: TG-03 — One execution per canonical ID with reasons; explicit distinct IDs remain distinct; conflicting argv/constraints and unknown values reject before launch; F failure blocks B even if overlap passed; diagnostic remainder preserves failure; dependencies/build gates, jobs=1, nested budget, fail-fast, timeout/interrupt cleanup and incomplete results remain correct.
- Evidence expectations: Focused isolated process tests with deliberately failing, skipped, missing, unknown and conflicting inputs; small real adapter integrations retain custom discovery, filtering and hooks. Establish replacement failure detection before removing the three full-suite comparison regressions. Record removed-case protection at group level.
- Implementation steps: Write focused regressions first; reconcile catalog aliases and all callers in the same slice; implement ordered set composition; replace expensive redundant comparisons with assessed focused/integration proof. Assess mutable roots and bounded nested demand in these four suites before case promotion; do not mark exclusive recursive runners parallel-safe without isolation proof.
- Validation commands: `python scripts/test-validation-execution.py`; `python scripts/test-select-validation.py`; `python scripts/test-artifact-lifecycle-validator.py`; `python scripts/test-change-metadata-validator.py`; `bash scripts/ci.sh --mode explicit --path scripts/validation_execution.py --path scripts/validation_selection.py --jobs 2`.
- Expected observable result: Overlapping required work has one factual result; gates and different required observations remain intact, including after failure.
- Completion criteria: Every removed alias has reconciled readers; preserved reports identify actual outcomes once; four suite populations retain complete independent proof and required negative cases.
- Required evidence: Before/after detection basis, scope/count differences, process/resource observations, exact commands/results and canonical caller map.
- Review handoff: Catalog/runner/wrapper/tests and actual callers as one independent Code Review slice.
- Optional commit boundary: `M3: Canonical execution and focused executor protection`.
- Risks: Over-deduplication, missed dependency rebind, recursive worker multiplication or missing required outcomes.
- Rollback/recovery: Revert catalog, composition, report consumers and tests together; restore lost proof immediately. Jobs=1 limits scheduling risk but cannot restore missing semantics.


### M4. Skill, documentation and product-delivery test isolation

- Milestone kind: implementation.
- Engineering purpose: Isolate package and documentation fixtures after the shared executor contract is established.
- Requirements: VAL-SR-02/07–10/12/14/17/21/22; TEST-SR-01–14; retained product contracts.
- Architecture responsibility: Validation execution; Skill, Packaging, Installation and Release keep behavior ownership.
- Dependencies: M3 approved; M1 packaged guidance basis.
- Implementation scope: Assess and refine the ten Python entrypoints in group P4 below, including generated archives, release candidates, subprocess fixtures and read-only source validation. Consolidate only overlapping protection with established retained detection; parallelize retained cases through the existing adapter and trusted catalog.
- Files/components likely touched: P4 test files and their owned fixture helpers; catalog constraints and actual selected/main/broad/release callers; production helpers only when required for approved isolation and without changing product semantics.
- Required verification: TG-04 — Complete discovery, individually runnable cases, isolated package/output roots and ports, complete teardown on failure, bounded nested children, preserved archive/installation/release negative proof and no live external publication.
- Evidence expectations: For this adoption group compare normal discovery and required outcomes with single-worker and reversed/concurrent isolated execution once, recording exact IDs, scope deltas and resource observations. Retain focused recurring tests; do not add these full comparisons to every CI run.
- Implementation steps: Inspect fixture writes and helper processes; give each case independent inputs/resources; strengthen replacement protection before deletion; execute group adoption proof; publish assessed constraints only after reviewable isolation evidence.
- Validation commands: `python scripts/test-skill-validator.py`; `python scripts/test-adapter-distribution.py`; `python scripts/test-release-transaction.py`; `python scripts/test-npm-package-publication.py`; run each remaining P4 entrypoint using its exact command in the allocation below, including the fidelity audit arguments.
- Expected observable result: Every retained P4 case can execute independently and under bounded parallel scheduling while detecting the same required violations.
- Completion criteria: No unassessed or coupled P4 remainder; no skipped/missing cases counted as passing; shared artifacts retain explicit preparation dependencies.
- Required evidence: Per-family isolation rationale, group-level consolidation rationale, direct/isolated population reconciliation and actual command results.
- Review handoff: P4 tests/helpers/catalog/callers and preserved product-boundary proof to independent Code Review.
- Optional commit boundary: `M4: Skill, documentation and product-delivery test isolation`.
- Risks: Fixed output roots, shared archive mutation, setup overhead and hidden live network operations.
- Rollback/recovery: Restore affected tests/helpers/catalog together; preserve required failing cases while correcting isolation; use isolated local fixtures for external effects.


### M5. Workflow, record-wrapper and measurement test isolation

- Milestone kind: implementation.
- Engineering purpose: Resolve custom loaders and process-global fixture dependencies as one distinct Python family.
- Requirements: VAL-SR-02/04/07–10/12/14/17/21/22; TEST-SR-01–14; unchanged Workflow/Records/Assessment contracts.
- Architecture responsibility: Validation adapters and tests; semantic owners unchanged.
- Dependencies: M3 approved; M4 completed for sequential reviewed delivery.
- Implementation scope: Assess and refine all twelve P5 entrypoints below, including dynamic/custom loading, environment patches, temporary Git repositories, record fixtures, wrapper invocations and measurement subprocesses. Preserve still-required historical fixtures without restoring retired runtime contracts.
- Files/components likely touched: P5 files and their actual fixture/helpers, catalog and caller constraints; no historical record rewrite or broad runtime feature changes.
- Required verification: TG-05 — Native discovery/filtering agrees with isolated selection and complete hooks; current/retired/unknown inputs retain failure sensitivity; fixtures own mutable state; failures clean up and preserve unrelated bytes; nested demand remains bounded.
- Evidence expectations: Record normal versus isolated population and outcomes once for each changed adoption group, with single-worker and concurrent/reversed observations, exact case IDs and all meaningful removals/additions. Assess custom runner support before catalog promotion.
- Implementation steps: Inspect loader/runner boundaries; refine self-contained scenarios; retain justified regression partitions and failure localization; adapt only incompatible entrypoints; establish protection and isolation before reducing cases.
- Validation commands: Run each P5 file using its exact `python scripts/test-....py` path below; `python scripts/test-validation-execution.py` for changed adapter semantics.
- Expected observable result: All retained P5 cases are independently runnable and parallel-capable with truthful dynamic discovery and outcomes.
- Completion criteria: No unknown-protection deletion or unassessed P5 remainder; wrapper and record negative proof remains at its real boundary.
- Required evidence: Exact population reconciliation, fixture ownership, justified case dispositions, command results and case-adapter observations.
- Review handoff: P5 tests/helpers/entrypoints/catalog changes and downstream wrapper behavior to independent Code Review.
- Optional commit boundary: `M5: Workflow, record-wrapper and measurement test isolation`.
- Risks: Custom loaders silently omit cases, environment leaks or historical fixtures mistakenly treated as current authority.
- Rollback/recovery: Restore the affected test/adapter slice and retained cases; repair custom selection before reenabling parallel constraints.


### M6. Node CLI and record-store case independence

- Milestone kind: implementation.
- Engineering purpose: Establish actual Node case isolation rather than relying on concurrent test files.
- Requirements: VAL-SR-02/04/07–10/12/14/17/21/22; TEST-SR-01–14; CLI/Records/Installation invariants.
- Architecture responsibility: Validation native Node adapter and CLI test boundaries.
- Dependencies: M3 adapter/composition approved; M4 and M5 reviewed.
- Implementation scope: Assess all 22 Node test files below, nested tests, hooks and spawned CLI processes. Use native selection/isolation only when it runs exactly the intended case with complete hooks and observable outcomes. Refine file-global mutable fixtures, ports and command stubs. Integrate the existing node-test execution unit with the shared worker budget as required; retain normal npm test coverage.
- Files/components likely touched: `packages/rigorloop/test/*.test.js`, shared test helpers, `scripts/validation_execution.py`, catalog native-runner constraints, package test entrypoint only if needed for bounded discovery/selection.
- Required verification: TG-06 — Selected case executes completely and alone, nested/hooks coverage is retained, duplicate names cannot select extra cases unnoticed, zero/missing/skip/failing outcomes reject complete-pass claims, isolated roots/ports and child cleanup survive concurrency, and all required record/install invariants remain detectable.
- Evidence expectations: Native discovery/selection experiments and focused adapter regressions precede adoption. Record exact case identities, completed leaf scope and normal/single-worker/concurrent outcomes for the full adoption population once. Native file scheduling alone is insufficient evidence.
- Implementation steps: Prove native selection and hook behavior with small fixtures; add focused negative adapter tests; refine each family's mutable setup; execute individual cases and bounded concurrent groups; reconcile npm, selected, main, broad and release callers without introducing a second scheduler.
- Validation commands: `npm test --prefix packages/rigorloop`; `node --test --test-concurrency=1 packages/rigorloop/test/*.test.js`; `node --test --test-concurrency=2 packages/rigorloop/test/*.test.js`; exact isolated name-selection commands and shared-executor invocations recorded for TG-06; `python scripts/test-validation-execution.py`.
- Expected observable result: Each retained Node case is independently runnable with native hooks and complete result attribution under the invocation budget.
- Completion criteria: All 22 file populations and any discovered nested cases reconciled; no case/file distinction hidden; all retained CLI/record/install protection preserved.
- Required evidence: Native selection and hook proof, full case population observations, bounded child-process evidence, actual commands and counterexample-based consolidation decisions.
- Review handoff: Native adapter, package entrypoint, all changed test families and preserved CLI behavior to independent Code Review.
- Optional commit boundary: `M6: Node CLI and record-store case independence`.
- Risks: Name-pattern ambiguity, parent tests skipped with child selectors, file-level concurrency misreported as case independence, oversubscribed native workers.
- Rollback/recovery: Restore adapter/catalog/package/test changes together; unresolved native behavior returns to Validation Design rather than weakening independence or dropping cases.


### M7. Integrated caller reconciliation and adoption

- Milestone kind: implementation.
- Engineering purpose: Close cross-family gaps only after all necessary mechanisms and populations coexist.
- Requirements: VAL-SR-03/11–22; TEST-SR-07–14; DES-SR-18/22; SYS-SR-10/11.
- Architecture responsibility: Engineering integration across Validation, Skill, CLI and Release.
- Dependencies: M1–M6 and their required corrections/reviews complete.
- Implementation scope: Reconcile final discovery and actual direct/selected/broad/main/release callers with the allocation inventory; resolve additions and unexpected disappearance in their owning group. Complete necessary guidance/catalog/CI caller adjustments and integration proof. Required release preparation, archive version/configuration distinctions and approval boundaries remain.
- Files/components likely touched: Actual remaining caller sites in catalog, wrappers, `.github/workflows/`, canonical shared guidance projections and current contributor references; no historical source cleanup rerun.
- Required verification: TG-07 — All required populations reachable with assessed isolation; no duplicate canonical execution in one invocation; public package guidance coherent; no cache; missing/failed work remains unsuccessful across composition; release-specific prerequisites preserved.
- Evidence expectations: Final entrypoint/case delta account, retained-protection mapping, scoped default-budget wall time and per-check/case durations with machine/command/subject limits. No universal CI-time target or comparison with unlike scopes.
- Implementation steps: Reconcile integration before broad checks; fix actual gaps through their owners; run required whole-change commands and supported candidate package checks; observe timing once the final implementation is stable.
- Validation commands: `bash scripts/ci.sh --mode main --jobs 2`; `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped --jobs 2`; final committed-range PR mode and additional required direct population checks as specified below.
- Expected observable result: The delivered skills explain the approved method and the full required validation population uses independent cases without redundant canonical scheduling.
- Completion criteria: All in-scope populations and affected callers accounted for; no unassessed serial remainder, unprotected deletion, stale required view or package resource; measurements disclose actual limits.
- Required evidence: Integrated command results, discovery deltas, package parity, measured timing scope and required current assessments.
- Review handoff: Integration slice to Code Review, followed by the distinct final whole-change checkpoint below.
- Optional commit boundary: `M7: Integrated caller reconciliation and adoption`.
- Risks: Late caller omissions, validation of the wrong source range, or premature whole-scope claims from a partial passing run.
- Rollback/recovery: Reopen the owning implementation group and rerun affected proof; restore lost protection; preserve failures and completed historical evidence.

### Test population allocation

This is a bounded plan allocation, not a permanent per-test ledger. M3 owns the four executor/initial-adoption entrypoints named in its scope. Each filename below is relative to the stated directory. For P4/P5 unittest entrypoints, the direct command is `python scripts/` followed by the exact filename. P4 also contains the read-only fidelity audit described below; its required arguments are explicit.

| Group | Directory and exact entrypoints |
| --- | --- |
| P4 / M4 | `scripts/`: `test-skill-validator.py`, `test-adapter-distribution.py`, `test-release-transaction.py`, `test-npm-package-publication.py`, `test-boundary-first-reference.py`, `test-boundary-first-validation.py`, `test-documentation-prose-validator.py`, `test-markdown-readability-validator.py`, `test-guide-system-validator.py`, `test-fidelity-gate-spec-reads.py`. |
| P5 / M5 | `scripts/`: `test-workflow-code-state.py`, `test-workflow-automation.py`, `test-workflow-automation-state.py`, `test-workflow-automation-policy.py`, `test-validate-workflow-automation.py`, `test-review-artifact-validator.py`, `test-retirement-ledger.py`, `test-query-change-record.py`, `test-governed-lifecycle-cli-validator.py`, `test-cli-result-measurement.py`, `test-token-cost-measurement.py`, `test-token-cost-report-validation.py`. |
| N6 / M6 | `packages/rigorloop/test/`: `cli.test.js`, `cli-observability.test.js`, `cli-invocation-observability.test.js`, `installer-replacement.test.js`, `workflow-context.test.js`, `result-renderer.test.js`, `record-retirement.test.js`, `record-store-model-examples.test.js`, `record-store-interactions.test.js`, `record-store-format.test.js`, `record-store-contract.test.js`, `record-store-cli.test.js`, `record-store-adoption.test.js`, `record-store-workflow.test.js`, `record-store-v3-reads.test.js`, `record-store-v3-persistence.test.js`, `record-store-v3-mutations.test.js`, `record-store-v3-contract.test.js`, `record-store-v3-adoption.test.js`, `record-store-targeted.test.js`, `record-store-queries.test.js`, `record-store-persistence.test.js`. |

P4 includes nine unittest entrypoints and one existing audit command. Run the audit as `python scripts/test-fidelity-gate-spec-reads.py --review-set tests/fixtures/requirement-fidelity-gate/representative-reviews --max-bytes-per-clause 4096 --assert-no-broad-reads`, matching `requirement_fidelity.spec_reads` in the catalog. It reads the complete selected log set and owns no mutable fixtures, services or worker pool. Assess and execute it as a bounded command; do not invent unittest cases or apply unittest discovery to it. Retain its scope and failure sensitivity. Normal/individual/reversed case-population observations apply to the nine unittest entrypoints; audit evidence records its exact inputs, command, result and independence rationale. This classification does not remove an entrypoint, a log or required verification.

For every family, inspect setup/teardown, module/class state, working directories, temporary files, environment, ports, Git repositories, external calls and nested workers. Change-local evidence records observed case IDs, meaningful dispositions and actual commands; the plan does not preapprove any particular case deletion. File additions/discovered alternate entrypoints must be assigned before closeout, never excluded solely because they were absent from this snapshot.

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: all seven implementation milestones and required corrections complete.
- Assessment: fresh independent final whole-change Code Review of the complete final diff, including prior authored model changes and cross-milestone interactions.
- Evidence: exact final subjects, independent reviewer basis, judgment, preserved protection and concern dispositions.
- Successor: distinct final Verify. Corrections return to their owner and require affected reassessment.

Milestone reviews and integrated tests do not substitute for this checkpoint. Verify alone owns successful final explanation and completion evidence.

## Change-level verification

### TG-FINAL-01. Coherent product guidance and complete validation adoption

- Covers: M1–M7; DES-SR-15/18/22, SKL-SR-08–14, SYS-SR-10/11, VAL-SR-03–22 and TEST-SR-01–14 as allocated above.
- Demonstrate: a candidate-packaged skill can guide coherent portable model views, while actual repository views and all required automated populations agree with the approved contract. An overlapping focused/boundary check executes once; a focused failure prevents successful boundary completion; distinct candidate/configuration checks and preparation remain distinct. Every new invocation executes anew.
- Evidence expectations: supported archive parity and semantic example assessment; normal/isolated full-population adoption evidence per family; final caller/discovery reconciliation; one final main/broad/PR boundary observation with failure and incomplete-work regressions; factual performance observations with exact subject and environment.
- Non-applicability: none for the integrated claim. Unchanged tests/evidence may be reused only under affirmative current-basis assessment; mandatory final gates and freshness overrides still apply.

## Validation plan

Run the milestone commands at the first owning boundary. Do not run full production suites repeatedly merely to test scheduling; small fixtures protect scheduler mechanics and one-time family adoption observations establish actual population independence. Changes after an adoption observation require affected fresh evidence.

For Python adoption observations, use the existing `validation_execution.discover_cases`, `_case_command('observe', ...)`, `case_plans` and `run_scheduled_checks` in an invocation-owned temporary directory, with `jobs=1` and bounded `jobs=2` for selected adoption cases and complete required family reconciliation. Preserve the original entrypoint/filter arguments, record every resulting case ID and outcome, and retain direct normal-entrypoint results. Implementation records the exact Python invocation used; these existing internal functions are not a new public runner. For Node, native direct and single-name executions plus the integrated node-test unit must prove exact selected scope and hooks; record precise escaping/name patterns and resulting identities rather than assume the installed runtime's behavior. Any need for a materially different mechanism returns to Design.

Final whole-change commands, from the repository root:

```bash
python scripts/validate-skills.py
python scripts/test-validation-execution.py
npm test --prefix packages/rigorloop
bash scripts/ci.sh --mode main --jobs 2
bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped --jobs 2
bash scripts/ci.sh --mode pr --base c815768aacb0a6762c0acd11acf1d21f3c26aac0 --head HEAD --jobs 2
python scripts/validate-change-metadata.py docs/changes/2026-09-13-independent-parallel-tests/change.json
git diff --check
```

Use the final committed source range for PR mode and record both exact commits. If the branch basis changes, Route/plan must reconcile that range before relying on the command. Full main/broad composition does not prove a direct-only population ran: M7 compares actual executed IDs to the plan inventory and runs every missing required direct population using its listed command. Within a run, canonical duplicates execute once; separate explicitly required invocations are fresh executions. Record failures as failures and fix their actual owners before progression.

Use `python scripts/validate-boundary-first.py --check` and `python scripts/validate-documentation-prose.py --mode enforce` with explicit `--path` arguments for the twelve `PROJECT_MODEL_PATHS` and affected examples where their format applies. Use the prose command with explicit plan/index/skill Markdown paths too. The validators take files, not a design directory. Render changed Mermaid sources with a recorded renderer version and inspect material owner links; graphical rendering does not assess design adequacy.

Run supported archive generation/parity and installation fixtures through `python scripts/test-adapter-distribution.py`, and release composition through `python scripts/test-release-transaction.py` and `python scripts/test-npm-package-publication.py`. A live `release-verify.sh` invocation needs an actual selected release/candidate basis; this initiative selects no release. Exercise its changed caller/composition paths with existing synthetic candidate fixtures and do not fabricate a release tag or claim live publication proof. Run stricter actual release checks if later separately authorized release scope requires them.

Manual semantic evidence is bounded to M1/M2: an independent reviewer inspects exact generated example/view subjects against the owning requirements and boundary scenarios, identifies coherent ownership and at least the listed negative counterexamples, and records conclusions/limitations in existing change evidence. It expires when relevant guidance, examples, model contracts or interfaces change. No paid hosted-agent experiment or specific target-agent success is required or implied.

## Risks and recovery

- Unsafe concurrency or unsupported native selection: keep the affected work incomplete, refine its fixtures/adapter or return the mechanism gap to Design; jobs=1 is a diagnostic safeguard, not completion of independence adoption.
- Lost protection: restore the case or establish assessed replacement detection before relying on a reduced suite. A passing remaining suite is insufficient.
- Excessive startup/setup cost: observe real durations and bound nested demand; preserve required observations without a speed threshold or cache.
- Diagram/guidance drift: restore or reconcile the exact owner, example and packaged-resource slice together; reassess changed Design subjects before downstream reliance.
- Partial implementation: recover at each milestone's coherent commit boundary. Preserve historical evidence/record bytes and user-owned files; do not rewrite old adoption or restore retired cache behavior.

## Dependencies

- Independent Delivery Review of this exact plan precedes work initialization and implementation.
- M1 → M2 → M3 → M4 → M5 → M6 → M7 is the stable reviewed delivery sequence. It limits simultaneous fixture/adapter changes; test execution within milestones remains bounded and parallel where assessed.
- Missing native-runner facts are resolved by M6's focused proof before adoption, not by assuming Node file concurrency establishes case independence.
- Current authoring/assessment owners retain authority. A newly necessary design decision returns to Design and independent Design Review; a delivery-allocation gap returns to plan and Delivery Review.
- Final Code Review then Verify are distinct from implementation and from each other. No external publication or PR is a completion prerequisite for this local implementation scope.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-13 | Deliver guidance and views before executor and family adoption, then integrate all callers. | Keeps the reviewed design usable and makes shared execution changes precede population promotion. | One giant unreviewed migration; dropping validation work while improving diagrams. |
| 2026-09-13 | Allocate all 26 Python entrypoints and 22 Node files, reconciling dynamic cases during implementation. | Bounds initial scope without pretending static file counts prove discovery or isolation. | A permanent case ledger; declaring unassessed suites out of scope. |
| 2026-09-13 | Replace repeated full-suite executor comparisons with focused protection and bounded adoption observations. | Separates scheduler mechanics from proof that real populations remain complete and independent. | Delete first and infer safety from green tests; triple-run every population on every CI invocation. |
| 2026-09-13 | Classify the P4 fidelity log audit by its actual entrypoint and name its existing required arguments. | Its parser requires a review set and byte bound; it validates selected logs and is not a unittest suite. | Bare invocation, phantom case discovery or dropping its proof. |
| 2026-09-13 | Use canonical IDs, existing case adapters and one worker budget. | Implements VAL-DEC-06 without inferred equivalence or duplicate scheduling infrastructure. | Fingerprint reuse, consumer graphs, result projection layers and a cache. |

## Readiness

- See the owning change record for current workflow state.
- Remaining completion gates: Delivery Review, seven implementation milestones with independent reviews and required Design reassessment, fresh whole-change Code Review, and distinct final Verify. Plan authoring does not establish any of these outcomes.
