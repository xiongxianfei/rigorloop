# Cleanup source disposition

This is author-owned evidence for [the cleanup change](change.json), interpreted under [Engineering ENG-SR-13/14](../../design/engineering/engineering.md#repository-retirement). It is not an additional normative model, permanent ledger or execution report. The first 12 mapped documents have been removed in the user-authorized Design diff; exact recoverable identities and reference updates are recorded in [design-source-removal.json](evidence/design-source-removal.json). A second user-authorized batch removes 14 method/skill documents and archive copies; [second-removal.json](evidence/second-removal.json) records its exact identities and consumer changes. Other selections remain proposed.

Baseline commit: `39b7c5cb1f03aa761d2f2493d3474ce985e59d6f`. [source-inventory.tsv](source-inventory.tsv) freezes exact tracked candidate paths and content identities, plus historical record roots. New files and concurrent changes require reconciliation before relying on this set. Inventory labels select the outcomes below, not approval or completed work.

## Exact selected retirements

| Inventory disposition | Sources | Surviving meaning and owner | Required consumer reconciliation |
| --- | --- | --- | --- |
| remove-archive-copy | Five files under `docs/archive/skill-model/2026-09-08/` | The complete Skill source maps preserve readability, portability and resource-integrity meaning. The mixed current `specs/skill-contract.md` keeps its existing remainder. Original byte identities and judgments remain recoverable at the baseline commit. | Replace current archive-navigation links with Skill/current owners or historical commit/path provenance; do not rewrite old reviews. |
| remove-mapped-common-source | `specs/skill-readability-contract.md`, `specs/customer-portable-public-skill-evidence.md`, `docs/adr/ADR-20260623-published-skill-resource-integrity.md` | Skill's existing “Readability and portability reconciliation” maps every numbered clause, unnumbered acceptance intent and the ADR decision to SKL-SR-03/05/06/08/09/12–15 and SKL-DEC-02 with their original applicability. Historical rollout lists, version choices and completed measurements remain historical. | Current guidance, validators and expected-source lists use Skill. Keep actual role/resource/enum/portability/quality failures. No global conformance claim or new universal heading rule. |
| remove-mapped-proof-document | Matching `.test.md` files for the two common sources above | Readability T1–16 and portability T1–13 are proof allocation for those historical initiatives. Current static content/resource, cold-read, semantic quality, measurement and package obligations follow the mapped Skill clauses, Validation and Packaging; exact historical commands and rollout scopes do not become current gates. | Keep meaningful current `test-skill-validator.py`, adapter and token behavior cases. Remove only original-path/file-shape dependencies after the current owner and proof remain accessible. Unique unresolved current proof intent blocks the affected document's removal. |
| remove-retired-stage-design | `docs/architecture/2026-06-25-independent-test-spec-review-gate.md`, `docs/adr/ADR-20260625-independent-test-spec-review-gate.md` | The dedicated test-spec stage and gate are retired. Architecture requirements R1–12/25–28's stage/package introductions are superseded by Workflow's consolidated gates; R13–18's proof adequacy goes to Delivery Review and Validation; R19–24's freshness, correction and recording go to Assessment and CLI Records. The ADR's underlying reason—independent proof assessment before implementation—survives through Delivery Review. Its rejected plan-review alternative assumed the old ordering and does not reject current combined Delivery Review. | Current navigation must not route to retired skills or old handoff enums. Preserve closed-value rejection, review independence, portable packaging and required final Code Review/Verify. Related mixed specs remain explicit retained sources below. |
| remove-generated-support | `dist/adapters/README.md`, `dist/adapters/manifest.yaml` | DIST-SR-21/22 preserve generated manifest shape and integrity; the existing package README receives installation/upgrade guidance. No replacement tracked manifest or new adapter directory. | Builder no-output write mode rejects; `--check` uses temporary candidate output; explicit `--output-dir` persists artifacts. Reconcile release/report paths, selectors, checks and current guide links. Keep raw resources and actual packed installer proof. |
| remove-exclusive-check | `scripts/retirement_ledger.py`, `scripts/test-retirement-ledger.py`, `scripts/test-fidelity-gate-spec-reads.py` | VAL-SR-23 retires the historical ledger schema/dual-proof inventory and fixed spec-read-log instrumentation, while TEST-SR-04/05/07–10/12 and VAL-SR-03–05 preserve meaningful current checks. | Remove `main.retirement_ledger.regression` and `requirement_fidelity.spec_reads`, fingerprints, imports, exclusive fixtures and routing expectations. Preserve current catalog completeness, missing/unknown values and substantive fidelity negatives. |
| remove-exclusive-fixture | August 10 `retirement-ledger.json`; `tests/fixtures/requirement-fidelity-gate/representative-reviews/r26-matrix-pilot/spec-read-log.json` | Frozen historical claims have no current executable reader after VAL-SR-23. | Remove with their readers; retain other requirement-fidelity fixtures and record-retirement protection. |
| retire-historical-report-input | Existing tracked `docs/reports/**` at the baseline | REL-SR-25 retires completed-release replay and historical production-report presence as current validation prerequisites. VAL-SR-24 retires the exact May 10 baseline and May 14 M4 historical existence/wording assertions. Report parsing, measurement, future production and currently relied-on candidate evidence remain supported. | Refactor current parser/adapter tests to owned fixtures; remove replay-only branches and original-path assertions; convert current provenance references. Any actual current release/assessment reliance must be preserved or coherently replaced before the affected file is removed. A directory may reappear for future actual evidence. |
| retire-historical-root | Baseline change directories other than the current v3 population, enumerated in the inventory | Completed judgments and original identities remain in Git. Original record format no longer supplies runtime authority. | Reconcile active registry/evidence consumers and current model provenance; replace tests importing finished production packs with justified current fixtures. Preserve current format rejection and discovery of malformed current stores. Noncurrent discovery alone does not prove a root unused. |

The report and historical-root selections require current-reliance closure rather than a blanket recursive deletion. Neither a source citation nor a byte-identical copy alone supplies that closure. Delivery must allocate this dependency work as part of the selected removal, not treat discovered readers as permission to silently drop a family.

## Retained operational inputs and unmapped sources

| Inventory disposition | Exact boundary | Concrete retained need and owner |
| --- | --- | --- |
| hold-unmapped-source | Other top-level `specs/*.md`, excluding the selected common sources and navigation index | These files require clause-level reconciliation against current owner maps before deciding whether they are wholly historical or retain mixed/unmigrated requirements. This cleanup does not treat publication of the model hierarchy as blanket migration of every specialist skill, measurement, boundary method, workflow automation or CLI contract. The inventory owner field names the source requiring reconciliation, not a new judgment that all its clauses remain authoritative. |
| hold-unmapped-proof | Other `specs/*.test.md` | Proof intent must be reconciled with the matching feature contract and current owner; retired test-spec authoring does not establish that all distinct edge cases were adopted elsewhere. They do not create a current test-spec lifecycle stage or require replaying old milestone commands. Removing these needs an explicit later Design amendment within this cleanup, not implementation guessing. |
| hold-unmapped-design | Other ADR and architecture files, including `docs/architecture/system/architecture.md` and its diagrams | Technical decisions and mixed responsibility descriptions require source-qualified reconciliation; existing authority applies only within their actual retained scope. Current owners are discoverable from System; file age alone cannot retire their remaining contracts. They are not copied into another archive. |
| retain-operational-reference | The three `specs/references/boundary-first-*.md` files plus `specs/boundary-first-resources.yaml` and `specs/boundary-first-activation.yaml` | Current raw-byte projection, manifest identity, adopted boundary-method applicability and mapped published resources consume these inputs. Keep exact current resource bytes and projection targets. Moving their source root adds no cleanup value without a separate canonical-resource ownership change. |
| retain-operational-tooling | All other tracked `scripts/**` | Current validators, test suites, generators, measurement, reports and release execution remain supported. Only the named exclusive checks and historical-only assertions retire. Do not infer redundancy from script count or age; current behavior and actual failure detection still require these owners. |
| retain-current-record-root | The three baseline v3 roots plus this cleanup root | Current adopted-model, record-retirement and parallel-test provenance/evidence remain available while current Design and assessments rely on them; this change adds its own live work. This is current reliance, not indefinite historical retention. |

These retained exceptions are an explicit scope limitation of this Design package. They preserve the approved broad initiative, but **do not establish that repository-wide legacy contract consolidation is complete**. Before a plan may claim the entire cleanup, Design must finish the clause/proof transfers for any remaining sources selected for removal and resolve the report/root live-reliance closure. The present exact mapped removals and behavioral changes can be independently assessed without granting deletion authority for the retained remainder. No hidden follow-up or unassessed source is labeled retired.

## Additional audited source dispositions

The following complete-source selections use existing owner maps with explicit retirement of obsolete mechanics. Their matching proof documents may retire only after current negative, compatibility and recovery proof is preserved. No executable test is selected merely because its former source is removed.

| Selected source family | Exact clause disposition and current owner |
| --- | --- |
| `architecture-package-method.md` and its test spec | Design's existing selected replacement map covers R1–124, AC1–22 and E1–10 through DES-SR-01–20. Diagram, decision, template and review intent survives; historical package topology does not. Related ADRs remain separately assessed. |
| `compact-current-state-change-record.md`, September 3 architecture and transaction ADR | SR02/03 → WF-MAP-03; SR07–13/47 → WF-MAP-04; SR14–18 → WF-MAP-05; SR32/34–36/48 → WF-MAP-06; SR19–25/46 → CLI-MAP-01; SR26–31 → CLI-MAP-02; SR33/37–39 → CLI-MAP-03. SR40–45's old digest, envelope, recovery shapes and limits retire in favor of current revision, transport and save safety. SR01/04–06's resumption/reliance intent survives in Records/Assessment and Engineering. Architecture flows and the ADR follow this same split; evaluator, bootstrap and compatibility readers retire under RF-SR-06. |
| `governed-lifecycle-cli.md`, its test spec and August 24 transaction ADR | R2–5/7–17/19–25/28 → CLI-MAP-04. R1/33's historical effective-state reconstruction and R30/34's rollout thresholds retire. R6/18/26/27/32 → CLI-SR-04–11/17; R29/31 → Skill/Workflow/CLI responsibility and permission boundaries. Old lifecycle interpreter, YAML transaction and migration machinery retire; persistence safety and non-authority survive. |
| `compact-change-validation-metadata.md` and its test spec | R1–56/59–61/63–83's retired YAML formats, interpolation, event histories, summaries and rollout measurements retire under RF-SR-06. R57/58's current validation protection and R62's diagnostics survive through Validation/CLI. |
| `rigorloop-cli-new-change.md` and its test spec | R1–76's removed command surface retires with CLI's explicit storage replacement. Safety and non-authority survive in `change.create` and CLI-SR-01–11. R2/70's generic package/rendering contracts remain available through the retained package spec. |

The inventory calls these `remove-mapped-legacy-source`; the table is their source-qualified assessment basis. Current consumers must use the named owner and current proof rather than demand an old file's presence.

| Retained source family | Concrete surviving contract |
| --- | --- |
| Skill contract and boundary resources | R37–45e plan assets/metadata/fingerprints, R56–63b boundary methods and R52c registry authority retain their declared ownership. |
| Proposal/proposal-review/plan simplification and progressive disclosure | Skill explicitly delegates specialist authoring, loading and method details; the common model does not replace them. |
| Vision, project-map, learn, optional discovery and constitution skill sources | Operation selection, exact transaction/retry behavior, manifests, positioning/README synchronization, discovery routing and canonical governance remain specialist contracts. |
| Artifact lifecycle, single-source state and stage-owned lifecycle sources | SLA-R074c/d retains terminal/staleness/replacement meaning, milestone order, evidence, portability and authoring boundaries. Old format/evaluator support is retired without retiring these policies. |
| Catalog registration, CLI observability, package/init and npm publication | Selector registration and bounded evidence reads, logging/privacy/path safety, package contents/generic output and retained publication contracts remain live. The v3 record registry does not replace selector policy. |
| Review, fidelity, automation, consolidated gates and final-verification sources | Assessment maps shared clauses, not every specialist protocol. Independence levels, receipts, calibration, correction budgets and permission limits remain with their declared owners. Obsolete topology and record shapes do not regain authority. |
| Markdown readability, stage evidence access and cost/measurement sources | Marker syntax, changed-section enforcement, conditional/full-file evidence access, measurement parsers and advisory report behavior remain operational. Historical produced-report presence may retire independently. |

Other inventory holds require source-qualified reconciliation before removal. Their presence is a stated limit of this cleanup package, not a claim that every old instruction still governs. This package deliberately retains detailed contracts until their replacement is established.

### Live dependency inside historical evidence

`docs/changes/2026-06-29-release-transaction-automation/release-literal-audit-baseline.yaml` is an operational input to `scripts/release_transaction.py::_preflight_literal_audit`. Missing that file currently skips the audit. Therefore this root is `retain-operational-record-root`, excluded from the historical-root removal set. Preserve the baseline and its unauthorized-literal regression proof. Relocation or changing missing-input behavior requires an explicit Release amendment; this Design does not authorize either. Historical location alone cannot justify disabling a live check.

## Consumer and failure observations

- `boundary_first_reference.py` has a closed source-root contract and raw hashes; its resources are operational, not redundant historical prose.
- `render_manifest_yaml` derives manifest content from portability reports. `_validate_untracked_public_adapter_surface` currently requires two tracked support files, so removing only the files would break validation. DIST-SR-21/22 replaces that requirement while retaining no-tracked-generated-fragments protection.
- The ledger library's only importer is its own test. The selector schedules its historical inventory check. Retiring both removes the dependency rather than copying the old ledger into fixtures.
- The fidelity checker reads a committed `bytes_read: 1024` claim and never observes a reader. It cannot establish actual bounded access; removing the fixed instrumentation does not retire requirement-fidelity assessment.
- Release's special v0.1.1 token-report and v0.1.2 compatibility branches are operational dependencies, explicitly withdrawn under REL-SR-25 rather than bypassed after report deletion.

## Independent assessment package and proof intent

Changed owners: System SYS-SR-12; Engineering ENG-SR-13/14; Validation VAL-SR-23/24; Packaging DIST-SR-21/22; Release REL-SR-25. Unchanged product consumers for review: Skill's mapped common contract, Workflow/Assessment, CLI Records and Installation. Existing examples are unchanged; no new example file is required for source retirement.

Observe the combined path: absent tracked adapters and retired reports → isolated generation and current profile qualification → real candidate metadata and packed CLI installation. A stale or absent manifest must fail, not fall back to tracked history. Observe retired-check deletion through selected/main/direct execution: surviving current negative cases still fail, unknown IDs still reject, and no absent command is launched. Observe a changed retirement candidate, open finding or missing historical revision: the affected removal stops and its current basis remains available. Concrete commands and fixture allocation belong to Delivery; none of these are claimed as executed implementation proof.

The Design package changes source-retention and tooling contracts, not customer policy or stored schemas. Earlier proposal direction remains unchanged; original model review identities are historical and do not approve these revisions. Independent Design Review must assess the new exact subjects and their interactions, including the explicit retained remainder and compatibility effects of retired script defaults/release replay.

## Second removal: selective consolidation

The user explicitly chose preservation of important current knowledge rather than lossless transfer of old documents. The second batch removes the architecture-method spec/proof and two method ADRs, readability and portability specs/proofs, the resource-integrity ADR, and five archive copies. Current Design already preserves relevant architecture concerns and decision rationale; Skill preserves portability, readability, resource integrity and evidence-access principles. Completed rollout scope, duplicate wording and frozen-copy retention are retired without replacement prose.

The frozen-method validator and its three historical tests are removed. Three archive-wording tests retire; actual current skill inventory checks survive in one bounded test. The Skill owner test retains current owner/resource obligations while dropping archived hash and duplicate-copy assertions. Existing model unsafe-path, missing-owner and unknown-value regressions and substantive skill/resource tests remain. The selector retains exact historical paths only to classify deletion diffs and select current regression protection; it neither reads archives nor requires their existence.

Current historical citations pin the recoverable commit and original path. Historical records and judgments remain byte-identical. This is a direct user-authorized cleanup slice; it does not claim independent review, whole-initiative completion or final Verify.

## Third removal: standalone test-spec stage

The user authorized removal of six spec/proof pairs plus the retirement architecture and ADR. [test-stage-removal.json](evidence/test-stage-removal.json) records exact paths, recoverable originals and the earlier link-only adjustment to one deleted proof document. Important current allocation guidance is consolidated into Skill Authoring; Design, Assessment and Validation keep their existing behavior, review and proof ownership. Retired stages, old record formats, historical skill-package layouts and completed rollout instructions are not copied into current models. Historical activation entries and old record fixtures remain valid; they do not read the deleted documents. The unused R26 helper and its two exclusive constants are removed, without deleting executed tests.

## Fourth removal: final verification and explanation

The user authorized removal of the Explain Change spec/proof pair, final-verification spec/architecture/ADR, and branch-reality spec/proof pair. [final-verification-source-removal.json](evidence/final-verification-source-removal.json) records all seven exact recoverable subjects. Assessment preserves the important current scope, branch-authority, direct-proof, evidence-reuse and success-only explanation principles; Records/CLI keeps representation and mechanics. Historical stage order, old formats, rollout steps and duplicate wording retire without replacement. No executable reader or test requires these document files, so no test is removed.

## Fifth removal: review gates and milestone handoffs

The user authorized the seven consolidated-gate, milestone-handoff and review-independence documents. [review-handoff-source-removal.json](evidence/review-handoff-source-removal.json) records exact originals and consumer changes. Important sequencing and isolation guidance is retained in Workflow, while Assessment owns first-pass review, correction and distinct review scopes. Specialist criticality and automation policies remain separate. Old package/state representations and duplicate prose retire; the tests asserting historical vocabulary and proof-document headings retire without removing current skill behavior checks.

## Sixth removal: review recording and upstream settlement

The user authorized the formal-review-recording and downstream-status-settlement spec/proof pairs and the archived April 24 review-finding-resolution architecture. [review-recording-source-removal.json](evidence/review-recording-source-removal.json) identifies the five recoverable originals. Assessment retains durable outcomes, recording failures, truthful reconstruction and current evidence before reliance; Workflow retains actor ownership and routes upstream corrections. Historical receipt formats and downstream status-writing permissions retire. Only an unused test constant is removed; executable review, recording and parser regressions remain. The separate review-finding-resolution spec remains because automation reads it.

## Seventh removal: archived April architecture

The user authorized the seven remaining April architecture snapshots and the historical architecture-normalization test specification. [april-architecture-source-removal.json](evidence/april-architecture-source-removal.json) records the eight exact originals and current citation updates. The snapshots already identify their completed consolidation into the former system architecture; the living models retain current responsibility ownership without additional copied prose. Completed normalization proof instructions and obsolete rollout details retire. Historical records, plans and retained proof documents remain unchanged; no executable reader or test requires the deleted files.

## Eighth removal: retired spec and architecture skills

The user authorized four spec/proof pairs for the retired spec, spec-review, architecture and architecture-review skills. [retired-authoring-source-removal.json](evidence/retired-authoring-source-removal.json) records all eight originals, current owner guidance and citation changes. Design retains target/authority safety and truthful interrupted-work handling; Assessment, Workflow and CLI/Records retain their current judgment, routing and persistence responsibilities. Old per-skill stage transactions, receipts, package inventories and rollout measurements retire. Existing historical ledgers and executable regression tests remain; no current operation needs to fetch these documents from Git.

## Ninth removal: spec-family assets and readability

The user authorized both spec/proof pairs for the retired spec-family asset extraction and readability pass. [spec-family-source-removal.json](evidence/spec-family-source-removal.json) records four exact deleted subjects, Git originals and complete patches preserving prior cleanup edits to the two specifications. Skill and Design already retain current resource, structural-asset and readability obligations; no repeated model prose is added. Historical inventories and rollout matrices retire. The baseline fixture and all executable tests remain unchanged.

## Tenth removal: former workflow and plan-review packages

The user authorized both spec/proof pairs for workflow-skill-simplification and plan-review-skill-simplification. [routing-review-source-removal.json](evidence/routing-review-source-removal.json) records the four recoverable originals and current citation changes. Workflow, Assessment and CLI/Records retain routing, judgment and persistence ownership. The retained plan and lifecycle sources preserve their applicable initialization boundaries; route/context and bounded-automation contracts remain separate live owners. Old package profiles, guide authoring and stage-specific settlement representations retire. No executable tests or historical fixtures are removed.

## Eleventh removal: superseded workflow guides

The user authorized the guide-system source-alignment and workflow artifact-location-map spec/proof pairs. [workflow-guide-source-removal.json](evidence/workflow-guide-source-removal.json) records the four originals and preserves the uncommitted compatibility amendment as an exact patch. Both contracts already declare their guide behavior superseded. The retained route/context contract owns current deterministic configuration and provenance; Design and System own model authoring and layout. Guide-authored registries, duplicate projections and completed rollout details retire. Historical evidence, current CLI contracts and executable tests remain unchanged.

## Twelfth removal: historical review-asset extraction

The user authorized the review-skill-family-consistency-parser-owned-finding-shape spec/proof pair. [review-assets-source-removal.json](evidence/review-assets-source-removal.json) records both Git originals and preserves the prior citation edit as an exact patch. Skill, Assessment and Records retain structural-asset, finding-policy and current representation ownership. Historical extraction inventories, Markdown record formats and rollout measurements retire. Existing asset/parser conformance, invalid-fill and policy-leakage regressions remain unchanged, along with the separate live review-finding-resolution contract.

## Thirteenth removal: legacy change-pack policy

The user authorized the docs-changes usage-policy and skill-enforcement spec/proof pairs. [change-pack-source-removal.json](evidence/change-pack-source-removal.json) records four originals and the prior citation edits as an exact patch. Constitution, Workflow, Assessment and Records retain durable evidence, coordinated recording and success-only closeout ownership. Old YAML pack shapes, retired workflow lanes and Explain Change rollout obligations retire. Historical records and executable record/skill validation remain unchanged.

## Fourteenth removal: artifact status and plan-index lifecycle

The user authorized both spec/proof pairs for artifact-status and plan-index lifecycle ownership. [lifecycle-navigation-source-removal.json](evidence/lifecycle-navigation-source-removal.json) identifies all four recoverable originals. Workflow preserves useful plan navigation, bounded recent history, historical intent and replacement evidence; Assessment retains current reliance and stale-evidence policy. Retired local status representations and synchronization procedures are not copied. One selector fixture now uses a surviving test-spec path while retaining its assertions. Lifecycle validators, executable tests and historical evidence remain.

## Fifteenth removal: superseded automation ADRs

The user authorized the June 24 authoring/implementation autoprogression ADRs and June 30 bounded-review-fix ADR. [superseded-automation-adr-removal.json](evidence/superseded-automation-adr-removal.json) identifies all three recoverable originals and current provenance updates. Each original explicitly names the July 21 single-mechanism ADR as its replacement. The replacement, live automation specifications, implementation and tests remain; historical alternatives and rollout procedures leave the current tree without duplicating model prose.

## Sixteenth removal: v0.1.1 transition-release documents

The user authorized the publish-next-release-with-single-authored-skill-source spec/proof pair. [transition-release-source-removal.json](evidence/transition-release-source-removal.json) records both recoverable originals and any current citation updates. Packaging and Release retain current ownership; separately applicable measurement/source-selection contracts remain. The completed tracked-adapter transition recipe retires as documentation only. Release notes, metadata, measurement inputs, validation code and fixtures remain unchanged; this does not implement the separately drafted historical-replay behavior change.

## Seventeenth removal: old README positioning

The user authorized the readme-user-value-positioning spec/proof pair. [readme-positioning-source-removal.json](evidence/readme-positioning-source-removal.json) records both originals. The retained discovery spec explicitly defers current identity and introductory structure to VISION.md and preserves truthful value, audience fit and usable next steps. Historical Git-first copy, fixed opening order and retired guide links no longer govern current positioning. Repository/npm metadata obligations remain. No README, public metadata, executable test or historical judgment is changed.

## Eighteenth removal: requirement-to-delivery design package

The user authorized the lightweight-requirement-delivery-model spec/proof pair and August 30 architecture. [requirement-delivery-source-removal.json](evidence/requirement-delivery-source-removal.json) records the originals and prior Design identity. Design preserves lightweight refinement, stable requirements, distinct proportional work decomposition and many-to-many evidence-backed allocation. Shared guidance, packaged copies and their regression tests remain unchanged. Historical rollout details and retired stage assumptions leave the current tree.

## Current-model coherence refinement

After selective source removal, the user requested a coherence pass across System, Skill, Design, Workflow and Assessment. [design-coherence-refinement.json](evidence/design-coherence-refinement.json) records exact prior/current identities, unchanged interface owners and authored walkthroughs. Current behavior and decisions now precede transfer inventories. All existing requirement rows and heading anchors remain; duplicated prose and superseded installation/retention instructions are reconciled with current owners. System adds explicit engineering handoffs and small-change, milestone, review-defect and interrupted-recording scenarios. No runtime or public skill behavior is implemented by this documentation pass; independent assessment remains outstanding.

## Nineteenth removal: simplified proposal contract

The user authorized consolidation of the simplified-proposal-contract spec/proof pair and August 30 architecture. [proposal-contract-source-removal.json](evidence/proposal-contract-source-removal.json) records the originals, owner mappings and test-reader amendment. Skill Authoring now owns the exact content contract and preserved compatibility; Assessment owns review criteria and vision judgment. Records retains lifecycle representation. No new submodel is created. Old YAML-specific descriptions and rollout instructions retire; current templates, validation behavior and historical judgments remain unchanged.

## Twentieth removal: proposal-family asset extraction

The user authorized the proposal-family-assets-progressive-disclosure spec/proof pair. [proposal-assets-source-removal.json](evidence/proposal-assets-source-removal.json) records exact originals and source dispositions. Skill now owns remaining proposal-family asset metadata, placeholders, structural boundaries and deterministic validation obligations. The current proposal content contract governs optional sections. Old extraction inventories and rollout details retire; real assets, baseline fixtures, parser behavior and executable tests remain unchanged.

## Twenty-first removal: proposal authoring and review procedures

The user authorized removal of both proposal-skill-simplification and proposal-review-skill-simplification spec/proof pairs (four files, 1,563 lines). [Source disposition and identities](evidence/proposal-procedures-source-removal.json) map surviving procedure rules to Skill and Assessment. Current CLI/Records replace obsolete recording mechanics; completed extraction metrics and ledgers remain historical. No actual skill, asset, fixture, executable test or runtime behavior changes. Independent assessment and wider cleanup Verify remain outstanding.

## Twenty-second removal: plan procedure simplification

The user authorized removal of the plan-skill-simplification spec/proof pair (two files, 653 lines). [Source identities and disposition](evidence/plan-procedure-source-removal.json) map surviving rules into Skill Delivery allocation and current shared owners. Approved-plan initialization remains bounded to absent work and a current approved Delivery Review package. Retired storage and settlement mechanics and completed extraction measurements remain historical. Actual skills, assets, executable tests and historical test fixtures are unchanged; independent review and wider cleanup Verify remain outstanding.

## Twenty-third removal: reviewed-plan initialization ADR

The user authorized removing ADR-20260813 (69 lines). [Exact source disposition](evidence/plan-initialization-adr-removal.json) preserves its Git identity. Skill SKL-DEC-06 retains the decision rationale and rejected alternatives supporting current approved-plan initialization; the architecture citation now points to the historical Git revision. No skills, tests, fixtures or runtime behavior changed.

## Twenty-fourth removal: Cost-Bounded Rigor guidance

The user authorized the initial Cost-Bounded Rigor, Stage Evidence Access, M2 reminders, M3 validation guidance and M5 progressive-loading spec/proof pairs. [Source identities and dispositions](evidence/cost-bounded-rigor-source-removal.json) record all ten files and 3631 deleted lines. Skill now owns their still-applicable evidence, scope and loading rules; Engineering Validation owns validation coverage and cost. Completed rollout detail and superseded guide/state conventions retire. M4 reporting, executable tests, fixtures, source skills and selector behavior remain unchanged. Independent review and wider cleanup Verify remain outstanding.

## First-round current-design refinement

After pausing legacy deletion, the user authorized refinement of the current models. [Refinement evidence](evidence/round-one-design-refinement.json) records exact four-model changes, preserved requirements/headings, bounded independent inspection and validation. Skill and Assessment share resource rules by reference; current capability owners, project-specific proposal pointers and Validation adoption boundaries are explicit. Historical source maps remain where they still constrain adoption. This is design authorship, not whole-cleanup review, implementation completion or final Verify.

## Token-cost feature retirement direction

The user reported inconclusive results and authorized refining the design to retire token-cost measurement and reporting entirely. [Design evidence](evidence/token-cost-retirement-design.json) records VAL-SR-25, its decision rationale and affected owner patches. This supersedes earlier optional-measurement retention, including M4 reporting duties, while preserving independently useful behavior and proof. The design maps tools, callers, fixtures and qualification consumers for coherent later implementation; no executable tool, test, fixture or report is deleted by this refinement.
