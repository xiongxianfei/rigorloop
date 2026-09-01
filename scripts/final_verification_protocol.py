#!/usr/bin/env python3
"""Inactive v3 final-verification evidence and result protocol.

This module validates deterministic structure. It deliberately does not infer
semantic impact from paths or filenames; Verify supplies that judgment and its
affirmative evidence.
"""

from __future__ import annotations

import json
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
TAIL_REPORT_SUFFIX = "/verify-report.md"
TAIL_CHANGE_FIELD = "/change.yaml#validation_events.verify"


def _unknown(prefix: str, value: Any, allowed: set[str]) -> list[str]:
    if not isinstance(value, str) or value not in allowed:
        return [f"{prefix}: unknown_value {value}"]
    return []


def _nonempty_scalar(value: Any) -> bool:
    return isinstance(value, (str, int)) and not isinstance(value, bool) and str(value).strip() != ""


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


def evaluate_evidence_decision(obligation: dict[str, Any], impacts: list[dict[str, Any]]) -> str:
    """Select the conservative decision from already-asserted semantic facts."""
    freshness = obligation.get("freshness")
    if freshness not in FRESHNESS_CLASSES:
        raise ValueError(f"freshness: unknown_value {freshness}")
    if obligation.get("new_obligation") is True:
        return "newly-required"
    if freshness in {"always-current", "fresh-required"}:
        return "rerun"

    by_surface = {item.get("surface"): item for item in impacts}
    proved_surfaces = obligation.get("proved_surfaces")
    if not _nonempty_strings(proved_surfaces):
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
    always_current = result.get("always_current")
    if isinstance(always_current, list):
        for index, item in enumerate(always_current):
            if not isinstance(item, dict):
                continue
            errors.extend(_unknown(f"always_current[{index}].check_id", item.get("check_id"), ALWAYS_CURRENT_CHECKS))
            errors.extend(_unknown(f"always_current[{index}].execution", item.get("execution"), EXECUTION_KINDS))
            errors.extend(_unknown(f"always_current[{index}].observed_result", item.get("observed_result"), EVIDENCE_RESULTS))
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
            if result.get("outcome") == "successful" and not _nonempty_scalar(basis[field]):
                errors.append(f"basis.{field}: expected exactly one non-empty scalar identity")
            elif result.get("outcome") != "successful" and basis[field] is not None and not _nonempty_scalar(basis[field]):
                errors.append(f"basis.{field}: expected one non-empty scalar identity or null")
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
        evidence_id = item.get("evidence_id")
        if not _nonempty_scalar(evidence_id):
            errors.append(f"evidence[{index}].evidence_id: required")
        elif evidence_id in seen_evidence:
            errors.append(f"evidence[{index}].evidence_id: duplicate {evidence_id}")
        seen_evidence.add(evidence_id)
        if not _nonempty_strings(item.get("proved_surfaces")):
            errors.append(f"evidence[{index}].proved_surfaces: expected non-empty list")
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

    if not isinstance(always_current, list) or (result.get("outcome") == "successful" and not always_current):
        errors.append("always_current: expected at least one check")
        always_current = []
    actual_always_current: set[str] = set()
    for index, item in enumerate(always_current):
        if not isinstance(item, dict):
            errors.append(f"always_current[{index}]: expected mapping")
            continue
        check_id = item.get("check_id")
        if check_id in actual_always_current:
            errors.append(f"always_current[{index}].check_id: duplicate {check_id}")
        actual_always_current.add(check_id)
        if result.get("outcome") == "successful" and item.get("execution") not in ACTUAL_EXECUTIONS:
            errors.append(f"always_current[{index}].execution: requires actual-run or hosted-observation")
        if item.get("observed_result") != "pass" and result.get("outcome") == "successful":
            errors.append(f"always_current[{index}].observed_result: success requires pass")
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
        elif any(not value for value in explanation.values()):
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
    if text.count(REPORT_MARKER) != 1:
        raise ValueError("verify report must contain exactly one final-verification-v3 payload")
    payload = text.split(REPORT_MARKER, 1)[1].split("\n```", 1)[0]
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


def tail_disposition(changed_paths: list[str], change_id: str) -> str:
    report_path = f"docs/changes/{change_id}/verify-report.md"
    change_field = f"docs/changes/{change_id}/change.yaml#validation_events.verify"
    for path in changed_paths:
        if path == report_path:
            continue
        if path == change_field:
            continue
        return "stale"
    return "current"
