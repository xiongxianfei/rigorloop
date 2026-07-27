# M4 Validation: Portable Boundary Capability Baseline

Date: 2026-07-27

Milestone: M4

Result: pass

## Scope

- Registered the six closed boundary-proof check IDs and their exact changed
  path routing.
- Proved raw-byte parity for the eight governed skills and their shared
  boundary resource across canonical, generated, packed, and installed
  adapter surfaces.
- Replayed the frozen incident set, current upstream behavior run, and M3
  preservation evidence into the sole-writer capability report.
- Added complete activation, partial-activation rejection, and rollback
  fixtures to the release-transaction regression suite without activating or
  publishing a release.

## Automated evidence

| Command | Result |
| --- | --- |
| `python scripts/test-select-validation.py` | pass; 134 checks |
| `python scripts/test-adapter-distribution.py` | pass; 132 tests |
| `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5` | pass; three candidate archives |
| `python scripts/test-release-transaction.py` | pass; 87 tests |
| `python scripts/test-boundary-proof.py` | pass; 113 tests |
| `python scripts/validate-boundary-proof.py generate-report --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills --output docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/boundary-capability-baseline.md` | pass |
| `python scripts/validate-boundary-proof.py validate-report docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/boundary-capability-baseline.md` | pass |
| `git diff --check` | pass |

The passing current behavior result is
`run-fea7ef7510b6ae94ec3d9485452b6102`, bound to input set
`sha256:623c9552fda539b5ff017e0354e1d2927794ac30cddd2d2791919123bf5b6710`.
The capability report result is `pass` with identity
`sha256:89fe2ff1a7c3476b207425da764765252a0793c4dbff5337263d15b019210589`.

## Release boundary

Bare validation of published v0.3.6 metadata is not a valid candidate check:
the historical report binds the archived source commit and archive hashes,
while this branch intentionally changes canonical adapter inputs. The
repository correctly rejected both a missing output directory and newly built
bytes that did not match the immutable published hashes.

M4 therefore validates current non-publishing output through fresh v0.1.5
candidate archives and validates activation/rollback semantics through the
release-transaction suite. It does not alter published v0.3.6 evidence, write
an activation marker, publish, or deploy.
