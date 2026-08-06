# M4 implementation evidence

Milestone: M4 — Active snapshot and integrated pre-public verification

Outcome: implemented and ready for code review.

## Active snapshot

- The exact independently reviewed M3 source baseline is
  `ca2630e4a0a4bc82c330b51f0480eb97e047ec3f`. Code-review M3 R7 reviewed that
  source tree and recorded its clean result in commit `5e6a4ce8`.
- The repository-internal `derive_grandfathered_specs(root,
  baseline_revision)` function was called exactly once for M4. It returned no
  issues and a raw-UTF-8-sorted tuple of 78 paths.
- The exact output tuple is frozen in
  `specs/boundary-first-activation.yaml#grandfathered_specs`; its first path is
  `specs/artifact-status-lifecycle-ownership.md` and its last path is
  `specs/workflow-stage-autoprogression.md`.
- The active record sets release intent `v0.4.0`, immutable rollback
  `v0.3.6`, and the full reviewed baseline identity. The bootstrap proof-model
  state now agrees with the active manifest.
- No transition writer, receipt, public CLI, recurring history check, or
  second activation mechanism was added.

## Checked-revision proof

- `python scripts/test-boundary-first-validation.py` — pass, 62 tests. The
  suite retains independent pending fixtures while treating the repository and
  no-history fixture as active snapshots.
- `python scripts/validate-boundary-first.py --check` — pass. Output reports
  snapshot `active`, release intent `v0.4.0`, rollback `v0.3.6`, and the three
  authoritative rollback archives; it does not inspect Git history or claim a
  tag, publication, or public availability.
- `python scripts/release-preflight.py v0.4.0 --skip-remote` — pass with only
  the pre-existing report-only `v0.3.4` literal warning.

## Integrated release proof

- `bash scripts/ci.sh --mode release --release-version v0.4.0` — pass.
  `release.validate` passed in 2.34 seconds and the required
  `broad_smoke.repo` passed in 493.99 seconds; total boundary-phase time was
  496.33 seconds.
- `bash scripts/release-verify.sh v0.4.0` — pass on the active snapshot. The
  gate ran 285 skill tests with 16 intentional skips, 149 adapter tests, and 6
  packed npm tests; rebuilt all three `v0.4.0` adapter archives; and validated
  release metadata against the recorded archive-source commit
  `c7b0babe6e8c91655c2b98f4092197eef5fabc69`.
- The recorded archive-source commit remains intentionally distinct from the
  M4 activation baseline and future trusted tag authority. M3 R2/R3 review
  already proved those identities cannot substitute for one another.

## Scope and safety

- Changed only the declarative activation record, its canonical proof-model
  state/readiness text, active-versus-pending regression fixtures, this
  implementation evidence, and matching local lifecycle/release evidence.
- Preserved the generated skill/resource projections and all package/archive
  bytes; the release gates found no derived-output drift.
- Performed no tag creation, push, registry write, publication, merge, network
  release check, or public-success claim.
