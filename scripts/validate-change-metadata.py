#!/usr/bin/env python3
"""Validate current v3 record sets without interpreting retired cache evidence."""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate_file(path: Path) -> list[str]:
    if path.name == "validation-cache-measurement.yaml":
        return ["unsupported validation-cache measurement input; use current validation evidence"]
    # No legacy decoder: complete-set contract-selected validation owns format and path safety,
    # including malformed JSON, duplicate keys, symlinks and an absent manifest.
    try:
        result = subprocess.run(
            ["node", str(ROOT / "scripts/validate-record-store.mjs"), str(path.absolute())],
            capture_output=True, text=True, timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ["current record validator unavailable"]
    return [] if result.returncode == 0 else ["invalid or unsupported record set; supported contract is rigorloop-records-v3"]


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(
            "usage: validate-change-metadata.py <change.json> [...]",
            file=sys.stderr,
        )
        return 2

    exit_code = 0
    for raw_path in argv[1:]:
        path = Path(raw_path)
        try:
            errors = validate_file(path)
        except FileNotFoundError:
            print(f"{path}: file not found", file=sys.stderr)
            exit_code = 1
            continue
        except OSError as exc:
            print(f"{path}: invalid change metadata", file=sys.stderr)
            print(f"  - {exc}", file=sys.stderr)
            exit_code = 1
            continue

        if errors:
            print(f"{path}: invalid change metadata", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
            exit_code = 1
            continue

        print(f"{path}: valid change metadata")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
