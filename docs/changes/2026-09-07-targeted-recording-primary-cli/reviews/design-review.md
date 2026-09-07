---
{
  "schema_version": 1,
  "change_id": "2026-09-07-targeted-recording-primary-cli",
  "id": "design-review",
  "target": "design",
  "reviewer": {
    "id": "record-format-rereview",
    "role": "review"
  },
  "contributors": [
    {
      "id": "codex-root",
      "role": "design"
    },
    {
      "id": "user",
      "role": "human"
    }
  ],
  "independence_basis": "The separately delegated record-format-rereview agent independently read all three complete models and their proposal/review basis and authored none of the reviewed model content. The user supplied direction and codex-root authored the model changes. The same independent reviewer now records its existing changes-requested assessment in the supported record store; no new approval is claimed.",
  "subjects": [
    {
      "path": "docs/design/workflow.md",
      "identity": "sha256:526d1d300db4eb1a7a772b9c0621c570bc04c73b3ae3a4424f1162d044571ee1"
    },
    {
      "path": "docs/design/cli.md",
      "identity": "sha256:938c9aeea27174f6ba7e86e839365b84c68a9765c84455dd648d435a9b461761"
    },
    {
      "path": "docs/design/record-format.md",
      "identity": "sha256:ec75b838464949029db9353995bf0fc69fabb3219ed1cc81d056a04b5e340782"
    }
  ],
  "judgment": "changes-requested",
  "findings": [
    {
      "id": "rf-dr-001",
      "reporter": {
        "id": "record-format-rereview",
        "role": "review"
      },
      "owner": {
        "id": "codex-root",
        "role": "design"
      },
      "subjects": [
        {
          "path": "docs/design/cli.md",
          "identity": "sha256:938c9aeea27174f6ba7e86e839365b84c68a9765c84455dd648d435a9b461761"
        }
      ],
      "evidence": "CLI model lines 258 and 274-278 define observation_identity as the hash of {schema_version: 1, revision, observations}, with diagnostics containing code, safe message and locations but no required observed external subject identity. Line 278 nevertheless promises conflict when an observed external subject changes. A retained subject identity A can observe B on the first scan and C on the next, both different from A. The registered revision and the subject-drift code, location and fixed safe message can all remain identical, so the explicitly defined digest input remains identical. This is a missing identity input, not a hash collision or an external edit during publication.",
      "required_outcome": "Make the exact observation digest input and continuation contract agree about changes to the observed external basis, including B-to-C drift that preserves the diagnostic category, location and message. Preserve bounded storage receipts and safe diagnostics; detail retrieval must not become a write prerequisite. Bind a deterministic observed path/identity basis, including absence, or define an equivalent identity-bearing diagnostic representation and acceptance case. Any deliberate narrowing to diagnostic-content stability must be an explicit reconciled Design decision and independently rereviewed.",
      "state": "open",
      "resolution": null
    }
  ]
}
---
# Design review of the Workflow, CLI and Record Format models

## Result and exact scope

Review status: changes-requested. The exact three-model subjects and their byte identities are in this record's metadata. Workflow owns actor decisions, Record Format owns durable layout and preservation, and CLI owns commands, construction and persistence. Each file combines requirements and architecture; no separate ADR member applies. This review grants no design approval, downstream progression, implementation authority, runtime activation or release readiness.

This is the independently conducted review recorded by its original reviewer in the supported explicit-recording-v1 store. The previous evidence placement was unsupported and has been removed. No deleted document, prior chat or Git history is required to understand the finding below. The supported v1 record has no v2 origin field; its full original finding basis and supporting judgment are retained here and in the finding's structured fields rather than inventing a new field.

## Finding RF-DR-001

Stored finding ID: rf-dr-001. Severity: medium. Scope: artifact-local. Affected model: cli. Correction owner and stage: codex-root, Design authoring. Reporter and disposition owner: record-format-rereview.

Location: CLI model, Primary result schema, diagnostics and preview, and Bounded storage receipt and diagnostic detail (lines 258 and 274-278 of the exact reviewed subject).

CLI model lines 258 and 274-278 define observation_identity as the hash of {schema_version: 1, revision, observations}, with diagnostics containing code, safe message and locations but no required observed external subject identity. Line 278 nevertheless promises conflict when an observed external subject changes. A retained subject identity A can observe B on the first scan and C on the next, both different from A. The registered revision and the subject-drift code, location and fixed safe message can all remain identical, so the explicitly defined digest input remains identical. This is a missing identity input, not a hash collision or an external edit during publication.

Required outcome: Make the exact observation digest input and continuation contract agree about changes to the observed external basis, including B-to-C drift that preserves the diagnostic category, location and message. Preserve bounded storage receipts and safe diagnostics; detail retrieval must not become a write prerequisite. Bind a deterministic observed path/identity basis, including absence, or define an equivalent identity-bearing diagnostic representation and acceptance case. Any deliberate narrowing to diagnostic-content stability must be an explicit reconciled Design decision and independently rereviewed.

Rationale: an actor using the two expected selectors is promised fresh diagnostic context, including changes to observed external subjects. A digest over an unchanged diagnostic projection cannot establish that stronger claim. A subject that is already drifted and then changes again is a distinct acceptance case from a previously matching subject becoming drifted.

Safe resolution path: the CLI Design author can add precisely defined, deterministically ordered observed external path/identity pairs to the digest, including explicit absence, or an equivalent identity-bearing diagnostic shape. Define equivalent basis reconstruction for candidate/current scans and test the already-drifted B-to-C case while the registered revision stays constant. Narrowing the freshness promise instead requires an explicit Design decision reconciling the related requirements and temporal acceptance scenario. No owner decision is missing if the current promise is retained. Independent rereview must assess the exact corrected package; this finding remains open.

## Supporting package assessment

Primary new-root creation explicitly selects v2 only after coordinated activation. Existing v1 roots retain compatible operations and advanced v1 creation remains a separate compatibility facility. Governance, schemas, runtime, skills and adapters still require coordinated adoption; the design does not change today's supported stored profile.

The record_contract addition supports the first targeted update: primary change-scoped reads expose the stored discriminator and revision from one snapshot, including empty selections; absent roots use null and invalid stores do not fabricate a contract. Writes still check freshness and actor-declared basis.

Bounded receipts separate storage results from potentially large diagnostics. The finite changed-target/count representation fits the documented reserve, optional detail can be explicitly omitted, and publication cannot become false rejection due to output delivery failure. RF-DR-001 concerns diagnostic retrieval freshness, not that core availability design.

Normal verify show, decisions show and full context selectors expose complete narratives, identities and applicability, with separate absent/missing/malformed behavior. Immutable v2 concern origin retains the original subjects, reporter, evidence, outcome and rationale, with explicitly absent or embedded supporting judgment. Later current assessments preserve that basis across targeted and advanced writes and recovery. These prospective requirements are not claimed as implemented by this v1 review record.

Purpose-specific commands and batch share final-candidate validation, lossless preservation, expected revision checks and exact-byte recovery. Findings and blockers retain distinct correction/disposition responsibility. Failed Verify and a new blocker remain recordable after completed work, with Route making a later independent routing decision. No additional material finding was identified in the reviewed package. Concrete runtime proof, adapter adoption and complete-interaction token measurements remain Delivery obligations.

## Validation and limits

The reviewer confirmed the three model files remain identical to the previously reviewed a5035818 revision using git diff a5035818 --exit-code -- docs/design/workflow.md docs/design/cli.md docs/design/record-format.md. This corroborates the earlier subject review; the metadata identities and recording read set bind the actual current subjects without requiring Git to interpret the finding.

Previously run model checks passed: python scripts/validate-boundary-first.py --check --path docs/design/cli.md --path docs/design/workflow.md --path docs/design/record-format.md (structure-and-references-only), and python scripts/validate-markdown-readability.py docs/design/cli.md docs/design/workflow.md docs/design/record-format.md (226 audit-only warnings). These checks do not establish semantic approval or runtime correctness. No implementation test was performed for this design-only assessment.

The present recording uses record-store inspect, then check and record of the same transient request with exact expected revision, manifest identity and model read identities. Successful storage means this changes-requested review was saved, not that its finding was resolved or that progression was approved.
