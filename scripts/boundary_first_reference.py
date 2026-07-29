#!/usr/bin/env python3
"""Closed manifest and raw-byte projections for boundary-first-v1."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Mapping

METHOD_VERSION = "boundary-first-v1"
RESOURCE_MANIFEST = Path("specs/boundary-first-resources.yaml")
CANONICAL_REFERENCE = Path(
    "specs/references/boundary-first-method-v1.md"
)
PROJECTED_REFERENCE = Path("references/boundary-first-method-v1.md")
GOVERNED_SKILLS = (
    "workflow",
    "spec",
    "spec-review",
    "plan",
    "plan-review",
    "test-spec",
    "test-spec-review",
    "implement",
    "code-review",
    "verify",
)
RESOURCE_IDS = ("compact-core", "feature-authoring", "proof")
PROJECTION_MODES = frozenset({"check", "write"})
_TOP_LEVEL_FIELDS = frozenset(
    {"schema_version", "contract_version", "resources"}
)
_RESOURCE_FIELDS = frozenset({"id", "source", "target", "consumers"})


class ProjectionContractError(ValueError):
    """Raised when a closed projection input is invalid."""


@dataclass(frozen=True)
class Resource:
    resource_id: str
    source: Path
    target: Path
    consumers: tuple[str, ...]


@dataclass(frozen=True)
class ResourceManifest:
    schema_version: int
    contract_version: str
    resources: tuple[Resource, ...]
    sha256: str


@dataclass(frozen=True)
class ProjectionResult:
    ok: bool
    mode: str
    source_sha256: str
    manifest_sha256: str
    projection_sha256: str
    records: Mapping[str, str]
    errors: tuple[str, ...]


def raw_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def inventory_digest(records: Mapping[str, str]) -> str:
    """Hash sorted POSIX path, NUL, raw-byte digest, newline records."""

    serialized = b"".join(
        f"{PurePosixPath(path)}\0{records[path].lower()}\n".encode("utf-8")
        for path in sorted(records)
    )
    return raw_sha256(serialized)


def _manifest_error(code: str, detail: str) -> ProjectionContractError:
    return ProjectionContractError(f"BFR-MANIFEST-{code}: {detail}")


def _split_mapping(
    stripped: str, *, line_number: int
) -> tuple[str, str]:
    if ":" not in stripped:
        raise _manifest_error(
            "SYNTAX", f"line {line_number} is not a mapping entry"
        )
    key, value = stripped.split(":", 1)
    if not key or key.strip() != key:
        raise _manifest_error(
            "SYNTAX", f"line {line_number} has an invalid key"
        )
    return key, value.strip()


def _parse_manifest_text(text: str) -> dict[str, object]:
    """Parse the intentionally small, dependency-free manifest subset."""

    lines = [
        (number, len(raw) - len(raw.lstrip(" ")), raw.strip())
        for number, raw in enumerate(text.splitlines(), start=1)
        if raw.strip() and not raw.lstrip().startswith("#")
    ]
    document: dict[str, object] = {}
    resources: list[dict[str, object]] = []
    index = 0
    while index < len(lines):
        number, indent, stripped = lines[index]
        if indent != 0:
            raise _manifest_error(
                "SYNTAX", f"line {number} has unexpected indentation"
            )
        key, value = _split_mapping(stripped, line_number=number)
        if key in document:
            raise _manifest_error("DUPLICATE-KEY", key)
        if key == "resources":
            if value:
                raise _manifest_error(
                    "SYNTAX", "resources must be a block list"
                )
            index += 1
            while index < len(lines) and lines[index][1] > 0:
                item_number, item_indent, item_text = lines[index]
                if item_indent != 2 or not item_text.startswith("- "):
                    raise _manifest_error(
                        "SYNTAX",
                        f"line {item_number} must begin a resource entry",
                    )
                resource: dict[str, object] = {}
                first_key, first_value = _split_mapping(
                    item_text[2:], line_number=item_number
                )
                resource[first_key] = first_value
                index += 1
                while index < len(lines) and lines[index][1] > 2:
                    field_number, field_indent, field_text = lines[index]
                    if field_indent != 4:
                        raise _manifest_error(
                            "SYNTAX",
                            f"line {field_number} has unexpected indentation",
                        )
                    field, field_value = _split_mapping(
                        field_text, line_number=field_number
                    )
                    if field in resource:
                        raise _manifest_error(
                            "DUPLICATE-KEY",
                            f"resource {len(resources) + 1}: {field}",
                        )
                    if field == "consumers":
                        if field_value:
                            raise _manifest_error(
                                "SYNTAX", "consumers must be a block list"
                            )
                        consumers: list[str] = []
                        index += 1
                        while (
                            index < len(lines) and lines[index][1] > 4
                        ):
                            (
                                consumer_number,
                                consumer_indent,
                                consumer_text,
                            ) = lines[index]
                            if (
                                consumer_indent != 6
                                or not consumer_text.startswith("- ")
                            ):
                                raise _manifest_error(
                                    "SYNTAX",
                                    "line "
                                    f"{consumer_number} must be a consumer",
                                )
                            consumers.append(consumer_text[2:])
                            index += 1
                        resource[field] = consumers
                        continue
                    resource[field] = field_value
                    index += 1
                resources.append(resource)
            document[key] = resources
            continue
        document[key] = value
        index += 1
    return document


def _closed_path(value: object, *, field: str) -> Path:
    if not isinstance(value, str) or not value:
        raise _manifest_error("PATH", f"{field} must be a non-empty path")
    if "\\" in value:
        raise _manifest_error("PATH", f"{field} must use POSIX separators")
    raw_parts = value.split("/")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or any(part in {"", ".", ".."} for part in raw_parts)
        or path.as_posix() != value
    ):
        raise _manifest_error(
            "PATH", f"{field} is not a normalized repository-relative path"
        )
    if field == "source" and raw_parts[:2] != ["specs", "references"]:
        raise _manifest_error(
            "PATH", f"source is outside specs/references: {value}"
        )
    if field == "target" and (
        len(raw_parts) != 2 or raw_parts[0] != "references"
    ):
        raise _manifest_error(
            "PATH", f"target is outside references/: {value}"
        )
    return Path(*path.parts)


def load_resource_manifest(root: Path) -> ResourceManifest:
    repository_root = root.resolve()
    manifest_path = _repository_path(repository_root, RESOURCE_MANIFEST)
    if not manifest_path.is_file():
        raise ProjectionContractError(
            f"BFR-MANIFEST-MISSING: {RESOURCE_MANIFEST.as_posix()}"
        )
    raw = manifest_path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise _manifest_error("ENCODING", "manifest must be UTF-8") from exc
    data = _parse_manifest_text(text)

    if frozenset(data) != _TOP_LEVEL_FIELDS:
        raise _manifest_error(
            "FIELDS",
            f"expected {sorted(_TOP_LEVEL_FIELDS)}, got {sorted(data)}",
        )
    schema_version = data["schema_version"]
    if schema_version != "1":
        raise _manifest_error(
            "SCHEMA-VERSION-UNKNOWN",
            f"expected 1, got {schema_version!r}",
        )
    contract_version = data["contract_version"]
    if contract_version != METHOD_VERSION:
        raise _manifest_error(
            "CONTRACT-VERSION-UNKNOWN",
            f"expected {METHOD_VERSION}, got {contract_version!r}",
        )

    raw_resources = data["resources"]
    if not isinstance(raw_resources, list):
        raise _manifest_error("RESOURCES", "resources must be a list")
    resource_ids = tuple(
        resource.get("id") if isinstance(resource, dict) else None
        for resource in raw_resources
    )
    if resource_ids != RESOURCE_IDS:
        raise _manifest_error(
            "RESOURCE-ID-UNKNOWN",
            f"expected {list(RESOURCE_IDS)}, got {list(resource_ids)}",
        )

    resources: list[Resource] = []
    sources: set[Path] = set()
    targets: set[Path] = set()
    for raw_resource in raw_resources:
        assert isinstance(raw_resource, dict)
        resource_id = str(raw_resource.get("id"))
        if frozenset(raw_resource) != _RESOURCE_FIELDS:
            raise _manifest_error(
                "FIELDS",
                f"{resource_id} expected {sorted(_RESOURCE_FIELDS)}, "
                f"got {sorted(raw_resource)}",
            )
        source = _closed_path(raw_resource["source"], field="source")
        target = _closed_path(raw_resource["target"], field="target")
        if source in sources:
            raise _manifest_error("SOURCE-DUPLICATE", source.as_posix())
        if target in targets:
            raise _manifest_error("TARGET-DUPLICATE", target.as_posix())
        sources.add(source)
        targets.add(target)

        raw_consumers = raw_resource["consumers"]
        if not isinstance(raw_consumers, list) or not raw_consumers:
            raise _manifest_error(
                "CONSUMERS", f"{resource_id} consumers must be non-empty"
            )
        consumers = tuple(raw_consumers)
        unknown = [
            consumer
            for consumer in consumers
            if not isinstance(consumer, str)
            or consumer not in GOVERNED_SKILLS
        ]
        if unknown:
            raise _manifest_error(
                "CONSUMER-UNKNOWN",
                f"{resource_id} contains {unknown!r}",
            )
        if len(consumers) != len(set(consumers)):
            raise _manifest_error(
                "CONSUMER-DUPLICATE", resource_id
            )
        expected_order = tuple(
            skill for skill in GOVERNED_SKILLS if skill in consumers
        )
        if consumers != expected_order:
            raise _manifest_error(
                "CONSUMER-ORDER", resource_id
            )
        resources.append(
            Resource(
                resource_id=resource_id,
                source=source,
                target=target,
                consumers=consumers,
            )
        )

    return ResourceManifest(
        schema_version=1,
        contract_version=METHOD_VERSION,
        resources=tuple(resources),
        sha256=raw_sha256(raw),
    )


def projected_paths(root: Path | None = None) -> tuple[Path, ...]:
    if root is None:
        root = Path(__file__).resolve().parents[1]
    manifest = load_resource_manifest(root)
    return tuple(
        Path("skills") / consumer / resource.target
        for resource in manifest.resources
        for consumer in resource.consumers
    )


def _relative_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _repository_path(root: Path, relative: Path) -> Path:
    if relative.is_absolute() or ".." in relative.parts:
        raise ProjectionContractError(
            f"BFR-PATH-OUTSIDE: {relative.as_posix()}"
        )
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ProjectionContractError(
                "BFR-PATH-SYMLINK: "
                + _relative_posix(current, root)
            )
    return current


def _unexpected_projections(
    root: Path, expected_paths: tuple[Path, ...]
) -> tuple[tuple[Path, ...], tuple[str, ...]]:
    expected = {root / path for path in expected_paths}
    skills_root = _repository_path(root, Path("skills"))
    if not skills_root.is_dir():
        return (), ()
    found: set[Path] = set()
    errors: list[str] = []
    for skill_root in skills_root.iterdir():
        if skill_root.is_symlink():
            errors.append(
                "BFR-UNEXPECTED-CONSUMER-SYMLINK: "
                + _relative_posix(skill_root, root)
            )
            continue
        if not skill_root.is_dir():
            continue
        references = skill_root / "references"
        if references.is_symlink():
            errors.append(
                "BFR-UNEXPECTED-CONSUMER-SYMLINK: "
                + _relative_posix(references, root)
            )
            continue
        if not references.is_dir():
            continue
        for candidate in references.glob("boundary-first-*-v1.md"):
            if candidate.is_symlink() or candidate.is_file():
                found.add(candidate)
    return tuple(sorted(found - expected)), tuple(sorted(errors))


def project_reference(root: Path, *, mode: str) -> ProjectionResult:
    """Write or check the complete boundary-first resource projection."""

    if mode not in PROJECTION_MODES:
        raise ProjectionContractError(
            f"BFR-MODE-UNKNOWN: unknown projection mode '{mode}'"
        )

    repository_root = root.resolve()
    manifest = load_resource_manifest(repository_root)
    source_bytes: dict[str, bytes] = {}
    source_hashes: dict[str, str] = {}
    operations: list[tuple[Path, bytes, str]] = []

    for resource in manifest.resources:
        source = _repository_path(repository_root, resource.source)
        if not source.is_file():
            raise ProjectionContractError(
                f"BFR-SOURCE-MISSING: {resource.source.as_posix()}"
            )
        data = source.read_bytes()
        source_bytes[resource.resource_id] = data
        source_hashes[resource.resource_id] = raw_sha256(data)
        for consumer in resource.consumers:
            relative = Path("skills") / consumer / resource.target
            _repository_path(repository_root, relative)
            operations.append((relative, data, resource.resource_id))

    expected_paths = tuple(operation[0] for operation in operations)
    unexpected, topology_errors = _unexpected_projections(
        repository_root, expected_paths
    )
    preflight_errors = list(topology_errors)
    preflight_errors.extend(
        "BFR-PROJECTION-UNEXPECTED: "
        + _relative_posix(path, repository_root)
        for path in unexpected
    )
    if mode == "write" and preflight_errors:
        return ProjectionResult(
            ok=False,
            mode=mode,
            source_sha256=source_hashes["compact-core"],
            manifest_sha256=manifest.sha256,
            projection_sha256=inventory_digest({}),
            records={},
            errors=tuple(sorted(preflight_errors)),
        )

    if mode == "write":
        for relative, data, _resource_id in operations:
            target = _repository_path(repository_root, relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)

    records: dict[str, str] = {}
    errors = list(preflight_errors)
    for relative, _data, resource_id in operations:
        target = _repository_path(repository_root, relative)
        relative_text = relative.as_posix()
        if not target.is_file():
            errors.append(f"BFR-PROJECTION-MISSING: {relative_text}")
            continue
        actual = raw_sha256(target.read_bytes())
        records[relative_text] = actual
        if actual != source_hashes[resource_id]:
            errors.append(f"BFR-PROJECTION-STALE: {relative_text}")

    return ProjectionResult(
        ok=not errors,
        mode=mode,
        source_sha256=source_hashes["compact-core"],
        manifest_sha256=manifest.sha256,
        projection_sha256=inventory_digest(records),
        records=records,
        errors=tuple(sorted(errors)),
    )
