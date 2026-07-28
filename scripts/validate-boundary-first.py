#!/usr/bin/env python3
"""Validate boundary-first records and the durable activation baseline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from boundary_first_validation import validate_activation, validate_changed_spec


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--root", default=".")
    parser.add_argument("--path", action="append", default=[])
    args = parser.parse_args()
    root = Path(args.root).resolve()
    issues = list(validate_activation(root))
    for path in args.path:
        issues.extend(validate_changed_spec(root, path))
    if issues:
        print(json.dumps({"status": "failed", "issues": [issue.as_dict() for issue in issues]}, sort_keys=True))
        return 1
    print(json.dumps({"status": "passed", "activation": "validated", "paths": sorted(args.path)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
