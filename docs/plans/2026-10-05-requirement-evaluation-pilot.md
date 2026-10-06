<!-- Template: plan-skeleton-v4 --> <!-- Skill: plan -->

# Requirement evaluation browser pilot

## Purpose / big picture

Deliver attributable Implementation and Verification assessments for IRs, SRs and ARs in the existing optional system Requirements tree, beside independently selected Design judgments. Preserve exact evidence, unknowns, history and conflicts. Demonstrate the flow with four real requirement subjects and separate synthetic boundary cases; neither child counts nor a successful browser test establishes requirement satisfaction.

## Current Handoff Summary

- Owning Change: `2026-10-04-system-requirements-view-design`; resume through `rigorloop change context --root . --change 2026-10-04-system-requirements-view-design --format json`.

Mutable authority, progress, review standing, blockers and execution results belong to that Change. This plan allocates future delivery. Authoring or approving it does not execute milestones or authorize new requirement judgments, installation or publication.

## Source artifacts

- Accepted requirement basis: IR-002 and SR-008/009/085/086, with existing AR-046 for attribution and reading. The accepted `g0-format-requirements` basis supplies the bounded requirement reuse; wider customer-generator obligations are not claimed by this repository pilot.
- Reviewed logical behavior: FUNC-007/009/080/081 under MOD-004, FEAT-003/022 and SCN-008/009/084. Relationships retain their canonical owners.
- Reviewed architecture: [delivery format](../../design/architecture/modules/MOD-016-engineering-model-management/modules/MOD-004-engineering-context-and-traceability/requirement-delivery-format.md), [version 2 JSON Schema](../../design/support/requirement-delivery-v2.schema.json), [evaluation semantics and Design disclosure](../../design/architecture/modules/MOD-016-engineering-model-management/modules/MOD-004-engineering-context-and-traceability/requirement-evaluation.md), and [current Requirements tree/v1 contract](../../design/architecture/modules/MOD-016-engineering-model-management/modules/MOD-004-engineering-context-and-traceability/requirement-tree.md). The accepted `g0-format-design` basis owns the concrete contract, including its normative semantic checks; structural schema validation alone is insufficient.
- Prior delivered pilot: [AR assessment browser pilot](2026-10-05-ar-assessment-browser-pilot.md). Preserve its original selected bytes, judgments and evidence. The new extension receives its own complete implementation review and scoped Verify.
- Prior-contract test spec: none. Allocate proof from the approved format's acceptance table and [shared test-design rules](../../design/support/test-design/rules.md); inspect actual assertions before reusing existing tests.

## Context and orientation

MOD-004 owns admission, applicability comparison, projection and the offline reader. MOD-007 owns assessment policy and adequacy; MOD-011 retains operational records. A caller prepares explicitly selected sanitized disclosures using the supported governed CLI and retained payloads. No record lookup enters model capture, generation or the offline reader.

`scripts/lib/rem_browser_assessments.py` currently admits delivery v1 AR accounts. Extend it for v2 and one normalized internal representation, composed by `scripts/lib/rem_architecture_browser.py` and `scripts/render-rem-architecture-browser.py`. `scripts/resources/rem-architecture-browser/viewer.js` and `viewer.css` render embedded content. `assessment-snapshot.data` freezes the selected delivery envelope; `design-review-snapshot.data` remains a separate Design selection. Generated browser files are renderer outputs, never hand-edited sources. This work uses the current supported CLI; it requires no operational-store migration or new public command.

### Pilot subjects and preparation

| Subject | Why included | Actual assessment preparation |
| --- | --- | --- |
| AR-046 | Existing AR disclosure and legacy compatibility | Preserve the original v1 Partial / Not assessed account and its current stale presentation. Any new v2 claim needs an actual attributable account and source payload; do not relabel an old Evidence reference as Verification. |
| SR-085 | SR with AR-046 and six integrated criteria | Assess its complete six-criterion basis directly. AR delivery state does not decide the SR result; scoped browser proof cannot establish all customer-generator obligations. |
| SR-050 | SR with four criteria and no ARs | Use the current FUNC-050/MOD-012 responsibility and reviewed no-further-AR-needed disposition. Assess direct evidence separately; no AR is a structural fact, not a gap or a pass. This is a reader/assessment subject, not new implementation of capability guidance. |
| IR-002 | Stakeholder need above SRs | Inspect the actual retained approved outcome review and source payloads, then explicitly select a suitable complete reviewed outcome basis. Design coverage never supplies a delivery judgment. If no suitable delivery basis or claim exists, retain explicit absence. |

SR-009 remains part of the feature's requirement basis but is no longer the no-AR example: it now owns AR-056. SR-050 is outside IR-002's subtree; select it in the same system tree and never invent an IR-002 parent link. Recheck pilot definitions and full direct-child memberships before assessment preparation. If SR-050 gains an AR, reconcile the pilot selection and affected delivery review before claiming the no-AR demonstration.

The four names identify primary demonstration subjects, not a four-account limit. Include exact supporting child claims or Design accounts whenever the selected parent actually relies on them. A complete parent claim must account for every captured direct child through support or attributable nonreliance. Unknown outcomes are acceptable real results; synthetic complete, failed and conflicting cases prove capability without being published as actual assessments. Unsupported positive claims never serve as a shortcut to pilot completion.

## Non-goals

No bulk AR creation, changed canonical requirement criteria, automatic code-based assessment, inherited parent pass, second dashboard, Module-level Requirements view, live status editor, new record type, customer generator, package release or external publication. Definition lifecycle remains independent of assessment. SR-050 capability guidance and SR-085 customer-generator delivery remain with their own owners. This pilot does not add SR-087's broader atomic publication guarantee.

## Requirements covered

| Required outcome | Delivery and proof allocation |
| --- | --- |
| SR-008/009: stable typed relationships and explicit completeness | M1 preserves canonical IDs and captured direct-child sets; M2/TG-2 and TG-FINAL-1 observe tree navigation and complete counts even under filtering. No new relationship traversal engine. |
| SR-085 / AR-046: faithful attribution, distinct meanings and explicit gaps | M1/TG-1 source mapping, identity, coverage, conflicts and compatibility; M2/TG-2 historical/current explanation and separate indicators; TG-FINAL-1 composed disclosure. |
| SR-086: portable reading within this repository artifact | M2/TG-2 and TG-FINAL-1 copied page, embedded details, navigation and diagrams with no network or private store. No complete customer-package qualification claim. |
| IR/SR/AR evaluation and SR allocation | M1 kind-specific coverage and dependencies; M2 existing Design/allocation join and missing-account explanations. SR-050 is test data for this feature, not added delivery scope. |
| Approved format's input, identity, resource and recovery boundaries | M1/TG-1 and real renderer checks; M2/TG-FINAL-1 old/new selection, explicit reuse/clear and bounded recovery. |

## Entry prerequisite: G0 — concrete format design

Use the approved delivery-format document and schema as one contract. Check current applicability of the accepted requirement and Design bases, this plan's formal delivery review and applicable execution authority before M1. Plan changes do not alter those upstream decisions. A missing or contradictory rule returns to its Design owner; implementation must not choose an unreviewed wire field, status mapping or compatibility behavior.

Delivery v2 uses `assessments` and `resolutions`; delivery v1 remains supported externally. Design disclosure has its own versions and companion. Preserve `--assessments`, `--clear-assessments` and ordinary companion reuse. The schema defines closed structure; the normative document defines source mapping, exact coverage, identities, captured/current membership, independent applicability, concern candidacy, resolution completeness and normalized reader fields. Both producer preparation and importer/reader proof below must follow that same source.

## Milestones

### M1. Admit and project selected evaluation accounts

- Milestone kind: implementation.
- Engineering purpose: support v2 disclosure with accurate provenance, independent claims and v1 compatibility through one internal projection.
- Requirements: scoped SR-008/009/085, AR-046 and the approved format's admission and semantic obligations.
- Architecture responsibility: MOD-004 importer/projection; accountable caller-side assessment preparation under MOD-007 policy using MOD-011 records.
- Dependencies: accepted applicable G0 basis, approved complete delivery package and implementation authority. Record execution scope before changing runtime behavior.
- Implementation scope: consume `design/support/requirement-delivery-v2.schema.json`; implement the mandatory semantic stages in `scripts/lib/rem_browser_assessments.py`; integrate capture, normalized projection, bounded companion serialization and prepublication checks in `scripts/lib/rem_architecture_browser.py` and `scripts/render-rem-architecture-browser.py`. Preserve the independent Design path. Update all old internal projection consumers in M2; remove obsolete internal interpretation rather than leaving parallel readers.
- Producer scope: use existing CLI context/attachment reads and retained authored supporting payloads. Make a reproducible caller-side preparation procedure, with any task-local helper retained as operational support. It must check actual source outcomes, authorship, scope, concerns and exact payload identities; it must not infer judgments or scan for a latest record. This plan does not introduce a product producer service or public command.
- Implementation steps: establish independently specified valid/invalid fixtures; add version-specific external admission; implement captured-definition coverage and leaf-first dependency/currentness checks; normalize both versions into the reviewed fields; preserve explicit reuse/clear and original v1 serialization behavior. Update the old test that rejects delivery version 2 so it accepts valid v2 and rejects unsupported versions and boolean/string lookalikes.
- Required verification: TG-1, including real renderer invocation for absence-of-write claims and independent semantic inspection for caller judgments. New closed vocabularies each receive unknown-value regression coverage. Existing structural schema examples remain structural evidence only.
- Validation commands: the schema and browser suites and explicit selector in Validation plan, using real D2 and browser tools where required.
- Expected observable result: valid v1/v2 accounts preserve source meaning and exact captured criteria/outcomes; invalid selections cannot replace outputs; changed support restricts only dependent claims.
- Completion conditions/evidence: every TG-1 partition has actual observations, independently expected results and exact source/fixture identities; no unimplemented semantic branch or skipped required toolchain case is represented as passed. M1 alone does not complete the user-visible extension; the changed internal reader contract is integrated and checked in M2 before delivery.
- Whole-change review contribution: source trust limits, complete admission, attribution, dependency ordering, conflict preservation, resource bounds and compatibility.
- Risks/recovery: malformed or oversized disclosure stops before output writes; preserve original supporting records and prior selected artifact. Restore only task-owned generated outputs after an interrupted publication, as specified below.

### M2. Render, assess and demonstrate the pilot

- Milestone kind: implementation.
- Engineering purpose: expose the admitted results clearly in the existing system tree and demonstrate accountable real preparation through offline reading.
- Requirements: scoped SR-008/009/085/086, AR-046 and the evaluation reading contract.
- Architecture responsibility: MOD-004 reader; independent reporters/reviewers/verifiers retain judgment authority.
- Dependencies: M1 and required checks complete; exact current pilot definitions and selected supporting payloads available. There is no separate milestone approval gate.
- Implementation scope: adapt `viewer.js` and `viewer.css` to the one normalized delivery representation; retain separate Design projection, three labeled indicators, criterion/outcome bases, source/scope/limitations, conflicts/resolutions, history and allocation explanations. Cover rows and both detail routes, reference navigation, complete direct-child counts, keyboard and narrow-screen reading. Add the three specified workspace filters: SRs without ARs, Design gaps and Not assessed; the existing navigation lists and text search do not implement these controls.
- Files and proof consumers: extend `tests/engineering/validation/architecture_browser_tests.py`, `architecture_assessment_ui_checks.cjs` and `architecture_browser_ui_checks.cjs`; reconcile the owning requirement-tree/evaluation documentation with delivered behavior and regenerate `design/architecture/views/browser/` through the existing renderer. Source contract changes need affected Design reassessment, not an implementation-only edit.
- Implementation steps: prove synthetic states first; prepare the four real subjects using actual accounts or explicit absence; retain safe selected payloads through the CLI; generate and inspect a candidate; reassess each materially affected existing Design account before relying on Covered. Runtime source changes may stale many of the 173 current accounts. Preserve their original judgments and renew only after actual review; never update hashes in bulk to manufacture currentness.
- Legacy selection handling: keep the original v1 envelope and an attributable pre-cutover browser copy as retained compatibility/recovery evidence. Exercise it byte-for-byte with the new reader. A selected delivery envelope has one version; do not merge raw v1 accounts into v2 or fabricate their missing Verification provenance. Prepare any new AR-046 v2 claims explicitly, with original historical support remaining in the retained v1 artifact. Null claims remain null when no matching accountable record exists. Compare old and new disclosures and disclose this selection boundary before replacing the selected companion.
- Required verification: TG-2 and TG-FINAL-1, with independent expected states/counts and actual retained sources. A positive synthetic fixture cannot become a real pilot judgment. Retain all required dependencies; if the complete safe selection exceeds 1 MiB, report the unmet pilot rather than truncating it or silently broadening the format.
- Validation commands: browser suite, syntax check, complete delivered-path selector, final local CI, prose enforcement and renderer `--check` with the selected D2 executable.
- Expected observable result: all four subjects are navigable in one tree, actual states or explicit absences agree with their support, no-AR structure is separate from reviewed allocation, and the copied browser reads without a server or store.
- Completion conditions/evidence: current selected bytes and generated identities, producer observation, independent actual assessment support where supplied, required UI/failure cases and uncovered scope are retained. Honest Unknown/Not assessed can satisfy the reading demonstration; an absent producer procedure, missing real source comparison or untested v2 behavior cannot.
- Whole-change review contribution: complete producer→importer→reader behavior, replacement of obsolete internal consumers, existing Design continuity, real account integrity and offline usability.
- Risks/recovery: keep private payloads out of generated output; withhold stale/conflicting positives; compare output and source identities after the last material edit. Restore the backed-up selected artifact if publication is interrupted; preserve original assessments.

### TG-1. Disclosure preparation, admission and projection

Use small realistic temporary models with separate original records/payloads and literal expected outcomes. Establish a valid control before mutating one condition. Use the existing browser test fixture/invocation boundary and actual filesystem where path, byte-preservation or capture races matter. Expected identities use independently specified golden examples; do not call the production identity function to calculate both actual and expected values. Accountable producer semantics additionally need an independent walkthrough of actual CLI-selected records and retained attachments; successful parsing cannot prove that a private judgment was adequate.

| Partition and plausible violation | Required observation and oracle | Primary realization |
| --- | --- | --- |
| Evidence Passed mistaken for Implemented; scoped Verification success inflated; inconclusive/failed/noncurrent hidden | Contrast actual v4 source outcomes and retained explicit claim detail. Inconclusive stays Not assessed; failed scoped criterion stays Failed; noncurrent cannot become current; success requires all applicable units. Source identity refers to pre-existing retained supporting bytes, never the enclosing export. | M1 caller-preparation semantic walkthrough plus controlled source packets through importer; repeat actual pilot path in TG-FINAL-1. |
| AR/SR criteria or IR outcomes incomplete, renumbered or silently aligned | Cover exact C1…Cn versus reviewed O1…On, missing/duplicate/additional/reordered keys, absent/wrong IR basis and independent Design/delivery outcome bases. Compare original definition text and all rows; null claim/basis semantics remain explicit. | M1 schema tests plus semantic browser suite; M2 checks displayed bases. |
| Closed input accepts unknown or ambiguous syntax | Each new enum/const/closed object rejects unknown values before relational checks; test required-null versus omission, duplicate JSON keys including captured definitions, invalid UTF-8, invalid real timestamps, unsupported version and numeric lookalikes. Observe intended diagnostic and unchanged output bytes. | M1 existing schema/browser suites, real renderer rejection before compiler/output. |
| Neighboring claim or unrelated edit stales everything; relocated definition coalesces with current | Change only Implementation support and then only Verification support; separately change a shared basis, unrelated file, definition content/order or path. Old/current paths have different claim identities and preserve history. Declared noncurrent remains restricted despite matching hashes. | M1 independently expected normalized reports and currentness reasons. |
| Captured child support confused with today's topology | Contrast valid leaf-first IR→SR→AR support with reparented still-present child, added/removed/changed membership, invented child, wrong-kind/cross-level/cycle/missing reference and deleted canonical ID. Valid reparenting yields stale history; malformed or unsupported deleted-ID selection rejects. Parent complete claims account for every child; empty membership is explicit. | M1 temporary model and exact selected claim graph; TG-FINAL-1 observes parent explanation. |
| Child pass/failure or Design presence automatically decides parent delivery | Contrast explicit child reliance/nonreliance, adverse child, missing/changed Design dependency, absent unrelated Design selection and direct no-AR evidence. Only declared dependencies constrain neighboring claims; no roll-up or implicit satisfaction. | M1 projection and M2 reader comparison. |
| Failed/open-concern candidate dropped; latest timestamp wins; incomplete resolution hides adverse history | Keep same-state distinct claims and Failed/Passed/open/deferred-concern competitors. Test complete resolution, missing adverse criterion/concern token, new competitor, stale resolution subject and two competing resolutions. Unknown/duplicate references reject; stale/insufficient valid resolutions remain visible with positive selection withheld. | M1 golden candidate sets, reason/disposition results; M2 visible conflict and history. |
| Legacy rewritten or Design version confused with delivery | Test v1 and v2 separately, each with absent and separately selected Design; v1 byte-preserving reuse, legacy source/null semantics, no forged Verification record, unsupported version rejection and independent clear operations. | M1 renderer and normalized output, TG-FINAL-1 candidate reading. |
| Resource or path checks happen after output modification | Use exact accepted/rejected edges: 1 MiB input/serialized companion, 4 MiB normalized data, schema collection/string bounds, 32-container nesting, 1,024 material paths, 16 MiB per file and 128 MiB total. Include Unicode byte growth/final newline, canonical/unsafe/private/generated/symlink paths and text containing markup. Check actual reads are bounded and prior output/companion bytes unchanged on rejection; no truncation or private read. V1 does not silently acquire new v2-only budgets; Design retains its separate 4 MiB cap. | M1 real reader/filesystem boundary; representative external renderer rejection for each distinct prepublication failure mechanism. |
| Capture changes between comparison and publication | Controlled change after initial capture and before publication stops generation; no mixed-generation artifact. Distinguish unavailable safe support (restricted claim) from unavailable required capture (rejected generation). | M1 controlled fault with actual captured files and real output snapshots. |

The current `DeliveryDisclosureSchemaTests` checks structure only. Existing `test_assessment_identity_and_independent_claim_applicability`, `test_assessment_rejection_before_compilation_or_writes`, byte-limit and generation/reuse/clear tests protect v1/Design boundaries; extend their distinct observations for v2 instead of assuming new semantics are covered. Keep useful regressions, including original-definition history and no-write rejection. Case counts are not adequacy targets.

### TG-2. One honest requirement workspace

At desktop and 390-pixel width, inspect tree rows and both detail routes for all three kinds, direct links and Back/Forward, keyboard expand/collapse and reference navigation. Compare literal expected states, criteria/outcomes, scope, source, limitations, conflict/disposition details and original history. Distinguish no account from stale account, failed candidate from unresolved authoritative selection, no AR from no further AR needed, and absent Design from independent delivery. For the three new filters, independently specify exact matching IDs: SRs without ARs uses captured current tree membership, Design gaps matches current Design Gap, and Not assessed matches current Verification Not assessed (including true absence), excluding stale Needs reassessment. Intersect each filter with text search; keep contextual ancestors visible but exclude them from match totals. Clear filters and confirm prior selection and expansion remain; exercise Back/Forward and Reveal-in-tree from a filtered detail selection. Full direct-child counts and denominators must remain unchanged by search/filter hiding and cannot set the parent result. Existing no-AR/gap navigation lists alone cannot demonstrate these filter controls. Use the existing Puppeteer harness with real generated HTML; block network and confirm no script errors, executable injected prose or unexpected requests. These checks prove captured reading, not later live change detection.

## Final review checkpoint

- Kind: lifecycle-closeout for this complete bounded extension.
- Dependency: M1/M2 and required corrections/checks complete, with exact final selected source and artifact identities.
- Assessment: one independent whole-change Code Review covering every changed producer/consumer, existing behavior, generated output and cross-milestone interactions. No mandatory per-milestone reviews.
- Evidence: actual independent judgment, exact assessed subjects, current support and explicit concern dispositions.
- Successor: distinct final Verify of this repository-browser delivery. Corrections return to their owner and receive proportionate reassessment within the same whole-change gate. Wider customer handoff and pre-existing unrelated obligations are not closed by this pilot.

## Change-level verification

### TG-FINAL-1. Four subjects from accountable preparation to copied reading

The producer and independent verifier select actual supported CLI records/attachments for AR-046, SR-085, SR-050 and IR-002, recording explicit absence where unavailable. Compare scope, complete captured criteria/outcomes, evidence limitations, membership and actual source identity to the disclosed values. Exercise the complete CLI-read→retained-support→safe-disclosure→real-renderer→copied-reader path; parser-only fixtures cannot prove it. Inspect original IR review support rather than interpreting a child total as an outcome assessment. SR-050's reviewed allocation remains separate from its direct delivery account. Record who performed each judgment and comparison.

Keep the real legacy v1 artifact as exact compatibility/history support and compare its original AR-046 meaning under the new reader. Separately generate the v2 pilot, ordinary regeneration/check reuse, explicit delivery clearing and restoration from the retained selection, with Design independently retained or cleared. Confirm no private storage/network lookup. Copy the complete generated artifact away from the source checkout; compare both routes at desktop/narrow widths and use keyboard navigation. Independently compare expected labels and full membership counts to source accounts, not to another projection of the same possibly faulty renderer.

Reject a malformed candidate at the real generation boundary and compare every prior selected/generated byte. Exercise controlled prepublication failure and an interrupted output write separately: the former preserves prior output, while the latter must report failure and recover from the captured selection/backup without claiming atomic multi-file rollback. Recovery must return an identifiable coherent artifact whose renderer check and offline reading pass. Preserve unrelated sentinel files during restore. Retain exact commands, environment/toolchain, input/output identities, results and limitations; observations expire when materially relied-upon sources, selection or procedures change.

## Validation plan

Use supported Node, Python, D2 and the existing Puppeteer/Chromium toolchain. Set `REM_D2`, `REM_PUPPETEER` and `REM_CHROMIUM` to inspected available executables/modules and place the supported Node executable on PATH. Required browser checks must actually run; a missing toolchain or skipped case is not success. No new dependency is selected by this plan.

```bash
python3 tests/engineering/validation/architecture_schema_tests.py
python3 tests/engineering/validation/architecture_browser_tests.py
node --check scripts/resources/rem-architecture-browser/viewer.js
bash scripts/ci.sh --mode explicit --path design/support/requirement-delivery-v2.schema.json --path scripts/lib/rem_browser_assessments.py --path scripts/lib/rem_architecture_browser.py --path scripts/render-rem-architecture-browser.py --path scripts/resources/rem-architecture-browser/viewer.js --path scripts/resources/rem-architecture-browser/viewer.css --path tests/engineering/validation/architecture_browser_tests.py --path tests/engineering/validation/architecture_schema_tests.py --path tests/engineering/validation/architecture_assessment_ui_checks.cjs --path tests/engineering/validation/architecture_browser_ui_checks.cjs
python3 scripts/render-rem-architecture-browser.py --check --d2 "$REM_D2"
bash scripts/ci.sh --mode local
git diff --check
```

These are future implementation commands. Expand the explicit path list to the actual delivered sources, documentation and generated output; inspect selection completeness and run the applicable groups. Run final local checks only against the complete authorized implementation and disclose unrelated baseline failures. Keep failed aggregates as failed alongside diagnosed reruns. Manual producer/judgment and recovery observations above remain required even when automated suites pass.

For this plan-only authoring pass, run `python3 scripts/validate-documentation-prose.py --mode enforce --path docs/plans/2026-10-05-requirement-evaluation-pilot.md`, `bash scripts/ci.sh --mode explicit --path docs/plans/2026-10-05-requirement-evaluation-pilot.md` and `git diff --check`. Independent delivery review evaluates allocation adequacy; those commands do not execute the proposed v2 proof.

## Risks and recovery

False positive presentation is the main risk. Require actual accountable judgments, complete outcome/criterion coverage and explicit adverse dispositions. Match retained payload identities before serialization, preserve noncurrent status despite matching bytes, and do not infer implementation from tests. Real pilot assessments may remain unknown without blocking truthful capability, but missing required source checks or recovery proof remain delivery gaps.

Before any actual selection cutover, retain exact prior companions and generated files with a file manifest, content identities and original absence/presence. The current renderer replaces prepared files directly and does not promise multi-file atomic publication. If an output write is interrupted, stop using that candidate; regenerate from the exact retained selection and compatible sources/toolchain, or restore only backed-up affected outputs and remove only task-created additions named in the manifest. Then run renderer `--check` and copied-page inspection. Do not replay record writes to repair browser files, rehash original judgments, reset the shared worktree or delete unrelated user files.

The old renderer cannot read delivery v2. Rollback therefore restores the original v1 companion and corresponding generated artifact, with the compatible prior runtime, before attempting ordinary reuse. A version downgrade is not permission to reinterpret v2 records or convert Verification into legacy Evidence. Retain the v2 source payloads operationally with their original scope for later supported reading. Disclosure preparation must inspect actual selected prose for privacy; schema/path checks cannot authenticate an actor or detect every sensitive string.

## Dependencies

Accepted requirement and G0 Design bases precede complete delivery review; applicable execution authority then permits M1, M2, whole-change Code Review and distinct final Verify. Existing Design assessments materially affected by runtime/source changes need explicit independent reassessment before current positive reliance. Actual pilot accounts and any supporting child claims must fit the unchanged disclosure limits. New requirement, format or ownership decisions return to their responsible author and affected review rather than being hidden inside implementation tasks.

## Material rationale

Two milestones separate the admission/projection boundary from the composed reader and actual account demonstration. One whole-change review assesses their integration. Four primary subjects expose three requirement kinds, a parent/child pair and a real no-AR case without broadening product scope. Maintain one internal delivery interpretation while preserving externally supported v1 bytes, separate Design authority and explicit v2 selection. The browser remains a reading projection of assessments, not an assessment engine.

## Readiness

See the owning Change for current basis, delivery-review standing, unresolved obligations and execution authority. This document supplies stable delivery intent; it does not announce approval, implementation progress or requirement satisfaction.
