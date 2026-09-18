# Complete model test coverage and execution cost

## Purpose / big picture

Deliver the approved test design across the complete model hierarchy: make selection guidance usable, align actual tests and fixtures with required observations, and report the execution cost of each executable case. Use the existing Markdown Designs as the planning basis. Required behavior, independent expected outcomes and meaningful failure detection determine the work; case counts and runtime savings do not determine adequacy.

Establish the population and timing baseline before changing product suites. Then implement reporting and complete alignment in bounded owner slices, preserving discovery, isolation and independent assessment. Every current model and section-owned responsibility receives an allocation below, including parent interactions and explicitly scoped historical obligations.

## Current Handoff Summary

- Owning change record: [complete model test coverage](../changes/2026-09-17-complete-model-test-coverage/change.json).

Mutable activity, milestone state, findings, command results, review status and closeout readiness belong only in that record and its registered evidence. This plan supplies stable delivery intent.

## Source artifacts

- [Approved proposal](../proposals/2026-09-17-complete-model-test-coverage.md): selection, complete model design, aligned proof and attributable runtime.
- [System](../design/system.md#living-test-design-composition), SYS-DEC-06 and TEST-SR-01–23; [shared selection and maintenance rules](../design/test-design/rules.md).
- [Markdown coverage navigation](../design/test-design/README.md): every owning Design and its local or parent test design. The allocation table below names all document owners.
- [Validation](../design/engineering/validation.md#execution-cost-reporting), VAL-SR-36–38 and VAL-DEC-12: measurement intervals, compatible reporting, complete caller accounting and report ownership.
- [Skill](../design/skill/skill.md#living-test-design-method-adoption), [Design](../design/skill/authoring/design.md#living-test-design), [Plan](../design/skill/authoring/plan.md#test-design) and [Assessment](../design/skill/assessment.md#test-design): published method, allocation and independent judgments.
- [Release](../design/engineering/release/test-design/test-design.md), [Skill](../design/skill/test-design/test-design.md) and [Authoring](../design/skill/authoring/test-design/test-design.md) Markdown strategies retain their existing scenario references and stated gaps.
- Proposal Review `proposal-review` and complete-package Design Review `design-review-final` in the owning change supply the exact assessed subjects and reliance limits. Read their current applicability before execution; a pathname or past approval alone is insufficient.

No separate feature specification, architecture document, ADR or test-specification artifact is introduced. Earlier testing plans are historical context for their own slices, not authority to restore retired formats or narrow this complete-model scope.

## Context and orientation

`docs/design/` owns lasting behavior and coverage intent. `skills/` and its mapped resources own authored public instructions; shared projections originate in `templates/shared/`. Actual tests live under `tests/skill/`, `tests/engineering/{validation,packaging,release}/` and `packages/rigorloop/test/`. Inline fixtures, generated registrations, imported cases and resource helpers are part of the population even when they do not have a separate fixture file.

`scripts/lib/validation/validation_selection.py` owns trusted check identity and routing. `validation_execution.py` and its Python/Node adapters own case discovery, scheduling and result facts; `scripts/ci.sh` owns the contributor-facing entrypoint. Reuse these components. Direct suite callers, local/explicit/PR/main modes, broad smoke, package checks and release-regression callers can expose different populations and preparation boundaries. Broad smoke or one naming-pattern scan cannot establish the complete population.

Package builders and the actual packed CLI provide the Packaging-to-Installation observation. Release regression uses private candidates, controlled providers and declared local artifact boundaries. External publication, real exceptional approval and live incidents remain separately authorized operational events.

Use current sources and native discovery when the project map does not establish freshness for the relevant area. Capture exact dirty-source identities as well as the commit, command, environment, worker budget and execution mode; a commit plus a dirty flag cannot identify the measurement basis.

## Non-goals

- No JSON catalog refinement, deletion, format migration or expansion in this plan. Existing `test-cases.json` and `cases/*.json` files remain unchanged reference material. Markdown owns the new allocation; native discovery owns executable inventory.
- No replacement runner, JSON-driven test execution, universal case schema, permanent per-function ledger, hosted evaluation service, validation-result cache or historical benchmark service.
- No automatic performance threshold, test-count quota, coverage percentage target or assertion generated from the same production logic it checks.
- No compatibility retirement, repository-wide incidental refactor, remote publication, PR creation, push or merge.

Generated execution-result JSON remains part of the approved Validation reporting behavior; it is distinct from an authored test-design catalog. Prefer preserving existing referenced method identities while strengthening proof. If necessary work would make a frozen catalog reference false, stop that affected change and return the concrete conflict to Design; do not silently edit JSON, keep a knowingly false link or omit required protection. Record newly established proof in the owning change; an unchanged catalog's conservative proposed/partial classification is not a new execution result.

## Requirements covered

Every row includes all of the owning Markdown test-design groups and their applicable boundary scenarios, not just an example named in a milestone. References are many-to-many; a shared test is executed once per required observation/configuration. Ranges below include only the actual declared requirement IDs.

| Model and source | Requirement basis | Allocation and proof |
| --- | --- | --- |
| [System](../design/system.md#test-design) | SYS-SR-01–13; TEST-SR-01–23 | M1 population and scope; M3 method; TG-FINAL-1/2/3 parent composition and protection. |
| [Skill](../design/skill/skill.md#test-design) | SKL-SR-01–35; section-owned Implementation, Bugfix and CI responsibilities | M3 published method; M4/M5 child interactions; M6 shared contracts and handoffs; TG-6 and TG-FINAL-2. |
| [Authoring](../design/skill/authoring/authoring.md#test-design) | AUTH-SR-01–05 | M4; TG-4, including goal and proof preservation across sibling handoffs. |
| [Proposal](../design/skill/authoring/proposal.md#test-design) | PROP-SR-01–06 | M4; TG-4 direction, conditional gates, target and recording boundaries. |
| [Design](../design/skill/authoring/design.md#test-design) | DES-SR-01–26 | M3 method consumers; M4; TG-4 coherent models, architecture, examples and source/output boundaries. |
| [Plan](../design/skill/authoring/plan.md#test-design) | PLAN-SR-01–08 | M3 method consumers; M4; TG-4 complete allocation, stable artifacts and bounded initialization. |
| [Project Foundations](../design/skill/project-foundations/project-foundations.md#test-design) | FOUND-SR-01–03 | M5; TG-5 child composition, conflicting evidence and partial completion. |
| [Vision](../design/skill/project-foundations/vision.md#test-design) | VIS-SR-01–03 | M5; TG-5 canonical source, markers, target binding and interrupted projection. |
| [Constitution](../design/skill/project-foundations/constitution.md#test-design) | GOV-SR-01–03 | M5; TG-5 authority, conflict and complete handoff. |
| [Project Map](../design/skill/project-foundations/project-map.md#test-design) | MAP-SR-01–03 | M5; TG-5 freshness, area registration, matching valid controls and retry. |
| [Discovery](../design/skill/discovery/discovery.md#test-design) | DISC-SR-01–03 | M5; TG-5 child selection and owner-preserving return. |
| [Explore](../design/skill/discovery/explore.md#test-design) | EXP-SR-01–03 | M5; TG-5 distinct options, safe targets and changing framing. |
| [Research](../design/skill/discovery/research.md#test-design) | RES-SR-01–03 | M5; TG-5 bounded questions, conflicting evidence and qualified conclusions. |
| [Learning](../design/skill/learning.md#test-design) | LRN-SR-01–03 | M5; TG-5 classification, confirmation, topic effects and exact route-result updates. |
| [Workflow](../design/skill/workflow.md#test-design) | WF-SR-01–19 | M6; TG-6 scope, changed basis, follow-up ownership and correction routing. |
| [Assessment](../design/skill/assessment.md#test-design) | RC-SR-01–23 | M6; TG-6 independence, concern disposition, reliance and final review/Verify separation. |
| [Delivery Handoff](../design/skill/delivery-handoff.md#test-design) | HAND-SR-01–04 | M6; TG-6 exact branch/verification basis, partial success and bounded CI repair. |
| [CLI](../design/cli/cli.md#test-design) | CLI-SR-01–32; Command Interface and Persistence sections | M7; TG-7 public request/result, mutation and recovery boundaries plus parent composition. |
| [Records](../design/cli/records.md#test-design) | RF-SR-01–14 | M7; TG-7 closed representation, typed references, correction versus immutable origin and faithful reading. |
| [Installation](../design/cli/installation.md#test-design) | DIST-SR-02, 07, 08, 10–16 | M7; TG-7 trusted input, conflict/force, races, truthful partial failure and retry. |
| [Engineering](../design/engineering/engineering.md#test-design) | ENG-SR-01–16; Development section | M1/M3/M8; TG-8 and TG-FINAL-1/2/3 source-to-product and development authority. |
| [Validation](../design/engineering/validation.md#test-design) | VAL-SR-01–32, 35–38 | M1 inventory; M2 reporting; M8 retained selection/admission/isolation; TG-1/2/8 and TG-FINAL-1/3. |
| [Packaging](../design/engineering/packaging.md#test-design) | DIST-SR-03–06, 09, 17–24 | M3 generated guidance; M8; TG-8 canonical resources, real archives, npm payload and installer composition. |
| [Release](../design/engineering/release/release.md#test-design) | REL-SR-01–26 | M8; TG-8 preparation, candidate qualification, authority, recovery and evidence. |

Historical source transfer, retirement and bounded rollout duties retain the applicability stated by each owner. M1 identifies their current reliance; the owning milestone verifies live consumers and surviving protection without recreating retired behavior or replaying completed releases. A genuinely inapplicable event needs a reasoned assessor disposition tied to exact scope. Missing deterministic proof is not historical non-applicability and blocks affected completion.

## Milestones

### M1. Establish the complete population and pre-change baseline

- Milestone kind: implementation.
- Engineering purpose: establish trustworthy scope and observations before suite changes can obscure missing or duplicated protection.
- Requirements: SYS-SR-03/06/08, TEST-SR-01–23, VAL-SR-12/14/18/21/29/32/37, ENG-SR-05/15/16 and every owner in the allocation table.
- Architecture responsibility: model owners supply intended observations; Validation supplies actual native discovery and caller identity.
- Dependencies: current independent Delivery Review of this plan and its unchanged approved Design basis.
- Implementation scope: inspect every Markdown coverage group, actual assertions, fixtures, helpers, generated cases and callers. Record a bounded group-level disposition and missing-proof allocation in existing change evidence; add no permanent method ledger or new catalog. Preserve all suites during baseline collection.
- Files/components likely touched: stage-owned evidence; current test entrypoints, package test scripts, CI/release callers and `validation_selection.py` are inspection inputs. Any necessary reachability repair belongs to M2 and receives proof before use.
- Required verification: TG-1 — reconcile required observations with current assertion boundaries and the complete caller/discovery union. Detect direct-only, generated and unexpanded populations; distinguish a scenario reference from an actual executable case.
- Implementation steps: capture exact source/environment basis; inventory callers and discovery using trusted repository adapters; inspect representative assertions and every explicit required gap; run the existing selected entrypoints; retain actual case/check timing where available and explicitly identify unmeasured populations. Allocate each gap to M3–M8, including semantic procedures and parent interactions.
- Validation commands: use the existing suite and selector commands under Validation plan. Collect broader modes only when their declared preconditions and authority are present; do not run a release operation to fill an inventory.
- Expected observable result: every model group and discovered population has an explained receiving milestone; no unknown group or missing caller is hidden by a passing subset.
- Completion criteria and required evidence: exact source and discovery basis, reproducible commands, observed outcomes, baseline measurement limits and group-level allocation, independently reviewed. No complete runtime-baseline claim while required cases remain unmeasured; M2 must close that measurement gap before relevant suite changes.
- Review handoff: complete scope reconciliation, assertion/fixture audit and baseline evidence. Review count changes only as investigation clues.
- Risks and recovery: importing or collecting tests can expose unsafe setup. Use private resources and bounded execution; preserve failure evidence, correct the owning isolation/reachability problem and recollect the affected population before proceeding.

### M2. Implement attributable timing and safe cross-mode reports

- Milestone kind: implementation.
- Engineering purpose: supply a common measurement boundary before changing product test bodies, setup or suite composition.
- Requirements: VAL-SR-01–12, 14, 17–22, 36–38; TEST-SR-04/05/10/17/20/22; ENG-SR-05/16.
- Architecture responsibility: existing selector, native adapters, scheduler, result writer and `ci.sh`; VAL-DEC-12. No additional runner or service.
- Dependencies: M1's assessed population and required missing-caller allocation.
- Implementation scope: add the approved `--durations N` view and `RIGORLOOP_VALIDATION_RESULT_JSON` output; preserve existing broad-smoke output compatibility. Reconcile uncovered deterministic callers with the existing executor without widening ordinary selection or changing direct Python/Node behavior.
- Files/components likely touched: `scripts/ci.sh`, `scripts/lib/validation/validation_execution.py`, `validation_selection.py`, `validation_node_adapter.mjs` where necessary; `tests/engineering/validation/execution_*_tests.py`, selector/wrapper tests and their private fixtures. Update existing contributor guidance and actual report consumers.
- Required verification: TG-2A — native identities, unique launches, compatible scope/status and duration ranking; TG-2B — report ownership, failure and cleanup; TG-2C — unchanged case reachability and a complete pre-alignment runtime baseline.
- Implementation steps: write focused failing proof first; extend existing result facts and report finalization; reconcile arguments, modes, nested environments and consumers; run normal selected paths and controlled failure paths; collect the reconciled baseline on unchanged product suites using the new reporting path. Keep pre-instrumentation observations and disclose measurement-boundary differences.
- Expected observations: worker cost includes launch, setup, body, teardown and owned-process cleanup but excludes queue wait; separately bounded wall time includes discovery and scheduling. Shared scenario links never duplicate execution. Unstarted work is visibly unmeasured; failures/timeouts retain their actual cost and reason. Ranking changes no selected scope, status or rerun command.
- Negative/recovery observations: invalid `N`, unknown closed values and conflicting report destinations reject before launch; equivalent legacy/generic destinations write once. Test symlink/source/capture collisions, concurrent writers, nested environment isolation, serialization/replacement failure, cancellation and partial discovery. Prior bytes remain safe; existing nonzero exit precedence survives a reporting failure. Use deterministic clock fixtures for arithmetic and small real workers for lifecycle claims.
- Validation commands: Validation execution and selection suites, then scoped CI for `scripts/ci.sh` and changed validation sources. Exercise all mode contracts using private fixture repositories and controlled release wrappers; no public release is authorized. Use the post-M2 reporting example below only after it is implemented.
- Completion criteria and required evidence: reviewed command/consumer compatibility, required negative observations, complete caller accounting and attributable actual baseline results for every retained deterministic case/configuration before its suite is changed. Unknown or unmeasured required populations prevent completion.
- Review handoff: reporting implementation, direct/selected caller agreement, exact baseline and failure evidence.
- Risks and recovery: report ownership can affect files outside worker scratch. Revert the complete reporting slice and its readers together if containment or compatibility fails; preserve earlier reports and unrelated data. Never reinterpret a failed run as a baseline pass.

### M3. Apply the selection method to authored guidance and generated consumers

- Milestone kind: implementation.
- Engineering purpose: make the reviewed Markdown selection method reachable in the instructions and templates used to author and assess subsequent proof.
- Requirements: TEST-SR-01–06/11–16/18–23, DES-SR-10/16/25/26, PLAN-SR-01/02/06/08, SKL-SR-08–15/24/28/35, VAL-SR-16/31 and applicable Packaging resource requirements.
- Architecture responsibility: System policy, Skill's canonical instructions, Design/Plan authorship and Packaging projections retain their existing ownership.
- Dependencies: M1 allocation and M2 baseline; published guidance and its resources are assessed as one slice.
- Implementation scope: reconcile `skills/design/`, `design-review/`, `plan/`, `delivery-review/`, `implement/`, `code-review/`, `verify/` and `route/` only where they consume selection and coverage intent. Update applicable `templates/shared/` sources and their declared projections. Preserve portable guidance and the current unsupported-output boundary.
- Files/components likely touched: relevant `SKILL.md`, mapped references/assets including the Design skeleton, shared quality/maintenance templates, `tests/skill/skill_design_resource_tests.py`, `skill_shared_policy_tests.py`, resource/portability tests and generated adapters through their existing generator.
- Required verification: TG-3 — ordinary, conditional and missing-resource reading paths reach the complete method; a small model accounts for its obligations without requiring JSON. A parent interaction and an unlisted regression cannot disappear through local coverage or a case whitelist.
- Implementation steps: compare actual source instructions with the approved method; make the smallest faithful changes; update declared copies together; test meaningful resource/shape negatives; regenerate through `scripts/build-adapters.py` and validate actual generated resources. Do not hand-edit generated output or replace semantic evidence with phrase-count tests.
- Validation commands: Skill suite, `python scripts/validate-guide-system.py`, adapter distribution suite and path-selected CI. Use the existing generator's checked command contract; package qualification is completed at M8.
- Expected observable result: the published reading path preserves requirement selection, independent expectations, fixture isolation, honest gaps and model-owned intent without internal maintenance requirements for customers.
- Completion criteria and required evidence: exact source/projection agreement, concrete compliant/faulty authoring walkthrough and required structural tests, with actual generated bytes and scope limits recorded.
- Review handoff: whole changed public reading path, templates, tests and generated consumers.
- Risks and recovery: shortening or projecting instructions can lose a triggered method. Restore the affected canonical source and regenerate its consumers together; do not retain a locally patched generated copy.

### M4. Align Authoring and its Proposal, Design and Plan children

- Milestone kind: implementation.
- Engineering purpose: establish proof of goal preservation and usable delivery allocation before relying on downstream artifact handoffs.
- Requirements: AUTH-SR-01–05, PROP-SR-01–06, DES-SR-01–26, PLAN-SR-01–08; applicable Skill parent refinement interactions and TEST-SR criteria.
- Architecture responsibility: Authoring owns cross-stage preservation; each child owns its local artifact/authority decisions; CLI owns actual storage guarantees.
- Dependencies: M1/M2 and M3's reconciled authored method.
- Implementation scope: strengthen existing structural and public-command tests where their asserted boundary is sufficient; execute the Markdown-designed independent walkthroughs with concrete compliant and faulty packets. Preserve the existing catalog and referenced test identities.
- Files/components likely touched: `tests/skill/skill_proposal_guidance_tests.py`, `skill_design_resource_tests.py`, `skill_plan_guidance_tests.py`, `skill_authority_tests.py`, `skill_shared_policy_tests.py`, relevant fixtures; document grammar tests under `tests/engineering/validation/`. Semantic packet identities and results belong in registered evidence.
- Required verification: TG-4 — atomic batch-import goal survives Proposal → Design → Plan; partial writes, weakened intent, inadequate proof allocation, wrong target, changed example-only basis and assumed approval are exposed. Exercise structural invalid content/unknown-value precedence separately from semantic gate selection; preserve neighboring bytes and scoped initialization authority.
- Implementation steps: inspect each owning coverage group; establish valid controls before fault mutations; fill required assertion gaps; assess actual canonical methods and produced artifact/action packets independently; retain source-read-only and separately authorized living-model adoption behavior. Follow the manual-proof contract below.
- Validation commands: Skill suite, boundary-first suite and applicable package-native model/example tests through the standard package test command; scoped CI on changed paths.
- Expected observable result: syntactically valid but behaviorally weakened outputs fail the independent assessment, while structural failures produce their intended diagnostics. A wording pass cannot close a semantic gap.
- Completion criteria and required evidence: every current Authoring/child group has actual sufficient proof or a justified original scoped-adoption disposition; required deterministic and semantic gaps are resolved, with distinct observations and exact subjects independently reviewed.
- Review handoff: assertions, fixture baselines, semantic evidence and the parent handoff chain.
- Risks and recovery: a synthetic walkthrough can be misreported as agent-runtime proof. Retain that limit, restore lost executable protection and repeat only affected assessments after a meaningful change.

### M5. Align Foundations, Discovery and Learning proof

- Milestone kind: implementation.
- Engineering purpose: establish trustworthy support inputs and bounded authoring effects before their results are consumed by workflow actors.
- Requirements: FOUND-SR-01–03, VIS-SR-01–03, GOV-SR-01–03, MAP-SR-01–03, DISC-SR-01–03, EXP-SR-01–03, RES-SR-01–03 and LRN-SR-01–03.
- Architecture responsibility: Foundations/Discovery own child composition; Vision, Constitution, Project Map, Explore, Research and Learning own their local evidence and effect boundaries.
- Dependencies: M1/M2 and M3; coordinate shared fixture edits with M4 to preserve its proof.
- Implementation scope: retain useful structural checks, add missing valid negative-case controls and execute the concrete Markdown walkthroughs. Use fresh synthetic evidence and private trees; no network investigation or policy adoption is needed to assess supplied evidence packets.
- Files/components likely touched: `tests/skill/skill_vision_guidance_tests.py`, `skill_project_map_tests.py`, `skill_project_map_guidance_tests.py`, `skill_discovery_guidance_tests.py`, `skill_learn_guidance_tests.py`, `skill_canonical_tests.py`, shared helpers and actual generator tests where canonical projection is claimed.
- Required verification: TG-5 — source/marker preservation, target collisions and interrupted writes; stale or contradictory map/evidence; genuinely distinct options and bounded source conclusions; confirmation before topic effects; exact route-result updates, retry and unrelated-state preservation. Include parent selection and receiving-owner boundaries.
- Implementation steps: identify each intended observation; assess whether an executable fixture or independent artifact walkthrough can expose it; establish coherent controls; apply one defining fault; inspect actual effects or candidate decisions; record exact evidence and limitations. Preserve current authorities and original historical identities.
- Validation commands: Skill suite and scoped CI for changed sources; relevant adapter/resource tests when support resources change.
- Expected observable result: plausible-looking but unsupported conclusions and overbroad effects are rejected on evidence and authority, not only formatting; repeated valid operations preserve the required state.
- Completion criteria and required evidence: all allocated child and parent groups accounted with actual observations; no unsupported claim that source-copy or wording checks establish useful reasoning.
- Review handoff: complete support-family proof, changed fixtures and independent semantic assessments.
- Risks and recovery: shared setup can hide the defining fault or leak state. Restore private fixture construction and sufficient assertions; preserve failed observations and reassess the affected family.

### M6. Align Workflow, Assessment and capability handoffs

- Milestone kind: implementation.
- Engineering purpose: prevent useful local proof from being converted into unjustified continuation, approval or external effects at capability boundaries.
- Requirements: WF-SR-01–19, RC-SR-01–23, HAND-SR-01–04 and SKL-SR-01–35 within their declared recurring/scoped applicability; section-owned Implement, Bugfix and CI obligations.
- Architecture responsibility: Workflow coordinates explicit actors, Assessment owns independent judgment, Skill owns common capability/resource interactions and Delivery Handoff owns the verified external-action boundary.
- Dependencies: M1/M2 and M3; consume M4/M5 proof when assessing their handoff interactions. Reuse public recording proof only within its exact current scope.
- Implementation scope: strengthen common contract/resource negatives and assess the Markdown-designed decision packets. Exercise permitted/prohibited transitions, changed basis, post-completion failure, reporter-owned disposition, follow-up status, final review before Verify, evidence-only suffixes and bounded PR repair. No real PR or hosted CI write is authorized.
- Files/components likely touched: `tests/skill/skill_contract_tests.py`, `skill_resource_tests.py`, `skill_route_guidance_tests.py`, `skill_verify_guidance_tests.py`, `skill_pr_guidance_tests.py`, `skill_bugfix_guidance_tests.py`, `skill_ci_contract_tests.py`, `skill_ci_guidance_tests.py`, and applicable package-native workflow/record tests.
- Required verification: TG-6 — use complete and faulty sibling handoffs, authority decisions and current-result packets. Explicitly distinguish nine-assembly CI declaration grammar from correct combined/late assembly choice, and ordinary CI write admission from exact failing-run/unchanged-head repair authority. Preserve unknown-value-first regression where an executable closed vocabulary exists; use semantic assessment where no such runtime exists.
- Implementation steps: trace each common/section-owned obligation to its real observation; add or strengthen missing negative/assertion proof; assess original-proof identity, feasibility failures, atomic group stops, stale approval and evidence suffixes; independently inspect the complete receiving decision and allowed effect set.
- Validation commands: Skill suite, package tests for changed workflow/record boundaries, and scoped CI. Use controlled provider results for hosted outcomes and disclose that boundary.
- Expected observable result: a saved record, passing structural test or stale favorable review cannot grant the next stage, close another actor's concern or authorize an unrelated write.
- Completion criteria and required evidence: all current groups have sufficient recurring proof and current independent semantic assessment; original scoped duties retain an explicit applicability account. No failing authority path is hidden by a successful sibling.
- Review handoff: common-resource assertions plus independent workflow, assessment and handoff evidence, including parent interactions.
- Risks and recovery: a reporter and author can be accidentally conflated or real external authority assumed. Keep actors and packets explicit, restore the permitted-effect boundary and obtain independent reassessment without replaying real writes.

### M7. Align CLI, Records and Installation at their public boundaries

- Milestone kind: implementation.
- Engineering purpose: close concrete persistence, diagnostic and installer gaps before broader source-to-product qualification relies on them.
- Requirements: CLI-SR-01–32, RF-SR-01–14 and Installation DIST-SR-02/07/08/10–16; relevant System/Validation preservation and independence criteria.
- Architecture responsibility: Command Interface, Persistence, record representation and installer acquisition/write boundaries; CLI parent composition.
- Dependencies: M1/M2. Incorporate M6's actor/record distinction in composed observations without replacing storage proof with walkthroughs.
- Implementation scope: inspect actual native package tests and private filesystem/network fixtures; strengthen intended diagnostics, no-read/no-write observations, typed-reference distinctions, exact conflict/recovery semantics and truthful partial-install reporting. Preserve current public behavior and historical evidence interpretation.
- Files/components likely touched: `packages/rigorloop/test/*.test.js` and their support files; `tests/engineering/packaging/adapter_install_tests.py`, `adapter_fixture_helpers.py`, `npm_recording_tests.py` and `npm_fixture_helpers.py` where the actual packaged boundary is required.
- Required verification: TG-7 — unknown input before consistency/access, stale basis and batch conflicts, winner/loser concurrent writes, interrupted persistence with exact recovery, faithful projections, default whole-candidate conflict, bounded force, containment races and late installation failure. Independently capture original bytes and intended diagnostics; do not invent operation-wide rollback where the contract reports a valid partial result.
- Implementation steps: compare each owner group with existing assertions; reproduce missing failure sensitivity where feasible; establish private valid candidates; inject the defining error at the claimed boundary; assert allowed changed and preserved state; run native and packed consumers as appropriate.
- Validation commands: `npm --prefix packages/rigorloop test`, adapter distribution and npm package suites for affected consumers, then scoped CI including `packages/rigorloop/test` and changed owner paths.
- Expected observable result: valid operations retain compatibility; invalid, stale, interrupted and concurrent operations produce their exact contractual result without unrelated mutation or hidden partial state.
- Completion criteria and required evidence: all required gaps at the allocated CLI/Records/Installation groups resolved with independent expected values, exact before/after state and actual public-boundary results.
- Review handoff: complete changed public observations, persistence/recovery fixtures and installer-to-package interactions.
- Risks and recovery: unsafe fixtures can touch user data or mock away the boundary. Use private destinations and controlled acquisition; restore affected tests/helpers and required detection before relying on any consolidation.

### M8. Align Engineering, Validation, Packaging and Release composition

- Milestone kind: implementation.
- Engineering purpose: establish complete source-to-artifact proof and preserved execution/reporting after the owner-specific suite changes.
- Requirements: ENG-SR-01–16, VAL-SR-01–32/35–38, Packaging DIST-SR-03–06/09/17–24 and REL-SR-01–26, with the scoped duties and operational limits in their Markdown owners.
- Architecture responsibility: Development's source/consumer loop, Validation selection/execution, deterministic Packaging and Release qualification/authority/recovery.
- Dependencies: M1/M2; M3 generated guidance and M7 packed-consumer proof. Final integrated comparisons additionally consume all M4–M6 changes.
- Implementation scope: close required selection/admission/discovery/isolation gaps and Release/Packaging assertion/fixture gaps; preserve actual archive, packed CLI, provider, recovery and evidence boundaries. Account for all direct-only and generated populations after changes. Keep catalog JSON unchanged and use Markdown group references in evidence.
- Hash compatibility allocation under Packaging DIST-DEC-07: before implementation, independently review the exact Packaging amendment and this plan revision. Introduce v2 only for newly built candidates; retain historical v1 metadata and verifier behavior. Bind independent mixed-case/punctuation/non-ASCII manifest oracles, retained-v1 controls, unknown-algorithm rejection, new producer/actual packed CLI agreement and current public-smoke algorithm selection to TG-8. Preserve the legacy profile observer’s v1 representation while correcting normalization, prefix and regular-file membership. Qualification must cover producer, bundled metadata, installer and Release together; rollback restores that coherent candidate slice, never rewrites published identities.
- Files/components likely touched: `tests/engineering/validation/`, `tests/engineering/packaging/`, `tests/engineering/release/`, their helpers and actual producer/selector consumers when required by an identified defect. Normal fixture corrections must not redefine governing behavior.
- Required verification: TG-8 — independent archive inventory/hash expectations, clean/repeated generation, actual packed installation, candidate identity through qualification/publication fixtures, changed authority between boundaries, uncertain writes, bounded visibility/retry, failed public smoke and failed durable reporting. Prove the packed boundary for empty installation-unit conflicts and unsafe destinations in both modes where the Design identifies gaps; a lower-level installer case alone cannot supply that observation.
- Implementation steps: resolve each Markdown group's gap against actual tests; establish valid controls and independent expected state; strengthen real boundary assertions; retain fresh candidate and package observations; run the necessary owner suites; reconcile native discovery with M1 and compare comparable M2 measurements after the final suite changes.
- Validation commands: Validation, adapter, npm-package and Release regression entrypoints below; applicable generated-resource validators and path-selected CI, followed by the change-level checks.
- Expected observable result: complete retained proof remains reachable, accurately measured and sensitive to the named faults; correct local fixtures do not claim live publication, actual emergency authority or a future incident assessment.
- Completion criteria and required evidence: every required deterministic gap resolved; each applicable semantic procedure assessed under the manual-proof contract; native population changes and meaningful variants reconciled; required real artifact evidence present. Conditional operational proof retains an assessor-owned disposition and an explicit limit; missing applicable proof blocks full completion.
- Review handoff: Engineering parent composition, final owner-suite evidence, retained-protection rationale and before/after measurement conditions.
- Risks and recovery: fixture reuse can erase public/packed boundaries or make the oracle depend on the producer. Restore independent expectations and real observation points. Roll back only owned fixture/test changes, preserve failed evidence and repeat affected integration after correction.

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: M1–M8 and all required corrections complete, with milestone reviews and change-level evidence available.
- Assessment: fresh independent final whole-change Code Review of the complete delivered diff, approved Design/Delivery allocation and cross-milestone interactions. Earlier milestone reviews do not substitute.
- Evidence: exact final subjects, independent reviewer basis, judgment, reporter-owned concern dispositions, actual validation and scope limits.
- Successor: distinct final Verify of the entire required chain. Corrections return to their owner and require affected reassessment; only successful Verify may record final completion.

This checkpoint cannot be waived by passing tests or by a verification group's non-applicability rationale. No PR, publication or merge is implied.

## Change-level verification

### TG-FINAL-1. Complete protection and execution reachability

- Covers: all allocated models, TEST-SR-01–23, VAL-SR-12/14/19–22/29/32/37, M1–M8 and System/Engineering parent composition.
- Demonstrate: every current Markdown group has adequate actual proof or an applicable explicit disposition; forward requirement-to-observation and reverse retained-test-to-protection inspection agree. Reconcile added/removed/renamed/imported/generated/native cases and all actual callers since M1. Unknown protection blocks removal; an absent catalog row cannot waive a regression.
- Evidence expectations: group-level before/after mapping, exact assertions/fixtures and required fault observations, complete caller/discovery accounting and independent assessment. A baseline pass or equal counts alone is insufficient.

### TG-FINAL-2. Usable guidance through the actual product boundary

- Covers: SYS-SR-03–06/08–11, DES-SR-25/26, Skill/Authoring/Assessment handoffs, Packaging/Installation and M3–M8.
- Demonstrate: the shared selection method reaches a model's concrete test design, a plan's adequate proof allocation, independent assessment and actual code/fixture evidence. Separately build and inspect the relevant generated resources and actual packed consumer; a canonical-only check cannot prove packaged reachability. Changed examples or resources are included with their owners in review.
- Evidence expectations: actual compliant/faulty artifact packets, exact produced and reviewed identities, source-to-generated resource observations and packed-boundary results. Preserve source-read-only, current compatibility and no-implicit-approval behavior.

### TG-FINAL-3. Comparable cost and honest failure reporting

- Covers: VAL-SR-08–12/17–20/36–38, ENG-SR-05/16, M1/M2 and every changed executable suite.
- Demonstrate: the same scope, native identity and relevant preparation yield attributable baseline and final measurements; scope changes are disclosed and never reported as speedup. Serial and parallel runs preserve the assessed case population where isolation/discovery changed. Failure, timeout, unavailable command, partial discovery and unstarted work remain unsuccessful/incomplete; concurrent total worker time is distinguished from wall time.
- Evidence expectations: actual commands, native result rows, conditions, changed-subject identities, rerun diagnostics and report safety observations. Use full serial/reordered comparisons only where establishing or changing isolation requires them; they are adoption evidence, not a permanent repeated benchmark inside regression suites. No fabricated durations for semantic reviews or live operations.

## Validation plan

Start with the smallest meaningful native case or behavior group for each change. The following are existing entrypoints; selected CI may supply a suite's execution without an unnecessary identical direct rerun. Derive exact per-case selectors from native discovery rather than inventing method names.

```bash
python tests/skill/test-skill-validator.py
python tests/engineering/validation/test-boundary-first-validation.py
python tests/engineering/validation/test-select-validation.py
python tests/engineering/validation/test-validation-execution.py
python tests/engineering/packaging/test-adapter-distribution.py
python tests/engineering/packaging/test-npm-package-publication.py
python tests/engineering/release/test-release-transaction.py
npm --prefix packages/rigorloop test
python scripts/validate-boundary-first.py --check
python scripts/validate-guide-system.py
bash scripts/ci.sh --mode local
git diff --check
git diff --cached --check
```

Use path-selected CI for a bounded change, for example:

```bash
bash scripts/ci.sh --mode explicit --path tests/skill/test-skill-validator.py
bash scripts/ci.sh --mode explicit --path scripts/ci.sh --path scripts/lib/validation/validation_execution.py
```

M1 must expand this command set for actual uncovered callers and record their exact existing commands; this list is not a whitelist or a claim that these suites cover the whole repository. Reconcile supported main/PR/release mode consumers using their real argument and preparation contracts. Test release-mode orchestration in a private controlled environment; do not run a public release to obtain test timings. Record whether an observation proves the real packed/local boundary, a controlled provider interaction or actual external state.

After M2 implements its approved interface, a scoped report command is:

```bash
validation_report_dir=$(mktemp -d)
RIGORLOOP_VALIDATION_RESULT_JSON="$validation_report_dir/skill-results.json" \
  bash scripts/ci.sh --mode explicit --path tests/skill/test-skill-validator.py --jobs 4 --durations 20
```

That interface is planned behavior, not a command claimed to work before M2. Preserve applicable measurement evidence before cleaning only the invocation-owned temporary directory. Use the same relevant mode, selected case population, environment and worker budget for comparisons; separate instrumentation changes, added proof and real efficiency improvements. An unavailable baseline or changed observation boundary requires an explicit comparison limit.

### Manual and operational proof

For each semantic group in M3–M6 and applicable M8 review, the author prepares the bounded fixture described by the owning Markdown Design: a valid control and a candidate with one material defect, the exact method/resource/input/output subjects, independently expected decision and prohibited effects. An independent assessor inspects the complete relied-on path and records the actual observation and rationale. Keep defining facts, oracle and scope visible; a matching paragraph or author-restated expectation is not evidence.

Record through the existing evidence/review commands the exact subject identities, conditions, expected versus observed outcome, authority source and limitations. Attach supporting subjects only through supported registration if needed; do not create a second permanent proof ledger. Evidence is reusable only while the relevant input, procedure, subject and environment remain applicable. Changes require affected reassessment; no arbitrary calendar expiry is invented.

Synthetic packets assess the chosen reasoning/authority boundary. They do not establish target-agent runtime behavior, live hosted configuration, real publication or actual incident resolution. For a condition that requires a future authorized event, name the original owning requirement, why it is presently inapplicable, what observation would be needed and who owns that future decision. Independent assessment settles the applicability; absence alone cannot become success or retire a requirement. All currently applicable deterministic and semantic gaps remain in scope.

## Risks and recovery

| Risk | Recovery and completion limit |
| --- | --- |
| A narrower inventory makes the suite look faster | Reconcile native cases, generated variants and callers against M1; restore lost reachability before comparing cost or claiming completion. |
| Shared fixtures hide faults, calculate the expected answer or leak mutable state | Restore independently owned setup and contract-derived assertions; demonstrate the intended negative case and affected concurrent behavior. |
| An expensive real boundary is replaced by a passing stub | Re-establish the required filesystem, persistence, archive, packed CLI or provider observation; do not count the cheaper test as equivalent proof. |
| JSON refinement expands the user's selected planning scope | Keep the catalog bytes unchanged. Preserve referenced methods where sufficient; route a necessary reference/behavior conflict to Design before dependent changes. |
| Proposed procedures are mistaken for executed proof | Record actual independent observations and exact identities; preserve explicit limits and block unsupported completion. |
| Timing output mutates a source or loses an existing failed result | Revert writer/reader changes together, preserve prior report/source bytes and failure evidence, and re-prove output ownership and exit precedence. |
| An implementation audit reveals a missing behavior decision | Return the precise gap to its Design owner, preserve uncertain tests and update approved allocation before implementation relies on a new decision. |
| A shared helper or public skill change invalidates an earlier milestone | Reassess affected proof and review with explicit applicability restrictions; retain historical judgments and failed evidence unchanged. |

Rollback is limited to the owned slice and its dependent consumers. Capture exact before states, preserve unrelated staged work and avoid repository-wide resets. Restore retained protection before removing replacement code or fixtures.

## Dependencies

Proposal and Design authority must remain applicable. Independent Delivery Review of this exact plan precedes implementation and any initialization of milestone work. M1 precedes baseline-dependent changes; M2 precedes product-suite changes; M3 precedes reliance on the revised public method. M4–M6 coordinate their shared Skill fixtures, and M8 consumes M3/M7 product-boundary proof. The final integrated groups require all affected milestones.

Each milestone hands its complete slice to independent Code Review. The final whole-change checkpoint and distinct Verify follow all implementation and required corrections. Operational authority is never inferred from those gates. No delivery-duration estimate is committed until M1 establishes the actual missing-proof scope; test runtime measurements are evidence about execution, not an estimate of engineering effort.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-17 | Use the approved Markdown test designs and leave existing JSON catalogs unchanged. | The user's explicit clarification selects planning and preserves the useful reviewed coverage basis. | Refining/removing catalogs first, introducing a universal schema, or treating native discovery as the intended-test specification. |
| 2026-09-17 | Establish population first, then reporting and the complete measurement baseline before suite changes. | Missing callers and measurement-boundary differences would invalidate an apparent improvement. | Broad-smoke-only completeness, timing by scenario-link counts, or optimizing setup before measuring its current cost. |
| 2026-09-17 | Allocate proof by owning responsibility and retain explicit parent integration. | Fixtures, authority and recovery observations differ; owner slices provide understandable review and recovery units. | One undifferentiated test rewrite or a separate milestone for every test function. |
| 2026-09-17 | Use independent semantic procedures where the Design chooses them, with deterministic regression where executable behavior exists. | Structural checks and static wording cannot prove useful decisions or complete handoffs. | Fabricating automated realization, running live operations for completeness, or deferring applicable proof without an owner disposition. |

## Readiness

See the owning change record for current workflow state. This plan defines allocation and proof obligations; independent Delivery Review, implementation, milestone review, fresh whole-change Code Review and successful Verify remain separate gates.
