#!/usr/bin/env python3
"""Shared semantic checks for RigorLoop change metadata."""

from __future__ import annotations

import re
from typing import Any


REVIEW_GATE_INDEPENDENCE_LEVELS = {"L1", "L2", "L3"}
REVIEW_GATE_PHASE_RECEIPTS = (
    "risk-map-recorded",
    "evidence-menu-released",
    "evidence-results-released",
    "verdict-recorded",
)
REVIEW_GATE_PHASE_ORDER = (
    "risk-map-recorded",
    "evidence-menu-released",
    "evidence-results-released",
    "prior-findings-released",
    "verdict-recorded",
)
REQUIREMENT_FIDELITY_APPLICABILITY_RESULTS = {"applicable", "not-applicable"}
REQUIREMENT_FIDELITY_PATH_TRIGGERS = {
    "skills/",
    "scripts/*validator*",
    "scripts/validate-*",
    "schemas/",
    "specs/",
    "templates/",
    "docs/workflows.md",
    "docs/changes/**/reviews/",
    "docs/changes/**/review-*.md",
}
REQUIREMENT_FIDELITY_CATEGORY_TRIGGERS = {
    "spec-derived validators",
    "skill instructions derived from specs",
    "review-recording contracts",
    "workflow routing contracts",
    "closed enums",
    "multi-surface public skill guidance",
    "artifact lifecycle validators",
    "metadata validators",
    "generated-output or package parity validators",
    "autoprogression gates",
    "material-finding schemas",
}
REQUIREMENT_FIDELITY_NOT_APPLICABLE_REASONS = {
    "change unrelated to normative contracts",
    "decomposition already accepted upstream and unchanged",
    "surfaces covered by spec-derived constants exercised in tests",
}
SHA256_RE = re.compile(r"^sha256:[0-9a-fA-F]{64}$")
STAGE_OWNED_CONTRACT = "stage-owned-change-local-v1"
ARTIFACT_KINDS = {
    "proposal", "spec", "architecture", "adr", "plan", "test-spec"
}
ARTIFACT_ROLES = {"primary", "supporting"}
ARTIFACT_STATES = {
    "authoring", "review-required", "revision-required", "accepted",
    "approved", "active", "blocked", "deprecated", "superseded",
    "abandoned", "archived",
}
ARTIFACT_STATES_BY_KIND = {
    "proposal": {"authoring", "review-required", "revision-required", "blocked", "accepted", "superseded", "abandoned", "archived"},
    "spec": {"authoring", "review-required", "revision-required", "blocked", "approved", "superseded", "abandoned", "archived"},
    "architecture": {"authoring", "review-required", "revision-required", "blocked", "approved", "superseded", "abandoned", "archived"},
    "adr": {"authoring", "review-required", "revision-required", "blocked", "accepted", "active", "deprecated", "superseded", "abandoned", "archived"},
    "plan": {"authoring", "review-required", "revision-required", "blocked", "active", "superseded", "abandoned", "archived"},
    "test-spec": {"authoring", "review-required", "revision-required", "blocked", "active", "superseded", "abandoned", "archived"},
}
REVIEW_OUTCOMES = {"approved", "changes-requested", "blocked", "inconclusive"}
WORKFLOW_LIFECYCLE_STATES = {"active", "paused", "completed", "cancelled"}
WORKFLOW_STAGES = {
    "explore", "research", "proposal", "proposal-review", "spec", "spec-review",
    "architecture-assessment", "architecture", "architecture-review", "plan",
    "plan-review", "test-spec", "test-spec-review", "implement", "code-review",
    "review-resolution", "ci-maintenance", "final-holistic-code-review",
    "explain-change", "verify", "pr", "learn", "none",
}
BLOCKER_CODES = {
    "owner-decision", "review-findings-open", "authoring-in-progress",
    "incomplete-settlement", "stale-evidence", "scope-expansion",
    "validation-failed", "tooling-unavailable", "external-action-prohibited",
    "cancelled",
}
AUTOMATION_STATUSES = {"active", "paused", "completed", "cancelled"}
MILESTONE_KINDS = {"implementation", "lifecycle-closeout"}
MILESTONE_STATES = {"planned", "implementing", "review-requested", "resolution-needed", "closed"}
LATEST_REVIEW_STATUSES = {"not-started", "not-required", "review-requested", "approved", "changes-requested", "blocked", "inconclusive"}
REVIEW_OCCURRENCES = {"singleton", "milestone", "final", "none"}
FINAL_CLOSEOUT_REASONS = {
    "ready", "lifecycle-gates-open", "implementation-milestones-open",
    "milestone-review-pending", "review-findings-open", "explain-change-pending",
    "verify-pending", "pr-handoff-pending", "plan-index-sync-pending",
    "external-completion-event-pending",
}
_ARTIFACT_ID_RE = re.compile(r"^[a-z][a-z0-9-]*$")
_ROUND_RE = re.compile(r"^r[1-9][0-9]*$")
LEGAL_ARTIFACT_TRANSITIONS = {
    ("missing", "authoring"),
    ("authoring", "review-required"),
    ("review-required", "accepted"),
    ("review-required", "approved"),
    ("review-required", "active"),
    ("review-required", "revision-required"),
    ("review-required", "blocked"),
    ("revision-required", "authoring"),
    ("blocked", "authoring"),
    ("accepted", "authoring"),
    ("approved", "authoring"),
    ("active", "authoring"),
    ("accepted", "deprecated"),
    ("active", "deprecated"),
}
for _source in {"authoring", "review-required", "revision-required", "blocked"}:
    LEGAL_ARTIFACT_TRANSITIONS.add((_source, "abandoned"))
for _source in {"accepted", "approved", "active", "deprecated"}:
    LEGAL_ARTIFACT_TRANSITIONS.add((_source, "archived"))
for _source in {
    "authoring", "review-required", "revision-required", "blocked",
    "accepted", "approved", "active", "deprecated",
}:
    LEGAL_ARTIFACT_TRANSITIONS.add((_source, "superseded"))


def is_declared_clean_receipt_root(data: Any) -> bool:
    if not isinstance(data, dict):
        return False
    review = data.get("review")
    if not isinstance(review, dict):
        return False
    return (
        review.get("status") == "clean"
        or ("reviewed_artifact" in review and "review_log" in review)
    )


def validate_clean_receipt_root_review_metadata(
    data: Any,
    *,
    require_clean_receipt_root: bool = False,
) -> list[str]:
    if not isinstance(data, dict):
        return []
    if not require_clean_receipt_root and not is_declared_clean_receipt_root(data):
        return []

    errors: list[str] = []
    review = data.get("review")
    if not isinstance(review, dict):
        return ["review: required for clean receipt roots"]

    status = review.get("status")
    if not isinstance(status, str) or not status.strip():
        errors.append("review.status must identify clean receipt root status")
    elif status != "clean":
        errors.append("review.status must be 'clean' for clean receipt roots")

    reviewed_artifact = review.get("reviewed_artifact")
    if reviewed_artifact is None:
        errors.append("review.reviewed_artifact is required for clean receipt roots")
    elif not isinstance(reviewed_artifact, str):
        errors.append("review.reviewed_artifact: expected string")

    review_log = review.get("review_log")
    if review_log is None:
        errors.append("review.review_log is required for clean receipt roots")
    elif not isinstance(review_log, str):
        errors.append("review.review_log: expected string")

    if review.get("unresolved_items") != 0:
        errors.append("review.unresolved_items must be 0 for clean receipt roots")

    return errors


def validate_review_gate_metadata(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return []
    review = data.get("review")
    if not isinstance(review, dict):
        return []
    gate = review.get("review_gate")
    if gate is None:
        return []
    if not isinstance(gate, dict):
        return ["review.review_gate: expected object"]

    errors: list[str] = []
    for field in ("manifest", "independence_level", "initial_packet_sha256", "phase_receipts"):
        if field not in gate:
            errors.append(f"review.review_gate.{field}: missing required field")

    manifest = gate.get("manifest")
    if "manifest" in gate and not _nonempty_string(manifest):
        errors.append("review.review_gate.manifest: expected string")

    independence = gate.get("independence_level")
    if "independence_level" in gate:
        if independence == "L0":
            errors.append("review.review_gate.independence_level: L0 is not valid for automated handoff")
        elif independence not in REVIEW_GATE_INDEPENDENCE_LEVELS:
            errors.append("review.review_gate.independence_level: expected one of L1, L2, L3")

    packet_hash = gate.get("initial_packet_sha256")
    if "initial_packet_sha256" in gate and (
        not isinstance(packet_hash, str) or SHA256_RE.fullmatch(packet_hash) is None
    ):
        errors.append("review.review_gate.initial_packet_sha256: expected sha256:<64 hex>")

    receipts = gate.get("phase_receipts")
    if "phase_receipts" in gate:
        if not isinstance(receipts, list) or not all(isinstance(item, str) for item in receipts):
            errors.append("review.review_gate.phase_receipts: expected list of strings")
        else:
            for receipt in REVIEW_GATE_PHASE_RECEIPTS:
                if receipt not in receipts:
                    errors.append(f"review.review_gate.phase_receipts: missing {receipt}")
            for earlier, later in zip(REVIEW_GATE_PHASE_ORDER, REVIEW_GATE_PHASE_ORDER[1:]):
                if earlier in receipts and later in receipts and receipts.index(later) < receipts.index(earlier):
                    errors.append(f"review.review_gate.phase_receipts: {later} appears before {earlier}")
            if len(set(receipts)) != len(receipts):
                errors.append("review.review_gate.phase_receipts: duplicate phase receipt")

    return errors


def validate_requirement_fidelity_metadata(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return []
    review = data.get("review")
    if not isinstance(review, dict):
        return []
    fidelity = review.get("requirement_fidelity")
    if fidelity is None:
        return []
    if not isinstance(fidelity, dict):
        return ["review.requirement_fidelity: expected object"]

    errors: list[str] = []
    applicability = fidelity.get("applicability")
    if applicability not in REQUIREMENT_FIDELITY_APPLICABILITY_RESULTS:
        errors.append("review.requirement_fidelity.applicability: expected one of applicable, not-applicable")

    _validate_string_list_closed(
        fidelity.get("matched_path_triggers"),
        "review.requirement_fidelity.matched_path_triggers",
        REQUIREMENT_FIDELITY_PATH_TRIGGERS | {"none"},
        errors,
    )
    _validate_string_list_closed(
        fidelity.get("matched_category_triggers"),
        "review.requirement_fidelity.matched_category_triggers",
        REQUIREMENT_FIDELITY_CATEGORY_TRIGGERS | {"none"},
        errors,
    )

    review_stage = fidelity.get("review_stage")
    if not _nonempty_string(review_stage):
        errors.append("review.requirement_fidelity.review_stage: expected string")

    if applicability == "applicable":
        if fidelity.get("receipt_valid") is not True:
            errors.append("review.requirement_fidelity.receipt_valid: expected true when applicability is applicable")
    if applicability == "not-applicable":
        reason = fidelity.get("not_applicable_reason")
        if reason not in REQUIREMENT_FIDELITY_NOT_APPLICABLE_REASONS:
            errors.append("review.requirement_fidelity.not_applicable_reason: expected closed reason")

    return errors


def _validate_string_list_closed(value: Any, path: str, allowed: set[str], errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        errors.append(f"{path}: expected non-empty list")
        return
    for index, item in enumerate(value):
        if not isinstance(item, str):
            errors.append(f"{path}[{index}]: expected string")
            continue
        if item not in allowed:
            kind = "path trigger" if "path" in path else "category trigger"
            errors.append(f"{path}[{index}]: unknown {kind} {item}")


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _repo_path(value: Any) -> bool:
    if not _nonempty_string(value):
        return False
    return not value.startswith("/") and ".." not in value.split("/")


def _exact_keys(
    value: Any, path: str, required: set[str], optional: set[str], errors: list[str]
) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{path}: expected object")
        return False
    missing = required - set(value)
    extra = set(value) - required - optional
    for key in sorted(missing):
        errors.append(f"{path}.{key}: missing required field")
    for key in sorted(extra):
        errors.append(f"{path}.{key}: unexpected field")
    return not missing and not extra


def _closed(value: Any, path: str, allowed: set[str], errors: list[str]) -> None:
    if value not in allowed:
        errors.append(f"{path}: unknown_value; expected one of {', '.join(sorted(allowed))}")


def _evidence_paths(value: Any, path: str, errors: list[str], *, nonempty: bool = False) -> None:
    if not isinstance(value, list) or (nonempty and not value):
        errors.append(f"{path}: expected {'non-empty ' if nonempty else ''}list")
        return
    if len(value) != len(set(item for item in value if isinstance(item, str))):
        errors.append(f"{path}: duplicate path")
    for index, item in enumerate(value):
        if not _repo_path(item):
            errors.append(f"{path}[{index}]: expected normalized repository-relative path")


def validate_stage_owned_lifecycle_metadata(data: Any) -> list[str]:
    """Validate only records that opt into the stage-owned lifecycle contract."""

    if not isinstance(data, dict) or data.get("lifecycle_contract") != STAGE_OWNED_CONTRACT:
        return []
    errors: list[str] = []
    states = data.get("artifact_states")
    workflow_state = data.get("workflow_state")
    if not isinstance(states, dict):
        errors.append("artifact_states: expected object")
        states = {}
    if not isinstance(workflow_state, dict):
        errors.append("workflow_state: expected object")
        workflow_state = {}

    paths: set[str] = set()
    primary_kinds: set[str] = set()
    for artifact_id, entry in states.items():
        base = f"artifact_states.{artifact_id}"
        if not isinstance(artifact_id, str) or _ARTIFACT_ID_RE.fullmatch(artifact_id) is None:
            errors.append(f"{base}: invalid artifact ID")
        if not _exact_keys(
            entry, base, {"kind", "path", "role", "lifecycle_state"},
            {"authoring_evidence", "review", "replacement_artifact_id"}, errors
        ):
            continue
        kind = entry.get("kind")
        role = entry.get("role")
        state = entry.get("lifecycle_state")
        _closed(kind, f"{base}.kind", ARTIFACT_KINDS, errors)
        _closed(role, f"{base}.role", ARTIFACT_ROLES, errors)
        _closed(state, f"{base}.lifecycle_state", ARTIFACT_STATES, errors)
        if kind in ARTIFACT_STATES_BY_KIND and state not in ARTIFACT_STATES_BY_KIND[kind]:
            errors.append(f"{base}.lifecycle_state: invalid state for {kind}")
        path = entry.get("path")
        if not _repo_path(path):
            errors.append(f"{base}.path: expected normalized repository-relative path")
        elif path in paths:
            errors.append(f"{base}.path: duplicate artifact path")
        else:
            paths.add(path)
        if role == "primary" and kind in primary_kinds:
            errors.append(f"{base}.role: duplicate primary {kind}")
        elif role == "primary":
            primary_kinds.add(kind)
        authoring = entry.get("authoring_evidence")
        review = entry.get("review")
        replacement = entry.get("replacement_artifact_id")
        if state in {"authoring", "review-required"}:
            if not _repo_path(authoring):
                errors.append(f"{base}.authoring_evidence: required repository-relative path")
        elif authoring is not None:
            errors.append(f"{base}.authoring_evidence: allowed only while authoring or review-required")
        if state in {"accepted", "approved", "active", "revision-required", "blocked", "deprecated"}:
            if not _exact_keys(review, f"{base}.review", {"id", "artifact_id", "outcome", "record", "round"}, {"adr_settlement"}, errors):
                continue
            _closed(review.get("outcome"), f"{base}.review.outcome", REVIEW_OUTCOMES, errors)
            if review.get("artifact_id") != artifact_id:
                errors.append(f"{base}.review.artifact_id: must match {artifact_id}")
            if not _repo_path(review.get("record")):
                errors.append(f"{base}.review.record: expected normalized repository-relative path")
            if _ROUND_RE.fullmatch(str(review.get("round"))) is None:
                errors.append(f"{base}.review.round: expected r<n>")
        elif review is not None:
            errors.append(f"{base}.review: not allowed for {state}")
        if state == "superseded":
            if replacement not in states or replacement == artifact_id:
                errors.append(f"{base}.replacement_artifact_id: must name a different registered artifact")
        elif replacement is not None:
            errors.append(f"{base}.replacement_artifact_id: allowed only for superseded state")

    if _exact_keys(
        workflow_state, "workflow_state",
        {"lifecycle_state", "current_stage", "next_stage", "blocker", "evidence"},
        {"planned_work"}, errors
    ):
        _closed(workflow_state.get("lifecycle_state"), "workflow_state.lifecycle_state", WORKFLOW_LIFECYCLE_STATES, errors)
        _closed(workflow_state.get("current_stage"), "workflow_state.current_stage", WORKFLOW_STAGES, errors)
        _closed(workflow_state.get("next_stage"), "workflow_state.next_stage", WORKFLOW_STAGES, errors)
        _evidence_paths(workflow_state.get("evidence"), "workflow_state.evidence", errors)
        blocker = workflow_state.get("blocker")
        if blocker is not None:
            if _exact_keys(blocker, "workflow_state.blocker", {"code", "evidence"}, set(), errors):
                _closed(blocker.get("code"), "workflow_state.blocker.code", BLOCKER_CODES, errors)
                _evidence_paths(blocker.get("evidence"), "workflow_state.blocker.evidence", errors, nonempty=True)
        has_primary_plan = "plan" in primary_kinds
        if has_primary_plan != ("planned_work" in workflow_state):
            errors.append("workflow_state.planned_work: presence must match primary plan registration")
        planned = workflow_state.get("planned_work")
        if isinstance(planned, dict) and _exact_keys(
            planned, "workflow_state.planned_work",
            {"plan_artifact_id", "current_milestone", "milestones",
             "remaining_implementation_milestones", "latest_review",
             "final_closeout"},
            set(), errors
        ):
            plan_id = planned.get("plan_artifact_id")
            plan_entry = states.get(plan_id)
            if not isinstance(plan_entry, dict) or plan_entry.get("kind") != "plan" or plan_entry.get("role") != "primary":
                errors.append("workflow_state.planned_work.plan_artifact_id: must name the primary plan")
            milestones = planned.get("milestones")
            if not isinstance(milestones, dict):
                errors.append("workflow_state.planned_work.milestones: expected object")
                milestones = {}
            remaining = []
            first_nonterminal = "none"
            for milestone_id, milestone in milestones.items():
                path = f"workflow_state.planned_work.milestones.{milestone_id}"
                if re.fullmatch(r"M[1-9][0-9]*", str(milestone_id)) is None:
                    errors.append(f"{path}: invalid milestone ID")
                if _exact_keys(milestone, path, {"kind", "state"}, set(), errors):
                    _closed(milestone.get("kind"), f"{path}.kind", MILESTONE_KINDS, errors)
                    _closed(milestone.get("state"), f"{path}.state", MILESTONE_STATES, errors)
                    if milestone.get("state") != "closed" and first_nonterminal == "none":
                        first_nonterminal = milestone_id
                    if milestone.get("kind") == "implementation" and milestone.get("state") != "closed":
                        remaining.append(milestone_id)
            if planned.get("current_milestone") != first_nonterminal:
                errors.append("workflow_state.planned_work.current_milestone: must name first nonterminal milestone")
            if planned.get("remaining_implementation_milestones") != remaining:
                errors.append("workflow_state.planned_work.remaining_implementation_milestones: inconsistent")
            latest = planned.get("latest_review")
            if _exact_keys(latest, "workflow_state.planned_work.latest_review",
                           {"status", "stage", "round", "artifact_id", "occurrence", "milestone_id", "evidence"}, set(), errors):
                _closed(latest.get("status"), "workflow_state.planned_work.latest_review.status", LATEST_REVIEW_STATUSES, errors)
                _closed(latest.get("stage"), "workflow_state.planned_work.latest_review.stage", WORKFLOW_STAGES, errors)
                _closed(latest.get("occurrence"), "workflow_state.planned_work.latest_review.occurrence", REVIEW_OCCURRENCES, errors)
                _evidence_paths(latest.get("evidence"), "workflow_state.planned_work.latest_review.evidence", errors)
            closeout = planned.get("final_closeout")
            if _exact_keys(closeout, "workflow_state.planned_work.final_closeout",
                           {"readiness", "reasons", "evidence"}, set(), errors):
                _closed(closeout.get("readiness"), "workflow_state.planned_work.final_closeout.readiness", {"ready", "not-ready"}, errors)
                reasons = closeout.get("reasons")
                if not isinstance(reasons, list) or not reasons:
                    errors.append("workflow_state.planned_work.final_closeout.reasons: expected non-empty list")
                else:
                    for index, reason in enumerate(reasons):
                        _closed(reason, f"workflow_state.planned_work.final_closeout.reasons[{index}]", FINAL_CLOSEOUT_REASONS, errors)
                    if closeout.get("readiness") == "ready" and reasons != ["ready"]:
                        errors.append("workflow_state.planned_work.final_closeout.reasons: ready requires sole ready reason")
                    if closeout.get("readiness") == "not-ready" and "ready" in reasons:
                        errors.append("workflow_state.planned_work.final_closeout.reasons: not-ready cannot include ready")
                _evidence_paths(closeout.get("evidence"), "workflow_state.planned_work.final_closeout.evidence", errors)

    workflow = data.get("workflow")
    if not isinstance(workflow, dict):
        errors.append("workflow: expected object")
    else:
        if "autoprogression" in workflow:
            errors.append("workflow.autoprogression: mixed legacy writer is prohibited")
        automation = workflow.get("automation")
        if automation is not None and _exact_keys(
            automation, "workflow.automation",
            {"mechanism", "target", "status", "current_stage", "stop_reason", "evidence"},
            set(), errors
        ):
            if automation.get("mechanism") != "bounded-review-fix":
                errors.append("workflow.automation.mechanism: unknown_value; expected bounded-review-fix")
            _closed(automation.get("status"), "workflow.automation.status", AUTOMATION_STATUSES, errors)
            _closed(automation.get("current_stage"), "workflow.automation.current_stage", WORKFLOW_STAGES, errors)
            _evidence_paths(automation.get("evidence"), "workflow.automation.evidence", errors)
            stop_reason = automation.get("stop_reason")
            if automation.get("status") == "active" and stop_reason is not None:
                errors.append("workflow.automation.stop_reason: must be null while active")
            if automation.get("status") != "active" and not _nonempty_string(stop_reason):
                errors.append("workflow.automation.stop_reason: required when not active")
            target = automation.get("target")
            if _exact_keys(
                target, "workflow.automation.target",
                {"stage", "occurrence", "bound_at", "completion"},
                {"plan_identity"}, errors
            ):
                _closed(
                    target.get("stage"), "workflow.automation.target.stage",
                    WORKFLOW_STAGES - {"none"}, errors
                )
                occurrence = target.get("occurrence")
                if not isinstance(occurrence, dict) or not _nonempty_string(occurrence.get("kind")):
                    errors.append("workflow.automation.target.occurrence: expected structured occurrence")
                if not _nonempty_string(target.get("bound_at")):
                    errors.append("workflow.automation.target.bound_at: expected string")
                if not isinstance(target.get("completion"), dict):
                    errors.append("workflow.automation.target.completion: expected object")
    return errors


def validate_artifact_transition(kind: str, source: str, target: str) -> list[str]:
    """Reject unknown values before checking transition consistency."""

    errors: list[str] = []
    _closed(kind, "artifact.kind", ARTIFACT_KINDS, errors)
    if source != "missing":
        _closed(source, "artifact.source_state", ARTIFACT_STATES, errors)
    _closed(target, "artifact.target_state", ARTIFACT_STATES, errors)
    if errors:
        return errors
    if (source, target) not in LEGAL_ARTIFACT_TRANSITIONS:
        return [f"artifact transition {source} -> {target} is not allowed"]
    if target == "deprecated" and kind != "adr":
        return ["artifact transition to deprecated is allowed only for adr"]
    return []
