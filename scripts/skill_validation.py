#!/usr/bin/env python3
"""Shared validation helpers for first-release RigorLoop skill checks."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_SKILLS_DIR = ROOT / "skills"
GENERATED_SKILLS_DIR = ROOT / ".codex" / "skills"
SKILL_SCHEMA_PATH = ROOT / "schemas" / "skill.schema.json"
PLACEHOLDER_PATTERN = re.compile(r"\b(TODO|TBD)\b")


@dataclass(frozen=True)
class ValidationResult:
    checked_files: list[Path]
    errors: list[str]


def _is_relative_to(path: Path, other: Path) -> bool:
    try:
        path.relative_to(other)
        return True
    except ValueError:
        return False


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _consume_block(lines: list[str], index: int) -> tuple[list[str], int]:
    block: list[str] = []
    while index < len(lines):
        raw_line = lines[index]
        if raw_line.startswith("  "):
            block.append(raw_line[2:])
            index += 1
            continue
        if raw_line.strip():
            break
        block.append("")
        index += 1
    return block, index


def _parse_frontmatter(frontmatter_lines: list[str], path: Path) -> dict[str, str]:
    metadata: dict[str, str] = {}
    index = 0
    while index < len(frontmatter_lines):
        raw_line = frontmatter_lines[index]
        index += 1

        if not raw_line.strip():
            continue
        if raw_line.startswith(" ") or raw_line.startswith("\t"):
            raise ValueError(f"{path}: frontmatter keys must be top-level mappings")
        if ":" not in raw_line:
            raise ValueError(f"{path}: invalid frontmatter line: {raw_line}")

        key, remainder = raw_line.split(":", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"{path}: frontmatter key must not be empty")
        remainder = remainder.lstrip()

        if remainder in {">", "|"}:
            block, index = _consume_block(frontmatter_lines, index)
            value = "\n".join(block).strip()
        elif remainder:
            value = _strip_quotes(remainder)
        else:
            block, index = _consume_block(frontmatter_lines, index)
            value = "\n".join(block).strip()

        metadata[key] = value

    return metadata


def load_skill_file(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path}: file must begin with YAML frontmatter")

    closing_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            closing_index = index
            break
    if closing_index is None:
        raise ValueError(f"{path}: YAML frontmatter must end with '---'")

    metadata = _parse_frontmatter(lines[1:closing_index], path)
    body = "\n".join(lines[closing_index + 1 :])
    return metadata, body


def load_skill_schema() -> dict:
    return json.loads(SKILL_SCHEMA_PATH.read_text(encoding="utf-8"))


def discover_skill_files(target: Path) -> list[Path]:
    if target.is_file():
        if target.name != "SKILL.md":
            return []
        return [target]
    return sorted(path for path in target.rglob("SKILL.md") if path.is_file())


def validate_metadata_against_schema(metadata: dict[str, str], schema: dict, path: Path) -> list[str]:
    errors: list[str] = []

    if schema.get("type") != "object":
        return [f"{path}: skill schema must define an object root"]

    for key in schema.get("required", []):
        if key not in metadata:
            errors.append(f"{path}: {key}: missing required field")

    properties = schema.get("properties", {})
    for key, property_schema in properties.items():
        if key not in metadata:
            continue
        value = metadata[key]
        if property_schema.get("type") == "string" and not isinstance(value, str):
            errors.append(f"{path}: {key}: expected string")
            continue
        min_length = property_schema.get("minLength")
        if isinstance(min_length, int) and len(value.strip()) < min_length:
            errors.append(f"{path}: {key}: must be at least {min_length} characters")

    return errors


def validate_skill_file(path: Path, schema: dict) -> tuple[list[str], str | None]:
    errors: list[str] = []
    full_text = path.read_text(encoding="utf-8")

    try:
        metadata, body = load_skill_file(path)
    except ValueError as exc:
        return [str(exc)], None

    errors.extend(validate_metadata_against_schema(metadata, schema, path))

    title_count = sum(1 for line in body.splitlines() if line.startswith("# "))
    if title_count != 1:
        errors.append(f"{path}: expected exactly one top-level # title, found {title_count}")

    if "## Expected output" not in body.splitlines():
        errors.append(f"{path}: missing required '## Expected output' section")

    if PLACEHOLDER_PATTERN.search(full_text):
        errors.append(f"{path}: placeholder text is not allowed")

    name = metadata.get("name")
    if isinstance(name, str) and not name.strip():
        errors.append(f"{path}: name: must be at least 1 characters")

    description = metadata.get("description")
    if isinstance(description, str) and not description.strip():
        errors.append(f"{path}: description: must be at least 1 characters")

    return errors, name.strip() if isinstance(name, str) and name.strip() else None


def validate_skill_tree(target: Path) -> ValidationResult:
    resolved_target = target.resolve()
    resolved_generated = GENERATED_SKILLS_DIR.resolve()
    if _is_relative_to(resolved_target, resolved_generated):
        return ValidationResult(
            checked_files=[],
            errors=[
                f"{target}: generated output path must not be used as authored source of truth"
            ],
        )

    checked_files = discover_skill_files(target)
    if not checked_files:
        return ValidationResult(checked_files=[], errors=[f"{target}: no SKILL.md files found"])

    schema = load_skill_schema()
    errors: list[str] = []
    owners: dict[str, Path] = {}

    for path in checked_files:
        file_errors, name = validate_skill_file(path, schema)
        errors.extend(file_errors)
        if not name:
            continue
        if name in owners:
            errors.append(f"duplicate skill name: {name} in {owners[name]} and {path}")
            continue
        owners[name] = path

    return ValidationResult(checked_files=checked_files, errors=errors)
