#!/usr/bin/env python3
"""Inactive v3 final-verification evidence and result protocol.

This module validates deterministic structure. It deliberately does not infer
semantic impact from paths or filenames; Verify supplies that judgment and its
affirmative evidence.
"""

from __future__ import annotations

import json
import hashlib
import re
from pathlib import PurePosixPath
from typing import Any


IMPACT_SURFACES = {
    "runtime-behavior",
    "public-api",
    "state-or-persistence",
    "migration",
    "dependencies",
    "build",
    "packaging",
    "generated-output",
    "security-or-authority",
    "documentation",
    "repository-metadata",
    "lifecycle-governance",
    "external-environment",
}
IMPACT_STATES = {"affected", "unaffected", "unknown"}
FRESHNESS_CLASSES = {"always-current", "fresh-required", "impact-sensitive"}
EVIDENCE_DECISIONS = {"reuse", "rerun", "newly-required"}
VERIFY_OUTCOMES = {"pending", "successful", "failed", "inconclusive", "interrupted", "stale"}
EVIDENCE_RESULTS = {"pass", "fail", "blocked", "missing", "conflicting", "unknown"}
EXECUTION_KINDS = {"actual-run", "hosted-observation", "reused-pass", "cache-hit", "not-run"}
CI_STATUSES = {"passed", "failed", "pending", "unavailable", "not-required"}
AUTHORITY_STATUSES = {"current", "stale", "missing", "conflicting", "ambiguous"}
PROOF_KINDS = {"command", "hosted", "prior-evidence", "cache"}

BASIS_FIELDS = {
    "repository_identity",
    "remote_identity",
    "base_branch",
    "base_revision",
    "merge_base_revision",
    "head_branch",
    "verified_subject_revision",
    "governed_change_id",
    "final_review_id",
    "design_package_id",
    "delivery_plan_id",
    "final_diff_sha256",
}
RESULT_FIELDS = {
    "protocol_version",
    "outcome",
    "basis",
    "basis_status",
    "impact",
    "evidence",
    "always_current",
    "ci_status",
    "blockers",
    "residual_risks",
    "branch_ready",
    "explanation",
}
BASIS_STATUS_FIELDS = {
    "repository",
    "governed_change",
    "verified_subject",
    "final_review",
    "design_package",
    "delivery_plan",
    "final_diff",
}
ALWAYS_CURRENT_CHECKS = {
    "current-change-and-repository-identity",
    "reviewed-subject-and-review-identity",
    "lifecycle-and-package-consistency",
    "review-closeout",
    "unresolved-blocker-state",
    "final-diff-classification",
    "required-artifact-and-evidence-existence",
    "complete-verify-result-consistency",
}
EXPLANATION_FIELDS = {
    "what_changed",
    "why",
    "requirements_and_design",
    "important_choices",
    "supporting_evidence",
    "limitations",
    "residual_risks",
}
ACTUAL_EXECUTIONS = {"actual-run", "hosted-observation"}
REPORT_MARKER = "```json final-verification-v3\n"
REPORT_PREFIX = "# Verify report\n\n" + REPORT_MARKER
REPORT_SUFFIX = "\n```\n"
SAFE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
REVISION_RE = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
REPOSITORY_ID_RE = re.compile(r"^repo:sha256:[0-9a-f]{64}$")
REMOTE_ID_RE = re.compile(r"^remote:sha256:[0-9a-f]{64}$")
BRANCH_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*[A-Za-z0-9]$|^[A-Za-z0-9]$")
EVIDENCE_FIELDS = {
    "evidence_id", "proved_surfaces", "freshness", "existing_result",
    "authority_current", "identity_current", "environment_current", "conflicting",
    "new_obligation", "decision", "decision_rationale", "execution",
    "observed_result", "cache_hit", "proof",
}
ALWAYS_CURRENT_FIELDS = {"check_id", "execution", "observed_result", "proof"}


def _unknown(prefix: str, value: Any, allowed: set[str]) -> list[str]:
    if not isinstance(value, str) or value not in allowed:
        return [f"{prefix}: unknown_value {value}"]
    return []


def _nonempty_strings(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(item, str) and item.strip() for item in value)


def _contains_self_commit_identity(value: Any) -> bool:
    if isinstance(value, dict):
        return any(
            key in {"report_commit", "report_commit_identity", "verify_report_revision"}
            or _contains_self_commit_identity(item)
            for key, item in value.items()
        )
    if isinstance(value, list):
        return any(_contains_self_commit_identity(item) for item in value)
    return False


def _repository_path(value: Any, suffix: str | None = None) -> bool:
    if not isinstance(value, str) or not value or "\\" in value or value.startswith("/"):
        return False
    path = PurePosixPath(value)
    if value != path.as_posix() or any(part in {"", ".", ".."} for part in path.parts):
        return False
    return suffix is None or value.endswith(suffix)


def _branch(value: Any) -> bool:
    return (
        isinstance(value, str)
        and BRANCH_RE.fullmatch(value) is not None
        and ".." not in value
        and "//" not in value
        and "@{" not in value
        and not value.endswith(".lock")
    )


def _validate_basis_identity(field: str, value: Any) -> bool:
    if field == "repository_identity":
        return isinstance(value, str) and REPOSITORY_ID_RE.fullmatch(value) is not None
    if field == "remote_identity":
        return isinstance(value, str) and REMOTE_ID_RE.fullmatch(value) is not None
    if field in {"base_revision", "merge_base_revision", "verified_subject_revision"}:
        return isinstance(value, str) and REVISION_RE.fullmatch(value) is not None
    if field in {"base_branch", "head_branch"}:
        return _branch(value)
    if field in {"governed_change_id", "final_review_id", "design_package_id"}:
        return isinstance(value, str) and SAFE_ID_RE.fullmatch(value) is not None
    if field == "delivery_plan_id":
        return _repository_path(value, ".md") and value.startswith("docs/plans/")
    if field == "final_diff_sha256":
        return isinstance(value, str) and DIGEST_RE.fullmatch(value) is not None
    return False


def _validate_proof(proof: Any, execution: Any, prefix: str) -> list[str]:
    if execution == "not-run" and proof is None:
        return []
    if not isinstance(proof, dict):
        return [f"{prefix}.proof: required mapping for {execution}"]
    kind = proof.get("kind")
    errors = _unknown(f"{prefix}.proof.kind", kind, PROOF_KINDS)
    if errors:
        return errors
    expected_kind = {
        "actual-run": "command",
        "hosted-observation": "hosted",
        "reused-pass": "prior-evidence",
        "cache-hit": "cache",
    }.get(execution)
    if expected_kind is None:
        return [f"{prefix}.proof: execution {execution} must not carry readiness proof"]
    if kind != expected_kind:
        return [f"{prefix}.proof.kind: expected {expected_kind} for {execution}"]
    shapes = {
        "command": {"kind", "command", "evidence_path", "evidence_sha256"},
        "hosted": {"kind", "provider", "run_id", "check_name", "subject_revision", "evidence_path", "evidence_sha256"},
        "prior-evidence": {"kind", "evidence_path", "evidence_sha256", "subject_revision"},
        "cache": {"kind", "cache_key"},
    }
    if set(proof) != shapes[kind]:
        errors.append(f"{prefix}.proof: invalid {kind} proof fields")
        return errors
    if kind == "command" and not _nonempty_strings(proof.get("command")):
        errors.append(f"{prefix}.proof.command: expected exact non-empty argv")
    if kind == "hosted":
        for field in ("provider", "run_id", "check_name"):
            if not isinstance(proof.get(field), str) or not proof[field].strip():
                errors.append(f"{prefix}.proof.{field}: required")
    if kind in {"hosted", "prior-evidence"} and (
        not isinstance(proof.get("subject_revision"), str)
        or REVISION_RE.fullmatch(proof["subject_revision"]) is None
    ):
        errors.append(f"{prefix}.proof.subject_revision: expected immutable Git revision")
    if kind in {"command", "hosted", "prior-evidence"}:
        if not _repository_path(proof.get("evidence_path")):
            errors.append(f"{prefix}.proof.evidence_path: expected normalized repository-relative path")
        if not isinstance(proof.get("evidence_sha256"), str) or DIGEST_RE.fullmatch(proof["evidence_sha256"]) is None:
            errors.append(f"{prefix}.proof.evidence_sha256: expected sha256 identity")
    if kind == "cache" and (not isinstance(proof.get("cache_key"), str) or DIGEST_RE.fullmatch(proof["cache_key"]) is None):
        errors.append(f"{prefix}.proof.cache_key: expected sha256 identity")
    return errors


def evaluate_evidence_decision(obligation: dict[str, Any], impacts: list[dict[str, Any]]) -> str:
    """Select the conservative decision from already-asserted semantic facts."""
    proved_surfaces = obligation.get("proved_surfaces")
    if not _nonempty_strings(proved_surfaces):
        raise ValueError("proved_surfaces: expected non-empty closed surface list")
    if len(set(proved_surfaces)) != len(proved_surfaces):
        raise ValueError("proved_surfaces: duplicate surface")
    by_surface = {item.get("surface"): item for item in impacts}
    for surface in proved_surfaces:
        if surface not in IMPACT_SURFACES:
            raise ValueError(f"proved_surfaces: unknown_value {surface}")
        if surface not in by_surface:
            raise ValueError(f"proved_surfaces: unclassified {surface}")
    freshness = obligation.get("freshness")
    if freshness not in FRESHNESS_CLASSES:
        raise ValueError(f"freshness: unknown_value {freshness}")
    if obligation.get("new_obligation") is True:
        return "newly-required"
    if freshness in {"always-current", "fresh-required"}:
        return "rerun"

    relevant = [by_surface.get(surface) for surface in proved_surfaces]
    if any(item is None or item.get("state") != "unaffected" or not _nonempty_strings(item.get("affirmative_evidence")) for item in relevant):
        return "rerun"
    if obligation.get("existing_result") != "pass":
        return "rerun"
    if obligation.get("authority_current") is not True or obligation.get("identity_current") is not True:
        return "rerun"
    if obligation.get("environment_current") is not True or obligation.get("conflicting") is not False:
        return "rerun"
    return "reuse"


def validate_final_verification_result(result: Any) -> list[str]:
    if not isinstance(result, dict):
        return ["result: expected mapping"]

    # Closed vocabularies fail before dependent consistency interpretation.
    errors = _unknown("outcome", result.get("outcome"), VERIFY_OUTCOMES)
    basis_status = result.get("basis_status")
    if isinstance(basis_status, dict):
        for field, status in basis_status.items():
            errors.extend(_unknown(f"basis_status.{field}", status, AUTHORITY_STATUSES))
    impacts = result.get("impact")
    if isinstance(impacts, list):
        for index, item in enumerate(impacts):
            if not isinstance(item, dict):
                continue
            errors.extend(_unknown(f"impact[{index}].surface", item.get("surface"), IMPACT_SURFACES))
            errors.extend(_unknown(f"impact[{index}].state", item.get("state"), IMPACT_STATES))
    evidence = result.get("evidence")
    if isinstance(evidence, list):
        for index, item in enumerate(evidence):
            if not isinstance(item, dict):
                continue
            errors.extend(_unknown(f"evidence[{index}].freshness", item.get("freshness"), FRESHNESS_CLASSES))
            errors.extend(_unknown(f"evidence[{index}].decision", item.get("decision"), EVIDENCE_DECISIONS))
            errors.extend(_unknown(f"evidence[{index}].existing_result", item.get("existing_result"), EVIDENCE_RESULTS))
            errors.extend(_unknown(f"evidence[{index}].observed_result", item.get("observed_result"), EVIDENCE_RESULTS))
            errors.extend(_unknown(f"evidence[{index}].execution", item.get("execution"), EXECUTION_KINDS))
            proved_surfaces = item.get("proved_surfaces")
            if isinstance(proved_surfaces, list):
                for surface_index, surface in enumerate(proved_surfaces):
                    errors.extend(_unknown(f"evidence[{index}].proved_surfaces[{surface_index}]", surface, IMPACT_SURFACES))
            proof = item.get("proof")
            if isinstance(proof, dict):
                errors.extend(_unknown(f"evidence[{index}].proof.kind", proof.get("kind"), PROOF_KINDS))
    always_current = result.get("always_current")
    if isinstance(always_current, list):
        for index, item in enumerate(always_current):
            if not isinstance(item, dict):
                continue
            errors.extend(_unknown(f"always_current[{index}].check_id", item.get("check_id"), ALWAYS_CURRENT_CHECKS))
            errors.extend(_unknown(f"always_current[{index}].execution", item.get("execution"), EXECUTION_KINDS))
            errors.extend(_unknown(f"always_current[{index}].observed_result", item.get("observed_result"), EVIDENCE_RESULTS))
            proof = item.get("proof")
            if isinstance(proof, dict):
                errors.extend(_unknown(f"always_current[{index}].proof.kind", proof.get("kind"), PROOF_KINDS))
    errors.extend(_unknown("ci_status", result.get("ci_status"), CI_STATUSES))
    if errors:
        return errors

    if set(result) != RESULT_FIELDS:
        errors.append(f"result fields: expected exactly {sorted(RESULT_FIELDS)}")
    if _contains_self_commit_identity(result):
        errors.append("result: Verify report must not embed its own Git commit identity")
    if result.get("protocol_version") != 3:
        errors.append(f"protocol_version: expected 3, got {result.get('protocol_version')}")

    basis = result.get("basis")
    if not isinstance(basis, dict) or set(basis) != BASIS_FIELDS:
        errors.append(f"basis fields: expected exactly {sorted(BASIS_FIELDS)}")
    else:
        for field in sorted(BASIS_FIELDS):
            if result.get("outcome") == "successful" and not _validate_basis_identity(field, basis[field]):
                errors.append(f"basis.{field}: invalid canonical identity")
            elif result.get("outcome") != "successful" and basis[field] is not None and not _validate_basis_identity(field, basis[field]):
                errors.append(f"basis.{field}: expected canonical identity or null")
    if not isinstance(basis_status, dict) or set(basis_status) != BASIS_STATUS_FIELDS:
        errors.append(f"basis_status fields: expected exactly {sorted(BASIS_STATUS_FIELDS)}")

    if not isinstance(impacts, list) or (result.get("outcome") == "successful" and not impacts):
        errors.append("impact: expected at least one classified surface")
        impacts = []
    seen_surfaces: set[str] = set()
    for index, item in enumerate(impacts):
        if not isinstance(item, dict):
            errors.append(f"impact[{index}]: expected mapping")
            continue
        surface = item.get("surface")
        if surface in seen_surfaces:
            errors.append(f"impact[{index}].surface: duplicate {surface}")
        seen_surfaces.add(surface)
        if not isinstance(item.get("rationale"), str) or not item["rationale"].strip():
            errors.append(f"impact[{index}].rationale: required")
        if item.get("state") == "unaffected" and not _nonempty_strings(item.get("affirmative_evidence")):
            errors.append(f"impact[{index}].unaffected: affirmative_evidence required")

    if not isinstance(evidence, list) or (result.get("outcome") == "successful" and not evidence):
        errors.append("evidence: expected at least one obligation")
        evidence = []
    seen_evidence: set[str] = set()
    for index, item in enumerate(evidence):
        if not isinstance(item, dict):
            errors.append(f"evidence[{index}]: expected mapping")
            continue
        if set(item) != EVIDENCE_FIELDS:
            errors.append(f"evidence[{index}] fields: expected closed evidence entry")
        evidence_id = item.get("evidence_id")
        if not isinstance(evidence_id, str) or SAFE_ID_RE.fullmatch(evidence_id) is None:
            errors.append(f"evidence[{index}].evidence_id: expected safe identifier")
        elif evidence_id in seen_evidence:
            errors.append(f"evidence[{index}].evidence_id: duplicate {evidence_id}")
        seen_evidence.add(evidence_id)
        proved_surfaces = item.get("proved_surfaces")
        if not _nonempty_strings(proved_surfaces):
            errors.append(f"evidence[{index}].proved_surfaces: expected non-empty list")
            proved_surfaces = []
        seen_proved: set[str] = set()
        for surface_index, surface in enumerate(proved_surfaces):
            if surface in seen_proved:
                errors.append(f"evidence[{index}].proved_surfaces: duplicate {surface}")
            seen_proved.add(surface)
            if surface not in seen_surfaces:
                errors.append(f"evidence[{index}].proved_surfaces[{surface_index}]: unclassified {surface}")
        if not isinstance(item.get("decision_rationale"), str) or not item["decision_rationale"].strip():
            errors.append(f"evidence[{index}].decision_rationale: required")
        try:
            expected = evaluate_evidence_decision(item, impacts)
            if item.get("decision") != expected:
                errors.append(f"evidence[{index}].decision: expected {expected} from applicability inputs")
        except ValueError as exc:
            errors.append(f"evidence[{index}].{exc}")
        decision = item.get("decision")
        execution = item.get("execution")
        if decision in {"rerun", "newly-required"} and execution not in ACTUAL_EXECUTIONS:
            errors.append(f"evidence[{index}].execution: {decision} requires actual-run or hosted-observation")
        if item.get("freshness") in {"fresh-required", "always-current"} and execution not in ACTUAL_EXECUTIONS:
            errors.append(f"evidence[{index}].execution: {item.get('freshness')} requires actual-run or hosted-observation")
        if decision == "reuse" and execution != "reused-pass":
            errors.append(f"evidence[{index}].execution: reuse requires reused-pass")
        if item.get("cache_hit") is True and execution in ACTUAL_EXECUTIONS:
            errors.append(f"evidence[{index}].cache_hit: cannot represent actual execution")
        errors.extend(_validate_proof(item.get("proof"), execution, f"evidence[{index}]"))

    if not isinstance(always_current, list) or (result.get("outcome") == "successful" and not always_current):
        errors.append("always_current: expected at least one check")
        always_current = []
    actual_always_current: set[str] = set()
    for index, item in enumerate(always_current):
        if not isinstance(item, dict):
            errors.append(f"always_current[{index}]: expected mapping")
            continue
        if set(item) != ALWAYS_CURRENT_FIELDS:
            errors.append(f"always_current[{index}] fields: expected closed always-current entry")
        check_id = item.get("check_id")
        if check_id in actual_always_current:
            errors.append(f"always_current[{index}].check_id: duplicate {check_id}")
        actual_always_current.add(check_id)
        if result.get("outcome") == "successful" and item.get("execution") not in ACTUAL_EXECUTIONS:
            errors.append(f"always_current[{index}].execution: requires actual-run or hosted-observation")
        if item.get("observed_result") != "pass" and result.get("outcome") == "successful":
            errors.append(f"always_current[{index}].observed_result: success requires pass")
        errors.extend(_validate_proof(item.get("proof"), item.get("execution"), f"always_current[{index}]"))
    if result.get("outcome") == "successful" and actual_always_current != ALWAYS_CURRENT_CHECKS:
        errors.append(f"always_current check_ids: expected exactly {sorted(ALWAYS_CURRENT_CHECKS)}")

    outcome = result.get("outcome")
    explanation = result.get("explanation")
    blockers = result.get("blockers")
    if outcome == "successful":
        if isinstance(basis_status, dict) and any(status != "current" for status in basis_status.values()):
            errors.append("successful result requires every basis authority current")
        if result.get("branch_ready") is not True:
            errors.append("successful result requires branch_ready true")
        if blockers != []:
            errors.append("successful result requires no blockers")
        if result.get("ci_status") not in {"passed", "not-required"}:
            errors.append("successful result requires CI passed or not-required")
        if not isinstance(explanation, dict) or set(explanation) != EXPLANATION_FIELDS:
            errors.append(f"successful result explanation fields: expected exactly {sorted(EXPLANATION_FIELDS)}")
        elif any(
            not (
                (isinstance(value, str) and bool(value.strip()))
                or _nonempty_strings(value)
            )
            for value in explanation.values()
        ):
            errors.append("successful result explanation fields must be non-empty")
        for index, item in enumerate(evidence):
            if item.get("observed_result") != "pass":
                errors.append(f"evidence[{index}].observed_result: success requires pass")
    else:
        if result.get("branch_ready") is not False:
            errors.append(f"{outcome} result must set branch_ready false")
        if explanation is not None:
            errors.append(f"{outcome} result must omit explanation")
        if not _nonempty_strings(blockers):
            errors.append(f"{outcome} result must record blockers")
    return errors


def render_verify_report(result: dict[str, Any]) -> str:
    errors = validate_final_verification_result(result)
    if errors:
        raise ValueError("invalid final verification result: " + "; ".join(errors))
    payload = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False)
    return "# Verify report\n\n" + REPORT_MARKER + payload + "\n```\n"


def parse_verify_report(text: str) -> dict[str, Any]:
    if not text.startswith(REPORT_PREFIX) or not text.endswith(REPORT_SUFFIX) or text.count(REPORT_MARKER) != 1:
        raise ValueError("verify report has trailing or malformed content")
    payload = text[len(REPORT_PREFIX):-len(REPORT_SUFFIX)]
    result = json.loads(payload)
    errors = validate_final_verification_result(result)
    if errors:
        raise ValueError("invalid final verification result: " + "; ".join(errors))
    return result


def replay_disposition(previous: dict[str, Any], candidate: dict[str, Any]) -> str:
    if previous == candidate:
        return "identical-replay"
    identity_fields = BASIS_FIELDS | {"protocol_version"}
    previous_identity = {key: previous.get(key) for key in identity_fields}
    candidate_identity = {key: candidate.get(key) for key in identity_fields}
    if previous_identity != candidate_identity or previous.get("basis") != candidate.get("basis"):
        return "changed-basis"
    return "new-attempt"


def tail_disposition(tail: Any, change_id: str, verified_subject_revision: str) -> str:
    if not isinstance(tail, dict):
        return "incomplete"
    report_path = f"docs/changes/{change_id}/verify-report.md"
    selector = "lifecycle_cli.validations.verify-result"
    change_field = f"docs/changes/{change_id}/change.yaml#{selector}"
    changed_paths = tail.get("changed_paths")
    if not isinstance(changed_paths, list) or len(changed_paths) != 2 or set(changed_paths) != {report_path, change_field}:
        if isinstance(changed_paths, list) and any(path not in {report_path, change_field} for path in changed_paths):
            return "stale"
        return "incomplete"
    if tail.get("report_path") != report_path or not isinstance(tail.get("report_content"), str):
        return "incomplete"
    report_identity = "sha256:" + hashlib.sha256(tail["report_content"].encode()).hexdigest()
    if tail.get("report_sha256") != report_identity:
        return "incomplete"
    try:
        report = parse_verify_report(tail["report_content"])
    except (ValueError, json.JSONDecodeError):
        return "incomplete"
    registration = tail.get("registration")
    expected_registration = {
        "selector": selector,
        "evidence_path": report_path,
        "evidence_sha256": report_identity,
        "verified_subject_revision": verified_subject_revision,
        "stage_authority": "verify",
    }
    if registration != expected_registration:
        return "incomplete"
    if report.get("basis", {}).get("verified_subject_revision") != verified_subject_revision:
        return "incomplete"
    if report.get("outcome") != "successful" or report.get("branch_ready") is not True:
        return "incomplete"
    for path in changed_paths:
        if path not in {report_path, change_field}:
            return "stale"
    return "current"
