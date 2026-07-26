#!/usr/bin/env python3
"""Standalone hermetic behavior harness for boundary-first proof evidence."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import platform
import re
import secrets
import select
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import tomllib
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from boundary_proof_model import (
    CORE_DIMENSION_IDS,
    BoundaryProofError,
    evaluate_simple_change_trace,
    normalize_feature_model,
    normalize_proof_map,
)


ROOT: Final[Path] = Path(__file__).resolve().parents[1]
CHANGE_ID_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9][a-z0-9-]*$"
)
IDENTITY_PATTERN: Final[re.Pattern[str]] = re.compile(r"^sha256:[0-9a-f]{64}$")
SEMVER_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)
MINIMUM_CODEX_VERSION: Final[str] = "0.138.0"
SUPPORTED_RUNTIME_VERSION: Final[str] = "0.145.0"
PARTICIPATING_SKILLS: Final[tuple[str, ...]] = (
    "workflow",
    "spec",
    "spec-review",
    "test-spec",
    "test-spec-review",
)
RUNTIME_SYSTEM_SKILLS: Final[tuple[str, ...]] = (
    "imagegen",
    "openai-docs",
    "plugin-creator",
    "review-agent",
    "skill-creator",
    "skill-installer",
)
PERMITTED_TOOL_FEATURES: Final[frozenset[str]] = frozenset(
    {"shell_tool", "unified_exec", "shell_snapshot"}
)
PERMITTED_NON_TOOL_FEATURES: Final[frozenset[str]] = frozenset(
    {
        "terminal_resize_reflow",
        "tool_search_always_defer_mcp_tools",
        "resize_all_images",
        "tui_app_server",
    }
)
CODEX_0_144_6_FEATURES: Final[tuple[str, ...]] = (
    "undo",
    "shell_tool",
    "secret_auth_storage",
    "unified_exec",
    "shell_zsh_fork",
    "unified_exec_zsh_fork",
    "shell_snapshot",
    "deferred_executor",
    "js_repl",
    "code_mode",
    "code_mode_host",
    "code_mode_only",
    "js_repl_tools_only",
    "terminal_resize_reflow",
    "web_search_request",
    "web_search_cached",
    "standalone_web_search",
    "search_tool",
    "codex_git_commit",
    "runtime_metrics",
    "sqlite",
    "memories",
    "local_thread_store_compression",
    "chronicle",
    "apply_patch_freeform",
    "apply_patch_streaming_events",
    "exec_permission_approvals",
    "hooks",
    "request_permissions_tool",
    "use_linux_sandbox_bwrap",
    "use_legacy_landlock",
    "request_rule",
    "experimental_windows_sandbox",
    "elevated_windows_sandbox",
    "remote_models",
    "enable_request_compression",
    "network_proxy",
    "respect_system_proxy",
    "multi_agent",
    "multi_agent_v2",
    "multi_agent_mode",
    "enable_fanout",
    "apps",
    "enable_mcp_apps",
    "apps_mcp_path_override",
    "tool_search",
    "tool_search_always_defer_mcp_tools",
    "non_prefixed_mcp_tool_names",
    "unavailable_dummy_tools",
    "tool_suggest",
    "plugins",
    "plugin_hooks",
    "in_app_browser",
    "browser_use",
    "browser_use_full_cdp_access",
    "browser_use_external",
    "computer_use",
    "remote_plugin",
    "plugin_sharing",
    "external_migration",
    "image_generation",
    "resize_all_images",
    "item_ids",
    "concurrent_reasoning_summaries",
    "skill_mcp_dependency_install",
    "skill_env_var_dependency_prompt",
    "mentions_v2",
    "steer",
    "default_mode_request_user_input",
    "terminal_visualization_instructions",
    "guardian_approval",
    "goals",
    "token_budget",
    "rollout_budget",
    "current_time_reminder",
    "collaboration_modes",
    "tool_call_mcp_elicitation",
    "auth_elicitation",
    "personality",
    "artifact",
    "fast_mode",
    "realtime_conversation",
    "remote_control",
    "image_detail_original",
    "tui_app_server",
    "prevent_idle_sleep",
    "workspace_owner_usage_nudge",
    "responses_websockets",
    "responses_websockets_v2",
    "remote_compaction_v2",
    "use_agent_identity",
    "workspace_dependencies",
)
CODEX_0_145_0_FEATURES: Final[tuple[str, ...]] = (
    *CODEX_0_144_6_FEATURES,
    "code_mode_buffered_exec",
    "executor_capability_discovery",
    "external_agent_memory_import",
    "skill_search",
)
RUNTIME_FEATURES_BY_VERSION: Final[dict[str, tuple[str, ...]]] = {
    "0.144.6": CODEX_0_144_6_FEATURES,
    "0.145.0": CODEX_0_145_0_FEATURES,
}
PARENT_PROXY_ENVIRONMENT_NAMES: Final[tuple[str, ...]] = (
    "ALL_PROXY",
    "HTTPS_PROXY",
    "HTTP_PROXY",
    "NO_PROXY",
    "all_proxy",
    "https_proxy",
    "http_proxy",
    "no_proxy",
)
RUNTIME_SCHEMA_IDENTITY_BY_VERSION: Final[dict[str, str]] = {
    "0.145.0": (
        "sha256:18d79891673d9d43a8e7a49864fef49a"
        "04305bd13571a8aef45824209f1bfae8"
    ),
}
RUNTIME_PROTOCOL_CLASSIFICATION_IDENTITY_BY_VERSION: Final[dict[str, str]] = {
    "0.145.0": (
        "sha256:35f1203d9c6abc62ef3f1aca94e2f316"
        "5e0213697d554ab11d0477d9cd7e4bf8"
    ),
}
PREFLIGHT_FIELDS: Final[tuple[str, ...]] = (
    "schema_version",
    "result",
    "diagnostic_id",
    "phase",
    "attestation_ref",
)
ATTESTATION_FIELDS: Final[tuple[str, ...]] = (
    "schema_version",
    "runtime_launcher_identity",
    "runtime_package_identity",
    "schema_bundle_identity",
    "generated_config_identity",
    "managed_requirements_identity",
    "active_permission_profile",
    "thread_metadata",
    "feature_inventory_identity",
    "capability_inventory_identity",
    "skill_inventory_identity",
    "feature_classification_identity",
    "protocol_item_classification_identity",
    "probe_results",
    "credential_isolation_results",
)
DIAGNOSTIC_PHASES: Final[dict[str, frozenset[str]]] = {
    "runtime-unavailable": frozenset({"pre-thread-start"}),
    "runtime-unreadable": frozenset({"pre-thread-start"}),
    "runtime-version-invalid": frozenset({"pre-thread-start"}),
    "runtime-version-unsupported": frozenset({"pre-thread-start"}),
    "runtime-identity-unstable": frozenset(
        {"pre-thread-start", "pre-turn-start", "in-turn"}
    ),
    "schema-bundle-invalid": frozenset({"pre-thread-start"}),
    "experimental-api-unavailable": frozenset({"pre-thread-start"}),
    "protocol-shape-incompatible": frozenset({"pre-thread-start"}),
    "thread-metadata-mismatch": frozenset({"pre-turn-start"}),
    "feature-pagination-invalid": frozenset({"pre-turn-start"}),
    "capability-inventory-mismatch": frozenset({"pre-turn-start"}),
    "skill-inventory-mismatch": frozenset({"pre-turn-start"}),
    "feature-classification-invalid": frozenset({"pre-turn-start"}),
    "protocol-item-classification-invalid": frozenset({"pre-turn-start"}),
    "permission-profile-mismatch": frozenset({"pre-turn-start"}),
    "config-equivalence-mismatch": frozenset({"pre-turn-start"}),
    "sandbox-probe-failed": frozenset({"pre-turn-start"}),
    "credential-isolation-failed": frozenset({"pre-turn-start"}),
    "unexpected-prohibited-event": frozenset({"in-turn"}),
}
CONTRACT_PATHS: Final[tuple[str, ...]] = (
    "docs/workflows.md",
    "specs/rigorloop-workflow.md",
    "specs/rigorloop-workflow.test.md",
    "specs/skill-contract.md",
    "specs/skill-contract.test.md",
)
MANIFEST_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "manifest_id",
        "harness_component_refs",
        "skill_package_refs",
        "instruction_refs",
        "contract_refs",
        "invocation_profile",
        "runtime_attestation",
    }
)
INVOCATION_PROFILE_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "agent_runtime",
        "runtime_version",
        "runtime_executable_identity",
        "model_id",
        "orchestration_mode",
        "instruction_profile",
        "tool_profile",
        "python_implementation",
        "python_version",
    }
)


class BoundaryRuntimeError(RuntimeError):
    """A closed, non-secret preflight failure."""

    def __init__(self, diagnostic_id: str, phase: str | None = None) -> None:
        phases = DIAGNOSTIC_PHASES.get(diagnostic_id)
        if phases is None:
            raise ValueError(f"unknown preflight diagnostic: {diagnostic_id}")
        selected = phase or sorted(phases)[0]
        if selected not in phases:
            raise ValueError(
                f"diagnostic {diagnostic_id} is not valid in phase {selected}"
            )
        self.diagnostic_id = diagnostic_id
        self.phase = selected
        super().__init__(f"{diagnostic_id} ({selected})")


@dataclass(frozen=True)
class _SemVer:
    major: int
    minor: int
    patch: int
    prerelease: tuple[tuple[int, int | str], ...]

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, _SemVer):
            return NotImplemented
        core = (self.major, self.minor, self.patch)
        other_core = (other.major, other.minor, other.patch)
        if core != other_core:
            return core < other_core
        if not self.prerelease:
            return False
        if not other.prerelease:
            return True
        for left, right in zip(self.prerelease, other.prerelease, strict=False):
            if left == right:
                continue
            if left[0] != right[0]:
                return left[0] < right[0]
            return left[1] < right[1]
        return len(self.prerelease) < len(other.prerelease)

    def __le__(self, other: object) -> bool:
        if not isinstance(other, _SemVer):
            return NotImplemented
        return self == other or self < other

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, _SemVer):
            return NotImplemented
        return not self <= other


@dataclass(frozen=True)
class _FileIdentity:
    device: int
    inode: int
    size: int
    modified_ns: int
    changed_ns: int
    digest: str


def _parse_semver(value: str) -> _SemVer:
    match = SEMVER_PATTERN.fullmatch(value)
    if match is None:
        raise BoundaryRuntimeError("runtime-version-invalid")
    prerelease: list[tuple[int, int | str]] = []
    for identifier in (match.group(4) or "").split("."):
        if not identifier:
            continue
        if identifier.isdigit():
            if len(identifier) > 1 and identifier.startswith("0"):
                raise BoundaryRuntimeError("runtime-version-invalid")
            prerelease.append((0, int(identifier)))
        else:
            prerelease.append((1, identifier))
    return _SemVer(
        int(match.group(1)),
        int(match.group(2)),
        int(match.group(3)),
        tuple(prerelease),
    )


def _canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _sha256(raw: bytes) -> str:
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def _preflight_failure(
    diagnostic_id: str, phase: str | None = None
) -> dict[str, object]:
    error = BoundaryRuntimeError(diagnostic_id, phase)
    return {
        "schema_version": "boundary-runtime-preflight-v1",
        "result": "environment-unavailable",
        "diagnostic_id": error.diagnostic_id,
        "phase": error.phase,
        "attestation_ref": None,
    }


def _select_change_root(repo_root: Path, change_id: str) -> Path:
    if CHANGE_ID_PATTERN.fullmatch(change_id) is None:
        raise BoundaryRuntimeError("runtime-unavailable")
    changes_root = repo_root / "docs" / "changes"
    change_root = changes_root / change_id
    try:
        changes_stat = changes_root.lstat()
        change_stat = change_root.lstat()
    except OSError as error:
        raise BoundaryRuntimeError("runtime-unavailable") from error
    if (
        stat.S_ISLNK(changes_stat.st_mode)
        or not stat.S_ISDIR(changes_stat.st_mode)
        or stat.S_ISLNK(change_stat.st_mode)
        or not stat.S_ISDIR(change_stat.st_mode)
        or change_root.name != change_id
    ):
        raise BoundaryRuntimeError("runtime-unavailable")
    return change_root


def _repository_head(repo_root: Path) -> str:
    completed = subprocess.run(
        ("git", "-C", str(repo_root), "rev-parse", "HEAD"),
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    value = completed.stdout.strip()
    if completed.returncode != 0 or re.fullmatch(r"[0-9a-f]{40}", value) is None:
        raise BoundaryRuntimeError("runtime-unavailable")
    return value


def _require_clean_worktree(repo_root: Path) -> None:
    completed = subprocess.run(
        (
            "git",
            "-C",
            str(repo_root),
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
        ),
        check=False,
        capture_output=True,
        text=True,
        timeout=20,
    )
    if completed.returncode != 0 or completed.stdout:
        raise BoundaryRuntimeError("runtime-identity-unstable")


def _selected_repository_path(path: str, change_id: str) -> bool:
    prefixes = (
        "specs/",
        "docs/proposals/",
        "docs/plans/",
        "docs/architecture/",
        "docs/adr/",
        f"docs/changes/{change_id}/",
    )
    if not path.startswith(prefixes):
        return False
    simple_prefix = f"docs/changes/{change_id}/evidence/simple-change/"
    return not (
        path.startswith(simple_prefix + "runs/")
        or path == simple_prefix + "current.json"
        or path == simple_prefix + "prepared.json"
        or "/.prepared-" in path
    )


def _artifact_kind(path: str, change_id: str) -> str:
    change_prefix = f"docs/changes/{change_id}/"
    if path.startswith("specs/") and path.endswith(".test.md"):
        return "test-spec"
    if (
        path.startswith("specs/")
        and path.endswith(".md")
        and not path.endswith(".test.md")
    ):
        return "feature-spec"
    if path.startswith(change_prefix) and (
        path == change_prefix + "review-log.md"
        or path == change_prefix + "review-resolution.md"
        or (
            path.startswith(change_prefix + "reviews/")
            and path.endswith(".md")
        )
    ):
        return "review-evidence"
    if (
        path.startswith("docs/proposals/")
        or path.startswith("docs/plans/")
        or path.startswith("docs/architecture/")
        or path.startswith("docs/adr/")
        or path == change_prefix + "change.yaml"
    ):
        return "other-lifecycle"
    return "non-lifecycle"


def _inventory_from_commit(
    repo_root: Path, change_id: str, commit: str
) -> list[dict[str, str]]:
    listed = subprocess.run(
        ("git", "-C", str(repo_root), "ls-tree", "-r", "-z", "--name-only", commit),
        check=False,
        capture_output=True,
        timeout=30,
    )
    if listed.returncode != 0:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    paths = [
        raw.decode("utf-8")
        for raw in listed.stdout.split(b"\0")
        if raw and _selected_repository_path(raw.decode("utf-8"), change_id)
    ]
    rows: list[dict[str, str]] = []
    for path in sorted(paths):
        shown = subprocess.run(
            ("git", "-C", str(repo_root), "show", f"{commit}:{path}"),
            check=False,
            capture_output=True,
            timeout=30,
        )
        if shown.returncode != 0:
            raise BoundaryRuntimeError("runtime-identity-unstable")
        rows.append(
            {
                "path": path,
                "artifact_kind": _artifact_kind(path, change_id),
                "identity": _sha256(shown.stdout),
            }
        )
    return rows


def _inventory_from_worktree(
    repo_root: Path, change_id: str
) -> list[dict[str, str]]:
    roots = (
        repo_root / "specs",
        repo_root / "docs" / "proposals",
        repo_root / "docs" / "plans",
        repo_root / "docs" / "architecture",
        repo_root / "docs" / "adr",
        repo_root / "docs" / "changes" / change_id,
    )
    rows: list[dict[str, str]] = []
    paths: set[str] = set()
    for root in roots:
        for path in root.rglob("*"):
            relative = path.relative_to(repo_root).as_posix()
            if not _selected_repository_path(relative, change_id):
                continue
            try:
                metadata = path.lstat()
            except OSError as error:
                raise BoundaryRuntimeError("runtime-identity-unstable") from error
            if stat.S_ISLNK(metadata.st_mode):
                raise BoundaryRuntimeError("runtime-identity-unstable")
            if not stat.S_ISREG(metadata.st_mode):
                continue
            if relative in paths:
                raise BoundaryRuntimeError("runtime-identity-unstable")
            paths.add(relative)
            rows.append(
                {
                    "path": relative,
                    "artifact_kind": _artifact_kind(relative, change_id),
                    "identity": _read_file_identity(path).digest,
                }
            )
    return sorted(rows, key=lambda row: row["path"])


def _derive_config_origin_paths(raw_config: bytes) -> set[tuple[str, ...]]:
    """Return complete TOML leaf paths without splitting decoded quoted keys."""

    try:
        generated = tomllib.loads(raw_config.decode("utf-8"))
    except (UnicodeError, tomllib.TOMLDecodeError) as error:
        raise BoundaryRuntimeError(
            "config-equivalence-mismatch", "pre-turn-start"
        ) from error
    paths: set[tuple[str, ...]] = set()

    def collect(value: object, path: tuple[str, ...] = ()) -> None:
        if isinstance(value, dict):
            for key, nested in value.items():
                collect(nested, (*path, key))
            return
        if isinstance(value, list):
            for index, nested in enumerate(value):
                collect(nested, (*path, str(index)))
            return
        if not path or path in paths:
            raise BoundaryRuntimeError(
                "config-equivalence-mismatch", "pre-turn-start"
            )
        paths.add(path)

    collect(generated)
    if not paths:
        raise BoundaryRuntimeError("config-equivalence-mismatch", "pre-turn-start")
    return paths


def _origin_key(path: tuple[str, ...]) -> str:
    return ".".join(path)


def _atomic_write(path: Path, raw: bytes, *, mode: int = 0o600) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "wb", closefd=True) as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    except OSError:
        temporary.unlink(missing_ok=True)
        raise


def _regular_reference(repo_root: Path, path: Path) -> dict[str, str]:
    """Return one current, non-symlink repository reference."""

    try:
        relative = path.relative_to(repo_root)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError
        cursor = repo_root
        for part in relative.parts:
            cursor = cursor / part
            metadata = cursor.lstat()
            if stat.S_ISLNK(metadata.st_mode):
                raise ValueError
        if not stat.S_ISREG(path.lstat().st_mode):
            raise ValueError
        raw = path.read_bytes()
    except (OSError, ValueError) as error:
        raise BoundaryRuntimeError("runtime-unreadable") from error
    return {"path": relative.as_posix(), "identity": _sha256(raw)}


def _validate_reference(repo_root: Path, reference: object) -> Path:
    if not isinstance(reference, dict) or set(reference) != {"path", "identity"}:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    raw_path = reference.get("path")
    identity = reference.get("identity")
    if (
        not isinstance(raw_path, str)
        or not isinstance(identity, str)
        or IDENTITY_PATTERN.fullmatch(identity) is None
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    path = repo_root / raw_path
    current = _regular_reference(repo_root, path)
    if current != reference:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    return path


def _resource_paths(repo_root: Path, skill: str) -> list[Path]:
    skill_root = repo_root / "skills" / skill
    skill_file = skill_root / "SKILL.md"
    try:
        lines = skill_file.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        raise BoundaryRuntimeError("runtime-unreadable") from error
    resources: list[Path] = [skill_file]
    in_map = False
    for line in lines:
        if line == "## Resource map":
            in_map = True
            continue
        if in_map and line.startswith("## "):
            break
        if not in_map:
            continue
        match = re.search(r"`(references/[A-Za-z0-9._/-]+)`", line)
        if match is not None:
            resources.append(skill_root / match.group(1))
    unique = {path.relative_to(repo_root).as_posix(): path for path in resources}
    return [unique[key] for key in sorted(unique)]


def _applicable_instruction_paths(
    repo_root: Path, governed_paths: Sequence[Path]
) -> list[Path]:
    selected: dict[str, Path] = {}
    constitution = repo_root / "CONSTITUTION.md"
    if constitution.exists():
        selected["CONSTITUTION.md"] = constitution
    for governed in governed_paths:
        try:
            relative_parent = governed.relative_to(repo_root).parent
        except ValueError as error:
            raise BoundaryRuntimeError("runtime-unreadable") from error
        cursor = repo_root
        root_agents = cursor / "AGENTS.md"
        if root_agents.exists():
            selected["AGENTS.md"] = root_agents
        for part in relative_parent.parts:
            cursor = cursor / part
            candidate = cursor / "AGENTS.md"
            if candidate.exists():
                selected[candidate.relative_to(repo_root).as_posix()] = candidate
    return [selected[key] for key in sorted(selected)]


def _assert_standalone_import_policy(repo_root: Path) -> None:
    allowed_local = {"boundary_proof_model"}
    standard = set(getattr(sys, "stdlib_module_names", ()))
    for relative in (
        "scripts/boundary_proof_behavior.py",
        "scripts/boundary_proof_model.py",
    ):
        path = repo_root / relative
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=relative)
        except (OSError, UnicodeError, SyntaxError) as error:
            raise BoundaryRuntimeError("runtime-unreadable") from error
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.level or node.module is None or any(
                    alias.name == "*" for alias in node.names
                ):
                    raise BoundaryRuntimeError("runtime-unreadable")
                root = node.module.partition(".")[0]
                if root not in standard and not (
                    relative.endswith("boundary_proof_behavior.py")
                    and root in allowed_local
                ):
                    raise BoundaryRuntimeError("runtime-unreadable")
            elif isinstance(node, ast.Import):
                if any(alias.name.partition(".")[0] not in standard for alias in node.names):
                    raise BoundaryRuntimeError("runtime-unreadable")
            elif isinstance(node, ast.Call):
                name = node.func.id if isinstance(node.func, ast.Name) else None
                if name in {"eval", "exec", "__import__"}:
                    raise BoundaryRuntimeError("runtime-unreadable")


def _build_behavior_manifest(
    repo_root: Path,
    attestation: Mapping[str, object],
) -> dict[str, object]:
    _assert_standalone_import_policy(repo_root)
    _validate_attestation(attestation)
    harness_paths = [
        repo_root / "scripts" / "boundary_proof_behavior.py",
        repo_root / "scripts" / "boundary_proof_model.py",
    ]
    skill_paths = [
        path
        for skill in PARTICIPATING_SKILLS
        for path in _resource_paths(repo_root, skill)
    ]
    scenario_paths = [
        repo_root / "tests" / "fixtures" / "boundary-proof" / "simple-change"
    ]
    instruction_paths = _applicable_instruction_paths(
        repo_root, [*skill_paths, *scenario_paths, *harness_paths]
    )
    thread = attestation["thread_metadata"]
    if not isinstance(thread, dict):
        raise BoundaryRuntimeError("thread-metadata-mismatch", "pre-turn-start")
    profile = {
        "agent_runtime": "codex",
        "runtime_version": thread["cli_version"],
        "runtime_executable_identity": attestation[
            "runtime_launcher_identity"
        ],
        "model_id": thread["model_id"],
        "orchestration_mode": "workflow-auto-isolated-v1",
        "instruction_profile": "repository-instructions-plus-runtime-default-v1",
        "tool_profile": "isolated-workspace-no-network-v1",
        "python_implementation": platform.python_implementation().lower(),
        "python_version": platform.python_version(),
    }
    skill_references = [
        _regular_reference(repo_root, path) for path in skill_paths
    ]
    skill_references.sort(key=lambda row: row["path"])
    return {
        "manifest_id": "boundary-behavior-implementation-v1",
        "harness_component_refs": [
            _regular_reference(repo_root, path) for path in sorted(harness_paths)
        ],
        "skill_package_refs": skill_references,
        "instruction_refs": [
            _regular_reference(repo_root, path) for path in instruction_paths
        ],
        "contract_refs": [
            _regular_reference(repo_root, repo_root / path)
            for path in CONTRACT_PATHS
        ],
        "invocation_profile": profile,
        "runtime_attestation": dict(attestation),
    }


def _validate_behavior_manifest(
    repo_root: Path, manifest: Mapping[str, object]
) -> None:
    if set(manifest) != MANIFEST_FIELDS:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    if manifest.get("manifest_id") != "boundary-behavior-implementation-v1":
        raise BoundaryRuntimeError("runtime-identity-unstable")
    _assert_standalone_import_policy(repo_root)
    for field in (
        "harness_component_refs",
        "skill_package_refs",
        "instruction_refs",
        "contract_refs",
    ):
        rows = manifest.get(field)
        if not isinstance(rows, list) or rows != sorted(
            rows, key=lambda row: row.get("path", "") if isinstance(row, dict) else ""
        ):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        paths = []
        for row in rows:
            paths.append(_validate_reference(repo_root, row))
        if len(paths) != len(set(paths)):
            raise BoundaryRuntimeError("runtime-identity-unstable")
    expected_harness = [
        _regular_reference(repo_root, repo_root / path)
        for path in (
            "scripts/boundary_proof_behavior.py",
            "scripts/boundary_proof_model.py",
        )
    ]
    if manifest["harness_component_refs"] != expected_harness:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    expected_skills = [
        _regular_reference(repo_root, path)
        for skill in PARTICIPATING_SKILLS
        for path in _resource_paths(repo_root, skill)
    ]
    expected_skills.sort(key=lambda row: row["path"])
    if manifest["skill_package_refs"] != expected_skills:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    expected_contracts = [
        _regular_reference(repo_root, repo_root / path) for path in CONTRACT_PATHS
    ]
    if manifest["contract_refs"] != expected_contracts:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    governed_paths = [
        repo_root / str(row["path"])
        for field in ("harness_component_refs", "skill_package_refs")
        for row in manifest[field]
    ]
    governed_paths.append(
        repo_root / "tests" / "fixtures" / "boundary-proof" / "simple-change"
    )
    expected_instructions = [
        _regular_reference(repo_root, path)
        for path in _applicable_instruction_paths(repo_root, governed_paths)
    ]
    if manifest["instruction_refs"] != expected_instructions:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    profile = manifest.get("invocation_profile")
    if not isinstance(profile, dict) or set(profile) != INVOCATION_PROFILE_FIELDS:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    attestation = manifest.get("runtime_attestation")
    if not isinstance(attestation, dict):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    _validate_attestation(attestation)
    thread = attestation["thread_metadata"]
    if (
        profile["agent_runtime"] != "codex"
        or profile["runtime_version"] != thread["cli_version"]
        or profile["runtime_executable_identity"]
        != attestation["runtime_launcher_identity"]
        or profile["model_id"] != thread["model_id"]
        or profile["orchestration_mode"] != "workflow-auto-isolated-v1"
        or profile["instruction_profile"]
        != "repository-instructions-plus-runtime-default-v1"
        or profile["tool_profile"] != "isolated-workspace-no-network-v1"
        or profile["python_implementation"]
        != platform.python_implementation().lower()
        or profile["python_version"] != platform.python_version()
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")


def _split_cells(line: str) -> list[str]:
    if not line.startswith("|") or not line.endswith("|"):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    return [cell.strip() for cell in line[1:-1].split("|")]


def _table_after(lines: list[str], heading: str) -> tuple[list[str], list[list[str]]]:
    try:
        start = lines.index(heading) + 1
    except ValueError as error:
        raise BoundaryRuntimeError("runtime-identity-unstable") from error
    while start < len(lines) and not lines[start].startswith("|"):
        start += 1
    if start + 1 >= len(lines):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    header = _split_cells(lines[start])
    separator = _split_cells(lines[start + 1])
    if len(separator) != len(header) or any(
        re.fullmatch(r":?-{3,}:?", cell) is None for cell in separator
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    rows: list[list[str]] = []
    for line in lines[start + 2 :]:
        if not line.startswith("|"):
            break
        row = _split_cells(line)
        if len(row) != len(header):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        rows.append(row)
    return header, rows


def _csv(value: str) -> list[str]:
    return [] if value == "-" else [item.strip() for item in value.split(",")]


def _parse_feature_markdown(raw: str) -> dict[str, object]:
    lines = raw.splitlines()
    version_rows = [
        line.partition(":")[2].strip()
        for line in lines
        if line.startswith("Boundary model version:")
    ]
    scope_rows = [
        line.partition(":")[2].strip()
        for line in lines
        if line.startswith("Boundary model scope:")
    ]
    requirement_ids = sorted(
        {
            match.group(1)
            for line in lines
            if (match := re.match(r"^(R[0-9]+[a-z]*)\.", line)) is not None
        }
    )
    if len(version_rows) != 1 or len(scope_rows) != 1 or not requirement_ids:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    header, rows = _table_after(lines, "## Boundary model")
    if header != [
        "Dimension ID",
        "Applicability",
        "Governing requirement IDs",
        "Boundary IDs",
        "Non-applicability rationale",
    ]:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    core = [
        {
            "dimension_id": row[0],
            "applicability": row[1],
            "governing_requirement_ids": _csv(row[2]),
            "boundary_ids": _csv(row[3]),
            "non_applicability_rationale": None if row[4] == "-" else row[4],
        }
        for row in rows
    ]
    example_header, example_rows = _table_after(lines, "## Examples")
    if example_header != [
        "Example ID",
        "Role",
        "Governing requirement IDs",
        "Boundary IDs",
        "Regression ID",
        "Discovery gap",
    ]:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    examples = [
        {
            "example_id": row[0],
            "role": row[1],
            "governing_requirement_ids": _csv(row[2]),
            "boundary_ids": _csv(row[3]),
            "regression_id": None if row[4] == "-" else row[4],
            "discovery_gap": None if row[5] == "-" else row[5],
            "non_normative_purpose": None,
        }
        for row in example_rows
    ]
    interactions: list[dict[str, object]] = []
    if any(line == "| Interaction ID | Boundary IDs | Rationale | Governing requirement IDs |" for line in lines):
        interaction_header, interaction_rows = _table_after(lines, "## Interactions")
        if interaction_header != [
            "Interaction ID",
            "Boundary IDs",
            "Rationale",
            "Governing requirement IDs",
        ]:
            raise BoundaryRuntimeError("runtime-identity-unstable")
        interactions = [
            {
                "interaction_id": row[0],
                "boundary_ids": _csv(row[1]),
                "rationale": row[2],
                "governing_requirement_ids": _csv(row[3]),
            }
            for row in interaction_rows
        ]
    return {
        "boundary_model_version": version_rows[0],
        "boundary_model_scope": scope_rows[0],
        "core_dimensions": core,
        "extensions": [],
        "examples": examples,
        "interactions": interactions,
    }


def _parse_test_spec_markdown(raw: str) -> dict[str, object]:
    lines = raw.splitlines()
    versions = [
        line.partition(":")[2].strip()
        for line in lines
        if line.startswith("Boundary model version:")
    ]
    scopes = [
        line.partition(":")[2].strip()
        for line in lines
        if line.startswith("Boundary model scope:")
    ]
    header, rows = _table_after(lines, "## Proof map")
    if header != [
        "Proof obligation ID",
        "Governing requirement IDs",
        "Boundary or interaction IDs",
        "Test case IDs",
        "Automation level",
        "Manual procedure IDs",
    ]:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    tests = sorted(
        {
            match.group(1)
            for line in lines
            if (match := re.match(r"^(T[0-9]+)\.", line)) is not None
        }
    )
    if len(versions) != 1 or len(scopes) != 1 or not tests:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    return {
        "boundary_model_version": versions[0],
        "boundary_model_scope": scopes[0],
        "proof_obligations": [
            {
                "proof_obligation_id": row[0],
                "governing_requirement_ids": _csv(row[1]),
                "boundary_or_interaction_ids": _csv(row[2]),
                "test_case_ids": _csv(row[3]),
                "automation_level": row[4],
                "manual_procedure_ids": _csv(row[5]),
            }
            for row in rows
        ],
    }


def _feature_record(model: object) -> dict[str, object]:
    return {
        "boundary_model_version": model.boundary_model_version,
        "boundary_model_scope": model.boundary_model_scope,
        "requirement_ids": sorted(
            {
                value
                for row in (*model.core_dimensions, *model.extensions)
                for value in row.governing_requirement_ids
            }
        ),
        "core_rows": sorted([
            {
                "dimension_id": row.dimension_id,
                "applicability": row.applicability,
                "governing_requirement_ids": list(row.governing_requirement_ids),
                "boundary_ids": list(row.boundary_ids),
                "non_applicability_rationale": row.non_applicability_rationale,
            }
            for row in model.core_dimensions
        ], key=lambda row: row["dimension_id"]),
        "extension_rows": [],
        "example_rows": sorted([
            {
                "example_id": row.example_id,
                "role": row.role,
                "governing_requirement_ids": list(row.governing_requirement_ids),
                "boundary_ids": list(row.boundary_ids),
                "regression_id": row.regression_id,
                "discovery_gap": row.discovery_gap,
                "non_normative_purpose": row.non_normative_purpose,
            }
            for row in model.examples
        ], key=lambda row: row["example_id"]),
        "interaction_rows": sorted([
            {
                "interaction_id": row.interaction_id,
                "boundary_ids": list(row.boundary_ids),
                "rationale": row.rationale,
                "governing_requirement_ids": list(row.governing_requirement_ids),
            }
            for row in model.interactions
        ], key=lambda row: row["interaction_id"]),
    }


def _proof_record(proof: object) -> dict[str, object]:
    return {
        "boundary_model_version": proof.boundary_model_version,
        "boundary_model_scope": proof.boundary_model_scope,
        "proof_rows": sorted([
            {
                "proof_obligation_id": row.proof_obligation_id,
                "governing_requirement_ids": list(row.governing_requirement_ids),
                "boundary_or_interaction_ids": list(
                    row.boundary_or_interaction_ids
                ),
                "test_case_ids": list(row.test_case_ids),
                "automation_level": row.automation_level,
                "manual_procedure_ids": list(row.manual_procedure_ids),
            }
            for row in proof.proof_obligations
        ], key=lambda row: row["proof_obligation_id"]),
        "test_case_ids": sorted(
            {
                test
                for row in proof.proof_obligations
                for test in row.test_case_ids
            }
        ),
    }


def _closed_object_schema(properties: Mapping[str, object]) -> dict[str, object]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": list(properties),
        "properties": dict(properties),
    }


def _route_request(request: str) -> dict[str, object]:
    return {
        "skill_names": ["workflow"],
        "stage": "workflow",
        "prompt": (
            "Use the installed workflow skill to route this bounded request. "
            "Do not author lifecycle artifacts and do not use tools. Return "
            "the exact ordered stage route only.\n\nRequest:\n" + request
        ),
        "output_schema": _closed_object_schema(
            {
                "stages": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "spec",
                            "spec-review",
                            "test-spec",
                            "test-spec-review",
                        ],
                    },
                    "minItems": 4,
                    "maxItems": 4,
                }
            }
        ),
    }


def _spec_request(request: str) -> dict[str, object]:
    return {
        "skill_names": ["spec"],
        "stage": "spec",
        "prompt": (
            "Use the installed spec skill to author the complete feature spec "
            "for the request below. Do not use tools or repository files. The "
            "Markdown itself is the stage-owned artifact. It must include "
            "Status, R1-R4 requirements, Boundary model version/scope, all "
            "twelve closed core-dimension rows with explicit applicability or "
            "non-applicability, governed examples, interactions, and "
            "acceptance criteria. Use the stable applicable mappings "
            "`canonical-trust` -> R1 / `text.canonical.requirements`; "
            "`closed-vocabulary` -> R1,R4 / `text.mode.valid`,"
            "`text.mode.unknown`; `outcome-stop` -> R2,R3,R4 / "
            "`text.outcome.value`,`text.outcome.error`; and "
            "`evidence-claims` -> R1,R2,R3,R4 / `text.evidence.tests`. "
            "The other eight core dimensions are not applicable with these "
            "exact rationales respectively: `No persisted identity is consumed.`, "
            "`The function is stateless.`, `The function grants no authority.`, "
            "`The function performs no mutation.`, `The operation is not "
            "interruptible.`, `The pure result has no shared state.`, `One "
            "public function owns the behavior.`, and `No legacy representation "
            "exists.` Include governed trim/preserve illustrations and the "
            "`text.regression.unknown-mode` regression. Return the artifact, "
            "not a profile label.\n\n"
            "Request:\n" + request
        ),
        "output_schema": _closed_object_schema(
            {"artifact_markdown": {"type": "string", "minLength": 500}}
        ),
    }


def _review_request(
    stage: str, artifact_markdown: str, artifact_identity: str
) -> dict[str, object]:
    if stage not in {"spec-review", "test-spec-review"}:
        raise BoundaryRuntimeError("protocol-shape-incompatible", "pre-turn-start")
    return {
        "skill_names": [stage],
        "stage": stage,
        "prompt": (
            f"Use the installed {stage} skill as an independent formal reviewer. "
            "Do not use tools or repository files. Review the exact artifact "
            f"whose raw UTF-8 identity is {artifact_identity}. Return a durable "
            "formal review record and review-log entry, not a label-only answer. "
            "The record must contain Review ID, Stage, Status, Reviewed artifact "
            "identity, Material findings, Recording status, evidence, and a "
            "review result. When approved, include the exact lines "
            "`Status: approved`, `Reviewed artifact identity: <the identity "
            "above>`, `Material findings: none`, and `Recording status: recorded` "
            "in the record, and all except Recording status in the log. "
            "Approve only if the artifact exhaustively models "
            "the applicable boundaries and explicit non-applicability.\n\n"
            "Artifact:\n" + artifact_markdown
        ),
        "output_schema": _closed_object_schema(
            {
                "review_id": {
                    "type": "string",
                    "pattern": rf"^{stage}-r[1-9][0-9]*$",
                },
                "outcome": {
                    "type": "string",
                    "enum": ["approved", "changes-requested", "blocked"],
                },
                "review_record_markdown": {"type": "string", "minLength": 200},
                "review_log_markdown": {"type": "string", "minLength": 100},
            }
        ),
    }


def _test_spec_request(
    request: str, feature_markdown: str, review_record: str
) -> dict[str, object]:
    return {
        "skill_names": ["test-spec"],
        "stage": "test-spec",
        "prompt": (
            "Use the installed test-spec skill to author the complete proof map "
            "for the approved feature spec below. Do not use tools or repository "
            "files. The Markdown itself is the stage-owned artifact. Map every "
            "applicable boundary to concrete tests and do not create obligations "
            "for explicitly non-applicable dimensions. Include Boundary model "
            "version/scope, proof obligations, and T1-T3 test cases. Use the "
            "stable proof IDs `text.proof.canonical`, `text.proof.mode`, "
            "`text.proof.outcome`, and `text.proof.evidence`; map them to the "
            "exact applicable boundary IDs in the feature spec and automated "
            "T1-T3 cases. T1 covers trim plus canonical/mode/outcome/evidence; "
            "T2 covers every unknown mode plus canonical/mode/outcome/evidence; "
            "T3 covers preserve plus outcome/evidence. Return the artifact, not "
            "a profile label.\n\nRequest:\n"
            + request
            + "\n\nApproved feature spec:\n"
            + feature_markdown
            + "\n\nIndependent review evidence:\n"
            + review_record
        ),
        "output_schema": _closed_object_schema(
            {"artifact_markdown": {"type": "string", "minLength": 400}}
        ),
    }


def _scenario(repo_root: Path, scenario_path: Path) -> dict[str, object]:
    try:
        record = json.loads(scenario_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise BoundaryRuntimeError("runtime-identity-unstable") from error
    expected = {
        "scenario_id",
        "request",
        "expected_branch",
        "corrected_role",
    }
    if (
        not isinstance(record, dict)
        or set(record) != expected
        or record.get("scenario_id") != "BFP-SIMPLE-001"
        or not isinstance(record.get("request"), str)
        or not record["request"].strip()
        or record.get("expected_branch") not in {
            "zero-correction",
            "one-correction",
        }
        or (
            record.get("corrected_role") is not None
            and record.get("corrected_role") not in {"feature-spec", "test-spec"}
        )
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    if (
        record["expected_branch"] == "zero-correction"
    ) != (record["corrected_role"] is None):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    _regular_reference(repo_root, scenario_path)
    return record


def _load_generated_payload(
    result: Mapping[str, object], expected_fields: set[str]
) -> dict[str, object]:
    message = result.get("agent_message")
    if not isinstance(message, str):
        raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
    try:
        payload = json.loads(message)
    except json.JSONDecodeError as error:
        raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn") from error
    if not isinstance(payload, dict) or set(payload) != expected_fields:
        raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
    return payload


def _validate_review_payload(
    payload: Mapping[str, object],
    *,
    stage: str,
    artifact_identity: str,
) -> None:
    review_id = payload.get("review_id")
    outcome = payload.get("outcome")
    record = payload.get("review_record_markdown")
    log = payload.get("review_log_markdown")
    if (
        not isinstance(review_id, str)
        or re.fullmatch(rf"{re.escape(stage)}-r[1-9][0-9]*", review_id) is None
        or outcome != "approved"
        or not isinstance(record, str)
        or not isinstance(log, str)
    ):
        raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
    record_required = (
        f"Review ID: {review_id}",
        f"Stage: {stage}",
        "Status: approved",
        f"Reviewed artifact identity: {artifact_identity}",
        "Material findings: none",
        "Recording status: recorded",
    )
    log_required = (
        f"Review ID: {review_id}",
        f"Stage: {stage}",
        "Status: approved",
        f"Reviewed artifact identity: {artifact_identity}",
        "Material findings: none",
    )
    if any(value not in record for value in record_required) or any(
        value not in log for value in log_required
    ):
        raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")


def _portable_text_contract() -> tuple[dict[str, object], dict[str, object]]:
    applicable = {
        "canonical-trust": (
            ["R1"],
            ["text.canonical.requirements"],
        ),
        "closed-vocabulary": (
            ["R1", "R4"],
            ["text.mode.valid", "text.mode.unknown"],
        ),
        "outcome-stop": (
            ["R2", "R3", "R4"],
            ["text.outcome.value", "text.outcome.error"],
        ),
        "evidence-claims": (
            ["R1", "R2", "R3", "R4"],
            ["text.evidence.tests"],
        ),
    }
    rationales = {
        "identity-freshness": "No persisted identity is consumed.",
        "state-transition": "The function is stateless.",
        "authorization-scope": "The function grants no authority.",
        "mutation-atomicity": "The function performs no mutation.",
        "interruption-recovery": "The operation is not interruptible.",
        "concurrency-idempotency": "The pure result has no shared state.",
        "composition-bypass": "One public function owns the behavior.",
        "compatibility-migration": "No legacy representation exists.",
    }
    core = []
    for dimension_id in CORE_DIMENSION_IDS:
        if dimension_id in applicable:
            requirements, boundaries = applicable[dimension_id]
            core.append(
                {
                    "dimension_id": dimension_id,
                    "applicability": "applicable",
                    "governing_requirement_ids": requirements,
                    "boundary_ids": boundaries,
                    "non_applicability_rationale": None,
                }
            )
        else:
            core.append(
                {
                    "dimension_id": dimension_id,
                    "applicability": "not-applicable",
                    "governing_requirement_ids": [],
                    "boundary_ids": [],
                    "non_applicability_rationale": rationales[dimension_id],
                }
            )
    feature = {
        "boundary_model_version": "v1",
        "boundary_model_scope": "R1-R4",
        "core_dimensions": core,
        "extensions": [],
        "examples": [
            {
                "example_id": "text.example.trim",
                "role": "illustration",
                "governing_requirement_ids": ["R1", "R2"],
                "boundary_ids": ["text.mode.valid", "text.outcome.value"],
                "regression_id": None,
                "discovery_gap": None,
                "non_normative_purpose": None,
            },
            {
                "example_id": "text.example.preserve",
                "role": "illustration",
                "governing_requirement_ids": ["R1", "R3"],
                "boundary_ids": ["text.mode.valid", "text.outcome.value"],
                "regression_id": None,
                "discovery_gap": None,
                "non_normative_purpose": None,
            },
            {
                "example_id": "text.example.unknown",
                "role": "regression",
                "governing_requirement_ids": ["R1", "R4"],
                "boundary_ids": ["text.mode.unknown", "text.outcome.error"],
                "regression_id": "text.regression.unknown-mode",
                "discovery_gap": None,
                "non_normative_purpose": None,
            },
        ],
        "interactions": [],
    }
    proof = {
        "boundary_model_version": "v1",
        "boundary_model_scope": "R1-R4",
        "proof_obligations": [
            {
                "proof_obligation_id": "text.proof.canonical",
                "governing_requirement_ids": ["R1"],
                "boundary_or_interaction_ids": ["text.canonical.requirements"],
                "test_case_ids": ["T1", "T2"],
                "automation_level": "automated",
                "manual_procedure_ids": [],
            },
            {
                "proof_obligation_id": "text.proof.mode",
                "governing_requirement_ids": ["R1", "R4"],
                "boundary_or_interaction_ids": [
                    "text.mode.valid",
                    "text.mode.unknown",
                ],
                "test_case_ids": ["T1", "T2"],
                "automation_level": "automated",
                "manual_procedure_ids": [],
            },
            {
                "proof_obligation_id": "text.proof.outcome",
                "governing_requirement_ids": ["R2", "R3", "R4"],
                "boundary_or_interaction_ids": [
                    "text.outcome.value",
                    "text.outcome.error",
                ],
                "test_case_ids": ["T1", "T2", "T3"],
                "automation_level": "automated",
                "manual_procedure_ids": [],
            },
            {
                "proof_obligation_id": "text.proof.evidence",
                "governing_requirement_ids": ["R1", "R2", "R3", "R4"],
                "boundary_or_interaction_ids": ["text.evidence.tests"],
                "test_case_ids": ["T1", "T2", "T3"],
                "automation_level": "automated",
                "manual_procedure_ids": [],
            },
        ],
    }
    return feature, proof


def _join(values: Sequence[str]) -> str:
    return ", ".join(values) if values else "-"


def _render_feature_markdown(payload: Mapping[str, object]) -> str:
    model = normalize_feature_model(payload)
    core_by_id = {row.dimension_id: row for row in model.core_dimensions}
    lines = [
        "# Portable text normalizer",
        "",
        "## Status",
        "",
        "approved",
        "",
        f"Boundary model version: {model.boundary_model_version}",
        f"Boundary model scope: {model.boundary_model_scope}",
        "",
        "## Requirements",
        "",
        "R1. The normalizer MUST accept exactly `trim` and `preserve`.",
        "",
        "R2. `trim` MUST remove leading and trailing Unicode whitespace.",
        "",
        "R3. `preserve` MUST return the input text unchanged.",
        "",
        "R4. An unknown mode MUST fail with `unknown-mode` and MUST NOT return text.",
        "",
        "## Boundary model",
        "",
        "| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |",
        "| --- | --- | --- | --- | --- |",
    ]
    for dimension_id in CORE_DIMENSION_IDS:
        row = core_by_id[dimension_id]
        lines.append(
            "| "
            + " | ".join(
                [
                    row.dimension_id,
                    row.applicability,
                    _join(row.governing_requirement_ids),
                    _join(row.boundary_ids),
                    row.non_applicability_rationale or "-",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Extensions: none.",
            "",
            "## Examples",
            "",
            "| Example ID | Role | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in sorted(model.examples, key=lambda item: item.example_id):
        lines.append(
            "| "
            + " | ".join(
                [
                    row.example_id,
                    row.role,
                    _join(row.governing_requirement_ids),
                    _join(row.boundary_ids),
                    row.regression_id or "-",
                    row.discovery_gap or "-",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Interactions",
            "",
            "None selected. The closed mode and outcome partitions do not create a cross-boundary hazard.",
            "",
        ]
    )
    return "\n".join(lines)


def _render_test_spec_markdown(
    payload: Mapping[str, object], feature_payload: Mapping[str, object]
) -> str:
    feature = normalize_feature_model(feature_payload)
    proof = normalize_proof_map(payload, feature)
    lines = [
        "# Portable text normalizer test spec",
        "",
        "## Status",
        "",
        "active",
        "",
        f"Boundary model version: {proof.boundary_model_version}",
        f"Boundary model scope: {proof.boundary_model_scope}",
        "",
        "## Proof map",
        "",
        "| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in sorted(proof.proof_obligations, key=lambda item: item.proof_obligation_id):
        lines.append(
            "| "
            + " | ".join(
                [
                    row.proof_obligation_id,
                    _join(row.governing_requirement_ids),
                    _join(row.boundary_or_interaction_ids),
                    _join(row.test_case_ids),
                    row.automation_level,
                    _join(row.manual_procedure_ids),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Test cases",
            "",
            "T1. `trim` removes surrounding Unicode whitespace and returns the selected mode.",
            "",
            "T2. Every unknown mode fails with `unknown-mode` and returns no text.",
            "",
            "T3. `preserve` returns the input unchanged and returns the selected mode.",
            "",
        ]
    )
    return "\n".join(lines)


def _snapshot(
    snapshot_id: str,
    source: str,
    role: str,
    path: str,
    raw: bytes,
) -> dict[str, object]:
    return {
        "snapshot_id": snapshot_id,
        "source": source,
        "artifact_role": role,
        "path": path,
        "identity": _sha256(raw),
    }


def _snapshot_ref(snapshot: Mapping[str, object]) -> dict[str, str]:
    return {
        "path": str(snapshot["path"]),
        "identity": str(snapshot["identity"]),
    }


def _event(
    stage: str,
    inputs: Sequence[Mapping[str, object]],
    output: Mapping[str, object],
    *,
    reviewed: Mapping[str, object] | None = None,
    bundle_artifacts: Sequence[Mapping[str, object]] = (),
    observed: str = "produced",
) -> dict[str, object]:
    evidence = {
        (str(item["path"]), str(item["identity"]))
        for item in (*inputs, output, *bundle_artifacts)
    }
    return {
        "stage": stage,
        "attempt": 1,
        "input_snapshot_ids": [str(item["snapshot_id"]) for item in inputs],
        "reviewed_snapshot_id": (
            None if reviewed is None else str(reviewed["snapshot_id"])
        ),
        "output_snapshot_ids": [str(output["snapshot_id"])],
        "structural_result": "pass",
        "observed_result": observed,
        "diagnostic_id": "none" if observed in {"produced", "approved"} else "review-nonapproval",
        "evidence_refs": [
            {"path": path, "identity": identity}
            for path, identity in sorted(evidence)
        ],
    }


def _write_run_artifact(root: Path, relative: str, raw: bytes) -> None:
    target = root / "artifacts" / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)


def _assemble_run(
    repo_root: Path,
    change_id: str,
    run_id: str,
    input_set: Mapping[str, object],
    payload: Mapping[str, object],
    candidate_feature: object,
    candidate_proof: object,
    before_inventory: Sequence[Mapping[str, str]],
    repository_after_inventory: Sequence[Mapping[str, str]],
) -> tuple[Path, dict[str, object]]:
    evidence_root = _select_change_root(repo_root, change_id) / "evidence"
    simple_root = evidence_root / "simple-change"
    simple_root.mkdir(parents=True, exist_ok=True)
    temporary = Path(
        tempfile.mkdtemp(prefix=f".{run_id}.", dir=simple_root)
    )
    final_prefix = (
        f"docs/changes/{change_id}/evidence/simple-change/runs/{run_id}"
    )
    feature_markdown = payload.get("feature_markdown")
    test_spec_markdown = payload.get("test_spec_markdown")
    spec_review_payload = payload.get("spec_review")
    test_review_payload = payload.get("test_spec_review")
    provenance = payload.get("stage_provenance")
    if (
        not isinstance(feature_markdown, str)
        or not isinstance(test_spec_markdown, str)
        or not isinstance(spec_review_payload, dict)
        or not isinstance(test_review_payload, dict)
        or not isinstance(provenance, list)
    ):
        raise BoundaryRuntimeError("protocol-shape-incompatible", "in-turn")
    try:
        feature_raw = feature_markdown.encode("utf-8")
        test_raw = test_spec_markdown.encode("utf-8")
    except UnicodeError as error:
        raise BoundaryRuntimeError("protocol-shape-incompatible", "in-turn") from error
    try:
        parsed_feature = normalize_feature_model(
            _parse_feature_markdown(feature_raw.decode("utf-8"))
        )
        parsed_proof = normalize_proof_map(
            _parse_test_spec_markdown(test_raw.decode("utf-8")),
            parsed_feature,
        )
    except (UnicodeError, BoundaryProofError) as error:
        raise BoundaryRuntimeError("runtime-identity-unstable", "in-turn") from error
    if (
        _feature_record(parsed_feature) != _feature_record(candidate_feature)
        or _proof_record(parsed_proof) != _proof_record(candidate_proof)
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable", "in-turn")
    if (
        spec_review_payload.get("outcome") != "approved"
        or test_review_payload.get("outcome") != "approved"
    ):
        raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")

    _write_run_artifact(temporary, "feature-spec/portable-text-normalizer.md", feature_raw)
    _write_run_artifact(temporary, "test-spec/portable-text-normalizer.test.md", test_raw)
    feature = _snapshot(
        "output.feature-spec.one",
        "behavior-output",
        "feature-spec",
        f"{final_prefix}/artifacts/feature-spec/portable-text-normalizer.md",
        feature_raw,
    )
    test_spec = _snapshot(
        "output.test-spec.one",
        "behavior-output",
        "test-spec",
        f"{final_prefix}/artifacts/test-spec/portable-text-normalizer.test.md",
        test_raw,
    )

    snapshots: list[dict[str, object]] = []
    oracle_feature_path = (
        repo_root
        / "tests/fixtures/boundary-proof/simple-change/candidates/feature-spec.md"
    )
    oracle_test_path = (
        repo_root
        / "tests/fixtures/boundary-proof/simple-change/candidates/test-spec.md"
    )
    snapshots.extend(
        [
            _snapshot(
                "oracle.feature-spec",
                "fixture-candidate",
                "feature-spec",
                oracle_feature_path.relative_to(repo_root).as_posix(),
                oracle_feature_path.read_bytes(),
            ),
            _snapshot(
                "oracle.test-spec",
                "fixture-candidate",
                "test-spec",
                oracle_test_path.relative_to(repo_root).as_posix(),
                oracle_test_path.read_bytes(),
            ),
            feature,
        ]
    )

    def review_bundle(
        stage: str,
        reviewed: Mapping[str, object],
        review_payload: Mapping[str, object],
        reviewer_thread_id: str,
    ) -> tuple[dict[str, object], dict[str, object], list[dict[str, object]]]:
        prefix = stage
        record_markdown = review_payload.get("review_record_markdown")
        log_markdown = review_payload.get("review_log_markdown")
        review_id = review_payload.get("review_id")
        if (
            not isinstance(record_markdown, str)
            or not isinstance(log_markdown, str)
            or not isinstance(review_id, str)
        ):
            raise BoundaryRuntimeError("protocol-shape-incompatible", "in-turn")
        record_raw = record_markdown.encode("utf-8")
        log_raw = log_markdown.encode("utf-8")
        record_path = f"{final_prefix}/artifacts/review-evidence/{prefix}-record.md"
        log_path = f"{final_prefix}/artifacts/review-evidence/{prefix}-log.md"
        record = _snapshot(
            f"output.{stage}.record",
            "behavior-output",
            "review-evidence",
            record_path,
            record_raw,
        )
        log = _snapshot(
            f"output.{stage}.log",
            "behavior-output",
            "review-evidence",
            log_path,
            log_raw,
        )
        bundle = {
            "review_id": review_id,
            "outcome": "approved",
            "reviewed_snapshot_id": reviewed["snapshot_id"],
            "material_finding_ids": [],
            "artifact_refs": {
                "review-record": _snapshot_ref(record),
                "review-log": _snapshot_ref(log),
            },
        }
        bundle_raw = _canonical_json_bytes(bundle)
        bundle_snapshot = _snapshot(
            f"output.{stage}.bundle",
            "behavior-output",
            "review-evidence",
            f"{final_prefix}/artifacts/review-evidence/{prefix}-bundle.json",
            bundle_raw,
        )
        _write_run_artifact(temporary, f"review-evidence/{prefix}-record.md", record_raw)
        _write_run_artifact(temporary, f"review-evidence/{prefix}-log.md", log_raw)
        _write_run_artifact(temporary, f"review-evidence/{prefix}-bundle.json", bundle_raw)
        return bundle_snapshot, bundle, [record, log]

    provenance_by_stage = {
        row.get("stage"): row
        for row in provenance
        if isinstance(row, dict) and isinstance(row.get("stage"), str)
    }
    if set(provenance_by_stage) != {
        "workflow",
        "spec",
        "spec-review",
        "test-spec",
        "test-spec-review",
    }:
        raise BoundaryRuntimeError("protocol-shape-incompatible", "in-turn")
    spec_review_thread = provenance_by_stage["spec-review"].get("thread_id")
    test_review_thread = provenance_by_stage["test-spec-review"].get("thread_id")
    if (
        not isinstance(spec_review_thread, str)
        or not isinstance(test_review_thread, str)
        or spec_review_thread == test_review_thread
    ):
        raise BoundaryRuntimeError("thread-metadata-mismatch", "in-turn")
    spec_bundle_snapshot, spec_bundle, spec_artifacts = review_bundle(
        "spec-review", feature, spec_review_payload, spec_review_thread
    )
    snapshots.extend([spec_bundle_snapshot, *spec_artifacts, test_spec])
    test_bundle_snapshot, test_bundle, test_artifacts = review_bundle(
        "test-spec-review",
        test_spec,
        test_review_payload,
        test_review_thread,
    )
    snapshots.extend([test_bundle_snapshot, *test_artifacts])

    events = [
        _event("spec", [], feature),
        _event(
            "spec-review",
            [feature],
            spec_bundle_snapshot,
            reviewed=feature,
            bundle_artifacts=spec_artifacts,
            observed="approved",
        ),
        _event(
            "test-spec",
            [feature, spec_bundle_snapshot, *spec_artifacts],
            test_spec,
        ),
        _event(
            "test-spec-review",
            [test_spec, feature, spec_bundle_snapshot, *spec_artifacts],
            test_bundle_snapshot,
            reviewed=test_spec,
            bundle_artifacts=test_artifacts,
            observed="approved",
        ),
    ]
    behavior_inventory = [
            {
                "path": snapshot["path"],
                "artifact_kind": snapshot["artifact_role"],
                "identity": snapshot["identity"],
            }
            for snapshot in snapshots
            if snapshot["source"] == "behavior-output"
        ]
    after_inventory = sorted(
        [*map(dict, repository_after_inventory), *behavior_inventory],
        key=lambda row: str(row["path"]),
    )
    if len({str(row["path"]) for row in after_inventory}) != len(after_inventory):
        raise BoundaryRuntimeError("runtime-identity-unstable", "in-turn")
    trace = {
        "snapshots": snapshots,
        "review_bundles": {
            spec_bundle_snapshot["snapshot_id"]: spec_bundle,
            test_bundle_snapshot["snapshot_id"]: test_bundle,
        },
        "events": events,
        "before_inventory": list(map(dict, before_inventory)),
        "after_inventory": after_inventory,
    }
    structural = {
        "spec#1": {"structural_result": "pass", "diagnostic_id": "none"},
        "spec-review#1": {
            "structural_result": "pass",
            "diagnostic_id": "none",
        },
        "test-spec#1": {
            "structural_result": "pass",
            "diagnostic_id": "none",
        },
        "test-spec-review#1": {
            "structural_result": "pass",
            "diagnostic_id": "none",
        },
    }
    metrics = evaluate_simple_change_trace(
        trace,
        feature_models={str(feature["snapshot_id"]): parsed_feature},
        proof_maps={str(test_spec["snapshot_id"]): parsed_proof},
        structural_evaluations=structural,
    )
    if (
        metrics.false_blocking_count != 0
        or metrics.new_universal_artifact_count != 0
        or metrics.structure_only_correction_cycles != 0
        or not metrics.applicable_only_mapping
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable", "in-turn")
    manifest = {
        "run_id": run_id,
        "input_set": dict(input_set),
        "input_set_identity": _sha256(_canonical_json_bytes(input_set)),
        "baseline_commit": input_set["baseline_commit"],
        "before_artifact_inventory": list(map(dict, before_inventory)),
        "after_artifact_inventory": after_inventory,
        "snapshots": snapshots,
        "events": events,
    }
    (temporary / "manifest.json").write_bytes(_canonical_json_bytes(manifest))
    return temporary, manifest


def _read_json(path: Path) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise BoundaryRuntimeError("runtime-identity-unstable") from error
    if not isinstance(value, dict):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    return value


def _pointer_for(
    repo_root: Path,
    change_id: str,
    run_id: str,
    input_set_identity: str,
) -> dict[str, object]:
    manifest_path = (
        repo_root
        / "docs"
        / "changes"
        / change_id
        / "evidence"
        / "simple-change"
        / "runs"
        / run_id
        / "manifest.json"
    )
    return {
        "run_id": run_id,
        "input_set_identity": input_set_identity,
        "manifest_ref": _regular_reference(repo_root, manifest_path),
    }


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _exclusive_write(path: Path, raw: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "wb", closefd=True) as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass
        raise
    _fsync_directory(path.parent)


def _validate_staged_run(
    staged: Path, manifest: Mapping[str, object], pointer: Mapping[str, object]
) -> None:
    manifest_path = staged / "manifest.json"
    manifest_ref = pointer.get("manifest_ref")
    if (
        not manifest_path.is_file()
        or manifest_path.is_symlink()
        or _read_json(manifest_path) != dict(manifest)
        or not isinstance(manifest_ref, dict)
        or manifest_ref.get("identity") != _read_file_identity(manifest_path).digest
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    snapshots = manifest.get("snapshots")
    if not isinstance(snapshots, list):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    for snapshot in snapshots:
        if not isinstance(snapshot, dict) or snapshot.get("source") != "behavior-output":
            continue
        path = snapshot.get("path")
        role = snapshot.get("artifact_role")
        identity = snapshot.get("identity")
        if (
            not isinstance(path, str)
            or not isinstance(role, str)
            or not isinstance(identity, str)
        ):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        marker = "/artifacts/"
        if marker not in path:
            raise BoundaryRuntimeError("runtime-identity-unstable")
        relative = path.split(marker, 1)[1]
        candidate = staged / "artifacts" / relative
        if (
            not candidate.is_file()
            or candidate.is_symlink()
            or _read_file_identity(candidate).digest != identity
        ):
            raise BoundaryRuntimeError("runtime-identity-unstable")


def _crash_if(boundary: str | None, expected: str) -> None:
    if boundary == expected:
        raise BoundaryRuntimeError("runtime-identity-unstable")


def _publish_run(
    repo_root: Path,
    change_id: str,
    temporary: Path,
    manifest: Mapping[str, object],
    *,
    crash_at: str | None = None,
) -> dict[str, object]:
    simple_root = (
        _select_change_root(repo_root, change_id) / "evidence" / "simple-change"
    )
    runs_root = simple_root / "runs"
    runs_root.mkdir(mode=0o700, parents=True, exist_ok=True)
    run_id = manifest["run_id"]
    if not isinstance(run_id, str) or re.fullmatch(r"run-[0-9a-f]{32}", run_id) is None:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    target = runs_root / run_id
    if target.exists():
        raise BoundaryRuntimeError("runtime-identity-unstable")
    staged = simple_root / f".prepared-{run_id}"
    if staged.exists():
        raise BoundaryRuntimeError("runtime-identity-unstable")
    prepared_path = simple_root / "prepared.json"
    current_path = simple_root / "current.json"
    if prepared_path.exists():
        raise BoundaryRuntimeError("runtime-identity-unstable")
    prior = _read_json(current_path) if current_path.exists() else None
    try:
        manifest_path = (
            repo_root
            / "docs"
            / "changes"
            / change_id
            / "evidence"
            / "simple-change"
            / "runs"
            / run_id
            / "manifest.json"
        )
        pointer = {
            "run_id": run_id,
            "input_set_identity": str(manifest["input_set_identity"]),
            "manifest_ref": {
                "path": manifest_path.relative_to(repo_root).as_posix(),
                "identity": _sha256(_canonical_json_bytes(manifest)),
            },
        }
        prepared = {
            **pointer,
            "prior_pointer": prior,
        }
        os.replace(temporary, staged)
        _fsync_directory(simple_root)
        _validate_staged_run(staged, manifest, pointer)
        _crash_if(crash_at, "before-receipt")
        _exclusive_write(prepared_path, _canonical_json_bytes(prepared))
        _crash_if(crash_at, "after-receipt-fsync")
        os.replace(staged, target)
        _fsync_directory(runs_root)
        _crash_if(crash_at, "after-run-install")
        _validate_run(repo_root, change_id, pointer)
        _crash_if(crash_at, "after-run-validation")
        _atomic_write(current_path, _canonical_json_bytes(pointer))
        _crash_if(crash_at, "after-pointer-replace")
        _fsync_directory(simple_root)
        _crash_if(crash_at, "after-parent-fsync")
        prepared_path.unlink()
        _fsync_directory(simple_root)
        _crash_if(crash_at, "after-receipt-cleanup")
    except OSError as error:
        raise BoundaryRuntimeError("runtime-identity-unstable") from error
    return pointer


def _validate_input_set(
    repo_root: Path,
    manifest: Mapping[str, object],
    input_set: Mapping[str, object],
) -> None:
    expected_fields = {
        "schema_version",
        "scenario_ref",
        "baseline_commit",
        "skill_resource_refs",
        "oracle_refs",
        "implementation_manifest_ref",
    }
    if (
        set(input_set) != expected_fields
        or input_set.get("schema_version") != "simple-change-input-v1"
        or not isinstance(input_set.get("baseline_commit"), str)
        or re.fullmatch(r"git:[0-9a-f]{40}", str(input_set["baseline_commit"]))
        is None
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    for field in ("scenario_ref", "implementation_manifest_ref"):
        _validate_reference(repo_root, input_set[field])
    for field in ("skill_resource_refs", "oracle_refs"):
        rows = input_set.get(field)
        if not isinstance(rows, list) or rows != sorted(
            rows, key=lambda row: row.get("path", "") if isinstance(row, dict) else ""
        ):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        for row in rows:
            _validate_reference(repo_root, row)
    if input_set["skill_resource_refs"] != manifest["skill_package_refs"]:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    expected_scenario = (
        repo_root
        / "tests"
        / "fixtures"
        / "boundary-proof"
        / "simple-change"
        / "scenario.json"
    )
    if _validate_reference(repo_root, input_set["scenario_ref"]) != expected_scenario:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    expected_oracles = [
        _regular_reference(repo_root, path)
        for path in sorted(
            [
                expected_scenario.parent / "candidates" / "feature-spec.md",
                expected_scenario.parent / "candidates" / "test-spec.md",
            ]
        )
    ]
    if input_set["oracle_refs"] != expected_oracles:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    implementation_path = _validate_reference(
        repo_root, input_set["implementation_manifest_ref"]
    )
    if _read_json(implementation_path) != manifest:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    baseline = str(input_set["baseline_commit"]).removeprefix("git:")
    completed = subprocess.run(
        ("git", "-C", str(repo_root), "merge-base", "--is-ancestor", baseline, "HEAD"),
        check=False,
        capture_output=True,
        timeout=10,
    )
    if completed.returncode != 0:
        raise BoundaryRuntimeError("runtime-identity-unstable")


def _validate_run(
    repo_root: Path,
    change_id: str,
    pointer: Mapping[str, object],
) -> object:
    if set(pointer) != {"run_id", "input_set_identity", "manifest_ref"}:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    run_id = pointer.get("run_id")
    if not isinstance(run_id, str) or re.fullmatch(r"run-[0-9a-f]{32}", run_id) is None:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    manifest_path = _validate_reference(repo_root, pointer["manifest_ref"])
    expected_path = (
        repo_root
        / "docs"
        / "changes"
        / change_id
        / "evidence"
        / "simple-change"
        / "runs"
        / run_id
        / "manifest.json"
    )
    if manifest_path != expected_path:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    run = _read_json(manifest_path)
    if set(run) != {
        "run_id",
        "input_set",
        "input_set_identity",
        "baseline_commit",
        "before_artifact_inventory",
        "after_artifact_inventory",
        "snapshots",
        "events",
    }:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    input_set = run.get("input_set")
    if not isinstance(input_set, dict):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    input_identity = _sha256(_canonical_json_bytes(input_set))
    if (
        run.get("run_id") != run_id
        or run.get("input_set_identity") != input_identity
        or pointer.get("input_set_identity") != input_identity
        or run.get("baseline_commit") != input_set.get("baseline_commit")
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    implementation_path = _validate_reference(
        repo_root, input_set["implementation_manifest_ref"]
    )
    implementation_manifest = _read_json(implementation_path)
    _validate_behavior_manifest(repo_root, implementation_manifest)
    _validate_input_set(repo_root, implementation_manifest, input_set)
    snapshots = run.get("snapshots")
    events = run.get("events")
    before = run.get("before_artifact_inventory")
    after = run.get("after_artifact_inventory")
    if not all(isinstance(value, list) for value in (snapshots, events, before, after)):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    baseline_commit = str(input_set["baseline_commit"]).removeprefix("git:")
    expected_before = _inventory_from_commit(repo_root, change_id, baseline_commit)
    if before != expected_before:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    before_by_path = {str(row["path"]): row for row in before}
    after_by_path = {str(row["path"]): row for row in after}
    if len(before_by_path) != len(before) or len(after_by_path) != len(after):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    implementation_relative = str(input_set["implementation_manifest_ref"]["path"])
    repository_after_paths = {
        path for path in after_by_path if "/evidence/simple-change/runs/" not in path
    }
    if repository_after_paths != set(before_by_path) | {implementation_relative}:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    for path, row in after_by_path.items():
        expected_kind = (
            str(row["artifact_kind"])
            if "/evidence/simple-change/runs/" in path
            else _artifact_kind(path, change_id)
        )
        if row.get("artifact_kind") != expected_kind:
            raise BoundaryRuntimeError("runtime-identity-unstable")
        if (
            path in before_by_path
            and path != implementation_relative
            and row != before_by_path[path]
        ):
            raise BoundaryRuntimeError("runtime-identity-unstable")
    output_snapshots: dict[str, Mapping[str, object]] = {}
    for snapshot in snapshots:
        if not isinstance(snapshot, dict):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        if snapshot.get("source") == "behavior-output":
            path = _validate_reference(repo_root, _snapshot_ref(snapshot))
            if not path.is_relative_to(manifest_path.parent / "artifacts"):
                raise BoundaryRuntimeError("runtime-identity-unstable")
            output_snapshots[str(snapshot["snapshot_id"])] = snapshot
        else:
            _validate_reference(repo_root, _snapshot_ref(snapshot))
    artifact_files = {
        path
        for path in (manifest_path.parent / "artifacts").rglob("*")
        if path.is_file()
    }
    snapshot_files = {
        repo_root / str(snapshot["path"]) for snapshot in output_snapshots.values()
    }
    if artifact_files != snapshot_files:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    bundles: dict[str, object] = {}
    for snapshot_id, snapshot in output_snapshots.items():
        if str(snapshot["path"]).endswith("-bundle.json"):
            bundles[snapshot_id] = _read_json(repo_root / str(snapshot["path"]))
    trace = {
        "snapshots": snapshots,
        "review_bundles": bundles,
        "events": events,
        "before_inventory": before,
        "after_inventory": after,
    }
    feature_snapshot = output_snapshots.get("output.feature-spec.one")
    test_snapshot = output_snapshots.get("output.test-spec.one")
    if feature_snapshot is None or test_snapshot is None:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    try:
        feature = normalize_feature_model(
            _parse_feature_markdown(
                (repo_root / str(feature_snapshot["path"])).read_text(
                    encoding="utf-8"
                )
            )
        )
        proof = normalize_proof_map(
            _parse_test_spec_markdown(
                (repo_root / str(test_snapshot["path"])).read_text(
                    encoding="utf-8"
                )
            ),
            feature,
        )
        oracle_refs = input_set["oracle_refs"]
        oracle_by_name = {
            Path(str(row["path"])).name: _validate_reference(repo_root, row)
            for row in oracle_refs
        }
        oracle_feature = normalize_feature_model(
            _parse_feature_markdown(
                oracle_by_name["feature-spec.md"].read_text(encoding="utf-8")
            )
        )
        oracle_proof = normalize_proof_map(
            _parse_test_spec_markdown(
                oracle_by_name["test-spec.md"].read_text(encoding="utf-8")
            ),
            oracle_feature,
        )
        if (
            _feature_record(feature) != _feature_record(oracle_feature)
            or _proof_record(proof) != _proof_record(oracle_proof)
        ):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        structural = {
            f"{event['stage']}#{event['attempt']}": {
                "structural_result": "pass",
                "diagnostic_id": "none",
            }
            for event in events
        }
        return evaluate_simple_change_trace(
            trace,
            feature_models={"output.feature-spec.one": feature},
            proof_maps={"output.test-spec.one": proof},
            structural_evaluations=structural,
        )
    except (OSError, UnicodeError, KeyError, BoundaryProofError) as error:
        if isinstance(error, BoundaryRuntimeError):
            raise
        raise BoundaryRuntimeError("runtime-identity-unstable") from error


def _reconcile_prepared(repo_root: Path, change_id: str) -> None:
    simple_root = (
        _select_change_root(repo_root, change_id) / "evidence" / "simple-change"
    )
    prepared_path = simple_root / "prepared.json"
    if not prepared_path.exists():
        return
    prepared = _read_json(prepared_path)
    if set(prepared) != {
        "run_id",
        "input_set_identity",
        "manifest_ref",
        "prior_pointer",
    }:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    target_pointer = {
        key: prepared[key]
        for key in ("run_id", "input_set_identity", "manifest_ref")
    }
    run_id = prepared["run_id"]
    if not isinstance(run_id, str):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    staged = simple_root / f".prepared-{run_id}"
    target = simple_root / "runs" / run_id
    if staged.exists() and target.exists():
        raise BoundaryRuntimeError("runtime-identity-unstable")
    if not target.exists():
        if not staged.is_dir() or staged.is_symlink():
            raise BoundaryRuntimeError("runtime-identity-unstable")
        os.replace(staged, target)
        _fsync_directory(target.parent)
    current_path = simple_root / "current.json"
    current = _read_json(current_path) if current_path.exists() else None
    if current == target_pointer:
        _validate_run(repo_root, change_id, target_pointer)
    elif current == prepared["prior_pointer"]:
        _validate_run(repo_root, change_id, target_pointer)
        _atomic_write(current_path, _canonical_json_bytes(target_pointer))
    else:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    prepared_path.unlink()
    _fsync_directory(simple_root)


def generate_behavior(
    change_id: str,
    scenario_path: Path,
    *,
    repo_root: Path = ROOT,
    command: str = "codex",
) -> dict[str, object]:
    _select_change_root(repo_root, change_id)
    _reconcile_prepared(repo_root, change_id)
    baseline_head = _repository_head(repo_root)
    _require_clean_worktree(repo_root)
    if not scenario_path.is_absolute():
        scenario_path = repo_root / scenario_path
    scenario = _scenario(repo_root, scenario_path)
    baseline_path = (
        _select_change_root(repo_root, change_id)
        / "evidence"
        / "boundary-proof-baseline.json"
    )
    baseline = _read_json(baseline_path)
    if (
        set(baseline)
        != {"schema_version", "change_id", "preservation_baseline_commit"}
        or baseline.get("schema_version") != "boundary-proof-baseline-v1"
        or baseline.get("change_id") != change_id
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    def invoke(request: Mapping[str, object]) -> tuple[dict[str, object], dict[str, object]]:
        if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
            print(f"stage-start:{request.get('stage')}", file=sys.stderr)
        generated: list[dict[str, object]] = []
        observed_attestation = _collect_runtime_attestation(
            command,
            repo_root=repo_root,
            generation_request=request,
            generation_sink=generated,
        )
        if len(generated) != 1:
            raise BoundaryRuntimeError("protocol-shape-incompatible", "in-turn")
        if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
            print(f"stage-complete:{request.get('stage')}", file=sys.stderr)
        return observed_attestation, generated[0]

    attestation, route_result = invoke(_route_request(str(scenario["request"])))
    route = _load_generated_payload(route_result, {"stages"})
    if route != {
        "stages": ["spec", "spec-review", "test-spec", "test-spec-review"]
    }:
        raise BoundaryRuntimeError("protocol-shape-incompatible", "in-turn")

    spec_attestation, spec_result = invoke(
        _spec_request(str(scenario["request"]))
    )
    spec_payload = _load_generated_payload(spec_result, {"artifact_markdown"})
    feature_markdown = spec_payload.get("artifact_markdown")
    if not isinstance(feature_markdown, str):
        raise BoundaryRuntimeError("protocol-shape-incompatible", "in-turn")
    feature_identity = _sha256(feature_markdown.encode("utf-8"))

    spec_review_attestation, spec_review_result = invoke(
        _review_request("spec-review", feature_markdown, feature_identity)
    )
    spec_review_payload = _load_generated_payload(
        spec_review_result,
        {
            "review_id",
            "outcome",
            "review_record_markdown",
            "review_log_markdown",
        },
    )
    _validate_review_payload(
        spec_review_payload,
        stage="spec-review",
        artifact_identity=feature_identity,
    )

    test_spec_attestation, test_spec_result = invoke(
        _test_spec_request(
            str(scenario["request"]),
            feature_markdown,
            str(spec_review_payload["review_record_markdown"]),
        )
    )
    test_spec_payload = _load_generated_payload(
        test_spec_result, {"artifact_markdown"}
    )
    test_spec_markdown = test_spec_payload.get("artifact_markdown")
    if not isinstance(test_spec_markdown, str):
        raise BoundaryRuntimeError("protocol-shape-incompatible", "in-turn")
    test_spec_identity = _sha256(test_spec_markdown.encode("utf-8"))

    test_review_attestation, test_review_result = invoke(
        _review_request(
            "test-spec-review", test_spec_markdown, test_spec_identity
        )
    )
    test_review_payload = _load_generated_payload(
        test_review_result,
        {
            "review_id",
            "outcome",
            "review_record_markdown",
            "review_log_markdown",
        },
    )
    _validate_review_payload(
        test_review_payload,
        stage="test-spec-review",
        artifact_identity=test_spec_identity,
    )
    attestation_identity_fields = {
        field
        for field in ATTESTATION_FIELDS
        if field.endswith("_identity") or field == "active_permission_profile"
    }
    for observed in (
        spec_attestation,
        spec_review_attestation,
        test_spec_attestation,
        test_review_attestation,
    ):
        if any(observed[field] != attestation[field] for field in attestation_identity_fields):
            raise BoundaryRuntimeError("runtime-identity-unstable", "in-turn")
    thread_ids = [
        route_result.get("thread_id"),
        spec_result.get("thread_id"),
        spec_review_result.get("thread_id"),
        test_spec_result.get("thread_id"),
        test_review_result.get("thread_id"),
    ]
    if any(not isinstance(value, str) for value in thread_ids) or len(
        set(thread_ids)
    ) != 5:
        raise BoundaryRuntimeError("thread-metadata-mismatch", "in-turn")
    payload = {
        "feature_markdown": feature_markdown,
        "spec_review": spec_review_payload,
        "test_spec_markdown": test_spec_markdown,
        "test_spec_review": test_review_payload,
        "stage_provenance": [
            {
                "stage": result["stage"],
                "thread_id": result["thread_id"],
                "skill_names": result["skill_names"],
            }
            for result in (
                route_result,
                spec_result,
                spec_review_result,
                test_spec_result,
                test_review_result,
            )
        ],
    }
    behavior_manifest = _build_behavior_manifest(repo_root, attestation)
    _validate_behavior_manifest(repo_root, behavior_manifest)
    change_root = _select_change_root(repo_root, change_id)
    implementation_path = (
        change_root / "evidence" / "behavior-implementation-manifest.json"
    )
    implementation_raw = _canonical_json_bytes(behavior_manifest)
    implementation_ref = {
        "path": implementation_path.relative_to(repo_root).as_posix(),
        "identity": _sha256(implementation_raw),
    }
    _atomic_write(implementation_path, implementation_raw)
    baseline_commit = "git:" + baseline_head
    skill_refs = list(behavior_manifest["skill_package_refs"])
    oracle_paths = [
        scenario_path.parent / "candidates" / "feature-spec.md",
        scenario_path.parent / "candidates" / "test-spec.md",
    ]
    oracle_refs = [
        _regular_reference(repo_root, path) for path in sorted(oracle_paths)
    ]
    input_set = {
        "schema_version": "simple-change-input-v1",
        "scenario_ref": _regular_reference(repo_root, scenario_path),
        "baseline_commit": baseline_commit,
        "skill_resource_refs": skill_refs,
        "oracle_refs": oracle_refs,
        "implementation_manifest_ref": implementation_ref,
    }
    candidate_feature = normalize_feature_model(
        _parse_feature_markdown(oracle_paths[0].read_text(encoding="utf-8"))
    )
    candidate_proof = normalize_proof_map(
        _parse_test_spec_markdown(oracle_paths[1].read_text(encoding="utf-8")),
        candidate_feature,
    )
    run_id = "run-" + secrets.token_hex(16)
    temporary, run_manifest = _assemble_run(
        repo_root,
        change_id,
        run_id,
        input_set,
        payload,
        candidate_feature,
        candidate_proof,
        _inventory_from_commit(repo_root, change_id, baseline_head),
        _inventory_from_worktree(repo_root, change_id),
    )
    pointer = _publish_run(
        repo_root, change_id, temporary, run_manifest
    )
    metrics = _validate_run(repo_root, change_id, pointer)
    return {
        "result": "pass",
        "run_id": run_id,
        "input_set_identity": pointer["input_set_identity"],
        "false_blocking_count": metrics.false_blocking_count,
        "new_universal_artifact_count": metrics.new_universal_artifact_count,
        "simple_fixture_structure_correction_cycles": (
            metrics.structure_only_correction_cycles
        ),
    }


def validate_behavior(
    change_id: str, *, repo_root: Path = ROOT
) -> dict[str, object]:
    _reconcile_prepared(repo_root, change_id)
    current_path = (
        _select_change_root(repo_root, change_id)
        / "evidence"
        / "simple-change"
        / "current.json"
    )
    pointer = _read_json(current_path)
    metrics = _validate_run(repo_root, change_id, pointer)
    return {
        "result": "pass",
        "run_id": pointer["run_id"],
        "input_set_identity": pointer["input_set_identity"],
        "false_blocking_count": metrics.false_blocking_count,
        "new_universal_artifact_count": metrics.new_universal_artifact_count,
        "simple_fixture_structure_correction_cycles": (
            metrics.structure_only_correction_cycles
        ),
    }


def exercise_fixture(
    fixture_path: Path,
    output_root: Path,
    *,
    repo_root: Path = ROOT,
) -> dict[str, object]:
    if not fixture_path.is_absolute():
        fixture_path = repo_root / fixture_path
    fixture = _read_json(fixture_path)
    if set(fixture) != {
        "fixture_id",
        "scenario",
        "feature_candidate",
        "test_spec_candidate",
    } or fixture.get("fixture_id") != "boundary-behavior-happy-path-v1":
        raise BoundaryRuntimeError("runtime-identity-unstable")
    scenario_path = repo_root / str(fixture["scenario"])
    _scenario(repo_root, scenario_path)
    feature_path = repo_root / str(fixture["feature_candidate"])
    test_path = repo_root / str(fixture["test_spec_candidate"])
    feature = normalize_feature_model(
        _parse_feature_markdown(feature_path.read_text(encoding="utf-8"))
    )
    proof = normalize_proof_map(
        _parse_test_spec_markdown(test_path.read_text(encoding="utf-8")),
        feature,
    )
    result = {
        "schema_version": "boundary-behavior-fixture-v1",
        "fixture_ref": _regular_reference(repo_root, fixture_path),
        "scenario_ref": _regular_reference(repo_root, scenario_path),
        "feature_ref": _regular_reference(repo_root, feature_path),
        "test_spec_ref": _regular_reference(repo_root, test_path),
        "feature_record": _feature_record(feature),
        "proof_record": _proof_record(proof),
    }
    output_root.mkdir(parents=True, exist_ok=True)
    _atomic_write(output_root / "fixture-result.json", _canonical_json_bytes(result))
    return result


def validate_fixture(
    output_root: Path, *, repo_root: Path = ROOT
) -> dict[str, object]:
    result = _read_json(output_root / "fixture-result.json")
    if set(result) != {
        "schema_version",
        "fixture_ref",
        "scenario_ref",
        "feature_ref",
        "test_spec_ref",
        "feature_record",
        "proof_record",
    } or result.get("schema_version") != "boundary-behavior-fixture-v1":
        raise BoundaryRuntimeError("runtime-identity-unstable")
    for field in ("fixture_ref", "scenario_ref", "feature_ref", "test_spec_ref"):
        _validate_reference(repo_root, result[field])
    feature_path = _validate_reference(repo_root, result["feature_ref"])
    test_path = _validate_reference(repo_root, result["test_spec_ref"])
    feature = normalize_feature_model(
        _parse_feature_markdown(feature_path.read_text(encoding="utf-8"))
    )
    proof = normalize_proof_map(
        _parse_test_spec_markdown(test_path.read_text(encoding="utf-8")),
        feature,
    )
    if (
        result["feature_record"] != _feature_record(feature)
        or result["proof_record"] != _proof_record(proof)
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    return {"result": "pass", "fixture_id": "boundary-behavior-happy-path-v1"}


def freeze_baseline(
    change_id: str, *, repo_root: Path = ROOT
) -> dict[str, str]:
    """Create the immutable pre-skill-mutation baseline exactly once."""

    change_root = _select_change_root(repo_root, change_id)
    record = {
        "schema_version": "boundary-proof-baseline-v1",
        "change_id": change_id,
        "preservation_baseline_commit": _repository_head(repo_root),
    }
    raw = _canonical_json_bytes(record)
    target = change_root / "evidence" / "boundary-proof-baseline.json"
    if target.exists():
        try:
            installed = target.read_bytes()
        except OSError as error:
            raise BoundaryRuntimeError("runtime-unavailable") from error
        if installed != raw:
            raise BoundaryRuntimeError("runtime-identity-unstable")
        return record
    try:
        _atomic_write(target, raw)
    except OSError as error:
        raise BoundaryRuntimeError("runtime-unavailable") from error
    return record


def _resolved_regular_executable(command: str) -> Path:
    discovered = shutil.which(command)
    if discovered is None:
        raise BoundaryRuntimeError("runtime-unavailable")
    try:
        resolved = Path(discovered).resolve(strict=True)
        metadata = resolved.lstat()
    except (OSError, RuntimeError) as error:
        raise BoundaryRuntimeError("runtime-unreadable") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise BoundaryRuntimeError("runtime-unreadable")
    return resolved


def _read_file_identity(path: Path) -> _FileIdentity:
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise BoundaryRuntimeError("runtime-unreadable") from error
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise BoundaryRuntimeError("runtime-unreadable")
        digest = hashlib.sha256()
        while chunk := os.read(descriptor, 1024 * 1024):
            digest.update(chunk)
        return _FileIdentity(
            device=metadata.st_dev,
            inode=metadata.st_ino,
            size=metadata.st_size,
            modified_ns=metadata.st_mtime_ns,
            changed_ns=metadata.st_ctime_ns,
            digest="sha256:" + digest.hexdigest(),
        )
    finally:
        os.close(descriptor)


def _bundle_projection(
    root: Path, diagnostic_id: str = "schema-bundle-invalid"
) -> tuple[list[dict[str, str]], str]:
    rows: list[dict[str, str]] = []
    try:
        entries = sorted(root.rglob("*"), key=lambda path: path.as_posix())
        for path in entries:
            metadata = path.lstat()
            if stat.S_ISDIR(metadata.st_mode):
                continue
            if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
                raise BoundaryRuntimeError(diagnostic_id)
            rows.append(
                {
                    "logical_path": path.relative_to(root).as_posix(),
                    "identity": _sha256(path.read_bytes()),
                }
            )
    except OSError as error:
        raise BoundaryRuntimeError(diagnostic_id) from error
    if not rows:
        raise BoundaryRuntimeError(diagnostic_id)
    return rows, _sha256(_canonical_json_bytes(rows))


def _schema_bundle_projection(root: Path) -> tuple[list[dict[str, str]], str]:
    rows: list[dict[str, str]] = []
    try:
        entries = sorted(root.rglob("*"), key=lambda path: path.as_posix())
        for path in entries:
            metadata = path.lstat()
            if stat.S_ISDIR(metadata.st_mode):
                continue
            if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
                raise BoundaryRuntimeError("schema-bundle-invalid")
            try:
                def unique_object(
                    pairs: list[tuple[str, object]],
                ) -> dict[str, object]:
                    result: dict[str, object] = {}
                    for key, value in pairs:
                        if key in result:
                            raise ValueError("duplicate JSON object member")
                        result[key] = value
                    return result

                document = json.loads(
                    path.read_text(encoding="utf-8"),
                    object_pairs_hook=unique_object,
                )
            except (UnicodeError, json.JSONDecodeError, ValueError) as error:
                raise BoundaryRuntimeError("schema-bundle-invalid") from error
            rows.append(
                {
                    "logical_path": path.relative_to(root).as_posix(),
                    "identity": _sha256(_canonical_json_bytes(document)),
                }
            )
    except OSError as error:
        raise BoundaryRuntimeError("schema-bundle-invalid") from error
    if not rows:
        raise BoundaryRuntimeError("schema-bundle-invalid")
    return rows, _sha256(_canonical_json_bytes(rows))


def _run_runtime(
    argv: Sequence[str],
    *,
    env: Mapping[str, str] | None = None,
    timeout: int = 30,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    selected_env = dict(env or {"HOME": os.environ.get("HOME", ""), "PATH": os.environ.get("PATH", "")})
    try:
        return subprocess.run(
            list(argv),
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=selected_env,
            input=input_text,
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise BoundaryRuntimeError("runtime-unavailable") from error


def _runtime_version(executable: Path) -> str:
    completed = _run_runtime((str(executable), "--version"))
    if completed.returncode != 0:
        raise BoundaryRuntimeError("runtime-unavailable")
    match = re.fullmatch(r"codex-cli ([^\r\n]+)\r?\n?", completed.stdout)
    if match is None:
        raise BoundaryRuntimeError("runtime-version-invalid")
    version = match.group(1)
    parsed = _parse_semver(version)
    if parsed < _parse_semver(MINIMUM_CODEX_VERSION):
        raise BoundaryRuntimeError("runtime-version-unsupported")
    return version


def _runtime_package(executable: Path, version: str) -> Path:
    matches: list[Path] = []
    for parent in executable.parents:
        package_file = parent / "package.json"
        try:
            metadata = package_file.lstat()
        except FileNotFoundError:
            continue
        except OSError as error:
            raise BoundaryRuntimeError("runtime-unreadable") from error
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
            raise BoundaryRuntimeError("runtime-unreadable")
        try:
            package = json.loads(package_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise BoundaryRuntimeError("runtime-version-invalid") from error
        if isinstance(package, dict) and package.get("name") == "@openai/codex":
            matches.append(parent)
            if package.get("version") != version:
                raise BoundaryRuntimeError("runtime-version-invalid")
            break
    if len(matches) != 1:
        raise BoundaryRuntimeError("runtime-unavailable")
    return matches[0]


def _copy_participating_skills(runtime_home: Path) -> None:
    skills_root = runtime_home / "skills"
    skills_root.mkdir(mode=0o700)
    for name in PARTICIPATING_SKILLS:
        source = ROOT / "skills" / name
        target = skills_root / name
        if not source.is_dir() or source.is_symlink():
            raise BoundaryRuntimeError("skill-inventory-mismatch", "pre-turn-start")
        try:
            shutil.copytree(source, target, symlinks=False)
        except OSError as error:
            raise BoundaryRuntimeError(
                "skill-inventory-mismatch", "pre-turn-start"
            ) from error


def _toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _generated_config(
    runtime_home: Path,
    runtime_package: Path,
    workspace: Path,
    model_id: str,
    runtime_version: str,
    command_path: str,
) -> bytes:
    runtime_features = RUNTIME_FEATURES_BY_VERSION.get(runtime_version)
    if runtime_features is None:
        raise BoundaryRuntimeError("feature-classification-invalid")
    disabled = set(runtime_features) - set(PERMITTED_TOOL_FEATURES)
    lines = [
        f"model = {_toml_string(model_id)}",
        'model_provider = "openai"',
        'approval_policy = "never"',
        'default_permissions = "boundary-proof-v1"',
        "include_apps_instructions = false",
        "",
        "[shell_environment_policy]",
        'inherit = "none"',
        f'set = {{ PATH = {_toml_string(command_path)} }}',
        "",
        "[features]",
    ]
    for feature in runtime_features:
        lines.append(f"{feature} = {'false' if feature in disabled else 'true'}")
    lines.extend(
        [
            "",
            "[permissions.boundary-proof-v1]",
            'description = "Boundary proof isolated runtime"',
            "",
            "[permissions.boundary-proof-v1.filesystem]",
            '":root" = "deny"',
            '":minimal" = "read"',
            f"{_toml_string(str(runtime_package))} = \"read\"",
            "",
            '[permissions.boundary-proof-v1.filesystem.":workspace_roots"]',
            '"." = "write"',
            "",
            "[permissions.boundary-proof-v1.network]",
            "enabled = false",
            "",
        ]
    )
    for name in RUNTIME_SYSTEM_SKILLS:
        path = runtime_home / "skills" / ".system" / name / "SKILL.md"
        lines.extend(
            [
                "[[skills.config]]",
                f"path = {_toml_string(str(path))}",
                "enabled = false",
                "",
            ]
        )
    lines.extend(
        [
            f"[projects.{_toml_string(str(workspace))}]",
            'trust_level = "trusted"',
            "",
        ]
    )
    return "\n".join(lines).encode("utf-8")


def _runtime_environment(
    runtime_home: Path,
    command_path: str,
    canary: str,
    *,
    parent_environment: Mapping[str, str] | None = None,
) -> dict[str, str]:
    """Build the closed parent-runtime environment without serializing it."""

    source = os.environ if parent_environment is None else parent_environment
    environment = {
        "BOUNDARY_PROOF_CANARY": canary,
        "CODEX_HOME": str(runtime_home),
        "HOME": str(runtime_home),
        "PATH": command_path,
    }
    for proxy_name in PARENT_PROXY_ENVIRONMENT_NAMES:
        proxy_value = source.get(proxy_name)
        if proxy_value is not None:
            environment[proxy_name] = proxy_value
    return environment


def _normalized_config_identity(
    raw: bytes, runtime_home: Path, runtime_package: Path, workspace: Path
) -> str:
    normalized = raw
    replacements = (
        (str(runtime_package).encode(), b"runtime-package"),
        (str(runtime_home).encode(), b"runtime-home"),
        (str(workspace).encode(), b"isolated-workspace"),
    )
    for original, logical in sorted(replacements, key=lambda item: len(item[0]), reverse=True):
        if original not in normalized:
            raise BoundaryRuntimeError("config-equivalence-mismatch", "pre-turn-start")
        normalized = normalized.replace(original, logical)
    for original, _ in replacements:
        if original in normalized:
            raise BoundaryRuntimeError("config-equivalence-mismatch", "pre-turn-start")
    return _sha256(normalized)


def _normalize_config_result(
    result: dict[str, object],
    raw_config: bytes,
    runtime_home: Path,
    runtime_package: Path,
    workspace: Path,
) -> dict[str, object]:
    origins = result.get("origins")
    if not isinstance(origins, dict) or not origins:
        raise BoundaryRuntimeError("config-equivalence-mismatch", "pre-turn-start")
    origin_paths = _derive_config_origin_paths(raw_config)
    required_origin_keys = {_origin_key(path) for path in origin_paths}
    if len(required_origin_keys) != len(origin_paths):
        raise BoundaryRuntimeError("config-equivalence-mismatch", "pre-turn-start")
    if not required_origin_keys or set(origins) != required_origin_keys:
        raise BoundaryRuntimeError("config-equivalence-mismatch", "pre-turn-start")
    user_origin_count = 0
    runtime_versions: set[str] = set()
    for origin in origins.values():
        if not isinstance(origin, dict):
            raise BoundaryRuntimeError(
                "config-equivalence-mismatch", "pre-turn-start"
            )
        name = origin.get("name")
        if (
            set(origin) == {"name", "version"}
            and isinstance(name, dict)
            and set(name) == {"type", "file", "profile"}
            and name.get("type") == "user"
            and name.get("file") == str(runtime_home / "config.toml")
            and name.get("profile") is None
        ):
            version = origin.get("version")
            if (
                not isinstance(version, str)
                or IDENTITY_PATTERN.fullmatch(version) is None
            ):
                raise BoundaryRuntimeError(
                    "config-equivalence-mismatch", "pre-turn-start"
                )
            runtime_versions.add(version)
            origin["version"] = "runtime-generated-config-origin"
            user_origin_count += 1
        else:
            raise BoundaryRuntimeError(
                "config-equivalence-mismatch", "pre-turn-start"
            )
    if user_origin_count == 0 or len(runtime_versions) != 1:
        raise BoundaryRuntimeError("config-equivalence-mismatch", "pre-turn-start")
    replacements = (
        (str(runtime_package), "runtime-package"),
        (str(runtime_home), "runtime-home"),
        (str(workspace), "isolated-workspace"),
    )

    def normalize(value: object) -> object:
        if isinstance(value, dict):
            normalized: dict[str, object] = {}
            for key, nested in value.items():
                normalized_key = key
                for actual, logical in sorted(
                    replacements, key=lambda item: len(item[0]), reverse=True
                ):
                    normalized_key = normalized_key.replace(actual, logical)
                if normalized_key in normalized:
                    raise BoundaryRuntimeError(
                        "config-equivalence-mismatch", "pre-turn-start"
                    )
                normalized[normalized_key] = normalize(nested)
            return normalized
        if isinstance(value, list):
            return [normalize(item) for item in value]
        if isinstance(value, str):
            normalized_value = value
            for actual, logical in sorted(
                replacements, key=lambda item: len(item[0]), reverse=True
            ):
                normalized_value = normalized_value.replace(actual, logical)
            return normalized_value
        return value

    normalized_result = normalize(result)
    assert isinstance(normalized_result, dict)
    serialized = _canonical_json_bytes(normalized_result)
    if any(actual.encode() in serialized for actual, _ in replacements):
        raise BoundaryRuntimeError("config-equivalence-mismatch", "pre-turn-start")
    return normalized_result


def _install_auth(runtime_home: Path) -> None:
    source_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    source = source_home / "auth.json"
    if not source.is_file() or source.is_symlink():
        raise BoundaryRuntimeError("runtime-unavailable")
    target = runtime_home / "auth.json"
    try:
        shutil.copyfile(source, target, follow_symlinks=False)
        target.chmod(0o600)
    except OSError as error:
        raise BoundaryRuntimeError("runtime-unavailable") from error


class _AppServer:
    def __init__(self, executable: Path, environment: Mapping[str, str]) -> None:
        try:
            self._process = subprocess.Popen(
                (str(executable), "app-server", "--stdio", "--strict-config"),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                bufsize=1,
                env=dict(environment),
            )
        except OSError as error:
            raise BoundaryRuntimeError("experimental-api-unavailable") from error
        self._next_id = 1
        self._notifications: list[dict[str, object]] = []

    def _read_message(self, deadline: float) -> dict[str, object]:
        output = self._process.stdout
        if output is None:
            raise BoundaryRuntimeError("experimental-api-unavailable")
        while time.monotonic() < deadline:
            ready, _, _ = select.select((output,), (), (), 1)
            if not ready:
                if self._process.poll() is not None:
                    break
                continue
            line = output.readline()
            if not line:
                break
            try:
                response = json.loads(line)
            except json.JSONDecodeError as error:
                raise BoundaryRuntimeError(
                    "protocol-shape-incompatible"
                ) from error
            if not isinstance(response, dict):
                raise BoundaryRuntimeError("protocol-shape-incompatible")
            return response
        raise BoundaryRuntimeError("experimental-api-unavailable")

    def request(self, method: str, params: object | None = None) -> object:
        request_id = self._next_id
        self._next_id += 1
        message: dict[str, object] = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
        }
        if params is not None:
            message["params"] = params
        stream = self._process.stdin
        if stream is None:
            raise BoundaryRuntimeError("experimental-api-unavailable")
        try:
            stream.write(_canonical_json_bytes(message).decode("utf-8") + "\n")
            stream.flush()
        except OSError as error:
            raise BoundaryRuntimeError("experimental-api-unavailable") from error
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            response = self._read_message(deadline)
            if "method" in response and "id" not in response:
                self._notifications.append(response)
                continue
            if response.get("id") != request_id:
                continue
            if set(response) != {"id", "result"}:
                raise BoundaryRuntimeError("protocol-shape-incompatible")
            return response["result"]
        raise BoundaryRuntimeError("experimental-api-unavailable")

    def collect_turn(
        self,
        thread_id: str,
        protocol_classification: Sequence[Mapping[str, str]],
        *,
        timeout: int = 300,
    ) -> dict[str, object]:
        """Collect one classified turn and reject unknown or prohibited events."""

        classifications = {
            row.get("item_variant"): row.get("classification")
            for row in protocol_classification
        }
        if len(classifications) != len(protocol_classification):
            raise BoundaryRuntimeError(
                "protocol-item-classification-invalid", "pre-turn-start"
            )
        messages: list[str] = []
        event_methods: list[str] = []
        pending = list(self._notifications)
        self._notifications.clear()
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            response = pending.pop(0) if pending else self._read_message(deadline)
            method = response.get("method")
            if not isinstance(method, str):
                raise BoundaryRuntimeError(
                    "unexpected-prohibited-event", "in-turn"
                )
            source = "ServerRequest" if "id" in response else "ServerNotification"
            classification = classifications.get(f"{source}:{method}")
            if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
                print(
                    f"turn-observed:{source}:{method}:{classification}",
                    file=sys.stderr,
                )
            if classification is None or classification == (
                "prohibited-capability-event"
            ):
                if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
                    print(
                        f"turn-event:{source}:{method}:{classification}",
                        file=sys.stderr,
                    )
                raise BoundaryRuntimeError(
                    "unexpected-prohibited-event", "in-turn"
                )
            if "id" in response:
                raise BoundaryRuntimeError(
                    "unexpected-prohibited-event", "in-turn"
                )
            params = response.get("params")
            if not isinstance(params, dict):
                raise BoundaryRuntimeError(
                    "unexpected-prohibited-event", "in-turn"
                )
            if method == "remoteControl/status/changed" and (
                params.get("status") != "disabled"
                or params.get("environmentId") is not None
            ):
                raise BoundaryRuntimeError(
                    "unexpected-prohibited-event", "in-turn"
                )
            if method == "error":
                if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
                    print("turn-error:", repr(params), file=sys.stderr)
                raise BoundaryRuntimeError(
                    "unexpected-prohibited-event", "in-turn"
                )
            event_methods.append(method)
            if method == "item/completed":
                item = params.get("item")
                if not isinstance(item, dict):
                    raise BoundaryRuntimeError(
                        "unexpected-prohibited-event", "in-turn"
                    )
                item_type = item.get("type")
                if item_type == "agentMessage":
                    text = item.get("text")
                    if not isinstance(text, str):
                        raise BoundaryRuntimeError(
                            "unexpected-prohibited-event", "in-turn"
                        )
                    messages.append(text)
                elif item_type not in {"userMessage", "reasoning"}:
                    if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
                        print(f"turn-item:{item_type}", file=sys.stderr)
                    raise BoundaryRuntimeError(
                        "unexpected-prohibited-event", "in-turn"
                    )
            if method == "turn/completed":
                if params.get("threadId") != thread_id:
                    raise BoundaryRuntimeError(
                        "unexpected-prohibited-event", "in-turn"
                    )
                turn = params.get("turn")
                if (
                    not isinstance(turn, dict)
                    or turn.get("status") != "completed"
                    or turn.get("error") is not None
                    or len(messages) != 1
                ):
                    if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
                        print(
                            "turn-completed:",
                            repr(
                                {
                                    "thread_match": params.get("threadId")
                                    == thread_id,
                                    "turn_status": (
                                        turn.get("status")
                                        if isinstance(turn, dict)
                                        else None
                                    ),
                                    "turn_error": (
                                        turn.get("error")
                                        if isinstance(turn, dict)
                                        else None
                                    ),
                                    "message_count": len(messages),
                                }
                            ),
                            file=sys.stderr,
                        )
                    raise BoundaryRuntimeError(
                        "unexpected-prohibited-event", "in-turn"
                    )
                return {
                    "agent_message": messages[0],
                    "event_methods": event_methods,
                }
        raise BoundaryRuntimeError(
            "unexpected-prohibited-event", "in-turn"
        )

    def close(self) -> None:
        self._process.terminate()
        try:
            self._process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self._process.kill()
            self._process.wait(timeout=5)


def _expect_object(value: object, keys: set[str], diagnostic: str) -> dict[str, object]:
    if not isinstance(value, dict) or set(value) != keys:
        raise BoundaryRuntimeError(diagnostic, "pre-turn-start")
    return value


def _feature_inventory(
    server: _AppServer,
    runtime_version: str = SUPPORTED_RUNTIME_VERSION,
) -> tuple[list[dict[str, object]], list[dict[str, str]]]:
    runtime_features = RUNTIME_FEATURES_BY_VERSION.get(runtime_version)
    if runtime_features is None:
        raise BoundaryRuntimeError(
            "feature-classification-invalid", "pre-turn-start"
        )
    pages: list[dict[str, object]] = []
    items: list[dict[str, object]] = []
    cursor: str | None = None
    seen_cursors: set[str] = set()
    while True:
        result = _expect_object(
            server.request(
                "experimentalFeature/list",
                {"cursor": cursor, "limit": 25},
            ),
            {"data", "nextCursor"},
            "feature-pagination-invalid",
        )
        data = result["data"]
        next_cursor = result["nextCursor"]
        if not isinstance(data, list) or not (
            next_cursor is None or isinstance(next_cursor, str)
        ):
            raise BoundaryRuntimeError(
                "feature-pagination-invalid", "pre-turn-start"
            )
        pages.append({"items": data, "next_cursor": next_cursor})
        for item in data:
            if not isinstance(item, dict):
                raise BoundaryRuntimeError(
                    "feature-pagination-invalid", "pre-turn-start"
                )
            items.append(item)
        if next_cursor is None:
            break
        if not next_cursor or next_cursor in seen_cursors:
            raise BoundaryRuntimeError(
                "feature-pagination-invalid", "pre-turn-start"
            )
        seen_cursors.add(next_cursor)
        cursor = next_cursor
    names = [item.get("name") for item in items]
    if (
        any(not isinstance(name, str) for name in names)
        or len(names) != len(set(names))
        or set(names) != set(runtime_features)
    ):
        raise BoundaryRuntimeError(
            "feature-classification-invalid", "pre-turn-start"
        )
    classifications: list[dict[str, str]] = []
    for item in items:
        name = item["name"]
        assert isinstance(name, str)
        enabled = item.get("enabled")
        if not isinstance(enabled, bool):
            raise BoundaryRuntimeError(
                "feature-pagination-invalid", "pre-turn-start"
            )
        if name in PERMITTED_TOOL_FEATURES:
            classification = "permitted-built-in-tool"
            if not enabled:
                raise BoundaryRuntimeError(
                    "capability-inventory-mismatch", "pre-turn-start"
                )
        elif name in PERMITTED_NON_TOOL_FEATURES:
            classification = "permitted-non-tool-runtime-behavior"
        else:
            classification = "must-be-disabled-tool-bearing-behavior"
            if enabled:
                raise BoundaryRuntimeError(
                    "capability-inventory-mismatch", "pre-turn-start"
                )
        classifications.append({"feature": name, "classification": classification})
    return pages, sorted(classifications, key=lambda row: row["feature"])


def _normalize_skill_inventory(
    result: object, runtime_home: Path, workspace: Path
) -> dict[str, object]:
    envelope = _expect_object(result, {"data"}, "skill-inventory-mismatch")
    data = envelope["data"]
    if not isinstance(data, list) or len(data) != 1 or not isinstance(data[0], dict):
        raise BoundaryRuntimeError("skill-inventory-mismatch", "pre-turn-start")
    row = dict(data[0])
    if (
        set(row) != {"cwd", "errors", "skills"}
        or row["cwd"] != str(workspace)
        or row["errors"] != []
    ):
        raise BoundaryRuntimeError("skill-inventory-mismatch", "pre-turn-start")
    skills = row.get("skills")
    if not isinstance(skills, list):
        raise BoundaryRuntimeError("skill-inventory-mismatch", "pre-turn-start")
    normalized_skills: list[dict[str, object]] = []
    enabled_names: set[str] = set()
    system_names: set[str] = set()
    raw_paths: set[str] = set()
    normalized_paths: set[str] = set()
    for skill in skills:
        if not isinstance(skill, dict):
            raise BoundaryRuntimeError("skill-inventory-mismatch", "pre-turn-start")
        item = dict(skill)
        name = item.get("name")
        path_value = item.get("path")
        enabled = item.get("enabled")
        scope = item.get("scope")
        if (
            not isinstance(name, str)
            or not isinstance(path_value, str)
            or not isinstance(enabled, bool)
            or not isinstance(scope, str)
        ):
            raise BoundaryRuntimeError("skill-inventory-mismatch", "pre-turn-start")
        if name in enabled_names or name in system_names or path_value in raw_paths:
            raise BoundaryRuntimeError("skill-inventory-mismatch", "pre-turn-start")
        raw_paths.add(path_value)
        path = Path(path_value)
        try:
            relative = path.relative_to(runtime_home)
        except ValueError as error:
            raise BoundaryRuntimeError(
                "skill-inventory-mismatch", "pre-turn-start"
            ) from error
        if name in PARTICIPATING_SKILLS:
            expected = Path("skills") / name / "SKILL.md"
            if relative != expected or not enabled or scope != "user":
                raise BoundaryRuntimeError(
                    "skill-inventory-mismatch", "pre-turn-start"
                )
            enabled_names.add(name)
            normalized_path = f"manifest-skill/{name}/SKILL.md"
            item["path"] = normalized_path
            item["classification"] = "manifested-lifecycle-skill"
            skill_root = runtime_home / "skills" / name
            logical_root = f"manifest-skill/{name}"
        elif name in RUNTIME_SYSTEM_SKILLS:
            expected = Path("skills") / ".system" / name / "SKILL.md"
            if relative != expected or enabled or scope != "system":
                raise BoundaryRuntimeError(
                    "skill-inventory-mismatch", "pre-turn-start"
                )
            system_names.add(name)
            normalized_path = f"runtime-system-skill/{name}/SKILL.md"
            item["path"] = normalized_path
            item["classification"] = "disabled-runtime-system-skill"
            skill_root = runtime_home / "skills" / ".system" / name
            logical_root = f"runtime-system-skill/{name}"
        else:
            raise BoundaryRuntimeError("skill-inventory-mismatch", "pre-turn-start")
        if normalized_path in normalized_paths:
            raise BoundaryRuntimeError("skill-inventory-mismatch", "pre-turn-start")
        normalized_paths.add(normalized_path)

        def normalize_nested(value: object) -> object:
            if isinstance(value, dict):
                return {
                    key: normalize_nested(nested) for key, nested in value.items()
                }
            if isinstance(value, list):
                return [normalize_nested(nested) for nested in value]
            if isinstance(value, str) and value.startswith("/"):
                candidate = Path(value)
                try:
                    relative_path = candidate.relative_to(skill_root)
                except ValueError as error:
                    raise BoundaryRuntimeError(
                        "skill-inventory-mismatch", "pre-turn-start"
                    ) from error
                return f"{logical_root}/{relative_path.as_posix()}"
            return value

        normalized_item = normalize_nested(item)
        assert isinstance(normalized_item, dict)
        normalized_skills.append(normalized_item)
    if enabled_names != set(PARTICIPATING_SKILLS) or system_names != set(
        RUNTIME_SYSTEM_SKILLS
    ):
        raise BoundaryRuntimeError("skill-inventory-mismatch", "pre-turn-start")
    row["cwd"] = "isolated-workspace"
    row["skills"] = sorted(normalized_skills, key=lambda item: str(item["name"]))
    return {"data": [row]}


def _empty_inventory(result: object, keys: set[str]) -> dict[str, object]:
    value = _expect_object(result, keys, "capability-inventory-mismatch")
    for key, item in value.items():
        if key == "nextCursor":
            if item is not None:
                raise BoundaryRuntimeError(
                    "capability-inventory-mismatch", "pre-turn-start"
                )
        elif not isinstance(item, list) or item:
            raise BoundaryRuntimeError(
                "capability-inventory-mismatch", "pre-turn-start"
            )
    return value


def _sandbox_probe(
    executable: Path,
    environment: Mapping[str, str],
    workspace: Path,
    argv: Sequence[str],
    *,
    expect_success: bool,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    completed = _run_runtime(
        (
            str(executable),
            "sandbox",
            "--permission-profile",
            "boundary-proof-v1",
            "--include-managed-config",
            "--cd",
            str(workspace),
            "--",
            *argv,
        ),
        env=environment,
        input_text=input_text,
    )
    if (completed.returncode == 0) != expect_success:
        raise BoundaryRuntimeError("sandbox-probe-failed", "pre-turn-start")
    return completed


def _protocol_classification(schema_root: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    permitted_side_effects = {
        "ServerRequest:item/commandExecution/requestApproval",
        "ServerRequest:item/fileChange/requestApproval",
        "ServerNotification:item/commandExecution/outputDelta",
        "ServerNotification:item/commandExecution/terminalInteraction",
        "ServerNotification:item/fileChange/outputDelta",
        "ServerNotification:item/fileChange/patchUpdated",
    }
    prohibited_fragments = (
        "mcp",
        "app/",
        "plugin/",
        "realtime",
        "remoteControl",
        "permissions/requestApproval",
        "tool/requestUserInput",
        "item/tool/call",
        "attestation/generate",
    )
    for stem in (
        "ClientRequest",
        "ClientNotification",
        "ServerRequest",
        "ServerNotification",
    ):
        path = schema_root / f"{stem}.json"
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise BoundaryRuntimeError(
                "protocol-item-classification-invalid", "pre-turn-start"
            ) from error
        methods: set[str] = set()

        def visit(value: object) -> None:
            if isinstance(value, dict):
                properties = value.get("properties")
                method = (
                    properties.get("method")
                    if isinstance(properties, dict)
                    else None
                )
                enum = method.get("enum") if isinstance(method, dict) else None
                if (
                    isinstance(enum, list)
                    and len(enum) == 1
                    and isinstance(enum[0], str)
                ):
                    methods.add(enum[0])
                for nested in value.values():
                    visit(nested)
            elif isinstance(value, list):
                for nested in value:
                    visit(nested)

        visit(document)
        if not methods:
            raise BoundaryRuntimeError(
                "protocol-item-classification-invalid", "pre-turn-start"
            )
        for method in methods:
            variant = f"{stem}:{method}"
            if variant in permitted_side_effects:
                classification = "permitted-side-effect"
            elif method == "remoteControl/status/changed":
                classification = "non-side-effect-protocol-traffic"
            elif any(fragment in method for fragment in prohibited_fragments):
                classification = "prohibited-capability-event"
            else:
                classification = "non-side-effect-protocol-traffic"
            rows.append(
                {"item_variant": variant, "classification": classification}
            )
    variants = [row["item_variant"] for row in rows]
    if len(variants) != len(set(variants)):
        raise BoundaryRuntimeError(
            "protocol-item-classification-invalid", "pre-turn-start"
        )
    return sorted(rows, key=lambda row: row["item_variant"])


def _validate_runtime_projection(
    version: str,
    schema_identity: str,
    protocol_classification: Sequence[Mapping[str, str]],
) -> None:
    if RUNTIME_SCHEMA_IDENTITY_BY_VERSION.get(version) != schema_identity:
        raise BoundaryRuntimeError("schema-bundle-invalid")
    if (
        RUNTIME_PROTOCOL_CLASSIFICATION_IDENTITY_BY_VERSION.get(version)
        != _sha256(_canonical_json_bytes(protocol_classification))
    ):
        raise BoundaryRuntimeError(
            "protocol-item-classification-invalid", "pre-turn-start"
        )


def _validated_thread_metadata(
    thread: object,
    *,
    version: str,
    model_id: str,
    workspace: Path,
) -> tuple[dict[str, object], str]:
    if not isinstance(thread, dict):
        raise BoundaryRuntimeError("thread-metadata-mismatch", "pre-turn-start")
    required_thread = {
        "thread",
        "model",
        "modelProvider",
        "serviceTier",
        "cwd",
        "runtimeWorkspaceRoots",
        "instructionSources",
        "approvalPolicy",
        "approvalsReviewer",
        "sandbox",
        "activePermissionProfile",
        "reasoningEffort",
        "multiAgentMode",
    }
    if set(thread) != required_thread:
        raise BoundaryRuntimeError("thread-metadata-mismatch", "pre-turn-start")
    thread_record = thread["thread"]
    active_profile = thread["activePermissionProfile"]
    sandbox = thread["sandbox"]
    expected_runtime_roots: list[str]
    expected_sandbox_type: str
    if version == "0.145.0":
        expected_runtime_roots = []
        expected_sandbox_type = "readOnly"
    else:
        expected_runtime_roots = [str(workspace)]
        expected_sandbox_type = "workspaceWrite"
    if (
        not isinstance(thread_record, dict)
        or not isinstance(thread_record.get("id"), str)
        or thread_record.get("cliVersion") != version
        or thread.get("model") != model_id
        or thread.get("modelProvider") != "openai"
        or thread.get("cwd") != str(workspace)
        or thread.get("runtimeWorkspaceRoots") != expected_runtime_roots
        or thread.get("instructionSources") != []
        or active_profile != {"id": "boundary-proof-v1", "extends": None}
        or not isinstance(sandbox, dict)
        or sandbox.get("type") != expected_sandbox_type
        or sandbox.get("networkAccess") is not False
    ):
        raise BoundaryRuntimeError("thread-metadata-mismatch", "pre-turn-start")
    return (
        {
            "cli_version": version,
            "model_id": model_id,
            "model_provider": "openai",
            "active_permission_profile": "boundary-proof-v1",
            "workspace_root_roles": (
                [] if not expected_runtime_roots else ["isolated-workspace"]
            ),
            "instruction_source_refs": [],
            "runtime_default_instruction_source": "identified-runtime-substrate",
            "cwd_role": "isolated-workspace",
        },
        thread_record["id"],
    )


def _thread_start_request(workspace: Path, model_id: str) -> dict[str, object]:
    return {
        "cwd": str(workspace),
        "dynamicTools": [],
        "environments": [],
        "ephemeral": True,
        "effort": "low",
        "model": model_id,
        "modelProvider": "openai",
        "permissions": "boundary-proof-v1",
        "runtimeWorkspaceRoots": [str(workspace)],
    }


def _turn_start_request(
    thread_id: str,
    workspace: Path,
    model_id: str,
    runtime_home: Path,
    prompt: str,
    output_schema: Mapping[str, object],
    skill_names: Sequence[str] = PARTICIPATING_SKILLS,
) -> dict[str, object]:
    if (
        not skill_names
        or len(skill_names) != len(set(skill_names))
        or any(name not in PARTICIPATING_SKILLS for name in skill_names)
    ):
        raise BoundaryRuntimeError("protocol-shape-incompatible", "pre-turn-start")
    skill_inputs = [
        {
            "type": "skill",
            "name": name,
            "path": str(runtime_home / "skills" / name / "SKILL.md"),
        }
        for name in skill_names
    ]
    return {
        "threadId": thread_id,
        "input": [*skill_inputs, {"type": "text", "text": prompt}],
        "cwd": str(workspace),
        "model": model_id,
        "permissions": "boundary-proof-v1",
        "runtimeWorkspaceRoots": [str(workspace)],
        "environments": [],
        "effort": "low",
        "outputSchema": dict(output_schema),
    }


def _collect_runtime_attestation(
    command: str = "codex",
    *,
    repo_root: Path = ROOT,
    generation_request: Mapping[str, object] | None = None,
    generation_sink: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    """Collect the trusted attestation or fail at the first unproved boundary."""

    executable = _resolved_regular_executable(command)
    launcher_before = _read_file_identity(executable)
    version = _runtime_version(executable)
    package_root = _runtime_package(executable, version)
    _, package_identity = _bundle_projection(package_root, "runtime-unreadable")
    with (
        tempfile.TemporaryDirectory(prefix="boundary-proof-schema-") as schema_raw,
        tempfile.TemporaryDirectory(prefix="boundary-proof-home-") as home_raw,
        tempfile.TemporaryDirectory(prefix="boundary-proof-workspace-") as work_raw,
    ):
        schema_root = Path(schema_raw)
        runtime_home = Path(home_raw)
        workspace = Path(work_raw)
        runtime_home.chmod(0o700)
        workspace.chmod(0o700)
        completed = _run_runtime(
            (
                str(executable),
                "app-server",
                "generate-json-schema",
                "--experimental",
                "--out",
                str(schema_root),
            ),
            timeout=60,
        )
        if completed.returncode != 0:
            raise BoundaryRuntimeError("schema-bundle-invalid")
        _, schema_identity = _schema_bundle_projection(schema_root)
        if version != SUPPORTED_RUNTIME_VERSION:
            raise BoundaryRuntimeError("schema-bundle-invalid")
        if (
            _read_file_identity(executable) != launcher_before
            or _bundle_projection(package_root, "runtime-unreadable")[1]
            != package_identity
        ):
            raise BoundaryRuntimeError("runtime-identity-unstable")

        _copy_participating_skills(runtime_home)
        _install_auth(runtime_home)
        model_id = "gpt-5.6-sol"
        node = shutil.which("node")
        if node is None:
            raise BoundaryRuntimeError("runtime-unavailable")
        command_path = f"{Path(node).parent}:/usr/bin:/bin"
        config = _generated_config(
            runtime_home,
            package_root,
            workspace,
            model_id,
            version,
            command_path,
        )
        config_path = runtime_home / "config.toml"
        try:
            config_path.write_bytes(config)
            config_path.chmod(0o600)
        except OSError as error:
            raise BoundaryRuntimeError("runtime-unavailable") from error
        config_identity = _normalized_config_identity(
            config, runtime_home, package_root, workspace
        )
        canary = "boundary-proof-" + secrets.token_hex(32)
        environment = _runtime_environment(runtime_home, command_path, canary)
        probe_source = workspace / "manifested.txt"
        probe_source.write_text("manifested\n", encoding="utf-8")

        _sandbox_probe(
            executable,
            environment,
            workspace,
            ("/bin/cat", str(probe_source)),
            expect_success=True,
        )
        environment_probe = _run_runtime(
            (
                str(executable),
                "sandbox",
                "--permission-profile",
                "boundary-proof-v1",
                "--include-managed-config",
                "--cd",
                str(workspace),
                "--",
                "/usr/bin/env",
            ),
            env=environment,
        )
        if environment_probe.returncode != 0:
            if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
                print(
                    "credential-environment-command:",
                    environment_probe.returncode,
                    environment_probe.stderr,
                    file=sys.stderr,
                )
            raise BoundaryRuntimeError(
                "credential-isolation-failed", "pre-turn-start"
            )
        environment_rows = environment_probe.stdout.splitlines()
        environment_values = {
            row.partition("=")[0]: row.partition("=")[2]
            for row in environment_rows
            if "=" in row
        }
        if (
            set(environment_values)
            != {"CODEX_SANDBOX_NETWORK_DISABLED", "PATH", "PWD"}
            or environment_values["PATH"] != command_path
            or environment_values["PWD"] != str(workspace)
            or environment_values["CODEX_SANDBOX_NETWORK_DISABLED"] != "1"
            or canary in environment_probe.stdout
            or canary in environment_probe.stderr
        ):
            if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
                print(
                    "credential-environment-values:",
                    repr(environment_values),
                    file=sys.stderr,
                )
            raise BoundaryRuntimeError(
                "credential-isolation-failed", "pre-turn-start"
            )
        canary_digest = hashlib.sha256(canary.encode()).hexdigest()
        argv_probe = _sandbox_probe(
            executable,
            environment,
            workspace,
            (
                "/usr/bin/python3",
                "-c",
                "import hashlib,sys;"
                f"d={canary_digest!r};"
                "raise SystemExit(9 if any(hashlib.sha256(v.encode()).hexdigest()==d "
                "for v in sys.argv) else 0)",
            ),
            expect_success=True,
        )
        stdin_probe = _sandbox_probe(
            executable,
            environment,
            workspace,
            (
                "/usr/bin/python3",
                "-c",
                "import hashlib,sys;"
                f"d={canary_digest!r};v=sys.stdin.read();"
                "raise SystemExit(9 if hashlib.sha256(v.encode()).hexdigest()==d else 0)",
            ),
            expect_success=True,
            input_text="",
        )
        if canary in argv_probe.stdout + argv_probe.stderr + stdin_probe.stdout + stdin_probe.stderr:
            if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
                print("credential-argv-stdin", file=sys.stderr)
            raise BoundaryRuntimeError(
                "credential-isolation-failed", "pre-turn-start"
            )
        for proxy_name in PARENT_PROXY_ENVIRONMENT_NAMES:
            proxy_environment = _runtime_environment(
                runtime_home,
                command_path,
                canary,
                parent_environment={proxy_name: f"http://{canary}.invalid"},
            )
            proxy_probe = _sandbox_probe(
                executable,
                proxy_environment,
                workspace,
                ("/usr/bin/env",),
                expect_success=True,
            )
            if (
                proxy_name in {
                    row.partition("=")[0]
                    for row in proxy_probe.stdout.splitlines()
                    if "=" in row
                }
                or canary in proxy_probe.stdout
                or canary in proxy_probe.stderr
            ):
                if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
                    print(f"credential-proxy:{proxy_name}", file=sys.stderr)
                raise BoundaryRuntimeError(
                    "credential-isolation-failed", "pre-turn-start"
                )
        _sandbox_probe(
            executable,
            environment,
            workspace,
            (
                "/usr/bin/python3",
                "-c",
                "from pathlib import Path;Path('probe-output.txt').write_text('ok')",
            ),
            expect_success=True,
        )
        _sandbox_probe(
            executable,
            environment,
            workspace,
            ("/bin/cat", str(repo_root / "CONSTITUTION.md")),
            expect_success=False,
        )
        _sandbox_probe(
            executable,
            environment,
            workspace,
            ("/bin/cat", str(runtime_home / "auth.json")),
            expect_success=False,
        )
        _sandbox_probe(
            executable,
            environment,
            workspace,
            (
                "/usr/bin/python3",
                "-c",
                "import socket,sys\n"
                "try:\n"
                " s=socket.socket();s.settimeout(1);s.connect(('1.1.1.1',53))\n"
                "except OSError:sys.exit(0)\n"
                "sys.exit(9)",
            ),
            expect_success=True,
        )
        process_metadata_probe = _sandbox_probe(
            executable,
            environment,
            workspace,
            (
                "/usr/bin/python3",
                "-c",
                "import hashlib,pathlib,re,sys\n"
                f"paths={[f'/proc/{os.getpid()}/{name}' for name in ('environ', 'cmdline', 'status')]!r}\n"
                f"d={canary_digest!r}\n"
                "for value in paths:\n"
                " try:raw=pathlib.Path(value).read_bytes()\n"
                " except OSError:continue\n"
                " for token in re.split(b'[\\\\x00\\\\s:=]+',raw):\n"
                "  if hashlib.sha256(token).hexdigest()==d:sys.exit(9)\n"
                "sys.exit(0)",
            ),
            expect_success=True,
        )
        if canary in process_metadata_probe.stdout + process_metadata_probe.stderr:
            if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
                print("credential-process-output", file=sys.stderr)
            raise BoundaryRuntimeError(
                "credential-isolation-failed", "pre-turn-start"
            )
        if (
            _read_file_identity(executable) != launcher_before
            or _bundle_projection(package_root, "runtime-unreadable")[1]
            != package_identity
        ):
            raise BoundaryRuntimeError(
                "runtime-identity-unstable", "pre-turn-start"
            )

        protocol_classification = _protocol_classification(schema_root)
        _validate_runtime_projection(
            version, schema_identity, protocol_classification
        )
        server = _AppServer(executable, environment)
        try:
            initialize = server.request(
                "initialize",
                {
                    "clientInfo": {"name": "boundary-proof", "version": "1"},
                    "capabilities": {"experimentalApi": True},
                },
            )
            if not isinstance(initialize, dict):
                raise BoundaryRuntimeError("experimental-api-unavailable")
            pages, feature_classification = _feature_inventory(server, version)
            config_result = _expect_object(
                server.request(
                    "config/read",
                    {"cwd": str(workspace), "includeLayers": False},
                ),
                {"config", "origins"},
                "capability-inventory-mismatch",
            )
            effective_config = config_result.get("config")
            if (
                not isinstance(effective_config, dict)
                or effective_config.get("model") != model_id
                or effective_config.get("model_provider") != "openai"
                or effective_config.get("default_permissions")
                != "boundary-proof-v1"
                or effective_config.get("sandbox_mode") is not None
            ):
                raise BoundaryRuntimeError(
                    "config-equivalence-mismatch", "pre-turn-start"
                )
            config_result = _normalize_config_result(
                config_result,
                config,
                runtime_home,
                package_root,
                workspace,
            )
            requirements = _expect_object(
                server.request("configRequirements/read", {}),
                {"requirements"},
                "capability-inventory-mismatch",
            )
            apps = _empty_inventory(
                server.request("app/list", {"limit": 100}),
                {"data", "nextCursor"},
            )
            plugins = _empty_inventory(
                server.request("plugin/list", {"cwds": [str(workspace)]}),
                {"marketplaces", "marketplaceLoadErrors", "featuredPluginIds"},
            )
            mcp = _empty_inventory(
                server.request("mcpServerStatus/list", {"limit": 100}),
                {"data", "nextCursor"},
            )
            skills = _normalize_skill_inventory(
                server.request(
                    "skills/list",
                    {"cwds": [str(workspace)], "forceReload": True},
                ),
                runtime_home,
                workspace,
            )
            thread = server.request(
                "thread/start",
                _thread_start_request(workspace, model_id),
            )
            thread_metadata, thread_id = _validated_thread_metadata(
                thread,
                version=version,
                model_id=model_id,
                workspace=workspace,
            )
            if generation_request is not None:
                prompt = generation_request.get("prompt")
                output_schema = generation_request.get("output_schema")
                skill_names = generation_request.get("skill_names")
                if not isinstance(prompt, str) or not isinstance(
                    output_schema, dict
                ) or not isinstance(skill_names, list) or any(
                    not isinstance(name, str) for name in skill_names
                ):
                    raise BoundaryRuntimeError(
                        "protocol-shape-incompatible", "pre-turn-start"
                    )
                started = server.request(
                    "turn/start",
                    _turn_start_request(
                        thread_id,
                        workspace,
                        model_id,
                        runtime_home,
                        prompt,
                        output_schema,
                        skill_names,
                    ),
                )
                if (
                    not isinstance(started, dict)
                    or set(started) != {"turn"}
                    or not isinstance(started["turn"], dict)
                    or not isinstance(started["turn"].get("id"), str)
                ):
                    raise BoundaryRuntimeError(
                        "protocol-shape-incompatible", "in-turn"
                    )
                generation_result = server.collect_turn(
                    thread_id, protocol_classification
                )
                if generation_sink is None:
                    raise BoundaryRuntimeError(
                        "protocol-shape-incompatible", "in-turn"
                    )
                generation_result["thread_id"] = thread_id
                generation_result["stage"] = generation_request.get("stage")
                generation_result["skill_names"] = list(skill_names)
                generation_sink.append(generation_result)
        finally:
            server.close()
        if (
            _read_file_identity(executable) != launcher_before
            or _bundle_projection(package_root, "runtime-unreadable")[1]
            != package_identity
        ):
            raise BoundaryRuntimeError(
                "runtime-identity-unstable", "pre-turn-start"
            )
        capability_inventory = {
            "config/read": config_result,
            "app/list": apps,
            "plugin/list": plugins,
            "mcpServerStatus/list": mcp,
        }
        return {
            "schema_version": "boundary-runtime-attestation-v1",
            "runtime_launcher_identity": launcher_before.digest,
            "runtime_package_identity": package_identity,
            "schema_bundle_identity": schema_identity,
            "generated_config_identity": config_identity,
            "managed_requirements_identity": _sha256(
                _canonical_json_bytes(requirements)
            ),
            "active_permission_profile": "boundary-proof-v1",
            "thread_metadata": thread_metadata,
            "feature_inventory_identity": _sha256(_canonical_json_bytes(pages)),
            "capability_inventory_identity": _sha256(
                _canonical_json_bytes(capability_inventory)
            ),
            "skill_inventory_identity": _sha256(_canonical_json_bytes(skills)),
            "feature_classification_identity": _sha256(
                _canonical_json_bytes(feature_classification)
            ),
            "protocol_item_classification_identity": _sha256(
                _canonical_json_bytes(protocol_classification)
            ),
            "probe_results": {
                "workspace_read": "pass",
                "workspace_write": "pass",
                "unmanifested_source_denied": "pass",
                "private_auth_denied": "pass",
                "network_denied": "pass",
            },
            "credential_isolation_results": {
                "environment_names_closed": "pass",
                "canary_absent_from_environment": "pass",
                "canary_absent_from_argv": "pass",
                "canary_absent_from_stdin": "pass",
                "private_paths_unreadable": "pass",
                "process_metadata_unreadable": "pass",
            },
        }


def _validate_attestation(attestation: Mapping[str, object]) -> None:
    if set(attestation) != set(ATTESTATION_FIELDS):
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    if attestation.get("schema_version") != "boundary-runtime-attestation-v1":
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    for field in ATTESTATION_FIELDS:
        if field.endswith("_identity") and (
            not isinstance(attestation[field], str)
            or IDENTITY_PATTERN.fullmatch(attestation[field]) is None
        ):
            raise BoundaryRuntimeError("protocol-shape-incompatible")
    if attestation.get("active_permission_profile") != "boundary-proof-v1":
        raise BoundaryRuntimeError("permission-profile-mismatch", "pre-turn-start")
    thread_metadata = attestation.get("thread_metadata")
    expected_thread_fields = {
        "cli_version",
        "model_id",
        "model_provider",
        "active_permission_profile",
        "workspace_root_roles",
        "instruction_source_refs",
        "runtime_default_instruction_source",
        "cwd_role",
    }
    if (
        not isinstance(thread_metadata, dict)
        or set(thread_metadata) != expected_thread_fields
        or thread_metadata.get("cli_version") != SUPPORTED_RUNTIME_VERSION
        or not isinstance(thread_metadata.get("model_id"), str)
        or re.fullmatch(
            r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}",
            thread_metadata["model_id"],
        )
        is None
        or not isinstance(thread_metadata.get("model_provider"), str)
        or re.fullmatch(
            r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}",
            thread_metadata["model_provider"],
        )
        is None
        or thread_metadata.get("active_permission_profile")
        != "boundary-proof-v1"
        or thread_metadata.get("workspace_root_roles") != []
        or not isinstance(thread_metadata.get("instruction_source_refs"), list)
        or any(
            not isinstance(reference, str)
            for reference in thread_metadata["instruction_source_refs"]
        )
        or thread_metadata.get("runtime_default_instruction_source")
        not in {"runtime-default", "identified-runtime-substrate"}
        or thread_metadata.get("cwd_role") != "isolated-workspace"
    ):
        raise BoundaryRuntimeError("thread-metadata-mismatch", "pre-turn-start")
    expected_probe_keys = {
        "workspace_read",
        "workspace_write",
        "unmanifested_source_denied",
        "private_auth_denied",
        "network_denied",
    }
    expected_credential_keys = {
        "environment_names_closed",
        "canary_absent_from_environment",
        "canary_absent_from_argv",
        "canary_absent_from_stdin",
        "private_paths_unreadable",
        "process_metadata_unreadable",
    }
    probe_results = attestation.get("probe_results")
    credential_results = attestation.get("credential_isolation_results")
    if (
        not isinstance(probe_results, dict)
        or set(probe_results) != expected_probe_keys
        or set(probe_results.values()) != {"pass"}
    ):
        raise BoundaryRuntimeError("sandbox-probe-failed", "pre-turn-start")
    if (
        not isinstance(credential_results, dict)
        or set(credential_results) != expected_credential_keys
        or set(credential_results.values()) != {"pass"}
    ):
        raise BoundaryRuntimeError(
            "credential-isolation-failed", "pre-turn-start"
        )


def _publish_attestation(
    repo_root: Path, change_id: str, attestation: Mapping[str, object]
) -> dict[str, str]:
    evidence_root = repo_root / "docs" / "changes" / change_id / "evidence"
    try:
        try:
            metadata = evidence_root.lstat()
        except FileNotFoundError:
            change_root = evidence_root.parent
            change_metadata = change_root.lstat()
            if stat.S_ISLNK(change_metadata.st_mode) or not stat.S_ISDIR(
                change_metadata.st_mode
            ):
                raise BoundaryRuntimeError("runtime-unavailable")
            evidence_root.mkdir(mode=0o700)
            parent_descriptor = os.open(change_root, os.O_RDONLY)
            try:
                os.fsync(parent_descriptor)
            finally:
                os.close(parent_descriptor)
            metadata = evidence_root.lstat()
    except OSError as error:
        raise BoundaryRuntimeError("runtime-unavailable") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise BoundaryRuntimeError("runtime-unavailable")
    target = evidence_root / "runtime-preflight-attestation.json"
    raw = _canonical_json_bytes(attestation)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".runtime-preflight-attestation.",
        suffix=".tmp",
        dir=evidence_root,
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "wb", closefd=True) as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
        directory = os.open(evidence_root, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    except OSError as error:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        raise BoundaryRuntimeError("runtime-unavailable") from error
    return {
        "path": target.relative_to(repo_root).as_posix(),
        "identity": _sha256(raw),
    }


def assess_environment(
    change_id: str, *, repo_root: Path = ROOT, command: str = "codex"
) -> dict[str, object]:
    """Return the exact bounded preflight receipt."""

    try:
        _select_change_root(repo_root, change_id)
        attestation = _collect_runtime_attestation(command, repo_root=repo_root)
        _validate_attestation(attestation)
        attestation_ref = _publish_attestation(repo_root, change_id, attestation)
    except BoundaryRuntimeError as error:
        return _preflight_failure(error.diagnostic_id, error.phase)
    return {
        "schema_version": "boundary-runtime-preflight-v1",
        "result": "pass",
        "diagnostic_id": "none",
        "phase": "pre-turn-start",
        "attestation_ref": attestation_ref,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    environment = subparsers.add_parser(
        "check-environment",
        help="run the evidence-only runtime boundary feasibility transaction",
    )
    environment.add_argument("--change-id", required=True)
    environment.add_argument(
        "--json",
        action="store_true",
        help="emit the exact bounded preflight receipt as canonical JSON",
    )
    baseline = subparsers.add_parser(
        "freeze-baseline",
        help="write or validate the immutable pre-skill-mutation baseline",
    )
    baseline.add_argument("--change-id", required=True)
    generate = subparsers.add_parser(
        "generate",
        help="generate and publish one fresh immutable upstream behavior run",
    )
    generate.add_argument("--change-id", required=True)
    generate.add_argument("--scenario", required=True, type=Path)
    validate = subparsers.add_parser(
        "validate",
        help="validate the current immutable run without lifecycle reinvocation",
    )
    validate.add_argument("--change-id", required=True)
    fixture = subparsers.add_parser(
        "exercise-fixture",
        help="exercise the controlled parser and oracle fixture",
    )
    fixture.add_argument("--fixture", required=True, type=Path)
    fixture.add_argument("--output-root", required=True, type=Path)
    fixture_validation = subparsers.add_parser(
        "validate-fixture",
        help="validate controlled fixture evidence without regeneration",
    )
    fixture_validation.add_argument("--root", required=True, type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "check-environment":
        result = assess_environment(args.change_id)
        if args.json:
            print(_canonical_json_bytes(result).decode("utf-8"))
        else:
            print(f"{result['result']}: {result['diagnostic_id']}")
        return 0 if result["result"] == "pass" else 2
    if args.command == "freeze-baseline":
        try:
            result = freeze_baseline(args.change_id)
        except BoundaryRuntimeError as error:
            print(f"fail: {error.diagnostic_id}")
            return 2
        print(_canonical_json_bytes(result).decode("utf-8"))
        return 0
    try:
        if args.command == "generate":
            result = generate_behavior(args.change_id, args.scenario)
        elif args.command == "validate":
            result = validate_behavior(args.change_id)
        elif args.command == "exercise-fixture":
            result = exercise_fixture(args.fixture, args.output_root)
        elif args.command == "validate-fixture":
            result = validate_fixture(args.root)
        else:
            raise AssertionError(f"unknown command: {args.command}")
    except (BoundaryRuntimeError, BoundaryProofError, OSError) as error:
        diagnostic = (
            error.diagnostic_id
            if isinstance(error, BoundaryRuntimeError)
            else "runtime-identity-unstable"
        )
        print(f"fail: {diagnostic}")
        return 2
    print(_canonical_json_bytes(result).decode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
