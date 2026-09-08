"""Restricted YAML grammar for project configuration and measurement artifacts.

This parser does not select or validate a stored-record contract.
"""
from __future__ import annotations
import json
import re
import shlex
from dataclasses import dataclass
from pathlib import Path
from typing import Any

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
        if value[0] == '"':
            try:
                return json.loads(value)
            except json.JSONDecodeError as exc:
                raise MetadataValidationError(f"invalid quoted scalar: {exc.msg}") from exc
        return value[1:-1]
    if value in {"true", "false"}:
        return value == "true"
    if value == "null":
        return None
    if value == "{}":
        return {}
    if value == "[]":
        return []
    if re.fullmatch(r"-?[0-9]+", value):
        return int(value)
    if re.fullmatch(r"-?(?:[0-9]+\.[0-9]+|[0-9]+[eE][+-]?[0-9]+|[0-9]+\.[0-9]+[eE][+-]?[0-9]+)", value):
        return float(value)
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
    if line.text == "-" or line.text.startswith("- "):
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
        if line.text == "-" or line.text.startswith("- "):
            raise MetadataValidationError(
                f"line {line.lineno}: unexpected list item where mapping entry was expected"
            )
        key, remainder = split_mapping_entry(line.text, line.lineno)
        if key in data:
            raise MetadataValidationError(
                f"line {line.lineno}: duplicate mapping key '{key}'"
            )
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
        if line.text != "-" and not line.text.startswith("- "):
            raise MetadataValidationError(
                f"line {line.lineno}: expected list item starting with '- '"
            )
        remainder = line.text[1:].lstrip()
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
    elif index < len(lines) and lines[index].indent > indent + 2:
        if lines[index].indent != indent + 4:
            raise MetadataValidationError(
                f"line {lines[index].lineno}: nested mapping blocks must be indented by two spaces"
            )
        item[key], index = parse_yaml_block(lines, index, indent + 4)
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
        if line.text == "-" or line.text.startswith("- "):
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
