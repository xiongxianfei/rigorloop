#!/usr/bin/env python3
"""Validate current model packages and owned examples."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from lib.validation.boundary_first_validation import validate_repository_examples
from lib.validation.model_layout import PROJECT_MODEL_PATHS
from lib.validation.test_design_validation import validate_documents

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--root", default=".")
    parser.add_argument("--path", action="append", default=[])
    args = parser.parse_args()
    root = Path(args.root).resolve()
    paths = sorted(set(args.path or PROJECT_MODEL_PATHS.values()))
    admitted, paths = validate_documents(root, paths)
    issues = list(admitted)
    examples = ()
    if not args.path:
        examples, example_issues = validate_repository_examples(root)
        issues.extend(example_issues)
    review_required = []
    if issues:
        print(json.dumps({"status": "failed", "issues": [issue.as_dict() for issue in issues], "review_required": review_required}, sort_keys=True))
        return 1
    output = {
        "status": "passed",
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
