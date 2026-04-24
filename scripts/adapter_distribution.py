#!/usr/bin/env python3
"""Shared helpers for generated multi-agent adapter packages."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from skill_validation import (
    CANONICAL_SKILLS_DIR,
    discover_source_skill_dirs,
    load_skill_file,
    load_skill_schema,
    validate_skill_file,
)


SUPPORTED_ADAPTERS = ("codex", "claude", "opencode")
DEFAULT_ADAPTER_VERSION = "0.1.1"
OPENCODE_COMMAND_ALIASES = (
    "proposal",
    "proposal-review",
    "spec",
    "spec-review",
    "plan",
    "plan-review",
    "test-spec",
    "implement",
    "code-review",
    "pr",
)
ROOT = Path(__file__).resolve().parents[1]
ADAPTER_OUTPUT_ROOT = ROOT / "dist" / "adapters"
ADAPTER_TEMPLATE_ROOT = ROOT / "scripts" / "adapter_templates"
RELEASE_ROOT = ROOT / "docs" / "releases"
ADAPTER_OUTPUT_CONTRACT_ROOT = PurePosixPath("dist/adapters")
OPENCODE_COMMAND_ROOT = PurePosixPath(".opencode/commands")
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


@dataclass(frozen=True)
class ManifestSkillEntry:
    name: str
    portable: bool
    adapters: tuple[str, ...]
    reason: str = ""


@dataclass(frozen=True)
class CommandAliasSection:
    count: int
    aliases: dict[str, str]


@dataclass(frozen=True)
class AdapterManifest:
    version: str
    skills: dict[str, ManifestSkillEntry]
    command_aliases: dict[str, CommandAliasSection]


@dataclass(frozen=True)
class SmokeRow:
    result: str
    tool_version: str
    evidence: str
    reason: str
    owner: str


@dataclass(frozen=True)
class ReleaseMetadata:
    version: str
    release_type: str
    manifest_version: str
    supported_tools: tuple[str, ...]
    adapter_paths: dict[str, str]
    instruction_entrypoints: dict[str, str]
    smoke: dict[str, SmokeRow]
    validation: dict[str, str]


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


RELEASE_TARGETS = {
    "v0.1.0-rc.1": ("rc", "0.1.0-rc.1"),
    "v0.1.0": ("final", "0.1.0"),
    "v0.1.1": ("final", "0.1.1"),
}
REQUIRED_RELEASE_VALIDATION_KEYS = (
    "generated_sync",
    "release_notes_consistency",
    "placeholder_release_check",
    "security",
)
PLACEHOLDER_RELEASE_PATTERNS = (
    "Replace this script with repository-specific release checks",
    "TODO: release checks",
    "placeholder release check",
)


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
    if _references_codex_skills_as_only_install_location(text):
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


def _references_codex_skills_as_only_install_location(text: str) -> bool:
    if ".codex/skills" not in text:
        return False

    lowered = text.lower()
    alternative_markers = (
        "dist/adapters/",
        ".agents/skills",
        ".claude/skills",
        ".opencode/skills",
    )
    return not any(marker in lowered for marker in alternative_markers)


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

    report_tuple = tuple(reports)
    if _supports_opencode_command_aliases(version):
        missing_alias_skills = _opencode_command_alias_missing_skill_errors(report_tuple)
        if missing_alias_skills:
            raise ValueError("\n".join(missing_alias_skills))

    lines = [f"version: {version}", "skills:"]
    for report in sorted(report_tuple, key=lambda item: item.name):
        lines.append(f"  {report.name}:")
        lines.append(f"    portable: {str(report.portable).lower()}")
        lines.append(f"    adapters: [{', '.join(report.included_adapters)}]")
        if not report.portable:
            lines.append(f"    reason: {_yaml_double_quoted(report.reason)}")
    if _supports_opencode_command_aliases(version):
        lines.append("command_aliases:")
        lines.append("  opencode:")
        lines.append(f"    count: {len(OPENCODE_COMMAND_ALIASES)}")
        lines.append("    aliases:")
        for alias, alias_path in _expected_opencode_command_alias_paths().items():
            lines.append(f"      {alias}: {alias_path}")
    lines.append("")
    return "\n".join(lines)


def _strip_manifest_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        quote = value[0]
        value = value[1:-1]
        if quote == '"':
            replacements = {
                "\\\\": "\\",
                '\\"': '"',
                "\\b": "\b",
                "\\f": "\f",
                "\\n": "\n",
                "\\r": "\r",
                "\\t": "\t",
            }
            for escaped, plain in replacements.items():
                value = value.replace(escaped, plain)
    return value


def _parse_manifest_adapter_list(value: str, path: Path, key: str) -> tuple[str, ...]:
    stripped = value.strip()
    if not stripped.startswith("[") or not stripped.endswith("]"):
        raise ValueError(f"{path}: {key}: adapters must use inline list syntax")
    body = stripped[1:-1].strip()
    if not body:
        return ()
    return tuple(item.strip() for item in body.split(",") if item.strip())


def _parse_manifest_bool(value: str, path: Path, key: str) -> bool:
    stripped = value.strip()
    if stripped == "true":
        return True
    if stripped == "false":
        return False
    raise ValueError(f"{path}: {key}: expected true or false")


def parse_manifest_yaml(text: str, path: Path = Path("manifest.yaml")) -> AdapterManifest:
    """Parse the constrained generated adapter manifest shape."""

    data = _parse_simple_yaml(text, path)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected top-level mapping")
    version = data.get("version")
    if not isinstance(version, str) or not version:
        raise ValueError(f"{path}: version must not be empty")
    skills_data = data.get("skills")
    if not isinstance(skills_data, dict):
        raise ValueError(f"{path}: missing top-level skills mapping")
    skills: dict[str, ManifestSkillEntry] = {}
    for skill_name, fields in skills_data.items():
        if not isinstance(skill_name, str) or not skill_name:
            raise ValueError(f"{path}: skill name must not be empty")
        if not isinstance(fields, dict):
            raise ValueError(f"{path}: {skill_name}: expected mapping")
        missing = {"portable", "adapters"} - set(fields)
        if missing:
            raise ValueError(f"{path}: {skill_name}: missing fields: {', '.join(sorted(missing))}")
        skills[skill_name] = ManifestSkillEntry(
            name=skill_name,
            portable=_parse_manifest_bool(str(fields["portable"]), path, f"{skill_name}.portable"),
            adapters=_parse_manifest_adapter_list(str(fields["adapters"]), path, f"{skill_name}.adapters"),
            reason=_strip_manifest_quotes(str(fields.get("reason", ""))),
        )

    command_aliases: dict[str, CommandAliasSection] = {}
    command_aliases_data = data.get("command_aliases", {})
    if command_aliases_data:
        if not isinstance(command_aliases_data, dict):
            raise ValueError(f"{path}: command_aliases: expected mapping")
        for tool, section in command_aliases_data.items():
            if not isinstance(tool, str) or not tool:
                raise ValueError(f"{path}: command_aliases: tool name must not be empty")
            if not isinstance(section, dict):
                raise ValueError(f"{path}: command_aliases.{tool}: expected mapping")
            count_value = section.get("count")
            try:
                count = int(str(count_value))
            except (TypeError, ValueError):
                raise ValueError(f"{path}: command_aliases.{tool}.count: expected integer") from None
            aliases = section.get("aliases")
            if not isinstance(aliases, dict):
                raise ValueError(f"{path}: command_aliases.{tool}.aliases: expected mapping")
            alias_map: dict[str, str] = {}
            for alias, alias_path in aliases.items():
                if not isinstance(alias, str) or not isinstance(alias_path, str):
                    raise ValueError(
                        f"{path}: command_aliases.{tool}.aliases: expected string keys and values"
                    )
                alias_map[alias] = alias_path
            command_aliases[tool] = CommandAliasSection(count=count, aliases=alias_map)

    return AdapterManifest(version=version, skills=skills, command_aliases=command_aliases)


@dataclass(frozen=True)
class _YamlLine:
    indent: int
    text: str
    lineno: int


def _parse_simple_yaml_scalar(value: str) -> str:
    stripped = value.strip()
    if len(stripped) >= 2 and stripped[0] == stripped[-1] and stripped[0] in {"'", '"'}:
        return _strip_manifest_quotes(stripped)
    return stripped


def _tokenize_simple_yaml(text: str, path: Path) -> list[_YamlLine]:
    rows: list[_YamlLine] = []
    for lineno, raw_line in enumerate(text.splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if "\t" in raw_line:
            raise ValueError(f"{path}: line {lineno}: tabs are not supported")
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        if indent % 2:
            raise ValueError(f"{path}: line {lineno}: indentation must use multiples of two spaces")
        rows.append(_YamlLine(indent=indent, text=raw_line[indent:], lineno=lineno))
    return rows


def _split_simple_yaml_mapping(text: str, path: Path, lineno: int) -> tuple[str, str]:
    if ":" not in text:
        raise ValueError(f"{path}: line {lineno}: expected key: value")
    key, value = text.split(":", 1)
    key = key.strip()
    if not key:
        raise ValueError(f"{path}: line {lineno}: mapping key must not be empty")
    return key, value.lstrip()


def _parse_simple_yaml_block(
    rows: list[_YamlLine],
    index: int,
    indent: int,
    path: Path,
) -> tuple[Any, int]:
    if index >= len(rows):
        raise ValueError(f"{path}: unexpected end of file")
    row = rows[index]
    if row.indent != indent:
        raise ValueError(f"{path}: line {row.lineno}: expected indentation {indent}, found {row.indent}")
    if row.text.startswith("- "):
        return _parse_simple_yaml_list(rows, index, indent, path)
    return _parse_simple_yaml_mapping(rows, index, indent, path)


def _parse_simple_yaml_mapping(
    rows: list[_YamlLine],
    index: int,
    indent: int,
    path: Path,
) -> tuple[dict[str, Any], int]:
    data: dict[str, Any] = {}
    while index < len(rows):
        row = rows[index]
        if row.indent < indent:
            break
        if row.indent > indent:
            raise ValueError(f"{path}: line {row.lineno}: unexpected indentation inside mapping")
        if row.text.startswith("- "):
            raise ValueError(f"{path}: line {row.lineno}: unexpected list item inside mapping")

        key, remainder = _split_simple_yaml_mapping(row.text, path, row.lineno)
        index += 1
        if remainder:
            data[key] = _parse_simple_yaml_scalar(remainder)
            continue
        if index >= len(rows) or rows[index].indent <= indent:
            data[key] = ""
            continue
        child_indent = rows[index].indent
        if child_indent != indent + 2:
            raise ValueError(
                f"{path}: line {rows[index].lineno}: nested block for {key} "
                "must be indented by two spaces"
            )
        data[key], index = _parse_simple_yaml_block(rows, index, child_indent, path)
    return data, index


def _parse_simple_yaml_list(
    rows: list[_YamlLine],
    index: int,
    indent: int,
    path: Path,
) -> tuple[list[str], int]:
    values: list[str] = []
    while index < len(rows):
        row = rows[index]
        if row.indent < indent:
            break
        if row.indent > indent:
            raise ValueError(f"{path}: line {row.lineno}: unexpected indentation inside list")
        if not row.text.startswith("- "):
            break
        item = row.text[2:].lstrip()
        if not item:
            raise ValueError(f"{path}: line {row.lineno}: list items must be scalar values")
        values.append(_parse_simple_yaml_scalar(item))
        index += 1
    return values, index


def _parse_simple_yaml(text: str, path: Path) -> Any:
    rows = _tokenize_simple_yaml(text, path)
    if not rows:
        raise ValueError(f"{path}: file must not be empty")
    data, index = _parse_simple_yaml_block(rows, 0, rows[0].indent, path)
    if index != len(rows):
        row = rows[index]
        raise ValueError(f"{path}: line {row.lineno}: unexpected trailing content")
    return data


def _required_string(data: dict[str, Any], key: str, path: Path) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{path}: {key}: missing or invalid string")
    return value


def _required_string_list(data: dict[str, Any], key: str, path: Path) -> tuple[str, ...]:
    value = data.get(key)
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{path}: {key}: expected a non-empty list of strings")
    return tuple(value)


def _required_string_mapping(data: dict[str, Any], key: str, path: Path) -> dict[str, str]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: {key}: expected mapping")
    mapping: dict[str, str] = {}
    for item_key, item_value in value.items():
        if not isinstance(item_key, str) or not isinstance(item_value, str):
            raise ValueError(f"{path}: {key}: expected string keys and values")
        mapping[item_key] = item_value
    return mapping


def _required_present_string(data: dict[str, Any], key: str, context: str, path: Path) -> str:
    if key not in data:
        raise ValueError(f"{path}: {context}: missing required field {key}")
    value = data[key]
    if not isinstance(value, str):
        raise ValueError(f"{path}: {context}.{key}: expected string")
    return value


def parse_release_yaml(text: str, path: Path = Path("release.yaml")) -> ReleaseMetadata:
    """Parse the constrained release metadata shape."""

    data = _parse_simple_yaml(text, path)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected top-level mapping")

    smoke_data = data.get("smoke")
    if not isinstance(smoke_data, dict):
        raise ValueError(f"{path}: smoke: expected mapping")
    smoke: dict[str, SmokeRow] = {}
    for tool, row in smoke_data.items():
        if not isinstance(tool, str) or not isinstance(row, dict):
            raise ValueError(f"{path}: smoke.{tool}: expected mapping")
        context = f"smoke.{tool}"
        smoke[tool] = SmokeRow(
            result=_required_string(row, "result", path),
            tool_version=_required_string(row, "tool_version", path),
            evidence=_required_present_string(row, "evidence", context, path),
            reason=_required_present_string(row, "reason", context, path),
            owner=_required_present_string(row, "owner", context, path),
        )

    return ReleaseMetadata(
        version=_required_string(data, "version", path),
        release_type=_required_string(data, "release_type", path),
        manifest_version=_required_string(data, "manifest_version", path),
        supported_tools=_required_string_list(data, "supported_tools", path),
        adapter_paths=_required_string_mapping(data, "adapter_paths", path),
        instruction_entrypoints=_required_string_mapping(data, "instruction_entrypoints", path),
        smoke=smoke,
        validation=_required_string_mapping(data, "validation", path),
    )


def collect_skill_reports(skills_root: Path = CANONICAL_SKILLS_DIR) -> tuple[SkillPortabilityReport, ...]:
    """Evaluate canonical skills in deterministic order."""

    if not skills_root.exists():
        return ()
    reports = [evaluate_skill(directory) for directory in discover_source_skill_dirs(skills_root)]
    return tuple(sorted(reports, key=lambda report: (report.name, report.path.as_posix())))


def _canonical_skill_source_errors(
    skills_root: Path,
    reports: tuple[SkillPortabilityReport, ...] | None = None,
) -> list[str]:
    if not skills_root.exists():
        return [f"canonical skills root does not exist: {skills_root}"]
    if not skills_root.is_dir() and not (skills_root.is_file() and skills_root.name == "SKILL.md"):
        return [f"canonical skills root is not a skill directory or SKILL.md file: {skills_root}"]

    reports = collect_skill_reports(skills_root) if reports is None else reports
    if not reports:
        return [f"canonical skills root contains no skill files: {skills_root}"]

    errors: list[str] = []
    for report in reports:
        if report.included_adapters:
            continue
        reason = report.reason or "no adapter inclusion decision"
        errors.append(f"canonical skill validation failed: {report.path}: {reason}")
    return errors


def _validated_skill_reports(skills_root: Path) -> tuple[SkillPortabilityReport, ...]:
    reports = collect_skill_reports(skills_root)
    errors = _canonical_skill_source_errors(skills_root, reports)
    if errors:
        raise ValueError("\n".join(errors))
    return reports


def _path_from_posix(path: PurePosixPath) -> Path:
    return Path(*path.parts)


def _adapter_package_relative_root(config: AdapterConfig) -> Path:
    return _path_from_posix(config.package_root.relative_to(ADAPTER_OUTPUT_CONTRACT_ROOT))


def _adapter_contract_relative_path(relative_path: Path) -> str:
    return (ADAPTER_OUTPUT_CONTRACT_ROOT / PurePosixPath(relative_path.as_posix())).as_posix()


def _parse_adapter_version_core(version: str) -> tuple[int, int, int] | None:
    core = version.split("-", 1)[0]
    parts = core.split(".")
    if len(parts) != 3:
        return None
    try:
        return int(parts[0]), int(parts[1]), int(parts[2])
    except ValueError:
        return None


def _supports_opencode_command_aliases(version: str) -> bool:
    parsed = _parse_adapter_version_core(version)
    return parsed is not None and parsed >= (0, 1, 1)


def opencode_command_alias_relative_path(alias: str) -> Path:
    """Return the output-root-relative path for one OpenCode command alias."""

    return (
        _adapter_package_relative_root(ADAPTERS["opencode"])
        / _path_from_posix(OPENCODE_COMMAND_ROOT)
        / f"{alias}.md"
    )


def _opencode_command_alias_contract_path(alias: str) -> str:
    return _adapter_contract_relative_path(opencode_command_alias_relative_path(alias))


def _expected_opencode_command_alias_paths() -> dict[str, str]:
    return {
        alias: _opencode_command_alias_contract_path(alias)
        for alias in OPENCODE_COMMAND_ALIASES
    }


def _opencode_command_alias_missing_skill_errors(
    reports: Iterable[SkillPortabilityReport],
) -> list[str]:
    included = {
        report.name
        for report in reports
        if "opencode" in report.included_adapters
    }
    return [
        (
            f"opencode command alias {alias} maps to missing included skill: "
            f"{_opencode_command_alias_contract_path(alias)}"
        )
        for alias in OPENCODE_COMMAND_ALIASES
        if alias not in included
    ]


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


def render_opencode_command_alias(alias: str) -> str:
    """Render one deterministic thin OpenCode command alias wrapper."""

    return "\n".join(
        [
            "---",
            f"description: Use the RigorLoop {alias} skill.",
            "---",
            "",
            f"Load and follow the `{alias}` skill for this request:",
            "",
            "$ARGUMENTS",
            "",
        ]
    )


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

    reports = _validated_skill_reports(skills_root)
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

    if _supports_opencode_command_aliases(version):
        for alias in OPENCODE_COMMAND_ALIASES:
            expected[opencode_command_alias_relative_path(alias)] = render_opencode_command_alias(alias)

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

    canonical_errors = _canonical_skill_source_errors(skills_root)
    if canonical_errors:
        return canonical_errors

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


def _adapter_root(output_root: Path, config: AdapterConfig) -> Path:
    return output_root / _adapter_package_relative_root(config)


def _adapter_skill_root(output_root: Path, config: AdapterConfig) -> Path:
    return _adapter_root(output_root, config) / _path_from_posix(config.skill_root)


def _generated_skill_files(output_root: Path, config: AdapterConfig) -> tuple[Path, ...]:
    skill_root = _adapter_skill_root(output_root, config)
    if not skill_root.is_dir():
        return ()
    return tuple(sorted(skill_root.glob("*/SKILL.md")))


def _opencode_command_root(output_root: Path) -> Path:
    return _adapter_root(output_root, ADAPTERS["opencode"]) / _path_from_posix(OPENCODE_COMMAND_ROOT)


def _generated_opencode_command_alias_files(output_root: Path) -> tuple[Path, ...]:
    command_root = _opencode_command_root(output_root)
    if not command_root.is_dir():
        return ()
    return tuple(sorted(command_root.glob("*.md")))


def _command_alias_contract_path(output_root: Path, path: Path) -> str:
    return _adapter_contract_relative_path(path.relative_to(output_root))


def _command_alias_output_path(output_root: Path, contract_path: str) -> Path | None:
    candidate = PurePosixPath(contract_path)
    try:
        relative = candidate.relative_to(ADAPTER_OUTPUT_CONTRACT_ROOT)
    except ValueError:
        return None
    return output_root / _path_from_posix(relative)


def _validate_opencode_command_alias_body(alias: str, path: Path, text: str) -> list[str]:
    errors: list[str] = []
    if "@" in text:
        errors.append(f"opencode command alias file-reference interpolation: {alias}: {path}")
    if "!" in text:
        errors.append(f"opencode command alias shell-output interpolation: {alias}: {path}")
    if re.search(r"(?im)^\s*model\s*:", text):
        errors.append(f"opencode command alias model override: {alias}: {path}")
    if re.search(r"(?im)^\s*agent\s*:", text):
        errors.append(f"opencode command alias agent override: {alias}: {path}")
    if re.search(r"(?im)^\s*permissions?\s*:", text):
        errors.append(f"opencode command alias permission policy change: {alias}: {path}")
    if text != render_opencode_command_alias(alias):
        errors.append(f"opencode command alias body mismatch: {alias}: {path}")
    return errors


def _validate_opencode_command_aliases(
    version: str,
    manifest: AdapterManifest,
    output_root: Path,
    generated_by_adapter: dict[str, set[str]],
) -> list[str]:
    errors: list[str] = []
    command_root = _opencode_command_root(output_root)
    actual_files = _generated_opencode_command_alias_files(output_root)
    actual_aliases = {
        path.stem: _command_alias_contract_path(output_root, path)
        for path in actual_files
    }

    unsupported_tools = sorted(set(manifest.command_aliases) - {"opencode"})
    for tool in unsupported_tools:
        errors.append(f"unsupported command alias tool: {tool}")

    if not _supports_opencode_command_aliases(version):
        if manifest.command_aliases:
            errors.append(f"manifest command aliases are not supported for adapter version {version}")
        return errors

    section = manifest.command_aliases.get("opencode")
    if section is None:
        errors.append("manifest missing command_aliases.opencode")
        section_aliases: dict[str, str] = {}
    else:
        section_aliases = section.aliases
        if section.count != len(section.aliases):
            errors.append(
                f"command_aliases.opencode.count mismatch: expected {len(section.aliases)}, "
                f"found {section.count}"
            )

    expected_aliases = _expected_opencode_command_alias_paths()
    for alias, expected_path in expected_aliases.items():
        if alias not in section_aliases:
            errors.append(f"opencode command alias missing from manifest: {alias}: {expected_path}")

    for alias, alias_path in section_aliases.items():
        if alias not in OPENCODE_COMMAND_ALIASES:
            errors.append(f"unexpected opencode command alias in manifest: {alias}: {alias_path}")
        if not alias_path.startswith("dist/adapters/opencode/.opencode/commands/"):
            errors.append(
                f"opencode command alias path must be under "
                f"dist/adapters/opencode/.opencode/commands: {alias}: {alias_path}"
            )
            continue
        if PurePosixPath(alias_path).stem != alias:
            errors.append(f"opencode command alias filename stem mismatch: {alias}: {alias_path}")
        expected_path = expected_aliases.get(alias)
        if expected_path is not None and alias_path != expected_path:
            errors.append(
                f"opencode command alias path mismatch: {alias}: expected {expected_path}, "
                f"found {alias_path}"
            )
        output_path = _command_alias_output_path(output_root, alias_path)
        if output_path is None or not output_path.is_file():
            errors.append(f"opencode command alias missing: {alias}: {alias_path}")

    for alias, alias_path in actual_aliases.items():
        if alias not in OPENCODE_COMMAND_ALIASES:
            errors.append(f"unexpected opencode command alias: {alias}: {alias_path}")
        if alias not in section_aliases:
            errors.append(f"opencode command alias file is not listed in manifest: {alias}: {alias_path}")
        if alias not in generated_by_adapter.get("opencode", set()):
            errors.append(f"opencode command alias maps to missing skill: {alias}: {alias_path}")
        try:
            text = (command_root / f"{alias}.md").read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"opencode command alias must be UTF-8 text: {alias}: {alias_path}")
            continue
        errors.extend(_validate_opencode_command_alias_body(alias, command_root / f"{alias}.md", text))

    return errors


SECURITY_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "private key delimiter",
        re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
    ),
    (
        "secret assignment",
        re.compile(
            r"\b(?:AWS_SECRET_ACCESS_KEY|SECRET_KEY|API_KEY|ACCESS_TOKEN|AUTH_TOKEN|PRIVATE_TOKEN)"
            r"\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{8,}",
            re.IGNORECASE,
        ),
    ),
    (
        "machine-local absolute path",
        re.compile(
            r"(?<![A-Za-z0-9_./-])"
            r"(?:/home/[A-Za-z0-9._-]+/|/Users/[A-Za-z0-9._-]+/|[A-Za-z]:\\Users\\)"
        ),
    ),
    (
        "permission bypass",
        re.compile(
            r"--dangerously-skip-permissions|dangerously skip permissions|"
            r"bypass (?:all )?(?:tool )?permissions|permission-bypass",
            re.IGNORECASE,
        ),
    ),
)


def scan_security_paths(paths: Iterable[Path]) -> list[str]:
    """Scan generated adapter files and templates for high-signal unsafe markers."""

    errors: list[str] = []
    files: list[Path] = []
    for path in paths:
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(item for item in sorted(path.rglob("*")) if item.is_file())

    for path in sorted(files):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"{path}: file must be UTF-8 text")
            continue
        for label, pattern in SECURITY_PATTERNS:
            if pattern.search(text):
                errors.append(f"{path}: security violation: {label}")

    return errors


def _dedupe_errors(errors: Iterable[str]) -> list[str]:
    deduped: list[str] = []
    for error in errors:
        if error not in deduped:
            deduped.append(error)
    return deduped


def validate_adapter_output(
    version: str,
    *,
    skills_root: Path = CANONICAL_SKILLS_DIR,
    template_root: Path = ADAPTER_TEMPLATE_ROOT,
    output_root: Path = ADAPTER_OUTPUT_ROOT,
) -> list[str]:
    """Validate generated adapter packages, manifest consistency, and security markers."""

    errors: list[str] = []
    canonical_errors = _canonical_skill_source_errors(skills_root)
    errors.extend(canonical_errors)
    if not canonical_errors:
        errors.extend(
            collect_adapter_drift(
                version,
                skills_root=skills_root,
                template_root=template_root,
                output_root=output_root,
            )
        )

    manifest_path = output_root / "manifest.yaml"
    manifest: AdapterManifest | None = None
    if not manifest_path.is_file():
        errors.append(f"missing adapter manifest: {manifest_path}")
    else:
        try:
            manifest = parse_manifest_yaml(manifest_path.read_text(encoding="utf-8"), manifest_path)
        except ValueError as exc:
            errors.append(str(exc))

    if manifest is not None and manifest.version != version:
        errors.append(
            f"manifest version mismatch: expected {version}, found {manifest.version} at {manifest_path}"
        )

    reports = {
        report.name: report
        for report in (() if canonical_errors else collect_skill_reports(skills_root))
    }
    generated_by_adapter: dict[str, set[str]] = {adapter: set() for adapter in SUPPORTED_ADAPTERS}

    for adapter_name in SUPPORTED_ADAPTERS:
        config = ADAPTERS[adapter_name]
        package_root = _adapter_root(output_root, config)
        entrypoint = package_root / _path_from_posix(config.entrypoint)
        skill_root = _adapter_skill_root(output_root, config)

        if not package_root.is_dir():
            errors.append(f"missing adapter directory: {adapter_name}: {package_root}")
            continue
        if not entrypoint.is_file():
            errors.append(f"missing instruction entrypoint: {adapter_name}: {entrypoint}")
        if adapter_name == "claude":
            claude_commands = package_root / ".claude" / "commands"
            if claude_commands.exists():
                errors.append(f"unexpected claude command wrapper directory: claude: {claude_commands}")
        if not skill_root.is_dir():
            errors.append(f"missing adapter skill directory: {adapter_name}: {skill_root}")
            continue

        for skill_path in _generated_skill_files(output_root, config):
            skill_name = skill_path.parent.name
            generated_by_adapter[adapter_name].add(skill_name)
            try:
                metadata, _body = load_skill_file(skill_path)
            except (OSError, ValueError) as exc:
                errors.append(f"{skill_path}: {exc}")
                continue
            errors.extend(validate_skill_file(skill_path, load_skill_schema())[0])
            name = _normalize_description(metadata.get("name"))
            description = _normalize_description(metadata.get("description"))
            errors.extend(f"{skill_path}: {error}" for error in _portable_name_errors(name, skill_name))
            errors.extend(f"{skill_path}: {error}" for error in _description_errors(description))

            if adapter_name != "codex":
                unsupported = sorted(set(metadata) - COMMON_FRONTMATTER)
                if unsupported:
                    errors.append(
                        f"unsupported metadata in {adapter_name}/{skill_name}: {', '.join(unsupported)}"
                    )

    if manifest is not None:
        for skill_name, report in reports.items():
            entry = manifest.skills.get(skill_name)
            if entry is None:
                errors.append(f"manifest omits canonical skill: {skill_name}")
                continue
            invalid_adapters = sorted(set(entry.adapters) - set(SUPPORTED_ADAPTERS))
            if invalid_adapters:
                errors.append(
                    f"manifest lists unsupported adapter for {skill_name}: {', '.join(invalid_adapters)}"
                )
            if entry.adapters != report.included_adapters:
                errors.append(
                    f"adapter list mismatch: {skill_name}: expected {report.included_adapters}, "
                    f"found {entry.adapters}"
                )
            if entry.portable != report.portable:
                errors.append(
                    f"portable flag mismatch: {skill_name}: expected {report.portable}, "
                    f"found {entry.portable}"
                )
            if not entry.portable and not entry.reason:
                errors.append(f"non-portable manifest entry missing reason: {skill_name}")
            for adapter_name in entry.adapters:
                if (
                    adapter_name in SUPPORTED_ADAPTERS
                    and skill_name not in generated_by_adapter[adapter_name]
                ):
                    config = ADAPTERS[adapter_name]
                    expected_path = _adapter_skill_root(output_root, config) / skill_name / "SKILL.md"
                    errors.append(
                        f"manifest lists adapter without generated skill: {adapter_name}/{skill_name}: "
                        f"{expected_path}"
                    )

        for skill_name in sorted(set(manifest.skills) - set(reports)):
            errors.append(f"manifest lists unknown skill: {skill_name}")

        for adapter_name, generated_names in generated_by_adapter.items():
            listed_names = {
                skill_name
                for skill_name, entry in manifest.skills.items()
                if adapter_name in entry.adapters
            }
            if generated_names != listed_names:
                errors.append(
                    f"generated skill count mismatch for {adapter_name}: "
                    f"manifest lists {len(listed_names)}, files contain {len(generated_names)}"
                )
            for skill_name in sorted(generated_names - listed_names):
                errors.append(f"generated skill is not listed in manifest: {adapter_name}/{skill_name}")

        errors.extend(
            _validate_opencode_command_aliases(
                version,
                manifest,
                output_root,
                generated_by_adapter,
            )
        )

    errors.extend(scan_security_paths((output_root, template_root)))
    return _dedupe_errors(errors)


def _expected_adapter_paths() -> dict[str, str]:
    return {
        adapter: f"{config.package_root.as_posix()}/"
        for adapter, config in ADAPTERS.items()
    }


def _expected_instruction_entrypoints() -> dict[str, str]:
    return {
        adapter: f"{config.package_root.as_posix()}/{config.entrypoint.as_posix()}"
        for adapter, config in ADAPTERS.items()
    }


def _release_notes_tools(text: str) -> tuple[str, ...]:
    tools: list[str] = []
    for line in text.splitlines():
        match = re.fullmatch(r"- `([^`]+)`: `dist/adapters/[^`]+/`", line.strip())
        if match:
            tools.append(match.group(1))
    return tuple(tools)


def _release_notes_consistency_errors(
    version: str,
    metadata: ReleaseMetadata,
    manifest: AdapterManifest,
    notes_text: str,
) -> list[str]:
    errors: list[str] = []
    first_heading = next((line.strip() for line in notes_text.splitlines() if line.strip()), "")
    if first_heading != f"# RigorLoop {version}":
        errors.append(f"release notes version mismatch: expected '# RigorLoop {version}'")

    notes_tools = _release_notes_tools(notes_text)
    if notes_tools != metadata.supported_tools:
        errors.append(
            f"release notes supported tools mismatch: expected {metadata.supported_tools}, "
            f"found {notes_tools}"
        )
    if "dist/adapters/" not in notes_text:
        errors.append("release notes must describe generated adapter packages under dist/adapters/")

    non_portable = sorted(name for name, entry in manifest.skills.items() if not entry.portable)
    if non_portable:
        for skill_name in non_portable:
            if skill_name not in notes_text:
                errors.append(f"release notes omit non-portable skill exclusion: {skill_name}")
    elif "No current non-portable skill exclusions." not in notes_text:
        errors.append("release notes must state that there are no current non-portable skill exclusions")

    if _supports_opencode_command_aliases(metadata.manifest_version):
        opencode_aliases = manifest.command_aliases.get("opencode")
        if opencode_aliases is None:
            errors.append("release notes consistency could not check missing OpenCode command aliases")
        else:
            missing_aliases = [
                alias for alias in opencode_aliases.aliases
                if f"`{alias}`" not in notes_text
            ]
            if missing_aliases:
                errors.append(
                    "release notes omit OpenCode command aliases: "
                    + ", ".join(missing_aliases)
                )
        if "OpenCode command aliases" not in notes_text:
            errors.append("release notes must describe OpenCode command aliases")
        if "Claude Code" not in notes_text or "skill-native" not in notes_text:
            errors.append("release notes must describe Claude Code skill-native usage")
        if "opencode run --command proposal" not in notes_text:
            errors.append(
                "release notes must include the smoke-tested OpenCode one-shot command form"
            )

    return errors


def _placeholder_release_check_status() -> str:
    release_verify = ROOT / "scripts" / "release-verify.sh"
    if not release_verify.is_file():
        return "fail"
    text = release_verify.read_text(encoding="utf-8")
    return "fail" if any(marker in text for marker in PLACEHOLDER_RELEASE_PATTERNS) else "pass"


def _validate_smoke_row(
    version: str,
    release_type: str,
    tool: str,
    row: SmokeRow,
) -> list[str]:
    errors: list[str] = []
    valid_results = {"pass", "fail", "not-run", "blocked"}
    if row.result not in valid_results:
        return [f"smoke.{tool}.result: unsupported value: {row.result}"]

    if row.result == "pass":
        if not row.tool_version or row.tool_version == "unknown":
            errors.append(f"smoke.{tool}.tool_version: pass requires known tool version")
        if not row.evidence:
            errors.append(f"smoke.{tool}.evidence: pass requires evidence")

    if row.result == "fail":
        for field_name, value in (
            ("tool_version", row.tool_version),
            ("evidence", row.evidence),
            ("reason", row.reason),
            ("owner", row.owner),
        ):
            if not value:
                errors.append(f"smoke.{tool}.{field_name}: fail requires non-empty value")
        if release_type == "rc":
            errors.append(f"smoke.{tool}.result: known smoke failure blocks rc {version}")

    if row.result == "not-run":
        if row.tool_version != "unknown":
            errors.append(f"smoke.{tool}.tool_version: not-run requires unknown")
        if row.evidence:
            errors.append(f"smoke.{tool}.evidence: not-run requires empty evidence")
        if not row.reason:
            errors.append(f"smoke.{tool}.reason: not-run requires reason")
        if not row.owner:
            errors.append(f"smoke.{tool}.owner: not-run requires owner")

    if row.result == "blocked":
        if not row.reason:
            errors.append(f"smoke.{tool}.reason: blocked requires reason")
        if not row.owner:
            errors.append(f"smoke.{tool}.owner: blocked requires owner")
        reason = row.reason.lower()
        if (
            release_type == "rc"
            and "external" not in reason
            and "tool-access" not in reason
            and "tool access" not in reason
        ):
            errors.append(
                f"smoke.{tool}.reason: blocked rc smoke must identify an "
                "external or tool-access blocker"
            )

    if release_type == "final" and row.result != "pass":
        errors.append(f"smoke.{tool}.result: final release requires smoke pass")

    return errors


def _validate_opencode_command_alias_smoke(version: str, metadata: ReleaseMetadata) -> list[str]:
    if not _supports_opencode_command_aliases(metadata.manifest_version):
        return []

    row = metadata.smoke.get("opencode")
    if row is None or row.result != "pass":
        return []

    evidence = row.evidence.lower()
    has_one_shot_form = "opencode run --command proposal" in evidence
    has_behavior = (
        "loaded" in evidence
        or "followed" in evidence
        or "argument_marker_m3_smoke" in evidence
    )
    has_skill = "proposal skill" in evidence or "`proposal` skill" in evidence
    if has_one_shot_form and has_behavior and has_skill:
        return []
    return [f"smoke.opencode.evidence: {version} requires command alias behavior evidence"]


def validate_release_output(
    version: str,
    *,
    skills_root: Path = CANONICAL_SKILLS_DIR,
    template_root: Path = ADAPTER_TEMPLATE_ROOT,
    output_root: Path = ADAPTER_OUTPUT_ROOT,
    release_root: Path = RELEASE_ROOT,
) -> list[str]:
    """Validate one target-version release metadata and notes surface."""

    errors: list[str] = []
    target = RELEASE_TARGETS.get(version)
    if target is None:
        return [f"unsupported release target: {version}"]
    expected_release_type, expected_manifest_version = target

    release_dir = release_root / version
    release_path = release_dir / "release.yaml"
    notes_path = release_dir / "release-notes.md"
    if not release_path.is_file():
        return [f"missing release metadata: {release_path}"]
    if not notes_path.is_file():
        return [f"missing release notes: {notes_path}"]

    try:
        metadata = parse_release_yaml(release_path.read_text(encoding="utf-8"), release_path)
    except ValueError as exc:
        return [str(exc)]

    if metadata.version != version:
        errors.append(
            f"{release_path}: version mismatch: expected {version}, found {metadata.version}"
        )
    if metadata.release_type != expected_release_type:
        errors.append(
            f"{release_path}: release_type mismatch: expected {expected_release_type}, "
            f"found {metadata.release_type}"
        )
    if metadata.manifest_version != expected_manifest_version:
        errors.append(
            f"{release_path}: manifest_version mismatch: expected {expected_manifest_version}, "
            f"found {metadata.manifest_version}"
        )
    if metadata.supported_tools != SUPPORTED_ADAPTERS:
        errors.append(
            f"{release_path}: supported_tools must be exactly {SUPPORTED_ADAPTERS}, "
            f"found {metadata.supported_tools}"
        )
    if metadata.adapter_paths != _expected_adapter_paths():
        errors.append(f"{release_path}: adapter_paths mismatch")
    if metadata.instruction_entrypoints != _expected_instruction_entrypoints():
        errors.append(f"{release_path}: instruction_entrypoints mismatch")
    if set(metadata.smoke) != set(SUPPORTED_ADAPTERS):
        errors.append(f"{release_path}: smoke rows must be exactly {SUPPORTED_ADAPTERS}")
    for tool in SUPPORTED_ADAPTERS:
        row = metadata.smoke.get(tool)
        if row is not None:
            errors.extend(_validate_smoke_row(version, expected_release_type, tool, row))
    errors.extend(_validate_opencode_command_alias_smoke(version, metadata))

    for key in REQUIRED_RELEASE_VALIDATION_KEYS:
        if key not in metadata.validation:
            errors.append(f"{release_path}: validation.{key}: missing required field")
        elif metadata.validation[key] not in {"pass", "fail"}:
            errors.append(f"{release_path}: validation.{key}: expected pass or fail")

    manifest_path = output_root / "manifest.yaml"
    manifest: AdapterManifest | None = None
    if not manifest_path.is_file():
        errors.append(f"missing adapter manifest: {manifest_path}")
    else:
        try:
            manifest = parse_manifest_yaml(
                manifest_path.read_text(encoding="utf-8"),
                manifest_path,
            )
        except ValueError as exc:
            errors.append(str(exc))
    if manifest is not None and manifest.version != expected_manifest_version:
        errors.append(
            f"{manifest_path}: version mismatch: expected {expected_manifest_version}, "
            f"found {manifest.version}"
        )

    generated_sync_errors = collect_adapter_drift(
        expected_manifest_version,
        skills_root=skills_root,
        template_root=template_root,
        output_root=output_root,
    )
    errors.extend(generated_sync_errors)

    adapter_validation_errors = validate_adapter_output(
        expected_manifest_version,
        skills_root=skills_root,
        template_root=template_root,
        output_root=output_root,
    )
    errors.extend(adapter_validation_errors)

    notes_text = notes_path.read_text(encoding="utf-8")
    release_notes_errors = (
        _release_notes_consistency_errors(version, metadata, manifest, notes_text)
        if manifest is not None
        else ["release notes consistency could not be checked without manifest"]
    )
    errors.extend(release_notes_errors)

    security_errors = scan_security_paths((release_path, notes_path))
    errors.extend(security_errors)

    actual_validation = {
        "generated_sync": "fail" if generated_sync_errors or adapter_validation_errors else "pass",
        "release_notes_consistency": "fail" if release_notes_errors else "pass",
        "placeholder_release_check": _placeholder_release_check_status(),
        "security": "fail" if security_errors else "pass",
    }
    for key, actual in actual_validation.items():
        recorded = metadata.validation.get(key)
        if recorded in {"pass", "fail"} and recorded != actual:
            errors.append(f"{release_path}: validation.{key}: expected {actual}, found {recorded}")

    return _dedupe_errors(errors)
