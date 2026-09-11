# Structured assessment explanations and editable findings

## Purpose / big picture

Deliver the approved v3 stored-record and CLI Design: named Review/Verify explanations, explicit projections and whole-field updates, current-account Review findings with stable IDs, and coherent consumer adoption. Sequence the change around the existing transaction engine so compatibility and correction remain usable throughout delivery.

## Current Handoff Summary

- Owning change record: [change.json](../changes/2026-09-10-structured-assessment-explanations/change.json).

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: [Structured Review and Verify Explanations](../proposals/2026-09-10-structured-assessment-explanations.md), with the explicit user direction revision recorded in decision `v3-finding-id-only` in the owning change's material-decisions.json. The original proposal and its review retain their earlier scope; the revised finding direction is assessed by the current Design Review.
- Spec: living [Record Format](../design/record-format/record-format.md), [CLI](../design/cli/cli.md), [Review and Closeout](../design/review-closeout/review-closeout.md), [Workflow](../design/workflow/workflow.md), and [System](../design/system/system.md), including their scoped amendments and displacement maps.
- Architecture: technical realization and decisions in those five models; no separate architecture artifact is required.
- Design assessment: [design-review.json](../changes/2026-09-10-structured-assessment-explanations/reviews/design-review.json), covering the exact models, [stored examples](../design/record-format/examples/README.md), [CLI examples](../design/cli/examples/README.md) and supporting subjects. Current reliance comes from that record's applicability and subjects, not this link alone.
- Prior-contract test spec: none independently applicable; retain existing v2 safety proof under the living models and [Test](../design/test/test.md).

## Context and orientation

The tracked JavaScript under packages/rigorloop/dist/lib is the implementation source in this repository. Schema/template copies under packages/rigorloop/dist/schemas and dist/templates are bundled from canonical schemas/ and templates/ by scripts/build-record-store-schema.mjs. Do not hand-edit those bundled copies. Public adapter package bodies are generated from canonical skills; do not author installed .agents or .codex copies.

The flow is public selector validation, contract-selected request validation, lossless candidate construction, the shared transaction engine, and contract-selected result validation/rendering. Advanced requests enter the same candidate boundary with full bytes. The current requestFormat implementation couples advanced request and stored version; v3 must separate them because advanced requests stay schema 2. Primary requests stay schema 1; primary results use the approved command/store dispatch table rather than copying a stored number.

Use the direct inspected owner and source inventory below for orientation; no reliance is placed on the older project map. Preserve the current branch's existing Design/example edits and fixture-path corrections. No new dependency or migration service is planned.

| Surface | Exact initial implementation/consumer locations |
| --- | --- |
| Stored contracts and transaction dispatch | schemas/rigorloop-records-v2.schema.json; schemas/record-store-transport.schema.json; new canonical v3 stored schema/template; packages/rigorloop/dist/lib/record-format-v2.js, record-store-format.js, record-store.js, record-store-files.js and record-discovery.js; scripts/build-record-store-schema.mjs |
| Primary mutation and results | schemas/targeted-recording-v1.schema.json; packages/rigorloop/dist/lib/recording-contract.js, recording-construction.js, recording-spans.js, recording-mutation-cli.js, recording-result.js, recording-cli.js and record-store-cli.js |
| Reads and discovery | packages/rigorloop/dist/lib/recording-query-cli.js, recording-observations.js and workflow-context.js; scripts/query-change-record.py and validate-record-store.mjs |
| Review/Verify authors | skills/proposal-review/SKILL.md, skills/design-review/SKILL.md, skills/delivery-review/SKILL.md, skills/code-review/SKILL.md, skills/verify/SKILL.md; the three proposal/design/delivery review references named *-review-recording-and-settlement.md; skills/verify/references/branch-readiness-verification.md and successful-explanation assets/resources selected by that skill |
| Other recording consumers | SKILL.md in skills/bugfix, ci-maintenance, explore, implement, learn, plan, pr, proposal, research and route; skills/design/references/governed-design-authoring.md; skills/proposal/references/governed-proposal-authoring.md; skills/implement/references/planned-milestone-implementation.md; skills/plan/references/governed-plan-authoring.md and skills/route/references/governed-lifecycle-routing.md |
| Shared policy/application content | templates/shared/review-assessment.md, review-reliance.md and review-isolation-and-recording.md; their selected skills/*/references copies and review/report assets; canonical skills/design/SKILL.md where it directs recording |
| Validation and publication inputs | scripts/validate-change-metadata.py, validation_selection.py, skill_validation.py, npm_package_validation.py, build-adapters.py; scripts/test-change-metadata-validator.py, test-select-validation.py, test-skill-validator.py, test-governed-lifecycle-cli-validator.py, test-artifact-lifecycle-validator.py and test-npm-package-publication.py; packages/rigorloop/README.md; CONSTITUTION.md and AGENTS.md |

Before changing a shared resource, expand its actual producer/copy/consumer edges with repository search and the existing packaging validators; include every reached caller in the same milestone. This is a concrete starting inventory, not permission to ignore a newly discovered current consumer. A discovered behavioral gap returns to Design; an additional consumer of already approved behavior is implementation scope. Retain document-only legacy validators and their independent callers.

## Non-goals

- Retiring existing v2 support, converting records or reinterpreting old approvals.
- Redesigning evidence, material-decisions body, or change-level blocker origins.
- Universal report sections, JSON Patch, per-paragraph IDs, finding history, field approvals, semantic prose extraction, or inferred workflow permission.
- Release, push, PR, publication, installation or customer-governance adoption.

## Requirements covered

| Owning requirement or retained obligation | Allocation | Proof |
| --- | --- | --- |
| RF-SR-09, RF-SR-11, RF-SR-13 | M1 shapes/preservation, M2 construction, M3 read representation | TG-01, TG-03, TG-05 |
| RF-SR-10; CLI-SR-25/26 | M2 whole-field edits and finding boundaries; M3 rendering | TG-03, TG-05 |
| RF-SR-12; CLI-SR-27 | M1 store/journal dispatch; M2 operation/result dispatch; M4 coordinated adoption | TG-02, TG-04, TG-06, TG-FINAL-01 |
| CLI-SR-24 | M3 explicit field selection, omissions, applicability and optional absence | TG-05 |
| RF-SR-01–08 as retained/mapped; CLI-SR-02–10/16/19/20 | M1–M3 shared containment, references, closed inputs, conflicts, receipts and recovery | TG-01, TG-02, TG-03, TG-06 |
| CLI-SR-01/11–15/17/18/21–23 as retained/mapped | M2 selector/response safety; M3 primary reads/discovery; M4 consumers | TG-04, TG-05, TG-07 |
| RC-SR-19/20 and retained RC-SR-01–18 applicability/correction/closeout duties | M2 explicit writes; M4 author guidance and reliance walkthroughs | TG-03, TG-07, TG-FINAL-01 |
| WF-SR-02/10/11/15 and structured-assessment consumer map; retained coordination/authority duties | M4 consumers and v2 continuation | TG-07, TG-FINAL-01 |
| System structured-assessment composition under SYS-SR-01/02/05/07 | M4 integrated store/consumer behavior | TG-FINAL-01 |
| Test criteria and existing negative/regression protection | Every milestone retains or demonstrably replaces useful protection | TG-01–07 and final independent review |

The model scenario dimensions are allocated as follows: input domain to TG-01/03/04/05; state/lifecycle to TG-03/07; identity/authority to TG-02/03/07; composition/path to TG-02/05 and TG-FINAL-01; temporal/retry to TG-06; failure/recovery to TG-04/06; compatibility/migration to TG-01/02/04/07; external/environment to TG-02/05/07. Apply each owner's scoped v3 displacement rather than treating retained v2 origin clauses as v3 Finding requirements.

## Milestones

### M1. Stored v3 contract and transaction safety

- Milestone kind: implementation.
- Engineering purpose: establish the common candidate and recovery boundary before adding callers.
- Requirements: RF-SR-09/11/12/13; retained RF-SR-01–08 and CLI-SR-02–10.
- Architecture responsibility: RF-DEC-06/07; contract dispatch and exact prepared-byte recovery.
- Dependencies: current approved Design and Delivery Review of this plan.
- Implementation scope: closed v3 schema and format implementation; separate advanced request schema 2 from stored schema 3; typed references, Finding versus Blocker preservation, v2/v3 journal dispatch and schema packaging. Retain the exact v2 validator and recovery path. Public new-store selection is wired only in M4; internal tests construct explicit temporary v3 fixtures, with no hidden adoption flag or production-store conversion.
- Files/components likely touched: stored-contract/transaction inventory row; canonical templates/rigorloop-records-v3/records.json; package contract, persistence and recovery tests.
- Required verification: TG-01 — all five v3 record kinds, required non-whitespace explanation values and item cardinality, conditional seven-field basis, body/dual/unknown/null/mixed rejection. TG-02 — v3 finding current fields editable, ID removal/rename rejected; origin/basis rejected for findings, blocker origins retained; advanced envelope/version separation and shared candidate safeguards.
- Evidence expectations: extend the existing record-store contract/persistence suites with v3 cases and run unchanged v2 cases. New closed-vocabulary constants have unknown_value or not_in_vocabulary regressions. Verify structural recordability separately from adequacy of review/evidence.
- Implementation steps: establish failing boundary fixtures; implement contract-selected validation and preservation; extend journal dispatch without regenerating bytes; bundle canonical data through the existing build script.
- Validation commands: V1, V3 and V6 below.
- Expected observable result: internal v3 and existing v2 candidates follow one safe transaction boundary, while mismatched format/version pairs cannot publish.
- Completion criteria: all five v3 examples validate against the executable schema; negative candidates leave files unchanged; recovery selects exact before/candidate bytes; existing v2 operation semantics remain intact.
- Required evidence: exact tested source/test/schema subjects, actual commands, results and failure-path observations in evidence records.
- Review handoff: independent Code Review of M1, including alternate advanced and recovery paths.
- Risks: accidental coupling of request/storage version or weakening existing v2 origin checks.
- Rollback/recovery: revert the unadopted M1 code unit without touching stores; retain the original executable for v2 recovery. Temporary fixtures are isolated from real change records.

### M2. Complete recording, narrow updates and response dispatch

- Milestone kind: implementation.
- Engineering purpose: add actor-supplied operations over the proved shared candidate engine, including errors that occur before store selection.
- Requirements: CLI-SR-25/26/27; RF-SR-09/10/11/13; retained conflict, selector and receipt obligations.
- Architecture responsibility: CLI-DEC-05/06; source-span edits, explicit operation catalogue and early command recognition.
- Dependencies: M1 and its independent review/corrections.
- Implementation scope: v3 review.record/verify.record, review.set/verify.set, finding.add/set, overlap expansion, complete Verify basis replacement/removal, and result schema 3. Keep schema-2 vocabulary unchanged. Recognized new commands use schema 3 for every outcome; retained batch and unknown-command errors follow the approved dispatch table. No production new-store adoption is claimed.
- Files/components likely touched: primary mutation/result inventory row; record-store-targeted.test.js, record-store-cli.test.js, record-store-interactions.test.js and relevant helpers.
- Required verification: TG-03 — full creation/replacement, closed whole-field updates, omitted bytes/order, multiline/literal escapes, semantic no-ops, exact finding preservation, explicit finding corrections, state/resolution coupling, optional basis removal, missing target versus missing registered record, explicit applicability and batch overlaps. TG-04 — both new commands across duplicate/unknown flags, invalid/repeated change selectors, malformed stdin, absent/v2/unknown/mixed stores, validated-v3 errors and success; retain valid operation/selector identity, omit unavailable metadata and prove no repository/stdin access for selector failures.
- Evidence expectations: exercise real public dispatch and validate emitted JSON/text against independently selected result profiles; include all approved negative response examples and schema-2 controls. Do not compute expected version through production dispatch logic.
- Implementation steps: add failing public/error and byte-preservation tests; implement catalogue/contract dispatch; construct candidates with the shared span engine; validate receipts before publication; exercise lost-response and mixed advanced/targeted concurrency.
- Validation commands: V1 and V3.
- Expected observable result: a requested field edit stores only intended values, while every recognized command has a valid, truthful response even without a store.
- Completion criteria: command/operation mismatch and closed fields reject; no-op is byte-identical; failures have no changed list or partial writes; complete review operations preserve findings independently of explicit finding edits.
- Required evidence: targeted/public command outcomes, raw-byte comparisons, response validation and exact subjects.
- Review handoff: independent Code Review of M2 with M1 interactions and both original CLI review hazards.
- Risks: a schema-2 fallback erases the new tag; construction retargets assessments or silently changes applicability.
- Rollback/recovery: revert M2 callers together with their result contract changes before adoption; keep M1 storage recovery available for any test-created v3 fixture. Never replay an old revision after a lost response.

### M3. Selected reads and derived human output

- Milestone kind: implementation.
- Engineering purpose: expose the stored fields through coherent reads after their construction contract is established.
- Requirements: CLI-SR-24/26/27 and retained CLI-SR-12–15/20–23; RF-SR-10/11/13.
- Architecture responsibility: projection, bounded rendering, observation identity and explicit absence metadata.
- Dependencies: M2 and its independent review/corrections.
- Implementation scope: Review/Verify --fields, full/context summaries, Review applicability, exact v3 Finding item/summary shape, conditional basis absence, discovery and observation traversal, readable explanation headings/lists without new authoritative prose.
- Files/components likely touched: reads/discovery inventory row; recording-result.js; query, model-example and observation/interactions tests.
- Required verification: TG-05 — no selection returns a complete selected record; named selection returns exact requested values and honest omissions; unknown/repeated/empty/wrong-record selectors reject. Full/summary v3 Finding has no origin_available; summary omits exactly evidence/resolution. V2 findings and v2/v3 blockers retain their origin representation. Verify optional absence differs from omission, context cannot accept arbitrary --fields, text preserves decoded multiline/literal escape content, Unicode and collection order, and bounded output cannot silently discard reasoning.
- Evidence expectations: full/selected JSON and human output compared to independently supplied stored values; all reviewed examples executable where applicable. Validate observation freshness for v3 current finding subjects and retained blocker-origin subjects; retain the internal digest version separately from result versions.
- Implementation steps: implement contract-selected item and scope shapes; wire selector parsing and result validation; render the same decoded selection; preserve pagination, output-limit and observation identity semantics.
- Validation commands: V1 and V3.
- Expected observable result: callers can request a rationale or limitation directly and recognize when their context is partial.
- Completion criteria: stored bytes never change on reads; selected metadata binds one coherent revision; examples for full finding and summary context match the actual public boundary.
- Required evidence: exact stored/request/response relationships, limit failures, no-read-side-effects and retained v2 outputs.
- Review handoff: independent Code Review of M3 across mutation/read/renderer interfaces.
- Risks: nonexistent origin reported as omitted; full-context indicators mistaken for complete assessment; double-decoding escapes.
- Rollback/recovery: revert the M3 reader/renderer unit before adoption; retain storage recovery and do not translate v3 records to v2 for an older client.

### M4. Coordinated consumers, adoption and integrated proof

- Milestone kind: implementation.
- Engineering purpose: expose new-store v3 creation only when runtime, guidance, validators and packages agree.
- Requirements: RF-SR-12; CLI-SR-27; RC-SR-19/20 and retained assessment authority; Workflow consumer map; System composition.
- Architecture responsibility: existing-v2/new-v3 coexistence, canonical skill distribution and separately authorized adoption.
- Dependencies: M1–M3 and their independent reviews/corrections.
- Implementation scope: reconcile every listed and transitively reached recording consumer, shared resource, schema/helper/selector and governance statement; add public explicit v3 creation and reject new v2 creation in the adoption candidate while keeping existing v2 reads/writes/recovery. Preserve historical stores and current initiative's v2 record chain. Build packages through existing machinery outside canonical/active skill roots.
- Files/components likely touched: all remaining inventory rows, reviewed examples and their selector tests, public package help/readme and governing adoption surfaces. Change only the selected stored/interface adoption clauses; do not alter Distribution/Release ownership.
- Required verification: TG-06 — integrated stale revision/read conflicts, duplicate retries, preview recheck, competing advanced/targeted writes, interrupted multi-record save at prepared/publication/acknowledgment points, third-state/tampered journal rejection, exact restoration/completion and bounded receipts under diagnostic pressure. TG-07 — each reviewer/Verify family supplies named reasoning, conditional Git basis and explicit applicability; author/support consumers select contracts; partial reads never imply approval. Existing-v2 continuation and v3 blocker/finding distinctions survive packaged consumption.
- Evidence expectations: execute public workflows in isolated v2/v3 stores, inspect actual generated package inputs/outputs, and record assessor walkthroughs for meaning-changing limitations versus editorial corrections. The CLI cannot mechanically decide those meanings; independent review inspects guidance and observed actor inputs without claiming prose inference.
- Implementation steps: reconcile canonical consumers and their copies through repository generation; wire final creation/adoption boundary; run full candidate CI and record failures honestly; preserve exact candidate subjects for final review/Verify.
- Validation commands: V1–V6, including candidate PR-mode CI with exact resolved revision variables.
- Expected observable result: a coherent candidate supports the new contract and continuing v2 work without conversion, hidden adoption, duplicate explanation or automatic approval.
- Completion criteria: all consumer edges agree, package checks pass, no required v2 support is removed, every changed contract has direct public proof, and TG-FINAL-01 can run on the complete candidate. Local adoption is recorded only after the final review checkpoint and successful Verify; package availability alone does not adopt governance.
- Required evidence: package/candidate identities, complete command results, integrated transaction observations and scoped actor walkthroughs. No hosted CI or publication claim without separate observed evidence/authority.
- Review handoff: independent Code Review of M4 followed by the distinct fresh whole-change checkpoint below.
- Risks: source-only checks miss a packaged consumer; provisional candidate creation is mistaken for adopted governance; rollback leaves inaccessible v3 data.
- Rollback/recovery: before adoption, revert the coherent candidate without altering real stores. After any real v3 store exists, retain a compatible executable and journal recovery access; do not downgrade or delete its records. A discovered need to remove v2 support returns to its separately owned retirement decision.

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: all in-scope implementation milestones and required corrections complete.
- Assessment: fresh independent final whole-change Code Review of the complete delivered engineering change and cross-milestone interactions.
- Evidence: exact final subjects, independent reviewer basis, judgment and concern dispositions.
- Successor: final Verify; corrections return to their owner and require affected reassessment.

This checkpoint applies the selected review policy. A verification-group non-applicability rationale does not waive it. M4's review is not automatically the final whole-change assessment.

## Change-level verification

### TG-FINAL-01. Coherent v3 adoption alongside v2 continuation

- Covers: M1–M4, RF-SR-09–13, CLI-SR-24–27, RC-SR-19/20, Workflow consumer reconciliation and System composition.
- Demonstrate: create an isolated v3 store with all five record kinds; record, project, edit and reread explanations through public commands; explicitly correct a finding under the same ID; change limitations and applicability atomically without inferred approval. Continue a separate v2 store and exercise its recovery without conversion. Use a non-Git Verify without basis and a conditional Git/PR Verify with the complete seven-value basis, without asserting hosted results. Exercise mixed-version clients, new-command early errors, v3 read metadata, interruption/recovery, and generated package parity on the same candidate.
- Evidence expectations: V1/V2/V4 plus candidate identity, public envelopes, exact byte/revision comparisons, preserved historical/v2 subjects and the relevant actor-policy walkthrough. Reuse milestone proof only with affirmative unchanged-basis evidence under Review and Closeout; final integrated proof covers the interactions that local groups cannot establish.
- Non-applicability: none; schema, CLI, journal and packaged actor guidance jointly define the delivered outcome.

## Validation plan

Commands are execution obligations, not claims that implementation tests already passed. Run the smallest relevant milestone group first; stop and correct failures before relying on wider results. New tests may be added under the existing test discovery; concrete fixture/function names remain implementation-owned.

- V1: `node --test packages/rigorloop/test/record-store*.test.js packages/rigorloop/test/record-retirement.test.js` — existing contract, persistence, CLI, targeted, query, workflow, example and integration surfaces; extend these suites or add discovered record-store suites for v3 without losing v2 partitions.
- V2: `npm test --prefix packages/rigorloop` — complete package tests after integration, including non-recording consumers.
- V3: `node scripts/build-record-store-schema.mjs --check` — canonical schema/template bundle parity after generation with the same script without --check.
- V4: `bash scripts/ci.sh --mode pr --base "$ASSESSMENT_BASE_REVISION" --head "$ASSESSMENT_SOURCE_REVISION"` — repository-owned candidate preparation and full selected/package checks. Resolve both task-specific variables to exact commits. Construct the source candidate from this change's intended paths without consuming unrelated user changes; record source/prepared/candidate identities. No push, PR or publication is implied. Use the existing failure detail and selector output to diagnose coverage, not an invented replacement CI wrapper.
- V5: `python scripts/test-select-validation.py`; `python scripts/test-change-metadata-validator.py`; `python scripts/test-skill-validator.py`; `python scripts/test-governed-lifecycle-cli-validator.py`; `python scripts/test-artifact-lifecycle-validator.py`; `python scripts/test-npm-package-publication.py` — retained selection, consumer, metadata and packaged proof. Preserve standalone document-validator coverage without feeding current stores to the legacy review validator.
- V6: `python scripts/validate-change-metadata.py docs/changes/2026-09-10-structured-assessment-explanations/change.json`; `git diff --check` — actual owning v2 records and patch whitespace after recording.

For plan authoring, validate this plan's prose using `python scripts/validate-documentation-prose.py --mode enforce --path docs/plans/2026-09-11-structured-assessment-explanations.md --path docs/plan.md`, inspect relative links and requirement references, and run V6. These checks do not execute the planned implementation or establish Delivery approval.

## Risks and recovery

Preserve existing negative tests unless an equivalent supported-boundary check demonstrably replaces them. Never delete a v2 test merely because a v3 example exists. Unknown behavioral protection returns to its owner before removal. Source formats, transport envelopes and document versions remain independently dispatched.

No milestone is a release or customer-adoption unit. Intermediate branch commits may contain unexposed internal capability, but the public adoption candidate must include all four milestones. Stage-owned records remain v2, and successful final Verify is the only owner of the closeout explanation. A failing final verification records evidence and its blocker rather than a success report.

## Dependencies

- Current exact-package Design approval, including the user's scoped finding direction and all resolved Design findings; any substantive Design change requires affected reassessment.
- Independent Delivery Review before implementing or initializing work entries; plan authorship alone adds no work state.
- Ordered milestone Code Reviews and corrections, followed by distinct whole-change Code Review and final Verify.
- Existing Distribution/Skill/Release tooling and authority boundaries; no new runtime dependency, network availability requirement or publication permission.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-11 | Establish storage, then writes/errors, then reads, then coordinated consumers/adoption. | Each caller depends on a proved common candidate boundary; deployment waits for compatible consumers. | Simultaneous unreviewable rewrite; public v3 creation before consumer reconciliation. |
| 2026-09-11 | Retain the original v2 implementation/proof and this initiative's v2 records. | The approved scope explicitly provides continuation without conversion. | Opportunistic v2 retirement or migrating this initiative's approval chain. |
| 2026-09-11 | Attach early-error and finding-read proof to public interface milestones. | Lower-level schema tests cannot detect an incorrect command tag or misleading projection metadata. | Relying only on parsed examples or schema helper tests. |

## Readiness

- See the owning change record for current workflow state.
- Remaining completion gates are Delivery Review, implementation and milestone reviews, fresh whole-change Code Review, and distinct successful Verify. This plan grants no implementation, adoption or external-action claim.
