---
{
  "schema_version": 1,
  "change_id": "2026-09-07-targeted-recording-primary-cli",
  "id": "delivery-review",
  "target": "delivery",
  "reviewer": {
    "id": "delivery-reliance-review",
    "role": "review"
  },
  "contributors": [
    {
      "id": "codex-root",
      "role": "plan"
    }
  ],
  "independence_basis": "Explicitly delegated independent Delivery reviewer reassessed the complete unchanged primary plan against the exact current approved Design Review and model/proposal basis without authoring the plan, models or the two M5 spec amendments. The reviewer independently authored only the separately attributed Design classification of those amendments, not their contents. This new assessment evaluates allocation and safe sequencing afresh, preserves prior reviewer attribution and all DP findings, and is not an automatic digest refresh or an implementation/Verify judgment.",
  "subjects": [
    {
      "path": "docs/plans/2026-09-07-targeted-recording-primary-cli.md",
      "identity": "sha256:2078ea15010d79a50941cc3bfaa80fa02d521972bb97c6cc01ee2e89cc5d393d"
    },
    {
      "path": "docs/design/workflow/workflow.md",
      "identity": "sha256:a3727f571eec0f9ae34bfdda31f9f7711e3903abdabd31e28903b8c3b69b2251"
    },
    {
      "path": "docs/design/cli/cli.md",
      "identity": "sha256:951c0f427e118914d70c1f326a02ae01efab47107a1cca897211b980b9d8d22c"
    },
    {
      "path": "docs/design/record-format/record-format.md",
      "identity": "sha256:6ddfcd350212437ddf2feaade14818fd66f9a04b8a00ccb01c5fb13291879eeb"
    },
    {
      "path": "docs/proposals/2026-09-07-targeted-recording-primary-cli.md",
      "identity": "sha256:8200c3145bbdbe929be893c7fdd9327a829308084a31efe25d96a032b9b4f0c4"
    },
    {
      "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/reviews/design-review.md",
      "identity": "sha256:0719f7cb5aa5e02f0bbb0bd80cfc72e94396f0f2ceeaba95a8688082bb3bac3f"
    },
    {
      "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/reviews/proposal-review-r1.md",
      "identity": "sha256:bdd21f4d0f122445ddf6f9f3bedb1d7b6b00eba59ad6da56ef20399d3270691a"
    },
    {
      "path": "specs/rigorloop-workflow.md",
      "identity": "sha256:0eae07ea872452fe203d01d50049b47e5df97b82542237af520d644671198cbc"
    },
    {
      "path": "specs/skill-contract.md",
      "identity": "sha256:ced40b68fc8c4e610b3bd66b19c10d4f8c0b2c394cd14adf95cd18c41cf35ca3"
    }
  ],
  "judgment": "approved",
  "findings": [
    {
      "id": "dp-01",
      "reporter": {
        "id": "targeted-delivery-review",
        "role": "review"
      },
      "owner": {
        "id": "codex-root",
        "role": "plan"
      },
      "subjects": [
        {
          "path": "docs/plans/2026-09-07-targeted-recording-primary-cli.md",
          "identity": "sha256:635e121d38ab31b45e47581a96204f59efbede92fef22b9224dfe3f799e5ed50"
        }
      ],
      "evidence": "User-discovered and independently validated. M5 Review handoff; M6 Dependencies; Dependencies and Readiness: The original plan required Code Review for M1\u2013M5 and integrated tests, then proceeded to Verify without explicitly requiring final independent review of the complete integrated implementation. Workflow Context and Scope and WF-MAP-02 explicitly retain final Code Review. Milestone-only assessment could therefore satisfy the written handoff without the required whole-change judgment.",
      "required_outcome": "Make final whole-change independent Code Review a prerequisite to Verify, against current implementation subjects and approved design/delivery basis, with no unresolved material findings. A shared final milestone invocation is acceptable only when whole-change scope is explicit.",
      "state": "resolved",
      "resolution": {
        "actor": {
          "id": "targeted-delivery-review",
          "role": "review"
        },
        "rationale": "M5 handoff, M6 dependencies, Dependencies and Readiness now require final independent whole-change Code Review and explicitly reject substitution by an M5-only review or integration tests. Current subjects and no unresolved material findings are required. This allocates the retained obligation without inventing a separate lifecycle stage.",
        "evidence_refs": []
      }
    },
    {
      "id": "dp-02",
      "reporter": {
        "id": "targeted-delivery-review",
        "role": "review"
      },
      "owner": {
        "id": "codex-root",
        "role": "plan"
      },
      "subjects": [
        {
          "path": "docs/plans/2026-09-07-targeted-recording-primary-cli.md",
          "identity": "sha256:635e121d38ab31b45e47581a96204f59efbede92fef22b9224dfe3f799e5ed50"
        }
      ],
      "evidence": "User-discovered and independently validated. M5 TG-08 and completion criteria; Validation plan token comparison: The original plan required running a full-interaction comparison and recording measurements but did not make supported qualitative benefit or an owning-Design disposition of unfavorable/inconclusive evidence a completion condition. CLI token evaluation requires failure to reduce routine reconstruction/context to return to the owning Design decision before adoption. Benchmark completion alone could therefore permit an unsupported adoption recommendation.",
      "required_outcome": "Require evidence supporting reduced routine reconstruction and avoidable context with adequate decision basis, or explicit owning-Design disposition and required rereview before adoption recommendation. Allocate reproducible named fixtures and a documented procedure for the complete comparison without inventing a percentage threshold.",
      "state": "resolved",
      "resolution": {
        "actor": {
          "id": "targeted-delivery-review",
          "role": "review"
        },
        "rationale": "TG-08, M5 completion and Readiness now make the qualitative acceptance/disposition explicit. Four named runnable fixtures, reset/construction, paired command sequences, guidance/help, tokenizer/version, environment, retries and inclusion rules are allocated, with C2/C4 automation and human basis-adequacy assessment. Unfavorable or inconclusive results return to Design; no unqualified adoption recommendation follows simply from completing the benchmark.",
        "evidence_refs": []
      }
    },
    {
      "id": "dp-03",
      "reporter": {
        "id": "targeted-delivery-review",
        "role": "review"
      },
      "owner": {
        "id": "codex-root",
        "role": "plan"
      },
      "subjects": [
        {
          "path": "docs/plans/2026-09-07-targeted-recording-primary-cli.md",
          "identity": "sha256:635e121d38ab31b45e47581a96204f59efbede92fef22b9224dfe3f799e5ed50"
        }
      ],
      "evidence": "User-discovered and independently validated. M4 TG-05 required verification: The original TG-05 phrase origin null/direct/from-review blurred required v2 Origin with its optional supporting judgment. Record Format requires a complete Origin for each v2 concern; only supporting_judgment may be null. The shorthand could direct tests toward accepting invalid v2 concern representation.",
      "required_outcome": "Distinguish mandatory v2 origin construction from supporting judgment explicitly absent, supplied directly or copied from an exact selected review. Allocate rejection of missing/null v2 origin while preserving v1 compatibility.",
      "state": "resolved",
      "resolution": {
        "actor": {
          "id": "targeted-delivery-review",
          "role": "review"
        },
        "rationale": "TG-05 now states required v2 origin, names the three supporting-judgment forms, and explicitly tests rejection of missing/null v2 origin with unchanged v1 compatibility absence. The correction agrees with RF-SR-01/04 and CLI finding-origin construction.",
        "evidence_refs": []
      }
    }
  ]
}
---
# Current independent Delivery Review reassessment

Outcome: approved. Reviewer: delivery-reliance-review (role: review). This is a genuinely new bounded independent assessment of the exact current delivery package for final reliance. It replaces the prior current Delivery judgment without attributing newer subjects to the prior reviewer. The plan, three governing models and prior DP finding bases are unchanged; the Design Review file changed only by appending a separately attributed independent classification of two exact M5 new-profile-only spec amendments. Its original structured Design reviewer/member map/judgment/finding and prior body remain unchanged.

The reviewer read the complete primary plan and reassessed its requirement-to-boundary-to-milestone-to-proof trace against the known unchanged model package and the new classification. M1 representation and field-specific references precede M2 coherent publication, identities and exact-byte recovery. M3 scoped reads and bounded diagnostics precede M4 lossless construction, explicit origin/applicability and related updates. M5 explicitly allocates the amended governance/skill entry surfaces, resource closure and supported-package proof, so the new-profile-only classification adds no unallocated implementation or verification requirement. Historical procedures, v1 compatibility, explicit v2 creation and separately authorized activation remain correctly distinguished.

The allocated normal/negative proof still covers each model dimension and the material compositions: stale declared basis, mixed readers/writers, interruptions and recovery, no-op/retry, unsafe containment, immutable origin, final-candidate references, full Verify/decisions reads, diagnostic density and B-to-C continuation drift. TG-FINAL-01 joins the public correction and safe-recording interaction; TG-FINAL-02 joins consumer/resource/installed-package coherence. C1-C10 remain concrete repository-owned checks, with structural validation and human assessment assigned distinct roles. Recovery after any v2 write retains version-capable readers and exact prepared bytes rather than replaying a constructor or migrating old data.

DP-01 remains resolved: final independent whole-change Code Review with current integrated subjects and no unresolved material findings is explicit in M5 handoff, M6 dependencies, Dependencies and Readiness. A milestone-only review does not satisfy it. DP-02 remains resolved: TG-08 requires named equivalent full interactions, guidance/help and follow-up inclusion, tokenizer/call totals, adequate decision basis and supported qualitative benefit, or owning-Design disposition of unfavorable/inconclusive results before adoption recommendation. Completing an experiment alone is insufficient. DP-03 remains resolved: v2 origin is required; only supporting judgment may be absent, and the plan separately preserves v1's lack of origin. All structured finding fields, original subjects, discovery attribution and dispositions are retained exactly.

The two spec amendments are explicitly allocated M5 entry-profile changes. Their Design-owned classification preserves the historical remainder and changes no approved model behavior, public semantic rule, milestone scope or acceptance consequence. No new Design decision, Delivery correction, historical feature-format adoption or additional artifact is required for this package. This conclusion is limited to the exact current subjects in the new structured assessment.

Validation actually performed for this review: read the selected recorded context; recomputed the existing Delivery subject identities and found only the expected Design Review body digest change; compared current Design metadata and original-body prefix to the prior committed record and confirmed preservation; ran `python scripts/validate-boundary-first.py --check --path docs/design/cli/cli.md --path docs/design/workflow/workflow.md --path docs/design/record-format/record-format.md`, which passed structure/reference validation. These checks support identity/document structure, not implementation correctness. The transient check/record request binds every exact new subject.

New findings: none. Recording status: recorded. Explicit applicability is current for this exact Delivery assessment. Plan/models, implementation, prior findings and routing are not edited. Next owner: the final whole-change Code Reviewer may rely on this current Delivery judgment; M6 Verify remains a separate downstream responsibility. This review makes no Code Review, implementation-completion, Verify, branch/PR readiness, release or customer-activation claim.

## Retained prior Delivery assessment attribution and subject map

The following former current metadata and narrative are historical evidence from the previous reviewer. They are not the subject map of this new assessment and are not retargeted to newer bytes.

```json
{
  "reviewer": {
    "id": "delivery-fresh-review",
    "role": "review"
  },
  "independence_basis": "Separately delegated delivery-fresh-review execution independently read the entire primary plan, traced its allocation against the three approved models and proposal, checked exact upstream subject identities and inspected proof harnesses. This reviewer authored no plan or model content and was not the previous approving reviewer. codex-root remains the plan contributor; role labels themselves do not authenticate independence.",
  "subjects": [
    {
      "path": "docs/plans/2026-09-07-targeted-recording-primary-cli.md",
      "identity": "sha256:2078ea15010d79a50941cc3bfaa80fa02d521972bb97c6cc01ee2e89cc5d393d"
    },
    {
      "path": "docs/design/workflow/workflow.md",
      "identity": "sha256:a3727f571eec0f9ae34bfdda31f9f7711e3903abdabd31e28903b8c3b69b2251"
    },
    {
      "path": "docs/design/cli/cli.md",
      "identity": "sha256:951c0f427e118914d70c1f326a02ae01efab47107a1cca897211b980b9d8d22c"
    },
    {
      "path": "docs/design/record-format/record-format.md",
      "identity": "sha256:6ddfcd350212437ddf2feaade14818fd66f9a04b8a00ccb01c5fb13291879eeb"
    },
    {
      "path": "docs/proposals/2026-09-07-targeted-recording-primary-cli.md",
      "identity": "sha256:8200c3145bbdbe929be893c7fdd9327a829308084a31efe25d96a032b9b4f0c4"
    },
    {
      "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/reviews/design-review.md",
      "identity": "sha256:86a25fafdf99fdc9e4782d91b2d6005751f0dcfaac5801a052001ceed3632971"
    },
    {
      "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/reviews/proposal-review-r1.md",
      "identity": "sha256:bdd21f4d0f122445ddf6f9f3bedb1d7b6b00eba59ad6da56ef20399d3270691a"
    }
  ],
  "judgment": "approved"
}
```

## Retained prior Delivery narrative

# Delivery review of targeted recording and Record Format v2

## Result

- Skill: delivery-review
- Review status: approved
- Package members: primary-plan = docs/plans/2026-09-07-targeted-recording-primary-cli.md. Its exact identity and the approved design/proposal basis are in structured subjects.
- Upstream review ID: design-review; approved and explicitly current, with all fourteen reviewed subject identities verified.
- Review ID and round: delivery-review, fresh independent rereview by delivery-fresh-review.
- Traceability result: all CLI-SR-01–22, RF-SR-01–08 and WF-SR-01–15 have proportional implementation and proof allocation; no material sequencing or verification gap found.
- Material findings: none new or open. Existing dp-01, dp-02 and dp-03 remain resolved with original attribution, subject identities, evidence and dispositions unchanged.
- Correction targets: none.
- Recording status: recorded through the explicit-recording-v1 check/record interface with expected revision and exact decision-basis reads; applicability is an explicit reviewer declaration.
- Settlement status: exact delivery judgment under actor-owned recording; no historical lifecycle settlement or derived routing is claimed.
- Open blockers: none for this delivery judgment.
- Immediate next stage: isolated stop.
- Claim limitations: approval concerns implementation sequence and proof allocation only. It establishes no implemented behavior, runtime safety, token saving, Code Review, final Verify, release or customer activation.

## Fresh independent assessment

The entire primary plan was read rather than relying on the earlier approval. M1 separates closed v2 schema/reference validation from preserved v1 behavior. M2 proves the shared transactional boundary before M3 query/receipt work and M4 targeted construction. Their required proof covers malformed inputs, unsafe paths, changed identities, exact prepared-byte recovery, mixed reader/writer states, retries and absence, with the explicitly limited external-edit guarantee. Public and advanced paths enter the same boundary; independent Code Review precedes each dependent milestone. The existing subprocess and injectable filesystem/transaction harnesses are suitable extension points, not proof that the new behavior already works.

M3 and M4 allocate the important compositions: first-read contract/revision discovery, whole-item scope and pagination, full final narratives, subject inspection, current observed-basis digest including the B-to-C regression, maximum diagnostic density with fitting truthful receipts, all targeted operations and equivalent batch, omitted neighbor/narrative preservation, required applicability, immutable origin and correction recording after completed activity. TG-FINAL-01 exercises these together, including conflicts and interrupted recovery, so milestone checks do not stand in for integrated proof.

M5 requires exact resource closure of named governance, skills, templates, validation and distribution entry points before edits/review, with no required deferred dependency or parallel ordinary reconstruction path. Newly discovered semantic requirements return to Design. Packed CLI and supported adapter proof is allocated through existing repository harnesses and TG-FINAL-02. Normal v2 creation remains coordinated with consumer adoption; this initiative stays v1, historical roots are not converted and rollback retains readers/recovery for any existing v2 data. Publication/customer activation is outside the package.

DP-01 is adequately corrected in M5, M6, Dependencies and Readiness: a final independent whole-change Code Review explicitly assesses the integrated implementation and current subjects before Verify. Sharing the last review invocation is permitted only with whole-change scope; an M5-only review is insufficient. DP-02 is adequately corrected in TG-08, M5 completion, Validation and Readiness: named reusable equal fixtures, documented command/guidance loading and tokenizer/call totals support reproducibility; qualitative benefit with adequate basis, or owning-Design disposition and required rereview, precedes adoption recommendation. Merely completing the experiment is insufficient. DP-03 now explicitly requires v2 origin and rejects missing/null origin while permitting an explicitly absent supporting judgment and preserving v1 compatibility.

The requirement matrix and local/final verification groups cover all eight model dimensions and their named combined hazards without introducing historical boundary-first proof-table prerequisites. C1–C10 are concrete existing harness entry points; the plan allocates future cases and extensions and does not claim they already prove the new format. M6 assesses complete current evidence only after milestone and whole-change reviews, returns defects to their owner and writes a success explanation only on success. No material correction is required by this rereview.

## Fresh validation evidence

- Ran record-store inspect for the selected change. Recomputed all current review subjects, including the fourteen upstream Design Review subjects and the proposal/plan basis; all matched. The stored design approval and applicability are current.
- Ran python scripts/validate-boundary-first.py --check --path docs/design/cli/cli.md --path docs/design/workflow/workflow.md --path docs/design/record-format/record-format.md: passed, structure-and-references-only.
- Ran node scripts/build-record-store-schema.mjs --check: passed for the existing compatibility baseline.
- Ran python scripts/validate-markdown-readability.py docs/plans/2026-09-07-targeted-recording-primary-cli.md: passed with 101 audit-only warnings.
- Inspected record-store CLI/workflow test entry points, filesystem/transaction fault injection, schema builder, adapter distribution and npm package publication harnesses for the proposed proof extension. No future implementation suite is claimed as executed.
- Recording binds the expected complete registered revision, exact subjects and upstream example/compatibility identities. The only writes are this review and its explicit applicability/matching review activity. Subsequent inspect checks the stored result; no plan, design, routing or implementation edits are made.

The existing subject-drift observations describe retained historical finding bases, including rf-dr-001 and the original DP plan identity. They do not contradict the separately checked current reviewed subjects and are not silently rewritten or used as approval evidence.

## Retained previous assessment and finding evidence

The following is preserved from targeted-delivery-review's earlier assessment. Its reviewer/discovery attribution and resolutions are historical evidence; the fresh judgment above owns the current assessment. No original finding basis or disposition is changed.

## Reassessment and retained feedback

The user identified three valid issues after the initial approval. The initial review missed the explicit final whole-change Code Review obligation and the qualitative benefit acceptance condition, and accepted ambiguous origin wording. This reassessment corrects that judgment rather than treating the earlier approval as sufficient evidence. The author revised only the plan; the reviewer read the revised plan in full and independently checked these corrections against the unchanged current approved models. The three adopted findings retain the original plan identity and user discovery attribution below.

## Finding DP-01

- Finding ID: dp-01
- Severity: medium
- Location: primary-plan, M5 Review handoff; M6 Dependencies; Dependencies and Readiness.
- Evidence: The original plan required Code Review for M1–M5 and integrated tests, then proceeded to Verify without explicitly requiring final independent review of the complete integrated implementation. Workflow Context and Scope and WF-MAP-02 explicitly retain final Code Review. Milestone-only assessment could therefore satisfy the written handoff without the required whole-change judgment.
- Required outcome: Make final whole-change independent Code Review a prerequisite to Verify, against current implementation subjects and approved design/delivery basis, with no unresolved material findings. A shared final milestone invocation is acceptable only when whole-change scope is explicit.
- Safe resolution path: Plan author corrects allocation/wording; independent Delivery Review reassesses the exact revised plan. No upstream behavior change is required.
- Finding scope: artifact-local.
- Affected artifact IDs: primary-plan.
- Owning stages: plan for correction; delivery-review for reassessment.
- Discovery attribution: user feedback identified this issue after the initial approval; targeted-delivery-review independently validates and adopts the finding and owns this disposition. It was not discovered during the initial review.
- Original basis: the original primary-plan identity remains in the structured finding; it is not replaced with the corrected subject.
- Current disposition: resolved. M5 handoff, M6 dependencies, Dependencies and Readiness now require final independent whole-change Code Review and explicitly reject substitution by an M5-only review or integration tests. Current subjects and no unresolved material findings are required. This allocates the retained obligation without inventing a separate lifecycle stage.

## Finding DP-02

- Finding ID: dp-02
- Severity: medium
- Location: primary-plan, M5 TG-08 and completion criteria; Validation plan token comparison.
- Evidence: The original plan required running a full-interaction comparison and recording measurements but did not make supported qualitative benefit or an owning-Design disposition of unfavorable/inconclusive evidence a completion condition. CLI token evaluation requires failure to reduce routine reconstruction/context to return to the owning Design decision before adoption. Benchmark completion alone could therefore permit an unsupported adoption recommendation.
- Required outcome: Require evidence supporting reduced routine reconstruction and avoidable context with adequate decision basis, or explicit owning-Design disposition and required rereview before adoption recommendation. Allocate reproducible named fixtures and a documented procedure for the complete comparison without inventing a percentage threshold.
- Safe resolution path: Plan author corrects allocation/wording; independent Delivery Review reassesses the exact revised plan. No upstream behavior change is required.
- Finding scope: artifact-local.
- Affected artifact IDs: primary-plan.
- Owning stages: plan for correction; delivery-review for reassessment.
- Discovery attribution: user feedback identified this issue after the initial approval; targeted-delivery-review independently validates and adopts the finding and owns this disposition. It was not discovered during the initial review.
- Original basis: the original primary-plan identity remains in the structured finding; it is not replaced with the corrected subject.
- Current disposition: resolved. TG-08, M5 completion and Readiness now make the qualitative acceptance/disposition explicit. Four named runnable fixtures, reset/construction, paired command sequences, guidance/help, tokenizer/version, environment, retries and inclusion rules are allocated, with C2/C4 automation and human basis-adequacy assessment. Unfavorable or inconclusive results return to Design; no unqualified adoption recommendation follows simply from completing the benchmark.

## Finding DP-03

- Finding ID: dp-03
- Severity: low
- Location: primary-plan, M4 TG-05 required verification.
- Evidence: The original TG-05 phrase origin null/direct/from-review blurred required v2 Origin with its optional supporting judgment. Record Format requires a complete Origin for each v2 concern; only supporting_judgment may be null. The shorthand could direct tests toward accepting invalid v2 concern representation.
- Required outcome: Distinguish mandatory v2 origin construction from supporting judgment explicitly absent, supplied directly or copied from an exact selected review. Allocate rejection of missing/null v2 origin while preserving v1 compatibility.
- Safe resolution path: Plan author corrects allocation/wording; independent Delivery Review reassesses the exact revised plan. No upstream behavior change is required.
- Finding scope: artifact-local.
- Affected artifact IDs: primary-plan.
- Owning stages: plan for correction; delivery-review for reassessment.
- Discovery attribution: user feedback identified this issue after the initial approval; targeted-delivery-review independently validates and adopts the finding and owns this disposition. It was not discovered during the initial review.
- Original basis: the original primary-plan identity remains in the structured finding; it is not replaced with the corrected subject.
- Current disposition: resolved. TG-05 now states required v2 origin, names the three supporting-judgment forms, and explicitly tests rejection of missing/null v2 origin with unchanged v1 compatibility absence. The correction agrees with RF-SR-01/04 and CLI finding-origin construction.

## Traceability and sequencing assessment

The complete primary plan was read. Its requirement matrix allocates CLI-SR-01 through CLI-SR-22, RF-SR-01 through RF-SR-08 and WF-SR-01 through WF-SR-15 to named implementation milestones, verification groups and concrete command entry points. The model-specific mapping replaces historical four-table proof serialization for this explicitly selected profile; no missing historical boundary IDs are invented. All eight dimensions and material interactions have direct scenario allocation rather than a Cartesian product.

M1 establishes closed versioned JSON representation and reference resolution before M2 extends persistence. M2 proves recovery, identity checks and coherent publication before M3 exposes scoped reads and bounded results. M4 builds purpose-specific and batch operations on those boundaries. Each implementation milestone requires independent Code Review before its dependent milestone. M5 reconciles the consumer/distribution package only after the implemented engine and operations have proof; Final independent Code Review assesses the complete integrated implementation before M6 independently assesses complete-change evidence. The last milestone invocation may cover both scopes explicitly; milestone-only review cannot substitute for the whole-change assessment.

TG-01 covers v2 EntryRef field-specific target collections, disjoint per-file IDs, malformed and missing targets, same-candidate references and the distinct retained v1 membership rule. Immutable origin is allocated both to representation comparison and to targeted, advanced and recovery paths. No historical root conversion, fabricated origin or schema renaming is authorized.

TG-02 allocates writer/reader concurrency, absent-root races, identity conflicts, unsafe paths and substitutions, interruption phases, restore/complete, unknown recovery state and stale retries. The requirement to preserve exact prepared bytes prevents recovery from reconstructing a different candidate. The external-editor guarantee remains limited to observed checks, and rollback after v2 data exists retains a capable reader/recovery implementation.

TG-03/TG-04 cover every selected query family, contract/revision discovery, selected full narratives, scope omissions and cursor identity. The rf-dr-001 regression receives direct proof: B-to-C drift must invalidate continuation even when diagnostics and registered revision are unchanged. Retained-origin Subject traversal, confirmed absence, duplicate subjects, silent-subject drift and exclusion of request-only reads are explicitly allocated. Maximum admissible diagnostic density must fit the receipt without an invented subject-count gate or false post-publication rejection.

TG-05 covers the complete purpose-specific mutation catalogue and batch, byte-preserving omitted content, required explicit decisions, registration/applicability, origin construction variants, overlapping edits, same-batch references, preview, no-op and retry. TG-06 and TG-FINAL-01 demonstrate correction after completed work, independently recorded routing, reporter-owned disposition and final assessment. Role labels remain attribution and save success never establishes workflow approval. Public subprocess proof and shared-engine parity prevent helper-only tests from substituting for admitted entry paths.

TG-FINAL-01 joins first-read contract discovery, subject identity, failed evidence/blocker, successive actor decisions, independent reassessment, final explanation and ordinary downstream reads. It includes v1, conflicts, interrupted recovery and maximum diagnostics. TG-FINAL-02 joins governance, skills, templates, schema dispatch, packed CLI and every supported adapter. These final groups are necessary even after all focused milestone checks pass.

## Adoption and feasibility assessment

M5's named governance, stage/support skill and validation/distribution entry points define the resource boundary. Its mandatory expansion of their references/assets into exact changed-or-unaffected paths before edits and closure before Code Review is an implementation task with an explicit acceptance condition, not a claim that directory inventories prove complete adoption. No required dependency may remain deferred, and newly discovered semantic requirements return to Design. This is adequate bounded allocation without guessing future resource diffs during review.

Coherent normal v2 creation is prepared as one implementation/guidance package. Earlier milestones withhold ordinary activation. Existing v1 roots and advanced v1 creation remain explicit compatibility paths; the initiative's own v1 manifest and reviews are not converted. Release publication and customer activation are outside the requested work. Rollback cannot remove the ability to read or recover already-created v2 records.

The named validation commands are feasible repository-owned harnesses. Direct inspection confirmed existing record-store CLI tests support subprocess behavior and injected filesystem/transaction failures, the schema builder checks canonical/package parity, package publication tests pack/install the current CLI in temporary fixtures, and adapter distribution tests exercise archives and resource closure. The plan explicitly allocates new tests and v2 bundling extensions rather than asserting these existing harnesses already prove the prospective behavior. C2 includes new record-store-prefixed suites; C4 exercises the complete CLI regression suite. C5 is correctly limited to document structure, and C10 to whitespace.

TG-08 measures complete interactions on equal isolated fixtures, including loaded guidance, required reads, previews/retries and follow-up reads with tool/tokenizer versions. It makes no invented numerical threshold or proven benefit claim. Evidence and reviewer assessment must support the selected qualitative benefit with adequate decision basis, or unfavorable/inconclusive evidence must receive owning-Design disposition and any required rereview before an adoption recommendation. Named runnable fixtures and documented procedure make the comparison reproducible. Mechanical correctness remains mandatory regardless of measured token differences.

## Validation and recording evidence

- Independently ran record-store inspect and recomputed the registered plan, proposal and model identities plus every subject in the current upstream Design Review. All matched; design-review judgment is approved and applicability current.
- Ran python scripts/validate-boundary-first.py --check --path docs/design/cli/cli.md --path docs/design/workflow/workflow.md --path docs/design/record-format/record-format.md: passed, structure-and-references-only.
- Ran python scripts/validate-markdown-readability.py docs/plans/2026-09-07-targeted-recording-primary-cli.md: passed with audit-only warnings; rerun on the revised plan for this reassessment.
- Ran node scripts/build-record-store-schema.mjs --check: passed for the existing compatibility baseline; this does not prove v2 implementation.
- Read packages/rigorloop/test/record-store-cli.test.js, scripts/build-record-store-schema.mjs, scripts/test-npm-package-publication.py and scripts/test-adapter-distribution.py to assess harness feasibility. No implementation test suite was represented as proving future work.
- The transient record-store check/record request binds the exact plan, three models and upstream review/proposal basis, preserves existing review evidence and findings, and publishes this review with explicit applicability and matching review activity. Subsequent inspect verifies the result.

The reviewer did not edit the primary plan or approved models. The existing truthful historical rf-dr-001 subject may still produce subject-drift; it remains resolved in the upstream review and is not rewritten by this review. No historical lifecycle command, advisory document, review log or durable operation request is introduced.
