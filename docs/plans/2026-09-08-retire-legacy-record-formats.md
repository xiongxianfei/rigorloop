# Deliver v2-only recording and legacy engine retirement

## Purpose / big picture

Remove the runtime support selected by the approved Design while preserving the functioning v2 system. Prepare shared dependencies before cutting support, remove obsolete tests with their owning capability, and finish with coherent current guidance and packages. Historical records remain unchanged evidence. Test deletion counts and numerical savings are not completion criteria.

## Current Handoff Summary

- Owning change record: [change.json](../changes/2026-09-08-retire-compact-workflow-mutations/change.json).

Mutable activity, milestone state, review status, findings, blockers, routing and closeout readiness live only in that record and its registered supporting records. This plan contains stable delivery intent; it does not initialize work or approve implementation.

## Source artifacts

- Proposal: [Retire Legacy Record Formats and Workflow Engines](../proposals/2026-09-08-retire-compact-workflow-mutations.md).
- Spec and architecture: the unified [Record Format](../design/record-format/record-format.md), [CLI](../design/cli/cli.md) and [Workflow](../design/workflow/workflow.md) models, including their exact retirement, discovery, recovery, dependency and governing-clause maps. No separate spec or ADR is required.
- Independent basis: [Proposal Review](../changes/2026-09-08-retire-compact-workflow-mutations/reviews/proposal-review.json) and [Design Review](../changes/2026-09-08-retire-compact-workflow-mutations/reviews/design-review.json). The owning registry and reviews bind exact subjects; later Design changes require reassessment before reliance.
- Governing dependencies: [Review and Closeout](../design/review-closeout/review-closeout.md), [Test](../design/test/test.md), Constitution and AGENTS. Workflow's scoped R14/R17–20/R22–25 replacement governs this retirement's evidence, rather than creating another ledger.
- Prior-contract test spec: none; this rigorloop-records-v2 plan owns verification allocation.

## Context and orientation

Use `node packages/rigorloop/dist/bin/rigorloop.js` for current v2 reads and targeted recording. The retained core comprises record-store persistence, targeted construction/queries, JSON schemas and their independent transport envelopes. Current workflow-context still imports legacy discovery/eligibility; the Design replaces it with schema-2 factual discovery. Its configuration YAML parser/root resolution must be separated before removing lifecycle modules.

The project owner confirms legacy work is complete and v2 operational. This is the selected operating baseline, not an executed inventory result. Existing preparatory duplicate-test correction, earlier 13-suite deletion, source audits and known failed M4 rollout assertion retain their recorded scopes. Do not replay those changes as new retirement work, assume their results prove this implementation, or restore the deleted suites wholesale. Investigate any concrete contrary residue in the selected removal paths and stop only the affected slice for an owned disposition.

Orientation comes from the approved models and directly inspected dispatcher, workflow-context, storage, validators, selectors, tests and builders. No project-map inference is used. The shared tree may contain user-owned artifacts such as docs/design.zip; they are not implementation targets.

### Allocated source boundaries

Brace lists enumerate named sources. A family bounded below by responsibility includes its directly imported helpers, dedicated fixtures and mapped packaged resources, not every file sharing a word. Before editing a milestone, expand its family into exact existing/new/deleted paths in evidence, give each an owner and changed/retained disposition, and inspect imports and callers. Newly discovered paths within the same approved responsibility may be allocated there; new behavior, an unrelated subsystem or a changed milestone boundary requires reviewed replanning or Design correction. No necessary caller may be deferred merely because its parent subsystem is otherwise out of scope.

| Family and inspected entry points | Allocation and treatment |
| --- | --- |
| `packages/rigorloop/dist/lib/{record-store,record-store-format,record-store-contract,record-store-files,record-store-cli,recording-contract,recording-construction,recording-spans,recording-cli,recording-mutation-cli,recording-query-cli,recording-observations,recording-result}.js`; `schemas/{explicit-recording-v1,rigorloop-records-v2,targeted-recording-v1}.schema.json`; `scripts/{build-record-store-schema,validate-record-store}.mjs` | M1 extracts shared transport/common validation without changing behavior. M2 removes v1 acceptance and exclusive schema/codec exports, preserving v2 and separately versioned transports. Neutral transport schema/module placement is implementation-owned inside these existing schema/lib boundaries; no new public command or stored shape. |
| `packages/rigorloop/dist/lib/workflow-context.js`, lifecycle root/configuration helpers, `packages/rigorloop/test/workflow-context.test.js` | M1 prepares neutral root/configuration parsing helpers if required; M2 implements the exact CLI-SR-23 classifier/query/configuration contract and removes old projection imports. |
| `packages/rigorloop/dist/bin/rigorloop.js`; `dist/lib/{compact-activation,compact-cli,compact-contract,compact-eligibility,compact-operations,compact-projection,compact-transaction,lifecycle-cli,lifecycle-contract,lifecycle-read,lifecycle-packages,lifecycle-operations,lifecycle-stage-routing,lifecycle-transaction,new-change,new-change-filesystem,cli-observability}.js` relative to the package | M3 removes compact/lifecycle/new-change dispatch, exclusive engines and obsolete result classification/help. Shared helpers are first moved to a surviving owner. No aliases or reimplementation of semantic orchestration. |
| `scripts/{validate-change-metadata,query-change-record,validate-artifact-lifecycle,validate-governed-lifecycle-cli}.py`, `{artifact_lifecycle_validation,artifact_lifecycle_contracts,change_metadata_semantics,review_artifact_validation,final_verification_protocol,lifecycle_state_sync}.py` | M2 removes explicit-recording-v1 acceptance where present and aligns current discovery; M3 removes compact/lifecycle record decoding, validation and execution. Preserve separately contracted document/review/calibration behavior only outside retired stored input. Retained public wrappers reject unsupported input before calling old engines; exclusive wrappers may be removed with callers/help. |
| Direct legacy-record edges in `scripts/{workflow_automation_state,workflow_code_state,validate_workflow_automation,validation_cache,boundary_first_reference,boundary_first_validation,npm_package_validation,adapter_distribution,skill_validation}.py`, related command entry points and their tests | M2/M3 adapt genuine v2 storage consumers or reject legacy-only operations before effects; remove exclusive calls/imports. Preserve unrelated automation/receipt/calibration/cache/release semantics. No new v2 orchestration or migration is authorized. |
| `scripts/{validation_selection,retirement_ledger}.py`, `scripts/select-validation.py`, `scripts/ci.sh`, their test modules and current check catalogues | M2/M3 update actual selection/discovery and retired check ownership; M4 finishes consumer checks. Reuse the existing runner and retirement-policy decision dimensions. The historical ledger remains untouched; this slice records its mapping through current v2 evidence/decisions per Workflow. Do not remove checks based on empty discovery or fabricate passing historical results. |
| `schemas/{change,compact-current-state-v1,compact-current-state-activation,lifecycle-contract-activation,final-verification-contract-activation}.schema.json`; `specs/{compact-current-state,lifecycle-contract,final-verification-contract}-activation.yaml`; `packages/rigorloop/dist/metadata/compact-current-state-activation.json`; `templates/{compact,explicit-recording}` | M3 removes exclusive legacy definitions, activation and scaffolds after shared dependencies are separated. Independently versioned boundary-first activation, document-validation and transport definitions remain. M4 removes any remaining packaging references; disabling a flag is insufficient. |
| `CONSTITUTION.md`, `AGENTS.md`, `specs/{rigorloop-workflow,governed-lifecycle-cli,compact-current-state-change-record,stage-owned-lifecycle-artifacts-and-change-local-workflow-state,change-record-catalog-registration-and-bounded-read-model,published-skill-first-repository-simplification,skill-contract}.md`, `docs/architecture/system/architecture.md`, current package/user documentation | M4 applies the exact approved replacement maps and scoped retirement-governance amendment. Preserve stable historical requirement identities and archival meaning; identify removed runtime promises explicitly. Do not rewrite historical change/review/plan evidence. |
| `skills/*/SKILL.md` and the exact transitive references/assets reachable through their resource maps; `templates/shared/*` as referenced by these consumers | M4 removes retired runtime profiles, paths, semantic CLI invocations and exclusively legacy resources. Retain specialist methods, selective loading, independent review/Verify, v2 procedures and ordinary invocation names. No separate spec/architecture skill refactor; no internal requirement IDs or maintainer-only machinery in shipped text. |
| `scripts/{build-skills,build-adapters,validate-skills,validate-adapters}.py`, builder/validator libraries, `dist/adapters/{README.md,manifest.yaml}`, package current metadata and README | M4 generates supported archives using existing tooling; repairs only demonstrated integration gaps. Refresh current v0.5.1 candidate metadata using existing adapter_distribution builders and matching current CLI assertion. Historical release metadata remains unchanged; no publication/version bump/new release procedure. |

### Test disposition boundary

Audit cases at each changed boundary, including parameter partitions and shared-helper users. Existing `packages/rigorloop/test/record-store-*.test.js` modules mix stored-v1, transport-schema-1 and v2 protections; classify actual bodies rather than delete the family. Retain/strengthen v2 origin/reference, path/identity, retry, publication/recovery, query/diagnostic, correction-after-completion and archive/rejection proof. Positive v1 acceptance leaves in M2, positive compact/lifecycle acceptance in M3. Keep the existing recording/workflow-context/public CLI harnesses for surviving and rejection scenarios.

M3 audits the nine `compact-*.test.js` modules and their dedicated `helpers/compact-fixture.js`, remaining lifecycle fixtures/helper imports, and matching Python suites. Remove exclusively retired acceptance, migration, rollout-phase assertions and fixtures only after mapping their required safety to the surviving boundary or explicit de-contracting. Preserve useful public rejection tests in retained harnesses. No unconditional file-count reduction is selected. The 13 already deleted historical lifecycle suites are not new deletion targets.

For each affected coherent group, evidence names the Design obligation or exact retirement decision, observed fixture behavior, contribution, retain/replace/remove disposition, retained proof and limitations. Unknown protection stays until resolved. If a shared helper/fixture changes, execute all affected complete modules after that change; focused-class or pre-change results cannot close the milestone. Runtime/case/token outcomes are reported only when measured, separately from static declarations and code size.

## Non-goals

- No migration, export, archive service/schema, permanent or temporary legacy reader, recovery compatibility program, new ledger or CLI readiness enforcement.
- No changes to v2 stored fields, origin/reference semantics, independent transport versions or storage safety guarantees.
- No broad automation/calibration/release retirement, authoring-skill refactor, blind suite deletion, benchmark requirement or performance target.
- No edits to archived change records/identities, user artifacts, old approvals or published historical release evidence. No release, push, PR creation or publication authority comes from this plan.

## Requirements covered

| Requirement basis | Milestone / verification allocation |
| --- | --- |
| RF-SR-01–05, RF-SR-07–08 | M1 TG-01; M2 TG-02; TG-FINAL-01 preserves closed JSON, registry/reference/origin invariants, correction availability and useful narrative |
| RF-SR-06 | M2 TG-02/03 for v1; M3 TG-04/05 for compact/lifecycle; M4 TG-06; TG-FINAL-01 for complete retirement and archives |
| CLI-SR-01–03, CLI-SR-07, CLI-SR-10–13, CLI-SR-17–19, CLI-SR-21–23 | M1 TG-01; M2 TG-02/03; M3 TG-04/05; M4 TG-06; TG-FINAL-01 for read/write boundaries, truthful results and coherent consumers |
| CLI-SR-04–06, CLI-SR-08–09, CLI-SR-14–16, CLI-SR-20 | M1 TG-01 and M2 TG-02 preserve concurrency, lossless construction, retry, recovery, scoped observations and bounded receipts; TG-FINAL-01 covers retained integrated paths |
| WF-SR-01–09, WF-SR-11–17 | M4 TG-06 preserves actor ownership, model authority, assessment/correction/closeout dependencies and useful v2 procedures; TG-FINAL-01 checks cross-consumer consistency |
| WF-SR-10 and scoped R14/R17–20/R22–25 mapping | M1 baseline/disposition preparation; M2/M3 test retirement and contrary-residue decisions; M4 governance alignment; TG-FINAL-01 validates complete supported boundary and honest proof |
| RC-SR-01–18, TEST-SR-01–13 | Existing governing policy applied throughout; group-level protective-value evidence, fresh independent milestone/whole-change review, separate Verify, explicit applicability and separately owned external authority |

All eight model boundary dimensions are allocated: input domain → TG-01/02/03/04; state/lifecycle → TG-02/05/06; identity/authority → TG-01/02/03/06; composition/path → all groups and TG-FINAL-01; temporal/retry → TG-01/02 and TG-FINAL-01; failure/recovery → TG-01/02/03/05; compatibility/migration → TG-02/03/04/06; external/environment → TG-02/03/06. No migration is performed; compatibility proof is retained v2 and unsupported old-input handling.

## Milestones

### M1. Separate the shared v2 dependencies

- Milestone kind: implementation.
- Engineering purpose: Create a behavior-preserving base so later removal cannot accidentally delete v2 result validation, path safety or configuration parsing.
- Requirements: RF-SR-01–05/07–08; CLI-SR-02–09/11–22; WF-SR-10.
- Architecture responsibility: Shared transport/common types, exact v2 persistence and configuration/root helpers.
- Dependencies: Approved exact Delivery package; inspect actual callers and representative before behavior before extraction.
- Implementation scope: Extract independently versioned advanced-result/common validation from stored-v1 ownership; remove v2 reliance on V1_FORMAT for neutral path checks/defaults where safe. Prepare independent configuration/root helpers. Keep old public acceptance unchanged until its owning removal milestone.
- Files/components likely touched: Storage/schema/build family, workflow-context neutral helpers and associated existing Node/Python test modules.
- Required verification: TG-01, defined below.
- Evidence expectations: Record exact before/after fixture results for retained boundaries, source-level dependency map, unknown-value rejection and all changed helper consumers.
- Implementation steps: Compare extracted semantics with their original definitions; keep result/request/stored versions separate. Introduce or adapt meaningful v2 and transport negative tests before moving logic; inspect the counterexample each catches.
- Validation commands: V1, V2, V3, V10; complete any additional module importing a changed helper.
- Expected observable result: V2 and currently retained legacy commands behave as before, while v2 no longer depends on exclusive legacy definitions scheduled for deletion.
- Completion criteria: All extracted dependencies have a surviving owner; schema generation and focused/full affected modules pass; no format is silently migrated or retired early.
- Required evidence: Current v2 evidence for TG-01 and exact dependency/disposition inventory; any baseline failed legacy expectations remain explicitly scoped.
- Review handoff: Independent M1 Code Review of extraction, proof and compatibility; return defects to M1 author.
- Optional commit boundary: `M1: Separate the shared v2 dependencies`.
- Risks: Accidental vocabulary, encoding, envelope or recovery change.
- Rollback/recovery: Revert this extraction commit as one unit before dependent removal; preserve record bytes and user changes.

### M2. Make recording and current discovery v2-only

- Milestone kind: implementation.
- Engineering purpose: Cut stored-v1 support after shared dependencies are isolated, and provide factual discovery that can safely ignore archives.
- Requirements: RF-SR-01–08; CLI-SR-01–23; WF-SR-10–15.
- Architecture responsibility: V2 recording, exact archive classifier, workflow-context schema2 and configuration boundaries.
- Dependencies: M1 independently reviewed and required corrections complete.
- Implementation scope: Remove explicit-recording-v1 request/read/write/validation/recovery acceptance and exclusive definitions. Implement exact approved discovery, explicit-target classification, limits, error envelope and configuration restrictions. Adapt direct v1 consumers and retire their positive tests with protection mapping. Compact/lifecycle commands remain until M3; no complete-retirement claim.
- Files/components likely touched: Record-store/targeted/query modules and schemas, workflow-context, v1 validator/caller edges, recording/workflow-context/metadata/query/selector test modules.
- Required verification: TG-02, TG-03, defined below.
- Evidence expectations: Execute public primary/advanced operations and public workflow-context against isolated v2/retired/malformed/archival fixtures, checking byte preservation and exact outcomes; retain full-module safety evidence after helper changes.
- Implementation steps: Establish v2 and rejection proof first; remove v1 branches/fixtures only after identifying transport-schema-1 cases that must remain. Update current discovery consumers and selectors with the same cutoff. Diagnose version1/unknown journals without writes while retaining version2 initial-create recovery.
- Validation commands: V2, V3, V4, V5, V10; V1 after schema generator changes; complete all affected Python/Node modules post-edit.
- Expected observable result: V2 operates through preserved transports; explicit v1 input rejects. Normal discovery excludes yaml-only archives, reports malformed/ambiguous v2, never infers authority and performs no recovery.
- Completion criteria: All TG-02/03 partitions and relevant safety checks pass; no v1 fallback or broken caller remains in this boundary. Intermediate compact/lifecycle support is explicitly limited to the pending M3 removal.
- Required evidence: Current v2 evidence with exact read/write/fixture identities, removed-case accounting, no-mutation comparisons and observation scope; no blanket current claim from an earlier audit.
- Review handoff: Independent M2 Code Review of complete recording/discovery diff and tests; corrections return to owning M1/M2 boundary as applicable.
- Optional commit boundary: `M2: Make recording and current discovery v2-only`.
- Risks: Deleting shared schema1 transport validation; hiding corrupt v2 as history; allowing recovery writes through version1 journals.
- Rollback/recovery: Revert the entire M2 boundary with its consumers before deployment if needed; do not convert any records. Preserve unknown transaction data and obtain a bounded owner disposition.

### M3. Remove compact and lifecycle execution and exclusive tests

- Milestone kind: implementation.
- Engineering purpose: Remove remaining legacy engines only after current discovery and v2 recording no longer need them.
- Requirements: RF-SR-06/08; CLI-SR-01–11/18/23; WF-SR-10 and scoped retirement-governance mapping.
- Architecture responsibility: Dispatcher, legacy engines, validators, activation, direct callers and check discovery.
- Dependencies: M2 independently reviewed and required corrections complete.
- Implementation scope: Remove compact/lifecycle/new-change commands and exclusive engines, activation metadata, stored schemas/scaffolds and fixtures. Reconcile every affected direct caller; remove exclusively old acceptance and rollout tests while retaining focused unsupported/no-fallback/no-mutation and v2 safety proof.
- Files/components likely touched: Named legacy Node family; Python record/eligibility/validator/automation edges; selectors; compact test modules and dedicated fixtures; schemas, activation metadata and old templates in the allocated boundaries.
- Required verification: TG-04, TG-05, defined below.
- Evidence expectations: Explicit disposition for each removed check group and affected caller; executed surviving safety/rejection proof; no dangling imports, stale selector command or accidental empty-suite success.
- Implementation steps: Inventory existing dedicated tests/fixtures before removing code. For each shared obligation retain or move its protection to v2 first. Remove public dispatch before allowing any old request effects; disconnect helpers and package data completely. Preserve unrelated automation/calibration/release behavior or explicitly reject only its legacy-record operation before effects.
- Validation commands: V3, V4, V5, V6, V10; run all affected full modules before closeout, replacing removed positive-suite commands with retained rejection harnesses rather than invoking missing files.
- Expected observable result: Only v2 runtime record support remains; removed commands reject before request processing/effects, and no wrapper or helper can invoke an old engine. Archived bytes remain unchanged.
- Completion criteria: Every exclusive legacy path has a removal disposition; shared v2 helpers survive; affected callers/selectors are coherent; required post-removal modules and rejection checks pass. No installed-package readiness is claimed until M4.
- Required evidence: Mapped de-contracting/retained protection, before/after support comparison, actual test discovery differences, fixture/archive byte checks and removal/rollback identities in existing v2 records.
- Review handoff: Independent M3 Code Review covering actual deletions, surviving proof and every directly affected caller.
- Optional commit boundary: `M3: Remove compact and lifecycle execution and exclusive tests`.
- Risks: Leaving hidden Python/automation fallback or disabling discovery to obtain green tests; deleting independent document/configuration/version contracts.
- Rollback/recovery: Revert the coupled M3 removal and its consumers as a code unit if needed under normal authority; preserve archives and v2 data. Restore lost retained protection or fix its replacement before progressing.

### M4. Align governing consumers and generated packages

- Milestone kind: implementation.
- Engineering purpose: Complete the retirement boundary across the instructions and artifacts users actually install.
- Requirements: RF-SR-06/08; CLI-SR-10/18/23; WF-SR-01–17; applicable RC/Test policy.
- Architecture responsibility: Governance, canonical skills/resources, builders/selectors/current metadata and public archives.
- Dependencies: M3 independently reviewed and required corrections complete; no release or external activation of intermediate milestones.
- Implementation scope: Apply exact governing-clause replacement maps; remove retired runtime guidance and exclusive packaged resources. Preserve specialized methods, v2 interface, independent whole-change review and distinct Verify. Generate and validate supported archives and current candidate metadata through existing tooling.
- Files/components likely touched: Allocated governance/spec/current docs, canonical skills and transitive resources, shared templates, builders/validators, adapters support and current package metadata/test expectation.
- Required verification: TG-06 and TG-FINAL-01, defined below.
- Evidence expectations: Current canonical/resource inventory, exact generated output/source identities, archive validation, full affected builder/validator modules and integrated v2-only evidence.
- Implementation steps: Reconcile each current legacy reference as removed or explicitly historical, never by blind v1 replacement. Apply Workflow scoped retirement evidence mapping without editing archived ledgers. Regenerate current metadata via existing builder functions and keep version/history intact. Verify complete public resources and runner selection.
- Validation commands: V1, V3, V5, V7, V8, V9, V10, V11; full surrounding modules after any shared builder/fixture edit.
- Expected observable result: Current instructions and installed archives support v2 only and no legacy execution path; private repository mapping IDs do not enter shipped skills.
- Completion criteria: All required consumer changes and TG-FINAL-01 proof are complete; generated output is coherent and exact new evidence supports retained v2 behavior. No final-review, Verify or PR claim is implied.
- Required evidence: Exact canonical/generated identities and commands, governing consumer dispositions and integrated results in registered v2 evidence.
- Review handoff: Independent M4 Code Review, followed after all corrections by the separately required fresh final whole-change review checkpoint.
- Optional commit boundary: `M4: Align governing consumers and generated packages`.
- Risks: A packaged conditional reference can preserve retired instructions; current metadata can drift after guidance changes; accidental historical release rewrite.
- Rollback/recovery: Regenerate from the reviewed canonical source or revert the M4 source/metadata unit; never hand-edit archives or rewrite historical release evidence.

### Milestone verification groups

| Group | Required behavior and representative cases | Concrete proof / evidence owner |
| --- | --- | --- |
| TG-01 | Same advanced schema1 envelope/diagnostic vocabulary, primary schema1 requests/schema2 results and v2 stored schema2; unknown values fail closed. V2 path allowlists, configuration parsing/root safety and exact source bytes survive helper extraction. | Existing Node recording suites, schema generator check and affected Python modules; M1 records before/after retained results and dependency map. Independent document/transport versions are positive retained cases. |
| TG-02 | Primary/advanced v2 creation, targeted edits, full useful queries, Origin immutability, field-specific EntryRef resolution and same-batch targets. Stored-v1/unknown/mismatched requests reject. Stale writes/lost-response retries conflict; mixed writers exclude; neighbor bytes and maximum-density receipts survive. Version2 prepared/committed journals recover initial creation and updates; version1/unknown/mismatched journals and third-state tampering stop without mutation. A new blocker/failed evidence after completion remains recordable. | Retained/adapted complete record-store Node modules, including v2-contract, v2-persistence, targeted, queries and interactions. Deterministic fault hooks and isolated fixtures exercise actual shared publisher/public adapters. M2 evidence identifies changed helpers and each reused or fresh proof. |
| TG-03 | All CLI-SR-23 classifier rows and precedence, including both manifests; malformed/unknown v2; yaml archive with/without reserved v2 residue; empty/absent roots; symlink/unreadable enumeration. Schema2 exact response, explicit selection, no implied next stage, stable ordering, configuration provenance/old override rejection, scope completeness and limit-exceeded at 1,024 directories/64 candidates/8 MiB. Explicit ID bypasses unrelated enumeration; no reads execute old validators or recovery. | Complete workflow-context module and affected metadata/query/selection suites; public-command tests check outcomes and unchanged archive/record/transaction bytes. M2 owns first proof; TG-FINAL-01 checks packaged integration. |
| TG-04 | The RF-SR-06 retired set is unavailable through public commands, record validators, wrappers and helper exports. compact/lifecycle/new-change reject before stdin/request effects with no alias, fallback, migration or writes. Known and unknown formats cannot gain v2 authority. | Retained public CLI and metadata/rejection harnesses plus source/import/package closure inspection; M3 records disposition of each retired positive check. Original positive behavior need not be reproduced by v2. |
| TG-05 | Removal leaves no dangling imports or selector targets and no legacy automation/receipt side path. Direct callers either retain a justified v2 storage purpose, lose an exclusively retired operation or explicitly reject unsupported input before effects. Unrelated current safety, calibration, release, cache and document-validation guarantees remain protected. | Complete affected caller modules and selector regression; reviewer inspects exact call-path reachability and no-effect assertions. Evidence names safe unsupported boundaries without claiming the entire deferred subsystem was retired. |
| TG-06 | Constitution/AGENTS/model consumers agree on retirement; no old writer/validator advertised in current skills, conditional references or archives. Specialist authority, fresh final review and Verify remain distinct. Generated resources are selective and portable, source identities/current metadata match, no private IDs or retired activation assets ship. | Canonical skill validation, full builder/adapter modules, generated archive validation and scoped manual current-reference/resource-map inspection. M4 records exact artifacts and explains legitimate archival/independent-version references. |

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: all four implementation milestones and required corrections complete.
- Assessment: fresh independent final whole-change Code Review of the complete delivered engineering change and cross-milestone interactions against the current approved Design and Delivery package.
- Evidence: exact final subjects, independent reviewer basis, judgment, retained/deleted protection and explicit concern dispositions.
- Successor: distinct final Verify. Corrections return to their owner and require affected independent reassessment and an adequate integrated final judgment.

This checkpoint is not implementation work. Milestone judgments, integrated tests, a single remaining milestone or a non-applicable verification group never waive it.

## Change-level verification

### TG-FINAL-01. Coherent v2-only product and preserved evidence

- Covers: M1–M4; RF-SR-01–08, CLI-SR-01–23, WF-SR-10/11/16/17 and the selected retirement/adoption maps.
- Demonstrate: in an isolated repository containing valid v2 work and unchanged legacy archives, installed/current CLI discovery returns only usable v2 candidates, explicit retired input fails without effects, and malformed v2 stays visible. Execute v2 creation, review/finding origin, evidence, targeted correction after completion, advanced/targeted concurrency and controlled version2 recovery through the retained interfaces. Verify the generated package has no legacy command/activation fallback and its instructions agree with actual results. Preserve model and transport schema1 identifiers for their independent purposes.
- Evidence expectations: V3, V5, V8–V11 plus retained public integration tests implementing these scenarios in existing Node harnesses; exact archive/source/store bytes and current consumer/check disposition map. Cross-milestone imported helper and generated-resource changes require renewed applicable proof. Full independent final Code Review then separate Verify assesses sufficiency.
- Non-applicability: not selected; shared transport extraction, engine deletion, caller changes and packaging span all milestones. Local tests cannot establish the complete delivered boundary alone.

## Validation plan

Run focused proof at its first owning milestone, followed by complete affected modules after all relevant helper/fixture changes and before that milestone's closeout. References to V commands are direct allocations, not permission to reuse an earlier milestone's result after its basis changes. Evidence reuse requires the affirmative Review and Closeout applicability basis; record exact subjects, procedure, environment and actual result. An unchanged audit does not require blind repetition. These are planned commands, not reported executions.

| ID | Exact command(s), allocation and purpose |
| --- | --- |
| V1 | `node scripts/build-record-store-schema.mjs --check` — M1, M2 when schema generation changes, M4/final after reconciliation; independently versioned schema parity, no restoration of retired stored definitions. |
| V2 | `node --test packages/rigorloop/test/record-store-v2-contract.test.js packages/rigorloop/test/record-store-v2-persistence.test.js packages/rigorloop/test/record-store-targeted.test.js packages/rigorloop/test/record-store-queries.test.js packages/rigorloop/test/record-store-interactions.test.js packages/rigorloop/test/record-store-contract.test.js packages/rigorloop/test/record-store-cli.test.js` — complete retained modules post M1/M2 changes. Adapt mixed legacy/transport cases; these retained harnesses must not disappear merely to make this command green. |
| V3 | `npm test --prefix packages/rigorloop` — M1–M4 and final as affected; complete Node discovery and surrounding public/package modules after shared changes. Deleted exclusively legacy modules leave with explicit disposition in M3; surviving tests must remain discovered. |
| V4 | `python scripts/test-change-metadata-validator.py`; `python scripts/test-query-change-record.py`; `node --test packages/rigorloop/test/workflow-context.test.js` — full modules after M2/M3 changes, with retained rejection/v2 harnesses replacing obsolete positive cases. |
| V5 | `python scripts/test-select-validation.py`; `python scripts/test-boundary-first-validation.py`; `python scripts/test-validation-cache.py` — M2–M4/final where affected; current selection, independent document contracts, archive separation and surviving cache protection. |
| V6 | `python scripts/test-workflow-automation.py`; `python scripts/test-workflow-automation-state.py`; `python scripts/test-workflow-code-state.py`; `python scripts/test-review-artifact-validator.py`; `python scripts/test-artifact-lifecycle-validator.py`; `python scripts/test-governed-lifecycle-cli-validator.py` — M3 full affected caller/rejection modules. Preserve these test entry points for retained behavior and explicit unsupported cases; remove only dedicated old acceptance bodies/fixtures, not all deferred-subsystem protection. |
| V7 | `python scripts/validate-skills.py`; `python scripts/test-skill-validator.py`; `python scripts/build-skills.py --check`; `python scripts/test-build-skills.py` — M4 complete canonical/mirror/shared-resource modules after edits. |
| V8 | `python scripts/build-adapters.py --version v0.5.1 --output-dir /tmp/rigorloop-retirement-adapters`; `python scripts/validate-adapters.py --version v0.5.1 --adapter-root /tmp/rigorloop-retirement-adapters` — M4/final current supported archive generation and validation; no publication. Use a task-owned output directory and preserve unrelated existing files. |
| V9 | `python scripts/test-adapter-distribution.py`; `python scripts/test-npm-package-publication.py` — M4 complete surrounding package/release-validation modules; refresh only current candidate metadata via existing builders before matching expectations. No historical release rewrite. |
| V10 | `python scripts/validate-boundary-first.py --check --path docs/design/record-format/record-format.md --path docs/design/cli/cli.md --path docs/design/workflow/workflow.md`; `python scripts/validate-markdown-readability.py docs/plans/2026-09-08-retire-legacy-record-formats.md`; `node scripts/validate-record-store.mjs docs/changes/2026-09-08-retire-compact-workflow-mutations/change.json`; `git diff --check` — authoring and each affected handoff; structure/readability/storage only. |
| V11 | `bash scripts/ci.sh --mode local --jobs 4` — M4/TG-FINAL-01 against the integrated working tree, with reviewed current selectors. If an authorized PR is later prepared, run the existing PR mode using the actual full base/head revisions resolved then. |

Required additional complete-module checks are determined by actual imports: invoke `python scripts/test-<affected-module>.py` or `node --test <affected-module-path>` with the exact inspected path recorded in evidence, alongside the directly allocated commands above. This is a dependency requirement, not an invented substitute runner. A command made obsolete by planned removal must have its positive check de-contracted and retained proof explicitly mapped; unplanned entry-point removal requires a reviewed plan amendment, not silently skipping validation.

Manual inspection is needed for instruction meaning, shared-helper ownership, historical/current reference classification and completeness of the removal map; text matching alone cannot judge those facts. Record inspected paths, concrete observations and rationale in existing evidence, and have the independent reviewer assess them. Automated tests must still prove runtime rejection, no mutation and v2 behavior at actual boundaries.

## Risks and recovery

- Shared definitions can carry hidden v1 coupling. M1 separates their surviving responsibility; M2 requires full-module v2/transport proof before deleting acceptance.
- Archive filtering can hide corruption or block valid explicit work. TG-03 proves precedence, limits, unsupported input, safe enumeration and exact-ID isolation.
- Broad historical suites mix exclusive behavior and enduring safety. Apply Test criteria and the scoped Workflow governance map; retain unknown protection and stop only its owned slice.
- Existing failed audit evidence or unavailable deleted-suite results can be misrepresented. Keep original outcomes and limits; establish the actual post-change v2/rejection evidence needed for reliance.
- Intermediate branches are reviewable development states, not coherent installed releases: M1 retains old support, M2 still has pending compact/lifecycle removal, M3 still has pending consumer/package alignment. Do not release, advertise complete retirement or treat these states as customer adoption before M4 and final gates.
- Unknown transactions or concrete unfinished legacy residue require a bounded owner decision before affected deletion. Preserve bytes; no speculative migration or legacy recovery subsystem is selected.
- Rollback units are the milestone's coupled code/tests/consumer changes, identified by actual commits in evidence. Reverting source is separately authorized work; do not rewrite v2 stores, archives or historical approvals to make rollback appear compatible.

## Dependencies

- Current approved proposal and exact three-model Design, independently approved Delivery package before implementation, and nonauthor milestone reviews before dependent milestones.
- Shared extraction precedes removal; discovery/recording independence precedes deleting legacy engine helpers; coherent consumers and packages precede final product claims.
- Record current decisions/evidence through primary v2 commands. This plan does not initialize mutable work from a draft; Route owns activity and work selection after approval.
- All required consumer/caller dispositions and proof are in scope; unrelated broader capability retirement returns to its owner.
- Fresh final whole-change Code Review precedes distinct successful Verify. PR/release/publication remain separately authorized external actions.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-08 | Separate shared dependency extraction before two bounded runtime retirement milestones, then align consumers/packages. | Exposes v2 safety regressions before deleting their former owners and provides explicit intermediate states. | One mass deletion; removing a schema by v1 spelling; claiming partial retirement as activation. |
| 2026-09-08 | Remove dedicated tests with their owning capability and retain shared/rejection proof in existing harnesses. | Approved retirement de-contracts positive legacy behavior while Test criteria preserve surviving protection. | Wholesale restoration of already deleted suites; blanket deletion by filename; using green counts as evidence. |
| 2026-09-08 | Use current v2 evidence/decision carriers and the exact Workflow retirement-governance replacement. | Keeps required protection/disposition/rollback reasoning without rewriting archival ledgers or inventing a new process. | A second ledger, mandatory old-engine benchmark or speculative continuation facility. |
| 2026-09-08 | Allocate fresh final whole-change Code Review as a separate closeout checkpoint. | Cross-milestone helper, dispatch, selector and package interactions require independent complete assessment before Verify. | Treating the last milestone review or integrated test run as final Code Review. |

## Readiness

- See the owning change record for current workflow state.
- Remaining completion gates: independent Delivery Review, implementation and Code Review for each milestone with required corrections, fresh final whole-change Code Review, and distinct successful Verify. This plan grants no PR, release or publication authority.
