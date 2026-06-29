#!/usr/bin/env python3
"""Release transaction profile loading and validation helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "release-profile-v1"
EXPECTED_NPM_PACKAGE = "@xiongxianfei/rigorloop"
RELEASE_KINDS = frozenset(("routine", "special"))
ROUTINE_RELEASE_KIND = "routine"
SPECIAL_RELEASE_KIND = "special"
ROUTINE_TARGETS = ("codex", "claude", "opencode")
SUPPORTED_TARGETS = frozenset(ROUTINE_TARGETS)
REQUIRED_VALUE = "required"

REQUIRED_TOP_LEVEL_FIELDS = (
    "schema_version",
    "release_kind",
    "release_tag",
    "package_version",
    "npm_package",
    "targets",
    "adapter_artifacts",
    "publication",
    "evidence",
    "validation",
)
REQUIRED_ADAPTER_ARTIFACT_FIELDS = (
    "required",
    "metadata_file",
    "archive_version",
)
REQUIRED_PUBLICATION_FIELDS = (
    "github_release_required",
    "npm_publication_required",
    "trusted_publishing_required",
    "public_smoke_required",
)
REQUIRED_EVIDENCE_FIELDS = (
    "release_yaml",
    "release_notes",
    "npm_publication",
    "public_target_init_smoke",
    "archive_hashes",
    "tree_hashes",
    "file_counts",
    "timing",
)
REQUIRED_VALIDATION_FIELDS = (
    "local_release_verify_required",
    "ci_release_verify_required",
    "security_scanning_required",
)


class ReleaseProfileError(ValueError):
    """Raised when a release profile cannot be parsed or validated."""

    def __init__(self, path: Path, errors: list[str]) -> None:
        self.path = path
        self.errors = errors
        super().__init__(f"{path}: " + "; ".join(errors))


@dataclass(frozen=True)
class ReleaseProfile:
    path: Path
    schema_version: str
    release_kind: str
    release_tag: str
    package_version: str
    npm_package: str
    targets: tuple[str, ...]
    adapter_artifacts: dict[str, Any]
    publication: dict[str, Any]
    evidence: dict[str, Any]
    validation: dict[str, Any]
    owner_decision: str | None = None


def profile_path_for_tag(tag: str, *, root: Path | str = Path(".")) -> Path:
    return Path(root) / "docs" / "releases" / "profiles" / f"{tag}.yaml"


def load_release_profile(tag: str, *, root: Path | str = Path(".")) -> ReleaseProfile:
    path = profile_path_for_tag(tag, root=root)
    profile = load_release_profile_file(path)
    if profile.release_tag != tag:
        raise ReleaseProfileError(
            path,
            [f"release_tag {profile.release_tag} does not match requested tag {tag}"],
        )
    return profile


def load_release_profile_file(path: Path | str) -> ReleaseProfile:
    profile_path = Path(path)
    try:
        text = profile_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ReleaseProfileError(
            profile_path,
            [f"release profile not found: {profile_path}"],
        ) from exc
    except OSError as exc:
        raise ReleaseProfileError(profile_path, [f"could not read release profile: {exc}"]) from exc

    try:
        data = _parse_profile_yaml(text)
    except ValueError as exc:
        raise ReleaseProfileError(profile_path, [f"could not parse release profile: {exc}"]) from exc

    return _validate_profile_data(profile_path, data)


def is_routine_release_profile(profile: ReleaseProfile) -> bool:
    return profile.release_kind == ROUTINE_RELEASE_KIND


def _validate_profile_data(path: Path, data: dict[str, Any]) -> ReleaseProfile:
    closed_errors = _closed_vocabulary_errors(data)
    if closed_errors:
        raise ReleaseProfileError(path, closed_errors)

    errors: list[str] = []
    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if field not in data:
            errors.append(f"release profile missing required field: {field}")

    if errors:
        raise ReleaseProfileError(path, errors)

    release_tag = _require_string(errors, data, "release_tag")
    package_version = _require_string(errors, data, "package_version")
    schema_version = _require_string(errors, data, "schema_version")
    release_kind = _require_string(errors, data, "release_kind")
    npm_package = _require_string(errors, data, "npm_package")
    targets = _require_string_list(errors, data, "targets")
    adapter_artifacts = _require_mapping(errors, data, "adapter_artifacts")
    publication = _require_mapping(errors, data, "publication")
    evidence = _require_mapping(errors, data, "evidence")
    validation = _require_mapping(errors, data, "validation")
    owner_decision = data.get("owner_decision")
    if owner_decision is not None and not isinstance(owner_decision, str):
        errors.append("owner_decision must be a string")
        owner_decision = None

    if schema_version and schema_version != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    if release_tag and package_version:
        expected_package_version = release_tag.removeprefix("v")
        if package_version != expected_package_version:
            errors.append(
                f"package_version {package_version} does not match release_tag {release_tag}"
            )
    if npm_package and npm_package != EXPECTED_NPM_PACKAGE:
        errors.append(f"npm_package must be {EXPECTED_NPM_PACKAGE}")

    _require_mapping_fields(errors, adapter_artifacts, "adapter_artifacts", REQUIRED_ADAPTER_ARTIFACT_FIELDS)
    _require_mapping_fields(errors, publication, "publication", REQUIRED_PUBLICATION_FIELDS)
    _require_mapping_fields(errors, evidence, "evidence", REQUIRED_EVIDENCE_FIELDS)
    _require_mapping_fields(errors, validation, "validation", REQUIRED_VALIDATION_FIELDS)

    if adapter_artifacts and adapter_artifacts.get("required") is not True:
        errors.append("adapter_artifacts.required must be true")
    for field in REQUIRED_PUBLICATION_FIELDS:
        if publication and publication.get(field) is not True:
            errors.append(f"publication.{field} must be true")
    for field in REQUIRED_EVIDENCE_FIELDS:
        if evidence and evidence.get(field) != REQUIRED_VALUE:
            errors.append(f"evidence.{field} must be required")
    for field in REQUIRED_VALIDATION_FIELDS:
        if validation and validation.get(field) is not True:
            errors.append(f"validation.{field} must be true")

    if release_kind == ROUTINE_RELEASE_KIND and tuple(targets) != ROUTINE_TARGETS:
        errors.append(
            "routine release targets must be codex, claude, opencode in that order"
        )
    if release_kind == SPECIAL_RELEASE_KIND and not owner_decision:
        errors.append("special release requires owner_decision")

    if errors:
        raise ReleaseProfileError(path, errors)

    return ReleaseProfile(
        path=path,
        schema_version=schema_version,
        release_kind=release_kind,
        release_tag=release_tag,
        package_version=package_version,
        npm_package=npm_package,
        targets=tuple(targets),
        adapter_artifacts=dict(adapter_artifacts),
        publication=dict(publication),
        evidence=dict(evidence),
        validation=dict(validation),
        owner_decision=owner_decision,
    )


def _closed_vocabulary_errors(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    release_kind = data.get("release_kind")
    if isinstance(release_kind, str) and release_kind not in RELEASE_KINDS:
        errors.append(f"unknown release_kind: {release_kind}")

    targets = data.get("targets")
    if isinstance(targets, list):
        for target in targets:
            if isinstance(target, str) and target not in SUPPORTED_TARGETS:
                errors.append(f"unknown target: {target}")
    return errors


def _require_string(errors: list[str], data: dict[str, Any], field: str) -> str:
    value = data.get(field)
    if isinstance(value, str) and value:
        return value
    errors.append(f"{field} must be a non-empty string")
    return ""


def _require_string_list(errors: list[str], data: dict[str, Any], field: str) -> list[str]:
    value = data.get(field)
    if isinstance(value, list) and value and all(isinstance(item, str) for item in value):
        return list(value)
    errors.append(f"{field} must be a non-empty list of strings")
    return []


def _require_mapping(errors: list[str], data: dict[str, Any], field: str) -> dict[str, Any]:
    value = data.get(field)
    if isinstance(value, dict):
        return dict(value)
    errors.append(f"{field} must be a mapping")
    return {}


def _require_mapping_fields(
    errors: list[str],
    mapping: dict[str, Any],
    prefix: str,
    fields: tuple[str, ...],
) -> None:
    for field in fields:
        if field not in mapping:
            errors.append(f"missing required field: {prefix}.{field}")


def _parse_profile_yaml(text: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_key: str | None = None

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        if indent == 0:
            if ":" not in line:
                raise ValueError(f"line {line_number} is missing ':'")
            key, raw_value = line.split(":", 1)
            key = key.strip()
            if not key:
                raise ValueError(f"line {line_number} has an empty key")
            value = raw_value.strip()
            if value:
                data[key] = _parse_scalar(value)
                current_key = None
            else:
                data[key] = None
                current_key = key
            continue

        if current_key is None:
            raise ValueError(f"line {line_number} has indented content without a parent key")
        if indent != 2:
            raise ValueError(f"line {line_number} uses unsupported indentation")

        if line.startswith("- "):
            if data[current_key] is None:
                data[current_key] = []
            if not isinstance(data[current_key], list):
                raise ValueError(f"line {line_number} mixes list and mapping values")
            data[current_key].append(_parse_scalar(line[2:].strip()))
            continue

        if ":" not in line:
            raise ValueError(f"line {line_number} is missing ':'")
        if data[current_key] is None:
            data[current_key] = {}
        if not isinstance(data[current_key], dict):
            raise ValueError(f"line {line_number} mixes mapping and list values")
        key, raw_value = line.split(":", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"line {line_number} has an empty key")
        value = raw_value.strip()
        if not value:
            raise ValueError(f"line {line_number} has an empty mapping value")
        data[current_key][key] = _parse_scalar(value)

    return data


def _parse_scalar(value: str) -> str | bool:
    if value == "true":
        return True
    if value == "false":
        return False
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value
