#!/usr/bin/env python3
"""Validate current routing and contributor-guide source-of-truth alignment."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


PRIMARY_GUIDE_LINKS = (
    "VISION.md",
    "CONSTITUTION.md",
    "docs/project-map.md",
    "docs/plan.md",
    "skills/",
)


@dataclass(frozen=True)
class ValidationResult:
    messages: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.messages


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _markdown_links(text: str) -> set[str]:
    links = set(re.findall(r"\[[^\]]+\]\(([^)]+)\)", text))
    links.update(re.findall(r"<([^>\s]+)>", text))
    return links


def validate(repo: Path) -> ValidationResult:
    repo = repo.resolve()
    messages: list[str] = []
    readme = _read(repo / "README.md")
    links = _markdown_links(readme)
    missing = [path for path in PRIMARY_GUIDE_LINKS if path not in links]
    if "## Where to go next" not in readme or missing:
        messages.append(
            "ROUTE-GUIDE-001: README.md must link current governance, orientation, "
            f"planning, and skill surfaces; missing: {', '.join(missing) or 'none'}"
        )
    if "docs/workflows.md" in readme:
        messages.append("ROUTE-GUIDE-002: README.md must not grant authority to the retired workflow guide")

    if (repo / "docs" / "workflows.md").exists():
        messages.append("ROUTE-GUIDE-003: current repository must not contain docs/workflows.md")

    route_root = repo / "skills" / "route"
    workflow_root = repo / "skills" / "workflow"
    if not (route_root / "SKILL.md").is_file() or workflow_root.exists():
        messages.append("ROUTE-GUIDE-004: canonical inventory must contain route and no workflow skill")
    for retired in (
        route_root / "references" / "workflow-guide-authoring.md",
        route_root / "assets" / "workflows-skeleton.md",
    ):
        if retired.exists():
            messages.append(f"ROUTE-GUIDE-005: retired guide resource remains: {retired.relative_to(repo)}")

    current_surfaces = (
        repo / "AGENTS.md",
        repo / "CONSTITUTION.md",
        repo / "README.md",
        repo / "docs" / "project-map.md",
        repo / "specs" / "rigorloop-workflow.md",
        repo / "specs" / "skill-contract.md",
    )
    for path in current_surfaces:
        text = _read(path)
        if "docs/workflows.md" in text or "skills/workflow" in text or "`workflow` skill" in text:
            messages.append(
                f"ROUTE-GUIDE-006: current surface retains retired authority: {path.relative_to(repo)}"
            )

    project_map = _read(repo / "docs" / "project-map.md").lower()
    required_map_terms = (
        "does not own workflow stage order",
        "cli owns deterministic workflow-context",
        "route",
    )
    if any(term not in project_map for term in required_map_terms):
        messages.append("ROUTE-GUIDE-007: project map must preserve orientation and route/CLI authority boundaries")

    plan_index = _read(repo / "docs" / "plan.md").lower()
    if not all(term in plan_index for term in ("navigation index", "owning change", "change.yaml")):
        messages.append("ROUTE-GUIDE-008: docs/plan.md must remain a bounded navigation index")

    return ValidationResult(tuple(messages))


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    result = validate(Path(args.root))
    if result.ok:
        print("Route and contributor-guide validation passed.")
        return 0
    for message in result.messages:
        print(message, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
