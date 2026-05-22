# Behavior Preservation

## Scope

Milestone M1 replaces the selector's hardcoded recurring change-local evidence filename allowlist with a selector-owned evidence class registry. Milestone M3 adds a bounded query helper for common change-record reads. The intended behavior changes are structural: registered evidence files now route by evidence class, and common reads can use bounded query outputs instead of full metadata history. Existing routed evidence still selects lifecycle validation, and full forensic reads remain available through detail pointers.

## Preservation Matrix

| Surface | Baseline proof | New proof | Preservation result |
| --- | --- | --- | --- |
| Existing registered evidence routes | Existing representative selector fixture expected `artifact_lifecycle.validate` for change-local evidence names. | `python scripts/test-select-validation.py` passes with registered evidence categories and the same lifecycle check coverage. | Preserved selected validation behavior; category names now reflect registry ownership. |
| New evidence pattern routing | `behavior-preservation.md` was previously an exact hardcoded lifecycle evidence name. | `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/behavior-preservation.md` routes as `registered-change-evidence` via preservation evidence class. | Improved: routed through registered pattern/class rather than one-off filename logic. |
| Validation command selection | Existing route selected `artifact_lifecycle.validate` for recurring evidence names. | Registered evidence route selects `artifact_lifecycle.validate` for the evidence file and governing `change.yaml`. | Preserved lifecycle validation coverage. |
| Broad and ambiguous pattern safety | No registry-level broad-pattern validation existed. | `scripts/test-select-validation.py` covers broad catch-all rejection and ambiguous match rejection. | Improved safety. |
| Query helper and skill guidance | Not in Workstream A/M1. | No query helper or stage-skill guidance changes were made in M1 or M2. | Workstream separation preserved. |
| Query summary | Manual extraction from `change.yaml` required reading artifact paths, review state, latest validation evidence, blockers, and validation history context. | `python scripts/query-change-record.py 2026-05-22-change-record-catalog-registration-and-bounded-read-model summary` returns change ID, artifact paths, review state, latest validation state, blockers, and detail pointers. | Same common-read answer is available through a bounded output; full metadata remains linked by `forensic_read`. |
| Query artifacts | Manual extraction from `change.yaml.artifacts` returned canonical artifact paths. | `python scripts/query-change-record.py 2026-05-22-change-record-catalog-registration-and-bounded-read-model artifacts` returns only artifact paths, change ID, query name, and status. | Same artifact path inventory, narrowed to the artifact slice. |
| Query validation latest | Manual extraction from the legacy `validation` list required identifying the final validation entry. | `python scripts/query-change-record.py 2026-05-22-change-record-catalog-registration-and-bounded-read-model validation --latest` returns only the latest validation slice and detail pointers. | Same latest validation answer, without dumping full validation history. |
| Compact validation stage query | Manual fixture inspection required selecting one event from `validation_events`. | `scripts/test-query-change-record.py` proves `validation --stage proposal-review-r1` returns only that event and excludes unrelated stage events. | Stage-scoped read is bounded and deterministic. |
| Query helper safety | Manual reads cannot execute validation commands, but ad hoc tooling could blur query and validation behavior. | `scripts/test-query-change-record.py` proves the helper does not execute validation bundle command strings, is deterministic across repeated runs, and fails closed on unsafe paths. | Query and validation responsibilities remain separate. |

## M1 Evidence

- Registry tests added in `scripts/test-select-validation.py`.
- Registry implementation added in `scripts/validation_selection.py`.
- Focused selector test command passed: `python scripts/test-select-validation.py`.
- Explicit evidence routing command passed: `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/behavior-preservation.md`.

## M3 Evidence

- Query helper tests added in `scripts/test-query-change-record.py`.
- Query helper implementation added in `scripts/query-change-record.py`.
- Selector routing for query helper paths added in `scripts/validation_selection.py` and covered by `scripts/test-select-validation.py`.
- Focused query test command passed: `python scripts/test-query-change-record.py`.
- Active change query commands passed:
  - `python scripts/query-change-record.py 2026-05-22-change-record-catalog-registration-and-bounded-read-model summary`
  - `python scripts/query-change-record.py 2026-05-22-change-record-catalog-registration-and-bounded-read-model artifacts`
  - `python scripts/query-change-record.py 2026-05-22-change-record-catalog-registration-and-bounded-read-model validation --latest`
