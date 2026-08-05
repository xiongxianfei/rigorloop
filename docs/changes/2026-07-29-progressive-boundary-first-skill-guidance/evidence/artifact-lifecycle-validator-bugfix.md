# Artifact Lifecycle Validator Bugfix Evidence

## Problem

The artifact lifecycle validator required an embedded `## Status` section from
the current proposal even though the approved
`stage-owned-change-local-v1` contract makes the exact `artifact_states` entry
in the owning `change.yaml` authoritative.

## Reproduction

Before the fix, validating the current proposal and change record blocked with:

> missing required Status section

The regression was reproduced before production code changed. Four new
stage-owned tests failed while the legacy no-status compatibility test passed.

## Root cause

`artifact_lifecycle_validation.py` still applied its legacy embedded-status
contract to every classified artifact. It neither followed the stable
`Owning change record` pointer nor delegated closed-vocabulary state validation
to `change_metadata_semantics.py`.

## Resolution

The validator now:

- follows the stable owning-change-record pointer from governed artifacts;
- expands stage-owned `artifact_states` paths into validation scope;
- reuses the existing change-metadata parser and
  `validate_stage_owned_lifecycle_metadata` semantic owner;
- resolves lifecycle state from exactly one normalized artifact entry;
- rejects missing, duplicate, mismatched, unknown, or kind-incompatible
  ownership data;
- rejects embedded `## Status` in current stage-owned artifacts; and
- preserves the legacy embedded-status path for artifacts that have not opted
  into `stage-owned-change-local-v1`.

This is a compatibility adapter, not a second workflow-state engine.

## Validation

- `python scripts/test-artifact-lifecycle-validator.py` — passed 162 tests.
- `python scripts/test-change-metadata-validator.py` — passed.
- `python -m py_compile scripts/artifact_lifecycle_validation.py scripts/test-artifact-lifecycle-validator.py` — passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-07-29-progressive-boundary-first-skill-guidance.md --path docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/change.yaml` — passed with one pre-existing nonblocking merge-dependent-language warning.
- `git diff --check -- scripts/artifact_lifecycle_validation.py scripts/test-artifact-lifecycle-validator.py` — passed.
