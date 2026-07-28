# M1 Implementation: Canonical Reference and Projection Foundation

## Scope completed

M1 adds one authored portable method, one closed projection inventory, and one shared digest helper.
It also adds check/write projection behavior and raw-byte-identical copies under the ten governed canonical skill roots.

The tests were added before the projection module and initially failed because `boundary_first_reference` did not exist.
The first projection check then failed on all ten missing consumers before write mode created them.
Code-review R1 then reproduced a parent-directory symlink escape.
The correction added failing source-parent and destination-parent regressions before adding one shared repository-path guard.

## Changed surfaces

- `specs/references/boundary-first-method-v1.md` owns the authored method.
- `scripts/boundary_first_reference.py` owns version, source, consumer inventory, digest serialization, and check/write behavior.
- `scripts/project-boundary-first-reference.py` exposes the read-only check mode and bounded write mode.
- `scripts/test-boundary-first-reference.py` proves vocabulary, membership, raw-byte identity, idempotency, drift, leaf and parent symlink rejection, digest, and content rules.
- Ten projected reference files under the governed skill roots are generated and not hand-authored.

## Aligned surfaces

The ten `SKILL.md` resource maps and stage-local instructions are unaffected with rationale.
M2 owns their mappings and semantic behavior after M1 is independently reviewed.

Structural boundary-record, activation, and selection validators are unaffected with rationale.
M3 owns those validators and imports the M1 digest and inventory rather than redefining them.

Adapter and installed-tree tests are unaffected with rationale.
M4 owns generated, packed, and installed parity after the canonical projection and skill mappings are reviewed.

## Validation

```text
python scripts/test-boundary-first-reference.py
python scripts/project-boundary-first-reference.py --check
python scripts/validate-change-metadata.py docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/change.yaml
git diff --check -- <M1 implementation paths>
```

All commands passed after the R1 correction.
The test suite ran nine tests.
The projection check found ten current consumers with inventory identity
`a764f05f5427e13ac69e44210fe6b006313afca0fa9d94135095358c64cec2d9`.

## Review correction

PBF-M1-CR1 is resolved by commit `0b198866`.
Every existing source or destination path component is checked for symlinks before reading, creating parents, checking, or writing.
Unexpected-projection enumeration no longer follows skill-root or reference-directory symlinks.
The two adversarial regressions prove the command fails before outside reads or writes while the original M1 proof remains green.
