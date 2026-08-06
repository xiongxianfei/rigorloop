# M3 implementation evidence

Milestone: M3 — Routine v0.4.0 release payload and package parity

Outcome: implemented and ready for code review.

## Implemented behavior

- Added the routine `v0.4.0` release profile for Codex, Claude, and opencode and
  prepared its profile-owned release, package, fixture, and timing surfaces.
- Updated the npm package to `0.4.0` and bundled exact adapter archive metadata
  for all three targets. The bundled release index pins the metadata file by
  SHA-256.
- Completed the local pre-publication release evidence with exact archive
  hashes, tree hashes, file counts, target-native smoke results, and tracked
  release notes. Publication evidence remains explicitly pending.
- Extended the existing release validator and standing release gate allowlists
  to recognize `v0.4.0`; no new publishing command or alternate release path
  was added.
- Kept `specs/boundary-first-activation.yaml` pending throughout this milestone.
  No tag, push, registry write, publication, merge, or public-success claim was
  performed.

## Test-first and generation evidence

- `python scripts/prepare-release.py v0.4.0` initially failed because the
  routine profile did not exist. Adding the profile generated the nine owned
  surfaces and the immediate `--check` run passed without writing output.
- Packed-package validation initially failed because the generated release
  index pointed to missing `v0.4.0` bundled adapter metadata. Building temporary
  archives supplied the exact archive and tree identities; after the bundled
  metadata and release evidence were completed, packed npm validation passed.
- Finalized pre-publication evidence is preserved only after its complete
  release-metadata and standing-record contracts pass. The exact review tree
  passes `prepare-release --check`; partial, stale, and prematurely public
  evidence is regenerated or rejected.

## Exact adapter evidence

| Target | Archive SHA-256 | Tree SHA-256 | Files |
| --- | --- | --- | ---: |
| Codex | `f37afb961f3527ddf677e5fc7ba85b5f2840b3abb25384b3ba88f22f844207f3` | `2986d5e38a83bf3044e96de9057048e7ce75d5439b44b65d6498e2309213f4c8` | 63 |
| Claude | `46d6ab7f79dcdf39dd3c5ec992c0fdac07b4d8e8c29443c061a613f9465dcdd2` | `1af6ce59bdc56609d88ee151f3740e5d69e462764823c0ed9950e5b8580066ec` | 63 |
| opencode skills | `55977a7b925325f3f4b07f51dd8a573deb7519c63d4a9cde96b387962c411fad` | `1af6ce59bdc56609d88ee151f3740e5d69e462764823c0ed9950e5b8580066ec` | 63 |
| opencode commands | same archive | `b9beece61c967adf20cd12d9290849c7137f8b59032a2ec45d85a960869eaa30` | 10 |

## Validation

- `python scripts/prepare-release.py v0.4.0` — pass; nine profile-owned
  surfaces prepared.
- `python scripts/prepare-release.py v0.4.0 --check` — pass immediately after
  preparation; no output drift.
- `python scripts/release-preflight.py v0.4.0 --skip-remote` — pass against the
  final local pre-publication payload.
- `python scripts/test-release-transaction.py` — pass, 102 tests.
- `python scripts/test-adapter-distribution.py` — pass, 149 tests.
- `python scripts/test-artifact-lifecycle-validator.py` — pass, 168 tests.
- `python scripts/test-npm-package-publication.py` — pass, 6 tests.
- `python scripts/select-validation.py --mode release --release-version v0.4.0`
  — pass; selected `release.validate` and required `broad_smoke.repo`.
- `bash scripts/ci.sh --mode release --release-version v0.4.0` — pass;
  `release.validate` passed in 2.40 seconds and `broad_smoke.repo` passed in
  525.12 seconds.
- `bash scripts/release-verify.sh v0.4.0` — pass; generated all three temporary
  archives, ran the adapter and packed-package suites, and validated the final
  `v0.4.0` metadata against reviewed source commit `c7b0babe`.
- `git diff --check` — pass.

## R6 review resolution

- `UBR-M3-CR6-001`: every required emergency-deferral field now rejects empty
  and placeholder values, and an actively deferred result requires the
  deferral-row status to be exactly `open`.
- The emergency table now has one exclusive shape: either exactly one `none`
  sentinel when nothing is deferred, or the real matched deferral row. Mixed
  sentinel and real-deferral evidence fails closed.
- Independent mutations cover all eight required metadata fields, unknown
  status, duplicate and missing deferrals, unmatched results, and the
  contradictory sentinel case. The correction passes 168 lifecycle tests and
  102 release-transaction tests.

## R5 review resolution

- `UBR-M3-CR5-001`: all ten preflight rows now use the same exact-cardinality
  contract in pending, finalized, and emergency states. npm package-build and
  local packed-install proof accept only applicable results, never
  `not-applicable`.
- Registry results are state-aware: unpublished evidence may record the
  registry as not yet applicable, while published evidence requires every
  registry row to pass. Only emergency `fresh registry install smoke` may be
  `deferred`.
- Each deferred result must match exactly one complete emergency-deferral row,
  and each deferral row must match a deferred result. Unsupported items,
  duplicate deferrals, and unbound results fail closed.
- Exhaustive missing, duplicate, unsupported, applicability, and deferral
  mutations across all fifteen governed rows pass for pending, finalized, and
  emergency evidence. The focused correction proof includes 166 lifecycle
  tests, 102 release-transaction tests, exact preparation and preflight, all
  nine tracked release records, and whitespace validation.

## R4 review resolution

- `UBR-M3-CR4-001`: the routine preflight contract now owns all ten governed
  rows, and the registry contract owns all five governed rows. Each row must
  appear exactly once, so missing and contradictory duplicate evidence fails
  closed before preservation or publication.
- Finalized routine evidence requires every preflight row to pass. Pending
  evidence retains only the row-specific allowed terminal states plus
  `pending`, and emergency registry deferral remains limited to the existing
  emergency contract.
- Passing smoke proof now trims both `tool_version` and `evidence`, rejecting
  whitespace-only values. Complete removal, unsupported-result, duplicate-row,
  and whitespace mutation regressions pass.
- The correction is covered by 102 release-transaction tests, 162 lifecycle
  tests, exact preparation and preflight, the complete standing release gate,
  and final-tree release-selected CI (`release.validate` 2.60 seconds;
  `broad_smoke.repo` 544.17 seconds).

## R2 review resolution

- `UBR-M3-CR2-001`: trusted hosted-tag verification now requires the requested
  release and `GITHUB_REF_NAME` to match, resolves the explicit
  `refs/tags/<name>^{commit}` ref with replacement objects and ambient Git
  authority disabled, and binds that commit to checked `HEAD` and the full
  trusted workflow commit. Real lightweight, annotated, mixed-name,
  missing-ref, and rewritten-tag fixtures pass.
- `UBR-M3-CR2-002`: release YAML preservation now uses the repository-owned
  parser and exact target, smoke, validation, npm, and adapter-release mappings.
  Standing evidence reuses the lifecycle checklist and additionally enforces
  the exact pending-publication and pre-public registry state. Partial release
  YAML, missing standing sections, and premature public status all fail closed.
- The corrected command set passes with 96 release-transaction tests, 149
  adapter-distribution tests, 162 artifact-lifecycle tests, 6 packed npm tests,
  final-state preparation, preflight, recorded-source validation, the standing
  full release gate, and release-selected CI (`release.validate` 2.39 seconds;
  `broad_smoke.repo` 548.85 seconds).

## R3 review resolution

- `UBR-M3-CR3-001`: pending standing evidence now always contains every required
  routine preflight row; pending validation accepts only `pending` or `pass`,
  while finalized lifecycle validation still requires `pass` and retains its
  established diagnostic contract.
- Finalized release YAML now binds `manifest_version` to the parsed
  `dist/adapters/manifest.yaml` authority and applies the same semantic rules as
  the full release validator to passing smoke rows: a known tool version and
  nonempty evidence are mandatory.
- Per-row removal, unknown pending result, bogus manifest identity, and empty
  passing-evidence regressions pass. The correction is covered by 100
  release-transaction tests, 162 lifecycle tests, exact preparation and
  preflight, the complete standing release gate, and final-tree release-selected
  CI (`release.validate` 2.81 seconds; `broad_smoke.repo` 546.86 seconds).

## R1 review resolution

- `UBR-M3-CR1-001`: finalized pre-publication release YAML and adapter evidence
  remain generator-owned but are no longer replaced by pending placeholders.
  The bundled index derives its metadata SHA from the actual bundled file, and
  a post-finalization regression plus the final repository tree pass
  `prepare-release --check`.
- `UBR-M3-CR1-002`: the `v0.4.0` profile owns the closed `latest` npm dist-tag.
  Preparation projects it into pending evidence, trusted publication passes it
  explicitly with `--tag`, unknown values fail closed, and ambient npm tag
  configuration cannot redirect the command.
- `UBR-M3-CR1-003`: hosted tag verification now requires a full
  `RELEASE_TAG_COMMIT` supplied from `github.sha`, compares it with checked
  `HEAD`, and compares a tag ref with the same commit. Missing, abbreviated, or
  mismatched authority stops before release checks. Adapter archive source
  identity remains a separate full SHA and no longer supplies both sides of the
  trusted tag check.
- `UBR-M3-CR1-004`: preparation now creates and validates the pending standing
  `docs/releases/v0.4.0.md` record with identity, gate, package, publication,
  registry, recovery, follow-up, and evidence-safety sections.
- The corrected command set passes with 87 release-transaction tests, 149
  adapter-distribution tests, 6 packed npm tests, final-state preparation,
  preflight, recorded-source validation, the standing full release gate, and
  release-selected CI (`release.validate` 2.41 seconds;
  `broad_smoke.repo` 545.44 seconds).

## Aligned-surface audit

- Updated: routine release profile/evidence, package version and README,
  bundled release metadata, current-version fixture, adapter release
  classification, and the standing release-gate target lists.
- Updated: the existing trusted tag gate now verifies one exact hosted release
  identity; publication closeout tooling remains unchanged. M3 still stops
  before external mutation.
- Unaffected: tracked generated adapter bodies. Release archives are temporary
  outputs; canonical skills remain the only authored source.
