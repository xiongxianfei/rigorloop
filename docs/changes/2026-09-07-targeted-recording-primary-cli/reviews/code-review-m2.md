---
{
  "schema_version": 1,
  "change_id": "2026-09-07-targeted-recording-primary-cli",
  "id": "code-review-m2",
  "target": "code",
  "reviewer": {
    "id": "m2-code-review",
    "role": "review"
  },
  "contributors": [
    {
      "id": "codex-root",
      "role": "implement"
    }
  ],
  "independence_basis": "Separate delegated reviewer independently inspected the complete M2 implementation diff against exact approved Design and Delivery subjects without editing implementation. Recorded m2-cr-001 before correction, reread the corrected acquisition/release boundary and full final diff, independently ran all 41 v2 persistence tests, examined completed broader validation summaries, and verified each registered M2 evidence subject identity. codex-root authored implementation and execution evidence; reviewer owns this assessment. Actor labels are attribution only.",
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
      "path": "packages/rigorloop/dist/lib/record-store.js",
      "identity": "sha256:08e946d727c10fcd43e4b545ce544c2e5077a1bc646a92746dde90be4e4feb9c"
    },
    {
      "path": "packages/rigorloop/dist/lib/record-store-format.js",
      "identity": "sha256:eabf51c610956c19c8490d42c7cdcd584a65258d0cba4155560886eeda59353a"
    },
    {
      "path": "packages/rigorloop/dist/lib/record-store-files.js",
      "identity": "sha256:5f83885b5198a8687942488887512344b9daa2ed77856072a9459996b3ed373d"
    },
    {
      "path": "packages/rigorloop/dist/lib/record-format-v2.js",
      "identity": "sha256:08cac36c9df883fb3fa6267b3e4f7f5e36a3f43e16d96900a72ede1ca57f8540"
    },
    {
      "path": "packages/rigorloop/dist/lib/record-store-cli.js",
      "identity": "sha256:05fd20c590a54fdcfbe639b7b1d91e956527e985997710a786be51482edfe34f"
    },
    {
      "path": "packages/rigorloop/test/record-store-v2-persistence.test.js",
      "identity": "sha256:6e85ded3a08a8104dbbc40f6f15343d1b8736a35037b673356841682a3f99140"
    },
    {
      "path": "scripts/validate-record-store.mjs",
      "identity": "sha256:70a255d2cad4fc993c9418294563a309244646b79399e3c1412d7208c1af1bc7"
    },
    {
      "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/evidence.yaml",
      "identity": "sha256:084d53d99a4e6c3eb8f824f35f283bfc48e9f8fb7fa62dc287d9d4d498f75164"
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
      "id": "m2-cr-001",
      "reporter": {
        "id": "m2-code-review",
        "role": "review"
      },
      "owner": {
        "id": "codex-root",
        "role": "implement"
      },
      "subjects": [
        {
          "path": "packages/rigorloop/dist/lib/record-store.js",
          "identity": "sha256:82d3191a8935e00f99c9ba4240204e51c6757108649b3e35687ed25bbb8eab50"
        },
        {
          "path": "packages/rigorloop/dist/lib/record-store-files.js",
          "identity": "sha256:5f83885b5198a8687942488887512344b9daa2ed77856072a9459996b3ed373d"
        }
      ],
      "evidence": "Severity: major. Location: Store.acquire lock-write catch and RecordFiles.write exclusive path. Exclusive write may successfully create/write the lock and then throw from fsync or containment checks. acquire unconditionally clears its token on error, so the outer finally cannot remove the owned lock. Independent reproduction wraps RecordFiles.write, invokes its real lock write, then throws EIO: record returns rejected/io-failure; immediately inspecting the same root returns busy with the current process lock retained and no prepared transaction. After process exit this becomes recovery-required with no journal to recover. This violates M2 TG-02 I/O failure recoverability.",
      "required_outcome": "Handle failed exclusive lock creation without discarding verified ownership of a lock this attempt created. Remove only an exact owned lock when safe; never remove a competing lock on EEXIST or unknown bytes. Add regression coverage for failure after actual lock creation and retained competing lock behavior through the shared boundary. No design decision is required.",
      "state": "resolved",
      "resolution": {
        "actor": {
          "id": "m2-code-review",
          "role": "review"
        },
        "rationale": "Rereview confirms non-EEXIST lock-write failures retain the attempted token for exact-identity cleanup. A fully written owned lock is removed safely; partial or third-state bytes remain unchanged and produce recovery-required. EEXIST contention does not acquire ownership or remove the competing lock. Added owned/partial/third-state regressions pass within the independently executed 41-case v2 suite; shared v1 and broader package regressions remain passing.",
        "evidence_refs": [
          {
            "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/evidence.yaml",
            "id": "m2-contract"
          }
        ]
      }
    }
  ]
}
---
# M2 Code Review

Native status: clean-with-notes. Approved scope: M2 shared persistence only. Finding m2-cr-001 was recorded before correction and is now resolved; its original finding subjects and evidence are retained above.

Reviewed the complete M2 implementation and its approved Design/Delivery subject maps. Both formats now enter the same version-dispatched candidate, exclusion, publication and exact-byte recovery path. Advanced v1 envelope and source schema remain unchanged; no targeted interface or general v2 adoption is activated here. Standalone live validation uses the shared coherent reader. Record and recovery prepare their validated storage results before publication; M3 still owns diagnostic bounds and primary rendering.

## Checklist

| Item | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | CLI-SR-02/04/05/06/08/09/10 and RF-SR-02/04/06/08 traced through M2/TG-02; exact approved model and delivery identities verified. |
| Test coverage | pass | 41 independent v2 persistence cases, all 119 recording cases and 582 package cases passing; 2 preexisting package skips. |
| Edge cases | pass | Concurrent readers/writers, stale revisions/targets/read basis, absent-root races, no-op preconditions, repeated recovery and lost-success retry directly exercised. |
| Error handling | pass | Prepare/publish/commit interruptions, owned/partial/third-state lock failures, EACCES/ENOSPC, third-state targets, exact recovery identities and post-publication basis drift. |
| Architecture boundaries | pass | Shared engine and format adapter retain actor-owned decisions and prevent migration; standalone live validator shares coherent reader. |
| Compatibility | pass | v1 request/result/journal paths remain supported; mixed/dual manifests reject; 115 metadata checks and full package regressions pass. |
| Security/privacy | pass | Containment and substituted-ancestor, symlink/hardlink tests; safe diagnostic codes and attribution-only actors; unknown bytes never guessed safe. |
| Derived artifact currency | pass | Schema parity, 7 package-publication checks and scoped structure checks pass; M2 adds no generated adapter sources. |
| Unrelated changes | pass | Six implementation/test/script files match M2; current evidence and route records are separate actor-owned recording. Models/plan unchanged. |
| Validation evidence | pass | Every subject in nine registered m2-* checks hash-matches; approved upstream review member maps also verified. |

Independent command: `node --test packages/rigorloop/test/record-store-v2-persistence.test.js` — 41 passed. Inspected registered procedures/results include `node --test packages/rigorloop/test/record-store-*.test.js` (119 passed), `npm --prefix packages/rigorloop test` (582 passed, 2 existing skips), `python scripts/test-change-metadata-validator.py` (115 passed), schema parity, model/boundary checks, package-publication checks and diff integrity. These are scoped validation evidence, not final Verify or CI claims.

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this stable review and its explicit manifest applicability/registration
- Open blockers: none within M2
- Next stage: Route may close M2 and select M3
- Review status: clean-with-notes
- Material findings: m2-cr-001 resolved; none open
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-09-07-targeted-recording-primary-cli/reviews/code-review-m2.md
- Review log: not-required under selected explicit-recording-v1 contract
- Review resolution: retained in this record; no separate artifact required
- Reviewed milestone: M2
- Milestone closeout: review supports closure; Route owns the milestone update
- Remaining implementation milestones: M3, M4, M5; M6 final Verify remains later
- Required review-resolution: no
- Finding IDs: m2-cr-001 (resolved)
- Verify readiness: not-claimed

This incremental review does not replace final whole-change Code Review. Primary queries, bounded diagnostic rendering, targeted constructors and coherent consumer adoption remain later milestones. The documented external-edit limitation is retained; this review claims only the observed checks and tested containment boundary.
