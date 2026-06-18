#!/usr/bin/env python3
"""Validate cross-guide source-of-truth alignment."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from skill_validation import validate_workflow_artifact_map_contract


PRIMARY_GUIDE_LINKS = (
    "VISION.md",
    "CONSTITUTION.md",
    "docs/workflows.md",
    "docs/project-map.md",
    "docs/plan.md",
    "skills/",
)

PLAN_INDEX_REQUIRED_HEADINGS = (
    "## Active",
    "## Blocked",
    "## Done (recent)",
    "## Superseded",
)

PLAN_INDEX_FORBIDDEN_HEADINGS = (
    "## Current Handoff Summary",
    "## Milestones",
    "## Implementation steps",
    "## Validation notes",
    "## Review summary",
    "## Full transcript",
)

GUIDE_REGISTRY_PATTERN = re.compile(
    r"```ya?ml\s*\n(?P<body>.*?\n)```",
    flags=re.IGNORECASE | re.DOTALL,
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


def _has_heading(text: str, heading: str) -> bool:
    return re.search(rf"^{re.escape(heading)}\s*$", text, flags=re.MULTILINE) is not None


def _markdown_links(text: str) -> set[str]:
    links = set(re.findall(r"\[[^\]]+\]\(([^)]+)\)", text))
    links.update(re.findall(r"<([^>\s]+)>", text))
    return links


def _yaml_registry_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    for match in GUIDE_REGISTRY_PATTERN.finditer(text):
        body = match.group("body")
        if re.search(r"^artifact_locations:\s*$", body, flags=re.MULTILINE):
            blocks.append(body)
    return blocks


def _validate_readme(repo: Path, messages: list[str]) -> None:
    text = _read(repo / "README.md")
    missing = [link for link in PRIMARY_GUIDE_LINKS if link not in _markdown_links(text)]
    if not _has_heading(text, "## Where to go next") or missing:
        missing_text = ", ".join(missing) if missing else "none"
        messages.append(
            "GUIDE-001: README.md must include a 'Where to go next' guide index "
            f"linking primary guides; missing links: {missing_text}"
        )


def _validate_workflow_guide(repo: Path, messages: list[str]) -> None:
    text = _read(repo / "docs/workflows.md")
    required_headings = ("## Guide ownership", "## Artifact registry", "## Artifact locations")
    missing = [heading for heading in required_headings if not _has_heading(text, heading)]
    if missing:
        messages.append(
            "GUIDE-002: docs/workflows.md must include guide ownership, artifact "
            f"registry, and artifact-location sections; missing: {', '.join(missing)}"
        )

    lower = text.lower()
    ownership_terms_present = (
        "stage skill" in lower
        and "portable default" in lower
        and "artifact content" in lower
        and "workflow guide routes" in lower
    )
    skill_route_present = "`skills/<stage>/skill.md`" in lower
    if not (ownership_terms_present and skill_route_present):
        messages.append(
            "GUIDE-003: docs/workflows.md must distinguish guide ownership from "
            "stage-skill content ownership and portable defaults"
        )

    workflow_errors = validate_workflow_artifact_map_contract(repo / "docs/workflows.md", text)
    for error in workflow_errors:
        messages.append(f"GUIDE-008: workflow map contract failed: {error}")


def _validate_project_map(repo: Path, messages: list[str]) -> None:
    text = _read(repo / "docs/project-map.md")
    lower = text.lower()
    boundary_terms_present = (
        "does not own" in lower
        and "workflow stage order" in lower
        and "exact lifecycle artifact placement" in lower
        and "current milestone state" in lower
    )
    owns_workflow_policy = bool(
        re.search(
            r"\b(?:this map|project-map|docs/project-map\.md|project map)\b[^.\n]{0,80}"
            r"\bowns?\b[^.\n]{0,80}\b(?:workflow stage order|artifact placement)\b",
            lower,
        )
    )
    if not boundary_terms_present or owns_workflow_policy:
        messages.append(
            "GUIDE-004: docs/project-map.md must orient to repository structure "
            "and must not own workflow stage order or artifact placement"
        )


def _validate_plan_index(repo: Path, messages: list[str]) -> None:
    text = _read(repo / "docs/plan.md")
    missing = [heading for heading in PLAN_INDEX_REQUIRED_HEADINGS if not _has_heading(text, heading)]
    forbidden = [heading for heading in PLAN_INDEX_FORBIDDEN_HEADINGS if _has_heading(text, heading)]
    lower = text.lower()
    index_boundary_present = "bounded lifecycle index" in lower or "not the body of a plan" in lower
    if missing or forbidden or not index_boundary_present:
        detail = []
        if missing:
            detail.append("missing " + ", ".join(missing))
        if forbidden:
            detail.append("forbidden " + ", ".join(forbidden))
        if not index_boundary_present:
            detail.append("missing bounded-index boundary wording")
        messages.append("GUIDE-005: docs/plan.md must remain a bounded live-work index; " + "; ".join(detail))


def _validate_learn_sessions(repo: Path, messages: list[str]) -> None:
    learn_root = repo / "docs/learn/sessions"
    if not learn_root.exists():
        return
    for path in sorted(learn_root.glob("*.md")):
        text = _read(path).lower()
        if "live routing authority" not in text:
            continue
        if re.search(r"\bnot\s+(?:be\s+)?(?:treated\s+as\s+)?live routing authority\b", text):
            continue
        if "not live routing authority" in text:
            continue
        messages.append(
            "GUIDE-006: learn sessions must not be cited as live routing authority "
            f"without promotion to the owning guide or contract: {path.relative_to(repo)}"
        )


def _validate_stage_skill_plan_defaults(repo: Path, messages: list[str]) -> None:
    workflow = _read(repo / "skills/workflow/SKILL.md")
    plan = _read(repo / "skills/plan/SKILL.md")
    workflow_lower = workflow.lower()
    plan_lower = plan.lower()

    workflow_has_current_paths = (
        "`docs/plans/yyyy-mm-dd-slug.md`" in workflow_lower
        and "`docs/plan.md`" in workflow_lower
    )
    workflow_rejects_change_local_plan = (
        "`docs/changes/<change-id>/plan.md`" in workflow_lower
        and "non-canonical" in workflow_lower
    )
    plan_has_current_paths = (
        "`docs/plan.md`" in plan_lower
        and "`docs/plans/yyyy-mm-dd-slug.md`" in plan_lower
    )
    if not (workflow_has_current_paths and workflow_rejects_change_local_plan and plan_has_current_paths):
        messages.append(
            "GUIDE-007: workflow and plan skills must keep portable plan defaults "
            "aligned with docs/plan.md as index and docs/plans/YYYY-MM-DD-slug.md as plan body"
        )


def _validate_registry_not_duplicated(repo: Path, messages: list[str]) -> None:
    allowed = repo / "docs/workflows.md"
    surfaces = (
        repo / "README.md",
        repo / "docs/project-map.md",
        repo / "docs/plan.md",
        repo / "VISION.md",
        repo / "CONSTITUTION.md",
    )
    for path in surfaces:
        if path == allowed or not path.exists():
            continue
        if _yaml_registry_blocks(_read(path)):
            messages.append(
                "GUIDE-008: canonical artifact_locations registry must not be "
                f"duplicated outside docs/workflows.md: {path.relative_to(repo)}"
            )


def validate(repo: Path) -> ValidationResult:
    messages: list[str] = []
    repo = repo.resolve()
    _validate_readme(repo, messages)
    _validate_workflow_guide(repo, messages)
    _validate_project_map(repo, messages)
    _validate_plan_index(repo, messages)
    _validate_learn_sessions(repo, messages)
    _validate_stage_skill_plan_defaults(repo, messages)
    _validate_registry_not_duplicated(repo, messages)
    return ValidationResult(tuple(messages))


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root to validate. Defaults to the current directory.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    result = validate(Path(args.root))
    if result.ok:
        print("guide system validation passed")
        return 0
    for message in result.messages:
        print(message, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
