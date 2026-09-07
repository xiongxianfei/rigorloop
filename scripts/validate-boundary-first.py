#!/usr/bin/env python3
"""Validate boundary-first records and the durable activation baseline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from boundary_first_validation import (
    ACTIVATION_RECORD,
    rollback_package_selection,
    validate_activation,
    validate_changed_spec,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--root", default=".")
    parser.add_argument("--path", action="append", default=[])
    args = parser.parse_args()
    root = Path(args.root).resolve()
    model_only = bool(args.path) and all(path.startswith("docs/design/") for path in args.path)
    issues = [] if model_only else list(validate_activation(root))
    for path in args.path:
        issues.extend(validate_changed_spec(root, path))
    # This one diagnostic is a semantic obligation, not a structural error.
    # All other (including unknown) diagnostics continue to fail closed.
    review_required = [
        {**issue.as_dict(), "owner": "design-review"}
        for issue in issues if issue.code == "BFR-GRANDFATHERED-REVIEW"
    ]
    issues = [issue for issue in issues if issue.code != "BFR-GRANDFATHERED-REVIEW"]
    if issues:
        print(json.dumps({"status": "failed", "issues": [issue.as_dict() for issue in issues], "review_required": review_required}, sort_keys=True))
        return 1
    if model_only:
        print(json.dumps({"status": "passed", "paths": sorted(args.path), "validation": "structure-and-references-only"}, sort_keys=True))
        return 0
    output: dict[str, object] = {
        "status": "review-required" if review_required else "passed",
        "validation": "structure-and-references-only",
        "review_required": review_required,
        "activation": "validated",
        "paths": sorted(args.path),
    }
    activation_data = json.loads((root / ACTIVATION_RECORD).read_text(encoding="utf-8"))
    output["snapshot"] = activation_data["state"]
    output["release_intent"] = activation_data["activating_release"]
    if activation_data.get("state") == "active":
        selection, selection_issues = rollback_package_selection(root)
        if selection_issues or selection is None:
            print(
                json.dumps(
                    {
                        "status": "failed",
                        "issues": [issue.as_dict() for issue in selection_issues],
                        "review_required": review_required,
                    },
                    sort_keys=True,
                )
            )
            return 1
        output["rollback_release"] = selection.release
        output["rollback_artifacts"] = [
            {
                "adapter": artifact.adapter,
                "archive": artifact.archive,
                "sha256": artifact.sha256,
            }
            for artifact in selection.artifacts
        ]
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
