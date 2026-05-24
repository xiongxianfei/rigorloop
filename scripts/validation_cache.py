#!/usr/bin/env python3
"""Validation cache identity primitives for first-slice idempotency."""

from __future__ import annotations

import ast
import hashlib
import json
import posixpath
import re
import shlex
import time
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Iterable, Sequence


class CacheIdentityError(RuntimeError):
    """Raised when a value is unsafe or unsupported for cache identity."""

    def __init__(self, code: str, message: str | None = None) -> None:
        if message is None:
            message = code
            code = "cache-identity-error"
        self.code = code
        super().__init__(message)


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
class LifecycleCacheIdentity:
    validator_id: str
    command_family: str
    normalized_command: NormalizedLifecycleCommand
    displayed_command: NormalizedLifecycleCommand
    input_surface: Manifest
    implementation: Manifest
    policy: Manifest
    cache_key: str


@dataclass(frozen=True)
class LocalCacheRecord:
    cache_key: str
    validator_id: str
    command_family: str
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
    prior_event_stage: str = ""
    prior_event_evidence: str = ""

    def with_updates(self, **updates: object) -> "LocalCacheRecord":
        return replace(self, **updates)


@dataclass(frozen=True)
class LocalCacheContext:
    cache_key: str
    validator_id: str
    command_family: str
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


@dataclass(frozen=True)
class LocalCacheLookup:
    record: LocalCacheRecord | None
    reason: str


_WINDOWS_ABSOLUTE_RE = re.compile(r"^[A-Za-z]:[\\/]")
_URL_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*://")
_HOSTNAME_PATH_RE = re.compile(r"^[A-Za-z0-9.-]+\.[A-Za-z]{2,}[/:]")
_SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_UNSAFE_PATH_CHARS = set("*?[")

_DEFAULT_POLICY_FILES = (
    "CONSTITUTION.md",
    "docs/workflows.md",
    "specs/plan-index-lifecycle-ownership.md",
)
_LOCAL_CACHE_FILE = "validation-cache.json"
_SUPPORTED_VALIDATOR_ID = "artifact-lifecycle"
_SUPPORTED_COMMAND_FAMILY = "validate-artifact-lifecycle-explicit-paths"
_DIRECT_EXPLICIT_PATHS_MODE = "explicit-paths"
_INNER_LOOP_HELPER_MODE = "explicit-paths-inner-loop"


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
    if script == "scripts/validate-artifact-lifecycle.py" and mode in {
        _DIRECT_EXPLICIT_PATHS_MODE,
        _INNER_LOOP_HELPER_MODE,
    }:
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
    command: str | Sequence[str],
    repo_root: Path | str,
    *,
    canonical_cache_identity: bool = True,
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
        normalized_arg = arg
        if (
            canonical_cache_identity
            and arg == _INNER_LOOP_HELPER_MODE
            and index > 0
            and argv[index - 1] == "--mode"
        ):
            normalized_arg = _DIRECT_EXPLICIT_PATHS_MODE
        normalized_argv.append(normalized_arg)
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
    entrypoint_path = normalize_repo_path(entrypoint, root)
    _require_implementation_file(
        root,
        entrypoint_path,
        missing_code="implementation-entrypoint-missing",
        unreadable_code="implementation-entrypoint-unreadable",
        label="entrypoint",
    )
    pending = [(entrypoint_path, True)]

    while pending:
        relative, is_entrypoint = pending.pop()
        if relative in included:
            continue
        included.add(relative)
        path = root / relative
        _require_implementation_file(
            root,
            relative,
            missing_code="repository-local-import-unresolved",
            unreadable_code="repository-local-helper-unreadable",
            label="repository-local implementation file",
        )
        for imported in _repository_imports(root, path, is_entrypoint=is_entrypoint):
            if imported not in included:
                pending.append((imported, False))

    if manifest_generator is not None:
        generator_path = normalize_repo_path(manifest_generator, root)
        _require_implementation_file(
            root,
            generator_path,
            missing_code="implementation-manifest-unresolved",
            unreadable_code="implementation-manifest-unresolved",
            label="manifest generator",
        )
        included.add(generator_path)

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


def build_lifecycle_cache_identity(
    repo_root: Path | str,
    command: str | Sequence[str],
    *,
    extra_policy_files: Iterable[str] = (),
) -> LifecycleCacheIdentity:
    root = Path(repo_root)
    evaluation = evaluate_command_family(command)
    if not evaluation.cache_eligible or not evaluation.validator_id or not evaluation.command_family:
        raise CacheIdentityError(
            "unsupported-command-family",
            f"{evaluation.reason}; cache eligibility disabled",
        )
    normalized_command = normalize_lifecycle_explicit_command(
        command,
        root,
        canonical_cache_identity=True,
    )
    displayed_command = normalize_lifecycle_explicit_command(
        command,
        root,
        canonical_cache_identity=False,
    )
    explicit_path_surface = build_input_surface_manifest(root, normalized_command.explicit_paths)
    implementation = build_implementation_manifest(
        root,
        "scripts/validate-artifact-lifecycle.py",
        manifest_generator="scripts/validation_cache.py",
    )
    policy = build_policy_manifest(root, extra_policy_files=extra_policy_files)
    input_surface = Manifest(
        files=explicit_path_surface.files,
        manifest_hash=_hash_json(
            {
                "command_hash": normalized_command.command_hash,
                "explicit_paths": list(explicit_path_surface.files),
                "implementation_hash": implementation.manifest_hash,
                "policy_hash": policy.manifest_hash,
            }
        ),
    )
    cache_key = _hash_json(
        {
            "validator_id": evaluation.validator_id,
            "command_family": evaluation.command_family,
            "command_hash": normalized_command.command_hash,
            "input_surface_hash": input_surface.manifest_hash,
            "implementation_hash": implementation.manifest_hash,
            "policy_hash": policy.manifest_hash,
        }
    )
    return LifecycleCacheIdentity(
        validator_id=evaluation.validator_id,
        command_family=evaluation.command_family,
        normalized_command=normalized_command,
        displayed_command=displayed_command,
        input_surface=input_surface,
        implementation=implementation,
        policy=policy,
        cache_key=cache_key,
    )


def local_cache_entry_eligible(
    record: LocalCacheRecord, context: LocalCacheContext
) -> LocalCacheEligibility:
    if record.result != "pass":
        return LocalCacheEligibility(False, "previous result was not pass")

    identity_comparisons = (
        ("cache_key", record.cache_key, context.cache_key),
        ("validator_id", record.validator_id, context.validator_id),
        ("command_family", record.command_family, context.command_family),
    )
    for name, record_value, context_value in identity_comparisons:
        if not record_value:
            return LocalCacheEligibility(False, f"{name} missing")
        if name == "cache_key" and not _SHA256_RE.match(record_value):
            return LocalCacheEligibility(False, "cache_key malformed")
        if record_value != context_value:
            return LocalCacheEligibility(False, f"{name} changed")

    if record.validator_id != _SUPPORTED_VALIDATOR_ID:
        return LocalCacheEligibility(False, "validator_id unsupported")
    if record.command_family != _SUPPORTED_COMMAND_FAMILY:
        return LocalCacheEligibility(False, "command_family unsupported")

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


def load_local_cache_records(cache_dir: Path | str) -> tuple[LocalCacheRecord, ...]:
    path = Path(cache_dir) / _LOCAL_CACHE_FILE
    if not path.is_file():
        return ()
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ()
    records: list[LocalCacheRecord] = []
    for item in raw.get("records", []):
        if not isinstance(item, dict):
            continue
        try:
            records.append(LocalCacheRecord(**item))
        except TypeError:
            continue
    return tuple(records)


def store_local_cache_record(cache_dir: Path | str, record: LocalCacheRecord) -> None:
    directory = Path(cache_dir)
    directory.mkdir(parents=True, exist_ok=True)
    records = [
        existing
        for existing in load_local_cache_records(directory)
        if existing.cache_key != record.cache_key
    ]
    records.append(record)
    payload = {
        "schema_version": 1,
        "records": [asdict(existing) for existing in records],
    }
    (directory / _LOCAL_CACHE_FILE).write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def find_local_cache_hit(
    cache_dir: Path | str,
    context: LocalCacheContext,
) -> LocalCacheLookup:
    last_reason = "no local cache record"
    for record in load_local_cache_records(cache_dir):
        eligibility = local_cache_entry_eligible(record, context)
        if eligibility.eligible:
            return LocalCacheLookup(record=record, reason=eligibility.reason)
        last_reason = eligibility.reason
    return LocalCacheLookup(record=None, reason=last_reason)


def make_local_cache_record(
    *,
    identity: LifecycleCacheIdentity,
    context: LocalCacheContext,
    prior_event_stage: str,
    prior_event_evidence: str,
    created_at: float | None = None,
) -> LocalCacheRecord:
    return LocalCacheRecord(
        cache_key=identity.cache_key,
        validator_id=identity.validator_id,
        command_family=identity.command_family,
        repository_id=context.repository_id,
        branch=context.branch,
        worktree_id=context.worktree_id,
        change_id=context.change_id,
        command_hash=identity.normalized_command.command_hash,
        input_surface_hash=identity.input_surface.manifest_hash,
        implementation_hash=identity.implementation.manifest_hash,
        policy_hash=identity.policy.manifest_hash,
        result="pass",
        created_at=time.time() if created_at is None else created_at,
        prior_event_stage=prior_event_stage,
        prior_event_evidence=prior_event_evidence,
    )


def write_cache_hit_evidence(
    *,
    repo_root: Path | str,
    evidence_file: str,
    change_id: str,
    cache_hit_id: str,
    identity: LifecycleCacheIdentity,
    record: LocalCacheRecord,
) -> str:
    root = Path(repo_root)
    evidence_relative = normalize_repo_path(evidence_file, root)
    expected = f"docs/changes/{change_id}/validation-cache-evidence.yaml"
    if evidence_relative != expected:
        raise CacheIdentityError(
            "invalid-cache-evidence-path",
            f"cache-hit evidence must be recorded at {expected}",
        )
    _validate_evidence_ref(record.prior_event_evidence, root)
    target = root / evidence_relative
    target.parent.mkdir(parents=True, exist_ok=True)
    new_entry = _cache_hit_evidence_entry(
        cache_hit_id=cache_hit_id,
        identity=identity,
        record=record,
    )
    if target.exists():
        document = _load_cache_hit_evidence_document(target)
        if document["change_id"] != change_id:
            raise _cache_error("invalid-cache-evidence-file")
        entries = list(document["cache_hits"])
    else:
        entries = []

    ids: set[str] = set()
    for entry in entries:
        entry_id = entry["id"]
        if entry_id in ids:
            raise _cache_error("duplicate-cache-hit-id")
        ids.add(entry_id)

    merged: list[dict[str, object]] = []
    replaced = False
    for entry in entries:
        if entry["id"] == cache_hit_id:
            merged.append(new_entry)
            replaced = True
        else:
            merged.append(entry)
    if not replaced:
        merged.append(new_entry)

    target.write_text(_render_cache_hit_evidence_document(change_id, merged), encoding="utf-8")
    return evidence_relative


def _cache_hit_evidence_entry(
    *,
    cache_hit_id: str,
    identity: LifecycleCacheIdentity,
    record: LocalCacheRecord,
) -> dict[str, object]:
    return {
        "id": cache_hit_id,
        "validator_id": identity.validator_id,
        "command_family": identity.command_family,
        "evidence_kind": "cache-hit-inner-loop",
        "command": {"argv": list(identity.normalized_command.argv)},
        "displayed_command_argv": list(identity.displayed_command.argv),
        "canonical_cache_argv": list(identity.normalized_command.argv),
        "prior_passing_event": {
            "stage": record.prior_event_stage,
            "evidence": record.prior_event_evidence,
        },
        "cache_key": {
            "input_surface_hash": identity.input_surface.manifest_hash,
            "validator_implementation_hash": identity.implementation.manifest_hash,
            "policy_hash": identity.policy.manifest_hash,
            "command_hash": identity.normalized_command.command_hash,
        },
        "result_reused": "pass",
        "allowed_reason": "input surface, validator implementation, policy, and command unchanged since prior passing event",
        "scope": "inner-loop",
        "closeout_evidence": False,
    }


def _render_cache_hit_evidence_document(
    change_id: str,
    entries: Sequence[dict[str, object]],
) -> str:
    lines = [
        "schema_version: 1",
        f"change_id: {_yaml_scalar(change_id)}",
        "cache_hits:",
    ]
    for entry in sorted(entries, key=lambda item: str(item["id"])):
        command = entry["command"]
        prior = entry["prior_passing_event"]
        cache_key = entry["cache_key"]
        if not isinstance(command, dict) or not isinstance(prior, dict) or not isinstance(cache_key, dict):
            raise _cache_error("invalid-cache-evidence-file")
        argv = command.get("argv")
        if not isinstance(argv, list):
            raise _cache_error("invalid-cache-evidence-file")
        lines.extend(
            [
                f"  - id: {_yaml_scalar(str(entry['id']))}",
                f"    validator_id: {_yaml_scalar(str(entry['validator_id']))}",
                f"    command_family: {_yaml_scalar(str(entry['command_family']))}",
                f"    evidence_kind: {entry['evidence_kind']}",
                "    displayed_command_argv:",
            ]
        )
        displayed = entry["displayed_command_argv"]
        canonical = entry["canonical_cache_argv"]
        if not isinstance(displayed, list) or not isinstance(canonical, list):
            raise _cache_error("invalid-cache-evidence-file")
        for arg in displayed:
            lines.append(f"      - {_yaml_scalar(str(arg))}")
        lines.append("    canonical_cache_argv:")
        for arg in canonical:
            lines.append(f"      - {_yaml_scalar(str(arg))}")
        lines.extend(
            [
                "    command:",
                "      argv:",
            ]
        )
        for arg in argv:
            lines.append(f"        - {_yaml_scalar(str(arg))}")
        lines.extend(
            [
            "    prior_passing_event:",
                f"      stage: {_yaml_scalar(str(prior['stage']))}",
                f"      evidence: {_yaml_scalar(str(prior['evidence']))}",
            "    cache_key:",
                f"      input_surface_hash: {_yaml_scalar(str(cache_key['input_surface_hash']))}",
                f"      validator_implementation_hash: {_yaml_scalar(str(cache_key['validator_implementation_hash']))}",
                f"      policy_hash: {_yaml_scalar(str(cache_key['policy_hash']))}",
                f"      command_hash: {_yaml_scalar(str(cache_key['command_hash']))}",
                f"    result_reused: {entry['result_reused']}",
                f"    allowed_reason: {entry['allowed_reason']}",
                f"    scope: {entry['scope']}",
                f"    closeout_evidence: {str(entry['closeout_evidence']).lower()}",
            ]
        )
    lines.append("")
    return "\n".join(lines)


def _load_cache_hit_evidence_document(path: Path) -> dict[str, object]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) < 3 or lines[0] != "schema_version: 1":
        raise _cache_error("invalid-cache-evidence-file")
    if not lines[1].startswith("change_id: "):
        raise _cache_error("invalid-cache-evidence-file")
    change_id = _parse_json_scalar(lines[1].split(": ", 1)[1])
    if lines[2] != "cache_hits:":
        raise _cache_error("invalid-cache-evidence-file")

    entries: list[dict[str, object]] = []
    index = 3
    while index < len(lines):
        if not lines[index]:
            index += 1
            continue
        if not lines[index].startswith("  - id: "):
            raise _cache_error("invalid-cache-evidence-file")
        entry: dict[str, object] = {
            "id": _parse_json_scalar(lines[index].split(": ", 1)[1]),
            "command": {"argv": []},
            "displayed_command_argv": [],
            "canonical_cache_argv": [],
            "prior_passing_event": {},
            "cache_key": {},
        }
        index += 1
        list_target: str | None = None
        while index < len(lines) and not lines[index].startswith("  - id: "):
            line = lines[index]
            if not line:
                index += 1
                continue
            if line.startswith("    validator_id: "):
                entry["validator_id"] = _parse_json_scalar(line.split(": ", 1)[1])
            elif line.startswith("    command_family: "):
                entry["command_family"] = _parse_json_scalar(line.split(": ", 1)[1])
            elif line.startswith("    evidence_kind: "):
                entry["evidence_kind"] = line.split(": ", 1)[1]
            elif line == "    displayed_command_argv:":
                list_target = "displayed_command_argv"
            elif line == "    canonical_cache_argv:":
                list_target = "canonical_cache_argv"
            elif line.startswith("      - "):
                if list_target not in {"displayed_command_argv", "canonical_cache_argv"}:
                    raise _cache_error("invalid-cache-evidence-file")
                argv = entry[list_target]
                assert isinstance(argv, list)
                argv.append(_parse_json_scalar(line.split("- ", 1)[1]))
            elif line.startswith("        - "):
                list_target = "command"
                command = entry["command"]
                assert isinstance(command, dict)
                argv = command["argv"]
                assert isinstance(argv, list)
                argv.append(_parse_json_scalar(line.split("- ", 1)[1]))
            elif line.startswith("      stage: "):
                prior = entry["prior_passing_event"]
                assert isinstance(prior, dict)
                prior["stage"] = _parse_json_scalar(line.split(": ", 1)[1])
            elif line.startswith("      evidence: "):
                prior = entry["prior_passing_event"]
                assert isinstance(prior, dict)
                prior["evidence"] = _parse_json_scalar(line.split(": ", 1)[1])
            elif line.startswith("      input_surface_hash: "):
                cache_key = entry["cache_key"]
                assert isinstance(cache_key, dict)
                cache_key["input_surface_hash"] = _parse_json_scalar(line.split(": ", 1)[1])
            elif line.startswith("      validator_implementation_hash: "):
                cache_key = entry["cache_key"]
                assert isinstance(cache_key, dict)
                cache_key["validator_implementation_hash"] = _parse_json_scalar(line.split(": ", 1)[1])
            elif line.startswith("      policy_hash: "):
                cache_key = entry["cache_key"]
                assert isinstance(cache_key, dict)
                cache_key["policy_hash"] = _parse_json_scalar(line.split(": ", 1)[1])
            elif line.startswith("      command_hash: "):
                cache_key = entry["cache_key"]
                assert isinstance(cache_key, dict)
                cache_key["command_hash"] = _parse_json_scalar(line.split(": ", 1)[1])
            elif line.startswith("    result_reused: "):
                entry["result_reused"] = line.split(": ", 1)[1]
            elif line.startswith("    allowed_reason: "):
                entry["allowed_reason"] = line.split(": ", 1)[1]
            elif line.startswith("    scope: "):
                entry["scope"] = line.split(": ", 1)[1]
            elif line.startswith("    closeout_evidence: "):
                entry["closeout_evidence"] = line.split(": ", 1)[1] == "true"
            elif line in (
                "    command:",
                "      argv:",
                "    prior_passing_event:",
                "    cache_key:",
            ):
                if line == "      argv:":
                    list_target = "command"
                elif line != "    command:":
                    list_target = None
                pass
            else:
                raise _cache_error("invalid-cache-evidence-file")
            index += 1
        command = entry["command"]
        if isinstance(command, dict) and isinstance(command.get("argv"), list):
            if not entry.get("displayed_command_argv"):
                entry["displayed_command_argv"] = list(command["argv"])
            if not entry.get("canonical_cache_argv"):
                entry["canonical_cache_argv"] = list(command["argv"])
        entry.setdefault("command_family", _SUPPORTED_COMMAND_FAMILY)
        entry.setdefault("evidence_kind", "cache-hit-inner-loop")
        _validate_cache_hit_entry(entry)
        entries.append(entry)

    ids: set[str] = set()
    for entry in entries:
        entry_id = str(entry["id"])
        if entry_id in ids:
            raise _cache_error("duplicate-cache-hit-id")
        ids.add(entry_id)
    return {"schema_version": 1, "change_id": change_id, "cache_hits": entries}


def _validate_cache_hit_entry(entry: dict[str, object]) -> None:
    required = (
        "id",
        "validator_id",
        "command_family",
        "evidence_kind",
        "displayed_command_argv",
        "canonical_cache_argv",
        "command",
        "prior_passing_event",
        "cache_key",
        "result_reused",
        "allowed_reason",
        "scope",
        "closeout_evidence",
    )
    if any(key not in entry for key in required):
        raise _cache_error("invalid-cache-evidence-file")
    command = entry["command"]
    prior = entry["prior_passing_event"]
    cache_key = entry["cache_key"]
    if not isinstance(command, dict) or not command.get("argv"):
        raise _cache_error("invalid-cache-evidence-file")
    if not entry.get("displayed_command_argv") or not entry.get("canonical_cache_argv"):
        raise _cache_error("invalid-cache-evidence-file")
    if not isinstance(prior, dict) or not prior.get("stage") or not prior.get("evidence"):
        raise _cache_error("invalid-cache-evidence-file")
    if not isinstance(cache_key, dict):
        raise _cache_error("invalid-cache-evidence-file")
    for key in (
        "input_surface_hash",
        "validator_implementation_hash",
        "policy_hash",
        "command_hash",
    ):
        if not cache_key.get(key):
            raise _cache_error("invalid-cache-evidence-file")


def _validate_evidence_ref(reference: str, repo_root: Path) -> None:
    if not reference or "#" not in reference:
        raise _cache_error("invalid-cache-evidence-reference")
    path, anchor = reference.split("#", 1)
    if not anchor:
        raise _cache_error("invalid-cache-evidence-reference")
    relative = normalize_repo_path(path, repo_root)
    if not (repo_root / relative).is_file():
        raise _cache_error("invalid-cache-evidence-reference")


def _yaml_scalar(value: str) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def _parse_json_scalar(value: str) -> str:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise _cache_error("invalid-cache-evidence-file") from exc
    if not isinstance(parsed, str):
        raise _cache_error("invalid-cache-evidence-file")
    return parsed


def _cache_error(code: str) -> CacheIdentityError:
    return CacheIdentityError(code, code)


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


def _require_implementation_file(
    repo_root: Path,
    relative_path: str,
    *,
    missing_code: str,
    unreadable_code: str,
    label: str,
) -> None:
    path = repo_root / relative_path
    if not path.exists():
        raise CacheIdentityError(
            missing_code,
            f"implementation manifest unresolved: {label} is missing: "
            f"{relative_path}; cache eligibility disabled",
        )
    if not path.is_file():
        raise CacheIdentityError(
            unreadable_code,
            f"implementation manifest unresolved: {label} is not a file: "
            f"{relative_path}; cache eligibility disabled",
        )


def _repository_imports(
    repo_root: Path, source: Path, *, is_entrypoint: bool = False
) -> tuple[str, ...]:
    try:
        text = source.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        relative = _repo_relative(repo_root, source)
        code = "implementation-entrypoint-unreadable" if is_entrypoint else "repository-local-helper-unreadable"
        raise CacheIdentityError(
            code,
            f"implementation manifest unresolved: cannot read {relative}: {exc}; "
            "cache eligibility disabled",
        ) from exc
    try:
        tree = ast.parse(text, filename=str(source))
    except SyntaxError as exc:
        relative = _repo_relative(repo_root, source)
        code = "implementation-entrypoint-unparseable" if is_entrypoint else "repository-local-helper-unparseable"
        raise CacheIdentityError(
            code,
            f"implementation manifest unresolved: cannot parse {relative}: {exc}; "
            "cache eligibility disabled",
        ) from exc

    candidates: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                resolved = _resolve_module(repo_root, source, alias.name)
                if not resolved and _is_required_repository_import(alias.name, source, node_level=0):
                    raise _unresolved_import_error(repo_root, source, alias.name)
                candidates.update(resolved)
        elif isinstance(node, ast.ImportFrom):
            if node.level > 0:
                if node.module:
                    module = "." * node.level + node.module
                    resolved = _resolve_module(repo_root, source, module)
                    if not resolved:
                        raise _unresolved_import_error(repo_root, source, module)
                    candidates.update(resolved)
                else:
                    for alias in node.names:
                        module = "." * node.level + alias.name
                        resolved = _resolve_module(repo_root, source, module)
                        if not resolved:
                            raise _unresolved_import_error(repo_root, source, module)
                        candidates.update(resolved)
                    continue
            else:
                module = node.module or ""
                resolved = _resolve_module(repo_root, source, module)
                if not resolved and _is_required_repository_import(module, source, node_level=0):
                    raise _unresolved_import_error(repo_root, source, module)
                candidates.update(resolved)
                if node.module:
                    continue
                for alias in node.names:
                    resolved = _resolve_module(repo_root, source, alias.name)
                    if not resolved and _is_required_repository_import(alias.name, source, node_level=0):
                        raise _unresolved_import_error(repo_root, source, alias.name)
                    candidates.update(resolved)

    return tuple(sorted(candidates))


def _resolve_module(repo_root: Path, source: Path, module_name: str) -> set[str]:
    if not module_name:
        return set()

    level = len(module_name) - len(module_name.lstrip("."))
    cleaned = module_name[level:]
    module_parts = [part for part in cleaned.split(".") if part]
    if not module_parts:
        return set()

    candidate_paths: list[Path] = []
    module_path = Path(*module_parts)
    relative_root = source.parent
    for _ in range(max(level - 1, 0)):
        relative_root = relative_root.parent
    search_roots = [relative_root] if level else [source.parent, repo_root]
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


def _is_required_repository_import(module_name: str, source: Path, *, node_level: int) -> bool:
    del source
    if node_level > 0 or module_name.startswith("."):
        return True
    return module_name == "scripts" or module_name.startswith("scripts.")


def _unresolved_import_error(repo_root: Path, source: Path, module_name: str) -> CacheIdentityError:
    relative_source = _repo_relative(repo_root, source)
    return CacheIdentityError(
        "repository-local-import-unresolved",
        f"implementation manifest unresolved: repository-local import "
        f"'{module_name}' from {relative_source} could not be resolved; "
        "cache eligibility disabled",
    )


def _repo_relative(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except (OSError, ValueError):
        return path.as_posix()


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
