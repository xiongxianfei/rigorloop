# Spec Revision Evidence R3: Usability-First Boundary-First v0.4.0 Release

Stage: spec
Revision: 3
Date: 2026-08-06
Artifact ID: spec
Spec: `specs/usability-first-boundary-release.md`
Review basis: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/spec-review-r2.md`

## Revision result

- `UBR-SR2-001`: UBR-R006 and UBR-R007 now define `pending` and `active` as independently valid checked-revision snapshots. The unobservable `active -> pending` rule is removed, validation makes no prior- or future-revision claim, and activation preparation explicitly receives the exact reviewed pending revision before deriving and recording the frozen inventory.
- `UBR-SR2-002`: E1 through E3 now use existing RigorLoop surfaces: focused `validate-boundary-first.py --check` behavior, its activation-record loader, and the diff that removes the custom candidate/publisher experiment while retaining checked-revision validation and routine release.
- User clarification: the ambiguous term `tree-local activation` is replaced by `checked-revision activation`, defined as validation from files in the current repository revision without Git history, remote state, release tags, or network access.

## Scope control

The revision adds no state-machine history, new release mode, extra checker, output-length metric, or speculative scenario catalog. It preserves the exact custom-experiment retirement inventory and the existing routine release workflow.
The formal R2 findings remain open until an independent `spec-review` rerun settles them.

## Validation

- `python scripts/validate-boundary-first.py --path specs/usability-first-boundary-release.md` — pass.
- `python scripts/test-boundary-first-validation.py` — pass, 87 tests.
- `python scripts/test-change-metadata-validator.py` — pass, 61 tests.

## Handoff

After final authoring validation, the specification returns to `review-required` for independent `spec-review` R3.
No review approval, architecture readiness, implementation readiness, release readiness, or publication claim is made here.
