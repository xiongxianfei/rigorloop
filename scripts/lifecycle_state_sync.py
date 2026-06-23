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
REVIEW_STAGES = frozenset(
    {"proposal-review", "spec-review", "architecture-review", "plan-review", "code-review", "none"}
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
            malformed.append(f"{label} is derived evidence, not a Current Handoff Summary owner field")
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
    fields, errors = _parse_exact_fields(sections[matching_sections[0]], REQUIRED_HANDOFF_FIELDS)
    if errors:
        return None, errors

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
        if not has_structured_workflow_state_marker(plan_path.read_text(encoding="utf-8")):
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
                findings.append(StateSyncFinding(plan_index_path, f"docs/plan.md Next stage must match Current Handoff Summary for {target}"))
            if state.change_id is None:
                findings.append(StateSyncFinding(plan_path, "Change ID field must appear exactly once and be non-empty in the plan Status block"))
            elif row.change_id != state.change_id:
                findings.append(StateSyncFinding(plan_index_path, f"docs/plan.md Change ID must match plan-body Change ID for {target}"))

    for change_yaml_path in change_yaml_paths:
        if not change_yaml_path.exists():
            continue
        yaml_id = _change_yaml_id(change_yaml_path.read_text(encoding="utf-8"))
        review_summary = summarize_review_evidence(change_yaml_path.parent)
        for plan_path, state in plan_states.items():
            if state.change_id and yaml_id and yaml_id != state.change_id:
                findings.append(
                    StateSyncFinding(
                        change_yaml_path,
                        f"change.yaml change_id must match plan-body Change ID for {plan_path.relative_to(root)}",
                    )
                )
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
