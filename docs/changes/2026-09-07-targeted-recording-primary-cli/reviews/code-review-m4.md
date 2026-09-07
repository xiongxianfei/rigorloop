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
  "independence_basis": "Separate delegated reviewer inspected the current M4 constructor, source-span editing, mutation adapter, shared engine and dispatcher against approved M4 allocation without authoring implementation. Independently reproduced both recorded result-contract defects before correction. This first-pass WIP review does not approve unfinished validation or integration. Actor labels are attribution only.",
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
      "path": "docs/plans/2026-09-07-targeted-recording-primary-cli.md",
      "identity": "sha256:2078ea15010d79a50941cc3bfaa80fa02d521972bb97c6cc01ee2e89cc5d393d"
    },
    {
      "path": "packages/rigorloop/dist/lib/recording-construction.js",
      "identity": "sha256:a8cd68442172e9f5c096a6cc0c8e3711b4274866175eeb29916061cd0f9472d9"
    },
    {
      "path": "packages/rigorloop/dist/lib/recording-spans.js",
      "identity": "sha256:c700208533711b12502e92838712f0c6470bb43c097bc39ea3800ec59c69523c"
    },
    {
      "path": "packages/rigorloop/dist/lib/recording-mutation-cli.js",
      "identity": "sha256:629cc4e3d826cdd796bbb8441845421e6d9a9cad2063627ade7a7b811bbc6a23"
    },
    {
      "path": "packages/rigorloop/dist/lib/recording-cli.js",
      "identity": "sha256:e0d18f9cc8096c7f02c509c0506a6f2810be81ff8ed6d47b3e4c950063c7ddda"
    },
    {
      "path": "packages/rigorloop/dist/lib/record-store.js",
      "identity": "sha256:15f1533f2ab21ae0f2798c086aaea5a8ff2d13c324073525c75c1ec6f23f3ada"
    },
    {
      "path": "packages/rigorloop/dist/bin/rigorloop.js",
      "identity": "sha256:9180936dab54fbaa39436b4b4fc022d77a1fb6675c7bb958e3bf93557a20580e"
    },
    {
      "path": "packages/rigorloop/test/record-store-targeted.test.js",
      "identity": "sha256:138d196509de9307ae6075e824c18c993e2303fd77f90f812f203f83aea2afc4"
    }
  ],
  "judgment": "changes-requested",
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
      "state": "open",
      "resolution": null
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
      "state": "open",
      "resolution": null
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
      "state": "open",
      "resolution": null
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
      "state": "open",
      "resolution": null
    }
  ]
}
---
# M4 independent Code Review

First-pass status: changes-requested. m4-cr-001 and m4-cr-002 are recorded before correction. Review covers the bounded current M4 WIP against approved CLI construction/overlap/error rules and plan TG-05/TG-06. Final implementation and validation remain pending.

Spec alignment: concern — duplicate-add batch classification and missing-container observation are inconsistent with explicit contracts. Test coverage: pending final M4 proof. Edge cases: concern — direct adapter reproductions recorded in findings. Error handling: concern — missing-content detail is absent from the required rejection. Architecture boundaries: pass for current pure construction under shared lock-held persistence. Compatibility: pending full v1 proof. Security/privacy: pass for inspected shared containment/identity enforcement. Derived artifact currency: pending final schema/package checks. Unrelated changes: pass for current M4 allocation. Validation evidence: pending final registered milestone evidence.

Reviewed milestone: M4. Milestone closeout: resolution-needed. Required review-resolution: yes, m4-cr-001 and m4-cr-002. Remaining implementation milestones: M4, M5; M6 final Verify remains. Next stage: implementation correction and independent rereview. Recording status: recorded. Review log and separate resolution ledger: not required by this selected explicit-recording-v1 contract. Final closeout readiness and Verify readiness: not claimed.

Additional first-pass finding m4-cr-003: producer receipts conflate explicit applicability changes with entry changes and mechanical bookkeeping; direct adapter reproduction is retained above. M4 remains changes-requested pending corrections and final evidence.

Additional first-pass finding m4-cr-004: normal per-command help does not describe admitted v1 differences or all required positional arguments. M4 remains changes-requested pending corrections and final evidence.
