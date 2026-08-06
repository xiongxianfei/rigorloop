# Spec Revision Evidence R2: Usability-First Boundary-First v0.4.0 Release

Stage: spec
Revision: 2
Date: 2026-08-06
Artifact ID: spec
Spec: `specs/usability-first-boundary-release.md`
Review basis: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/spec-review-r1.md`

## Revision result

- `UBR-SR1-001`: UBR-R006 and UBR-R007 now define the complete declarative pending/active tuple, one-time baseline-derived frozen inventory, local validation rules, illegal states, and exact standing proof-model dispositions without tag, network, transition-parent, or publication-history proof.
- `UBR-SR1-002`: E1 through E3 now provide concrete specification, inspection, and code-review fixtures with required inclusions and named unrelated exclusions; AC-UBR-001 and AC-UBR-002 provide semantic oracles without prose-length checks.
- `UBR-SR1-003`: UBR-R013 now owns a closed eight-surface cleanup table. It deletes the three unpublished custom helpers and removes only candidate/publication behavior from five retained validator, CLI, test, and selector surfaces.
- User clarification: UBR-R012, UBR-R013, INT-003, EC10, and AC-UBR-007 explicitly preserve the original routine release steps. Tree-local activation does not retire, replace, or bypass preparation, preflight, full verification, trusted tag publication, public smoke, or closeout.

## Scope control

The revision adds no new release mode, compatibility shim, Git transaction, public action, boundary dimension, or global scenario-count rule.
The formal review findings and dispositions remain open until an independent `spec-review` rerun settles them.

## Validation

- `python scripts/validate-boundary-first.py --path specs/usability-first-boundary-release.md` — pass.
- `python scripts/test-boundary-first-validation.py` — pass, 87 tests.
- `python scripts/test-change-metadata-validator.py` — pass, 61 tests.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-06-usability-first-boundary-release/change.yaml` — pass.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-06-usability-first-boundary-release` — pass, two reviews and three recorded findings.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/usability-first-boundary-release.md --path docs/changes/2026-08-06-usability-first-boundary-release/change.yaml --path docs/changes/2026-08-06-usability-first-boundary-release/evidence/spec-authoring-r2.md --path docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md` — pass with intentional merge-language warnings inherited from the explicit maintainer-owned publication boundary.
- `git diff --check` — pass.

## Handoff

After final authoring validation, the specification returns to `review-required` for independent `spec-review` R2.
No review approval, architecture readiness, implementation readiness, release readiness, or publication claim is made here.
