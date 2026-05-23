#!/usr/bin/env python3
"""Validation cache identity primitives for first-slice idempotency."""

from __future__ import annotations

import ast
import hashlib
import json
import posixpath
import re
import shlex
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Iterable, Sequence


class CacheIdentityError(ValueError):
    """Raised when a value is unsafe or unsupported for cache identity."""


@dataclass(frozen=True)
class CommandFamilyEvaluation:
    cache_eligible: bool
    validator_id: str | None
    command_family: str | None
    reason: str


@dataclass(frozen=True)
class NormalizedLifecycleCommand:
    argv: tuple[str, ...]
    explicit_paths: tuple[str, ...]
    command_hash: str


@dataclass(frozen=True)
class Manifest:
    files: tuple[dict[str, str], ...]
    manifest_hash: str


@dataclass(frozen=True)
class LocalCacheRecord:
    repository_id: str
    branch: str
    worktree_id: str
    change_id: str
    command_hash: str
    input_surface_hash: str
    implementation_hash: str
    policy_hash: str
    result: str
    created_at: float = 0.0

    def with_updates(self, **updates: object) -> "LocalCacheRecord":
        return replace(self, **updates)


@dataclass(frozen=True)
class LocalCacheContext:
    repository_id: str
    branch: str
    worktree_id: str
    change_id: str
    command_hash: str
    input_surface_hash: str
    implementation_hash: str
    policy_hash: str
    now: float = 0.0
    ttl_seconds: float | None = None

    def with_updates(self, **updates: object) -> "LocalCacheContext":
        return replace(self, **updates)


@dataclass(frozen=True)
class LocalCacheEligibility:
    eligible: bool
    reason: str


_WINDOWS_ABSOLUTE_RE = re.compile(r"^[A-Za-z]:[\\/]")
_URL_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*://")
_HOSTNAME_PATH_RE = re.compile(r"^[A-Za-z0-9.-]+\.[A-Za-z]{2,}[/:]")
_UNSAFE_PATH_CHARS = set("*?[")

_DEFAULT_POLICY_FILES = (
    "CONSTITUTION.md",
    "docs/workflows.md",
    "specs/plan-index-lifecycle-ownership.md",
)


def normalize_command(command: str | Sequence[str]) -> list[str]:
    if isinstance(command, str):
        argv = shlex.split(command, posix=True)
    else:
        argv = [str(part) for part in command]
    if not argv:
        raise CacheIdentityError("command argv must not be empty")
    return argv


def command_hash(command: str | Sequence[str]) -> str:
    return _hash_json(list(normalize_command(command)))


def evaluate_command_family(command: str | Sequence[str]) -> CommandFamilyEvaluation:
    argv = normalize_command(command)
    script = _script_arg(argv)
    mode = _option_value(argv, "--mode")
    if script == "scripts/validate-artifact-lifecycle.py" and mode == "explicit-paths":
        return CommandFamilyEvaluation(
            cache_eligible=True,
            validator_id="artifact-lifecycle",
            command_family="validate-artifact-lifecycle-explicit-paths",
            reason="cache-eligible first-slice command family",
        )
    return CommandFamilyEvaluation(
        cache_eligible=False,
        validator_id=None,
        command_family=None,
        reason="unsupported first-slice command family",
    )


def normalize_repo_path(raw_path: str, repo_root: Path | str) -> str:
    del repo_root
    if raw_path is None:
        raise CacheIdentityError("path value is missing")
    raw = str(raw_path)
    if not raw:
        raise CacheIdentityError("path value is empty")
    if raw.startswith("~"):
        raise CacheIdentityError("home-relative paths are not cache-eligible")
    if raw.startswith("$") or "${" in raw:
        raise CacheIdentityError("environment-expanded paths are not cache-eligible")
    if _URL_RE.match(raw):
        raise CacheIdentityError("URLs are not cache-eligible path values")
    if _HOSTNAME_PATH_RE.match(raw):
        raise CacheIdentityError("hostname-like path values are not cache-eligible")
    if raw.startswith("/") or _WINDOWS_ABSOLUTE_RE.match(raw):
        raise CacheIdentityError("absolute paths are not cache-eligible")
    if "\\" in raw:
        raise CacheIdentityError("backslash path separators are not cache-eligible")
    if any(char in raw for char in _UNSAFE_PATH_CHARS):
        raise CacheIdentityError("glob path values are not cache-eligible")

    normalized = posixpath.normpath(raw.replace("\\", "/"))
    if normalized in (".", ""):
        raise CacheIdentityError("path value does not identify a repository file")
    parts = normalized.split("/")
    if any(part == ".." for part in parts):
        raise CacheIdentityError("escaping paths are not cache-eligible")
    if "@" in parts[0] and ":" in raw:
        raise CacheIdentityError("credential-bearing paths are not cache-eligible")
    return normalized


def normalize_lifecycle_explicit_command(
    command: str | Sequence[str], repo_root: Path | str
) -> NormalizedLifecycleCommand:
    argv = list(normalize_command(command))
    evaluation = evaluate_command_family(argv)
    if not evaluation.cache_eligible:
        raise CacheIdentityError(evaluation.reason)

    explicit_paths: list[str] = []
    normalized_argv: list[str] = []
    index = 0
    while index < len(argv):
        arg = argv[index]
        normalized_argv.append(arg)
        if arg == "--path":
            if index + 1 >= len(argv):
                raise CacheIdentityError("--path requires a value")
            normalized_path = normalize_repo_path(argv[index + 1], repo_root)
            explicit_paths.append(normalized_path)
            normalized_argv.append(normalized_path)
            index += 2
            continue
        index += 1

    if not explicit_paths:
        raise CacheIdentityError("explicit-paths commands require at least one --path value")
    duplicate_paths = sorted(path for path in set(explicit_paths) if explicit_paths.count(path) > 1)
    if duplicate_paths:
        raise CacheIdentityError(
            "duplicate explicit --path values are not cache-eligible: "
            + ", ".join(duplicate_paths)
        )

    normalized_tuple = tuple(normalized_argv)
    return NormalizedLifecycleCommand(
        argv=normalized_tuple,
        explicit_paths=tuple(explicit_paths),
        command_hash=command_hash(normalized_tuple),
    )


def build_input_surface_manifest(repo_root: Path | str, explicit_paths: Iterable[str]) -> Manifest:
    root = Path(repo_root)
    entries = [_file_entry(root, path) for path in explicit_paths]
    return Manifest(files=tuple(entries), manifest_hash=_hash_json(entries))


def build_implementation_manifest(
    repo_root: Path | str,
    entrypoint: str,
    *,
    manifest_generator: str | None = "scripts/validation_cache.py",
) -> Manifest:
    root = Path(repo_root)
    included: set[str] = set()
    pending = [normalize_repo_path(entrypoint, root)]

    while pending:
        relative = pending.pop()
        if relative in included:
            continue
        included.add(relative)
        path = root / relative
        if not path.is_file():
            continue
        for imported in _repository_imports(root, path):
            if imported not in included:
                pending.append(imported)

    if manifest_generator is not None:
        included.add(normalize_repo_path(manifest_generator, root))

    entries = [_file_entry(root, path) for path in sorted(included)]
    return Manifest(files=tuple(entries), manifest_hash=_hash_json(entries))


def build_policy_manifest(
    repo_root: Path | str, *, extra_policy_files: Iterable[str] = ()
) -> Manifest:
    root = Path(repo_root)
    paths: list[str] = []
    seen: set[str] = set()
    for raw_path in (*_DEFAULT_POLICY_FILES, *tuple(extra_policy_files)):
        normalized = normalize_repo_path(raw_path, root)
        if normalized not in seen:
            paths.append(normalized)
            seen.add(normalized)
    entries = [_file_entry(root, path) for path in paths]
    return Manifest(files=tuple(entries), manifest_hash=_hash_json(entries))


def local_cache_entry_eligible(
    record: LocalCacheRecord, context: LocalCacheContext
) -> LocalCacheEligibility:
    if record.result != "pass":
        return LocalCacheEligibility(False, "previous result was not pass")

    comparisons = (
        ("repository_id", record.repository_id, context.repository_id),
        ("branch", record.branch, context.branch),
        ("worktree_id", record.worktree_id, context.worktree_id),
        ("change_id", record.change_id, context.change_id),
        ("command_hash", record.command_hash, context.command_hash),
        ("input_surface_hash", record.input_surface_hash, context.input_surface_hash),
        ("implementation_hash", record.implementation_hash, context.implementation_hash),
        ("policy_hash", record.policy_hash, context.policy_hash),
    )
    for name, record_value, context_value in comparisons:
        if record_value != context_value:
            return LocalCacheEligibility(False, f"{name} changed")

    if context.ttl_seconds is not None and context.now - record.created_at > context.ttl_seconds:
        return LocalCacheEligibility(False, "local cache entry expired")

    return LocalCacheEligibility(True, "local cache entry matches branch/worktree/change-local key")


def _script_arg(argv: Sequence[str]) -> str | None:
    for arg in argv:
        normalized = arg.replace("\\", "/")
        if normalized.endswith("scripts/validate-artifact-lifecycle.py"):
            return "scripts/validate-artifact-lifecycle.py"
    return None


def _option_value(argv: Sequence[str], option: str) -> str | None:
    for index, arg in enumerate(argv):
        if arg == option and index + 1 < len(argv):
            return argv[index + 1]
    return None


def _file_entry(repo_root: Path, relative_path: str) -> dict[str, str]:
    normalized = normalize_repo_path(relative_path, repo_root)
    path = repo_root / normalized
    if not path.is_file():
        return {"path": normalized, "state": "missing"}
    return {"path": normalized, "state": "present", "sha256": _hash_file(path)}


def _repository_imports(repo_root: Path, source: Path) -> tuple[str, ...]:
    try:
        tree = ast.parse(source.read_text(encoding="utf-8"))
    except (OSError, SyntaxError, UnicodeDecodeError):
        return ()

    candidates: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                candidates.update(_resolve_module(repo_root, source, alias.name))
        elif isinstance(node, ast.ImportFrom):
            if node.level > 0:
                module = "." * node.level + (node.module or "")
            else:
                module = node.module or ""
            candidates.update(_resolve_module(repo_root, source, module))
            if node.module:
                continue
            for alias in node.names:
                candidates.update(_resolve_module(repo_root, source, alias.name))

    return tuple(sorted(candidates))


def _resolve_module(repo_root: Path, source: Path, module_name: str) -> set[str]:
    if not module_name:
        return set()

    cleaned = module_name.lstrip(".")
    module_parts = [part for part in cleaned.split(".") if part]
    if not module_parts:
        return set()

    candidate_paths: list[Path] = []
    module_path = Path(*module_parts)
    search_roots = [source.parent, repo_root]
    for search_root in search_roots:
        candidate_paths.append(search_root / f"{module_path}.py")
        candidate_paths.append(search_root / module_path / "__init__.py")

    resolved: set[str] = set()
    for candidate in candidate_paths:
        try:
            relative = candidate.resolve().relative_to(repo_root.resolve())
        except (OSError, ValueError):
            continue
        if candidate.is_file():
            resolved.add(relative.as_posix())
    return resolved


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def _hash_json(value: object) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"
