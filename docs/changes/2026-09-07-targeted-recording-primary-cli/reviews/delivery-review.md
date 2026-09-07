---
{
  "schema_version": 1,
  "change_id": "2026-09-07-targeted-recording-primary-cli",
  "id": "delivery-review",
  "target": "delivery",
  "reviewer": {
    "id": "targeted-delivery-review",
    "role": "review"
  },
  "contributors": [
    {
      "id": "codex-root",
      "role": "plan"
    }
  ],
  "independence_basis": "Separate delegated agent /root/targeted_delivery_review independently read the complete plan and assessed its sequencing and proof allocation. The reviewer authored no plan or model content and owns this judgment; the parent authored the plan. Role text records attribution, while the distinct review execution supplies independence evidence.",
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
# Delivery review of targeted recording and Record Format v2

## Result

- Skill: delivery-review
- Review status: approved
- Package members: primary-plan = docs/plans/2026-09-07-targeted-recording-primary-cli.md. This is the sole delivery member; the approved models and upstream reviews are supporting decision basis, not extra delivery members. Exact identities are in metadata.
- Upstream review ID: design-review; all current model and relied-on review subjects matched their recorded identities and its declared applicability is current.
- Review ID and round: delivery-review, independent reassessment after user findings DP-01, DP-02 and DP-03; the stable record retains the original finding basis.
- Traceability result: sufficient implementation sequencing and verification allocation for every affected model requirement and material boundary hazard.
- Material findings: dp-01 and dp-02 resolved; wording finding dp-03 resolved; none open.
- Correction targets: none.
- Recording status: supported actor-owned recording through record-store with explicit current applicability.
- Settlement status: not-applicable to historical lifecycle settlement. This record owns the exact delivery judgment under the selected explicit-recording-v1 profile; persistence itself establishes storage only.
- Open blockers: none identified within this delivery package.
- Immediate next stage: isolated stop. No routing decision is recorded.
- Claim limitations: Delivery approval only; no implementation correctness, completed milestone, final Verify, branch readiness, publication or customer activation is claimed.

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
