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

from review_artifact_validation import (
    parse_formal_review_log,
    parse_formal_review_record,
)
from artifact_lifecycle_validation import inspect_lifecycle_artifact
from lifecycle_state_sync import parse_handoff_summary
from workflow_automation_policy import STAGE_POLICY_BY_STAGE
from validate_workflow_automation import (
    compute_transition_key,
    has_read_only_legacy_migration,
    validate_workflow_automation,
)


ROOT = Path(__file__).resolve().parents[1]
METADATA_VALIDATOR = ROOT / "scripts" / "validate-change-metadata.py"
TERMINAL_LEGACY_STATES = frozenset(
    {"cancelled", "completed", "complete", "off", "inactive", "stopped"}
)
RECEIPT_TERMINAL_STATUSES = frozenset(
    {"completed", "failed", "paused", "cancelled"}
)
PROPOSAL_REVIEW_OUTCOMES = frozenset(
    {"approved", "changes-requested", "blocked", "inconclusive"}
)
FORMAL_REVIEW_INPUT_IDENTITIES = {
    "proposal-review": "proposal",
    "spec-review": "spec",
    "architecture-review": "architecture",
    "plan-review": "plan",
    "test-spec-review": "test-spec",
}
LIFECYCLE_STAGE_CLASSES = {
    "proposal": "proposal",
    "spec": "spec",
    "architecture": "architecture",
    "test-spec": "test-spec",
}
STAGE_NATIVE_VERIFIER_STAGES = frozenset(
    set(FORMAL_REVIEW_INPUT_IDENTITIES)
    | set(LIFECYCLE_STAGE_CLASSES)
    | {"architecture-assessment", "plan"}
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
    verified_completion: "VerifiedCompletion | None" = None


@dataclass(frozen=True)
class CompletionVerification:
    valid: bool
    reason: str
    proof: "VerifiedCompletion | None" = None


@dataclass(frozen=True)
class VerifiedCompletion:
    """Engine-derived completion proof safe for durable persistence."""

    outputs: tuple[dict[str, str], ...]
    canonical_evidence: dict[str, Any]
    observed_identities: dict[str, str]
    stage_facts: dict[str, str]


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


def _strip_code(value: str) -> str:
    normalized = value.strip()
    if len(normalized) >= 2 and normalized.startswith("`") and normalized.endswith("`"):
        return normalized[1:-1].strip()
    return normalized


def _resolve_repository_file(
    relative: Path,
    *,
    repository_root: Path,
) -> Path | None:
    """Resolve one repository-owned regular file without following symlinks."""

    if relative.is_absolute() or ".." in relative.parts or not relative.parts:
        return None
    root = repository_root.resolve()
    candidate = root
    for part in relative.parts:
        candidate = candidate / part
        if candidate.is_symlink():
            return None
    try:
        resolved = candidate.resolve(strict=True)
    except (FileNotFoundError, OSError, RuntimeError):
        return None
    if not resolved.is_relative_to(root) or not resolved.is_file():
        return None
    return resolved


def _resolve_completion_artifact(
    evidence: Any,
    *,
    repository_root: Path,
    affected_path_roots: list[str],
) -> tuple[Path, str] | None:
    if not isinstance(evidence, dict) or set(evidence) != {"path", "identity"}:
        return None
    relative_text = evidence.get("path")
    identity = evidence.get("identity")
    if not isinstance(relative_text, str) or not isinstance(identity, str):
        return None
    relative = Path(relative_text)
    roots = tuple(Path(root) for root in affected_path_roots if isinstance(root, str))
    if (
        not relative_text
        or relative.is_absolute()
        or ".." in relative.parts
        or not roots
        or any(root.is_absolute() or ".." in root.parts for root in roots)
        or not any(relative == root or relative.is_relative_to(root) for root in roots)
    ):
        return None
    artifact = _resolve_repository_file(
        relative,
        repository_root=repository_root,
    )
    if artifact is None:
        return None
    observed_identity = _identity(artifact.read_bytes())
    if identity != observed_identity:
        return None
    return artifact, observed_identity


def verify_transition_completion(
    automation: dict[str, Any],
    receipt: dict[str, Any],
    *,
    completion_evidence: dict[str, Any],
    repository_root: Path,
) -> CompletionVerification:
    """Verify one stage completion from stage-native and canonical evidence."""

    capability_id = receipt.get("effective_capability_id")
    capabilities = automation.get("effective_capabilities")
    capability = capabilities.get(capability_id) if isinstance(capabilities, dict) else None
    if not isinstance(capability, dict):
        return CompletionVerification(False, "effective-capability-not-found")
    stage = capability.get("stage")
    stage_name = stage.get("name") if isinstance(stage, dict) else None
    policy = STAGE_POLICY_BY_STAGE.get(stage_name)
    if policy is None:
        return CompletionVerification(False, "unknown-capability-stage")
    inputs = completion_evidence.get("input_identities")
    if inputs != receipt.get("input_identities"):
        return CompletionVerification(False, "input-identity-drift")
    if completion_evidence.get("expected_postcondition") != receipt.get(
        "expected_postcondition"
    ):
        return CompletionVerification(False, "postcondition-drift")
    outputs = completion_evidence.get("outputs")
    canonical_sync = completion_evidence.get("canonical_sync")
    if not isinstance(outputs, list) or not outputs or not isinstance(canonical_sync, dict):
        return CompletionVerification(False, "incomplete-completion-evidence")
    if canonical_sync.get("status") != "synchronized":
        return CompletionVerification(False, "canonical-state-not-synchronized")
    sync_evidence = canonical_sync.get("evidence")
    observed_identities = canonical_sync.get("observed_identities")
    if (
        not isinstance(sync_evidence, dict)
        or set(sync_evidence) != set(policy.completion_evidence)
        or not isinstance(observed_identities, dict)
    ):
        return CompletionVerification(False, "canonical-stage-evidence-incomplete")

    scope = capability.get("scope")
    affected_roots = scope.get("affected_path_roots") if isinstance(scope, dict) else None
    if not isinstance(affected_roots, list):
        return CompletionVerification(False, "capability-evidence-scope-invalid")
    resolved_evidence: dict[str, tuple[dict[str, str], Path, str]] = {}
    for evidence_name in policy.completion_evidence:
        evidence = sync_evidence.get(evidence_name)
        resolved = _resolve_completion_artifact(
            evidence,
            repository_root=repository_root,
            affected_path_roots=affected_roots,
        )
        if resolved is None:
            return CompletionVerification(False, "stage-completion-artifact-invalid")
        artifact, artifact_identity = resolved
        if evidence not in outputs or observed_identities.get(evidence_name) != artifact_identity:
            return CompletionVerification(False, "stage-completion-identity-mismatch")
        resolved_evidence[evidence_name] = (evidence, artifact, artifact_identity)

    expected_input = FORMAL_REVIEW_INPUT_IDENTITIES.get(stage_name)
    if expected_input is None:
        artifacts = {value[1].resolve() for value in resolved_evidence.values()}
        stage_facts: dict[str, str] = {}
        if stage_name == "plan":
            if len(artifacts) != 1:
                return CompletionVerification(False, "stage-native-plan-evidence-mismatch")
            plan = next(iter(artifacts))
            handoff, handoff_errors = parse_handoff_summary(plan.read_text(encoding="utf-8"))
            if handoff is None or handoff_errors:
                return CompletionVerification(False, "stage-native-plan-invalid")
        elif stage_name == "architecture-assessment":
            assessment = next(iter(artifacts), None)
            if assessment is None:
                return CompletionVerification(False, "stage-native-assessment-invalid")
            fields: dict[str, str] = {}
            for line in assessment.read_text(encoding="utf-8").splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    fields[key.strip()] = value.strip()
            if (
                fields.get("Stage") != "architecture-assessment"
                or fields.get("Applicability") not in {"required", "not-required"}
                or fields.get("Spec identity") != inputs.get("spec")
            ):
                return CompletionVerification(False, "stage-native-assessment-invalid")
            stage_facts["architecture_applicability"] = fields["Applicability"]
        elif stage_name in LIFECYCLE_STAGE_CLASSES:
            if len(artifacts) != 1:
                return CompletionVerification(False, "stage-native-artifact-evidence-mismatch")
            inspection = inspect_lifecycle_artifact(next(iter(artifacts)), repository_root)
            if (
                inspection is None
                or inspection.contract.class_name != LIFECYCLE_STAGE_CLASSES[stage_name]
                or inspection.errors
            ):
                return CompletionVerification(False, "stage-native-artifact-invalid")
            if stage_name == "proposal" and capability.get("capability_kind") == "proposal-correction":
                previous = inputs.get("reviewed_proposal_identity")
                current = next(iter(resolved_evidence.values()))[2]
                if not isinstance(previous, str) or previous == current:
                    return CompletionVerification(False, "proposal-identity-unchanged")
        else:
            return CompletionVerification(False, "stage-native-verifier-unavailable")

        unique_outputs: dict[tuple[str, str], dict[str, str]] = {}
        normalized_evidence: dict[str, Any] = {}
        normalized_observed: dict[str, str] = {}
        for name, (evidence, _artifact, identity) in resolved_evidence.items():
            normalized_evidence[name] = copy.deepcopy(evidence)
            normalized_observed[name] = identity
            unique_outputs[(evidence["path"], identity)] = copy.deepcopy(evidence)
        return CompletionVerification(
            True,
            "stage-completion-evidence-valid",
            VerifiedCompletion(
                outputs=tuple(unique_outputs.values()),
                canonical_evidence=normalized_evidence,
                observed_identities=normalized_observed,
                stage_facts=stage_facts,
            ),
        )

    evidence_name = next(iter(policy.completion_evidence), None)
    evidence, artifact, artifact_identity = resolved_evidence[evidence_name]

    review, review_findings = parse_formal_review_record(artifact)
    if review is None or review_findings:
        return CompletionVerification(False, "stage-native-review-invalid")
    if _identity(artifact.read_bytes()) != artifact_identity:
        return CompletionVerification(False, "stage-completion-identity-drift")
    if review.stage != stage_name:
        return CompletionVerification(False, "stage-native-review-stage-mismatch")
    if review.status not in PROPOSAL_REVIEW_OUTCOMES:
        return CompletionVerification(False, "stage-native-review-outcome-invalid")

    target_text = _strip_code(review.target)
    target_relative = Path(target_text)
    target = _resolve_repository_file(
        target_relative,
        repository_root=repository_root,
    )
    expected_identity = inputs.get(expected_input) if isinstance(inputs, dict) else None
    if (
        not target_text
        or target_relative.is_absolute()
        or ".." in target_relative.parts
        or target is None
        or _identity(target.read_bytes()) != expected_identity
    ):
        return CompletionVerification(False, "reviewed-artifact-identity-mismatch")

    if artifact.parent.name != "reviews":
        return CompletionVerification(False, "formal-review-record-location-invalid")
    root = repository_root.resolve()
    change_root = artifact.parent.parent
    review_log = change_root / "review-log.md"
    if not review_log.exists() and not review_log.is_symlink():
        return CompletionVerification(False, "canonical-review-log-missing")
    try:
        review_log_relative = review_log.relative_to(root)
    except ValueError:
        return CompletionVerification(False, "canonical-review-log-path-invalid")
    resolved_review_log = _resolve_repository_file(
        review_log_relative,
        repository_root=repository_root,
    )
    if resolved_review_log is None:
        return CompletionVerification(False, "canonical-review-log-path-invalid")
    review_log_identity = _identity(resolved_review_log.read_bytes())
    entries, log_findings = parse_formal_review_log(resolved_review_log)
    if log_findings:
        return CompletionVerification(False, "canonical-review-log-invalid")
    if _identity(resolved_review_log.read_bytes()) != review_log_identity:
        return CompletionVerification(False, "canonical-review-log-identity-drift")
    matches = [entry for entry in entries if entry.review_id == review.review_id]
    expected_record = artifact.relative_to(change_root).as_posix()
    if len(matches) != 1:
        return CompletionVerification(False, "canonical-review-occurrence-missing")
    entry = matches[0]
    if (
        entry.stage != review.stage
        or entry.round != review.round
        or entry.status != review.status
        or _strip_code(entry.detailed_record) != expected_record
    ):
        return CompletionVerification(False, "canonical-review-occurrence-mismatch")
    normalized_evidence = {evidence_name: copy.deepcopy(evidence)}
    normalized_observed_identities = {
        evidence_name: artifact_identity,
        f"{evidence_name}-log": review_log_identity,
    }
    proof = VerifiedCompletion(
        outputs=(copy.deepcopy(evidence),),
        canonical_evidence=normalized_evidence,
        observed_identities=normalized_observed_identities,
        stage_facts={
            "review_id": review.review_id,
            "review_outcome": review.status,
            "reviewed_artifact_identity": expected_identity,
        },
    )
    return CompletionVerification(True, "stage-completion-evidence-valid", proof)


def evaluate_receipt_recovery(
    automation: dict[str, Any],
    transition_id: str,
    *,
    completion_evidence: dict[str, Any] | None,
    repository_root: Path | None = None,
) -> RecoveryDecision:
    """Return the only safe action for one durable transition receipt."""

    prepared = _active_prepared_receipts(automation)
    if len(prepared) > 1:
        return RecoveryDecision("fail-closed", False, "multiple-in-flight-transitions")
    receipts = automation.get("transition_receipts")
    receipt = receipts.get(transition_id) if isinstance(receipts, dict) else None
    if not isinstance(receipt, dict):
        return RecoveryDecision("fail-closed", False, "transition-receipt-not-found")
    if receipt.get("transition_id") != transition_id:
        return RecoveryDecision("fail-closed", False, "transition-receipt-identity-mismatch")
    try:
        expected_transition_key = compute_transition_key(receipt)
    except (TypeError, ValueError, RecursionError):
        return RecoveryDecision("fail-closed", False, "transition-key-uncomputable")
    if receipt.get("transition_key") != expected_transition_key:
        return RecoveryDecision("fail-closed", False, "transition-key-mismatch")
    status = receipt.get("status")
    if status == "completed":
        if completion_evidence is None:
            return RecoveryDecision("pause", False, "completed-evidence-unavailable")
        if completion_evidence.get("outputs") != receipt.get("outputs"):
            return RecoveryDecision("pause", False, "completed-output-identity-drift")
        if completion_evidence.get("canonical_sync") != receipt.get("canonical_sync"):
            return RecoveryDecision("pause", False, "completed-canonical-state-drift")
        if repository_root is None:
            return RecoveryDecision("pause", False, "stage-completion-evidence-invalid")
        current_evidence = copy.deepcopy(completion_evidence)
        current_evidence["input_identities"] = copy.deepcopy(
            receipt.get("input_identities")
        )
        current_evidence["expected_postcondition"] = copy.deepcopy(
            receipt.get("expected_postcondition")
        )
        verification = verify_transition_completion(
            automation,
            receipt,
            completion_evidence=current_evidence,
            repository_root=repository_root,
        )
        if not verification.valid:
            return RecoveryDecision("pause", False, verification.reason)
        proof = verification.proof
        if proof is None:
            return RecoveryDecision("pause", False, "stage-completion-proof-missing")
        persisted_sync = receipt.get("canonical_sync")
        persisted_observed = (
            persisted_sync.get("observed_identities")
            if isinstance(persisted_sync, dict)
            else None
        )
        log_identity_names = tuple(
            name for name in proof.observed_identities if name.endswith("-log")
        )
        if (
            len(log_identity_names) == 1
            and isinstance(persisted_observed, dict)
            and persisted_observed.get(log_identity_names[0])
            != proof.observed_identities.get(log_identity_names[0])
        ):
            return RecoveryDecision(
                "pause", False, "canonical-review-log-identity-drift"
            )
        if (
            receipt.get("outputs") != list(proof.outputs)
            or not isinstance(persisted_sync, dict)
            or persisted_sync.get("evidence") != proof.canonical_evidence
            or persisted_observed != proof.observed_identities
        ):
            return RecoveryDecision("pause", False, "completed-canonical-state-drift")
        return RecoveryDecision(
            "continue", False, "completed-evidence-current", proof
        )
    if status != "prepared":
        return RecoveryDecision("fail-closed", False, "unknown-or-nonrecoverable-receipt")
    if len(prepared) != 1 or prepared[0].get("transition_id") != transition_id:
        return RecoveryDecision("fail-closed", False, "prepared-receipt-binding-mismatch")

    capability_id = receipt.get("effective_capability_id")
    capabilities = automation.get("effective_capabilities")
    capability = capabilities.get(capability_id) if isinstance(capabilities, dict) else None
    if not isinstance(capability, dict) or capability.get("status") != "active":
        return RecoveryDecision("pause", False, "effective-capability-not-active")

    stage = capability.get("stage")
    stage_name = stage.get("name") if isinstance(stage, dict) else None
    stage_policy = STAGE_POLICY_BY_STAGE.get(stage_name)
    if stage_policy is None:
        return RecoveryDecision("fail-closed", False, "unknown-capability-stage")
    if capability.get("capability_kind") != stage_policy.capability_kind.value:
        return RecoveryDecision("fail-closed", False, "capability-policy-mismatch")
    retry_policy = stage_policy.retry_policy.value
    if receipt.get("retry_policy") != retry_policy:
        return RecoveryDecision(
            "fail-closed", False, "retry-policy-projection-mismatch"
        )
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
    if repository_root is None:
        return RecoveryDecision("pause", False, "stage-completion-evidence-invalid")
    verification = verify_transition_completion(
        automation,
        receipt,
        completion_evidence=completion_evidence,
        repository_root=repository_root,
    )
    if not verification.valid:
        return RecoveryDecision("pause", False, verification.reason)
    if verification.proof is None:
        return RecoveryDecision("pause", False, "stage-completion-proof-missing")
    return RecoveryDecision(
        "reconcile-completed",
        False,
        "completion-evidence-valid",
        verification.proof,
    )


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

    def __init__(self, metadata_path: Path, *, repository_root: Path | None = None):
        lexical_metadata = Path(os.path.abspath(metadata_path))
        canonical_layout = (
            lexical_metadata.name == "change.yaml"
            and lexical_metadata.parent.parent.name == "changes"
            and lexical_metadata.parent.parent.parent.name == "docs"
        )
        if canonical_layout:
            lexical_root = lexical_metadata.parent.parent.parent.parent
            if repository_root is not None:
                explicit_root = Path(os.path.abspath(repository_root))
                if explicit_root != lexical_root:
                    raise StateContractError(
                        "explicit repository root must equal canonical root"
                    )
            current = Path(lexical_metadata.parts[0])
            for component in lexical_metadata.parts[1:]:
                current /= component
                if current.is_symlink():
                    raise StateContractError(
                        "canonical change metadata path must not contain symlinks"
                    )
            resolved_root = lexical_root.resolve()
            resolved_metadata = lexical_metadata.resolve()
            canonical_change_id = lexical_metadata.parent.name
        else:
            resolved_metadata = metadata_path.resolve()
            resolved_root = (repository_root or resolved_metadata.parent).resolve()
            canonical_change_id = None
        try:
            relative_metadata = resolved_metadata.relative_to(resolved_root)
        except ValueError as error:
            raise StateContractError(
                "change metadata must belong to the state store repository root"
            ) from error
        if relative_metadata.parts[:2] == ("docs", "changes") and (
            len(relative_metadata.parts) != 4
            or relative_metadata.parts[-1] != "change.yaml"
        ):
            raise StateContractError(
                "canonical change metadata must use docs/changes/<change-id>/change.yaml"
            )
        self.metadata_path = resolved_metadata
        self._repository_root = resolved_root
        self._canonical_change_id = canonical_change_id

    @property
    def repository_root(self) -> Path:
        """Return the immutable repository root bound to this state store."""

        return self._repository_root

    def require_repository_root(self, repository_root: Path | None = None) -> Path:
        """Reject evidence roots that are not the store's canonical repository."""

        candidate = (
            self._repository_root
            if repository_root is None
            else Path(os.path.abspath(repository_root))
        )
        if candidate != self._repository_root:
            raise StateContractError("repository root does not match state store")
        return self._repository_root

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
        if self._canonical_change_id is not None:
            change_id = document.get("change_id")
            if change_id != self._canonical_change_id:
                raise StateContractError(
                    "change metadata change_id must match its canonical change directory"
                )
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
        canonical_sync_evidence: dict[str, Any] | None = None,
        canonical_sync_observed_identities: dict[str, str] | None = None,
        activated_capabilities: tuple[dict[str, Any], ...] = (),
        invalidate_bound_capability: bool = False,
        expected_document_identity: str,
    ) -> StateMutationResult:
        evidence_root = self.repository_root
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
        canonical_sync: dict[str, Any] = {"status": canonical_sync_status}
        if canonical_sync_evidence is not None:
            canonical_sync["evidence"] = copy.deepcopy(canonical_sync_evidence)
        if canonical_sync_observed_identities is not None:
            canonical_sync["observed_identities"] = copy.deepcopy(
                canonical_sync_observed_identities
            )
        receipt["canonical_sync"] = canonical_sync
        if status == "completed":
            completion_evidence = {
                "input_identities": copy.deepcopy(receipt.get("input_identities")),
                "expected_postcondition": copy.deepcopy(
                    receipt.get("expected_postcondition")
                ),
                "outputs": copy.deepcopy(outputs),
                "canonical_sync": copy.deepcopy(canonical_sync),
            }
            verification = verify_transition_completion(
                replacement,
                receipt,
                completion_evidence=completion_evidence,
                repository_root=evidence_root,
            )
            if not verification.valid:
                raise StateContractError(
                    "stage-native completion evidence invalid: " + verification.reason
                )
            proof = verification.proof
            if proof is None:
                raise StateContractError("stage-native completion proof is missing")
            receipt["outputs"] = [copy.deepcopy(item) for item in proof.outputs]
            receipt["canonical_sync"] = {
                "status": "synchronized",
                "evidence": copy.deepcopy(proof.canonical_evidence),
                "observed_identities": copy.deepcopy(proof.observed_identities),
            }
            capabilities = replacement.get("effective_capabilities")
            capability = (
                capabilities.get(receipt.get("effective_capability_id"))
                if isinstance(capabilities, dict)
                else None
            )
            if not isinstance(capability, dict) or capability.get("status") != "active":
                raise StateContractError("completed transition requires its active capability")
            capability["status"] = "consumed"
            for activated in activated_capabilities:
                if not isinstance(activated, dict):
                    raise StateContractError(
                        "activated effective capability must be an object"
                    )
                activated_id = activated.get("capability_id")
                if (
                    not isinstance(activated_id, str)
                    or not activated_id
                    or activated_id in capabilities
                ):
                    raise StateContractError(
                        "activated effective capability identity is invalid"
                    )
                capabilities[activated_id] = copy.deepcopy(activated)
            capability_stage = capability.get("stage")
            if (
                isinstance(capability_stage, dict)
                and capability_stage.get("name") == "proposal-review"
            ):
                run = replacement.get("run")
                if not isinstance(run, dict):
                    raise StateContractError(
                        "proposal-review result requires an automation run"
                    )
                outcome = proof.stage_facts.get("review_outcome")
                target = run.get("target")
                target_stage = (
                    target.get("stage") if isinstance(target, dict) else None
                )
                if outcome in {"blocked", "inconclusive"}:
                    expected_action = "pause"
                    expected_pause_reason = f"proposal-review-{outcome}"
                elif target_stage == "proposal-review":
                    expected_action = "stop-at-target"
                    expected_pause_reason = None
                elif outcome == "approved":
                    expected_action = "continue"
                    expected_pause_reason = None
                else:
                    expected_action = "pause"
                    expected_pause_reason = (
                        "proposal-correction-authorization-required"
                    )
                expected_review_result = {
                    "review_id": proof.stage_facts.get("review_id"),
                    "reviewed_artifact_identity": proof.stage_facts.get(
                        "reviewed_artifact_identity"
                    ),
                    "outcome": outcome,
                    "occurrence_recorded": True,
                    "clean_gate": (
                        "satisfied"
                        if outcome == "approved"
                        else "not-satisfied"
                    ),
                    "routing_action": expected_action,
                }
                if expected_pause_reason is not None:
                    expected_review_result["pause_reason"] = (
                        expected_pause_reason
                    )
                replacement["latest_review_result"] = expected_review_result
                routing_action = expected_action
                if routing_action == "pause":
                    run["status"] = "paused"
                    run["pause_reason"] = expected_review_result.get(
                        "pause_reason"
                    )
                elif routing_action == "stop-at-target":
                    run["status"] = "completed"
                    run.pop("pause_reason", None)
        elif invalidate_bound_capability:
            capabilities = replacement.get("effective_capabilities")
            capability = (
                capabilities.get(receipt.get("effective_capability_id"))
                if isinstance(capabilities, dict)
                else None
            )
            if not isinstance(capability, dict) or capability.get("status") != "active":
                raise StateContractError(
                    "paused transition requires its active capability for invalidation"
                )
            capability["status"] = "invalidated"
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
                prepared[0]["transition_id"],
                completion_evidence=completion_evidence,
                repository_root=self.repository_root,
            )
            if decision.action != "reconcile-completed":
                return StateMutationResult(
                    "reconciliation-required", False, snapshot.document_identity
                )

        replacement = copy.deepcopy(snapshot.automation)
        if prepared:
            proof = decision.verified_completion
            if proof is None:
                raise StateContractError("verified completion disappeared during reconciliation")
            transition_id = prepared[0]["transition_id"]
            receipt = replacement["transition_receipts"][transition_id]
            receipt["status"] = "completed"
            receipt["outputs"] = [copy.deepcopy(item) for item in proof.outputs]
            receipt["canonical_sync"] = {
                "status": "synchronized",
                "evidence": copy.deepcopy(proof.canonical_evidence),
                "observed_identities": copy.deepcopy(proof.observed_identities),
            }
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
