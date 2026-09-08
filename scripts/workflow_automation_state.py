#!/usr/bin/env python3
"""Deferred automation policy helpers and explicit retired-storage boundaries.

Legacy YAML state stores are unsupported. No automation-to-v2 mapping is implied.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from review_artifact_validation import (
    finding_closure_state,
    parse_formal_review_findings,
    parse_formal_review_log,
    parse_formal_review_record,
    parse_formal_review_resolution,
)
from artifact_lifecycle_validation import inspect_lifecycle_artifact
from lifecycle_state_sync import parse_handoff_summary
from workflow_automation_policy import (
    STAGE_POLICY_BY_STAGE,
    project_proposal_review_result,
)
from validate_workflow_automation import (
    compute_transition_key,
    has_read_only_legacy_migration,
    proposal_review_route_binding,
    resolve_active_proposal_correction_capability,
    resolve_recorded_proposal_correction_capability,
    resolve_recorded_proposal_review_receipt,
    validate_workflow_automation,
)


ROOT = Path(__file__).resolve().parents[1]
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
}
PACKAGE_REVIEW_STAGES = {"design-review": "design", "delivery-review": "delivery"}
LIFECYCLE_STAGE_CLASSES = {
    "proposal": "proposal",
    "architecture": "architecture",
    "spec": "spec",
}
STAGE_NATIVE_VERIFIER_STAGES = frozenset(
    set(FORMAL_REVIEW_INPUT_IDENTITIES)
    | set(PACKAGE_REVIEW_STAGES)
    | set(LIFECYCLE_STAGE_CLASSES)
    | {
        "plan",
        "implement",
        "code-review",
        "review-resolution",
        "ci-maintenance",
        "final-holistic-code-review",
        "verify",
    }
)
_PLAIN_STRING_RESERVED = frozenset({"true", "false", "null", "[]", "{}"})
_NUMBER_RE = re.compile(
    r"-?(?:[0-9]+|[0-9]+\.[0-9]+|[0-9]+[eE][+-]?[0-9]+|[0-9]+\.[0-9]+[eE][+-]?[0-9]+)"
)


class StateContractError(RuntimeError):
    """Raised before mutation when workflow-automation state is unsafe."""


class AutomationStateContractError(StateContractError):
    """Raised when a parsed document contains invalid unified automation."""


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


def _proposal_review_evidence_from_proof(
    proof: VerifiedCompletion,
) -> dict[str, str | None]:
    """Project the only proposal-review facts trusted by durable state."""

    return {
        "review_id": proof.stage_facts.get("review_id"),
        "outcome": proof.stage_facts.get("review_outcome"),
        "reviewed_artifact_identity": proof.stage_facts.get(
            "reviewed_artifact_identity"
        ),
        "review_record_identity": proof.observed_identities.get(
            "proposal-review"
        ),
    }


def _project_completed_proposal_review(
    automation: dict[str, Any],
    receipt: dict[str, Any],
    proof: VerifiedCompletion,
) -> None:
    """Persist the complete proposal-review result for every completion path."""

    run = automation.get("run")
    if not isinstance(run, dict):
        raise StateContractError(
            "proposal-review result requires an automation run"
        )
    transition_id = receipt.get("transition_id")
    if not isinstance(transition_id, str) or not transition_id:
        raise StateContractError(
            "proposal-review result requires a transition identity"
        )
    target = run.get("target")
    target_stage = target.get("stage") if isinstance(target, dict) else None
    proposal_review_evidence = _proposal_review_evidence_from_proof(proof)
    try:
        correction_capability_id = resolve_active_proposal_correction_capability(
            automation,
            reviewed_proposal_identity=proposal_review_evidence[
                "reviewed_artifact_identity"
            ],
            review_record_identity=proposal_review_evidence[
                "review_record_identity"
            ],
        )
        projection = project_proposal_review_result(
            outcome=proposal_review_evidence["outcome"],
            target_stage=target_stage,
            review_id=proposal_review_evidence["review_id"],
            reviewed_artifact_identity=proposal_review_evidence[
                "reviewed_artifact_identity"
            ],
            review_record_identity=proposal_review_evidence[
                "review_record_identity"
            ],
            correction_capability_id=correction_capability_id,
        )
    except (TypeError, ValueError) as error:
        raise StateContractError(
            "proposal-review result projection failed: " + str(error)
        ) from error
    receipt["proposal_review_evidence"] = copy.deepcopy(
        proposal_review_evidence
    )
    receipt["proposal_review_route"] = copy.deepcopy(
        proposal_review_route_binding(projection.review_result, target)
    )
    automation["latest_review_result"] = {
        **projection.review_result,
        "source_transition_id": transition_id,
    }
    run["status"] = projection.run_status
    if projection.run_pause_reason is not None:
        run["pause_reason"] = projection.run_pause_reason
    else:
        run.pop("pause_reason", None)


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


def _evidence_fields(path: Path) -> dict[str, str]:
    return parse_stage_evidence_fields(path, required_fields=set())


def parse_stage_evidence_fields(
    path: Path,
    *,
    required_fields: set[str] | frozenset[str],
) -> dict[str, str]:
    """Parse one closed stage-evidence record without first-value wins."""

    fields: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        label = key.strip().lstrip("-").strip()
        if not label:
            continue
        if label in fields:
            raise StateContractError(f"duplicate evidence field: {label}")
        fields[label] = value.strip().strip("`")
    missing = sorted(field for field in required_fields if not fields.get(field))
    if missing:
        raise StateContractError(
            "missing required evidence field: " + ", ".join(missing)
        )
    return fields


def _selected_fields(path: Path, labels: set[str] | frozenset[str]) -> dict[str, str] | None:
    values: dict[str, list[str]] = {label: [] for label in labels}
    for line in path.read_text(encoding="utf-8").splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        label = key.strip().lstrip("-").strip()
        if label in values:
            values[label].append(value.strip().strip("`"))
    if any(len(found) > 1 for found in values.values()):
        return None
    return {
        label: found[0]
        for label, found in values.items()
        if found and found[0]
    }


def _milestone_state_from_change_metadata(
    repository_root: Path,
    plan_path: Path,
    milestone_id: str,
) -> tuple[str | None, bool]:
    raise StateContractError("legacy change-record assessment adapter is unsupported")


def _review_applicability(
    fields: dict[str, str],
    *,
    target: str,
) -> tuple[str, str] | None:
    reviewed_milestone = fields.get("Reviewed milestone")
    if reviewed_milestone is not None:
        match = re.match(r"^(M[0-9]+)(?:\.|$)", reviewed_milestone)
        if match is None:
            return None
        return "milestone", match.group(1)
    review_scope = fields.get("Review scope")
    if review_scope is not None:
        return "scope", review_scope
    return "target", _strip_code(target)


def _canonical_review_occurrence(
    review_path: Path,
    *,
    repository_root: Path,
) -> tuple[Any, Any, Path, str] | None:
    root = repository_root.resolve()
    try:
        review_relative = review_path.relative_to(root)
    except ValueError:
        return None
    resolved_review = _resolve_repository_file(
        review_relative,
        repository_root=repository_root,
    )
    if resolved_review is None or resolved_review != review_path.resolve():
        return None
    review, review_findings = parse_formal_review_record(review_path)
    if review is None or review_findings or review_path.parent.name != "reviews":
        return None
    change_root = review_path.parent.parent
    review_log = change_root / "review-log.md"
    try:
        log_relative = review_log.relative_to(root)
    except ValueError:
        return None
    resolved_log = _resolve_repository_file(
        log_relative,
        repository_root=repository_root,
    )
    if resolved_log is None:
        return None
    entries, log_findings = parse_formal_review_log(resolved_log)
    if log_findings:
        return None
    matches = [entry for entry in entries if entry.review_id == review.review_id]
    if len(matches) != 1:
        return None
    entry = matches[0]
    try:
        expected_record = review_path.relative_to(change_root).as_posix()
        resolved_log.relative_to(root)
    except ValueError:
        return None
    if (
        entry.stage != review.stage
        or entry.round != review.round
        or entry.status != review.status
        or _strip_code(entry.detailed_record) != expected_record
    ):
        return None
    current_fields = _selected_fields(
        review_path,
        frozenset({"Reviewed milestone", "Review scope"}),
    )
    if current_fields is None:
        return None
    applicability = _review_applicability(
        current_fields,
        target=review.target,
    )
    if applicability is None:
        return None
    for later in entries:
        if later.line <= entry.line or later.stage != review.stage:
            continue
        later_relative = Path(_strip_code(later.detailed_record))
        later_path = _resolve_repository_file(
            change_root.relative_to(root) / later_relative,
            repository_root=repository_root,
        )
        if later_path is None:
            return None
        later_review, later_findings = parse_formal_review_record(later_path)
        if later_review is None or later_findings:
            return None
        later_fields = _selected_fields(
            later_path,
            frozenset({"Reviewed milestone", "Review scope"}),
        )
        if later_fields is None:
            return None
        later_applicability = _review_applicability(
            later_fields,
            target=later_review.target,
        )
        if later_applicability is None:
            return None
        if later_applicability == applicability:
            return None
    return review, entry, resolved_log, _identity(resolved_log.read_bytes())


def _review_resolution_gate(
    *,
    review_path: Path,
    review: Any,
    entry: Any,
    review_log: Path,
    resolution_path: Path,
    repository_root: Path,
) -> str | None:
    """Return a truthful review closeout state for one formal occurrence."""

    parsed_review, review_findings, review_errors = parse_formal_review_findings(
        review_path
    )
    entries, log_errors = parse_formal_review_log(review_log)
    if (
        parsed_review is None
        or review_errors
        or log_errors
        or parsed_review.review_id != review.review_id
    ):
        return None
    material_ids = frozenset(finding.finding_id for finding in review_findings)
    if not material_ids:
        if (
            entry.material_finding_ids
            or entry.open_finding_ids
            or resolution_path.resolve() != review_log.resolve()
        ):
            return None
        return "not-required"

    expected = review_path.parent.parent / "review-resolution.md"
    try:
        expected_relative = expected.relative_to(repository_root.resolve())
    except ValueError:
        return None
    canonical_resolution = _resolve_repository_file(
        expected_relative,
        repository_root=repository_root,
    )
    if (
        canonical_resolution is None
        or resolution_path.resolve() != canonical_resolution
        or frozenset(entry.material_finding_ids) != material_ids
        or entry.open_finding_ids
    ):
        return None
    resolution, resolution_errors = parse_formal_review_resolution(
        canonical_resolution
    )
    if resolution_errors or resolution.closeout_status != "closed":
        return None
    if any(
        finding_closure_state(
            finding_id,
            entries,
            resolution,
            review_findings,
        )
        != "closed"
        for finding_id in material_ids
    ):
        return None
    return "closed"


def _verify_implementation_stage_completion(
    *,
    stage_name: str,
    capability: dict[str, Any],
    resolved_evidence: dict[str, tuple[dict[str, str], Path, str]],
    repository_root: Path,
) -> tuple[dict[str, str] | None, str | None]:
    stage = capability.get("stage")
    occurrence = stage.get("occurrence") if isinstance(stage, dict) else None
    milestone_id = (
        occurrence.get("milestone_id")
        if isinstance(occurrence, dict)
        else None
    )

    if stage_name == "implement":
        try:
            validation = parse_stage_evidence_fields(
                resolved_evidence["validation"][1],
                required_fields={"Stage", "Milestone", "Result"},
            )
        except StateContractError:
            return None, "stage-native-implementation-invalid"
        plan = resolved_evidence["plan-handoff"][1]
        milestone_state, has_governed_owner = _milestone_state_from_change_metadata(
            repository_root, plan, str(milestone_id)
        )
        if (
            not isinstance(milestone_id, str)
            or validation.get("Stage") != "implement"
            or validation.get("Milestone") != milestone_id
            or validation.get("Result") != "passed"
            or not has_governed_owner
            or milestone_state != "review-requested"
        ):
            return None, "stage-native-implementation-invalid"
        return {
            "milestone_id": milestone_id,
            "milestone_validation_passed": "true",
        }, None

    if stage_name == "code-review":
        review_path = resolved_evidence["code-review"][1]
        occurrence_proof = _canonical_review_occurrence(
            review_path, repository_root=repository_root
        )
        plan = resolved_evidence["plan-handoff"][1]
        if occurrence_proof is None or not isinstance(milestone_id, str):
            return None, "stage-native-code-review-invalid"
        review, entry, review_log, review_log_identity = occurrence_proof
        fields = _selected_fields(review_path, frozenset({"Reviewed milestone"}))
        if fields is None:
            return None, "stage-native-code-review-invalid"
        reviewed_milestone = fields.get("Reviewed milestone", "")
        resolution_path = resolved_evidence["review-resolution"][1]
        resolution_status = _review_resolution_gate(
            review_path=review_path,
            review=review,
            entry=entry,
            review_log=review_log,
            resolution_path=resolution_path,
            repository_root=repository_root,
        )
        milestone_state, has_governed_owner = _milestone_state_from_change_metadata(
            repository_root, plan, milestone_id
        )
        if (
            review.stage != "code-review"
            or review.status not in {"approved", "clean-with-notes"}
            or not reviewed_milestone.startswith(milestone_id)
            or resolution_status not in {"not-required", "closed"}
            or not has_governed_owner
            or milestone_state != "closed"
        ):
            return None, "stage-native-code-review-invalid"
        return {
            "milestone_id": milestone_id,
            "review_outcome": review.status,
            "review_resolution_status": resolution_status,
            "review_log_identity": review_log_identity,
        }, None

    if stage_name == "review-resolution":
        resolution = resolved_evidence["review-resolution"][1]
        parsed, findings = parse_formal_review_resolution(resolution)
        scope = capability.get("scope")
        accepted_ids = (
            scope.get("accepted_finding_ids")
            if isinstance(scope, dict)
            else None
        )
        review_log_relative = (
            scope.get("review_log_path")
            if isinstance(scope, dict)
            else None
        )
        review_log = (
            _resolve_repository_file(
                Path(review_log_relative),
                repository_root=repository_root,
            )
            if isinstance(review_log_relative, str)
            else None
        )
        log_entries, log_findings = (
            parse_formal_review_log(review_log)
            if review_log is not None
            else ((), ())
        )
        entries_by_id = {
            entry.finding_id: entry for entry in parsed.entries
        }
        if (
            findings
            or log_findings
            or not isinstance(accepted_ids, list)
            or not accepted_ids
            or len(set(accepted_ids)) != len(accepted_ids)
            or set(accepted_ids) - set(entries_by_id)
            or any(
                entries_by_id[finding_id].disposition == "needs-decision"
                or entries_by_id[finding_id].fields.get("Status") is None
                or entries_by_id[finding_id].fields["Status"].value
                != "resolved"
                or entries_by_id[finding_id].fields.get(
                    "Validation evidence"
                )
                is None
                or entries_by_id[finding_id].fields[
                    "Validation evidence"
                ].value.strip()
                in {"", "pending"}
                for finding_id in accepted_ids
            )
            or any(
                finding_id in entry.open_finding_ids
                for entry in log_entries
                for finding_id in accepted_ids
            )
        ):
            return None, "stage-native-review-resolution-invalid"
        return {
            "review_resolution_closed": "true",
            "global_review_resolution_status": str(parsed.closeout_status),
        }, None

    if stage_name == "ci-maintenance":
        try:
            configuration = parse_stage_evidence_fields(
                resolved_evidence["ci-configuration"][1],
                required_fields={"Stage"},
            )
            validation = parse_stage_evidence_fields(
                resolved_evidence["ci-validation"][1],
                required_fields={"Stage", "Result"},
            )
        except StateContractError:
            return None, "stage-native-ci-maintenance-invalid"
        if (
            configuration.get("Stage") != "ci-maintenance"
            or validation.get("Stage") != "ci-maintenance"
            or validation.get("Result") != "passed"
        ):
            return None, "stage-native-ci-maintenance-invalid"
        return {"ci_validation_passed": "true"}, None

    if stage_name == "final-holistic-code-review":
        review_path = resolved_evidence["final-code-review"][1]
        occurrence_proof = _canonical_review_occurrence(
            review_path, repository_root=repository_root
        )
        if occurrence_proof is None:
            return None, "stage-native-final-review-invalid"
        review, entry, review_log, review_log_identity = occurrence_proof
        fields = _selected_fields(
            review_path,
            frozenset(
                {
                    "Review scope",
                    "complete_final_diff",
                    "cross_milestone_interactions",
                    "governing_artifacts",
                    "review_resolutions",
                    "final_validation_selection",
                    "generated_and_derived_artifacts",
                    "cross_milestone_scope",
                }
            ),
        )
        if (
            fields is None
            or review.stage != "code-review"
            or review.status not in {"approved", "clean-with-notes"}
            or fields.get("Review scope") != "final-holistic"
            or fields.get("complete_final_diff") != "reviewed"
            or fields.get("cross_milestone_interactions") != "reviewed"
            or fields.get("governing_artifacts") != "reviewed"
            or fields.get("review_resolutions")
            not in {"closed", "not-required"}
            or fields.get("final_validation_selection") != "reviewed"
            or fields.get("generated_and_derived_artifacts") != "current"
            or fields.get("cross_milestone_scope") != "reviewed"
            or entry.material_finding_ids
            or entry.open_finding_ids
        ):
            return None, "stage-native-final-review-invalid"
        return {
            "review_outcome": review.status,
            "review_resolution_status": "not-required",
            "final_review_clean": "true",
            "review_log_identity": review_log_identity,
        }, None

    if stage_name == "verify":
        try:
            report = parse_stage_evidence_fields(
                resolved_evidence["verify-report"][1],
                required_fields={"Stage", "Result"},
            )
            validation = parse_stage_evidence_fields(
                resolved_evidence["validation"][1],
                required_fields={"Stage", "Result"},
            )
        except StateContractError:
            return None, "stage-native-verification-invalid"
        if (
            report.get("Stage") == "verify"
            and report.get("Result") == "failed"
            and validation.get("Stage") == "verify"
            and validation.get("Result") == "failed"
        ):
            return None, "stage-native-verification-failed"
        if (
            report.get("Stage") != "verify"
            or report.get("Result") != "passed"
            or report.get("Next stage") != "pr"
            or report.get("External actions performed") != "no"
            or validation.get("Stage") != "verify"
            or validation.get("Result") != "passed"
        ):
            return None, "stage-native-verification-invalid"
        return {
            "verification_passed": "true",
            "external_action_performed": "false",
        }, None
    return None, "stage-native-verifier-unavailable"


def _package_members(document: dict[str, Any], kind: str) -> dict[str, str] | None:
    states = document.get("artifact_states")
    if not isinstance(states, dict):
        return None

    def members_for(artifact_kind: str, role: str) -> list[tuple[str, dict[str, Any]]]:
        return sorted(
            (
                (artifact_id, entry)
                for artifact_id, entry in states.items()
                if isinstance(artifact_id, str)
                and isinstance(entry, dict)
                and entry.get("kind") == artifact_kind
                and entry.get("role") == role
            ),
            key=lambda item: item[0],
        )

    if kind == "design":
        architecture = members_for("architecture", "primary")
        spec = members_for("spec", "primary")
        adrs = members_for("adr", "supporting")
        if len(architecture) != 1 or len(spec) != 1:
            return None
        selected = [architecture[0], spec[0], *adrs]
    else:
        plan = members_for("plan", "primary")
        if len(plan) != 1:
            return None
        selected = [plan[0]]
    if any(not isinstance(entry.get("path"), str) for _, entry in selected):
        return None
    return {artifact_id: entry["path"] for artifact_id, entry in selected}


def _package_review_fields(path: Path) -> dict[str, Any] | None:
    labels = {
        "Review ID",
        "Stage",
        "Round",
        "Reviewer authority",
        "Package kind",
        "Package members",
        "Upstream review ID",
        "Status",
        "Recording status",
    }
    fields = _selected_fields(path, labels)
    if fields is None or set(fields) != labels:
        return None
    members: dict[str, str] = {}
    for item in fields["Package members"].split(","):
        artifact_id, separator, artifact_path = item.strip().partition("=")
        if not separator or not artifact_id or not artifact_path or artifact_id in members:
            return None
        members[artifact_id] = artifact_path
    return {**fields, "members": members}


def _verify_package_review_completion(
    *,
    stage_name: str,
    evidence_name: str,
    evidence: dict[str, str],
    artifact: Path,
    artifact_identity: str,
    repository_root: Path,
) -> CompletionVerification:
    raise StateContractError("legacy change-record assessment adapter is unsupported")


def _verify_transition_completion(
    automation: dict[str, Any],
    receipt: dict[str, Any],
    *,
    completion_evidence: dict[str, Any],
    repository_root: Path,
    allow_stale_reviewed_artifact: bool = False,
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

    if stage_name in {
        "implement",
        "code-review",
        "review-resolution",
        "ci-maintenance",
        "final-holistic-code-review",
        "verify",
    }:
        stage_facts, error = _verify_implementation_stage_completion(
            stage_name=stage_name,
            capability=capability,
            resolved_evidence=resolved_evidence,
            repository_root=repository_root,
        )
        if error is not None or stage_facts is None:
            return CompletionVerification(False, error or "stage-native-verifier-unavailable")
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

    if stage_name in PACKAGE_REVIEW_STAGES:
        evidence_name = next(iter(policy.completion_evidence), None)
        evidence, artifact, artifact_identity = resolved_evidence[evidence_name]
        return _verify_package_review_completion(
            stage_name=stage_name,
            evidence_name=evidence_name,
            evidence=evidence,
            artifact=artifact,
            artifact_identity=artifact_identity,
            repository_root=repository_root,
        )

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
        or (
            not allow_stale_reviewed_artifact
            and _identity(target.read_bytes()) != expected_identity
        )
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
    match_indices = [
        index
        for index, entry in enumerate(entries)
        if entry.review_id == review.review_id
    ]
    expected_record = artifact.relative_to(change_root).as_posix()
    if len(match_indices) != 1:
        return CompletionVerification(False, "canonical-review-occurrence-missing")
    occurrence_index = match_indices[0]
    entry = entries[occurrence_index]
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
            "review_log_path": review_log_relative.as_posix(),
            "review_occurrence_line": str(entry.line),
        },
    )
    return CompletionVerification(True, "stage-completion-evidence-valid", proof)


def verify_transition_completion(
    automation: dict[str, Any],
    receipt: dict[str, Any],
    *,
    completion_evidence: dict[str, Any],
    repository_root: Path,
) -> CompletionVerification:
    """Verify live stage completion against current repository evidence."""

    return _verify_transition_completion(
        automation,
        receipt,
        completion_evidence=completion_evidence,
        repository_root=repository_root,
        allow_stale_reviewed_artifact=False,
    )


def _verify_completed_proposal_review_semantics(
    automation: dict[str, Any],
    transition_id: str,
    receipt: dict[str, Any],
    *,
    repository_root: Path,
    proof: VerifiedCompletion | None = None,
    require_current_log_identity: bool,
) -> CompletionVerification:
    """Bind one completed proposal-review receipt to repository review facts."""

    if proof is None:
        verification = _verify_transition_completion(
            automation,
            receipt,
            completion_evidence={
                "input_identities": copy.deepcopy(
                    receipt.get("input_identities")
                ),
                "expected_postcondition": copy.deepcopy(
                    receipt.get("expected_postcondition")
                ),
                "outputs": copy.deepcopy(receipt.get("outputs")),
                "canonical_sync": copy.deepcopy(receipt.get("canonical_sync")),
            },
            repository_root=repository_root,
            allow_stale_reviewed_artifact=not require_current_log_identity,
        )
        if not verification.valid or verification.proof is None:
            return CompletionVerification(
                False,
                "proposal-review-semantic-evidence-"
                + verification.reason,
            )
        proof = verification.proof

    parsed_evidence = _proposal_review_evidence_from_proof(proof)
    if receipt.get("proposal_review_evidence") != parsed_evidence:
        return CompletionVerification(
            False,
            "proposal-review-semantic-evidence-drift",
        )

    persisted_sync = receipt.get("canonical_sync")
    persisted_observed = (
        persisted_sync.get("observed_identities")
        if isinstance(persisted_sync, dict)
        else None
    )
    if not isinstance(persisted_observed, dict):
        return CompletionVerification(
            False,
            "proposal-review-semantic-observed-identities-invalid",
        )
    if (
        persisted_observed.get("proposal-review")
        != proof.observed_identities.get("proposal-review")
    ):
        return CompletionVerification(
            False,
            "proposal-review-semantic-review-identity-drift",
        )
    if require_current_log_identity and (
        persisted_observed.get("proposal-review-log")
        != proof.observed_identities.get("proposal-review-log")
    ):
        return CompletionVerification(
            False,
            "canonical-review-log-identity-drift",
        )

    try:
        resolve_recorded_proposal_review_receipt(
            automation,
            transition_id,
            receipt,
        )
    except (TypeError, ValueError):
        return CompletionVerification(
            False,
            "proposal-review-semantic-route-drift",
        )
    return CompletionVerification(
        True,
        "proposal-review-semantic-evidence-valid",
        proof,
    )


def validate_workflow_automation_semantics(
    automation: dict[str, Any],
    *,
    repository_root: Path,
) -> list[str]:
    """Validate durable automation facts that require repository evidence."""

    errors: list[str] = []
    receipts = automation.get("transition_receipts")
    capabilities = automation.get("effective_capabilities")
    completed_proposal_reviews: list[str] = []
    verified_occurrences: list[tuple[str, int, str]] = []
    if not isinstance(receipts, dict) or not isinstance(capabilities, dict):
        return errors

    for transition_id, receipt in receipts.items():
        if (
            not isinstance(transition_id, str)
            or not isinstance(receipt, dict)
            or receipt.get("status") != "completed"
        ):
            continue
        capability = capabilities.get(receipt.get("effective_capability_id"))
        stage = capability.get("stage") if isinstance(capability, dict) else None
        if (
            not isinstance(capability, dict)
            or capability.get("capability_kind") != "proposal-review"
            or not isinstance(stage, dict)
            or stage.get("name") != "proposal-review"
        ):
            continue
        completed_proposal_reviews.append(transition_id)
        verification = _verify_completed_proposal_review_semantics(
            automation,
            transition_id,
            receipt,
            repository_root=repository_root,
            require_current_log_identity=False,
        )
        if not verification.valid:
            errors.append(f"{transition_id}: {verification.reason}")
        elif verification.proof is not None:
            occurrence_line = verification.proof.stage_facts.get(
                "review_occurrence_line"
            )
            review_log_path = verification.proof.stage_facts.get(
                "review_log_path"
            )
            try:
                parsed_line = int(occurrence_line)
            except (TypeError, ValueError):
                errors.append(
                    f"{transition_id}: proposal-review semantic occurrence "
                    "source position missing"
                )
            else:
                if not isinstance(review_log_path, str) or not review_log_path:
                    errors.append(
                        f"{transition_id}: proposal-review semantic canonical "
                        "log identity missing"
                    )
                else:
                    verified_occurrences.append(
                        (transition_id, parsed_line, review_log_path)
                    )

    if completed_proposal_reviews:
        latest_result = automation.get("latest_review_result")
        if not isinstance(latest_result, dict):
            errors.append(
                "latest_review_result: completed proposal-review requires "
                "repository-backed latest result"
            )
        else:
            try:
                resolve_recorded_proposal_correction_capability(
                    automation,
                    latest_result,
                )
            except (TypeError, ValueError) as error:
                errors.append(
                    "latest_review_result: proposal-review semantic "
                    f"projection drift: {error}"
                )
        if (
            not errors
            and isinstance(latest_result, dict)
            and verified_occurrences
        ):
            review_log_paths = {
                review_log_path
                for _, _, review_log_path in verified_occurrences
            }
            occurrence_indices = [
                occurrence_index
                for _, occurrence_index, _ in verified_occurrences
            ]
            if len(review_log_paths) != 1:
                errors.append(
                    "latest_review_result: completed proposal-review "
                    "receipts use different canonical review logs"
                )
            elif len(set(occurrence_indices)) != len(occurrence_indices):
                errors.append(
                    "latest_review_result: completed proposal-review "
                    "receipts have duplicate canonical occurrences"
                )
            else:
                latest_transition_id = max(
                    verified_occurrences,
                    key=lambda occurrence: occurrence[1],
                )[0]
                if (
                    latest_result.get("source_transition_id")
                    != latest_transition_id
                ):
                    errors.append(
                        "latest_review_result: must select the latest "
                        "canonical proposal-review occurrence represented by "
                        "a completed receipt"
                    )
    return errors


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
        capabilities = automation.get("effective_capabilities")
        capability = (
            capabilities.get(receipt.get("effective_capability_id"))
            if isinstance(capabilities, dict)
            else None
        )
        capability_stage = (
            capability.get("stage")
            if isinstance(capability, dict)
            else None
        )
        if (
            isinstance(capability_stage, dict)
            and capability_stage.get("name") == "proposal-review"
        ):
            semantic_verification = _verify_completed_proposal_review_semantics(
                automation,
                transition_id,
                receipt,
                repository_root=repository_root,
                proof=proof,
                require_current_log_identity=True,
            )
            if not semantic_verification.valid:
                reason = semantic_verification.reason
                if reason == "proposal-review-semantic-evidence-drift":
                    reason = "completed-proposal-review-evidence-drift"
                elif reason in {
                    "proposal-review-semantic-route-drift",
                    "proposal-review-semantic-observed-identities-invalid",
                    "proposal-review-semantic-review-identity-drift",
                }:
                    reason = "completed-proposal-review-projection-drift"
                return RecoveryDecision(
                    "pause",
                    False,
                    reason,
                )
            semantic_errors = validate_workflow_automation_semantics(
                automation,
                repository_root=repository_root,
            )
            if semantic_errors:
                return RecoveryDecision(
                    "pause",
                    False,
                    "completed-proposal-review-projection-drift",
                )
            latest_result = automation.get("latest_review_result")
            try:
                if not isinstance(latest_result, dict):
                    raise ValueError(
                        "completed proposal-review requires latest result"
                    )
                resolve_recorded_proposal_correction_capability(
                    automation,
                    latest_result,
                )
            except (TypeError, ValueError):
                return RecoveryDecision(
                    "pause",
                    False,
                    "completed-proposal-review-projection-drift",
                )
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
    receipts = state.get("transition_receipts")
    transition_history = [
        copy.deepcopy(receipt)
        for receipt in receipts.values()
        if isinstance(receipts, dict) and isinstance(receipt, dict)
    ] if isinstance(receipts, dict) else []
    artifacts_changed: list[str] = []
    fixes_applied: list[str] = []
    for receipt in transition_history:
        if receipt.get("status") == "completed":
            for output in receipt.get("outputs", []):
                path = output.get("path") if isinstance(output, dict) else None
                if isinstance(path, str) and path not in artifacts_changed:
                    artifacts_changed.append(path)
        capability_id = receipt.get("effective_capability_id")
        capability = (
            capabilities.get(capability_id)
            if isinstance(capabilities, dict)
            and isinstance(capability_id, str)
            else None
        )
        if (
            receipt.get("status") == "completed"
            and isinstance(capability, dict)
            and capability.get("capability_kind")
            in {"proposal-correction", "implementation-correction"}
        ):
            fixes_applied.append(str(receipt.get("transition_id")))
    latest_completed = next(
        (
            receipt
            for receipt in reversed(transition_history)
            if receipt.get("status") == "completed"
        ),
        None,
    )
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
        "latest_completed_transition": copy.deepcopy(latest_completed),
        "transition_history": transition_history,
        "fixes_applied": fixes_applied,
        "artifacts_changed": artifacts_changed,
        "pause_reason": run.get("pause_reason"),
        "stop_reason": run.get("stop_reason"),
        "latest_evidence_identities": copy.deepcopy(state.get("observed_identities", {})),
        "latest_review_result": copy.deepcopy(state.get("latest_review_result")),
        "external_actions": state.get("external_actions"),
    }


class WorkflowAutomationStateStore:
    """Unsupported legacy persistence adapter for the deferred automation engine.

    No v2 automation field or transition mapping is selected by this retirement.
    Reject before resolving, reading, locking or writing any supplied path.
    """

    def __init__(self, metadata_path: Path, *, repository_root: Path | None = None):
        raise StateContractError("legacy automation record storage is unsupported; use explicit v2 recording")


class StageOwnedChangeStateStore:
    """Reject calls to the removed stage-owned persistence adapter."""

    def __init__(self, metadata_path: Path):
        raise StateContractError("stage-owned record storage is unsupported; use explicit v2 recording")
