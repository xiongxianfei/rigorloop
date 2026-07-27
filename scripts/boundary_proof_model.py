#!/usr/bin/env python3
"""Immutable executable projection of the boundary-first proof contract.

The approved workflow and skill specifications remain normative.  This module
implements only deterministic shape, vocabulary, traceability, and aggregate
rules.  It deliberately does not judge semantic completeness, applicability,
partition quality, interaction sufficiency, or review reasoning.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence


CORE_DIMENSION_IDS = (
    "canonical-trust",
    "identity-freshness",
    "closed-vocabulary",
    "state-transition",
    "authorization-scope",
    "mutation-atomicity",
    "interruption-recovery",
    "concurrency-idempotency",
    "composition-bypass",
    "compatibility-migration",
    "outcome-stop",
    "evidence-claims",
)
APPLICABILITY_VALUES = ("applicable", "not-applicable")
EXAMPLE_ROLES = ("illustration", "regression", "discovery", "non-normative")
INTERACTION_RATIONALES = (
    "state-coupling",
    "trust-or-authority",
    "mutation-or-recovery",
    "compatibility-or-migration",
    "composed-path",
    "incident-evidence",
)
BOUNDARY_MODEL_VERSIONS = ("legacy", "v1")
AUTOMATION_LEVELS = ("automated", "manual", "hybrid")
RESULT_VALUES = ("pass", "fail", "not-run")
RUNTIME_PROJECTION_FIELDS = frozenset(
    {
        "projection_id",
        "runtime_version",
        "runtime_launcher_identity",
        "runtime_package_identity",
        "schema_bundle_identity",
        "protocol_item_classification_identity",
        "feature_classification_identity",
        "permitted_tool_features",
        "permitted_non_tool_features",
        "required_disabled_features",
        "file_change_capability_state",
    }
)
CODEX_0_145_0_FEATURES = (
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
    "code_mode_buffered_exec",
    "executor_capability_discovery",
    "external_agent_memory_import",
    "skill_search",
)
PERMITTED_PROJECTED_TOOL_FEATURES = (
    "shell_snapshot",
    "shell_tool",
    "unified_exec",
)
PERMITTED_PROJECTED_NON_TOOL_FEATURES = (
    "terminal_resize_reflow",
    "tool_search_always_defer_mcp_tools",
    "resize_all_images",
    "tui_app_server",
)
REQUIRED_DISABLED_PROJECTED_FEATURES = tuple(
    feature
    for feature in CODEX_0_145_0_FEATURES
    if feature
    not in (
        *PERMITTED_PROJECTED_TOOL_FEATURES,
        *PERMITTED_PROJECTED_NON_TOOL_FEATURES,
    )
)
RUNTIME_PROJECTIONS = (
    MappingProxyType(
        {
            "projection_id": "codex-0.145.0-readonly-boundary-v1",
            "runtime_version": "0.145.0",
            "runtime_launcher_identity": (
                "sha256:134063e133f0b4244fa3b251acf973d4f"
                "e4b4aeeacbdc135211bf480f59f1477"
            ),
            "runtime_package_identity": (
                "sha256:a66a2dee773de39b690a08048971ec18"
                "d04f97d8a8d5e9a205f51a9f0d4cdbfa"
            ),
            "schema_bundle_identity": (
                "sha256:18d79891673d9d43a8e7a49864fef49"
                "a04305bd13571a8aef45824209f1bfae8"
            ),
            "protocol_item_classification_identity": (
                "sha256:35f1203d9c6abc62ef3f1aca94e2f316"
                "5e0213697d554ab11d0477d9cd7e4bf8"
            ),
            "feature_classification_identity": (
                "sha256:6f833f4c43196e43f67fea215de09743"
                "e5a5e3a80bed53973b42740041369268"
            ),
            "permitted_tool_features": PERMITTED_PROJECTED_TOOL_FEATURES,
            "permitted_non_tool_features": (
                PERMITTED_PROJECTED_NON_TOOL_FEATURES
            ),
            "required_disabled_features": REQUIRED_DISABLED_PROJECTED_FEATURES,
            "file_change_capability_state": "not-exposed-projection",
        }
    ),
)
HANDLER_CONFORMANCE_CASES = (
    "matching-request-declined",
    "missing-handler-rejected",
    "wrong-policy-identity-rejected",
    "thread-mismatch-rejected",
    "turn-mismatch-rejected",
    "item-mismatch-rejected",
    "change-mismatch-rejected",
    "accept-rejected",
    "accept-for-session-rejected",
    "widened-response-rejected",
    "malformed-request-rejected",
)
EXPECTED_GATES = ("spec", "spec-review", "test-spec", "test-spec-review", "implement")
DETECTED_STAGES = (*EXPECTED_GATES, "not-detected")
EVALUATED_SKILLS = (
    "spec",
    "spec-review",
    "test-spec",
    "test-spec-review",
    "implement",
    "code-review",
    "verify",
    "workflow",
)
CHECK_IDS = (
    "boundary-workflow-contract",
    "boundary-skill-contract",
    "boundary-traceability",
    "boundary-incident-replay",
    "boundary-adapter-parity",
    "boundary-capability-baseline",
)
INCIDENT_RULES = {
    "BFP-FX-CANONICAL-001": (
        "caller assertion accepted instead of canonical evidence",
        "canonical_source",
        "caller-asserted",
        "owner-derived",
        "spec-review",
        "bfp-canonical-source-invalid",
    ),
    "BFP-FX-VOCAB-001": (
        "unknown closed-vocabulary value is not rejected",
        "vocabulary_state",
        "unknown",
        "known",
        "test-spec-review",
        "bfp-unknown-vocabulary",
    ),
    "BFP-FX-TRANSITION-001": (
        "illegal state transition is unmodeled",
        "transition_state",
        "illegal",
        "legal",
        "test-spec-review",
        "bfp-illegal-transition",
    ),
    "BFP-FX-IDENTITY-001": (
        "stale or substituted identity is accepted",
        "identity_state",
        "non-current",
        "current",
        "test-spec-review",
        "bfp-non-current-identity",
    ),
    "BFP-FX-ATOMICITY-001": (
        "partial durable write is unproved",
        "mutation_state",
        "partial",
        "complete",
        "test-spec-review",
        "bfp-partial-mutation",
    ),
    "BFP-FX-RECOVERY-001": (
        "retry repeats work instead of reconciling",
        "recovery_state",
        "repeated",
        "reconciled",
        "test-spec-review",
        "bfp-repeat-without-reconcile",
    ),
    "BFP-FX-COMPOSITION-001": (
        "helper proof omits the composed public path",
        "composition_state",
        "helper-only",
        "complete",
        "test-spec-review",
        "bfp-composed-path-omitted",
    ),
    "BFP-FX-SIBLING-001": (
        "reported bypass is fixed while a sibling bypass remains",
        "sibling_state",
        "one-only",
        "complete",
        "implement",
        "bfp-sibling-bypass-remains",
    ),
}
FIXTURE_GATES = {key: value[4] for key, value in INCIDENT_RULES.items()}
BOUNDARY_STATE_VALUES = {
    "canonical_source": ("owner-derived", "caller-asserted"),
    "vocabulary_state": ("known", "unknown"),
    "transition_state": ("legal", "illegal", "not-applicable"),
    "identity_state": ("current", "non-current"),
    "mutation_state": ("complete", "partial", "not-applicable"),
    "recovery_state": ("reconciled", "repeated", "not-applicable"),
    "composition_state": ("complete", "helper-only", "not-applicable"),
    "sibling_state": ("complete", "one-only", "not-applicable"),
}
BLOCKING_REASON_CODES = (
    "prerequisite-unsatisfied",
    "authorization-required",
    "environment-unavailable",
    "upstream-failure",
)
BOUNDARY_CHANGE_ROOT = (
    "docs/changes/"
    "2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills"
)
PRESERVATION_KEYS = (
    "behavior",
    "claim-boundary",
    "review-recording",
    "isolation",
    "handoff",
)
CAPABILITY_REPORT_SCHEMA = "boundary-capability-baseline-v1"

STABLE_ID_RE = re.compile(r"^[a-z][a-z0-9-]*(?:\.[a-z][a-z0-9-]*)+$")
EXTENSION_ID_RE = re.compile(r"^x\.[a-z][a-z0-9-]*(?:\.[a-z][a-z0-9-]*)+$")
TEST_ID_RE = re.compile(r"^T[1-9][0-9]*$")
SCOPE_RE = re.compile(r"^(?:whole-spec|[A-Za-z][A-Za-z0-9]*-[A-Za-z][A-Za-z0-9]*)$")

CORE_FIELDS = frozenset(
    {
        "dimension_id",
        "applicability",
        "governing_requirement_ids",
        "boundary_ids",
        "non_applicability_rationale",
    }
)
EXTENSION_FIELDS = frozenset(
    {
        "extension_id",
        "title",
        "applicability",
        "rationale",
        "governing_requirement_ids",
        "boundary_ids",
        "non_applicability_rationale",
    }
)
EXAMPLE_FIELDS = frozenset(
    {
        "example_id",
        "role",
        "governing_requirement_ids",
        "boundary_ids",
        "regression_id",
        "discovery_gap",
        "non_normative_purpose",
    }
)
INTERACTION_FIELDS = frozenset(
    {
        "interaction_id",
        "boundary_ids",
        "rationale",
        "governing_requirement_ids",
    }
)
PROOF_FIELDS = frozenset(
    {
        "proof_obligation_id",
        "governing_requirement_ids",
        "boundary_or_interaction_ids",
        "test_case_ids",
        "automation_level",
        "manual_procedure_ids",
    }
)
REPORT_FIELDS = frozenset(
    {
        "schema_version",
        "boundary_model_version",
        "evaluated_skills",
        "required_check_ids",
        "checks",
        "fixtures",
        "preservation_results",
        "adapter_parity",
        "false_blocking_count",
        "duplicate_normative_owner_count",
        "new_universal_artifact_count",
        "simple_fixture_structure_correction_cycles",
        "overall_result",
    }
)


class BoundaryProofError(ValueError):
    """Raised when deterministic boundary-proof validation fails."""


def _canonical_identity(value: object) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def runtime_projection_identity(projection: Mapping[str, object]) -> str:
    """Return the identity of one complete, non-self-referential row."""

    if set(projection) != RUNTIME_PROJECTION_FIELDS:
        raise BoundaryProofError("runtime projection fields are not closed")
    return _canonical_identity(dict(projection))


def _validate_runtime_projection_registry() -> None:
    projection_ids: set[str] = set()
    selection_keys: set[tuple[object, ...]] = set()
    identities: set[str] = set()
    identity_pattern = re.compile(r"^sha256:[0-9a-f]{64}$")
    projection_pattern = re.compile(
        r"^codex-[0-9]+\.[0-9]+\.[0-9]+-[a-z0-9-]+-v[0-9]+$"
    )
    for projection in RUNTIME_PROJECTIONS:
        if set(projection) != RUNTIME_PROJECTION_FIELDS:
            raise BoundaryProofError("runtime projection fields are not closed")
        projection_id = projection["projection_id"]
        if (
            not isinstance(projection_id, str)
            or projection_pattern.fullmatch(projection_id) is None
            or projection_id in projection_ids
        ):
            raise BoundaryProofError("runtime projection id is invalid")
        projection_ids.add(projection_id)
        for field in (
            "runtime_launcher_identity",
            "runtime_package_identity",
            "schema_bundle_identity",
            "protocol_item_classification_identity",
            "feature_classification_identity",
        ):
            if (
                not isinstance(projection[field], str)
                or identity_pattern.fullmatch(projection[field]) is None
            ):
                raise BoundaryProofError(
                    f"runtime projection {field} is invalid"
                )
        permitted = projection["permitted_tool_features"]
        non_tool = projection["permitted_non_tool_features"]
        disabled = projection["required_disabled_features"]
        if (
            not isinstance(permitted, tuple)
            or not isinstance(non_tool, tuple)
            or not isinstance(disabled, tuple)
            or not permitted
            or len(permitted) != len(set(permitted))
            or len(non_tool) != len(set(non_tool))
            or len(disabled) != len(set(disabled))
            or set(permitted) & set(non_tool)
            or set(permitted) & set(disabled)
            or set(non_tool) & set(disabled)
            or set(permitted) | set(non_tool) | set(disabled)
            != set(CODEX_0_145_0_FEATURES)
            or permitted != PERMITTED_PROJECTED_TOOL_FEATURES
            or non_tool != PERMITTED_PROJECTED_NON_TOOL_FEATURES
            or disabled != REQUIRED_DISABLED_PROJECTED_FEATURES
        ):
            raise BoundaryProofError(
                "runtime projection feature partition is invalid"
            )
        if projection["file_change_capability_state"] not in (
            "exposed-live-probe-required",
            "not-exposed-projection",
        ):
            raise BoundaryProofError(
                "runtime projection capability state is unknown"
            )
        selection_key = tuple(
            projection[field]
            for field in (
                "runtime_version",
                "runtime_launcher_identity",
                "runtime_package_identity",
                "schema_bundle_identity",
                "protocol_item_classification_identity",
                "feature_classification_identity",
            )
        )
        if selection_key in selection_keys:
            raise BoundaryProofError("runtime projection selection is ambiguous")
        selection_keys.add(selection_key)
        identity = runtime_projection_identity(projection)
        if identity in identities:
            raise BoundaryProofError("runtime projection identity is duplicated")
        identities.add(identity)


def select_runtime_projection(
    *,
    runtime_version: str,
    runtime_launcher_identity: str,
    runtime_package_identity: str,
    schema_bundle_identity: str,
    protocol_item_classification_identity: str,
    feature_classification_identity: str,
) -> dict[str, object]:
    """Select exactly one immutable row using the complete implementation key."""

    _validate_runtime_projection_registry()
    observed = (
        runtime_version,
        runtime_launcher_identity,
        runtime_package_identity,
        schema_bundle_identity,
        protocol_item_classification_identity,
        feature_classification_identity,
    )
    matches = [
        projection
        for projection in RUNTIME_PROJECTIONS
        if observed
        == tuple(
            projection[field]
            for field in (
                "runtime_version",
                "runtime_launcher_identity",
                "runtime_package_identity",
                "schema_bundle_identity",
                "protocol_item_classification_identity",
                "feature_classification_identity",
            )
        )
    ]
    if len(matches) != 1:
        raise BoundaryProofError("runtime projection is unsupported")
    return dict(matches[0])


def handler_conformance_policy(
    authorization_policy_identity: str,
) -> dict[str, object]:
    if re.fullmatch(r"sha256:[0-9a-f]{64}", authorization_policy_identity) is None:
        raise BoundaryProofError("authorization policy identity is invalid")
    return {
        "schema_version": "stage-file-change-handler-conformance-v1",
        "authorization_policy_identity": authorization_policy_identity,
        "cases": list(HANDLER_CONFORMANCE_CASES),
    }


def validate_handler_conformance(
    policy: Mapping[str, object],
    result: Mapping[str, object],
    *,
    authorization_policy_identity: str,
) -> str:
    """Validate the complete ordered conformance result and its identities."""

    expected_policy = handler_conformance_policy(authorization_policy_identity)
    if dict(policy) != expected_policy:
        raise BoundaryProofError("handler conformance policy is invalid")
    policy_identity = _canonical_identity(expected_policy)
    if set(result) != {
        "schema_version",
        "policy_identity",
        "case_results",
        "result",
        "result_identity",
    }:
        raise BoundaryProofError("handler conformance result fields are not closed")
    if (
        result.get("schema_version")
        != "stage-file-change-handler-conformance-result-v1"
        or result.get("policy_identity") != policy_identity
        or result.get("result") != "pass"
    ):
        raise BoundaryProofError("handler conformance result is invalid")
    case_results = result.get("case_results")
    if not isinstance(case_results, list) or case_results != [
        {"case": case, "result": "pass"}
        for case in HANDLER_CONFORMANCE_CASES
    ]:
        raise BoundaryProofError("handler conformance cases are invalid")
    without_identity = {
        key: value for key, value in result.items() if key != "result_identity"
    }
    expected_identity = _canonical_identity(without_identity)
    if result.get("result_identity") != expected_identity:
        raise BoundaryProofError("handler conformance identity is invalid")
    return expected_identity


_validate_runtime_projection_registry()


@dataclass(frozen=True)
class CoreBoundaryEntry:
    dimension_id: str
    applicability: str
    governing_requirement_ids: tuple[str, ...]
    boundary_ids: tuple[str, ...]
    non_applicability_rationale: str | None


@dataclass(frozen=True)
class BoundaryExtension:
    extension_id: str
    title: str
    applicability: str
    rationale: str
    governing_requirement_ids: tuple[str, ...]
    boundary_ids: tuple[str, ...]
    non_applicability_rationale: str | None


@dataclass(frozen=True)
class BoundaryExample:
    example_id: str
    role: str
    governing_requirement_ids: tuple[str, ...]
    boundary_ids: tuple[str, ...]
    regression_id: str | None
    discovery_gap: str | None
    non_normative_purpose: str | None


@dataclass(frozen=True)
class BoundaryInteraction:
    interaction_id: str
    boundary_ids: tuple[str, ...]
    rationale: str
    governing_requirement_ids: tuple[str, ...]


@dataclass(frozen=True)
class FeatureBoundaryModel:
    boundary_model_version: str
    boundary_model_scope: str
    core_dimensions: tuple[CoreBoundaryEntry, ...]
    extensions: tuple[BoundaryExtension, ...]
    examples: tuple[BoundaryExample, ...]
    interactions: tuple[BoundaryInteraction, ...]


@dataclass(frozen=True)
class ProofObligation:
    proof_obligation_id: str
    governing_requirement_ids: tuple[str, ...]
    boundary_or_interaction_ids: tuple[str, ...]
    test_case_ids: tuple[str, ...]
    automation_level: str
    manual_procedure_ids: tuple[str, ...]


@dataclass(frozen=True)
class BoundaryProofMap:
    boundary_model_version: str
    boundary_model_scope: str
    proof_obligations: tuple[ProofObligation, ...]


@dataclass(frozen=True)
class FeatureInvariantProjection:
    """Closed candidate/produced comparison surface for one feature model."""

    boundary_model_version: str
    boundary_model_scope: str
    requirement_ids: tuple[str, ...]
    core_dimension_ids: tuple[str, ...]


@dataclass(frozen=True)
class ProofInvariantProjection:
    """Closed candidate/produced comparison surface for one proof map."""

    boundary_model_version: str
    boundary_model_scope: str
    governing_requirement_ids: tuple[str, ...]


@dataclass(frozen=True)
class StageGateResult:
    detected_stage: str
    diagnostic_id: str
    escaped_to_code_review: bool
    sibling_bypass_remaining: bool


@dataclass(frozen=True)
class SimpleTraceMetrics:
    false_blocking_count: int
    new_universal_artifact_count: int
    structure_only_correction_cycles: int
    applicable_only_mapping: bool


def _object(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise BoundaryProofError(f"{label}: expected object")
    return value


def _records(value: Any, label: str) -> list[Mapping[str, Any]]:
    if not isinstance(value, list):
        raise BoundaryProofError(f"{label}: expected list")
    return [_object(item, f"{label}[{index}]") for index, item in enumerate(value)]


def _exact_fields(record: Mapping[str, Any], expected: frozenset[str], label: str) -> None:
    actual = set(record)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        raise BoundaryProofError(f"{label}: missing fields: {', '.join(missing)}")
    if extra:
        raise BoundaryProofError(f"{label}: unexpected fields: {', '.join(extra)}")


def _nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BoundaryProofError(f"{label}: expected non-empty string")
    return value


def _optional_string(value: Any, label: str) -> str | None:
    if value is None:
        return None
    return _nonempty_string(value, label)


def _strings(
    value: Any,
    label: str,
    *,
    nonempty: bool,
    stable_ids: bool = False,
    test_ids: bool = False,
) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise BoundaryProofError(f"{label}: expected list")
    if nonempty and not value:
        raise BoundaryProofError(f"{label}: expected one or more values")
    result: list[str] = []
    for index, item in enumerate(value):
        item = _nonempty_string(item, f"{label}[{index}]")
        if stable_ids and not STABLE_ID_RE.fullmatch(item):
            raise BoundaryProofError(f"{label}[{index}]: invalid stable ID")
        if test_ids and not (TEST_ID_RE.fullmatch(item) or STABLE_ID_RE.fullmatch(item)):
            raise BoundaryProofError(f"{label}[{index}]: invalid test-case ID")
        result.append(item)
    if len(result) != len(set(result)):
        raise BoundaryProofError(f"{label}: duplicate values")
    return tuple(result)


def _unknown_vocabulary_checks(model: Mapping[str, Any]) -> None:
    version = model.get("boundary_model_version")
    if version not in BOUNDARY_MODEL_VERSIONS:
        raise BoundaryProofError(f"unknown boundary-model version: {version!r}")
    for index, row in enumerate(_records(model.get("core_dimensions"), "core_dimensions")):
        dimension_id = row.get("dimension_id")
        if dimension_id not in CORE_DIMENSION_IDS:
            raise BoundaryProofError(
                f"core_dimensions[{index}]: unknown core dimension: {dimension_id!r}"
            )
        applicability = row.get("applicability")
        if applicability not in APPLICABILITY_VALUES:
            raise BoundaryProofError(
                f"core_dimensions[{index}]: unknown applicability: {applicability!r}"
            )
    for index, row in enumerate(_records(model.get("extensions", []), "extensions")):
        applicability = row.get("applicability")
        if applicability not in APPLICABILITY_VALUES:
            raise BoundaryProofError(
                f"extensions[{index}]: unknown applicability: {applicability!r}"
            )
    for index, row in enumerate(_records(model.get("examples", []), "examples")):
        role = row.get("role")
        if role not in EXAMPLE_ROLES:
            raise BoundaryProofError(
                f"examples[{index}]: unknown example role: {role!r}"
            )
    for index, row in enumerate(_records(model.get("interactions", []), "interactions")):
        rationale = row.get("rationale")
        if rationale not in INTERACTION_RATIONALES:
            raise BoundaryProofError(
                f"interactions[{index}]: unknown interaction rationale: {rationale!r}"
            )


def _applicability_values(
    row: Mapping[str, Any],
    label: str,
) -> tuple[tuple[str, ...], tuple[str, ...], str | None]:
    applicability = row["applicability"]
    requirements = _strings(
        row["governing_requirement_ids"],
        f"{label}.governing_requirement_ids",
        nonempty=applicability == "applicable",
    )
    boundaries = _strings(
        row["boundary_ids"],
        f"{label}.boundary_ids",
        nonempty=applicability == "applicable",
        stable_ids=True,
    )
    rationale = _optional_string(
        row["non_applicability_rationale"],
        f"{label}.non_applicability_rationale",
    )
    if applicability == "applicable":
        if rationale is not None:
            raise BoundaryProofError(
                f"{label}: applicable entry cannot have non-applicability rationale"
            )
    elif requirements or boundaries or rationale is None:
        raise BoundaryProofError(
            f"{label}: not-applicable entry requires rationale and no proof links"
        )
    return requirements, boundaries, rationale


def normalize_feature_model(payload: Mapping[str, Any]) -> FeatureBoundaryModel:
    """Validate and freeze one structured feature boundary model."""

    model = _object(payload, "feature_model")
    expected_top = {
        "boundary_model_version",
        "boundary_model_scope",
        "core_dimensions",
        "extensions",
        "examples",
        "interactions",
    }
    _exact_fields(model, frozenset(expected_top), "feature_model")
    _unknown_vocabulary_checks(model)
    version = _nonempty_string(model["boundary_model_version"], "boundary_model_version")
    scope = _nonempty_string(model["boundary_model_scope"], "boundary_model_scope")
    if not SCOPE_RE.fullmatch(scope):
        raise BoundaryProofError("boundary_model_scope: invalid closed scope")

    core: list[CoreBoundaryEntry] = []
    for index, row in enumerate(_records(model["core_dimensions"], "core_dimensions")):
        label = f"core_dimensions[{index}]"
        _exact_fields(row, CORE_FIELDS, label)
        requirements, boundaries, rationale = _applicability_values(row, label)
        core.append(
            CoreBoundaryEntry(
                row["dimension_id"],
                row["applicability"],
                requirements,
                boundaries,
                rationale,
            )
        )
    core_ids = [row.dimension_id for row in core]
    if len(core_ids) != len(set(core_ids)):
        raise BoundaryProofError("duplicate core dimension")
    missing = sorted(set(CORE_DIMENSION_IDS) - set(core_ids))
    if missing:
        raise BoundaryProofError("missing core dimensions: " + ", ".join(missing))

    extensions: list[BoundaryExtension] = []
    extension_ids: set[str] = set()
    for index, row in enumerate(_records(model["extensions"], "extensions")):
        label = f"extensions[{index}]"
        _exact_fields(row, EXTENSION_FIELDS, label)
        extension_id = _nonempty_string(row["extension_id"], f"{label}.extension_id")
        if extension_id == "other" or not EXTENSION_ID_RE.fullmatch(extension_id):
            raise BoundaryProofError(f"{label}: invalid extension ID")
        if extension_id in extension_ids:
            raise BoundaryProofError(f"{label}: duplicate extension ID")
        extension_ids.add(extension_id)
        requirements, boundaries, rationale = _applicability_values(row, label)
        extensions.append(
            BoundaryExtension(
                extension_id,
                _nonempty_string(row["title"], f"{label}.title"),
                row["applicability"],
                _nonempty_string(row["rationale"], f"{label}.rationale"),
                requirements,
                boundaries,
                rationale,
            )
        )

    all_boundary_ids = {
        boundary_id for entry in (*core, *extensions) for boundary_id in entry.boundary_ids
    }
    if len(all_boundary_ids) != sum(
        len(entry.boundary_ids) for entry in (*core, *extensions)
    ):
        raise BoundaryProofError("duplicate boundary ID")

    examples: list[BoundaryExample] = []
    example_ids: set[str] = set()
    regression_ids: set[str] = set()
    discovery_gap_ids: set[str] = set()
    boundary_requirements = {
        boundary_id: frozenset(entry.governing_requirement_ids)
        for entry in (*core, *extensions)
        for boundary_id in entry.boundary_ids
    }
    for index, row in enumerate(_records(model["examples"], "examples")):
        label = f"examples[{index}]"
        _exact_fields(row, EXAMPLE_FIELDS, label)
        example_id = _nonempty_string(row["example_id"], f"{label}.example_id")
        if not STABLE_ID_RE.fullmatch(example_id):
            raise BoundaryProofError(f"{label}: invalid example ID")
        if example_id in example_ids:
            raise BoundaryProofError(f"{label}: duplicate example ID")
        example_ids.add(example_id)
        requirements = _strings(
            row["governing_requirement_ids"],
            f"{label}.governing_requirement_ids",
            nonempty=False,
        )
        boundaries = _strings(
            row["boundary_ids"],
            f"{label}.boundary_ids",
            nonempty=False,
            stable_ids=True,
        )
        orphan = sorted(set(boundaries) - all_boundary_ids)
        if orphan:
            raise BoundaryProofError(f"{label}: orphan boundary: {orphan[0]}")
        regression_id = _optional_string(row["regression_id"], f"{label}.regression_id")
        discovery_gap = _optional_string(row["discovery_gap"], f"{label}.discovery_gap")
        purpose = _optional_string(
            row["non_normative_purpose"], f"{label}.non_normative_purpose"
        )
        role = row["role"]
        if regression_id is not None:
            if not STABLE_ID_RE.fullmatch(regression_id):
                raise BoundaryProofError(f"{label}: invalid regression ID")
            if regression_id in regression_ids:
                raise BoundaryProofError(f"{label}: duplicate regression ID")
            regression_ids.add(regression_id)
        if discovery_gap is not None:
            if not STABLE_ID_RE.fullmatch(discovery_gap):
                raise BoundaryProofError(f"{label}: invalid discovery gap ID")
            if discovery_gap in discovery_gap_ids:
                raise BoundaryProofError(f"{label}: duplicate discovery gap ID")
            discovery_gap_ids.add(discovery_gap)
        if boundaries:
            owned_requirements = set().union(
                *(boundary_requirements[boundary_id] for boundary_id in boundaries)
            )
            if not set(requirements) <= owned_requirements:
                raise BoundaryProofError(
                    f"{label}: governing requirement does not own cited boundary"
                )
            for boundary_id in boundaries:
                if not set(requirements) & boundary_requirements[boundary_id]:
                    raise BoundaryProofError(
                        f"{label}: cited boundary lacks governing requirement overlap"
                    )
        if role == "illustration":
            if not requirements or not boundaries or any(
                value is not None for value in (regression_id, discovery_gap, purpose)
            ):
                raise BoundaryProofError(f"{label}: invalid illustration links")
        elif role == "regression":
            if not requirements or not boundaries or regression_id is None:
                raise BoundaryProofError(f"{label}: regression ID is required")
            if discovery_gap is not None or purpose is not None:
                raise BoundaryProofError(f"{label}: invalid regression links")
        elif role == "discovery":
            if requirements or boundaries or regression_id is not None or discovery_gap is None:
                raise BoundaryProofError(f"{label}: discovery gap is required")
        elif requirements or boundaries or regression_id is not None or discovery_gap is not None or purpose is None:
            raise BoundaryProofError(f"{label}: non-normative purpose is required")
        examples.append(
            BoundaryExample(
                example_id,
                role,
                requirements,
                boundaries,
                regression_id,
                discovery_gap,
                purpose,
            )
        )

    interactions: list[BoundaryInteraction] = []
    interaction_ids: set[str] = set()
    for index, row in enumerate(_records(model["interactions"], "interactions")):
        label = f"interactions[{index}]"
        _exact_fields(row, INTERACTION_FIELDS, label)
        interaction_id = _nonempty_string(
            row["interaction_id"], f"{label}.interaction_id"
        )
        if not STABLE_ID_RE.fullmatch(interaction_id):
            raise BoundaryProofError(f"{label}: invalid interaction ID")
        if interaction_id in interaction_ids:
            raise BoundaryProofError(f"{label}: duplicate interaction ID")
        interaction_ids.add(interaction_id)
        boundaries = _strings(
            row["boundary_ids"],
            f"{label}.boundary_ids",
            nonempty=True,
            stable_ids=True,
        )
        if len(boundaries) < 2:
            raise BoundaryProofError(f"{label}: at least two boundary IDs are required")
        orphan = sorted(set(boundaries) - all_boundary_ids)
        if orphan:
            raise BoundaryProofError(f"{label}: orphan boundary: {orphan[0]}")
        requirements = _strings(
            row["governing_requirement_ids"],
            f"{label}.governing_requirement_ids",
            nonempty=True,
        )
        interactions.append(
            BoundaryInteraction(
                interaction_id,
                boundaries,
                row["rationale"],
                requirements,
            )
        )

    return FeatureBoundaryModel(
        version,
        scope,
        tuple(core),
        tuple(extensions),
        tuple(examples),
        tuple(interactions),
    )


def normalize_proof_map(
    payload: Mapping[str, Any],
    feature: FeatureBoundaryModel,
) -> BoundaryProofMap:
    """Validate one proof map against an already-normalized feature model."""

    record = _object(payload, "proof_map")
    _exact_fields(
        record,
        frozenset(
            {
                "boundary_model_version",
                "boundary_model_scope",
                "proof_obligations",
            }
        ),
        "proof_map",
    )
    version = record["boundary_model_version"]
    if version not in BOUNDARY_MODEL_VERSIONS:
        raise BoundaryProofError(f"unknown boundary-model version: {version!r}")
    if version != feature.boundary_model_version:
        raise BoundaryProofError("boundary-model version mismatch")
    scope = _nonempty_string(record["boundary_model_scope"], "proof_map scope")
    if scope != feature.boundary_model_scope:
        raise BoundaryProofError("boundary-model scope mismatch")
    rows = _records(record["proof_obligations"], "proof_obligations")
    for index, row in enumerate(rows):
        level = row.get("automation_level")
        if level not in AUTOMATION_LEVELS:
            raise BoundaryProofError(
                f"proof_obligations[{index}]: unknown automation level: {level!r}"
            )

    boundary_ids = {
        boundary_id
        for entry in (*feature.core_dimensions, *feature.extensions)
        if entry.applicability == "applicable"
        for boundary_id in entry.boundary_ids
    }
    interaction_ids = {entry.interaction_id for entry in feature.interactions}
    known_ids = boundary_ids | interaction_ids
    known_requirements = {
        requirement
        for entry in (*feature.core_dimensions, *feature.extensions)
        for requirement in entry.governing_requirement_ids
    } | {
        requirement
        for entry in feature.interactions
        for requirement in entry.governing_requirement_ids
    }
    reference_requirements = {
        boundary_id: frozenset(entry.governing_requirement_ids)
        for entry in (*feature.core_dimensions, *feature.extensions)
        if entry.applicability == "applicable"
        for boundary_id in entry.boundary_ids
    }
    reference_requirements.update(
        {
            entry.interaction_id: frozenset(entry.governing_requirement_ids)
            for entry in feature.interactions
        }
    )
    normalized: list[ProofObligation] = []
    proof_ids: set[str] = set()
    mapped_ids: set[str] = set()
    for index, row in enumerate(rows):
        label = f"proof_obligations[{index}]"
        _exact_fields(row, PROOF_FIELDS, label)
        proof_id = _nonempty_string(
            row["proof_obligation_id"], f"{label}.proof_obligation_id"
        )
        if not STABLE_ID_RE.fullmatch(proof_id):
            raise BoundaryProofError(f"{label}: invalid proof obligation ID")
        if proof_id in proof_ids:
            raise BoundaryProofError(f"{label}: duplicate proof obligation ID")
        proof_ids.add(proof_id)
        requirements = _strings(
            row["governing_requirement_ids"],
            f"{label}.governing_requirement_ids",
            nonempty=True,
        )
        unknown_requirements = sorted(set(requirements) - known_requirements)
        if unknown_requirements:
            raise BoundaryProofError(
                f"{label}: unapproved governing requirement: "
                + unknown_requirements[0]
            )
        references = _strings(
            row["boundary_or_interaction_ids"],
            f"{label}.boundary_or_interaction_ids",
            nonempty=True,
            stable_ids=True,
        )
        orphan = sorted(set(references) - known_ids)
        if orphan:
            raise BoundaryProofError(f"{label}: orphan boundary or interaction: {orphan[0]}")
        owned_requirements = set().union(
            *(reference_requirements[reference] for reference in references)
        )
        unrelated = sorted(set(requirements) - owned_requirements)
        if unrelated:
            raise BoundaryProofError(
                f"{label}: governing requirement does not own cited reference: "
                + unrelated[0]
            )
        for reference in references:
            if not set(requirements) & reference_requirements[reference]:
                raise BoundaryProofError(
                    f"{label}: cited reference lacks governing requirement overlap: "
                    + reference
                )
        tests = _strings(
            row["test_case_ids"],
            f"{label}.test_case_ids",
            nonempty=True,
            test_ids=True,
        )
        manuals = _strings(
            row["manual_procedure_ids"],
            f"{label}.manual_procedure_ids",
            nonempty=False,
            stable_ids=True,
        )
        level = row["automation_level"]
        if level == "automated" and manuals:
            raise BoundaryProofError(f"{label}: automated proof cannot cite manual procedure")
        if level in {"manual", "hybrid"} and not manuals:
            raise BoundaryProofError(f"{label}: manual procedure is required")
        mapped_ids.update(references)
        normalized.append(
            ProofObligation(
                proof_id,
                requirements,
                references,
                tests,
                level,
                manuals,
            )
        )
    missing = sorted(known_ids - mapped_ids)
    if missing:
        raise BoundaryProofError("unmapped boundary or interaction: " + ", ".join(missing))
    return BoundaryProofMap(version, scope, tuple(normalized))


def feature_invariant_projection(
    model: FeatureBoundaryModel,
) -> FeatureInvariantProjection:
    """Project only the closed, stage-independent feature invariants."""

    requirement_ids = {
        requirement_id
        for row in (*model.core_dimensions, *model.extensions, *model.interactions)
        for requirement_id in row.governing_requirement_ids
    }
    return FeatureInvariantProjection(
        boundary_model_version=model.boundary_model_version,
        boundary_model_scope=model.boundary_model_scope,
        requirement_ids=tuple(sorted(requirement_ids)),
        core_dimension_ids=tuple(
            sorted(row.dimension_id for row in model.core_dimensions)
        ),
    )


def proof_invariant_projection(
    proof: BoundaryProofMap,
) -> ProofInvariantProjection:
    """Project only the closed, stage-independent proof-map invariants."""

    return ProofInvariantProjection(
        boundary_model_version=proof.boundary_model_version,
        boundary_model_scope=proof.boundary_model_scope,
        governing_requirement_ids=tuple(
            sorted(
                {
                    requirement_id
                    for row in proof.proof_obligations
                    for requirement_id in row.governing_requirement_ids
                }
            )
        ),
    )


def boundary_invariant_projections_match(
    candidate_feature: FeatureBoundaryModel,
    produced_feature: FeatureBoundaryModel,
    candidate_proof: BoundaryProofMap,
    produced_proof: BoundaryProofMap,
) -> bool:
    """Compare candidates and stage outputs without comparing modeling choices."""

    return (
        feature_invariant_projection(candidate_feature)
        == feature_invariant_projection(produced_feature)
        and proof_invariant_projection(candidate_proof)
        == proof_invariant_projection(produced_proof)
    )


def evaluate_boundary_state(payload: Mapping[str, Any]) -> StageGateResult:
    """Derive a gate result only from one closed boundary-state envelope."""

    state = _object(payload, "boundary_state")
    _exact_fields(state, frozenset(BOUNDARY_STATE_VALUES), "boundary_state")
    for field, allowed in BOUNDARY_STATE_VALUES.items():
        if state[field] not in allowed:
            raise BoundaryProofError(
                f"boundary_state.{field}: unknown closed value: {state[field]!r}"
            )
    matches = [
        rule
        for rule in INCIDENT_RULES.values()
        if state[rule[1]] == rule[2]
    ]
    if not matches:
        return StageGateResult("not-detected", "none", False, False)
    if len(matches) != 1:
        raise BoundaryProofError("boundary_state: multiple seeded triggers")
    rule = matches[0]
    return StageGateResult(
        detected_stage=rule[4],
        diagnostic_id=rule[5],
        escaped_to_code_review=False,
        sibling_bypass_remaining=False,
    )


def validate_incident_fixture(payload: Mapping[str, Any]) -> StageGateResult:
    """Validate one incident fixture and replay it through the shared evaluator."""

    record = _object(payload, "incident_fixture")
    _exact_fields(
        record,
        frozenset(
            {
                "fixture_id",
                "seeded_omission",
                "expected_gate",
                "expected_diagnostic",
                "boundary_state",
                "valid_contrast_state",
            }
        ),
        "incident_fixture",
    )
    fixture_id = record["fixture_id"]
    if fixture_id not in INCIDENT_RULES:
        raise BoundaryProofError(f"incident_fixture: unknown fixture: {fixture_id!r}")
    omission, trigger_field, trigger_value, contrast_value, gate, diagnostic = (
        INCIDENT_RULES[fixture_id]
    )
    expected = (omission, gate, diagnostic)
    actual = (
        record["seeded_omission"],
        record["expected_gate"],
        record["expected_diagnostic"],
    )
    if actual != expected:
        raise BoundaryProofError("incident_fixture: closed registry mismatch")
    state = _object(record["boundary_state"], "boundary_state")
    contrast = _object(record["valid_contrast_state"], "valid_contrast_state")
    result = evaluate_boundary_state(state)
    if (
        state.get(trigger_field) != trigger_value
        or contrast.get(trigger_field) != contrast_value
    ):
        raise BoundaryProofError("incident_fixture: trigger/contrast mismatch")
    changed = [field for field in BOUNDARY_STATE_VALUES if state.get(field) != contrast.get(field)]
    if changed != [trigger_field]:
        raise BoundaryProofError("incident_fixture: contrast must change exactly the trigger")
    contrast_result = evaluate_boundary_state(contrast)
    if contrast_result.diagnostic_id != "none":
        raise BoundaryProofError("incident_fixture: valid contrast contains a trigger")
    if result.detected_stage != gate or result.diagnostic_id != diagnostic:
        raise BoundaryProofError("incident_fixture: derived result mismatch")
    return result


def validate_incident_registry(
    payload: Mapping[str, Any],
    *,
    repository_root: Path | None = None,
) -> tuple[StageGateResult, ...]:
    """Validate the exact registry and all eight executable incident fixtures."""

    record = _object(payload, "incident_registry")
    _exact_fields(record, frozenset({"fixtures"}), "incident_registry")
    rows = _records(record["fixtures"], "fixtures")
    if len(rows) != len(INCIDENT_RULES):
        raise BoundaryProofError("incident_registry: expected every exact fixture")
    root = repository_root or Path(__file__).resolve().parents[1]
    results: list[StageGateResult] = []
    seen: set[str] = set()
    for index, row in enumerate(rows):
        label = f"fixtures[{index}]"
        _exact_fields(row, frozenset({"fixture_id", "path"}), label)
        fixture_id = row["fixture_id"]
        if fixture_id not in INCIDENT_RULES:
            raise BoundaryProofError(f"{label}: unknown fixture: {fixture_id!r}")
        if fixture_id in seen:
            raise BoundaryProofError(f"{label}: duplicate fixture")
        seen.add(fixture_id)
        expected_path = (
            f"tests/fixtures/boundary-proof/incidents/{fixture_id}.json"
        )
        if row["path"] != expected_path:
            raise BoundaryProofError(f"{label}: fixture path mismatch")
        path = root / expected_path
        if not path.is_file() or path.is_symlink():
            raise BoundaryProofError(f"{label}: fixture file is missing or unsafe")
        results.append(validate_incident_fixture(json.loads(path.read_text())))
    return tuple(results)


def _evidence_ref(value: Any, label: str, repository_root: Path) -> None:
    record = _object(value, label)
    _exact_fields(record, frozenset({"path", "identity"}), label)
    raw_path = _nonempty_string(record["path"], f"{label}.path")
    path = Path(raw_path)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != raw_path:
        raise BoundaryProofError(f"{label}: unsafe evidence path")
    candidate = repository_root / path
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(repository_root.resolve(strict=True))
    except (OSError, ValueError):
        raise BoundaryProofError(f"{label}: missing or out-of-repository evidence")
    current = repository_root
    traverses_symlink = False
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            traverses_symlink = True
            break
    if not resolved.is_file() or traverses_symlink:
        raise BoundaryProofError(f"{label}: evidence must be a non-symlink regular file")
    is_change_local = path.as_posix().startswith(BOUNDARY_CHANGE_ROOT + "/")
    try:
        tracked = subprocess.run(
            [
                "git",
                "-C",
                str(repository_root),
                "ls-files",
                "--error-unmatch",
                "--",
                raw_path,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode == 0
    except OSError:
        tracked = False
    if not tracked and not is_change_local:
        raise BoundaryProofError(
            f"{label}: evidence must be tracked or current change-local"
        )
    identity = _nonempty_string(record["identity"], f"{label}.identity")
    expected = "sha256:" + hashlib.sha256(resolved.read_bytes()).hexdigest()
    if identity != expected:
        raise BoundaryProofError(f"{label}: stale or substituted evidence identity")


def _blocking_reason(value: Any, label: str) -> None:
    record = _object(value, label)
    _exact_fields(record, frozenset({"code", "detail"}), label)
    if record["code"] not in BLOCKING_REASON_CODES:
        raise BoundaryProofError(f"{label}: unknown blocking reason code")
    _nonempty_string(record["detail"], f"{label}.detail")


def _result_record(
    value: Any,
    label: str,
    repository_root: Path,
) -> str:
    record = _object(value, label)
    _exact_fields(
        record,
        frozenset({"result", "evidence_refs", "blocking_reason"}),
        label,
    )
    result = record["result"]
    if result not in RESULT_VALUES:
        raise BoundaryProofError(f"{label}: unknown result: {result!r}")
    evidence = record["evidence_refs"]
    if not isinstance(evidence, list):
        raise BoundaryProofError(f"{label}.evidence_refs: expected list")
    if result == "not-run":
        if evidence:
            raise BoundaryProofError(f"{label}: not-run cannot cite evidence")
        _blocking_reason(record["blocking_reason"], f"{label}.blocking_reason")
    else:
        if not evidence:
            raise BoundaryProofError(f"{label}.evidence_refs: expected one or more values")
        if record["blocking_reason"] is not None:
            raise BoundaryProofError(f"{label}: executed result cannot have blocking reason")
        for index, reference in enumerate(evidence):
            _evidence_ref(
                reference,
                f"{label}.evidence_refs[{index}]",
                repository_root,
            )
    return result


def _validate_report_shape(
    report: Mapping[str, Any],
    repository_root: Path | None = None,
) -> None:
    root = repository_root or Path(__file__).resolve().parents[1]
    _exact_fields(report, REPORT_FIELDS, "capability_report")
    if report["schema_version"] != CAPABILITY_REPORT_SCHEMA:
        raise BoundaryProofError("unknown capability report schema version")
    if report["boundary_model_version"] not in BOUNDARY_MODEL_VERSIONS:
        raise BoundaryProofError("unknown boundary-model version")
    if report["boundary_model_version"] != "v1":
        raise BoundaryProofError("capability report requires boundary model v1")
    if not isinstance(report["evaluated_skills"], list):
        raise BoundaryProofError("evaluated_skills: expected list")
    if tuple(report["evaluated_skills"]) != EVALUATED_SKILLS:
        raise BoundaryProofError("evaluated_skills must contain the exact eight skills")
    if not isinstance(report["required_check_ids"], list):
        raise BoundaryProofError("required_check_ids: expected list")
    if tuple(report["required_check_ids"]) != CHECK_IDS:
        unknown = sorted(set(report["required_check_ids"]) - set(CHECK_IDS))
        if unknown:
            raise BoundaryProofError("unknown required check ID: " + unknown[0])
        raise BoundaryProofError("required_check_ids must contain the exact six checks")
    checks = _object(report["checks"], "checks")
    if set(checks) != set(CHECK_IDS):
        unknown = sorted(set(checks) - set(CHECK_IDS))
        if unknown:
            raise BoundaryProofError("unknown required check ID: " + unknown[0])
        raise BoundaryProofError("checks must contain the exact six check IDs")
    for check_id in CHECK_IDS:
        _result_record(checks[check_id], f"checks.{check_id}", root)

    rows = _records(report["fixtures"], "fixtures")
    seen: set[str] = set()
    fixture_fields = frozenset(
        {
            "fixture_id",
            "result",
            "expected_gate",
            "detected_stage",
            "escaped_to_code_review",
            "sibling_bypass_remaining",
            "evidence_refs",
            "blocking_reason",
        }
    )
    for index, row in enumerate(rows):
        label = f"fixtures[{index}]"
        _exact_fields(row, fixture_fields, label)
        fixture_id = row["fixture_id"]
        if fixture_id not in FIXTURE_GATES:
            raise BoundaryProofError(f"{label}: unknown fixture: {fixture_id!r}")
        if fixture_id in seen:
            raise BoundaryProofError(f"{label}: duplicate fixture")
        seen.add(fixture_id)
        result = row["result"]
        if result not in RESULT_VALUES:
            raise BoundaryProofError(f"{label}: unknown result: {result!r}")
        if row["expected_gate"] not in EXPECTED_GATES:
            raise BoundaryProofError(f"{label}: unknown expected gate")
        if row["expected_gate"] != FIXTURE_GATES[fixture_id]:
            raise BoundaryProofError(f"{label}: expected gate mismatch")
        if row["detected_stage"] not in DETECTED_STAGES:
            raise BoundaryProofError(f"{label}: unknown detected stage")
        for field in ("escaped_to_code_review", "sibling_bypass_remaining"):
            if not isinstance(row[field], bool):
                raise BoundaryProofError(f"{label}.{field}: expected boolean")
        _result_record(
            {
                "result": result,
                "evidence_refs": row["evidence_refs"],
                "blocking_reason": row["blocking_reason"],
            },
            label,
            root,
        )
    if seen != set(FIXTURE_GATES):
        raise BoundaryProofError("fixtures must contain every exact seeded fixture")

    preservation = _object(report["preservation_results"], "preservation_results")
    if set(preservation) != set(PRESERVATION_KEYS):
        raise BoundaryProofError("preservation_results must contain exact preservation keys")
    for key in PRESERVATION_KEYS:
        _result_record(preservation[key], f"preservation_results.{key}", root)
    _result_record(report["adapter_parity"], "adapter_parity", root)
    for field in (
        "false_blocking_count",
        "duplicate_normative_owner_count",
        "new_universal_artifact_count",
        "simple_fixture_structure_correction_cycles",
    ):
        value = report[field]
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise BoundaryProofError(f"{field}: expected non-negative integer")
    if report["overall_result"] not in {"pass", "fail"}:
        raise BoundaryProofError("overall_result: expected pass or fail")


def validate_version_parity(
    feature_version: str | None,
    feature_scope: str | None,
    proof_version: str | None,
    proof_scope: str | None,
    *,
    public_activation: bool,
    explicitly_reviewed_opt_in: bool,
) -> str:
    """Validate prospective legacy/v1 adoption without inferring authority.

    Missing markers are grandfathered as ``legacy`` only before public
    activation.  A pre-activation ``v1`` pair requires an explicitly reviewed
    opt-in.  This function validates deterministic parity only; it does not
    decide whether an artifact is substantively revised.
    """

    def normalize(value: str | None, label: str) -> str:
        if value is None:
            if public_activation:
                raise BoundaryProofError(f"{label}: boundary-model marker required")
            return "legacy"
        if value not in BOUNDARY_MODEL_VERSIONS:
            raise BoundaryProofError(f"{label}: unknown boundary-model version")
        return value

    feature = normalize(feature_version, "feature")
    proof = normalize(proof_version, "proof")
    markers_absent = feature_version is None and proof_version is None
    if (feature_version is None) != (proof_version is None):
        raise BoundaryProofError("boundary-model marker presence mismatch")
    if feature != proof:
        raise BoundaryProofError("boundary-model version mismatch")
    if markers_absent:
        if feature_scope is not None or proof_scope is not None:
            raise BoundaryProofError("markerless legacy pair cannot contain scope")
    else:
        if not isinstance(feature_scope, str) or not SCOPE_RE.fullmatch(feature_scope):
            raise BoundaryProofError("feature boundary-model scope is invalid")
        if not isinstance(proof_scope, str) or not SCOPE_RE.fullmatch(proof_scope):
            raise BoundaryProofError("proof boundary-model scope is invalid")
        if feature_scope != proof_scope:
            raise BoundaryProofError("boundary-model scope mismatch")
    if feature == "v1":
        if not public_activation and not explicitly_reviewed_opt_in:
            raise BoundaryProofError("pre-activation v1 requires reviewed opt-in")
    return feature


def capability_report_result(
    payload: Mapping[str, Any],
    *,
    repository_root: Path | None = None,
) -> str:
    """Compute the capability baseline without trusting an asserted outcome."""

    report = _object(payload, "capability_report")
    _validate_report_shape(report, repository_root)
    checks = report["checks"]
    fixtures = report["fixtures"]
    preservation = report["preservation_results"]
    pass_result = all(checks[check_id]["result"] == "pass" for check_id in CHECK_IDS)
    pass_result = pass_result and all(
        preservation[key]["result"] == "pass" for key in PRESERVATION_KEYS
    )
    pass_result = pass_result and report["adapter_parity"]["result"] == "pass"
    gate_index = {gate: index for index, gate in enumerate(EXPECTED_GATES)}
    for row in fixtures:
        detected = row["detected_stage"]
        timely = (
            detected != "not-detected"
            and gate_index[detected] <= gate_index[row["expected_gate"]]
        )
        pass_result = (
            pass_result
            and row["result"] == "pass"
            and timely
            and not row["escaped_to_code_review"]
            and not row["sibling_bypass_remaining"]
        )
    pass_result = pass_result and report["false_blocking_count"] == 0
    pass_result = pass_result and report["duplicate_normative_owner_count"] == 0
    pass_result = pass_result and report["new_universal_artifact_count"] == 0
    pass_result = (
        pass_result
        and report["simple_fixture_structure_correction_cycles"] <= 1
    )
    return "pass" if pass_result else "fail"


def validate_boundary_activation_notes(
    text: str,
    *,
    report_identity: str | None = None,
) -> str:
    """Validate the closed activation or rollback release-note transaction."""

    activation_lines = [
        line.strip()
        for line in text.splitlines()
        if line.startswith("Boundary model activation:")
    ]
    report_lines = [
        line.strip()
        for line in text.splitlines()
        if line.startswith("Boundary capability report identity:")
    ]
    prior_lines = [
        line.strip()
        for line in text.splitlines()
        if line.startswith("Prior boundary activation identity:")
    ]
    if len(activation_lines) != 1:
        raise BoundaryProofError(
            "release notes require exactly one boundary activation state"
        )
    state = activation_lines[0].split(":", 1)[1].strip()
    if state == "v1":
        if len(report_lines) != 1 or prior_lines:
            raise BoundaryProofError(
                "v1 activation requires exactly one report identity"
            )
        identity = report_lines[0].split(":", 1)[1].strip()
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", identity):
            raise BoundaryProofError(
                "activation report identity is invalid"
            )
        if report_identity is None or identity != report_identity:
            raise BoundaryProofError(
                "activation report identity is stale or unavailable"
            )
        return "activated"
    if state == "rolled-back":
        if report_lines or len(prior_lines) != 1:
            raise BoundaryProofError(
                "rollback requires exactly one prior activation identity"
            )
        prior = prior_lines[0].split(":", 1)[1].strip()
        if not re.fullmatch(
            r"[^\s]+@sha256:[0-9a-f]{64}", prior
        ):
            raise BoundaryProofError(
                "prior activation identity is invalid"
            )
        return "rolled-back"
    raise BoundaryProofError("unknown boundary activation state")


def validate_capability_report(
    payload: Mapping[str, Any],
    *,
    repository_root: Path | None = None,
) -> None:
    """Validate report shape and reject caller-asserted aggregate results."""

    report = _object(payload, "capability_report")
    computed = capability_report_result(report, repository_root=repository_root)
    if report["overall_result"] != computed:
        raise BoundaryProofError(
            "overall_result does not match computed capability result"
        )


def evaluate_simple_change_trace(
    payload: Mapping[str, Any],
    *,
    feature_models: Mapping[str, FeatureBoundaryModel] | None = None,
    proof_maps: Mapping[str, BoundaryProofMap] | None = None,
    structural_evaluations: Mapping[str, Mapping[str, str]] | None = None,
) -> SimpleTraceMetrics:
    """Validate the exact R28y synthetic trace and derive its observations."""

    record = _object(payload, "simple_trace")
    _exact_fields(
        record,
        frozenset(
            {
                "snapshots",
                "review_bundles",
                "events",
                "before_inventory",
                "after_inventory",
            }
        ),
        "simple_trace",
    )

    identity_pattern = re.compile(r"^sha256:[0-9a-f]{64}$")
    snapshot_fields = frozenset(
        {"snapshot_id", "source", "artifact_role", "path", "identity"}
    )
    event_fields = frozenset(
        {
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
    )
    inventory_fields = frozenset({"path", "artifact_kind", "identity"})
    allowed_stages = ("spec", "spec-review", "test-spec", "test-spec-review")
    allowed_roles = ("feature-spec", "test-spec", "review-evidence")
    artifact_kinds = (
        "feature-spec",
        "test-spec",
        "review-evidence",
        "other-lifecycle",
        "non-lifecycle",
    )
    behavior_artifact_pattern = re.compile(
        r"^docs/changes/[a-z0-9-]+/evidence/simple-change/runs/"
        r"run-[0-9a-f]{32}/artifacts/(?P<relative>.+)$"
    )

    def normalized_path(value: Any, label: str) -> str:
        raw = _nonempty_string(value, label)
        path = Path(raw)
        if path.is_absolute() or ".." in path.parts or path.as_posix() != raw:
            raise BoundaryProofError(f"{label}: unsafe path")
        return raw

    def identity(value: Any, label: str) -> str:
        result = _nonempty_string(value, label)
        if not identity_pattern.fullmatch(result):
            raise BoundaryProofError(f"{label}: invalid identity")
        return result

    def classify_artifact(path: str) -> str:
        behavior_match = behavior_artifact_pattern.fullmatch(path)
        if behavior_match is not None:
            relative = Path(behavior_match.group("relative"))
            top = relative.parts[0]
            if (
                len(relative.parts) == 2
                and relative.suffix == ".md"
                and top in {"feature-spec", "test-spec"}
            ):
                return top
            if len(relative.parts) == 2 and top == "review-evidence":
                return "review-evidence"
            if top in {"proposal", "plan", "architecture", "adr", "change-record"}:
                return "other-lifecycle"
            return "non-lifecycle"

        parts = Path(path).parts
        if (
            len(parts) == 2
            and parts[0] == "specs"
            and parts[1].endswith(".md")
        ):
            return "test-spec" if parts[1].endswith(".test.md") else "feature-spec"
        if path.startswith(BOUNDARY_CHANGE_ROOT + "/reviews/") and path.endswith(
            ".md"
        ):
            return "review-evidence"
        if path in {
            BOUNDARY_CHANGE_ROOT + "/review-log.md",
            BOUNDARY_CHANGE_ROOT + "/review-resolution.md",
        }:
            return "review-evidence"
        if (
            (
                (
                    len(parts) == 3
                    and parts[:2]
                    in {
                        ("docs", "proposals"),
                        ("docs", "plans"),
                        ("docs", "adr"),
                    }
                )
                and path.endswith(".md")
            )
            or (len(parts) >= 3 and parts[:2] == ("docs", "architecture"))
        ):
            return "other-lifecycle"
        if path == BOUNDARY_CHANGE_ROOT + "/change.yaml":
            return "other-lifecycle"
        return "non-lifecycle"

    snapshots: dict[str, Mapping[str, Any]] = {}
    snapshot_by_ref: dict[tuple[str, str], str] = {}
    for index, raw_snapshot in enumerate(_records(record["snapshots"], "snapshots")):
        label = f"snapshots[{index}]"
        snapshot = _object(raw_snapshot, label)
        _exact_fields(snapshot, snapshot_fields, label)
        snapshot_id = _nonempty_string(snapshot["snapshot_id"], f"{label}.snapshot_id")
        if not STABLE_ID_RE.fullmatch(snapshot_id):
            raise BoundaryProofError(f"{label}: invalid snapshot ID")
        if snapshot_id in snapshots:
            raise BoundaryProofError(f"{label}: duplicate snapshot ID")
        source = snapshot["source"]
        if source not in ("fixture-candidate", "behavior-output"):
            raise BoundaryProofError(f"{label}: unknown snapshot source")
        role = snapshot["artifact_role"]
        if role not in allowed_roles:
            raise BoundaryProofError(f"{label}: unknown snapshot role")
        path = normalized_path(snapshot["path"], f"{label}.path")
        digest = identity(snapshot["identity"], f"{label}.identity")
        if source == "fixture-candidate":
            prefix = "tests/fixtures/boundary-proof/simple-change/candidates/"
            if role == "review-evidence" or not path.startswith(prefix):
                raise BoundaryProofError(f"{label}: invalid fixture-candidate path")
        else:
            marker = "/evidence/simple-change/runs/run-"
            role_path = f"/artifacts/{role}/"
            if marker not in path or role_path not in path:
                raise BoundaryProofError(f"{label}: invalid behavior-output path")
        reference = (path, digest)
        if reference in snapshot_by_ref:
            raise BoundaryProofError(f"{label}: duplicate snapshot path and identity")
        if any(existing[0] == path for existing in snapshot_by_ref):
            raise BoundaryProofError(f"{label}: duplicate snapshot path")
        snapshots[snapshot_id] = snapshot
        snapshot_by_ref[reference] = snapshot_id

    def snapshot_ref(snapshot_id: str) -> dict[str, str]:
        snapshot = snapshots[snapshot_id]
        return {"path": snapshot["path"], "identity": snapshot["identity"]}

    def snapshot_ids(value: Any, label: str) -> tuple[str, ...]:
        values = _strings(value, label, nonempty=False)
        if len(values) != len(set(values)):
            raise BoundaryProofError(f"{label}: duplicate snapshot ID")
        for snapshot_id in values:
            if snapshot_id not in snapshots:
                raise BoundaryProofError(f"{label}: unknown snapshot ID")
            if snapshots[snapshot_id]["source"] != "behavior-output":
                raise BoundaryProofError(f"{label}: fixture candidates cannot enter events")
        return values

    def evidence_refs(value: Any, label: str) -> tuple[tuple[str, str], ...]:
        rows = _records(value, label)
        result: list[tuple[str, str]] = []
        for index, row in enumerate(rows):
            item_label = f"{label}[{index}]"
            _exact_fields(row, frozenset({"path", "identity"}), item_label)
            reference = (
                normalized_path(row["path"], f"{item_label}.path"),
                identity(row["identity"], f"{item_label}.identity"),
            )
            if reference not in snapshot_by_ref:
                raise BoundaryProofError(f"{item_label}: evidence does not name a snapshot")
            result.append(reference)
        if len(result) != len(set(result)):
            raise BoundaryProofError(f"{label}: duplicate evidence reference")
        if result != sorted(result):
            raise BoundaryProofError(f"{label}: evidence references are not normalized")
        return tuple(result)

    bundle_records = _object(record["review_bundles"], "review_bundles")
    bundles: dict[str, Mapping[str, Any]] = {}
    bundle_artifacts: dict[str, tuple[str, ...]] = {}
    bundle_resolutions: dict[str, str | None] = {}
    for bundle_snapshot_id, raw_bundle in bundle_records.items():
        label = f"review_bundles.{bundle_snapshot_id}"
        if bundle_snapshot_id not in snapshots:
            raise BoundaryProofError(f"{label}: unknown bundle snapshot")
        bundle_snapshot = snapshots[bundle_snapshot_id]
        if (
            bundle_snapshot["source"] != "behavior-output"
            or bundle_snapshot["artifact_role"] != "review-evidence"
        ):
            raise BoundaryProofError(f"{label}: invalid bundle snapshot")
        bundle = _object(raw_bundle, label)
        _exact_fields(
            bundle,
            frozenset(
                {
                    "review_id",
                    "outcome",
                    "reviewed_snapshot_id",
                    "material_finding_ids",
                    "finding_projection",
                    "finding_projection_identity",
                    "correction_eligibility",
                    "artifact_refs",
                }
            ),
            label,
        )
        _nonempty_string(bundle["review_id"], f"{label}.review_id")
        outcome = bundle["outcome"]
        if outcome not in ("approved", "changes-requested", "blocked"):
            raise BoundaryProofError(f"{label}: unknown review outcome")
        reviewed_snapshot_id = _nonempty_string(
            bundle["reviewed_snapshot_id"], f"{label}.reviewed_snapshot_id"
        )
        if reviewed_snapshot_id not in snapshots:
            raise BoundaryProofError(f"{label}: unknown reviewed snapshot")
        findings = _strings(
            bundle["material_finding_ids"],
            f"{label}.material_finding_ids",
            nonempty=False,
        )
        if len(findings) != len(set(findings)):
            raise BoundaryProofError(f"{label}: duplicate material finding")
        for finding in findings:
            if not STABLE_ID_RE.fullmatch(finding):
                raise BoundaryProofError(f"{label}: invalid material finding ID")
        projection = _records(
            bundle["finding_projection"], f"{label}.finding_projection"
        )
        projection_ids: list[str] = []
        for index, raw_row in enumerate(projection):
            row_label = f"{label}.finding_projection[{index}]"
            row = _object(raw_row, row_label)
            _exact_fields(
                row,
                frozenset(
                    {
                        "finding_id",
                        "evidence",
                        "required_outcome",
                        "safe_resolution_path",
                        "needs_decision_rationale",
                    }
                ),
                row_label,
            )
            finding_id = _nonempty_string(
                row["finding_id"], f"{row_label}.finding_id"
            )
            if not STABLE_ID_RE.fullmatch(finding_id):
                raise BoundaryProofError(f"{row_label}: invalid finding ID")
            projection_ids.append(finding_id)
            for field in (
                "evidence",
                "required_outcome",
                "safe_resolution_path",
                "needs_decision_rationale",
            ):
                _nonempty_string(row[field], f"{row_label}.{field}")
        if projection_ids != sorted(projection_ids) or len(
            projection_ids
        ) != len(set(projection_ids)):
            raise BoundaryProofError(f"{label}: finding projection order")
        if outcome == "changes-requested":
            if projection_ids != list(findings):
                raise BoundaryProofError(
                    f"{label}: finding projection ID mismatch"
                )
        elif projection:
            raise BoundaryProofError(
                f"{label}: non-correction projection must be empty"
            )
        if bundle["finding_projection_identity"] != _canonical_identity(
            projection
        ):
            raise BoundaryProofError(
                f"{label}: finding projection identity mismatch"
            )
        eligibility = bundle["correction_eligibility"]
        if eligibility not in (
            "not-applicable",
            "automatic-eligible",
            "owner-decision-required",
        ):
            raise BoundaryProofError(
                f"{label}: unknown correction eligibility"
            )
        expected_eligibility = "not-applicable"
        if outcome == "changes-requested":
            expected_eligibility = (
                "owner-decision-required"
                if any(
                    row["needs_decision_rationale"] != "none"
                    for row in projection
                )
                else "automatic-eligible"
            )
        if eligibility != expected_eligibility:
            raise BoundaryProofError(
                f"{label}: correction eligibility mismatch"
            )
        artifact_refs = _object(bundle["artifact_refs"], f"{label}.artifact_refs")
        required_roles = {"review-record", "review-log"}
        if outcome in ("changes-requested", "blocked") or (
            outcome == "approved" and findings
        ):
            required_roles.add("review-resolution")
        if set(artifact_refs) != required_roles:
            raise BoundaryProofError(f"{label}: review artifact roles mismatch")
        if outcome == "approved" and findings:
            if "review-resolution" not in artifact_refs:
                raise BoundaryProofError(
                    f"{label}: approving rereview lacks resolution"
                )
        elif (outcome == "approved") != (not findings):
            raise BoundaryProofError(f"{label}: material findings mismatch outcome")
        artifact_snapshot_ids: list[str] = []
        for role, raw_reference in artifact_refs.items():
            reference_label = f"{label}.artifact_refs.{role}"
            reference = _object(raw_reference, reference_label)
            _exact_fields(reference, frozenset({"path", "identity"}), reference_label)
            key = (
                normalized_path(reference["path"], f"{reference_label}.path"),
                identity(reference["identity"], f"{reference_label}.identity"),
            )
            artifact_snapshot_id = snapshot_by_ref.get(key)
            if artifact_snapshot_id is None:
                raise BoundaryProofError(f"{reference_label}: unknown snapshot reference")
            artifact_snapshot = snapshots[artifact_snapshot_id]
            if (
                artifact_snapshot["source"] != "behavior-output"
                or artifact_snapshot["artifact_role"] != "review-evidence"
            ):
                raise BoundaryProofError(f"{reference_label}: invalid review evidence")
            artifact_snapshot_ids.append(artifact_snapshot_id)
        if len(artifact_snapshot_ids) != len(set(artifact_snapshot_ids)):
            raise BoundaryProofError(f"{label}: duplicate review artifact reference")
        bundles[bundle_snapshot_id] = bundle
        bundle_artifacts[bundle_snapshot_id] = tuple(artifact_snapshot_ids)
        bundle_resolutions[bundle_snapshot_id] = (
            snapshot_by_ref[
                (
                    normalized_path(
                        artifact_refs["review-resolution"]["path"],
                        f"{label}.artifact_refs.review-resolution.path",
                    ),
                    identity(
                        artifact_refs["review-resolution"]["identity"],
                        f"{label}.artifact_refs.review-resolution.identity",
                    ),
                )
            ]
            if "review-resolution" in artifact_refs
            else None
        )

    false_blocking = 0
    correction_cycles = 0
    correction_used = False
    awaiting_correction_approval: (
        tuple[str, int, tuple[str, ...], str] | None
    ) = None
    expected_stage = "spec"
    expected_attempt = 1
    terminal = False
    produced: set[str] = set()
    produced_paths: set[str] = set()
    prior_authoring_output: dict[str, str] = {}
    review_evidence_for_snapshot: dict[str, tuple[str, ...]] = {}
    final_approved_feature: str | None = None
    final_approved_test_spec: str | None = None

    events = _records(record["events"], "events")
    if structural_evaluations is None:
        raise BoundaryProofError(
            "simple_trace: independent structural evaluations are required"
        )
    expected_structural_keys = {
        f"{event.get('stage')}#{event.get('attempt')}" for event in events
    }
    if set(structural_evaluations) != expected_structural_keys:
        raise BoundaryProofError(
            "simple_trace: structural evaluation key set mismatch"
        )
    for index, raw_event in enumerate(events):
        label = f"events[{index}]"
        event = _object(raw_event, label)
        _exact_fields(event, event_fields, label)
        stage = event["stage"]
        if stage not in allowed_stages:
            raise BoundaryProofError(f"{label}: unknown stage")
        attempt = event["attempt"]
        if attempt not in (1, 2):
            raise BoundaryProofError(f"{label}: invalid attempt")
        if terminal:
            raise BoundaryProofError(f"{label}: event follows terminal result")
        if (stage, attempt) != (expected_stage, expected_attempt):
            raise BoundaryProofError(
                f"{label}: unsupported stage sequence; expected "
                f"{expected_stage}#{expected_attempt}"
            )
        inputs = snapshot_ids(event["input_snapshot_ids"], f"{label}.input_snapshot_ids")
        outputs = snapshot_ids(event["output_snapshot_ids"], f"{label}.output_snapshot_ids")
        if len(outputs) != 1:
            raise BoundaryProofError(f"{label}: expected exactly one output snapshot")
        if any(snapshot_id not in produced for snapshot_id in inputs):
            raise BoundaryProofError(f"{label}: input snapshot used before production")
        if any(snapshot_id in produced for snapshot_id in outputs):
            raise BoundaryProofError(f"{label}: output snapshot already produced")
        structural = event["structural_result"]
        if structural not in ("pass", "fail"):
            raise BoundaryProofError(f"{label}: unknown structural result")
        observed = event["observed_result"]
        diagnostic = _nonempty_string(event["diagnostic_id"], f"{label}.diagnostic_id")
        diagnostic_is_none = diagnostic == "none"
        if not diagnostic_is_none and not STABLE_ID_RE.fullmatch(diagnostic):
            raise BoundaryProofError(f"{label}: invalid diagnostic ID")
        reviewed = event["reviewed_snapshot_id"]
        is_review = stage.endswith("-review")
        output_id = outputs[0]
        structural_key = f"{stage}#{attempt}"
        structural_evaluation = _object(
            structural_evaluations[structural_key],
            f"structural_evaluations.{structural_key}",
        )
        _exact_fields(
            structural_evaluation,
            frozenset({"structural_result", "diagnostic_id"}),
            f"structural_evaluations.{structural_key}",
        )
        evaluated_result = structural_evaluation["structural_result"]
        if evaluated_result not in ("pass", "fail"):
            raise BoundaryProofError(
                f"structural_evaluations.{structural_key}: unknown result"
            )
        evaluated_diagnostic = _nonempty_string(
            structural_evaluation["diagnostic_id"],
            f"structural_evaluations.{structural_key}.diagnostic_id",
        )
        if (
            evaluated_diagnostic != "none"
            and not STABLE_ID_RE.fullmatch(evaluated_diagnostic)
        ):
            raise BoundaryProofError(
                f"structural_evaluations.{structural_key}: invalid diagnostic ID"
            )
        if (evaluated_result == "pass") != (evaluated_diagnostic == "none"):
            raise BoundaryProofError(
                f"structural_evaluations.{structural_key}: result/diagnostic mismatch"
            )
        if structural != evaluated_result:
            raise BoundaryProofError(f"{label}: structural result mismatch")
        if structural == "fail" and diagnostic != evaluated_diagnostic:
            raise BoundaryProofError(f"{label}: structural diagnostic mismatch")
        if not is_review and diagnostic != evaluated_diagnostic:
            raise BoundaryProofError(f"{label}: authoring diagnostic mismatch")

        if is_review:
            expected_role = "feature-spec" if stage == "spec-review" else "test-spec"
            if reviewed not in snapshots:
                raise BoundaryProofError(f"{label}: unknown reviewed snapshot")
            if reviewed not in inputs or inputs.count(reviewed) != 1:
                raise BoundaryProofError(f"{label}: reviewed snapshot linkage mismatch")
            if snapshots[reviewed]["artifact_role"] != expected_role:
                raise BoundaryProofError(f"{label}: reviewed snapshot role mismatch")
            if snapshots[output_id]["artifact_role"] != "review-evidence":
                raise BoundaryProofError(f"{label}: review output role mismatch")
            bundle = bundles.get(output_id)
            if bundle is None:
                raise BoundaryProofError(f"{label}: missing review bundle")
            if (
                bundle["reviewed_snapshot_id"] != reviewed
                or bundle["outcome"] != observed
            ):
                raise BoundaryProofError(f"{label}: review bundle mismatch")
            if observed not in ("approved", "changes-requested", "blocked"):
                raise BoundaryProofError(f"{label}: invalid review result")
            if structural == "pass" and observed == "approved":
                if not diagnostic_is_none:
                    raise BoundaryProofError(f"{label}: approved review requires no diagnostic")
            elif observed in ("changes-requested", "blocked"):
                if diagnostic_is_none:
                    raise BoundaryProofError(f"{label}: non-approval requires diagnostic")
                if structural == "pass":
                    false_blocking += 1
            else:
                raise BoundaryProofError(f"{label}: failed structure cannot be approved")
        else:
            if reviewed is not None:
                raise BoundaryProofError(f"{label}: authoring cannot review a snapshot")
            expected_role = "feature-spec" if stage == "spec" else "test-spec"
            if snapshots[output_id]["artifact_role"] != expected_role:
                raise BoundaryProofError(f"{label}: authoring output role mismatch")
            if observed != "produced":
                raise BoundaryProofError(f"{label}: authoring result must be produced")
            if (structural == "pass") != diagnostic_is_none:
                raise BoundaryProofError(f"{label}: authoring diagnostic mismatch")

        if stage == "spec" and attempt == 1 and inputs:
            raise BoundaryProofError(f"{label}: spec#1 must have no inputs")
        if stage == "spec-review" and set(inputs) != {reviewed}:
            raise BoundaryProofError(f"{label}: spec-review input mismatch")

        if stage == "spec" and attempt == 2:
            prior = prior_authoring_output.get("spec")
            expected_inputs = (
                {prior, *review_evidence_for_snapshot.get(prior or "", ())}
                if prior is not None
                else set()
            )
            if set(inputs) != expected_inputs:
                raise BoundaryProofError(f"{label}: spec#2 input mismatch")
            if snapshots[output_id]["path"] == snapshots[prior]["path"]:
                raise BoundaryProofError(f"{label}: corrected output must use a distinct path")
            if snapshots[output_id]["identity"] == snapshots[prior]["identity"]:
                raise BoundaryProofError(f"{label}: corrected output must use a distinct identity")

        if stage == "test-spec":
            if final_approved_feature is None:
                raise BoundaryProofError(f"{label}: approved feature input is missing")
            expected_inputs = {
                final_approved_feature,
                *review_evidence_for_snapshot[final_approved_feature],
            }
            if attempt == 2:
                prior = prior_authoring_output.get("test-spec")
                if prior is None:
                    raise BoundaryProofError(f"{label}: prior test-spec is missing")
                expected_inputs.update(
                    {prior, *review_evidence_for_snapshot.get(prior, ())}
                )
                if snapshots[output_id]["path"] == snapshots[prior]["path"]:
                    raise BoundaryProofError(
                        f"{label}: corrected output must use a distinct path"
                    )
                if snapshots[output_id]["identity"] == snapshots[prior]["identity"]:
                    raise BoundaryProofError(
                        f"{label}: corrected output must use a distinct identity"
                    )
            if set(inputs) != expected_inputs:
                raise BoundaryProofError(f"{label}: test-spec input mismatch")

        if stage == "test-spec-review":
            if final_approved_feature is None:
                raise BoundaryProofError(f"{label}: approved feature input is missing")
            expected_inputs = {
                reviewed,
                final_approved_feature,
                *review_evidence_for_snapshot[final_approved_feature],
            }
            if set(inputs) != expected_inputs:
                raise BoundaryProofError(f"{label}: test-spec-review input mismatch")

        expected_evidence_ids = set(inputs) | set(outputs)
        if is_review:
            expected_evidence_ids.update(bundle_artifacts[output_id])
        expected_evidence = tuple(
            sorted(
                (
                    snapshots[snapshot_id]["path"],
                    snapshots[snapshot_id]["identity"],
                )
                for snapshot_id in expected_evidence_ids
            )
        )
        if evidence_refs(event["evidence_refs"], f"{label}.evidence_refs") != expected_evidence:
            raise BoundaryProofError(f"{label}: evidence reference union mismatch")

        produced.add(output_id)
        produced_paths.add(snapshots[output_id]["path"])
        if is_review:
            produced.update(bundle_artifacts[output_id])
            produced_paths.update(
                snapshots[snapshot_id]["path"]
                for snapshot_id in bundle_artifacts[output_id]
            )
            review_evidence_for_snapshot[reviewed] = (
                output_id,
                *bundle_artifacts[output_id],
            )

            if observed == "changes-requested":
                if bundle["correction_eligibility"] != "automatic-eligible":
                    raise BoundaryProofError(
                        f"{label}: non-executable correction authority"
                    )
                if correction_used or attempt != 1:
                    raise BoundaryProofError(f"{label}: more than one correction")
                correction_used = True
                expected_stage = stage.removesuffix("-review")
                expected_attempt = 2
                resolution_snapshot_id = bundle_resolutions[output_id]
                if resolution_snapshot_id is None:
                    raise BoundaryProofError(
                        f"{label}: correction review lacks resolution"
                    )
                awaiting_correction_approval = (
                    stage,
                    2,
                    tuple(bundle["material_finding_ids"]),
                    resolution_snapshot_id,
                )
            elif observed == "blocked":
                terminal = True
            elif awaiting_correction_approval is not None:
                (
                    pending_stage,
                    pending_attempt,
                    pending_findings,
                    pending_resolution,
                ) = awaiting_correction_approval
                if (stage, attempt) != (pending_stage, pending_attempt):
                    raise BoundaryProofError(f"{label}: correction approval mismatch")
                if tuple(bundle["material_finding_ids"]) != pending_findings:
                    raise BoundaryProofError(
                        f"{label}: approving rereview finding set mismatch"
                    )
                rereview_resolution = bundle_resolutions[output_id]
                if (
                    rereview_resolution is None
                    or rereview_resolution == pending_resolution
                ):
                    raise BoundaryProofError(
                        f"{label}: approving rereview resolution mismatch"
                    )
                correction_cycles += 1
                awaiting_correction_approval = None
                if stage == "spec-review":
                    final_approved_feature = reviewed
                    expected_stage, expected_attempt = "test-spec", 1
                else:
                    final_approved_test_spec = reviewed
                    terminal = True
            elif stage == "spec-review":
                final_approved_feature = reviewed
                expected_stage, expected_attempt = "test-spec", 1
            else:
                final_approved_test_spec = reviewed
                terminal = True
        else:
            prior_authoring_output[stage] = output_id
            if structural == "fail":
                terminal = True
            else:
                expected_stage, expected_attempt = f"{stage}-review", attempt

    if not terminal:
        raise BoundaryProofError("simple_trace: incomplete terminal branch")

    def inventory(value: Any, label: str) -> dict[str, tuple[str, str]]:
        rows = _records(value, label)
        paths = [row.get("path") for row in rows]
        if paths != sorted(paths):
            raise BoundaryProofError(f"{label}: inventory is not path sorted")
        result: dict[str, tuple[str, str]] = {}
        identities: set[str] = set()
        for index, raw_row in enumerate(rows):
            item_label = f"{label}[{index}]"
            row = _object(raw_row, item_label)
            _exact_fields(row, inventory_fields, item_label)
            path = normalized_path(row["path"], f"{item_label}.path")
            kind = row["artifact_kind"]
            if kind not in artifact_kinds:
                raise BoundaryProofError(f"{item_label}: unknown artifact kind")
            expected_kind = classify_artifact(path)
            if kind != expected_kind:
                raise BoundaryProofError(
                    f"{item_label}: artifact kind does not match closed path classifier"
                )
            digest = identity(row["identity"], f"{item_label}.identity")
            if path in result:
                raise BoundaryProofError(f"{item_label}: duplicate inventory path")
            if digest in identities:
                raise BoundaryProofError(f"{item_label}: duplicate inventory identity")
            result[path] = (kind, digest)
            identities.add(digest)
        return result

    before = inventory(record["before_inventory"], "before_inventory")
    after = inventory(record["after_inventory"], "after_inventory")
    behavior_outputs = {
        snapshot_id
        for snapshot_id, snapshot in snapshots.items()
        if snapshot["source"] == "behavior-output"
    }
    for snapshot_id in behavior_outputs:
        snapshot = snapshots[snapshot_id]
        path = snapshot["path"]
        expected_inventory = (
            snapshot["artifact_role"],
            snapshot["identity"],
        )
        if after.get(path) != expected_inventory:
            raise BoundaryProofError(
                f"after_inventory: produced snapshot missing or mismatched: {snapshot_id}"
            )
    new_paths = set(after) - set(before)
    new_universal = sum(
        1
        for path in new_paths - produced_paths
        if after[path][0] != "non-lifecycle"
    )

    applicable_only = False
    if final_approved_feature is not None and final_approved_test_spec is not None:
        if feature_models is None or proof_maps is None:
            raise BoundaryProofError(
                "simple_trace: normalized final feature and proof models are required"
            )
        feature = feature_models.get(final_approved_feature)
        proof = proof_maps.get(final_approved_test_spec)
        if feature is None or proof is None:
            raise BoundaryProofError(
                "simple_trace: final approved snapshot model is missing"
            )
        applicable_references = {
            boundary_id
            for entry in (*feature.core_dimensions, *feature.extensions)
            if entry.applicability == "applicable"
            for boundary_id in entry.boundary_ids
        }
        applicable_references.update(
            interaction.interaction_id for interaction in feature.interactions
        )
        mapped_references = {
            reference
            for obligation in proof.proof_obligations
            for reference in obligation.boundary_or_interaction_ids
        }
        applicable_only = mapped_references == applicable_references
        if not applicable_only:
            raise BoundaryProofError("simple_trace: applicable-only mapping mismatch")

    return SimpleTraceMetrics(
        false_blocking,
        new_universal,
        correction_cycles,
        applicable_only,
    )


__all__ = [
    "APPLICABILITY_VALUES",
    "AUTOMATION_LEVELS",
    "BOUNDARY_MODEL_VERSIONS",
    "BoundaryExample",
    "BoundaryExtension",
    "BoundaryInteraction",
    "BoundaryProofError",
    "BoundaryProofMap",
    "CAPABILITY_REPORT_SCHEMA",
    "CHECK_IDS",
    "CORE_DIMENSION_IDS",
    "CoreBoundaryEntry",
    "DETECTED_STAGES",
    "EVALUATED_SKILLS",
    "EXAMPLE_ROLES",
    "EXPECTED_GATES",
    "FIXTURE_GATES",
    "INCIDENT_RULES",
    "FeatureBoundaryModel",
    "FeatureInvariantProjection",
    "INTERACTION_RATIONALES",
    "PRESERVATION_KEYS",
    "ProofObligation",
    "ProofInvariantProjection",
    "RESULT_VALUES",
    "SimpleTraceMetrics",
    "StageGateResult",
    "capability_report_result",
    "boundary_invariant_projections_match",
    "evaluate_boundary_state",
    "evaluate_simple_change_trace",
    "feature_invariant_projection",
    "normalize_feature_model",
    "normalize_proof_map",
    "proof_invariant_projection",
    "validate_capability_report",
    "validate_boundary_activation_notes",
    "validate_incident_registry",
    "validate_incident_fixture",
    "validate_version_parity",
]
