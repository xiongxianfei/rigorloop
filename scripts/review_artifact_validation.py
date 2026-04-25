#!/usr/bin/env python3
"""Review artifact parser and structure-mode validation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


APPROVED_DISPOSITIONS = frozenset(
    {
        "accepted",
        "rejected",
        "deferred",
        "partially-accepted",
        "needs-decision",
    }
)
FORMAL_REVIEW_STAGES = frozenset(
    {
        "proposal-review",
        "spec-review",
        "architecture-review",
        "plan-review",
        "code-review",
    }
)
REVIEW_LOG_REQUIRED_FIELDS = (
    "Review ID",
    "Stage",
    "Round",
    "Status",
    "Detailed record",
    "Resolution",
    "Material findings",
    "Open findings",
)
RECONSTRUCTED_REQUIRED_FIELDS = (
    "Original review source",
    "Original review evidence",
    "Created after fixes began",
    "Loss of fidelity",
)
ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
FIELD_PATTERN = re.compile(r"^\s*(?P<label>[A-Za-z][A-Za-z0-9 /-]*):\s*(?P<value>.*)$")


@dataclass(frozen=True)
class FieldValue:
    value: str
    line: int


@dataclass(frozen=True)
class ReviewRecord:
    path: Path
    line: int
    review_id: str
    stage: str
    round: str
    reviewer: str
    target: str
    status: str
    record_mode: str | None


@dataclass(frozen=True)
class FindingRecord:
    path: Path
    line: int
    review_id: str
    finding_id: str


@dataclass(frozen=True)
class ReviewLogEntry:
    path: Path
    line: int
    review_id: str
    stage: str
    round: str
    status: str
    detailed_record: str
    resolution: str
    material_finding_ids: tuple[str, ...]
    open_finding_ids: tuple[str, ...]


@dataclass(frozen=True)
class ResolutionRecord:
    path: Path
    line: int
    finding_id: str
    disposition: str | None
    fields: dict[str, FieldValue]


@dataclass(frozen=True)
class ReviewResolution:
    path: Path
    closeout_status: str | None
    closeout_line: int | None
    entries: tuple[ResolutionRecord, ...]


@dataclass(frozen=True)
class ValidationFinding:
    path: Path
    line: int | None
    mode: str
    message: str
    review_id: str | None = None
    finding_id: str | None = None


@dataclass(frozen=True)
class ReviewArtifactValidationResult:
    change_root: Path
    mode: str
    blocking_findings: tuple[ValidationFinding, ...]
    review_count: int
    finding_count: int
    review_log_entry_count: int
    resolution_entry_count: int
    closeout_status: str | None


def validate_change_root(change_root: Path, *, mode: str = "structure") -> ReviewArtifactValidationResult:
    if mode != "structure":
        raise ValueError(f"unsupported review artifact validation mode: {mode}")

    change_root = change_root.resolve()
    findings: list[ValidationFinding] = []

    if not change_root.exists():
        findings.append(
            ValidationFinding(
                path=change_root,
                line=None,
                mode=mode,
                message="change root does not exist",
            )
        )
        return _result(change_root, mode, findings, [], [], [], None)

    reviews_dir = change_root / "reviews"
    review_log_path = change_root / "review-log.md"
    resolution_path = change_root / "review-resolution.md"

    review_records: list[ReviewRecord] = []
    finding_records: list[FindingRecord] = []
    log_entries: list[ReviewLogEntry] = []
    resolution: ReviewResolution | None = None

    if reviews_dir.exists() and not review_log_path.exists():
        findings.append(
            ValidationFinding(
                path=review_log_path,
                line=None,
                mode=mode,
                message="reviews/ exists without review-log.md",
            )
        )

    if reviews_dir.exists():
        if not reviews_dir.is_dir():
            findings.append(
                ValidationFinding(
                    path=reviews_dir,
                    line=None,
                    mode=mode,
                    message="reviews path exists but is not a directory",
                )
            )
        else:
            for review_path in sorted(reviews_dir.glob("*.md")):
                review, review_findings, parse_findings = _parse_review_file(review_path, mode)
                findings.extend(parse_findings)
                if review is not None:
                    review_records.append(review)
                    finding_records.extend(review_findings)

    if review_log_path.exists():
        log_entries, log_findings = _parse_review_log(review_log_path, mode)
        findings.extend(log_findings)

    if resolution_path.exists():
        resolution, resolution_findings = _parse_review_resolution(resolution_path, mode)
        findings.extend(resolution_findings)

    findings.extend(_validate_review_relationships(change_root, review_records, finding_records, log_entries, mode))
    findings.extend(_validate_finding_relationships(resolution_path, finding_records, resolution, mode))

    return _result(change_root, mode, findings, review_records, finding_records, log_entries, resolution)


def format_finding(finding: ValidationFinding, *, root: Path | None = None) -> str:
    path_label = _display_path(finding.path, root)
    if finding.line is not None:
        path_label = f"{path_label}:{finding.line}"
    identifiers: list[str] = []
    if finding.review_id:
        identifiers.append(f"Review ID={finding.review_id}")
    if finding.finding_id:
        identifiers.append(f"Finding ID={finding.finding_id}")
    id_text = f": {'; '.join(identifiers)}" if identifiers else ""
    return f"{path_label}: mode={finding.mode}{id_text}: {finding.message}"


def _result(
    change_root: Path,
    mode: str,
    findings: list[ValidationFinding],
    review_records: list[ReviewRecord],
    finding_records: list[FindingRecord],
    log_entries: list[ReviewLogEntry],
    resolution: ReviewResolution | None,
) -> ReviewArtifactValidationResult:
    return ReviewArtifactValidationResult(
        change_root=change_root,
        mode=mode,
        blocking_findings=tuple(findings),
        review_count=len(review_records),
        finding_count=len(finding_records),
        review_log_entry_count=len(log_entries),
        resolution_entry_count=len(resolution.entries) if resolution else 0,
        closeout_status=resolution.closeout_status if resolution else None,
    )


def _parse_review_file(
    path: Path,
    mode: str,
) -> tuple[ReviewRecord | None, list[FindingRecord], list[ValidationFinding]]:
    lines = _read_lines(path)
    fields = _collect_fields(lines)
    findings: list[ValidationFinding] = []

    review_id_values = fields.get("Review ID", [])
    if len(review_id_values) != 1:
        findings.append(
            ValidationFinding(
                path=path,
                line=review_id_values[0].line if review_id_values else None,
                mode=mode,
                message="detailed review file must contain exactly one Review ID",
            )
        )
        return None, [], findings

    review_id_field = review_id_values[0]
    review_id = review_id_field.value
    if not _is_stable_identifier(review_id):
        findings.append(
            ValidationFinding(
                path=path,
                line=review_id_field.line,
                mode=mode,
                message="Review ID must be a stable ASCII identifier with no whitespace",
                review_id=review_id,
            )
        )

    required_values: dict[str, FieldValue] = {}
    for label in ("Stage", "Round", "Reviewer", "Target", "Status"):
        value = _first_nonempty(fields, label)
        if value is None:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=review_id_field.line,
                    mode=mode,
                    message=f"missing required field {label}",
                    review_id=review_id,
                )
            )
            continue
        required_values[label] = value

    stage = required_values.get("Stage")
    if stage is not None and stage.value not in FORMAL_REVIEW_STAGES:
        findings.append(
            ValidationFinding(
                path=path,
                line=stage.line,
                mode=mode,
                message=f"unknown review stage '{stage.value}'",
                review_id=review_id,
            )
        )

    record_mode_field = _first_nonempty(fields, "Record mode")
    record_mode = record_mode_field.value if record_mode_field else None
    finding_records = _parse_finding_records(path, review_id, fields, mode, findings)

    if record_mode == "reconstructed":
        _validate_reconstructed_record(path, review_id, fields, finding_records, mode, findings)
    elif record_mode is not None:
        findings.append(
            ValidationFinding(
                path=path,
                line=record_mode_field.line if record_mode_field else review_id_field.line,
                mode=mode,
                message="unsupported Record mode",
                review_id=review_id,
            )
        )

    if len(required_values) != 5:
        return None, finding_records, findings

    return (
        ReviewRecord(
            path=path,
            line=review_id_field.line,
            review_id=review_id,
            stage=required_values["Stage"].value,
            round=required_values["Round"].value,
            reviewer=required_values["Reviewer"].value,
            target=required_values["Target"].value,
            status=required_values["Status"].value,
            record_mode=record_mode,
        ),
        finding_records,
        findings,
    )


def _parse_finding_records(
    path: Path,
    review_id: str,
    fields: dict[str, list[FieldValue]],
    mode: str,
    findings: list[ValidationFinding],
) -> list[FindingRecord]:
    records: list[FindingRecord] = []
    for finding_id_field in fields.get("Finding ID", []):
        finding_id = finding_id_field.value
        if not _is_stable_identifier(finding_id):
            findings.append(
                ValidationFinding(
                    path=path,
                    line=finding_id_field.line,
                    mode=mode,
                    message="Finding ID must be a stable ASCII identifier with no whitespace",
                    review_id=review_id,
                    finding_id=finding_id,
                )
            )
            continue
        records.append(
            FindingRecord(
                path=path,
                line=finding_id_field.line,
                review_id=review_id,
                finding_id=finding_id,
            )
        )
    return records


def _validate_reconstructed_record(
    path: Path,
    review_id: str,
    fields: dict[str, list[FieldValue]],
    finding_records: list[FindingRecord],
    mode: str,
    findings: list[ValidationFinding],
) -> None:
    for label in RECONSTRUCTED_REQUIRED_FIELDS:
        value = _first_nonempty(fields, label)
        if value is None:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=None,
                    mode=mode,
                    message=f"missing reconstructed metadata field {label}",
                    review_id=review_id,
                )
            )
            continue
        if label == "Created after fixes began" and not value.value.lower().startswith("yes"):
            findings.append(
                ValidationFinding(
                    path=path,
                    line=value.line,
                    mode=mode,
                    message="reconstructed record must state Created after fixes began: yes",
                    review_id=review_id,
                )
            )

    if not finding_records:
        findings.append(
            ValidationFinding(
                path=path,
                line=None,
                mode=mode,
                message="reconstructed record must include at least one stable Finding ID",
                review_id=review_id,
            )
        )


def _parse_review_log(path: Path, mode: str) -> tuple[list[ReviewLogEntry], list[ValidationFinding]]:
    lines = _read_lines(path)
    entries: list[ReviewLogEntry] = []
    findings: list[ValidationFinding] = []

    entry_indexes = [index for index, line in enumerate(lines) if line.strip() == "### Review entry"]
    for position, start in enumerate(entry_indexes):
        end = entry_indexes[position + 1] if position + 1 < len(entry_indexes) else len(lines)
        block_lines = lines[start:end]
        block_fields = _collect_fields(block_lines, start_line=start + 1)
        review_id_values = block_fields.get("Review ID", [])
        block_line = start + 1
        if len(review_id_values) != 1:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=block_line,
                    mode=mode,
                    message="review-log entry missing required field Review ID"
                    if not review_id_values
                    else "review-log entry must contain exactly one Review ID",
                )
            )
            continue

        review_id_field = review_id_values[0]
        review_id = review_id_field.value
        if not _is_stable_identifier(review_id):
            findings.append(
                ValidationFinding(
                    path=path,
                    line=review_id_field.line,
                    mode=mode,
                    message="Review ID must be a stable ASCII identifier with no whitespace",
                    review_id=review_id,
                )
            )

        field_values: dict[str, FieldValue] = {}
        for label in REVIEW_LOG_REQUIRED_FIELDS:
            value = _first_nonempty(block_fields, label)
            if value is None:
                findings.append(
                    ValidationFinding(
                        path=path,
                        line=block_line,
                        mode=mode,
                        message=f"review-log entry missing required field {label}",
                        review_id=review_id,
                    )
                )
                continue
            field_values[label] = value

        if len(field_values) != len(REVIEW_LOG_REQUIRED_FIELDS):
            continue

        entries.append(
            ReviewLogEntry(
                path=path,
                line=review_id_field.line,
                review_id=review_id,
                stage=field_values["Stage"].value,
                round=field_values["Round"].value,
                status=field_values["Status"].value,
                detailed_record=field_values["Detailed record"].value,
                resolution=field_values["Resolution"].value,
                material_finding_ids=_parse_id_list(field_values["Material findings"].value),
                open_finding_ids=_parse_id_list(field_values["Open findings"].value),
            )
        )

    return entries, findings


def _parse_review_resolution(
    path: Path,
    mode: str,
) -> tuple[ReviewResolution, list[ValidationFinding]]:
    lines = _read_lines(path)
    fields = _collect_fields(lines)
    findings: list[ValidationFinding] = []

    closeout_values = fields.get("Closeout status", [])
    closeout_status: str | None = None
    closeout_line: int | None = None
    if len(closeout_values) != 1:
        findings.append(
            ValidationFinding(
                path=path,
                line=closeout_values[0].line if closeout_values else None,
                mode=mode,
                message="review-resolution.md must contain exactly one Closeout status",
            )
        )
    else:
        closeout_status = closeout_values[0].value
        closeout_line = closeout_values[0].line
        if closeout_status not in {"open", "closed"}:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=closeout_line,
                    mode=mode,
                    message="invalid closeout status",
                )
            )

    entries = _parse_resolution_entries(path, lines, mode, findings)
    return ReviewResolution(path=path, closeout_status=closeout_status, closeout_line=closeout_line, entries=tuple(entries)), findings


def _parse_resolution_entries(
    path: Path,
    lines: list[str],
    mode: str,
    findings: list[ValidationFinding],
) -> list[ResolutionRecord]:
    entry_starts = [
        index
        for index, line in enumerate(lines)
        if _label_from_line(line) == "Finding ID"
    ]
    entries: list[ResolutionRecord] = []

    for position, start in enumerate(entry_starts):
        end = entry_starts[position + 1] if position + 1 < len(entry_starts) else len(lines)
        block_fields = _collect_fields(lines[start:end], start_line=start + 1)
        finding_id_values = block_fields.get("Finding ID", [])
        if len(finding_id_values) != 1:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=start + 1,
                    mode=mode,
                    message="resolution entry must contain exactly one Finding ID",
                )
            )
            continue
        finding_id_field = finding_id_values[0]
        finding_id = finding_id_field.value
        if not _is_stable_identifier(finding_id):
            findings.append(
                ValidationFinding(
                    path=path,
                    line=finding_id_field.line,
                    mode=mode,
                    message="Finding ID must be a stable ASCII identifier with no whitespace",
                    finding_id=finding_id,
                )
            )

        disposition_value = _first_nonempty(block_fields, "Disposition")
        disposition = disposition_value.value if disposition_value else None
        if disposition is None:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=finding_id_field.line,
                    mode=mode,
                    message="resolution entry missing disposition",
                    finding_id=finding_id,
                )
            )
        elif disposition not in APPROVED_DISPOSITIONS:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=disposition_value.line,
                    mode=mode,
                    message=f"unsupported disposition '{disposition}'",
                    finding_id=finding_id,
                )
            )

        entry = ResolutionRecord(
            path=path,
            line=finding_id_field.line,
            finding_id=finding_id,
            disposition=disposition,
            fields={label: values[0] for label, values in block_fields.items() if values},
        )
        _validate_resolution_entry_structure(entry, mode, findings)
        entries.append(entry)

    return entries


def _validate_resolution_entry_structure(
    entry: ResolutionRecord,
    mode: str,
    findings: list[ValidationFinding],
) -> None:
    if entry.disposition is None or entry.disposition not in APPROVED_DISPOSITIONS:
        return

    if entry.disposition == "needs-decision":
        for label, message in (
            ("Decision owner", "missing decision owner"),
            ("Decision needed", "missing decision needed"),
            ("Owning stage", "missing owning stage"),
        ):
            if not _entry_has(entry, label):
                findings.append(
                    ValidationFinding(
                        path=entry.path,
                        line=entry.line,
                        mode=mode,
                        message=message,
                        finding_id=entry.finding_id,
                    )
                )
        if not _entry_has_any(entry, ("Stop state", "Chosen action", "Final action")):
            findings.append(
                ValidationFinding(
                    path=entry.path,
                    line=entry.line,
                    mode=mode,
                    message="missing chosen action or stop state",
                    finding_id=entry.finding_id,
                )
            )
        if not _entry_has_any(entry, ("Validation target", "Expected proof")):
            findings.append(
                ValidationFinding(
                    path=entry.path,
                    line=entry.line,
                    mode=mode,
                    message="missing validation target or expected proof",
                    finding_id=entry.finding_id,
                )
            )
        return

    for label, message in (
        ("Owner", "missing owner"),
        ("Owning stage", "missing owning stage"),
        ("Rationale", "missing rationale"),
    ):
        if not _entry_has(entry, label):
            findings.append(
                ValidationFinding(
                    path=entry.path,
                    line=entry.line,
                    mode=mode,
                    message=message,
                    finding_id=entry.finding_id,
                )
            )
    if not _entry_has_any(entry, ("Chosen action", "Final action", "Stop state", "Accepted portion")):
        findings.append(
            ValidationFinding(
                path=entry.path,
                line=entry.line,
                mode=mode,
                message="missing chosen action or stop state",
                finding_id=entry.finding_id,
            )
        )
    if not _entry_has_any(entry, ("Validation target", "Expected proof")):
        findings.append(
            ValidationFinding(
                path=entry.path,
                line=entry.line,
                mode=mode,
                message="missing validation target or expected proof",
                finding_id=entry.finding_id,
            )
        )


def _validate_review_relationships(
    change_root: Path,
    review_records: list[ReviewRecord],
    finding_records: list[FindingRecord],
    log_entries: list[ReviewLogEntry],
    mode: str,
) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []

    review_by_id: dict[str, ReviewRecord] = {}
    for review in review_records:
        existing = review_by_id.get(review.review_id)
        if existing is not None:
            findings.append(
                ValidationFinding(
                    path=review.path,
                    line=review.line,
                    mode=mode,
                    message=f"duplicate Review ID also used in {existing.path.name}",
                    review_id=review.review_id,
                )
            )
        else:
            review_by_id[review.review_id] = review

    log_by_id: dict[str, ReviewLogEntry] = {}
    for entry in log_entries:
        if entry.review_id in log_by_id:
            findings.append(
                ValidationFinding(
                    path=entry.path,
                    line=entry.line,
                    mode=mode,
                    message="duplicate Review ID in review-log.md",
                    review_id=entry.review_id,
                )
            )
            continue
        log_by_id[entry.review_id] = entry

        review = review_by_id.get(entry.review_id)
        if review is None:
            findings.append(
                ValidationFinding(
                    path=entry.path,
                    line=entry.line,
                    mode=mode,
                    message="review-log references unknown Review ID",
                    review_id=entry.review_id,
                )
            )
            continue

        expected_path = review.path.relative_to(change_root).as_posix()
        if entry.detailed_record != expected_path:
            findings.append(
                ValidationFinding(
                    path=entry.path,
                    line=entry.line,
                    mode=mode,
                    message=f"Detailed record does not match review file {expected_path}",
                    review_id=entry.review_id,
                )
            )
        for label, entry_value, review_value in (
            ("Stage", entry.stage, review.stage),
            ("Round", entry.round, review.round),
            ("Status", entry.status, review.status),
        ):
            if entry_value != review_value:
                findings.append(
                    ValidationFinding(
                        path=entry.path,
                        line=entry.line,
                        mode=mode,
                        message=f"review-log {label} does not match detailed review",
                        review_id=entry.review_id,
                    )
                )

    for review in review_records:
        if review.review_id not in log_by_id:
            findings.append(
                ValidationFinding(
                    path=review.path,
                    line=review.line,
                    mode=mode,
                    message="Review ID missing from review-log.md",
                    review_id=review.review_id,
                )
            )

    findings.extend(_validate_log_finding_lists(finding_records, log_entries, mode))
    return findings


def _validate_log_finding_lists(
    finding_records: list[FindingRecord],
    log_entries: list[ReviewLogEntry],
    mode: str,
) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    finding_ids_by_review: dict[str, set[str]] = {}
    for finding in finding_records:
        finding_ids_by_review.setdefault(finding.review_id, set()).add(finding.finding_id)

    for entry in log_entries:
        expected = finding_ids_by_review.get(entry.review_id, set())
        material = set(entry.material_finding_ids)
        if material != expected:
            missing = expected - material
            unexpected = material - expected
            if missing:
                findings.append(
                    ValidationFinding(
                        path=entry.path,
                        line=entry.line,
                        mode=mode,
                        message=f"review-log Material findings missing {', '.join(sorted(missing))}",
                        review_id=entry.review_id,
                    )
                )
            if unexpected:
                findings.append(
                    ValidationFinding(
                        path=entry.path,
                        line=entry.line,
                        mode=mode,
                        message=f"review-log Material findings reference unknown Finding ID {', '.join(sorted(unexpected))}",
                        review_id=entry.review_id,
                    )
                )
        open_unknown = set(entry.open_finding_ids) - expected
        if open_unknown:
            findings.append(
                ValidationFinding(
                    path=entry.path,
                    line=entry.line,
                    mode=mode,
                    message=f"review-log Open findings reference unknown Finding ID {', '.join(sorted(open_unknown))}",
                    review_id=entry.review_id,
                )
            )
    return findings


def _validate_finding_relationships(
    resolution_path: Path,
    finding_records: list[FindingRecord],
    resolution: ReviewResolution | None,
    mode: str,
) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []

    finding_by_id: dict[str, FindingRecord] = {}
    for finding in finding_records:
        existing = finding_by_id.get(finding.finding_id)
        if existing is not None:
            findings.append(
                ValidationFinding(
                    path=finding.path,
                    line=finding.line,
                    mode=mode,
                    message=f"duplicate Finding ID also used in {existing.path.name}",
                    review_id=finding.review_id,
                    finding_id=finding.finding_id,
                )
            )
        else:
            finding_by_id[finding.finding_id] = finding

    material_ids = set(finding_by_id)
    if material_ids and resolution is None:
        findings.append(
            ValidationFinding(
                path=resolution_path,
                line=None,
                mode=mode,
                message="material findings require review-resolution.md",
            )
        )
        return findings
    if resolution is None:
        return findings

    resolution_by_id: dict[str, ResolutionRecord] = {}
    for entry in resolution.entries:
        if entry.finding_id in resolution_by_id:
            findings.append(
                ValidationFinding(
                    path=entry.path,
                    line=entry.line,
                    mode=mode,
                    message="duplicate Finding ID in review-resolution.md",
                    finding_id=entry.finding_id,
                )
            )
            continue
        resolution_by_id[entry.finding_id] = entry

        if entry.finding_id not in material_ids:
            findings.append(
                ValidationFinding(
                    path=entry.path,
                    line=entry.line,
                    mode=mode,
                    message="review-resolution.md references unknown Finding ID",
                    finding_id=entry.finding_id,
                )
            )

    for finding_id in sorted(material_ids - set(resolution_by_id)):
        finding = finding_by_id[finding_id]
        findings.append(
            ValidationFinding(
                path=resolution.path,
                line=None,
                mode=mode,
                message="material Finding ID missing from review-resolution.md",
                review_id=finding.review_id,
                finding_id=finding_id,
            )
        )

    return findings


def _read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def _collect_fields(lines: list[str], *, start_line: int = 1) -> dict[str, list[FieldValue]]:
    fields: dict[str, list[FieldValue]] = {}
    for offset, line in enumerate(lines, start=start_line):
        match = FIELD_PATTERN.match(line)
        if not match:
            continue
        label = match.group("label").strip()
        value = match.group("value").strip()
        fields.setdefault(label, []).append(FieldValue(value=value, line=offset))
    return fields


def _label_from_line(line: str) -> str | None:
    match = FIELD_PATTERN.match(line)
    if not match:
        return None
    return match.group("label").strip()


def _first_nonempty(fields: dict[str, list[FieldValue]], label: str) -> FieldValue | None:
    for value in fields.get(label, []):
        if value.value:
            return value
    return None


def _parse_id_list(raw_value: str) -> tuple[str, ...]:
    value = raw_value.strip()
    if not value or value.lower() == "none":
        return ()
    return tuple(
        part.strip().strip("`")
        for part in value.split(",")
        if part.strip() and part.strip().lower() != "none"
    )


def _is_stable_identifier(value: str) -> bool:
    return value.isascii() and ID_PATTERN.fullmatch(value) is not None


def _entry_has(entry: ResolutionRecord, label: str) -> bool:
    value = entry.fields.get(label)
    return value is not None and bool(value.value.strip())


def _entry_has_any(entry: ResolutionRecord, labels: tuple[str, ...]) -> bool:
    return any(_entry_has(entry, label) for label in labels)


def _display_path(path: Path, root: Path | None) -> str:
    if root is not None:
        try:
            return path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            pass
    return path.as_posix()
