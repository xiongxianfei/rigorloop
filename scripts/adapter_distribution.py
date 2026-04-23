#!/usr/bin/env python3
"""Shared helpers for generated multi-agent adapter packages."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable

from skill_validation import (
    CANONICAL_SKILLS_DIR,
    discover_source_skill_dirs,
    load_skill_file,
    load_skill_schema,
    validate_skill_file,
)


SUPPORTED_ADAPTERS = ("codex", "claude", "opencode")
DEFAULT_ADAPTER_VERSION = "0.1.0-rc.1"
ROOT = Path(__file__).resolve().parents[1]
ADAPTER_OUTPUT_ROOT = ROOT / "dist" / "adapters"
ADAPTER_TEMPLATE_ROOT = ROOT / "scripts" / "adapter_templates"
ADAPTER_OUTPUT_CONTRACT_ROOT = PurePosixPath("dist/adapters")
COMMON_FRONTMATTER = frozenset({"name", "description"})
TRANSFORMABLE_FRONTMATTER = frozenset({"argument-hint"})
PORTABLE_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CODEX_SKILL_INVOCATION_PATTERN = re.compile(r"(?<![A-Za-z0-9_])\$[a-z][a-z0-9-]*\b")
TARGET_INCOMPATIBILITY_PATTERNS = {
    "claude": re.compile(r"\bnot compatible with Claude Code\b", re.IGNORECASE),
    "opencode": re.compile(r"\bnot compatible with opencode\b", re.IGNORECASE),
}


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


def _structure_errors(path: Path) -> list[str]:
    errors, _name = validate_skill_file(path, load_skill_schema())
    return errors


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


def _target_adapter_reasons(text: str) -> dict[str, tuple[str, ...]]:
    return {
        adapter: (f"Not compatible with {adapter}.",)
        for adapter, pattern in TARGET_INCOMPATIBILITY_PATTERNS.items()
        if pattern.search(text)
    }


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
    common_errors.extend(_structure_errors(path))
    if common_errors:
        return SkillPortabilityReport(
            path=path,
            name=name or directory_name,
            description=description,
            decisions=_all_adapter_decisions(common_errors),
        )

    full_text = path.read_text(encoding="utf-8")
    non_codex_reasons = tuple(_non_codex_reasons(metadata, full_text))
    target_reasons = _target_adapter_reasons(full_text)
    non_codex_transforms = _non_codex_transforms(metadata)

    decisions: list[AdapterDecision] = [
        AdapterDecision(adapter="codex", included=True),
    ]
    for adapter in ("claude", "opencode"):
        adapter_reasons = non_codex_reasons + target_reasons.get(adapter, ())
        decisions.append(
            AdapterDecision(
                adapter=adapter,
                included=not adapter_reasons,
                reasons=adapter_reasons,
                transforms=() if adapter_reasons else non_codex_transforms,
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


def collect_skill_reports(skills_root: Path = CANONICAL_SKILLS_DIR) -> tuple[SkillPortabilityReport, ...]:
    """Evaluate canonical skills in deterministic order."""

    if not skills_root.exists():
        return ()
    reports = [evaluate_skill(directory) for directory in discover_source_skill_dirs(skills_root)]
    return tuple(sorted(reports, key=lambda report: (report.name, report.path.as_posix())))


def _path_from_posix(path: PurePosixPath) -> Path:
    return Path(*path.parts)


def _adapter_package_relative_root(config: AdapterConfig) -> Path:
    return _path_from_posix(config.package_root.relative_to(ADAPTER_OUTPUT_CONTRACT_ROOT))


def _render_frontmatter_field(key: str, value: str) -> list[str]:
    if key == "name" and PORTABLE_NAME_PATTERN.fullmatch(value):
        return [f"{key}: {value}"]

    lines = [f"{key}: >"]
    value_lines = value.splitlines() or [""]
    lines.extend(f"  {line}" for line in value_lines)
    return lines


def _render_transformed_skill(path: Path, drop_keys: tuple[str, ...]) -> str:
    metadata, body = load_skill_file(path)
    transformed_metadata = {
        key: value
        for key, value in metadata.items()
        if key in COMMON_FRONTMATTER and key not in drop_keys
    }

    lines = ["---"]
    for key in ("name", "description"):
        lines.extend(_render_frontmatter_field(key, transformed_metadata[key]))
    lines.append("---")

    text = "\n".join(lines) + "\n" + body
    if not text.endswith("\n"):
        text += "\n"
    return text


def render_skill_for_adapter(report: SkillPortabilityReport, decision: AdapterDecision) -> str:
    """Render one generated skill file for a target adapter."""

    drop_keys = tuple(
        transform.removeprefix("drop frontmatter: ")
        for transform in decision.transforms
        if transform.startswith("drop frontmatter: ")
    )
    if not drop_keys:
        return report.path.read_text(encoding="utf-8")
    return _render_transformed_skill(report.path, drop_keys)


def render_entrypoint_template(
    template_path: Path,
    *,
    version: str,
    adapter: AdapterConfig,
) -> str:
    """Render one authored thin adapter entrypoint template."""

    return template_path.read_text(encoding="utf-8").format(
        adapter=adapter.name,
        entrypoint=adapter.entrypoint.as_posix(),
        package_root=adapter.package_root.as_posix(),
        skill_root=adapter.skill_root.as_posix(),
        version=version,
    )


def expected_adapter_files(
    version: str,
    *,
    skills_root: Path = CANONICAL_SKILLS_DIR,
    template_root: Path = ADAPTER_TEMPLATE_ROOT,
) -> dict[Path, str]:
    """Return the complete expected generated adapter file map."""

    reports = collect_skill_reports(skills_root)
    expected: dict[Path, str] = {
        Path("manifest.yaml"): render_manifest_yaml(version, reports),
    }

    for adapter_name in SUPPORTED_ADAPTERS:
        config = ADAPTERS[adapter_name]
        package_root = _adapter_package_relative_root(config)
        template_path = template_root / adapter_name / _path_from_posix(config.entrypoint)
        expected[package_root / _path_from_posix(config.entrypoint)] = render_entrypoint_template(
            template_path,
            version=version,
            adapter=config,
        )

        for report in reports:
            decision = report.adapter_decision(adapter_name)
            if not decision.included:
                continue
            expected[package_root / _path_from_posix(config.skill_path(report.name))] = (
                render_skill_for_adapter(report, decision)
            )

    return dict(sorted(expected.items(), key=lambda item: item[0].as_posix()))


def _collect_generated_files(root: Path) -> dict[Path, Path]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root): path
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def collect_adapter_drift(
    version: str,
    *,
    skills_root: Path = CANONICAL_SKILLS_DIR,
    template_root: Path = ADAPTER_TEMPLATE_ROOT,
    output_root: Path = ADAPTER_OUTPUT_ROOT,
) -> list[str]:
    """Collect missing, stale, and unexpected generated adapter output."""

    expected = expected_adapter_files(
        version,
        skills_root=skills_root,
        template_root=template_root,
    )
    existing = _collect_generated_files(output_root)
    errors: list[str] = []

    for relative_path, expected_text in expected.items():
        generated_path = output_root / relative_path
        if relative_path not in existing:
            errors.append(f"missing generated adapter file: {generated_path}")
            continue
        if existing[relative_path].read_text(encoding="utf-8") != expected_text:
            errors.append(f"stale generated adapter file: {generated_path}")

    for relative_path in sorted(set(existing) - set(expected)):
        errors.append(f"unexpected generated adapter file: {output_root / relative_path}")

    return errors


def _remove_empty_directories(root: Path) -> None:
    if not root.exists():
        return
    directories = sorted(
        (path for path in root.rglob("*") if path.is_dir()),
        key=lambda path: len(path.parts),
        reverse=True,
    )
    for directory in directories:
        try:
            directory.rmdir()
        except OSError:
            continue


def sync_adapter_output(
    version: str,
    *,
    skills_root: Path = CANONICAL_SKILLS_DIR,
    template_root: Path = ADAPTER_TEMPLATE_ROOT,
    output_root: Path = ADAPTER_OUTPUT_ROOT,
) -> None:
    """Synchronize generated adapter output with canonical sources."""

    expected = expected_adapter_files(
        version,
        skills_root=skills_root,
        template_root=template_root,
    )
    existing = _collect_generated_files(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    for relative_path, expected_text in expected.items():
        target_path = output_root / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        if not target_path.exists() or target_path.read_text(encoding="utf-8") != expected_text:
            target_path.write_text(expected_text, encoding="utf-8")

    for relative_path in sorted(set(existing) - set(expected), reverse=True):
        path = output_root / relative_path
        if path.exists():
            path.unlink()

    _remove_empty_directories(output_root)
