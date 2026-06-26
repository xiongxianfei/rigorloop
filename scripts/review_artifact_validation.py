#!/usr/bin/env python3
"""Review artifact parser and structure-mode validation."""

from __future__ import annotations

import importlib.util
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from change_metadata_semantics import validate_clean_receipt_root_review_metadata


APPROVED_DISPOSITIONS = frozenset(
    {
        "accepted",
        "rejected",
        "deferred",
        "partially-accepted",
        "needs-decision",
    }
)
BLOCKING_REVIEW_STATUSES = frozenset(
    {
        "revise",
        "changes-requested",
        "blocked",
        "rethink",
        "inconclusive",
    }
)
FORMAL_REVIEW_STAGES = frozenset(
    {
        "proposal-review",
        "spec-review",
        "architecture-review",
        "plan-review",
        "test-spec-review",
        "code-review",
    }
)
TEST_SPEC_REVIEW_STATUSES = frozenset({"approved", "changes-requested", "blocked", "inconclusive"})
TEST_SPEC_REVIEW_IMMEDIATE_NEXT_STAGES = frozenset(
    {
        "test-spec revision",
        "spec revision",
        "architecture revision",
        "plan revision",
        "review-resolution",
        "implement",
        "none",
    }
)
TEST_SPEC_REVIEW_IMPLEMENTATION_HANDOFFS = frozenset({"allowed", "not-allowed"})
VALIDATION_MODES = frozenset({"structure", "closeout"})
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
FIELD_PATTERN = re.compile(r"^\s*(?P<label>[A-Za-z][A-Za-z0-9 _/-]*):\s*(?P<value>.*)$")
REVIEW_RESOLUTION_HEADING_PATTERN = re.compile(r"^\s{0,3}###\s+(?P<review_id>[A-Za-z0-9][A-Za-z0-9._-]*)\s*$")
AUTO_FIX_CLASSES = frozenset({"none", "mechanical", "declared-safe"})
INDEPENDENCE_LEVELS = frozenset({"L0", "L1", "L2", "L3"})
REVIEW_GATE_OUTCOMES = frozenset({"advance", "stop", "blocked", "inconclusive"})
REVIEW_GATE_RISK_TIERS = frozenset({"standard", "elevated", "critical-internal", "irreversible-external-action"})
ROLLOUT_MIN_STANDARD_SAMPLE_RATE = 20
ROLLOUT_MIN_STANDARD_SECOND_REVIEWS = 10
RFG_PHASE_B_MIN_APPLICABLE_SAMPLE_RATE = 10
RFG_PHASE_B_MIN_REVIEWER_AUTHORED_SAMPLE_RATE = 30
RFG_PHASE_B_MIN_NOT_APPLICABLE_SAMPLE_RATE = 5
RFG_STEADY_STATE_MIN_BASELINE_SAMPLE_RATE = 5
RFG_STEADY_STATE_MIN_REVIEWER_AUTHORED_SAMPLE_RATE = 15
# Source: specs/review-independence-and-criticality.md R1-R7, R13, AC1-AC5.
REVIEW_GATE_REQUIRED_FIELDS = (
    "Review gate outcome",
    "Native review status",
    "Independence level",
    "Reviewer context ID",
    "Context separation mechanism",
    "Risk tier",
    "Risk-tier triggers",
    "Risk-tier classifier",
    "Governing artifacts",
    "Formal criteria",
    "Initial packet inventory",
    "Prompt template version",
    "Initial packet hash",
    "Manifest owner",
    "Phase receipts",
)
NATIVE_STATUS_GATE_OUTCOMES = {
    "approved": "advance",
    "clean-with-notes": "advance",
    "changes-requested": "stop",
    "blocked": "blocked",
    "inconclusive": "inconclusive",
}
RISK_MAP_REQUIRED_FIELDS = (
    "Affected behavior",
    "Highest-impact failure modes",
    "Changed boundaries",
    "Evidence expected",
    "Areas requiring direct inspection",
    "Areas intentionally out of scope",
    "Risk classes considered",
    "Falsifiable review questions",
)
CLEAN_REVIEW_SUFFICIENCY_FIELDS = (
    "Review target identity",
    "Independence level",
    "Governing artifacts inspected",
    "Risk classes considered",
    "Adversarial hypotheses tested",
    "Direct proofs performed",
    "Validation evidence challenged",
    "Unreviewed surfaces",
    "Confidence",
    "No-finding rationale",
)
REQUIRED_PHASE_RECEIPTS = (
    "risk-map-recorded",
    "evidence-menu-released",
    "evidence-results-released",
    "verdict-recorded",
)
ORDERED_PHASE_RECEIPTS = (
    "risk-map-recorded",
    "evidence-menu-released",
    "evidence-results-released",
    "prior-findings-released",
    "verdict-recorded",
)
FORBIDDEN_AUTOMATED_REVIEW_FIELDS = frozenset(
    {
        "Author hidden reasoning",
        "Author chain-of-thought",
        "Author self-assessment",
        "Author claim",
        "Desired review outcome",
        "Autoprogression round budget",
        "Approval needed to continue",
        "Auto-fix eligibility",
        "Implementation safety narrative",
        "Prior reviewer conclusion",
        "Prior finding content",
        "Validation-result summaries",
        "Evidence menu",
        "Private chain-of-thought",
        "Hidden reasoning",
    }
)
PROHIBITED_INITIAL_PACKET_TOKENS = (
    "author hidden reasoning",
    "author chain-of-thought",
    "author self-assessment",
    "desired review outcome",
    "validation-result summaries",
    "evidence menu",
    "prior finding content",
    "auto-fix budget",
    "implementation safety narrative",
)
BOUNDED_AUTOMATED_FREEFORM_FIELDS = ("Manifest notes", "Process rationale")
CALIBRATION_RECORD_REQUIRED_FIELDS = (
    "Calibration record ID",
    "Review skill",
    "Risk tier",
    "Fixture mode",
    "Sampling phase",
    "Sample rate",
    "Standard clean outcomes independently reviewed",
    "Sample-rate reduction requested",
    "Second reviewer type",
    "Second review required",
    "Second-review disagreement",
    "Critical authority kind",
    "Critical authority satisfied",
    "Independence level",
    "Recurrence detection",
    "Novel defect detection",
    "Material disagreements",
    "Severity disagreements",
    "Evidence gaps",
    "Downstream escape",
    "False-positive rate",
    "Inconclusive rate",
    "Receipt quality",
    "Review duration",
)
CALIBRATION_RECORD_TRIGGER_FIELDS = tuple(
    label for label in CALIBRATION_RECORD_REQUIRED_FIELDS if label not in {"Risk tier", "Independence level"}
)
CALIBRATION_FIXTURE_MODES = frozenset(
    {"public-defect-class", "private-rotating-instance", "access-controlled-rotating-instance", "not-applicable"}
)
CALIBRATION_DETECTION_VALUES = frozenset({"detected", "missed", "not-applicable"})
CALIBRATION_SECOND_REVIEW_VALUES = frozenset({"none", "material-finding", "blocked", "inconclusive"})
CALIBRATION_SECOND_REVIEW_DISAGREEMENTS = frozenset({"material-finding", "blocked", "inconclusive"})
CALIBRATION_YES_NO_VALUES = frozenset({"yes", "no"})
CALIBRATION_BOOLEAN_FIELDS = (
    "Sample-rate reduction requested",
    "Second review required",
    "Automatic continuation",
    "Critical authority satisfied",
)
CALIBRATION_AUTHORITY_KINDS = frozenset({"L3", "human", "n/a"})
CALIBRATION_AUTHORITY_TIERS = {
    "critical-internal": frozenset({"L3", "human"}),
    "irreversible-external-action": frozenset({"human"}),
}
REQUIREMENT_COMPRESSION_SEED_TYPES = frozenset(
    {
        "A+B+C compressed to A+B",
        "N surfaces compressed to N-1",
        "closed enum compressed",
        "normative verbs compressed",
        "multi-surface asymmetry",
        "validator mirrors implementation",
    }
)
REQUIREMENT_COMPRESSION_SAMPLING_REASONS = frozenset(
    {
        "routine",
        "reviewer-authored-decomposition",
        "rotation-cycle",
        "escape-investigation",
    }
)
REQUIREMENT_COMPRESSION_ROTATION_TRIGGERS = frozenset(
    {
        "complete-defect-set-exposure",
        "recall-above-95-two-cycles",
        "scheduled-two-cycle-rotation",
    }
)
REQUIREMENT_COMPRESSION_AUDIT_OUTCOMES = frozenset(
    {
        "correct",
        "misclassified-should-have-applied",
        "out-of-scope",
    }
)
REQUIREMENT_COMPRESSION_REQUIRED_FIELDS = (
    "Corpus iteration ID",
    "Seed types covered",
    "Seed defect count",
    "Expected finding IDs",
    "Canonical R26 missing-recorded seed",
    "Calibration result iteration ID",
    "Sampling reason",
    "Applicable receipt sample rate",
    "Reviewer-authored decomposition sample rate",
    "Not-applicable receipt sample rate",
    "Steady-state baseline sample rate",
    "Steady-state reviewer-authored sample rate",
    "Follow-on sampling amendment",
    "Not-applicable receipts in cycle",
    "Not-applicable sampling proportional",
    "Original not-applicable reason",
    "Audit outcome",
    "Corrective action",
    "Rotation trigger",
    "Previous iteration ID",
    "Next iteration ID",
    "Rotated by",
    "Rotation date",
)
CALIBRATION_BOUNDED_FREEFORM_FIELDS = ("Evidence gaps",)
FORBIDDEN_CALIBRATION_FIELDS = frozenset(
    {
        "Calibration private reasoning",
        "Calibration chain-of-thought",
        "Reviewer private reasoning",
        "Reviewer chain-of-thought",
    }
)
MECHANICAL_AUTO_FIX_KINDS = frozenset(
    {
        "formatter-output",
        "lint-autofix",
        "generated-output-refresh",
        "exact-approved-rename",
        "unique-required-field-value",
        "mechanical-state-projection-sync",
        "deterministic-manifest-regeneration",
    }
)
# Source: specs/requirement-fidelity-gate.md R6-R11, R17d, R44g, R45c, R48.
REQUIREMENT_FIDELITY_APPLICABILITY_RESULTS = frozenset({"applicable", "not-applicable"})
REQUIREMENT_FIDELITY_GATE_MARKERS = frozenset({"required"})
REQUIREMENT_FIDELITY_OVERRIDE_DIRECTIONS = frozenset({"force-applicable", "force-not-applicable"})
REQUIREMENT_FIDELITY_NOT_APPLICABLE_REASONS = frozenset(
    {
        "change unrelated to normative contracts",
        "decomposition already accepted upstream and unchanged",
        "surfaces covered by spec-derived constants exercised in tests",
    }
)
REQUIREMENT_FIDELITY_PATH_TRIGGERS = frozenset(
    {
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
)
REQUIREMENT_FIDELITY_CATEGORY_TRIGGERS = frozenset(
    {
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
)
REQUIREMENT_FIDELITY_RECEIPT_FIELDS = (
    "Relevant spec clauses decomposed",
    "Property matrix complete",
    "Multi-surface contracts identified",
    "Validator assertions checked against spec",
    "Compressed requirement risk",
    "Requirement-fidelity no-finding rationale",
)


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
    fields: dict[str, tuple[FieldValue, ...]]


@dataclass(frozen=True)
class ReviewLogEntry:
    path: Path
    line: int
    review_id: str
    stage: str
    round: str
    status: str
    detailed_record: str
    resolution: str | None
    material_finding_ids: tuple[str, ...]
    open_finding_ids: tuple[str, ...]
    material_findings_count: int | None = None
    recording_status: str | None = None
    record_label: str = "Detailed record"


@dataclass(frozen=True)
class ResolutionRecord:
    path: Path
    line: int
    finding_id: str
    disposition: str | None
    disposition_count: int
    fields: dict[str, FieldValue]


@dataclass(frozen=True)
class ReviewResolution:
    path: Path
    closeout_status: str | None
    closeout_line: int | None
    explicit_review_closeout_ids: tuple[str, ...]
    review_ids: tuple[str, ...]
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


@dataclass(frozen=True)
class ReviewEvidenceSummary:
    material_finding_ids: tuple[str, ...]
    open_finding_ids: tuple[str, ...]

    @property
    def material_count(self) -> int:
        return len(self.material_finding_ids)

    @property
    def open_count(self) -> int:
        return len(self.open_finding_ids)

    @property
    def closed_count(self) -> int:
        return self.material_count - self.open_count


def finding_closure_state(
    finding_id: str,
    review_log: list[ReviewLogEntry] | tuple[ReviewLogEntry, ...],
    review_resolution: ReviewResolution | None,
    review_records: list[FindingRecord] | tuple[FindingRecord, ...],
) -> str:
    """Return closed only when the review-finding closeout predicate is satisfied."""
    if _finding_closure_findings(
        finding_id,
        review_log,
        review_resolution,
        review_records,
        "closeout",
    ):
        return "open"
    return "closed"


def validate_change_root(change_root: Path, *, mode: str = "structure") -> ReviewArtifactValidationResult:
    if mode not in VALIDATION_MODES:
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

    findings.extend(_validate_clean_receipt_change_metadata(change_root, finding_records, log_entries, mode))
    findings.extend(_validate_review_relationships(change_root, review_records, finding_records, log_entries, resolution, mode))
    findings.extend(_validate_finding_relationships(resolution_path, finding_records, resolution, mode))
    findings.extend(_validate_clean_receipt_resolution_absence(resolution_path, finding_records, log_entries, resolution, mode))
    if mode == "closeout":
        findings.extend(_validate_closeout(finding_records, log_entries, resolution, mode))

    return _result(change_root, mode, findings, review_records, finding_records, log_entries, resolution)


def summarize_review_evidence(change_root: Path) -> ReviewEvidenceSummary:
    """Return derived material/open finding IDs from review evidence."""
    change_root = change_root.resolve()
    material_ids: set[str] = set()
    finding_records: list[FindingRecord] = []
    log_entries: list[ReviewLogEntry] = []
    resolution: ReviewResolution | None = None

    reviews_dir = change_root / "reviews"
    if reviews_dir.is_dir():
        for review_path in sorted(reviews_dir.glob("*.md")):
            _, review_findings, _ = _parse_review_file(review_path, "structure")
            finding_records.extend(review_findings)
            for finding in review_findings:
                material_ids.add(finding.finding_id)

    review_log_path = change_root / "review-log.md"
    if review_log_path.exists():
        log_entries, _ = _parse_review_log(review_log_path, "structure")
        for entry in log_entries:
            material_ids.update(entry.material_finding_ids)

    resolution_path = change_root / "review-resolution.md"
    if resolution_path.exists():
        resolution, _ = _parse_review_resolution(resolution_path, "structure")

    open_ids = {
        finding_id
        for finding_id in material_ids
        if finding_closure_state(finding_id, log_entries, resolution, finding_records) == "open"
    }

    return ReviewEvidenceSummary(
        material_finding_ids=tuple(sorted(material_ids)),
        open_finding_ids=tuple(sorted(open_ids)),
    )


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
    finding_records = _parse_finding_records(path, review_id, lines, mode, findings)
    _validate_clean_receipt_review_fields(path, review_id, fields, mode, findings)
    _validate_automated_review_gate_fields(path, review_id, fields, mode, findings)
    _validate_requirement_fidelity_fields(path, review_id, fields, mode, findings)
    _validate_calibration_record_fields(path, review_id, fields, mode, findings)
    if stage is not None and stage.value == "test-spec-review":
        _validate_test_spec_review_result_fields(path, review_id, fields, mode, findings)
    _validate_implementation_profile_finding_fields(path, review_id, fields, finding_records, mode, findings)

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
    lines: list[str],
    mode: str,
    findings: list[ValidationFinding],
) -> list[FindingRecord]:
    records: list[FindingRecord] = []
    entry_starts = [
        index
        for index, line in enumerate(lines)
        if _label_from_line(line) == "Finding ID"
    ]
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
                    message="finding block must contain exactly one Finding ID",
                    review_id=review_id,
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
                fields={label: tuple(values) for label, values in block_fields.items()},
            )
        )
    return records


def _validate_implementation_profile_finding_fields(
    path: Path,
    review_id: str,
    file_fields: dict[str, list[FieldValue]],
    finding_records: list[FindingRecord],
    mode: str,
    findings: list[ValidationFinding],
) -> None:
    stage = _first_nonempty(file_fields, "Stage")
    if stage is None or stage.value != "code-review":
        return
    profile = _first_nonempty(file_fields, "Autoprogression profile")
    if profile is None:
        profile = _first_nonempty(file_fields, "Implementation profile")
    if profile is None or profile.value != "implementation-through-verify":
        return

    for record in finding_records:
        auto_fix_class = _finding_field(record, "auto_fix_class")
        if auto_fix_class is None:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=record.line,
                    mode=mode,
                    message="implementation-profile code-review finding missing auto_fix_class",
                    review_id=review_id,
                    finding_id=record.finding_id,
                )
            )
            continue
        if auto_fix_class.value not in AUTO_FIX_CLASSES:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=auto_fix_class.line,
                    mode=mode,
                    message=f"unsupported auto_fix_class '{auto_fix_class.value}'",
                    review_id=review_id,
                    finding_id=record.finding_id,
                )
            )
            continue
        if auto_fix_class.value == "mechanical":
            _validate_mechanical_auto_fix(path, review_id, record, mode, findings)
        if auto_fix_class.value == "declared-safe":
            _validate_declared_safe_auto_fix(path, review_id, record, mode, findings)


def _validate_mechanical_auto_fix(
    path: Path,
    review_id: str,
    record: FindingRecord,
    mode: str,
    findings: list[ValidationFinding],
) -> None:
    for label in ("auto_fix_kind", "affected_paths", "deterministic_authority", "required_validation"):
        if _finding_field(record, label) is None:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=record.line,
                    mode=mode,
                    message=f"mechanical auto-fix missing {label}",
                    review_id=review_id,
                    finding_id=record.finding_id,
                )
            )
    kind = _finding_field(record, "auto_fix_kind")
    if kind is not None and kind.value not in MECHANICAL_AUTO_FIX_KINDS:
        findings.append(
            ValidationFinding(
                path=path,
                line=kind.line,
                mode=mode,
                message=f"unsupported auto_fix_kind '{kind.value}'",
                review_id=review_id,
                finding_id=record.finding_id,
            )
        )


def _validate_declared_safe_auto_fix(
    path: Path,
    review_id: str,
    record: FindingRecord,
    mode: str,
    findings: list[ValidationFinding],
) -> None:
    for label in (
        "affected_paths",
        "resolution_recipe",
        "named_inputs",
        "named_outputs",
        "forbidden_paths",
        "acceptance_criteria",
        "required_validation_commands",
        "scope_preservation_rule",
    ):
        if _finding_field(record, label) is None:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=record.line,
                    mode=mode,
                    message=f"declared-safe auto-fix missing {label}",
                    review_id=review_id,
                    finding_id=record.finding_id,
                )
            )
    production_change = _finding_field(record, "production_code_change")
    if production_change is not None and production_change.value.lower() == "yes":
        if _finding_field(record, "behavior_test") is None and _finding_field(record, "test_spec_mapping") is None:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=production_change.line,
                    mode=mode,
                    message="declared-safe production-code change missing behavior proof",
                    review_id=review_id,
                    finding_id=record.finding_id,
                )
            )


def _validate_clean_receipt_review_fields(
    path: Path,
    review_id: str,
    fields: dict[str, list[FieldValue]],
    mode: str,
    findings: list[ValidationFinding],
) -> None:
    if _first_nonempty(fields, "Recording status") is None and _first_nonempty(fields, "Reviewed artifact") is None:
        return
    for label in ("Reviewed artifact", "Review date", "Recording status"):
        if _first_nonempty(fields, label) is None:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=None,
                    mode=mode,
                    message=f"clean receipt missing required field {label}",
                    review_id=review_id,
                )
            )
    recording_status = _first_nonempty(fields, "Recording status")
    if recording_status is not None and recording_status.value != "recorded":
        findings.append(
            ValidationFinding(
                path=path,
                line=recording_status.line,
                mode=mode,
                message="clean receipt Recording status must be recorded",
                review_id=review_id,
            )
        )


def _validate_automated_review_gate_fields(
    path: Path,
    review_id: str,
    fields: dict[str, list[FieldValue]],
    mode: str,
    findings: list[ValidationFinding],
) -> None:
    if not _is_automated_review_gate_record(fields):
        return

    for label in REVIEW_GATE_REQUIRED_FIELDS:
        if _first_nonempty(fields, label) is None:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=None,
                    mode=mode,
                    message=f"automated review gate missing required field {label}",
                    review_id=review_id,
                )
            )

    for label in RISK_MAP_REQUIRED_FIELDS:
        if _first_nonempty(fields, label) is None:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=None,
                    mode=mode,
                    message=f"risk map missing required field {label}",
                    review_id=review_id,
                )
            )

    for label in FORBIDDEN_AUTOMATED_REVIEW_FIELDS:
        value = _first_nonempty(fields, label)
        if value is not None:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=value.line,
                    mode=mode,
                    message=f"forbidden automated-review context field {label}",
                    review_id=review_id,
                )
            )

    for label in BOUNDED_AUTOMATED_FREEFORM_FIELDS:
        value = _first_nonempty(fields, label)
        if value is not None and len(value.value) > 240:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=value.line,
                    mode=mode,
                    message=f"automated review gate field {label} is too long",
                    review_id=review_id,
                )
            )

    outcome = _first_nonempty(fields, "Review gate outcome")
    if outcome is not None and outcome.value not in REVIEW_GATE_OUTCOMES:
        findings.append(
            ValidationFinding(
                path=path,
                line=outcome.line,
                mode=mode,
                message=f"unsupported review_gate_outcome '{outcome.value}'",
                review_id=review_id,
            )
        )

    native_status = _first_nonempty(fields, "Native review status")
    if native_status is not None:
        if native_status.value not in NATIVE_STATUS_GATE_OUTCOMES:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=native_status.line,
                    mode=mode,
                    message=(
                        f"unsupported native review status '{native_status.value}'; allowed values are "
                        f"{', '.join(sorted(NATIVE_STATUS_GATE_OUTCOMES))} per "
                        "specs/review-independence-and-criticality.md R12"
                    ),
                    review_id=review_id,
                )
            )
        elif outcome is not None:
            expected_outcome = NATIVE_STATUS_GATE_OUTCOMES[native_status.value]
            if outcome.value != expected_outcome:
                findings.append(
                    ValidationFinding(
                        path=path,
                        line=outcome.line,
                        mode=mode,
                        message=(
                            "R12-mismatch: Native review status "
                            f"{native_status.value} maps to review_gate_outcome {expected_outcome}, not {outcome.value}"
                        ),
                        review_id=review_id,
                    )
                )

    independence = _first_nonempty(fields, "Independence level")
    if independence is not None:
        if independence.value not in INDEPENDENCE_LEVELS:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=independence.line,
                    mode=mode,
                    message=f"unsupported independence level '{independence.value}'",
                    review_id=review_id,
                )
            )
        elif independence.value == "L0" and outcome is not None and outcome.value == "advance":
            findings.append(
                ValidationFinding(
                    path=path,
                    line=independence.line,
                    mode=mode,
                    message="automated review gate cannot advance with L0",
                    review_id=review_id,
                )
            )

    author_context = _first_nonempty(fields, "Author context ID")
    reviewer_context = _first_nonempty(fields, "Reviewer context ID")
    platform_verifiability = _first_nonempty(fields, "Platform verifiability")
    if (
        platform_verifiability is not None
        and platform_verifiability.value == "unverifiable"
        and reviewer_context is None
    ):
        findings.append(
            ValidationFinding(
                path=path,
                line=platform_verifiability.line,
                mode=mode,
                message="reviewer-context-id-required-on-unverifiable-platform",
                review_id=review_id,
            )
        )
    if author_context is not None and reviewer_context is not None and author_context.value == reviewer_context.value:
        findings.append(
            ValidationFinding(
                path=path,
                line=reviewer_context.line,
                mode=mode,
                message="reviewer_context_id must differ from author_context_id",
                review_id=review_id,
            )
        )

    author_context_excluded = _first_nonempty(fields, "Author context excluded")
    if author_context_excluded is not None and _first_nonempty(fields, "Initial packet inventory") is None:
        findings.append(
            ValidationFinding(
                path=path,
                line=author_context_excluded.line,
                mode=mode,
                message="author_context_excluded is not sufficient initial-packet proof",
                review_id=review_id,
            )
        )

    packet_inventory = _first_nonempty(fields, "Initial packet inventory")
    if packet_inventory is not None:
        _validate_initial_packet_inventory(path, review_id, packet_inventory, mode, findings)

    packet_hash = _first_nonempty(fields, "Initial packet hash")
    if packet_hash is not None and not _is_sha256_reference(packet_hash.value):
        findings.append(
            ValidationFinding(
                path=path,
                line=packet_hash.line,
                mode=mode,
                message="Initial packet hash must use sha256:<64 hex>",
                review_id=review_id,
            )
        )

    initial_packet_contains = _first_nonempty(fields, "Initial packet contains")
    if initial_packet_contains is not None:
        lower_value = initial_packet_contains.value.lower()
        for token in PROHIBITED_INITIAL_PACKET_TOKENS:
            if token in lower_value:
                findings.append(
                    ValidationFinding(
                        path=path,
                        line=initial_packet_contains.line,
                        mode=mode,
                        message=f"initial packet contains prohibited context {token}",
                        review_id=review_id,
                    )
                )

    phase_receipts = _first_nonempty(fields, "Phase receipts")
    if phase_receipts is not None:
        _validate_phase_receipts(path, review_id, phase_receipts, mode, findings)

    if _is_clean_automated_review(fields):
        for label in CLEAN_REVIEW_SUFFICIENCY_FIELDS:
            if _first_nonempty(fields, label) is None:
                findings.append(
                    ValidationFinding(
                        path=path,
                        line=None,
                        mode=mode,
                        message=f"clean sufficiency receipt missing required field {label}",
                        review_id=review_id,
                    )
                )


def _is_automated_review_gate_record(fields: dict[str, list[FieldValue]]) -> bool:
    automated = _first_nonempty(fields, "Automated review")
    if automated is not None and automated.value.lower() in {"yes", "true"}:
        return True
    return any(
        _first_nonempty(fields, label) is not None
        for label in ("Review gate outcome", "Independence level", "Initial packet hash", "Phase receipts")
    )


def _is_clean_automated_review(fields: dict[str, list[FieldValue]]) -> bool:
    clean_receipt = _first_nonempty(fields, "Clean-review sufficiency receipt")
    if clean_receipt is not None and clean_receipt.value.lower() in {"yes", "true"}:
        return True
    status = _first_nonempty(fields, "Status")
    outcome = _first_nonempty(fields, "Review gate outcome")
    return (
        status is not None
        and status.value in {"approved", "clean-with-notes"}
        and outcome is not None
        and outcome.value == "advance"
    )


def _is_requirement_fidelity_record(fields: dict[str, list[FieldValue]]) -> bool:
    return any(_first_nonempty(fields, label) is not None for label in (
        "Requirement-fidelity gate",
        "Requirement-fidelity applicability",
        "Requirement-fidelity affected paths",
        "Requirement-fidelity matched path triggers",
        "Requirement-fidelity matched category triggers",
        "Requirement-fidelity receipt",
    ))


def _validate_requirement_fidelity_fields(
    path: Path,
    review_id: str,
    fields: dict[str, list[FieldValue]],
    mode: str,
    findings: list[ValidationFinding],
) -> None:
    if not _is_requirement_fidelity_record(fields):
        return

    gate_marker = _first_nonempty(fields, "Requirement-fidelity gate")
    applicability = _first_nonempty(fields, "Requirement-fidelity applicability")
    affected_paths = _first_nonempty(fields, "Requirement-fidelity affected paths")
    path_triggers = _first_nonempty(fields, "Requirement-fidelity matched path triggers")
    category_triggers = _first_nonempty(fields, "Requirement-fidelity matched category triggers")
    review_stage = _first_nonempty(fields, "Requirement-fidelity review stage")

    if gate_marker is not None and gate_marker.value not in REQUIREMENT_FIDELITY_GATE_MARKERS:
        findings.append(
            ValidationFinding(
                path=path,
                line=gate_marker.line,
                mode=mode,
                message=f"unsupported requirement-fidelity gate marker '{gate_marker.value}'",
                review_id=review_id,
            )
        )

    for label, value in (
        ("Requirement-fidelity applicability", applicability),
        ("Requirement-fidelity affected paths", affected_paths),
        ("Requirement-fidelity matched path triggers", path_triggers),
        ("Requirement-fidelity matched category triggers", category_triggers),
        ("Requirement-fidelity review stage", review_stage),
    ):
        if value is None:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=None,
                    mode=mode,
                    message=(
                        "fidelity-applicability-missing"
                        if label == "Requirement-fidelity applicability"
                        else f"requirement-fidelity manifest missing required field {label}"
                    ),
                    review_id=review_id,
                )
            )

    applicability_value = applicability.value if applicability is not None else None
    if applicability is not None and applicability.value not in REQUIREMENT_FIDELITY_APPLICABILITY_RESULTS:
        findings.append(
            ValidationFinding(
                path=path,
                line=applicability.line,
                mode=mode,
                message=f"unsupported requirement-fidelity applicability '{applicability.value}'",
                review_id=review_id,
            )
        )

    _validate_requirement_fidelity_trigger_list(
        path,
        review_id,
        path_triggers,
        allowed_values=REQUIREMENT_FIDELITY_PATH_TRIGGERS,
        value_kind="path trigger",
        mode=mode,
        findings=findings,
    )
    _validate_requirement_fidelity_trigger_list(
        path,
        review_id,
        category_triggers,
        allowed_values=REQUIREMENT_FIDELITY_CATEGORY_TRIGGERS,
        value_kind="category trigger",
        mode=mode,
        findings=findings,
    )

    if applicability_value == "applicable" and path_triggers is not None and category_triggers is not None:
        matched_path_values = set(_split_list_field(path_triggers.value))
        matched_category_values = set(_split_list_field(category_triggers.value))
        if matched_path_values <= {"none"} and matched_category_values <= {"none"}:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=applicability.line,
                    mode=mode,
                    message="requirement-fidelity applicable manifest missing matched trigger evidence",
                    review_id=review_id,
                )
            )

    override_direction = _first_nonempty(fields, "Requirement-fidelity override direction")
    override_justification = _first_nonempty(fields, "Requirement-fidelity override justification")
    if override_direction is not None:
        if override_direction.value not in REQUIREMENT_FIDELITY_OVERRIDE_DIRECTIONS:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=override_direction.line,
                    mode=mode,
                    message=f"unsupported requirement-fidelity override direction '{override_direction.value}'",
                    review_id=review_id,
                )
            )
        if override_justification is None:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=override_direction.line,
                    mode=mode,
                    message="requirement-fidelity override missing non-empty justification",
                    review_id=review_id,
                )
            )

    not_applicable_reason = _first_nonempty(fields, "Requirement-fidelity not-applicable reason")
    if applicability_value == "not-applicable" and not_applicable_reason is None:
        findings.append(
            ValidationFinding(
                path=path,
                line=applicability.line if applicability is not None else None,
                mode=mode,
                message="requirement-fidelity not-applicable manifest missing closed reason",
                review_id=review_id,
            )
        )
    if not_applicable_reason is not None and not_applicable_reason.value not in REQUIREMENT_FIDELITY_NOT_APPLICABLE_REASONS:
        findings.append(
            ValidationFinding(
                path=path,
                line=not_applicable_reason.line,
                mode=mode,
                message=f"unsupported requirement-fidelity not-applicable reason '{not_applicable_reason.value}'",
                review_id=review_id,
            )
        )

    if applicability_value == "applicable":
        packet_order = _first_nonempty(fields, "Requirement-fidelity packet order")
        if packet_order is None:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=applicability.line if applicability is not None else None,
                    mode=mode,
                    message="requirement-fidelity applicable review missing packet order evidence",
                    review_id=review_id,
                )
            )
        else:
            order = _split_list_field(packet_order.value)
            if not order or order[0] != "spec clause":
                findings.append(
                    ValidationFinding(
                        path=path,
                        line=packet_order.line,
                        mode=mode,
                        message="requirement-fidelity packet order must start with spec clause",
                        review_id=review_id,
                    )
                )

    if applicability_value == "applicable" and _is_clean_automated_review(fields):
        receipt = _first_nonempty(fields, "Requirement-fidelity receipt")
        if receipt is None or receipt.value.lower() not in {"yes", "true"}:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=applicability.line if applicability is not None else None,
                    mode=mode,
                    message="applicable clean automated review missing requirement-fidelity receipt",
                    review_id=review_id,
                )
            )
        for label in REQUIREMENT_FIDELITY_RECEIPT_FIELDS:
            if _first_nonempty(fields, label) is None:
                findings.append(
                    ValidationFinding(
                        path=path,
                        line=None,
                        mode=mode,
                        message=f"requirement-fidelity receipt missing required field {label}",
                        review_id=review_id,
                    )
                )
        for label in (
            "Relevant spec clauses decomposed",
            "Property matrix complete",
            "Multi-surface contracts identified",
            "Validator assertions checked against spec",
        ):
            value = _first_nonempty(fields, label)
            if value is not None and value.value != "yes":
                findings.append(
                    ValidationFinding(
                        path=path,
                        line=value.line,
                        mode=mode,
                        message=f"requirement-fidelity receipt field {label} must be yes",
                        review_id=review_id,
                    )
                )
        decomposed = _first_nonempty(fields, "Relevant spec clauses decomposed")
        decomposition = _first_nonempty(fields, "Requirement-property decomposition evidence")
        if decomposed is not None and decomposed.value == "yes" and decomposition is None:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=decomposed.line,
                    mode=mode,
                    message="requirement-fidelity receipt says clauses were decomposed but decomposition evidence is missing",
                    review_id=review_id,
                )
            )


def _validate_requirement_fidelity_trigger_list(
    path: Path,
    review_id: str,
    field: FieldValue | None,
    *,
    allowed_values: frozenset[str],
    value_kind: str,
    mode: str,
    findings: list[ValidationFinding],
) -> None:
    if field is None:
        return
    for value in _split_list_field(field.value):
        if value == "none":
            continue
        if value not in allowed_values:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=field.line,
                    mode=mode,
                    message=f"unsupported requirement-fidelity {value_kind} '{value}'",
                    review_id=review_id,
                )
            )


def _validate_calibration_record_fields(
    path: Path,
    review_id: str,
    fields: dict[str, list[FieldValue]],
    mode: str,
    findings: list[ValidationFinding],
) -> None:
    if not _is_calibration_record(fields):
        return

    for label in CALIBRATION_RECORD_REQUIRED_FIELDS:
        if _first_nonempty(fields, label) is None:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=None,
                    mode=mode,
                    message=f"calibration record missing required field {label}",
                    review_id=review_id,
                )
            )

    for label in FORBIDDEN_CALIBRATION_FIELDS:
        value = _first_nonempty(fields, label)
        if value is not None:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=value.line,
                    mode=mode,
                    message=f"forbidden calibration field {label}",
                    review_id=review_id,
                )
            )

    for label in CALIBRATION_BOUNDED_FREEFORM_FIELDS:
        value = _first_nonempty(fields, label)
        if value is not None and len(value.value) > 240:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=value.line,
                    mode=mode,
                    message=f"calibration field {label} is too long",
                    review_id=review_id,
                )
            )

    review_skill = _first_nonempty(fields, "Review skill")
    if review_skill is not None and review_skill.value not in FORMAL_REVIEW_STAGES:
        findings.append(
            ValidationFinding(
                path=path,
                line=review_skill.line,
                mode=mode,
                message=f"unsupported calibration review skill '{review_skill.value}'",
                review_id=review_id,
            )
        )

    risk_tier = _first_nonempty(fields, "Risk tier")
    if risk_tier is not None and risk_tier.value not in REVIEW_GATE_RISK_TIERS:
        findings.append(
            ValidationFinding(
                path=path,
                line=risk_tier.line,
                mode=mode,
                message=f"unsupported calibration risk tier '{risk_tier.value}'",
                review_id=review_id,
            )
        )

    fixture_mode = _first_nonempty(fields, "Fixture mode")
    if fixture_mode is not None:
        if fixture_mode.value not in CALIBRATION_FIXTURE_MODES:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=fixture_mode.line,
                    mode=mode,
                    message=f"unsupported calibration fixture mode '{fixture_mode.value}'",
                    review_id=review_id,
                )
            )
        elif fixture_mode.value == "public-defect-class":
            corpus_scope = _first_nonempty(fields, "Fixture corpus scope")
            if corpus_scope is None or corpus_scope.value != "defect-class-example-not-measured-corpus":
                findings.append(
                    ValidationFinding(
                        path=path,
                        line=fixture_mode.line,
                        mode=mode,
                        message="public calibration fixture must declare defect-class-example-not-measured-corpus",
                        review_id=review_id,
                    )
                )

    for label in ("Recurrence detection", "Novel defect detection"):
        value = _first_nonempty(fields, label)
        if value is not None and value.value not in CALIBRATION_DETECTION_VALUES:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=value.line,
                    mode=mode,
                    message=f"unsupported calibration {label} '{value.value}'",
                    review_id=review_id,
                )
            )

    disagreement = _first_nonempty(fields, "Second-review disagreement")
    if disagreement is not None and disagreement.value not in CALIBRATION_SECOND_REVIEW_VALUES:
        findings.append(
            ValidationFinding(
                path=path,
                line=disagreement.line,
                mode=mode,
                message=f"unsupported second-review disagreement '{disagreement.value}'",
                review_id=review_id,
            )
        )

    downstream_escape = _first_nonempty(fields, "Downstream escape")
    if downstream_escape is not None and downstream_escape.value not in CALIBRATION_YES_NO_VALUES:
        findings.append(
            ValidationFinding(
                path=path,
                line=downstream_escape.line,
                mode=mode,
                message=f"unsupported downstream escape value '{downstream_escape.value}'",
                review_id=review_id,
            )
        )
    if downstream_escape is not None and downstream_escape.value == "yes":
        for label in ("Downstream escape stage", "Downstream escape analysis"):
            if _first_nonempty(fields, label) is None:
                findings.append(
                    ValidationFinding(
                        path=path,
                        line=downstream_escape.line,
                        mode=mode,
                        message=f"downstream escape record missing required field {label}",
                        review_id=review_id,
                    )
                )

    calibration_booleans = _parse_calibration_booleans(path, review_id, fields, mode, findings)
    _validate_calibration_critical_authority(path, review_id, fields, calibration_booleans, mode, findings)
    _validate_calibration_sampling_gates(path, review_id, fields, calibration_booleans, mode, findings)
    _validate_requirement_compression_calibration_fields(path, review_id, fields, mode, findings)


def _validate_test_spec_review_result_fields(
    path: Path,
    review_id: str,
    fields: dict[str, list[FieldValue]],
    mode: str,
    findings: list[ValidationFinding],
) -> None:
    review_status = _first_nonempty(fields, "Review status")
    immediate_next_stage = _first_nonempty(fields, "Immediate next stage")
    implementation_handoff = _first_nonempty(fields, "Implementation handoff")

    for label, value in (
        ("Review status", review_status),
        ("Immediate next stage", immediate_next_stage),
        ("Implementation handoff", implementation_handoff),
    ):
        if value is None:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=None,
                    mode=mode,
                    message=f"test-spec-review missing required result field {label}",
                    review_id=review_id,
                )
            )

    vocabulary_errors = False
    if review_status is not None and review_status.value not in TEST_SPEC_REVIEW_STATUSES:
        vocabulary_errors = True
        findings.append(
            ValidationFinding(
                path=path,
                line=review_status.line,
                mode=mode,
                message=(
                    f"unsupported test-spec-review Review status '{review_status.value}'; "
                    f"allowed values are {', '.join(sorted(TEST_SPEC_REVIEW_STATUSES))}"
                ),
                review_id=review_id,
            )
        )
    if immediate_next_stage is not None and immediate_next_stage.value not in TEST_SPEC_REVIEW_IMMEDIATE_NEXT_STAGES:
        vocabulary_errors = True
        findings.append(
            ValidationFinding(
                path=path,
                line=immediate_next_stage.line,
                mode=mode,
                message=(
                    f"unsupported test-spec-review Immediate next stage '{immediate_next_stage.value}'; "
                    f"allowed values are {', '.join(sorted(TEST_SPEC_REVIEW_IMMEDIATE_NEXT_STAGES))}"
                ),
                review_id=review_id,
            )
        )
    if implementation_handoff is not None and implementation_handoff.value not in TEST_SPEC_REVIEW_IMPLEMENTATION_HANDOFFS:
        vocabulary_errors = True
        findings.append(
            ValidationFinding(
                path=path,
                line=implementation_handoff.line,
                mode=mode,
                message=(
                    f"unsupported test-spec-review Implementation handoff '{implementation_handoff.value}'; "
                    f"allowed values are {', '.join(sorted(TEST_SPEC_REVIEW_IMPLEMENTATION_HANDOFFS))}"
                ),
                review_id=review_id,
            )
        )

    if (
        vocabulary_errors
        or review_status is None
        or immediate_next_stage is None
        or implementation_handoff is None
    ):
        return

    expected_handoff = "allowed" if review_status.value == "approved" else "not-allowed"
    if implementation_handoff.value != expected_handoff:
        findings.append(
            ValidationFinding(
                path=path,
                line=implementation_handoff.line,
                mode=mode,
                message=(
                    f"test-spec-review Review status {review_status.value} requires "
                    f"Implementation handoff: {expected_handoff}"
                ),
                review_id=review_id,
            )
        )

    allowed_next_stages_by_status = {
        "approved": {"implement"},
        "changes-requested": {"test-spec revision", "review-resolution"},
        "blocked": {"spec revision", "architecture revision", "plan revision", "none"},
        "inconclusive": {"none"},
    }
    allowed_next_stages = allowed_next_stages_by_status[review_status.value]
    if immediate_next_stage.value not in allowed_next_stages:
        findings.append(
            ValidationFinding(
                path=path,
                line=immediate_next_stage.line,
                mode=mode,
                message=(
                    f"test-spec-review Review status {review_status.value} does not allow "
                    f"Immediate next stage: {immediate_next_stage.value}"
                ),
                review_id=review_id,
            )
        )


def _is_calibration_record(fields: dict[str, list[FieldValue]]) -> bool:
    calibration_record = _first_nonempty(fields, "Calibration record")
    if calibration_record is not None and calibration_record.value.lower() in {"yes", "true"}:
        return True
    return any(_first_nonempty(fields, label) is not None for label in CALIBRATION_RECORD_TRIGGER_FIELDS)


def _parse_calibration_boolean(
    path: Path,
    review_id: str,
    field_name: str,
    field_value: FieldValue | None,
    mode: str,
    findings: list[ValidationFinding],
) -> bool | None:
    if field_value is None:
        return None
    value = field_value.value.strip().lower()
    if value not in CALIBRATION_YES_NO_VALUES:
        findings.append(
            ValidationFinding(
                path=path,
                line=field_value.line,
                mode=mode,
                message=f"calibration-control-value-invalid: {field_name} must be one of no, yes",
                review_id=review_id,
            )
        )
        return None
    return value == "yes"


def _parse_calibration_booleans(
    path: Path,
    review_id: str,
    fields: dict[str, list[FieldValue]],
    mode: str,
    findings: list[ValidationFinding],
) -> dict[str, bool | None]:
    return {
        label: _parse_calibration_boolean(path, review_id, label, _first_nonempty(fields, label), mode, findings)
        for label in CALIBRATION_BOOLEAN_FIELDS
    }


def _validate_calibration_critical_authority(
    path: Path,
    review_id: str,
    fields: dict[str, list[FieldValue]],
    booleans: dict[str, bool | None],
    mode: str,
    findings: list[ValidationFinding],
) -> None:
    risk_tier = _first_nonempty(fields, "Risk tier")
    kind = _first_nonempty(fields, "Critical authority kind")
    kind_value = kind.value if kind is not None else None
    if kind_value is not None and kind_value not in CALIBRATION_AUTHORITY_KINDS:
        findings.append(
            ValidationFinding(
                path=path,
                line=kind.line if kind is not None else None,
                mode=mode,
                message=(
                    "calibration-authority-kind-invalid: Critical authority kind "
                    f"'{kind_value}' must be one of L3, human, n/a"
                ),
                review_id=review_id,
            )
        )
        return

    if risk_tier is None or risk_tier.value not in CALIBRATION_AUTHORITY_TIERS:
        if kind_value not in {None, "n/a"}:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=kind.line if kind is not None else None,
                    mode=mode,
                    message="calibration-authority-kind-not-applicable: Critical authority kind applies only to critical tiers",
                    review_id=review_id,
                )
            )
        return

    allowed_kinds = CALIBRATION_AUTHORITY_TIERS[risk_tier.value]
    if kind_value in {None, "n/a"} or booleans.get("Critical authority satisfied") is not True:
        findings.append(
            ValidationFinding(
                path=path,
                line=kind.line if kind is not None else risk_tier.line,
                mode=mode,
                message=(
                    f"calibration-authority-missing: {risk_tier.value} requires Critical authority kind "
                    f"{', '.join(sorted(allowed_kinds))} with Critical authority satisfied: yes"
                ),
                review_id=review_id,
            )
        )
        return

    if kind_value not in allowed_kinds:
        findings.append(
            ValidationFinding(
                path=path,
                line=kind.line if kind is not None else risk_tier.line,
                mode=mode,
                message=(
                    f"calibration-authority-kind-insufficient: {risk_tier.value} does not accept "
                    f"Critical authority kind {kind_value}"
                ),
                review_id=review_id,
            )
        )


def _validate_calibration_sampling_gates(
    path: Path,
    review_id: str,
    fields: dict[str, list[FieldValue]],
    booleans: dict[str, bool | None],
    mode: str,
    findings: list[ValidationFinding],
) -> None:
    risk_tier = _first_nonempty(fields, "Risk tier")
    sampling_phase = _first_nonempty(fields, "Sampling phase")
    sample_rate = _first_nonempty(fields, "Sample rate")
    if (
        risk_tier is not None
        and risk_tier.value == "standard"
        and sampling_phase is not None
        and sampling_phase.value == "rollout"
    ):
        parsed_rate = _parse_percent(sample_rate.value) if sample_rate is not None else None
        if parsed_rate is None or parsed_rate < ROLLOUT_MIN_STANDARD_SAMPLE_RATE:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=sample_rate.line if sample_rate is not None else None,
                    mode=mode,
                    message="standard-risk rollout sample rate must be at least 20%",
                    review_id=review_id,
                )
            )
        if booleans.get("Sample-rate reduction requested") is True:
            reviewed_outcomes = _first_nonempty(fields, "Standard clean outcomes independently reviewed")
            reviewed_count = _parse_int(reviewed_outcomes.value) if reviewed_outcomes is not None else None
            if reviewed_count is None or reviewed_count < ROLLOUT_MIN_STANDARD_SECOND_REVIEWS:
                findings.append(
                    ValidationFinding(
                        path=path,
                        line=reviewed_outcomes.line if reviewed_outcomes is not None else None,
                        mode=mode,
                        message="standard-risk sampling reduction requires at least 10 independently reviewed clean outcomes",
                        review_id=review_id,
                    )
                )

    second_review_required = _first_nonempty(fields, "Second review required")
    if (
        risk_tier is not None
        and risk_tier.value == "elevated"
        and booleans.get("Second review required") is not True
    ):
        findings.append(
            ValidationFinding(
                path=path,
                line=second_review_required.line if second_review_required is not None else risk_tier.line,
                mode=mode,
                message="elevated-risk clean review requires second review at 100%",
                review_id=review_id,
            )
        )

    disagreement = _first_nonempty(fields, "Second-review disagreement")
    continuation = _first_nonempty(fields, "Automatic continuation")
    if (
        disagreement is not None
        and disagreement.value in CALIBRATION_SECOND_REVIEW_DISAGREEMENTS
        and booleans.get("Automatic continuation") is True
    ):
        findings.append(
            ValidationFinding(
                path=path,
                line=continuation.line,
                mode=mode,
                message="second-review disagreement prevents automatic continuation",
                review_id=review_id,
            )
        )


def _validate_requirement_compression_calibration_fields(
    path: Path,
    review_id: str,
    fields: dict[str, list[FieldValue]],
    mode: str,
    findings: list[ValidationFinding],
) -> None:
    family = _first_nonempty(fields, "Seeded defect family")
    if family is None:
        return
    if family.value != "requirement-compression":
        findings.append(
            ValidationFinding(
                path=path,
                line=family.line,
                mode=mode,
                message=f"unsupported seeded defect family '{family.value}'",
                review_id=review_id,
            )
        )
        return

    for label in REQUIREMENT_COMPRESSION_REQUIRED_FIELDS:
        if _first_nonempty(fields, label) is None:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=family.line,
                    mode=mode,
                    message=f"requirement-compression calibration missing required field {label}",
                    review_id=review_id,
                )
            )

    seed_types_field = _first_nonempty(fields, "Seed types covered")
    if seed_types_field is not None:
        seed_types = set(_split_list_field(seed_types_field.value))
        for seed_type in sorted(seed_types):
            if seed_type not in REQUIREMENT_COMPRESSION_SEED_TYPES:
                findings.append(
                    ValidationFinding(
                        path=path,
                        line=seed_types_field.line,
                        mode=mode,
                        message=f"unsupported requirement-compression seed type '{seed_type}'",
                        review_id=review_id,
                    )
                )
        if len(seed_types & REQUIREMENT_COMPRESSION_SEED_TYPES) < 4:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=seed_types_field.line,
                    mode=mode,
                    message="requirement-compression corpus iteration must span at least four seed types",
                    review_id=review_id,
                )
            )

    seed_count_field = _first_nonempty(fields, "Seed defect count")
    seed_count = _parse_int(seed_count_field.value) if seed_count_field is not None else None
    if seed_count is None or seed_count < 6:
        findings.append(
            ValidationFinding(
                path=path,
                line=seed_count_field.line if seed_count_field is not None else family.line,
                mode=mode,
                message="requirement-compression corpus iteration must contain at least six defects",
                review_id=review_id,
            )
        )

    canonical_r26 = _first_nonempty(fields, "Canonical R26 missing-recorded seed")
    if canonical_r26 is not None and canonical_r26.value != "yes":
        findings.append(
            ValidationFinding(
                path=path,
                line=canonical_r26.line,
                mode=mode,
                message="requirement-compression corpus must include canonical R26 missing-recorded seed",
                review_id=review_id,
            )
        )

    expected_findings = _first_nonempty(fields, "Expected finding IDs")
    if expected_findings is not None and "R26-missing-recorded" not in _split_list_field(expected_findings.value):
        findings.append(
            ValidationFinding(
                path=path,
                line=expected_findings.line,
                mode=mode,
                message="requirement-compression expected findings must include R26-missing-recorded",
                review_id=review_id,
            )
        )

    _validate_requirement_compression_closed_value(
        path,
        review_id,
        fields,
        "Sampling reason",
        REQUIREMENT_COMPRESSION_SAMPLING_REASONS,
        "sampling reason",
        mode,
        findings,
    )
    _validate_requirement_compression_closed_value(
        path,
        review_id,
        fields,
        "Audit outcome",
        REQUIREMENT_COMPRESSION_AUDIT_OUTCOMES,
        "audit outcome",
        mode,
        findings,
    )
    _validate_requirement_compression_closed_value(
        path,
        review_id,
        fields,
        "Rotation trigger",
        REQUIREMENT_COMPRESSION_ROTATION_TRIGGERS,
        "rotation trigger",
        mode,
        findings,
    )

    _validate_requirement_compression_min_percent(
        path,
        review_id,
        fields,
        "Applicable receipt sample rate",
        RFG_PHASE_B_MIN_APPLICABLE_SAMPLE_RATE,
        "applicable fidelity receipt sample rate must be at least 10% during Phase B",
        mode,
        findings,
    )
    _validate_requirement_compression_min_percent(
        path,
        review_id,
        fields,
        "Reviewer-authored decomposition sample rate",
        RFG_PHASE_B_MIN_REVIEWER_AUTHORED_SAMPLE_RATE,
        "reviewer-authored decomposition sample rate must be at least 30% during Phase B",
        mode,
        findings,
    )
    _validate_requirement_compression_min_percent(
        path,
        review_id,
        fields,
        "Not-applicable receipt sample rate",
        RFG_PHASE_B_MIN_NOT_APPLICABLE_SAMPLE_RATE,
        "not-applicable receipt sample rate must be at least 5% during Phase B",
        mode,
        findings,
    )
    _validate_requirement_compression_min_percent(
        path,
        review_id,
        fields,
        "Steady-state baseline sample rate",
        RFG_STEADY_STATE_MIN_BASELINE_SAMPLE_RATE,
        "steady-state baseline sample rate cannot drop below 5% without follow-on amendment",
        mode,
        findings,
    )
    _validate_requirement_compression_min_percent(
        path,
        review_id,
        fields,
        "Steady-state reviewer-authored sample rate",
        RFG_STEADY_STATE_MIN_REVIEWER_AUTHORED_SAMPLE_RATE,
        "steady-state reviewer-authored sample rate cannot drop below 15% without follow-on amendment",
        mode,
        findings,
    )

    not_applicable_count_field = _first_nonempty(fields, "Not-applicable receipts in cycle")
    not_applicable_count = (
        _parse_int(not_applicable_count_field.value)
        if not_applicable_count_field is not None
        else None
    )
    proportional = _first_nonempty(fields, "Not-applicable sampling proportional")
    if (
        not_applicable_count is not None
        and not_applicable_count >= 5
        and proportional is not None
        and proportional.value != "yes"
    ):
        findings.append(
            ValidationFinding(
                path=path,
                line=proportional.line,
                mode=mode,
                message="not-applicable receipt sampling must be proportional when at least five receipts exist",
                review_id=review_id,
            )
        )


def _validate_requirement_compression_closed_value(
    path: Path,
    review_id: str,
    fields: dict[str, list[FieldValue]],
    label: str,
    allowed_values: frozenset[str],
    value_kind: str,
    mode: str,
    findings: list[ValidationFinding],
) -> None:
    value = _first_nonempty(fields, label)
    if value is None or value.value in allowed_values:
        return
    findings.append(
        ValidationFinding(
            path=path,
            line=value.line,
            mode=mode,
            message=f"unsupported requirement-compression {value_kind} '{value.value}'",
            review_id=review_id,
        )
    )


def _validate_requirement_compression_min_percent(
    path: Path,
    review_id: str,
    fields: dict[str, list[FieldValue]],
    label: str,
    minimum: int,
    message: str,
    mode: str,
    findings: list[ValidationFinding],
) -> None:
    value = _first_nonempty(fields, label)
    parsed = _parse_percent(value.value) if value is not None else None
    if parsed is not None and parsed >= minimum:
        return
    findings.append(
        ValidationFinding(
            path=path,
            line=value.line if value is not None else None,
            mode=mode,
            message=message,
            review_id=review_id,
        )
    )


def _validate_initial_packet_inventory(
    path: Path,
    review_id: str,
    value: FieldValue,
    mode: str,
    findings: list[ValidationFinding],
) -> None:
    entries = [entry.strip() for entry in value.value.split(";") if entry.strip()]
    if not entries:
        findings.append(
            ValidationFinding(
                path=path,
                line=value.line,
                mode=mode,
                message="Initial packet inventory must list tracked artifact entries",
                review_id=review_id,
            )
        )
        return
    for entry in entries:
        if "@" not in entry or "#sha256:" not in entry:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=value.line,
                    mode=mode,
                    message="Initial packet inventory entries must include path@revision#sha256:<64 hex>",
                    review_id=review_id,
                )
            )
            continue
        _, hash_part = entry.rsplit("#", 1)
        if not _is_sha256_reference(hash_part):
            findings.append(
                ValidationFinding(
                    path=path,
                    line=value.line,
                    mode=mode,
                    message="Initial packet inventory entries must include path@revision#sha256:<64 hex>",
                    review_id=review_id,
                )
            )


def _validate_phase_receipts(
    path: Path,
    review_id: str,
    value: FieldValue,
    mode: str,
    findings: list[ValidationFinding],
) -> None:
    receipts = _split_list_field(value.value)
    seen: set[str] = set()
    for receipt in receipts:
        if receipt in seen:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=value.line,
                    mode=mode,
                    message=f"duplicate phase receipt {receipt}",
                    review_id=review_id,
                )
            )
        seen.add(receipt)
    for receipt in REQUIRED_PHASE_RECEIPTS:
        if receipt not in seen:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=value.line,
                    mode=mode,
                    message=f"missing phase receipt {receipt}",
                    review_id=review_id,
                )
            )
    for earlier, later in zip(ORDERED_PHASE_RECEIPTS, ORDERED_PHASE_RECEIPTS[1:]):
        if earlier in receipts and later in receipts and receipts.index(later) < receipts.index(earlier):
            findings.append(
                ValidationFinding(
                    path=path,
                    line=value.line,
                    mode=mode,
                    message=f"phase receipt {later} appears before required predecessor {earlier}",
                    review_id=review_id,
                )
            )


def _split_list_field(value: str) -> list[str]:
    return [part.strip() for part in re.split(r"\s*(?:>|,|;)\s*", value) if part.strip()]


def _parse_percent(value: str) -> int | None:
    match = re.fullmatch(r"\s*(?P<number>[0-9]+)\s*%?\s*", value)
    if match is None:
        return None
    return int(match.group("number"))


def _parse_int(value: str) -> int | None:
    match = re.fullmatch(r"\s*(?P<number>[0-9]+)\s*", value)
    if match is None:
        return None
    return int(match.group("number"))


def _is_sha256_reference(value: str) -> bool:
    return re.fullmatch(r"sha256:[0-9a-fA-F]{64}", value.strip()) is not None


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
        duplicate_resolution = len(block_fields.get("Resolution", [])) > 1
        if duplicate_resolution:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=block_fields["Resolution"][1].line,
                    mode=mode,
                    message="review-log entry must contain exactly one Resolution",
                    review_id=review_id,
                )
            )

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

        if len(field_values) != len(REVIEW_LOG_REQUIRED_FIELDS) or duplicate_resolution:
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

    table_entries, table_findings = _parse_clean_receipt_log_table(path, lines, mode)
    entries.extend(table_entries)
    findings.extend(table_findings)
    return entries, findings


def _parse_clean_receipt_log_table(
    path: Path,
    lines: list[str],
    mode: str,
) -> tuple[list[ReviewLogEntry], list[ValidationFinding]]:
    entries: list[ReviewLogEntry] = []
    findings: list[ValidationFinding] = []
    required_headers = [
        "Review ID",
        "Stage",
        "Round",
        "Reviewed artifact",
        "Record",
        "Status",
        "Material findings",
        "Recording",
    ]

    for index, line in enumerate(lines):
        cells = _markdown_table_cells(line)
        if cells != required_headers:
            continue
        if index + 2 > len(lines):
            continue
        for row_index in range(index + 2, len(lines)):
            row = _markdown_table_cells(lines[row_index])
            if not row:
                break
            if len(row) != len(required_headers):
                findings.append(
                    ValidationFinding(
                        path=path,
                        line=row_index + 1,
                        mode=mode,
                        message="clean receipt review-log row must match header column count",
                    )
                )
                continue
            values = dict(zip(required_headers, row))
            review_id = _strip_code(values["Review ID"])
            material_count_text = _strip_code(values["Material findings"])
            recording_status = _strip_code(values["Recording"])
            material_count: int | None = None
            if material_count_text.isdigit():
                material_count = int(material_count_text)
            else:
                findings.append(
                    ValidationFinding(
                        path=path,
                        line=row_index + 1,
                        mode=mode,
                        message="clean receipt Material findings must be 0",
                        review_id=review_id or None,
                    )
                )
            if material_count is not None and material_count != 0:
                findings.append(
                    ValidationFinding(
                        path=path,
                        line=row_index + 1,
                        mode=mode,
                        message="clean receipt Material findings must be 0",
                        review_id=review_id or None,
                    )
                )
            if recording_status != "recorded":
                findings.append(
                    ValidationFinding(
                        path=path,
                        line=row_index + 1,
                        mode=mode,
                        message="clean receipt Recording must be recorded",
                        review_id=review_id or None,
                    )
                )
            if not _is_stable_identifier(review_id):
                findings.append(
                    ValidationFinding(
                        path=path,
                        line=row_index + 1,
                        mode=mode,
                        message="Review ID must be a stable ASCII identifier with no whitespace",
                        review_id=review_id or None,
                    )
                )
            entries.append(
                ReviewLogEntry(
                    path=path,
                    line=row_index + 1,
                    review_id=review_id,
                    stage=_strip_code(values["Stage"]),
                    round=_strip_code(values["Round"]),
                    status=_strip_code(values["Status"]),
                    detailed_record=_strip_code(values["Record"]),
                    resolution=None,
                    material_finding_ids=(),
                    open_finding_ids=(),
                    material_findings_count=material_count,
                    recording_status=recording_status,
                    record_label="Record",
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
    explicit_closeout_ids = tuple(value.value for value in fields.get("Review closeout", []))
    for value in fields.get("Review closeout", []):
        if not _is_stable_identifier(value.value):
            findings.append(
                ValidationFinding(
                    path=path,
                    line=value.line,
                    mode=mode,
                    message="Review closeout must reference a stable Review ID",
                    review_id=value.value,
                )
            )

    return (
        ReviewResolution(
            path=path,
            closeout_status=closeout_status,
            closeout_line=closeout_line,
            explicit_review_closeout_ids=explicit_closeout_ids,
            review_ids=tuple(_parse_review_resolution_review_ids(lines)),
            entries=tuple(entries),
        ),
        findings,
    )


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

        disposition_values = block_fields.get("Disposition", [])
        disposition_value = _first_nonempty(block_fields, "Disposition")
        disposition = disposition_value.value if disposition_value else None
        if len(disposition_values) > 1:
            findings.append(
                ValidationFinding(
                    path=path,
                    line=disposition_values[1].line,
                    mode=mode,
                    message="resolution entry must contain exactly one Disposition",
                    finding_id=finding_id,
                )
            )
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
            disposition_count=len(disposition_values),
            fields={label: values[0] for label, values in block_fields.items() if values},
        )
        _validate_resolution_entry_structure(entry, mode, findings)
        entries.append(entry)

    return entries


def _parse_review_resolution_review_ids(lines: list[str]) -> list[str]:
    review_ids: list[str] = []
    for line in lines:
        match = REVIEW_RESOLUTION_HEADING_PATTERN.match(line)
        if match:
            review_ids.append(match.group("review_id"))
    return review_ids


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
    resolution: ReviewResolution | None,
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
                    message=f"{entry.record_label} does not match review file {expected_path}",
                    review_id=entry.review_id,
                )
            )
        if entry.resolution is not None:
            expected_resolution = f"review-resolution.md#{entry.review_id}"
            if entry.resolution != expected_resolution:
                findings.append(
                    ValidationFinding(
                        path=entry.path,
                        line=entry.line,
                        mode=mode,
                        message="Resolution must be review-resolution.md#<Review ID>",
                        review_id=entry.review_id,
                    )
                )
            elif resolution is not None and entry.review_id not in set(resolution.review_ids):
                findings.append(
                    ValidationFinding(
                        path=entry.path,
                        line=entry.line,
                        mode=mode,
                        message="Resolution Review ID not found in review-resolution.md",
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


def _validate_clean_receipt_resolution_absence(
    resolution_path: Path,
    finding_records: list[FindingRecord],
    log_entries: list[ReviewLogEntry],
    resolution: ReviewResolution | None,
    mode: str,
) -> list[ValidationFinding]:
    if resolution is None or finding_records:
        return []
    if not any(entry.recording_status == "recorded" for entry in log_entries):
        return []
    return [
        ValidationFinding(
            path=resolution_path,
            line=resolution.closeout_line,
            mode=mode,
            message="clean receipt root must not include review-resolution.md without material findings",
        )
    ]


def _validate_clean_receipt_change_metadata(
    change_root: Path,
    finding_records: list[FindingRecord],
    log_entries: list[ReviewLogEntry],
    mode: str,
) -> list[ValidationFinding]:
    if finding_records:
        return []
    if not any(entry.recording_status == "recorded" for entry in log_entries):
        return []

    metadata_path = change_root / "change.yaml"
    if not metadata_path.exists():
        return [
            ValidationFinding(
                path=metadata_path,
                line=None,
                mode=mode,
                message="change.yaml is required for clean receipt roots",
            )
        ]

    try:
        metadata = _load_change_metadata(metadata_path)
    except Exception as exc:  # noqa: BLE001 - preserve parser detail as validator evidence.
        return [
            ValidationFinding(
                path=metadata_path,
                line=None,
                mode=mode,
                message=f"change.yaml could not be parsed: {exc}",
            )
        ]

    return [
        ValidationFinding(path=metadata_path, line=None, mode=mode, message=message)
        for message in validate_clean_receipt_root_review_metadata(
            metadata,
            require_clean_receipt_root=True,
        )
    ]


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


def _validate_closeout(
    finding_records: list[FindingRecord],
    log_entries: list[ReviewLogEntry],
    resolution: ReviewResolution | None,
    mode: str,
) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []

    if resolution is not None and resolution.closeout_status != "closed":
        findings.append(
            ValidationFinding(
                path=resolution.path,
                line=resolution.closeout_line,
                mode=mode,
                message="Closeout status must be closed",
            )
        )

    material_ids = _material_finding_ids(finding_records, log_entries)
    for finding_id in sorted(material_ids):
        findings.extend(_finding_closure_findings(finding_id, log_entries, resolution, finding_records, mode))
    findings.extend(_validate_blocking_review_closeout(log_entries, resolution, mode))
    return findings


def _material_finding_ids(
    finding_records: list[FindingRecord] | tuple[FindingRecord, ...],
    log_entries: list[ReviewLogEntry] | tuple[ReviewLogEntry, ...],
) -> set[str]:
    material_ids = {finding.finding_id for finding in finding_records}
    for entry in log_entries:
        material_ids.update(entry.material_finding_ids)
    return material_ids


def _finding_closure_findings(
    finding_id: str,
    log_entries: list[ReviewLogEntry] | tuple[ReviewLogEntry, ...],
    resolution: ReviewResolution | None,
    finding_records: list[FindingRecord] | tuple[FindingRecord, ...],
    mode: str,
) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    indexed = any(finding_id in entry.material_finding_ids for entry in log_entries)
    if not indexed:
        finding_record = next((record for record in finding_records if record.finding_id == finding_id), None)
        findings.append(
            ValidationFinding(
                path=finding_record.path if finding_record is not None else Path("review-log.md"),
                line=finding_record.line if finding_record is not None else None,
                mode=mode,
                message="material Finding ID missing from review-log.md",
                review_id=finding_record.review_id if finding_record is not None else None,
                finding_id=finding_id,
            )
        )
    for entry in log_entries:
        if finding_id not in entry.open_finding_ids:
            continue
        findings.append(
            ValidationFinding(
                path=entry.path,
                line=entry.line,
                mode=mode,
                message="review-log Open findings must be empty for closed closeout",
                review_id=entry.review_id,
                finding_id=finding_id,
            )
        )
    if resolution is None:
        findings.append(
            ValidationFinding(
                path=Path("review-resolution.md"),
                line=None,
                mode=mode,
                message="material Finding ID missing from review-resolution.md",
                finding_id=finding_id,
            )
        )
        return findings

    if resolution.closeout_status is None:
        findings.append(
            ValidationFinding(
                path=resolution.path,
                line=resolution.closeout_line,
                mode=mode,
                message="review-resolution.md closeout status is missing or invalid",
                finding_id=finding_id,
            )
        )

    matches = [entry for entry in resolution.entries if entry.finding_id == finding_id]
    if len(matches) != 1:
        findings.append(
            ValidationFinding(
                path=resolution.path,
                line=matches[0].line if matches else None,
                mode=mode,
                message="material Finding ID must appear exactly once in review-resolution.md",
                finding_id=finding_id,
            )
        )
        return findings
    findings.extend(_validate_resolution_entry_closeout(matches[0], mode))
    return findings


def _validate_resolution_entry_closeout(
    entry: ResolutionRecord,
    mode: str,
) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    if entry.disposition_count != 1:
        findings.append(
            ValidationFinding(
                path=entry.path,
                line=entry.line,
                mode=mode,
                message="resolution entry disposition must appear exactly once",
                finding_id=entry.finding_id,
            )
        )
    if entry.disposition is None:
        findings.append(
            ValidationFinding(
                path=entry.path,
                line=entry.line,
                mode=mode,
                message="resolution entry missing disposition",
                finding_id=entry.finding_id,
            )
        )
    elif entry.disposition not in APPROVED_DISPOSITIONS:
        findings.append(
            ValidationFinding(
                path=entry.path,
                line=entry.line,
                mode=mode,
                message=f"unsupported disposition '{entry.disposition}'",
                finding_id=entry.finding_id,
            )
        )
    if not _entry_has(entry, "Validation evidence"):
        findings.append(
            ValidationFinding(
                path=entry.path,
                line=entry.line,
                mode=mode,
                message="finding closeout missing validation evidence",
                finding_id=entry.finding_id,
            )
        )

    if entry.disposition == "needs-decision":
        findings.append(
            ValidationFinding(
                path=entry.path,
                line=entry.line,
                mode=mode,
                message="needs-decision is not a final disposition",
                finding_id=entry.finding_id,
            )
        )

    if entry.disposition == "accepted":
        if not _entry_has_any(entry, ("Chosen action", "Final action")):
            findings.append(
                ValidationFinding(
                    path=entry.path,
                    line=entry.line,
                    mode=mode,
                    message="accepted finding missing chosen action",
                    finding_id=entry.finding_id,
                )
            )
        if not _entry_has(entry, "Validation evidence"):
            findings.append(
                ValidationFinding(
                    path=entry.path,
                    line=entry.line,
                    mode=mode,
                    message="accepted finding missing validation evidence",
                    finding_id=entry.finding_id,
                )
            )

    if entry.disposition == "rejected":
        if not _entry_has(entry, "Rationale"):
            findings.append(
                ValidationFinding(
                    path=entry.path,
                    line=entry.line,
                    mode=mode,
                    message="rejected finding missing rationale",
                    finding_id=entry.finding_id,
                )
            )

    if entry.disposition == "deferred":
        if not _entry_has(entry, "Rationale"):
            findings.append(
                ValidationFinding(
                    path=entry.path,
                    line=entry.line,
                    mode=mode,
                    message="deferred finding missing rationale",
                    finding_id=entry.finding_id,
                )
            )
        if not _entry_has_any(entry, ("Follow-up owner", "Owning stage", "No-follow-up reason")):
            findings.append(
                ValidationFinding(
                    path=entry.path,
                    line=entry.line,
                    mode=mode,
                    message="deferred finding missing follow-up owner, owning stage, or no-follow-up reason",
                    finding_id=entry.finding_id,
                )
            )

    if entry.disposition == "partially-accepted":
        if not _entry_has(entry, "Accepted portion"):
            findings.append(
                ValidationFinding(
                    path=entry.path,
                    line=entry.line,
                    mode=mode,
                    message="partially-accepted finding missing accepted portion",
                    finding_id=entry.finding_id,
                )
            )
        if not _entry_has_any(
            entry,
            (
                "Rejected or deferred portion",
                "Rejected portion",
                "Deferred portion",
                "Non-accepted portion",
            ),
        ):
            findings.append(
                ValidationFinding(
                    path=entry.path,
                    line=entry.line,
                    mode=mode,
                    message="partially-accepted finding missing rejected or deferred portion",
                    finding_id=entry.finding_id,
                )
            )
        if not _entry_has(entry, "Rationale"):
            findings.append(
                ValidationFinding(
                    path=entry.path,
                    line=entry.line,
                    mode=mode,
                    message="partially-accepted finding missing rationale",
                    finding_id=entry.finding_id,
                )
            )
        if not _entry_has(entry, "Validation evidence"):
            findings.append(
                ValidationFinding(
                    path=entry.path,
                    line=entry.line,
                    mode=mode,
                    message="partially-accepted finding missing validation evidence",
                    finding_id=entry.finding_id,
                )
            )
    return findings


def _validate_blocking_review_closeout(
    log_entries: list[ReviewLogEntry],
    resolution: ReviewResolution | None,
    mode: str,
) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    explicit_closeouts = set(resolution.explicit_review_closeout_ids) if resolution else set()
    for index, entry in enumerate(log_entries):
        if entry.status.lower() not in BLOCKING_REVIEW_STATUSES:
            continue
        if _has_later_nonblocking_review(entry, log_entries[index + 1 :]):
            continue
        if entry.review_id in explicit_closeouts:
            continue
        findings.append(
            ValidationFinding(
                path=entry.path,
                line=entry.line,
                mode=mode,
                message="blocking review outcome requires same-stage re-review or explicit closeout",
                review_id=entry.review_id,
            )
        )
    return findings


def _has_later_nonblocking_review(
    entry: ReviewLogEntry,
    later_entries: list[ReviewLogEntry],
) -> bool:
    entry_round = _round_number(entry.round)
    if entry_round is None:
        return False

    for later in later_entries:
        if later.stage != entry.stage:
            continue
        if later.status.lower() in BLOCKING_REVIEW_STATUSES:
            continue
        later_round = _round_number(later.round)
        if later_round is None or later_round <= entry_round:
            continue
        return True
    return False


def _round_number(value: str) -> int | None:
    try:
        return int(value, 10)
    except ValueError:
        return None


def _read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def _load_change_metadata(path: Path) -> Any:
    script_path = Path(__file__).with_name("validate-change-metadata.py")
    spec = importlib.util.spec_from_file_location("validate_change_metadata_for_review_artifacts", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load change metadata parser")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.load_yaml(path)


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


def _finding_field(record: FindingRecord, label: str) -> FieldValue | None:
    for value in record.fields.get(label, ()):
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


def _markdown_table_cells(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    cells = [cell.strip() for cell in stripped.strip("|").split("|")]
    if not cells:
        return []
    if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
        return []
    return cells


def _strip_code(value: str) -> str:
    stripped = value.strip()
    if len(stripped) >= 2 and stripped.startswith("`") and stripped.endswith("`"):
        return stripped[1:-1].strip()
    return stripped


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
