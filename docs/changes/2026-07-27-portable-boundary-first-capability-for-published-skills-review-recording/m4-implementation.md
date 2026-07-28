# M4 Package Parity and Prospective Activation

## Scope

M4 reuses the existing adapter distribution and boundary validation modules.
It adds no standalone packaging command, activation writer, rollback writer,
receipt, transaction, attestation store, installer, or publication action.

## Package and install proof

The existing adapter suite now has two focused `boundary_first` tests. They
build the three local adapter archives, validate mapped-resource parity,
explicitly read each included governed `SKILL.md` and reference, install the
archives into empty temporary projects through the existing local installer,
and compare installed reference bytes.

The matrix is derived from existing adapter portability decisions: ten
canonical skill projections remain mandatory, while package/install proof
covers all 28 currently published target/skill pairs across all three target
trees. The two workflow exclusions remain owned and validated by the adapter
contract rather than being invented by boundary-first logic.

`validate_clean_install_smoke` now respects those existing per-skill adapter
decisions and verifies that each included installed skill file is readable
before checking its mapped resources.

## Read-only rollback proof

The existing boundary validator selects the active fixture's rollback release,
reads the existing adapter manifest and tracked artifact metadata, and returns
one ordered adapter/archive/SHA-256 identity per supported adapter. Missing,
additional, duplicated, failing, and mixed-version matrices fail. The selector
does not open archives, install packages, publish releases, or mutate inputs.

The repository activation manifest remains `pending`; a real release
transition remains outside this change.

## Validation

| Command | Result |
| --- | --- |
| `python scripts/test-adapter-distribution.py -k boundary_first` | pass; 2 tests |
| `python scripts/test-adapter-distribution.py` | pass; 133 tests |
| `python scripts/test-boundary-first-validation.py` | pass; 54 tests |
| `python scripts/build-skills.py --check` | pass |
| `python scripts/project-boundary-first-reference.py --check` | pass; 10 projections |
| `python scripts/validate-boundary-first.py --check` | pass; pending activation |
| `python scripts/test-boundary-first-validation.py -k active_rollback_release_matches_current_adapter_metadata` | pass; 1 test |
| `bash scripts/ci.sh --mode broad-smoke` | pass; 12 checks |

## Handoff

M4 is ready for independent code review after its plan and change-local
evidence are synchronized.
