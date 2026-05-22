# M1 Behavior Preservation

## Scope

Milestone M1 replaces the selector's hardcoded recurring change-local evidence filename allowlist with a selector-owned evidence class registry. The intended behavior change is structural: registered evidence files now route by evidence class. Existing routed evidence still selects lifecycle validation.

## Preservation Matrix

| Surface | Baseline proof | New proof | Preservation result |
| --- | --- | --- | --- |
| Existing registered evidence routes | Existing representative selector fixture expected `artifact_lifecycle.validate` for change-local evidence names. | `python scripts/test-select-validation.py` passes with registered evidence categories and the same lifecycle check coverage. | Preserved selected validation behavior; category names now reflect registry ownership. |
| New evidence pattern routing | `behavior-preservation.md` was previously an exact hardcoded lifecycle evidence name. | `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/behavior-preservation.md` routes as `registered-change-evidence` via preservation evidence class. | Improved: routed through registered pattern/class rather than one-off filename logic. |
| Validation command selection | Existing route selected `artifact_lifecycle.validate` for recurring evidence names. | Registered evidence route selects `artifact_lifecycle.validate` for the evidence file and governing `change.yaml`. | Preserved lifecycle validation coverage. |
| Broad and ambiguous pattern safety | No registry-level broad-pattern validation existed. | `scripts/test-select-validation.py` covers broad catch-all rejection and ambiguous match rejection. | Improved safety. |
| Query helper and skill guidance | Not in Workstream A/M1. | No query helper or stage-skill guidance changes were made in M1. | Workstream separation preserved. |

## M1 Evidence

- Registry tests added in `scripts/test-select-validation.py`.
- Registry implementation added in `scripts/validation_selection.py`.
- Focused selector test command passed: `python scripts/test-select-validation.py`.
- Explicit evidence routing command passed: `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/behavior-preservation.md`.
