# Spec Authoring Evidence: Usability-First Boundary-First v0.4.0 Release

Stage: spec
Date: 2026-08-06
Artifact ID: spec
Spec: `specs/usability-first-boundary-release.md`
Upstream proposal: `docs/proposals/2026-08-06-usability-first-boundary-release.md`
Upstream settlement: accepted; proposal-review-r1 approved; no open findings

## Authoring result

- Converted the approved usability-first direction into twenty testable requirements and twelve acceptance criteria.
- Made boundary coverage automatic for the ten governed skills while keeping default output proportional to admitted correctness risk.
- Defined representative specification, code-inspection, and code-review journeys instead of an exact-wording or fixed-length checker.
- Separated tree-local activation from immutable public release proof.
- Reused the standing routine release workflow and retained package parity, install, integrity, privacy, rollback, and public-closeout protections.
- Enumerated the cancelled spec, test spec, ADR, plan, candidate validator, publisher, tests, and selector surfaces that downstream architecture and planning must retire or re-scope.
- Classified all eight `boundary-first-v1` dimensions and selected only three material composed interactions.
- Classified post-merge wording as intentional: it separates lifecycle preparation from the explicit maintainer-owned publication action and does not make merge a lifecycle closeout trigger.

## Evidence expansion

The complete superseded activation spec and the focused routine-release contract were read because this specification changes their composition and must identify precisely which behavior remains authoritative.

## Validation

- `python scripts/test-boundary-first-validation.py` — pass, 87 tests.
- `python scripts/test-change-metadata-validator.py` — pass, 61 tests.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-06-usability-first-boundary-release/change.yaml` — pass.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/usability-first-boundary-release.md --path docs/changes/2026-08-06-usability-first-boundary-release/change.yaml --path docs/changes/2026-08-06-usability-first-boundary-release/evidence/spec-authoring.md` — pass with intentional merge-language warnings described above.
- `python scripts/validate-boundary-first.py --check` — pass.
- `git diff --check` — pass.

## Handoff

The specification is complete and the `spec` artifact entry is `review-required`.
No spec-review approval, architecture readiness, implementation readiness, release readiness, or publication claim is made here.
