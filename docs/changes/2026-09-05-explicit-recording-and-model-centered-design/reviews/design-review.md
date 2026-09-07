---
{
  "schema_version": 1,
  "change_id": "2026-09-05-explicit-recording-and-model-centered-design",
  "id": "design-review",
  "target": "design",
  "reviewer": {
    "id": "review-compact-fix",
    "role": "review"
  },
  "contributors": [
    {
      "id": "root",
      "role": "design"
    }
  ],
  "independence_basis": "Current separate review by /root/review_compact_fix, which authored no proposal, model, plan or implementation contribution. /root authored those contributions and coordinated proof; prior reviewer-owned advisory records preserve first-pass findings and actual rereviews. This current assessment rereads the adopted context and exact basis; actor labels alone are not relied on as independence evidence.",
  "subjects": [
    {
      "path": "docs/design/workflow.md",
      "identity": "sha256:29f9c0994e6468ee630516198d2e7d0f6a28ebcaae81ab1ea5b9b43d55b3094e"
    },
    {
      "path": "docs/design/cli.md",
      "identity": "sha256:f0bde78dcdd9bd9daaaaf4639df42f712ea9b9a90184f09ad062244558d535a5"
    },
    {
      "path": "docs/proposals/2026-09-05-explicit-recording-and-model-centered-design.md",
      "identity": "sha256:b4efd7fd9010fa0e9af32207afc68abbc847f12f707047c2f640ec7f6e9e44a9"
    },
    {
      "path": "CONSTITUTION.md",
      "identity": "sha256:ba13fbf7bbce39f8257f91ca07c657f06b3e22658da89807acb3be9512b38a92"
    },
    {
      "path": "specs/rigorloop-workflow.md",
      "identity": "sha256:b755687df0f75199dbab35438895bb23fe26a2e150d75b9407f7cdc589355dde"
    },
    {
      "path": "specs/skill-contract.md",
      "identity": "sha256:02efe372f358bce68a1d1e85e4dcd4ca6a8686c652f0cb1258d2563884215408"
    },
    {
      "path": "specs/boundary-first-proof-model.md",
      "identity": "sha256:a166b68a673d485c83a0b665446933c774406b03a4f464b205426ae9b8b315bb"
    },
    {
      "path": "docs/reviews/explicit-recording-and-model-centered-design.md",
      "identity": "sha256:56e21a1a7d0cda7e38516de99347ddc6c95f59c5e256bcf56e3d3bc9f0a04d6d"
    },
    {
      "path": "docs/changes/2026-09-05-explicit-recording-and-model-centered-design/reviews/proposal-review.md",
      "identity": "sha256:5b14201e9045aacfe606fcdf97fa09a56b178f0fffc68ef3a5748538e150f51f"
    },
    {
      "path": "specs/compact-current-state-change-record.md",
      "identity": "sha256:fb0a17528b0a5653c383ad8aef55b40e06eeaface7a968a9fdd0d46dd04f92e6"
    }
  ],
  "judgment": "approved",
  "findings": []
}
---

# Current Design Review

## Result

- Skill: design-review
- Review status: approved
- Package: workflow → docs/design/workflow.md; cli → docs/design/cli.md
- Upstream current judgment: proposal-review in this change
- Material findings / correction targets: none
- Recording: current explicit-recording-v1 judgment on 2026-09-07
- Settlement: no historical package operation; no automatic downstream handoff
- Claim limitations: exact model-package adequacy, not implementation correctness or Verify

Both complete model files, their owned relationship, embedded decisions, all 21 requirements, both eight-row scenario tables and combined hazards were reread. The prior independent advisory assessments remain unchanged evidence; this is an affirmative current assessment in the explicitly authorized new root. Historical draft/no-root prose records drafting context; current adoption and applicability reside in the change records. No mandatory separate spec/architecture/ADR or OS investigation is introduced.

## Coherence assessment

All six substantive Design criteria pass: the actor/storage architecture supports the required behavior and failures; authority, containment, concurrency and compatibility constraints remain explicit; the accepted simplification goals are not weakened; ownership, trust and recovery boundaries agree; embedded decisions do not conflict; and the package is sufficiently defined for safe Delivery reliance. Structure and semantic judgment remain distinct. Subject drift permits correction recording but prevents unsupported reliance. Failed Verify can record a blocker without a success report, and completed work can reopen explicitly.

The approved external-edit limit remains: no simultaneous manual/other-tool target edits during record/recover; freshness is at observed checks, not atomic protection of the final exact-target window. Cooperating-writer exclusion, substituted-ancestor containment, observed third-state stops and explicit recovery remain mandatory.

## Current shared-authority classification

The exact opening Explicit recording amendments in specs/rigorloop-workflow.md and the first Goal and context paragraph in specs/skill-contract.md are new-profile-only adoption reconciliation, not formatting changes. They select explicitly requested new roots and matching guidance, retain independent review and final Verify, and preserve the historical remainder. The boundary-first-proof-model reconciliation assigns grandfathered semantic classification to Design Review while retaining feature-format/activation rules. Review-required exit zero establishes structural success only; absent or stale classification still blocks reliance. These current subjects are included explicitly. The selector correction restores that settled separation; it requires no new Design decision.

Prior MODEL-DR-001 and subsequent selector-error, external-edit and model-validation clarifications retain their recorded dispositions and rationale in the unchanged advisory record. No approval is inferred merely because hashes match; this reviewer reassessed the exact package and current adoption context.

## Current adoption reconciliation: preserve historical compact specification

- Skill: design-review
- Review status: approved
- Package members: workflow -> docs/design/workflow.md; cli -> docs/design/cli.md; affected adoption boundary -> specs/compact-current-state-change-record.md
- Upstream review ID: proposal-review in this change
- Material findings/correction targets: none
- Recording status: recorded; settlement: no historical lifecycle operation
- Claim limitations: Design coherence only, not implementation or PR verification

The spec owner removed only this initiative's redundant scope paragraph. Independent git diff --exit-code against d6770adfbbd835363d3b428acbd5a27a9485171b confirms exact historical bytes. The current material decision preserve-historical-compact-spec owns the inventory correction: compact specification preserved unchanged, replacing only the earlier implementation-note claim of an added paragraph. Historical records, approvals and subject registrations are untouched.

All six Design criteria remain satisfied. Both model documents and approved direction are unchanged; WF-MAP-02 through06 and CLI-MAP-01 through06 already assign new-profile ownership. Adopted Constitution/workflow/skill-contract provide explicit selection; the removed paragraph owns no unique requirement. This restoration preserves compatibility and independent authority without weakening behavior, changing boundaries or requiring a new model/plan. No blanket stale-evidence waiver or historical approval conversion is granted.
