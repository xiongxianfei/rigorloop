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
  "independence_basis": "Separate delegated reviewer execution independently inspected the complete M1 diff and relevant approved model/plan authority without editing implementation. It recorded three findings before fixes, reread corrected code and integration diffs, ran the focused 19-test v2 suite independently, and checked all registered evidence subject identities plus approved Design/Delivery subject maps. codex-root authored implementation and execution evidence; reviewer owns this assessment. Actor labels are attribution only.",
  "subjects": [
    {
      "path": "docs/design/cli/cli.md",
      "identity": "sha256:951c0f427e118914d70c1f326a02ae01efab47107a1cca897211b980b9d8d22c"
    },
    {
      "path": "docs/design/record-format/record-format.md",
      "identity": "sha256:6ddfcd350212437ddf2feaade14818fd66f9a04b8a00ccb01c5fb13291879eeb"
    },
    {
      "path": "docs/design/workflow/workflow.md",
      "identity": "sha256:a3727f571eec0f9ae34bfdda31f9f7711e3903abdabd31e28903b8c3b69b2251"
    },
    {
      "path": "docs/plans/2026-09-07-targeted-recording-primary-cli.md",
      "identity": "sha256:2078ea15010d79a50941cc3bfaa80fa02d521972bb97c6cc01ee2e89cc5d393d"
    },
    {
      "path": "packages/rigorloop/dist/lib/record-format-v2.js",
      "identity": "sha256:7bbb5b5542d7a016bf63a80e453db616ce90269df6ecb3e41b9a9c15433ae02d"
    },
    {
      "path": "packages/rigorloop/dist/lib/record-store-contract.js",
      "identity": "sha256:72a9813be174d2fdeb9dd8c552a5c23fda916befa8d2338107b130ea5f90f458"
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
      "identity": "sha256:0a175f69c1b3f642e4ee0e6f362fdf319b3e7b85e47b1eb6138fa78ff481f506"
    },
    {
      "path": "packages/rigorloop/test/record-store-workflow.test.js",
      "identity": "sha256:e6691cdbedd907e4f13104bfd836b4ea183807216d4d823621b4cbbcf3369765"
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
      "path": "scripts/test-select-validation.py",
      "identity": "sha256:3ef4a27b6a3fa3705b8717b3de2b62eabab46741c86f1cd57cc499ca6cfb1af0"
    },
    {
      "path": "scripts/validate-record-store.mjs",
      "identity": "sha256:9a3e7839589f59f5c6924fb405891cc608dbbd9dfcb52569c4177023c6975321"
    },
    {
      "path": "scripts/validation_selection.py",
      "identity": "sha256:84615800f907324ac3991b40d2d8019e25ca1b6ba76b492133892d5ae067ad6a"
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
      "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/evidence.yaml",
      "identity": "sha256:3df0ba0549df9ed0eb63527ef423ad4ebdde491382a3786309769f9b03cec6c9"
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
  "judgment": "approved",
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
      "state": "resolved",
      "resolution": {
        "actor": {
          "id": "m1-code-review",
          "role": "review"
        },
        "rationale": "Both change.yaml and change.json entry paths now reject a competing manifest in live and exact-Git-snapshot validation. Direct regression covers all four combinations; v1-only compatibility remains covered by C2/C3/package evidence.",
        "evidence_refs": [
          {
            "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/evidence.yaml",
            "id": "m1-contract"
          }
        ]
      }
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
      "state": "resolved",
      "resolution": {
        "actor": {
          "id": "m1-code-review",
          "role": "review"
        },
        "rationale": "Nullable validation selects the actual null/non-null branch and preserves nested unsafe-path. Present unsupported schema versions and mismatched contracts return unsupported-contract before representation consistency. Exact-code regressions pass without modifying v1 validation.",
        "evidence_refs": [
          {
            "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/evidence.yaml",
            "id": "m1-contract"
          }
        ]
      }
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
      "state": "resolved",
      "resolution": {
        "actor": {
          "id": "m1-code-review",
          "role": "review"
        },
        "rationale": "Before-state parsing validates available records and collects readable origins without requiring resolved prior EntryRefs or all registered files. Complete after-state references remain validated. Existing registry membership and every available original concern origin must survive; missing content restoration and dangling-ref repair pass, malformed origins and removed membership reject.",
        "evidence_refs": [
          {
            "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/evidence.yaml",
            "id": "m1-contract"
          }
        ]
      }
    }
  ]
}
---
# M1 independent Code Review

Native review status: clean-with-notes. Stored judgment: approved. Reviewed milestone: M1 only, versioned JSON structure and reference validation. Recording status: recorded. Milestone closeout: review satisfied; Route owns the state change. Required review-resolution: no; all three recorded findings are resolved after reassessment of the corrected implementation. Remaining implementation milestones: M2–M5, followed by M6 final Verify. Next stage: Route may select M2 under its authority. This review performs no routing edit or next-milestone execution. Final whole-change Code Review and final Verify remain outstanding; branch/PR/CI/Verify readiness are not claimed.

The current subjects cover the full M1 source, schemas, fixtures/templates, package mirrors, tests, bundler and standalone validator, plus the narrow test model-path correction and validation selector mapping needed to run the repository's actual proof. Approved Design Review (14 subjects) and Delivery Review (7 subjects) were rechecked with no drift. Every subject in each of the ten registered M1 checks also matched current bytes.

| Checklist | Result | Basis |
| --- | --- | --- |
| Spec alignment | pass | RF-SR-01/02/06/08 and CLI-SR-02/09/10 are realized at the M1 representation boundary; correction availability and preservation findings were corrected. |
| Test coverage | pass | C2 has 78 passing tests including 19 v2 checks for closed vocabularies, JSON encoding, limits, namespaces, origin comparisons, compatibility and repair. |
| Edge cases | pass | Direct tests cover duplicate/ambiguous IDs, unsupported/missing references, same-candidate targets, decision self-links, null origin/supporting judgment distinction, missing prior content and dual manifests. |
| Error handling | pass | Unknown versions/contracts, unsafe nested paths and invalid structure retain distinct rejection outcomes; no persistence capability is introduced. |
| Architecture boundaries | pass | Separate pure v2 module supplies representation checks; existing public v1 runtime and actor-owned workflow meaning remain intact. |
| Compatibility | pass | V1 schema/template/validator bytes remain unchanged and broad v1 EntryRef membership has an explicit regression. Existing model-path test updates use selected canonical locations. |
| Security/privacy | pass | Standalone validation uses contained bounded reads, rejects symlinks/mixed manifests and performs no writes. No network, secret, authentication or release authority is added. |
| Derived artifact currency | pass | C1 byte parity passed; canonical/package templates validate; package publication tests passed without publishing. |
| Unrelated changes | pass | Selector mapping is narrowly scoped to new v2 surfaces and tests preserve required publication proof. No M2–M5 activation or behavior is claimed. |
| Validation evidence | pass | Exact-subject evidence records all required checks with successful outcomes; reviewer independently reran focused v2 tests. |

Direct reviewer command: `node --test packages/rigorloop/test/record-store-v2-contract.test.js` — 19 passed, zero failed. Author-owned evidence checked: C1 schema bundling passed; C2 recording tests 78 passed; C3 metadata tests 115 passed; model structural check passed; boundary regression 87 passed; selector regression 163 passed; package tests 541 passed with 2 existing skips; publication tests 7 passed; working/staged whitespace checks passed. Explicit selector outcome reports no blockers. These results support this M1 boundary only.

The original finding subjects remain truthful historical bases; their resolutions cite the current registered contract-test check. No finding origin is invented for this v1 review. All three findings were recorded before correction and resolved only after independent rereview.

Residual limits: v2 persistence dispatch, lossless target construction, bounded public reads/receipts, consumer adoption and final integrated proof belong to later milestones. M1 standalone validation is read-only and does not promise exclusion of external editors. Review log: not required by explicit-recording-v1. Review resolution: retained directly in this stable record.
