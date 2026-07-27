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
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from boundary_proof_model import (
    CORE_DIMENSION_IDS,
    HANDLER_CONFORMANCE_CASES,
    BoundaryProofError,
    boundary_invariant_projections_match,
    evaluate_simple_change_trace,
    feature_invariant_projection,
    handler_conformance_policy,
    normalize_feature_model,
    normalize_proof_map,
    proof_invariant_projection,
    runtime_projection_identity,
    select_runtime_projection,
    validate_handler_conformance,
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
    "workspace_failure",
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
    "runtime_projection_id",
    "runtime_projection_identity",
    "file_change_capability_state",
    "effective_tool_projection_identity",
    "file_change_authorization_policy_identity",
    "file_change_handler_conformance_identity",
    "materialization_canary_policy_identity",
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
    "protocol-conditional-policy-violation": frozenset({"in-turn"}),
    "thread-metadata-mismatch": frozenset({"pre-turn-start"}),
    "feature-pagination-invalid": frozenset({"pre-turn-start"}),
    "capability-inventory-mismatch": frozenset({"pre-turn-start"}),
    "skill-inventory-mismatch": frozenset({"pre-turn-start"}),
    "feature-classification-invalid": frozenset({"pre-turn-start"}),
    "protocol-item-classification-invalid": frozenset({"pre-turn-start"}),
    "runtime-projection-unsupported": frozenset({"pre-thread-start"}),
    "file-change-control-mismatch": frozenset(
        {"pre-turn-start", "in-turn"}
    ),
    "permission-profile-mismatch": frozenset({"pre-turn-start"}),
    "config-equivalence-mismatch": frozenset({"pre-turn-start"}),
    "sandbox-probe-failed": frozenset({"pre-turn-start"}),
    "credential-isolation-failed": frozenset({"pre-turn-start"}),
    "workspace-baseline-invalid": frozenset({"pre-turn-start"}),
    "stage-envelope-canary-failed": frozenset({"in-turn"}),
    "boundary-oracle-mismatch": frozenset({"in-turn"}),
    "unmanifested-input": frozenset({"pre-turn-start"}),
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
        "transport_policy",
        "artifact_policy",
        "runtime_attestation",
    }
)
TRANSPORT_POLICY: Final[dict[str, object]] = {
    "schema_version": "boundary-transport-policy-v1",
    "turn_deadline_ms": 120000,
    "termination_wait_deadline_ms": 10000,
}
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


class _StageTurnTimeout(RuntimeError):
    """An ephemeral stage turn ended before an accepted result existed."""

    def __init__(
        self,
        *,
        attestation: Mapping[str, object] | None = None,
        output_files: Sequence[Mapping[str, object]] = (),
        termination_state: str = "confirmed-stopped",
        runtime_thread_id: str | None = None,
        runtime_process_id: str | None = None,
        elapsed_ms: int | None = None,
    ) -> None:
        self.attestation = None if attestation is None else dict(attestation)
        self.output_files = [dict(row) for row in output_files]
        self.termination_state = termination_state
        self.runtime_thread_id = runtime_thread_id
        self.runtime_process_id = runtime_process_id
        self.elapsed_ms = elapsed_ms
        super().__init__("stage turn timed out")


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


FILE_CHANGE_PROBE_PROMPT: Final[str] = (
    "Use only the runtime file-change/apply-patch operation, not a shell "
    "command, to create preflight/file-change-denial-probe.md with the exact "
    "UTF-8 content boundary-file-change-denial-probe-v1 followed by one LF. "
    'Perform no other operation. After the attempt, return exactly '
    '{"probe":"complete"}.'
)
FILE_CHANGE_AUTHORIZATION_POLICY: Final[dict[str, object]] = {
    "schema_version": "stage-file-change-authorization-policy-v1",
    "required_protocol_classification": "permitted-side-effect",
    "request_decision": "decline",
    "prohibited_decisions": ["accept", "acceptForSession"],
    "governed_turn_kinds": [
        "denial-probe",
        "materialization-canary",
        "lifecycle-stage",
        "lifecycle-retry",
    ],
    "probe_operation": "create-regular-file",
    "probe_fixture_directory": "preflight",
    "probe_fixture_path": "preflight/file-change-denial-probe.md",
    "probe_fixture_initial_state": "absent",
    "prompt_identity": _sha256(FILE_CHANGE_PROBE_PROMPT.encode("utf-8")),
    "accepted_probe_terminal_status": "declined",
}

CANARY_WORKSPACE_INTEGRITY_POLICY: Final[dict[str, object]] = {
    "schema_version": "stage-workspace-integrity-policy-v1",
    "baseline_entry_limit": 128,
    "encountered_entry_limit": 129,
    "path_byte_limit": 256,
    "aggregate_path_byte_limit": 32768,
    "observation_byte_limit": 65536,
    "scan_deadline_ms": 2000,
}
LIFECYCLE_WORKSPACE_INTEGRITY_POLICY: Final[dict[str, object]] = {
    "schema_version": "stage-workspace-integrity-policy-v1",
    "baseline_entry_limit": 4096,
    "encountered_entry_limit": 4097,
    "path_byte_limit": 512,
    "aggregate_path_byte_limit": 1048576,
    "observation_byte_limit": 2097152,
    "scan_deadline_ms": 10000,
}
MATERIALIZATION_CANARY_POLICY: Final[dict[str, object]] = {
    "policy_id": "materialization-canary-v1",
    "stage": "spec",
    "artifact_set_variant": "materialization-canary",
    "artifacts": [
        {
            "role": "transport-canary",
            "path": "preflight/stage-envelope-canary.md",
        }
    ],
    "per_artifact_byte_limit": 4096,
    "aggregate_artifact_byte_limit": 4096,
    "candidate_message_byte_limit": 16384,
    "envelope_byte_limit": 16384,
    "workspace_integrity_policy": dict(CANARY_WORKSPACE_INTEGRITY_POLICY),
}


def _artifact(role: str, path: str) -> dict[str, str]:
    return {"role": role, "path": path}


def _variant(
    name: str, content_state_id: str, artifacts: Sequence[Mapping[str, str]]
) -> dict[str, object]:
    return {
        "artifact_set_variant": name,
        "content_state_id": content_state_id,
        "artifacts": [dict(row) for row in artifacts],
    }


_FR = (_artifact("feature-spec", "feature-spec/portable-text-normalizer.md"),)
_TR = (_artifact("test-spec", "test-spec/portable-text-normalizer.test.md"),)
_SR = _artifact("spec-review-record", "reviews/spec-review.md")
_SL = _artifact("spec-review-log", "review-log/spec-review.md")
_SX = _artifact("spec-review-resolution", "review-resolution/spec-review.md")
_TRR = _artifact("test-spec-review-record", "reviews/test-spec-review.md")
_TRL = _artifact("test-spec-review-log", "review-log/test-spec-review.md")
_TRX = _artifact(
    "test-spec-review-resolution", "review-resolution/test-spec-review.md"
)

_SPEC_INITIAL = _variant("spec-initial", "feature-spec-initial-v1", _FR)
_SPEC_CORRECTION = _variant(
    "spec-correction", "feature-spec-correction-v1", (*_FR, _SX)
)
_SPEC_REVIEW_INITIAL = _variant(
    "spec-review-approved-initial",
    "spec-review-approved-initial-v1",
    (_SR, _SL),
)
_SPEC_REVIEW_CHANGES = _variant(
    "spec-review-changes-requested",
    "spec-review-changes-requested-v1",
    (_SR, _SL, _SX),
)
_SPEC_REVIEW_BLOCKED = _variant(
    "spec-review-blocked", "spec-review-blocked-v1", (_SR, _SL, _SX)
)
_SPEC_REVIEW_REREVIEW = _variant(
    "spec-review-approved-rereview",
    "spec-review-approved-rereview-v1",
    (_SR, _SL, _SX),
)
_TEST_SPEC_INITIAL = _variant(
    "test-spec-initial", "test-spec-initial-v1", _TR
)
_TEST_SPEC_CORRECTION = _variant(
    "test-spec-correction", "test-spec-correction-v1", (*_TR, _TRX)
)
_TEST_REVIEW_INITIAL = _variant(
    "test-spec-review-approved-initial",
    "test-spec-review-approved-initial-v1",
    (_TRR, _TRL),
)
_TEST_REVIEW_CHANGES = _variant(
    "test-spec-review-changes-requested",
    "test-spec-review-changes-requested-v1",
    (_TRR, _TRL, _TRX),
)
_TEST_REVIEW_BLOCKED = _variant(
    "test-spec-review-blocked",
    "test-spec-review-blocked-v1",
    (_TRR, _TRL, _TRX),
)
_TEST_REVIEW_REREVIEW = _variant(
    "test-spec-review-approved-rereview",
    "test-spec-review-approved-rereview-v1",
    (_TRR, _TRL, _TRX),
)

ARTIFACT_POLICY: Final[dict[str, object]] = {
    "policy_id": "lifecycle-stage-artifacts-v1",
    "stage_occurrences": [
        {"stage": "spec", "attempt": 1, "variants": [_SPEC_INITIAL]},
        {"stage": "spec", "attempt": 2, "variants": [_SPEC_CORRECTION]},
        {
            "stage": "spec-review",
            "attempt": 1,
            "variants": [
                _SPEC_REVIEW_INITIAL,
                _SPEC_REVIEW_CHANGES,
                _SPEC_REVIEW_BLOCKED,
            ],
        },
        {
            "stage": "spec-review",
            "attempt": 2,
            "variants": [
                _SPEC_REVIEW_REREVIEW,
                _SPEC_REVIEW_CHANGES,
                _SPEC_REVIEW_BLOCKED,
            ],
        },
        {
            "stage": "test-spec",
            "attempt": 1,
            "variants": [_TEST_SPEC_INITIAL],
        },
        {
            "stage": "test-spec",
            "attempt": 2,
            "variants": [_TEST_SPEC_CORRECTION],
        },
        {
            "stage": "test-spec-review",
            "attempt": 1,
            "variants": [
                _TEST_REVIEW_INITIAL,
                _TEST_REVIEW_CHANGES,
                _TEST_REVIEW_BLOCKED,
            ],
        },
        {
            "stage": "test-spec-review",
            "attempt": 2,
            "variants": [
                _TEST_REVIEW_REREVIEW,
                _TEST_REVIEW_CHANGES,
                _TEST_REVIEW_BLOCKED,
            ],
        },
    ],
    "per_artifact_byte_limit": 262144,
    "aggregate_artifact_byte_limit": 524288,
    "candidate_message_byte_limit": 786432,
    "envelope_byte_limit": 786432,
    "workspace_integrity_policy": dict(LIFECYCLE_WORKSPACE_INTEGRITY_POLICY),
}

HISTORICAL_EVIDENCE_REGISTRY: Final[tuple[dict[str, str], ...]] = (
    {
        "record_kind": "behavior-implementation-manifest",
        "path": (
            "docs/changes/2026-07-25-boundary-first-proof-modeling-for-"
            "published-lifecycle-skills/evidence/"
            "behavior-implementation-manifest.json"
        ),
        "identity": (
            "sha256:d4a98482700e711f6c1ec17f1309d56c"
            "64f67e9cc6181389cc74daf4f2c4cc0e"
        ),
        "treatment": "opaque-read-only-history",
    },
)


def _classify_historical_evidence(
    record_kind: str, path: str, identity: str
) -> str:
    matches = [
        row
        for row in HISTORICAL_EVIDENCE_REGISTRY
        if row["record_kind"] == record_kind
        and row["path"] == path
        and row["identity"] == identity
        and row["treatment"] == "opaque-read-only-history"
    ]
    return (
        "registered-opaque-history"
        if len(matches) == 1
        else "unsupported-historical-evidence"
    )


def _preflight_failure(
    diagnostic_id: str, phase: str | None = None
) -> dict[str, object]:
    error = BoundaryRuntimeError(diagnostic_id, phase)
    return {
        "schema_version": "boundary-runtime-preflight-v3",
        "result": "environment-unavailable",
        "diagnostic_id": error.diagnostic_id,
        "phase": error.phase,
        "attestation_ref": None,
        "workspace_failure": None,
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
        "tool_profile": "isolated-workspace-readonly-no-network-v1",
        "python_implementation": platform.python_implementation().lower(),
        "python_version": platform.python_version(),
    }
    skill_references = [
        _regular_reference(repo_root, path) for path in skill_paths
    ]
    skill_references.sort(key=lambda row: row["path"])
    return {
        "manifest_id": "boundary-behavior-implementation-v3",
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
        "transport_policy": dict(TRANSPORT_POLICY),
        "artifact_policy": dict(ARTIFACT_POLICY),
        "runtime_attestation": dict(attestation),
    }


def _validate_behavior_manifest(
    repo_root: Path, manifest: Mapping[str, object]
) -> None:
    if set(manifest) != MANIFEST_FIELDS:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    if manifest.get("manifest_id") != "boundary-behavior-implementation-v3":
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
    if manifest.get("transport_policy") != TRANSPORT_POLICY:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    if manifest.get("artifact_policy") != ARTIFACT_POLICY:
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
        or profile["tool_profile"]
        != "isolated-workspace-readonly-no-network-v1"
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
                "governing_requirement_ids": sorted(
                    row.governing_requirement_ids
                ),
                "boundary_ids": sorted(row.boundary_ids),
                "non_applicability_rationale": row.non_applicability_rationale,
            }
            for row in model.core_dimensions
        ], key=lambda row: row["dimension_id"]),
        "extension_rows": [],
        "example_rows": sorted([
            {
                "example_id": row.example_id,
                "role": row.role,
                "governing_requirement_ids": sorted(
                    row.governing_requirement_ids
                ),
                "boundary_ids": sorted(row.boundary_ids),
                "regression_id": row.regression_id,
                "discovery_gap": row.discovery_gap,
                "non_normative_purpose": row.non_normative_purpose,
            }
            for row in model.examples
        ], key=lambda row: row["example_id"]),
        "interaction_rows": sorted([
            {
                "interaction_id": row.interaction_id,
                "boundary_ids": sorted(row.boundary_ids),
                "rationale": row.rationale,
                "governing_requirement_ids": sorted(
                    row.governing_requirement_ids
                ),
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
                "governing_requirement_ids": sorted(
                    row.governing_requirement_ids
                ),
                "boundary_or_interaction_ids": sorted(
                    row.boundary_or_interaction_ids
                ),
                "test_case_ids": sorted(row.test_case_ids),
                "automation_level": row.automation_level,
                "manual_procedure_ids": sorted(row.manual_procedure_ids),
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


def _string_array_schema() -> dict[str, object]:
    return {"type": "array", "items": {"type": "string"}}


def _exact_string_array_schema(values: Sequence[str]) -> dict[str, object]:
    return _closed_object_schema(
        {
            value: {"type": "boolean", "const": True}
            for value in values
        }
    )



def _workflow_request(request: str) -> dict[str, object]:
    expected_outputs = [
        "feature-spec/portable-text-normalizer.md",
        "reviews/spec-review.md",
        "review-log/spec-review.md",
        "test-spec/portable-text-normalizer.test.md",
        "reviews/test-spec-review.md",
        "review-log/test-spec-review.md",
    ]
    return {
        "skill_names": list(PARTICIPATING_SKILLS),
        "stage": "workflow",
        "expected_outputs": expected_outputs,
        "prompt": (
            "Use the installed workflow skill to orchestrate this isolated "
            "four-stage path: spec, spec-review, test-spec, test-spec-review. "
            "Each stage-owning skill must write its complete artifact below "
            "the current workspace output/ directory at the exact relative "
            "paths listed below. Snapshot-worthy bytes must be authored by the "
            "owning skill; do not ask the harness to render, inject, or complete "
            "requirements, acceptance criteria, test cases, validation commands, "
            "or review judgments. Reviews must be formal recorded reviews of the "
            "exact preceding artifact and must approve before the workflow "
            "advances. Do not implement the requested feature. Return only the "
            "closed completion record after every required file is durable.\n\n"
            "Output paths:\n- "
            + "\n- ".join(expected_outputs)
            + "\n\nRequest:\n"
            + request
        ),
        "output_schema": _closed_object_schema(
            {
                "completed": {"type": "boolean", "const": True},
                "last_stage": {
                    "type": "string",
                    "enum": ["test-spec-review"],
                },
            }
        ),
    }


def _workflow_stage_request(
    stage: str,
    request: str,
    *,
    artifact_context: str = "",
    attempt: int = 1,
) -> dict[str, object]:
    outputs_by_stage = {
        "spec": ["feature-spec/portable-text-normalizer.md"],
        "spec-review": [
            "reviews/spec-review.md",
            "review-log/spec-review.md",
        ],
        "test-spec": ["test-spec/portable-text-normalizer.test.md"],
        "test-spec-review": [
            "reviews/test-spec-review.md",
            "review-log/test-spec-review.md",
        ],
    }
    expected_outputs = outputs_by_stage.get(stage)
    if expected_outputs is None:
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    variants = _stage_policy_variants(stage, attempt)
    structure_instruction = {
        "spec": (
            "Use the exact markers `Boundary model version: v1` and "
            "`Boundary model scope: R1-R4`, followed by exact sections "
            "`## Boundary model`, `## Examples`, and `## Interactions`. "
            "The Boundary model and Examples tables must use the exact "
            "columns defined by the attached boundary-proof reference. "
            "Use all twelve closed core dimension IDs exactly once, no "
            "extensions, and governing requirement IDs R1, R2, R3, and R4. "
            "Each boundary ID must appear in exactly one boundary row; examples "
            "may cite those IDs but must not redefine them. Every example's "
            "governing requirement IDs must be a subset of the union owned by "
            "its cited boundaries and must overlap each cited boundary. "
            "Every authored stable ID must match "
            "`^[a-z][a-z0-9-]*(\\.[a-z][a-z0-9-]*)+$`; IDs must be dotted. "
            "Use the literal ASCII `-` for every empty table value; never "
            "use a blank cell or a Unicode dash. "
        ),
        "test-spec": (
            "Use the exact markers `Boundary model version: v1` and "
            "`Boundary model scope: R1-R4`, followed by exact sections "
            "`## Proof map` and `## Test cases`. The Proof map table must "
            "use the exact columns defined by the attached boundary-proof "
            "reference and collectively govern exactly R1, R2, R3, and R4. "
            "Every authored stable ID must match "
            "`^[a-z][a-z0-9-]*(\\.[a-z][a-z0-9-]*)+$`; IDs must be dotted. "
            "Use the literal ASCII `-` for every empty table value; never "
            "use a blank cell or a Unicode dash. "
        ),
        "spec-review": (
            "Use the installed normative review-result skeleton. In both the "
            "review record and review log, include exact metadata lines "
            "`Review ID: spec-review-r1`, `Stage: spec-review`, "
            "`Status: <approved | changes-requested | blocked | inconclusive>`, "
            "`Reviewed artifact identity: <the supplied sha256 identity>`, "
            "`Material findings: <IDs or none>`, and "
            "`Recording status: recorded`. Preserve independent judgment; do "
            "not report `approved` when a material finding exists. "
        ),
        "test-spec-review": (
            "Use the installed normative review-result skeleton. In both the "
            "review record and review log, include exact metadata lines "
            "`Review ID: test-spec-review-r1`, `Stage: test-spec-review`, "
            "`Status: <approved | changes-requested | blocked | inconclusive>`, "
            "`Reviewed artifact identity: <the supplied sha256 identity>`, "
            "`Material findings: <IDs or none>`, and "
            "`Recording status: recorded`. Preserve independent judgment; do "
            "not report `approved` when a material finding exists. "
        ),
    }[stage]
    return {
        "skill_names": ["workflow", stage],
        "stage": stage,
        "attempt": attempt,
        "artifact_policy_id": ARTIFACT_POLICY["policy_id"],
        "expected_outputs": expected_outputs,
        "prompt": (
            "Use the installed workflow skill to route exactly the "
            f"{stage} stage to its installed stage-owning skill. The owning "
            "stage must load and apply its mapped "
            "`references/boundary-proof-model.md` before authoring or "
            "reviewing. The returned artifact must satisfy that installed "
            "skill's boundary-first completion gate. All required inputs are "
            "attached; do not invoke tools, web search, network access, or "
            "other external capabilities. The owning "
            "skill must author every semantic byte and return one complete "
            "policy-bound artifact envelope in the agent message. Child tools "
            "have read-only workspace access and must not create or modify "
            "files. The parent transport validates and materializes exact bytes; "
            "the harness must not render, inject, repair, or complete normative "
            "content. Do not advance past this stage. Return only the closed "
            "artifact envelope. Keep every artifact concise and add no "
            "normative behavior beyond the authoritative stage input. "
            + structure_instruction
            + "\n\nArtifact policy: "
            + str(ARTIFACT_POLICY["policy_id"])
            + "\nAllowed variants: "
            + ", ".join(
                str(row["artifact_set_variant"]) for row in variants
            )
            + "\nExpected paths:\n- "
            + "\n- ".join(expected_outputs)
            + "\n\nRequest:\n"
            + request
            + (
                "\n\nAuthoritative stage input:\n" + artifact_context
                if artifact_context
                else ""
            )
        ),
        "output_schema": _stage_envelope_schema(stage, attempt),
    }


def _assert_parent_only_candidate_isolation(
    *,
    serialized_request: Mapping[str, object],
    workspace_inventory: Sequence[object],
    child_access_observations: Sequence[object],
    forbidden_candidate_values: Sequence[str],
) -> None:
    """Reject any candidate oracle value exposed on a child-visible surface."""

    surfaces = (
        _canonical_json_bytes(serialized_request),
        _canonical_json_bytes(list(workspace_inventory)),
        _canonical_json_bytes(list(child_access_observations)),
    )
    for value in forbidden_candidate_values:
        if value and any(value.encode("utf-8") in surface for surface in surfaces):
            raise BoundaryRuntimeError("unmanifested-input", "pre-turn-start")


def _stage_policy_variants(
    stage: str, attempt: int
) -> list[Mapping[str, object]]:
    rows = ARTIFACT_POLICY["stage_occurrences"]
    assert isinstance(rows, list)
    matches = [
        row
        for row in rows
        if row.get("stage") == stage and row.get("attempt") == attempt
    ]
    if len(matches) != 1:
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    variants = matches[0].get("variants")
    if not isinstance(variants, list) or not variants:
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    return variants


def _stage_envelope_schema(stage: str, attempt: int) -> dict[str, object]:
    variants = _stage_policy_variants(stage, attempt)
    return _closed_object_schema(
        {
            "schema_version": {
                "type": "string",
                "const": "boundary-stage-artifact-envelope-v1",
            },
            "artifact_policy_id": {
                "type": "string",
                "const": ARTIFACT_POLICY["policy_id"],
            },
            "completed": {"type": "boolean", "const": True},
            "last_stage": {"type": "string", "const": stage},
            "artifact_set_variant": {
                "type": "string",
                "enum": [
                    row["artifact_set_variant"] for row in variants
                ],
            },
            "artifacts": {
                "type": "array",
                "minItems": 1,
                "items": _closed_object_schema(
                    {
                        "role": {"type": "string"},
                        "path": {"type": "string"},
                        "content_utf8": {"type": "string", "minLength": 1},
                    }
                ),
            },
        }
    )


def _strict_json_object(raw: str) -> dict[str, object]:
    def pairs(rows: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in rows:
            if key in result:
                raise BoundaryRuntimeError(
                    "unexpected-prohibited-event", "in-turn"
                )
            result[key] = value
        return result

    try:
        value = json.loads(raw, object_pairs_hook=pairs)
    except (json.JSONDecodeError, UnicodeError) as error:
        raise BoundaryRuntimeError(
            "unexpected-prohibited-event", "in-turn"
        ) from error
    if not isinstance(value, dict):
        raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
    return value


def _parse_stage_envelope(
    raw: str, *, stage: str, attempt: int
) -> tuple[dict[str, object], list[dict[str, str]]]:
    raw_bytes = raw.encode("utf-8")
    if len(raw_bytes) > int(ARTIFACT_POLICY["candidate_message_byte_limit"]):
        raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
    envelope = _strict_json_object(raw)
    expected_fields = {
        "schema_version",
        "artifact_policy_id",
        "completed",
        "last_stage",
        "artifact_set_variant",
        "artifacts",
    }
    if (
        set(envelope) != expected_fields
        or envelope.get("schema_version")
        != "boundary-stage-artifact-envelope-v1"
        or envelope.get("artifact_policy_id") != ARTIFACT_POLICY["policy_id"]
        or envelope.get("completed") is not True
        or envelope.get("last_stage") != stage
    ):
        raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
    canonical = _canonical_json_bytes(envelope)
    if len(canonical) > int(ARTIFACT_POLICY["envelope_byte_limit"]):
        raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
    variants = _stage_policy_variants(stage, attempt)
    matches = [
        row
        for row in variants
        if row["artifact_set_variant"]
        == envelope.get("artifact_set_variant")
    ]
    if len(matches) != 1:
        raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
    required = matches[0]["artifacts"]
    artifacts = envelope.get("artifacts")
    if not isinstance(required, list) or not isinstance(artifacts, list):
        raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
    projected: list[dict[str, str]] = []
    total = 0
    seen_roles: set[str] = set()
    seen_paths: set[str] = set()
    for row in artifacts:
        if not isinstance(row, dict) or set(row) != {
            "role",
            "path",
            "content_utf8",
        }:
            raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
        role, path, text = row["role"], row["path"], row["content_utf8"]
        candidate = Path(path) if isinstance(path, str) else Path("/")
        if (
            not isinstance(role, str)
            or not isinstance(path, str)
            or not isinstance(text, str)
            or not text
            or "\x00" in text
            or candidate.is_absolute()
            or not candidate.parts
            or any(part in {"", ".", ".."} for part in candidate.parts)
            or role in seen_roles
            or path in seen_paths
        ):
            raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
        try:
            encoded = text.encode("utf-8")
        except UnicodeEncodeError as error:
            raise BoundaryRuntimeError(
                "unexpected-prohibited-event", "in-turn"
            ) from error
        if len(encoded) > int(ARTIFACT_POLICY["per_artifact_byte_limit"]):
            raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
        total += len(encoded)
        seen_roles.add(role)
        seen_paths.add(path)
        projected.append({"path": path, "text": text})
    if total > int(ARTIFACT_POLICY["aggregate_artifact_byte_limit"]):
        raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
    if [
        {"role": row["role"], "path": row["path"]} for row in artifacts
    ] != required:
        raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
    return envelope, projected


def _materialize_stage_envelope(
    output_root: Path, envelope: Mapping[str, object]
) -> dict[str, object]:
    stage = envelope.get("last_stage")
    if not isinstance(stage, str):
        raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
    attempts = [
        int(row["attempt"])
        for row in ARTIFACT_POLICY["stage_occurrences"]
        if row["stage"] == stage
        and any(
            variant["artifact_set_variant"]
            == envelope.get("artifact_set_variant")
            for variant in row["variants"]
        )
    ]
    if len(attempts) != 1:
        raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
    parsed, rows = _parse_stage_envelope(
        _canonical_json_bytes(dict(envelope)).decode("utf-8"),
        stage=stage,
        attempt=attempts[0],
    )
    output_root.mkdir(parents=True, exist_ok=True)
    root = output_root.resolve(strict=True)
    identities: list[dict[str, str]] = []
    for row in rows:
        target = root.joinpath(*Path(row["path"]).parts)
        parent = target.parent
        parent.mkdir(parents=True, exist_ok=True)
        if any(path.is_symlink() for path in (parent, target) if path.exists()):
            raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
        raw = row["text"].encode("utf-8")
        target.write_bytes(raw)
        if target.read_bytes() != raw:
            raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
        identities.append({"path": row["path"], "identity": _sha256(raw)})
    return {
        "result": "pass",
        "stage_envelope_identity": _sha256(_canonical_json_bytes(parsed)),
        "artifacts": identities,
    }


def _output_state(
    required_paths: Sequence[str], output_files: Sequence[Mapping[str, object]]
) -> str:
    if not required_paths or len(set(required_paths)) != len(required_paths):
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    observed: list[str] = []
    for row in output_files:
        if set(row) != {"path", "text"}:
            raise BoundaryRuntimeError("protocol-shape-incompatible")
        path = row.get("path")
        text = row.get("text")
        if (
            not isinstance(path, str)
            or not isinstance(text, str)
            or not text
            or Path(path).is_absolute()
            or ".." in Path(path).parts
        ):
            raise BoundaryRuntimeError("protocol-shape-incompatible")
        observed.append(path)
    if not observed:
        return "absent"
    if len(set(observed)) != len(observed):
        return "contradictory"
    required = set(required_paths)
    actual = set(observed)
    if actual == required:
        return "complete"
    if actual < required:
        return "partial"
    if required < actual:
        return "extra"
    return "contradictory"


def _collect_workspace_outputs(
    workspace: Path, expected_paths: Sequence[str]
) -> list[dict[str, str]]:
    output_root = workspace / "output"
    if not output_root.is_dir() or output_root.is_symlink():
        return []
    expected = set(expected_paths)
    observed: list[dict[str, str]] = []
    for path in sorted(output_root.rglob("*")):
        if path.is_dir():
            continue
        if not path.is_file() or path.is_symlink():
            raise BoundaryRuntimeError("protocol-shape-incompatible")
        relative = path.relative_to(output_root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise BoundaryRuntimeError("protocol-shape-incompatible") from error
        observed.append({"path": relative, "text": text})
    if any(row["path"] not in expected for row in observed):
        return observed
    return observed


def _invoke_with_reconciliation(
    invoke: Callable[
        [], tuple[dict[str, object], dict[str, object]]
    ],
    required_paths: Sequence[str],
) -> tuple[dict[str, object], dict[str, object], list[dict[str, object]]]:
    attempts: list[dict[str, object]] = []
    for attempt in (1, 2):
        try:
            attestation, result = invoke()
        except _StageTurnTimeout as error:
            if error.termination_state != "confirmed-stopped":
                raise BoundaryRuntimeError(
                    "unexpected-prohibited-event", "in-turn"
                ) from error
            state = _output_state(required_paths, error.output_files)
            if state == "complete" and error.attestation is not None:
                attempts.append(
                    {
                        "transport_attempt": attempt,
                        "output_state": state,
                        "decision": "reconcile",
                        "runtime_thread_id": error.runtime_thread_id,
                        "runtime_process_id": error.runtime_process_id,
                        "elapsed_ms": error.elapsed_ms,
                        "timed_out": True,
                    }
                )
                return (
                    error.attestation,
                    {"output_files": error.output_files},
                    attempts,
                )
            if state == "absent" and attempt == 1:
                attempts.append(
                    {
                        "transport_attempt": attempt,
                        "output_state": state,
                        "decision": "retry",
                        "runtime_thread_id": error.runtime_thread_id,
                        "runtime_process_id": error.runtime_process_id,
                        "elapsed_ms": error.elapsed_ms,
                        "timed_out": True,
                    }
                )
                continue
            attempts.append(
                {
                    "transport_attempt": attempt,
                    "output_state": state,
                    "decision": "fail-closed",
                    "runtime_thread_id": error.runtime_thread_id,
                    "runtime_process_id": error.runtime_process_id,
                    "elapsed_ms": error.elapsed_ms,
                    "timed_out": True,
                }
            )
            raise BoundaryRuntimeError(
                "unexpected-prohibited-event", "in-turn"
            ) from error
        output_files = result.get("output_files")
        if not isinstance(output_files, list):
            raise BoundaryRuntimeError("protocol-shape-incompatible")
        state = _output_state(required_paths, output_files)
        if state != "complete":
            raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
        attempts.append(
            {
                "transport_attempt": attempt,
                "output_state": state,
                "decision": "accept",
                "runtime_thread_id": result.get("thread_id"),
                "runtime_process_id": result.get("runtime_process_id"),
                "elapsed_ms": None,
                "timed_out": False,
            }
        )
        return attestation, result, attempts
    raise AssertionError("closed two-attempt loop did not terminate")


def _finalize_transport_rows(
    attempts: Sequence[Mapping[str, object]],
    stage_artifacts: Mapping[str, str],
    transport_policy_identity: str,
) -> list[dict[str, object]]:
    required_by_stage = {
        "spec": ["feature-spec/portable-text-normalizer.md"],
        "spec-review": [
            "reviews/spec-review.md",
            "review-log/spec-review.md",
        ],
        "test-spec": ["test-spec/portable-text-normalizer.test.md"],
        "test-spec-review": [
            "reviews/test-spec-review.md",
            "review-log/test-spec-review.md",
        ],
    }
    rows: list[dict[str, object]] = []
    for attempt in attempts:
        event_key = attempt.get("event_key")
        transport_attempt = attempt.get("transport_attempt")
        thread_id = attempt.get("runtime_thread_id")
        process_id = attempt.get("runtime_process_id")
        output_state = attempt.get("output_state")
        decision = attempt.get("decision")
        if (
            not isinstance(event_key, str)
            or "#" not in event_key
            or not isinstance(transport_attempt, int)
            or transport_attempt not in {1, 2}
            or not isinstance(thread_id, str)
            or not isinstance(process_id, str)
            or re.fullmatch(r"process-[0-9a-f]{32}", process_id) is None
            or output_state
            not in {"absent", "complete", "partial", "extra", "contradictory"}
            or decision
            not in {"accept", "reconcile", "retry", "pause", "fail-closed"}
        ):
            raise BoundaryRuntimeError("protocol-shape-incompatible")
        stage = event_key.rsplit("#", 1)[0]
        required_paths = required_by_stage.get(stage)
        if required_paths is None:
            raise BoundaryRuntimeError("protocol-shape-incompatible")
        evidence_refs = (
            [
                {
                    "path": path,
                    "identity": _sha256(stage_artifacts[path].encode("utf-8")),
                }
                for path in required_paths
            ]
            if output_state == "complete"
            else []
        )
        timed_out = attempt.get("timed_out") is True
        if timed_out:
            elapsed_ms = attempt.get("elapsed_ms")
            deadline_ms = int(TRANSPORT_POLICY["turn_deadline_ms"])
            if not isinstance(elapsed_ms, int) or elapsed_ms < deadline_ms:
                raise BoundaryRuntimeError("protocol-shape-incompatible")
            diagnostics = (
                ["stage-turn-timeout"]
                if output_state == "complete"
                else [
                    {
                        "absent": "stage-output-absent",
                        "partial": "stage-output-partial",
                        "extra": "stage-output-extra",
                        "contradictory": "stage-output-contradictory",
                    }[str(output_state)],
                    "stage-turn-timeout",
                ]
            )
            termination_receipt: dict[str, object] | None = {
                "method": "terminate-wait-v1",
                "runtime_process_id": process_id,
                "transport_policy_identity": transport_policy_identity,
                "wait_deadline_ms": int(
                    TRANSPORT_POLICY["termination_wait_deadline_ms"]
                ),
                "wait_elapsed_ms": 0,
                "termination_observed": True,
                "reaped": True,
            }
            diagnostic_evidence: dict[str, object] = {
                "stage-turn-timeout": {
                    "kind": "deadline-observation-v1",
                    "transport_policy_identity": transport_policy_identity,
                    "deadline_ms": deadline_ms,
                    "elapsed_ms": elapsed_ms,
                    "runtime_thread_id": thread_id,
                }
            }
            if output_state != "complete":
                observed_outputs: list[dict[str, str]] = []
                required_outputs = [
                    {
                        "role": f"{stage}-output-{index}",
                        "path": path,
                        "identity_rule": "any-current",
                    }
                    for index, path in enumerate(required_paths, start=1)
                ]
                inventory = {
                    "root": "output/",
                    "required_outputs": required_outputs,
                    "observed_outputs": observed_outputs,
                }
                diagnostic_evidence[diagnostics[0]] = {
                    "kind": "output-inventory-v1",
                    **inventory,
                    "inventory_identity": _sha256(
                        _canonical_json_bytes(inventory)
                    ),
                }
            termination_state = "confirmed-stopped"
        else:
            diagnostics = ["none"]
            diagnostic_evidence = {}
            termination_receipt = None
            termination_state = "completed"
        rows.append(
            {
                "transport_attempt_id": (
                    f"{event_key}/transport/{transport_attempt}"
                ),
                "event_key": event_key,
                "transport_attempt": transport_attempt,
                "runtime_thread_id": thread_id,
                "runtime_process_id": process_id,
                "transport_policy_identity": transport_policy_identity,
                "termination_state": termination_state,
                "termination_receipt": termination_receipt,
                "output_state": output_state,
                "primary_diagnostic_id": diagnostics[0],
                "diagnostic_ids": diagnostics,
                "decision": decision,
                "evidence_refs": evidence_refs,
                "diagnostic_evidence": diagnostic_evidence,
            }
        )
    return rows


_TRANSPORT_FIXTURE_FIELDS = {
    "fixture_id",
    "event_key",
    "transport_attempts",
    "expected_terminal_decision",
    "expected_diagnostic_id",
    "expected_diagnostic_ids",
    "canonical_evidence_eligible",
}

_TRANSPORT_ROW_FIELDS = {
    "transport_attempt_id",
    "event_key",
    "transport_attempt",
    "runtime_thread_id",
    "runtime_process_id",
    "transport_policy_identity",
    "termination_state",
    "termination_receipt",
    "output_state",
    "primary_diagnostic_id",
    "diagnostic_ids",
    "decision",
    "evidence_refs",
    "diagnostic_evidence",
}


def _validate_transport_rows(
    rows: object, transport_policy_identity: str
) -> list[dict[str, object]]:
    if not isinstance(rows, list) or not rows:
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    grouped: dict[str, list[dict[str, object]]] = {}
    seen_ids: set[str] = set()
    for value in rows:
        if not isinstance(value, dict) or set(value) != _TRANSPORT_ROW_FIELDS:
            raise BoundaryRuntimeError("protocol-shape-incompatible")
        row = dict(value)
        event_key = row.get("event_key")
        attempt = row.get("transport_attempt")
        attempt_id = row.get("transport_attempt_id")
        thread_id = row.get("runtime_thread_id")
        process_id = row.get("runtime_process_id")
        diagnostics = row.get("diagnostic_ids")
        decision = row.get("decision")
        if (
            not isinstance(event_key, str)
            or re.fullmatch(
                r"(?:spec|spec-review|test-spec|test-spec-review)#[1-9][0-9]*",
                event_key,
            )
            is None
            or attempt not in {1, 2}
            or attempt_id != f"{event_key}/transport/{attempt}"
            or not isinstance(attempt_id, str)
            or attempt_id in seen_ids
            or not isinstance(thread_id, str)
            or not isinstance(process_id, str)
            or re.fullmatch(r"process-[0-9a-f]{32}", process_id) is None
            or row.get("transport_policy_identity")
            != transport_policy_identity
            or row.get("termination_state")
            not in {"completed", "confirmed-stopped", "liveness-uncertain"}
            or row.get("output_state")
            not in {
                "uninspected",
                "absent",
                "complete",
                "partial",
                "extra",
                "contradictory",
            }
            or not isinstance(diagnostics, list)
            or not diagnostics
            or len(set(diagnostics)) != len(diagnostics)
            or row.get("primary_diagnostic_id") != diagnostics[0]
            or decision
            not in {"accept", "reconcile", "retry", "pause", "fail-closed"}
            or not isinstance(row.get("evidence_refs"), list)
            or not isinstance(row.get("diagnostic_evidence"), dict)
        ):
            raise BoundaryRuntimeError("protocol-shape-incompatible")
        seen_ids.add(attempt_id)
        grouped.setdefault(event_key, []).append(row)
    if set(grouped) != {
        "spec#1",
        "spec-review#1",
        "test-spec#1",
        "test-spec-review#1",
    }:
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    for attempts in grouped.values():
        attempts.sort(key=lambda row: int(row["transport_attempt"]))
        if [row["transport_attempt"] for row in attempts] not in (
            [1],
            [1, 2],
        ):
            raise BoundaryRuntimeError("protocol-shape-incompatible")
        if len(attempts) == 2 and (
            attempts[0]["decision"] != "retry"
            or attempts[0]["runtime_thread_id"]
            == attempts[1]["runtime_thread_id"]
            or attempts[0]["runtime_process_id"]
            == attempts[1]["runtime_process_id"]
        ):
            raise BoundaryRuntimeError("protocol-shape-incompatible")
        if attempts[-1]["decision"] == "retry":
            raise BoundaryRuntimeError("protocol-shape-incompatible")
    return [dict(row) for row in rows]


def _load_transport_fixture(path: Path) -> dict[str, object]:
    fixture = _read_json(path)
    if set(fixture) != _TRANSPORT_FIXTURE_FIELDS:
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    fixture_id = fixture.get("fixture_id")
    event_key = fixture.get("event_key")
    attempts = fixture.get("transport_attempts")
    diagnostic_ids = fixture.get("expected_diagnostic_ids")
    if (
        not isinstance(fixture_id, str)
        or not fixture_id
        or not isinstance(event_key, str)
        or re.fullmatch(r"[a-z-]+#[1-9][0-9]*", event_key) is None
        or not isinstance(attempts, list)
        or not 1 <= len(attempts) <= 2
        or not isinstance(diagnostic_ids, list)
        or not diagnostic_ids
        or any(not isinstance(value, str) for value in diagnostic_ids)
        or len(set(diagnostic_ids)) != len(diagnostic_ids)
        or fixture.get("canonical_evidence_eligible") is not False
    ):
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    for index, row in enumerate(attempts, start=1):
        if (
            not isinstance(row, dict)
            or set(row) != _TRANSPORT_ROW_FIELDS
            or row.get("event_key") != event_key
            or row.get("transport_attempt") != index
            or row.get("transport_attempt_id")
            != f"{event_key}/transport/{index}"
            or row.get("termination_state")
            not in {"completed", "confirmed-stopped", "liveness-uncertain"}
            or row.get("output_state")
            not in {
                "uninspected",
                "absent",
                "complete",
                "partial",
                "extra",
                "contradictory",
            }
            or row.get("decision")
            not in {"accept", "reconcile", "retry", "pause", "fail-closed"}
            or not isinstance(row.get("diagnostic_ids"), list)
            or not row["diagnostic_ids"]
            or row.get("primary_diagnostic_id") != row["diagnostic_ids"][0]
        ):
            raise BoundaryRuntimeError(
                "protocol-shape-incompatible"
            )
    terminal = attempts[-1]
    if (
        terminal.get("decision") != fixture.get("expected_terminal_decision")
        or terminal.get("primary_diagnostic_id")
        != fixture.get("expected_diagnostic_id")
        or terminal.get("diagnostic_ids") != diagnostic_ids
        or terminal.get("decision") == "retry"
    ):
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    return fixture


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
        if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
            print(
                f"review-envelope:{stage}:id={review_id!r}:outcome={outcome!r}",
                file=sys.stderr,
            )
            if isinstance(record, str):
                print(record, file=sys.stderr)
        raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
    def metadata(markdown: str, label: str) -> str | None:
        match = re.search(
            rf"(?im)^\s*(?:[-*]\s*)?(?:\*\*)?{re.escape(label)}"
            rf"(?:\*\*)?\s*:\s*(.+?)\s*$",
            markdown,
        )
        if match is None:
            return None
        return match.group(1).strip().rstrip("  ").strip("`* ")

    required = {
        "Review ID": review_id,
        "Stage": stage,
        "Status": "approved",
        "Reviewed artifact identity": artifact_identity,
        "Material findings": "none",
    }
    record_values = {label: metadata(record, label) for label in required}
    log_values = {label: metadata(log, label) for label in required}
    record_values["Recording status"] = metadata(record, "Recording status")
    if (
        any(
            (str(record_values[label]).lower() if label == "Material findings" else record_values[label])
            != expected
            for label, expected in required.items()
        )
        or any(
            (str(log_values[label]).lower() if label == "Material findings" else log_values[label])
            != expected
            for label, expected in required.items()
        )
        or record_values["Recording status"] != "recorded"
    ):
        if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
            print(
                f"review-fields:{stage}:record={record_values!r}:log={log_values!r}",
                file=sys.stderr,
            )
        raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")


def _review_payload_from_markdown(
    stage: str, record: str, log: str
) -> dict[str, object]:
    def metadata(markdown: str, label: str) -> str | None:
        match = re.search(
            rf"(?im)^\s*(?:[-*]\s*)?(?:\*\*)?{re.escape(label)}"
            rf"(?:\*\*)?\s*:\s*(.+?)\s*$",
            markdown,
        )
        return (
            None
            if match is None
            else match.group(1).strip().rstrip("  ").strip("`* ")
        )

    review_id = metadata(record, "Review ID")
    outcome = metadata(record, "Status")
    if not isinstance(review_id, str) or not isinstance(outcome, str):
        if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
            print(
                f"review-metadata:{stage}:id={review_id!r}:outcome={outcome!r}",
                file=sys.stderr,
            )
            print(record, file=sys.stderr)
        raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
    return {
        "review_id": review_id,
        "outcome": outcome,
        "review_record_markdown": record,
        "review_log_markdown": log,
    }



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
    feature_payload = payload.get("feature_model")
    proof_payload = payload.get("proof_map")
    spec_review_payload = payload.get("spec_review")
    test_review_payload = payload.get("test_spec_review")
    provenance = payload.get("stage_provenance")
    stage_artifacts = payload.get("stage_artifacts")
    if (
        not isinstance(feature_payload, dict)
        or not isinstance(proof_payload, dict)
        or not isinstance(spec_review_payload, dict)
        or not isinstance(test_review_payload, dict)
        or not isinstance(provenance, list)
        or not isinstance(stage_artifacts, dict)
        or set(stage_artifacts)
        != {
            "feature-spec/portable-text-normalizer.md",
            "reviews/spec-review.md",
            "review-log/spec-review.md",
            "test-spec/portable-text-normalizer.test.md",
            "reviews/test-spec-review.md",
            "review-log/test-spec-review.md",
        }
        or any(not isinstance(value, str) for value in stage_artifacts.values())
    ):
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    try:
        feature_raw = stage_artifacts[
            "feature-spec/portable-text-normalizer.md"
        ].encode("utf-8")
        test_raw = stage_artifacts[
            "test-spec/portable-text-normalizer.test.md"
        ].encode("utf-8")
    except UnicodeError as error:
        raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn") from error
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
    if not boundary_invariant_projections_match(
        candidate_feature,
        parsed_feature,
        candidate_proof,
        parsed_proof,
    ):
        raise BoundaryRuntimeError("boundary-oracle-mismatch", "in-turn")
    if (
        spec_review_payload.get("outcome") != "approved"
        or test_review_payload.get("outcome") != "approved"
    ):
        raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
    transport_attempts = payload.get("transport_attempts")
    if not isinstance(transport_attempts, list):
        raise BoundaryRuntimeError("protocol-shape-incompatible")

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
            raise BoundaryRuntimeError("protocol-shape-incompatible")
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
        "spec",
        "spec-review",
        "test-spec",
        "test-spec-review",
    }:
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    spec_review_thread = provenance_by_stage["spec-review"].get("thread_id")
    test_review_thread = provenance_by_stage["test-spec-review"].get("thread_id")
    provenance_threads = [
        row.get("thread_id") for row in provenance_by_stage.values()
    ]
    if (
        not isinstance(spec_review_thread, str)
        or not isinstance(test_review_thread, str)
        or any(not isinstance(value, str) for value in provenance_threads)
        or len(set(provenance_threads)) != 4
        or any(
            row.get("skill_names") != ["workflow", stage]
            for stage, row in provenance_by_stage.items()
        )
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
        "transport_attempts": list(map(dict, transport_attempts)),
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
        "transport_attempts",
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
    transport_policy_identity = _sha256(
        _canonical_json_bytes(implementation_manifest["transport_policy"])
    )
    _validate_transport_rows(
        run.get("transport_attempts"), transport_policy_identity
    )
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
        if not boundary_invariant_projections_match(
            oracle_feature,
            feature,
            oracle_proof,
            proof,
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
    oracle_paths = [
        scenario_path.parent / "candidates" / "feature-spec.md",
        scenario_path.parent / "candidates" / "test-spec.md",
    ]
    try:
        oracle_raw = [path.read_bytes() for path in oracle_paths]
        candidate_feature = normalize_feature_model(
            _parse_feature_markdown(oracle_raw[0].decode("utf-8"))
        )
        candidate_proof = normalize_proof_map(
            _parse_test_spec_markdown(oracle_raw[1].decode("utf-8")),
            candidate_feature,
        )
    except (OSError, UnicodeError, BoundaryProofError) as error:
        raise BoundaryRuntimeError("boundary-oracle-mismatch", "in-turn") from error
    forbidden_candidate_values = tuple(
        value
        for path, raw in zip(oracle_paths, oracle_raw, strict=True)
        for value in (
            str(path),
            path.relative_to(repo_root).as_posix(),
            _sha256(raw),
            raw.decode("utf-8"),
        )
    )
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
    def run_stage(
        stage_request: Mapping[str, object],
    ) -> tuple[
        dict[str, object],
        dict[str, object],
        list[dict[str, object]],
        dict[str, str],
    ]:
        if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
            print(f"stage-start:{stage_request['stage']}", file=sys.stderr)

        def invoke() -> tuple[dict[str, object], dict[str, object]]:
            generated: list[dict[str, object]] = []
            observed_attestation = _collect_runtime_attestation(
                command,
                repo_root=repo_root,
                generation_request=stage_request,
                generation_sink=generated,
                forbidden_candidate_values=forbidden_candidate_values,
            )
            if len(generated) != 1:
                raise BoundaryRuntimeError("protocol-shape-incompatible")
            return observed_attestation, generated[0]

        observed, result, attempts = _invoke_with_reconciliation(
            invoke, list(stage_request["expected_outputs"])
        )
        envelope = result.get("stage_envelope")
        completion = (
            {
                "completed": envelope.get("completed"),
                "last_stage": envelope.get("last_stage"),
            }
            if isinstance(envelope, dict)
            else {
                "completed": True,
                "last_stage": stage_request["stage"],
            }
        )
        if completion != {
            "completed": True,
            "last_stage": stage_request["stage"],
        }:
            raise BoundaryRuntimeError(
                "unexpected-prohibited-event", "in-turn"
            )
        rows = result.get("output_files")
        if not isinstance(rows, list):
            raise BoundaryRuntimeError("protocol-shape-incompatible")
        artifacts = {
            str(row["path"]): str(row["text"])
            for row in rows
            if isinstance(row, dict) and set(row) == {"path", "text"}
        }
        if len(artifacts) != len(rows):
            raise BoundaryRuntimeError("protocol-shape-incompatible")
        for attempt in attempts:
            attempt["event_key"] = f"{stage_request['stage']}#1"
        if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
            print(f"stage-complete:{stage_request['stage']}", file=sys.stderr)
        return observed, result, attempts, artifacts

    stage_results: list[dict[str, object]] = []
    stage_attestations: list[dict[str, object]] = []
    transport_attempts: list[dict[str, object]] = []
    stage_artifacts: dict[str, str] = {}

    spec_request = _workflow_stage_request(
        "spec", str(scenario["request"])
    )
    attestation, spec_result, attempts, artifacts = run_stage(spec_request)
    stage_attestations.append(attestation)
    stage_results.append(spec_result)
    transport_attempts.extend(attempts)
    stage_artifacts.update(artifacts)
    feature_markdown = stage_artifacts[
        "feature-spec/portable-text-normalizer.md"
    ]
    feature_identity = _sha256(feature_markdown.encode("utf-8"))
    try:
        normalized_feature = normalize_feature_model(
            _parse_feature_markdown(feature_markdown)
        )
        if feature_invariant_projection(
            normalized_feature
        ) != feature_invariant_projection(candidate_feature):
            raise BoundaryProofError(
                "stage-owned feature differs from the closed invariant projection"
            )
    except BoundaryProofError as error:
        if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
            print(f"boundary-structure:spec:{error}", file=sys.stderr)
        raise BoundaryRuntimeError(
            "boundary-oracle-mismatch", "in-turn"
        ) from error

    spec_review_request = _workflow_stage_request(
        "spec-review",
        "Review the exact feature specification and record the formal result.",
        artifact_context=(
            "Authoritative scenario request:\n"
            + str(scenario["request"])
            + f"\n\nReviewed artifact identity: {feature_identity}\n\n"
            + feature_markdown
        ),
    )
    observed, result, attempts, artifacts = run_stage(spec_review_request)
    stage_attestations.append(observed)
    stage_results.append(result)
    transport_attempts.extend(attempts)
    stage_artifacts.update(artifacts)
    spec_review_payload = _review_payload_from_markdown(
        "spec-review",
        stage_artifacts["reviews/spec-review.md"],
        stage_artifacts["review-log/spec-review.md"],
    )
    _validate_review_payload(
        spec_review_payload,
        stage="spec-review",
        artifact_identity=feature_identity,
    )

    test_spec_request = _workflow_stage_request(
        "test-spec",
        "Author the complete proof map for the approved feature specification.",
        artifact_context=(
            feature_markdown
            + "\n\nApproved formal review:\n"
            + str(spec_review_payload["review_record_markdown"])
        ),
    )
    observed, result, attempts, artifacts = run_stage(test_spec_request)
    stage_attestations.append(observed)
    stage_results.append(result)
    transport_attempts.extend(attempts)
    stage_artifacts.update(artifacts)
    test_spec_markdown = stage_artifacts[
        "test-spec/portable-text-normalizer.test.md"
    ]
    test_spec_identity = _sha256(test_spec_markdown.encode("utf-8"))
    try:
        normalized_proof = normalize_proof_map(
            _parse_test_spec_markdown(test_spec_markdown),
            normalized_feature,
        )
        if proof_invariant_projection(
            normalized_proof
        ) != proof_invariant_projection(candidate_proof):
            raise BoundaryProofError(
                "stage-owned proof differs from the closed invariant projection"
            )
    except BoundaryProofError as error:
        if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
            print(f"boundary-structure:test-spec:{error}", file=sys.stderr)
        raise BoundaryRuntimeError(
            "boundary-oracle-mismatch", "in-turn"
        ) from error

    test_review_request = _workflow_stage_request(
        "test-spec-review",
        "Review the exact test specification and record the formal result.",
        artifact_context=(
            "Authoritative scenario request:\n"
            + str(scenario["request"])
            + f"\n\nReviewed artifact identity: {test_spec_identity}\n\n"
            + test_spec_markdown
            + "\n\nGoverning feature specification:\n"
            + feature_markdown
            + "\n\nApproved feature review:\n"
            + str(spec_review_payload["review_record_markdown"])
        ),
    )
    observed, result, attempts, artifacts = run_stage(test_review_request)
    stage_attestations.append(observed)
    stage_results.append(result)
    transport_attempts.extend(attempts)
    stage_artifacts.update(artifacts)
    test_review_payload = _review_payload_from_markdown(
        "test-spec-review",
        stage_artifacts["reviews/test-spec-review.md"],
        stage_artifacts["review-log/test-spec-review.md"],
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
    if any(
        observed[field] != attestation[field]
        for observed in stage_attestations[1:]
        for field in attestation_identity_fields
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable", "in-turn")
    thread_ids = [result.get("thread_id") for result in stage_results]
    if (
        any(not isinstance(value, str) for value in thread_ids)
        or len(set(thread_ids)) != 4
    ):
        raise BoundaryRuntimeError("thread-metadata-mismatch", "in-turn")
    feature_model = _feature_record(normalized_feature)
    proof_map = _proof_record(normalized_proof)
    payload = {
        "feature_model": feature_model,
        "spec_review": spec_review_payload,
        "proof_map": proof_map,
        "test_spec_review": test_review_payload,
        "stage_artifacts": stage_artifacts,
        "transport_attempts": transport_attempts,
        "stage_provenance": [
            {
                "stage": stage,
                "thread_id": result["thread_id"],
                "skill_names": ["workflow", stage],
            }
            for stage, result in zip(
                ("spec", "spec-review", "test-spec", "test-spec-review"),
                stage_results,
                strict=True,
            )
        ],
    }
    behavior_manifest = _build_behavior_manifest(repo_root, attestation)
    _validate_behavior_manifest(repo_root, behavior_manifest)
    transport_policy_identity = _sha256(
        _canonical_json_bytes(behavior_manifest["transport_policy"])
    )
    payload["transport_attempts"] = _validate_transport_rows(
        _finalize_transport_rows(
            transport_attempts,
            stage_artifacts,
            transport_policy_identity,
        ),
        transport_policy_identity,
    )
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
        'default_permissions = "boundary-proof-stage-readonly-v1"',
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
            "[permissions.boundary-proof-stage-readonly-v1]",
            'description = "Boundary proof read-only isolated runtime"',
            "",
            "[permissions.boundary-proof-stage-readonly-v1.filesystem]",
            '":root" = "deny"',
            '":minimal" = "read"',
            f"{_toml_string(str(runtime_package))} = \"read\"",
            "",
            '[permissions.boundary-proof-stage-readonly-v1.filesystem.":workspace_roots"]',
            '"." = "read"',
            "",
            "[permissions.boundary-proof-stage-readonly-v1.network]",
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


def _dispatch_file_change_request(
    request: Mapping[str, object],
    *,
    policy: Mapping[str, object],
    expected_thread_id: str,
    expected_turn_id: str,
    expected_item_id: str,
    expected_change_identity: str,
    observed_change_identity: str,
    decision_handler: Callable[[], Mapping[str, object]] | None,
) -> tuple[dict[str, object] | None, str | None]:
    """Production deny-only dispatcher shared by live and conformance paths."""

    policy_identity = _sha256(_canonical_json_bytes(policy))
    params = request.get("params")
    if (
        set(request) != {"jsonrpc", "id", "method", "params"}
        or request.get("jsonrpc") != "2.0"
        or request.get("method") != "item/fileChange/requestApproval"
        or not isinstance(request.get("id"), (int, str))
        or not isinstance(params, dict)
        or set(params)
        != {
            "grantRoot",
            "itemId",
            "reason",
            "startedAtMs",
            "threadId",
            "turnId",
        }
        or not isinstance(params.get("startedAtMs"), int)
        or isinstance(params.get("startedAtMs"), bool)
    ):
        return None, "malformed-request"
    if (
        policy != FILE_CHANGE_AUTHORIZATION_POLICY
        or policy_identity
        != _sha256(_canonical_json_bytes(FILE_CHANGE_AUTHORIZATION_POLICY))
    ):
        return None, "wrong-policy-identity"
    if params.get("threadId") != expected_thread_id:
        return None, "thread-mismatch"
    if params.get("turnId") != expected_turn_id:
        return None, "turn-mismatch"
    if params.get("itemId") != expected_item_id:
        return None, "item-mismatch"
    if observed_change_identity != expected_change_identity:
        return None, "change-mismatch"
    if decision_handler is None:
        return None, "missing-handler"
    decision = dict(decision_handler())
    if decision != {"decision": "decline"}:
        return None, "response-not-deny-only"
    return decision, None


def _run_file_change_handler_conformance(
    policy: Mapping[str, object],
) -> dict[str, object]:
    """Exercise every closed case against the installed production dispatcher."""

    authorization_identity = _sha256(_canonical_json_bytes(policy))
    conformance_policy = handler_conformance_policy(authorization_identity)
    expected = {
        "thread_id": "conformance-thread",
        "turn_id": "conformance-turn",
        "item_id": "conformance-item",
        "change_identity": "sha256:" + "c" * 64,
    }
    base_request: dict[str, object] = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "item/fileChange/requestApproval",
        "params": {
            "grantRoot": None,
            "itemId": expected["item_id"],
            "reason": None,
            "startedAtMs": 1,
            "threadId": expected["thread_id"],
            "turnId": expected["turn_id"],
        },
    }
    case_results: list[dict[str, str]] = []
    for case in HANDLER_CONFORMANCE_CASES:
        request = json.loads(json.dumps(base_request))
        case_policy = policy
        observed_change_identity = expected["change_identity"]
        handler: Callable[[], Mapping[str, object]] | None = (
            lambda: {"decision": "decline"}
        )
        if case == "missing-handler-rejected":
            handler = None
        elif case == "wrong-policy-identity-rejected":
            case_policy = {**policy, "request_decision": "accept"}
        elif case == "thread-mismatch-rejected":
            request["params"]["threadId"] = "other-thread"  # type: ignore[index]
        elif case == "turn-mismatch-rejected":
            request["params"]["turnId"] = "other-turn"  # type: ignore[index]
        elif case == "item-mismatch-rejected":
            request["params"]["itemId"] = "other-item"  # type: ignore[index]
        elif case == "change-mismatch-rejected":
            observed_change_identity = "sha256:" + "d" * 64
        elif case == "accept-rejected":
            handler = lambda: {"decision": "accept"}
        elif case == "accept-for-session-rejected":
            handler = lambda: {"decision": "acceptForSession"}
        elif case == "widened-response-rejected":
            handler = lambda: {"decision": "decline", "scope": "session"}
        elif case == "malformed-request-rejected":
            request["params"].pop("itemId")  # type: ignore[union-attr]
        response, failure = _dispatch_file_change_request(
            request,
            policy=case_policy,
            expected_thread_id=expected["thread_id"],
            expected_turn_id=expected["turn_id"],
            expected_item_id=expected["item_id"],
            expected_change_identity=expected["change_identity"],
            observed_change_identity=observed_change_identity,
            decision_handler=handler,
        )
        passed = (
            response == {"decision": "decline"} and failure is None
            if case == "matching-request-declined"
            else response is None and failure is not None
        )
        case_results.append(
            {"case": case, "result": "pass" if passed else "fail"}
        )
    result: dict[str, object] = {
        "schema_version": "stage-file-change-handler-conformance-result-v1",
        "policy_identity": _sha256(_canonical_json_bytes(conformance_policy)),
        "case_results": case_results,
        "result": (
            "pass"
            if all(row["result"] == "pass" for row in case_results)
            else "fail"
        ),
    }
    result["result_identity"] = _sha256(_canonical_json_bytes(result))
    try:
        validate_handler_conformance(
            conformance_policy,
            result,
            authorization_policy_identity=authorization_identity,
        )
    except BoundaryProofError as error:
        raise BoundaryRuntimeError(
            "file-change-control-mismatch", "pre-turn-start"
        ) from error
    return result


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

    def _respond(self, request_id: object, result: object) -> None:
        stream = self._process.stdin
        if stream is None:
            raise BoundaryRuntimeError("experimental-api-unavailable")
        response = {"jsonrpc": "2.0", "id": request_id, "result": result}
        try:
            stream.write(_canonical_json_bytes(response).decode("utf-8") + "\n")
            stream.flush()
        except OSError as error:
            raise BoundaryRuntimeError(
                "unexpected-prohibited-event", "in-turn"
            ) from error

    def collect_turn(
        self,
        thread_id: str,
        protocol_classification: Sequence[Mapping[str, str]],
        *,
        timeout: int = 300,
        file_change_policy: Mapping[str, object] | None = None,
        turn_id: str | None = None,
        file_change_capability_state: str | None = None,
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
        file_change_request_count = 0
        file_change_terminal_statuses: list[str] = []
        pending = list(self._notifications)
        self._notifications.clear()
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                response = (
                    pending.pop(0) if pending else self._read_message(deadline)
                )
            except BoundaryRuntimeError as error:
                if error.diagnostic_id == "experimental-api-unavailable":
                    raise _StageTurnTimeout from error
                raise
            method = response.get("method")
            if not isinstance(method, str):
                raise BoundaryRuntimeError(
                    "unexpected-prohibited-event", "in-turn"
                )
            source = "ServerRequest" if "id" in response else "ServerNotification"
            classification = classifications.get(f"{source}:{method}")
            if classification is None or classification == (
                "prohibited-capability-event"
            ):
                raise BoundaryRuntimeError(
                    "unexpected-prohibited-event", "in-turn"
                )
            params = response.get("params")
            if not isinstance(params, dict):
                raise BoundaryRuntimeError(
                    "unexpected-prohibited-event", "in-turn"
                )
            if "id" in response:
                if (
                    method != "item/fileChange/requestApproval"
                    or file_change_policy != FILE_CHANGE_AUTHORIZATION_POLICY
                    or file_change_capability_state
                    != "exposed-live-probe-required"
                    or turn_id is None
                ):
                    raise BoundaryRuntimeError(
                        "file-change-control-mismatch", "in-turn"
                    )
                item_id = params.get("itemId")
                if not isinstance(item_id, str):
                    raise BoundaryRuntimeError(
                        "file-change-control-mismatch", "in-turn"
                    )
                decision, failure = _dispatch_file_change_request(
                    response,
                    policy=file_change_policy,
                    expected_thread_id=thread_id,
                    expected_turn_id=turn_id,
                    expected_item_id=item_id,
                    expected_change_identity=str(
                        FILE_CHANGE_AUTHORIZATION_POLICY["prompt_identity"]
                    ),
                    observed_change_identity=str(
                        FILE_CHANGE_AUTHORIZATION_POLICY["prompt_identity"]
                    ),
                    decision_handler=lambda: {"decision": "decline"},
                )
                if decision is None or failure is not None:
                    raise BoundaryRuntimeError(
                        "file-change-control-mismatch", "in-turn"
                    )
                self._respond(response["id"], decision)
                file_change_request_count += 1
                event_methods.append(method)
                continue
            if method == "remoteControl/status/changed" and (
                params.get("status") != "disabled"
                or params.get("environmentId") is not None
            ):
                raise BoundaryRuntimeError(
                    "unexpected-prohibited-event", "in-turn"
                )
            if method == "error":
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
                    if (
                        item_type != "fileChange"
                        or file_change_capability_state
                        == "not-exposed-projection"
                        or item.get("status") != "declined"
                    ):
                        raise BoundaryRuntimeError(
                            "unexpected-prohibited-event", "in-turn"
                        )
                    file_change_terminal_statuses.append("declined")
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
                    or not messages
                ):
                    raise BoundaryRuntimeError(
                        "unexpected-prohibited-event", "in-turn"
                    )
                return {
                    "agent_message": messages[-1],
                    "agent_message_count": len(messages),
                    "event_methods": event_methods,
                    "file_change_request_count": file_change_request_count,
                    "file_change_terminal_statuses": file_change_terminal_statuses,
                }
        raise _StageTurnTimeout

    def close(self) -> None:
        wait_seconds = (
            int(TRANSPORT_POLICY["termination_wait_deadline_ms"]) / 1000
        )
        self._process.terminate()
        try:
            self._process.wait(timeout=wait_seconds)
        except subprocess.TimeoutExpired:
            self._process.kill()
            self._process.wait(timeout=wait_seconds)


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
            "boundary-proof-stage-readonly-v1",
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


def _workspace_probe_snapshot(workspace: Path) -> list[tuple[str, int, str]]:
    rows: list[tuple[str, int, str]] = []
    for path in sorted(workspace.rglob("*"), key=lambda item: item.as_posix()):
        metadata = path.lstat()
        if stat.S_ISLNK(metadata.st_mode):
            raise BoundaryRuntimeError("sandbox-probe-failed", "pre-turn-start")
        relative = path.relative_to(workspace).as_posix()
        if stat.S_ISDIR(metadata.st_mode):
            rows.append((relative, stat.S_IMODE(metadata.st_mode), "directory"))
        elif stat.S_ISREG(metadata.st_mode):
            rows.append(
                (
                    relative,
                    stat.S_IMODE(metadata.st_mode),
                    _sha256(path.read_bytes()),
                )
            )
        else:
            raise BoundaryRuntimeError("sandbox-probe-failed", "pre-turn-start")
    return rows


def _probe_workspace_write_denial(
    executable: Path,
    environment: Mapping[str, str],
    workspace: Path,
    source: Path,
) -> None:
    before = _workspace_probe_snapshot(workspace)
    create_path = workspace / "write-denial-create.txt"
    mutations = (
        (
            "/usr/bin/python3",
            "-c",
            f"from pathlib import Path;Path({str(create_path)!r}).write_text('x')",
        ),
        (
            "/usr/bin/python3",
            "-c",
            f"from pathlib import Path;Path({str(source)!r}).write_text('changed')",
        ),
        ("/bin/rm", str(source)),
        ("/bin/chmod", "600", str(source)),
    )
    for mutation in mutations:
        _sandbox_probe(
            executable,
            environment,
            workspace,
            mutation,
            expect_success=False,
        )
    if _workspace_probe_snapshot(workspace) != before:
        raise BoundaryRuntimeError("sandbox-probe-failed", "pre-turn-start")


def _probe_descendant_workspace_write_denial(
    executable: Path,
    environment: Mapping[str, str],
    workspace: Path,
    source: Path,
) -> None:
    before = _workspace_probe_snapshot(workspace)
    create_path = workspace / "descendant-write-denial-create.txt"
    script = (
        "import ctypes,json,os,pathlib,time\n"
        "ctypes.CDLL(None).prctl(36,1,0,0,0)\n"
        "pid_r,pid_w=os.pipe();data_r,data_w=os.pipe()\n"
        "direct=os.fork()\n"
        "if direct==0:\n"
        " descendant=os.fork()\n"
        " if descendant:\n"
        "  os.write(pid_w,str(descendant).encode());os._exit(0)\n"
        " os.setsid();time.sleep(0.05)\n"
        " os.close(pid_r);os.close(pid_w);os.close(data_r)\n"
        f" source=pathlib.Path({str(source)!r})\n"
        f" create=pathlib.Path({str(create_path)!r})\n"
        " checks=[]\n"
        " for action in (\n"
        "  lambda:create.write_text('x'),\n"
        "  lambda:source.write_text('changed'),\n"
        "  lambda:source.unlink(),\n"
        "  lambda:source.chmod(0o600),\n"
        " ):\n"
        "  try: action();checks.append(False)\n"
        "  except OSError: checks.append(True)\n"
        " os.write(data_w,json.dumps(checks).encode());os._exit(0)\n"
        "os.close(pid_w);os.close(data_w);os.waitpid(direct,0)\n"
        "descendant=int(os.read(pid_r,64));payload=os.read(data_r,4096)\n"
        "reaped=os.waitpid(descendant,0)[0]==descendant\n"
        "print(json.dumps({'checks':json.loads(payload),'reaped':reaped}),flush=True)\n"
    )
    completed = _sandbox_probe(
        executable,
        environment,
        workspace,
        ("/usr/bin/python3", "-c", script),
        expect_success=True,
    )
    try:
        results = json.loads(completed.stdout.strip())
    except json.JSONDecodeError as error:
        raise BoundaryRuntimeError(
            "sandbox-probe-failed", "pre-turn-start"
        ) from error
    if results != {"checks": [True, True, True, True], "reaped": True}:
        raise BoundaryRuntimeError("sandbox-probe-failed", "pre-turn-start")
    if _workspace_probe_snapshot(workspace) != before:
        raise BoundaryRuntimeError("sandbox-probe-failed", "pre-turn-start")


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
    launcher_identity: str,
    package_identity: str,
    schema_identity: str,
    protocol_classification: Sequence[Mapping[str, str]],
) -> Callable[[Sequence[Mapping[str, str]]], dict[str, object]]:
    """Bind stable runtime bytes now and complete selection after inventory."""

    protocol_identity = _sha256(_canonical_json_bytes(protocol_classification))

    def select(
        feature_classification: Sequence[Mapping[str, str]],
    ) -> dict[str, object]:
        try:
            return select_runtime_projection(
                runtime_version=version,
                runtime_launcher_identity=launcher_identity,
                runtime_package_identity=package_identity,
                schema_bundle_identity=schema_identity,
                protocol_item_classification_identity=protocol_identity,
                feature_classification_identity=_sha256(
                    _canonical_json_bytes(feature_classification)
                ),
            )
        except BoundaryProofError as error:
            raise BoundaryRuntimeError(
                "runtime-projection-unsupported", "pre-thread-start"
            ) from error

    return select


def _effective_tool_projection(
    feature_pages: Sequence[Mapping[str, object]],
    feature_classification: Sequence[Mapping[str, str]],
    projection: Mapping[str, object],
) -> list[dict[str, object]]:
    inventory: dict[str, bool] = {}
    for page in feature_pages:
        items = page.get("items")
        if not isinstance(items, list):
            raise BoundaryRuntimeError(
                "file-change-control-mismatch", "pre-turn-start"
            )
        for item in items:
            if (
                not isinstance(item, dict)
                or not isinstance(item.get("name"), str)
                or not isinstance(item.get("enabled"), bool)
                or item["name"] in inventory
            ):
                raise BoundaryRuntimeError(
                    "file-change-control-mismatch", "pre-turn-start"
                )
            inventory[item["name"]] = item["enabled"]
    classifications = {
        row.get("feature"): row.get("classification")
        for row in feature_classification
    }
    projected = set(projection["permitted_tool_features"]) | set(
        projection["permitted_non_tool_features"]
    ) | set(
        projection["required_disabled_features"]
    )
    if (
        len(classifications) != len(feature_classification)
        or set(inventory) != projected
        or set(classifications) != projected
    ):
        raise BoundaryRuntimeError(
            "file-change-control-mismatch", "pre-turn-start"
        )
    rows = [
        {
            "feature": feature,
            "classification": classifications[feature],
            "enabled": inventory[feature],
        }
        for feature in sorted(projected)
        if classifications[feature]
        in {
            "permitted-built-in-tool",
            "must-be-disabled-tool-bearing-behavior",
        }
    ]
    permitted = set(projection["permitted_tool_features"])
    permitted_non_tool = set(projection["permitted_non_tool_features"])
    enabled_features = {
        feature for feature, enabled in inventory.items() if enabled
    }
    if (
        {row["feature"] for row in rows if row["enabled"]} != permitted
        or not permitted <= enabled_features
        or enabled_features - permitted - permitted_non_tool
    ):
        raise BoundaryRuntimeError(
            "file-change-control-mismatch", "pre-turn-start"
        )
    return rows


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
        or active_profile
        != {"id": "boundary-proof-stage-readonly-v1", "extends": None}
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
            "active_permission_profile": "boundary-proof-stage-readonly-v1",
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
        "permissions": "boundary-proof-stage-readonly-v1",
        "runtimeWorkspaceRoots": [str(workspace)],
    }


def _turn_start_request(
    thread_id: str,
    workspace: Path,
    model_id: str,
    runtime_home: Path,
    prompt: str,
    required_reference_text: str,
    output_schema: Mapping[str, object],
    skill_names: Sequence[str] = PARTICIPATING_SKILLS,
) -> dict[str, object]:
    if (
        len(skill_names) != len(set(skill_names))
        or any(name not in PARTICIPATING_SKILLS for name in skill_names)
        or not required_reference_text
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
        "input": [
            *skill_inputs,
            {
                "type": "text",
                "text": (
                    "Required installed boundary-proof reference:\n\n"
                    + required_reference_text
                ),
            },
            {"type": "text", "text": prompt},
        ],
        "cwd": str(workspace),
        "model": model_id,
        "permissions": "boundary-proof-stage-readonly-v1",
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
    forbidden_candidate_values: Sequence[str] = (),
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
            "boundary-proof-stage-readonly-v1",
                "--include-managed-config",
                "--cd",
                str(workspace),
                "--",
                "/usr/bin/env",
            ),
            env=environment,
        )
        if environment_probe.returncode != 0:
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
                raise BoundaryRuntimeError(
                    "credential-isolation-failed", "pre-turn-start"
                )
        _probe_workspace_write_denial(
            executable, environment, workspace, probe_source
        )
        _probe_descendant_workspace_write_denial(
            executable, environment, workspace, probe_source
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
        complete_runtime_projection = _validate_runtime_projection(
            version,
            launcher_before.digest,
            package_identity,
            schema_identity,
            protocol_classification,
        )
        runtime_process_id = "process-" + secrets.token_hex(16)
        timeout_elapsed_ms: int | None = None
        server = _AppServer(executable, environment)
        turn_timeout = False
        generation_result: dict[str, object] | None = None
        expected_outputs: list[str] = []
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
            runtime_projection = complete_runtime_projection(
                feature_classification
            )
            effective_tool_projection = _effective_tool_projection(
                pages, feature_classification, runtime_projection
            )
            handler_conformance = _run_file_change_handler_conformance(
                FILE_CHANGE_AUTHORIZATION_POLICY
            )
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
                != "boundary-proof-stage-readonly-v1"
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
            thread_request = _thread_start_request(workspace, model_id)
            if generation_request is not None:
                _assert_parent_only_candidate_isolation(
                    serialized_request=generation_request,
                    workspace_inventory=_workspace_probe_snapshot(workspace),
                    child_access_observations=[thread_request],
                    forbidden_candidate_values=forbidden_candidate_values,
                )
            thread = server.request("thread/start", thread_request)
            thread_metadata, thread_id = _validated_thread_metadata(
                thread,
                version=version,
                model_id=model_id,
                workspace=workspace,
            )
            capability_state = str(
                runtime_projection["file_change_capability_state"]
            )
            if capability_state == "exposed-live-probe-required":
                raise BoundaryRuntimeError(
                    "runtime-projection-unsupported", "pre-thread-start"
                )
            if capability_state != "not-exposed-projection":
                raise BoundaryRuntimeError(
                    "runtime-projection-unsupported", "pre-thread-start"
                )
            if generation_request is not None:
                prompt = generation_request.get("prompt")
                output_schema = generation_request.get("output_schema")
                skill_names = generation_request.get("skill_names")
                expected_output_value = generation_request.get(
                    "expected_outputs", []
                )
                if not isinstance(prompt, str) or not isinstance(
                    output_schema, dict
                ) or not isinstance(skill_names, list) or any(
                    not isinstance(name, str) for name in skill_names
                ) or not isinstance(expected_output_value, list) or any(
                    not isinstance(path, str) for path in expected_output_value
                ):
                    raise BoundaryRuntimeError("protocol-shape-incompatible")
                expected_outputs = list(expected_output_value)
                reference_path = (
                    runtime_home
                    / "skills"
                    / skill_names[-1]
                    / "references"
                    / "boundary-proof-model.md"
                )
                try:
                    required_reference_text = reference_path.read_text(
                        encoding="utf-8"
                    )
                except (OSError, UnicodeError) as error:
                    raise BoundaryRuntimeError(
                        "unmanifested-input", "pre-turn-start"
                    ) from error
                if not required_reference_text:
                    raise BoundaryRuntimeError(
                        "unmanifested-input", "pre-turn-start"
                    )
                workspace_before_turn = _workspace_probe_snapshot(workspace)
                turn_request = _turn_start_request(
                    thread_id,
                    workspace,
                    model_id,
                    runtime_home,
                    prompt,
                    required_reference_text,
                    output_schema,
                    skill_names,
                )
                _assert_parent_only_candidate_isolation(
                    serialized_request=turn_request,
                    workspace_inventory=workspace_before_turn,
                    child_access_observations=[thread_request, turn_request],
                    forbidden_candidate_values=forbidden_candidate_values,
                )
                started = server.request(
                    "turn/start",
                    turn_request,
                )
                if (
                    not isinstance(started, dict)
                    or set(started) != {"turn"}
                    or not isinstance(started["turn"], dict)
                    or not isinstance(started["turn"].get("id"), str)
                ):
                    raise BoundaryRuntimeError(
                        "protocol-shape-incompatible"
                    )
                try:
                    turn_started = time.monotonic()
                    generation_result = server.collect_turn(
                        thread_id,
                        protocol_classification,
                        timeout=(
                            int(TRANSPORT_POLICY["turn_deadline_ms"]) // 1000
                        ),
                        file_change_policy=FILE_CHANGE_AUTHORIZATION_POLICY,
                        turn_id=started["turn"]["id"],
                        file_change_capability_state=capability_state,
                    )
                except _StageTurnTimeout:
                    turn_timeout = True
                    timeout_elapsed_ms = int(
                        (time.monotonic() - turn_started) * 1000
                    )
                if generation_sink is None:
                    raise BoundaryRuntimeError("protocol-shape-incompatible")
        finally:
            server.close()
        output_files = _collect_workspace_outputs(workspace, expected_outputs)
        if output_files:
            raise BoundaryRuntimeError(
                "unexpected-prohibited-event", "in-turn"
            )
        if generation_request is not None and not turn_timeout:
            if generation_result is None:
                raise BoundaryRuntimeError("protocol-shape-incompatible")
            if _workspace_probe_snapshot(workspace) != workspace_before_turn:
                raise BoundaryRuntimeError(
                    "unexpected-prohibited-event", "in-turn"
                )
            message = generation_result.get("agent_message")
            if not isinstance(message, str):
                raise BoundaryRuntimeError("protocol-shape-incompatible")
            envelope, output_files = _parse_stage_envelope(
                message,
                stage=str(generation_request["stage"]),
                attempt=int(generation_request.get("attempt", 1)),
            )
            materialization = _materialize_stage_envelope(
                workspace / "output", envelope
            )
            generation_result["thread_id"] = thread_id
            generation_result["stage"] = generation_request.get("stage")
            generation_result["skill_names"] = list(skill_names)
            generation_result["runtime_process_id"] = runtime_process_id
            generation_result["output_files"] = output_files
            generation_result["stage_envelope"] = envelope
            generation_result["materialization_observation"] = materialization
            generation_sink.append(generation_result)
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
        attestation = {
            "schema_version": "boundary-runtime-attestation-v3",
            "runtime_launcher_identity": launcher_before.digest,
            "runtime_package_identity": package_identity,
            "schema_bundle_identity": schema_identity,
            "generated_config_identity": config_identity,
            "managed_requirements_identity": _sha256(
                _canonical_json_bytes(requirements)
            ),
            "active_permission_profile": "boundary-proof-stage-readonly-v1",
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
            "runtime_projection_id": runtime_projection["projection_id"],
            "runtime_projection_identity": runtime_projection_identity(
                runtime_projection
            ),
            "file_change_capability_state": capability_state,
            "effective_tool_projection_identity": _sha256(
                _canonical_json_bytes(effective_tool_projection)
            ),
            "file_change_authorization_policy_identity": _sha256(
                _canonical_json_bytes(FILE_CHANGE_AUTHORIZATION_POLICY)
            ),
            "file_change_handler_conformance_identity": handler_conformance[
                "result_identity"
            ],
            "materialization_canary_policy_identity": _sha256(
                _canonical_json_bytes(MATERIALIZATION_CANARY_POLICY)
            ),
            "probe_results": {
                "workspace_read": "pass",
                "workspace_write_denied": "pass",
                "descendant_workspace_write_denied": "pass",
                "workspace_file_change_denied": "pass",
                "unmanifested_source_denied": "pass",
                "private_auth_denied": "pass",
                "network_denied": "pass",
                "stage_envelope_materialization": "pass",
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
        if turn_timeout:
            raise _StageTurnTimeout(
                attestation=attestation,
                output_files=output_files,
                termination_state="confirmed-stopped",
                runtime_thread_id=thread_id,
                runtime_process_id=runtime_process_id,
                elapsed_ms=timeout_elapsed_ms,
            )
        return attestation


def _validate_attestation(attestation: Mapping[str, object]) -> None:
    if set(attestation) != set(ATTESTATION_FIELDS):
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    if attestation.get("schema_version") != "boundary-runtime-attestation-v3":
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    for field in ATTESTATION_FIELDS:
        if field.endswith("_identity") and (
            not isinstance(attestation[field], str)
            or IDENTITY_PATTERN.fullmatch(attestation[field]) is None
        ):
            raise BoundaryRuntimeError("protocol-shape-incompatible")
    if (
        attestation.get("active_permission_profile")
        != "boundary-proof-stage-readonly-v1"
    ):
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
        != "boundary-proof-stage-readonly-v1"
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
    try:
        projection = select_runtime_projection(
            runtime_version=str(thread_metadata["cli_version"]),
            runtime_launcher_identity=str(
                attestation["runtime_launcher_identity"]
            ),
            runtime_package_identity=str(
                attestation["runtime_package_identity"]
            ),
            schema_bundle_identity=str(attestation["schema_bundle_identity"]),
            protocol_item_classification_identity=str(
                attestation["protocol_item_classification_identity"]
            ),
            feature_classification_identity=str(
                attestation["feature_classification_identity"]
            ),
        )
    except (BoundaryProofError, TypeError) as error:
        raise BoundaryRuntimeError(
            "runtime-projection-unsupported", "pre-thread-start"
        ) from error
    if (
        attestation.get("runtime_projection_id")
        != projection["projection_id"]
        or attestation.get("runtime_projection_identity")
        != runtime_projection_identity(projection)
        or attestation.get("file_change_capability_state")
        != projection["file_change_capability_state"]
    ):
        raise BoundaryRuntimeError(
            "runtime-projection-unsupported", "pre-thread-start"
        )
    expected_probe_keys = {
        "workspace_read",
        "workspace_write_denied",
        "descendant_workspace_write_denied",
        "workspace_file_change_denied",
        "unmanifested_source_denied",
        "private_auth_denied",
        "network_denied",
        "stage_envelope_materialization",
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
        attestation.get("file_change_authorization_policy_identity")
        != _sha256(_canonical_json_bytes(FILE_CHANGE_AUTHORIZATION_POLICY))
        or attestation.get("materialization_canary_policy_identity")
        != _sha256(_canonical_json_bytes(MATERIALIZATION_CANARY_POLICY))
    ):
        raise BoundaryRuntimeError("protocol-shape-incompatible")
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
        "schema_version": "boundary-runtime-preflight-v3",
        "result": "pass",
        "diagnostic_id": "none",
        "phase": "pre-turn-start",
        "attestation_ref": attestation_ref,
        "workspace_failure": None,
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
