#!/usr/bin/env python3
"""Validate current models or explicitly selected feature/proof records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from boundary_first_validation import validate_changed_spec, validate_repository_examples
from model_layout import PROJECT_MODEL_PATHS

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--root", default=".")
    parser.add_argument("--path", action="append", default=[])
    args = parser.parse_args()
    root = Path(args.root).resolve()
    paths = sorted(set(args.path or PROJECT_MODEL_PATHS.values()))
    issues = []
    for path in paths:
        issues.extend(validate_changed_spec(root, path))
    examples = ()
    if not args.path:
        examples, example_issues = validate_repository_examples(root)
        issues.extend(example_issues)
    # This one diagnostic is a semantic obligation, not a structural error.
    # All other (including unknown) diagnostics continue to fail closed.
    review_required = [
        {**issue.as_dict(), "owner": "design-review"}
        for issue in issues if issue.code == "BFR-ADOPTION-REVIEW"
    ]
    issues = [issue for issue in issues if issue.code != "BFR-ADOPTION-REVIEW"]
    if issues:
        print(json.dumps({"status": "failed", "issues": [issue.as_dict() for issue in issues], "review_required": review_required}, sort_keys=True))
        return 1
    output = {
        "status": "review-required" if review_required else "passed",
        "validation": "structure-and-references-only",
        "review_required": review_required,
        "paths": paths,
        "examples": list(examples),
        "example_validation": "model-document-structure-and-json-syntax",
    }
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
