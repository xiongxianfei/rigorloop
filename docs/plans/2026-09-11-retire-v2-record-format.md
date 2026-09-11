# Retire the v2 stored-record format

<!-- Template: plan-skeleton-v3 -->

## Purpose / big picture

Deliver the approved v3-only operational storage boundary without losing shared safety behavior, rewriting historical assessments or retaining an operational v2 dependency. Separate reversible preparation from the coordinated removal so that necessary old-work and recovery obligations can be settled while the supporting executable is still available.

## Current Handoff Summary

- Owning change record: [change.json](../changes/2026-09-11-retire-v2-record-format/change.json).

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: [Retire the v2 stored-record format](../proposals/2026-09-11-retire-v2-record-format.md), with [Proposal Review](../changes/2026-09-11-retire-v2-record-format/reviews/proposal-review.json).
- Spec: the approved owning [Record Format](../design/record-format/record-format.md#v2-stored-format-retirement), [CLI](../design/cli/cli.md#v2-runtime-retirement), [Workflow](../design/workflow/workflow.md#v2-retirement-coordination), [Review and Closeout](../design/review-closeout/review-closeout.md#v2-retirement-and-assessment-reliance) and [System](../design/system/system.md#v2-retirement-composition) amendments.
- Architecture: technical realization and decisions in those five living Designs; [Design Review](../changes/2026-09-11-retire-v2-record-format/reviews/design-review.json) identifies the exact approved package and the resolved header-recognition correction.
- Prior-contract test spec: none independently applicable. Historical plans and tests inform dependency inspection but do not override the selected retirement scope.
- Shared criteria: [Test](../design/test/test.md), with assessment and final-closeout authority retained by Review and Closeout.

## Context and orientation

JavaScript under packages/rigorloop/dist/lib is authored implementation. Canonical schemas and templates are bundled by scripts/build-record-store-schema.mjs; bundled copies are not hand-authored. Canonical skills and their selectively shared resources supply adapter content; installed skill copies and generated public packages are not authoring targets.

record-store-format.js dispatches v2/v3 and imports shared parsing through record-format-v2.js. record-store.js uses V2_FORMAT for initialization and journal dispatch. record-format-core.js serves both adapters; targeted schemas contain v2-prefixed definitions still used by v3 and independent transports. Therefore filename or numeric-version matching alone cannot determine removal.

The archive discriminator is kind-specific: change.json carries contract/schema_version/change_id; supporting v2 records carry schema_version/change_id. CLI owns the exact recognition bounds, diagnostic precedence and transaction-residue behavior. No new manifest or supporting contract field is required.

Use the current repository CLI, node packages/rigorloop/dist/bin/rigorloop.js, for exact context, subject inspection and targeted recording. Do not rely on an installed older CLI. The direct owner, source, test and build-input inventory supplies this plan's bounded orientation; no project-map inference is required.

## Non-goals

- No migration, narrative extraction, historical record edits, approval copying, new stored version, permanent legacy reader or recovery service.
- No new v2 retirement, rejection or archive-compatibility tests, including manual probes presented as replacement tests. Remove v2-only cases and retain or retarget existing shared protection.
- No unrelated document-validator removal, universal report redesign, field-level approval or additional finding immutability.
- No publication, PR, release or customer activation as part of these implementation milestones.

## Requirements covered

| Requirement or owned obligation | Allocation | Proof |
| --- | --- | --- |
| RF-SR-14 and retained RF-SR-01–08 | M1 shared extraction; M2 sole operational v3 and unchanged historical records | TG-01, TG-02, TG-03, TG-FINAL-01 |
| RF-SR-09–13 and CLI-SR-24–27 | M1/M2 preserve named fields, ID-only Review findings, conditional basis, exact updates and independent interface dispatch | TG-01, TG-02 |
| CLI-SR-28 and retained CLI-SR-02–06/08/09/12–23 | M1 safety preparation; M2 dispatch, classifier, recovery, consumers and package boundary | TG-01, TG-02, TG-03, TG-FINAL-01 |
| WF-SR-18 and WF-SR-10/11/14/15 | M2 prerequisite disposition, coordinated consumer/test removal and explicit supported recording | TG-00, TG-03, TG-FINAL-01 |
| RC-SR-21 and RC-SR-05/06/16/19/20 | M2 provenance, fresh supported correction and unchanged assessment policy | TG-00, TG-03, TG-FINAL-01 |
| SYS-SR-02/04/06/08/09 | M2 integrated dependency removal and coherent governance/package adoption | TG-03, TG-FINAL-01 |
| RC-SR-11–15; Test TEST-SR-01–13 | Both milestone reviews, retained protection comparison, fresh final whole-change Code Review and distinct Verify | TG-01–03, final review checkpoint, TG-FINAL-01 |

The retirement amendments displace only their mapped continuation clauses. Unrelated baseline requirements remain unchanged; they are protected through affected retained suites rather than a new exhaustive compliance inventory.

## Milestones

### M1. Isolate shared dependencies and preserve shared coverage

- Milestone kind: implementation.
- Engineering purpose: make later removal selective while leaving the pre-retirement operational boundary usable and recoverable.
- Requirements: RF-SR-14; CLI-SR-28 and retained safety/interface requirements; WF-SR-18; Test maintenance criteria.
- Architecture responsibility: RF-DEC-08, CLI-DEC-07; shared core, transport, parser and synthetic test setup.
- Dependencies: current approved Design and Delivery Review of this plan; no work initialization from an unreviewed draft.
- Implementation scope: extract shared parsing/definitions and neutral initialization where needed; retarget existing shared checks to v3 or identify adequate existing equivalents. Keep v2-exclusive acceptance and recovery support until M2's disposition.
- Files/components likely touched: record-format-v2.js, record-format-v3.js, record-format-core.js, record-store-format.js, record-store.js, targeted-recording-v1.schema.json, record-store-transport.schema.json, existing test helpers and the shared suites listed below; schema bundler if extraction changes its inputs.
- Required verification: TG-01 for retained contracts, shared safety and proof-equivalence comparison.
- Evidence expectations: group-level retain/retarget/remove rationale, exact assertions and retained counterexample detection, commands/results and candidate identities. Record what remains v2-exclusive for M2; no per-test history ledger is required.
- Implementation steps: identify transitive v3/transport imports; extract without changing public meaning; adapt existing synthetic setups; run affected checks; compare lost parameter partitions before relying on a consolidated suite. Keep unknown protection until its owner determines whether it is shared.
- Validation commands: V1, V3 and affected V4 callers; V2 when fixture/helper changes span the package. Start with the exact affected files from V1 before its complete recording family.
- Expected observable result: existing v2/v3 behavior still works, while shared production and retained test consumers no longer depend unnecessarily on the exclusive v2 adapter or fixtures.
- Completion criteria: shared dependencies have explicit owners; selected checks pass with no lost distinct safety protection; no operational v2 support has been removed; scope is independently reviewed.
- Required evidence: registered implementation evidence for TG-01 and independent milestone Code Review with exact subjects.
- Review handoff: complete M1 diff, extraction equivalence, setup changes and retained coverage comparison.
- Optional commit boundary: `M1: isolate shared recording dependencies and coverage`.
- Risks: extracting transport definitions can accidentally change early errors or serialization; retargeting can lose origin-independent safety assertions.
- Rollback/recovery: revert the bounded preparation diff without touching real records. If shared equivalence is uncertain, restore the affected existing test/helper until the comparison is settled. Preserve all private journals and use only their supporting executable for authorized recovery.

### M2. Retire v2 through one coherent runtime and consumer change

- Milestone kind: implementation.
- Engineering purpose: remove the operational contract and all necessary consumer dependencies in one reviewable integration unit, avoiding an executable that strands its own governance or packages.
- Requirements: RF-SR-14, CLI-SR-28, WF-SR-18, RC-SR-21, SYS-SR-02/04/06/08/09 and retained v3 requirements in the allocation table.
- Architecture responsibility: the five approved retirement amendments, including CLI's corrected per-kind header rule and independent early-response versions.
- Dependencies: reviewed M1; TG-00's explicit responsible disposition before any support removal. Any unresolved operational dependency stops the removal portion; completing the preparatory milestone does not waive it.
- Implementation scope: remove v2 dispatch, validation, recovery and exclusive resources/tests; implement approved archival classification; reconcile canonical consumers, validators, documentation, selectors and generated package inputs together.
- Files/components likely touched: record-store-format.js, record-format-v2.js, record-format-core.js, record-store.js, record-discovery.js, workflow-context.js, recording-construction.js, recording-mutation-cli.js, recording-query-cli.js and their result/observation helpers; schemas, templates and bundled copies; scripts/build-record-store-schema.mjs, validate-change-metadata.py, validation_selection.py, skill_validation.py, npm_package_validation.py and direct query/validation callers; canonical skills/shared resources, example indexes, AGENTS.md, CONSTITUTION.md and package/installation support guidance where they describe support.
- Required verification: TG-00, TG-02, TG-03 and TG-FINAL-01 once the complete candidate exists.
- Evidence expectations: refreshed per-store disposition, exact source/candidate identities, retained suite results, dependency/import and package inventory, historical byte comparison, consumer/authority walkthrough and independent review. Distinguish inspection from executed runtime proof.
- Implementation steps: settle and record TG-00 using the supporting baseline; remove exclusive branches/resources; retain independent transport envelopes and v3 recovery; apply archive recognition without a full v2 validator; remove v2-only tests and reconcile retained discovery; update consumers and historical-example labels; regenerate through existing builders; review all transitive callers and execute the allocated retained checks.
- Validation commands: V1–V6. V5 uses exact source/base revisions only after all intended changes are captured in the candidate. Use V7 for actual store inspection before removal and the owning v3 store afterward.
- Expected observable result: only v3 is operational; ordinary actors and packages use the same supported interface; historical provenance remains accessible as files; malformed current data and transaction residue stay visible under the approved CLI rules.
- Completion criteria: TG-00 is explicitly settled, required consumers are coherent, no operational v2 import/resource remains, retained verification passes, v2-only cases are removed without new retirement tests, historical bytes are unchanged and milestone Code Review approves the complete integration.
- Required evidence: registered TG-00/02/03 evidence, refreshed change-level integration evidence and independent M2 Code Review. Adoption remains contingent on the distinct final review and successful Verify.
- Review handoff: the whole removal and its cross-owner consequences, including test-deletion justification, actual headers, response tags and package payloads. Necessary consumer work cannot be deferred beyond this milestone.
- Optional commit boundary: `M2: retire v2 storage and reconcile consumers`.
- Risks: hidden operational dependencies, malformed-current exclusion, forgotten schema imports, dropped shared tests or stale generated guidance.
- Rollback/recovery: before adoption, revert the coherent M2 source/package-input unit to the reviewed supporting baseline while preserving all records and journals. Recover a known v2 transaction before removal with its supporting baseline, never by conversion. Unexpected residue after removal needs explicit owner disposition; do not silently bundle a legacy recovery reader. Recheck evidence applicability after any rollback or correction.

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: all in-scope implementation milestones and required corrections complete.
- Assessment: fresh independent final whole-change Code Review of the complete delivered engineering change and cross-milestone interactions.
- Evidence: exact final subjects, independent reviewer basis, judgment and concern dispositions.
- Successor: final Verify; corrections return to their owner and require affected reassessment.

This checkpoint applies even with only two implementation milestones. M2 review, a passing suite or a verification-group non-applicability rationale cannot substitute for it. Final Verify alone records successful adoption and the final explanation in this initiative's v3 records; failure produces evidence and an owned blocker.

## Change-level verification

### TG-00. Disposition before removing required support

- Covers: WF-SR-18, RF-SR-14, RC-SR-21 and SYS-SR-06/09; prerequisite to M2 removal.
- Demonstrate: a responsible actor accounts for each selected v2 store's work, findings, blockers, relevant review/Verify limitations, governance dependence and private journal/lock state. Begin with the twelve stores in design-v2-dependency-observation; refresh the selected repository inventory rather than assuming it is exhaustive or still current.
- Evidence expectations: implementation records the inspected paths, exact revisions, complete selected context, private-state observations and historical byte identities in existing evidence. The responsible owner records a separate explicit disposition in this v3 initiative's material decisions. This is operational dependency inspection, not a new retirement test. Completion labels alone cannot supply the decision; a live v2 obligation or unassessed contrary evidence blocks removal. No claim covers unknown external customer repositories.
- Freshness: repeat the relevant inspection immediately before removal when work, records or recovery state changed; re-evaluate governance dependence on the complete candidate. Preserve the pre-removal supporting executable by its exact existing commit identity, not as a new compatibility feature.

### TG-01. Retained contracts and shared safety

- Covers: M1, retained RF/CLI safety and interface behavior, WF-SR-18 and Test maintenance criteria.
- Demonstrate: existing shared tests still detect malformed/unknown current input, schema closure, byte/depth/path limits, stale revisions and declared read basis, lost-response retry, no-op preservation, unsafe filesystem targets, writer exclusion, interruptions and malicious/third-state journals. Preserve independent transport error tags and v3 finding/blocker distinctions.
- Evidence expectations: V1/V3 and affected V4 checks; compare retained assertions and scenario partitions before deleting duplicates. An existing v3 test with a similar name is insufficient evidence of equivalence.

### TG-02. Supported v3 interface and recovery

- Covers: M2; RF-SR-09–14 and CLI-SR-24–28 with retained safety requirements.
- Demonstrate: retained v3 contract, reads, mutations, adoption and persistence suites cover complete records, named projection/omissions, narrow updates, nonempty required fields, optional basis, finding ID stability, unchanged neighbors, conflicts and v3 journal restore/complete. Existing early-error cases preserve recognized review.set/verify.set schema-3 failures and independent schema-2 responses for other pre-store operations.
- Evidence expectations: V1/V2/V3 with exact candidate identity. Review the implemented retirement branches against the approved per-kind header, diagnostic, recovery and version-domain clauses. Do not add synthetic v2 rejection/archive/recovery probes or disguise them as manual tests. Existing generic/current-format protection remains applicable; static inspection of retired paths is labeled as such.

### TG-03. Consumer, package and test-removal coherence

- Covers: M2; WF-SR-18, RC-SR-21, SYS-SR-02/04/06/08/09 and CLI-SR-28.
- Demonstrate: required imports, resources, command producers and validators no longer depend on operational v2 support. Canonical guidance uses v3; historical adoption links retain provenance without invoking a v2 reader or acquiring new judgments. V3 examples remain executable; retained referenced historical illustrations are labeled non-operational. Package payloads agree with canonical inputs.
- Evidence expectations: V2–V6, existing selectors/package checks and a bounded author/reviewer walkthrough of governing references through installed guidance. Use rg dependency searches and inspect every remaining match's role; do not equate zero occurrences of v2 with success. Inspect the generated payload for obsolete v2 files because a copy-only builder may leave stale output. Preserve the reference population's historical bytes through exact before/after comparison, without registering new retirement test cases.

### TG-FINAL-01. Complete supported workflow after coordinated removal

- Covers: M1/M2 and every requirement group above.
- Demonstrate: the complete candidate's existing recording/workflow/interaction and package checks establish that a fresh actor can discover v3 work, retrieve and edit named explanations, handle conflicts/recovery and record explicit applicability without automatic approval. Governance provenance, build inputs and packaged consumers agree on the same boundary.
- Evidence expectations: retained full package suite and repository-owned selected PR checks on exact source/prepared/candidate revisions, plus TG-00 disposition and TG-03 dependency evidence. Reuse unchanged milestone proof only with affirmative unaffected-basis evidence; required fresh final checks remain fresh. New retirement tests are outside scope, and this limitation must remain visible in Code Review and Verify.
- Non-applicability: none; shared runtime, consumers, governance and package outputs jointly establish the delivered contract. This group supplements the final whole-change review and distinct Verify.

## Validation plan

These are planned execution commands, not reported passes. Concrete test assertions remain implementation-owned. Run the smallest affected existing files first, then the allocated family; investigate failures before relying on broader results.

| ID | Exact command | Purpose and timing |
| --- | --- | --- |
| V1 | `node --test packages/rigorloop/test/record-store*.test.js packages/rigorloop/test/record-retirement.test.js packages/rigorloop/test/workflow-context.test.js` | Retained recording, query, workflow and generic retired-command protection after applicable cleanup. Keep shared cases in the discovered family. record-retirement.test.js is an existing suite, not authorization to add v2-retirement cases. |
| V2 | `npm test --prefix packages/rigorloop` | Complete existing package discovery after shared-helper changes and integration. Account for removed cases; a smaller count alone does not establish coverage. |
| V3 | `node scripts/build-record-store-schema.mjs --check` | Canonical/bundled parity after generation using the same command without --check. Remove obsolete tracked bundle files coherently with their source removal. |
| V4 | `python scripts/test-select-validation.py`; `python scripts/test-change-metadata-validator.py`; `python scripts/test-skill-validator.py`; `python scripts/test-governed-lifecycle-cli-validator.py`; `python scripts/test-artifact-lifecycle-validator.py`; `python scripts/test-npm-package-publication.py`; `python scripts/test-query-change-record.py` | Existing selector, metadata, guidance, query and packaging protection, with shared synthetic setup adapted to v3 where needed. |
| V5 | `bash scripts/ci.sh --mode pr --base "$RETIRE_V2_BASE_REVISION" --head "$RETIRE_V2_SOURCE_REVISION"` | Repository-owned candidate preparation, selected checks and package composition. Resolve both task-specific variables to exact commits; record source/prepared/candidate identities. Capture only intended files and preserve unrelated user changes. This local check grants no push, PR or release authority. |
| V6 | `python scripts/validate-change-metadata.py docs/changes/2026-09-11-retire-v2-record-format/change.json`; `git diff --check` | Actual owning v3 record coherence and patch whitespace after evidence recording. |
| V7 | `node packages/rigorloop/dist/bin/rigorloop.js status --root . --change "$RETIRE_V2_CHANGE_ID" --format json`; `node packages/rigorloop/dist/bin/rigorloop.js context --root . --change "$RETIRE_V2_CHANGE_ID" --limit 100 --max-bytes 8388608 --input - --format json` | Before removal, bind the variable to each selected real v2 ID and supply an explicit context selection of activity/work/review/finding/blocker/evidence/verify/decision; expand incomplete selections. Inspect required subjects and private transaction locations separately. After removal use supported v3 context for this initiative, not operational v2 inspection. |

Test disposition is based on protected behavior:

| Existing population | Allocation |
| --- | --- |
| record-store-v2-contract.test.js; v2-only portions of contract/adoption/model-example suites | Remove exclusive v2 schema, body, origin, creation and continuation assertions in M2. First preserve any shared parsing, vocabulary, limits or transport protection through TG-01. |
| record-store-v2-persistence.test.js | Retain/retarget distinct shared safety cases in M1, or demonstrate equivalent existing v3 coverage. Remove v2-only journal/continuation branches in M2. Do not delete the file wholesale without this comparison. |
| record-store-v3-*.test.js | Keep supported v3 cases; remove only parameters or subcases solely establishing v2 behavior. Unknown-value and malformed-current cases remain. |
| record-store-{cli,targeted,queries,workflow,interactions,adoption}.test.js and workflow-context.test.js | Adapt existing shared fixture setup to v3. Preserve public-boundary, semantic-no-op, observer drift and coordination protections; remove exclusively v2 expectations. |
| historical-v2.mjs, historical-v2-launcher.mjs, v2 fixtures/templates and bundled resources | Remove after retained callers are detached. Real historical change stores are never fixture-conversion targets. |
| Python tests in V4 and build/selector assertions | Adapt existing shared checks, remove exclusively v2 cases and keep independent document/transport versions. Standalone legacy review-document validation is outside removal scope. |

For plan authorship, run `python scripts/validate-documentation-prose.py --mode enforce --path docs/plans/2026-09-11-retire-v2-record-format.md --path docs/plan.md`, check source links and requirement references, and run V6. These checks do not execute the implementation allocation or establish Delivery approval.

## Risks and recovery

- A live old-work or transaction dependency can outlast the initial inventory. Resolve it with its responsible owner before removal; preserve the supporting baseline until settled, without shipping a permanent reader.
- Header recognition can hide or misclassify data. Apply the approved per-kind fields and existing diagnostic precedence; retain generic malformed-current coverage and inspect the retirement branch directly.
- Removing a v2-named suite can erase shared safety. Preserve and execute its distinct supported assertions before removing the old setup; restore uncertain protection until assessed.
- Independent schema-2 transports or document contracts can be removed accidentally. Trace transitive imports and existing error-envelope checks, retaining their definitions without the exclusive stored adapter.
- Source rollback does not restore assessment applicability automatically. Keep records and exact candidate evidence, assess the changed basis and obtain the necessary fresh review/Verify before adoption.

## Dependencies

- Approved exact Design package and Delivery Review precede implementation. Only approved-plan initialization may create missing work; Route owns later work state.
- TG-00 disposition precedes M2 removal; required consumer/package changes land with it. Author observations alone are not owner-confirmed closure.
- M1 Code Review precedes M2; M2 Code Review and all corrections precede fresh final whole-change Code Review, then distinct final Verify.
- Historical governing references remain provenance; no implementation command or package generation changes adoption authority by itself.
- Publication, installation/customer activation and external integration retain their separate owners and authorization.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-11 | Prepare shared dependencies and coverage in M1, then perform one coordinated removal in M2. | Makes shared protection independently reviewable while keeping old recovery available until disposition; consumers must agree at the removal boundary. | Delete every v2-named file at once; remove the runtime first and defer necessary consumers. |
| 2026-09-11 | Use existing suites, selective retargeting and bounded dependency inspection; add no retirement tests. | Implements the explicit user constraint while preserving supported safety and making proof limits visible. | New v2 rejection/archive suites or manual retirement probes disguised as replacement tests. |
| 2026-09-11 | Keep the operational disposition as a prerequisite with current evidence, not a completed label in this plan. | Initial inventory cannot settle semantic obligations or promise future recovery state. | Assume twelve completed labels authorize removal; introduce a permanent compatibility subsystem. |

## Readiness

- See the owning change record for current workflow state.
- Remaining completion gates: independent Delivery Review, approved work initialization, implementation and milestone reviews, fresh final whole-change Code Review and distinct final Verify. This plan grants none of their outcomes.
