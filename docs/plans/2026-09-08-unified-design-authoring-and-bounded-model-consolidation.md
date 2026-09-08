# Unified Design Authoring and Bounded Model Consolidation

## Purpose / big picture

Deliver the approved unified authoring method and its first authority-consolidation slice as one coherent source/package/installation capability. Prepare installer safety separately, then switch the coupled authoring and consumer surfaces together. Completion includes the selected migration and actual local/integrated proof, with remaining consolidation explicitly assigned; it does not mean repository-wide migration or publication.

## Current Handoff Summary

- Owning change record: [change.json](../changes/2026-09-08-unified-design-authoring-and-bounded-model-consolidation/change.json).

Mutable lifecycle state, milestone state, review judgments, findings, command results, routing and closeout readiness live only in that record and its registered evidence. This plan records stable intent; work initialization requires independent Delivery Review of this exact primary plan.

## Source artifacts

- Proposal: [Unified Design Authoring](../proposals/2026-09-08-unified-design-authoring-and-bounded-model-consolidation.md), with its independently approved Proposal Review.
- Combined behavioral/technical Design: [Design](../design/design/design.md), [System](../design/system/system.md), scoped [Workflow](../design/workflow/workflow.md) convention transfer and [Target-native init](../../specs/target-native-init.md#scoped-design-amendment-managed-authoring-replacement), TNI-DES-01–06.
- Approved Design Review: [design-review-r5](../changes/2026-09-08-unified-design-authoring-and-bounded-model-consolidation/reviews/design-review-r5.json). Consume its exact four subjects, all resolved finding dispositions and recorded limitations; do not retarget that judgment if an engineering subject changes.
- Retained installer dependencies: [lockfile](../../specs/rigorloop-cli-lockfile.md) R46–R51; Target-native init TNI-R19–28/R72–75; [multi-adapter init](../../specs/multi-adapter-init-and-proxy-aware-download.md). Installation remains owned by these unmigrated contracts.
- Method displacement and decision sources: Design's complete R1–R124 and unnumbered-obligation maps, both named method ADRs, and System's exact mixed-architecture section map. These maps select the edits; the original documents are not blanket deletion targets.
- Shared governing dependencies: Constitution; Review and Closeout RC-SR-01–18; Test TEST-SR-01–13; Workflow coordination; Record Format and CLI recording mechanics. The applicable adopted profile retains stage boundaries and independently owned execution permissions.
- Prior-contract test specs: no new standalone test spec or test-spec stage. Retain independently applicable installer trust/drift/negative protection and the historical acceptance meaning of architecture-package-method.test.md, skill-contract.test.md and skill-invocation-commands-for-adapters.test.md. Retired author/gate names and historical record procedures do not become current execution prerequisites. This plan allocates the six installer SRs, eight exact feature boundaries and three interactions using verification groups; it does not replace or rename their feature-format record.

## Context and orientation

`skills/` is authored public content. `scripts/skill_validation.py` owns source validation and shared-resource expectations; `scripts/boundary_first_reference.py` and `specs/boundary-first-resources.yaml` own boundary-resource projection. `scripts/adapter_distribution.py` builds target archives and validates installed resources. The public installer is `packages/rigorloop/dist/bin/rigorloop.js`; its existing workflow-to-route replacement and `packages/rigorloop/test/cli.test.js` are a bounded feasibility/reuse basis, not proof of the new authoring transition.

The project map contains obsolete record-format descriptions, so this allocation uses direct inspection of these sources and tests rather than treating the map as current authority. Refresh only the affected map areas at cutover. Preserve the user's unrelated untracked `docs/design.zip` and all historical record bytes. The current branch also contains the approved proposal/Design authoring diff; final whole-change review includes that material alongside implementation.

### Concrete source allocation

M1 creates `packages/rigorloop/dist/lib/managed-authoring-replacement.js` and `packages/rigorloop/test/managed-authoring-replacement.test.js` for internal safety support. These are private implementation modules, not a new public command, schema or model. Existing installer behavior remains connected to its current implementation until M2. The helper's exact internal factoring belongs to implementation; a different contained file arrangement must retain this responsibility and be recorded in the milestone file disposition.

M2 owns the following exact surfaces. A brace list is an explicit list of sibling filenames, not a wildcard. Implementation evidence records changed/retained/deleted disposition and actual subject identity for each allocated path; an unchanged disposition needs inspected reason. A newly discovered directly required caller cannot be left broken: contain it within the same approved responsibility and reassess the affected diff, or return a changed milestone/behavior boundary to planning/Design before editing.

| Source set | Required disposition and proof |
| --- | --- |
| `skills/design/SKILL.md`; `skills/design/references/{model-authoring,technical-design,system-composition,legacy-source-reconciliation,boundary-first-method-v1,boundary-first-feature-authoring-v1,legacy-technical-authoring,governed-design-authoring,test-quality}.md`; `skills/design/assets/{design-skeleton,legacy-architecture-skeleton,legacy-adr-skeleton}.md`; `skills/design/assets/diagram-styles.mmd` | Create exactly the selected portable common/conditional contract and assets. Preserve complete example/decision/boundary method content and subject handoff. TG-02/TG-03. |
| Entire authored `skills/spec/` and `skills/architecture/` packages, enumerated below | Reconcile every material source responsibility before removing both packages and their old aliases. Retain Test/shared method substance in its named owner; do not concatenate the old manuals. TG-02/TG-05. |
| Consumer files enumerated below | Change normal authoring/correction routing and affected review/allocation language; preserve historical document names, retained feature format, distinct reviewers and v2 mechanics. TG-02/TG-03. |
| `templates/shared/requirement-to-delivery-model.md`; `templates/shared/boundary-first-compact-scan.md`; `specs/references/{boundary-first-method-v1,boundary-first-feature-authoring-v1}.md`; `specs/boundary-first-resources.yaml` | Reconcile actual author-role references and consumer projections at their source. Preserve vocabulary/format and unchanged adequacy rules. Update exact projections and pinned identities together through existing tooling; no private IDs in published guidance. TG-02/TG-05. |
| `templates/{architecture,adr}.md`, `templates/diagram-styles.mmd` | Retain contributor source aids and reconcile the matching installed conditional assets. Do not require repository templates from portable invocations. TG-03. |
| `scripts/{skill_validation,boundary_first_reference,boundary_first_validation,validation_selection}.py`; `scripts/{validate-skills,validate-boundary-first,validate-documentation-prose,build-skills,select-validation}.py` | Update inventories, resource triggers, projections, source-owner references and selection where affected. Preserve contained paths, model/example pairing, format discriminators and fail-closed unknown-value handling. Entry wrappers otherwise retain their behavior. TG-05. |
| `scripts/{test-skill-validator,test-build-skills,test-boundary-first-reference,test-boundary-first-validation,test-select-validation}.py`; `scripts/fixtures/boundary-first/semantic/progressive-cases.json` | Reconcile author selection and preserved negative/semantic fixtures; retain any independently protective historical-format cases. Add unknown-value regressions for changed closed sets. TG-05. |
| `scripts/{adapter_distribution,build-adapters,validate-adapters}.py`; `scripts/{test-adapter-distribution,test-npm-package-publication}.py`; `scripts/adapter_templates/{codex/AGENTS.md,claude/CLAUDE.md,opencode/AGENTS.md}`; `dist/adapters/{manifest.yaml,README.md}` | Generate one new authoring inventory for Codex, Claude and OpenCode, switch aliases and prove source/archive/install parity and contained transitive resources. Templates with no authoring reference remain unchanged after inspection. TG-03/TG-06. |
| `packages/rigorloop/dist/bin/rigorloop.js`; M1 private module; `packages/rigorloop/test/cli.test.js`; `packages/rigorloop/README.md`; `packages/rigorloop/dist/metadata/adapter-artifacts-v0.5.1.json` | Connect retired-entry guards and eligible managed replacement, diagnostics and documented operator sequence. Regenerate only current candidate metadata from actual generated archives using the existing builder; never invent hashes or rewrite historical metadata. Public-command proof in all targets covers aliases, multi-root state, failure, retry and unrelated-content preservation. TG-01/TG-04/TG-06. |
| `packages/rigorloop/dist/lib/workflow-context.js`; `packages/rigorloop/test/workflow-context.test.js`; `specs/workflow-skill-artifact-location-map.md` | Preserve existing model inspection and legacy placement metadata. Revise only a demonstrated current actor-reference mismatch; no new discovery kind, semantic dependency graph, readiness engine or record API. Record inspected unaffected disposition for unchanged mechanics. TG-02/TG-05. |
| `CONSTITUTION.md`, `AGENTS.md`; `specs/{skill-contract,rigorloop-workflow,skill-invocation-commands-for-adapters,boundary-first-proof-model}.md`; `specs/{target-native-init,multi-adapter-init-and-proxy-aware-download}.md` | Adopt the approved bounded method/invocation/installer amendments under their existing owners, retaining governance precedence and unmigrated contract scope. Replace the current Workflow-owned mapping reference in boundary-first-proof-model.md with its Design owner. Substantive legacy-format edits must retain their applicable feature-format procedure and receive owner review. No new behavior may be inferred in implementation. TG-04/TG-07. |
| `specs/architecture-package-method.md`, `specs/architecture-package-method.test.md`; `docs/architecture/system/architecture.md` | Add historical/replacement notice to the fully displaced method contract while preserving its body/IDs. In mixed architecture edit only System's selected sections and directly affected caller references; retain Level 2/unselected current owners and historical normalization meaning. TG-07. |
| `docs/adr/ADR-20260428-architecture-package-method.md`, `docs/adr/ADR-20260509-architecture-skill-surface-simplification.md` | Retain byte-identical historical decisions. Change only their current navigation summaries in mixed architecture to link replacement decisions. TG-07. |
| `docs/design/{design/design,system/system,workflow/workflow}.md` | Apply the approved ownership transfer and use them as current owner references at coordinated adoption. No implementation bookkeeping in models. A necessary semantic correction requires renewed Design Review, not self-approval. TG-07. |
| `README.md`, `docs/project-map.md`, `docs/follow-ups.md`, `specs/README.md`, `docs/plan.md` | Update affected current navigation, independently owned installation guidance and explicit later consolidation assignments. Preserve README vision block, other follow-ups, historical plan links and unrelated map content. TG-07. |

The current package is version 0.5.1; its candidate metadata exists, while there is no tracked v0.5.1 release report or release-note directory. Candidate generation/validation is in scope. Historical metadata files, release archives and prior review records stay unchanged. A separately authorized publication must choose and verify its release basis; this plan does not authorize that operation or claim a new release.

### Canonical authoring sources to retire

- `skills/architecture/SKILL.md`
- `skills/architecture/assets/adr-skeleton.md`
- `skills/architecture/assets/architecture-skeleton.md`
- `skills/architecture/assets/diagram-styles.mmd`
- `skills/architecture/references/architecture-package-method.md`
- `skills/architecture/references/governed-architecture-authoring.md`
- `skills/architecture/references/requirement-to-delivery-model.md`
- `skills/architecture/references/test-quality.md`
- `skills/spec/SKILL.md`
- `skills/spec/assets/spec-skeleton.md`
- `skills/spec/references/boundary-first-feature-authoring-v1.md`
- `skills/spec/references/boundary-first-method-v1.md`
- `skills/spec/references/governed-spec-authoring.md`
- `skills/spec/references/requirement-to-delivery-model.md`
- `skills/spec/references/test-quality.md`

### Exact current consumer files

The following table is the inspected authoring-reference closure. Paths are relative to the named `skills/` directory. Replace live author-role/normal invocation assumptions; a reference to a retained document contract or specialist technical concern remains legitimate. Preserve the explicit v2 recording procedures and all reviewer/Verify independence rules. Shared references are reconciled at the source and projected, not independently rewritten into conflicting copies.

| Skill directory | Exact files allocated to M2 |
| --- | --- |
| `skills/bugfix/` | `SKILL.md` |
| `skills/ci-maintenance/` | `SKILL.md` |
| `skills/code-review/` | `SKILL.md`, `references/boundary-first-method-v1.md`, `references/requirement-to-delivery-model.md`, `references/workflow-managed-automated-review.md` |
| `skills/constitution/` | `SKILL.md` |
| `skills/delivery-review/` | `SKILL.md`, `references/boundary-first-method-v1.md`, `references/boundary-first-proof-v1.md`, `references/requirement-to-delivery-model.md` |
| `skills/design-review/` | `SKILL.md`, `references/boundary-first-feature-authoring-v1.md`, `references/boundary-first-method-v1.md`, `references/requirement-to-delivery-model.md` |
| `skills/explore/` | `SKILL.md`, `references/option-discovery-methods.md` |
| `skills/implement/` | `SKILL.md`, `references/automated-review-correction.md`, `references/boundary-first-method-v1.md` |
| `skills/learn/` | `SKILL.md` |
| `skills/plan/` | `SKILL.md`, `assets/plan-skeleton.md`, `references/boundary-first-method-v1.md`, `references/requirement-to-delivery-model.md`, `references/security-and-authority-verification.md`, `references/state-machine-verification.md` |
| `skills/pr/` | `assets/pr-body-skeleton.md`, `references/governed-pr-readiness.md` |
| `skills/project-map/` | `SKILL.md` |
| `skills/proposal/` | `SKILL.md`, `references/requirement-to-delivery-model.md`, `references/strategic-and-scope-gates.md` |
| `skills/proposal-review/` | `SKILL.md`, `references/requirement-to-delivery-model.md` |
| `skills/research/` | `SKILL.md` |
| `skills/route/` | `SKILL.md`, `references/boundary-first-method-v1.md`, `references/bounded-workflow-automation.md` |
| `skills/verify/` | `SKILL.md`, `references/boundary-first-method-v1.md`, `references/branch-readiness-verification.md`, `references/requirement-to-delivery-model.md` |
| `skills/vision/` | `SKILL.md`, `references/strategic-vision-authoring.md` |

Retain historical artifact-class and retired protocol identifiers in `scripts/{artifact_lifecycle_contracts,artifact_lifecycle_validation,lifecycle_state_sync,workflow_automation,workflow_automation_policy,workflow_automation_state}.py`; these names are not new public author aliases and this plan does not reactivate their retired execution paths. Inspect `scripts/{test-token-cost-measurement,test-token-cost-report-validation}.py` for current-source fixture assumptions affected by removing skill paths; retain historical measurement identities/data, and amend only demonstrated current-inventory expectations with the full affected test module. No measurement campaign or historical report rewrite is required.

Unlisted resources with no authoring reference, such as current Test/review-policy application copies, retain their bytes and owners unless their existing consumer manifest needs the named inventory amendment. `skills/pr/SKILL.md` has no live old-author invocation to change; its two listed resources still require reconciliation. Historical automation protocol keys and archived contracts are not normal public invocation aliases.

## Non-goals

- No repository-wide document conversion, runtime record migration, automatic semantic dependency service, new lifecycle gate, public API/schema or broad force operation.
- No standalone test-spec stage or per-test ledger. Representative scenarios never authorize removing additional justified tests.
- No publication, push/PR/merge, release tag, customer adoption, real customer installation or edits to local installed runtime skills. Generated candidates and installation fixtures use disposable isolated directories.
- No whole-file deletion of mixed architecture, ADR rewriting, historical approval retargeting, unrelated CI redesign, quantitative token/runtime target or unrelated baseline cleanup.

## Requirements covered

| Governing obligations | Implementation allocation | Required proof |
| --- | --- | --- |
| DES-SR-01–06 | M2 common method, model/technical resources, unified invocation and decision-preservation maps | TG-02, TG-03, TG-07; TG-FINAL-01 |
| DES-SR-07–10 | M2 composition method, System relationships, scenario/assessment distinction and downstream allocation | TG-02, TG-03, TG-07; TG-FINAL-01 |
| DES-SR-11–14 | M2 model/example convention, exact displacement/decision map and retained legacy procedures | TG-03, TG-05, TG-07; TG-FINAL-01 |
| DES-SR-15–16 | M2 complete conditional installed resources, exact affected subject and independent review/Delivery handoffs | TG-02, TG-03, TG-06; TG-FINAL-01 |
| DES-SR-17 | M1 private safety support; M2 public guards, managed/unmanaged transition and package aliases | TG-01, TG-04, TG-06; TG-FINAL-02 |
| DES-SR-18–20 | M2 coordinated source/governance/validation adoption, preservation and assigned later work | TG-05, TG-06, TG-07; both final groups |
| SYS-SR-01–09 | M2 owner inventory, relationships, integrated authoring/install path, historical/state distinction, safe correction and bounded retirement | TG-02–07; both final groups |
| Workflow WF-SR-07/08/09 and affected WF-SR-14/15/17 coordination boundaries | M2 reference consumer and shared-authoring handoff | TG-02, TG-05, TG-07; TG-FINAL-01 |
| TNI-DES-01 | M2 candidate/installed entry and alias guard, managed versus unmanaged diagnostic | TG-04/TG-06 |
| TNI-DES-02–05 | M1 safety primitive evidence; M2 full command integration, original-hash eligibility, explicit authority, backup, transaction, conflict and recovery | TG-01/TG-04; TG-FINAL-02 |
| TNI-DES-06 | M2 unmanaged cleanup boundary and retained workflow-to-route behavior | TG-04/TG-06; TG-FINAL-02 |
| TNI-R19–28/R72–75 and lockfile R46–R51 | M1/M2 retained state/hash/mutation invariants | TG-01/TG-04; TG-FINAL-02 |
| DES-DEC-01–05, SYS-DEC-01–03; mapped architecture-method R1–R124 and unnumbered obligations; two historical ADRs | M2 exact mapped reconciliation, embedded rationale and historical disposition | TG-07 and independent semantic migration review |
| TEST-SR-01–13 and RC-SR-01–18 | Apply throughout; retain protective value, evidence applicability, original reporter disposition and independent final closeout | Group-level test-maintenance rationale, milestone reviews, final whole-change review and separate Verify |

### Retained installer boundary allocation

All identifiers below are source-qualified to Target-native init's scoped TNI-DES record. Coverage here means required allocation, not executed evidence or a passing result.

| Exact boundary or interaction | Earliest local proof | Required integrated proof and observation |
| --- | --- | --- |
| BND-INPUT-001 | M2 / TG-04 | Invalid/retired/trust-failing candidate and valid clean inventory through public init; no target/state writes on rejection. |
| BND-STATE-001 | M1 / TG-01 | M2 / TG-04 and TG-FINAL-02: matching old, matching new, drifted and partial target/state pairs; original/new hashes and exact bytes. |
| BND-AUTH-001 | M1 / TG-01 | M2 / TG-04: ordinary/dry-run/explicit replacement, managed/unmanaged/ambiguous ownership, no scope expansion or inferred removal. |
| BND-COMPOSE-001 | M1 / TG-01 | M2 / TG-04/TG-06: archive, skills, OpenCode commands, other targets and shared state preserve coherent ownership. |
| BND-TEMPORAL-001 | M1 / TG-01 | M2 / TG-04 and TG-FINAL-02: final prewrite recheck, intervening writer, completed retry and interrupted recovery. |
| BND-RECOVERY-001 | M1 / TG-01 | M2 / TG-04 and TG-FINAL-02: caught failure, rollback failure, interruption and original-backup recovery without silently refreshing hashes. |
| BND-COMPAT-001 | M2 / TG-04 | TG-FINAL-02: managed old upgrade without pre-deletion; unmanaged cleanup cannot bypass a recorded basis; retained workflow-to-route path. |
| BND-ENV-001 | M1 / TG-01 | M2 / TG-04: symlinks, unsafe/missing roots, external backup and filesystem/state-write failures; zero unauthorized mutation. |
| INT-001 | M2 / TG-04 | TG-FINAL-02: original locked tree, clean verified candidate and new state basis cooperate; reproduce the would-be manual-predelete drift trap as a negative contrast. |
| INT-002 | M1 / TG-01 | M2 / TG-04 and TG-FINAL-02: interrupted publish/rollback cannot overwrite independent state or accept a partial tree. |
| INT-003 | M2 / TG-04 | TG-FINAL-02: state-implicated/overlapping roots cannot take the unmanaged cleanup bypass. |

## Milestones

### M1. Prepare bounded managed-replacement safety

- Milestone kind: implementation.
- Engineering purpose: isolate filesystem/state safety from the cross-repository authoring cutover while preserving the current public installer.
- Requirements: TNI-DES-02–05; retained TNI/lockfile invariants; supporting DES-SR-17 and SYS-SR-09.
- Architecture responsibility: installation-owned scoped amendment; original tree basis, selected-root transaction and conflict-aware recovery. No transfer to the CLI recording model.
- Dependencies: approved exact Design and Delivery packages; implementation authority for this milestone.
- Implementation scope: the two named private module/test files. Reuse existing trust/hash/state utilities only where it preserves their contract; no connection to normal init, old-skill removal or public capability claim yet.
- Files/components likely touched: `packages/rigorloop/dist/lib/managed-authoring-replacement.js`, `packages/rigorloop/test/managed-authoring-replacement.test.js`. Any extraction needed from `dist/bin/rigorloop.js` requires unchanged public behavior and complete CLI regression proof.
- Required verification: TG-01 — unchanged original basis, selected-root scope, safe staging, multi-root/state rollback and intervention detection.
- Evidence expectations: deterministic fixtures for before/after bytes and failure injection at stage, publication, installed verification, each state write and rollback; preserve competing content. Unit/helper evidence is explicitly limited to the private boundary.
- Implementation steps: author protective cases first; implement the contained mechanism; exercise each materially distinct failure/authority path; run complete affected modules and record limitations.
- Validation commands: V1; V2 if shared installer utilities change; V7 for record integrity.
- Expected observable result: internal support satisfies its allocated safety invariants; current public init and workflow-to-route behavior remain unchanged.
- Completion criteria: all TG-01 outcomes demonstrated, no connected new authoring entrypoint, no lost existing protection, independent milestone review and required corrections resolved.
- Required evidence: implementation-owned exact code/test/fixture subjects, commands/results, failure-detection rationale and reviewer basis in the owning records.
- Review handoff: independent Code Review of the entire M1 diff and its unchanged-public-path claim. This is not approval of the future authoring upgrade.
- Optional commit boundary: `M1: prepare bounded managed authoring replacement safety`.
- Risks: unsafe snapshots, symlink following, stale shared-state restore, or a helper proof misrepresented as public-path proof.
- Rollback/recovery: revert the unconnected support/test unit under source authority. Preserve user work and historical evidence; a helper correction requires affected tests/review again.

### M2. Cut over authoring, consumers and the selected authorities together

- Milestone kind: implementation.
- Engineering purpose: one coherent replacement across skill names, semantic consumers, projections, installer dispatch, package metadata and authority navigation. Splitting these into independently complete public transitions would recreate the contradictions this Design removes.
- Requirements: DES-SR-01–20; SYS-SR-01–09; scoped Workflow references; TNI-DES-01–06; retained installation/Test/Review obligations above.
- Architecture responsibility: DES-DEC-01–05 and SYS-DEC-01–03; exact method/system migration maps; independent installation-owner procedure.
- Dependencies: reviewed M1; approved Design/Delivery basis; current exact consumer inventory and untouched historical source identities.
- Implementation scope: the concrete M2 source allocation and consumer closure. Reconcile the skill and resources, replace normal invocations/aliases, connect guards and managed replacement, update validators/projections and candidate metadata, apply bounded source notices/navigation and assign follow-ups. Add concrete fixtures/assertions and public/installed proof with the capability they verify.
- Files/components likely touched: all M2 rows above and only justified contained callers discovered through their imports/resource maps. No hand-edited generated adapter bodies or local runtime skill installation.
- Required verification: TG-02–07 plus TG-FINAL-01/02 at the first point the complete candidate exists. Repeat only proof defeated by later changes; final whole-change review remains separately fresh.
- Evidence expectations: exact file dispositions; source-to-destination obligation/decision reconciliation; reviewer-owned walkthrough evidence for semantic claims; actual three-target candidate generation, clean installed resource checks and public init/upgrade/recovery tests. Record every failure and limitation rather than substituting source assertions for execution.
- Implementation steps: establish tests against the approved requirements; reconcile shared sources/resources; update skill consumers and validators in the same candidate; connect the installer; generate measured metadata and archives; apply the exact historical/mixed authority notices; Route assigns follow-ups; execute local and integrated groups; hand the complete candidate diff to independent review.
- Validation commands: V1–V8; V9 release verification only under its stated publication trigger. Use the changed-path selector to discover any additional required maintained checks without inventing a separate validation flow.
- Expected observable result: one portable `design` authoring path, exact model/legacy review and Delivery handoff, an executable authorized managed upgrade, and one current owner per migrated obligation. Unmigrated responsibilities and historical evidence remain distinguishable.
- Completion criteria: full consumer closure and exact migration maps reconciled; all required local/integrated outcomes evidenced; no unresolved required correction or contradictory current authority; separately reviewed governing changes; durable later-work assignments; independent milestone review completed. No candidate publication or customer adoption is implied.
- Required evidence: current implementation/evidence records, named semantic walkthroughs, generated archive identities and fixture transcripts, exact full diff, independently assessed concern dispositions and test-maintenance rationale.
- Review handoff: independent Code Review of the entire coordinated cutover and M1 integration. Review can inspect logical facets separately, but one complete milestone judgment must cover their interaction. A facet-only review cannot close M2.
- Optional commit boundary: `M2: adopt unified authoring and bounded model ownership` after the coherent candidate is complete. Partial commits are implementation history only; do not publish/install them as a supported transition.
- Risks: high file count from replicated consumer guidance, stale projection hashes, an omitted legacy method, premature supersession, incorrect backup guidance or an installer guard that breaks every current archive before candidate metadata is aligned.
- Rollback/recovery: before adoption revert the whole unadopted coupled source/metadata unit, not one old skill beside `design`. Generated outputs are disposable and recreated from the retained source. After adoption use the Design's authorized coherent reversal/forward correction; installed recovery follows TNI-DES-05 and preserves unrelated changes. If the cutover cannot be independently reviewed as this bounded responsibility, replan before splitting its acceptance boundary.

### M3. Rename the document marker and demonstrate its contract

- Scope: user-requested `model-document-v1` rename and the indexed fenced example in the owning Design. Preserve structural rules, stored `rigorloop-records-v2`, targeted transport versions and historical records. Current model documents, validator, authoring resource/skeleton and measured candidate metadata change together.
- Dependencies: independent approval of the revised model set and this Delivery addendum; M1/M2 implementation remains unchanged.
- Requirements: DES-SR-09/11/12/16/19 and the model-document structural/transition/example contract; no new runtime record format or automatic customer-document migration.
- Implementation: update validator dispatch and diagnostics; update current authoring resources; add regression proof for the new marker, retired/unknown/missing/duplicate markers and the fenced example. Update the seven living-model declarations and current boundary-method consumer. Rebuild the same supported adapter set into a new empty task directory and regenerate current local-candidate metadata using the existing archive-measurement helper; do not hand-edit archive bodies or historical metadata.
- Verification: V3/V4/V6 for affected source/model/prose/selector checks; validate the extracted example directly as a hypothetical model and reject an invalid-marker variant. V5/V8 for current candidate generation, clean installation and metadata coherence. Rerun the selector's maintained checks. Repeat the installed authoring walkthrough against the changed guidance and candidate; retain other prior proof only with independent unaffected-basis assessment. Public managed-installation/recovery proof must use the revised candidate where archive identity is material. No broad smoke or release-only V9 without their existing triggers.
- Acceptance: no live document declaration or current authoring instruction selects the retired marker; old/unknown markers fail before table validation; the new example and parent each validate with exactly one live declaration. All eight dimensions, model-local references and illustrative scope are reviewable. Packages provide the current marker guidance without internal checkout; historical v1 stored-record names and exact approvals remain historical.
- Evidence: actual command results and new exact subjects/candidate identities in existing v2 records; independent M3 review, then fresh complete whole-change Code Review and distinct Verify before updating the existing PR.
- Recovery: restore the coherent document/validator/guidance/candidate set together if the rename is not adopted. Never change a historical record or rewrite customer model files through installation. An incompatible or interrupted customer edit is corrected under that project's document owner.

## Verification groups

| Group | Required claim, representative conditions and distinguishing oracle | Commands / evidence owner |
| --- | --- | --- |
| TG-01 | Private replacement operates only on the verified unchanged selected basis. Changed hashes, unsafe roots and ambiguous state reject. Stage/verify/write/rollback failures and a competing writer preserve either a coherent original pair or explicit conflict/partial recovery without overwriting independent bytes. | M1: V1, implementation-owned fixtures/results; independent Code Review inspects detection and authority boundaries. |
| TG-02 | Normal descriptions/routing/correction refer to one `design` author, while Design Review selects exact affected models, retained legacy members, examples and interactions. A material behavior/feasibility conflict returns to the direction owner. Recording and structural success grant no approval; retained stage/record/placement meanings are not renamed by text replacement. | M2: V3/V4 and MW-01; Code Review assesses common and triggered paths, with exact counterexamples. |
| TG-03 | Installed common/new-model, multi-owner, example, substantive legacy-feature and required legacy-architecture/ADR scaffold paths resolve every triggered resource without internal checkout. Missing package guidance differs from missing customer authority. Examples preserve parent indexing, parse/schema limits and before/after invariants. MW-01 separately checks a changed relied-on example with an unchanged parent: exact subject selection/handoff and required reassessment before current reliance. | M2: V3/V5 plus MW-01; missing-resource negatives and artifact/expectation inspection. Local parsing cannot establish an illustrated invariant or author judgment. |
| TG-04 | Public init in Codex/Claude/OpenCode rejects retired candidates and ordinary old/mixed installs before writes. Eligible managed old roots upgrade only with original hashes/authorization; modified entries, additional files, missing roots, symlinks, conflicting state and unmanaged bypass attempts block unchanged. Test dry-run, both OpenCode roots/aliases, unrelated targets/state, completed idempotent retry, pre-delete drift contrast, caught failure and process interruption through the documented backup restoration. | M2: V1/V2 and TG-FINAL-02; real subprocess/filesystem fixture assertions at public output and persistent bytes. Preserve existing trust/legacy-state/workflow-to-route regressions. |
| TG-05 | Inventory, resource projections, model/example selectors, exact source identities and validators agree. Unknown closed values/markers, missing references, escaped paths and malformed model/example content fail closed; unmarked grandfathered handling retains semantic classification. Every installer example requirement is governed by every cited boundary, beyond the existing validator's overlap check. | M2: V3/V4/V6; group-level retain/strengthen/replace/remove rationale applies Test criteria. No test is removed merely because it names an old skill or is absent from representative scenarios. |
| TG-06 | Generated supported archives omit both retired directories/aliases, include one author and complete conditional assets, and match measured current candidate metadata. Clean install and managed upgrade use the same candidate. Tampered/traversing/untrusted archives reject; private source paths/policy IDs do not leak into shipped guidance. | M2: V2/V5/V8; implementation records source/archive/tree identities, with distinct public-path assertions. |
| TG-07 | All architecture-method R1–R124, unnumbered obligations, meaningful decisions and exact mixed-system sections have the approved destination/retention. Full superseded method sources have historical notices; mixed sources retain unmigrated owners. ADR bytes and historical reviews are preserved. Each of the three System follow-up families has maintainer accountability, a receiving owner and durable next action. | M2: V6/V7 and MW-02; independent migration/Code Review judges semantic preservation, not just identifier counts. |

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: all in-scope implementation milestones (M1–M3) and all required corrections complete, including integrated evidence and durable follow-up assignments.
- Assessment: fresh independent final whole-change Code Review of the complete delivered engineering change, including proposal/Design/Delivery artifacts, implementation and cross-milestone interactions. Earlier milestone reviews inform but do not replace it.
- Evidence: exact final subjects, complete diff, independent reviewer basis, current proof and all required concern dispositions.
- Successor: distinct final Verify. Corrections return to the owning stage and require affected reassessment; only successful Verify owns the final explanation and completion assessment.

This checkpoint is not an implementation milestone or a place to defer in-scope work. No verification-group non-applicability rationale waives it.

## Change-level verification

### TG-FINAL-01. Composed authoring and bounded authority migration

- Covers: M2; DES-SR-01–16/18–20; SYS-SR-01–09; Workflow convention and independent assessment boundaries.
- Demonstrate: in an isolated project with installed candidate resources, a selected change updates the smallest affected model set, coordinates a shared-contract consumer, exposes representative local/integrated outcomes and hands exact model/example/legacy subjects to independent review and Delivery. A second path substantively amends an unmigrated feature under its declared format; no internal checkout, forced migration, independent old author or accidental approval is needed. Validate the complete current navigation/source map and owned follow-up dispositions.
- Evidence expectations: V3–V8 plus MW-01/02 with exact candidate/source subjects, emitted artifacts, counterexamples and assessor-owned conclusions. Actual recording results use existing v2 records; no new lifecycle service or target-agent correctness claim.
- Non-applicability: none; local resource or model checks cannot establish the composed semantic handoff or migration ownership.

### TG-FINAL-02. Managed installation reaches a coherent replacement safely

- Covers: M1/M2; DES-SR-17/18; SYS-SR-05/09; TNI-DES-01–06 and all three selected installer interactions.
- Demonstrate: run the complete documented clean-managed sequence against the exact new candidate, contrasting local modifications and interrupted cleanup/replacement/retry. Observe both target roots where applicable, selected and unrelated state entries, retained backup, installed hashes/counts and diagnostic scope. Detect a competing shared-state write before publication/rollback; preserve that write and report conflict. Restore a coherent original basis under explicit authority and retry successfully. A completed new pair retries idempotently; a partial pair cannot be blessed by `--write-state` or lock deletion.
- Evidence expectations: V1/V2/V5/V8 plus MW-03. Automated subprocess tests must exercise actual public dispatch and controlled failure points; helper-only, mock-only and dry-run-only results are insufficient. Record the generated old/new fixture bases independently of production expected-output calculation.
- Non-applicability: none; guard rejection without a demonstrated successful authorized upgrade leaves the original integration gap unresolved.

## Validation plan

These are required commands for implementation, not authoring-time results. Run the smallest affected group first, fix a new failure before proceeding and then run the full affected module. Preserve useful existing negative/regression protection; do not update expected snapshots solely from changed production output. Record actual commands, exit status, subject/environment identities and limitations in stage-owned evidence.

| ID | Concrete commands and purpose |
| --- | --- |
| V1 | `node --test packages/rigorloop/test/managed-authoring-replacement.test.js` — new M1 private safety module, rerun on relevant M2 changes. |
| V2 | `node --test packages/rigorloop/test/cli.test.js packages/rigorloop/test/workflow-context.test.js`; `npm test --prefix packages/rigorloop` — complete public installer/context suites and surrounding Node discovery after integration/shared changes. |
| V3 | `python scripts/validate-skills.py`; `python scripts/test-skill-validator.py`; `python scripts/test-build-skills.py`; `python scripts/test-boundary-first-reference.py` — public source contract, exact triggered resources, shared projection/consumer inventory and retained negative protection. |
| V4 | `python scripts/test-boundary-first-validation.py`; `python scripts/test-select-validation.py`; `python scripts/test-documentation-prose-validator.py`; `python scripts/test-markdown-readability-validator.py` — preserved structural format, selectors and validation behavior where affected. |
| V5 | `python scripts/build-adapters.py --version v0.5.1 --output-dir /tmp/rigorloop-unified-design-candidate`; `python scripts/validate-adapters.py --version v0.5.1 --adapter-root /tmp/rigorloop-unified-design-candidate --clean-install-smoke --skill design --skill design-review --skill plan`; `python scripts/test-adapter-distribution.py` — isolated candidate archives, installed resource closure and surrounding generation/installation tests. Reserve a new empty task directory before generation; never reuse unknown contents. |
| V6 | `python scripts/validate-boundary-first.py --path docs/design/design/design.md --path docs/design/system/system.md --path docs/design/workflow/workflow.md --path specs/target-native-init.md`; `python scripts/validate-documentation-prose.py --mode enforce --path docs/plans/2026-09-08-unified-design-authoring-and-bounded-model-consolidation.md --path docs/design/design/design.md --path docs/design/system/system.md --path docs/design/workflow/workflow.md`; `python scripts/validate-markdown-readability.py --generated-document docs/design/design/design.md --generated-document docs/design/system/system.md docs/design/design/design.md docs/design/system/system.md docs/design/workflow/workflow.md specs/target-native-init.md docs/plans/2026-09-08-unified-design-authoring-and-bounded-model-consolidation.md` — repeat with other actually changed governed paths as selected. |
| V7 | `node scripts/validate-record-store.mjs docs/changes/2026-09-08-unified-design-authoring-and-bounded-model-consolidation/change.json`; `git diff --check` — current record integrity and whitespace, not semantic approval. |
| V8 | `python scripts/test-npm-package-publication.py`; `python scripts/validate-npm-package.py` — package metadata/trust coherence and retained packaging tests. Use existing metadata generation from measured archives, not a hand-built claimed release report. |
| V9 | Separately authorized release only: `bash scripts/release-verify.sh v0.5.1` and `python scripts/validate-release.py --version v0.5.1` after the release owner supplies the supported release target, tracked release notes/report and exact release basis. The current shell gate does not accept v0.5.1 and no release report exists; do not broaden its allowlist or fabricate history to make this non-release initiative pass a publication gate. Candidate validation V5/V8 remains mandatory here. |

Use `python scripts/select-validation.py --mode explicit --path PATH` for every actual affected path and consume the union of selected maintained checks. PATH means the concrete inspected source, not a literal command argument. If a selected check executes a retired procedure or depends on unavailable release authority, record the exact result and route its applicability to the owning assessor; do not silently substitute a smaller suite or claim success. Broad CI smoke runs only on the existing classifier's actual trigger. `.github/workflows/ci.yml` is an inspected CI consumer; CI maintenance is conditional on a demonstrated coverage gap, with a bounded reviewed correction before final whole-change review. Release workflows remain outside this non-publication scope.

The approved Design evidence records 13 unchanged prose errors in historical Target-native init examples. Retain the original historical body and independently compare any full-file prose failure to that recorded baseline; new errors block correction closure. This scoped limitation is evidence for assessors, not a blanket waiver for touched documentation or future Verify. Missing real implementation proof cannot be categorized as baseline debt.

### Manual and operational evidence

| Procedure | Environment, bounded action and expected observation | Owner, durable evidence and freshness |
| --- | --- | --- |
| MW-01 | Use disposable customer projects without RigorLoop's internal checkout and each supported installed candidate. Walk the common model path, shared-contract change, substantive retained feature-format amendment and conditional architecture/ADR scaffold use. Include a material product-direction constraint, missing packaged method versus missing project authority, and a parseable but invariant-breaking example pair. Separately, change a relied-on example while leaving its parent model unchanged. Confirm that selection and handoff include the affected example and its owner, identify the example’s new exact subject, and do not treat the unchanged parent or earlier approval as sufficient for current reliance before required reassessment. Mechanical selection supplies subjects; responsible actors judge applicability and reassessment under the existing review policy, without automatic CLI invalidation or another review gate. Inspect the selected resources and resulting artifact/subject handoff against the contract. Static presence checks cannot decide semantic sufficiency. | Independent nonauthor reviewer under Code Review; implementation supplies candidate/fixtures. Record bounded actions, resource selection, artifacts, counterexamples and conclusions in current evidence. Expires when relied-on content, trigger, fixture authority or candidate identity changes. No target-agent performance or deterministic model-judgment claim. |
| MW-02 | Compare the exact approved displacement maps against the final notice/owner/decision diff. Trace each material numbered and unnumbered obligation and each selected system section; inspect unchanged ADR bytes and distinguish old approvals from current evidence. Resolve all three System follow-up families to actual existing owners or Route-created register entries. | Independent reviewer judges migration preservation; Route owns follow-up assignments in `docs/follow-ups.md` using its next available IDs. Repository maintainer is accountable; receiving proposal/Design owner and next decision are explicit. Reassess on mapped source/destination/reference changes. |
| MW-03 | In disposable managed fixtures, execute the documented operator sequence using the real CLI and same candidate as V5. Preserve backup outside roots, authorize exact replacement, inspect untouched original hash, test normal completion and recover controlled interrupted/partial cases. Compare target/state/neighbor bytes with expected contract-derived results and preserve simulated independent writes. No real customer filesystem is involved. | Implementation records actual command transcripts, fixture/backup identities and comparisons; independent Code Review assesses them. Automated public-path tests supply repeatability; the walkthrough checks that the published instructions can be followed completely. Expires on relevant installer/candidate/state-contract/procedure changes. |

## Risks and recovery

- The coordinated cutover touches many small consumers. Keep the exact path disposition visible and inspect transitive resources before declaring closure; a search hit is neither automatic rewrite authority nor proof that another path is unaffected.
- Retired names in historical contracts, protected tests and storage keys are not uniformly obsolete. Establish replacement protection first and retain unknown-value, drift, no-write, recovery and independent-review safeguards.
- If a concrete technical choice requires changing approved behavior or a governing amendment, stop dependent implementation and return to Design; renew exact assessments rather than allocating an inferred solution here.
- Candidate metadata changes require new measured archives and trust checks. Historical releases and user backups remain immutable; no direct install/publish action follows from a package pass.

## Dependencies

- Delivery Review of this exact primary plan precedes work initialization and implementation.
- M2 depends on reviewed M1. All integrated groups and owned follow-up entries precede final whole-change review; final Verify remains distinct.
- Route assigns later consolidation to three durable families: skill/resource/validation architecture; installation/distribution/release models; remaining feature/Level 2/ADR/automation/observability/measurement inventory. Existing active owners are referenced; otherwise Route creates explicit follow-up entries. No part of the required present consumer reconciliation is deferred with those families.
- Review results, actual validation and mutable work remain in existing v2 records. A save or installed package never grants approval, publication or customer adoption.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-08 | Prepare private installer safety before the coordinated cutover. | Local failures/concurrency can be isolated without immediately rejecting the existing released inventory. Full public-path proof belongs at connection in M2. | An early unconditional guard would block old candidate archives before a coherent replacement is available; helper tests alone would not prove the user procedure. |
| 2026-09-08 | Keep the connected name/resource/consumer/authority switch one closeable milestone. | A separately complete rename leaves competing instructions or missing installed methods. Logical review facets retain inspectability while the final judgment covers their composition. | Eagerly adding a competing public author, publishing partial source packages, or making artificial test-only milestones to disguise unfinished integration. |
| 2026-09-08 | Allocate semantic walkthroughs alongside automated source/archive/public-command checks. | Coherent decisions, correct source ownership and sufficient guidance cannot be established by file presence or structural validation alone. | Universal target-agent correctness claims, a new readiness engine, or deferring integration evidence to a release not authorized here. |

## Readiness

See the owning change record for current workflow state. This plan does not claim implementation, adoption, review approval, final verification or publication.
