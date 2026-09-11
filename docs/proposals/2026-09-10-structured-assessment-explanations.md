# Structured Review and Verify Explanations

## Challenge

Review and Verify currently place their remaining explanation in a required `body` string. Readers cannot select a rationale or limitation directly, and authors must replace mixed narrative to edit one part. Readable rendering improves presentation but does not make the underlying explanation independently addressable.

The [Record Format](../design/record-format/record-format.md) already gives judgments, findings, actors, subjects and evidence authoritative structured homes, and prohibits a narrative from maintaining competing status, findings or reviewer rosters. The problem is the remaining explanation: conclusion summaries, assessment scope, reasons, limitations and delivered-change explanations share one undifferentiated field.

## Goals

- Let actors supply, readers select and responsible assessors edit meaningful explanation fields directly.
- Keep each assessment fact in one authoritative location and derive readable output from stored values.
- Preserve assessment integrity, immutable finding origins, explicit applicability and safe concurrent recording.
- Introduce an explicit replacement stored contract with coherent adoption and preservation of historical assessments.

## Scope and non-goals

This proposal selects one coordinated Review/Verify stored-record redesign. The following table preserves the initial request and bounds its supporting work; slice allocation remains a Delivery decision.

| Initial intent | Goal treatment | Scope budget treatment | Destination |
| --- | --- | --- | --- |
| Four shared explanation fields and Verify-specific delivered changes replace `body` | in scope | core to this proposal | Record Format |
| Direct field selection, narrow edits and derived readable output | in scope | core to this proposal | CLI |
| Existing facts, finding origins, applicability and assessment authority remain intact | in scope | same-slice dependency | Record Format, CLI, Review and Closeout, Workflow |
| Explicit verification-basis disposition without universal Git requirements | in scope | same-slice dependency | Verify policy owner and Record Format |
| Coordinated version adoption and unfinished-work disposition | in scope | same-slice dependency | Record Format, CLI and Workflow |
| Aligned skills, schemas, examples, validators and package generation | in scope | same-slice dependency | Existing content, validation and Distribution owners |
| Universal reports, arbitrary paragraph objects, extension bags and unrestricted patches | rejected option | out of scope | No new Report model or generic JSON system |
| Automatic narrative conversion and historical approval reinterpretation | rejected option | out of scope | Preserve historical bytes and meanings |
| Redesigning evidence entries or material-decisions `body` | out of scope | out of scope | Retain existing contracts |

No required consumer alignment is deferred to an unnamed follow-up. Publication, customer activation and conversion of existing work require their existing separate authority. This isolated authoring request creates a proposal only; it does not activate a governed change or authorize implementation.

## Governing principle

Give each explanation a meaningful home while leaving assessment authority with its responsible actor.

## Proposed direction

Replace Review and Verify `body` with the following small explanation vocabulary. These are proposed direction constraints, not implemented schema or commands.

| Field | Proposed value | Meaning |
| --- | --- | --- |
| `summary` | Nonempty string | Explain the conclusion without repeating its status. |
| `assessment_scope` | Nonempty string | Explain coverage and supported reliance; exact identities remain in `subjects`. |
| `rationale` | Nonempty array of substantive strings | Complete reasons supporting the conclusion, including missing basis for an inconclusive review. |
| `limitations` | Array of strings | Known assessment or evidence limits; an explicit empty list claims no listed limitations, not completeness. |
| `changes` | Array of strings, Verify only | Final explanation of what was delivered, not an execution log or task list. |

Preserve Review's `target`, `reviewer`, `contributors`, `independence_basis`, `subjects`, `judgment` and `findings`; preserve Verify's `verifier`, `subjects`, `evidence_refs`, `review_refs` and success-only `outcome`. Referenced evidence retains actual checks, procedures, results and its own actor-authored summary. Existing change records retain current work, blockers and next activity. Do not introduce explanation status, blocker counts, reviewer rosters, recording receipts or field-level approvals.

Extend existing Review and Verify reads with explicit named-field projection, with `--fields` as proposed syntax. Without selection, return the normal complete selected record. Explicit selection returns exactly the requested content with record identity, coherent revision, contract, applicability and selection/omission metadata; it must not masquerade as complete context. Unknown fields reject. Selection is mechanical and does not choose which reasons justify approval.

Retain complete `review.record` and `verify.record` assessments and add narrow `review.set` and `verify.set` operations limited to the corresponding explanation fields above. Updates replace whole named values; omitted fields and unrelated bytes remain unchanged, semantic no-ops preserve bytes, and arrays are neither merged nor patched by index. Missing targets, stale revisions, invalid nulls and empty required values reject. Complete creation requires summary, scope and at least one substantive rationale item. Design settles the remaining field cardinality and validation details.

Changes to judgment, exact subjects, assessor identity or verification evidence basis require a complete reassessment operation. Complete Review replacement continues to preserve findings, which retain separate explicit operations. Neither targeted editing, complete replacement nor recovery refreshes immutable finding origins or embedded supporting judgments from an edited explanation.

Successfully storing an edit does not establish applicability, independent review, verification success or permission to progress. A responsible assessor distinguishes editorial correction from a change affecting reliance, explicitly updates applicability and records necessary corrections, using existing transactions when related edits must publish together. Newly discovered failed proof requires failed evidence and its owned blocker; it cannot be concealed as a harmless limitation edit. Structurally recordable incomplete or contradictory claims remain correctable without CLI endorsement or prose-based inference.

Human output renders the supplied selected values as headings and lists without synthesizing rationale, dropping reasoning or retaining another editable report. Multiline strings and code examples remain valid; decoded presentation and JSON encoding remain distinct. New-format Review/Verify records reject both legacy `body` and dual representations.

Adopt an explicit replacement stored-contract version, provisionally `rigorloop-records-v3`, coherently across each change store and registered records. Request, response and document-validation versions remain separate domains. New stores use the new fields only after coordinated adoption. Completed historical records remain unchanged. Before removing required v2 support, explicitly resolve any unfinished v2 work through an owner-authorized continuation or separately authorized conversion disposition, including this initiative if subsequently registered under v2. Introducing a version never completes old work; a human-authored new assessment is not a mechanical migration of approval.

Design must explicitly settle `verification_basis` with its existing owner. If current consumers require independently addressable basis values, define a closed conditional object for the applicable assessment; otherwise demonstrate how existing subjects and evidence preserve the necessary basis. Do not infer structure from prose, make branch/remote/merge-base fields universal, or discard required information to fit the baseline.

## Feasibility

Assessment: feasible enough to enter Design, with compatibility and basis ownership requiring explicit resolution before implementation. The [CLI model](../design/cli/cli.md) already describes complete assessment operations, scoped reads with omissions, revision-bound transactions, lossless targeted value edits and semantic no-op preservation. These provide an existing construction path; this proposal does not claim that the proposed fields or operations exist or have passed tests.

The [Review and Closeout model](../design/review-closeout/review-closeout.md) already separates recording from reliance and retains specialist assessment duties. The [Verify skill](../../skills/verify/SKILL.md) and its [branch-readiness procedure](../../skills/verify/references/branch-readiness-verification.md) require normalized verification basis for Git/PR readiness while permitting non-Git closeout. This is concrete evidence that basis disposition needs owner reconciliation, rather than removal or universalization.

Repository-local `workflow-context` discovery succeeds with response schema 2 and reports v2 stores; discovery alone does not establish which work is unfinished. Design must inspect relevant current records before choosing retirement treatment. Repository orientation here relies on the directly inspected owning models and canonical skill sources, not the project map's older architecture inventory.

There is no identified blocker to proposal review or subsequent Design authorship. Design must reconcile Record Format, CLI, Review and Closeout/Workflow and affected skill consumers as one package; Delivery then allocates proof for field selection/editing, invalid and dual representations, stale conflicts, byte/origin preservation, honest partial context, recovery and absence of automatic approval. Runtime implementation and broad regression testing are outside this proposal-only task.

## Impact and major trade-offs

The selected direction intentionally breaks the current closed v2 stored schema; silently changing v2 would reinterpret existing contracts. Coordinated governance, schemas, validators, examples, skills and generated packages are necessary even though the explanation vocabulary is small. [Distribution](../design/distribution/distribution.md) retains package and installation ownership; package availability does not adopt customer governance or authorize release.

Named fields improve access while asking assessors to distinguish reasons, scope and limitations. Whole-field edits keep concurrency and authoring understandable, but do not provide per-paragraph collaboration. Structural validation can protect storage invariants; only the responsible assessor can judge whether an explanatory edit changes the decision's meaning.

## Decision requested

Approve this bounded direction for Design: replace Review/Verify `body` with four shared explanation fields and Verify's `changes`, add explicit projection and two narrow update operations, derive readable output, and coordinate an explicit stored-version change under existing owners. Preserve the stated integrity and historical boundaries, and require explicit verification-basis and unfinished-v2-work dispositions before implementation. Exact schemas, command envelopes, adoption mechanics and verification allocation belong to Design and Delivery. Proposal approval does not establish a new assessment result, activate the replacement contract or approve implementation.
