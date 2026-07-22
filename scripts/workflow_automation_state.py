#!/usr/bin/env python3
"""Sole durable-state writer for unified workflow automation.

The module owns complete-file atomic replacement of
``change.yaml#workflow.automation``.  It does not select stages or invoke skills;
callers must persist a prepared receipt here before performing stage mutation.
"""

from __future__ import annotations

import copy
import fcntl
import hashlib
import importlib.util
import json
import math
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from validate_workflow_automation import (
    has_read_only_legacy_migration,
    validate_workflow_automation,
)


ROOT = Path(__file__).resolve().parents[1]
METADATA_VALIDATOR = ROOT / "scripts" / "validate-change-metadata.py"
TERMINAL_LEGACY_STATES = frozenset(
    {"cancelled", "completed", "complete", "off", "inactive", "stopped"}
)
RETRY_POLICIES = frozenset(
    {"idempotent-retry", "reconcile-only", "manual-recovery"}
)
RECEIPT_TERMINAL_STATUSES = frozenset(
    {"completed", "failed", "paused", "cancelled"}
)
_PLAIN_STRING_RESERVED = frozenset({"true", "false", "null", "[]", "{}"})
_NUMBER_RE = re.compile(
    r"-?(?:[0-9]+|[0-9]+\.[0-9]+|[0-9]+[eE][+-]?[0-9]+|[0-9]+\.[0-9]+[eE][+-]?[0-9]+)"
)


class StateContractError(RuntimeError):
    """Raised before mutation when workflow-automation state is unsafe."""


class ConcurrentStateChange(StateContractError):
    """Raised when the canonical file changes during a state transaction."""


@dataclass(frozen=True)
class StateSnapshot:
    document: dict[str, Any]
    automation: dict[str, Any] | None
    document_identity: str


@dataclass(frozen=True)
class StateMutationResult:
    status: str
    mutated: bool
    document_identity: str


@dataclass(frozen=True)
class RecoveryDecision:
    action: str
    invoke_stage: bool
    reason: str


def _load_metadata_parser() -> Any:
    spec = importlib.util.spec_from_file_location(
        "change_metadata_validator_for_automation_state", METADATA_VALIDATOR
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load change metadata parser")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _identity(payload: bytes) -> str:
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


def _structured_identity(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return _identity(payload)


def compute_transition_key(receipt: dict[str, Any]) -> str:
    """Compute the stable transition identity from immutable operation inputs."""

    return _structured_identity(
        {
            "policy_version": receipt.get("policy_version"),
            "run_id": receipt.get("run_id"),
            "change_id": receipt.get("change_id"),
            "from_position": receipt.get("from_position"),
            "target": receipt.get("target"),
            "effective_capability_id": receipt.get("effective_capability_id"),
            "input_identities": receipt.get("input_identities"),
            "expected_postcondition": receipt.get("expected_postcondition"),
        }
    )


def _yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise StateContractError("non-finite numbers cannot be persisted")
        return repr(value)
    if not isinstance(value, str):
        raise StateContractError(f"unsupported YAML scalar type: {type(value).__name__}")
    if (
        not value
        or value.strip() != value
        or value in _PLAIN_STRING_RESERVED
        or _NUMBER_RE.fullmatch(value)
        or value.startswith(("#", "- ", "'", '"'))
        or value.endswith(("'", '"'))
    ):
        return json.dumps(value, ensure_ascii=False)
    return value


def _dump_yaml_lines(value: Any, indent: int) -> list[str]:
    prefix = " " * indent
    if isinstance(value, dict):
        lines: list[str] = []
        for key, child in value.items():
            if not isinstance(key, str) or not key or ":" in key or "\n" in key:
                raise StateContractError(f"unsupported YAML mapping key: {key!r}")
            if isinstance(child, dict):
                if child:
                    lines.append(f"{prefix}{key}:")
                    lines.extend(_dump_yaml_lines(child, indent + 2))
                else:
                    lines.append(f"{prefix}{key}: {{}}")
            elif isinstance(child, list):
                if child:
                    lines.append(f"{prefix}{key}:")
                    lines.extend(_dump_yaml_lines(child, indent + 2))
                else:
                    lines.append(f"{prefix}{key}: []")
            else:
                lines.append(f"{prefix}{key}: {_yaml_scalar(child)}")
        return lines
    if isinstance(value, list):
        lines = []
        for child in value:
            if isinstance(child, dict):
                if not child:
                    lines.append(f"{prefix}- {{}}")
                    continue
                lines.append(f"{prefix}-")
                lines.extend(_dump_yaml_lines(child, indent + 2))
            elif isinstance(child, list):
                lines.append(f"{prefix}-")
                lines.extend(_dump_yaml_lines(child, indent + 2))
            else:
                lines.append(f"{prefix}- {_yaml_scalar(child)}")
        return lines
    raise StateContractError("YAML document root must be an object or array")


def dump_yaml(document: dict[str, Any]) -> str:
    """Serialize the repository's deliberately small change-metadata subset."""

    return "\n".join(_dump_yaml_lines(document, 0)) + "\n"


def _active_prepared_receipts(automation: dict[str, Any]) -> list[dict[str, Any]]:
    receipts = automation.get("transition_receipts")
    if not isinstance(receipts, dict):
        return []
    return [
        receipt
        for receipt in receipts.values()
        if isinstance(receipt, dict) and receipt.get("status") == "prepared"
    ]


def evaluate_receipt_recovery(
    automation: dict[str, Any],
    receipt: dict[str, Any],
    *,
    completion_evidence: dict[str, Any] | None,
) -> RecoveryDecision:
    """Return the only safe action for one durable transition receipt."""

    prepared = _active_prepared_receipts(automation)
    if len(prepared) > 1:
        return RecoveryDecision("fail-closed", False, "multiple-in-flight-transitions")
    status = receipt.get("status")
    if status == "completed":
        if completion_evidence is None:
            return RecoveryDecision("pause", False, "completed-evidence-unavailable")
        if completion_evidence.get("outputs") != receipt.get("outputs"):
            return RecoveryDecision("pause", False, "completed-output-identity-drift")
        if completion_evidence.get("canonical_sync") != receipt.get("canonical_sync"):
            return RecoveryDecision("pause", False, "completed-canonical-state-drift")
        return RecoveryDecision("continue", False, "completed-evidence-current")
    if status != "prepared":
        return RecoveryDecision("fail-closed", False, "unknown-or-nonrecoverable-receipt")

    capability_id = receipt.get("effective_capability_id")
    capabilities = automation.get("effective_capabilities")
    capability = capabilities.get(capability_id) if isinstance(capabilities, dict) else None
    if not isinstance(capability, dict) or capability.get("status") != "active":
        return RecoveryDecision("pause", False, "effective-capability-not-active")

    retry_policy = receipt.get("retry_policy")
    if retry_policy not in RETRY_POLICIES:
        return RecoveryDecision("fail-closed", False, "unknown-retry-policy")
    if completion_evidence is None:
        if retry_policy == "idempotent-retry":
            return RecoveryDecision("retry", True, "no-completion-evidence")
        if retry_policy == "manual-recovery":
            return RecoveryDecision("manual-recovery", False, "manual-recovery-required")
        return RecoveryDecision("pause", False, "reconciliation-evidence-required")
    if completion_evidence.get("partial") is True:
        return RecoveryDecision("fail-closed", False, "partial-output")
    if completion_evidence.get("input_identities") != receipt.get("input_identities"):
        return RecoveryDecision("pause", False, "input-identity-drift")
    if completion_evidence.get("expected_postcondition") != receipt.get(
        "expected_postcondition"
    ):
        return RecoveryDecision("pause", False, "postcondition-drift")
    outputs = completion_evidence.get("outputs")
    if not isinstance(outputs, list) or not outputs:
        return RecoveryDecision("fail-closed", False, "incomplete-completion-evidence")
    canonical_sync = completion_evidence.get("canonical_sync")
    if not isinstance(canonical_sync, dict) or canonical_sync.get("status") != "synchronized":
        return RecoveryDecision("pause", False, "canonical-state-not-synchronized")
    return RecoveryDecision("reconcile-completed", False, "completion-evidence-valid")


def project_automation_status(automation: dict[str, Any]) -> dict[str, Any]:
    """Project bounded read-only status without manufacturing workflow state."""

    state = copy.deepcopy(automation)
    run = state.get("run") if isinstance(state.get("run"), dict) else {}
    parents = state.get("parent_authorizations")
    capabilities = state.get("effective_capabilities")
    active_parents = [
        value.get("authorization_class")
        for value in parents.values()
        if isinstance(parents, dict)
        and isinstance(value, dict)
        and value.get("status") == "active"
    ] if isinstance(parents, dict) else []
    active_capabilities = [
        value.get("capability_kind")
        for value in capabilities.values()
        if isinstance(capabilities, dict)
        and isinstance(value, dict)
        and value.get("status") == "active"
    ] if isinstance(capabilities, dict) else []
    prepared = _active_prepared_receipts(state)
    return {
        "source": "unified",
        "mechanism": state.get("mechanism"),
        "run_id": run.get("run_id"),
        "run_status": run.get("status"),
        "target": copy.deepcopy(run.get("target")),
        "authorization_boundary": active_parents[0] if len(active_parents) == 1 else active_parents,
        "effective_capability_kind": (
            active_capabilities[0] if len(active_capabilities) == 1 else active_capabilities
        ),
        "canonical_position_source": state.get("canonical_position_source"),
        "in_flight_transition": (
            prepared[0].get("transition_id") if len(prepared) == 1 else None
        ),
        "stop_reason": run.get("stop_reason"),
        "latest_evidence_identities": copy.deepcopy(state.get("observed_identities", {})),
        "latest_review_result": copy.deepcopy(state.get("latest_review_result")),
    }


class WorkflowAutomationStateStore:
    """Read and atomically replace the one canonical automation subsection."""

    def __init__(self, metadata_path: Path):
        self.metadata_path = metadata_path

    def read(self) -> StateSnapshot:
        payload = self.metadata_path.read_bytes()
        parser = _load_metadata_parser()
        lines = parser.tokenize_yaml(payload.decode("utf-8"))
        if not lines:
            raise StateContractError("change metadata file is empty")
        document, index = parser.parse_yaml_block(lines, 0, lines[0].indent)
        if index != len(lines):
            raise StateContractError("change metadata contains trailing content")
        if not isinstance(document, dict):
            raise StateContractError("change metadata root must be an object")
        workflow = document.get("workflow")
        automation = workflow.get("automation") if isinstance(workflow, dict) else None
        if automation is not None:
            errors = validate_workflow_automation(
                automation, top_level_change_id=document.get("change_id")
            )
            if errors:
                raise StateContractError("invalid workflow.automation: " + "; ".join(errors))
            legacy = workflow.get("autoprogression")
            if legacy is not None:
                if not has_read_only_legacy_migration(automation):
                    raise StateContractError("mixed writable legacy and unified state")
                binding_errors = parser.validate_legacy_migration_binding(
                    automation, legacy
                )
                if binding_errors:
                    raise StateContractError(
                        "invalid legacy migration binding: " + "; ".join(binding_errors)
                    )
        return StateSnapshot(document, automation, _identity(payload))

    def replace_automation(
        self,
        automation: dict[str, Any],
        *,
        expected_document_identity: str,
        before_replace: Callable[[Path], None] | None = None,
    ) -> StateMutationResult:
        snapshot = self.read()
        if snapshot.document_identity != expected_document_identity:
            raise ConcurrentStateChange("change metadata identity changed before transaction")
        errors = validate_workflow_automation(
            automation, top_level_change_id=snapshot.document.get("change_id")
        )
        if errors:
            raise StateContractError("invalid replacement automation state: " + "; ".join(errors))
        document = copy.deepcopy(snapshot.document)
        workflow = document.setdefault("workflow", {})
        if not isinstance(workflow, dict):
            raise StateContractError("workflow must be an object")
        workflow["automation"] = copy.deepcopy(automation)
        payload = dump_yaml(document).encode("utf-8")

        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{self.metadata_path.name}.",
            suffix=".tmp",
            dir=self.metadata_path.parent,
        )
        temporary_path = Path(temporary_name)
        try:
            os.fchmod(descriptor, self.metadata_path.stat().st_mode & 0o7777)
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            if before_replace is not None:
                before_replace(temporary_path)
            directory_fd = os.open(self.metadata_path.parent, os.O_RDONLY)
            try:
                fcntl.flock(directory_fd, fcntl.LOCK_EX)
                if _identity(self.metadata_path.read_bytes()) != expected_document_identity:
                    raise ConcurrentStateChange("change metadata identity changed during transaction")
                os.replace(temporary_path, self.metadata_path)
                os.fsync(directory_fd)
            finally:
                fcntl.flock(directory_fd, fcntl.LOCK_UN)
                os.close(directory_fd)
        finally:
            temporary_path.unlink(missing_ok=True)
        return StateMutationResult("updated", True, _identity(payload))

    def prepare_transition(
        self,
        receipt: dict[str, Any],
        *,
        expected_document_identity: str,
    ) -> StateMutationResult:
        snapshot = self.read()
        if snapshot.automation is None:
            raise StateContractError("unified automation state does not exist")
        if _active_prepared_receipts(snapshot.automation):
            raise StateContractError("only one transition may be in flight for a change")
        if receipt.get("status") != "prepared":
            raise StateContractError("new transition receipt must have status prepared")
        if receipt.get("transition_key") != compute_transition_key(receipt):
            raise StateContractError("transition key does not match immutable operation inputs")
        capabilities = snapshot.automation.get("effective_capabilities")
        capability = (
            capabilities.get(receipt.get("effective_capability_id"))
            if isinstance(capabilities, dict)
            else None
        )
        if not isinstance(capability, dict) or capability.get("status") != "active":
            raise StateContractError("effective capability must be active before preparation")
        replacement = copy.deepcopy(snapshot.automation)
        receipts = replacement.get("transition_receipts")
        if not isinstance(receipts, dict):
            raise StateContractError("transition receipts must be an object")
        transition_id = receipt.get("transition_id")
        if not isinstance(transition_id, str) or not transition_id:
            raise StateContractError("transition receipt requires a stable transition ID")
        if transition_id in receipts:
            raise StateContractError("transition ID already exists")
        receipts[transition_id] = copy.deepcopy(receipt)
        result = self.replace_automation(
            replacement, expected_document_identity=expected_document_identity
        )
        return StateMutationResult("prepared", True, result.document_identity)

    def finalize_transition(
        self,
        transition_id: str,
        *,
        status: str,
        outputs: list[Any],
        canonical_sync_status: str,
        expected_document_identity: str,
    ) -> StateMutationResult:
        if status not in RECEIPT_TERMINAL_STATUSES:
            raise StateContractError(f"invalid terminal receipt status: {status}")
        snapshot = self.read()
        if snapshot.automation is None:
            raise StateContractError("unified automation state does not exist")
        replacement = copy.deepcopy(snapshot.automation)
        receipts = replacement.get("transition_receipts")
        receipt = receipts.get(transition_id) if isinstance(receipts, dict) else None
        if not isinstance(receipt, dict) or receipt.get("status") != "prepared":
            raise StateContractError("transition is not prepared")
        receipt["status"] = status
        receipt["outputs"] = copy.deepcopy(outputs)
        receipt["canonical_sync"] = {"status": canonical_sync_status}
        if status == "completed":
            capabilities = replacement.get("effective_capabilities")
            capability = (
                capabilities.get(receipt.get("effective_capability_id"))
                if isinstance(capabilities, dict)
                else None
            )
            if not isinstance(capability, dict) or capability.get("status") != "active":
                raise StateContractError("completed transition requires its active capability")
            capability["status"] = "consumed"
        result = self.replace_automation(
            replacement, expected_document_identity=expected_document_identity
        )
        return StateMutationResult(status, True, result.document_identity)

    def cancel(
        self,
        *,
        cancelled_by: str,
        cancelled_at: str,
        expected_document_identity: str | None = None,
        completion_evidence: dict[str, Any] | None = None,
    ) -> StateMutationResult:
        snapshot = self.read()
        if snapshot.automation is None:
            return StateMutationResult("no-active-run", False, snapshot.document_identity)
        run = snapshot.automation.get("run")
        if not isinstance(run, dict):
            raise StateContractError("automation run must be an object")
        if run.get("status") == "cancelled":
            return StateMutationResult("cancelled", False, snapshot.document_identity)
        if run.get("status") == "completed":
            return StateMutationResult("already-completed", False, snapshot.document_identity)
        prepared = _active_prepared_receipts(snapshot.automation)
        if len(prepared) > 1:
            raise StateContractError("multiple in-flight transitions fail closed")
        if prepared:
            decision = evaluate_receipt_recovery(
                snapshot.automation,
                prepared[0],
                completion_evidence=completion_evidence,
            )
            if decision.action != "reconcile-completed":
                return StateMutationResult(
                    "reconciliation-required", False, snapshot.document_identity
                )

        replacement = copy.deepcopy(snapshot.automation)
        if prepared:
            if completion_evidence is None:
                raise StateContractError("completion evidence disappeared during reconciliation")
            transition_id = prepared[0]["transition_id"]
            receipt = replacement["transition_receipts"][transition_id]
            receipt["status"] = "completed"
            receipt["outputs"] = copy.deepcopy(completion_evidence["outputs"])
            receipt["canonical_sync"] = copy.deepcopy(
                completion_evidence["canonical_sync"]
            )
            capability = replacement["effective_capabilities"][
                receipt["effective_capability_id"]
            ]
            capability["status"] = "consumed"
        replacement["run"]["status"] = "cancelled"
        replacement["run"]["stop_reason"] = "run-cancelled"
        replacement["cancellation"] = {
            "cancelled_by": cancelled_by,
            "cancelled_at": cancelled_at,
            "reason": "run-cancelled",
        }
        for parent in replacement["parent_authorizations"].values():
            if isinstance(parent, dict) and parent.get("status") == "active":
                parent["status"] = "revoked"
                parent["revocation"] = {
                    "revoked": True,
                    "revoked_by": cancelled_by,
                    "revoked_at": cancelled_at,
                    "reason": "run-cancelled",
                }
        for capability in replacement["effective_capabilities"].values():
            if isinstance(capability, dict) and capability.get("status") == "active":
                capability["status"] = "invalidated"
                capability["invalidation_reason"] = "parent-revoked"
        expected = expected_document_identity or snapshot.document_identity
        result = self.replace_automation(replacement, expected_document_identity=expected)
        return StateMutationResult("cancelled", True, result.document_identity)

    def status(self) -> dict[str, Any]:
        snapshot = self.read()
        if snapshot.automation is not None:
            return project_automation_status(snapshot.automation)
        workflow = snapshot.document.get("workflow")
        legacy = workflow.get("autoprogression") if isinstance(workflow, dict) else None
        if not isinstance(legacy, dict):
            return {"source": "none", "run_status": "no-active-run"}
        return {
            "source": "legacy-read-only",
            "legacy": copy.deepcopy(legacy),
            "source_record_identity": _structured_identity(legacy),
        }

    def migrate_legacy(
        self,
        automation: dict[str, Any],
        *,
        migrated_at: str,
        expected_document_identity: str | None = None,
    ) -> StateMutationResult:
        snapshot = self.read()
        workflow = snapshot.document.get("workflow")
        legacy = workflow.get("autoprogression") if isinstance(workflow, dict) else None
        if snapshot.automation is not None:
            migrations = snapshot.automation.get("migration_receipts")
            if isinstance(migrations, dict) and migrations:
                return StateMutationResult(
                    "already-migrated", False, snapshot.document_identity
                )
            if legacy is not None:
                raise StateContractError("mixed writable legacy and unified state")
            raise StateContractError("unified automation state already exists")
        if not isinstance(legacy, dict):
            raise StateContractError("active legacy automation state does not exist")
        mechanism, record = self._select_legacy_record(legacy)
        state = record.get("state", record.get("status"))
        if mechanism == "off" or state in TERMINAL_LEGACY_STATES:
            raise StateContractError("terminal legacy state is read-only and cannot migrate")
        source_identity = _structured_identity(record)
        migration_id = f"migration-{source_identity.split(':', 1)[1][:16]}"
        replacement = copy.deepcopy(automation)
        replacement["migration_receipts"] = {
            migration_id: {
                "migration_id": migration_id,
                "source_mechanism": mechanism,
                "source_record_identity": source_identity,
                "migrated_at": migrated_at,
                "unified_run_id": replacement.get("run", {}).get("run_id"),
                "projection_result": "equivalent",
                "legacy_read_only": True,
            }
        }
        expected = expected_document_identity or snapshot.document_identity
        result = self.replace_automation(replacement, expected_document_identity=expected)
        return StateMutationResult("migrated", True, result.document_identity)

    @staticmethod
    def _select_legacy_record(legacy: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        if isinstance(legacy.get("profile"), str):
            return legacy["profile"], legacy
        candidates = [
            (name.replace("_", "-"), record)
            for name in (
                "authoring_through_plan_review",
                "implementation_through_verify",
                "review_fix",
            )
            if isinstance((record := legacy.get(name)), dict)
            and record.get("state", record.get("status")) not in TERMINAL_LEGACY_STATES
        ]
        if len(candidates) != 1:
            raise StateContractError(
                "legacy migration requires exactly one active source record"
            )
        key_mechanism, record = candidates[0]
        mechanism = record.get("profile") or record.get("mechanism") or key_mechanism
        return mechanism, record


__all__ = [
    "ConcurrentStateChange",
    "RecoveryDecision",
    "StateContractError",
    "StateMutationResult",
    "StateSnapshot",
    "WorkflowAutomationStateStore",
    "compute_transition_key",
    "dump_yaml",
    "evaluate_receipt_recovery",
    "project_automation_status",
]
