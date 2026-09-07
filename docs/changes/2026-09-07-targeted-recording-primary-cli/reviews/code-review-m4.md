---
{
  "schema_version": 1,
  "change_id": "2026-09-07-targeted-recording-primary-cli",
  "id": "code-review-m4",
  "target": "code",
  "reviewer": {
    "id": "m4-code-review",
    "role": "review"
  },
  "contributors": [
    {
      "id": "codex-root",
      "role": "implement"
    }
  ],
  "independence_basis": "Separate delegated M4 reviewer independently inspected the complete M4 constructor, source spans, schemas, targeted executor, mutation/public dispatch and relevant shared persistence against exact approved Design/Delivery packages without authoring implementation. Recorded four findings and reproduced result-contract defects before correction; reread all corrections and final integration, independently ran29 TG-05/TG-06 tests successfully, inspected broader registered validation and verified all M4 evidence subjects and approved package members. codex-root authored implementation/execution evidence; reviewer owns this assessment. Actor labels remain attribution only.",
  "subjects": [
    {
      "path": "docs/design/cli/cli.md",
      "identity": "sha256:951c0f427e118914d70c1f326a02ae01efab47107a1cca897211b980b9d8d22c"
    },
    {
      "path": "docs/design/workflow/workflow.md",
      "identity": "sha256:a3727f571eec0f9ae34bfdda31f9f7711e3903abdabd31e28903b8c3b69b2251"
    },
    {
      "path": "docs/design/record-format/record-format.md",
      "identity": "sha256:6ddfcd350212437ddf2feaade14818fd66f9a04b8a00ccb01c5fb13291879eeb"
    },
    {
      "path": "docs/plans/2026-09-07-targeted-recording-primary-cli.md",
      "identity": "sha256:2078ea15010d79a50941cc3bfaa80fa02d521972bb97c6cc01ee2e89cc5d393d"
    },
    {
      "path": "packages/rigorloop/dist/lib/recording-construction.js",
      "identity": "sha256:1b9cb899f860d3a547fa28a0aab9a4c4f4a8a06356c371161e9ece53ec055977"
    },
    {
      "path": "packages/rigorloop/dist/lib/recording-spans.js",
      "identity": "sha256:c700208533711b12502e92838712f0c6470bb43c097bc39ea3800ec59c69523c"
    },
    {
      "path": "packages/rigorloop/dist/lib/recording-mutation-cli.js",
      "identity": "sha256:3e8b757a53050e6f72c55c42791d8a2f4b4eb14513fb98932c1e6087d4fa4088"
    },
    {
      "path": "packages/rigorloop/dist/lib/recording-cli.js",
      "identity": "sha256:8e8da58ee13619ab84ce0161d13db193a4493f51ca125614813343322addeee9"
    },
    {
      "path": "packages/rigorloop/dist/lib/recording-contract.js",
      "identity": "sha256:6304134e4f8f8b2a90169187a2cba4bbbf299ba2e614c7bea2500f0205890450"
    },
    {
      "path": "packages/rigorloop/dist/lib/record-store.js",
      "identity": "sha256:2286df8358d9086fe4b33b9e67e12c30d94bb62457291d52fb5a851ca1d6c188"
    },
    {
      "path": "packages/rigorloop/dist/bin/rigorloop.js",
      "identity": "sha256:4503d48667581e4f61d922d847df5a7630b25a5e4c476d1c1c49c554dce422e0"
    },
    {
      "path": "packages/rigorloop/test/record-store-targeted.test.js",
      "identity": "sha256:2e76a15c30a790f272a9bcdb740e917ac284ed3e886b0ca5b15e5bdb152a7499"
    },
    {
      "path": "schemas/targeted-recording-v1.schema.json",
      "identity": "sha256:d7e91f166a58d3db5077f475d25ab3a342026cf6795cfa3daa2d6571a4f1cecc"
    },
    {
      "path": "packages/rigorloop/dist/schemas/targeted-recording-v1.schema.json",
      "identity": "sha256:d7e91f166a58d3db5077f475d25ab3a342026cf6795cfa3daa2d6571a4f1cecc"
    },
    {
      "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/evidence.yaml",
      "identity": "sha256:4e58bb85a68c1af72310c7700e92ab60f5b3f78535f037b36b86fc0142aa3039"
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
      "id": "m4-cr-001",
      "reporter": {
        "id": "m4-code-review",
        "role": "review"
      },
      "owner": {
        "id": "codex-root",
        "role": "implement"
      },
      "subjects": [
        {
          "path": "packages/rigorloop/dist/lib/recording-construction.js",
          "identity": "sha256:a8cd68442172e9f5c096a6cc0c8e3711b4274866175eeb29916061cd0f9472d9"
        }
      ],
      "evidence": "Finding ID: m4-cr-001. Severity: minor. Location: entry() add existence check before assignment overlap. Independent batch of two identical work.add operations for an initially absent ID returned target-exists at operation_index 1. CLI batch explicitly requires overlapping-operation for two adds to the same ID, even when supplied values agree.",
      "required_outcome": "Distinguish previously assigned batch targets from preexisting entries; duplicate adds in one batch reject overlapping-operation, while a single add to a preexisting target retains target-exists. Add direct adapter proof for work/blocker/finding collections and all-or-none state preservation. Safe resolution is implementation-local.",
      "state": "resolved",
      "resolution": {
        "actor": {
          "id": "m4-code-review",
          "role": "review"
        },
        "rationale": "Assignment-overlap checks now precede existing-entry rejection for repeated batch targets. Duplicate batch adds reject overlapping-operation; single preexisting adds retain target-exists; disjoint fields still compose. Independently rereviewed and tested.",
        "evidence_refs": [
          {
            "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/evidence.yaml",
            "id": "m4-contract"
          }
        ]
      }
    },
    {
      "id": "m4-cr-002",
      "reporter": {
        "id": "m4-code-review",
        "role": "review"
      },
      "owner": {
        "id": "codex-root",
        "role": "implement"
      },
      "subjects": [
        {
          "path": "packages/rigorloop/dist/lib/recording-mutation-cli.js",
          "identity": "sha256:629cc4e3d826cdd796bbb8441845421e6d9a9cad2063627ade7a7b811bbc6a23"
        }
      ],
      "evidence": "Finding ID: m4-cr-002. Severity: minor. Location: mutation failure result / shared targeted construction failure. Independent removal of registered evidence.json followed by targeted evidence.record returned rejected/broken-reference with no observation_summary. CLI requires broken-reference plus missing-content observation for a primary mutation targeting a registered missing file; the current receipt omits this important unavailable-content distinction.",
      "required_outcome": "Return a truthful bounded missing-content observation summary for the verified registered snapshot when a mutation targets missing registered content. Preserve coherence and error priority: do not expose an unverified snapshot or allow observation expansion/read errors to replace an established storage result. Add direct missing-container mutation and overlap/error-boundary proof. Safe resolution is implementation-local.",
      "state": "resolved",
      "resolution": {
        "actor": {
          "id": "m4-code-review",
          "role": "review"
        },
        "rationale": "Broken-reference failures can attach bounded observations only from a rechecked coherent registered snapshot; missing-content is exposed without initializing lost data. Optional diagnostic failure does not replace the established storage error. Independent missing-container regression passes.",
        "evidence_refs": [
          {
            "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/evidence.yaml",
            "id": "m4-contract"
          }
        ]
      }
    },
    {
      "id": "m4-cr-003",
      "reporter": {
        "id": "m4-code-review",
        "role": "review"
      },
      "owner": {
        "id": "codex-root",
        "role": "implement"
      },
      "subjects": [
        {
          "path": "packages/rigorloop/dist/lib/recording-construction.js",
          "identity": "sha256:a8cd68442172e9f5c096a6cc0c8e3711b4274866175eeb29916061cd0f9472d9"
        }
      ],
      "evidence": "Finding ID: m4-cr-003. Severity: minor. Location: applicable() and operation-wide edits counter. Independent evidence.record of byte-equivalent check-1 fields plus explicit stale applicability returned changed:[{kind:evidence,target:{id:check-1}}], omitted the actual applicability target, and marked applicability effects bookkeeping:true. CLI changed names explicitly requested entries that changed, explicitly includes producer applicability targets in its128-target bound, and separates actor decisions from derived registry/container work.",
      "required_outcome": "Track producer entry changes separately from explicit applicability changes. Include changed applicability targets only when their declarations change; do not report an unchanged check merely because applicability changed. Mark explicit applicability effects as semantic (bookkeeping:false), retaining true only for derived registry/container work. Add direct producer-only-applicability, both-change, and no-op receipt tests. Safe resolution is implementation-local.",
      "state": "resolved",
      "resolution": {
        "actor": {
          "id": "m4-code-review",
          "role": "review"
        },
        "rationale": "Constructor tracks explicit applicability edits separately, reports their changed targets and marks their effects semantic. An unchanged evidence check with changed applicability now reports only applicability. Independent receipt regression passes.",
        "evidence_refs": [
          {
            "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/evidence.yaml",
            "id": "m4-contract"
          }
        ]
      }
    },
    {
      "id": "m4-cr-004",
      "reporter": {
        "id": "m4-code-review",
        "role": "review"
      },
      "owner": {
        "id": "codex-root",
        "role": "implement"
      },
      "subjects": [
        {
          "path": "packages/rigorloop/dist/lib/recording-mutation-cli.js",
          "identity": "sha256:a4b9b11327380f8ed32f5ccc2f22e5305f85ce2521c8bd1fcd90b2668eb697a7"
        }
      ],
      "evidence": "Finding ID: m4-cr-004. Severity: minor. Location: per-command help always selects v2-operation schema. finding add --help advertises required basis, while supported explicit-recording-v1 finding.add rejects basis/origin. Help lists a generic contract field without explaining this incompatibility. Required positional IDs are also omitted from the usage line for work/review/evidence and other ID-bearing commands. This makes the documented normal command help incomplete or incorrect for admitted invocations.",
      "required_outcome": "Make per-command help executable for both supported existing-record contracts: show required positional IDs and explain operation-specific v1/v2 differences, especially v1 absence of basis/origin and retained body encoding. Keep output bounded to that operation and shared request safety fields rather than loading all schemas. Add help regressions tied to valid corresponding v1/v2 requests. Safe resolution is implementation-local; no Design change required.",
      "state": "resolved",
      "resolution": {
        "actor": {
          "id": "m4-code-review",
          "role": "review"
        },
        "rationale": "Operation-specific help now provides correct positional examples, states v1 finding/blocker omission of basis/origin, v2 basis and creation requirements, and v1 Markdown final-LF rule. Independent help and v1/v2 command regressions pass; no unrelated schema guidance is required.",
        "evidence_refs": [
          {
            "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/evidence.yaml",
            "id": "m4-contract"
          }
        ]
      }
    }
  ]
}
---
# M4 independent Code Review

Review status: clean-with-notes. Stored judgment: approved. The complete M4 increment satisfies its approved targeted construction and public command allocation. Findings m4-cr-001 through m4-cr-004 were recorded and independently reassessed as resolved. Original finding subjects/evidence are retained rather than retargeted to corrected bytes.

Reviewed every admitted mutation and batch dispatch, closed request schemas, source-span replacement/append implementation, producer registration and explicit applicability, immutable concern-origin construction, shared lock-held execution and preview, bounded receipt/error integration, public dispatcher and operation-specific help. Exact CLI/Workflow/Record Format models and delivery plan supplied authority; related shared persistence and prior read/result layers were inspected where their boundaries changed. Every approved Design/Delivery member and every registered M4 execution-evidence subject matched current bytes.

| Checklist | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | M4 TG-05/TG-06 cover CLI-SR-03/07/11/12/13/15/16/17, RF-SR-03/04/05 and WF-SR-01/02/04/05/06/12/13; actor decisions remain explicit. |
| Test coverage | pass | Independently ran all29 record-store-targeted.test.js tests successfully; m4-contract records177 passing recording tests. |
| Edge cases | pass | Tests cover all operation families, explicit origin forms and ordered source-review capture, missing fields/containers/applicability/body, ID/assignment collisions, disjoint composition, final-candidate references, stale/no-op/preview and correction after completed activity. |
| Error handling | pass | Registered missing files remain unavailable; malformed/unsafe/identity errors retain storage-only outcomes. Direct interruption tests at preparation, replacement, precommit and postcommit recover exact candidate state without a partial changed receipt. |
| Architecture boundaries | pass | Pure construction edits exact spans under the shared writer exclusion; final candidate validation/persistence owns safety. Preview uses coherent reads without reservation. Public commands bypass historical workflow eligibility. |
| Compatibility | pass | Existing-root v1/v2 dispatch remains explicit. V1 narrative/front matter and lack of origin remain truthful; v1 creation is rejected on the primary path. Lazy public-adapter import preserves historical isolated CLI load behavior. |
| Security/privacy | pass | Shared containment, identity and recovery checks remain intact; unregistered bytes are not overwritten. Missing decision errors use structural locations and safe messages; role labels do not authenticate. |
| Derived artifact currency | pass | m4-schema confirms canonical/package request/result schema parity; m4-package-publication passes7 checks. No release publication or consumer activation claim. |
| Unrelated changes | pass | Changes stay within M4 constructors, request contracts, adapters/public help, shared execution boundary and stage-owned evidence. |
| Validation evidence | pass | Current registered m4-* checks: schema/model pass;177 recording tests;641 package tests plus2 historical skips; metadata115, boundary87 and publication7 pass; selected checks all passed with zero blockers. |

Source-span editing preserves omitted values, neighbors, ordering, whitespace and narrative. The actor supplies complete required decisions; registry/container creation is mechanical, while applicability is recorded explicitly and reported as a separate semantic target when changed. Batch construction is ordered, final references are validated together, overlapping semantic assignments reject, and later reviewer approval does not close a Verify-owned blocker or retarget an earlier concern origin. Human/machine responses retain the shared storage-only boundary.

Reviewed milestone: M4. Milestone closeout: closed at the independent review boundary; Route owns milestone-state recording. Required review-resolution: no outstanding work; all four findings resolved. Remaining implementation milestone: M5; M6 final Verify remains. Next stage: Route may select M5 implementation under its existing authority. Recording status: recorded. Review log and separate resolution ledger: not required by this selected explicit-recording-v1 contract.

This increment review does not substitute for the retained final whole-change Code Review. Consumer alignment, coordinated adoption, complete-interaction token evaluation and final Verify remain downstream. Final closeout readiness, branch/PR readiness and Verify readiness are not claimed. No expanded external-editor guarantee is established.
