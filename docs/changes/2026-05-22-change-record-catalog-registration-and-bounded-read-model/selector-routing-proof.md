# Selector Routing Proof

## Purpose

This proof records the M2 requirement that changed-path selector routing runs over the branch's actual changed paths before verify. Explicit-path validation remains supplemental and does not substitute for routing the actual changed set.

## Proof expectations

- Registered change-local evidence routes through its evidence class.
- Unregistered deterministic change-local evidence produces `manual-routing-required` registration debt.
- Actual local selector mode discovers changed and untracked branch paths instead of relying on a hand-picked explicit path list.
- Selected CI preserves blocking selector diagnostics and fails closed when the selector reports registration debt.

## M2 evidence

The M2 selector tests add direct coverage for:

- `docs/changes/<change-id>/notes.md` as unregistered deterministic evidence, with `manual-routing-required`, `debt: evidence-registration`, `verify_readiness: blocked`, and an owner-approved deferral shape naming owner, path, reason, validation impact, and follow-up;
- local changed-path mode discovering `docs/changes/<change-id>/selector-routing-proof.md` even when explicit mode is run only over `change.yaml`.

The implementation registers `selector-routing-proof.md` as routing-coverage evidence so this proof file itself routes deterministically through changed-path selection.

## Owner-approved deferral proof

The `CRM-M2-CR1` resolution adds selector-owned deferral evaluation for deterministic unregistered change-local evidence. A complete owner-approved deferral is read from the governing `change.yaml` field `evidence_registration_deferrals` and must include:

- `owner`
- `path`
- `reason`
- `validation_impact`
- `follow_up`

Selector regression covers four cases:

- no deferral remains `manual-routing-required` with `verify_readiness: blocked`;
- incomplete deferral remains blocked and names missing fields;
- mismatched deferral path does not unblock the evidence path;
- complete deferral remains visible as `manual-routing-required` and `debt: evidence-registration`, but reports `verify_readiness: owner-deferred`.

## Validation evidence

`python scripts/select-validation.py --mode explicit --path docs/changes/2026-04-25-example/notes.md` returned `status: blocked`, `category: unregistered-change-evidence`, `code: manual-routing-required`, `debt: evidence-registration`, and `verify_readiness: blocked`.

`python scripts/select-validation.py --mode local` discovered the actual changed M2 paths:

- `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`
- `docs/plan.md`
- `docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md`
- `scripts/test-select-validation.py`
- `scripts/validation_selection.py`
- `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/selector-routing-proof.md`

The same local selector run returned `status: ok`, selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`, and included `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/` in `affected_roots`.

`bash scripts/ci.sh --mode local` ran selected checks for the actual M2 changed paths and passed `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`.
