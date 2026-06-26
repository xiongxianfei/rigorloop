#!/usr/bin/env python3
"""Validate requirement-fidelity representative spec-read logs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path}: log must be a JSON object")
    return data


def iter_logs(review_set: Path) -> list[Path]:
    if not review_set.exists():
        raise ValueError(f"{review_set}: review set does not exist")
    if not review_set.is_dir():
        raise ValueError(f"{review_set}: review set must be a directory")
    logs = sorted(review_set.rglob("spec-read-log.json"))
    if not logs:
        raise ValueError(f"{review_set}: no spec-read-log.json files found")
    return logs


def validate_log(
    path: Path,
    *,
    max_bytes_per_clause: int,
    assert_no_broad_reads: bool,
) -> list[str]:
    errors: list[str] = []
    data = load_json(path)
    reads = data.get("reads")
    if not isinstance(reads, list) or not reads:
        return [f"{path}: reads must be a non-empty list"]

    for index, read in enumerate(reads, start=1):
        prefix = f"{path}: reads[{index}]"
        if not isinstance(read, dict):
            errors.append(f"{prefix}: read entry must be an object")
            continue
        clause_id = read.get("clause_id")
        bytes_read = read.get("bytes_read")
        full_file = read.get("full_file")
        if not isinstance(clause_id, str) or not clause_id:
            errors.append(f"{prefix}: clause_id must be non-empty")
        if not isinstance(bytes_read, int) or bytes_read < 0:
            errors.append(f"{prefix}: bytes_read must be a non-negative integer")
        elif bytes_read > max_bytes_per_clause:
            errors.append(
                f"{prefix}: {bytes_read} bytes exceeds max {max_bytes_per_clause}"
            )
        if not isinstance(full_file, bool):
            errors.append(f"{prefix}: full_file must be boolean")
        elif assert_no_broad_reads and full_file:
            errors.append(f"{prefix}: full spec-file read is not allowed")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-set", required=True, type=Path)
    parser.add_argument("--max-bytes-per-clause", required=True, type=int)
    parser.add_argument("--assert-no-broad-reads", action="store_true")
    args = parser.parse_args(argv)

    errors: list[str] = []
    try:
        logs = iter_logs(args.review_set)
        for log in logs:
            errors.extend(
                validate_log(
                    log,
                    max_bytes_per_clause=args.max_bytes_per_clause,
                    assert_no_broad_reads=args.assert_no_broad_reads,
                )
            )
    except ValueError as exc:
        errors.append(str(exc))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"validated {len(logs)} requirement-fidelity spec-read log(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

