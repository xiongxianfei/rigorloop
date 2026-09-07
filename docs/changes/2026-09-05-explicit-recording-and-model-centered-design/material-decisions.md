---
{
  "schema_version": 1,
  "change_id": "2026-09-05-explicit-recording-and-model-centered-design",
  "decisions": [
    {
      "id": "explicit-recording-adoption",
      "actor": {
        "id": "root-coordinator",
        "role": "route"
      },
      "subjects": [
        {
          "path": "docs/proposals/2026-09-05-explicit-recording-and-model-centered-design.md",
          "identity": "sha256:b4efd7fd9010fa0e9af32207afc68abbc847f12f707047c2f640ec7f6e9e44a9"
        },
        {
          "path": "docs/plans/2026-09-05-explicit-recording-and-model-centered-design.md",
          "identity": "sha256:2058ebf122e130f7d92f0c5d6dfa464200927ad85f99d4c754893d4ddd4904f4"
        },
        {
          "path": "docs/design/workflow.md",
          "identity": "sha256:29f9c0994e6468ee630516198d2e7d0f6a28ebcaae81ab1ea5b9b43d55b3094e"
        },
        {
          "path": "docs/design/cli.md",
          "identity": "sha256:f0bde78dcdd9bd9daaaaf4639df42f712ea9b9a90184f09ad062244558d535a5"
        },
        {
          "path": "CONSTITUTION.md",
          "identity": "sha256:ba13fbf7bbce39f8257f91ca07c657f06b3e22658da89807acb3be9512b38a92"
        },
        {
          "path": "docs/implementation/explicit-recording-m4.md",
          "identity": "sha256:8a94a65a1ea390f5917393d5eaa21aa78daf42da15d235e6e89e5d6e68c6830b"
        },
        {
          "path": "docs/reviews/explicit-recording-and-model-centered-design.md",
          "identity": "sha256:56e21a1a7d0cda7e38516de99347ddc6c95f59c5e256bcf56e3d3bc9f0a04d6d"
        },
        {
          "path": "docs/reviews/explicit-recording-and-model-centered-design-delivery.md",
          "identity": "sha256:a41728e98c4018a3ee9b47c7d0757d8dbf5e95c71e9bc1fcc3232b3b813b9273"
        },
        {
          "path": "docs/reviews/explicit-recording-m1-code-review.md",
          "identity": "sha256:94d54108699b64e2466f1d6bb211b3cdeb9eb9864562993c35e6720a74812349"
        },
        {
          "path": "docs/reviews/explicit-recording-m2-code-review.md",
          "identity": "sha256:1787d5e21b82ef7599db76020f0b3f2d996ed30c2d33386fa6f1db41bfc3b9e1"
        },
        {
          "path": "docs/reviews/explicit-recording-m3-code-review.md",
          "identity": "sha256:694bdec6f994f655252d4839cebbdf022f955c11c2b81ac1f8ca06c08b14c984"
        },
        {
          "path": "docs/reviews/explicit-recording-m4-code-review.md",
          "identity": "sha256:f7f4db5fdb0b57f073c004723aafca99c7175d97a1a4c4f9c291ccac5eb19d4c"
        }
      ],
      "rationale": "On 2026-09-07 the user explicitly approved creation of this previously absent explicit-recording-v1 root, preservation of existing review evidence, and resuming M5. M4 packaged adoption and distinct whole-change review are clean-with-notes. This records new-contract selection in the isolated worktree only; it grants no commit, publication or historical migration. Existing advisory records and exact judgments remain unchanged; their independent owners must record any new current judgment, never relabel old evidence automatically.",
      "source_refs": []
    },
    {
      "id": "preserve-historical-compact-spec",
      "actor": {
        "id": "root-spec",
        "role": "design"
      },
      "subjects": [
        {
          "path": "specs/compact-current-state-change-record.md",
          "identity": "sha256:fb0a17528b0a5653c383ad8aef55b40e06eeaface7a968a9fdd0d46dd04f92e6"
        },
        {
          "path": "docs/design/workflow.md",
          "identity": "sha256:29f9c0994e6468ee630516198d2e7d0f6a28ebcaae81ab1ea5b9b43d55b3094e"
        },
        {
          "path": "docs/design/cli.md",
          "identity": "sha256:f0bde78dcdd9bd9daaaaf4639df42f712ea9b9a90184f09ad062244558d535a5"
        },
        {
          "path": "CONSTITUTION.md",
          "identity": "sha256:ba13fbf7bbce39f8257f91ca07c657f06b3e22658da89807acb3be9512b38a92"
        }
      ],
      "rationale": "Spec-owner reconciliation under user fix-then-PR authority: preserve specs/compact-current-state-change-record.md byte-identical to the reviewed historical base. Remove only this initiative's redundant scope paragraph. No compact requirement, boundary, approval, evidence registration or record changes. WF-MAP-02 through WF-MAP-06 and CLI-MAP-01 through CLI-MAP-06 remain owned by the two models; explicit selection already lives in adopted Constitution, rigorloop-workflow and skill-contract. Current adoption inventory disposition for the compact spec is preserved unchanged, superseding only the earlier M4 implementation-note claim that this file receives an entry paragraph. Those notes remain historical execution evidence. No new normative outcome, model or plan change, exception or waiver; independent affected Design and Code review must confirm this reconciliation before reliance.",
      "source_refs": []
    }
  ,{"actor":{"id":"repository-cleanup","role":"support"},"id":"retire-implementation-directory","rationale":"The user requested direct cleanup and PR submission without a proposal. Remove docs/implementation after preserving its four historical documents verbatim in this change’s existing evidence record. This supersedes the earlier decision to keep those files in place, not the historical account or its original reviewed identities. Existing reviews and Verify reports remain unchanged historical assessments; no approval is retargeted to the retained entries. No contract migration or new artifact type is introduced.","source_refs":[{"id":"retained-implementation-m1","path":"docs/changes/2026-09-05-explicit-recording-and-model-centered-design/evidence.yaml"},{"id":"retained-implementation-m2","path":"docs/changes/2026-09-05-explicit-recording-and-model-centered-design/evidence.yaml"},{"id":"retained-implementation-m3","path":"docs/changes/2026-09-05-explicit-recording-and-model-centered-design/evidence.yaml"},{"id":"retained-implementation-m4","path":"docs/changes/2026-09-05-explicit-recording-and-model-centered-design/evidence.yaml"}],"subjects":[{"identity":"sha256:3dfc7e53a04e49c3c91421c532500af8632610711e25d2c8af7c444c8c46f2c8","path":"docs/implementation/explicit-recording-m1.md"},{"identity":"sha256:c7af8821db15d8e8cd51d94ee1dccd831a8bb78e6b234c187413e2dd02801c0d","path":"docs/implementation/explicit-recording-m2.md"},{"identity":"sha256:4a4b6b9a34ae19c1d67ceb87237f578ae2574a33c549b60fca9fb9105626b0f1","path":"docs/implementation/explicit-recording-m3.md"},{"identity":"sha256:8a94a65a1ea390f5917393d5eaa21aa78daf42da15d235e6e89e5d6e68c6830b","path":"docs/implementation/explicit-recording-m4.md"}]}]
}
---

# Explicit adoption and preserved evidence

The user authorized this new record and M5 on 2026-09-07. Existing model, plan, implementation and advisory review files remain in place and unchanged. Their initial-draft/no-root wording records historical drafting context, not current state. The exact subjects above preserve that basis; new review decisions remain independently reviewer-owned.

M1-M4 are recorded completed from their execution evidence and independently reviewed handoffs. M5 remains pending, with no successful Verify report. Public release, commits and changes to historical roots remain outside scope.
