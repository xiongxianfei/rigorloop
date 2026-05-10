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


USAGE_KEYS = {
    "input_tokens",
    "cached_input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
}
HIGH_OUTPUT_TOKEN_THRESHOLD = 20000


@dataclass
class ToolEvent:
    command: str
    output: str
    max_output_tokens: int | None
    line_number: int

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


def find_command(record: dict[str, Any]) -> str:
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
    output_keys = {"output", "stdout", "stderr", "content", "text"}
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

            if looks_like_tool_record(record):
                events.append(
                    ToolEvent(
                        command=find_command(record),
                        output=find_output(record),
                        max_output_tokens=find_max_output_tokens(record),
                        line_number=line_number,
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


def repeated_file_reads(events: list[ToolEvent]) -> list[tuple[str, int]]:
    counts: dict[str, int] = {}
    for event in events:
        path = command_path(event.command)
        if path and is_full_file_read(event.command):
            counts[path] = counts.get(path, 0) + 1
    return sorted((path, count) for path, count in counts.items() if count > 1)


def command_summary(command: str, limit: int = 120) -> str:
    normalized = " ".join(command.split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3] + "..."


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
    args = parser.parse_args(argv)

    try:
        usage, events, unknown_records = read_events(Path(args.jsonl_path))
    except ValueError as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 1

    output_lines = sum(event.output_lines for event in events)
    output_bytes = sum(event.output_bytes for event in events)
    output_tokens = sum(event.estimated_output_tokens for event in events)
    broad_search_events = [event for event in events if is_broad_search(event.command)]
    full_file_events = [event for event in events if is_full_file_read(event.command)]
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
