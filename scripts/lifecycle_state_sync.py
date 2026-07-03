#!/usr/bin/env python3
"""Workflow-state owner and projection parser helpers."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from review_artifact_validation import summarize_review_evidence


REQUIRED_HANDOFF_FIELDS = (
    "Current milestone",
    "Current milestone state",
    "Latest review evidence",
    "Review status",
    "Remaining in-scope implementation milestones",
    "Next stage",
    "Final closeout readiness",
    "Reason final closeout is or is not ready",
)
MILESTONE_STATES = frozenset({"planned", "implementing", "review-requested", "resolution-needed", "closed"})
REVIEW_STATUSES = frozenset(
    {"not-started", "not-required", "review-requested", "approved", "changes-requested", "blocked", "inconclusive"}
)
REQUIREMENT_FIDELITY_APPLICABILITY_RESULTS = frozenset({"applicable", "not-applicable"})
REQUIREMENT_FIDELITY_NOT_APPLICABLE_REASONS = frozenset(
    {
        "change unrelated to normative contracts",
        "decomposition already accepted upstream and unchanged",
        "surfaces covered by spec-derived constants exercised in tests",
    }
)
REVIEW_STAGES = frozenset(
    {
        "proposal-review",
        "spec-review",
        "architecture-review",
        "plan-review",
        "test-spec-review",
        "code-review",
        "none",
    }
)
FORMAL_REVIEW_STAGES = REVIEW_STAGES - {"none"}
REASON_CODES = (
    "ready",
    "lifecycle-gates-open",
    "implementation-milestones-open",
    "milestone-review-pending",
    "review-findings-open",
    "explain-change-pending",
    "verify-pending",
    "pr-handoff-pending",
    "plan-index-sync-pending",
    "external-completion-event-pending",
)
PLAN_LIFECYCLE_STATES = frozenset({"active", "blocked", "done", "superseded"})
LIVE_INDEX_STATES = frozenset({"active", "blocked"})
REVIEW_STATUS_PATTERN = re.compile(
    r"^(?P<status>[a-z-]+); stage=(?P<stage>[a-z-]+); round=(?P<round>none|r[1-9][0-9]*)$"
)
FIELD_PATTERN = re.compile(r"^\s*-?\s*(?P<label>[A-Za-z][A-Za-z -]*):\s*(?P<value>.+?)\s*$")
HANDOFF_FIELD_PATTERN = re.compile(r"^\s*-\s*(?P<label>[A-Za-z][A-Za-z -]*):\s*(?P<value>.+?)\s*$")
MARKDOWN_LINK_PATTERN = re.compile(r"^\[(?P<text>[^\]]+)\]\((?P<target>[^)]+)\)$")
READINESS_STAGE_CLAIM_PATTERN = re.compile(r"\b(?:ready for|next stage|current stage|current round)\b", re.IGNORECASE)


@dataclass(frozen=True)
class StateSyncFinding:
    path: Path
    message: str


@dataclass(frozen=True)
class AuthoringAutoprogressionRoute:
    profile_state: str
    next_stage: str | None
    stop_reason: str | None


@dataclass(frozen=True)
class ImplementationAutoprogressionRoute:
    profile_state: str
    next_stage: str | None
    stop_reason: str | None


@dataclass(frozen=True)
class HandoffSummary:
    fields: dict[str, str]

    @property
    def current_milestone(self) -> str:
        return self.fields["Current milestone"]

    @property
    def current_milestone_state(self) -> str:
        return self.fields["Current milestone state"]

    @property
    def review_status(self) -> str:
        return self.fields["Review status"]

    @property
    def next_stage(self) -> str:
        return self.fields["Next stage"]

    @property
    def final_closeout_readiness(self) -> str:
        return self.fields["Final closeout readiness"]

    @property
    def final_closeout_reason(self) -> str:
        return self.fields["Reason final closeout is or is not ready"]


@dataclass(frozen=True)
class PlanBodyState:
    lifecycle_state: str | None
    change_id: str | None
    lifecycle_errors: tuple[str, ...]
    change_id_errors: tuple[str, ...]
    handoff: HandoffSummary | None
    handoff_errors: tuple[str, ...]


@dataclass(frozen=True)
class PlanIndexRow:
    section: str
    plan_target: str
    plan_text: str
    state: str
    next_stage: str
    change_id: str


@dataclass(frozen=True)
class IndexOwnerResolution:
    plan_paths: tuple[Path, ...]
    findings: tuple[StateSyncFinding, ...]


def _sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current: str | None = None
    body: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(body).strip("\n")
            current = line[3:].strip()
            body = []
            continue
        if current is not None:
            body.append(line)
    if current is not None:
        sections[current] = "\n".join(body).strip("\n")
    return sections


def _normalize_whitespace(value: str) -> str:
    return " ".join(value.split())


def _strip_code(value: str) -> str:
    stripped = value.strip()
    if stripped.startswith("`") and stripped.endswith("`") and len(stripped) >= 2:
        return stripped[1:-1].strip()
    return stripped


def _resolve_plan_link(root: Path, source: Path, raw_target: str) -> Path | None:
    clean = raw_target.split("#", 1)[0].strip()
    if not clean:
        return None
    if clean.startswith("plans/"):
        candidate = (source.parent / clean).resolve()
    else:
        candidate = (root / clean).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    relative = candidate.relative_to(root).as_posix()
    if not relative.startswith("docs/plans/") or not relative.endswith(".md"):
        return None
    return candidate


def _parse_exact_fields(section: str, required_labels: tuple[str, ...]) -> tuple[dict[str, str], list[str]]:
    found: dict[str, list[str]] = {label: [] for label in required_labels}
    malformed: list[str] = []
    allowed = set(required_labels)
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        match = HANDOFF_FIELD_PATTERN.match(line)
        if match is None:
            if ":" in stripped and not stripped.startswith("#"):
                malformed.append(stripped)
            continue
        label = match.group("label")
        value = match.group("value").strip()
        if label in allowed:
            found[label].append(value)
        elif label in {"Last reviewed milestone"}:
            continue
        else:
            malformed.append(f"unexpected Current Handoff Summary field: {label}")

    errors: list[str] = []
    fields: dict[str, str] = {}
    for label in required_labels:
        values = found[label]
        if not values:
            errors.append(f"Current Handoff Summary missing required field: {label}")
        elif len(values) > 1:
            errors.append(f"Current Handoff Summary duplicate field: {label}")
        else:
            fields[label] = values[0]
    errors.extend(malformed)
    return fields, errors


def parse_handoff_summary(text: str) -> tuple[HandoffSummary | None, list[str]]:
    sections = _sections(text)
    matching_sections = [name for name in sections if name.casefold() == "current handoff summary"]
    if len(matching_sections) != 1:
        return None, ["Current Handoff Summary must appear exactly once"]
    section = sections[matching_sections[0]]
    if "Latest review evidence:" not in section:
        return None, ["structured-handoff-not-parseable: Current Handoff Summary missing Latest review evidence owner marker"]
    fields, errors = _parse_exact_fields(section, REQUIRED_HANDOFF_FIELDS)
    if errors:
        return None, [f"structured-handoff-incomplete: {message}" for message in errors]

    errors.extend(_validate_milestone_state(fields["Current milestone state"]))
    errors.extend(_validate_review_status(fields["Review status"]))
    errors.extend(_validate_final_closeout(fields["Final closeout readiness"], fields["Reason final closeout is or is not ready"]))
    if errors:
        return None, errors
    return HandoffSummary(fields=fields), []


def has_structured_workflow_state_marker(text: str) -> bool:
    sections = _sections(text)
    handoff = next((body for name, body in sections.items() if name.casefold() == "current handoff summary"), None)
    if handoff is None:
        return False
    return "Latest review evidence:" in handoff


def has_workflow_state_handoff_section(text: str) -> bool:
    sections = _sections(text)
    return any(name.casefold() == "current handoff summary" for name in sections)


def _validate_milestone_state(value: str) -> list[str]:
    if value not in MILESTONE_STATES:
        return [f"Current milestone state must be one of {', '.join(sorted(MILESTONE_STATES))}: {value}"]
    return []


def _validate_review_status(value: str) -> list[str]:
    match = REVIEW_STATUS_PATTERN.fullmatch(value)
    if match is None:
        return ["Review status must use '<status>; stage=<review-stage>; round=<round-token>' with no prose suffix"]
    status = match.group("status")
    stage = match.group("stage")
    round_token = match.group("round")
    errors: list[str] = []
    if status not in REVIEW_STATUSES:
        errors.append(f"Review status has unknown status: {status}")
    if stage not in REVIEW_STAGES:
        errors.append(f"Review status has unknown stage: {stage}")
    if status in {"not-started", "not-required"}:
        if stage != "none" or round_token != "none":
            errors.append("Review status not-started and not-required must use stage=none; round=none")
    elif stage not in FORMAL_REVIEW_STAGES or round_token == "none":
        errors.append("Review status review outcomes must name a formal review stage and positive round token")
    return errors


def _validate_final_closeout(readiness: str, reason: str) -> list[str]:
    errors: list[str] = []
    if readiness not in {"ready", "not ready"}:
        errors.append(f"Final closeout readiness must be ready or not ready: {readiness}")
    if "\u2014" not in reason:
        return errors + ["Reason final closeout is or is not ready must use '<reason-code-list> — <bounded detail>'"]
    code_text, detail = [part.strip() for part in reason.split("\u2014", 1)]
    codes = [code.strip() for code in code_text.split(",") if code.strip()]
    if not codes:
        errors.append("Reason final closeout is or is not ready must include at least one reason code")
    if not detail:
        errors.append("Reason final closeout is or is not ready must include bounded detail")
    unknown = [code for code in codes if code not in REASON_CODES]
    if unknown:
        errors.append(f"Reason final closeout is or is not ready has unknown reason code: {', '.join(unknown)}")
    if len(codes) != len(set(codes)):
        errors.append("Reason final closeout is or is not ready must not contain duplicate reason codes")
    expected_order = [code for code in REASON_CODES if code in codes]
    if codes != expected_order:
        errors.append("Reason final closeout is or is not ready reason codes must appear in normative order")
    if readiness == "ready" and codes != ["ready"]:
        errors.append("Reason final closeout is or is not ready must use sole reason code ready when readiness is ready")
    if readiness == "not ready":
        if "ready" in codes:
            errors.append("Reason final closeout is or is not ready must not include ready when readiness is not ready")
        if not codes:
            errors.append("Reason final closeout is or is not ready must include non-ready reason codes when readiness is not ready")
    return errors


AUTHORING_PROFILE = "authoring-through-plan-review"
AUTHORING_PROFILE_STAGES = (
    "spec",
    "spec-review",
    "architecture",
    "architecture-review",
    "plan",
    "plan-review",
)
AUTHORING_PROFILE_REVIEW_STAGES = {
    "proposal-review",
    "spec-review",
    "architecture-review",
    "plan-review",
}
AUTHORING_PROFILE_NONCLEAN_REVIEW_STATUSES = {
    "changes-requested",
    "blocked",
    "inconclusive",
}
AUTHORING_PROFILE_DURABLE_AUTHORIZATION_FAILURES = {
    "missing",
    "malformed",
    "partial",
    "failed",
}
AUTHORING_PROFILE_STATES = {
    "off",
    "armed",
    "active",
    "paused",
    "completed",
}
REVIEW_FIX_PROFILE = "bounded-review-fix"
REVIEW_FIX_PROFILE_TARGET_STAGES = (
    "proposal-review",
    "spec",
    "spec-review",
    "architecture",
    "architecture-review",
    "plan",
    "plan-review",
    "test-spec",
    "test-spec-review",
)
REVIEW_FIX_PROFILE_STATES = {
    "off",
    "armed",
    "active",
    "paused",
    "completed",
    "cancelled",
}
REVIEW_FIX_ARCHITECTURE_ASSESSMENTS = {
    "architecture-required",
    "architecture-not-required",
    "architecture-ambiguous",
}
IMPLEMENTATION_PROFILE = "implementation-through-verify"
IMPLEMENTATION_PROFILE_STATES = {
    "off",
    "armed",
    "active",
    "paused",
    "completed",
    "cancelled",
}
IMPLEMENTATION_PROFILE_PHASES = {"A", "B", "C"}
IMPLEMENTATION_DURABLE_AUTHORIZATION_FAILURES = {
    "missing",
    "malformed",
    "partial",
    "failed",
}
IMPLEMENTATION_MILESTONE_STATES = {"planned", "implementing", "review-requested", "resolution-needed", "closed"}
AUTO_FIX_CLASSES = {"none", "mechanical", "declared-safe"}
REVIEW_GATE_OUTCOMES = {"advance", "stop", "blocked", "inconclusive"}
REVIEW_GATE_RISK_TIERS = {"standard", "elevated", "critical-internal", "irreversible-external-action"}
REVIEW_GATE_CRITICAL_TIERS = {"critical-internal", "irreversible-external-action"}
REVIEW_GATE_AUTHORITY_KINDS = {"L3", "human", "n/a"}
REVIEW_GATE_TIER_AUTHORITY_KINDS = {
    "critical-internal": {"L3", "human"},
    "irreversible-external-action": {"human"},
}
REVIEW_GATE_ROLLOUT_MIN_STANDARD_SAMPLE_RATE = 20
REVIEW_GATE_ROLLOUT_MIN_STANDARD_SECOND_REVIEWS = 10
DETERMINATE_NATIVE_OUTCOMES = {
    "changes-requested": "stop",
    "blocked": "blocked",
    "inconclusive": "inconclusive",
}
CLEAN_NATIVE_STATUSES = ("approved", "clean-with-notes")
NATIVE_REVIEW_GATE_OUTCOMES = DETERMINATE_NATIVE_OUTCOMES | {
    status: "advance" for status in CLEAN_NATIVE_STATUSES
}
# Source: specs/review-independence-and-criticality.md R12c, R12d, R13c.
CLEAN_ADVANCE_GATES = (
    "independence_valid",
    "evidence_valid",
    "recording_valid",
    "clean_review_receipt_valid",
    "escalation_satisfied",
)
MECHANICAL_AUTO_FIX_KINDS = {
    "formatter-output",
    "lint-autofix",
    "generated-output-refresh",
    "exact-approved-rename",
    "unique-required-field-value",
    "mechanical-state-projection-sync",
    "deterministic-manifest-regeneration",
}
MECHANICAL_REQUIRED_FIELDS = (
    "auto_fix_kind",
    "affected_paths",
    "deterministic_authority",
    "required_validation",
)
DECLARED_SAFE_REQUIRED_FIELDS = (
    "affected_paths",
    "resolution_recipe",
    "named_inputs",
    "named_outputs",
    "forbidden_paths",
    "acceptance_criteria",
    "required_validation_commands",
    "scope_preservation_rule",
    "production_code_change",
    "behavior_test",
)
IMPLEMENTATION_CORRECTION_ROUND_CAP = 3
FINAL_HOLISTIC_REVIEW_REQUIRED_FIELDS = (
    "complete_final_diff",
    "cross_milestone_interactions",
    "governing_artifacts",
    "review_resolutions",
    "final_validation_selection",
    "generated_and_derived_artifacts",
    "cross_milestone_scope",
)


def _stop(profile_state: str, reason: str) -> AuthoringAutoprogressionRoute:
    return AuthoringAutoprogressionRoute(
        profile_state=profile_state,
        next_stage=None,
        stop_reason=reason,
    )


def _continue(profile_state: str, next_stage: str) -> AuthoringAutoprogressionRoute:
    return AuthoringAutoprogressionRoute(
        profile_state=profile_state,
        next_stage=next_stage,
        stop_reason=None,
    )


def _implementation_stop(profile_state: str, reason: str) -> ImplementationAutoprogressionRoute:
    return ImplementationAutoprogressionRoute(
        profile_state=profile_state,
        next_stage=None,
        stop_reason=reason,
    )


def _implementation_continue(profile_state: str, next_stage: str) -> ImplementationAutoprogressionRoute:
    return ImplementationAutoprogressionRoute(
        profile_state=profile_state,
        next_stage=next_stage,
        stop_reason=None,
    )


def _review_gate_stop(reason: str) -> ImplementationAutoprogressionRoute:
    return _implementation_stop("paused", reason)


def _critical_authority_parse_failure_reason(data: dict[str, object]) -> str | None:
    kind = data.get("critical_authority_kind")
    if kind is not None and kind not in REVIEW_GATE_AUTHORITY_KINDS:
        return "critical-authority-kind-invalid"

    satisfied = data.get("critical_authority_satisfied")
    if satisfied is not None and not isinstance(satisfied, bool):
        return "critical-authority-satisfied-invalid"

    return None


def _critical_authority_requirement_failure_reason(data: dict[str, object]) -> str | None:
    tier = data.get("risk_tier")
    kind = data.get("critical_authority_kind")
    satisfied = data.get("critical_authority_satisfied") is True

    if tier not in REVIEW_GATE_RISK_TIERS:
        return None

    if tier not in REVIEW_GATE_CRITICAL_TIERS:
        if kind not in {None, "n/a"}:
            return "critical-authority-kind-not-applicable"
        return None

    allowed_kinds = REVIEW_GATE_TIER_AUTHORITY_KINDS[str(tier)]
    if kind in {None, "n/a"} or not satisfied:
        return f"critical-authority-missing:{tier}"
    if kind not in allowed_kinds:
        return f"critical-authority-kind-insufficient:{tier}"
    return None


def _independent_review_failure_reason(data: dict[str, object]) -> str | None:
    if data.get("independence_manifest_valid") is not True:
        return "invalid-review-manifest"
    if data.get("phase_receipts_recorded") is not True:
        return "missing-phase-receipts"
    if data.get("recording_valid") is not True:
        return "review-recording-invalid"
    if data.get("clean_review_receipt_valid") is not True:
        return "insufficient-clean-receipt"
    return None


def _fidelity_applicability_presence_reason(data: dict[str, object]) -> str | None:
    applicability = data.get("requirement_fidelity_applicability")
    if applicability is None:
        return "fidelity-applicability-missing"
    if applicability not in REQUIREMENT_FIDELITY_APPLICABILITY_RESULTS:
        return "fidelity-applicability-unknown"
    return None


def _fidelity_receipt_failure_reason(data: dict[str, object]) -> str | None:
    applicability = data.get("requirement_fidelity_applicability")
    if applicability == "not-applicable":
        reason = data.get("requirement_fidelity_not_applicable_reason")
        if reason not in REQUIREMENT_FIDELITY_NOT_APPLICABLE_REASONS:
            return "fidelity-not-applicable-reason-invalid"
        return None
    if applicability == "applicable" and data.get("requirement_fidelity_receipt_valid") is not True:
        return "fidelity-receipt-invalid"
    return None


# Source: specs/requirement-fidelity-gate.md R3, R4-R8, R30-R34.
WORKFLOW_MANAGED_CLEAN_REVIEW_GATES = (
    ("review_independence", _independent_review_failure_reason),
    ("fidelity_applicability", _fidelity_applicability_presence_reason),
    ("fidelity_receipt", _fidelity_receipt_failure_reason),
)


def _clean_review_gate_failure_reason(data: dict[str, object]) -> str | None:
    for _gate_name, check in WORKFLOW_MANAGED_CLEAN_REVIEW_GATES:
        gate_failure = check(data)
        if gate_failure is not None:
            return gate_failure
    if data.get("unresolved_findings") not in {0, None}:
        return "review-findings-open"
    if data.get("risk_tier") not in REVIEW_GATE_RISK_TIERS:
        return "risk-tier-classification-invalid"
    if data.get("risk_tier_classifier_valid") is not True:
        return "risk-tier-classification-incomplete"
    if data.get("risk_tier_satisfied") is not True:
        return "risk-tier-escalation-failed"
    critical_authority_failure = _critical_authority_requirement_failure_reason(data)
    if critical_authority_failure is not None:
        return critical_authority_failure
    if data.get("risk_tier") == "standard" and data.get("sampling_phase") == "rollout":
        sample_rate = data.get("standard_clean_review_sample_rate")
        if not isinstance(sample_rate, int) or sample_rate < REVIEW_GATE_ROLLOUT_MIN_STANDARD_SAMPLE_RATE:
            return "standard-clean-review-sampling-floor-unmet"
        if data.get("standard_sampling_rate_reduction_requested") is True:
            reviewed_outcomes = data.get("standard_clean_reviews_independently_reviewed")
            if (
                not isinstance(reviewed_outcomes, int)
                or reviewed_outcomes < REVIEW_GATE_ROLLOUT_MIN_STANDARD_SECOND_REVIEWS
            ):
                return "standard-clean-review-sampling-evidence-floor-unmet"
    if data.get("risk_tier") == "elevated" and data.get("second_review_required") is not True:
        return "elevated-second-review-required"
    if data.get("second_review_required") is True:
        second_status = data.get("second_review_status")
        if second_status not in {"approved", "clean-with-notes"}:
            return "second-review-disagreement"
    return None


def evaluate_automated_review_gate_route(data: dict[str, object]) -> ImplementationAutoprogressionRoute:
    """Evaluate normalized automated review-gate routing for workflow-managed reviews."""

    if data.get("invocation_context") != "workflow-managed":
        return _review_gate_stop("isolated-invocation")

    critical_authority_parse_failure = _critical_authority_parse_failure_reason(data)
    if critical_authority_parse_failure is not None:
        return _review_gate_stop(critical_authority_parse_failure)

    critical_authority_requirement_failure = _critical_authority_requirement_failure_reason(data)
    if critical_authority_requirement_failure is not None:
        return _review_gate_stop(critical_authority_requirement_failure)

    native_status = data.get("native_review_status")
    gate_outcome = data.get("review_gate_outcome")
    if native_status not in NATIVE_REVIEW_GATE_OUTCOMES:
        return _review_gate_stop("unsupported-native-review-status")
    if gate_outcome not in REVIEW_GATE_OUTCOMES:
        return _review_gate_stop("unsupported-review-gate-outcome")

    if native_status in DETERMINATE_NATIVE_OUTCOMES:
        expected_outcome = DETERMINATE_NATIVE_OUTCOMES[native_status]  # type: ignore[index]
        if gate_outcome != expected_outcome:
            return _review_gate_stop("review-gate-outcome-mismatch")
    elif native_status in CLEAN_NATIVE_STATUSES:
        failure_reason = _clean_review_gate_failure_reason(data)
        expected_outcome = "inconclusive" if failure_reason is not None else "advance"
        if gate_outcome != expected_outcome:
            return _review_gate_stop("review-gate-outcome-mismatch-given-gate-state")
        if failure_reason is not None:
            return _review_gate_stop(failure_reason)
        return _implementation_continue("active", "advance")
    else:
        return _review_gate_stop("unsupported-native-review-status")

    if native_status in {"blocked", "inconclusive"}:
        return _review_gate_stop(str(gate_outcome))

    if data.get("independence_manifest_valid") is not True:
        return _review_gate_stop("invalid-review-manifest")
    if data.get("phase_receipts_recorded") is not True:
        return _review_gate_stop("missing-phase-receipts")
    if data.get("risk_tier") not in REVIEW_GATE_RISK_TIERS:
        return _review_gate_stop("risk-tier-classification-invalid")
    if data.get("risk_tier_classifier_valid") is not True:
        return _review_gate_stop("risk-tier-classification-incomplete")
    if data.get("risk_tier_satisfied") is not True:
        return _review_gate_stop("risk-tier-escalation-failed")

    if native_status == "changes-requested":
        if data.get("findings_auto_fix_classified") is not True:
            return _review_gate_stop("correction-finding-unclassified")
        if data.get("active_profile_authorizes_review_resolution") is not True:
            return _review_gate_stop("changes-requested-not-routable")
        rounds_remaining = data.get("correction_loop_rounds_remaining")
        if not isinstance(rounds_remaining, int) or rounds_remaining <= 0:
            return _review_gate_stop("changes-requested-not-routable")
        if (
            not isinstance(data.get("authorizing_profile"), str)
            or not isinstance(data.get("round_number"), int)
            or not data.get("satisfied_independence_evidence")
        ):
            return _review_gate_stop("review-resolution-route-record-incomplete")
        return _implementation_continue("active", "review-resolution")

    return _review_gate_stop("unsupported-native-review-status")


def _is_clean_proposal_gate(gate: object) -> bool:
    if not isinstance(gate, dict):
        return False
    return (
        gate.get("proposal_exists") is True
        and gate.get("proposal_status") == "accepted"
        and gate.get("proposal_review_status") == "approved"
        and gate.get("proposal_review_recording") == "recorded"
        and gate.get("proposal_review_material_findings") == 0
        and gate.get("proposal_review_open_blockers") == 0
        and gate.get("scope_settled") is True
        and gate.get("open_questions_block_spec") is False
        and gate.get("standing_gates_satisfied") is True
        and gate.get("change_identity_unambiguous") is True
        and gate.get("artifact_placement_unambiguous") is True
    )


def _profile_route_from_current_stage(stage: str, architecture_assessment: object) -> str | None:
    if stage == "proposal-review":
        return "spec"
    if stage == "spec":
        return "spec-review"
    if stage == "spec-review":
        return "architecture-assessment"
    if stage == "architecture-assessment":
        if architecture_assessment == "architecture-required":
            return "architecture"
        if architecture_assessment == "architecture-not-required":
            return "plan"
        return None
    if stage == "architecture":
        return "architecture-review"
    if stage == "architecture-review":
        return "plan"
    if stage == "plan":
        return "plan-review"
    if stage == "plan-review":
        return "test-spec"
    return None


def _profile_route_from_completed_stages(completed_stages: object, architecture_assessment: object) -> str | None:
    if not isinstance(completed_stages, list):
        return None
    completed = [stage for stage in completed_stages if isinstance(stage, str)]
    if len(completed) != len(set(completed)):
        return None
    completed_set = set(completed)

    if "spec" not in completed_set:
        return "spec"
    if "spec-review" not in completed_set:
        return "spec-review"
    if architecture_assessment == "architecture-ambiguous":
        return None
    if architecture_assessment == "architecture-required":
        if "architecture" not in completed_set:
            return "architecture"
        if "architecture-review" not in completed_set:
            return "architecture-review"
    elif architecture_assessment != "architecture-not-required":
        return "architecture-assessment"
    if "plan" not in completed_set:
        return "plan"
    if "plan-review" not in completed_set:
        return "plan-review"
    return "test-spec"


def evaluate_authoring_autoprogression_route(data: dict[str, object]) -> AuthoringAutoprogressionRoute:
    """Evaluate the bounded authoring-through-plan-review route for fixture validation."""

    profile = data.get("profile")
    profile_state = data.get("profile_state")
    durable_authorization = data.get("durable_authorization")
    current_stage = data.get("current_stage")
    latest_review_status = data.get("latest_review_status")
    architecture_assessment = data.get("architecture_assessment")

    if not isinstance(profile_state, str):
        profile_state = "off"

    if data.get("invocation_context") != "workflow-managed":
        return _stop(profile_state, "isolated-invocation")

    if profile == "off":
        return _continue("off", "explicit-user-action")
    if profile != AUTHORING_PROFILE:
        return _stop(profile_state, "unknown-profile")

    if isinstance(data.get("cancellation_record"), dict):
        return _continue("off", "explicit-user-action")

    if profile_state == "off":
        return _continue("off", "explicit-user-action")
    if profile_state == "completed":
        if isinstance(data.get("resume_record"), dict):
            return _stop("completed", "cannot-resume-completed")
        return _stop("completed", "profile-completed")
    if profile_state == "paused":
        if isinstance(data.get("resume_record"), dict):
            profile_state = "armed"
        else:
            return _stop("paused", "explicit-resume-required")
    if profile_state not in AUTHORING_PROFILE_STATES:
        return _stop("paused", "unhandled-profile-state")

    if durable_authorization in AUTHORING_PROFILE_DURABLE_AUTHORIZATION_FAILURES:
        return _stop(profile_state, "authorization-not-persisted")
    if durable_authorization != "persisted":
        return _stop(profile_state, "authorization-not-persisted")

    if data.get("user_paused") is True:
        return _stop(profile_state, "user-paused")
    if data.get("user_cancelled") is True:
        return _stop(profile_state, "user-cancelled")
    if data.get("needs_decision") is True:
        return _stop(profile_state, "needs-decision")
    if data.get("contradictory_workflow_state") is True:
        return _stop(profile_state, "contradictory-workflow-state")
    if data.get("unreliable_partial_completion") is True:
        return _stop(profile_state, "unreliable-partial-completion")
    if data.get("transition_count") == 6:
        return _stop(profile_state, "transition-budget-exhausted")

    if not _is_clean_proposal_gate(data.get("proposal_gate")):
        return _stop(profile_state, "proposal-gate-incomplete")

    if latest_review_status in AUTHORING_PROFILE_NONCLEAN_REVIEW_STATUSES:
        return _stop(profile_state, latest_review_status)
    if data.get("material_findings") is True:
        return _stop(profile_state, "material-finding")

    if current_stage == "resume":
        next_stage = _profile_route_from_completed_stages(
            data.get("completed_stages"),
            architecture_assessment,
        )
        if next_stage is None:
            return _stop(profile_state, "ambiguous-resume")
    elif isinstance(current_stage, str):
        next_stage = _profile_route_from_current_stage(current_stage, architecture_assessment)
        if current_stage == "architecture-assessment" and architecture_assessment == "architecture-ambiguous":
            return _stop(profile_state, "architecture-ambiguous")
        if next_stage is None:
            return _stop(profile_state, "ambiguous-workflow-state")
    else:
        return _stop(profile_state, "ambiguous-workflow-state")

    if next_stage in {"test-spec", "implement", "code-review", "explain-change", "verify", "pr"}:
        if next_stage == "test-spec" and current_stage == "plan-review" and latest_review_status == "approved":
            return _continue("completed", "test-spec")
        return _stop(profile_state, "out-of-scope-stage")

    return _continue("active", next_stage)


def _review_fix_next_stage(current_stage: str, architecture_assessment: object) -> tuple[str | None, str | None]:
    if current_stage == "proposal":
        return "proposal-review", None
    if current_stage == "proposal-review":
        return "spec", None
    if current_stage == "spec":
        return "spec-review", None
    if current_stage == "spec-review":
        if architecture_assessment is None:
            return None, "architecture-assessment-missing"
        if architecture_assessment not in REVIEW_FIX_ARCHITECTURE_ASSESSMENTS:
            return None, "architecture-assessment-invalid"
        if architecture_assessment == "architecture-ambiguous":
            return None, "architecture-ambiguous"
        if architecture_assessment == "architecture-required":
            return "architecture", None
        return "plan", None
    if current_stage == "architecture":
        return "architecture-review", None
    if current_stage == "architecture-review":
        return "plan", None
    if current_stage == "plan":
        return "plan-review", None
    if current_stage == "plan-review":
        return "test-spec", None
    if current_stage == "test-spec":
        return "test-spec-review", None
    return None, "ambiguous-workflow-state"


def _review_fix_reaches_or_exceeds_target(current_stage: str, target_stage: str) -> bool:
    if current_stage == target_stage:
        return True
    if current_stage not in REVIEW_FIX_PROFILE_TARGET_STAGES:
        return False
    return REVIEW_FIX_PROFILE_TARGET_STAGES.index(current_stage) > REVIEW_FIX_PROFILE_TARGET_STAGES.index(target_stage)


def _review_fix_next_exceeds_target(next_stage: str, target_stage: str) -> bool:
    return REVIEW_FIX_PROFILE_TARGET_STAGES.index(next_stage) > REVIEW_FIX_PROFILE_TARGET_STAGES.index(target_stage)


def evaluate_review_fix_autoprogression_route(data: dict[str, object]) -> AuthoringAutoprogressionRoute:
    """Evaluate bounded review-fix autoprogression routing for proposal-side fixtures."""

    profile = data.get("profile")
    profile_state = data.get("profile_state")
    target_stage = data.get("target_stage")
    current_stage = data.get("current_stage")
    latest_review_status = data.get("latest_review_status")

    if not isinstance(profile_state, str):
        profile_state = "off"

    if data.get("invocation_context") != "workflow-managed" or data.get("direct_review_invocation") is True:
        return _stop(profile_state, "isolated-invocation")

    if profile == "off":
        return _continue("off", "explicit-user-action")
    if profile != REVIEW_FIX_PROFILE:
        return _stop(profile_state, "unknown-profile")
    if target_stage not in REVIEW_FIX_PROFILE_TARGET_STAGES:
        return _stop("paused", "unknown-target-stage")

    if isinstance(data.get("cancellation_record"), dict):
        return _continue("cancelled", "explicit-user-action")

    if profile_state == "off":
        return _continue("off", "explicit-user-action")
    if profile_state == "completed":
        return _stop("completed", "profile-completed")
    if profile_state == "cancelled":
        return _stop("cancelled", "profile-cancelled")
    if profile_state == "paused":
        if not isinstance(data.get("resume_record"), dict):
            return _stop("paused", "explicit-resume-required")
        if data.get("cursor_valid") is not True:
            return _stop("paused", "resume-cursor-mismatch")
        profile_state = "armed"
    if profile_state not in REVIEW_FIX_PROFILE_STATES:
        return _stop("paused", "unhandled-profile-state")

    if data.get("durable_authorization") in AUTHORING_PROFILE_DURABLE_AUTHORIZATION_FAILURES:
        return _stop(profile_state, "authorization-not-persisted")
    if data.get("durable_authorization") != "persisted":
        return _stop(profile_state, "authorization-not-persisted")

    if data.get("change_id_resolved") is not True:
        return _stop(profile_state, "missing-change-id")
    if data.get("artifact_placement") != "resolved":
        return _stop(profile_state, "artifact-placement-ambiguous")
    if data.get("contradictory_workflow_state") is True:
        return _stop(profile_state, "contradictory-workflow-state")
    if data.get("user_paused") is True:
        return _stop(profile_state, "user-paused")
    if data.get("user_cancelled") is True:
        return _stop(profile_state, "user-cancelled")
    if data.get("needs_decision") is True:
        return _stop(profile_state, "needs-decision")

    if not _is_clean_proposal_gate(data.get("proposal_gate")):
        return _stop(profile_state, "proposal-gate-incomplete")
    if data.get("current_gate_clean") is not True:
        return _stop(profile_state, "current-gate-not-clean")
    if data.get("review_recording") != "recorded":
        return _stop(profile_state, "missing-review-evidence")
    if data.get("artifact_fresh") is not True:
        return _stop(profile_state, "stale-review")

    if latest_review_status in AUTHORING_PROFILE_NONCLEAN_REVIEW_STATUSES:
        return _stop(profile_state, latest_review_status)
    if latest_review_status != "approved":
        return _stop(profile_state, "current-review-not-approved")
    if data.get("material_findings") is True:
        return _stop(profile_state, "material-finding")
    if data.get("transition_count") == len(REVIEW_FIX_PROFILE_TARGET_STAGES):
        return _stop(profile_state, "transition-budget-exhausted")
    if not isinstance(current_stage, str):
        return _stop(profile_state, "ambiguous-workflow-state")

    if _review_fix_reaches_or_exceeds_target(current_stage, str(target_stage)):
        return _stop("completed", "target-reached")

    architecture_assessment = data.get("architecture_assessment")
    next_stage, blocked_reason = _review_fix_next_stage(current_stage, architecture_assessment)
    if blocked_reason is not None:
        return _stop("paused" if blocked_reason.startswith("architecture") else profile_state, blocked_reason)
    if next_stage is None:
        return _stop(profile_state, "ambiguous-workflow-state")
    if (
        current_stage == "spec-review"
        and architecture_assessment == "architecture-not-required"
        and target_stage in {"architecture", "architecture-review"}
    ):
        return _stop("paused", "target-not-applicable")
    if _review_fix_next_exceeds_target(next_stage, str(target_stage)):
        return _stop("completed", "target-reached")
    return _continue("active", next_stage)


def _is_settled_test_spec(settlement: object) -> bool:
    if not isinstance(settlement, dict):
        return False
    return (
        settlement.get("status") in {"active", "settled"}
        and settlement.get("requirements_covered") is True
        and settlement.get("acceptance_covered") is True
        and settlement.get("negative_boundary_cases") is True
        and settlement.get("uncovered_gaps") == "none"
        and settlement.get("needs_decision") is False
        and settlement.get("validation_commands_named") is True
        and settlement.get("contradicts_governing") is False
        and settlement.get("structural_validation") == "pass"
        and settlement.get("workflow_state_synchronized") is True
        and isinstance(settlement.get("input_identities"), dict)
    )


def _settlement_identities(settlement: object) -> dict[str, object] | None:
    if not isinstance(settlement, dict):
        return None
    identities = settlement.get("input_identities")
    if not isinstance(identities, dict):
        return None
    return identities


def _approved_recorded_test_spec_review(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    return (
        value.get("review_status") == "approved"
        and value.get("recording_status") == "recorded"
        and value.get("implementation_handoff") == "allowed"
        and value.get("open_blockers") in {0, None}
        and value.get("open_findings") in {0, None}
    )


def _promotion_evidence_complete(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    return value.get("phase_b_dogfood") == "recorded" and value.get("synthetic_fixtures") == "pass"


def _final_holistic_review_complete(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    if value.get("milestone_local_only") is True:
        return False
    return all(value.get(field) is True for field in FINAL_HOLISTIC_REVIEW_REQUIRED_FIELDS)


def _next_milestone_route(milestones: object) -> str | None:
    if not isinstance(milestones, list):
        return None
    for milestone in milestones:
        if not isinstance(milestone, dict):
            return None
        milestone_id = milestone.get("id")
        state = milestone.get("state")
        if not isinstance(milestone_id, str) or not isinstance(state, str):
            return None
        if state not in IMPLEMENTATION_MILESTONE_STATES:
            return None
        if state in {"planned", "implementing"}:
            return f"implement {milestone_id}"
        if state == "review-requested":
            return f"code-review {milestone_id}"
        if state == "resolution-needed":
            return f"review-resolution {milestone_id}"
    return None


def _all_milestones_closed(milestones: object) -> bool:
    if not isinstance(milestones, list) or not milestones:
        return False
    for milestone in milestones:
        if not isinstance(milestone, dict) or milestone.get("state") != "closed":
            return False
    return True


def evaluate_implementation_autoprogression_route(data: dict[str, object]) -> ImplementationAutoprogressionRoute:
    """Evaluate the implementation-through-verify route for fixture validation."""

    profile = data.get("profile")
    profile_state = data.get("profile_state")
    phase = data.get("phase")
    durable_authorization = data.get("durable_authorization")

    if not isinstance(profile_state, str):
        profile_state = "off"

    if data.get("invocation_context") != "workflow-managed":
        return _implementation_stop(profile_state, "isolated-invocation")

    if profile == "off":
        return _implementation_continue("off", "explicit-user-action")
    if profile != IMPLEMENTATION_PROFILE:
        return _implementation_stop(profile_state, "unknown-profile")

    if isinstance(data.get("cancellation_record"), dict):
        return _implementation_continue("cancelled", "explicit-user-action")

    if profile_state == "off":
        return _implementation_continue("off", "explicit-user-action")
    if profile_state == "completed":
        return _implementation_stop("completed", "profile-completed")
    if profile_state == "cancelled":
        return _implementation_stop("cancelled", "profile-cancelled")
    if profile_state == "paused":
        if isinstance(data.get("resume_record"), dict):
            profile_state = "armed"
        else:
            return _implementation_stop("paused", "explicit-resume-required")
    if profile_state not in IMPLEMENTATION_PROFILE_STATES:
        return _implementation_stop("paused", "unhandled-profile-state")

    if durable_authorization in IMPLEMENTATION_DURABLE_AUTHORIZATION_FAILURES:
        return _implementation_stop(profile_state, "authorization-not-persisted")
    if durable_authorization != "persisted":
        return _implementation_stop(profile_state, "authorization-not-persisted")

    if phase not in IMPLEMENTATION_PROFILE_PHASES:
        return _implementation_stop("paused", "unsupported-phase")

    if data.get("authoring_gates") not in {"completed", "manual-plan-review-approved"}:
        return _implementation_stop(profile_state, "authoring-gates-incomplete")
    if data.get("plan_review_status") != "approved":
        return _implementation_stop(profile_state, "plan-review-not-approved")
    if data.get("plan_review_recording") != "recorded":
        return _implementation_stop(profile_state, "plan-review-not-recorded")
    if data.get("plan_synchronized") is not True:
        return _implementation_stop(profile_state, "plan-not-synchronized")
    if data.get("milestones_ordered") is not True:
        return _implementation_stop(profile_state, "milestones-not-ordered")
    if data.get("test_spec_inputs_complete") is not True:
        return _implementation_stop(profile_state, "test-spec-inputs-incomplete")
    if data.get("working_tree_baseline") != "recorded":
        return _implementation_stop(profile_state, "working-tree-baseline-missing")
    if data.get("unrelated_dirty_state") not in {"absent", "excluded"}:
        return _implementation_stop(profile_state, "unrelated-dirty-state")
    if data.get("required_commands_approved") is not True:
        return _implementation_stop(profile_state, "commands-not-approved")
    if data.get("governing_findings_open") is True:
        return _implementation_stop(profile_state, "governing-findings-open")
    if data.get("artifact_placement_unambiguous") is not True:
        return _implementation_stop(profile_state, "artifact-placement-ambiguous")
    if data.get("workflow_state_synchronized") is not True:
        return _implementation_stop(profile_state, "workflow-state-unsynchronized")

    if phase == "A":
        return _implementation_continue("active", "audit-only")

    settlement = data.get("test_spec_settlement")
    if not _is_settled_test_spec(settlement):
        return _implementation_stop(profile_state, "test-spec-settlement-incomplete")
    if not _approved_recorded_test_spec_review(data.get("test_spec_review")):
        return _implementation_stop(profile_state, "implementation-without-test-spec-review")

    current_stage = data.get("current_stage")
    if current_stage == "first-code-review-precheck":
        settled_identities = _settlement_identities(settlement)
        current_identities = data.get("current_input_identities")
        if not isinstance(current_identities, dict) or current_identities != settled_identities:
            return _implementation_stop(profile_state, "settlement-identity-mismatch")
        route = _next_milestone_route(data.get("milestones"))
        if route is None:
            return _implementation_stop(profile_state, "milestone-state-ambiguous")
        if route.startswith("code-review "):
            return _implementation_continue("active", route)
        return _implementation_stop(profile_state, "first-review-not-current-milestone")

    if current_stage == "final-clean-code-review" or _all_milestones_closed(data.get("milestones")):
        if phase == "B":
            return _implementation_stop("active", "phase-boundary-explain-change")
        if not _promotion_evidence_complete(data.get("promotion_evidence")):
            return _implementation_stop("active", "promotion-evidence-missing")
        if not _final_holistic_review_complete(data.get("final_holistic_review")):
            return _implementation_stop("active", "final-holistic-review-missing")
        return _implementation_continue("active", "explain-change")

    route = _next_milestone_route(data.get("milestones"))
    if route is None:
        return _implementation_stop(profile_state, "milestone-state-ambiguous")
    return _implementation_continue("active", route)


def evaluate_implementation_correction_guardrails(data: dict[str, object]) -> ImplementationAutoprogressionRoute:
    """Evaluate implementation-profile automatic correction guardrails for fixtures."""

    profile_state = data.get("profile_state")
    if not isinstance(profile_state, str):
        profile_state = "active"
    if data.get("profile") != IMPLEMENTATION_PROFILE:
        return _implementation_stop(profile_state, "unknown-profile")
    if profile_state not in {"armed", "active"}:
        return _implementation_stop(profile_state, "profile-not-active")

    milestone = data.get("milestone")
    if not isinstance(milestone, str) or not milestone:
        return _implementation_stop(profile_state, "milestone-missing")

    finding_stop = _correction_findings_stop_reason(data.get("findings"))
    if finding_stop is not None:
        return _implementation_stop(profile_state, finding_stop)

    cap = data.get("per_milestone_round_cap", IMPLEMENTATION_CORRECTION_ROUND_CAP)
    if not isinstance(cap, int) or cap < 0 or cap > IMPLEMENTATION_CORRECTION_ROUND_CAP:
        return _implementation_stop(profile_state, "round-cap-policy-invalid")
    rounds_completed = data.get("correction_rounds_completed", 0)
    if not isinstance(rounds_completed, int) or rounds_completed >= cap:
        return _implementation_stop(profile_state, "correction-round-cap-exceeded")
    activation_count = data.get("activation_round_count")
    activation_ceiling = data.get("activation_round_ceiling")
    if isinstance(activation_count, int) and isinstance(activation_ceiling, int) and activation_count >= activation_ceiling:
        return _implementation_stop(profile_state, "activation-round-ceiling-exceeded")

    previous = _finding_identity_set(data.get("previous_unresolved_findings"))
    current = _finding_identity_set(data.get("current_unresolved_findings"))
    if previous is None or current is None:
        return _implementation_stop(profile_state, "finding-set-invalid")
    if not current.issubset(previous):
        return _implementation_stop(profile_state, "new-finding-introduced")
    if len(current) >= len(previous):
        return _implementation_stop(profile_state, "findings-not-shrinking")

    declared_paths, declared_path_stop = _reviewer_declared_affected_paths(data.get("findings"))
    if declared_path_stop is not None:
        return _implementation_stop(profile_state, declared_path_stop)
    if declared_paths is None:
        return _implementation_stop(profile_state, "affected-paths-invalid")
    top_level_paths = data.get("affected_paths")
    if top_level_paths is not None:
        top_level_path_set = _string_set(top_level_paths)
        if top_level_path_set is None:
            return _implementation_stop(profile_state, "affected-paths-invalid")
        if top_level_path_set != declared_paths:
            return _implementation_stop(profile_state, "correction-affected-paths-disagree-with-findings")

    allowed_paths = set(declared_paths)
    for key in ("approved_generated_paths", "workflow_projection_paths", "evidence_record_paths"):
        extra_paths = _string_set(data.get(key))
        if extra_paths is None:
            return _implementation_stop(profile_state, "affected-paths-invalid")
        allowed_paths.update(extra_paths)
    changed_paths = _string_set(data.get("changed_paths"))
    if changed_paths is None or not changed_paths.issubset(allowed_paths):
        return _implementation_stop(profile_state, "correction-path-out-of-scope")

    if data.get("substantive_governing_artifact_edit") is True:
        return _implementation_stop(profile_state, "governing-artifact-edit")
    scope_expansions = data.get("scope_expansions")
    if isinstance(scope_expansions, list) and scope_expansions:
        return _implementation_stop(profile_state, "scope-budget-expanded")
    if not isinstance(scope_expansions, list):
        return _implementation_stop(profile_state, "scope-budget-invalid")

    commands = _string_set(data.get("commands"))
    approved_commands = _string_set(data.get("approved_commands"))
    if commands is None or approved_commands is None or not commands.issubset(approved_commands):
        return _implementation_stop(profile_state, "unapproved-command")

    if data.get("ci_maintenance") is True:
        if data.get("ci_files_enumerated") is not True:
            return _implementation_stop(profile_state, "ci-files-not-enumerated")
        deny_hits = data.get("ci_deny_list_hits")
        if not isinstance(deny_hits, list) or deny_hits:
            return _implementation_stop(profile_state, "ci-deny-list-hit")

    if data.get("audit_recorded") is not True:
        return _implementation_stop(profile_state, "audit-record-missing")

    return _implementation_continue(profile_state, f"code-review {milestone}")


def _correction_findings_stop_reason(findings: object) -> str | None:
    if not isinstance(findings, list) or not findings:
        return "finding-set-invalid"
    for finding in findings:
        if not isinstance(finding, dict):
            return "finding-set-invalid"
        if _is_resolved_finding(finding):
            continue
        auto_fix_class = finding.get("auto_fix_class")
        if _is_empty_required_value(auto_fix_class) or auto_fix_class == "none":
            return "correction-finding-unclassified"
        if auto_fix_class not in AUTO_FIX_CLASSES:
            return "correction-finding-unknown-class"
        if auto_fix_class == "mechanical":
            for field in MECHANICAL_REQUIRED_FIELDS:
                if _is_empty_required_value(finding.get(field)):
                    return f"correction-finding-missing-{field.replace('_', '-')}"
            if finding.get("auto_fix_kind") not in MECHANICAL_AUTO_FIX_KINDS:
                return "correction-finding-unsupported-auto-fix-kind"
        if auto_fix_class == "declared-safe":
            for field in DECLARED_SAFE_REQUIRED_FIELDS:
                if _is_empty_required_value(finding.get(field)):
                    return f"correction-finding-missing-{field.replace('_', '-')}"
    return None


def _reviewer_declared_affected_paths(findings: object) -> tuple[set[str] | None, str | None]:
    if not isinstance(findings, list) or not findings:
        return None, "finding-set-invalid"
    declared_paths: set[str] = set()
    for finding in findings:
        if not isinstance(finding, dict):
            return None, "finding-set-invalid"
        if _is_resolved_finding(finding):
            continue
        affected_paths = _string_set(finding.get("affected_paths"))
        if not affected_paths:
            return None, "correction-finding-missing-affected-paths"
        declared_paths.update(affected_paths)
    if not declared_paths:
        return None, "correction-finding-missing-affected-paths"
    return declared_paths, None


def _is_resolved_finding(finding: dict[str, object]) -> bool:
    return finding.get("status") in {"resolved", "closed"}


def _is_empty_required_value(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, dict, set, tuple)):
        return not value or any(
            isinstance(item, str) and not item.strip()
            for item in value
        )
    return False


def _finding_identity_set(value: object) -> set[tuple[str, str]] | None:
    if not isinstance(value, list):
        return None
    identities: set[tuple[str, str]] = set()
    for item in value:
        if not isinstance(item, dict):
            return None
        finding_id = item.get("id")
        finding_class = item.get("class")
        if not isinstance(finding_id, str) or not isinstance(finding_class, str):
            return None
        identities.add((finding_id, finding_class))
    return identities


def _string_set(value: object) -> set[str] | None:
    if not isinstance(value, list):
        return None
    result: set[str] = set()
    for item in value:
        if not isinstance(item, str) or not item:
            return None
        result.add(item)
    return result


def _nonempty_string_list(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(item, str) and item for item in value)


def _field_values_in_status(text: str, label: str) -> tuple[list[str], list[str]]:
    status = _sections(text).get("Status", "")
    values: list[str] = []
    malformed: list[str] = []
    for line in status.splitlines():
        match = FIELD_PATTERN.match(line)
        if match is None:
            if label.casefold() in line.casefold():
                malformed.append(line.strip())
            continue
        if match.group("label").casefold() == label.casefold():
            values.append(match.group("value").strip())
    return values, malformed


def parse_plan_body_state(text: str) -> PlanBodyState:
    lifecycle_values, lifecycle_malformed = _field_values_in_status(text, "Plan lifecycle state")
    change_values, change_malformed = _field_values_in_status(text, "Change ID")
    lifecycle_errors: list[str] = []
    change_errors: list[str] = []
    lifecycle_state = lifecycle_values[0] if len(lifecycle_values) == 1 else None
    change_id = change_values[0] if len(change_values) == 1 else None

    if lifecycle_malformed or len(lifecycle_values) != 1:
        lifecycle_errors.append("Plan lifecycle state field must appear exactly once in the plan Status block")
    elif lifecycle_state not in PLAN_LIFECYCLE_STATES:
        lifecycle_errors.append(f"Plan lifecycle state has unknown value: {lifecycle_state}")

    if change_malformed or len(change_values) != 1 or not change_id:
        change_errors.append("Change ID field must appear exactly once and be non-empty in the plan Status block")

    handoff, handoff_errors = parse_handoff_summary(text)
    return PlanBodyState(
        lifecycle_state=lifecycle_state,
        change_id=change_id,
        lifecycle_errors=tuple(lifecycle_errors),
        change_id_errors=tuple(change_errors),
        handoff=handoff,
        handoff_errors=tuple(handoff_errors),
    )


def _parse_plan_index_rows(root: Path, plan_index: Path, text: str) -> tuple[list[PlanIndexRow], list[str]]:
    rows: list[PlanIndexRow] = []
    errors: list[str] = []
    sections = _sections(text)
    for section_name in ("Active", "Blocked"):
        section = sections.get(section_name)
        if section is None:
            continue
        table_lines = [line.strip() for line in section.splitlines() if line.strip().startswith("|") and line.strip().endswith("|")]
        if not table_lines:
            continue
        header = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
        if header != ["Plan", "State", "Next stage", "Change ID"]:
            errors.append(f"docs/plan.md {section_name} projection table must use columns Plan, State, Next stage, Change ID")
            continue
        for line in table_lines[2:]:
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) != 4:
                errors.append(f"docs/plan.md {section_name} projection row must contain exactly four cells")
                continue
            link = MARKDOWN_LINK_PATTERN.fullmatch(cells[0])
            if link is None or not link.group("text").strip():
                errors.append("docs/plan.md Plan cell must contain a non-empty Markdown link")
                continue
            resolved = _resolve_plan_link(root, plan_index, link.group("target"))
            if resolved is None:
                errors.append("docs/plan.md Plan cell link must resolve to a docs/plans Markdown file")
                continue
            rows.append(
                PlanIndexRow(
                    section=section_name,
                    plan_target=resolved.relative_to(root).as_posix(),
                    plan_text=link.group("text").strip(),
                    state=cells[1],
                    next_stage=_normalize_whitespace(cells[2]),
                    change_id=_strip_code(cells[3]),
                )
            )
    return rows, errors


def resolve_owners_from_index(root: Path, plan_index_path: Path) -> IndexOwnerResolution:
    if not plan_index_path.exists():
        return IndexOwnerResolution(plan_paths=(), findings=())
    rows, row_errors = _parse_plan_index_rows(root, plan_index_path, plan_index_path.read_text(encoding="utf-8"))
    findings = [StateSyncFinding(plan_index_path, message) for message in row_errors]
    plan_paths: set[Path] = set()
    for row in rows:
        if row.section.casefold() not in LIVE_INDEX_STATES:
            continue
        plan_path = (root / row.plan_target).resolve()
        if not plan_path.exists():
            findings.append(
                StateSyncFinding(
                    plan_index_path,
                    f"docs/plan.md row references nonexistent plan: {row.plan_target}",
                )
            )
            continue
        plan_text = plan_path.read_text(encoding="utf-8")
        if not has_workflow_state_handoff_section(plan_text):
            findings.append(
                StateSyncFinding(
                    plan_path,
                    "active-document-missing-handoff: active or blocked plan must contain Current Handoff Summary",
                )
            )
            continue
        plan_paths.add(plan_path)
    return IndexOwnerResolution(plan_paths=tuple(sorted(plan_paths)), findings=tuple(findings))


def _read_optional(root: Path, relative_path: str) -> str | None:
    path = root / relative_path
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def _change_yaml_id(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("change_id:"):
            return line.split(":", 1)[1].strip().strip("'\"")
    return None


def _change_yaml_artifact_plan(text: str) -> str | None:
    in_artifacts = False
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith((" ", "\t")):
            in_artifacts = line.strip() == "artifacts:"
            continue
        if in_artifacts:
            stripped = line.strip()
            if stripped.startswith("plan:"):
                return stripped.split(":", 1)[1].strip().strip("'\"")
    return None


def _validate_readiness_pointer(path: Path, text: str, handoff: HandoffSummary) -> list[StateSyncFinding]:
    readiness = _sections(text).get("Readiness")
    if readiness is None:
        return [StateSyncFinding(path, "Readiness must point to Current Handoff Summary")]
    findings: list[StateSyncFinding] = []
    if "Current Handoff Summary" not in readiness:
        findings.append(StateSyncFinding(path, "Readiness must point to Current Handoff Summary"))
    forbidden_values = {
        handoff.next_stage,
        handoff.current_milestone_state,
        handoff.final_closeout_readiness,
    }
    review_match = REVIEW_STATUS_PATTERN.fullmatch(handoff.review_status)
    if review_match is not None:
        forbidden_values.add(review_match.group("round"))
        forbidden_values.add(review_match.group("status"))
    readiness_lower = readiness.casefold()
    for value in sorted(forbidden_values):
        if value and value != "none" and value.casefold() in readiness_lower:
            findings.append(
                StateSyncFinding(
                    path,
                    f"Readiness must not restate live owner value '{value}'; point to Current Handoff Summary instead",
                )
            )
            break
    if READINESS_STAGE_CLAIM_PATTERN.search(readiness):
        findings.append(
            StateSyncFinding(
                path,
                "Readiness must not state current or stale lifecycle routing; point to Current Handoff Summary instead",
            )
        )
    return findings


def _current_milestone_projection_state(text: str, current_milestone: str) -> tuple[str | None, list[str]]:
    sections = _sections(text)
    milestones = sections.get("Milestones")
    if milestones is None:
        return None, ["Current milestone section missing: Milestones"]

    current_body: list[str] | None = None
    body: list[str] = []
    active_heading: str | None = None
    for line in milestones.splitlines():
        if line.startswith("### "):
            if active_heading == current_milestone:
                current_body = body
            active_heading = line[4:].strip()
            body = []
            continue
        if active_heading is not None:
            body.append(line)
    if active_heading == current_milestone:
        current_body = body

    if current_body is None:
        return None, [f"Current milestone section missing: {current_milestone}"]

    values: list[str] = []
    malformed: list[str] = []
    for line in current_body:
        match = FIELD_PATTERN.match(line)
        if match is None:
            if "milestone state" in line.casefold():
                malformed.append(line.strip())
            continue
        if match.group("label").casefold() == "milestone state":
            values.append(match.group("value").strip())
    if malformed or len(values) != 1:
        return None, [f"Current milestone Milestone state must appear exactly once for {current_milestone}"]
    return values[0], []


def _validate_current_milestone_projection(path: Path, text: str, handoff: HandoffSummary) -> list[StateSyncFinding]:
    projection, errors = _current_milestone_projection_state(text, handoff.current_milestone)
    findings = [StateSyncFinding(path, message) for message in errors]
    if projection is not None and projection != handoff.current_milestone_state:
        findings.append(
            StateSyncFinding(
                path,
                "Current milestone Milestone state must match Current Handoff Summary Current milestone state",
            )
        )
    return findings


def validate_workflow_state_sync(
    root: Path,
    *,
    plan_paths: tuple[Path, ...],
    plan_index_path: Path | None = None,
    change_yaml_paths: tuple[Path, ...] = (),
) -> list[StateSyncFinding]:
    findings: list[StateSyncFinding] = []
    root = root.resolve()
    plan_states: dict[Path, PlanBodyState] = {}

    for plan_path in sorted(set(path.resolve() for path in plan_paths)):
        if not plan_path.exists():
            continue
        text = plan_path.read_text(encoding="utf-8")
        state = parse_plan_body_state(text)
        plan_states[plan_path] = state
        for message in (*state.lifecycle_errors, *state.change_id_errors, *state.handoff_errors):
            findings.append(StateSyncFinding(plan_path, message))
        if state.handoff is not None:
            findings.extend(_validate_readiness_pointer(plan_path, text, state.handoff))
            findings.extend(_validate_current_milestone_projection(plan_path, text, state.handoff))

    if plan_index_path is not None and plan_index_path.exists():
        rows, row_errors = _parse_plan_index_rows(root, plan_index_path, plan_index_path.read_text(encoding="utf-8"))
        findings.extend(StateSyncFinding(plan_index_path, message) for message in row_errors)
        rows_by_target: dict[str, list[PlanIndexRow]] = {}
        change_ids: dict[str, int] = {}
        for row in rows:
            rows_by_target.setdefault(row.plan_target, []).append(row)
            if row.change_id:
                change_ids[row.change_id] = change_ids.get(row.change_id, 0) + 1
        for change_id, count in change_ids.items():
            if count > 1:
                findings.append(StateSyncFinding(plan_index_path, f"Duplicate Change ID in docs/plan.md projection: {change_id}"))
        for plan_path, state in plan_states.items():
            if state.lifecycle_state not in LIVE_INDEX_STATES:
                continue
            target = plan_path.relative_to(root).as_posix()
            matches = rows_by_target.get(target, [])
            if len(matches) != 1:
                findings.append(StateSyncFinding(plan_index_path, f"Duplicate or missing docs/plan.md projection row for {target}"))
                continue
            row = matches[0]
            if row.section.casefold() != state.lifecycle_state:
                findings.append(StateSyncFinding(plan_index_path, f"docs/plan.md section must match Plan lifecycle state for {target}"))
            if row.state != state.lifecycle_state:
                findings.append(StateSyncFinding(plan_index_path, f"docs/plan.md State must match Plan lifecycle state for {target}"))
            if state.handoff is not None and row.next_stage != _normalize_whitespace(state.handoff.next_stage):
                findings.append(StateSyncFinding(plan_index_path, f"contradictory-workflow-state: docs/plan.md Next stage must match Current Handoff Summary for {target}"))
            if state.change_id is None:
                findings.append(StateSyncFinding(plan_path, "Change ID field must appear exactly once and be non-empty in the plan Status block"))
            elif row.change_id != state.change_id:
                findings.append(StateSyncFinding(plan_index_path, f"docs/plan.md Change ID must match plan-body Change ID for {target}"))

    plan_states_by_change_id: dict[str, list[tuple[Path, PlanBodyState]]] = {}
    for plan_path, state in plan_states.items():
        if state.change_id:
            plan_states_by_change_id.setdefault(state.change_id, []).append((plan_path, state))

    for change_yaml_path in change_yaml_paths:
        if not change_yaml_path.exists():
            continue
        yaml_text = change_yaml_path.read_text(encoding="utf-8")
        yaml_id = _change_yaml_id(yaml_text)
        artifact_plan = _change_yaml_artifact_plan(yaml_text)
        review_summary = summarize_review_evidence(change_yaml_path.parent)
        matching_plan_states = plan_states_by_change_id.get(yaml_id or "", [])

        if yaml_id and change_yaml_path.parent.name != yaml_id:
            findings.append(
                StateSyncFinding(
                    change_yaml_path,
                    f"change.yaml change_id must match change directory name: {yaml_id}",
                )
            )

        if artifact_plan:
            artifact_plan_path = (root / artifact_plan).resolve()
            artifact_state = plan_states.get(artifact_plan_path)
            if artifact_state is None and artifact_plan_path.exists() and not has_workflow_state_handoff_section(
                artifact_plan_path.read_text(encoding="utf-8")
            ):
                continue
            if artifact_state is not None:
                if artifact_state.change_id is None:
                    findings.append(
                        StateSyncFinding(
                            artifact_plan_path,
                            f"Change ID field must match associated change.yaml change_id for {change_yaml_path.relative_to(root)}",
                        )
                    )
                elif yaml_id and artifact_state.change_id != yaml_id:
                    findings.append(
                        StateSyncFinding(
                            change_yaml_path,
                            f"change.yaml change_id must match plan-body Change ID for {artifact_plan_path.relative_to(root)}",
                        )
                    )

        if yaml_id and not matching_plan_states:
            if artifact_plan:
                artifact_plan_path = (root / artifact_plan).resolve()
                artifact_state = plan_states.get(artifact_plan_path)
                if artifact_state is not None:
                    matching_plan_states = [(artifact_plan_path, artifact_state)]
                elif artifact_plan_path.exists():
                    terminal_state = parse_plan_body_state(artifact_plan_path.read_text(encoding="utf-8"))
                    if terminal_state.change_id == yaml_id and terminal_state.lifecycle_state not in LIVE_INDEX_STATES:
                        continue
                    findings.append(
                        StateSyncFinding(
                            change_yaml_path,
                            f"change.yaml change_id has no matching plan-body Change ID: {yaml_id}",
                        )
                    )
                else:
                    findings.append(
                        StateSyncFinding(
                            change_yaml_path,
                            f"change.yaml change_id has no matching plan-body Change ID: {yaml_id}",
                        )
                    )
            else:
                findings.append(
                    StateSyncFinding(
                        change_yaml_path,
                        f"change.yaml change_id has no matching plan-body Change ID: {yaml_id}",
                    )
                )

        for plan_path, state in matching_plan_states:
            if review_summary.open_count and state.handoff is not None:
                if state.handoff.current_milestone_state != "resolution-needed":
                    findings.append(
                        StateSyncFinding(
                            plan_path,
                            "Current milestone state must be resolution-needed while accepted material findings remain open",
                        )
                    )
                if state.handoff.final_closeout_readiness != "not ready":
                    findings.append(
                        StateSyncFinding(
                            plan_path,
                            "Final closeout readiness must be not ready while accepted material findings remain open",
                        )
                    )
                review_match = REVIEW_STATUS_PATTERN.fullmatch(state.handoff.review_status)
                if review_match is not None and review_match.group("status") == "review-requested":
                    findings.append(
                        StateSyncFinding(
                            plan_path,
                            "Review status must not be review-requested while required finding dispositions remain unresolved",
                        )
                    )

    return findings
