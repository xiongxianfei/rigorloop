# Simple requirement evaluation

This document defines assessment reading in the [system Requirements view](requirement-tree.md), owned by MOD-004. It answers how to evaluate IRs, SRs and ARs consistently, including SRs with no ARs. The repository renderer accepts the original AR-only delivery version 1 and the [IR/SR/AR delivery version 2](requirement-delivery-format.md). The scoped design-review disclosure below supplies actual IR/SR/AR design judgments without changing their canonical definitions or inferring delivery results.

## Read actual selected assessments in the architecture browser

The [system Requirements workspace](../../../../views/browser/index.html#requirements/SR-085) displays available, explicitly selected design judgments on ordinary IR/SR/AR rows and detail pages. There is no separate preview mode or uniform example-state overlay. This is repository Design reading support; it does not assess a requirement automatically or establish a production customer assessment service.

Design state comes from an actual retained design-purpose review, with exact assessed definition, material source identities, actor/time, scope, criterion conclusions, limitations and review reference. No selected review means Not reviewed with an absence explanation. A selected Covered or Gap judgment remains distinct from implementation and verification. IRs without a reviewed stakeholder-outcome basis remain Not reviewed; child coverage never creates an IR result.

Implementation and verification come from explicitly selected delivery accounts. Absence reads Unknown / Not assessed with a missing-account explanation for every requirement kind. Existing stale AR accounts retain historical results and show current Unknown / Needs reassessment; new design coverage cannot renew them.

The detail panel presents real criterion-by-criterion design reasoning, remaining gaps, actual source/review attribution and separately qualified implementation/verification. Direct-child state counts use all distinct declared children, including unknown/unreviewed/stale states, and never set the parent's judgment. Lists of SRs without ARs and reviewed design gaps navigate the same tree. No-AR is a structural fact; only an actual allocation review may call it an unexpressed necessary obligation.

### Scoped design-review disclosure

The repository renderer accepts `--design-reviews PATH`, explicitly selecting a sanitized retained operational attachment. Its generated `design-review-snapshot.data` companion freezes those exact disclosed accounts for deterministic regeneration and offline embedding; ordinary generation/check reuses that named companion. `--clear-design-reviews` replaces only that selection with an empty one. Existing `--assessments` and its version 1 AR disclosure retain their contract. The renderer does not scan private records, select a latest review or authenticate an actor. The caller must select actual applicable judgments and resolve known contradictory operational support before disclosure.

The design-only envelope has closed fields `format_version` and `reviews`. Version 1 retains its SR/AR-only meaning. Version 2 adds reviewed IR stakeholder-outcome accounts; every version 2 account additionally has `outcome_basis`, null for SR/AR accounts. Each account has `requirement`, `definition` (`path`, SHA256 `identity`, original JSON `content`), `state` (covered or gap), `scope`, `actor`, UTC `reported_at`, `review` (`change`, `id`), `summary`, `limitations`, `subjects` (nonempty path/identity list), `criteria` (complete numbered entries with `state` covered/gap and nonempty `explanation`), `allocation`, and `ar_children`. Selected SR/AR definitions must match their stable identity and kind. Every captured criterion appears exactly once; Covered requires all criteria covered. Gap requires an identified criterion or allocation gap. Criterion statements come from captured definition bytes, never rewritten by the renderer.

For SR accounts, `ar_children` is the captured sorted unique child-AR identity list; `allocation` is null or `{state, explanation}`, with state review-needed, deferred, required or not-required. A Covered SR with no AR requires an explicit reviewed not-required rationale; a covered claim cannot have a required/deferred/review-needed allocation. For AR accounts both fields are null. Material source, definition, kind or child-membership changes downgrade Design to Needs reassessment with the original judgment and rationale retained. Allocation explanations inherit that applicability. Membership and identities are compared at generation; a copied snapshot does not detect live changes.

Version 2 admits an IR only with an explicitly reviewed stakeholder-outcome basis. It does not add SR/IR delivery claims or the broader operational export contract. Unknown versions/fields/states, duplicate accounts/keys/criteria/subjects, unsafe or private paths and inconsistent complete claims reject before diagram compilation or output writes. Reuse the existing size, UTF-8, JSON, contained-path and symlink protections. The historical selected review remains operational; generated disclosure is a shareable reading projection, not authored assessment authority.

For an IR, `outcome_basis` contains `identity`, `outcomes`, `sr_children` and `support`. Each outcome contains `number`, nonempty `text` and nonempty `sources` with exact public path/identity pairs also declared in the account's material `subjects`. Outcome numbers are contiguous from one. They express the assessor's reviewed reading of the exact need and relevant Features/Scenarios, not invented canonical IR acceptance criteria. The nonempty sorted unique `sr_children` captures every direct SR; `support` contains exactly one `{requirement, identity}` reference for each child, binding the canonical JSON bytes of its selected original Design account. The basis identity binds the remaining basis fields by SHA256 of UTF-8 JSON with sorted keys, compact separators and unescaped Unicode. Support identities use the same canonical JSON rule. All SR/AR version 1 bytes remain readable without migration; version 2 SR/AR accounts use `outcome_basis: null`.

An IR account has null `allocation` and `ar_children`; its complete numbered `criteria` assess every declared outcome, and the reader labels them **Assessed stakeholder outcomes**. Covered requires every outcome covered plus all selected relied-upon child accounts current and covered. This consistency guard cannot manufacture an IR judgment: a complete independent account remains mandatory. Gap requires an identified outcome gap. Missing, changed or stale relied-upon child accounts and changed direct-SR membership make the original IR assessment Needs reassessment. A selected adverse child prevents a parent Covered account from being shown current; a parent's explicit Gap may remain current with the adverse support it assessed. Changed outcome sources similarly preserve only the historical judgment. An edited basis without its corresponding digest rejects; a newly self-consistent basis is still only caller-supplied and must have actual independent review before selection.

IR outcome presentation adds no acceptance-criteria field to canonical IR definitions, no automatic child roll-up and no new runtime assessment service. The UI exposes outcome source identities, basis identity and exact relied-upon child-account identities. Without an IR account the existing Not reviewed explanation remains unchanged. Negative cases include missing/empty outcomes, incorrect outcome numbering, missing source attribution, changed basis bytes, incomplete support membership, invalid version/state, conflicting positive support, and changed child/source identities. These complement the existing SR/AR admission and offline-reading checks.

Acceptance observations cover two reviewed Covered accounts, a real Gap account, a genuinely unreviewed IR, stale AR history, absent neighboring accounts, source/criterion identity changes, changed AR membership, unknown vocabulary, malformed/rejected selection, explicit reuse/clearing, and copied offline narrow/keyboard navigation. Source judgments and presentation adequacy receive separate attributable review. No dummy positive or negative result is attached to a real requirement for demonstration.

## Basis and boundaries

Reuse IR-002, SR-008/009 and SR-085: preserve authored relationships, expose bounded traceability and present attributable engineering meaning. FUNC-007/009/080/081 retain their existing MOD-004 allocation. This extends their requirement-reading behavior without adding a Function, Module, Interface or allocated obligation. Requirement validity, design coverage, implementation and satisfaction remain distinct under the [Requirement model](../../../../../../rem/models/requirements.md).

The extension stays in the optional RigorLoop system Requirements workspace. It adds no Module-level requirement view, status editor or second dashboard. Canonical requirement definitions retain lifecycle status only. Assessment judgments and follow-ups remain operational records; the browser presents explicitly selected, sanitized accounts through the existing capture and assembly boundary.

## One compact evaluation per requirement

Every IR, SR and AR row presents three separately named indicators. Definition lifecycle remains in details. The reader never derives an assessment from link counts, code presence, test totals or child statuses.

| Indicator | States | Meaning |
| --- | --- | --- |
| Design | Not reviewed / Gap / Covered / Needs reassessment | No applicable reviewed coverage account; a reviewed material design gap; reviewed coverage of the whole obligation; or a previous account whose basis is no longer applicable |
| Implementation | Unknown / Not started / Partial / Implemented | Reuse the existing implementation meanings at this requirement's complete assessed scope |
| Verification | Not assessed / Failed / Passed / Needs reassessment | Reuse the existing verification meanings at this requirement's complete assessed scope |

Not reviewed and Unknown are absence of a usable account, not adverse judgments. Not started requires an explicit report. Partial requires identified realized scope and remaining gaps. Covered, Implemented and Passed require complete applicable support for their respective claims; none implies the other two. Inconclusive verification remains Not assessed with its limitation visible. A confirmed applicable failure must not disappear behind unassessed remainder.

Design Covered is a supplied reviewed coverage conclusion, not merely a count of design links or a generic approved-review label. It includes required logical behavior, architectural responsibility, interactions and realization relevant to the obligation. Coverage approval does not establish execution or successful verification.

Display text is independent of color. At narrow widths, the three labeled indicators wrap below the requirement title; all remain readable. Missing accounts show the absence states without hiding the requirement.

## Evaluate each level at its own scope

| Level | Assessment basis | Supporting material |
| --- | --- | --- |
| AR | Exact AR definition and every acceptance criterion, at its single allocated Module's responsibility | Owning design, implementation references and criterion evidence |
| SR | Exact SR definition and every acceptance criterion, including integrated system behavior | Confirmed/constrained Functions, architecture, applicable AR accounts and direct system evidence |
| IR | Exact need statement and an explicitly reviewed stakeholder-outcome basis | Derived SRs, confirmed Features and relevant governed Scenarios, plus integrated outcome evidence |

SR and AR criteria are taken from the captured definition, preserving exact text and identity. An assessor may map one criterion to several design/evidence references, or one observation to several criteria, but must justify each contribution and expose remaining scope. Passing an isolated implementation test is not automatically an assessment of its mapped criteria.

The current IR schema has no acceptance-criteria field. Do not fabricate canonical criteria, use an empty list as success, or copy SR criteria into the IR. A selected operational IR account must identify a reviewed outcome basis: stable outcome labels, assessable outcome statements, their mapping to the IR need and relevant Feature/Scenario/SR sources, reviewed source identities, limitations and accountable assessment actor. The reader labels these **Assessed stakeholder outcomes**, not **IR acceptance criteria**. Without this basis, show Not reviewed / Unknown / Not assessed with “Stakeholder outcome basis not established.” Missing or conflicting stakeholder intent returns to requirement analysis; an assessment cannot rewrite the IR.

Implementation at SR/IR level means the scoped system capability or stakeholder outcome is reported realized. It does not allocate that requirement to every supporting Module. Each account names its responsible reporting actor; architecture responsibility continues to come from the model. MOD-007 retains assessment/judgment policy; MOD-004 owns presentation only.

## SRs with no AR

Compute the factual label **No AR declared** from the complete captured containment model. Never convert it automatically into Not started, Failed, design Gap, or allocation complete. Existing Functions and their accountable Modules remain visible, but they are not substitute ARs or proof of allocation completeness.

Alongside the fact, show an explicitly recorded architectural disposition when available:

| Disposition | Required explanation |
| --- | --- |
| Review needed | No applicable allocation disposition is supplied |
| Allocation deferred | What responsibility is unresolved, its accountable follow-up owner and the next decision |
| AR required | The uncovered lower-level obligation, intended responsible boundary and owned AR-authoring follow-up |
| No further AR needed | Reviewed rationale that no required lower-level obligation remains unexpressed, the existing responsibility/design references and the direct system assessment approach |

No further AR needed is not a waiver of required architectural allocation. If a lower-level obligation is needed, the [allocation method](../../../../../../rem/methods/architecture-allocation.md) requires an AR with exactly one accountable Module. The disposition cannot claim design Covered while necessary allocation remains unresolved. Conversely, applicable direct SR evidence may be displayed without manufacturing an AR; design and verification remain separate claims.

The disposition binds the SR definition, relevant design/Function/Module identities and selected AR membership. Adding an AR, changing necessary responsibility or altering that basis requires reassessment. Preserve the previous rationale as history and show Review needed with the cause. The same completeness review applies to SRs that already have ARs: one AR is not proof that all lower-level obligations are covered.

## Child summaries are counts, not parent judgments

An IR summarizes its distinct direct SR children; an SR summarizes its distinct direct AR children. Reference occurrences, Functions and Module links never enter the denominator. Show total child count and explicit state counts for each indicator, including unknown, unassessed and stale states. A filtered tree keeps the full captured count and labels the visible subset separately.

An illustrative SR summary may read: “AR verification: 2 passed, 1 failed, 2 not assessed; 5 total.” The SR's own Verification indicator still comes from its direct assessment. An IR's denominator is SRs, not all descendant ARs. Zero children displays “No SR declared” or “No AR declared”; it never displays 100% or a vacuous pass. Omit percentages in the first version.

Applicable child failure or newly adverse evidence within the relied-upon parent scope creates an explicit conflict that withholds current parent Passed until the responsible verifier resolves its relevance. It does not mechanically declare the parent Failed. A child result outside the parent's assessed scope remains visible with its stated non-reliance reason. A parent's complete positive claim cannot exclude one of its own required outcomes by narrowing its scope. All child passes likewise cannot manufacture a parent pass or establish decomposition completeness.

## Details and filters

Keep the existing selected-node detail panel. Its first section gives a concise reason for each indicator. Expandable detail supplies:

- assessed scope and revision, actual actor/time and source record;
- each criterion or assessed stakeholder outcome, design references, implementation account, evidence and remaining gap;
- child contribution and any uncovered integrated behavior;
- architectural disposition and next owned action where applicable;
- historical states and the reason current applicability was lost.

Add **SRs without ARs**, **Design gaps**, and **Not assessed** filters to the same workspace. SRs without ARs uses captured membership; Design gaps matches current Design Gap accounts; Not assessed matches current Verification Not assessed. Stale verification remains a distinct state, available in details and state summaries. Filters show matching requirements and contextual ancestors, compose with text search by intersection, preserve current selection and expansion on clear, and never change counts or model data. Contextual ancestors are not counted as matches. Reuse the existing Back/Forward and Reveal-in-tree behavior.

## Assessment selection and applicability

Reuse the existing caller-selected operational disclosure boundary, not live store discovery. Each independent claim retains requirement kind/ID, exact definition identity, full assessed basis, scope, actor/time, source records, outcome coverage, evidence, limitations and gaps. Design accounts additionally identify their actual design-purpose review support; no newly invented generic progress record owns approval. Reuse supported Evidence/Review/Verification accounts and retained disclosure attachments; no storage migration is required for this design.

Claims track separate material subjects and separate applicability. Changed definitions invalidate coverage mapping for all dependent claims; changed claim-specific sources restrict the affected claim. IR outcome bases and SR allocation dispositions carry their own identities. Parent accounts identify relied-upon child assessment references/identities and coverage, not just child IDs. Selected new contradictory support must be exposed rather than resolved by newest timestamp. Assembly diagnoses conflicting supplied current accounts and withholds positive presentation.

The repository Design companion uses deterministic compact JSON: sorted keys, UTF-8 with unescaped Unicode, compact separators and one final newline. This removes formatting overhead as the selected assessment population grows; it preserves every parsed field and the exact decoded definition-content strings and identities. The selected Design export and generated Design companion have a 4 MiB admission limit; the separate delivery disclosure retains its 1 MiB limit. The earlier 1 MiB shared cap is insufficient for the growing complete system assessment: the 88-account compact selection already occupies about 0.95 MiB before this IR-007 branch. A bounded 4 MiB Design allowance provides room for the current requirement tree and justified allocation growth without truncating judgments or material dependencies; it is not an unlimited-model guarantee. Indented and compact JSON inputs have the same meaning when admitted; generation normalizes only the Design companion, and subsequent frozen-selection reuse and `--check` must succeed on that output. Delivery-companion serialization and its 1 MiB limit, and the operational CLI request limit, are unchanged. Admission reads at most the applicable limit plus one byte, rejects any excess before JSON decoding/compilation/output writes and retains the same strict schema, identity and duplicate-key checks for admitted content. Before compilation or output writes, also check the normalized Design companion including its final newline against the same cap; an admitted input must not generate a companion that frozen reuse would reject. Reject an oversized input or normalized result rather than silently dropping accounts, sources or explanations.

The copied browser states what was assessed in its captured snapshot. It cannot discover subsequent live changes. Comparison and reassessment happen at explicit selection/assembly or assessment boundaries. Unrelated edits and operational bookkeeping alone do not invalidate a claim.

The version 1 AR export must not silently gain new fields or admit IR/SR records. The [G0 delivery format](requirement-delivery-format.md) and its exact schema define the version 2 producer/importer/reader contract, including closed vocabulary, kind-specific coverage, claim identities, dispositions and version 1 normalization. The repository importer and reader consume the matched version 2 representation; actual selected accounts and qualification remain attributable operational evidence. Existing selected version 1 AR accounts remain readable with Design Not reviewed; they must not acquire invented design judgments. Unknown versions/kinds/states or inconsistent coverage reject before output writes, preserving the prior artifact. The concrete contract supplies the architecture basis for the broader delivery-assessment export; its separately selected operational accounts remain authoritative, and version 2 Design disclosure never supplies delivery version 2 judgments.

## Acceptance intent for the extension

These are specified observations, not executed tests or satisfaction claims.

| Situation | Required observation |
| --- | --- |
| Requirement has no selected assessment | All three absence states and their reason are visible; Draft remains separate |
| SR has no AR and no allocation disposition | No AR declared / Review needed; no inferred failure or completion |
| Direct SR proof exists without ARs | Attributed SR verification is readable; unresolved design/allocation remains separately visible |
| SR has one AR but an uncovered necessary obligation | Reviewed design gap and owned AR follow-up remain visible |
| All children passed, parent unassessed | Child counts show passes; parent remains Not assessed |
| Relied-upon child has applicable adverse evidence | Parent's positive presentation is withheld with the conflict and required reassessment |
| IR has no reviewed stakeholder-outcome basis | No fabricated criteria, zero-item success or inherited pass |
| Definition, outcome basis, allocation or relied-upon child support changes | Affected positive claims are withheld; exact previous scope and historical explanation remain readable |
| Search/filter hides some children or repeats shared references | Full distinct-child denominator is unchanged and visible subset is explicit |
| Only a version 1 AR selection is supplied | Existing AR claims keep their original meaning; Design defaults to Not reviewed; IR/SR remain unassessed |
| Copied artifact is read offline at narrow width or by keyboard | Labels, evidence limitations, filters and selected-node details remain usable |

## Realization and handoff

The existing reader/projection remains the implementation location: `scripts/lib/rem_browser_assessments.py`, `scripts/lib/rem_architecture_browser.py`, `scripts/resources/rem-architecture-browser/viewer.js` and `viewer.css`, with the renderer retaining explicit selection. No new runtime service, datastore, mutable requirement field or automated assessment engine is proposed. MOD-004 owns coherent producer/consumer projection; source and judgment owners keep their existing authority.

This companion keeps assessment ownership separate from browser presentation. The scoped Design disclosure and versioned delivery disclosure make explicitly selected IR/SR/AR accounts readable in the same tree. Extend the selected inventory only after actual attributable assessment. Do not bulk-generate ARs or statuses to populate the view.
