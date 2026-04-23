#!/usr/bin/env python3
"""Shared helpers for generated multi-agent adapter packages."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable

from skill_validation import load_skill_file


SUPPORTED_ADAPTERS = ("codex", "claude", "opencode")
COMMON_FRONTMATTER = frozenset({"name", "description"})
TRANSFORMABLE_FRONTMATTER = frozenset({"argument-hint"})
PORTABLE_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CODEX_SKILL_INVOCATION_PATTERN = re.compile(r"(?<![A-Za-z0-9_])\$[a-z][a-z0-9-]*\b")


@dataclass(frozen=True)
class AdapterConfig:
    name: str
    package_root: PurePosixPath
    entrypoint: PurePosixPath
    skill_root: PurePosixPath

    def skill_path(self, skill_name: str) -> PurePosixPath:
        return self.skill_root / skill_name / "SKILL.md"


@dataclass(frozen=True)
class AdapterDecision:
    adapter: str
    included: bool
    reasons: tuple[str, ...] = ()
    transforms: tuple[str, ...] = ()


@dataclass(frozen=True)
class SkillPortabilityReport:
    path: Path
    name: str
    description: str
    decisions: tuple[AdapterDecision, ...]

    @property
    def included_adapters(self) -> tuple[str, ...]:
        return tuple(decision.adapter for decision in self.decisions if decision.included)

    @property
    def portable(self) -> bool:
        return self.included_adapters == SUPPORTED_ADAPTERS

    @property
    def reason(self) -> str:
        reasons: list[str] = []
        for decision in self.decisions:
            for reason in decision.reasons:
                if reason not in reasons:
                    reasons.append(reason)
        return " ".join(reasons)

    def adapter_decision(self, adapter: str) -> AdapterDecision:
        for decision in self.decisions:
            if decision.adapter == adapter:
                return decision
        raise KeyError(adapter)


ADAPTERS = {
    "codex": AdapterConfig(
        name="codex",
        package_root=PurePosixPath("dist/adapters/codex"),
        entrypoint=PurePosixPath("AGENTS.md"),
        skill_root=PurePosixPath(".agents/skills"),
    ),
    "claude": AdapterConfig(
        name="claude",
        package_root=PurePosixPath("dist/adapters/claude"),
        entrypoint=PurePosixPath("CLAUDE.md"),
        skill_root=PurePosixPath(".claude/skills"),
    ),
    "opencode": AdapterConfig(
        name="opencode",
        package_root=PurePosixPath("dist/adapters/opencode"),
        entrypoint=PurePosixPath("AGENTS.md"),
        skill_root=PurePosixPath(".opencode/skills"),
    ),
}


def _skill_file(target: Path) -> Path:
    return target if target.name == "SKILL.md" else target / "SKILL.md"


def _normalize_description(value: str | None) -> str:
    return value.strip() if isinstance(value, str) else ""


def _portable_name_errors(name: str, directory_name: str) -> list[str]:
    errors: list[str] = []
    if not name:
        errors.append("Invalid portable skill name: name is required.")
        return errors
    if len(name) > 64:
        errors.append("Invalid portable skill name: name must be 64 characters or fewer.")
    if not PORTABLE_NAME_PATTERN.fullmatch(name):
        errors.append(
            "Invalid portable skill name: use lowercase alphanumeric tokens separated by single hyphens."
        )
    if name != directory_name:
        errors.append("Invalid portable skill name: name must match the generated skill directory.")
    return errors


def _description_errors(description: str) -> list[str]:
    if not description:
        return ["Invalid portable description: description is required."]
    if len(description) > 1024:
        return ["Invalid portable description: description must be 1024 characters or fewer."]
    return []


def _non_codex_reasons(metadata: dict[str, str], text: str) -> list[str]:
    reasons: list[str] = []
    unsupported = sorted(set(metadata) - COMMON_FRONTMATTER - TRANSFORMABLE_FRONTMATTER)
    if unsupported:
        reasons.append(f"Uses unsupported frontmatter: {', '.join(unsupported)}.")
    if re.search(r"\bCodex-only invocation syntax\b", text, re.IGNORECASE):
        reasons.append("Requires Codex-only invocation syntax.")
    if "agents/openai.yaml" in text:
        reasons.append("Depends on agents/openai.yaml.")
    if ".codex/skills" in text:
        reasons.append("References .codex/skills as the only install location.")
    if CODEX_SKILL_INVOCATION_PATTERN.search(text):
        reasons.append("Requires Codex-specific $skill invocation.")
    if _has_codex_runtime_assumption(text):
        reasons.append("Assumes Codex-only tool, UI, approval, or runtime assumption.")
    return reasons


def _has_codex_runtime_assumption(text: str) -> bool:
    lowered = text.lower()
    return any(
        marker in lowered
        for marker in (
            "sandbox_permissions",
            "codex approval behavior",
            "codex-only tool",
            "codex-only ui",
            "codex runtime",
        )
    )


def _non_codex_transforms(metadata: dict[str, str]) -> tuple[str, ...]:
    return tuple(
        f"drop frontmatter: {key}"
        for key in sorted(set(metadata) & TRANSFORMABLE_FRONTMATTER)
    )


def _all_adapter_decisions(reasons: Iterable[str]) -> tuple[AdapterDecision, ...]:
    reason_tuple = tuple(reasons)
    return tuple(
        AdapterDecision(adapter=adapter, included=False, reasons=reason_tuple)
        for adapter in SUPPORTED_ADAPTERS
    )


def evaluate_skill(target: Path) -> SkillPortabilityReport:
    """Classify one canonical skill for first-public-release adapter inclusion."""

    path = _skill_file(target)
    directory_name = path.parent.name
    try:
        metadata, body = load_skill_file(path)
    except (OSError, ValueError) as exc:
        return SkillPortabilityReport(
            path=path,
            name=directory_name,
            description="",
            decisions=_all_adapter_decisions([str(exc)]),
        )

    name = _normalize_description(metadata.get("name"))
    description = _normalize_description(metadata.get("description"))
    common_errors = _portable_name_errors(name, directory_name)
    common_errors.extend(_description_errors(description))
    if common_errors:
        return SkillPortabilityReport(
            path=path,
            name=name or directory_name,
            description=description,
            decisions=_all_adapter_decisions(common_errors),
        )

    full_text = path.read_text(encoding="utf-8")
    non_codex_reasons = tuple(_non_codex_reasons(metadata, full_text))
    non_codex_transforms = _non_codex_transforms(metadata)

    decisions: list[AdapterDecision] = [
        AdapterDecision(adapter="codex", included=True),
    ]
    for adapter in ("claude", "opencode"):
        decisions.append(
            AdapterDecision(
                adapter=adapter,
                included=not non_codex_reasons,
                reasons=non_codex_reasons,
                transforms=() if non_codex_reasons else non_codex_transforms,
            )
        )

    return SkillPortabilityReport(
        path=path,
        name=name,
        description=description,
        decisions=tuple(decisions),
    )


def _yaml_double_quoted(value: str) -> str:
    replacements = {
        "\\": "\\\\",
        '"': '\\"',
        "\b": "\\b",
        "\f": "\\f",
        "\n": "\\n",
        "\r": "\\r",
        "\t": "\\t",
    }
    return '"' + "".join(replacements.get(char, char) for char in value) + '"'


def render_manifest_yaml(version: str, reports: Iterable[SkillPortabilityReport]) -> str:
    """Render the constrained generated adapter manifest shape deterministically."""

    lines = [f"version: {version}", "skills:"]
    for report in sorted(reports, key=lambda item: item.name):
        lines.append(f"  {report.name}:")
        lines.append(f"    portable: {str(report.portable).lower()}")
        lines.append(f"    adapters: [{', '.join(report.included_adapters)}]")
        if not report.portable:
            lines.append(f"    reason: {_yaml_double_quoted(report.reason)}")
    lines.append("")
    return "\n".join(lines)
