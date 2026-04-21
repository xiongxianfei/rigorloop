#!/usr/bin/env python3
"""Validate first-release RigorLoop change metadata without third-party deps."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "change.schema.json"
CANONICAL_ARTIFACT_KEYS = {
    "adr",
    "architecture",
    "change_summary",
    "explain_change",
    "plan",
    "pr_body",
    "proposal",
    "retrospective",
    "review_resolution",
    "spec",
    "test_spec",
    "verify_report",
}


class MetadataValidationError(Exception):
    """Raised when change metadata cannot be parsed or validated."""


@dataclass(frozen=True)
class Line:
    indent: int
    text: str
    lineno: int


def parse_scalar(text: str) -> Any:
    value = text.strip()
    if not value:
        return ""
    if value[0] == value[-1] and value[0] in {"'", '"'} and len(value) >= 2:
        return value[1:-1]
    if value in {"true", "false"}:
        return value == "true"
    if value == "null":
        return None
    if re.fullmatch(r"-?[0-9]+", value):
        return int(value)
    return value


def tokenize_yaml(text: str) -> list[Line]:
    lines: list[Line] = []
    for lineno, raw_line in enumerate(text.splitlines(), start=1):
        if not raw_line.strip():
            continue
        if raw_line.lstrip().startswith("#"):
            continue
        if "\t" in raw_line:
            raise MetadataValidationError(f"line {lineno}: tabs are not supported")
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        if indent % 2:
            raise MetadataValidationError(
                f"line {lineno}: indentation must use multiples of two spaces"
            )
        lines.append(Line(indent=indent, text=raw_line[indent:], lineno=lineno))
    return lines


def split_mapping_entry(text: str, lineno: int) -> tuple[str, str]:
    if ":" not in text:
        raise MetadataValidationError(f"line {lineno}: expected 'key: value'")
    key, value = text.split(":", 1)
    key = key.strip()
    if not key:
        raise MetadataValidationError(f"line {lineno}: mapping key must not be empty")
    return key, value.lstrip()


def parse_yaml_block(lines: list[Line], index: int, indent: int) -> tuple[Any, int]:
    if index >= len(lines):
        raise MetadataValidationError("unexpected end of file")
    line = lines[index]
    if line.indent != indent:
        raise MetadataValidationError(
            f"line {line.lineno}: expected indentation {indent}, found {line.indent}"
        )
    if line.text.startswith("- "):
        return parse_yaml_list(lines, index, indent)
    return parse_yaml_mapping(lines, index, indent)


def parse_yaml_mapping(lines: list[Line], index: int, indent: int) -> tuple[dict[str, Any], int]:
    data: dict[str, Any] = {}
    while index < len(lines):
        line = lines[index]
        if line.indent < indent:
            break
        if line.indent > indent:
            raise MetadataValidationError(
                f"line {line.lineno}: unexpected indentation inside mapping"
            )
        if line.text.startswith("- "):
            raise MetadataValidationError(
                f"line {line.lineno}: unexpected list item where mapping entry was expected"
            )
        key, remainder = split_mapping_entry(line.text, line.lineno)
        index += 1
        if remainder:
            data[key] = parse_scalar(remainder)
            continue
        if index >= len(lines) or lines[index].indent <= indent:
            data[key] = None
            continue
        child_indent = lines[index].indent
        if child_indent != indent + 2:
            raise MetadataValidationError(
                f"line {lines[index].lineno}: nested block for '{key}' must be indented by two spaces"
            )
        data[key], index = parse_yaml_block(lines, index, child_indent)
    return data, index


def parse_yaml_list(lines: list[Line], index: int, indent: int) -> tuple[list[Any], int]:
    items: list[Any] = []
    while index < len(lines):
        line = lines[index]
        if line.indent < indent:
            break
        if line.indent > indent:
            raise MetadataValidationError(
                f"line {line.lineno}: unexpected indentation inside list"
            )
        if not line.text.startswith("- "):
            raise MetadataValidationError(
                f"line {line.lineno}: expected list item starting with '- '"
            )
        remainder = line.text[2:].lstrip()
        index += 1
        if not remainder:
            if index >= len(lines) or lines[index].indent <= indent:
                items.append(None)
                continue
            child_indent = lines[index].indent
            if child_indent != indent + 2:
                raise MetadataValidationError(
                    f"line {lines[index].lineno}: nested list item blocks must be indented by two spaces"
                )
            item, index = parse_yaml_block(lines, index, child_indent)
            items.append(item)
            continue
        if ":" in remainder:
            item, index = parse_inline_mapping_item(
                lines, index, indent, remainder, line.lineno
            )
            items.append(item)
            continue
        items.append(parse_scalar(remainder))
    return items, index


def parse_inline_mapping_item(
    lines: list[Line], index: int, indent: int, remainder: str, lineno: int
) -> tuple[dict[str, Any], int]:
    item: dict[str, Any] = {}
    key, value = split_mapping_entry(remainder, lineno)
    if value:
        item[key] = parse_scalar(value)
    elif index < len(lines) and lines[index].indent > indent:
        if lines[index].indent != indent + 2:
            raise MetadataValidationError(
                f"line {lines[index].lineno}: nested mapping blocks must be indented by two spaces"
            )
        item[key], index = parse_yaml_block(lines, index, indent + 2)
    else:
        item[key] = None

    while index < len(lines):
        line = lines[index]
        if line.indent < indent + 2:
            break
        if line.indent > indent + 2:
            raise MetadataValidationError(
                f"line {line.lineno}: unexpected indentation inside inline mapping item"
            )
        if line.text.startswith("- "):
            break
        key, value = split_mapping_entry(line.text, line.lineno)
        index += 1
        if value:
            item[key] = parse_scalar(value)
            continue
        if index >= len(lines) or lines[index].indent <= indent + 2:
            item[key] = None
            continue
        if lines[index].indent != indent + 4:
            raise MetadataValidationError(
                f"line {lines[index].lineno}: nested mapping blocks must be indented by two spaces"
            )
        item[key], index = parse_yaml_block(lines, index, indent + 4)
    return item, index


def load_yaml(path: Path) -> Any:
    lines = tokenize_yaml(path.read_text(encoding="utf-8"))
    if not lines:
        raise MetadataValidationError("metadata file is empty")
    data, index = parse_yaml_block(lines, 0, lines[0].indent)
    if index != len(lines):
        line = lines[index]
        raise MetadataValidationError(
            f"line {line.lineno}: unexpected trailing content at indentation {line.indent}"
        )
    return data


def load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def path_label(path: str, key: str | int | None = None) -> str:
    if key is None:
        return path
    if isinstance(key, int):
        return f"{path}[{key}]"
    if path == "$":
        return key
    return f"{path}.{key}"


def validate_property_name(schema: dict[str, Any], name: str, path: str) -> list[str]:
    errors: list[str] = []
    if schema.get("type") == "string" and not isinstance(name, str):
        errors.append(f"{path}: expected property name to be a string")
        return errors
    min_length = schema.get("minLength")
    if isinstance(min_length, int) and len(name) < min_length:
        errors.append(f"{path}: property name must be at least {min_length} characters")
    return errors


def validate_against_schema(schema: dict[str, Any], value: Any, path: str = "$") -> list[str]:
    errors: list[str] = []
    expected_type = schema.get("type")

    if expected_type == "object":
        if not isinstance(value, dict):
            return [f"{path}: expected object"]
        for required_key in schema.get("required", []):
            if required_key not in value:
                errors.append(f"{path_label(path, required_key)}: missing required field")
        property_name_schema = schema.get("propertyNames")
        if isinstance(property_name_schema, dict):
            for key in value:
                errors.extend(
                    validate_property_name(property_name_schema, key, path_label(path, key))
                )
        properties = schema.get("properties", {})
        additional_properties = schema.get("additionalProperties", True)
        for key, child in value.items():
            if key in properties:
                errors.extend(
                    validate_against_schema(properties[key], child, path_label(path, key))
                )
                continue
            if additional_properties is False:
                errors.append(f"{path_label(path, key)}: unexpected property")
            elif isinstance(additional_properties, dict):
                errors.extend(
                    validate_against_schema(additional_properties, child, path_label(path, key))
                )
        return errors

    if expected_type == "array":
        if not isinstance(value, list):
            return [f"{path}: expected array"]
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, child in enumerate(value):
                errors.extend(
                    validate_against_schema(item_schema, child, path_label(path, index))
                )
        return errors

    if expected_type == "string":
        if not isinstance(value, str):
            return [f"{path}: expected string"]
        min_length = schema.get("minLength")
        if isinstance(min_length, int) and len(value) < min_length:
            errors.append(f"{path}: expected at least {min_length} characters")
        return errors

    if expected_type == "integer":
        if not isinstance(value, int) or isinstance(value, bool):
            return [f"{path}: expected integer"]
        minimum = schema.get("minimum")
        if isinstance(minimum, int) and value < minimum:
            errors.append(f"{path}: expected value >= {minimum}")
        return errors

    return errors


def validate_metadata_semantics(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return []

    artifacts = data.get("artifacts")
    if not isinstance(artifacts, dict):
        return []

    allowed_keys = ", ".join(sorted(CANONICAL_ARTIFACT_KEYS))
    errors: list[str] = []
    for key in artifacts:
        if key not in CANONICAL_ARTIFACT_KEYS:
            errors.append(
                f"{path_label('$', 'artifacts')}.{key}: invalid artifact key; "
                f"use one of: {allowed_keys}"
            )
    return errors


def validate_file(path: Path) -> list[str]:
    data = load_yaml(path)
    schema = load_schema()
    schema_errors = validate_against_schema(schema, data)
    if schema_errors:
        return schema_errors
    return validate_metadata_semantics(data)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(
            "usage: validate-change-metadata.py <change.yaml> [<change.yaml> ...]",
            file=sys.stderr,
        )
        return 2

    exit_code = 0
    for raw_path in argv[1:]:
        path = Path(raw_path)
        try:
            errors = validate_file(path)
        except FileNotFoundError:
            print(f"{path}: file not found", file=sys.stderr)
            exit_code = 1
            continue
        except MetadataValidationError as exc:
            print(f"{path}: invalid change metadata", file=sys.stderr)
            print(f"  - {exc}", file=sys.stderr)
            exit_code = 1
            continue

        if errors:
            print(f"{path}: invalid change metadata", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
            exit_code = 1
            continue

        print(f"{path}: valid change metadata")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
