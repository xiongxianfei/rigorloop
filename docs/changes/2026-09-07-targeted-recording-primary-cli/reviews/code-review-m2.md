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
  "independence_basis": "Separate delegated reviewer independently inspected implementation, approved model and delivery subject maps, and fault tests without editing implementation. Reproduced an acquisition failure in a disposable root and recorded the finding before correction. Actor labels are attribution only.",
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
      "identity": "sha256:82d3191a8935e00f99c9ba4240204e51c6757108649b3e35687ed25bbb8eab50"
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
      "identity": "sha256:dc4ec7513b95b60bf01f60d660ae8cf7f2f77bc8db1d15afb48de47890b4824d"
    },
    {
      "path": "scripts/validate-record-store.mjs",
      "identity": "sha256:70a255d2cad4fc993c9418294563a309244646b79399e3c1412d7208c1af1bc7"
    }
  ],
  "judgment": "changes-requested",
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
      "state": "open",
      "resolution": null
    }
  ]
}
---
# M2 Code Review

First-pass status: changes-requested. M2 shared persistence only; no whole-change or Verify approval.

Finding ID: m2-cr-001

A failed exclusive lock write can leave an unrecoverable owned lock. See the structured finding for evidence, severity and required correction.

Checklist: spec alignment concern (I/O recoverability); tests concern (post-create lock failure missing); edge cases concern (same failure); error handling concern; architecture pass; compatibility pass on inspected v1 boundary; security/privacy pass; derived artifacts pass for reviewed scope; unrelated changes pass; validation evidence pending final registered execution results. Independent v2 persistence run: 33 tests passed before the remaining root-authored regression additions.

Recording status: recorded. Milestone closeout: resolution-needed. Required review-resolution: yes, by implementation owner then this reviewer. Remaining implementation milestones: M3, M4, M5; M6 final Verify remains later. Next stage: M2 correction and rereview. Verify readiness: not-claimed. Review log and separate review-resolution artifacts are not required under the selected explicit-recording-v1 contract.
