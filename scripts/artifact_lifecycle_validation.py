#!/usr/bin/env python3
"""Shared validation helpers for artifact lifecycle ownership."""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from artifact_lifecycle_contracts import ArtifactContract, classify_artifact


PLACEHOLDER_PATTERN = re.compile(r"\b(TODO|TBD|lorem ipsum)\b", re.IGNORECASE)
REPO_PATH_PATTERN = re.compile(
    r"(?P<path>(?:\.\./|\.\/)?(?:docs|specs|\.codex)/[A-Za-z0-9._/\-]+(?:\.md|\.yaml))"
)
STALE_READINESS_PATTERN = re.compile(
    r"(ready for `?(proposal-review|spec-review|implement|implementation|pr|code-review)`?|"
    r"next stage should be `?(proposal-review|spec-review|implement|implementation|pr|code-review)`?)",
    re.IGNORECASE,
)
PLAN_INDEX_SECTIONS = {
    "Active": "active",
    "Blocked": "blocked",
    "Done": "done",
    "Superseded": "superseded",
}
PLAN_TERMINAL_STATUSES = frozenset({"blocked", "done", "superseded"})
PLAN_STATUS_LINE_PATTERN = re.compile(r"^\s*-\s*Status:\s*(?P<status>[A-Za-z][A-Za-z -]*)\s*$")
PLAN_INDEX_LINK_PATTERN = re.compile(r"\[[^\]]+\]\((?P<path>[^)]+)\)")
PLAN_STALE_TERMINAL_READINESS_PATTERN = re.compile(
    r"(\b(?:still|remains|is|are)\s+active\b|\bin progress\b|"
    r"\bnext (?:implementation )?milestone\b|ready for `?(?:review|pr|code-review|implement|implementation)`?)",
    re.IGNORECASE,
)
MERGE_DEPENDENT_LANGUAGE_PATTERN = re.compile(
    r"\b(after merge|post-merge|once this lands|merge-dependent)\b",
    re.IGNORECASE,
)
PLAN_NON_SCOPE_SECTIONS = frozenset(
    {
        "Milestones",
        "Progress",
        "Decision log",
        "Surprises and discoveries",
        "Validation notes",
        "Outcome and retrospective",
        "Readiness",
    }
)
PLAN_SCOPE_SECTIONS = frozenset(
    {
        "Source artifacts",
        "Pre-implementation prerequisites",
        "Related artifacts",
    }
)


@dataclass(frozen=True)
class ValidationFinding:
    severity: str
    path: Path
    artifact_class: str | None
    status: str | None
    message: str


@dataclass(frozen=True)
class ValidationResult:
    checked_artifacts: list[Path]
    blocking_findings: list[ValidationFinding]
    warning_findings: list[ValidationFinding]


@dataclass(frozen=True)
class ValidationScope:
    mode: str
    input_source: str
    tracked_revision: str | None
    changed_paths: tuple[Path, ...]
    change_yaml_paths: tuple[Path, ...]
    related_artifact_paths: tuple[Path, ...]
    baseline_paths: tuple[Path, ...]
    generated_paths: tuple[Path, ...]


class ValidationInputError(Exception):
    """Raised when validator input is incomplete or ambiguous."""


@dataclass(frozen=True)
class ArtifactInspection:
    path: Path
    contract: ArtifactContract
    status: str | None
    identifier: str | None
    errors: tuple[str, ...]


@dataclass(frozen=True)
class PlanLifecycleMarker:
    state: str | None
    disposition: str | None
    explicit: bool
    errors: tuple[str, ...]


@dataclass(frozen=True)
class PlanSurfaceEntry:
    source: Path
    section: str
    location: str
    line_number: int
    line: str
    plan_path: Path | None


def _is_relative_to(path: Path, other: Path) -> bool:
    try:
        path.relative_to(other)
        return True
    except ValueError:
        return False


def _is_generated_output_path(relative_path: Path) -> bool:
    relative = relative_path.as_posix()
    return relative.startswith(".codex/") or relative.startswith("dist/adapters/")


def _normalize_repo_path(root: Path, source_path: Path, raw_path: str) -> Path | None:
    candidate = raw_path.strip().strip("`").rstrip(").,")
    if not candidate:
        return None

    if candidate.startswith("./") or candidate.startswith("../"):
        resolved = (source_path.parent / candidate).resolve()
    else:
        resolved = (root / candidate).resolve()

    if not _is_relative_to(resolved, root):
        return None
    return resolved


def _extract_markdown_refs(root: Path, path: Path) -> set[Path]:
    return _extract_repo_path_refs_from_text(root, path, _read_repo_text(root, path))


def _extract_repo_path_refs_from_text(root: Path, path: Path, text: str) -> set[Path]:
    refs: set[Path] = set()
    for match in REPO_PATH_PATTERN.finditer(text):
        resolved = _normalize_repo_path(root, path, match.group("path"))
        if resolved is not None:
            refs.add(resolved)
    return refs


def _extract_plan_refs(root: Path, path: Path, tracked_revision: str | None = None) -> set[Path]:
    refs: set[Path] = set()
    sections = _parse_sections(_read_repo_text(root, path, tracked_revision))
    for section_name, body in sections.items():
        if section_name in PLAN_NON_SCOPE_SECTIONS:
            continue
        if section_name not in PLAN_SCOPE_SECTIONS and not section_name.startswith("Related "):
            continue
        refs.update(_extract_repo_path_refs_from_text(root, path, body))
    return {ref for ref in refs if _is_lifecycle_reference_path(root, ref)}


PLAN_LIFECYCLE_STATES = frozenset({"active", "blocked", "done", "abandoned", "superseded"})
PLAN_TERMINAL_LIFECYCLE_STATES = frozenset({"done", "abandoned", "superseded"})
PLAN_NONTERMINAL_LIFECYCLE_STATES = frozenset({"active", "blocked"})
PLAN_TERMINAL_DISPOSITIONS = frozenset({"merged", "closed", "abandoned", "superseded"})
PLAN_DISPOSITIONS = PLAN_TERMINAL_DISPOSITIONS | {"none"}
DONE_RECENT_CAP = 10
PLAN_ARCHIVE_PATH = "docs/plan-archive.md"


def _extract_plan_lifecycle_marker(text: str) -> PlanLifecycleMarker:
    status_body = _get_section(_parse_sections(text), "Status")
    if status_body is None:
        return PlanLifecycleMarker(state=None, disposition=None, explicit=False, errors=())

    state_values: list[str] = []
    disposition_values: list[str] = []
    malformed: list[str] = []
    for line in status_body.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        lowered = stripped.lower()
        if lowered.startswith("plan lifecycle state:"):
            state_values.append(stripped.split(":", 1)[1].strip().lower())
        elif lowered.startswith("terminal disposition:"):
            disposition_values.append(stripped.split(":", 1)[1].strip().lower())
        elif "plan lifecycle state" in lowered or "terminal disposition" in lowered:
            malformed.append(stripped)

    explicit = bool(state_values or disposition_values or malformed)
    if not explicit:
        return PlanLifecycleMarker(state=None, disposition=None, explicit=False, errors=())

    errors: list[str] = []
    if malformed:
        errors.append("malformed plan lifecycle-state marker field")
    if len(state_values) != 1:
        errors.append("plan lifecycle-state marker requires exactly one Plan lifecycle state field")
    if len(disposition_values) != 1:
        errors.append("plan lifecycle-state marker requires exactly one Terminal disposition field")

    state = state_values[0] if len(state_values) == 1 else None
    disposition = disposition_values[0] if len(disposition_values) == 1 else None

    if state is not None and state not in PLAN_LIFECYCLE_STATES:
        errors.append(f"unknown Plan lifecycle state: {state}")
    if disposition is not None and disposition not in PLAN_DISPOSITIONS:
        errors.append(f"unknown Terminal disposition: {disposition}")

    if state in PLAN_NONTERMINAL_LIFECYCLE_STATES and disposition != "none":
        errors.append("Terminal disposition must be none for nonterminal lifecycle state")
    if state in PLAN_TERMINAL_LIFECYCLE_STATES and disposition not in PLAN_TERMINAL_DISPOSITIONS:
        errors.append("Terminal disposition must be merged, closed, abandoned, or superseded for terminal lifecycle state")

    return PlanLifecycleMarker(
        state=state,
        disposition=disposition,
        explicit=True,
        errors=tuple(errors),
    )


def _extract_plan_body_status(text: str) -> str | None:
    marker = _extract_plan_lifecycle_marker(text)
    if marker.explicit:
        return marker.state

    section_status = _extract_status(_parse_sections(text))
    if section_status:
        return section_status.lower()

    for line in text.splitlines():
        match = PLAN_STATUS_LINE_PATTERN.match(line)
        if match:
            return match.group("status").strip().lower()
    return None


def _is_plan_body_path(root: Path, path: Path) -> bool:
    try:
        relative = path.relative_to(root).as_posix()
    except ValueError:
        return False
    return relative.startswith("docs/plans/") and relative.endswith(".md")


def _is_plan_index_path(root: Path, path: Path) -> bool:
    try:
        return path.relative_to(root).as_posix() == "docs/plan.md"
    except ValueError:
        return False


def _is_plan_archive_path(root: Path, path: Path) -> bool:
    try:
        return path.relative_to(root).as_posix() == PLAN_ARCHIVE_PATH
    except ValueError:
        return False


def _is_plan_index_surface_path(root: Path, path: Path) -> bool:
    return _is_plan_index_path(root, path) or _is_plan_archive_path(root, path)


def _section_line_offsets(text: str) -> dict[str, int]:
    offsets: dict[str, int] = {}
    for line_number, line in enumerate(text.splitlines(), start=1):
        if line.startswith("## "):
            offsets[line[3:].strip()] = line_number
    return offsets


def _normalize_plan_link(root: Path, source: Path, raw_path: str) -> Path | None:
    clean_path = raw_path.split("#", 1)[0]
    if clean_path.startswith("plans/"):
        resolved = (source.parent / clean_path).resolve()
    else:
        resolved = _normalize_repo_path(root, source, clean_path)
    if resolved is None or not _is_relative_to(resolved, root):
        return None
    return resolved if _is_plan_body_path(root, resolved) else None


def _section_location(source: Path, section: str) -> str | None:
    source_name = source.as_posix()
    if source_name.endswith("docs/plan.md"):
        normalized = section.casefold()
        if normalized == "active":
            return "active"
        if normalized == "blocked":
            return "blocked"
        if normalized in {"done", "done (recent)"}:
            return "done_recent"
        if normalized == "superseded":
            return "superseded"
    if source_name.endswith(PLAN_ARCHIVE_PATH) and section.casefold() in {"done", "done (archive)"}:
        return "done_archive"
    return None


def _parse_plan_surface_entries(
    root: Path,
    source: Path,
    tracked_revision: str | None = None,
) -> tuple[list[PlanSurfaceEntry], list[ValidationFinding]]:
    if not _path_exists(root, source, tracked_revision):
        return [], []

    text = _read_repo_text(root, source, tracked_revision)
    sections = _parse_sections(text)
    line_offsets = _section_line_offsets(text)
    entries: list[PlanSurfaceEntry] = []
    findings: list[ValidationFinding] = []

    for section, body in sections.items():
        location = _section_location(source, section)
        if location is None:
            continue
        section_start = line_offsets.get(section, 0)
        for offset, line in enumerate(body.splitlines(), start=1):
            stripped = line.strip()
            if not stripped or not stripped.startswith("- "):
                continue
            if stripped.lower() == "- none yet":
                continue

            links = list(PLAN_INDEX_LINK_PATTERN.finditer(line))
            plan_links = [
                resolved
                for match in links
                if (resolved := _normalize_plan_link(root, source, match.group("path"))) is not None
            ]
            plan_path = plan_links[0] if plan_links else None
            line_number = section_start + offset
            if location in {"done_recent", "done_archive"}:
                if plan_path is None:
                    findings.append(
                        ValidationFinding(
                            severity="block",
                            path=source,
                            artifact_class="plan-index",
                            status=None,
                            message=f"{section} terminal entry must link to an existing docs/plans file",
                        )
                    )
                elif not _path_exists(root, plan_path, tracked_revision):
                    findings.append(
                        ValidationFinding(
                            severity="block",
                            path=source,
                            artifact_class="plan-index",
                            status=None,
                            message=f"terminal entry links to missing plan file: {plan_path.relative_to(root)}",
                        )
                    )
                if len(stripped.splitlines()) != 1:
                    findings.append(
                        ValidationFinding(
                            severity="block",
                            path=source,
                            artifact_class="plan-index",
                            status=None,
                            message="terminal entries must be one-line summaries",
                        )
                    )

            entries.append(
                PlanSurfaceEntry(
                    source=source,
                    section=section,
                    location=location,
                    line_number=line_number,
                    line=line,
                    plan_path=plan_path,
                )
            )

    return entries, findings


def _parse_plan_index(root: Path, tracked_revision: str | None = None) -> dict[Path, tuple[str, ...]]:
    plan_index_path = root / "docs" / "plan.md"
    if not _path_exists(root, plan_index_path, tracked_revision):
        return {}

    entries: dict[Path, list[str]] = {}
    surface_entries, _ = _parse_plan_surface_entries(root, plan_index_path, tracked_revision)
    for entry in surface_entries:
        if entry.plan_path is None:
            continue
        if entry.location == "done_recent":
            status = "done"
        elif entry.location in {"active", "blocked", "superseded"}:
            status = entry.location
        else:
            continue
        entries.setdefault(entry.plan_path, []).append(status)
    return {path: tuple(statuses) for path, statuses in entries.items()}


def _contains_placeholder_text(text: str) -> bool:
    sanitized_lines: list[str] = []
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        sanitized_lines.append(re.sub(r"`[^`]+`", "", line))
    sanitized = "\n".join(sanitized_lines)
    return PLACEHOLDER_PATTERN.search(sanitized) is not None


def _extract_change_yaml_refs(root: Path, path: Path, tracked_revision: str | None = None) -> set[Path]:
    refs: set[Path] = set()
    lines = _read_repo_text(root, path, tracked_revision).splitlines()
    in_artifacts = False
    artifact_indent = 0

    for raw_line in lines:
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()
        if stripped == "artifacts:":
            in_artifacts = True
            artifact_indent = indent
            continue
        if in_artifacts and indent <= artifact_indent:
            break
        if not in_artifacts or ":" not in stripped:
            continue
        _, value = stripped.split(":", 1)
        resolved = _normalize_repo_path(root, path, value.strip().strip("'\""))
        if resolved is not None:
            refs.add(resolved)

    return refs


def _change_yaml_closeout_cache_findings(
    root: Path,
    path: Path,
    tracked_revision: str | None = None,
) -> list[str]:
    text = _read_repo_text(root, path, tracked_revision)
    if "schema_version: 2" not in text or "validation_events:" not in text:
        return []

    events: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_events = False
    events_indent = 0
    current_indent = 0

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()
        if stripped == "validation_events:":
            in_events = True
            events_indent = indent
            continue
        if in_events and indent <= events_indent:
            break
        if not in_events:
            continue
        if indent == events_indent + 2 and stripped.startswith("- "):
            if current is not None:
                events.append(current)
            current = {}
            current_indent = indent
            remainder = stripped[2:].strip()
            if ":" in remainder:
                key, value = remainder.split(":", 1)
                current[key.strip()] = value.strip().strip("'\"")
            continue
        if current is None or indent <= current_indent or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        key = key.strip()
        if key in {"stage", "result", "evidence_kind"}:
            current[key] = value.strip().strip("'\"")

    if current is not None:
        events.append(current)

    cache_closeout = any(
        "closeout" in event.get("stage", "").lower()
        and event.get("result") == "pass"
        and event.get("evidence_kind") == "cache-hit-inner-loop"
        for event in events
    )
    actual_closeout = any(
        "closeout" in event.get("stage", "").lower()
        and event.get("result") == "pass"
        and event.get("evidence_kind") == "actual-run-pass"
        for event in events
    )
    if cache_closeout and not actual_closeout:
        return [
            "closeout requires actual-run-pass evidence; cache-hit-inner-loop is inner-loop evidence only"
        ]
    return []


def _plan_lifecycle_candidate_paths(
    root: Path,
    scope: ValidationScope,
    index_statuses_by_path: dict[Path, tuple[str, ...]],
) -> set[Path]:
    candidates: set[Path] = set()
    plan_surface_in_scope = False
    for path in (*scope.changed_paths, *scope.related_artifact_paths):
        if _is_plan_body_path(root, path) and _path_exists(root, path, scope.tracked_revision):
            candidates.add(path)
        elif _is_plan_index_surface_path(root, path):
            plan_surface_in_scope = True

    if plan_surface_in_scope and not candidates:
        candidates.update(
            plan_path
            for plan_path in index_statuses_by_path
            if _path_exists(root, plan_path, scope.tracked_revision)
        )
    return candidates


def _all_plan_body_paths(root: Path, tracked_revision: str | None = None) -> list[Path]:
    if tracked_revision is not None:
        candidates = _tracked_markdown_paths(root, tracked_revision)
    else:
        plan_root = root / "docs" / "plans"
        candidates = list(plan_root.glob("*.md")) if plan_root.exists() else []
    return sorted(path.resolve() for path in candidates if _is_plan_body_path(root, path.resolve()))


def _plan_index_surface_in_scope(root: Path, scope: ValidationScope) -> bool:
    return any(
        _is_plan_index_surface_path(root, path)
        for path in (*scope.changed_paths, *scope.related_artifact_paths)
    )


def _explicit_terminal_plan_body_in_scope(root: Path, scope: ValidationScope) -> bool:
    for path in (*scope.changed_paths, *scope.related_artifact_paths):
        if not _is_plan_body_path(root, path) or not _path_exists(root, path, scope.tracked_revision):
            continue
        marker = _extract_plan_lifecycle_marker(_read_repo_text(root, path, scope.tracked_revision))
        if marker.explicit and marker.state in PLAN_TERMINAL_LIFECYCLE_STATES:
            return True
    return False


def _validate_plan_surface_shape(
    root: Path,
    scope: ValidationScope,
    surface_entries: list[PlanSurfaceEntry],
) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    plan_index_path = root / "docs" / "plan.md"
    archive_path = root / PLAN_ARCHIVE_PATH

    if _path_exists(root, plan_index_path, scope.tracked_revision):
        text = _read_repo_text(root, plan_index_path, scope.tracked_revision)
        sections = _parse_sections(text)
        heading_order = list(sections)
        for required in ("Active", "Blocked"):
            if not any(section.casefold() == required.casefold() for section in heading_order):
                findings.append(
                    ValidationFinding(
                        severity="block",
                        path=plan_index_path,
                        artifact_class="plan-index",
                        status=None,
                        message=f"docs/plan.md missing required {required} section",
                    )
                )
        lowered_order = [section.casefold() for section in heading_order]
        done_positions = [
            index for index, section in enumerate(lowered_order) if section in {"done", "done (recent)"}
        ]
        for live_section in ("active", "blocked"):
            if live_section in lowered_order and done_positions and lowered_order.index(live_section) > min(done_positions):
                findings.append(
                    ValidationFinding(
                        severity="block",
                        path=plan_index_path,
                        artifact_class="plan-index",
                        status=None,
                        message="Active and Blocked sections must appear before Done history",
                    )
                )
                break

        recent_entries = [entry for entry in surface_entries if entry.source == plan_index_path and entry.location == "done_recent"]
        if len(recent_entries) > DONE_RECENT_CAP:
            findings.append(
                ValidationFinding(
                    severity="block",
                    path=plan_index_path,
                    artifact_class="plan-index",
                    status=None,
                    message=f"Done (recent) exceeds approved cap of {DONE_RECENT_CAP}",
                )
            )

        archive_entries = [entry for entry in surface_entries if entry.source == archive_path and entry.location == "done_archive"]
        if archive_entries and "plan-archive.md" not in text:
            findings.append(
                ValidationFinding(
                    severity="block",
                    path=plan_index_path,
                    artifact_class="plan-index",
                    status=None,
                    message="docs/plan.md must link to docs/plan-archive.md when older terminal history exists",
                )
            )

    for entry in surface_entries:
        if entry.location != "superseded" or entry.source != plan_index_path:
            continue
        if entry.plan_path is None:
            findings.append(
                ValidationFinding(
                    severity="block",
                    path=entry.source,
                    artifact_class="plan-index",
                    status=None,
                    message="superseded entry in docs/plan.md requires a superseded plan link",
                )
            )
        if "superseded by:" not in entry.line.lower():
            findings.append(
                ValidationFinding(
                    severity="block",
                    path=entry.source,
                    artifact_class="plan-index",
                    status=None,
                    message="superseded entry in docs/plan.md requires superseded by replacement link",
                )
            )
        active_context = re.search(r"active-context:\s*(?P<value>.+)", entry.line, re.IGNORECASE)
        if active_context is None or not active_context.group("value").strip().rstrip(".;"):
            findings.append(
                ValidationFinding(
                    severity="block",
                    path=entry.source,
                    artifact_class="plan-index",
                    status=None,
                    message="superseded entry in docs/plan.md requires non-empty active-context",
                )
            )

    for entry in surface_entries:
        if entry.location == "done_archive" and "active-context:" in entry.line.lower():
            findings.append(
                ValidationFinding(
                    severity="block",
                    path=entry.source,
                    artifact_class="plan-index",
                    status=None,
                    message="archived superseded entries must not retain active-context",
                )
            )

    return findings


def _validate_terminal_plan_conservation(
    root: Path,
    scope: ValidationScope,
    surface_entries: list[PlanSurfaceEntry],
) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    if not (_plan_index_surface_in_scope(root, scope) or _explicit_terminal_plan_body_in_scope(root, scope)):
        return findings

    by_plan: dict[Path, list[PlanSurfaceEntry]] = {}
    for entry in surface_entries:
        if entry.plan_path is not None:
            by_plan.setdefault(entry.plan_path, []).append(entry)

    for plan_path in _all_plan_body_paths(root, scope.tracked_revision):
        text = _read_repo_text(root, plan_path, scope.tracked_revision)
        marker = _extract_plan_lifecycle_marker(text)
        if marker.errors:
            for error in marker.errors:
                findings.append(
                    ValidationFinding(
                        severity="block",
                        path=plan_path,
                        artifact_class="plan",
                        status=marker.state,
                        message=error,
                    )
                )
            continue
        if not marker.explicit or marker.state is None:
            continue

        entries = by_plan.get(plan_path, [])
        terminal_locations = [
            entry
            for entry in entries
            if entry.location in {"done_recent", "done_archive"}
            or (marker.state == "superseded" and entry.location == "superseded" and "active-context:" in entry.line.lower())
        ]
        archive_locations = [entry for entry in entries if entry.location == "done_archive"]
        live_locations = [entry for entry in entries if entry.location in {"active", "blocked", "superseded"}]

        if marker.state in PLAN_TERMINAL_LIFECYCLE_STATES:
            if not terminal_locations:
                findings.append(
                    ValidationFinding(
                        severity="block",
                        path=plan_path,
                        artifact_class="plan",
                        status=marker.state,
                        message="terminal plan missing from Done (recent) and Done (archive)",
                    )
                )
            elif len(terminal_locations) > 1:
                findings.append(
                    ValidationFinding(
                        severity="block",
                        path=plan_path,
                        artifact_class="plan",
                        status=marker.state,
                        message="terminal plan appears more than once across Done (recent) and Done (archive)",
                    )
                )
        elif marker.state in PLAN_NONTERMINAL_LIFECYCLE_STATES and archive_locations and not live_locations:
            findings.append(
                ValidationFinding(
                    severity="block",
                    path=plan_path,
                    artifact_class="plan",
                    status=marker.state,
                    message="nonterminal plan must not be stored only in docs/plan-archive.md",
                )
            )

    return findings


def _validate_plan_lifecycle_consistency(
    root: Path,
    scope: ValidationScope,
) -> tuple[list[ValidationFinding], list[ValidationFinding]]:
    blocking: list[ValidationFinding] = []
    warnings: list[ValidationFinding] = []
    index_statuses_by_path = _parse_plan_index(root, scope.tracked_revision)

    for plan_path in sorted(_plan_lifecycle_candidate_paths(root, scope, index_statuses_by_path)):
        text = _read_repo_text(root, plan_path, scope.tracked_revision)
        marker = _extract_plan_lifecycle_marker(text)
        if marker.errors:
            for error in marker.errors:
                blocking.append(
                    ValidationFinding(
                        severity="block",
                        path=plan_path,
                        artifact_class="plan",
                        status=marker.state,
                        message=error,
                    )
                )
            continue
        body_status = marker.state if marker.explicit else _extract_plan_body_status(text)
        index_statuses = index_statuses_by_path.get(plan_path, ())

        if body_status is None:
            continue

        if "active" in index_statuses and body_status in PLAN_TERMINAL_STATUSES:
            blocking.append(
                ValidationFinding(
                    severity="block",
                    path=plan_path,
                    artifact_class="plan",
                    status=body_status,
                    message="completed, blocked, or superseded plan must not be listed under Active",
                )
            )
        elif index_statuses and body_status not in index_statuses:
            index_label = ", ".join(index_statuses)
            blocking.append(
                ValidationFinding(
                    severity="block",
                    path=plan_path,
                    artifact_class="plan",
                    status=body_status,
                    message=f"docs/plan.md lists plan as {index_label} but plan body status is {body_status}",
                )
            )

        if body_status in PLAN_TERMINAL_STATUSES:
            sections = _parse_sections(text)
            readiness_text = "\n".join(
                section
                for section in (
                    sections.get("Outcome and Retrospective", ""),
                    sections.get("Readiness", ""),
                )
                if section
            )
            if PLAN_STALE_TERMINAL_READINESS_PATTERN.search(readiness_text):
                blocking.append(
                    ValidationFinding(
                        severity="block",
                        path=plan_path,
                        artifact_class="plan",
                        status=body_status,
                        message="terminal plan readiness still describes active or in-progress work",
                    )
                )

    return blocking, warnings


def _merge_dependent_warning_paths(root: Path, scope: ValidationScope) -> set[Path]:
    candidates: set[Path] = set()
    for path in (*scope.changed_paths, *scope.related_artifact_paths):
        if not _is_relative_to(path, root):
            continue
        relative = path.relative_to(root)
        if _is_generated_output_path(relative):
            continue
        if path.suffix not in {".md", ".yaml"}:
            continue
        if _path_exists(root, path, scope.tracked_revision):
            candidates.add(path)
    return candidates


def _validate_merge_dependent_language_warnings(root: Path, scope: ValidationScope) -> list[ValidationFinding]:
    warnings: list[ValidationFinding] = []
    for path in sorted(_merge_dependent_warning_paths(root, scope)):
        text = _read_repo_text(root, path, scope.tracked_revision)
        matches: list[tuple[int, str]] = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            match = MERGE_DEPENDENT_LANGUAGE_PATTERN.search(line)
            if match is None:
                continue
            matches.append((line_number, match.group(1)))
        if matches:
            first_line, first_match = matches[0]
            extra_count = len(matches) - 1
            suffix = f"; {extra_count} additional match(es)" if extra_count else ""
            warnings.append(
                ValidationFinding(
                    severity="warn",
                    path=path,
                    artifact_class="lifecycle-language",
                    status=None,
                    message=(
                        "merge-dependent lifecycle language requires reviewer attention "
                        f"or contributor-visible classification (first match line {first_line}: {first_match}{suffix})"
                    ),
                )
            )
    return warnings


def _parse_sections(text: str) -> dict[str, str]:
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


def _get_section(sections: dict[str, str], name: str) -> str | None:
    if name in sections:
        return sections[name]

    normalized_name = name.casefold()
    for section_name, body in sections.items():
        if section_name.casefold() == normalized_name:
            return body
    return None


def _has_section(sections: dict[str, str], name: str) -> bool:
    return _get_section(sections, name) is not None


def _extract_status(sections: dict[str, str]) -> str | None:
    raw = _get_section(sections, "Status")
    if raw is None:
        return None
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- "):
            return stripped[2:].strip()
        return stripped
    return None


def _extract_identifier(contract: ArtifactContract, relative_path: Path) -> str | None:
    if contract.class_name == "proposal":
        return relative_path.stem
    if contract.class_name == "spec":
        return relative_path.stem
    if contract.class_name == "adr":
        return relative_path.stem
    return None


def _has_replacement_pointer(text: str) -> bool:
    lowered = text.lower()
    return "superseded_by:" in lowered or "superseded by:" in lowered


def _has_terminal_closeout(sections: dict[str, str]) -> bool:
    return _has_section(sections, "Follow-on artifacts") or _has_section(sections, "Closeout")


def _is_lifecycle_reference_path(root: Path, path: Path) -> bool:
    relative = path.relative_to(root).as_posix()
    if relative.startswith("docs/proposals/"):
        return True
    if relative.startswith("docs/architecture/"):
        return True
    if relative.startswith("docs/adr/"):
        return True
    if relative.startswith("docs/plans/"):
        return True
    if relative.startswith("docs/explain/"):
        return True
    if relative.startswith("docs/changes/") and relative.endswith("/change.yaml"):
        return True
    if relative.startswith("specs/") and relative.endswith(".md"):
        return True
    return False


def _read_git_text(root: Path, tracked_revision: str, relative_path: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), "show", f"{tracked_revision}:{relative_path.as_posix()}"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def _read_repo_text(root: Path, path: Path, tracked_revision: str | None = None) -> str:
    if tracked_revision is None:
        return path.read_text(encoding="utf-8")
    return _read_git_text(root, tracked_revision, path.relative_to(root))


def _tracked_path_exists(root: Path, tracked_revision: str, relative_path: Path) -> bool:
    result = subprocess.run(
        ["git", "-C", str(root), "cat-file", "-e", f"{tracked_revision}:{relative_path.as_posix()}"],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def _path_exists(root: Path, path: Path, tracked_revision: str | None = None) -> bool:
    if tracked_revision is None:
        return path.exists()
    return _tracked_path_exists(root, tracked_revision, path.relative_to(root))


def _requires_readiness_consistency_check(contract: ArtifactContract, status: str | None) -> bool:
    if status is None:
        return False
    return status in contract.settlement_statuses or status in contract.terminal_statuses


def _validate_status_and_sections(
    path: Path,
    contract: ArtifactContract,
    sections: dict[str, str],
    text: str,
) -> tuple[list[str], str | None]:
    errors: list[str] = []
    status = _extract_status(sections)

    if status is None:
        return ["missing required Status section"], None
    if status not in contract.allowed_statuses:
        errors.append(f"invalid status '{status}' for {contract.class_name}")

    if _contains_placeholder_text(text):
        errors.append("placeholder text is not allowed")

    for section_name in contract.required_sections:
        section_body = _get_section(sections, section_name)
        if section_body is None:
            errors.append(f"missing required '{section_name}' section")
            continue
        if not section_body.strip():
            errors.append(f"required '{section_name}' section must not be empty")

    identifier = _extract_identifier(contract, path)
    if identifier and contract.identifier_pattern and not contract.identifier_pattern.fullmatch(identifier):
        errors.append(f"invalid {contract.identifier_label}: {identifier}")

    if status in contract.terminal_statuses:
        if not _has_terminal_closeout(sections):
            errors.append("terminal artifacts must include a Closeout or Follow-on artifacts section")
        follow_on = _get_section(sections, "Follow-on artifacts")
        if follow_on is not None and not follow_on.strip():
            errors.append("Follow-on artifacts section must not be empty")
        if status.lower() == "superseded" and not _has_replacement_pointer(text):
            errors.append("superseded artifacts must identify a replacement")

    next_artifacts = _get_section(sections, "Next artifacts")
    if next_artifacts is not None and not next_artifacts.strip():
        errors.append("Next artifacts section must not be empty")

    follow_on = _get_section(sections, "Follow-on artifacts")
    if follow_on is not None:
        follow_on_body = follow_on.strip()
        if not follow_on_body:
            errors.append("Follow-on artifacts section must not be empty")
        elif follow_on_body.lower() == "none yet":
            pass

    readiness = _get_section(sections, "Readiness") or ""
    if readiness and _requires_readiness_consistency_check(contract, status) and STALE_READINESS_PATTERN.search(
        readiness
    ):
        errors.append("status and readiness disagree about whether earlier pending stages remain")

    return errors, status


def _inspect_artifact(path: Path, root: Path, tracked_revision: str | None = None) -> ArtifactInspection | None:
    relative_path = path.relative_to(root)
    text = _read_repo_text(root, path, tracked_revision)
    contract = classify_artifact(relative_path, text)
    if contract is None:
        return None
    sections = _parse_sections(text)
    errors, status = _validate_status_and_sections(relative_path, contract, sections, text)
    identifier = _extract_identifier(contract, relative_path)
    return ArtifactInspection(
        path=path,
        contract=contract,
        status=status,
        identifier=identifier,
        errors=tuple(errors),
    )


def _tracked_markdown_paths(root: Path, tracked_revision: str) -> list[Path]:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-tree", "-r", "--name-only", "-z", tracked_revision],
        check=True,
        capture_output=True,
    )
    return [
        (root / entry.decode("utf-8")).resolve()
        for entry in result.stdout.split(b"\0")
        if entry and entry.decode("utf-8").endswith(".md")
    ]


def _discover_all_in_scope_artifacts(root: Path, tracked_revision: str | None = None) -> set[Path]:
    results: set[Path] = set()
    candidates = root.rglob("*.md") if tracked_revision is None else _tracked_markdown_paths(root, tracked_revision)
    for candidate in candidates:
        if not candidate.is_file():
            if tracked_revision is None:
                continue
        if not _is_relative_to(candidate.resolve(), root):
            continue
        text = _read_repo_text(root, candidate.resolve(), tracked_revision)
        relative = candidate.resolve().relative_to(root)
        if classify_artifact(relative, text) is not None:
            results.add(candidate.resolve())
    return results


def _collect_local_changed_paths(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain", "--untracked-files=all"],
        check=True,
        capture_output=True,
        text=True,
    )
    changed: list[Path] = []
    for line in result.stdout.splitlines():
        if len(line) < 4:
            continue
        raw_path = line[3:]
        if " -> " in raw_path:
            raw_path = raw_path.split(" -> ", 1)[1]
        changed.append((root / raw_path).resolve())
    return changed


def _collect_diff_paths(root: Path, diff_spec: str) -> list[Path]:
    result = subprocess.run(
        ["git", "-C", str(root), "diff", "--name-only", diff_spec],
        check=True,
        capture_output=True,
        text=True,
    )
    return [(root / line.strip()).resolve() for line in result.stdout.splitlines() if line.strip()]


def _resolve_scope(
    root: Path,
    *,
    mode: str,
    paths: list[str],
    base: str | None = None,
    head: str | None = None,
    before: str | None = None,
    after: str | None = None,
    pr_body_file: str | None = None,
) -> ValidationScope:
    tracked_revision: str | None = None
    if mode == "explicit-paths":
        if not paths:
            raise ValidationInputError("explicit-paths mode requires at least one --path")
        changed_paths = [((root / raw).resolve()) for raw in paths]
        input_source = "explicit paths"
    elif mode == "local":
        changed_paths = _collect_local_changed_paths(root)
        input_source = "local working tree"
    elif mode == "pr-ci":
        if not base or not head:
            raise ValidationInputError("pr-ci mode requires --base and --head")
        changed_paths = _collect_diff_paths(root, f"{base}...{head}")
        input_source = "explicit PR diff range"
        tracked_revision = head
    elif mode == "push-main-ci":
        if not before or not after:
            raise ValidationInputError("push-main-ci mode requires --before and --after")
        changed_paths = _collect_diff_paths(root, f"{before}..{after}")
        input_source = "explicit push diff range"
        tracked_revision = after
    else:
        raise ValidationInputError(f"unsupported mode: {mode}")

    queue: list[Path] = []
    for path in changed_paths:
        if not _path_exists(root, path, tracked_revision):
            if tracked_revision is not None:
                continue
            raise ValidationInputError(f"input path does not exist: {path.relative_to(root)}")
        queue.append(path)

    if pr_body_file:
        pr_path = (root / pr_body_file).resolve()
        if not pr_path.exists():
            raise ValidationInputError(f"PR body file does not exist: {pr_body_file}")
        queue.append(pr_path)
    else:
        pr_path = None

    visited: set[Path] = set()
    related_artifacts: set[Path] = set()
    change_yaml_paths: set[Path] = set()
    generated_paths: set[Path] = set()

    while queue:
        current = queue.pop()
        if current in visited:
            continue
        visited.add(current)

        current_revision = None if current == pr_path else tracked_revision

        if not _path_exists(root, current, current_revision):
            continue

        if not _is_relative_to(current, root):
            continue

        relative = current.relative_to(root)
        if _is_generated_output_path(relative):
            if mode == "explicit-paths":
                generated_paths.add(current)
            continue

        current_text = _read_repo_text(root, current, current_revision) if current.suffix in {".md", ".yaml"} else None
        contract = classify_artifact(relative, current_text if current.suffix == ".md" else None)
        if contract is not None:
            related_artifacts.add(current)

        if current.name == "change.yaml":
            change_yaml_paths.add(current)
            queue.extend(sorted(_extract_change_yaml_refs(root, current, current_revision)))
            continue

        relative_text = relative.as_posix()
        is_reference_surface = (
            current == pr_path
            or relative_text.startswith("docs/explain/")
            or relative_text.startswith("docs/plans/")
        )
        if current.suffix == ".md" and is_reference_surface:
            if relative_text.startswith("docs/plans/"):
                queue.extend(sorted(_extract_plan_refs(root, current, current_revision)))
            else:
                queue.extend(sorted(_extract_repo_path_refs_from_text(root, current, current_text or "")))

    baseline_paths: set[Path] = set()
    if mode != "explicit-paths":
        baseline_paths = _discover_all_in_scope_artifacts(root, tracked_revision) - related_artifacts

    return ValidationScope(
        mode=mode,
        input_source=input_source,
        tracked_revision=tracked_revision,
        changed_paths=tuple(sorted(changed_paths)),
        change_yaml_paths=tuple(sorted(change_yaml_paths)),
        related_artifact_paths=tuple(sorted(related_artifacts)),
        baseline_paths=tuple(sorted(baseline_paths)),
        generated_paths=tuple(sorted(generated_paths)),
    )


def validate_repository(
    root: Path,
    *,
    mode: str,
    paths: list[str] | None = None,
    base: str | None = None,
    head: str | None = None,
    before: str | None = None,
    after: str | None = None,
    pr_body_file: str | None = None,
) -> ValidationResult:
    scope = _resolve_scope(
        root.resolve(),
        mode=mode,
        paths=paths or [],
        base=base,
        head=head,
        before=before,
        after=after,
        pr_body_file=pr_body_file,
    )

    blocking_findings: list[ValidationFinding] = []
    warning_findings: list[ValidationFinding] = []
    root_resolved = root.resolve()
    related_paths = set(scope.related_artifact_paths)

    for path in scope.change_yaml_paths:
        for message in _change_yaml_closeout_cache_findings(
            root_resolved,
            path,
            scope.tracked_revision,
        ):
            blocking_findings.append(
                ValidationFinding(
                    severity="block",
                    path=path,
                    artifact_class="change_metadata",
                    status=None,
                    message=message,
                )
            )

    for path in scope.generated_paths:
        blocking_findings.append(
            ValidationFinding(
                severity="block",
                path=path,
                artifact_class=None,
                status=None,
                message="generated output path must not be treated as authored source of truth",
            )
        )

    inspections: dict[Path, ArtifactInspection] = {}
    for path in tuple(sorted(related_paths | set(scope.baseline_paths))):
        inspection = _inspect_artifact(path, root_resolved, scope.tracked_revision)
        if inspection is not None:
            inspections[path] = inspection

    for inspection in inspections.values():
        target_findings = blocking_findings if inspection.path in related_paths else warning_findings
        for error in inspection.errors:
            target_findings.append(
                ValidationFinding(
                    severity="block" if inspection.path in related_paths else "warn",
                    path=inspection.path,
                    artifact_class=inspection.contract.class_name,
                    status=inspection.status,
                    message=error,
                )
            )

    duplicate_groups: dict[tuple[str, str], list[ArtifactInspection]] = {}
    for inspection in inspections.values():
        if inspection.identifier is None:
            continue
        key = (inspection.contract.class_name, inspection.identifier)
        duplicate_groups.setdefault(key, []).append(inspection)

    for (artifact_class, identifier), group in duplicate_groups.items():
        if len(group) < 2:
            continue
        any_related = any(inspection.path in related_paths for inspection in group)
        target_findings = blocking_findings if any_related else warning_findings
        severity = "block" if any_related else "warn"
        for inspection in sorted(group, key=lambda item: item.path.as_posix()):
            target_findings.append(
                ValidationFinding(
                    severity=severity,
                    path=inspection.path,
                    artifact_class=artifact_class,
                    status=inspection.status,
                    message=f"duplicate {artifact_class} identifier: {identifier}",
                )
            )

    plan_blockers, plan_warnings = _validate_plan_lifecycle_consistency(root_resolved, scope)
    blocking_findings.extend(plan_blockers)
    warning_findings.extend(plan_warnings)
    if _plan_index_surface_in_scope(root_resolved, scope) or _explicit_terminal_plan_body_in_scope(root_resolved, scope):
        surface_entries: list[PlanSurfaceEntry] = []
        surface_findings: list[ValidationFinding] = []
        for surface_path in (root_resolved / "docs" / "plan.md", root_resolved / PLAN_ARCHIVE_PATH):
            entries, findings = _parse_plan_surface_entries(root_resolved, surface_path, scope.tracked_revision)
            surface_entries.extend(entries)
            surface_findings.extend(findings)
        if _plan_index_surface_in_scope(root_resolved, scope):
            blocking_findings.extend(surface_findings)
            blocking_findings.extend(_validate_plan_surface_shape(root_resolved, scope, surface_entries))
        blocking_findings.extend(_validate_terminal_plan_conservation(root_resolved, scope, surface_entries))
    warning_findings.extend(_validate_merge_dependent_language_warnings(root_resolved, scope))

    return ValidationResult(
        checked_artifacts=[path.relative_to(root_resolved) for path in scope.related_artifact_paths],
        blocking_findings=blocking_findings,
        warning_findings=warning_findings,
    )
