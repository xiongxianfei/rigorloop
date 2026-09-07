---
{
  "schema_version": 1,
  "change_id": "2026-09-07-targeted-recording-primary-cli",
  "id": "code-review-m1",
  "target": "code",
  "reviewer": {
    "id": "m1-code-review",
    "role": "review"
  },
  "contributors": [
    {
      "id": "codex-root",
      "role": "implement"
    }
  ],
  "independence_basis": "Separate delegated reviewer execution inspected M1 implementation and governing models without authoring or modifying implementation. Actor labels are attribution only.",
  "subjects": [
    {
      "path": "packages/rigorloop/dist/lib/record-format-v2.js",
      "identity": "sha256:ea420502344aec9edbdbcd112a90338137c66b98767ceb6aa45c95de76675055"
    },
    {
      "path": "packages/rigorloop/dist/schemas/rigorloop-records-v2.schema.json",
      "identity": "sha256:be265e71549a69579eba68b78fb687a3115792796ce4fe663b5d81e633db58e8"
    },
    {
      "path": "packages/rigorloop/dist/templates/rigorloop-records-v2/records.json",
      "identity": "sha256:6ed0d3721362d86339baed664340b0f25fe9ecf833ef6f1c4bf6827e40a8f0f5"
    },
    {
      "path": "packages/rigorloop/test/record-store-v2-contract.test.js",
      "identity": "sha256:5700f8e7704d4f1f192fe6f3959b4dc2cfa081cf63c7108e59838c4bc6ccf44f"
    },
    {
      "path": "schemas/rigorloop-records-v2.schema.json",
      "identity": "sha256:be265e71549a69579eba68b78fb687a3115792796ce4fe663b5d81e633db58e8"
    },
    {
      "path": "scripts/build-record-store-schema.mjs",
      "identity": "sha256:b20b6b010654048b4e81c367342bada3c9e58aff327d50e4f70f0074e5dfa48f"
    },
    {
      "path": "scripts/validate-record-store.mjs",
      "identity": "sha256:62692cce99754839011a21ec393a4ddc72f5bdee0cb9d9f85fce63c4a98e5639"
    },
    {
      "path": "templates/rigorloop-records-v2/records.json",
      "identity": "sha256:6ed0d3721362d86339baed664340b0f25fe9ecf833ef6f1c4bf6827e40a8f0f5"
    },
    {
      "path": "tests/fixtures/rigorloop-records-v2/records.json",
      "identity": "sha256:9ff381578ee2000ad5dcab8793b1d3d7ae42af77199be459ff62f372b2a6a281"
    },
    {
      "path": "docs/plans/2026-09-07-targeted-recording-primary-cli.md",
      "identity": "sha256:2078ea15010d79a50941cc3bfaa80fa02d521972bb97c6cc01ee2e89cc5d393d"
    },
    {
      "path": "docs/design/record-format/record-format.md",
      "identity": "sha256:6ddfcd350212437ddf2feaade14818fd66f9a04b8a00ccb01c5fb13291879eeb"
    },
    {
      "path": "docs/design/cli/cli.md",
      "identity": "sha256:951c0f427e118914d70c1f326a02ae01efab47107a1cca897211b980b9d8d22c"
    },
    {
      "path": "docs/design/workflow/workflow.md",
      "identity": "sha256:a3727f571eec0f9ae34bfdda31f9f7711e3903abdabd31e28903b8c3b69b2251"
    },
    {
      "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/reviews/design-review.md",
      "identity": "sha256:86a25fafdf99fdc9e4782d91b2d6005751f0dcfaac5801a052001ceed3632971"
    },
    {
      "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/reviews/delivery-review.md",
      "identity": "sha256:f4ffd37cc3aa73448cf05c6731663c96cc18c62de040928619fddf35209ccb8d"
    }
  ],
  "judgment": "changes-requested",
  "findings": [
    {
      "id": "m1-cr-01",
      "reporter": {
        "id": "m1-code-review",
        "role": "review"
      },
      "owner": {
        "id": "codex-root",
        "role": "implement"
      },
      "subjects": [
        {
          "path": "scripts/validate-record-store.mjs",
          "identity": "sha256:62692cce99754839011a21ec393a4ddc72f5bdee0cb9d9f85fce63c4a98e5639"
        }
      ],
      "evidence": "Severity: major. Location: live dispatch lines 64-70 and snapshotFiles lines 42-43. A temporary valid v1 change.yaml plus adjacent change.json, validated via change.yaml, exits 0 and prints structure valid. Only the change.json direction checks the competing manifest. This violates M1 TG-01 dual-manifest rejection and permits selecting one of two contracts by filename.",
      "required_outcome": "Make standalone live and exact-Git-snapshot validation reject a competing manifest regardless of the selected extension. Add regression coverage for both entry paths while retaining valid v1-only behavior. No design decision is needed.",
      "state": "open",
      "resolution": null
    },
    {
      "id": "m1-cr-02",
      "reporter": {
        "id": "m1-code-review",
        "role": "review"
      },
      "owner": {
        "id": "codex-root",
        "role": "implement"
      },
      "subjects": [
        {
          "path": "packages/rigorloop/dist/lib/record-format-v2.js",
          "identity": "sha256:ea420502344aec9edbdbcd112a90338137c66b98767ceb6aa45c95de76675055"
        }
      ],
      "evidence": "Severity: minor. Location: validate anyOf lines 46-48. A review finding with resolution.evidence_refs[0].path set to ../escape returns invalid-input (invalid nullable value), because anyOf catches and replaces the nested unsafe-path error. Record Format reference-resolution table requires unsafe paths retain unsafe-path rejection; supporting_judgment and nullable plan subjects have the same wrapper. Additional first-pass case: a present schema_version 99 with rigorloop-records-v2 returns invalid-input through const validation; CLI Paths requires unsupported-contract for unknown/mismatched version/contract pairs.",
      "required_outcome": "Preserve specific unsafe-path diagnostics through nullable object validation and add regressions for unsafe EntryRef paths inside finding/blocker resolutions and subject paths under other nullable objects. Do not weaken rejection or alter v1 diagnostics. No design decision is needed. Report unsupported-contract for present unsupported schema versions and mismatched contract/version pairs in v2; retain invalid-input for malformed/missing required discriminator fields. Add exact-code regression assertions.",
      "state": "open",
      "resolution": null
    },
    {
      "id": "m1-cr-03",
      "reporter": {
        "id": "m1-code-review",
        "role": "review"
      },
      "owner": {
        "id": "codex-root",
        "role": "implement"
      },
      "subjects": [
        {
          "path": "packages/rigorloop/dist/lib/record-format-v2.js",
          "identity": "sha256:ea420502344aec9edbdbcd112a90338137c66b98767ceb6aa45c95de76675055"
        }
      ],
      "evidence": "Severity: major. Location: validateV2Preservation line 222. It runs validateV2Set over the before-state before comparing origins. Direct proof: remove registered evidence.json from the fixture before-state and restore the exact file in a complete after-state; preservation rejects broken-reference. The same problem affects a readable before-record with a dangling EntryRef that the candidate repairs. CLI advanced candidate contract explicitly allows broken current references and missing registered records to be repaired.",
      "required_outcome": "Separate before-state structural parsing and available-origin collection from complete candidate validation. Keep manifest/available-record identity and origin checks, preserve registry membership, reject malformed available origin records safely, and permit restoring missing registered content or repairing dangling references without losing any readable original origin. Add direct regression tests. No design decision is needed.",
      "state": "open",
      "resolution": null
    }
  ]
}
---
# M1 independent Code Review

Status: changes-requested. Reviewed milestone: M1 only. Recording status: recorded. Milestone closeout: resolution-needed. Required resolution: m1-cr-01 and m1-cr-02; implementation owner can correct both without an upstream design decision. Remaining implementation milestones: M2–M5; M6 remains final Verify. Final closeout and Verify readiness are not claimed.

The review examines separately versioned schemas, pure parsing and reference validation, preservation, templates/fixtures, bundling and the standalone validator. Direct reproductions establish both findings before correction. Formal clean judgment awaits author-owned test evidence and review of corrected subjects.

| Checklist | Result | Basis |
| --- | --- | --- |
| Spec alignment | concern | Dual-manifest and unsafe-path outcomes differ from TG-01/RF-SR-02. |
| Test coverage | concern | Existing cases omit change.yaml dual-manifest entry and unsafe paths inside nullable values. |
| Edge cases | concern | Both reproduced alternate paths require regressions. |
| Error handling | concern | Nullable error wrapping loses the specified code. |
| Architecture boundaries | pass | Pure v2 module, no publisher or lifecycle activation. |
| Compatibility | concern | Existing v1 definitions are unchanged; dual-manifest ambiguity is not rejected by standalone v1 selection. |
| Security/privacy | pass | No network/secrets or new write path; unsafe inputs reject, though one diagnostic class is wrong. |
| Derived artifact currency | pass | V2 schema/template mirror byte comparison is explicit; required build check evidence pending. |
| Unrelated changes | pass | Reviewed staged slice is limited to M1 representation. |
| Validation evidence | concern | Root is completing required C1/C2/C3 and selected checks; no passing suite claim is made here. |

Direct proof: reviewer used an in-memory fixture mutation through validateV2Record and a temporary filesystem store through node scripts/validate-record-store.mjs. Results: nested unsafe EntryRef produced invalid-input; v1-selected dual manifest exited 0. No reviewed source was modified.

Review log: not required by the selected explicit-recording-v1 contract. Review resolution: findings remain in this stable review. Handoff: same-milestone correction and rereview only; no next-milestone execution is authorized by this review.

Additional first-pass finding m1-cr-03: origin-preservation validation currently demands a complete reference-valid before-state. The direct missing-evidence restoration reproduction returns broken-reference despite an otherwise valid candidate with unchanged origins. This is an additional spec-alignment, correction-availability and test-coverage concern. Root identified this candidate concern; the independent reviewer verified it against CLI line 340 and reproduced it without editing implementation.
