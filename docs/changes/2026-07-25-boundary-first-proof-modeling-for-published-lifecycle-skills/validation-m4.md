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
| `python scripts/test-boundary-proof.py` | pass; 115 tests |
| `python scripts/validate-skills.py` | pass; 24 skills |
| `python scripts/test-skill-validator.py` | pass; 261 tests |
| `python scripts/build-skills.py --check` | pass |
| `python scripts/validate-boundary-proof.py generate-report --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills --output docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/boundary-capability-baseline.md` | pass |
| `python scripts/validate-boundary-proof.py validate-report docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/boundary-capability-baseline.md` | pass |
| `git diff --check` | pass |

The passing current behavior result is
`run-62735d2bff6ab29bfe208183cf33fc03`, bound to input set
`sha256:6a213f0df33f642c0f46661c47aeca84c8c531c99610af0a6d64256649580729`.
The capability report result is `pass` with identity
`sha256:4cfacf61164795d4e227e97f93211e70b8f1554162ee5381b8ef36bc24f33b1c`.

The first typed-report reconstruction exposed and rejected a non-semantic
mapping-order assumption in the `support` projection. The corrected validator
requires the exact support key set while preserving exact order for normative
sequences such as operation dependencies. The fresh run and report above were
generated only after that correction was committed.

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
