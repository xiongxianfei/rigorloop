#!/usr/bin/env python3
"""Analyze a Codex JSONL export for token usage and tool-output amplification."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
USAGE_KEYS = {
    "input_tokens",
    "cached_input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
}
HIGH_OUTPUT_TOKEN_THRESHOLD = 20000
SUMMARY_WARNING_TOKEN_THRESHOLD = 8000
REPEATED_READ_THRESHOLD = 3


@dataclass
class ToolEvent:
    command: str
    output: str
    max_output_tokens: int | None
    line_number: int
    kind: str = ""

    @property
    def output_lines(self) -> int:
        if not self.output:
            return 0
        return len(self.output.splitlines())

    @property
    def output_bytes(self) -> int:
        return len(self.output.encode("utf-8"))

    @property
    def estimated_output_tokens(self) -> int:
        if not self.output:
            return 0
        return max(1, max(len(self.output.split()), math.ceil(len(self.output) / 4)))


def iter_dicts(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from iter_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_dicts(child)


def iter_strings(value: Any, key_hint: str | None = None) -> Iterable[tuple[str | None, str]]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield from iter_strings(child, key)
    elif isinstance(value, list):
        for child in value:
            yield from iter_strings(child, key_hint)
    elif isinstance(value, str):
        yield key_hint, value


def first_usage(record: dict[str, Any]) -> dict[str, int] | None:
    for item in iter_dicts(record):
        if any(key in item for key in USAGE_KEYS):
            usage: dict[str, int] = {}
            for key in USAGE_KEYS:
                value = item.get(key)
                if isinstance(value, int):
                    usage[key] = value
            if usage:
                return usage
    return None


def looks_like_tool_record(record: dict[str, Any]) -> bool:
    tool_markers = {"tool", "recipient", "name", "function", "tool_call_id"}
    if any(key in record for key in tool_markers):
        return True
    return any(key in record for key in {"cmd", "command", "args", "arguments", "output", "result"})


def current_codex_command_execution(record: dict[str, Any]) -> dict[str, Any] | None:
    item = record.get("item")
    if (
        record.get("type") == "item.completed"
        and isinstance(item, dict)
        and item.get("type") == "command_execution"
    ):
        return item
    return None


def find_command(record: dict[str, Any]) -> str:
    command_event = current_codex_command_execution(record)
    if command_event is not None:
        value = command_event.get("command")
        if isinstance(value, str) and value.strip():
            return value.strip()
    command_keys = {"cmd", "command", "query", "q"}
    for item in iter_dicts(record):
        for key in command_keys:
            value = item.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    for key, value in iter_strings(record):
        if key in {"tool", "recipient", "name"} and value.strip():
            return value.strip()
    return "unknown"


def find_output(record: dict[str, Any]) -> str:
    command_event = current_codex_command_execution(record)
    if command_event is not None:
        for key in ["aggregated_output", "output", "stdout", "stderr"]:
            value = command_event.get(key)
            if isinstance(value, str) and value:
                return value
    output_keys = {"aggregated_output", "output", "stdout", "stderr", "content", "text"}
    outputs: list[str] = []
    for item in iter_dicts(record):
        for key in output_keys:
            value = item.get(key)
            if isinstance(value, str) and value:
                outputs.append(value)
    return "\n".join(outputs)


def find_max_output_tokens(record: dict[str, Any]) -> int | None:
    for item in iter_dicts(record):
        value = item.get("max_output_tokens")
        if isinstance(value, int):
            return value
    return None


def read_events(path: Path) -> tuple[dict[str, int], list[ToolEvent], int]:
    usage_totals: dict[str, int] = {}
    events: list[ToolEvent] = []
    unknown_records = 0

    try:
        handle = path.open("r", encoding="utf-8")
    except FileNotFoundError:
        raise ValueError(f"missing file: {path}") from None
    except OSError as exc:
        raise ValueError(f"unreadable file: {path}: {exc}") from None

    with handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"malformed JSONL at line {line_number}: {exc.msg}") from None
            if not isinstance(record, dict):
                unknown_records += 1
                continue

            usage = first_usage(record)
            if usage:
                for key, value in usage.items():
                    usage_totals[key] = usage_totals.get(key, 0) + value

            command_event = current_codex_command_execution(record)
            if command_event is not None or looks_like_tool_record(record):
                events.append(
                    ToolEvent(
                        command=find_command(record),
                        output=find_output(record),
                        max_output_tokens=find_max_output_tokens(record),
                        line_number=line_number,
                        kind="command_execution" if command_event is not None else "",
                    )
                )
            elif not usage:
                unknown_records += 1

    return usage_totals, events, unknown_records


def command_path(command: str) -> str | None:
    patterns = [
        r"\b(?:cat|nl)\s+([^\s|;&]+)",
        r"\bsed\s+-n\s+['\"]?[^'\"]+['\"]?\s+([^\s|;&]+)",
        r"\b(?:rg|grep)\b.*\s([^\s|;&]+)$",
    ]
    for pattern in patterns:
        match = re.search(pattern, command)
        if match:
            value = match.group(1).strip("'\"")
            if value and value not in {".", "./"}:
                return value
    return None


def display_path(path: Path, repo_root: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return str(resolved)


def is_file_read_like_command(command: str) -> bool:
    stripped = command.strip()
    return bool(
        re.search(r"\b(?:cat|nl|head|tail)\s+[^\s|;&]+", stripped)
        or re.search(r"\bsed\s+-n\s+['\"]?[^'\"]+['\"]?\s+[^\s|;&]+", stripped)
        or re.search(r"\bawk\b.*\s+[^\s|;&]+$", stripped)
        or re.search(r"open\([^)]+\)\.read\(\)", stripped)
    )


def event_kind(event: ToolEvent) -> str:
    if event.kind:
        return event.kind
    if command_path(event.command):
        return "file-read"
    if event.command != "unknown":
        return "shell-output"
    return "unknown"


def is_broad_search(command: str) -> bool:
    stripped = command.strip()
    if re.search(r"\b(?:rg|grep|find)\b", stripped) is None:
        return False
    if re.search(r"\b(?:rg|grep)\b.*\s\.(?:\s|$)", stripped):
        return True
    if re.search(r"\bfind\s+\.", stripped):
        return True
    return bool(re.fullmatch(r"(?:rg|grep)(?:\s+-[^\s]+)*\s+\S+", stripped))


def is_full_file_read(command: str) -> bool:
    stripped = command.strip()
    if re.search(r"\b(?:cat|nl)\s+[^\s|;&]+", stripped):
        return True
    return bool(re.search(r"\bsed\s+-n\s+['\"]?1,\d+p['\"]?", stripped))


def large_leading_range(command: str) -> bool:
    match = re.search(r"\bsed\s+-n\s+['\"]?1,(\d+)p['\"]?", command.strip())
    return bool(match and int(match.group(1)) >= 200)


def is_full_file_read_event(event: ToolEvent) -> bool:
    if not is_full_file_read(event.command):
        return False
    return event.output_lines > 80 or event.estimated_output_tokens >= SUMMARY_WARNING_TOKEN_THRESHOLD


def is_suspected_full_file_read_event(event: ToolEvent) -> bool:
    if is_full_file_read_event(event):
        return False
    return large_leading_range(event.command) or event.output_lines >= 300


def is_generated_output_read(command: str) -> bool:
    path = command_path(command)
    if not path:
        return False
    return ".codex/skills/" in path or "dist/adapters/" in path


def repeated_file_reads(events: list[ToolEvent]) -> list[tuple[str, int]]:
    counts: dict[str, int] = {}
    for event in events:
        path = command_path(event.command)
        if path and is_file_read_like_command(event.command):
            counts[path] = counts.get(path, 0) + 1
    return sorted((path, count) for path, count in counts.items() if count >= REPEATED_READ_THRESHOLD)


def command_summary(command: str, limit: int = 120) -> str:
    normalized = " ".join(command.split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3] + "..."


def yaml_scalar(value: object) -> str:
    if value is None:
        return '""'
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    text = str(value)
    if text == "":
        return '""'
    if re.fullmatch(r"[A-Za-z0-9_./:@+=,-]+", text):
        return text
    return json.dumps(text)


def signal_counts(events: list[ToolEvent]) -> dict[str, int]:
    repeated = repeated_file_reads(events)
    return {
        "full_file_read_count": len([event for event in events if is_full_file_read_event(event)]),
        "broad_search_count": len([event for event in events if is_broad_search(event.command)]),
        "generated_output_read_count": len(
            [event for event in events if is_generated_output_read(event.command)]
        ),
        "repeated_file_read_count": len(repeated),
    }


def full_file_read_classification(events: list[ToolEvent]) -> tuple[str, list[str]]:
    signals: list[str] = []
    if any(is_full_file_read_event(event) for event in events):
        signals.append("full_file_read_command")
        if any(event.output_lines >= 300 for event in events):
            signals.append("high_volume_single_file_output")
        return "confirmed", signals
    if any(is_suspected_full_file_read_event(event) for event in events):
        signals.append("large_leading_range_read")
        return "suspected", signals
    return "none", signals


def normalized_read_path(path_text: str, repo_root: Path) -> str:
    path = Path(path_text)
    if path.is_absolute():
        return display_path(path, repo_root)
    return path.as_posix()


def justified_read_set(paths: list[str], repo_root: Path) -> set[str]:
    return {normalized_read_path(path, repo_root) for path in paths}


def read_is_justified(event: ToolEvent, justified_reads: set[str], repo_root: Path) -> bool:
    path = command_path(event.command)
    if not path:
        return False
    normalized = normalized_read_path(path, repo_root)
    if normalized in justified_reads:
        return True
    resolved = (repo_root / normalized).resolve()
    return any(resolved == (repo_root / item).resolve() for item in justified_reads)


def full_file_read_detail(
    events: list[ToolEvent], justified_reads: set[str], repo_root: Path
) -> tuple[str, list[str], list[ToolEvent], list[ToolEvent], list[ToolEvent]]:
    confirmed = [event for event in events if is_full_file_read_event(event)]
    suspected = [event for event in events if is_suspected_full_file_read_event(event)]
    justified = [
        event
        for event in confirmed + suspected
        if read_is_justified(event, justified_reads, repo_root)
    ]
    unjustified_confirmed = [event for event in confirmed if event not in justified]
    unjustified_suspected = [event for event in suspected if event not in justified]
    if unjustified_confirmed:
        result = "confirmed"
    elif unjustified_suspected:
        result = "suspected"
    elif justified:
        result = "justified"
    else:
        result = "none"
    signals: list[str] = []
    if confirmed:
        signals.append("full_file_read_command")
    if any(event.output_lines >= 300 for event in confirmed):
        signals.append("high_volume_single_file_output")
    if suspected:
        signals.append("large_leading_range_read")
    return result, signals, justified, unjustified_confirmed, unjustified_suspected


def verdict_for(events: list[ToolEvent]) -> tuple[str, list[str], list[str]]:
    warnings: list[str] = []
    blockers: list[str] = []
    if any(event.estimated_output_tokens >= HIGH_OUTPUT_TOKEN_THRESHOLD for event in events):
        blockers.append("single tool output exceeds 20000 estimated tokens")
    elif any(event.estimated_output_tokens >= SUMMARY_WARNING_TOKEN_THRESHOLD for event in events):
        warnings.append("single tool output exceeds 8000 estimated tokens")
    if any(is_broad_search(event.command) for event in events):
        warnings.append("broad search observed")
    if any(is_full_file_read_event(event) for event in events):
        warnings.append("full-file-style read observed")
    if any(is_generated_output_read(event.command) for event in events):
        warnings.append("generated output read observed")
    if blockers:
        return "blocked", warnings, blockers
    if warnings:
        return "warning", warnings, blockers
    return "pass", warnings, blockers


def write_summary(
    path: Path,
    *,
    run_id: str,
    jsonl_path: Path,
    raw_jsonl_tracked: bool,
    sanitized_source: str,
    sanitized_summary: str,
    raw_omission_reason: str,
    repo_root: Path,
    justified_reads: set[str],
    justification: str,
    usage: dict[str, int],
    events: list[ToolEvent],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ranked_outputs = sorted(events, key=lambda event: event.estimated_output_tokens, reverse=True)
    largest = ranked_outputs[0] if ranked_outputs else None
    counts = signal_counts(events)
    verdict, warnings, blockers = verdict_for(events)
    (
        full_file_result,
        full_file_signals,
        justified_events,
        confirmed_events,
        suspected_events,
    ) = full_file_read_detail(events, justified_reads, repo_root)
    jsonl_value = display_path(jsonl_path, repo_root) if raw_jsonl_tracked else ""
    lines = [
        "schema_version: 1",
        "",
        "run:",
        f"  id: {yaml_scalar(run_id)}",
        f"  raw_jsonl_tracked: {yaml_scalar(raw_jsonl_tracked)}",
        f"  jsonl: {yaml_scalar(jsonl_value)}",
        f"  sanitized_source: {yaml_scalar(sanitized_source)}",
        f"  sanitized_summary: {yaml_scalar(sanitized_summary)}",
        f"  raw_omission_reason: {yaml_scalar(raw_omission_reason)}",
        "",
        "usage:",
    ]
    for key in sorted(USAGE_KEYS):
        lines.append(f"  {key}: {usage.get(key, 0)}")
    lines.extend(
        [
            "",
            "tool_output:",
            f"  total_estimated_tokens: {sum(event.estimated_output_tokens for event in events)}",
            "  largest_event:",
            f"    kind: {yaml_scalar(event_kind(largest) if largest else 'none')}",
            f"    command: {yaml_scalar(largest.command if largest else '')}",
            f"    path: {yaml_scalar(command_path(largest.command) if largest else '')}",
            f"    lines: {largest.output_lines if largest else 0}",
            f"    estimated_tokens: {largest.estimated_output_tokens if largest else 0}",
            "",
            "signals:",
        ]
    )
    for key, value in counts.items():
        lines.append(f"  {key}: {value}")
    lines.extend(
        [
            "",
            "full_file_read:",
            f"  result: {full_file_result}",
            f"  justification: {yaml_scalar(justification if justified_events else '')}",
        ]
    )
    if full_file_signals:
        lines.append("  signals:")
        lines.extend(f"    - {yaml_scalar(item)}" for item in full_file_signals)
    else:
        lines.append("  signals: []")
    for title, detail_events in [
        ("justified_reads", justified_events),
        ("confirmed_reads", confirmed_events),
        ("suspected_reads", suspected_events),
    ]:
        if detail_events:
            lines.append(f"  {title}:")
            for event in detail_events:
                lines.append(f"    - path: {yaml_scalar(command_path(event.command) or '')}")
                lines.append(f"      lines: {event.output_lines}")
                lines.append(f"      estimated_tokens: {event.estimated_output_tokens}")
        else:
            lines.append(f"  {title}: []")
    repeated = repeated_file_reads(events)
    if repeated:
        lines.append("  repeated_file_reads:")
        for path_text, count in repeated:
            lines.append(f"    - path: {yaml_scalar(path_text)}")
            lines.append(f"      count: {count}")
    else:
        lines.append("  repeated_file_reads: []")
    lines.extend(["", "verdict:", f"  result: {verdict}"])
    if warnings:
        lines.append("  warnings:")
        lines.extend(f"    - {yaml_scalar(item)}" for item in warnings)
    else:
        lines.append("  warnings: []")
    if blockers:
        lines.append("  blockers:")
        lines.extend(f"    - {yaml_scalar(item)}" for item in blockers)
    else:
        lines.append("  blockers: []")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def print_event_list(title: str, events: list[ToolEvent]) -> None:
    print(f"{title}: {len(events)}")
    for event in events[:5]:
        print(
            f"  - line {event.line_number}: {command_summary(event.command)} "
            f"(output_lines={event.output_lines}, estimated_tokens={event.estimated_output_tokens})"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl_path", help="Path to exported Codex JSONL session.")
    parser.add_argument("--summary-output", help="Write schema version 1 analyzer summary YAML.")
    parser.add_argument("--run-id", default="", help="Benchmark run id for summary output.")
    parser.add_argument(
        "--raw-jsonl-omitted",
        action="store_true",
        help="Write summary identity for intentionally omitted raw JSONL.",
    )
    parser.add_argument("--sanitized-source", default="", help="Sanitized source label.")
    parser.add_argument("--sanitized-summary", default="", help="Sanitized summary evidence path.")
    parser.add_argument("--raw-omission-reason", default="", help="Reason raw JSONL is omitted.")
    parser.add_argument("--repo-root", default=str(ROOT), help="Repository root for stable paths.")
    parser.add_argument(
        "--justified-read",
        action="append",
        default=[],
        help="File path whose whole-file/generated-output read is justified.",
    )
    parser.add_argument("--justification", default="", help="Reason justified reads are allowed.")
    args = parser.parse_args(argv)

    if args.raw_jsonl_omitted and (
        not args.sanitized_source or not args.sanitized_summary or not args.raw_omission_reason
    ):
        sys.stderr.write(
            "error: --raw-jsonl-omitted requires --sanitized-source, "
            "--sanitized-summary, and --raw-omission-reason\n"
        )
        return 1

    try:
        jsonl_path = Path(args.jsonl_path)
        usage, events, unknown_records = read_events(jsonl_path)
    except ValueError as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 1

    if args.summary_output:
        repo_root = Path(args.repo_root)
        write_summary(
            Path(args.summary_output),
            run_id=args.run_id or Path(args.jsonl_path).stem,
            jsonl_path=jsonl_path,
            raw_jsonl_tracked=not args.raw_jsonl_omitted,
            sanitized_source=args.sanitized_source,
            sanitized_summary=args.sanitized_summary,
            raw_omission_reason=args.raw_omission_reason,
            repo_root=repo_root,
            justified_reads=justified_read_set(args.justified_read, repo_root),
            justification=args.justification,
            usage=usage,
            events=events,
        )

    output_lines = sum(event.output_lines for event in events)
    output_bytes = sum(event.output_bytes for event in events)
    output_tokens = sum(event.estimated_output_tokens for event in events)
    broad_search_events = [event for event in events if is_broad_search(event.command)]
    full_file_events = [event for event in events if is_full_file_read_event(event)]
    high_cap_events = [
        event
        for event in events
        if event.max_output_tokens is not None
        and event.max_output_tokens >= HIGH_OUTPUT_TOKEN_THRESHOLD
    ]
    ranked_outputs = sorted(events, key=lambda event: event.estimated_output_tokens, reverse=True)

    print("# Codex JSONL Session Cost")
    print()
    if usage:
        for key in sorted(USAGE_KEYS):
            if key in usage:
                print(f"{key}: {usage[key]}")
    else:
        print("token_usage: unavailable")
    print(f"tool_calls: {len(events)}")
    print(f"command_output_lines: {output_lines}")
    print(f"command_output_bytes: {output_bytes}")
    print(f"estimated_command_output_tokens: {output_tokens}")
    print(f"unknown_records: {unknown_records}")
    if output_lines == 0:
        print("note: no command-output amplification observed")
    print()
    print_event_list("largest_outputs", ranked_outputs)
    print_event_list("broad_searches", broad_search_events)
    print_event_list("full_file_reads", full_file_events)
    print_event_list("high_max_output_tokens", high_cap_events)
    repeated = repeated_file_reads(events)
    print(f"repeated_file_reads: {len(repeated)}")
    for path, count in repeated[:5]:
        print(f"  - {path}: {count}")
    print("top_cost_drivers:")
    if ranked_outputs:
        for rank, event in enumerate(ranked_outputs[:5], start=1):
            print(
                f"  {rank}. command_output estimated_tokens={event.estimated_output_tokens} "
                f"lines={event.output_lines} command={command_summary(event.command)}"
            )
    else:
        print("  - none observed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
