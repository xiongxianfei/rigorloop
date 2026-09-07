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
  "independence_basis": "Separate delegated M3 reviewer independently inspected the complete M3 implementation diff and exact approved Design/Delivery packages without authoring implementation. Recorded m3-cr-001 and m3-cr-002 before correction, independently reproduced both defects, reread their corrections and final integrated slice, ran all 29 TG-03/TG-04 tests successfully, examined registered broader validation evidence, and verified every M3 evidence subject plus approved Design/Delivery member identity. codex-root authored implementation and execution evidence; reviewer owns this assessment. Actor labels remain attribution only.",
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
      "path": "packages/rigorloop/dist/lib/recording-query-cli.js",
      "identity": "sha256:ae3aadb182ab9f6983c8235a3e2eed522a6f05bfaeb3839f643202523576ddfd"
    },
    {
      "path": "packages/rigorloop/dist/lib/recording-observations.js",
      "identity": "sha256:59b47f1f4ce5c22db8dee714febc20a01e61a01c921f7d51eb9d633246f2e5a4"
    },
    {
      "path": "packages/rigorloop/dist/lib/recording-result.js",
      "identity": "sha256:352fccdd52e95bba878972b39d2284d70a1dfe0e616bb1abfd9d5ca896089141"
    },
    {
      "path": "packages/rigorloop/dist/lib/recording-contract.js",
      "identity": "sha256:574a3bc7573d1463f9e5cbe5c09faf6fedc539a0320b9f77d1ac5bbdb6004657"
    },
    {
      "path": "packages/rigorloop/dist/lib/record-store.js",
      "identity": "sha256:f719ced00e197612a0605cdd568c962562cbb3ad39468335bebc457cd4c90f6b"
    },
    {
      "path": "packages/rigorloop/test/record-store-queries.test.js",
      "identity": "sha256:1dfc9405bf776908086b1b7f134e86043982636924d781ba213ca7fa7b871a85"
    },
    {
      "path": "packages/rigorloop/test/helpers/recording-query-launcher.mjs",
      "identity": "sha256:a11c35bf45bb2c3c5e36f6b988d6d33f5e029fbe7ed22549a74a0defa9b57273"
    },
    {
      "path": "schemas/targeted-recording-v1.schema.json",
      "identity": "sha256:a704663b14046baace59be80c4ece92fce87177082f3bc33b2edefd6665ab475"
    },
    {
      "path": "packages/rigorloop/dist/schemas/targeted-recording-v1.schema.json",
      "identity": "sha256:a704663b14046baace59be80c4ece92fce87177082f3bc33b2edefd6665ab475"
    },
    {
      "path": "scripts/build-record-store-schema.mjs",
      "identity": "sha256:e2774e543455d86eab5b1e2e9a32edf75b4c04ffc63c3dd3bc4cacf340fd52aa"
    },
    {
      "path": "scripts/validation_selection.py",
      "identity": "sha256:66d2b298bcf848ec2b8095fc38845be3e5d8596136bf64def6a8e2a2bff8757f"
    },
    {
      "path": "scripts/test-select-validation.py",
      "identity": "sha256:3b6a9ba5d1a14258903342ea386afaddffc631c3c392c1090f2b003a27c31520"
    },
    {
      "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/evidence.yaml",
      "identity": "sha256:a2c72fa0156c21c6e489a4783d70602526f81d3eb11c95e17e5be3c83dbfa307"
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
      "state": "resolved",
      "resolution": {
        "actor": {
          "id": "m3-code-review",
          "role": "review"
        },
        "rationale": "Independent rereview confirms filter arrays sort by canonical JSON encoding. The quote/uppercase-path regression passes and selection/cursor normalization retains deterministic documented order.",
        "evidence_refs": [
          {
            "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/evidence.yaml",
            "id": "m3-contract"
          }
        ]
      }
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
      "state": "resolved",
      "resolution": {
        "actor": {
          "id": "m3-code-review",
          "role": "review"
        },
        "rationale": "Independent rereview confirms schema union validation preserves unsafe-path when no branch matches, while closed malformed selectors still reject. Direct subject_paths and applicability.paths traversal regressions pass.",
        "evidence_refs": [
          {
            "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/evidence.yaml",
            "id": "m3-contract"
          }
        ]
      }
    }
  ]
}
---
# M3 independent Code Review

Review status: clean-with-notes. Stored judgment: approved. The complete M3 increment at implementation handoff 8065bad7 satisfies the approved scoped-read, subject identity and bounded-receipt allocation. Findings m3-cr-001 and m3-cr-002 were recorded before correction and independently reassessed as resolved. Their original reviewed subjects and evidence remain truthful in the retained findings.

Reviewed the primary query adapter, structured observation traversal and canonical digest, strict query/result contract and canonical/package schema, compact receipt preparation, shared store snapshot and publication changes, test-only subprocess entry, and schema/validation-selection integration. The approved CLI, Workflow and Record Format models and delivery plan supplied authority; existing storage internals were inspected for coherence and publication interactions. Every approved Design/Delivery member identity and every registered M3 evidence subject matched current bytes.

| Checklist | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | CLI-SR-01/14/17/19/20/21/22, RF-SR-07 and WF-SR-14/15 mapped through M3 TG-03/TG-04; decisions remain actor-owned and public activation remains withheld. |
| Test coverage | pass | Independently ran all 29 record-store-queries.test.js tests; all passed. Registered m3-contract covers 148 recording checks. |
| Edge cases | pass | Direct tests cover literal selectors, missing/unselected containers, v1 origin absence, full Verify/decisions, normalized/nonmember/stale cursors, byte boundaries, external subject drift/absence, retained origins, busy/recovery/conflict, preview and retry. |
| Error handling | pass | Both recorded corrections verified; coherent snapshot checks precede optional failure metadata; malformed/unsafe/unreadable outcomes remain explicit. Prepared receipt proof prevents postcommit diagnostic reads and distinguishes lost response from storage failure. |
| Architecture boundaries | pass | Query selection, observer and renderer share the existing snapshot/publisher safety boundary; no targeted-construction or workflow eligibility engine added. |
| Compatibility | pass | Existing v1 schema and validator remain unchanged. v1 narrative/origin reads remain truthful; advanced aggregate fallback retains existing diagnostic codes. |
| Security/privacy | pass | Exact contained paths and safe messages; symlink/unreadable subjects reject, missing identities remain explicit, role labels do not authenticate. |
| Derived artifact currency | pass | m3-schema byte parity and m3-package-publication support the canonical/packaged result schema; test launcher preserves no-argument package discovery. No release activation claim. |
| Unrelated changes | pass | Implementation stays within M3 plus required schema bundling, selector proof and stage-owned evidence. |
| Validation evidence | pass | Current registered m3-* evidence: schema/model checks passed; 148 recording tests; 612 package tests plus 2 existing skips; metadata 115, boundary 87, selector 163, publication 7; explicit selection reports zero blockers. |

The dense completed-work failure test and maximum receipt/detail-overflow checks support bounded reporting without a readiness gate. The observer uses all schema-defined stored Subjects, including origin/supporting judgment, observes each unique path once, and hashes deterministic diagnostics plus current identities; request-only reads do not enter this reconstructible basis. Existing external-editor limitations remain. The internal query launcher demonstrates text/JSON parity without prematurely activating normal public dispatch.

Reviewed milestone: M3. Milestone closeout: closed at the independent review boundary; Route owns recording the milestone state. Required review-resolution: no outstanding work; m3-cr-001 and m3-cr-002 resolved. Remaining implementation milestones: M4 and M5; M6 final Verify remains. Next stage: Route may select M4 implementation under its existing authority. Recording status: recorded. Review log and separate resolution ledger: not required by this selected explicit-recording-v1 contract.

This is an increment assessment, not the required final whole-change Code Review. Primary targeted constructors/commands, consuming-skill adoption, token-benefit evaluation and final Verify remain downstream. Final closeout readiness, branch/PR readiness and Verify readiness are not claimed.
