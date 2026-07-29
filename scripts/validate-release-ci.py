#!/usr/bin/env python3
"""Compatibility wrapper for recorded-source release validation."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

def main(argv: list[str] | None = None) -> int:
    canonical = Path(__file__).with_name("validate-release.py")
    completed = subprocess.run(
        [
            sys.executable,
            str(canonical),
            "--recorded-source-auto",
            *(argv if argv is not None else sys.argv[1:]),
        ]
    )
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
