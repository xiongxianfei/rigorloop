# Behavior Preservation

## Status

- active

## Change

This record covers M1 of the independent `test-spec-review` gate change: workflow and contract baseline.

## Preservation matrix

| Surface | Baseline | M1 proof | Result |
| --- | --- | --- | --- |
| Test-spec authoring | Produces an active proof map before implementation. | `specs/rigorloop-workflow.md` keeps test-spec settlement state `active` and routes formal workflow-managed test specs to `test-spec-review`. | preserved |
| Plan-review | Approves plan readiness before test-spec authoring. | `docs/workflows.md` keeps `plan-review` as the immediate handoff into `test-spec`. | preserved |
| Implement | Consumes the active test spec. | M1 adds an approved, current `test-spec-review` precondition before formal implementation eligibility. | strengthened |
| Code-review | Reviews implemented code and tests after implementation. | Stage order keeps `code-review` after `implement`; no M1 text weakens code-review ownership. | preserved |
| Verify | Confirms final evidence and branch readiness after explanation. | Stage order keeps `verify` after `explain-change`; `test-spec-review` does not claim validation success or branch readiness. | preserved |
| Test-spec state | `active`. | Artifact lifecycle table keeps `active` and stores approval in review evidence. | preserved |
| Review evidence | Repository-defined test-spec review surface. | `test-spec-review` becomes a formal review stage with result-field validation. | strengthened |
| Generated adapters | No dedicated test-spec-review skill in M1. | Adapter package work remains deferred to M3; M1 changes only the contract baseline. | preserved |

## Validation evidence

- `python scripts/test-review-artifact-validator.py`: pass.
- `python scripts/test-skill-validator.py -k implementation_through_verify_behavior_preservation_covers_acceptance_and_itv_checks`: pass.
- `python scripts/test-skill-validator.py -k test_test_spec_review_gate_workflow_baseline_surfaces_are_declared`: pass.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-25-independent-test-spec-review-gate`: pass.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-25-independent-test-spec-review-gate/change.yaml`: pass.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`: pass.
- `git diff --check -- AGENTS.md docs/workflows.md specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md scripts/review_artifact_validation.py scripts/test-review-artifact-validator.py scripts/test-skill-validator.py docs/changes/2026-06-25-independent-test-spec-review-gate/change.yaml`: pass.

## Open items

M2 must add the canonical `test-spec-review` skill and review assets. M3 must add the remaining lifecycle, fixture, stale-review, and generated package proof.
