"""Schema and invariant checks for a validation retirement ledger.

This is deliberately a library owned by the existing validation system, not a
new contributor-facing validator command.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

import yaml


STATES = frozenset({"inventoried", "dual-proof", "removable", "retired", "paused"})
DISPOSITIONS = frozenset(
    {"retained", "replacement-planned", "optional-analysis", "de-contracted", "blocked-active-contract"}
)
OWNERS = frozenset({"gate-a", "gate-b", "gate-c", "governance", "semantic-review", "product"})
REQUIRED_ENTRY_FIELDS = frozenset(
    {
        "id", "check_ids", "scripts", "protected_failure", "owner",
        "deterministic_automation", "existing_owner_decision", "invocation",
        "actionable_repair", "fixture_inventory", "governing_clauses",
        "contract_disposition", "state", "replacement_proof", "retirement_evidence",
        "rollback", "retirement_decision",
    }
)
R26_EXACT = frozenset(
    {
        "R35", "R35a", "R35b", "R35e", "R35f", "R35g", "R36i", "R36j",
        "R43d", "R44a", "R44e", "R45", "R45a", "R45b", "R45c", "R45d",
        "R52", "R52a", "R52b", "R55a:installed-target-tree", "R59b",
    }
)


def load_ledger(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: ledger root must be a mapping")
    return value


def _present(value: Any) -> bool:
    return value not in (None, "", [], {})


def validate_ledger(
    ledger: dict[str, Any], *, expected_check_ids: set[str] | None = None
) -> list[str]:
    errors: list[str] = []
    if ledger.get("schema_version") != 1:
        errors.append("schema_version: expected closed value 1")
    entries = ledger.get("entries")
    if not isinstance(entries, list) or not entries:
        return errors + ["entries: expected a non-empty list"]

    all_check_ids: list[str] = []
    seen_entry_ids: set[str] = set()
    for index, entry in enumerate(entries):
        label = f"entries[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{label}: expected mapping")
            continue
        entry_id = entry.get("id")
        if entry_id in seen_entry_ids:
            errors.append(f"{label}.id: duplicate {entry_id!r}")
        if isinstance(entry_id, str):
            seen_entry_ids.add(entry_id)
            label = entry_id
        for field in sorted(REQUIRED_ENTRY_FIELDS):
            if field not in entry or not _present(entry[field]):
                errors.append(f"{label}.{field}: required")
        state = entry.get("state")
        if state not in STATES:
            errors.append(f"{label}.state: unknown state {state!r}; allowed={sorted(STATES)}")
        disposition = entry.get("contract_disposition")
        if disposition not in DISPOSITIONS:
            errors.append(
                f"{label}.contract_disposition: unknown contract_disposition {disposition!r}; "
                f"allowed={sorted(DISPOSITIONS)}"
            )
        owner = entry.get("owner")
        if owner not in OWNERS:
            errors.append(f"{label}.owner: unknown owner {owner!r}; allowed={sorted(OWNERS)}")
        check_ids = entry.get("check_ids")
        if not isinstance(check_ids, list) or not check_ids:
            errors.append(f"{label}.check_ids: expected a non-empty list")
        else:
            all_check_ids.extend(value for value in check_ids if isinstance(value, str))
        fixtures = entry.get("fixture_inventory", [])
        if state in {"removable", "retired"} and "unknown" in fixtures:
            errors.append(f"{label}.fixture_inventory: unknown fixture behavior blocks removal")
        if state in {"removable", "retired"}:
            for field in ("replacement_proof", "retirement_evidence", "rollback"):
                if entry.get(field) in (None, "", "none", [], {}):
                    errors.append(f"{label}.{field}: complete proof is required for {state}")
            if disposition == "blocked-active-contract":
                errors.append(f"{label}: contradictory clause disposition blocks removal")

    duplicates = sorted(check_id for check_id, count in Counter(all_check_ids).items() if count > 1)
    if duplicates:
        errors.append(f"check_ids: owned more than once: {duplicates}")
    if expected_check_ids is not None:
        missing = sorted(expected_check_ids - set(all_check_ids))
        unknown = sorted(set(all_check_ids) - expected_check_ids)
        if missing:
            errors.append(f"check_ids: missing catalog entries: {missing}")
        if unknown:
            errors.append(f"check_ids: unknown catalog entries: {unknown}")

    if set(ledger.get("r26_disposition", {})) != R26_EXACT:
        errors.append("r26_disposition: clause set does not exactly match primary spec R26")
    if ledger.get("retained_clauses") != ["R35c", "R35d"]:
        errors.append("retained_clauses: R35c and R35d must remain active")
    parity = set(ledger.get("retained_deterministic_parity", []))
    if not {"R50a", "R50b"}.issubset(parity):
        errors.append("retained_deterministic_parity: R50a and R50b are required")
    return errors
