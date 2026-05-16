#!/usr/bin/env python3
"""Validate the public RigorLoop npm package metadata or tarball."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from npm_package_validation import NpmPackageValidationError, inspect_package_json, inspect_package_tarball


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", default="packages/rigorloop")
    parser.add_argument("--tarball")
    args = parser.parse_args(argv)

    try:
        inspect_package_json(Path(args.package_root))
        if args.tarball:
            inspect_package_tarball(Path(args.tarball))
    except NpmPackageValidationError as exc:
        print(f"npm package validation failed: {exc}", file=sys.stderr)
        return 1

    print("npm package validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
