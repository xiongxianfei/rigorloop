#!/usr/bin/env python3
"""Validate release Token-Friendliness report metadata."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GENERIC_STATUSES = {"pass", "warning", "blocked", "not-run", "waived", "fail"}
RELEASE_GATE_STATUSES = {"pass", "warning", "blocked", "waived"}
WARNING_SEVERITIES = {"warning", "high-warning"}
ANALYZER_VERDICTS = {"pass", "warning", "blocked"}
PUBLIC_CODEX_SKILL_SOURCE = "dist/adapters/codex/.agents/skills/"
VALID_WAIVER_REASON_MARKERS = (
    "codex unavailable",
    "no benchmark-relevant changes",
    "emergency security",
    "critical fix",
    "benchmark tooling failure",
)


class MetadataValidationError(Exception):
    """Raised when token-cost metadata cannot be parsed."""


@dataclass(frozen=True)
class Line:
    indent: int
    text: str
    lineno: int


def parse_scalar(text: str) -> Any:
    value = text.strip()
    if not value:
        return ""
    if value == "[]":
        return []
    if value == "{}":
        return {}
    if value[0] == value[-1] and value[0] in {"'", '"'} and len(value) >= 2:
        return value[1:-1]
    if value in {"true", "false"}:
        return value == "true"
    if value == "null":
        return None
    if value.isdigit() or (value.startswith("-") and value[1:].isdigit()):
        return int(value)
    return value


def tokenize_yaml(text: str) -> list[Line]:
    lines: list[Line] = []
    for lineno, raw_line in enumerate(text.splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if "\t" in raw_line:
            raise MetadataValidationError(f"line {lineno}: tabs are not supported")
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        if indent % 2:
            raise MetadataValidationError(
                f"line {lineno}: indentation must use multiples of two spaces"
            )
        lines.append(Line(indent=indent, text=raw_line[indent:], lineno=lineno))
    return lines


def split_mapping_entry(text: str, lineno: int) -> tuple[str, str]:
    if ":" not in text:
        raise MetadataValidationError(f"line {lineno}: expected 'key: value'")
    key, value = text.split(":", 1)
    key = key.strip()
    if not key:
        raise MetadataValidationError(f"line {lineno}: mapping key must not be empty")
    return key, value.lstrip()


def parse_yaml_block(lines: list[Line], index: int, indent: int) -> tuple[Any, int]:
    if index >= len(lines):
        raise MetadataValidationError("unexpected end of file")
    line = lines[index]
    if line.indent != indent:
        raise MetadataValidationError(
            f"line {line.lineno}: expected indentation {indent}, found {line.indent}"
        )
    if line.text.startswith("- "):
        return parse_yaml_list(lines, index, indent)
    return parse_yaml_mapping(lines, index, indent)


def parse_yaml_mapping(lines: list[Line], index: int, indent: int) -> tuple[dict[str, Any], int]:
    data: dict[str, Any] = {}
    while index < len(lines):
        line = lines[index]
        if line.indent < indent:
            break
        if line.indent > indent:
            raise MetadataValidationError(
                f"line {line.lineno}: unexpected indentation inside mapping"
            )
        if line.text.startswith("- "):
            raise MetadataValidationError(
                f"line {line.lineno}: unexpected list item where mapping entry was expected"
            )
        key, remainder = split_mapping_entry(line.text, line.lineno)
        index += 1
        if remainder:
            data[key] = parse_scalar(remainder)
            continue
        if index >= len(lines) or lines[index].indent <= indent:
            data[key] = None
            continue
        child_indent = lines[index].indent
        if child_indent != indent + 2:
            raise MetadataValidationError(
                f"line {lines[index].lineno}: nested block for '{key}' must be indented by two spaces"
            )
        data[key], index = parse_yaml_block(lines, index, child_indent)
    return data, index


def parse_yaml_list(lines: list[Line], index: int, indent: int) -> tuple[list[Any], int]:
    items: list[Any] = []
    while index < len(lines):
        line = lines[index]
        if line.indent < indent:
            break
        if line.indent > indent:
            raise MetadataValidationError(
                f"line {line.lineno}: unexpected indentation inside list"
            )
        if not line.text.startswith("- "):
            raise MetadataValidationError(
                f"line {line.lineno}: expected list item starting with '- '"
            )
        remainder = line.text[2:].lstrip()
        index += 1
        if not remainder:
            if index >= len(lines) or lines[index].indent <= indent:
                items.append(None)
                continue
            if lines[index].indent != indent + 2:
                raise MetadataValidationError(
                    f"line {lines[index].lineno}: nested list item blocks must be indented by two spaces"
                )
            item, index = parse_yaml_block(lines, index, indent + 2)
            items.append(item)
            continue
        if ":" in remainder:
            item, index = parse_inline_mapping_item(lines, index, indent, remainder, line.lineno)
            items.append(item)
            continue
        items.append(parse_scalar(remainder))
    return items, index


def parse_inline_mapping_item(
    lines: list[Line], index: int, indent: int, remainder: str, lineno: int
) -> tuple[dict[str, Any], int]:
    item: dict[str, Any] = {}
    key, value = split_mapping_entry(remainder, lineno)
    if value:
        item[key] = parse_scalar(value)
    elif index < len(lines) and lines[index].indent > indent:
        if lines[index].indent != indent + 2:
            raise MetadataValidationError(
                f"line {lines[index].lineno}: nested mapping blocks must be indented by two spaces"
            )
        item[key], index = parse_yaml_block(lines, index, indent + 2)
    else:
        item[key] = None

    while index < len(lines):
        line = lines[index]
        if line.indent < indent + 2:
            break
        if line.indent > indent + 2:
            raise MetadataValidationError(
                f"line {line.lineno}: unexpected indentation inside inline mapping item"
            )
        if line.text.startswith("- "):
            break
        key, value = split_mapping_entry(line.text, line.lineno)
        index += 1
        if value:
            item[key] = parse_scalar(value)
            continue
        if index >= len(lines) or lines[index].indent <= indent + 2:
            item[key] = None
            continue
        if lines[index].indent != indent + 4:
            raise MetadataValidationError(
                f"line {lines[index].lineno}: nested mapping blocks must be indented by two spaces"
            )
        item[key], index = parse_yaml_block(lines, index, indent + 4)
    return item, index


def load_yaml(path: Path) -> Any:
    lines = tokenize_yaml(path.read_text(encoding="utf-8"))
    if not lines:
        raise MetadataValidationError("metadata file is empty")
    data, index = parse_yaml_block(lines, 0, lines[0].indent)
    if index != len(lines):
        line = lines[index]
        raise MetadataValidationError(
            f"line {line.lineno}: unexpected trailing content at indentation {line.indent}"
        )
    return data


def label(parent: str, child: str | int) -> str:
    if isinstance(child, int):
        return f"{parent}[{child}]"
    return child if parent == "$" else f"{parent}.{child}"


def child(data: Any, key: str, path: str, errors: list[str]) -> Any:
    if not isinstance(data, dict):
        errors.append(f"{path}: expected object")
        return None
    if key not in data:
        errors.append(f"{label(path, key)}: missing required field")
        return None
    return data[key]


def require_fields(data: Any, path: str, fields: list[str], errors: list[str]) -> None:
    if not isinstance(data, dict):
        errors.append(f"{path}: expected object")
        return
    for field in fields:
        if field not in data:
            errors.append(f"{label(path, field)}: missing required field")


def require_mapping(data: Any, path: str, errors: list[str]) -> dict[str, Any]:
    if isinstance(data, dict):
        return data
    errors.append(f"{path}: expected object")
    return {}


def require_list(data: Any, path: str, errors: list[str]) -> list[Any]:
    if isinstance(data, list):
        return data
    errors.append(f"{path}: expected list")
    return []


def require_non_empty_string(value: Any, path: str, errors: list[str]) -> str:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}: expected non-empty string")
        return ""
    return value


def require_int(value: Any, path: str, errors: list[str]) -> int | None:
    if not isinstance(value, int) or isinstance(value, bool):
        errors.append(f"{path}: expected integer")
        return None
    return value


def require_bool(value: Any, path: str, errors: list[str]) -> bool | None:
    if not isinstance(value, bool):
        errors.append(f"{path}: expected boolean")
        return None
    return value


def require_enum(value: Any, path: str, allowed: set[str], errors: list[str]) -> str:
    if not isinstance(value, str) or value not in allowed:
        errors.append(f"{path}: expected one of {', '.join(sorted(allowed))}")
        return ""
    return value


def require_existing_repo_path(value: Any, path: str, errors: list[str], *, allow_empty: bool = False) -> str:
    if allow_empty and value == "":
        return ""
    raw = require_non_empty_string(value, path, errors)
    if not raw:
        return ""
    target = ROOT / raw
    if not target.exists():
        errors.append(f"{path}: referenced path does not exist: {raw}")
    return raw


def is_final_release(release: str) -> bool:
    return "-" not in release


def validate_analyzer_summary(path: str, expected_raw_tracked: bool, errors: list[str]) -> None:
    if not path:
        return
    summary_path = ROOT / path
    if not summary_path.exists():
        return
    try:
        data = load_yaml(summary_path)
    except MetadataValidationError as exc:
        errors.append(f"{path}: invalid analyzer summary: {exc}")
        return
    summary = require_mapping(data, path, errors)
    if summary.get("schema_version") != 1:
        errors.append(f"{path}.schema_version: expected 1")
    run = require_mapping(summary.get("run"), f"{path}.run", errors)
    raw_tracked = run.get("raw_jsonl_tracked")
    if raw_tracked is not expected_raw_tracked:
        errors.append(f"{path}.run.raw_jsonl_tracked: must match dynamic run evidence")
    if expected_raw_tracked:
        require_existing_repo_path(run.get("jsonl"), f"{path}.run.jsonl", errors)
    else:
        if run.get("jsonl") != "":
            errors.append(f"{path}.run.jsonl: must be empty when raw JSONL is omitted")
        require_non_empty_string(run.get("sanitized_source"), f"{path}.run.sanitized_source", errors)
        require_existing_repo_path(run.get("sanitized_summary"), f"{path}.run.sanitized_summary", errors)
        require_non_empty_string(
            run.get("raw_omission_reason"), f"{path}.run.raw_omission_reason", errors
        )
    usage = require_mapping(summary.get("usage"), f"{path}.usage", errors)
    for key in [
        "input_tokens",
        "cached_input_tokens",
        "output_tokens",
        "reasoning_output_tokens",
    ]:
        require_int(usage.get(key), f"{path}.usage.{key}", errors)
    tool_output = require_mapping(summary.get("tool_output"), f"{path}.tool_output", errors)
    require_int(
        tool_output.get("total_estimated_tokens"),
        f"{path}.tool_output.total_estimated_tokens",
        errors,
    )
    largest = require_mapping(
        tool_output.get("largest_event"), f"{path}.tool_output.largest_event", errors
    )
    for key in ["kind", "command", "path"]:
        if not isinstance(largest.get(key), str):
            errors.append(f"{path}.tool_output.largest_event.{key}: expected string")
    for key in ["lines", "estimated_tokens"]:
        require_int(largest.get(key), f"{path}.tool_output.largest_event.{key}", errors)
    signals = require_mapping(summary.get("signals"), f"{path}.signals", errors)
    for key in [
        "full_file_read_count",
        "broad_search_count",
        "generated_output_read_count",
        "repeated_file_read_count",
    ]:
        require_int(signals.get(key), f"{path}.signals.{key}", errors)
    verdict = require_mapping(summary.get("verdict"), f"{path}.verdict", errors)
    require_enum(verdict.get("result"), f"{path}.verdict.result", ANALYZER_VERDICTS, errors)
    require_list(verdict.get("warnings"), f"{path}.verdict.warnings", errors)
    require_list(verdict.get("blockers"), f"{path}.verdict.blockers", errors)


def validate_run(run: Any, index: int, errors: list[str]) -> None:
    path = f"dynamic_runtime.runs[{index}]"
    item = require_mapping(run, path, errors)
    for key in ["id", "prompt", "fixture", "result", "evidence"]:
        if key not in item:
            errors.append(f"{path}.{key}: missing required field")
    require_non_empty_string(item.get("id"), f"{path}.id", errors)
    require_existing_repo_path(item.get("prompt"), f"{path}.prompt", errors)
    require_existing_repo_path(item.get("fixture"), f"{path}.fixture", errors)
    require_enum(item.get("result"), f"{path}.result", {"pass", "fail", "blocked", "not-run"}, errors)

    evidence = require_mapping(item.get("evidence"), f"{path}.evidence", errors)
    for key in [
        "raw_jsonl_tracked",
        "jsonl",
        "analysis",
        "sanitized_summary",
        "raw_omission_reason",
    ]:
        if key not in evidence:
            errors.append(f"{path}.evidence.{key}: missing required field")
    raw_tracked = require_bool(
        evidence.get("raw_jsonl_tracked"), f"{path}.evidence.raw_jsonl_tracked", errors
    )
    if raw_tracked is True:
        require_existing_repo_path(evidence.get("jsonl"), f"{path}.evidence.jsonl", errors)
        require_existing_repo_path(evidence.get("analysis"), f"{path}.evidence.analysis", errors)
        if evidence.get("raw_omission_reason") not in {"", None}:
            errors.append(f"{path}.evidence.raw_omission_reason: must be empty when raw JSONL is tracked")
    elif raw_tracked is False:
        if evidence.get("jsonl") != "":
            errors.append(f"{path}.evidence.jsonl: must be empty when raw JSONL is omitted")
        require_non_empty_string(
            evidence.get("raw_omission_reason"),
            f"{path}.evidence.raw_omission_reason",
            errors,
        )
        analysis = evidence.get("analysis")
        sanitized = evidence.get("sanitized_summary")
        if not analysis and not sanitized:
            errors.append(
                f"{path}.evidence.analysis: required when raw JSONL is omitted unless sanitized_summary exists"
            )
        require_existing_repo_path(analysis, f"{path}.evidence.analysis", errors, allow_empty=True)
        require_existing_repo_path(
            sanitized, f"{path}.evidence.sanitized_summary", errors, allow_empty=True
        )
    analysis_value = evidence.get("analysis")
    if isinstance(analysis_value, str) and analysis_value:
        validate_analyzer_summary(analysis_value, raw_tracked is True, errors)


def validate_dynamic_runtime(data: dict[str, Any], release: str, errors: list[str]) -> None:
    dynamic = require_mapping(data.get("dynamic_runtime"), "dynamic_runtime", errors)
    status = require_enum(dynamic.get("status"), "dynamic_runtime.status", GENERIC_STATUSES, errors)
    final = is_final_release(release)
    if final and status not in {"pass", "waived"}:
        errors.append("dynamic_runtime.status: final public releases require pass or waived")
    if status in {"blocked", "not-run"}:
        incomplete = dynamic.get("incomplete")
        if not isinstance(incomplete, dict):
            errors.append(
                "dynamic_runtime.incomplete: required when dynamic runtime is blocked or not-run"
            )
        else:
            for key in ["reason", "owner", "environment", "follow_up"]:
                require_non_empty_string(
                    incomplete.get(key), f"dynamic_runtime.incomplete.{key}", errors
                )
            require_bool(
                incomplete.get("release_may_proceed"),
                "dynamic_runtime.incomplete.release_may_proceed",
                errors,
            )
    if status != "waived":
        runs = require_list(dynamic.get("runs"), "dynamic_runtime.runs", errors)
        if not runs and final:
            errors.append("dynamic_runtime.runs: required when no final waiver exists")
        for index, run in enumerate(runs):
            validate_run(run, index, errors)


def validate_waiver(data: dict[str, Any], dynamic_status: str, errors: list[str]) -> None:
    waiver = require_mapping(data.get("waiver"), "waiver", errors)
    require_bool(waiver.get("required"), "waiver.required", errors)
    status = waiver.get("status")
    if dynamic_status == "waived" and status != "approved":
        errors.append("waiver.status: waived dynamic runtime requires approved waiver")
    for key in ["reason", "approved_by", "approval_surface", "evidence"]:
        value = waiver.get(key)
        if dynamic_status == "waived":
            require_non_empty_string(value, f"waiver.{key}", errors)
    if dynamic_status == "waived":
        reason = str(waiver.get("reason", "")).lower()
        if not any(marker in reason for marker in VALID_WAIVER_REASON_MARKERS):
            errors.append("waiver.reason: invalid waiver reason")
        require_existing_repo_path(waiver.get("evidence"), "waiver.evidence", errors)


def validate_comparison(data: dict[str, Any], errors: list[str]) -> None:
    comparison = require_mapping(data.get("comparison"), "comparison", errors)
    baseline = require_bool(comparison.get("baseline"), "comparison.baseline", errors)
    comparable = require_bool(comparison.get("comparable"), "comparison.comparable", errors)
    if baseline is True:
        if comparison.get("previous_release") is not None:
            errors.append("comparison.previous_release: must be null for first baseline")
        if comparison.get("previous_report") is not None:
            errors.append("comparison.previous_report: must be null for first baseline")
        if comparison.get("deltas") is not None:
            errors.append("comparison.deltas: must be null for first baseline")
        require_non_empty_string(comparison.get("rationale"), "comparison.rationale", errors)
    elif baseline is False:
        if not isinstance(comparison.get("previous_release"), str) or not comparison.get(
            "previous_release"
        ):
            errors.append("comparison.previous_release: required for non-baseline reports")
        if not isinstance(comparison.get("previous_report"), str) or not comparison.get(
            "previous_report"
        ):
            errors.append(
                "comparison.previous_report: required for non-baseline comparable reports"
            )
        else:
            require_existing_repo_path(
                comparison.get("previous_report"), "comparison.previous_report", errors
            )
        if comparable is True:
            deltas = require_mapping(comparison.get("deltas"), "comparison.deltas", errors)
            for key in [
                "static_total_estimated_tokens",
                "median_input_tokens",
                "median_output_tokens",
                "max_single_tool_output_estimated_tokens",
            ]:
                require_int(deltas.get(key), f"comparison.deltas.{key}", errors)
        else:
            require_non_empty_string(comparison.get("rationale"), "comparison.rationale", errors)


def validate_runner_and_suite(data: dict[str, Any], errors: list[str]) -> None:
    suite = require_mapping(data.get("benchmark_suite"), "benchmark_suite", errors)
    runner = require_mapping(data.get("runner"), "runner", errors)
    require_existing_repo_path(suite.get("manifest"), "benchmark_suite.manifest", errors)
    require_existing_repo_path(suite.get("fixture"), "benchmark_suite.fixture", errors)
    require_non_empty_string(suite.get("id"), "benchmark_suite.id", errors)
    require_int(suite.get("prompt_count"), "benchmark_suite.prompt_count", errors)
    require_int(suite.get("runs_per_prompt"), "benchmark_suite.runs_per_prompt", errors)
    require_non_empty_string(runner.get("command"), "runner.command", errors)
    if runner.get("tool") != "codex":
        errors.append("runner.tool: expected codex")
    if runner.get("suite") != suite.get("manifest"):
        errors.append("runner.suite: must match benchmark_suite.manifest")
    if runner.get("fixture") != suite.get("fixture"):
        errors.append("runner.fixture: must match benchmark_suite.fixture")
    if runner.get("skill_source") != PUBLIC_CODEX_SKILL_SOURCE:
        errors.append(f"runner.skill_source: expected {PUBLIC_CODEX_SKILL_SOURCE}")
    require_existing_repo_path(runner.get("output_dir"), "runner.output_dir", errors)
    require_bool(runner.get("install_public_skills"), "runner.install_public_skills", errors)


def validate_static_and_summary(data: dict[str, Any], errors: list[str]) -> None:
    static = require_mapping(data.get("static_skill_size"), "static_skill_size", errors)
    require_enum(static.get("status"), "static_skill_size.status", GENERIC_STATUSES, errors)
    require_non_empty_string(static.get("command"), "static_skill_size.command", errors)
    require_int(static.get("skills_measured"), "static_skill_size.skills_measured", errors)
    require_int(
        static.get("total_estimated_tokens"),
        "static_skill_size.total_estimated_tokens",
        errors,
    )
    max_skill = require_mapping(static.get("max_skill"), "static_skill_size.max_skill", errors)
    require_non_empty_string(max_skill.get("path"), "static_skill_size.max_skill.path", errors)
    require_int(
        max_skill.get("estimated_tokens"),
        "static_skill_size.max_skill.estimated_tokens",
        errors,
    )

    summary = require_mapping(data.get("summary"), "summary", errors)
    for key in [
        "median_input_tokens",
        "median_cached_input_tokens",
        "median_output_tokens",
        "median_reasoning_output_tokens",
        "max_single_tool_output_estimated_tokens",
        "full_file_read_count",
        "broad_search_count",
        "generated_output_read_count",
    ]:
        require_int(summary.get(key), f"summary.{key}", errors)


def validate_portability_and_gate(data: dict[str, Any], errors: list[str]) -> None:
    portability = require_mapping(data.get("portability"), "portability", errors)
    status = require_enum(
        portability.get("status"), "portability.status", {"pass", "warning", "fail", "not-run"}, errors
    )
    if status == "fail":
        errors.append("portability.status: public skill portability failure blocks release")
    for key in [
        "public_skill_internal_path_leaks",
        "generated_output_internals_in_public_skills",
        "local_examples_in_public_skills",
    ]:
        require_int(portability.get(key), f"portability.{key}", errors)

    gate = require_mapping(data.get("release_gate"), "release_gate", errors)
    require_enum(gate.get("result"), "release_gate.result", RELEASE_GATE_STATUSES, errors)
    for list_key in ["blockers", "warnings"]:
        value = gate.get(list_key)
        if value is not None:
            require_list(value, f"release_gate.{list_key}", errors)
    for warning in gate.get("warnings") or []:
        if isinstance(warning, dict):
            severity = warning.get("severity")
            if severity is not None and severity not in WARNING_SEVERITIES:
                errors.append(f"release_gate.warnings: invalid warning severity {severity}")
        elif isinstance(warning, str) and "hard warning" in warning.lower():
            errors.append("release_gate.warnings: use high-warning, not hard warning")


def validate_report(path: Path) -> list[str]:
    data = load_yaml(path)
    errors: list[str] = []
    root = require_mapping(data, "$", errors)
    for section in [
        "schema_version",
        "report",
        "benchmark_suite",
        "environment",
        "runner",
        "static_skill_size",
        "dynamic_runtime",
        "summary",
        "portability",
        "comparison",
        "waiver",
        "release_gate",
    ]:
        if section not in root:
            errors.append(f"{section}: missing required field")
    if errors:
        return errors
    if root.get("schema_version") != 1:
        errors.append("schema_version: expected 1")

    report = require_mapping(root.get("report"), "report", errors)
    for key in ["release", "report_date", "commit", "report_markdown"]:
        require_non_empty_string(report.get(key), f"report.{key}", errors)
    release = str(report.get("release") or "")
    require_existing_repo_path(report.get("report_markdown"), "report.report_markdown", errors)

    validate_runner_and_suite(root, errors)
    validate_static_and_summary(root, errors)
    validate_dynamic_runtime(root, release, errors)
    dynamic = require_mapping(root.get("dynamic_runtime"), "dynamic_runtime", errors)
    dynamic_status = dynamic.get("status") if isinstance(dynamic.get("status"), str) else ""
    validate_waiver(root, dynamic_status, errors)
    validate_comparison(root, errors)
    validate_portability_and_gate(root, errors)
    return errors


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(
            "usage: validate-token-cost-report.py <release-metadata.yaml> [<release-metadata.yaml> ...]",
            file=sys.stderr,
        )
        return 2

    exit_code = 0
    for raw_path in argv[1:]:
        path = Path(raw_path)
        try:
            errors = validate_report(path)
        except FileNotFoundError:
            print(f"{path}: file not found", file=sys.stderr)
            exit_code = 1
            continue
        except MetadataValidationError as exc:
            print(f"{path}: invalid token-cost report metadata", file=sys.stderr)
            print(f"  - {exc}", file=sys.stderr)
            exit_code = 1
            continue

        if errors:
            print(f"{path}: invalid token-cost report metadata", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
            exit_code = 1
            continue

        print(f"{path}: valid token-cost report metadata")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
