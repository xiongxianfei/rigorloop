#!/usr/bin/env python3
"""Validate first-release RigorLoop change metadata without third-party deps."""

from __future__ import annotations

import json
import re
import shlex
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from change_metadata_semantics import validate_clean_receipt_root_review_metadata


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
COMPACT_REQUIRED_FIELDS = {
    "path_vars",
    "validation_bundles",
    "validation_events",
    "validation_summary",
}
LEGACY_VALIDATION_FIELDS = {"validation"}
VALIDATION_EVENT_RESULTS = {"pass", "fail", "blocked", "skipped", "not-run"}
COMPACT_CHANGE_ID_RE = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}-(?P<slug>[a-z0-9][a-z0-9-]*[a-z0-9])$"
)
COMPACT_LIFECYCLE_STAGES = [
    "change-created",
    "proposal",
    "proposal-review",
    "spec",
    "spec-review",
    "architecture",
    "architecture-review",
    "plan",
    "plan-review",
    "test-spec",
    "implement",
    "code-review",
    "review-resolution",
    "ci-maintenance",
    "explain-change",
    "verify",
    "pr",
]
COMPACT_LIFECYCLE_INDEX = {
    stage: index for index, stage in enumerate(COMPACT_LIFECYCLE_STAGES)
}
COMPACT_ARTIFACT_FIRST_EXISTS = {
    "change_root": "change-created",
    "change_metadata": "change-created",
    "proposal": "proposal",
    "proposal_review": "proposal-review",
    "review_log": "proposal-review",
    "review_resolution": "review-resolution",
    "spec": "spec",
    "spec_review": "spec-review",
    "architecture": "architecture",
    "adr": "architecture",
    "plan": "plan",
    "plan_review": "plan-review",
    "test_spec": "test-spec",
    "code_review": "code-review",
    "explain_change": "explain-change",
    "verify": "verify",
    "pr": "pr",
}
COMPACT_NON_ARTIFACT_PATH_VARS = {"change_id", "slug", "reviews_root"}
COMPACT_FORBIDDEN_OPT_OUT_KEYS = {"optional", "not_yet_created"}
COMPACT_CREDENTIAL_URL_RE = re.compile(r"[A-Za-z][A-Za-z0-9+.-]*://[^/\s]+@")
COMPACT_SECRET_VALUE_RE = re.compile(
    r"(?i)(?:^|[=&\s])(?:password|passwd|token|secret|private[_-]?key)[=:][^\s]+|gh[pousr]_[A-Za-z0-9_]+"
)
COMPACT_HOME_PATH_TOKEN_RE = re.compile(r"(?:^|\s)(?:~|\$HOME|\$\{HOME\})(?:[/\\]|$)")
COMPACT_WINDOWS_ABSOLUTE_PATH_RE = re.compile(r"(?:^|\s)[A-Za-z]:[\\/]")


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
    if value == "{}":
        return {}
    if value == "[]":
        return []
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

    errors: list[str] = []
    review = data.get("review")
    if isinstance(review, dict):
        reviewed_artifact = review.get("reviewed_artifact")
        if reviewed_artifact is not None and not isinstance(reviewed_artifact, str):
            errors.append("review.reviewed_artifact: expected string")
        review_log = review.get("review_log")
        if review_log is not None and not isinstance(review_log, str):
            errors.append("review.review_log: expected string")
    errors.extend(validate_clean_receipt_root_review_metadata(data))

    artifacts = data.get("artifacts")
    if not isinstance(artifacts, dict):
        return errors

    allowed_keys = ", ".join(sorted(CANONICAL_ARTIFACT_KEYS))
    for key in artifacts:
        if key not in CANONICAL_ARTIFACT_KEYS:
            errors.append(
                f"{path_label('$', 'artifacts')}.{key}: invalid artifact key; "
                f"use one of: {allowed_keys}"
            )
    return errors


def is_compact_metadata(data: Any) -> bool:
    return isinstance(data, dict) and data.get("schema_version") == 2


def is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def derive_compact_slug(change_id: str) -> str:
    match = COMPACT_CHANGE_ID_RE.fullmatch(change_id)
    if match is None:
        raise MetadataValidationError(
            "path_vars.change_id: expected dated identifier '<YYYY-MM-DD>-<slug>'"
        )
    return match.group("slug")


def resolve_compact_path_template(template: str, variables: dict[str, str]) -> str:
    for unsupported in ("${", "$(", "%"):
        if unsupported in template:
            raise MetadataValidationError(
                f"unsupported interpolation syntax '{unsupported}'"
            )

    output: list[str] = []
    index = 0
    while index < len(template):
        char = template[index]
        if char == "{":
            if template.startswith("{{", index):
                output.append("{")
                index += 2
                continue
            end = template.find("}", index + 1)
            if end == -1:
                raise MetadataValidationError("unmatched '{'")
            name = template[index + 1 : end]
            if not name or "{" in name or "}" in name:
                raise MetadataValidationError("nested or malformed interpolation")
            if name not in variables:
                raise MetadataValidationError(f"unknown variable '{name}'")
            output.append(variables[name])
            index = end + 1
            continue
        if char == "}":
            if template.startswith("}}", index):
                output.append("}")
                index += 2
                continue
            raise MetadataValidationError("unmatched '}'")
        output.append(char)
        index += 1
    return "".join(output)


def validate_repo_relative_path(value: str, path: str) -> list[str]:
    errors: list[str] = []
    lower_value = value.lower()
    if value.startswith("/"):
        errors.append(f"{path}: unsafe absolute path")
    if value.startswith("~"):
        errors.append(f"{path}: unsafe home-directory path")
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*://", value):
        errors.append(f"{path}: unsafe URL or hostname path")
    if re.match(r"^[A-Za-z0-9.-]+\.[A-Za-z]{2,}(/|$)", value):
        errors.append(f"{path}: unsafe hostname path")
    if "@" in value.split("/", 1)[0] or re.search(r"://[^/\s]+@", value):
        errors.append(f"{path}: unsafe credential-bearing path")
    if any(part == ".." for part in value.split("/")):
        errors.append(f"{path}: unsafe parent-directory path")
    if (
        lower_value.startswith(("home/", "users/"))
        or "/home/" in lower_value
        or "/users/" in lower_value
    ):
        errors.append(f"{path}: unsafe machine-local path")
    secret_markers = (
        "password=",
        "passwd=",
        "token=",
        "secret=",
        "private_key",
        "private-key",
        "http_proxy=",
        "https_proxy=",
    )
    if any(marker in lower_value for marker in secret_markers):
        errors.append(f"{path}: unsafe secret-like value")
    return errors


def command_token_is_path_like(token: str) -> bool:
    return (
        "/" in token
        or "\\" in token
        or token.startswith(("~", "$HOME", "${HOME}"))
        or re.match(r"^[A-Za-z]:[\\/]", token) is not None
    )


def validate_compact_bundle_command_safety(
    bundle_path: str,
    command: str,
    variables: dict[str, str],
) -> list[str]:
    command_path = f"{bundle_path}.command"
    errors: list[str] = []

    if COMPACT_CREDENTIAL_URL_RE.search(command):
        errors.append(f"{command_path} contains credential-bearing URL")
    if COMPACT_SECRET_VALUE_RE.search(command):
        errors.append(f"{command_path} contains secret-like value")
    if COMPACT_HOME_PATH_TOKEN_RE.search(command):
        errors.append(f"{command_path} contains unsafe machine-local path")
    if COMPACT_WINDOWS_ABSOLUTE_PATH_RE.search(command):
        errors.append(f"{command_path} contains unsafe machine-local path")

    try:
        tokens = shlex.split(command)
    except ValueError as exc:
        errors.append(f"{command_path}: malformed command string: {exc}")
        return errors

    for token in tokens:
        try:
            resolved_token = resolve_compact_path_template(token, variables)
        except MetadataValidationError as exc:
            errors.append(f"{command_path}: {exc}")
            continue

        token_path_errors = validate_repo_relative_path(resolved_token, command_path)
        if resolved_token.startswith(("$HOME", "${HOME}")):
            errors.append(f"{command_path} contains unsafe machine-local path")
            continue
        if any(
            category in error
            for error in token_path_errors
            for category in (
                "absolute path",
                "home-directory path",
                "parent-directory path",
                "machine-local path",
            )
        ):
            errors.append(f"{command_path} contains unsafe machine-local path")
            continue
        if any("credential-bearing" in error for error in token_path_errors):
            errors.append(f"{command_path} contains credential-bearing URL")
            continue
        if any("URL or hostname" in error or "hostname path" in error for error in token_path_errors):
            errors.append(f"{command_path} contains unsafe hostname or URL")
            continue
        if any("secret-like" in error for error in token_path_errors):
            errors.append(f"{command_path} contains secret-like value")
            continue
        if command_token_is_path_like(resolved_token) and token_path_errors:
            errors.extend(token_path_errors)

    return list(dict.fromkeys(errors))


def resolve_compact_path_vars(path_vars: dict[str, Any]) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    raw_change_id = path_vars.get("change_id")
    if not is_nonempty_string(raw_change_id):
        return {}, ["path_vars.change_id: missing required field"]

    try:
        derived_slug = derive_compact_slug(raw_change_id)
    except MetadataValidationError as exc:
        errors.append(str(exc))
        derived_slug = ""

    explicit_slug = path_vars.get("slug")
    if explicit_slug is not None:
        if not is_nonempty_string(explicit_slug):
            errors.append("path_vars.slug: expected string")
        elif derived_slug and explicit_slug != derived_slug:
            errors.append(
                f"path_vars.slug: must match derived slug '{derived_slug}'"
            )

    for key, value in path_vars.items():
        variable_path = path_label("path_vars", key)
        if (
            key not in COMPACT_ARTIFACT_FIRST_EXISTS
            and key not in COMPACT_NON_ARTIFACT_PATH_VARS
        ):
            errors.append(f"{variable_path}: unknown compact path variable")
        if not isinstance(value, str):
            errors.append(f"{variable_path}: expected string")

    resolved: dict[str, str] = {
        "change_id": raw_change_id if isinstance(raw_change_id, str) else "",
        "slug": derived_slug,
    }
    resolving: set[str] = set()

    def resolve_key(key: str) -> str:
        if key in resolved:
            return resolved[key]
        if key not in path_vars:
            raise MetadataValidationError(f"unknown variable '{key}'")
        if key in resolving:
            raise MetadataValidationError(f"recursive variable reference '{key}'")
        value = path_vars[key]
        if not isinstance(value, str):
            raise MetadataValidationError("expected string")
        if re.search(r"(?<!{){" + re.escape(key) + r"}(?!})", value):
            raise MetadataValidationError(f"recursive variable reference '{key}'")
        resolving.add(key)

        def resolve_template_reference(template: str) -> str:
            referenced_variables = dict(resolved)
            for referenced_key in path_vars:
                if referenced_key not in referenced_variables and referenced_key != key:
                    try:
                        referenced_variables[referenced_key] = resolve_key(referenced_key)
                    except MetadataValidationError:
                        pass
            return resolve_compact_path_template(template, referenced_variables)

        try:
            value = resolve_template_reference(value)
        finally:
            resolving.remove(key)
        resolved[key] = value
        return value

    for key in path_vars:
        if key in {"change_id", "slug"}:
            continue
        try:
            resolve_key(key)
        except MetadataValidationError as exc:
            errors.append(f"{path_label('path_vars', key)}: {exc}")

    for key, value in resolved.items():
        if key in {"change_id", "slug"}:
            continue
        errors.extend(validate_repo_relative_path(value, path_label("path_vars", key)))

    slug = resolved.get("slug", "")
    if "spec" in resolved and slug and resolved["spec"] != f"specs/{slug}.md":
        errors.append(
            f"path_vars.spec: expected canonical spec path 'specs/{slug}.md'"
        )
    if (
        "test_spec" in resolved
        and slug
        and resolved["test_spec"] != f"specs/{slug}.test.md"
    ):
        errors.append(
            f"path_vars.test_spec: expected canonical test spec path 'specs/{slug}.test.md'"
        )

    return resolved, errors


def compact_stage_reaches(current: str, required: str) -> bool:
    return COMPACT_LIFECYCLE_INDEX[current] >= COMPACT_LIFECYCLE_INDEX[required]


def validate_no_compact_path_opt_outs(value: Any, path: str = "$") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = path_label(path, key)
            if key in COMPACT_FORBIDDEN_OPT_OUT_KEYS:
                errors.append(
                    f"{child_path}: per-path existence opt-out flags are not allowed"
                )
            errors.extend(validate_no_compact_path_opt_outs(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(validate_no_compact_path_opt_outs(child, path_label(path, index)))
    return errors


def validate_compact_required_fields(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in sorted(COMPACT_REQUIRED_FIELDS):
        if field not in data:
            errors.append(f"{field}: missing required compact field")
    return errors


def validate_compact_top_level_shape(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if any(field in data for field in LEGACY_VALIDATION_FIELDS):
        errors.append("validation: mixed legacy and compact validation metadata")

    path_vars = data.get("path_vars")
    if path_vars is not None and not isinstance(path_vars, dict):
        errors.append("path_vars: expected object")

    validation_bundles = data.get("validation_bundles")
    if validation_bundles is not None and not isinstance(validation_bundles, dict):
        errors.append("validation_bundles: expected object")

    validation_events = data.get("validation_events")
    if validation_events is not None and not isinstance(validation_events, list):
        errors.append("validation_events: expected array")

    validation_summary = data.get("validation_summary")
    if validation_summary is not None and not isinstance(validation_summary, dict):
        errors.append("validation_summary: expected object")

    return errors


def validate_compact_bundle_definitions(
    validation_bundles: dict[str, Any],
    variables: dict[str, str],
) -> list[str]:
    errors: list[str] = []
    for bundle_id, definition in validation_bundles.items():
        bundle_path = path_label("validation_bundles", bundle_id)
        if not isinstance(definition, dict):
            errors.append(f"{bundle_path}: expected object")
            continue
        command = definition.get("command")
        if not is_nonempty_string(command):
            errors.append(f"{bundle_path}.command: missing required field")
        else:
            errors.extend(
                validate_compact_bundle_command_safety(bundle_path, command, variables)
            )
        for optional_field in ("description", "expands_with", "required_for"):
            if optional_field in definition and not is_nonempty_string(definition[optional_field]):
                errors.append(f"{bundle_path}.{optional_field}: expected string")
    return errors


def validate_compact_counts(counts: Any, event_path: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(counts, dict):
        return [f"{event_path}.counts: expected object"]
    for key, value in counts.items():
        if not isinstance(value, int) or isinstance(value, bool):
            errors.append(f"{event_path}.counts.{key}: expected integer")
    return errors


def validate_compact_failure_details(event: dict[str, Any], event_path: str) -> list[str]:
    result = event.get("result")
    if result not in {"fail", "blocked"}:
        return []
    failures = event.get("failures")
    if not isinstance(failures, list) or not failures:
        return [f"{event_path}.failures: required when result is {result}"]
    return []


def validate_compact_lifecycle_stage(event: dict[str, Any], event_path: str) -> list[str]:
    lifecycle_stage = event.get("lifecycle_stage")
    if lifecycle_stage is None or not isinstance(lifecycle_stage, str):
        return []
    if lifecycle_stage not in COMPACT_LIFECYCLE_INDEX:
        allowed = ", ".join(COMPACT_LIFECYCLE_STAGES)
        return [f"{event_path}.lifecycle_stage: expected one of: {allowed}"]
    return []


def resolve_compact_event_path(
    template: Any,
    variables: dict[str, str],
    path: str,
) -> tuple[str | None, list[str]]:
    if not is_nonempty_string(template):
        return None, [f"{path}: expected string"]
    try:
        resolved = resolve_compact_path_template(template, variables)
    except MetadataValidationError as exc:
        return None, [f"{path}: {exc}"]
    return resolved, validate_repo_relative_path(resolved, path)


def iter_compact_paths_added(value: Any, path: str) -> list[tuple[str, Any]]:
    paths: list[tuple[str, Any]] = []
    if isinstance(value, str):
        paths.append((path, value))
        return paths
    if isinstance(value, list):
        for index, child in enumerate(value):
            paths.extend(iter_compact_paths_added(child, path_label(path, index)))
        return paths
    if isinstance(value, dict):
        for key, child in value.items():
            paths.extend(iter_compact_paths_added(child, path_label(path, key)))
        return paths
    paths.append((path, value))
    return paths


def validate_compact_event_paths(
    event: dict[str, Any],
    event_path: str,
    variables: dict[str, str],
) -> list[str]:
    errors: list[str] = []
    if "paths_added" not in event:
        return errors
    paths_added = iter_compact_paths_added(
        event["paths_added"], f"{event_path}.paths_added"
    )
    for path, template in paths_added:
        resolved, path_errors = resolve_compact_event_path(template, variables, path)
        errors.extend(path_errors)
        if resolved and not (ROOT / resolved).exists():
            errors.append(f"{path}: referenced artifact does not exist: {resolved}")
    return errors


def validate_compact_transcript_reference(
    event: dict[str, Any],
    event_path: str,
    variables: dict[str, str],
) -> list[str]:
    evidence = event.get("evidence")
    if evidence is None:
        return []
    if not isinstance(evidence, dict):
        return [f"{event_path}.evidence: expected object"]
    if "transcript" not in evidence or evidence["transcript"] is None:
        return []

    transcript_path = f"{event_path}.evidence.transcript"
    transcript = evidence["transcript"]
    if not is_nonempty_string(transcript):
        return [f"{transcript_path}: expected string"]
    if transcript.count("#") > 1:
        return [f"{transcript_path}: malformed transcript reference"]
    file_template, _, anchor = transcript.partition("#")
    if not file_template or (transcript.endswith("#") and not anchor):
        return [f"{transcript_path}: malformed transcript reference"]
    resolved, errors = resolve_compact_event_path(file_template, variables, transcript_path)
    if errors:
        return errors
    if resolved and not (ROOT / resolved).exists():
        return [
            f"{transcript_path}: referenced transcript file does not exist: {resolved}"
        ]
    return []


def validate_compact_event(
    event: Any,
    index: int,
    validation_bundles: dict[str, Any],
    variables: dict[str, str] | None = None,
) -> list[str]:
    event_path = path_label("validation_events", index)
    if not isinstance(event, dict):
        return [f"{event_path}: expected object"]

    errors: list[str] = []
    for field in ("stage", "lifecycle_stage", "bundles", "result"):
        if field not in event:
            errors.append(f"{event_path}.{field}: missing required field")

    for field in ("stage", "lifecycle_stage"):
        if field in event and not is_nonempty_string(event[field]):
            errors.append(f"{event_path}.{field}: expected string")
    errors.extend(validate_compact_lifecycle_stage(event, event_path))

    bundles = event.get("bundles")
    if "bundles" in event:
        if not isinstance(bundles, list):
            errors.append(f"{event_path}.bundles: expected array")
        else:
            for bundle_index, bundle_id in enumerate(bundles):
                bundle_path = path_label(path_label(event_path, "bundles"), bundle_index)
                if not is_nonempty_string(bundle_id):
                    errors.append(f"{bundle_path}: expected string")
                    continue
                if bundle_id not in validation_bundles:
                    errors.append(
                        f"{bundle_path}: unknown validation bundle '{bundle_id}'"
                    )

    result = event.get("result")
    if "result" in event and result not in VALIDATION_EVENT_RESULTS:
        allowed = ", ".join(sorted(VALIDATION_EVENT_RESULTS))
        errors.append(f"{event_path}.result: expected one of: {allowed}")

    if "counts" in event:
        errors.extend(validate_compact_counts(event["counts"], event_path))

    errors.extend(validate_compact_failure_details(event, event_path))
    if variables is not None:
        errors.extend(validate_compact_event_paths(event, event_path, variables))
        errors.extend(validate_compact_transcript_reference(event, event_path, variables))
    return errors


def validate_compact_first_exists(
    resolved_vars: dict[str, str],
    validation_events: list[Any],
) -> list[str]:
    errors: list[str] = []
    valid_lifecycle_stages = [
        event.get("lifecycle_stage")
        for event in validation_events
        if isinstance(event, dict) and event.get("lifecycle_stage") in COMPACT_LIFECYCLE_INDEX
    ]
    if not valid_lifecycle_stages:
        return errors

    for key, first_stage in COMPACT_ARTIFACT_FIRST_EXISTS.items():
        if key not in resolved_vars:
            continue
        if not any(compact_stage_reaches(stage, first_stage) for stage in valid_lifecycle_stages):
            continue
        resolved = resolved_vars[key]
        if not (ROOT / resolved).exists():
            errors.append(
                f"{path_label('path_vars', key)}: required artifact does not exist: {resolved}"
            )
    return errors


def validate_compact_metadata_semantics(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return []

    errors = validate_compact_required_fields(data)
    errors.extend(validate_compact_top_level_shape(data))
    errors.extend(validate_no_compact_path_opt_outs(data))

    path_vars = data.get("path_vars")
    resolved_vars: dict[str, str] = {}
    if isinstance(path_vars, dict):
        resolved_vars, path_var_errors = resolve_compact_path_vars(path_vars)
        errors.extend(path_var_errors)

    validation_bundles = data.get("validation_bundles")
    if isinstance(validation_bundles, dict):
        errors.extend(validate_compact_bundle_definitions(validation_bundles, resolved_vars))

    validation_events = data.get("validation_events")
    if isinstance(validation_events, list) and isinstance(validation_bundles, dict):
        for index, event in enumerate(validation_events):
            errors.extend(
                validate_compact_event(event, index, validation_bundles, resolved_vars)
            )
        errors.extend(validate_compact_first_exists(resolved_vars, validation_events))

    return errors


def validate_file(path: Path) -> list[str]:
    data = load_yaml(path)
    if is_compact_metadata(data):
        return validate_compact_metadata_semantics(data)
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
