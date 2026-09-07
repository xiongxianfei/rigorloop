---
{
  "schema_version": 1,
  "change_id": "2026-09-07-targeted-recording-primary-cli",
  "id": "code-review-m3",
  "target": "code",
  "reviewer": {
    "id": "m3-code-review",
    "role": "review"
  },
  "contributors": [
    {
      "id": "codex-root",
      "role": "implement"
    }
  ],
  "independence_basis": "Separate delegated reviewer inspected the M3 source and approved design/plan without authoring implementation. Independently ran the current 13 TG-03/TG-04 tests and reproduced the escaped-path normalization mismatch. This is an early first-pass assessment of the bounded WIP slice; final integration and evidence remain pending. Actor attribution does not authenticate independence.",
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
      "path": "packages/rigorloop/dist/lib/recording-query-cli.js",
      "identity": "sha256:1ec2b71b65a4fa4dc24a0c1ccfa268bda5063c0786948adddaf2bdb58df15b21"
    },
    {
      "path": "packages/rigorloop/dist/lib/recording-observations.js",
      "identity": "sha256:59b47f1f4ce5c22db8dee714febc20a01e61a01c921f7d51eb9d633246f2e5a4"
    },
    {
      "path": "packages/rigorloop/dist/lib/recording-result.js",
      "identity": "sha256:6d208612ab3d0854d6ee02b3fa450b8920fb3cf493f06c9cdb8e411590572677"
    },
    {
      "path": "packages/rigorloop/dist/lib/record-store.js",
      "identity": "sha256:98293ccfcdf82f5bbd2ef55469dcf8c6d2fc2d4ee885817f34cf1e91fae5b7ba"
    },
    {
      "path": "packages/rigorloop/test/record-store-queries.test.js",
      "identity": "sha256:c1801a06a6969aceef0d5b73fbf55ea6d27a98850d35a245da96ead3915c6978"
    },
    {
      "path": "packages/rigorloop/dist/lib/recording-contract.js",
      "identity": "sha256:91afa8f36f4eac92678f95ea4c51c56b1aa99626c7a54c6699ffd21e830f0d72"
    }
  ],
  "judgment": "changes-requested",
  "findings": [
    {
      "id": "m3-cr-001",
      "reporter": {
        "id": "m3-code-review",
        "role": "review"
      },
      "owner": {
        "id": "codex-root",
        "role": "implement"
      },
      "subjects": [
        {
          "path": "packages/rigorloop/dist/lib/recording-query-cli.js",
          "identity": "sha256:1ec2b71b65a4fa4dc24a0c1ccfa268bda5063c0786948adddaf2bdb58df15b21"
        }
      ],
      "evidence": "Severity: minor. Finding ID: m3-cr-001. Location: packages/rigorloop/dist/lib/recording-query-cli.js normalize(). Direct independent invocation with review.subject_paths containing uppercase A and a double-quote path returned the quote before A. Both paths are admitted contained ASCII strings. CLI Bounded queries requires ASCII encoded-value ordering: JSON encoding sorts A before the escaped quote. The resulting normalized selector and selection_identity violate the documented interoperable cursor algorithm.",
      "required_outcome": "Sort selector filter values by their canonical JSON encodings, retain literal matching, and add an escaped-path regression that independently computes the documented normalized selector and cursor digest. Safe resolution: implementation-local correction; no owning Design decision needed.",
      "state": "open",
      "resolution": null
    },
    {
      "id": "m3-cr-002",
      "reporter": {
        "id": "m3-code-review",
        "role": "review"
      },
      "owner": {
        "id": "codex-root",
        "role": "implement"
      },
      "subjects": [
        {
          "path": "packages/rigorloop/dist/lib/recording-contract.js",
          "identity": "sha256:91afa8f36f4eac92678f95ea4c51c56b1aa99626c7a54c6699ffd21e830f0d72"
        },
        {
          "path": "packages/rigorloop/dist/lib/recording-query-cli.js",
          "identity": "sha256:46bd18e98fb2879c36853b04416a70bdb6cdafdbf69b869dd9cfb9b753e582cf"
        }
      ],
      "evidence": "Severity: minor. Finding ID: m3-cr-002. Location: recording-contract.js validate() union branches and validateQueryInput(). Independent context invocations using review.subject_paths:[\"../secret\"] and applicability.paths:[\"../secret\"] returned rejected/invalid-input. The branch validator catches safePath unsafe-path errors and collapses them into invalid-input. subject inspect returns the retained unsafe-path outcome for the same invalid path. The CLI design retains existing unsafe-path errors for containment violations.",
      "required_outcome": "Preserve unsafe-path classification for selected query path filters while retaining closed unknown-kind/field validation. Add direct adapter tests for both subject_paths and paths, and regression for a structurally invalid selector to avoid misclassifying unrelated malformed inputs. Safe resolution is local schema/query validation; no Design decision needed.",
      "state": "open",
      "resolution": null
    }
  ]
}
---
# M3 independent Code Review

First-pass status: changes-requested. Finding m3-cr-001 is recorded before correction. This bounded review covers current query selection, observation digest construction, snapshot hook and receipt renderer. Root is completing strict result validation, publisher integration and remaining temporal proof; this review does not judge those unfinished components complete.

Spec alignment: concern — encoded filter-value ordering differs from CLI pagination normalization. Test coverage: concern — existing 13 focused checks independently pass, but escaped-path ordering was not covered and final M3 proof is pending. Edge cases: concern — direct admitted-input counterexample documented in the finding. Error handling: pending final integration. Architecture boundaries: pass for current shared snapshot/observer separation. Compatibility: pass for inspected v1 body/origin behavior. Security/privacy: pass for inspected containment and safe messages. Derived artifact currency: pending final bundle checks. Unrelated changes: pass for current M3 scope. Validation evidence: pending completed milestone evidence.

Reviewed milestone: M3. Milestone closeout: resolution-needed. Required review-resolution: yes, m3-cr-001. Remaining implementation milestones: M3, M4, M5; M6 final Verify remains. Next stage: implementation correction and independent rereview. Recording status: recorded. Review log and separate resolution ledger: not required by selected explicit-recording-v1 contract. Final closeout readiness and Verify readiness: not claimed.

Additional first-pass finding m3-cr-002: unsafe selected paths lose their retained unsafe-path code after strict-schema integration. Independent 16 focused tests passed before this counterexample; M3 remains changes-requested pending corrections and final evidence.
