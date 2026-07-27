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
| `python scripts/test-select-validation.py` | pass; 137 tests |
| `python scripts/test-adapter-distribution.py` | pass; 132 tests |
| `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5` | pass; three candidate archives |
| `python scripts/test-release-transaction.py` | pass; 87 tests |
| `python scripts/test-boundary-proof.py` | pass; 115 tests |
| `python scripts/validate-skills.py` | pass; 24 skills |
| `python scripts/test-skill-validator.py` | pass; 261 tests |
| `python scripts/build-skills.py --check` | pass |
| `python scripts/validate-boundary-proof.py generate-report --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills --output docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/boundary-capability-baseline.md` | pass |
| `python scripts/validate-boundary-proof.py validate-report docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/boundary-capability-baseline.md` | pass |
| `bash scripts/ci.sh --mode explicit --path scripts/boundary_proof_behavior.py --path scripts/boundary_proof_model.py --path scripts/validate-boundary-proof.py --path scripts/test-boundary-proof.py --path tests/fixtures/boundary-proof/incident-registry.json --path tests/fixtures/boundary-proof/simple-change.json --path templates/shared/boundary-proof-model.md --path skills/spec/SKILL.md --path skills/spec-review/SKILL.md --path skills/test-spec/SKILL.md --path skills/test-spec-review/SKILL.md --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path skills/verify/SKILL.md --path skills/workflow/SKILL.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path specs/skill-contract.md --path specs/skill-contract.test.md` | pass; 14 selected checks |
| `git diff --check` | pass |

The passing current behavior result is
`run-62735d2bff6ab29bfe208183cf33fc03`, bound to input set
`sha256:6a213f0df33f642c0f46661c47aeca84c8c531c99610af0a6d64256649580729`.
The capability report result is `pass` with identity
`sha256:ab0057f39cb928f0f08d07a8398aca82659bbeba267aa557514c02e5249c101f`.

The first typed-report reconstruction exposed and rejected a non-semantic
mapping-order assumption in the `support` projection. The corrected validator
requires the exact support key set while preserving exact order for normative
sequences such as operation dependencies. The fresh run and report above were
generated only after that correction was committed.

Final holistic review R1 then exposed that helper-level boundary routing did
not compose through the public selector: governed scripts remained
`script-unsupported`, most boundary fixtures were unclassified, and the
stateful boundary suite was incorrectly marked parallel-safe under three
different check IDs. The correction gives governed scripts and the complete
fixture subtree one closed `boundary-proof` category, retains
`release_transaction.regression` for release fixtures, leaves unrelated
unsupported scripts fail-closed, and serializes the three shared-state suite
routes. The exact plan-owned selected-CI command now passes all 14 checks.

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
