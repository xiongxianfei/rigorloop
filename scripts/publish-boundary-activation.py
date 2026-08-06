#!/usr/bin/env python3
"""Explicit CLI boundary for boundary-first activation publication."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from boundary_activation_release import (
    PublicationError,
    check_publication,
    error_payload,
    publish_activation,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--publish", action="store_true")
    parser.add_argument("--release", required=True)
    parser.add_argument("--candidate-evidence", required=True, type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        result = (
            publish_activation(args.root, args.release, args.candidate_evidence)
            if args.publish
            else check_publication(args.root, args.release, args.candidate_evidence)
        )
    except PublicationError as error:
        print(json.dumps(error_payload(error), sort_keys=True))
        return 2
    payload = {"status": "published" if args.publish else "ready", **result.as_dict()}
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
