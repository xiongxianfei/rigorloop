#!/usr/bin/env python3
"""Closed manifest and raw-byte projections for boundary-first-v1."""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Mapping

METHOD_VERSION = "boundary-first-v1"
RESOURCE_MANIFEST = Path("specs/boundary-first-resources.yaml")
RESOURCE_MANIFEST_SHA256 = (
    "8f255f2706fd18081921bb4725fd24715dddb9d61e0cc17cc36ec8cc4289ff71"
)
CANONICAL_REFERENCE = Path(
    "specs/references/boundary-first-method-v1.md"
)
PROJECTED_REFERENCE = Path("references/boundary-first-method-v1.md")
GOVERNED_SKILLS = (
    "workflow",
    "spec",
    "design-review",
    "plan",
    "delivery-review",
    "implement",
    "code-review",
    "verify",
)
RESOURCE_IDS = ("compact-core", "feature-authoring", "proof")
RESOURCE_IDENTITY_SHA256 = {
    "compact-core": (
        "ec9d4a5cd0c0111a1d0da08b7170c1f1a6b0eaf3609c4b9555023aad4887072e"
    ),
    "feature-authoring": (
        "78cf6cc80e180781526fc33f4b0894dccf6373a429be8ff13c7e5a7567f6272e"
    ),
    "proof": (
        "2b1578894cb078139cf5be7f1193784b639aedcdeefe75ff7a083fd1feb974cc"
    ),
}
PROJECTION_MODES = frozenset({"check", "write"})
_TOP_LEVEL_FIELDS = frozenset(
    {"schema_version", "contract_version", "resources"}
)
_RESOURCE_FIELDS = frozenset({"id", "source", "target", "consumers"})


class ProjectionContractError(ValueError):
    """Raised when a closed projection input is invalid."""

    def __init__(
        self,
        code_or_text: str,
        *,
        path: str = "-",
        message: str = "",
        offending_value: str = "-",
        expected: str = "-",
    ) -> None:
        if ": " in code_or_text and not message:
            code, detail = code_or_text.split(": ", 1)
            message = detail
        else:
            code = code_or_text
        self.code = code
        self.path = path
        self.message = message
        self.offending_value = offending_value
        self.expected = expected
        display = path if path != "-" else message
        super().__init__(f"{code}: {display}")


def _bounded_diagnostic_value(value: object) -> str:
    text = str(value)
    home = str(Path.home())
    if text.startswith("/") or (home and home in text):
        return "<redacted>"
    return text.replace("\n", "\\n")[:300]


def format_contract_error(error: ProjectionContractError) -> str:
    """Render a stable, privacy-bounded projection diagnostic."""

    return (
        f"{error.code}: path={_bounded_diagnostic_value(error.path)}; "
        f"message={_bounded_diagnostic_value(error.message)}; "
        "offending_value="
        f"{_bounded_diagnostic_value(error.offending_value)}; "
        f"expected={_bounded_diagnostic_value(error.expected)}"
    )


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


def _resource_identity(resource: Resource) -> str:
    serialized = (
        "\0".join(
            (
                resource.resource_id,
                resource.source.as_posix(),
                resource.target.as_posix(),
                *resource.consumers,
            )
        )
        + "\n"
    ).encode("utf-8")
    return raw_sha256(serialized)


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


def _manifest_error(
    code: str,
    detail: str,
    *,
    expected: str = "exact boundary-first resource manifest contract",
    safe_message: str | None = None,
) -> ProjectionContractError:
    normalized_code = code.lower().replace("-", " ")
    return ProjectionContractError(
        f"BFR-MANIFEST-{code}",
        path=RESOURCE_MANIFEST.as_posix(),
        message=(
            safe_message
            or f"resource manifest failed {normalized_code} validation"
        ),
        offending_value=f"sha256:{raw_sha256(detail.encode('utf-8'))}",
        expected=expected,
    )


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
            "BFR-MANIFEST-MISSING",
            path=RESOURCE_MANIFEST.as_posix(),
            message="resource manifest is missing",
            expected="existing resource manifest",
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
            expected="1",
        )
    contract_version = data["contract_version"]
    if contract_version != METHOD_VERSION:
        raise _manifest_error(
            "CONTRACT-VERSION-UNKNOWN",
            f"expected {METHOD_VERSION}, got {contract_version!r}",
            expected=METHOD_VERSION,
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

    manifest_sha256 = raw_sha256(raw)
    if manifest_sha256 != RESOURCE_MANIFEST_SHA256:
        affected_layers = [
            resource.resource_id
            for resource in resources
            if _resource_identity(resource)
            != RESOURCE_IDENTITY_SHA256[resource.resource_id]
        ]
        layer_message = "affected resource layers: " + (
            ", ".join(affected_layers)
            if affected_layers
            else "manifest-metadata"
        )
        raise _manifest_error(
            "IDENTITY",
            layer_message,
            expected=RESOURCE_MANIFEST_SHA256,
            safe_message=layer_message,
        )

    return ResourceManifest(
        schema_version=1,
        contract_version=METHOD_VERSION,
        resources=tuple(resources),
        sha256=manifest_sha256,
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
            "BFR-PATH-OUTSIDE",
            path=_bounded_diagnostic_value(relative.as_posix()),
            message="repository path is outside the repository",
            offending_value=_bounded_diagnostic_value(
                relative.as_posix()
            ),
            expected="normalized repository-relative path",
        )
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ProjectionContractError(
                "BFR-PATH-SYMLINK",
                path=_relative_posix(current, root),
                message="repository path traverses a symlink",
                offending_value=_relative_posix(current, root),
                expected="repository-contained non-symlink path",
            )
    return current


def _validate_resource_version(relative: Path, data: bytes) -> None:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ProjectionContractError(
            "BFR-RESOURCE-ENCODING",
            path=relative.as_posix(),
            message="canonical resource must be UTF-8",
            expected="UTF-8 text",
        ) from exc
    versions = [
        line.partition(":")[2].strip()
        for line in text.splitlines()
        if line.startswith("Boundary model version:")
    ]
    if not versions or set(versions) != {METHOD_VERSION}:
        version_detail = ", ".join(versions) if versions else "-"
        raise ProjectionContractError(
            "BFR-RESOURCE-VERSION-UNKNOWN",
            path=relative.as_posix(),
            message="canonical resource version is missing or unknown",
            offending_value=(
                f"sha256:{raw_sha256(version_detail.encode('utf-8'))}"
            ),
            expected=METHOD_VERSION,
        )


def _open_parent_directory(
    root: Path, relative: Path, *, create: bool
) -> int:
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    descriptor = os.open(root, flags)
    try:
        for part in relative.parent.parts:
            try:
                child = os.open(part, flags, dir_fd=descriptor)
            except FileNotFoundError:
                if not create:
                    raise
                os.mkdir(part, dir_fd=descriptor)
                child = os.open(part, flags, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


def _write_target_bytes(root: Path, relative: Path, data: bytes) -> None:
    parent_fd = _open_parent_directory(root, relative, create=True)
    try:
        descriptor = os.open(
            relative.name,
            os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW,
            0o666,
            dir_fd=parent_fd,
        )
        try:
            view = memoryview(data)
            while view:
                written = os.write(descriptor, view)
                view = view[written:]
        finally:
            os.close(descriptor)
    finally:
        os.close(parent_fd)


def _remove_target(root: Path, relative: Path) -> None:
    try:
        parent_fd = _open_parent_directory(root, relative, create=False)
    except FileNotFoundError:
        return
    try:
        try:
            os.unlink(relative.name, dir_fd=parent_fd)
        except FileNotFoundError:
            pass
    finally:
        os.close(parent_fd)


def _restore_targets(
    root: Path,
    snapshots: Mapping[Path, bytes | None],
) -> tuple[str, ...]:
    errors: list[str] = []
    for relative, previous in reversed(tuple(snapshots.items())):
        try:
            if previous is None:
                _remove_target(root, relative)
            else:
                _write_target_bytes(root, relative, previous)
        except (OSError, ProjectionContractError):
            errors.append(relative.as_posix())
    return tuple(errors)


def _changed_projection_inputs(
    root: Path,
    manifest: ResourceManifest,
    source_hashes: Mapping[str, str],
) -> tuple[str, ...]:
    changed: list[str] = []
    identities = (
        (RESOURCE_MANIFEST, manifest.sha256),
        *(
            (resource.source, source_hashes[resource.resource_id])
            for resource in manifest.resources
        ),
    )
    for relative, expected_hash in identities:
        try:
            path = _repository_path(root, relative)
            if (
                not path.is_file()
                or raw_sha256(path.read_bytes()) != expected_hash
            ):
                changed.append(relative.as_posix())
        except (OSError, ProjectionContractError):
            changed.append(relative.as_posix())
    return tuple(changed)


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
        for candidate in references.rglob("*"):
            if candidate.is_symlink():
                if candidate.match("boundary-first-*.md"):
                    errors.append(
                        "BFR-UNEXPECTED-CONSUMER-SYMLINK: "
                        + _relative_posix(candidate, root)
                    )
                continue
            if (
                candidate.is_file()
                and candidate.match("boundary-first-*.md")
            ):
                found.add(candidate)
    return tuple(sorted(found - expected)), tuple(sorted(errors))


def _unexpected_canonical_resources(
    root: Path,
    expected_sources: tuple[Path, ...],
) -> tuple[Path, ...]:
    references = _repository_path(root, Path("specs/references"))
    if not references.is_dir():
        return ()
    expected = {root / source for source in expected_sources}
    found = {
        candidate
        for candidate in references.rglob("*")
        if (
            candidate.is_symlink()
            and candidate.match("boundary-first-*.md")
        )
        or (
            candidate.is_file()
            and candidate.match("boundary-first-*.md")
        )
    }
    return tuple(sorted(found - expected))


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
                "BFR-SOURCE-MISSING",
                path=resource.source.as_posix(),
                message="canonical resource is missing",
                offending_value="-",
                expected="existing canonical resource",
            )
        data = source.read_bytes()
        _validate_resource_version(resource.source, data)
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
    unexpected_canonical = _unexpected_canonical_resources(
        repository_root,
        tuple(resource.source for resource in manifest.resources),
    )
    preflight_errors = list(topology_errors)
    preflight_errors.extend(
        "BFR-PROJECTION-UNEXPECTED: "
        + _relative_posix(path, repository_root)
        for path in unexpected
    )
    preflight_errors.extend(
        "BFR-PROJECTION-UNEXPECTED: "
        + _relative_posix(path, repository_root)
        for path in unexpected_canonical
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

    snapshots: dict[Path, bytes | None] = {}
    if mode == "write":
        snapshots = {
            relative: (
                _repository_path(repository_root, relative).read_bytes()
                if _repository_path(repository_root, relative).is_file()
                else None
            )
            for relative, _data, _resource_id in operations
        }
        try:
            for relative, data, _resource_id in operations:
                _write_target_bytes(repository_root, relative, data)
        except BaseException as exc:
            restore_errors = _restore_targets(
                repository_root, snapshots
            )
            if restore_errors:
                raise ProjectionContractError(
                    "BFR-PROJECTION-RESTORE",
                    path=", ".join(restore_errors),
                    message="projection write failed and restoration was incomplete",
                    expected="all prior target bytes restored",
                ) from exc
            if isinstance(exc, OSError):
                raise ProjectionContractError(
                    "BFR-PROJECTION-WRITE",
                    path=relative.as_posix(),
                    message=(
                        "projection write failed; "
                        "prior target state restored"
                    ),
                    expected="successful complete projection write",
                ) from exc
            raise

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

    changed_inputs = _changed_projection_inputs(
        repository_root, manifest, source_hashes
    )
    if changed_inputs:
        if mode == "write":
            restore_errors = _restore_targets(
                repository_root, snapshots
            )
            if restore_errors:
                raise ProjectionContractError(
                    "BFR-PROJECTION-RESTORE",
                    path=", ".join(restore_errors),
                    message=(
                        "projection inputs changed and restoration "
                        "was incomplete"
                    ),
                    expected="all prior target bytes restored",
                )
            raise ProjectionContractError(
                "BFR-INPUT-CHANGED",
                path=", ".join(changed_inputs),
                message=(
                    "projection input changed during the transaction; "
                    "prior target state restored"
                ),
                expected="stable manifest and canonical resources",
            )
        errors.extend(
            f"BFR-INPUT-CHANGED: {path}" for path in changed_inputs
        )

    return ProjectionResult(
        ok=not errors,
        mode=mode,
        source_sha256=source_hashes["compact-core"],
        manifest_sha256=manifest.sha256,
        projection_sha256=inventory_digest(records),
        records=records,
        errors=tuple(sorted(errors)),
    )
