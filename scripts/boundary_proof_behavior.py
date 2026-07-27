#!/usr/bin/env python3
"""Standalone hermetic behavior harness for boundary-first proof evidence."""

from __future__ import annotations

import argparse
import ast
import fcntl
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
import traceback
import tomllib
from collections.abc import Callable, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Final

from boundary_proof_model import (
    CORE_DIMENSION_IDS,
    EVALUATED_SKILLS,
    HANDLER_CONFORMANCE_CASES,
    PRESERVATION_KEYS,
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
BOUNDARY_PROOF_REFERENCE: Final[str] = (
    "references/boundary-proof-model.md"
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
    "publisher-active": frozenset({"pre-thread-start"}),
    "runtime-unavailable": frozenset({"pre-thread-start"}),
    "runtime-unreadable": frozenset({"pre-thread-start"}),
    "runtime-version-invalid": frozenset({"pre-thread-start"}),
    "runtime-version-unsupported": frozenset({"pre-thread-start"}),
    "runtime-identity-unstable": frozenset(
        {"pre-thread-start", "pre-turn-start", "in-turn"}
    ),
    "schema-bundle-invalid": frozenset({"pre-thread-start"}),
    "experimental-api-unavailable": frozenset({"pre-thread-start"}),
    "protocol-shape-incompatible": frozenset(
        {"pre-thread-start", "in-turn"}
    ),
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
    "correction-authorization-required": frozenset({"in-turn"}),
    "review-nonapproval": frozenset({"in-turn"}),
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
RUN_MANIFEST_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "run_id",
        "publisher_instance_id",
        "input_set",
        "input_set_identity",
        "baseline_commit",
        "before_artifact_inventory",
        "after_artifact_inventory",
        "snapshots",
        "events",
        "transport_attempts",
    }
)
PUBLISHER_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "schema_version",
        "publisher_instance_id",
        "run_id",
        "input_set_identity",
        "prior_pointer",
        "working_root",
        "staging_root",
        "target_root",
    }
)
PREPARED_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "publisher_instance_id",
        "run_id",
        "input_set_identity",
        "staged_manifest_snapshot",
        "target_manifest",
        "prior_pointer",
    }
)
RECOVERY_BASIS_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "schema_version",
        "recovery_id",
        "run_id",
        "publisher_instance_id",
        "authorized_by",
        "authorization_evidence_ref",
        "publisher_lease_snapshot",
        "publisher_lock_proof",
        "orphan_snapshot",
        "input_set_identity",
        "action",
    }
)
RECOVERY_STATE_FIELDS: Final[frozenset[str]] = frozenset(
    {"schema_version", "recovery_id", "basis_identity", "state"}
)
RECOVERY_DECISION_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "schema_version",
        "change_id",
        "run_id",
        "publisher_instance_id",
        "input_set_identity",
        "action",
        "authorized_by",
        "outcome",
    }
)
CORRECTION_STOP_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "schema_version",
        "run_id",
        "publisher_instance_id",
        "input_set_identity",
        "stage",
        "attempt",
        "review_id",
        "reviewed_artifact_identity",
        "material_finding_ids",
        "finding_projection_identity",
        "diagnostic_id",
    }
)
CORRECTION_STOP_EVIDENCE_FILES: Final[frozenset[str]] = frozenset(
    {
        "review-record.md",
        "review-log.md",
        "review-resolution.md",
        "review-bundle.json",
        "review-event.json",
        "finding-projection.json",
    }
)
CORRECTION_STOP_BUNDLE_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "schema_version",
        "stage",
        "attempt",
        "review_id",
        "outcome",
        "reviewed_artifact_identity",
        "material_finding_ids",
        "finding_projection_identity",
        "correction_eligibility",
        "artifact_refs",
    }
)
CORRECTION_STOP_EVENT_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "schema_version",
        "stage",
        "attempt",
        "observed_result",
        "diagnostic_id",
        "evidence_refs",
    }
)
RUN_ID_PATTERN: Final[re.Pattern[str]] = re.compile(r"^run-[0-9a-f]{32}$")
PUBLISHER_ID_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^publisher-[0-9a-f]{32}$"
)
RECOVERY_ID_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^recovery-[0-9a-f]{32}$"
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


def _trace_prohibited_event(subreason: str, **shape: object) -> None:
    """Emit opt-in, value-free detail for a closed prohibited-event result."""

    if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") != "1":
        return
    fields = ":".join(
        f"{key}={value}"
        for key, value in sorted(shape.items())
        if isinstance(value, (bool, int, str)) or value is None
    )
    suffix = "" if not fields else ":" + fields
    print(f"prohibited-event:{subreason}{suffix}", file=sys.stderr)


def _trace_transport_decision(
    *,
    attempt: int,
    termination_state: str,
    output_state: str,
    decision: str,
) -> None:
    """Emit the closed, value-free transport tuple selected by the coordinator."""

    if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") != "1":
        return
    print(
        "transport-decision:"
        f"attempt={attempt}:"
        f"termination_state={termination_state}:"
        f"output_state={output_state}:"
        f"decision={decision}",
        file=sys.stderr,
    )


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
        or path == simple_prefix + "publisher.lock"
        or path == simple_prefix + "publisher.json"
        or path == simple_prefix + "prepared.json"
        or path.startswith(simple_prefix + ".working-")
        or path.startswith(simple_prefix + ".prepared-")
        or path.startswith(simple_prefix + ".current-")
        or path.startswith(simple_prefix + "manual-recovery-")
        or path.startswith(simple_prefix + "manual-recovery-state-")
        or path.startswith(simple_prefix + ".manual-recovery-")
        or path.startswith(simple_prefix + ".recovery-quarantine-")
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
    extension_none_count = sum(
        line.strip() == "Extensions: none." for line in lines
    )
    extension_table_count = sum(line.strip() == "Extensions:" for line in lines)
    if extension_none_count + extension_table_count != 1:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    extensions: list[dict[str, object]] = []
    if extension_table_count == 1:
        extension_header, extension_rows = _table_after(lines, "Extensions:")
        if extension_header != [
            "Extension ID",
            "Title",
            "Applicability",
            "Rationale",
            "Governing requirement IDs",
            "Boundary IDs",
            "Non-applicability rationale",
        ]:
            raise BoundaryRuntimeError("runtime-identity-unstable")
        extensions = [
            {
                "extension_id": row[0],
                "title": row[1],
                "applicability": row[2],
                "rationale": row[3],
                "governing_requirement_ids": _csv(row[4]),
                "boundary_ids": _csv(row[5]),
                "non_applicability_rationale": (
                    None if row[6] == "-" else row[6]
                ),
            }
            for row in extension_rows
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
    if any(line.startswith("| Interaction ID |") for line in lines):
        interaction_header, interaction_rows = _table_after(lines, "## Interactions")
        if interaction_header != [
            "Interaction ID",
            "Governing requirement IDs",
            "Boundary IDs",
            "Rationale",
        ]:
            raise BoundaryRuntimeError("runtime-identity-unstable")
        interactions = [
            {
                "interaction_id": row[0],
                "governing_requirement_ids": _csv(row[1]),
                "boundary_ids": _csv(row[2]),
                "rationale": row[3],
            }
            for row in interaction_rows
        ]
    return {
        "boundary_model_version": version_rows[0],
        "boundary_model_scope": scope_rows[0],
        "core_dimensions": core,
        "extensions": extensions,
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
            if (
                match := re.match(r"^(?:#{1,6}\s+)?(T[0-9]+)\.", line)
            )
            is not None
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
    governing_reference_ids: Sequence[str] = (),
    governing_interaction_ids: Sequence[str] = (),
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
    if (
        governing_reference_ids
        and (
            stage != "test-spec"
            or len(set(governing_reference_ids))
            != len(governing_reference_ids)
            or any(
                not isinstance(value, str)
                or re.fullmatch(
                    r"^[a-z][a-z0-9-]*(?:\.[a-z][a-z0-9-]*)+$",
                    value,
                )
                is None
                for value in governing_reference_ids
            )
        )
    ):
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    if (
        governing_interaction_ids
        and (
            stage != "test-spec"
            or len(set(governing_interaction_ids))
            != len(governing_interaction_ids)
            or not set(governing_interaction_ids)
            <= set(governing_reference_ids)
        )
    ):
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    variants = _stage_policy_variants(stage, attempt)
    structure_instruction = {
        "spec": (
            "Use the exact markers `Boundary model version: v1` and "
            "`Boundary model scope: R1-R4`, followed by exact sections "
            "`## Boundary model`, `## Examples`, and `## Interactions`. "
            "Keep `## Boundary model`, one extension marker, `## Examples`, "
            "and `## Interactions` contiguous in that exact order, before any "
            "other following section. Use exactly `Extensions: none.` when "
            "there is no meaningful feature-specific dimension. Otherwise "
            "use `Extensions:` followed by exactly this table header: "
            "`Extension ID | Title | Applicability | Rationale | Governing "
            "requirement IDs | Boundary IDs | Non-applicability rationale`. "
            "The Boundary model, optional Extensions, and Examples tables "
            "must use the exact columns defined by the attached "
            "boundary-proof reference. Use all twelve closed core dimension "
            "IDs exactly once and governing requirement IDs R1, R2, R3, and "
            "R4. Every extension ID must use the narrower exact grammar "
            "`^x\\.[a-z][a-z0-9-]*(\\.[a-z][a-z0-9-]*)+$`. "
            "Each boundary ID must appear in exactly one boundary row; examples "
            "may cite those IDs but must not redefine them. Every example's "
            "governing requirement IDs must be a subset of the union owned by "
            "its cited boundaries and must overlap each cited boundary. "
            "Before returning, audit each example independently: compute the "
            "exact requirement-owner union of its cited boundaries and remove "
            "any example requirement outside that union. If the example needs "
            "such a requirement, define an applicable requirement-owned "
            "boundary for it instead of borrowing an unrelated boundary. "
            "Apply the reference's interaction-selection rule whenever "
            "correctness depends on boundaries composing; do not default to "
            "no interaction merely because the feature is small. "
            "For every selected interaction, use exactly one closed rationale "
            "value: `state-coupling`, `trust-or-authority`, "
            "`mutation-or-recovery`, `compatibility-or-migration`, "
            "`composed-path`, or `incident-evidence`; never put prose in the "
            "Rationale cell. "
            "Every authored stable ID must match "
            "`^[a-z][a-z0-9-]*(\\.[a-z][a-z0-9-]*)+$`; IDs must be dotted. "
            "As a final referential-integrity audit, require the union of "
            "governing requirement IDs across boundary, extension, and "
            "interaction rows to equal exactly `R1`, `R2`, `R3`, and `R4`; "
            "require every boundary ID cited by an example or interaction to "
            "exist in exactly one boundary or extension row; and reject the "
            "draft yourself if any requirement is unowned or any cited ID is "
            "orphaned. "
            "Use the literal ASCII `-` for every empty table value; never "
            "use a blank cell or a Unicode dash. "
        ),
        "test-spec": (
            "Use the exact markers `Boundary model version: v1` and "
            "`Boundary model scope: R1-R4`, followed by exact sections "
            "`## Proof map` and `## Test cases`. The Proof map table must "
            "use the exact columns defined by the attached boundary-proof "
            "reference and collectively govern exactly R1, R2, R3, and R4. "
            "Every proof-obligation and manual-procedure ID must match "
            "`^[a-z][a-z0-9-]*(\\.[a-z][a-z0-9-]*)+$`; IDs must be dotted. "
            "Every proof-map boundary or interaction reference must exactly "
            "match an ID defined by the attached governing feature's boundary "
            "record. Do not invent, rename, infer, or repair an ID. "
            "Use `T1`, `T2`, and subsequent uppercase numeric IDs for both "
            "proof-map test-case references and matching `## Test cases` "
            "records. "
            "Use the literal ASCII `-` for every empty table value; never "
            "use a blank cell or a Unicode dash. "
        ),
        "spec-review": (
            "Use the installed normative review-result skeleton. In both the "
            "review record and review log, include exact metadata lines "
            f"`Review ID: spec-review-r{attempt}`, `Stage: spec-review`, "
            "`Status: <approved | changes-requested | blocked | inconclusive>`, "
            "`Reviewed artifact identity: <the supplied sha256 identity>`, "
            "`Material findings: <IDs or none>`, and "
            "`Recording status: recorded`. Preserve independent judgment; do "
            "not report `approved` when a material finding exists. "
        ),
        "test-spec-review": (
            "Use the installed normative review-result skeleton. In both the "
            "review record and review log, include exact metadata lines "
            f"`Review ID: test-spec-review-r{attempt}`, "
            "`Stage: test-spec-review`, "
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
            + "\nAllowed artifact sets:\n"
            + "\n".join(
                "- "
                + str(row["artifact_set_variant"])
                + ": "
                + ", ".join(
                    str(artifact["role"]) + "=" + str(artifact["path"])
                    for artifact in row["artifacts"]
                )
                for row in variants
            )
            + "\nExpected paths:\n- "
            + "\n- ".join(expected_outputs)
            + (
                "\nClosed governing boundary and interaction IDs:\n- "
                + "\n- ".join(governing_reference_ids)
                + "\nEvery proof-map boundary or interaction reference must "
                "be one exact member of this closed list. The test spec does "
                "not own boundary or interaction definitions. Copy needed IDs "
                "verbatim, perform a final membership audit, and never coin a "
                "replacement.\n"
                + (
                    "The governing feature selected these interactions:\n- "
                    + "\n- ".join(governing_interaction_ids)
                    if governing_interaction_ids
                    else (
                        "The governing feature selected no interactions. Do "
                        "not add an interaction reference or interaction proof "
                        "obligation."
                    )
                )
                if governing_reference_ids
                else ""
            )
            + "\n\nRequest:\n"
            + request
            + (
                "\n\nMandatory boundary-table serialization: every "
                "`applicable` core row MUST put the literal ASCII `-` in "
                "`Non-applicability rationale`; every `not-applicable` core "
                "row MUST put `-` in both proof-link columns and a nonempty "
                "rationale in that final column. Explanations for applicable "
                "rows belong outside the non-applicability field."
                if stage == "spec"
                else ""
            )
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
    output_root: Path,
    envelope: Mapping[str, object],
    *,
    attempt: int | None = None,
) -> dict[str, object]:
    stage = envelope.get("last_stage")
    if not isinstance(stage, str):
        raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
    if attempt is None:
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
        attempt = attempts[0]
    parsed, rows = _parse_stage_envelope(
        _canonical_json_bytes(dict(envelope)).decode("utf-8"),
        stage=stage,
        attempt=attempt,
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


def _output_state_for_allowed_sets(
    allowed_path_sets: Sequence[Sequence[str]],
    output_files: Sequence[Mapping[str, object]],
) -> str:
    """Classify output against mutually exclusive policy-approved artifact sets."""

    if not allowed_path_sets:
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    observed_paths = [row.get("path") for row in output_files]
    if any(not isinstance(path, str) for path in observed_paths):
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    if len(observed_paths) != len(set(observed_paths)):
        return "contradictory"
    actual = set(observed_paths)
    if not actual:
        return "absent"
    permitted = [set(paths) for paths in allowed_path_sets]
    if any(len(paths) != len(set(paths)) for paths in allowed_path_sets):
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    if actual in permitted:
        return "complete"
    if any(actual < candidate for candidate in permitted):
        return "partial"
    if any(candidate < actual for candidate in permitted):
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
    *,
    allowed_path_sets: Sequence[Sequence[str]] | None = None,
) -> tuple[dict[str, object], dict[str, object], list[dict[str, object]]]:
    attempts: list[dict[str, object]] = []
    for attempt in (1, 2):
        try:
            attestation, result = invoke()
        except _StageTurnTimeout as error:
            if error.termination_state != "confirmed-stopped":
                _trace_transport_decision(
                    attempt=attempt,
                    termination_state=error.termination_state,
                    output_state="uninspected",
                    decision="pause",
                )
                raise BoundaryRuntimeError(
                    "unexpected-prohibited-event", "in-turn"
                ) from error
            state = (
                _output_state_for_allowed_sets(
                    allowed_path_sets, error.output_files
                )
                if allowed_path_sets is not None
                else _output_state(required_paths, error.output_files)
            )
            if state == "complete" and error.attestation is not None:
                _trace_transport_decision(
                    attempt=attempt,
                    termination_state=error.termination_state,
                    output_state=state,
                    decision="reconcile",
                )
                attempts.append(
                    {
                        "transport_attempt": attempt,
                        "output_state": state,
                        "decision": "reconcile",
                        "runtime_thread_id": error.runtime_thread_id,
                        "runtime_process_id": error.runtime_process_id,
                        "elapsed_ms": error.elapsed_ms,
                        "timed_out": True,
                        "artifact_paths": sorted(
                            str(row["path"]) for row in error.output_files
                        ),
                        "required_paths": list(required_paths),
                    }
                )
                return (
                    error.attestation,
                    {"output_files": error.output_files},
                    attempts,
                )
            if state == "absent" and attempt == 1:
                _trace_transport_decision(
                    attempt=attempt,
                    termination_state=error.termination_state,
                    output_state=state,
                    decision="retry",
                )
                attempts.append(
                    {
                        "transport_attempt": attempt,
                        "output_state": state,
                        "decision": "retry",
                        "runtime_thread_id": error.runtime_thread_id,
                        "runtime_process_id": error.runtime_process_id,
                        "elapsed_ms": error.elapsed_ms,
                        "timed_out": True,
                        "artifact_paths": [],
                        "required_paths": list(required_paths),
                    }
                )
                continue
            _trace_transport_decision(
                attempt=attempt,
                termination_state=error.termination_state,
                output_state=state,
                decision="fail-closed",
            )
            attempts.append(
                {
                    "transport_attempt": attempt,
                    "output_state": state,
                    "decision": "fail-closed",
                    "runtime_thread_id": error.runtime_thread_id,
                    "runtime_process_id": error.runtime_process_id,
                    "elapsed_ms": error.elapsed_ms,
                    "timed_out": True,
                    "artifact_paths": sorted(
                        str(row.get("path")) for row in error.output_files
                    ),
                    "required_paths": list(required_paths),
                }
            )
            raise BoundaryRuntimeError(
                "unexpected-prohibited-event", "in-turn"
            ) from error
        output_files = result.get("output_files")
        if not isinstance(output_files, list):
            raise BoundaryRuntimeError("protocol-shape-incompatible")
        state = (
            _output_state_for_allowed_sets(allowed_path_sets, output_files)
            if allowed_path_sets is not None
            else _output_state(required_paths, output_files)
        )
        if state != "complete":
            _trace_transport_decision(
                attempt=attempt,
                termination_state="completed",
                output_state=state,
                decision="fail-closed",
            )
            raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
        _trace_transport_decision(
            attempt=attempt,
            termination_state="completed",
            output_state=state,
            decision="accept",
        )
        attempts.append(
            {
                "transport_attempt": attempt,
                "output_state": state,
                "decision": "accept",
                "runtime_thread_id": result.get("thread_id"),
                "runtime_process_id": result.get("runtime_process_id"),
                "elapsed_ms": None,
                "timed_out": False,
                "artifact_paths": sorted(
                    str(row["path"]) for row in output_files
                ),
                "required_paths": list(required_paths),
            }
        )
        return attestation, result, attempts
    raise AssertionError("closed two-attempt loop did not terminate")


def _finalize_transport_rows(
    attempts: Sequence[Mapping[str, object]],
    stage_artifacts_by_event: Mapping[str, Mapping[str, str]],
    transport_policy_identity: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for attempt in attempts:
        event_key = attempt.get("event_key")
        transport_attempt = attempt.get("transport_attempt")
        thread_id = attempt.get("runtime_thread_id")
        process_id = attempt.get("runtime_process_id")
        output_state = attempt.get("output_state")
        decision = attempt.get("decision")
        artifact_paths = attempt.get("artifact_paths")
        required_paths = attempt.get("required_paths")
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
            or not isinstance(artifact_paths, list)
            or any(not isinstance(path, str) for path in artifact_paths)
            or len(artifact_paths) != len(set(artifact_paths))
            or not isinstance(required_paths, list)
            or not required_paths
            or any(not isinstance(path, str) for path in required_paths)
        ):
            raise BoundaryRuntimeError("protocol-shape-incompatible")
        event_artifacts = stage_artifacts_by_event.get(event_key)
        if event_artifacts is None:
            raise BoundaryRuntimeError("protocol-shape-incompatible")
        evidence_refs = (
            [
                {
                    "path": path,
                    "identity": _sha256(
                        event_artifacts[path].encode("utf-8")
                    ),
                }
                for path in artifact_paths
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
                        "role": (
                            f"{event_key.rsplit('#', 1)[0]}-output-{index}"
                        ),
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
    observed_events = frozenset(grouped)
    allowed_event_sets = {
        frozenset(
            {
                "spec#1",
                "spec-review#1",
                "test-spec#1",
                "test-spec-review#1",
            }
        ),
        frozenset(
            {
                "spec#1",
                "spec-review#1",
                "spec#2",
                "spec-review#2",
                "test-spec#1",
                "test-spec-review#1",
            }
        ),
        frozenset(
            {
                "spec#1",
                "spec-review#1",
                "test-spec#1",
                "test-spec-review#1",
                "test-spec#2",
                "test-spec-review#2",
            }
        ),
    }
    if observed_events not in allowed_event_sets:
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


FINDING_PROJECTION_LABELS: Final[tuple[str, ...]] = (
    "Finding ID",
    "Evidence",
    "Required outcome",
    "Safe resolution path",
    "needs-decision rationale",
)
FINDING_ID_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^[a-z][a-z0-9-]*(?:\.[a-z][a-z0-9-]*)+$"
)


def _finding_projection(
    record: str,
    outcome: object,
    material_finding_ids: Sequence[object],
) -> list[dict[str, str]]:
    """Derive the closed correction-authority projection from review bytes."""

    if outcome != "changes-requested":
        return []
    headings = list(
        re.finditer(
            r"(?m)^## Finding ([a-z][a-z0-9-]*(?:\.[a-z][a-z0-9-]*)+)$",
            record,
        )
    )
    expected_ids = [
        value for value in material_finding_ids if isinstance(value, str)
    ]
    if (
        len(expected_ids) != len(material_finding_ids)
        or expected_ids != sorted(expected_ids)
        or len(expected_ids) != len(set(expected_ids))
        or [match.group(1) for match in headings] != expected_ids
    ):
        raise BoundaryRuntimeError("protocol-shape-incompatible", "in-turn")
    rows: list[dict[str, str]] = []
    label_pattern = re.compile(
        r"^- (" + "|".join(re.escape(label) for label in FINDING_PROJECTION_LABELS)
        + r"):\s*(.*)$"
    )
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(record)
        block = record[heading.end():end]
        recognized: list[tuple[str, str]] = []
        for line in block.splitlines():
            match = label_pattern.fullmatch(line)
            if match is not None:
                recognized.append((match.group(1), match.group(2).strip(" ")))
        if (
            [label for label, _ in recognized] != list(FINDING_PROJECTION_LABELS)
            or any(not value for _, value in recognized)
            or recognized[0][1] != heading.group(1)
        ):
            raise BoundaryRuntimeError("protocol-shape-incompatible", "in-turn")
        values = dict(recognized)
        rows.append(
            {
                "finding_id": values["Finding ID"],
                "evidence": values["Evidence"],
                "required_outcome": values["Required outcome"],
                "safe_resolution_path": values["Safe resolution path"],
                "needs_decision_rationale": values[
                    "needs-decision rationale"
                ],
            }
        )
    return rows


def _correction_eligibility(
    outcome: object, finding_projection: Sequence[Mapping[str, str]]
) -> str:
    if outcome != "changes-requested":
        return "not-applicable"
    if any(
        row["needs_decision_rationale"] != "none"
        for row in finding_projection
    ):
        return "owner-decision-required"
    if finding_projection and all(
        row["evidence"]
        and row["required_outcome"]
        and row["safe_resolution_path"]
        for row in finding_projection
    ):
        return "automatic-eligible"
    raise BoundaryRuntimeError("protocol-shape-incompatible", "in-turn")


def _validate_review_payload(
    payload: Mapping[str, object],
    *,
    stage: str,
    artifact_identity: str,
    require_approval: bool = True,
) -> None:
    review_id = payload.get("review_id")
    outcome = payload.get("outcome")
    record = payload.get("review_record_markdown")
    log = payload.get("review_log_markdown")
    if (
        not isinstance(review_id, str)
        or re.fullmatch(rf"{re.escape(stage)}-r[1-9][0-9]*", review_id) is None
        or outcome
        not in {"approved", "changes-requested", "blocked", "inconclusive"}
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
    if outcome != "approved":
        if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
            print(
                f"review-nonapproval:{stage}:outcome={outcome}",
                file=sys.stderr,
            )
            print(record[:8192], file=sys.stderr)
        if require_approval:
            raise BoundaryRuntimeError("review-nonapproval", "in-turn")
    def metadata(markdown: str, label: str) -> str | None:
        match = re.search(
            rf"(?im)^\s*(?:[-*]\s*)?(?:\*\*)?{re.escape(label)}"
            rf"(?:\*\*)?\s*:\s*(.+?)\s*$",
            markdown,
        )
        if match is None:
            return None
        return match.group(1).strip().rstrip("  ").strip("`* ")

    material_finding_ids = payload.get("material_finding_ids")
    if (
        not isinstance(material_finding_ids, list)
        or any(
            not isinstance(value, str)
            or FINDING_ID_PATTERN.fullmatch(value) is None
            for value in material_finding_ids
        )
        or len(material_finding_ids) != len(set(material_finding_ids))
        or (outcome == "approved") != (not material_finding_ids)
    ):
        raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
    projection = _finding_projection(record, outcome, material_finding_ids)
    projection_identity = _sha256(_canonical_json_bytes(projection))
    eligibility = _correction_eligibility(outcome, projection)
    if (
        payload.get("finding_projection") != projection
        or payload.get("finding_projection_identity") != projection_identity
        or payload.get("correction_eligibility") != eligibility
    ):
        raise BoundaryRuntimeError("protocol-shape-incompatible", "in-turn")
    findings_value = (
        "none" if not material_finding_ids else ", ".join(material_finding_ids)
    )
    required = {
        "Review ID": review_id,
        "Stage": stage,
        "Status": outcome,
        "Reviewed artifact identity": artifact_identity,
        "Material findings": findings_value,
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
    material_findings = metadata(record, "Material findings")
    if (
        not isinstance(review_id, str)
        or not isinstance(outcome, str)
        or not isinstance(material_findings, str)
    ):
        if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
            print(
                f"review-metadata:{stage}:id={review_id!r}:outcome={outcome!r}",
                file=sys.stderr,
            )
            print(record, file=sys.stderr)
        raise BoundaryRuntimeError("unexpected-prohibited-event", "in-turn")
    finding_ids = (
        []
        if material_findings.lower() == "none"
        else [
            value.strip().strip("`")
            for value in material_findings.split(",")
            if value.strip()
        ]
    )
    projection = _finding_projection(record, outcome, finding_ids)
    return {
        "review_id": review_id,
        "outcome": outcome,
        "material_finding_ids": finding_ids,
        "finding_projection": projection,
        "finding_projection_identity": _sha256(
            _canonical_json_bytes(projection)
        ),
        "correction_eligibility": _correction_eligibility(
            outcome, projection
        ),
        "review_record_markdown": record,
        "review_log_markdown": log,
    }


def _validate_correction_stop_receipt(
    receipt: Mapping[str, object],
    *,
    lease: Mapping[str, object] | None = None,
) -> None:
    if (
        set(receipt) != CORRECTION_STOP_FIELDS
        or receipt.get("schema_version")
        != "simple-change-correction-stop-v1"
        or not isinstance(receipt.get("run_id"), str)
        or RUN_ID_PATTERN.fullmatch(str(receipt["run_id"])) is None
        or not isinstance(receipt.get("publisher_instance_id"), str)
        or PUBLISHER_ID_PATTERN.fullmatch(
            str(receipt["publisher_instance_id"])
        )
        is None
        or not isinstance(receipt.get("input_set_identity"), str)
        or IDENTITY_PATTERN.fullmatch(str(receipt["input_set_identity"]))
        is None
        or receipt.get("stage") not in {"spec-review", "test-spec-review"}
        or receipt.get("attempt") != 1
        or not isinstance(receipt.get("review_id"), str)
        or re.fullmatch(
            rf"{re.escape(str(receipt['stage']))}-r[1-9][0-9]*",
            str(receipt["review_id"]),
        )
        is None
        or not isinstance(receipt.get("reviewed_artifact_identity"), str)
        or IDENTITY_PATTERN.fullmatch(
            str(receipt["reviewed_artifact_identity"])
        )
        is None
        or not isinstance(receipt.get("material_finding_ids"), list)
        or receipt["material_finding_ids"]
        != sorted(receipt["material_finding_ids"])
        or len(receipt["material_finding_ids"])
        != len(set(receipt["material_finding_ids"]))
        or not receipt["material_finding_ids"]
        or any(
            not isinstance(value, str)
            or re.fullmatch(
                r"^[a-z][a-z0-9-]*(?:\.[a-z][a-z0-9-]*)+$", value
            )
            is None
            for value in receipt["material_finding_ids"]
        )
        or not isinstance(receipt.get("finding_projection_identity"), str)
        or IDENTITY_PATTERN.fullmatch(
            str(receipt["finding_projection_identity"])
        )
        is None
        or receipt.get("diagnostic_id")
        != "correction-authorization-required"
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    if lease is not None and any(
        receipt[field] != lease[field]
        for field in (
            "run_id",
            "publisher_instance_id",
            "input_set_identity",
        )
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")


def _write_correction_stop(
    working_root: Path,
    lease: Mapping[str, object],
    *,
    stage: str,
    reviewed_artifact_identity: str,
    review_payload: Mapping[str, object],
    resolution_markdown: str,
) -> dict[str, object]:
    if not isinstance(resolution_markdown, str) or not resolution_markdown:
        raise BoundaryRuntimeError("protocol-shape-incompatible", "in-turn")
    evidence_root = working_root / "correction-stop-evidence"
    evidence_root.mkdir(mode=0o700, parents=False, exist_ok=False)
    raw_artifacts = {
        "review-record.md": str(review_payload["review_record_markdown"]).encode(
            "utf-8"
        ),
        "review-log.md": str(review_payload["review_log_markdown"]).encode(
            "utf-8"
        ),
        "review-resolution.md": resolution_markdown.encode("utf-8"),
        "finding-projection.json": _canonical_json_bytes(
            review_payload["finding_projection"]
        ),
    }
    artifact_refs = {
        name.removesuffix(".md").removesuffix(".json"): {
            "path": f"correction-stop-evidence/{name}",
            "identity": _sha256(raw),
        }
        for name, raw in raw_artifacts.items()
    }
    bundle = {
        "schema_version": "simple-change-correction-stop-bundle-v1",
        "stage": stage,
        "attempt": 1,
        "review_id": review_payload["review_id"],
        "outcome": review_payload["outcome"],
        "reviewed_artifact_identity": reviewed_artifact_identity,
        "material_finding_ids": list(
            review_payload["material_finding_ids"]
        ),
        "finding_projection_identity": review_payload[
            "finding_projection_identity"
        ],
        "correction_eligibility": review_payload[
            "correction_eligibility"
        ],
        "artifact_refs": artifact_refs,
    }
    bundle_raw = _canonical_json_bytes(bundle)
    raw_artifacts["review-bundle.json"] = bundle_raw
    bundle_ref = {
        "path": "correction-stop-evidence/review-bundle.json",
        "identity": _sha256(bundle_raw),
    }
    event = {
        "schema_version": "simple-change-correction-stop-event-v1",
        "stage": stage,
        "attempt": 1,
        "observed_result": "changes-requested",
        "diagnostic_id": "correction-authorization-required",
        "evidence_refs": [
            bundle_ref,
            *sorted(
                artifact_refs.values(),
                key=lambda reference: str(reference["path"]),
            ),
        ],
    }
    raw_artifacts["review-event.json"] = _canonical_json_bytes(event)
    if set(raw_artifacts) != CORRECTION_STOP_EVIDENCE_FILES:
        raise BoundaryRuntimeError("runtime-identity-unstable", "in-turn")
    for name, raw in raw_artifacts.items():
        _exclusive_write(evidence_root / name, raw)
    _fsync_directory(evidence_root)
    receipt = {
        "schema_version": "simple-change-correction-stop-v1",
        "run_id": lease["run_id"],
        "publisher_instance_id": lease["publisher_instance_id"],
        "input_set_identity": lease["input_set_identity"],
        "stage": stage,
        "attempt": 1,
        "review_id": review_payload["review_id"],
        "reviewed_artifact_identity": reviewed_artifact_identity,
        "material_finding_ids": list(
            review_payload["material_finding_ids"]
        ),
        "finding_projection_identity": review_payload[
            "finding_projection_identity"
        ],
        "diagnostic_id": "correction-authorization-required",
    }
    _validate_correction_stop_receipt(receipt, lease=lease)
    _exclusive_write(
        working_root / "correction-stop.json",
        _canonical_json_bytes(receipt),
    )
    _fsync_directory(working_root)
    return receipt


def _observed_scenario_outcome(
    events: Sequence[Mapping[str, object]],
) -> tuple[str, str | None]:
    corrected_roles = [
        "feature-spec" if event.get("stage") == "spec" else "test-spec"
        for event in events
        if event.get("stage") in {"spec", "test-spec"}
        and event.get("attempt") == 2
    ]
    if len(corrected_roles) > 1:
        raise BoundaryRuntimeError("boundary-oracle-mismatch", "in-turn")
    if corrected_roles:
        return "one-correction", corrected_roles[0]
    return "zero-correction", None


def _validate_scenario_expectations(
    scenario: Mapping[str, object],
    events: Sequence[Mapping[str, object]],
) -> None:
    observed_branch, corrected_role = _observed_scenario_outcome(events)
    if (
        scenario.get("expected_branch") != observed_branch
        or scenario.get("corrected_role") != corrected_role
    ):
        raise BoundaryRuntimeError("boundary-oracle-mismatch", "in-turn")



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
    attempt: int = 1,
    diagnostic_id: str | None = None,
) -> dict[str, object]:
    evidence = {
        (str(item["path"]), str(item["identity"]))
        for item in (*inputs, output, *bundle_artifacts)
    }
    return {
        "stage": stage,
        "attempt": attempt,
        "input_snapshot_ids": [str(item["snapshot_id"]) for item in inputs],
        "reviewed_snapshot_id": (
            None if reviewed is None else str(reviewed["snapshot_id"])
        ),
        "output_snapshot_ids": [str(output["snapshot_id"])],
        "structural_result": "pass",
        "observed_result": observed,
        "diagnostic_id": (
            diagnostic_id
            if diagnostic_id is not None
            else (
                "none"
                if observed in {"produced", "approved"}
                else "review-nonapproval"
            )
        ),
        "evidence_refs": [
            {"path": path, "identity": identity}
            for path, identity in sorted(evidence)
        ],
    }


def _write_run_artifact(root: Path, relative: str, raw: bytes) -> None:
    target = root / "artifacts" / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)


def _correction_review_bundle(
    authored_snapshot: Callable[
        [str, str, str, bytes], dict[str, object]
    ],
    stage: str,
    attempt: int,
    reviewed: Mapping[str, object],
    review_payload: Mapping[str, object],
    *,
    resolution_markdown: str | None = None,
    prior_finding_ids: Sequence[str] | None = None,
) -> tuple[dict[str, object], dict[str, object], list[dict[str, object]]]:
    """Materialize one identity-bound correction review evidence bundle."""

    record = review_payload.get("review_record_markdown")
    log = review_payload.get("review_log_markdown")
    review_id = review_payload.get("review_id")
    outcome = review_payload.get("outcome")
    findings = review_payload.get("material_finding_ids")
    finding_projection = review_payload.get("finding_projection")
    finding_projection_identity = review_payload.get(
        "finding_projection_identity"
    )
    correction_eligibility = review_payload.get("correction_eligibility")
    if (
        not isinstance(record, str)
        or not isinstance(log, str)
        or not isinstance(review_id, str)
        or outcome not in {"approved", "changes-requested", "blocked"}
        or not isinstance(findings, list)
        or not isinstance(finding_projection, list)
        or not isinstance(finding_projection_identity, str)
        or correction_eligibility
        not in {
            "not-applicable",
            "automatic-eligible",
            "owner-decision-required",
        }
    ):
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    if (
        prior_finding_ids is not None
        and (
            outcome != "approved"
            or not prior_finding_ids
            or list(prior_finding_ids) != sorted(prior_finding_ids)
            or len(prior_finding_ids) != len(set(prior_finding_ids))
            or any(
                FINDING_ID_PATTERN.fullmatch(finding_id) is None
                for finding_id in prior_finding_ids
            )
        )
    ):
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    if (
        (outcome == "approved" and prior_finding_ids is None)
        != (resolution_markdown is None)
        or (
            outcome in {"changes-requested", "blocked"}
            and resolution_markdown is None
        )
    ):
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    bundle_findings = (
        list(prior_finding_ids)
        if prior_finding_ids is not None
        else list(findings)
    )
    if resolution_markdown is not None:
        if any(
            finding_id not in resolution_markdown
            for finding_id in bundle_findings
        ):
            raise BoundaryRuntimeError("protocol-shape-incompatible")
        expected_closeout = (
            "Closeout status: closed"
            if outcome == "approved"
            else "Closeout status: open"
            if outcome == "changes-requested"
            else None
        )
        if (
            expected_closeout is not None
            and expected_closeout not in resolution_markdown
        ):
            raise BoundaryRuntimeError("protocol-shape-incompatible")
    prefix = f"{stage}-attempt-{attempt}"
    record_snapshot = authored_snapshot(
        f"output.{stage}.attempt-{attempt}.record",
        "review-evidence",
        f"review-evidence/{prefix}-record.md",
        record.encode("utf-8"),
    )
    log_snapshot = authored_snapshot(
        f"output.{stage}.attempt-{attempt}.log",
        "review-evidence",
        f"review-evidence/{prefix}-log.md",
        log.encode("utf-8"),
    )
    artifacts = [record_snapshot, log_snapshot]
    refs = {
        "review-record": _snapshot_ref(record_snapshot),
        "review-log": _snapshot_ref(log_snapshot),
    }
    if resolution_markdown is not None:
        resolution_snapshot = authored_snapshot(
            f"output.{stage}.attempt-{attempt}.resolution",
            "review-evidence",
            f"review-evidence/{prefix}-resolution.md",
            resolution_markdown.encode("utf-8"),
        )
        artifacts.append(resolution_snapshot)
        refs["review-resolution"] = _snapshot_ref(resolution_snapshot)
    bundle = {
        "review_id": review_id,
        "outcome": outcome,
        "reviewed_snapshot_id": reviewed["snapshot_id"],
        "material_finding_ids": bundle_findings,
        "finding_projection": list(finding_projection),
        "finding_projection_identity": finding_projection_identity,
        "correction_eligibility": correction_eligibility,
        "artifact_refs": refs,
    }
    bundle_snapshot = authored_snapshot(
        f"output.{stage}.attempt-{attempt}.bundle",
        "review-evidence",
        f"review-evidence/{prefix}-bundle.json",
        _canonical_json_bytes(bundle),
    )
    return bundle_snapshot, bundle, artifacts


def _validate_review_bundle_payloads(
    bundles: Mapping[str, object],
    output_snapshots: Mapping[str, Mapping[str, object]],
    resolve_snapshot: Callable[[Mapping[str, object]], Path],
) -> None:
    """Recompute bundle fields from exact review and resolution bytes."""

    snapshots_by_ref = {
        (str(snapshot["path"]), str(snapshot["identity"])): snapshot
        for snapshot in output_snapshots.values()
    }
    for raw_bundle in bundles.values():
        if not isinstance(raw_bundle, dict):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        artifact_refs = raw_bundle.get("artifact_refs")
        reviewed_snapshot_id = raw_bundle.get("reviewed_snapshot_id")
        findings = raw_bundle.get("material_finding_ids")
        if (
            not isinstance(artifact_refs, dict)
            or not isinstance(reviewed_snapshot_id, str)
            or reviewed_snapshot_id not in output_snapshots
            or not isinstance(findings, list)
            or any(
                not isinstance(finding_id, str)
                or FINDING_ID_PATTERN.fullmatch(finding_id) is None
                for finding_id in findings
            )
            or findings != sorted(findings)
            or len(findings) != len(set(findings))
        ):
            raise BoundaryRuntimeError("runtime-identity-unstable")

        def referenced(role: str) -> Mapping[str, object]:
            reference = artifact_refs.get(role)
            if (
                not isinstance(reference, dict)
                or set(reference) != {"path", "identity"}
            ):
                raise BoundaryRuntimeError("runtime-identity-unstable")
            snapshot = snapshots_by_ref.get(
                (str(reference["path"]), str(reference["identity"]))
            )
            if snapshot is None:
                raise BoundaryRuntimeError("runtime-identity-unstable")
            return snapshot

        record_snapshot = referenced("review-record")
        log_snapshot = referenced("review-log")
        record_name = Path(str(record_snapshot["path"])).name
        stage = (
            "test-spec-review"
            if record_name.startswith("test-spec-review")
            else "spec-review"
            if record_name.startswith("spec-review")
            else None
        )
        if stage is None:
            raise BoundaryRuntimeError("runtime-identity-unstable")
        try:
            record = resolve_snapshot(record_snapshot).read_text(
                encoding="utf-8"
            )
            log = resolve_snapshot(log_snapshot).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise BoundaryRuntimeError(
                "runtime-identity-unstable"
            ) from error
        payload = _review_payload_from_markdown(stage, record, log)
        reviewed = output_snapshots[str(reviewed_snapshot_id)]
        _validate_review_payload(
            payload,
            stage=stage,
            artifact_identity=str(reviewed["identity"]),
            require_approval=False,
        )
        outcome = raw_bundle.get("outcome")
        if (
            raw_bundle.get("review_id") != payload["review_id"]
            or outcome != payload["outcome"]
            or raw_bundle.get("finding_projection")
            != payload["finding_projection"]
            or raw_bundle.get("finding_projection_identity")
            != payload["finding_projection_identity"]
            or raw_bundle.get("correction_eligibility")
            != payload["correction_eligibility"]
            or (
                outcome != "approved"
                and findings != payload["material_finding_ids"]
            )
        ):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        resolution_ref = artifact_refs.get("review-resolution")
        if resolution_ref is not None:
            resolution_snapshot = referenced("review-resolution")
            try:
                resolution = resolve_snapshot(
                    resolution_snapshot
                ).read_text(encoding="utf-8")
            except (OSError, UnicodeError) as error:
                raise BoundaryRuntimeError(
                    "runtime-identity-unstable"
                ) from error
            expected_closeout = (
                "Closeout status: closed"
                if outcome == "approved" and findings
                else "Closeout status: open"
                if outcome == "changes-requested"
                else None
            )
            if (
                any(finding_id not in resolution for finding_id in findings)
                or (
                    expected_closeout is not None
                    and expected_closeout not in resolution
                )
            ):
                raise BoundaryRuntimeError("runtime-identity-unstable")


def _assemble_test_spec_correction_run(
    repo_root: Path,
    change_id: str,
    run_id: str,
    input_set: Mapping[str, object],
    payload: Mapping[str, object],
    candidate_feature: object,
    candidate_proof: object,
    before_inventory: Sequence[Mapping[str, str]],
    repository_after_inventory: Sequence[Mapping[str, str]],
    correction: Mapping[str, object],
    publisher_instance_id: str,
    working_root: Path,
) -> tuple[Path, dict[str, object]]:
    """Assemble the closed R28y test-spec correction branch."""

    evidence_root = _select_change_root(repo_root, change_id) / "evidence"
    simple_root = evidence_root / "simple-change"
    simple_root.mkdir(parents=True, exist_ok=True)
    temporary = working_root
    final_prefix = (
        f"docs/changes/{change_id}/evidence/simple-change/runs/{run_id}"
    )
    stage_artifacts = payload.get("stage_artifacts")
    provenance = payload.get("stage_provenance")
    spec_review_payload = payload.get("spec_review")
    test_review_payload = payload.get("test_spec_review")
    initial_test_review = correction.get("initial_review")
    initial_test_markdown = correction.get("initial_artifact_markdown")
    initial_resolution = correction.get("initial_resolution_markdown")
    corrected_resolution = correction.get("corrected_resolution_markdown")
    if (
        correction.get("role") != "test-spec"
        or not isinstance(stage_artifacts, dict)
        or not isinstance(provenance, list)
        or not isinstance(spec_review_payload, dict)
        or not isinstance(test_review_payload, dict)
        or not isinstance(initial_test_review, dict)
        or not isinstance(initial_test_markdown, str)
        or not isinstance(initial_resolution, str)
        or not isinstance(corrected_resolution, str)
    ):
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    try:
        feature_raw = str(
            stage_artifacts["feature-spec/portable-text-normalizer.md"]
        ).encode("utf-8")
        final_test_raw = str(
            stage_artifacts["test-spec/portable-text-normalizer.test.md"]
        ).encode("utf-8")
        initial_test_raw = initial_test_markdown.encode("utf-8")
        parsed_feature = normalize_feature_model(
            _parse_feature_markdown(feature_raw.decode("utf-8"))
        )
        initial_proof = normalize_proof_map(
            _parse_test_spec_markdown(initial_test_raw.decode("utf-8")),
            parsed_feature,
        )
        final_proof = normalize_proof_map(
            _parse_test_spec_markdown(final_test_raw.decode("utf-8")),
            parsed_feature,
        )
    except (KeyError, UnicodeError, BoundaryProofError) as error:
        raise BoundaryRuntimeError(
            "runtime-identity-unstable", "in-turn"
        ) from error
    if not boundary_invariant_projections_match(
        candidate_feature,
        parsed_feature,
        candidate_proof,
        final_proof,
    ):
        raise BoundaryRuntimeError("boundary-oracle-mismatch", "in-turn")
    provenance_by_occurrence = {
        (row.get("stage"), row.get("attempt")): row
        for row in provenance
        if isinstance(row, dict)
    }
    expected_occurrences = {
        ("spec", 1),
        ("spec-review", 1),
        ("test-spec", 1),
        ("test-spec-review", 1),
        ("test-spec", 2),
        ("test-spec-review", 2),
    }
    if (
        set(provenance_by_occurrence) != expected_occurrences
        or len(
            {
                row.get("thread_id")
                for row in provenance_by_occurrence.values()
            }
        )
        != len(expected_occurrences)
        or any(
            row.get("skill_names") != ["workflow", stage]
            for (stage, _), row in provenance_by_occurrence.items()
        )
    ):
        raise BoundaryRuntimeError("thread-metadata-mismatch", "in-turn")

    def authored_snapshot(
        snapshot_id: str,
        role: str,
        relative: str,
        raw: bytes,
    ) -> dict[str, object]:
        _write_run_artifact(temporary, relative, raw)
        return _snapshot(
            snapshot_id,
            "behavior-output",
            role,
            f"{final_prefix}/artifacts/{relative}",
            raw,
        )

    feature = authored_snapshot(
        "output.feature-spec.one",
        "feature-spec",
        "feature-spec/portable-text-normalizer.md",
        feature_raw,
    )
    test_one = authored_snapshot(
        "output.test-spec.one",
        "test-spec",
        "test-spec/portable-text-normalizer-attempt-1.test.md",
        initial_test_raw,
    )
    test_two = authored_snapshot(
        "output.test-spec.two",
        "test-spec",
        "test-spec/portable-text-normalizer-attempt-2.test.md",
        final_test_raw,
    )

    spec_bundle_snapshot, spec_bundle, spec_artifacts = _correction_review_bundle(
        authored_snapshot, "spec-review", 1, feature, spec_review_payload
    )
    initial_findings = initial_test_review.get("material_finding_ids")
    if not isinstance(initial_findings, list) or not initial_findings:
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    test_bundle_one, test_bundle_one_record, test_artifacts_one = (
        _correction_review_bundle(
            authored_snapshot,
            "test-spec-review",
            1,
            test_one,
            initial_test_review,
            resolution_markdown=initial_resolution,
        )
    )
    test_bundle_two, test_bundle_two_record, test_artifacts_two = (
        _correction_review_bundle(
            authored_snapshot,
            "test-spec-review",
            2,
            test_two,
            test_review_payload,
            resolution_markdown=corrected_resolution,
            prior_finding_ids=initial_findings,
        )
    )
    snapshots = [
        _snapshot(
            "oracle.feature-spec",
            "fixture-candidate",
            "feature-spec",
            (
                "tests/fixtures/boundary-proof/simple-change/candidates/"
                "feature-spec.md"
            ),
            (
                repo_root
                / "tests/fixtures/boundary-proof/simple-change/candidates/"
                "feature-spec.md"
            ).read_bytes(),
        ),
        _snapshot(
            "oracle.test-spec",
            "fixture-candidate",
            "test-spec",
            (
                "tests/fixtures/boundary-proof/simple-change/candidates/"
                "test-spec.md"
            ),
            (
                repo_root
                / "tests/fixtures/boundary-proof/simple-change/candidates/"
                "test-spec.md"
            ).read_bytes(),
        ),
        feature,
        spec_bundle_snapshot,
        *spec_artifacts,
        test_one,
        test_bundle_one,
        *test_artifacts_one,
        test_two,
        test_bundle_two,
        *test_artifacts_two,
    ]
    first_diagnostic = str(initial_findings[0])
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
            test_one,
        ),
        _event(
            "test-spec-review",
            [test_one, feature, spec_bundle_snapshot, *spec_artifacts],
            test_bundle_one,
            reviewed=test_one,
            bundle_artifacts=test_artifacts_one,
            observed="changes-requested",
            diagnostic_id=first_diagnostic,
        ),
        _event(
            "test-spec",
            [
                test_one,
                test_bundle_one,
                *test_artifacts_one,
                feature,
                spec_bundle_snapshot,
                *spec_artifacts,
            ],
            test_two,
            attempt=2,
        ),
        _event(
            "test-spec-review",
            [test_two, feature, spec_bundle_snapshot, *spec_artifacts],
            test_bundle_two,
            reviewed=test_two,
            bundle_artifacts=test_artifacts_two,
            observed="approved",
            attempt=2,
        ),
    ]
    events[3]["structural_result"] = "fail"
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
    trace = {
        "snapshots": snapshots,
        "review_bundles": {
            spec_bundle_snapshot["snapshot_id"]: spec_bundle,
            test_bundle_one["snapshot_id"]: test_bundle_one_record,
            test_bundle_two["snapshot_id"]: test_bundle_two_record,
        },
        "events": events,
        "before_inventory": list(map(dict, before_inventory)),
        "after_inventory": after_inventory,
    }
    structural = {
        f"{event['stage']}#{event['attempt']}": {
            "structural_result": (
                "fail"
                if event["stage"] == "test-spec-review"
                and event["attempt"] == 1
                else "pass"
            ),
            "diagnostic_id": (
                first_diagnostic
                if event["stage"] == "test-spec-review"
                and event["attempt"] == 1
                else "none"
            ),
        }
        for event in events
    }
    metrics = evaluate_simple_change_trace(
        trace,
        feature_models={str(feature["snapshot_id"]): parsed_feature},
        proof_maps={
            str(test_one["snapshot_id"]): initial_proof,
            str(test_two["snapshot_id"]): final_proof,
        },
        structural_evaluations=structural,
    )
    if (
        metrics.false_blocking_count != 0
        or metrics.new_universal_artifact_count != 0
        or metrics.structure_only_correction_cycles != 1
        or not metrics.applicable_only_mapping
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable", "in-turn")
    transport_attempts = payload.get("transport_attempts")
    if not isinstance(transport_attempts, list):
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    manifest = {
        "run_id": run_id,
        "publisher_instance_id": publisher_instance_id,
        "input_set": dict(input_set),
        "input_set_identity": _sha256(_canonical_json_bytes(input_set)),
        "baseline_commit": input_set["baseline_commit"],
        "before_artifact_inventory": list(map(dict, before_inventory)),
        "after_artifact_inventory": after_inventory,
        "snapshots": snapshots,
        "events": events,
        "transport_attempts": list(map(dict, transport_attempts)),
    }
    _atomic_write(temporary / "manifest.json", _canonical_json_bytes(manifest))
    return temporary, manifest


def _assemble_feature_spec_correction_run(
    repo_root: Path,
    change_id: str,
    run_id: str,
    input_set: Mapping[str, object],
    payload: Mapping[str, object],
    candidate_feature: object,
    candidate_proof: object,
    before_inventory: Sequence[Mapping[str, str]],
    repository_after_inventory: Sequence[Mapping[str, str]],
    correction: Mapping[str, object],
    publisher_instance_id: str,
    working_root: Path,
) -> tuple[Path, dict[str, object]]:
    """Assemble the closed R28y feature-spec correction branch."""

    evidence_root = _select_change_root(repo_root, change_id) / "evidence"
    simple_root = evidence_root / "simple-change"
    simple_root.mkdir(parents=True, exist_ok=True)
    temporary = working_root
    final_prefix = (
        f"docs/changes/{change_id}/evidence/simple-change/runs/{run_id}"
    )
    stage_artifacts = payload.get("stage_artifacts")
    provenance = payload.get("stage_provenance")
    final_spec_review = payload.get("spec_review")
    test_review = payload.get("test_spec_review")
    initial_spec_review = correction.get("initial_review")
    initial_feature_markdown = correction.get("initial_artifact_markdown")
    initial_resolution = correction.get("initial_resolution_markdown")
    corrected_resolution = correction.get("corrected_resolution_markdown")
    if (
        correction.get("role") != "feature-spec"
        or not isinstance(stage_artifacts, dict)
        or not isinstance(provenance, list)
        or not isinstance(final_spec_review, dict)
        or not isinstance(test_review, dict)
        or not isinstance(initial_spec_review, dict)
        or not isinstance(initial_feature_markdown, str)
        or not isinstance(initial_resolution, str)
        or not isinstance(corrected_resolution, str)
    ):
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    try:
        initial_feature_raw = initial_feature_markdown.encode("utf-8")
        final_feature_raw = str(
            stage_artifacts["feature-spec/portable-text-normalizer.md"]
        ).encode("utf-8")
        test_raw = str(
            stage_artifacts["test-spec/portable-text-normalizer.test.md"]
        ).encode("utf-8")
        initial_feature = normalize_feature_model(
            _parse_feature_markdown(initial_feature_raw.decode("utf-8"))
        )
        final_feature = normalize_feature_model(
            _parse_feature_markdown(final_feature_raw.decode("utf-8"))
        )
        final_proof = normalize_proof_map(
            _parse_test_spec_markdown(test_raw.decode("utf-8")),
            final_feature,
        )
    except (KeyError, UnicodeError, BoundaryProofError) as error:
        raise BoundaryRuntimeError("runtime-identity-unstable", "in-turn") from error
    if not boundary_invariant_projections_match(
        candidate_feature,
        final_feature,
        candidate_proof,
        final_proof,
    ):
        raise BoundaryRuntimeError("boundary-oracle-mismatch", "in-turn")

    provenance_by_occurrence = {
        (row.get("stage"), row.get("attempt")): row
        for row in provenance
        if isinstance(row, dict)
    }
    expected_occurrences = {
        ("spec", 1),
        ("spec-review", 1),
        ("spec", 2),
        ("spec-review", 2),
        ("test-spec", 1),
        ("test-spec-review", 1),
    }
    if (
        set(provenance_by_occurrence) != expected_occurrences
        or len(
            {row.get("thread_id") for row in provenance_by_occurrence.values()}
        )
        != len(expected_occurrences)
        or any(
            row.get("skill_names") != ["workflow", stage]
            for (stage, _), row in provenance_by_occurrence.items()
        )
    ):
        raise BoundaryRuntimeError("thread-metadata-mismatch", "in-turn")

    def authored_snapshot(
        snapshot_id: str,
        role: str,
        relative: str,
        raw: bytes,
    ) -> dict[str, object]:
        _write_run_artifact(temporary, relative, raw)
        return _snapshot(
            snapshot_id,
            "behavior-output",
            role,
            f"{final_prefix}/artifacts/{relative}",
            raw,
        )

    feature_one = authored_snapshot(
        "output.feature-spec.one",
        "feature-spec",
        "feature-spec/portable-text-normalizer-attempt-1.md",
        initial_feature_raw,
    )
    feature_two = authored_snapshot(
        "output.feature-spec.two",
        "feature-spec",
        "feature-spec/portable-text-normalizer-attempt-2.md",
        final_feature_raw,
    )
    test_spec = authored_snapshot(
        "output.test-spec.one",
        "test-spec",
        "test-spec/portable-text-normalizer.test.md",
        test_raw,
    )

    initial_findings = initial_spec_review.get("material_finding_ids")
    if not isinstance(initial_findings, list) or not initial_findings:
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    spec_bundle_one, spec_record_one, spec_artifacts_one = (
        _correction_review_bundle(
            authored_snapshot,
            "spec-review",
            1,
            feature_one,
            initial_spec_review,
            resolution_markdown=initial_resolution,
        )
    )
    spec_bundle_two, spec_record_two, spec_artifacts_two = (
        _correction_review_bundle(
            authored_snapshot,
            "spec-review",
            2,
            feature_two,
            final_spec_review,
            resolution_markdown=corrected_resolution,
            prior_finding_ids=initial_findings,
        )
    )
    test_bundle, test_record, test_artifacts = _correction_review_bundle(
        authored_snapshot, "test-spec-review", 1, test_spec, test_review
    )
    snapshots = [
        _snapshot(
            "oracle.feature-spec",
            "fixture-candidate",
            "feature-spec",
            "tests/fixtures/boundary-proof/simple-change/candidates/feature-spec.md",
            (
                repo_root
                / "tests/fixtures/boundary-proof/simple-change/candidates/"
                "feature-spec.md"
            ).read_bytes(),
        ),
        _snapshot(
            "oracle.test-spec",
            "fixture-candidate",
            "test-spec",
            "tests/fixtures/boundary-proof/simple-change/candidates/test-spec.md",
            (
                repo_root
                / "tests/fixtures/boundary-proof/simple-change/candidates/"
                "test-spec.md"
            ).read_bytes(),
        ),
        feature_one,
        spec_bundle_one,
        *spec_artifacts_one,
        feature_two,
        spec_bundle_two,
        *spec_artifacts_two,
        test_spec,
        test_bundle,
        *test_artifacts,
    ]
    diagnostic_id = str(initial_findings[0])
    events = [
        _event("spec", [], feature_one),
        _event(
            "spec-review",
            [feature_one],
            spec_bundle_one,
            reviewed=feature_one,
            bundle_artifacts=spec_artifacts_one,
            observed="changes-requested",
            diagnostic_id=diagnostic_id,
        ),
        _event(
            "spec",
            [feature_one, spec_bundle_one, *spec_artifacts_one],
            feature_two,
            attempt=2,
        ),
        _event(
            "spec-review",
            [feature_two],
            spec_bundle_two,
            reviewed=feature_two,
            bundle_artifacts=spec_artifacts_two,
            observed="approved",
            attempt=2,
        ),
        _event(
            "test-spec",
            [feature_two, spec_bundle_two, *spec_artifacts_two],
            test_spec,
        ),
        _event(
            "test-spec-review",
            [test_spec, feature_two, spec_bundle_two, *spec_artifacts_two],
            test_bundle,
            reviewed=test_spec,
            bundle_artifacts=test_artifacts,
            observed="approved",
        ),
    ]
    events[1]["structural_result"] = "fail"
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
    trace = {
        "snapshots": snapshots,
        "review_bundles": {
            spec_bundle_one["snapshot_id"]: spec_record_one,
            spec_bundle_two["snapshot_id"]: spec_record_two,
            test_bundle["snapshot_id"]: test_record,
        },
        "events": events,
        "before_inventory": list(map(dict, before_inventory)),
        "after_inventory": after_inventory,
    }
    structural = {
        f"{event['stage']}#{event['attempt']}": {
            "structural_result": (
                "fail"
                if event["stage"] == "spec-review" and event["attempt"] == 1
                else "pass"
            ),
            "diagnostic_id": (
                diagnostic_id
                if event["stage"] == "spec-review" and event["attempt"] == 1
                else "none"
            ),
        }
        for event in events
    }
    metrics = evaluate_simple_change_trace(
        trace,
        feature_models={
            str(feature_one["snapshot_id"]): initial_feature,
            str(feature_two["snapshot_id"]): final_feature,
        },
        proof_maps={str(test_spec["snapshot_id"]): final_proof},
        structural_evaluations=structural,
    )
    if (
        metrics.false_blocking_count != 0
        or metrics.new_universal_artifact_count != 0
        or metrics.structure_only_correction_cycles != 1
        or not metrics.applicable_only_mapping
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable", "in-turn")
    transport_attempts = payload.get("transport_attempts")
    if not isinstance(transport_attempts, list):
        raise BoundaryRuntimeError("protocol-shape-incompatible")
    manifest = {
        "run_id": run_id,
        "publisher_instance_id": publisher_instance_id,
        "input_set": dict(input_set),
        "input_set_identity": _sha256(_canonical_json_bytes(input_set)),
        "baseline_commit": input_set["baseline_commit"],
        "before_artifact_inventory": list(map(dict, before_inventory)),
        "after_artifact_inventory": after_inventory,
        "snapshots": snapshots,
        "events": events,
        "transport_attempts": list(map(dict, transport_attempts)),
    }
    _atomic_write(temporary / "manifest.json", _canonical_json_bytes(manifest))
    return temporary, manifest


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
    publisher_instance_id: str,
    working_root: Path,
) -> tuple[Path, dict[str, object]]:
    correction = payload.get("correction_history")
    if isinstance(correction, dict) and correction.get("role") == "feature-spec":
        return _assemble_feature_spec_correction_run(
            repo_root,
            change_id,
            run_id,
            input_set,
            payload,
            candidate_feature,
            candidate_proof,
            before_inventory,
            repository_after_inventory,
            correction,
            publisher_instance_id,
            working_root,
        )
    if isinstance(correction, dict) and correction.get("role") == "test-spec":
        return _assemble_test_spec_correction_run(
            repo_root,
            change_id,
            run_id,
            input_set,
            payload,
            candidate_feature,
            candidate_proof,
            before_inventory,
            repository_after_inventory,
            correction,
            publisher_instance_id,
            working_root,
        )
    evidence_root = _select_change_root(repo_root, change_id) / "evidence"
    simple_root = evidence_root / "simple-change"
    simple_root.mkdir(parents=True, exist_ok=True)
    temporary = working_root
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
        finding_projection = review_payload.get("finding_projection")
        finding_projection_identity = review_payload.get(
            "finding_projection_identity"
        )
        correction_eligibility = review_payload.get(
            "correction_eligibility"
        )
        if (
            not isinstance(record_markdown, str)
            or not isinstance(log_markdown, str)
            or not isinstance(review_id, str)
            or finding_projection != []
            or not isinstance(finding_projection_identity, str)
            or correction_eligibility != "not-applicable"
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
            "finding_projection": finding_projection,
            "finding_projection_identity": finding_projection_identity,
            "correction_eligibility": correction_eligibility,
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
        "publisher_instance_id": publisher_instance_id,
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


def _simple_root(repo_root: Path, change_id: str) -> Path:
    return (
        _select_change_root(repo_root, change_id)
        / "evidence"
        / "simple-change"
    )


@contextmanager
def _publisher_lock(repo_root: Path, change_id: str):
    """Hold the one persistent nonblocking publisher lock for an operation."""

    simple_root = _simple_root(repo_root, change_id)
    simple_root.mkdir(mode=0o700, parents=True, exist_ok=True)
    lock_path = simple_root / "publisher.lock"
    if lock_path.exists() and (
        lock_path.is_symlink() or not lock_path.is_file()
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    descriptor = os.open(lock_path, os.O_RDWR | os.O_CREAT, 0o600)
    try:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise BoundaryRuntimeError("publisher-active") from error
        yield
    finally:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)


def _publisher_paths(
    repo_root: Path, change_id: str, run_id: str
) -> tuple[str, str, str]:
    simple = (
        f"docs/changes/{change_id}/evidence/simple-change"
    )
    return (
        f"{simple}/.working-{run_id}",
        f"{simple}/.prepared-{run_id}",
        f"{simple}/runs/{run_id}",
    )


def _validate_pointer_shape(pointer: object) -> None:
    if pointer is None:
        return
    if (
        not isinstance(pointer, dict)
        or set(pointer) != {"run_id", "input_set_identity", "manifest_ref"}
        or not isinstance(pointer.get("run_id"), str)
        or RUN_ID_PATTERN.fullmatch(str(pointer["run_id"])) is None
        or not isinstance(pointer.get("input_set_identity"), str)
        or IDENTITY_PATTERN.fullmatch(str(pointer["input_set_identity"])) is None
        or not isinstance(pointer.get("manifest_ref"), dict)
        or set(pointer["manifest_ref"]) != {"path", "identity"}
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")


def _validate_publisher_lease(
    repo_root: Path,
    change_id: str,
    lease: Mapping[str, object],
) -> None:
    if (
        set(lease) != PUBLISHER_FIELDS
        or lease.get("schema_version") != "simple-change-publisher-v1"
        or not isinstance(lease.get("publisher_instance_id"), str)
        or PUBLISHER_ID_PATTERN.fullmatch(
            str(lease["publisher_instance_id"])
        )
        is None
        or not isinstance(lease.get("run_id"), str)
        or RUN_ID_PATTERN.fullmatch(str(lease["run_id"])) is None
        or not isinstance(lease.get("input_set_identity"), str)
        or IDENTITY_PATTERN.fullmatch(str(lease["input_set_identity"])) is None
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    _validate_pointer_shape(lease.get("prior_pointer"))
    expected = _publisher_paths(
        repo_root, change_id, str(lease["run_id"])
    )
    actual = tuple(
        lease[field] for field in ("working_root", "staging_root", "target_root")
    )
    if actual != expected:
        raise BoundaryRuntimeError("runtime-identity-unstable")


def _read_publisher_lease(
    repo_root: Path, change_id: str
) -> dict[str, object]:
    lease = _read_json(_simple_root(repo_root, change_id) / "publisher.json")
    _validate_publisher_lease(repo_root, change_id, lease)
    return lease


def _create_publisher_lease(
    repo_root: Path,
    change_id: str,
    run_id: str,
    publisher_instance_id: str,
    input_set_identity: str,
) -> tuple[dict[str, object], Path]:
    simple_root = _simple_root(repo_root, change_id)
    simple_root.mkdir(mode=0o700, parents=True, exist_ok=True)
    current_path = simple_root / "current.json"
    prior = _read_json(current_path) if current_path.exists() else None
    _validate_pointer_shape(prior)
    working, staging, target = _publisher_paths(repo_root, change_id, run_id)
    lease = {
        "schema_version": "simple-change-publisher-v1",
        "publisher_instance_id": publisher_instance_id,
        "run_id": run_id,
        "input_set_identity": input_set_identity,
        "prior_pointer": prior,
        "working_root": working,
        "staging_root": staging,
        "target_root": target,
    }
    _validate_publisher_lease(repo_root, change_id, lease)
    lease_path = simple_root / "publisher.json"
    _exclusive_write(lease_path, _canonical_json_bytes(lease))
    working_path = repo_root / working
    working_path.mkdir(mode=0o700, parents=False, exist_ok=False)
    _fsync_directory(simple_root)
    return lease, working_path


def _validate_prepared_receipt(
    repo_root: Path,
    change_id: str,
    prepared: Mapping[str, object],
    lease: Mapping[str, object],
) -> None:
    if set(prepared) != PREPARED_FIELDS:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    for field in ("publisher_instance_id", "run_id", "input_set_identity"):
        if prepared.get(field) != lease.get(field):
            raise BoundaryRuntimeError("runtime-identity-unstable")
    if prepared.get("prior_pointer") != lease.get("prior_pointer"):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    staged_ref = prepared.get("staged_manifest_snapshot")
    target_ref = prepared.get("target_manifest")
    if (
        not isinstance(staged_ref, dict)
        or set(staged_ref) != {"path", "identity"}
        or not isinstance(target_ref, dict)
        or set(target_ref) != {"path", "identity"}
        or staged_ref.get("identity") != target_ref.get("identity")
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    run_id = str(lease["run_id"])
    expected_staged = (
        f"docs/changes/{change_id}/evidence/simple-change/"
        f".prepared-{run_id}/manifest.json"
    )
    expected_target = (
        f"docs/changes/{change_id}/evidence/simple-change/"
        f"runs/{run_id}/manifest.json"
    )
    if (
        staged_ref.get("path") != expected_staged
        or target_ref.get("path") != expected_target
        or not isinstance(target_ref.get("identity"), str)
        or IDENTITY_PATTERN.fullmatch(str(target_ref["identity"])) is None
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")


def _validate_recovery_state(
    state: Mapping[str, object],
    *,
    basis_identity: str | None = None,
    recovery_id: str | None = None,
) -> None:
    if (
        set(state) != RECOVERY_STATE_FIELDS
        or state.get("schema_version")
        != "simple-change-manual-recovery-state-v1"
        or not isinstance(state.get("recovery_id"), str)
        or RECOVERY_ID_PATTERN.fullmatch(str(state["recovery_id"])) is None
        or not isinstance(state.get("basis_identity"), str)
        or IDENTITY_PATTERN.fullmatch(str(state["basis_identity"])) is None
        or state.get("state")
        not in {"authorized", "orphan-detached", "completed"}
        or (
            basis_identity is not None
            and state.get("basis_identity") != basis_identity
        )
        or (
            recovery_id is not None
            and state.get("recovery_id") != recovery_id
        )
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")


def _validate_recovery_decision_ref(
    repo_root: Path,
    change_id: str,
    authority_ref: object,
    *,
    run_id: object,
    publisher_instance_id: object,
    input_set_identity: object,
    action: object,
    authorized_by: object,
) -> None:
    expected_path = (
        f"docs/changes/{change_id}/recovery-decisions/{run_id}.json"
    )
    if (
        not isinstance(authority_ref, dict)
        or set(authority_ref) != {"path", "identity"}
        or authority_ref.get("path") != expected_path
        or not isinstance(authority_ref.get("identity"), str)
        or IDENTITY_PATTERN.fullmatch(str(authority_ref["identity"])) is None
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    _validate_reference(repo_root, authority_ref)
    decision = _read_json(repo_root / expected_path)
    if (
        set(decision) != RECOVERY_DECISION_FIELDS
        or decision.get("schema_version")
        != "simple-change-recovery-decision-v1"
        or decision.get("change_id") != change_id
        or decision.get("run_id") != run_id
        or decision.get("publisher_instance_id") != publisher_instance_id
        or decision.get("input_set_identity") != input_set_identity
        or decision.get("action") != action
        or decision.get("authorized_by") != authorized_by
        or decision.get("outcome") != "authorized"
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")


def _validate_recovery_basis(
    repo_root: Path,
    change_id: str,
    basis: Mapping[str, object],
    *,
    expected_run_id: str | None = None,
    require_current_authority: bool = True,
) -> None:
    if (
        set(basis) != RECOVERY_BASIS_FIELDS
        or basis.get("schema_version")
        != "simple-change-manual-recovery-v1"
        or not isinstance(basis.get("recovery_id"), str)
        or RECOVERY_ID_PATTERN.fullmatch(str(basis["recovery_id"])) is None
        or not isinstance(basis.get("run_id"), str)
        or RUN_ID_PATTERN.fullmatch(str(basis["run_id"])) is None
        or not isinstance(basis.get("publisher_instance_id"), str)
        or PUBLISHER_ID_PATTERN.fullmatch(
            str(basis["publisher_instance_id"])
        )
        is None
        or not isinstance(basis.get("authorized_by"), str)
        or not str(basis["authorized_by"]).strip()
        or not isinstance(basis.get("input_set_identity"), str)
        or IDENTITY_PATTERN.fullmatch(str(basis["input_set_identity"])) is None
        or basis.get("action") != "discard-and-regenerate"
        or (
            expected_run_id is not None
            and basis.get("run_id") != expected_run_id
        )
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    authority_ref = basis.get("authorization_evidence_ref")
    if (
        not isinstance(authority_ref, dict)
        or set(authority_ref) != {"path", "identity"}
        or not isinstance(authority_ref.get("path"), str)
        or PurePosixPath(str(authority_ref["path"])).is_absolute()
        or ".." in PurePosixPath(str(authority_ref["path"])).parts
        or not isinstance(authority_ref.get("identity"), str)
        or IDENTITY_PATTERN.fullmatch(str(authority_ref["identity"])) is None
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    if require_current_authority:
        _validate_recovery_decision_ref(
            repo_root,
            change_id,
            authority_ref,
            run_id=basis["run_id"],
            publisher_instance_id=basis["publisher_instance_id"],
            input_set_identity=basis["input_set_identity"],
            action=basis["action"],
            authorized_by=basis["authorized_by"],
        )
    lease_snapshot = basis.get("publisher_lease_snapshot")
    if (
        not isinstance(lease_snapshot, dict)
        or set(lease_snapshot) != {"path", "identity", "values"}
        or lease_snapshot.get("path")
        != (
            f"docs/changes/{change_id}/evidence/simple-change/"
            "publisher.json"
        )
        or not isinstance(lease_snapshot.get("identity"), str)
        or IDENTITY_PATTERN.fullmatch(str(lease_snapshot["identity"])) is None
        or not isinstance(lease_snapshot.get("values"), dict)
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    lease = lease_snapshot["values"]
    _validate_publisher_lease(repo_root, change_id, lease)
    if (
        lease_snapshot["identity"] != _sha256(_canonical_json_bytes(lease))
        or basis["run_id"] != lease["run_id"]
        or basis["publisher_instance_id"] != lease["publisher_instance_id"]
        or basis["input_set_identity"] != lease["input_set_identity"]
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    lock_proof = basis.get("publisher_lock_proof")
    if (
        not isinstance(lock_proof, dict)
        or set(lock_proof)
        != {"method", "lock_path", "acquired", "prior_lease_identity"}
        or lock_proof.get("method") != "exclusive-nonblocking-file-lock-v1"
        or lock_proof.get("lock_path") != "publisher.lock"
        or lock_proof.get("acquired") is not True
        or lock_proof.get("prior_lease_identity")
        != lease_snapshot["identity"]
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    orphan = basis.get("orphan_snapshot")
    if (
        not isinstance(orphan, dict)
        or set(orphan)
        != {"kind", "path", "identity", "quarantine_path", "durability_parent"}
        or orphan.get("kind") not in {"working", "staging", "lease-only"}
        or orphan.get("durability_parent")
        != f"docs/changes/{change_id}/evidence/simple-change"
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    kind = str(orphan["kind"])
    if kind == "lease-only":
        if any(
            orphan.get(field) is not None
            for field in ("path", "identity", "quarantine_path")
        ):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        return
    root_field = "working_root" if kind == "working" else "staging_root"
    expected_path = lease[root_field]
    expected_quarantine = (
        f"docs/changes/{change_id}/evidence/simple-change/"
        f".recovery-quarantine-{basis['run_id']}-"
        f"{basis['recovery_id']}-{kind}"
    )
    if (
        orphan.get("path") != expected_path
        or not isinstance(orphan.get("identity"), str)
        or IDENTITY_PATTERN.fullmatch(str(orphan["identity"])) is None
        or orphan.get("quarantine_path") != expected_quarantine
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")


def _completed_recovery_is_valid(
    repo_root: Path,
    change_id: str,
    basis_path: Path,
    state_path: Path,
) -> bool:
    run_id = basis_path.name.removeprefix("manual-recovery-").removesuffix(
        ".json"
    )
    basis = _read_json(basis_path)
    _validate_recovery_basis(
        repo_root,
        change_id,
        basis,
        expected_run_id=run_id,
        require_current_authority=False,
    )
    basis_identity = _read_file_identity(basis_path).digest
    state = _read_json(state_path)
    _validate_recovery_state(
        state,
        basis_identity=basis_identity,
        recovery_id=str(basis["recovery_id"]),
    )
    if state["state"] != "completed":
        return False
    simple_root = _simple_root(repo_root, change_id)
    lease_path = simple_root / "publisher.json"
    if lease_path.exists():
        lease = _read_publisher_lease(repo_root, change_id)
        if lease["run_id"] == run_id:
            raise BoundaryRuntimeError("runtime-identity-unstable")
    orphan = basis["orphan_snapshot"]
    assert isinstance(orphan, dict)
    orphan_path = orphan.get("path")
    if orphan_path is not None and (repo_root / str(orphan_path)).exists():
        raise BoundaryRuntimeError("runtime-identity-unstable")
    unexpected_paths = (
        simple_root / f".working-{run_id}",
        simple_root / f".prepared-{run_id}",
        simple_root / f".current-{run_id}.json",
        simple_root / "runs" / run_id,
    )
    if any(path.exists() for path in unexpected_paths):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    if list(
        simple_root.glob(f".manual-recovery-{run_id}-recovery-*.tmp")
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    quarantine_path = orphan.get("quarantine_path")
    if orphan["kind"] == "lease-only":
        if quarantine_path is not None:
            raise BoundaryRuntimeError("runtime-identity-unstable")
    else:
        if quarantine_path is None:
            raise BoundaryRuntimeError("runtime-identity-unstable")
        quarantine = repo_root / str(quarantine_path)
        lease_snapshot = basis["publisher_lease_snapshot"]
        assert isinstance(lease_snapshot, dict)
        lease_values = lease_snapshot["values"]
        assert isinstance(lease_values, dict)
        observed_identity = (
            _working_tree_identity(quarantine, lease_values)
            if orphan["kind"] == "working"
            else _tree_identity(quarantine)
        )
        if (
            not quarantine.is_dir()
            or quarantine.is_symlink()
            or observed_identity != orphan["identity"]
        ):
            raise BoundaryRuntimeError("runtime-identity-unstable")
    allowed_quarantine = (
        None if quarantine_path is None else Path(str(quarantine_path)).name
    )
    for candidate in simple_root.glob(
        f".recovery-quarantine-{run_id}-recovery-*-*"
    ):
        if candidate.name != allowed_quarantine:
            raise BoundaryRuntimeError("runtime-identity-unstable")
    return True


def _discover_global_candidate(
    repo_root: Path, change_id: str
) -> str | None:
    """Validate the transient namespace and select at most one active run."""

    simple_root = _simple_root(repo_root, change_id)
    if not simple_root.exists():
        return None
    recovery_temps = list(simple_root.glob(".manual-recovery-*.tmp"))
    if len(recovery_temps) > 1:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    run_ids: set[str] = set()
    known_fixed = {
        "current.json",
        "publisher.lock",
        "publisher.json",
        "prepared.json",
        "runs",
    }
    transient_patterns = (
        re.compile(r"^\.working-(run-[0-9a-f]{32})$"),
        re.compile(r"^\.prepared-(run-[0-9a-f]{32})$"),
        re.compile(r"^\.current-(run-[0-9a-f]{32})\.json$"),
        re.compile(r"^manual-recovery-(run-[0-9a-f]{32})\.json$"),
        re.compile(r"^manual-recovery-state-(run-[0-9a-f]{32})\.json$"),
        re.compile(
            r"^\.manual-recovery-(run-[0-9a-f]{32})-"
            r"recovery-[0-9a-f]{32}\.tmp$"
        ),
        re.compile(
            r"^\.recovery-quarantine-(run-[0-9a-f]{32})-"
            r"recovery-[0-9a-f]{32}-(?:working|staging)$"
        ),
    )
    for path in simple_root.iterdir():
        name = path.name
        if name in known_fixed:
            expected_directory = name == "runs"
            if (
                path.is_symlink()
                or (expected_directory and not path.is_dir())
                or (not expected_directory and not path.is_file())
            ):
                raise BoundaryRuntimeError("runtime-identity-unstable")
            continue
        match = next(
            (pattern.fullmatch(name) for pattern in transient_patterns
             if pattern.fullmatch(name) is not None),
            None,
        )
        if match is not None:
            if path.is_symlink():
                raise BoundaryRuntimeError("runtime-identity-unstable")
            run_ids.add(match.group(1))
            continue
        if (
            name.startswith(".working-")
            or name.startswith(".prepared-")
            or name.startswith(".current-")
            or name.startswith("manual-recovery-")
            or name.startswith("manual-recovery-state-")
            or name.startswith(".manual-recovery-")
            or name.startswith(".recovery-quarantine-")
        ):
            raise BoundaryRuntimeError("runtime-identity-unstable")
    lease_path = simple_root / "publisher.json"
    if lease_path.exists():
        lease = _read_publisher_lease(repo_root, change_id)
        run_ids.add(str(lease["run_id"]))
    prepared_path = simple_root / "prepared.json"
    if prepared_path.exists():
        if not lease_path.exists():
            raise BoundaryRuntimeError("runtime-identity-unstable")
        prepared = _read_json(prepared_path)
        lease = _read_publisher_lease(repo_root, change_id)
        _validate_prepared_receipt(repo_root, change_id, prepared, lease)
        run_ids.add(str(prepared["run_id"]))
    completed_ids: set[str] = set()
    state_paths = {
        path.name.removeprefix("manual-recovery-state-").removesuffix(".json"):
        path
        for path in simple_root.glob("manual-recovery-state-run-*.json")
    }
    basis_paths = {
        path.name.removeprefix("manual-recovery-").removesuffix(".json"):
        path
        for path in simple_root.glob("manual-recovery-run-*.json")
    }
    if set(state_paths) - set(basis_paths):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    for history_run_id, basis_path in basis_paths.items():
        if basis_path.is_symlink() or not basis_path.is_file():
            raise BoundaryRuntimeError("runtime-identity-unstable")
        basis = _read_json(basis_path)
        _validate_recovery_basis(
            repo_root,
            change_id,
            basis,
            expected_run_id=history_run_id,
            require_current_authority=False,
        )
        state_path = state_paths.get(history_run_id)
        if state_path is None:
            continue
        match = re.fullmatch(
            r"manual-recovery-state-(run-[0-9a-f]{32})\.json",
            state_path.name,
        )
        if match is None or state_path.is_symlink():
            raise BoundaryRuntimeError("runtime-identity-unstable")
        history_run_id = match.group(1)
        state = _read_json(state_path)
        _validate_recovery_state(
            state,
            basis_identity=_read_file_identity(basis_path).digest,
            recovery_id=str(basis["recovery_id"]),
        )
        if state["state"] == "completed":
            if not _completed_recovery_is_valid(
                repo_root, change_id, basis_path, state_path
            ):
                raise BoundaryRuntimeError("runtime-identity-unstable")
            completed_ids.add(history_run_id)
        else:
            _validate_recovery_basis(
                repo_root,
                change_id,
                basis,
                expected_run_id=history_run_id,
                require_current_authority=True,
            )
    if lease_path.exists() and str(
        _read_publisher_lease(repo_root, change_id)["run_id"]
    ) in completed_ids:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    run_ids.difference_update(completed_ids)
    if len(run_ids) > 1:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    return next(iter(run_ids), None)


def _completed_correction_stop_input_identities(
    repo_root: Path, change_id: str
) -> frozenset[str]:
    """Return preserved stopped-input identities from valid completed recovery."""

    simple_root = _simple_root(repo_root, change_id)
    identities: set[str] = set()
    for basis_path in simple_root.glob("manual-recovery-run-*.json"):
        run_id = basis_path.name.removeprefix(
            "manual-recovery-"
        ).removesuffix(".json")
        state_path = simple_root / f"manual-recovery-state-{run_id}.json"
        if not state_path.exists():
            continue
        basis = _read_json(basis_path)
        _validate_recovery_basis(
            repo_root,
            change_id,
            basis,
            expected_run_id=run_id,
            require_current_authority=False,
        )
        state = _read_json(state_path)
        _validate_recovery_state(
            state,
            basis_identity=_read_file_identity(basis_path).digest,
            recovery_id=str(basis["recovery_id"]),
        )
        if state["state"] != "completed":
            continue
        if not _completed_recovery_is_valid(
            repo_root, change_id, basis_path, state_path
        ):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        orphan = basis.get("orphan_snapshot")
        lease_snapshot = basis.get("publisher_lease_snapshot")
        if not isinstance(orphan, dict) or not isinstance(
            lease_snapshot, dict
        ):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        quarantine_value = orphan.get("quarantine_path")
        if quarantine_value is None:
            continue
        quarantine = repo_root / str(quarantine_value)
        stop_path = quarantine / "correction-stop.json"
        if not stop_path.exists():
            continue
        if stop_path.is_symlink() or not stop_path.is_file():
            raise BoundaryRuntimeError("runtime-identity-unstable")
        lease_values = lease_snapshot.get("values")
        if not isinstance(lease_values, dict):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        receipt = _read_json(stop_path)
        _validate_correction_stop_receipt(receipt, lease=lease_values)
        identities.add(str(receipt["input_set_identity"]))
    return frozenset(identities)


def _assert_correction_input_is_fresh(
    repo_root: Path,
    change_id: str,
    input_set_identity: str,
) -> None:
    if input_set_identity in _completed_correction_stop_input_identities(
        repo_root, change_id
    ):
        raise BoundaryRuntimeError(
            "correction-authorization-required", "in-turn"
        )


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


def _parse_output_models(
    output_snapshots: Mapping[str, Mapping[str, object]],
    path_for: Callable[[Mapping[str, object]], Path],
) -> tuple[dict[str, object], dict[str, object]]:
    feature_models: dict[str, object] = {}
    feature_order: list[str] = []
    for snapshot_id, snapshot in output_snapshots.items():
        if snapshot.get("artifact_role") != "feature-spec":
            continue
        feature_models[snapshot_id] = normalize_feature_model(
            _parse_feature_markdown(
                path_for(snapshot).read_text(encoding="utf-8")
            )
        )
        feature_order.append(snapshot_id)
    if not feature_order:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    final_feature = feature_models[feature_order[-1]]
    proof_maps: dict[str, object] = {}
    for snapshot_id, snapshot in output_snapshots.items():
        if snapshot.get("artifact_role") != "test-spec":
            continue
        proof_maps[snapshot_id] = normalize_proof_map(
            _parse_test_spec_markdown(
                path_for(snapshot).read_text(encoding="utf-8")
            ),
            final_feature,
        )
    if not proof_maps:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    return feature_models, proof_maps


def _validate_staged_run(
    repo_root: Path,
    staged: Path,
    manifest: Mapping[str, object],
    pointer: Mapping[str, object],
    lease: Mapping[str, object],
    *,
    require_current_inputs: bool = True,
) -> None:
    manifest_path = staged / "manifest.json"
    manifest_ref = pointer.get("manifest_ref")
    if (
        not manifest_path.is_file()
        or manifest_path.is_symlink()
        or _read_json(manifest_path) != dict(manifest)
        or set(manifest) != RUN_MANIFEST_FIELDS
        or not isinstance(manifest_ref, dict)
        or manifest_ref.get("identity") != _read_file_identity(manifest_path).digest
        or manifest.get("publisher_instance_id")
        != lease.get("publisher_instance_id")
        or manifest.get("run_id") != lease.get("run_id")
        or manifest.get("input_set_identity") != lease.get("input_set_identity")
        or not isinstance(manifest.get("input_set"), dict)
        or manifest.get("input_set_identity")
        != _sha256(_canonical_json_bytes(manifest["input_set"]))
        or manifest.get("baseline_commit")
        != manifest["input_set"].get("baseline_commit")
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    input_set = manifest["input_set"]
    expected_input_fields = {
        "schema_version",
        "scenario_ref",
        "baseline_commit",
        "skill_resource_refs",
        "oracle_refs",
        "implementation_manifest_ref",
    }
    if (
        set(input_set) != expected_input_fields
        or input_set.get("schema_version") != "simple-change-input-v1"
        or not isinstance(input_set.get("baseline_commit"), str)
        or re.fullmatch(
            r"git:[0-9a-f]{40}", str(input_set["baseline_commit"])
        )
        is None
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    references_to_check = [
        input_set.get("scenario_ref"),
        input_set.get("implementation_manifest_ref"),
    ]
    for field in ("skill_resource_refs", "oracle_refs"):
        references = input_set.get(field)
        if not isinstance(references, list):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        references_to_check.extend(references)
    for reference in references_to_check:
        if (
            not isinstance(reference, dict)
            or set(reference) != {"path", "identity"}
            or not isinstance(reference.get("path"), str)
            or not isinstance(reference.get("identity"), str)
            or IDENTITY_PATTERN.fullmatch(str(reference["identity"])) is None
        ):
            raise BoundaryRuntimeError("runtime-identity-unstable")
    snapshots = manifest.get("snapshots")
    events = manifest.get("events")
    before = manifest.get("before_artifact_inventory")
    after = manifest.get("after_artifact_inventory")
    transport = manifest.get("transport_attempts")
    if not all(
        isinstance(value, list)
        for value in (snapshots, events, before, after, transport)
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    if require_current_inputs:
        implementation_path = _validate_reference(
            repo_root, manifest["input_set"]["implementation_manifest_ref"]
        )
        implementation_manifest = _read_json(implementation_path)
        _validate_behavior_manifest(repo_root, implementation_manifest)
        _validate_transport_rows(
            transport,
            _sha256(
                _canonical_json_bytes(
                    implementation_manifest["transport_policy"]
                )
            ),
        )
        _validate_input_set(
            repo_root, implementation_manifest, manifest["input_set"]
        )
    output_files: set[Path] = set()
    output_snapshots: dict[str, Mapping[str, object]] = {}
    snapshot_ids: set[str] = set()
    target_artifact_prefix = str(lease["target_root"]) + "/artifacts/"
    for snapshot in snapshots:
        if (
            not isinstance(snapshot, dict)
            or set(snapshot)
            != {"snapshot_id", "source", "artifact_role", "path", "identity"}
            or not isinstance(snapshot.get("snapshot_id"), str)
            or not str(snapshot["snapshot_id"])
            or snapshot["snapshot_id"] in snapshot_ids
            or snapshot.get("source")
            not in {"behavior-output", "fixture-candidate"}
            or not isinstance(snapshot.get("artifact_role"), str)
            or not isinstance(snapshot.get("path"), str)
            or not isinstance(snapshot.get("identity"), str)
            or IDENTITY_PATTERN.fullmatch(str(snapshot["identity"])) is None
        ):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        snapshot_ids.add(str(snapshot["snapshot_id"]))
        if snapshot.get("source") != "behavior-output":
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
        if not path.startswith(target_artifact_prefix):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        relative = path.removeprefix(target_artifact_prefix)
        candidate = staged / "artifacts" / relative
        if (
            not candidate.is_file()
            or candidate.is_symlink()
            or _read_file_identity(candidate).digest != identity
        ):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        output_files.add(candidate)
        output_snapshots[str(snapshot["snapshot_id"])] = snapshot
    actual_files = {
        path
        for path in (staged / "artifacts").rglob("*")
        if path.is_file()
    }
    if actual_files != output_files:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    if not transport:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    first_transport = transport[0]
    if (
        not isinstance(first_transport, dict)
        or not isinstance(
            first_transport.get("transport_policy_identity"), str
        )
        or IDENTITY_PATTERN.fullmatch(
            str(first_transport["transport_policy_identity"])
        )
        is None
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    _validate_transport_rows(
        transport, str(first_transport["transport_policy_identity"])
    )
    for inventory in (before, after):
        seen_paths: set[str] = set()
        for row in inventory:
            if (
                not isinstance(row, dict)
                or set(row) != {"path", "artifact_kind", "identity"}
                or not isinstance(row.get("path"), str)
                or not isinstance(row.get("artifact_kind"), str)
                or not isinstance(row.get("identity"), str)
                or IDENTITY_PATTERN.fullmatch(str(row["identity"])) is None
                or row["path"] in seen_paths
            ):
                raise BoundaryRuntimeError("runtime-identity-unstable")
            seen_paths.add(str(row["path"]))
    event_fields = {
        "stage",
        "attempt",
        "input_snapshot_ids",
        "reviewed_snapshot_id",
        "output_snapshot_ids",
        "structural_result",
        "observed_result",
        "diagnostic_id",
        "evidence_refs",
    }
    for event in events:
        if (
            not isinstance(event, dict)
            or set(event) != event_fields
            or event.get("stage")
            not in {"spec", "spec-review", "test-spec", "test-spec-review"}
            or not isinstance(event.get("attempt"), int)
            or event["attempt"] not in {1, 2}
            or event.get("structural_result") not in {"pass", "fail"}
            or not isinstance(event.get("input_snapshot_ids"), list)
            or not isinstance(event.get("output_snapshot_ids"), list)
            or not isinstance(event.get("evidence_refs"), list)
        ):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        referenced_ids = (
            list(event["input_snapshot_ids"])
            + list(event["output_snapshot_ids"])
            + (
                []
                if event.get("reviewed_snapshot_id") is None
                else [event["reviewed_snapshot_id"]]
            )
        )
        if any(value not in snapshot_ids for value in referenced_ids):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        for reference in event["evidence_refs"]:
            if (
                not isinstance(reference, dict)
                or set(reference) != {"path", "identity"}
                or not isinstance(reference.get("path"), str)
                or not isinstance(reference.get("identity"), str)
                or IDENTITY_PATTERN.fullmatch(str(reference["identity"]))
                is None
            ):
                raise BoundaryRuntimeError("runtime-identity-unstable")
    def staged_output(snapshot: Mapping[str, object]) -> Path:
        return staged / "artifacts" / str(snapshot["path"]).removeprefix(
            target_artifact_prefix
        )

    bundles: dict[str, object] = {}
    for snapshot_id, snapshot in output_snapshots.items():
        if str(snapshot["path"]).endswith("-bundle.json"):
            bundles[snapshot_id] = _read_json(staged_output(snapshot))
    _validate_review_bundle_payloads(
        bundles, output_snapshots, staged_output
    )
    try:
        feature_models, proof_maps = _parse_output_models(
            output_snapshots, staged_output
        )
        structural = {
            f"{event['stage']}#{event['attempt']}": {
                "structural_result": event["structural_result"],
                "diagnostic_id": (
                    "none"
                    if event["structural_result"] == "pass"
                    else event["diagnostic_id"]
                ),
            }
            for event in events
        }
        evaluate_simple_change_trace(
            {
                "snapshots": snapshots,
                "review_bundles": bundles,
                "events": events,
                "before_inventory": before,
                "after_inventory": after,
            },
            feature_models=feature_models,
            proof_maps=proof_maps,
            structural_evaluations=structural,
        )
    except (OSError, UnicodeError, KeyError, BoundaryProofError) as error:
        if isinstance(error, BoundaryRuntimeError):
            raise
        raise BoundaryRuntimeError("runtime-identity-unstable") from error


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
    simple_root = _simple_root(repo_root, change_id)
    runs_root = simple_root / "runs"
    runs_root.mkdir(mode=0o700, parents=True, exist_ok=True)
    run_id = manifest["run_id"]
    if not isinstance(run_id, str) or RUN_ID_PATTERN.fullmatch(run_id) is None:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    lease = _read_publisher_lease(repo_root, change_id)
    publisher_instance_id = manifest.get("publisher_instance_id")
    if (
        manifest.get("run_id") != lease.get("run_id")
        or publisher_instance_id != lease.get("publisher_instance_id")
        or manifest.get("input_set_identity") != lease.get("input_set_identity")
        or temporary != repo_root / str(lease["working_root"])
    ):
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
    if prior != lease["prior_pointer"]:
        raise BoundaryRuntimeError("runtime-identity-unstable")
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
        target_manifest = {
            "path": manifest_path.relative_to(repo_root).as_posix(),
            "identity": _sha256(_canonical_json_bytes(manifest)),
        }
        pointer = {
            "run_id": run_id,
            "input_set_identity": str(manifest["input_set_identity"]),
            "manifest_ref": target_manifest,
        }
        os.replace(temporary, staged)
        _fsync_directory(simple_root)
        staged_manifest = staged / "manifest.json"
        staged_snapshot = {
            "path": staged_manifest.relative_to(repo_root).as_posix(),
            "identity": _read_file_identity(staged_manifest).digest,
        }
        prepared = {
            "publisher_instance_id": publisher_instance_id,
            "run_id": run_id,
            "input_set_identity": str(manifest["input_set_identity"]),
            "staged_manifest_snapshot": staged_snapshot,
            "target_manifest": target_manifest,
            "prior_pointer": prior,
        }
        _validate_staged_run(repo_root, staged, manifest, pointer, lease)
        _validate_prepared_receipt(repo_root, change_id, prepared, lease)
        _crash_if(crash_at, "before-receipt")
        _exclusive_write(prepared_path, _canonical_json_bytes(prepared))
        _crash_if(crash_at, "after-receipt-fsync")
        os.replace(staged, target)
        _fsync_directory(runs_root)
        _crash_if(crash_at, "after-run-install")
        _validate_run(repo_root, change_id, pointer)
        _crash_if(crash_at, "after-run-validation")
        temporary_pointer = simple_root / f".current-{run_id}.json"
        _exclusive_write(temporary_pointer, _canonical_json_bytes(pointer))
        os.replace(temporary_pointer, current_path)
        _crash_if(crash_at, "after-pointer-replace")
        _fsync_directory(simple_root)
        _crash_if(crash_at, "after-parent-fsync")
        prepared_path.unlink()
        _fsync_directory(simple_root)
        _crash_if(crash_at, "after-receipt-cleanup")
        (simple_root / "publisher.json").unlink()
        _fsync_directory(simple_root)
        _crash_if(crash_at, "after-lease-cleanup")
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
    if set(run) != RUN_MANIFEST_FIELDS:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    input_set = run.get("input_set")
    if not isinstance(input_set, dict):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    input_identity = _sha256(_canonical_json_bytes(input_set))
    if (
        run.get("run_id") != run_id
        or not isinstance(run.get("publisher_instance_id"), str)
        or PUBLISHER_ID_PATTERN.fullmatch(
            str(run["publisher_instance_id"])
        )
        is None
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
    _validate_review_bundle_payloads(
        bundles,
        output_snapshots,
        lambda snapshot: repo_root / str(snapshot["path"]),
    )
    trace = {
        "snapshots": snapshots,
        "review_bundles": bundles,
        "events": events,
        "before_inventory": before,
        "after_inventory": after,
    }
    try:
        feature_models, proof_maps = _parse_output_models(
            output_snapshots,
            lambda snapshot: repo_root / str(snapshot["path"]),
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
        for feature in feature_models.values():
            for proof in proof_maps.values():
                if not boundary_invariant_projections_match(
                    oracle_feature,
                    feature,
                    oracle_proof,
                    proof,
                ):
                    raise BoundaryRuntimeError("runtime-identity-unstable")
        scenario_path = _validate_reference(
            repo_root, input_set["scenario_ref"]
        )
        _validate_scenario_expectations(
            _scenario(repo_root, scenario_path), events
        )
        structural = {
            f"{event['stage']}#{event['attempt']}": {
                "structural_result": event["structural_result"],
                "diagnostic_id": (
                    "none"
                    if event["structural_result"] == "pass"
                    else event["diagnostic_id"]
                ),
            }
            for event in events
        }
        return evaluate_simple_change_trace(
            trace,
            feature_models=feature_models,
            proof_maps=proof_maps,
            structural_evaluations=structural,
        )
    except (OSError, UnicodeError, KeyError, BoundaryProofError) as error:
        if isinstance(error, BoundaryRuntimeError):
            raise
        raise BoundaryRuntimeError("runtime-identity-unstable") from error


def _reconcile_prepared(repo_root: Path, change_id: str) -> None:
    simple_root = _simple_root(repo_root, change_id)
    candidate = _discover_global_candidate(repo_root, change_id)
    prepared_path = simple_root / "prepared.json"
    lease_path = simple_root / "publisher.json"
    if not prepared_path.exists():
        if not lease_path.exists():
            if candidate is not None:
                raise BoundaryRuntimeError("runtime-identity-unstable")
            return
        lease = _read_publisher_lease(repo_root, change_id)
        run_id = str(lease["run_id"])
        target_pointer = {
            "run_id": run_id,
            "input_set_identity": lease["input_set_identity"],
            "manifest_ref": {
                "path": (
                    f"docs/changes/{change_id}/evidence/simple-change/"
                    f"runs/{run_id}/manifest.json"
                ),
                "identity": (
                    _read_file_identity(
                        simple_root / "runs" / run_id / "manifest.json"
                    ).digest
                    if (simple_root / "runs" / run_id / "manifest.json").is_file()
                    else ""
                ),
            },
        }
        current_path = simple_root / "current.json"
        current = _read_json(current_path) if current_path.exists() else None
        if (
            (simple_root / "runs" / run_id).is_dir()
            and current == target_pointer
            and not (simple_root / f".working-{run_id}").exists()
            and not (simple_root / f".prepared-{run_id}").exists()
        ):
            _validate_run(repo_root, change_id, target_pointer)
            lease_path.unlink()
            _fsync_directory(simple_root)
            return
        # A later lock holder cannot reconstruct same-live-publisher authority.
        # Lease-only, working, and unreceipted staging require explicit bounded
        # discard-and-regenerate recovery.
        raise BoundaryRuntimeError("runtime-identity-unstable")
    if not lease_path.exists():
        raise BoundaryRuntimeError("runtime-identity-unstable")
    lease = _read_publisher_lease(repo_root, change_id)
    prepared = _read_json(prepared_path)
    _validate_prepared_receipt(repo_root, change_id, prepared, lease)
    run_id = prepared["run_id"]
    if not isinstance(run_id, str) or RUN_ID_PATTERN.fullmatch(run_id) is None:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    target_pointer = {
        "run_id": run_id,
        "input_set_identity": prepared["input_set_identity"],
        "manifest_ref": prepared["target_manifest"],
    }
    staged = simple_root / f".prepared-{run_id}"
    target = simple_root / "runs" / run_id
    temporary_pointer = simple_root / f".current-{run_id}.json"
    if staged.exists() and target.exists():
        raise BoundaryRuntimeError("runtime-identity-unstable")
    if not target.exists():
        if not staged.is_dir() or staged.is_symlink():
            raise BoundaryRuntimeError("runtime-identity-unstable")
        staged_manifest = staged / "manifest.json"
        if (
            _read_file_identity(staged_manifest).digest
            != prepared["staged_manifest_snapshot"]["identity"]
        ):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        os.replace(staged, target)
        _fsync_directory(target.parent)
    current_path = simple_root / "current.json"
    current = _read_json(current_path) if current_path.exists() else None
    if current == target_pointer:
        if temporary_pointer.exists():
            raise BoundaryRuntimeError("runtime-identity-unstable")
        _validate_run(repo_root, change_id, target_pointer)
    elif current == prepared["prior_pointer"]:
        _validate_run(repo_root, change_id, target_pointer)
        if temporary_pointer.exists():
            if (
                temporary_pointer.is_symlink()
                or _read_json(temporary_pointer) != target_pointer
            ):
                raise BoundaryRuntimeError("runtime-identity-unstable")
        else:
            _exclusive_write(
                temporary_pointer, _canonical_json_bytes(target_pointer)
            )
        os.replace(temporary_pointer, current_path)
        _fsync_directory(simple_root)
    else:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    prepared_path.unlink()
    _fsync_directory(simple_root)
    lease_path.unlink()
    _fsync_directory(simple_root)


def _working_output_paths() -> tuple[set[str], set[str]]:
    files: set[str] = set()
    directories = {"output"}
    occurrences = ARTIFACT_POLICY.get("stage_occurrences")
    if not isinstance(occurrences, list):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    for occurrence in occurrences:
        if not isinstance(occurrence, dict):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        variants = occurrence.get("variants")
        if not isinstance(variants, list):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        for variant in variants:
            if not isinstance(variant, dict):
                raise BoundaryRuntimeError("runtime-identity-unstable")
            artifacts = variant.get("artifacts")
            if not isinstance(artifacts, list):
                raise BoundaryRuntimeError("runtime-identity-unstable")
            for artifact in artifacts:
                if (
                    not isinstance(artifact, dict)
                    or not isinstance(artifact.get("path"), str)
                ):
                    raise BoundaryRuntimeError("runtime-identity-unstable")
                relative = PurePosixPath(str(artifact["path"]))
                if relative.is_absolute() or ".." in relative.parts:
                    raise BoundaryRuntimeError("runtime-identity-unstable")
                output_file = PurePosixPath("output") / relative
                files.add(output_file.as_posix())
                for parent in output_file.parents:
                    if parent.as_posix() != ".":
                        directories.add(parent.as_posix())
    return files, directories


def _assembled_working_paths() -> tuple[set[str], set[str]]:
    """Return the closed file set an assembled run may hold before staging."""

    files = {
        "feature-spec/portable-text-normalizer.md",
        "feature-spec/portable-text-normalizer-attempt-1.md",
        "feature-spec/portable-text-normalizer-attempt-2.md",
        "test-spec/portable-text-normalizer.test.md",
        "test-spec/portable-text-normalizer-attempt-1.test.md",
        "test-spec/portable-text-normalizer-attempt-2.test.md",
    }
    for stage in ("spec-review", "test-spec-review"):
        for prefix in (stage, f"{stage}-attempt-1", f"{stage}-attempt-2"):
            files.update(
                {
                    f"review-evidence/{prefix}-record.md",
                    f"review-evidence/{prefix}-log.md",
                    f"review-evidence/{prefix}-bundle.json",
                    f"review-evidence/{prefix}-resolution.md",
                }
            )
    directories = {"feature-spec", "test-spec", "review-evidence"}
    return files, directories


def _validate_correction_stop_evidence(
    root: Path,
    receipt: Mapping[str, object],
) -> None:
    evidence_root = root / "correction-stop-evidence"
    if evidence_root.is_symlink() or not evidence_root.is_dir():
        raise BoundaryRuntimeError("runtime-identity-unstable")
    entries = list(evidence_root.iterdir())
    if (
        {entry.name for entry in entries} != CORRECTION_STOP_EVIDENCE_FILES
        or any(entry.is_symlink() or not entry.is_file() for entry in entries)
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    raw_by_name = {entry.name: entry.read_bytes() for entry in entries}
    try:
        record = raw_by_name["review-record.md"].decode("utf-8")
        log = raw_by_name["review-log.md"].decode("utf-8")
        resolution = raw_by_name["review-resolution.md"].decode("utf-8")
    except UnicodeError as error:
        raise BoundaryRuntimeError("runtime-identity-unstable") from error
    payload = _review_payload_from_markdown(str(receipt["stage"]), record, log)
    _validate_review_payload(
        payload,
        stage=str(receipt["stage"]),
        artifact_identity=str(receipt["reviewed_artifact_identity"]),
        require_approval=False,
    )
    try:
        projection = json.loads(
            raw_by_name["finding-projection.json"].decode("utf-8")
        )
    except (UnicodeError, json.JSONDecodeError) as error:
        raise BoundaryRuntimeError("runtime-identity-unstable") from error
    bundle = _read_json(evidence_root / "review-bundle.json")
    event = _read_json(evidence_root / "review-event.json")
    artifact_refs = {
        name.removesuffix(".md").removesuffix(".json"): {
            "path": f"correction-stop-evidence/{name}",
            "identity": _sha256(raw),
        }
        for name, raw in raw_by_name.items()
        if name
        in {
            "review-record.md",
            "review-log.md",
            "review-resolution.md",
            "finding-projection.json",
        }
    }
    if (
        projection != payload["finding_projection"]
        or set(bundle) != CORRECTION_STOP_BUNDLE_FIELDS
        or bundle.get("schema_version")
        != "simple-change-correction-stop-bundle-v1"
        or bundle.get("stage") != receipt["stage"]
        or bundle.get("attempt") != 1
        or bundle.get("review_id") != receipt["review_id"]
        or bundle.get("outcome") != "changes-requested"
        or bundle.get("reviewed_artifact_identity")
        != receipt["reviewed_artifact_identity"]
        or bundle.get("material_finding_ids")
        != receipt["material_finding_ids"]
        or bundle.get("finding_projection_identity")
        != receipt["finding_projection_identity"]
        or bundle.get("correction_eligibility")
        != "owner-decision-required"
        or bundle.get("artifact_refs") != artifact_refs
        or payload["review_id"] != receipt["review_id"]
        or payload["material_finding_ids"]
        != receipt["material_finding_ids"]
        or payload["finding_projection_identity"]
        != receipt["finding_projection_identity"]
        or payload["correction_eligibility"]
        != "owner-decision-required"
        or any(
            finding_id not in resolution
            for finding_id in receipt["material_finding_ids"]
        )
        or str(receipt["review_id"]) not in resolution
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    expected_refs = [
        {
            "path": "correction-stop-evidence/review-bundle.json",
            "identity": _sha256(raw_by_name["review-bundle.json"]),
        },
        *sorted(
            artifact_refs.values(),
            key=lambda reference: str(reference["path"]),
        ),
    ]
    if (
        set(event) != CORRECTION_STOP_EVENT_FIELDS
        or event.get("schema_version")
        != "simple-change-correction-stop-event-v1"
        or event.get("stage") != receipt["stage"]
        or event.get("attempt") != 1
        or event.get("observed_result") != "changes-requested"
        or event.get("diagnostic_id")
        != "correction-authorization-required"
        or event.get("evidence_refs") != expected_refs
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")


def _working_tree_identity(
    root: Path, lease: Mapping[str, object] | None = None
) -> str:
    if root.is_symlink() or not root.is_dir():
        raise BoundaryRuntimeError("runtime-identity-unstable")
    allowed_files, allowed_directories = _working_output_paths()
    stop_path = root / "correction-stop.json"
    stop_receipt: Mapping[str, object] | None = None
    if stop_path.exists():
        if stop_path.is_symlink() or not stop_path.is_file():
            raise BoundaryRuntimeError("runtime-identity-unstable")
        stop_receipt = _read_json(stop_path)
        _validate_correction_stop_receipt(stop_receipt, lease=lease)
    assembled_files, assembled_directories = _assembled_working_paths()
    for child in root.iterdir():
        if child == stop_path:
            continue
        if child.name == "correction-stop-evidence":
            if stop_receipt is None:
                raise BoundaryRuntimeError("runtime-identity-unstable")
            _validate_correction_stop_evidence(root, stop_receipt)
            continue
        if child.name == "manifest.json":
            if child.is_symlink() or not child.is_file():
                raise BoundaryRuntimeError("runtime-identity-unstable")
            continue
        if child.name == "artifacts":
            if child.is_symlink() or not child.is_dir():
                raise BoundaryRuntimeError("runtime-identity-unstable")
            for path in child.rglob("*"):
                if path.is_symlink() or not (path.is_dir() or path.is_file()):
                    raise BoundaryRuntimeError("runtime-identity-unstable")
                relative = path.relative_to(child).as_posix()
                if path.is_dir():
                    if relative not in assembled_directories:
                        raise BoundaryRuntimeError(
                            "runtime-identity-unstable"
                        )
                elif relative not in assembled_files:
                    raise BoundaryRuntimeError("runtime-identity-unstable")
            continue
        if (
            child.is_symlink()
            or not child.is_dir()
            or re.fullmatch(
                r"boundary-proof-workspace-[a-z0-9_]+", child.name
            )
            is None
        ):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        for path in child.rglob("*"):
            if path.is_symlink() or not (path.is_dir() or path.is_file()):
                raise BoundaryRuntimeError("runtime-identity-unstable")
            relative = path.relative_to(child).as_posix()
            if path.is_dir():
                if relative not in {".git"} | allowed_directories:
                    raise BoundaryRuntimeError("runtime-identity-unstable")
            elif relative not in {"manifested.txt"} | allowed_files:
                raise BoundaryRuntimeError("runtime-identity-unstable")
    if stop_receipt is not None:
        if not (root / "correction-stop-evidence").is_dir():
            raise BoundaryRuntimeError("runtime-identity-unstable")
    return _tree_identity(root)


def _staged_tree_identity(
    repo_root: Path,
    change_id: str,
    staged: Path,
    lease: Mapping[str, object],
) -> str:
    manifest_path = staged / "manifest.json"
    manifest = _read_json(manifest_path)
    target_manifest = {
        "path": (
            f"docs/changes/{change_id}/evidence/simple-change/"
            f"runs/{lease['run_id']}/manifest.json"
        ),
        "identity": _read_file_identity(manifest_path).digest,
    }
    pointer = {
        "run_id": lease["run_id"],
        "input_set_identity": lease["input_set_identity"],
        "manifest_ref": target_manifest,
    }
    _validate_staged_run(
        repo_root,
        staged,
        manifest,
        pointer,
        lease,
        require_current_inputs=False,
    )
    return _tree_identity(staged)


def _tree_identity(root: Path) -> str:
    if root.is_symlink() or not root.is_dir():
        raise BoundaryRuntimeError("runtime-identity-unstable")
    rows: list[dict[str, str]] = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink() or not (path.is_dir() or path.is_file()):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        relative = path.relative_to(root).as_posix()
        rows.append(
            {
                "path": relative,
                "kind": "directory" if path.is_dir() else "file",
                "identity": (
                    _sha256(path.read_bytes()) if path.is_file() else "directory"
                ),
            }
        )
    return _sha256(_canonical_json_bytes(rows))


def discard_interrupted_publication(
    change_id: str,
    authorization_evidence: Path,
    *,
    authorized_by: str,
    repo_root: Path = ROOT,
    crash_at: str | None = None,
) -> dict[str, object]:
    """Discard one H-false lease-owned orphan through durable recovery evidence."""

    with _publisher_lock(repo_root, change_id):
        simple_root = _simple_root(repo_root, change_id)
        candidate = _discover_global_candidate(repo_root, change_id)
        lease_path = simple_root / "publisher.json"
        if not authorization_evidence.is_absolute():
            authorization_evidence = repo_root / authorization_evidence
        authority_ref = _regular_reference(repo_root, authorization_evidence)
        if lease_path.exists():
            authority_lease = _read_publisher_lease(repo_root, change_id)
            _validate_recovery_decision_ref(
                repo_root,
                change_id,
                authority_ref,
                run_id=authority_lease["run_id"],
                publisher_instance_id=authority_lease[
                    "publisher_instance_id"
                ],
                input_set_identity=authority_lease["input_set_identity"],
                action="discard-and-regenerate",
                authorized_by=authorized_by,
            )
        recovery_temps = sorted(simple_root.glob(".manual-recovery-run-*.tmp"))
        if len(recovery_temps) > 1:
            raise BoundaryRuntimeError("runtime-identity-unstable")
        forced_recovery_id: str | None = None
        if recovery_temps:
            temporary_path = recovery_temps[0]
            match = re.fullmatch(
                r"\.manual-recovery-(run-[0-9a-f]{32})-"
                r"(recovery-[0-9a-f]{32})\.tmp",
                temporary_path.name,
            )
            if match is None or temporary_path.is_symlink():
                raise BoundaryRuntimeError("runtime-identity-unstable")
            temp_run_id, temp_recovery_id = match.groups()
            canonical_basis = (
                simple_root / f"manual-recovery-{temp_run_id}.json"
            )
            try:
                temporary_basis = _read_json(temporary_path)
            except BoundaryRuntimeError:
                temporary_basis = None
            if temporary_basis is None:
                state_path = (
                    simple_root
                    / f"manual-recovery-state-{temp_run_id}.json"
                )
                if canonical_basis.exists():
                    basis = _read_json(canonical_basis)
                    _validate_recovery_basis(
                        repo_root,
                        change_id,
                        basis,
                        expected_run_id=temp_run_id,
                    )
                    if basis["recovery_id"] != temp_recovery_id:
                        raise BoundaryRuntimeError(
                            "runtime-identity-unstable"
                        )
                    if not state_path.exists():
                        raise BoundaryRuntimeError(
                            "runtime-identity-unstable"
                        )
                    _validate_recovery_state(
                        _read_json(state_path),
                        basis_identity=_read_file_identity(
                            canonical_basis
                        ).digest,
                        recovery_id=temp_recovery_id,
                    )
                else:
                    if (
                        not lease_path.exists()
                        or state_path.exists()
                        or (simple_root / "prepared.json").exists()
                    ):
                        raise BoundaryRuntimeError(
                            "runtime-identity-unstable"
                        )
                    lease = _read_publisher_lease(repo_root, change_id)
                    if (
                        lease["run_id"] != temp_run_id
                        or candidate != temp_run_id
                    ):
                        raise BoundaryRuntimeError(
                            "runtime-identity-unstable"
                        )
                    forced_recovery_id = temp_recovery_id
                temporary_path.unlink()
                _fsync_directory(simple_root)
            else:
                _validate_recovery_basis(
                    repo_root,
                    change_id,
                    temporary_basis,
                    expected_run_id=temp_run_id,
                )
                if temporary_basis["recovery_id"] != temp_recovery_id:
                    raise BoundaryRuntimeError("runtime-identity-unstable")
                if canonical_basis.exists():
                    if canonical_basis.read_bytes() != temporary_path.read_bytes():
                        raise BoundaryRuntimeError(
                            "runtime-identity-unstable"
                        )
                else:
                    if (
                        not lease_path.exists()
                        or (simple_root / "prepared.json").exists()
                        or _read_publisher_lease(
                            repo_root, change_id
                        )["run_id"]
                        != temp_run_id
                    ):
                        raise BoundaryRuntimeError(
                            "runtime-identity-unstable"
                        )
                    try:
                        os.link(temporary_path, canonical_basis)
                    except FileExistsError as error:
                        raise BoundaryRuntimeError(
                            "runtime-identity-unstable"
                        ) from error
                    _fsync_directory(simple_root)
                temporary_path.unlink()
                _fsync_directory(simple_root)
        basis_paths = sorted(simple_root.glob("manual-recovery-run-*.json"))
        active_basis_paths = [
            path
            for path in basis_paths
            if (
                not (
                    simple_root
                    / path.name.replace(
                        "manual-recovery-", "manual-recovery-state-"
                    )
                ).exists()
                or _read_json(
                    simple_root
                    / path.name.replace(
                        "manual-recovery-", "manual-recovery-state-"
                    )
                ).get("state")
                != "completed"
            )
        ]
        if len(active_basis_paths) > 1:
            raise BoundaryRuntimeError("runtime-identity-unstable")
        if active_basis_paths:
            basis_path = active_basis_paths[0]
            basis = _read_json(basis_path)
            run_id = str(basis.get("run_id"))
            _validate_recovery_basis(
                repo_root, change_id, basis, expected_run_id=run_id
            )
            if (
                basis.get("authorized_by") != authorized_by
                or basis.get("authorization_evidence_ref") != authority_ref
                or candidate != run_id
            ):
                raise BoundaryRuntimeError("runtime-identity-unstable")
            recovery_id = str(basis["recovery_id"])
            orphan_snapshot = basis.get("orphan_snapshot")
            if not isinstance(orphan_snapshot, dict):
                raise BoundaryRuntimeError("runtime-identity-unstable")
        else:
            if not lease_path.exists():
                raise BoundaryRuntimeError("runtime-identity-unstable")
            lease = _read_publisher_lease(repo_root, change_id)
            run_id = str(lease["run_id"])
            if candidate != run_id or (simple_root / "prepared.json").exists():
                raise BoundaryRuntimeError("runtime-identity-unstable")
            working = repo_root / str(lease["working_root"])
            staging = repo_root / str(lease["staging_root"])
            present = [path for path in (working, staging) if path.exists()]
            if len(present) > 1:
                raise BoundaryRuntimeError("runtime-identity-unstable")
            kind = (
                "working" if present and present[0] == working
                else "staging" if present
                else "lease-only"
            )
            orphan = present[0] if present else None
            recovery_id = (
                forced_recovery_id
                if forced_recovery_id is not None
                else "recovery-" + secrets.token_hex(16)
            )
            quarantine = (
                simple_root
                / f".recovery-quarantine-{run_id}-{recovery_id}-{kind}"
                if orphan is not None
                else None
            )
            lease_raw = lease_path.read_bytes()
            orphan_snapshot = {
                "kind": kind,
                "path": (
                    orphan.relative_to(repo_root).as_posix()
                    if orphan is not None
                    else None
                ),
                "identity": (
                    _working_tree_identity(orphan, lease)
                    if kind == "working" and orphan is not None
                    else _staged_tree_identity(
                        repo_root, change_id, orphan, lease
                    )
                    if kind == "staging" and orphan is not None
                    else None
                ),
                "quarantine_path": (
                    quarantine.relative_to(repo_root).as_posix()
                    if quarantine is not None
                    else None
                ),
                "durability_parent":
                    simple_root.relative_to(repo_root).as_posix(),
            }
            basis = {
                "schema_version": "simple-change-manual-recovery-v1",
                "recovery_id": recovery_id,
                "run_id": run_id,
                "publisher_instance_id": lease["publisher_instance_id"],
                "authorized_by": authorized_by,
                "authorization_evidence_ref": authority_ref,
                "publisher_lease_snapshot": {
                    "path": lease_path.relative_to(repo_root).as_posix(),
                    "identity": _sha256(lease_raw),
                    "values": lease,
                },
                "publisher_lock_proof": {
                    "method": "exclusive-nonblocking-file-lock-v1",
                    "lock_path": "publisher.lock",
                    "acquired": True,
                    "prior_lease_identity": _sha256(lease_raw),
                },
                "orphan_snapshot": orphan_snapshot,
                "input_set_identity": lease["input_set_identity"],
                "action": "discard-and-regenerate",
            }
            _validate_recovery_basis(
                repo_root, change_id, basis, expected_run_id=run_id
            )
            basis_path = simple_root / f"manual-recovery-{run_id}.json"
            temporary = (
                simple_root
                / f".manual-recovery-{run_id}-{recovery_id}.tmp"
            )
            _exclusive_write(temporary, _canonical_json_bytes(basis))
            _crash_if(crash_at, "after-recovery-temp-fsync")
            try:
                os.link(temporary, basis_path)
            except FileExistsError as error:
                raise BoundaryRuntimeError("runtime-identity-unstable") from error
            _fsync_directory(simple_root)
            _crash_if(crash_at, "after-recovery-basis-install")
            temporary.unlink()
            _fsync_directory(simple_root)
        if not isinstance(orphan_snapshot, dict) or set(orphan_snapshot) != {
            "kind", "path", "identity", "quarantine_path", "durability_parent"
        }:
            raise BoundaryRuntimeError("runtime-identity-unstable")
        basis_identity = _read_file_identity(basis_path).digest
        state_path = simple_root / f"manual-recovery-state-{run_id}.json"

        def write_state(state: str) -> None:
            _atomic_write(
                state_path,
                _canonical_json_bytes(
                    {
                        "schema_version":
                            "simple-change-manual-recovery-state-v1",
                        "recovery_id": recovery_id,
                        "basis_identity": basis_identity,
                        "state": state,
                    }
                ),
            )

        state = _read_json(state_path) if state_path.exists() else None
        if state is None:
            write_state("authorized")
            _crash_if(crash_at, "after-recovery-authorized")
            state = _read_json(state_path)
        if not isinstance(state, dict):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        _validate_recovery_state(
            state,
            basis_identity=basis_identity,
            recovery_id=recovery_id,
        )
        lease_snapshot = basis["publisher_lease_snapshot"]
        assert isinstance(lease_snapshot, dict)
        if state["state"] in {"authorized", "orphan-detached"}:
            if lease_path.exists():
                if (
                    _read_file_identity(lease_path).digest
                    != lease_snapshot["identity"]
                    or _read_json(lease_path) != lease_snapshot["values"]
                ):
                    raise BoundaryRuntimeError("runtime-identity-unstable")
            elif state["state"] == "authorized":
                raise BoundaryRuntimeError("runtime-identity-unstable")
        orphan_path = orphan_snapshot["path"]
        quarantine_path = orphan_snapshot["quarantine_path"]
        orphan = repo_root / str(orphan_path) if orphan_path is not None else None
        quarantine = (
            repo_root / str(quarantine_path)
            if quarantine_path is not None
            else None
        )
        if state["state"] == "authorized":
            if orphan is not None and orphan.exists():
                if (
                    quarantine is None
                    or quarantine.exists()
                    or _tree_identity(orphan) != orphan_snapshot["identity"]
                ):
                    raise BoundaryRuntimeError("runtime-identity-unstable")
                os.replace(orphan, quarantine)
                _crash_if(crash_at, "after-recovery-quarantine-rename")
                _fsync_directory(simple_root)
            elif quarantine is not None and quarantine.exists():
                if _tree_identity(quarantine) != orphan_snapshot["identity"]:
                    raise BoundaryRuntimeError("runtime-identity-unstable")
                _fsync_directory(simple_root)
            elif orphan_snapshot["kind"] == "lease-only":
                _fsync_directory(simple_root)
            else:
                raise BoundaryRuntimeError("runtime-identity-unstable")
            write_state("orphan-detached")
            _crash_if(crash_at, "after-recovery-orphan-detached")
            state = _read_json(state_path)
        if state["state"] == "orphan-detached":
            if lease_path.exists():
                if (
                    lease_snapshot.get("identity")
                    != _read_file_identity(lease_path).digest
                ):
                    raise BoundaryRuntimeError("runtime-identity-unstable")
                lease_path.unlink()
                _crash_if(crash_at, "after-recovery-lease-delete")
            _fsync_directory(simple_root)
            write_state("completed")
            _crash_if(crash_at, "after-recovery-completed")
            state = _read_json(state_path)
        if state["state"] != "completed" or lease_path.exists():
            raise BoundaryRuntimeError("runtime-identity-unstable")
        return {
            "result": "completed",
            "run_id": run_id,
            "recovery_id": recovery_id,
            "orphan_kind": orphan_snapshot["kind"],
            "quarantine_path": orphan_snapshot["quarantine_path"],
        }


def _generate_behavior_locked(
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
    except (
        OSError,
        UnicodeError,
        BoundaryProofError,
        BoundaryRuntimeError,
    ) as error:
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
    preflight_path = (
        _select_change_root(repo_root, change_id)
        / "evidence"
        / "runtime-preflight-attestation.json"
    )
    attestation = _read_json(preflight_path)
    _validate_attestation(attestation)
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
    input_set = {
        "schema_version": "simple-change-input-v1",
        "scenario_ref": _regular_reference(repo_root, scenario_path),
        "baseline_commit": "git:" + baseline_head,
        "skill_resource_refs": list(behavior_manifest["skill_package_refs"]),
        "oracle_refs": [
            _regular_reference(repo_root, path) for path in sorted(oracle_paths)
        ],
        "implementation_manifest_ref": implementation_ref,
    }
    input_set_identity = _sha256(_canonical_json_bytes(input_set))
    _assert_correction_input_is_fresh(
        repo_root, change_id, input_set_identity
    )
    run_id = "run-" + secrets.token_hex(16)
    publisher_instance_id = "publisher-" + secrets.token_hex(16)
    lease, working_root = _create_publisher_lease(
        repo_root,
        change_id,
        run_id,
        publisher_instance_id,
        input_set_identity,
    )

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
                workspace_parent=working_root,
            )
            if len(generated) != 1:
                raise BoundaryRuntimeError("protocol-shape-incompatible")
            return observed_attestation, generated[0]

        variants = _stage_policy_variants(
            str(stage_request["stage"]),
            int(stage_request.get("attempt", 1)),
        )
        allowed_path_sets = [
            [str(artifact["path"]) for artifact in variant["artifacts"]]
            for variant in variants
        ]
        observed, result, attempts = _invoke_with_reconciliation(
            invoke,
            list(stage_request["expected_outputs"]),
            allowed_path_sets=allowed_path_sets,
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
        event_key = (
            f"{stage_request['stage']}#{int(stage_request.get('attempt', 1))}"
        )
        for attempt in attempts:
            attempt["event_key"] = event_key
        result["attempt"] = int(stage_request.get("attempt", 1))
        stage_artifacts_by_event[event_key] = dict(artifacts)
        if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
            print(f"stage-complete:{stage_request['stage']}", file=sys.stderr)
        return observed, result, attempts, artifacts

    stage_results: list[dict[str, object]] = []
    stage_attestations: list[dict[str, object]] = []
    transport_attempts: list[dict[str, object]] = []
    stage_artifacts: dict[str, str] = {}
    stage_artifacts_by_event: dict[str, dict[str, str]] = {}
    correction_history: dict[str, object] | None = None

    spec_request = _workflow_stage_request(
        "spec", str(scenario["request"])
    )
    observed, spec_result, attempts, artifacts = run_stage(spec_request)
    stage_attestations.append(observed)
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
    except (BoundaryProofError, BoundaryRuntimeError) as error:
        if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
            print(f"boundary-structure:spec:{error}", file=sys.stderr)
            print(feature_markdown[:8192], file=sys.stderr)
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
        require_approval=False,
    )
    if spec_review_payload["outcome"] == "changes-requested":
        if (
            spec_review_payload["correction_eligibility"]
            == "owner-decision-required"
        ):
            resolution_markdown = artifacts.get(
                "review-resolution/spec-review.md"
            )
            if not isinstance(resolution_markdown, str):
                raise BoundaryRuntimeError(
                    "protocol-shape-incompatible", "in-turn"
                )
            _write_correction_stop(
                working_root,
                lease,
                stage="spec-review",
                reviewed_artifact_identity=feature_identity,
                review_payload=spec_review_payload,
                resolution_markdown=resolution_markdown,
            )
            raise BoundaryRuntimeError(
                "correction-authorization-required", "in-turn"
            )
        if (
            spec_review_payload["correction_eligibility"]
            != "automatic-eligible"
        ):
            raise BoundaryRuntimeError(
                "protocol-shape-incompatible", "in-turn"
            )
        resolution_path = "review-resolution/spec-review.md"
        resolution_markdown = artifacts.get(resolution_path)
        if not isinstance(resolution_markdown, str):
            raise BoundaryRuntimeError(
                "unexpected-prohibited-event", "in-turn"
            )
        initial_feature_markdown = feature_markdown
        initial_feature_identity = feature_identity
        initial_spec_review_payload = dict(spec_review_payload)
        initial_spec_review_resolution = resolution_markdown
        correction_request = _workflow_stage_request(
            "spec",
            "The reviewer-declared finding is authorized for bounded "
            "correction. Apply its recorded Required outcome exactly, preserve "
            "R1-R4, change the feature-spec bytes, and update the supplied "
            "review resolution to record that action. Do not reject, "
            "reinterpret, or leave the finding unresolved.",
            attempt=2,
            artifact_context=(
                "Authoritative scenario request:\n"
                + str(scenario["request"])
                + "\n\nPrior feature specification:\n"
                + initial_feature_markdown
                + "\n\nChanges-requested review:\n"
                + str(spec_review_payload["review_record_markdown"])
                + "\n\nOpen review resolution:\n"
                + resolution_markdown
            ),
        )
        observed, result, attempts, correction_artifacts = run_stage(
            correction_request
        )
        stage_attestations.append(observed)
        stage_results.append(result)
        transport_attempts.extend(attempts)
        stage_artifacts.update(correction_artifacts)
        feature_markdown = correction_artifacts[
            "feature-spec/portable-text-normalizer.md"
        ]
        feature_identity = _sha256(feature_markdown.encode("utf-8"))
        if feature_identity == initial_feature_identity:
            raise BoundaryRuntimeError(
                "boundary-oracle-mismatch", "in-turn"
            )
        try:
            normalized_feature = normalize_feature_model(
                _parse_feature_markdown(feature_markdown)
            )
            if feature_invariant_projection(
                normalized_feature
            ) != feature_invariant_projection(candidate_feature):
                raise BoundaryProofError(
                    "corrected feature differs from the closed invariant "
                    "projection"
                )
        except (BoundaryProofError, BoundaryRuntimeError) as error:
            raise BoundaryRuntimeError(
                "boundary-oracle-mismatch", "in-turn"
            ) from error
        closed_resolution = correction_artifacts.get(resolution_path)
        if not isinstance(closed_resolution, str):
            raise BoundaryRuntimeError(
                "unexpected-prohibited-event", "in-turn"
            )
        rereview_request = _workflow_stage_request(
            "spec-review",
            "Rereview the corrected feature specification against the exact "
            "prior findings and record the formal result.",
            attempt=2,
            artifact_context=(
                "Authoritative scenario request:\n"
                + str(scenario["request"])
                + f"\n\nReviewed artifact identity: {feature_identity}\n\n"
                + feature_markdown
                + "\n\nPrior changes-requested review:\n"
                + str(initial_spec_review_payload["review_record_markdown"])
                + "\n\nUpdated review resolution:\n"
                + closed_resolution
            ),
        )
        observed, result, attempts, rereview_artifacts = run_stage(
            rereview_request
        )
        stage_attestations.append(observed)
        stage_results.append(result)
        transport_attempts.extend(attempts)
        stage_artifacts.update(rereview_artifacts)
        spec_review_payload = _review_payload_from_markdown(
            "spec-review",
            rereview_artifacts["reviews/spec-review.md"],
            rereview_artifacts["review-log/spec-review.md"],
        )
        _validate_review_payload(
            spec_review_payload,
            stage="spec-review",
            artifact_identity=feature_identity,
        )
        correction_history = {
            "role": "feature-spec",
            "initial_artifact_markdown": initial_feature_markdown,
            "initial_artifact_identity": initial_feature_identity,
            "initial_review": initial_spec_review_payload,
            "initial_resolution_markdown": initial_spec_review_resolution,
            "corrected_resolution_markdown": rereview_artifacts.get(
                resolution_path, closed_resolution
            ),
        }
    else:
        _validate_review_payload(
            spec_review_payload,
            stage="spec-review",
            artifact_identity=feature_identity,
        )

    test_spec_request = _workflow_stage_request(
        "test-spec",
        "Author the complete proof map for the approved feature specification. "
        "For R2, deterministically enumerate every code point in the Unicode "
        "`White_Space` property and prove both removal at text boundaries and "
        "preservation of the same code points between retained non-whitespace "
        "code points. Treat this as proof guidance, not additional normative "
        "feature behavior.",
        artifact_context=(
            feature_markdown
            + "\n\nApproved formal review:\n"
            + str(spec_review_payload["review_record_markdown"])
        ),
        governing_reference_ids=tuple(
            sorted(
                {
                    boundary_id
                    for entry in (
                        *normalized_feature.core_dimensions,
                        *normalized_feature.extensions,
                    )
                    if entry.applicability == "applicable"
                    for boundary_id in entry.boundary_ids
                }
                | {
                    interaction.interaction_id
                    for interaction in normalized_feature.interactions
                }
            )
        ),
        governing_interaction_ids=tuple(
            sorted(
                interaction.interaction_id
                for interaction in normalized_feature.interactions
            )
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
    except (BoundaryProofError, BoundaryRuntimeError) as error:
        if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
            print(f"boundary-structure:test-spec:{error}", file=sys.stderr)
            print(test_spec_markdown[:8192], file=sys.stderr)
        raise BoundaryRuntimeError(
            "boundary-oracle-mismatch", "in-turn"
        ) from error

    test_review_request = _workflow_stage_request(
        "test-spec-review",
        "Under approved R28y, perform the isolated behavior-evidence review of "
        "the exact test specification and record the formal result. The closed "
        "upstream set is the authoritative scenario request, approved feature "
        "specification, approving feature review, and current test "
        "specification supplied here. Architecture, plan, and plan-review are "
        "outside this scenario and must not be invented or required. This "
        "review never grants implementation authority; record "
        "`Implementation handoff: not-allowed` even when approved.",
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
        require_approval=False,
    )
    if test_review_payload["outcome"] == "changes-requested":
        if (
            test_review_payload["correction_eligibility"]
            == "owner-decision-required"
        ):
            resolution_markdown = artifacts.get(
                "review-resolution/test-spec-review.md"
            )
            if not isinstance(resolution_markdown, str):
                raise BoundaryRuntimeError(
                    "protocol-shape-incompatible", "in-turn"
                )
            _write_correction_stop(
                working_root,
                lease,
                stage="test-spec-review",
                reviewed_artifact_identity=test_spec_identity,
                review_payload=test_review_payload,
                resolution_markdown=resolution_markdown,
            )
            raise BoundaryRuntimeError(
                "correction-authorization-required", "in-turn"
            )
        if (
            test_review_payload["correction_eligibility"]
            != "automatic-eligible"
        ):
            raise BoundaryRuntimeError(
                "protocol-shape-incompatible", "in-turn"
            )
        if correction_history is not None:
            raise BoundaryRuntimeError("review-nonapproval", "in-turn")
        resolution_path = "review-resolution/test-spec-review.md"
        resolution_markdown = artifacts.get(resolution_path)
        if not isinstance(resolution_markdown, str):
            raise BoundaryRuntimeError(
                "unexpected-prohibited-event", "in-turn"
            )
        initial_test_spec_markdown = test_spec_markdown
        initial_test_spec_identity = test_spec_identity
        initial_test_review_payload = dict(test_review_payload)
        initial_test_review_resolution = resolution_markdown
        reference_ids = tuple(
            sorted(
                {
                    boundary_id
                    for entry in (
                        *normalized_feature.core_dimensions,
                        *normalized_feature.extensions,
                    )
                    if entry.applicability == "applicable"
                    for boundary_id in entry.boundary_ids
                }
                | {
                    interaction.interaction_id
                    for interaction in normalized_feature.interactions
                }
            )
        )
        interaction_ids = tuple(
            sorted(
                interaction.interaction_id
                for interaction in normalized_feature.interactions
            )
        )
        correction_request = _workflow_stage_request(
            "test-spec",
            "The reviewer-declared finding is authorized for bounded "
            "correction. Apply its recorded Required outcome exactly, change "
            "the test-spec bytes, and update the supplied review resolution "
            "to record that action. Do not reject, reinterpret, or leave the "
            "finding unresolved.",
            attempt=2,
            governing_reference_ids=reference_ids,
            governing_interaction_ids=interaction_ids,
            artifact_context=(
                "Governing approved feature specification:\n"
                + feature_markdown
                + "\n\nPrior test specification:\n"
                + initial_test_spec_markdown
                + "\n\nChanges-requested review:\n"
                + str(test_review_payload["review_record_markdown"])
                + "\n\nOpen review resolution:\n"
                + resolution_markdown
            ),
        )
        observed, result, attempts, correction_artifacts = run_stage(
            correction_request
        )
        stage_attestations.append(observed)
        stage_results.append(result)
        transport_attempts.extend(attempts)
        stage_artifacts.update(correction_artifacts)
        test_spec_markdown = correction_artifacts[
            "test-spec/portable-text-normalizer.test.md"
        ]
        test_spec_identity = _sha256(test_spec_markdown.encode("utf-8"))
        if test_spec_identity == initial_test_spec_identity:
            if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
                print(
                    "correction-identity-unchanged:test-spec",
                    file=sys.stderr,
                )
                print(
                    str(correction_artifacts.get(resolution_path, ""))[:8192],
                    file=sys.stderr,
                )
            raise BoundaryRuntimeError(
                "boundary-oracle-mismatch", "in-turn"
            )
        try:
            normalized_proof = normalize_proof_map(
                _parse_test_spec_markdown(test_spec_markdown),
                normalized_feature,
            )
            if proof_invariant_projection(
                normalized_proof
            ) != proof_invariant_projection(candidate_proof):
                raise BoundaryProofError(
                    "corrected proof differs from the closed invariant "
                    "projection"
                )
        except (BoundaryProofError, BoundaryRuntimeError) as error:
            raise BoundaryRuntimeError(
                "boundary-oracle-mismatch", "in-turn"
            ) from error
        closed_resolution = correction_artifacts.get(resolution_path)
        if not isinstance(closed_resolution, str):
            raise BoundaryRuntimeError(
                "unexpected-prohibited-event", "in-turn"
            )
        rereview_request = _workflow_stage_request(
            "test-spec-review",
            "Under approved R28y, rereview the corrected test specification "
            "against the exact prior findings in the isolated "
            "behavior-evidence mode. Use only the closed supplied upstream "
            "set; architecture, plan, and plan-review are outside this "
            "scenario. Record the formal result and always record "
            "`Implementation handoff: not-allowed`.",
            attempt=2,
            artifact_context=(
                "Authoritative scenario request:\n"
                + str(scenario["request"])
                + f"\n\nReviewed artifact identity: {test_spec_identity}\n\n"
                + test_spec_markdown
                + "\n\nGoverning feature specification:\n"
                + feature_markdown
                + "\n\nApproved feature review:\n"
                + str(spec_review_payload["review_record_markdown"])
                + "\n\nPrior changes-requested review:\n"
                + str(initial_test_review_payload["review_record_markdown"])
                + "\n\nUpdated review resolution:\n"
                + closed_resolution
            ),
        )
        observed, result, attempts, rereview_artifacts = run_stage(
            rereview_request
        )
        stage_attestations.append(observed)
        stage_results.append(result)
        transport_attempts.extend(attempts)
        stage_artifacts.update(rereview_artifacts)
        test_review_payload = _review_payload_from_markdown(
            "test-spec-review",
            rereview_artifacts["reviews/test-spec-review.md"],
            rereview_artifacts["review-log/test-spec-review.md"],
        )
        _validate_review_payload(
            test_review_payload,
            stage="test-spec-review",
            artifact_identity=test_spec_identity,
        )
        correction_history = {
            "role": "test-spec",
            "initial_artifact_markdown": initial_test_spec_markdown,
            "initial_artifact_identity": initial_test_spec_identity,
            "initial_review": initial_test_review_payload,
            "initial_resolution_markdown": initial_test_review_resolution,
            "corrected_resolution_markdown": rereview_artifacts.get(
                resolution_path, closed_resolution
            ),
        }
    else:
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
        for observed in stage_attestations
        for field in attestation_identity_fields
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable", "in-turn")
    thread_ids = [result.get("thread_id") for result in stage_results]
    if (
        any(not isinstance(value, str) for value in thread_ids)
        or len(set(thread_ids)) != len(thread_ids)
    ):
        raise BoundaryRuntimeError("thread-metadata-mismatch", "in-turn")
    feature_model = _feature_record(normalized_feature)
    proof_map = _proof_record(normalized_proof)
    payload = {
        "feature_model": feature_model,
        "spec_review": spec_review_payload,
        "proof_map": proof_map,
        "test_spec_review": test_review_payload,
        "stage_artifacts": {
            path: stage_artifacts[path]
            for path in (
                "feature-spec/portable-text-normalizer.md",
                "reviews/spec-review.md",
                "review-log/spec-review.md",
                "test-spec/portable-text-normalizer.test.md",
                "reviews/test-spec-review.md",
                "review-log/test-spec-review.md",
            )
        },
        "correction_history": correction_history,
        "transport_attempts": transport_attempts,
        "stage_provenance": [
            {
                "stage": result["stage"],
                "attempt": result["attempt"],
                "thread_id": result["thread_id"],
                "skill_names": ["workflow", result["stage"]],
            }
            for result in stage_results
        ],
    }
    transport_policy_identity = _sha256(
        _canonical_json_bytes(behavior_manifest["transport_policy"])
    )
    payload["transport_attempts"] = _validate_transport_rows(
        _finalize_transport_rows(
            transport_attempts,
            stage_artifacts_by_event,
            transport_policy_identity,
        ),
        transport_policy_identity,
    )
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
        publisher_instance_id,
        working_root,
    )
    _validate_scenario_expectations(scenario, run_manifest["events"])
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


def generate_behavior(
    change_id: str,
    scenario_path: Path,
    *,
    repo_root: Path = ROOT,
    command: str = "codex",
) -> dict[str, object]:
    with _publisher_lock(repo_root, change_id):
        return _generate_behavior_locked(
            change_id,
            scenario_path,
            repo_root=repo_root,
            command=command,
        )


def _validate_behavior_locked(
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


def validate_behavior(
    change_id: str, *, repo_root: Path = ROOT
) -> dict[str, object]:
    with _publisher_lock(repo_root, change_id):
        return _validate_behavior_locked(change_id, repo_root=repo_root)


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
                _trace_prohibited_event(
                    "method-not-string",
                    source=(
                        "ServerRequest"
                        if "id" in response
                        else "ServerNotification"
                    ),
                )
                raise BoundaryRuntimeError(
                    "unexpected-prohibited-event", "in-turn"
                )
            source = "ServerRequest" if "id" in response else "ServerNotification"
            classification = classifications.get(f"{source}:{method}")
            if classification is None or classification == (
                "prohibited-capability-event"
            ):
                _trace_prohibited_event(
                    "classification-rejected",
                    event_kind=f"{source}:{method}",
                    classification=classification,
                )
                raise BoundaryRuntimeError(
                    "unexpected-prohibited-event", "in-turn"
                )
            params = response.get("params")
            if not isinstance(params, dict):
                _trace_prohibited_event(
                    "params-not-object",
                    event_kind=f"{source}:{method}",
                )
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
                _trace_prohibited_event(
                    "remote-control-policy-violation",
                    event_kind=f"{source}:{method}",
                    status_is_disabled=params.get("status") == "disabled",
                    environment_identity_is_null=(
                        params.get("environmentId") is None
                    ),
                )
                raise BoundaryRuntimeError(
                    "unexpected-prohibited-event", "in-turn"
                )
            if method == "error":
                _trace_prohibited_event(
                    "runtime-error-event",
                    event_kind=f"{source}:{method}",
                )
                raise BoundaryRuntimeError(
                    "unexpected-prohibited-event", "in-turn"
                )
            event_methods.append(method)
            if method == "item/completed":
                item = params.get("item")
                if not isinstance(item, dict):
                    _trace_prohibited_event(
                        "completed-item-not-object",
                        event_kind=f"{source}:{method}",
                    )
                    raise BoundaryRuntimeError(
                        "unexpected-prohibited-event", "in-turn"
                    )
                item_type = item.get("type")
                if item_type == "agentMessage":
                    text = item.get("text")
                    if not isinstance(text, str):
                        _trace_prohibited_event(
                            "agent-message-text-not-string",
                            event_kind=f"{source}:{method}",
                            item_type=item_type,
                        )
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
                        _trace_prohibited_event(
                            "completed-item-type-rejected",
                            event_kind=f"{source}:{method}",
                            item_type=item_type,
                            status=item.get("status"),
                        )
                        raise BoundaryRuntimeError(
                            "unexpected-prohibited-event", "in-turn"
                        )
                    file_change_terminal_statuses.append("declined")
            if method == "turn/completed":
                if params.get("threadId") != thread_id:
                    _trace_prohibited_event(
                        "turn-thread-mismatch",
                        event_kind=f"{source}:{method}",
                    )
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
                    _trace_prohibited_event(
                        "turn-terminal-shape-rejected",
                        event_kind=f"{source}:{method}",
                        turn_is_object=isinstance(turn, dict),
                        status=(
                            turn.get("status")
                            if isinstance(turn, dict)
                            else None
                        ),
                        error_is_null=(
                            turn.get("error") is None
                            if isinstance(turn, dict)
                            else False
                        ),
                        agent_message_count=len(messages),
                    )
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
            if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
                print(
                    "unexpected-skill:"
                    f"name={name!r};path={path_value!r};"
                    f"enabled={enabled!r};scope={scope!r}",
                    file=sys.stderr,
                )
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
    workspace_parent: Path | None = None,
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
        tempfile.TemporaryDirectory(
            prefix="boundary-proof-workspace-",
            dir=workspace_parent,
        ) as work_raw,
    ):
        schema_root = Path(schema_raw)
        runtime_home = Path(home_raw)
        workspace = Path(work_raw)
        runtime_home.chmod(0o700)
        workspace.chmod(0o700)
        # The durable working root lives below the repository. Give each
        # ephemeral child workspace its own project boundary so Codex does not
        # inherit repository-local skills or instruction files from ancestors.
        (workspace / ".git").mkdir(mode=0o700)
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
                stage_skill_root = runtime_home / "skills" / skill_names[-1]
                reference_path = (
                    stage_skill_root / "references" / "boundary-proof-model.md"
                )
                try:
                    resource_paths = [
                        reference_path,
                        *sorted((stage_skill_root / "assets").glob("*.md")),
                    ]
                    required_reference_text = "\n\n".join(
                        "Installed resource "
                        + path.relative_to(stage_skill_root).as_posix()
                        + ":\n\n"
                        + path.read_text(encoding="utf-8")
                        for path in resource_paths
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
            try:
                envelope, output_files = _parse_stage_envelope(
                    message,
                    stage=str(generation_request["stage"]),
                    attempt=int(generation_request.get("attempt", 1)),
                )
            except BoundaryRuntimeError:
                if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
                    print(
                        "stage-envelope-rejected:"
                        + str(generation_request["stage"])
                        + ":"
                        + message[:4096],
                        file=sys.stderr,
                    )
                raise
            if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
                print(
                    f"stage-envelope-accepted:{generation_request['stage']}",
                    file=sys.stderr,
                )
            materialization = _materialize_stage_envelope(
                workspace / "output",
                envelope,
                attempt=int(generation_request.get("attempt", 1)),
            )
            if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
                print(
                    f"stage-materialized:{generation_request['stage']}",
                    file=sys.stderr,
                )
            generation_result["thread_id"] = thread_id
            generation_result["stage"] = generation_request.get("stage")
            generation_result["skill_names"] = list(skill_names)
            generation_result["runtime_process_id"] = runtime_process_id
            generation_result["output_files"] = output_files
            generation_result["stage_envelope"] = envelope
            generation_result["materialization_observation"] = materialization
            generation_sink.append(generation_result)
            if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
                print(
                    f"stage-result-collected:{generation_request['stage']}",
                    file=sys.stderr,
                )
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


PRESERVATION_MANIFEST_ID: Final[str] = (
    "boundary-preservation-manifest-v1"
)
PRESERVATION_RESULT_SCHEMA: Final[str] = (
    "boundary-preservation-result-v1"
)


def _git_blob(repo_root: Path, commit: str, path: str) -> bytes:
    if re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    if PurePosixPath(path).is_absolute() or ".." in PurePosixPath(path).parts:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    process = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=repo_root,
        check=False,
        capture_output=True,
    )
    if process.returncode != 0:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    return process.stdout


def _preservation_pair_keys() -> tuple[str, ...]:
    return tuple(
        f"{skill}:{category}"
        for skill in EVALUATED_SKILLS
        for category in PRESERVATION_KEYS
    )


def _preservation_inputs(
    repo_root: Path,
) -> tuple[tuple[str, bytes, bytes], ...]:
    rows: list[tuple[str, bytes, bytes]] = []
    for skill in EVALUATED_SKILLS:
        skill_path = repo_root / "skills" / skill / "SKILL.md"
        resource_path = (
            repo_root
            / "skills"
            / skill
            / BOUNDARY_PROOF_REFERENCE
        )
        try:
            skill_raw = skill_path.read_bytes()
            resource_raw = resource_path.read_bytes()
        except OSError as error:
            raise BoundaryRuntimeError(
                "runtime-identity-unstable"
            ) from error
        if b"Boundary model version: v1" not in resource_raw:
            raise BoundaryRuntimeError("runtime-identity-unstable")
        rows.append((skill, skill_raw, resource_raw))
    return tuple(rows)


def _preservation_run_id(
    baseline_commit: str,
    inputs: Sequence[tuple[str, bytes, bytes]],
) -> str:
    projection = {
        "result_schema": PRESERVATION_RESULT_SCHEMA,
        "baseline_commit": baseline_commit,
        "skills": [
            {
                "skill": skill,
                "skill_identity": _sha256(skill_raw),
                "resource_identity": _sha256(resource_raw),
            }
            for skill, skill_raw, resource_raw in inputs
        ],
    }
    return "run-" + hashlib.sha256(
        _canonical_json_bytes(projection)
    ).hexdigest()[:32]


def _preservation_baseline(
    repo_root: Path, change_id: str
) -> str:
    baseline_path = (
        _select_change_root(repo_root, change_id)
        / "evidence"
        / "boundary-proof-baseline.json"
    )
    baseline = _read_json(baseline_path)
    if (
        set(baseline)
        != {
            "schema_version",
            "change_id",
            "preservation_baseline_commit",
        }
        or baseline.get("schema_version")
        != "boundary-proof-baseline-v1"
        or baseline.get("change_id") != change_id
        or not isinstance(
            baseline.get("preservation_baseline_commit"), str
        )
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    commit = str(baseline["preservation_baseline_commit"])
    if re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise BoundaryRuntimeError("runtime-identity-unstable")
    return commit


def generate_preservation(
    change_id: str, *, repo_root: Path = ROOT
) -> dict[str, object]:
    """Materialize the exact invocation-free eight-skill preservation set."""

    change_root = _select_change_root(repo_root, change_id)
    baseline_commit = _preservation_baseline(repo_root, change_id)
    inputs = _preservation_inputs(repo_root)
    run_id = _preservation_run_id(baseline_commit, inputs)
    preservation_root = change_root / "evidence" / "preservation"
    run_root = preservation_root / run_id
    manifest_path = preservation_root / "manifest.json"

    if run_root.exists():
        return validate_preservation(change_id, repo_root=repo_root)

    preservation_root.mkdir(parents=True, exist_ok=True)
    temporary_root = preservation_root / f".{run_id}.tmp"
    if temporary_root.exists():
        shutil.rmtree(temporary_root)
    before_root = temporary_root / "before"
    after_root = temporary_root / "after"
    before_refs: list[dict[str, object]] = []
    after_refs: list[dict[str, object]] = []
    try:
        for skill, skill_raw, resource_raw in inputs:
            origin_path = f"skills/{skill}/SKILL.md"
            origin_raw = _git_blob(
                repo_root, baseline_commit, origin_path
            )
            for category in PRESERVATION_KEYS:
                pair_key = f"{skill}:{category}"
                before_path = before_root / skill / f"{category}.md"
                _atomic_write(before_path, origin_raw)
                before_final = (
                    run_root
                    / "before"
                    / skill
                    / f"{category}.md"
                )
                before_refs.append(
                    {
                        "pair_key": pair_key,
                        "origin_path": origin_path,
                        "origin_commit": baseline_commit,
                        "snapshot_ref": {
                            "path": before_final.relative_to(
                                repo_root
                            ).as_posix(),
                            "identity": _sha256(origin_raw),
                        },
                    }
                )
                result = {
                    "schema_version": PRESERVATION_RESULT_SCHEMA,
                    "pair_key": pair_key,
                    "category": category,
                    "result": "structural-pass",
                    "before_identity": _sha256(origin_raw),
                    "current_skill_ref": {
                        "path": origin_path,
                        "identity": _sha256(skill_raw),
                    },
                    "current_resource_ref": {
                        "path": (
                            f"skills/{skill}/"
                            f"{BOUNDARY_PROOF_REFERENCE}"
                        ),
                        "identity": _sha256(resource_raw),
                    },
                    "upstream_invocation_count": 0,
                    "semantic_review_required": True,
                }
                result_raw = _canonical_json_bytes(result)
                after_path = after_root / skill / f"{category}.json"
                _atomic_write(after_path, result_raw)
                after_final = (
                    run_root
                    / "after"
                    / skill
                    / f"{category}.json"
                )
                after_refs.append(
                    {
                        "pair_key": pair_key,
                        "artifact_ref": {
                            "path": after_final.relative_to(
                                repo_root
                            ).as_posix(),
                            "identity": _sha256(result_raw),
                        },
                    }
                )
        manifest = {
            "manifest_id": PRESERVATION_MANIFEST_ID,
            "baseline_commit": baseline_commit,
            "skills": list(EVALUATED_SKILLS),
            "before_refs": before_refs,
            "after_refs": after_refs,
        }
        os.replace(temporary_root, run_root)
        _fsync_directory(preservation_root)
        _atomic_write(manifest_path, _canonical_json_bytes(manifest))
    except Exception:
        if temporary_root.exists():
            shutil.rmtree(temporary_root)
        raise
    return validate_preservation(change_id, repo_root=repo_root)


def validate_preservation(
    change_id: str, *, repo_root: Path = ROOT
) -> dict[str, object]:
    """Validate preservation origins and current refs without reinvocation."""

    change_root = _select_change_root(repo_root, change_id)
    baseline_commit = _preservation_baseline(repo_root, change_id)
    inputs = _preservation_inputs(repo_root)
    current_inputs = {
        skill: (skill_raw, resource_raw)
        for skill, skill_raw, resource_raw in inputs
    }
    manifest_path = (
        change_root / "evidence" / "preservation" / "manifest.json"
    )
    manifest = _read_json(manifest_path)
    if (
        set(manifest)
        != {
            "manifest_id",
            "baseline_commit",
            "skills",
            "before_refs",
            "after_refs",
        }
        or manifest.get("manifest_id")
        != PRESERVATION_MANIFEST_ID
        or manifest.get("baseline_commit") != baseline_commit
        or manifest.get("skills") != list(EVALUATED_SKILLS)
        or not isinstance(manifest.get("before_refs"), list)
        or not isinstance(manifest.get("after_refs"), list)
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    expected_keys = _preservation_pair_keys()
    before_rows = manifest["before_refs"]
    after_rows = manifest["after_refs"]
    assert isinstance(before_rows, list)
    assert isinstance(after_rows, list)
    if (
        len(before_rows) != len(expected_keys)
        or len(after_rows) != len(expected_keys)
    ):
        raise BoundaryRuntimeError("runtime-identity-unstable")
    if [
        row.get("pair_key") if isinstance(row, dict) else None
        for row in before_rows
    ] != list(expected_keys) or [
        row.get("pair_key") if isinstance(row, dict) else None
        for row in after_rows
    ] != list(expected_keys):
        raise BoundaryRuntimeError("runtime-identity-unstable")

    for pair_key, before_row, after_row in zip(
        expected_keys, before_rows, after_rows, strict=True
    ):
        if not isinstance(before_row, dict) or set(before_row) != {
            "pair_key",
            "origin_path",
            "origin_commit",
            "snapshot_ref",
        }:
            raise BoundaryRuntimeError("runtime-identity-unstable")
        skill, category = pair_key.split(":", 1)
        origin_path = f"skills/{skill}/SKILL.md"
        if (
            before_row["origin_path"] != origin_path
            or before_row["origin_commit"] != baseline_commit
        ):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        snapshot = before_row["snapshot_ref"]
        if not isinstance(snapshot, dict):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        snapshot_path = _validate_reference(repo_root, snapshot)
        if (
            "/evidence/preservation/" not in f"/{snapshot['path']}"
            or snapshot_path.read_bytes()
            != _git_blob(repo_root, baseline_commit, origin_path)
        ):
            raise BoundaryRuntimeError("runtime-identity-unstable")

        if not isinstance(after_row, dict) or set(after_row) != {
            "pair_key",
            "artifact_ref",
        }:
            raise BoundaryRuntimeError("runtime-identity-unstable")
        artifact = after_row["artifact_ref"]
        if not isinstance(artifact, dict):
            raise BoundaryRuntimeError("runtime-identity-unstable")
        artifact_path = _validate_reference(repo_root, artifact)
        if "/evidence/preservation/" not in f"/{artifact['path']}":
            raise BoundaryRuntimeError("runtime-identity-unstable")
        result = _read_json(artifact_path)
        skill_raw, resource_raw = current_inputs[skill]
        if result != {
            "schema_version": PRESERVATION_RESULT_SCHEMA,
            "pair_key": pair_key,
            "category": category,
            "result": "structural-pass",
            "before_identity": snapshot["identity"],
            "current_skill_ref": {
                "path": origin_path,
                "identity": _sha256(skill_raw),
            },
            "current_resource_ref": {
                "path": (
                    f"skills/{skill}/{BOUNDARY_PROOF_REFERENCE}"
                ),
                "identity": _sha256(resource_raw),
            },
            "upstream_invocation_count": 0,
            "semantic_review_required": True,
        }:
            raise BoundaryRuntimeError("runtime-identity-unstable")
    return {
        "result": "structural-pass",
        "pair_count": len(expected_keys),
        "upstream_invocation_count": 0,
        "manifest": manifest,
    }


def generate_canonical_skill_resource_manifest(
    change_id: str, *, repo_root: Path = ROOT
) -> dict[str, object]:
    """Write the exact current eight-skill resource manifest."""

    change_root = _select_change_root(repo_root, change_id)
    files: list[dict[str, str]] = []
    for skill, skill_raw, resource_raw in _preservation_inputs(repo_root):
        files.extend(
            (
                {
                    "skill": skill,
                    "logical_path": "SKILL.md",
                    "path": f"skills/{skill}/SKILL.md",
                    "identity": _sha256(skill_raw),
                },
                {
                    "skill": skill,
                    "logical_path": BOUNDARY_PROOF_REFERENCE,
                    "path": (
                        f"skills/{skill}/{BOUNDARY_PROOF_REFERENCE}"
                    ),
                    "identity": _sha256(resource_raw),
                },
            )
        )
    files.sort(key=lambda row: row["path"])
    manifest = {
        "manifest_id": "canonical-boundary-skill-resources-v1",
        "skills": list(EVALUATED_SKILLS),
        "files": files,
    }
    target = (
        change_root
        / "evidence"
        / "canonical-skill-resource-manifest.json"
    )
    _atomic_write(target, _canonical_json_bytes(manifest))
    return manifest


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
    generate_preservation_parser = subparsers.add_parser(
        "generate-preservation",
        help="materialize exact eight-skill preservation evidence",
    )
    generate_preservation_parser.add_argument("--change-id", required=True)
    validate_preservation_parser = subparsers.add_parser(
        "validate-preservation",
        help="validate preservation evidence without upstream reinvocation",
    )
    validate_preservation_parser.add_argument("--change-id", required=True)
    resource_manifest_parser = subparsers.add_parser(
        "generate-resource-manifest",
        help="write the exact current eight-skill resource manifest",
    )
    resource_manifest_parser.add_argument("--change-id", required=True)
    recover = subparsers.add_parser(
        "recover-discard",
        help=(
            "discard one interrupted lease-owned run with an exact "
            "change-local recovery decision"
        ),
    )
    recover.add_argument("--change-id", required=True)
    recover.add_argument(
        "--authorization-evidence",
        required=True,
        type=Path,
        help=(
            "docs/changes/<change-id>/recovery-decisions/"
            "<run-id>.json"
        ),
    )
    recover.add_argument("--authorized-by", required=True)
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
        elif args.command == "generate-preservation":
            result = generate_preservation(args.change_id)
        elif args.command == "validate-preservation":
            result = validate_preservation(args.change_id)
        elif args.command == "generate-resource-manifest":
            result = generate_canonical_skill_resource_manifest(
                args.change_id
            )
        elif args.command == "recover-discard":
            result = discard_interrupted_publication(
                args.change_id,
                args.authorization_evidence,
                authorized_by=args.authorized_by,
            )
        elif args.command == "exercise-fixture":
            result = exercise_fixture(args.fixture, args.output_root)
        elif args.command == "validate-fixture":
            result = validate_fixture(args.root)
        else:
            raise AssertionError(f"unknown command: {args.command}")
    except (BoundaryRuntimeError, BoundaryProofError, OSError) as error:
        if os.environ.get("BOUNDARY_PROOF_DIAGNOSTICS") == "1":
            traceback.print_exc()
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
