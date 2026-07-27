#!/usr/bin/env python3
"""Regression tests for the boundary-first proof model."""

from __future__ import annotations

import dataclasses
import copy
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from boundary_proof_behavior import (
    ARTIFACT_POLICY,
    ATTESTATION_FIELDS,
    CODEX_0_144_6_FEATURES,
    CODEX_0_145_0_FEATURES,
    PARTICIPATING_SKILLS,
    PREFLIGHT_FIELDS,
    FILE_CHANGE_AUTHORIZATION_POLICY,
    DIAGNOSTIC_PHASES,
    MATERIALIZATION_CANARY_POLICY,
    RUNTIME_SYSTEM_SKILLS,
    RUNTIME_PROTOCOL_CLASSIFICATION_IDENTITY_BY_VERSION,
    RUNTIME_SCHEMA_IDENTITY_BY_VERSION,
    BoundaryRuntimeError,
    _AppServer,
    _StageTurnTimeout,
    _assert_parent_only_candidate_isolation,
    _assert_correction_input_is_fresh,
    _assembled_working_paths,
    _artifact_kind,
    _assemble_feature_spec_correction_run,
    _assemble_test_spec_correction_run,
    _build_behavior_manifest,
    _classify_historical_evidence,
    _completed_correction_stop_input_identities,
    _correction_review_bundle,
    _create_publisher_lease,
    _dispatch_file_change_request,
    _discover_global_candidate,
    _invoke_with_reconciliation,
    _load_transport_fixture,
    _derive_config_origin_paths,
    _effective_tool_projection,
    _feature_inventory,
    _finding_projection as _runtime_finding_projection,
    freeze_baseline,
    _normalize_config_result,
    _normalize_skill_inventory,
    _load_generated_payload,
    _materialize_stage_envelope,
    _parse_stage_envelope,
    _publish_run,
    _publisher_lock,
    _reconcile_prepared,
    _parse_feature_markdown,
    _parse_test_spec_markdown,
    _parse_semver,
    _preflight_failure,
    _runtime_environment,
    _run_file_change_handler_conformance,
    _schema_bundle_projection,
    _workflow_request,
    _workflow_stage_request,
    _working_tree_identity,
    _thread_start_request,
    _turn_start_request,
    _observed_scenario_outcome,
    _review_payload_from_markdown,
    _validate_correction_stop_receipt,
    _validate_correction_stop_evidence,
    _validate_review_bundle_payloads,
    _validate_review_payload,
    _validate_scenario_expectations,
    _write_correction_stop,
    _validate_prepared_receipt,
    _validate_publisher_lease,
    _validate_recovery_basis,
    _validate_recovery_state,
    _validate_attestation,
    _validate_runtime_projection,
    _validated_thread_metadata,
    assess_environment,
    discard_interrupted_publication,
    exercise_fixture,
    generate_preservation,
    generate_canonical_skill_resource_manifest,
    validate_behavior,
    validate_fixture,
    validate_preservation,
)

from boundary_proof_model import (
    APPLICABILITY_VALUES,
    AUTOMATION_LEVELS,
    CHECK_IDS,
    CORE_DIMENSION_IDS,
    EVALUATED_SKILLS,
    EXAMPLE_ROLES,
    FIXTURE_GATES,
    INCIDENT_RULES,
    INTERACTION_RATIONALES,
    HANDLER_CONFORMANCE_CASES,
    RESULT_VALUES,
    RUNTIME_PROJECTIONS,
    RUNTIME_PROJECTION_FIELDS,
    runtime_projection_identity,
    BoundaryProofError,
    boundary_invariant_projections_match,
    feature_invariant_projection,
    CoreBoundaryEntry,
    capability_report_result,
    evaluate_boundary_state,
    evaluate_simple_change_trace,
    handler_conformance_policy,
    normalize_feature_model,
    normalize_proof_map,
    proof_invariant_projection,
    select_runtime_projection,
    validate_capability_report,
    validate_boundary_activation_notes,
    validate_handler_conformance,
    validate_incident_registry,
    validate_incident_fixture,
    validate_version_parity,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "boundary-proof"


def _recovery_authority(
    root: Path,
    change_id: str,
    *,
    authorized_by: str = "test-maintainer",
) -> Path:
    lease_path = (
        root
        / "docs"
        / "changes"
        / change_id
        / "evidence"
        / "simple-change"
        / "publisher.json"
    )
    lease = json.loads(lease_path.read_text(encoding="utf-8"))
    authority = (
        root
        / "docs"
        / "changes"
        / change_id
        / "recovery-decisions"
        / f"{lease['run_id']}.json"
    )
    authority.parent.mkdir(parents=True, exist_ok=True)
    authority.write_text(
        json.dumps(
            {
                "schema_version": "simple-change-recovery-decision-v1",
                "change_id": change_id,
                "run_id": lease["run_id"],
                "publisher_instance_id": lease["publisher_instance_id"],
                "input_set_identity": lease["input_set_identity"],
                "action": "discard-and-regenerate",
                "authorized_by": authorized_by,
                "outcome": "authorized",
            },
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    return authority


def _core_rows() -> list[dict[str, object]]:
    return [
        {
            "dimension_id": dimension_id,
            "applicability": "applicable",
            "governing_requirement_ids": ["R1"],
            "boundary_ids": [f"sample.{dimension_id}"],
            "non_applicability_rationale": None,
        }
        for dimension_id in CORE_DIMENSION_IDS
    ]


def _feature_model() -> dict[str, object]:
    return {
        "boundary_model_version": "v1",
        "boundary_model_scope": "R1-R9",
        "core_dimensions": _core_rows(),
        "extensions": [],
        "examples": [
            {
                "example_id": "sample.example.illustration",
                "role": "illustration",
                "governing_requirement_ids": ["R1"],
                "boundary_ids": ["sample.canonical-trust"],
                "regression_id": None,
                "discovery_gap": None,
                "non_normative_purpose": None,
            },
            {
                "example_id": "sample.example.regression",
                "role": "regression",
                "governing_requirement_ids": ["R1"],
                "boundary_ids": ["sample.identity-freshness"],
                "regression_id": "sample.regression.stale",
                "discovery_gap": None,
                "non_normative_purpose": None,
            },
            {
                "example_id": "sample.example.discovery",
                "role": "discovery",
                "governing_requirement_ids": [],
                "boundary_ids": [],
                "regression_id": None,
                "discovery_gap": "sample.gap.missing-rule",
                "non_normative_purpose": None,
            },
            {
                "example_id": "sample.example.non-normative",
                "role": "non-normative",
                "governing_requirement_ids": [],
                "boundary_ids": [],
                "regression_id": None,
                "discovery_gap": None,
                "non_normative_purpose": "Demonstrates layout only.",
            },
        ],
        "interactions": [
            {
                "interaction_id": "sample.interaction.identity-authority",
                "boundary_ids": [
                    "sample.identity-freshness",
                    "sample.authorization-scope",
                ],
                "rationale": "trust-or-authority",
                "governing_requirement_ids": ["R1"],
            }
        ],
    }


def _proof_map() -> dict[str, object]:
    rows = [
        {
            "proof_obligation_id": f"sample.proof.t{index + 1}",
            "governing_requirement_ids": ["R1"],
            "boundary_or_interaction_ids": [f"sample.{dimension_id}"],
            "test_case_ids": [f"T{index + 1}"],
            "automation_level": "automated",
            "manual_procedure_ids": [],
        }
        for index, dimension_id in enumerate(CORE_DIMENSION_IDS)
    ]
    rows.append(
        {
            "proof_obligation_id": "sample.proof.interaction",
            "governing_requirement_ids": ["R1"],
            "boundary_or_interaction_ids": [
                "sample.interaction.identity-authority"
            ],
            "test_case_ids": ["T20"],
            "automation_level": "hybrid",
            "manual_procedure_ids": ["sample.manual.semantic-review"],
        }
    )
    return {
        "boundary_model_version": "v1",
        "boundary_model_scope": "R1-R9",
        "proof_obligations": rows,
    }


def _report(result: str = "pass") -> dict[str, object]:
    evidence_path = ROOT / "specs" / "rigorloop-workflow.md"
    evidence = [
        {
            "path": "specs/rigorloop-workflow.md",
            "identity": "sha256:" + hashlib.sha256(evidence_path.read_bytes()).hexdigest(),
        }
    ]
    blocking_reason = (
        {
            "code": "prerequisite-unsatisfied",
            "detail": "M1 synthetic proof does not claim published-skill behavior.",
        }
        if result == "not-run"
        else None
    )
    fixtures = [
        {
            "fixture_id": fixture_id,
            "result": result,
            "expected_gate": expected_gate,
            "detected_stage": expected_gate if result != "not-run" else "not-detected",
            "escaped_to_code_review": False,
            "sibling_bypass_remaining": False,
            "evidence_refs": evidence if result != "not-run" else [],
            "blocking_reason": blocking_reason,
        }
        for fixture_id, expected_gate in FIXTURE_GATES.items()
    ]
    return {
        "schema_version": "boundary-capability-baseline-v1",
        "boundary_model_version": "v1",
        "evaluated_skills": list(EVALUATED_SKILLS),
        "required_check_ids": list(CHECK_IDS),
        "checks": {
            check_id: {
                "result": result,
                "evidence_refs": evidence if result != "not-run" else [],
                "blocking_reason": blocking_reason,
            }
            for check_id in CHECK_IDS
        },
        "fixtures": fixtures,
        "preservation_results": {
            key: {
                "result": result,
                "evidence_refs": evidence if result != "not-run" else [],
                "blocking_reason": blocking_reason,
            }
            for key in (
                "behavior",
                "claim-boundary",
                "review-recording",
                "isolation",
                "handoff",
            )
        },
        "adapter_parity": {
            "result": result,
            "evidence_refs": evidence if result != "not-run" else [],
            "blocking_reason": blocking_reason,
        },
        "false_blocking_count": 0,
        "duplicate_normative_owner_count": 0,
        "new_universal_artifact_count": 0,
        "simple_fixture_structure_correction_cycles": 1,
        "overall_result": "pass" if result == "pass" else "fail",
    }


def _set_all_report_evidence(
    report: dict[str, object],
    reference: dict[str, str],
) -> None:
    for row in report["checks"].values():  # type: ignore[union-attr]
        row["evidence_refs"] = [reference]  # type: ignore[index]
    for row in report["fixtures"]:  # type: ignore[union-attr]
        row["evidence_refs"] = [reference]
    for row in report["preservation_results"].values():  # type: ignore[union-attr]
        row["evidence_refs"] = [reference]  # type: ignore[index]
    report["adapter_parity"]["evidence_refs"] = [reference]  # type: ignore[index]


def _simple_models(
    payload: dict[str, object],
    *,
    feature_snapshot_ids: tuple[str, ...] = ("simple.snapshot.feature.v1",),
    proof_snapshot_ids: tuple[str, ...] = ("simple.snapshot.test-spec.v1",),
) -> tuple[dict[str, object], dict[str, object]]:
    feature = normalize_feature_model(payload["feature_model"])  # type: ignore[arg-type]
    proof = normalize_proof_map(payload["proof_map"], feature)  # type: ignore[arg-type]
    return (
        {snapshot_id: feature for snapshot_id in feature_snapshot_ids},
        {snapshot_id: proof for snapshot_id in proof_snapshot_ids},
    )


def _evaluate_simple(
    payload: dict[str, object],
    *,
    feature_snapshot_ids: tuple[str, ...] = ("simple.snapshot.feature.v1",),
    proof_snapshot_ids: tuple[str, ...] = ("simple.snapshot.test-spec.v1",),
) -> object:
    feature_models, proof_maps = _simple_models(
        payload,
        feature_snapshot_ids=feature_snapshot_ids,
        proof_snapshot_ids=proof_snapshot_ids,
    )
    return evaluate_simple_change_trace(
        payload["simple_trace"],  # type: ignore[arg-type]
        feature_models=feature_models,  # type: ignore[arg-type]
        proof_maps=proof_maps,  # type: ignore[arg-type]
        structural_evaluations=_structural_evaluations(  # type: ignore[arg-type]
            payload["simple_trace"]
        ),
    )


def _structural_evaluations(
    trace: dict[str, object],
) -> dict[str, dict[str, str]]:
    return {
        f"{event['stage']}#{event['attempt']}": {
            "structural_result": event["structural_result"],
            "diagnostic_id": (
                "none"
                if event["structural_result"] == "pass"
                else event["diagnostic_id"]
            ),
        }
        for event in trace["events"]  # type: ignore[union-attr]
    }


def _finding_projection(
    finding_id: str,
    *,
    needs_decision_rationale: str = "none",
) -> list[dict[str, str]]:
    return [
        {
            "finding_id": finding_id,
            "evidence": "direct evidence",
            "required_outcome": "apply the bounded correction",
            "safe_resolution_path": "update and rereview",
            "needs_decision_rationale": needs_decision_rationale,
        }
    ]


def _projection_identity(projection: object) -> str:
    raw = json.dumps(
        projection, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def _owner_decision_review(
    stage: str,
    artifact_identity: str,
    *,
    finding_ids: tuple[str, ...] = ("finding.owner-decision",),
) -> tuple[dict[str, object], str]:
    review_id = f"{stage}-r1"
    blocks = []
    for finding_id in finding_ids:
        blocks.append(
            f"## Finding {finding_id}\n\n"
            f"- Finding ID: {finding_id}\n"
            "- Evidence: exact boundary evidence\n"
            "- Required outcome: preserve owner authority\n"
            "- Safe resolution path: clarify the authoritative input\n"
            "- needs-decision rationale: owner must select compatibility\n"
        )
    joined_ids = ", ".join(finding_ids)
    record = (
        "# Review\n\n"
        f"Review ID: {review_id}\n"
        f"Stage: {stage}\n"
        "Status: changes-requested\n"
        f"Reviewed artifact identity: {artifact_identity}\n"
        f"Material findings: {joined_ids}\n"
        "Recording status: recorded\n\n"
        + "\n".join(blocks)
    )
    log = (
        f"Review ID: {review_id}\n"
        f"Stage: {stage}\n"
        "Status: changes-requested\n"
        f"Reviewed artifact identity: {artifact_identity}\n"
        f"Material findings: {joined_ids}\n"
    )
    payload = _review_payload_from_markdown(stage, record, log)
    resolution = (
        "# Review resolution\n\n"
        f"Review ID: {review_id}\n"
        + "\n".join(f"Finding ID: {value}" for value in finding_ids)
        + "\nCloseout status: open\n"
    )
    return payload, resolution


def _snapshot_ref(trace: dict[str, object], snapshot_id: str) -> dict[str, str]:
    snapshot = next(
        row
        for row in trace["snapshots"]  # type: ignore[union-attr]
        if row["snapshot_id"] == snapshot_id
    )
    return {"path": snapshot["path"], "identity": snapshot["identity"]}


def _sync_event_evidence(trace: dict[str, object], event: dict[str, object]) -> None:
    snapshot_ids = set(event["input_snapshot_ids"]) | set(event["output_snapshot_ids"])  # type: ignore[arg-type]
    if event["stage"].endswith("-review"):  # type: ignore[union-attr]
        bundle_id = event["output_snapshot_ids"][0]  # type: ignore[index]
        bundle = trace["review_bundles"][bundle_id]  # type: ignore[index]
        for reference in bundle["artifact_refs"].values():
            snapshot_ids.add(
                next(
                    row["snapshot_id"]
                    for row in trace["snapshots"]  # type: ignore[union-attr]
                    if row["path"] == reference["path"]
                    and row["identity"] == reference["identity"]
                )
            )
    event["evidence_refs"] = sorted(
        (_snapshot_ref(trace, snapshot_id) for snapshot_id in snapshot_ids),
        key=lambda reference: (reference["path"], reference["identity"]),
    )


def _trim_trace_to_event_snapshots(
    trace: dict[str, object],
    *,
    trim_inventory: bool,
) -> None:
    retained: set[str] = set()
    for event in trace["events"]:  # type: ignore[union-attr]
        retained.update(event["input_snapshot_ids"])
        retained.update(event["output_snapshot_ids"])
        if event["stage"].endswith("-review"):
            bundle = trace["review_bundles"][event["output_snapshot_ids"][0]]  # type: ignore[index]
            for reference in bundle["artifact_refs"].values():
                retained.add(
                    next(
                        snapshot["snapshot_id"]
                        for snapshot in trace["snapshots"]  # type: ignore[union-attr]
                        if snapshot["path"] == reference["path"]
                        and snapshot["identity"] == reference["identity"]
                    )
                )
    trace["snapshots"] = [  # type: ignore[index]
        snapshot
        for snapshot in trace["snapshots"]  # type: ignore[union-attr]
        if snapshot["snapshot_id"] in retained
    ]
    trace["review_bundles"] = {  # type: ignore[index]
        snapshot_id: bundle
        for snapshot_id, bundle in trace["review_bundles"].items()  # type: ignore[union-attr]
        if snapshot_id in retained
    }
    if trim_inventory:
        retained_paths = {
            snapshot["path"] for snapshot in trace["snapshots"]  # type: ignore[union-attr]
        }
        trace["after_inventory"] = [  # type: ignore[index]
            row
            for row in trace["after_inventory"]  # type: ignore[union-attr]
            if row["path"] in retained_paths
        ]


class BoundaryProofModelTests(unittest.TestCase):
    def test_boundary_activation_requires_complete_identity_or_rollback(
        self,
    ) -> None:
        identity = "sha256:" + "a" * 64
        release_root = (
            ROOT / "tests" / "fixtures" / "boundary-proof" / "release"
        )
        self.assertEqual(
            "activated",
            validate_boundary_activation_notes(
                (
                    release_root
                    / "valid-activation"
                    / "release-notes.md"
                ).read_text(encoding="utf-8"),
                report_identity=identity,
            ),
        )
        self.assertEqual(
            "rolled-back",
            validate_boundary_activation_notes(
                (
                    release_root
                    / "valid-rollback"
                    / "release-notes.md"
                ).read_text(encoding="utf-8"),
            ),
        )
        for text in (
            (
                release_root
                / "invalid-partial-activation"
                / "release-notes.md"
            ).read_text(encoding="utf-8"),
            f"Boundary capability report identity: {identity}\n",
            "Boundary model activation: unknown\n",
            "Boundary model activation: rolled-back\n",
        ):
            with self.subTest(text=text):
                with self.assertRaises(BoundaryProofError):
                    validate_boundary_activation_notes(
                        text,
                        report_identity=identity,
                    )

    def test_projection_is_closed_and_frozen(self) -> None:
        self.assertEqual(len(CORE_DIMENSION_IDS), 12)
        self.assertEqual(len(EVALUATED_SKILLS), 8)
        self.assertEqual(len(CHECK_IDS), 6)
        self.assertEqual(len(FIXTURE_GATES), 8)
        self.assertEqual(APPLICABILITY_VALUES, ("applicable", "not-applicable"))
        self.assertEqual(
            EXAMPLE_ROLES,
            ("illustration", "regression", "discovery", "non-normative"),
        )
        self.assertEqual(
            RESULT_VALUES,
            ("pass", "fail", "not-run"),
        )
        self.assertEqual(
            AUTOMATION_LEVELS,
            ("automated", "manual", "hybrid"),
        )
        self.assertIn("composed-path", INTERACTION_RATIONALES)
        normalized = normalize_feature_model(_feature_model())
        with self.assertRaises(dataclasses.FrozenInstanceError):
            normalized.core_dimensions[0].applicability = "other"  # type: ignore[misc]

    def test_runtime_projection_binds_exact_implementation_bytes(self) -> None:
        self.assertEqual(len(RUNTIME_PROJECTIONS), 1)
        projection = dict(RUNTIME_PROJECTIONS[0])
        self.assertEqual(set(projection), RUNTIME_PROJECTION_FIELDS)
        self.assertEqual(
            projection["projection_id"],
            "codex-0.145.0-readonly-boundary-v1",
        )
        self.assertEqual(
            runtime_projection_identity(projection),
            "sha256:ab6416627d461e3f11a2bc0d16d465ae8601478a8d085b64e86a6945931a4624",
        )
        self.assertEqual(
            projection["permitted_tool_features"],
            ("shell_snapshot", "shell_tool", "unified_exec"),
        )
        self.assertEqual(
            projection["permitted_non_tool_features"],
            (
                "terminal_resize_reflow",
                "tool_search_always_defer_mcp_tools",
                "resize_all_images",
                "tui_app_server",
            ),
        )
        self.assertEqual(len(projection["required_disabled_features"]), 89)
        selected = select_runtime_projection(
            runtime_version=str(projection["runtime_version"]),
            runtime_launcher_identity=str(
                projection["runtime_launcher_identity"]
            ),
            runtime_package_identity=str(
                projection["runtime_package_identity"]
            ),
            schema_bundle_identity=str(projection["schema_bundle_identity"]),
            protocol_item_classification_identity=str(
                projection["protocol_item_classification_identity"]
            ),
            feature_classification_identity=str(
                projection["feature_classification_identity"]
            ),
        )
        self.assertEqual(selected, projection)

        with self.assertRaises(BoundaryProofError):
            select_runtime_projection(
                runtime_version=str(projection["runtime_version"]),
                runtime_launcher_identity="sha256:" + "0" * 64,
                runtime_package_identity=str(
                    projection["runtime_package_identity"]
                ),
                schema_bundle_identity=str(
                    projection["schema_bundle_identity"]
                ),
                protocol_item_classification_identity=str(
                    projection["protocol_item_classification_identity"]
                ),
                feature_classification_identity=str(
                    projection["feature_classification_identity"]
                ),
            )

        for left, right in (
            ("permitted_tool_features", "permitted_non_tool_features"),
            ("permitted_tool_features", "required_disabled_features"),
            ("permitted_non_tool_features", "required_disabled_features"),
        ):
            with self.subTest(left=left, right=right):
                swapped = copy.deepcopy(projection)
                left_values = list(swapped[left])
                right_values = list(swapped[right])
                left_values[0], right_values[0] = (
                    right_values[0],
                    left_values[0],
                )
                swapped[left] = tuple(left_values)
                swapped[right] = tuple(right_values)
                with (
                    mock.patch(
                        "boundary_proof_model.RUNTIME_PROJECTIONS",
                        (swapped,),
                    ),
                    self.assertRaises(BoundaryProofError),
                ):
                    select_runtime_projection(
                        runtime_version=str(swapped["runtime_version"]),
                        runtime_launcher_identity=str(
                            swapped["runtime_launcher_identity"]
                        ),
                        runtime_package_identity=str(
                            swapped["runtime_package_identity"]
                        ),
                        schema_bundle_identity=str(
                            swapped["schema_bundle_identity"]
                        ),
                        protocol_item_classification_identity=str(
                            swapped[
                                "protocol_item_classification_identity"
                            ]
                        ),
                        feature_classification_identity=str(
                            swapped["feature_classification_identity"]
                        ),
                    )

    def test_handler_conformance_is_closed_and_identity_bound(self) -> None:
        authorization_identity = "sha256:" + "a" * 64
        policy = handler_conformance_policy(authorization_identity)
        self.assertEqual(tuple(policy["cases"]), HANDLER_CONFORMANCE_CASES)
        policy_identity = "sha256:" + hashlib.sha256(
            json.dumps(
                policy,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()
        result = {
            "schema_version": (
                "stage-file-change-handler-conformance-result-v1"
            ),
            "policy_identity": policy_identity,
            "case_results": [
                {"case": case, "result": "pass"}
                for case in HANDLER_CONFORMANCE_CASES
            ],
            "result": "pass",
        }
        result["result_identity"] = "sha256:" + hashlib.sha256(
            json.dumps(
                result,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()
        self.assertEqual(
            validate_handler_conformance(
                policy,
                result,
                authorization_policy_identity=authorization_identity,
            ),
            result["result_identity"],
        )

        reordered = copy.deepcopy(result)
        reordered["case_results"].reverse()
        with self.assertRaises(BoundaryProofError):
            validate_handler_conformance(
                policy,
                reordered,
                authorization_policy_identity=authorization_identity,
            )

    def test_production_handler_passes_every_closed_conformance_case(
        self,
    ) -> None:
        result = _run_file_change_handler_conformance(
            FILE_CHANGE_AUTHORIZATION_POLICY
        )
        self.assertEqual(result["result"], "pass")
        self.assertEqual(
            [row["case"] for row in result["case_results"]],
            list(HANDLER_CONFORMANCE_CASES),
        )

        malformed = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "item/fileChange/requestApproval",
            "params": {
                "grantRoot": None,
                "itemId": "item",
                "reason": None,
                "startedAtMs": True,
                "threadId": "thread",
                "turnId": "turn",
            },
        }
        response, failure = _dispatch_file_change_request(
            malformed,
            policy=FILE_CHANGE_AUTHORIZATION_POLICY,
            expected_thread_id="thread",
            expected_turn_id="turn",
            expected_item_id="item",
            expected_change_identity="sha256:" + "a" * 64,
            observed_change_identity="sha256:" + "a" * 64,
            decision_handler=lambda: {"decision": "decline"},
        )
        self.assertIsNone(response)
        self.assertEqual(failure, "malformed-request")

    def test_effective_tool_projection_excludes_permitted_non_tool_behavior(
        self,
    ) -> None:
        projection = dict(RUNTIME_PROJECTIONS[0])
        permitted_tools = set(projection["permitted_tool_features"])
        permitted_non_tools = set(
            projection["permitted_non_tool_features"]
        )
        disabled = set(projection["required_disabled_features"])
        pages = [
            {
                "items": [
                    {
                        "name": feature,
                        "enabled": feature
                        in permitted_tools | permitted_non_tools,
                    }
                    for feature in CODEX_0_145_0_FEATURES
                ],
                "next_cursor": None,
            }
        ]
        classifications = [
            {
                "feature": feature,
                "classification": (
                    "permitted-built-in-tool"
                    if feature in permitted_tools
                    else (
                        "permitted-non-tool-runtime-behavior"
                        if feature in permitted_non_tools
                        else "must-be-disabled-tool-bearing-behavior"
                    )
                ),
            }
            for feature in sorted(CODEX_0_145_0_FEATURES)
        ]
        effective = _effective_tool_projection(
            pages, classifications, projection
        )
        self.assertEqual(len(effective), len(permitted_tools | disabled))
        self.assertTrue(
            permitted_non_tools.isdisjoint(
                {str(row["feature"]) for row in effective}
            )
        )
        self.assertEqual(
            {str(row["feature"]) for row in effective if row["enabled"]},
            permitted_tools,
        )

    def test_unknown_closed_values_fail_before_consistency(self) -> None:
        cases = (
            ("dimension_id", "unknown-dimension", "unknown core dimension"),
            ("applicability", "sometimes", "unknown applicability"),
        )
        for field, value, message in cases:
            with self.subTest(field=field):
                model = _feature_model()
                model["core_dimensions"] = [dict(row) for row in _core_rows()]
                model["core_dimensions"][0][field] = value  # type: ignore[index]
                model["core_dimensions"] = model["core_dimensions"][:1]  # type: ignore[index]
                with self.assertRaisesRegex(BoundaryProofError, message):
                    normalize_feature_model(model)

        bad_version = _feature_model()
        bad_version["boundary_model_version"] = "v2"
        with self.assertRaisesRegex(BoundaryProofError, "unknown boundary-model version"):
            normalize_feature_model(bad_version)

        for role in ("example", "interaction"):
            with self.subTest(record=role):
                model = _feature_model()
                if role == "example":
                    model["examples"][0]["role"] = "walkthrough"  # type: ignore[index]
                    message = "unknown example role"
                else:
                    model["interactions"][0]["rationale"] = "convenient"  # type: ignore[index]
                    message = "unknown interaction rationale"
                with self.assertRaisesRegex(BoundaryProofError, message):
                    normalize_feature_model(model)

        feature = normalize_feature_model(_feature_model())
        bad_level = _proof_map()
        bad_level["proof_obligations"][0]["automation_level"] = "semi-auto"  # type: ignore[index]
        with self.assertRaisesRegex(BoundaryProofError, "unknown automation level"):
            normalize_proof_map(bad_level, feature)

        bad_check = _report()
        bad_check["required_check_ids"][-1] = "boundary-unknown"  # type: ignore[index]
        with self.assertRaisesRegex(BoundaryProofError, "unknown required check ID"):
            validate_capability_report(bad_check)

        bad_result = _report()
        bad_result["checks"]["boundary-traceability"]["result"] = "skipped"  # type: ignore[index]
        with self.assertRaisesRegex(BoundaryProofError, "unknown result"):
            validate_capability_report(bad_result)

    def test_core_rows_require_exact_fields_uniqueness_and_conditional_values(self) -> None:
        normalized = normalize_feature_model(_feature_model())
        self.assertEqual(
            {row.dimension_id for row in normalized.core_dimensions},
            set(CORE_DIMENSION_IDS),
        )
        self.assertTrue(
            all(isinstance(row, CoreBoundaryEntry) for row in normalized.core_dimensions)
        )

        missing = _feature_model()
        missing["core_dimensions"] = missing["core_dimensions"][:-1]  # type: ignore[index]
        with self.assertRaisesRegex(BoundaryProofError, "missing core dimensions"):
            normalize_feature_model(missing)

        duplicate = _feature_model()
        duplicate["core_dimensions"] = [  # type: ignore[index]
            *duplicate["core_dimensions"],  # type: ignore[misc]
            dict(duplicate["core_dimensions"][0]),  # type: ignore[index]
        ]
        with self.assertRaisesRegex(BoundaryProofError, "duplicate core dimension"):
            normalize_feature_model(duplicate)

        extra = _feature_model()
        extra["core_dimensions"][0]["extra"] = True  # type: ignore[index]
        with self.assertRaisesRegex(BoundaryProofError, "unexpected fields"):
            normalize_feature_model(extra)

        not_applicable = _feature_model()
        row = not_applicable["core_dimensions"][7]  # type: ignore[index]
        row["applicability"] = "not-applicable"
        row["governing_requirement_ids"] = []
        row["boundary_ids"] = []
        row["non_applicability_rationale"] = "No durable mutation exists."
        normalize_feature_model(not_applicable)

    def test_extensions_examples_and_interactions_follow_closed_contracts(self) -> None:
        model = _feature_model()
        model["extensions"] = [
            {
                "extension_id": "x.sample.rate-limit",
                "title": "Rate limit",
                "applicability": "applicable",
                "rationale": "External quota changes outcomes.",
                "governing_requirement_ids": ["R2"],
                "boundary_ids": ["sample.extension.rate-limit"],
                "non_applicability_rationale": None,
            }
        ]
        normalize_feature_model(model)

        invalid = _feature_model()
        invalid["extensions"] = [
            {
                "extension_id": "other",
                "title": "Other",
                "applicability": "applicable",
                "rationale": "Catch all",
                "governing_requirement_ids": ["R2"],
                "boundary_ids": ["sample.extension.other"],
                "non_applicability_rationale": None,
            }
        ]
        with self.assertRaisesRegex(BoundaryProofError, "invalid extension ID"):
            normalize_feature_model(invalid)

        bad_interaction = _feature_model()
        bad_interaction["interactions"][0]["boundary_ids"] = [  # type: ignore[index]
            "sample.identity-freshness"
        ]
        with self.assertRaisesRegex(BoundaryProofError, "at least two"):
            normalize_feature_model(bad_interaction)

        invalid_regression = _feature_model()
        invalid_regression["examples"][1]["regression_id"] = "Not Stable!"  # type: ignore[index]
        with self.assertRaisesRegex(BoundaryProofError, "invalid regression ID"):
            normalize_feature_model(invalid_regression)

        duplicate_regression = _feature_model()
        duplicate_row = copy.deepcopy(duplicate_regression["examples"][1])  # type: ignore[index]
        duplicate_row["example_id"] = "sample.example.regression-two"
        duplicate_regression["examples"].append(duplicate_row)  # type: ignore[union-attr]
        with self.assertRaisesRegex(BoundaryProofError, "duplicate regression ID"):
            normalize_feature_model(duplicate_regression)

        invalid_gap = _feature_model()
        invalid_gap["examples"][2]["discovery_gap"] = "not stable"  # type: ignore[index]
        with self.assertRaisesRegex(BoundaryProofError, "invalid discovery gap ID"):
            normalize_feature_model(invalid_gap)

    def test_proof_map_requires_version_scope_and_complete_references(self) -> None:
        feature = normalize_feature_model(_feature_model())
        proof = normalize_proof_map(_proof_map(), feature)
        self.assertEqual(len(proof.proof_obligations), 13)

        mismatched = _proof_map()
        mismatched["boundary_model_version"] = "legacy"
        with self.assertRaisesRegex(BoundaryProofError, "version mismatch"):
            normalize_proof_map(mismatched, feature)

        omitted = _proof_map()
        omitted["proof_obligations"] = omitted["proof_obligations"][:-2]  # type: ignore[index]
        with self.assertRaisesRegex(BoundaryProofError, "unmapped boundary"):
            normalize_proof_map(omitted, feature)

        orphan = _proof_map()
        orphan["proof_obligations"][0]["boundary_or_interaction_ids"] = [  # type: ignore[index]
            "sample.missing"
        ]
        with self.assertRaisesRegex(BoundaryProofError, "orphan boundary"):
            normalize_proof_map(orphan, feature)

        bad_manual = _proof_map()
        bad_manual["proof_obligations"][-1]["manual_procedure_ids"] = []  # type: ignore[index]
        with self.assertRaisesRegex(BoundaryProofError, "manual procedure"):
            normalize_proof_map(bad_manual, feature)

        unapproved = _proof_map()
        unapproved["proof_obligations"][0]["governing_requirement_ids"] = ["R999"]  # type: ignore[index]
        with self.assertRaisesRegex(BoundaryProofError, "unapproved governing requirement"):
            normalize_proof_map(unapproved, feature)

        unrelated_known = _feature_model()
        unrelated_known["core_dimensions"][0]["governing_requirement_ids"] = ["R1"]  # type: ignore[index]
        unrelated_known["core_dimensions"][1]["governing_requirement_ids"] = ["R2"]  # type: ignore[index]
        unrelated_known["examples"][1]["governing_requirement_ids"] = ["R2"]  # type: ignore[index]
        unrelated_feature = normalize_feature_model(unrelated_known)
        unrelated_proof = _proof_map()
        unrelated_proof["proof_obligations"][1]["governing_requirement_ids"] = ["R2"]  # type: ignore[index]
        unrelated_proof["proof_obligations"][0]["governing_requirement_ids"] = ["R2"]  # type: ignore[index]
        with self.assertRaisesRegex(BoundaryProofError, "does not own cited reference"):
            normalize_proof_map(unrelated_proof, unrelated_feature)

        mixed = _proof_map()
        mixed["proof_obligations"][0]["boundary_or_interaction_ids"] = [  # type: ignore[index]
            "sample.canonical-trust",
            "sample.identity-freshness",
        ]
        mixed["proof_obligations"][0]["governing_requirement_ids"] = ["R1"]  # type: ignore[index]
        with self.assertRaisesRegex(BoundaryProofError, "lacks governing requirement overlap"):
            normalize_proof_map(mixed, unrelated_feature)

    def test_legacy_and_v1_version_parity_is_prospective(self) -> None:
        self.assertEqual(
            validate_version_parity(
                None,
                None,
                None,
                None,
                public_activation=False,
                explicitly_reviewed_opt_in=False,
            ),
            "legacy",
        )
        self.assertEqual(
            validate_version_parity(
                "v1",
                "R1-R9",
                "v1",
                "R1-R9",
                public_activation=False,
                explicitly_reviewed_opt_in=True,
            ),
            "v1",
        )
        with self.assertRaisesRegex(BoundaryProofError, "version mismatch"):
            validate_version_parity(
                "v1",
                "R1-R9",
                "legacy",
                None,
                public_activation=False,
                explicitly_reviewed_opt_in=True,
            )
        with self.assertRaisesRegex(BoundaryProofError, "reviewed opt-in"):
            validate_version_parity(
                "v1",
                "R1-R9",
                "v1",
                "R1-R9",
                public_activation=False,
                explicitly_reviewed_opt_in=False,
            )
        for arguments, message in (
            ((None, "R1-R9", None, None), "markerless legacy"),
            ((None, None, "legacy", "R1-R9"), "marker presence mismatch"),
            (("legacy", "R1-R9", "legacy", "R2-R9"), "scope mismatch"),
            (("legacy", None, "legacy", None), "scope is invalid"),
        ):
            with self.subTest(arguments=arguments):
                with self.assertRaisesRegex(BoundaryProofError, message):
                    validate_version_parity(
                        *arguments,
                        public_activation=False,
                        explicitly_reviewed_opt_in=False,
                    )
        self.assertEqual(
            validate_version_parity(
                "legacy",
                "R1-R9",
                "legacy",
                "R1-R9",
                public_activation=False,
                explicitly_reviewed_opt_in=False,
            ),
            "legacy",
        )

    def test_incident_registry_is_exact_and_evidence_bound(self) -> None:
        payload = json.loads((FIXTURES / "incident-registry.json").read_text())
        results = validate_incident_registry(payload)
        self.assertEqual(len(results), 8)
        self.assertTrue(all(not result.escaped_to_code_review for result in results))
        self.assertTrue(all(not result.sibling_bypass_remaining for result in results))
        payload["fixtures"][0]["fixture_id"] = "BFP-FX-UNKNOWN-001"
        with self.assertRaisesRegex(BoundaryProofError, "unknown fixture"):
            validate_incident_registry(payload)

    def test_each_incident_derives_from_state_not_fixture_labels(self) -> None:
        for fixture_id, rule in INCIDENT_RULES.items():
            with self.subTest(fixture_id=fixture_id):
                path = FIXTURES / "incidents" / f"{fixture_id}.json"
                fixture = json.loads(path.read_text())
                result = validate_incident_fixture(fixture)
                self.assertEqual(result.detected_stage, rule[4])
                self.assertEqual(result.diagnostic_id, rule[5])

                for field, replacement in (
                    ("seeded_omission", "different omission"),
                    ("expected_gate", "spec"),
                    ("expected_diagnostic", "different-diagnostic"),
                ):
                    changed = copy.deepcopy(fixture)
                    changed[field] = replacement
                    with self.assertRaisesRegex(BoundaryProofError, "closed registry mismatch"):
                        validate_incident_fixture(changed)

                state_only = evaluate_boundary_state(fixture["boundary_state"])
                relabeled = copy.deepcopy(fixture)
                relabeled["fixture_id"] = next(
                    candidate for candidate in INCIDENT_RULES if candidate != fixture_id
                )
                self.assertEqual(
                    evaluate_boundary_state(relabeled["boundary_state"]),
                    state_only,
                )

                multi = copy.deepcopy(fixture["boundary_state"])
                other = next(
                    value
                    for value in INCIDENT_RULES.values()
                    if value[1] != rule[1]
                )
                multi[other[1]] = other[2]
                with self.assertRaisesRegex(BoundaryProofError, "multiple seeded triggers"):
                    evaluate_boundary_state(multi)

    def test_capability_report_result_is_computed_not_asserted(self) -> None:
        passing = _report()
        self.assertEqual(capability_report_result(passing), "pass")
        validate_capability_report(passing)

        def not_run(report: dict[str, object]) -> None:
            report["checks"]["boundary-traceability"].update(  # type: ignore[index]
                result="not-run",
                evidence_refs=[],
                blocking_reason={
                    "code": "prerequisite-unsatisfied",
                    "detail": "Synthetic prerequisite omitted.",
                },
            )

        for mutation in (
            not_run,
            lambda report: report["fixtures"][0].update(escaped_to_code_review=True),  # type: ignore[index]
            lambda report: report["fixtures"][1].update(sibling_bypass_remaining=True),  # type: ignore[index]
            lambda report: report["fixtures"][2].update(detected_stage="not-detected"),  # type: ignore[index]
            lambda report: report.update(false_blocking_count=1),
            lambda report: report.update(duplicate_normative_owner_count=1),
            lambda report: report.update(new_universal_artifact_count=1),
            lambda report: report.update(simple_fixture_structure_correction_cycles=2),
        ):
            with self.subTest(mutation=mutation):
                report = _report()
                mutation(report)
                report["overall_result"] = "fail"
                self.assertEqual(capability_report_result(report), "fail")
                validate_capability_report(report)

        asserted = _report("fail")
        asserted["overall_result"] = "pass"
        with self.assertRaisesRegex(BoundaryProofError, "does not match computed"):
            validate_capability_report(asserted)

    def test_report_rows_require_current_repository_visible_evidence(self) -> None:
        report = _report()
        report["checks"]["boundary-traceability"]["evidence_refs"] = []  # type: ignore[index]
        with self.assertRaisesRegex(BoundaryProofError, "evidence_refs"):
            validate_capability_report(report)

        missing = _report()
        missing["checks"]["boundary-traceability"]["evidence_refs"] = [  # type: ignore[index]
            {
                "path": "docs/does-not-exist.md",
                "identity": "sha256:" + "0" * 64,
            }
        ]
        with self.assertRaisesRegex(BoundaryProofError, "missing"):
            validate_capability_report(missing)

        stale = _report()
        stale["checks"]["boundary-traceability"]["evidence_refs"][0]["identity"] = (  # type: ignore[index]
            "sha256:" + "0" * 64
        )
        with self.assertRaisesRegex(BoundaryProofError, "stale or substituted"):
            validate_capability_report(stale)

        unsafe = _report()
        unsafe["checks"]["boundary-traceability"]["evidence_refs"][0]["path"] = "../outside"  # type: ignore[index]
        with self.assertRaisesRegex(BoundaryProofError, "unsafe evidence path"):
            validate_capability_report(unsafe)

        bad_not_run = _report("not-run")
        bad_not_run["checks"]["boundary-traceability"]["blocking_reason"] = None  # type: ignore[index]
        with self.assertRaisesRegex(BoundaryProofError, "expected object"):
            validate_capability_report(bad_not_run)

        unknown_blocker = _report("not-run")
        unknown_blocker["checks"]["boundary-traceability"]["blocking_reason"]["code"] = "later"  # type: ignore[index]
        with self.assertRaisesRegex(BoundaryProofError, "unknown blocking reason"):
            validate_capability_report(unknown_blocker)

        with tempfile.TemporaryDirectory() as raw:
            repository = Path(raw)
            subprocess.run(
                ["git", "init", "-q", str(repository)],
                check=True,
            )
            tracked = repository / "tracked-proof.md"
            tracked.write_text("tracked proof\n")
            subprocess.run(
                ["git", "-C", str(repository), "add", "tracked-proof.md"],
                check=True,
            )
            tracked_reference = {
                "path": "tracked-proof.md",
                "identity": "sha256:"
                + hashlib.sha256(tracked.read_bytes()).hexdigest(),
            }
            tracked_report = _report()
            _set_all_report_evidence(tracked_report, tracked_reference)
            validate_capability_report(
                tracked_report,
                repository_root=repository,
            )

            scratch = repository / "untracked-review-scratch.bin"
            scratch.write_bytes(b"caller scratch")
            scratch_reference = {
                "path": "untracked-review-scratch.bin",
                "identity": "sha256:"
                + hashlib.sha256(scratch.read_bytes()).hexdigest(),
            }
            untracked = _report()
            _set_all_report_evidence(untracked, scratch_reference)
            with self.assertRaisesRegex(
                BoundaryProofError,
                "tracked or current change-local",
            ):
                validate_capability_report(untracked, repository_root=repository)

            change_local = (
                repository
                / "docs"
                / "changes"
                / "2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills"
                / "proof.md"
            )
            change_local.parent.mkdir(parents=True)
            change_local.write_text("change-local proof\n")
            change_reference = {
                "path": change_local.relative_to(repository).as_posix(),
                "identity": "sha256:"
                + hashlib.sha256(change_local.read_bytes()).hexdigest(),
            }
            local_report = _report()
            _set_all_report_evidence(local_report, change_reference)
            validate_capability_report(local_report, repository_root=repository)

            real = repository / "real"
            real.mkdir()
            linked_file = real / "proof.md"
            linked_file.write_text("linked proof\n")
            (repository / "linked").symlink_to(real, target_is_directory=True)
            linked_reference = {
                "path": "linked/proof.md",
                "identity": "sha256:"
                + hashlib.sha256(linked_file.read_bytes()).hexdigest(),
            }
            linked_report = _report()
            _set_all_report_evidence(linked_report, linked_reference)
            with self.assertRaisesRegex(BoundaryProofError, "non-symlink"):
                validate_capability_report(linked_report, repository_root=repository)

    def test_simple_fixture_is_compact_and_requires_at_most_one_cycle(self) -> None:
        payload = json.loads((FIXTURES / "simple-change.json").read_text())
        feature = normalize_feature_model(payload["feature_model"])
        proof = normalize_proof_map(payload["proof_map"], feature)
        self.assertEqual(len(feature.core_dimensions), 12)
        metrics = evaluate_simple_change_trace(
            payload["simple_trace"],
            feature_models={"simple.snapshot.feature.v1": feature},
            proof_maps={"simple.snapshot.test-spec.v1": proof},
            structural_evaluations=_structural_evaluations(
                payload["simple_trace"]
            ),
        )
        self.assertEqual(metrics.new_universal_artifact_count, 0)
        self.assertEqual(metrics.false_blocking_count, 0)
        self.assertLessEqual(metrics.structure_only_correction_cycles, 1)
        self.assertTrue(metrics.applicable_only_mapping)

        false_block = copy.deepcopy(payload["simple_trace"])
        false_block["events"][1].update(  # type: ignore[index]
            observed_result="blocked",
            diagnostic_id="simple.diagnostic.review-blocked",
        )
        false_block["review_bundles"]["simple.snapshot.spec-review.bundle.v1"].update(  # type: ignore[index]
            outcome="blocked",
            material_finding_ids=["simple.finding.blocked"],
        )
        false_block["snapshots"].append(  # type: ignore[union-attr]
            {
                "snapshot_id": "simple.snapshot.spec-review.resolution.v1",
                "source": "behavior-output",
                "artifact_role": "review-evidence",
                "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/simple-change/runs/run-11111111111111111111111111111111/artifacts/review-evidence/spec-review-resolution.md",
                "identity": "sha256:" + "9" * 64,
            }
        )
        false_block["review_bundles"]["simple.snapshot.spec-review.bundle.v1"][  # type: ignore[index]
            "artifact_refs"
        ]["review-resolution"] = _snapshot_ref(  # type: ignore[index]
            false_block,
            "simple.snapshot.spec-review.resolution.v1",
        )
        false_block["events"] = false_block["events"][:2]  # type: ignore[index]
        _trim_trace_to_event_snapshots(false_block, trim_inventory=False)
        _sync_event_evidence(false_block, false_block["events"][1])  # type: ignore[index]
        allowed_paths = {
            snapshot_id
            for event in false_block["events"]  # type: ignore[union-attr]
            for snapshot_id in event["output_snapshot_ids"]
        }
        allowed_paths.update(
            (
                "simple.snapshot.spec-review.record.v1",
                "simple.snapshot.spec-review.log.v1",
                "simple.snapshot.spec-review.resolution.v1",
            )
        )
        false_block["after_inventory"] = sorted(  # type: ignore[index]
            (
                {
                    "path": snapshot["path"],
                    "artifact_kind": snapshot["artifact_role"],
                    "identity": snapshot["identity"],
                }
                for snapshot in false_block["snapshots"]  # type: ignore[union-attr]
                if snapshot["snapshot_id"] in allowed_paths
            ),
            key=lambda row: row["path"],
        )
        self.assertEqual(
            evaluate_simple_change_trace(
                false_block,
                structural_evaluations=_structural_evaluations(false_block),
            ).false_blocking_count,
            1,
        )

        universal = copy.deepcopy(payload["simple_trace"])
        universal["after_inventory"].append(  # type: ignore[union-attr]
            {
                "path": "docs/plans/new-required.md",
                "artifact_kind": "other-lifecycle",
                "identity": "sha256:" + "a" * 64,
            }
        )
        universal["after_inventory"].sort(key=lambda row: row["path"])  # type: ignore[union-attr]
        self.assertEqual(
            evaluate_simple_change_trace(
                universal,
                feature_models={"simple.snapshot.feature.v1": feature},
                proof_maps={"simple.snapshot.test-spec.v1": proof},
                structural_evaluations=_structural_evaluations(universal),
            ).new_universal_artifact_count,
            1,
        )

        extra_feature = copy.deepcopy(payload["simple_trace"])
        extra_feature["after_inventory"].append(  # type: ignore[union-attr]
            {
                "path": "specs/unproduced-feature.md",
                "artifact_kind": "feature-spec",
                "identity": "sha256:" + "b" * 64,
            }
        )
        extra_feature["after_inventory"].sort(key=lambda row: row["path"])  # type: ignore[union-attr]
        self.assertEqual(
            evaluate_simple_change_trace(
                extra_feature,
                feature_models={"simple.snapshot.feature.v1": feature},
                proof_maps={"simple.snapshot.test-spec.v1": proof},
                structural_evaluations=_structural_evaluations(extra_feature),
            ).new_universal_artifact_count,
            1,
        )

        classified_extras = (
            ("specs/extra-feature.md", "feature-spec", "c"),
            ("specs/extra-proof.test.md", "test-spec", "d"),
            (
                "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/extra-review.md",
                "review-evidence",
                "e",
            ),
            ("docs/plans/extra-plan.md", "other-lifecycle", "f"),
        )
        for path, artifact_kind, digit in classified_extras:
            with self.subTest(artifact_kind=artifact_kind):
                candidate = copy.deepcopy(payload["simple_trace"])
                candidate["after_inventory"].append(
                    {
                        "path": path,
                        "artifact_kind": artifact_kind,
                        "identity": "sha256:" + digit * 64,
                    }
                )
                candidate["after_inventory"].sort(key=lambda row: row["path"])
                self.assertEqual(
                    evaluate_simple_change_trace(
                        candidate,
                        feature_models={"simple.snapshot.feature.v1": feature},
                        proof_maps={"simple.snapshot.test-spec.v1": proof},
                        structural_evaluations=_structural_evaluations(candidate),
                    ).new_universal_artifact_count,
                    1,
                )

    def test_simple_trace_rejects_invalid_diagnostics_and_linkage(self) -> None:
        payload = json.loads((FIXTURES / "simple-change.json").read_text())
        cases = []

        authoring_diagnostic = copy.deepcopy(payload)
        authoring_diagnostic["simple_trace"]["events"][0][
            "diagnostic_id"
        ] = "simple.diagnostic.unexpected"
        cases.append((authoring_diagnostic, "authoring diagnostic mismatch"))

        review_without_diagnostic = copy.deepcopy(payload)
        review_without_diagnostic["simple_trace"]["events"][1].update(
            observed_result="blocked",
            diagnostic_id="none",
        )
        review_without_diagnostic["simple_trace"]["snapshots"].append(
            {
                "snapshot_id": "simple.snapshot.spec-review.resolution.no-diagnostic",
                "source": "behavior-output",
                "artifact_role": "review-evidence",
                "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/simple-change/runs/run-11111111111111111111111111111111/artifacts/review-evidence/spec-review-resolution-no-diagnostic.md",
                "identity": "sha256:" + "e" * 64,
            }
        )
        no_diagnostic_bundle = review_without_diagnostic["simple_trace"][
            "review_bundles"
        ]["simple.snapshot.spec-review.bundle.v1"]
        no_diagnostic_bundle.update(
            outcome="blocked",
            material_finding_ids=["simple.finding.no-diagnostic"],
        )
        no_diagnostic_bundle["artifact_refs"][
            "review-resolution"
        ] = _snapshot_ref(
            review_without_diagnostic["simple_trace"],
            "simple.snapshot.spec-review.resolution.no-diagnostic",
        )
        _sync_event_evidence(
            review_without_diagnostic["simple_trace"],
            review_without_diagnostic["simple_trace"]["events"][1],
        )
        cases.append(
            (
                review_without_diagnostic,
                "non-approval requires diagnostic",
            )
        )

        authoring_failure_without_diagnostic = copy.deepcopy(payload)
        authoring_failure_without_diagnostic["simple_trace"]["events"][0][
            "structural_result"
        ] = "fail"
        authoring_failure_without_diagnostic["simple_trace"]["events"] = (
            authoring_failure_without_diagnostic["simple_trace"]["events"][:1]
        )
        cases.append(
            (
                authoring_failure_without_diagnostic,
                "authoring diagnostic mismatch|result/diagnostic mismatch",
            )
        )

        broken_review_link = copy.deepcopy(payload)
        broken_review_link["simple_trace"]["events"][1][
            "reviewed_snapshot_id"
        ] = "simple.snapshot.test-spec.v1"
        cases.append((broken_review_link, "used before production|linkage mismatch"))

        bad_evidence_union = copy.deepcopy(payload)
        bad_evidence_union["simple_trace"]["events"][2]["evidence_refs"] = (
            bad_evidence_union["simple_trace"]["events"][2]["evidence_refs"][:-1]
        )
        cases.append((bad_evidence_union, "evidence reference union mismatch"))

        for candidate, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(BoundaryProofError, message):
                    _evaluate_simple(candidate)

        failed_approved = copy.deepcopy(payload)
        failed_approved["simple_trace"]["events"][1].update(
            structural_result="fail",
            observed_result="approved",
            diagnostic_id="simple.diagnostic.structural-failure",
        )
        with self.assertRaisesRegex(
            BoundaryProofError,
            "approved review requires no diagnostic|failed structure",
        ):
            _evaluate_simple(failed_approved)

        duplicate_review_input = copy.deepcopy(payload)
        duplicate_review_input["simple_trace"]["events"][1][
            "input_snapshot_ids"
        ].append("simple.snapshot.feature.v1")
        with self.assertRaisesRegex(
            BoundaryProofError,
            "duplicate snapshot ID|duplicate values",
        ):
            _evaluate_simple(duplicate_review_input)

        inventory_mismatch = copy.deepcopy(payload)
        inventory_mismatch["simple_trace"]["after_inventory"][0][
            "identity"
        ] = "sha256:" + "f" * 64
        with self.assertRaisesRegex(
            BoundaryProofError,
            "produced snapshot missing or mismatched",
        ):
            _evaluate_simple(inventory_mismatch)

        for path, claimed_kind in (
            ("docs/plans/evades-count.md", "non-lifecycle"),
            ("specs/evades-count.md", "non-lifecycle"),
        ):
            mislabeled = copy.deepcopy(payload)
            mislabeled["simple_trace"]["after_inventory"].append(
                {
                    "path": path,
                    "artifact_kind": claimed_kind,
                    "identity": "sha256:" + "c" * 64,
                }
            )
            mislabeled["simple_trace"]["after_inventory"].sort(
                key=lambda row: row["path"]
            )
            with self.assertRaisesRegex(
                BoundaryProofError,
                "closed path classifier",
            ):
                _evaluate_simple(mislabeled)

        duplicate_inventory_identity = copy.deepcopy(payload)
        duplicate_inventory_identity["simple_trace"]["after_inventory"].append(
            {
                "path": "notes/duplicate-content.txt",
                "artifact_kind": "non-lifecycle",
                "identity": "sha256:" + "1" * 64,
            }
        )
        duplicate_inventory_identity["simple_trace"]["after_inventory"].sort(
            key=lambda row: row["path"]
        )
        with self.assertRaisesRegex(BoundaryProofError, "duplicate inventory identity"):
            _evaluate_simple(duplicate_inventory_identity)

        orphan_snapshot = copy.deepcopy(payload)
        orphan_snapshot["simple_trace"]["snapshots"].append(
            {
                "snapshot_id": "simple.snapshot.orphan.output",
                "source": "behavior-output",
                "artifact_role": "review-evidence",
                "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/simple-change/runs/run-11111111111111111111111111111111/artifacts/review-evidence/orphan.md",
                "identity": "sha256:" + "c" * 64,
            }
        )
        with self.assertRaisesRegex(
            BoundaryProofError,
            "produced snapshot missing or mismatched",
        ):
            _evaluate_simple(orphan_snapshot)

        missing_final_model = copy.deepcopy(payload)
        with self.assertRaisesRegex(
            BoundaryProofError,
            "final approved snapshot model is missing",
        ):
            evaluate_simple_change_trace(
                missing_final_model["simple_trace"],
                feature_models={},
                proof_maps={},
                structural_evaluations=_structural_evaluations(
                    missing_final_model["simple_trace"]
                ),
            )

        unbound_failure_diagnostic = copy.deepcopy(payload["simple_trace"])
        unbound_failure_diagnostic["events"][0].update(
            structural_result="fail",
            diagnostic_id="simple.diagnostic.caller-selected",
        )
        unbound_failure_diagnostic["events"] = unbound_failure_diagnostic["events"][:1]
        _trim_trace_to_event_snapshots(
            unbound_failure_diagnostic,
            trim_inventory=True,
        )
        with self.assertRaisesRegex(
            BoundaryProofError,
            "structural diagnostic mismatch",
        ):
            evaluate_simple_change_trace(
                unbound_failure_diagnostic,
                structural_evaluations={
                    "spec#1": {
                        "structural_result": "fail",
                        "diagnostic_id": "simple.diagnostic.structural-owner",
                    }
                },
            )

    def test_simple_trace_accepts_closed_terminal_failure_branches(self) -> None:
        payload = json.loads((FIXTURES / "simple-change.json").read_text())

        authoring_failure = copy.deepcopy(payload["simple_trace"])
        authoring_failure["events"][0].update(
            structural_result="fail",
            diagnostic_id="simple.diagnostic.authoring-failure",
        )
        authoring_failure["events"] = authoring_failure["events"][:1]
        _trim_trace_to_event_snapshots(authoring_failure, trim_inventory=False)
        first_output = "simple.snapshot.feature.v1"
        authoring_failure["after_inventory"] = [
            {
                "path": _snapshot_ref(authoring_failure, first_output)["path"],
                "artifact_kind": "feature-spec",
                "identity": _snapshot_ref(authoring_failure, first_output)["identity"],
            }
        ]
        authoring_metrics = evaluate_simple_change_trace(
            authoring_failure,
            structural_evaluations=_structural_evaluations(authoring_failure),
        )
        self.assertFalse(authoring_metrics.applicable_only_mapping)
        self.assertEqual(authoring_metrics.false_blocking_count, 0)

        blocked = copy.deepcopy(payload["simple_trace"])
        blocked["snapshots"].append(
            {
                "snapshot_id": "simple.snapshot.spec-review.resolution.blocked",
                "source": "behavior-output",
                "artifact_role": "review-evidence",
                "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/simple-change/runs/run-11111111111111111111111111111111/artifacts/review-evidence/spec-review-resolution-blocked.md",
                "identity": "sha256:" + "f" * 64,
            }
        )
        bundle = blocked["review_bundles"]["simple.snapshot.spec-review.bundle.v1"]
        bundle.update(
            outcome="blocked",
            material_finding_ids=["simple.finding.structural-block"],
        )
        bundle["artifact_refs"]["review-resolution"] = _snapshot_ref(
            blocked,
            "simple.snapshot.spec-review.resolution.blocked",
        )
        blocked["events"][1].update(
            structural_result="fail",
            observed_result="blocked",
            diagnostic_id="simple.diagnostic.structural-block",
        )
        _sync_event_evidence(blocked, blocked["events"][1])
        blocked["events"] = blocked["events"][:2]
        _trim_trace_to_event_snapshots(blocked, trim_inventory=False)
        blocked_with_unproduced_inventory = copy.deepcopy(blocked)
        blocked_with_unproduced_inventory["after_inventory"].append(
            {
                "path": _snapshot_ref(
                    blocked_with_unproduced_inventory,
                    "simple.snapshot.spec-review.resolution.blocked",
                )["path"],
                "artifact_kind": "review-evidence",
                "identity": _snapshot_ref(
                    blocked_with_unproduced_inventory,
                    "simple.snapshot.spec-review.resolution.blocked",
                )["identity"],
            }
        )
        blocked_with_unproduced_inventory["after_inventory"].sort(
            key=lambda row: row["path"]
        )
        self.assertGreater(
            evaluate_simple_change_trace(
                blocked_with_unproduced_inventory,
                structural_evaluations=_structural_evaluations(
                    blocked_with_unproduced_inventory
                ),
            ).new_universal_artifact_count,
            0,
        )
        produced_ids = {
            "simple.snapshot.feature.v1",
            "simple.snapshot.spec-review.bundle.v1",
            "simple.snapshot.spec-review.record.v1",
            "simple.snapshot.spec-review.log.v1",
            "simple.snapshot.spec-review.resolution.blocked",
        }
        blocked["after_inventory"] = sorted(
            (
                {
                    "path": snapshot["path"],
                    "artifact_kind": snapshot["artifact_role"],
                    "identity": snapshot["identity"],
                }
                for snapshot in blocked["snapshots"]
                if snapshot["snapshot_id"] in produced_ids
            ),
            key=lambda row: row["path"],
        )
        blocked_metrics = evaluate_simple_change_trace(
            blocked,
            structural_evaluations=_structural_evaluations(blocked),
        )
        self.assertEqual(blocked_metrics.false_blocking_count, 0)
        self.assertEqual(blocked_metrics.new_universal_artifact_count, 0)

    def test_simple_trace_accepts_exactly_one_identity_bound_correction(
        self,
    ) -> None:
        payload = json.loads((FIXTURES / "simple-change.json").read_text())
        trace = payload["simple_trace"]
        run_root = (
            "docs/changes/"
            "2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/"
            "evidence/simple-change/runs/run-11111111111111111111111111111111/"
            "artifacts"
        )

        additions = [
            (
                "simple.snapshot.spec-review.resolution.v1",
                "review-evidence",
                f"{run_root}/review-evidence/spec-review-resolution.md",
                "9",
            ),
            (
                "simple.snapshot.feature.v2",
                "feature-spec",
                f"{run_root}/feature-spec/feature-v2.md",
                "a",
            ),
            (
                "simple.snapshot.spec-review.bundle.v2",
                "review-evidence",
                f"{run_root}/review-evidence/spec-review-bundle-v2.json",
                "b",
            ),
            (
                "simple.snapshot.spec-review.record.v2",
                "review-evidence",
                f"{run_root}/review-evidence/spec-review-record-v2.md",
                "c",
            ),
            (
                "simple.snapshot.spec-review.log.v2",
                "review-evidence",
                f"{run_root}/review-evidence/spec-review-log-v2.md",
                "d",
            ),
            (
                "simple.snapshot.spec-review.resolution.v2",
                "review-evidence",
                f"{run_root}/review-evidence/spec-review-resolution-v2.md",
                "f",
            ),
        ]
        for snapshot_id, role, path, digit in additions:
            trace["snapshots"].append(
                {
                    "snapshot_id": snapshot_id,
                    "source": "behavior-output",
                    "artifact_role": role,
                    "path": path,
                    "identity": "sha256:" + digit * 64,
                }
            )

        first_bundle = trace["review_bundles"][
            "simple.snapshot.spec-review.bundle.v1"
        ]
        first_projection = _finding_projection(
            "simple.finding.missing-boundary"
        )
        first_bundle.update(
            outcome="changes-requested",
            material_finding_ids=["simple.finding.missing-boundary"],
            finding_projection=first_projection,
            finding_projection_identity=_projection_identity(
                first_projection
            ),
            correction_eligibility="automatic-eligible",
        )
        first_bundle["artifact_refs"]["review-resolution"] = _snapshot_ref(
            trace,
            "simple.snapshot.spec-review.resolution.v1",
        )
        trace["review_bundles"]["simple.snapshot.spec-review.bundle.v2"] = {
            "review_id": "simple.review.spec.v2",
            "outcome": "approved",
            "reviewed_snapshot_id": "simple.snapshot.feature.v2",
            "material_finding_ids": ["simple.finding.missing-boundary"],
            "finding_projection": [],
            "finding_projection_identity": _projection_identity([]),
            "correction_eligibility": "not-applicable",
            "artifact_refs": {
                "review-record": _snapshot_ref(
                    trace,
                    "simple.snapshot.spec-review.record.v2",
                ),
                "review-log": _snapshot_ref(
                    trace,
                    "simple.snapshot.spec-review.log.v2",
                ),
                "review-resolution": _snapshot_ref(
                    trace,
                    "simple.snapshot.spec-review.resolution.v2",
                ),
            },
        }

        first_review = trace["events"][1]
        first_review.update(
            structural_result="fail",
            observed_result="changes-requested",
            diagnostic_id="simple.diagnostic.missing-boundary",
        )
        _sync_event_evidence(trace, first_review)

        spec2 = {
            "stage": "spec",
            "attempt": 2,
            "input_snapshot_ids": [
                "simple.snapshot.feature.v1",
                "simple.snapshot.spec-review.bundle.v1",
                "simple.snapshot.spec-review.record.v1",
                "simple.snapshot.spec-review.log.v1",
                "simple.snapshot.spec-review.resolution.v1",
            ],
            "reviewed_snapshot_id": None,
            "output_snapshot_ids": ["simple.snapshot.feature.v2"],
            "structural_result": "pass",
            "observed_result": "produced",
            "diagnostic_id": "none",
            "evidence_refs": [],
        }
        spec_review2 = {
            "stage": "spec-review",
            "attempt": 2,
            "input_snapshot_ids": ["simple.snapshot.feature.v2"],
            "reviewed_snapshot_id": "simple.snapshot.feature.v2",
            "output_snapshot_ids": ["simple.snapshot.spec-review.bundle.v2"],
            "structural_result": "pass",
            "observed_result": "approved",
            "diagnostic_id": "none",
            "evidence_refs": [],
        }
        _sync_event_evidence(trace, spec2)
        _sync_event_evidence(trace, spec_review2)
        trace["events"][2:2] = [spec2, spec_review2]

        test_spec = trace["events"][4]
        test_spec["input_snapshot_ids"] = [
            "simple.snapshot.feature.v2",
            "simple.snapshot.spec-review.bundle.v2",
            "simple.snapshot.spec-review.record.v2",
            "simple.snapshot.spec-review.log.v2",
            "simple.snapshot.spec-review.resolution.v2",
        ]
        _sync_event_evidence(trace, test_spec)
        test_review = trace["events"][5]
        test_review["input_snapshot_ids"] = [
            "simple.snapshot.test-spec.v1",
            "simple.snapshot.feature.v2",
            "simple.snapshot.spec-review.bundle.v2",
            "simple.snapshot.spec-review.record.v2",
            "simple.snapshot.spec-review.log.v2",
            "simple.snapshot.spec-review.resolution.v2",
        ]
        _sync_event_evidence(trace, test_review)

        trace["after_inventory"] = sorted(
            (
                {
                    "path": snapshot["path"],
                    "artifact_kind": snapshot["artifact_role"],
                    "identity": snapshot["identity"],
                }
                for snapshot in trace["snapshots"]
            ),
            key=lambda row: row["path"],
        )
        metrics = _evaluate_simple(
            payload,
            feature_snapshot_ids=(
                "simple.snapshot.feature.v1",
                "simple.snapshot.feature.v2",
            ),
        )
        self.assertEqual(metrics.structure_only_correction_cycles, 1)
        self.assertTrue(metrics.applicable_only_mapping)

        for name, mutate, diagnostic in (
            (
                "empty-rereview-findings",
                lambda bundle, trace: bundle.update(
                    material_finding_ids=[]
                ),
                "review artifact roles mismatch",
            ),
            (
                "changed-rereview-findings",
                lambda bundle, trace: bundle.update(
                    material_finding_ids=["simple.finding.substituted"]
                ),
                "finding set mismatch",
            ),
            (
                "missing-rereview-resolution",
                lambda bundle, trace: bundle["artifact_refs"].pop(
                    "review-resolution"
                ),
                "review artifact roles mismatch",
            ),
            (
                "reused-open-resolution",
                lambda bundle, trace: bundle["artifact_refs"].update(
                    {
                        "review-resolution": _snapshot_ref(
                            trace,
                            "simple.snapshot.spec-review.resolution.v1",
                        )
                    }
                ),
                "resolution mismatch",
            ),
        ):
            with self.subTest(contrast=name):
                invalid = copy.deepcopy(payload)
                invalid_trace = invalid["simple_trace"]
                invalid_bundle = invalid_trace["review_bundles"][
                    "simple.snapshot.spec-review.bundle.v2"
                ]
                mutate(invalid_bundle, invalid_trace)
                _sync_event_evidence(
                    invalid_trace, invalid_trace["events"][3]
                )
                with self.assertRaisesRegex(
                    BoundaryProofError, diagnostic
                ):
                    _evaluate_simple(
                        invalid,
                        feature_snapshot_ids=(
                            "simple.snapshot.feature.v1",
                            "simple.snapshot.feature.v2",
                        ),
                    )

        same_path = copy.deepcopy(payload)
        next(
            snapshot
            for snapshot in same_path["simple_trace"]["snapshots"]
            if snapshot["snapshot_id"] == "simple.snapshot.feature.v2"
        )["path"] = _snapshot_ref(
            same_path["simple_trace"],
            "simple.snapshot.feature.v1",
        )["path"]
        with self.assertRaisesRegex(
            BoundaryProofError,
            "duplicate snapshot path|distinct path",
        ):
            _evaluate_simple(
                same_path,
                feature_snapshot_ids=(
                    "simple.snapshot.feature.v1",
                    "simple.snapshot.feature.v2",
                ),
            )

        second_correction = copy.deepcopy(payload)
        second_trace = second_correction["simple_trace"]
        second_trace["snapshots"].append(
            {
                "snapshot_id": "simple.snapshot.test-spec-review.resolution.v1",
                "source": "behavior-output",
                "artifact_role": "review-evidence",
                "path": f"{run_root}/review-evidence/test-spec-review-resolution.md",
                "identity": "sha256:" + "e" * 64,
            }
        )
        second_bundle = second_trace["review_bundles"][
            "simple.snapshot.test-spec-review.bundle.v1"
        ]
        second_projection = _finding_projection(
            "simple.finding.missing-proof"
        )
        second_bundle.update(
            outcome="changes-requested",
            material_finding_ids=["simple.finding.missing-proof"],
            finding_projection=second_projection,
            finding_projection_identity=_projection_identity(
                second_projection
            ),
            correction_eligibility="automatic-eligible",
        )
        second_bundle["artifact_refs"]["review-resolution"] = _snapshot_ref(
            second_trace,
            "simple.snapshot.test-spec-review.resolution.v1",
        )
        second_event = second_trace["events"][-1]
        second_event.update(
            structural_result="fail",
            observed_result="changes-requested",
            diagnostic_id="simple.diagnostic.missing-proof",
        )
        _sync_event_evidence(second_trace, second_event)
        second_trace["after_inventory"].append(
            {
                "path": f"{run_root}/review-evidence/test-spec-review-resolution.md",
                "artifact_kind": "review-evidence",
                "identity": "sha256:" + "e" * 64,
            }
        )
        second_trace["after_inventory"].sort(key=lambda row: row["path"])
        with self.assertRaisesRegex(BoundaryProofError, "more than one correction"):
            _evaluate_simple(
                second_correction,
                feature_snapshot_ids=(
                    "simple.snapshot.feature.v1",
                    "simple.snapshot.feature.v2",
                ),
            )

    def test_correction_assemblers_publish_a_canonical_manifest(self) -> None:
        final_feature = (
            FIXTURES / "simple-change/candidates/feature-spec.md"
        ).read_text(encoding="utf-8")
        final_test_spec = (
            FIXTURES / "simple-change/candidates/test-spec.md"
        ).read_text(encoding="utf-8")
        candidate_feature = normalize_feature_model(
            _parse_feature_markdown(final_feature)
        )
        candidate_proof = normalize_proof_map(
            _parse_test_spec_markdown(final_test_spec),
            candidate_feature,
        )
        approved_spec_review = {
            "review_id": "spec-review-r2",
            "outcome": "approved",
            "material_finding_ids": [],
            "finding_projection": [],
            "finding_projection_identity": _projection_identity([]),
            "correction_eligibility": "not-applicable",
            "review_record_markdown": "# Spec review r2\n",
            "review_log_markdown": "# Spec review log r2\n",
        }
        approved_test_review = {
            "review_id": "test-spec-review-r2",
            "outcome": "approved",
            "material_finding_ids": [],
            "finding_projection": [],
            "finding_projection_identity": _projection_identity([]),
            "correction_eligibility": "not-applicable",
            "review_record_markdown": "# Test-spec review r2\n",
            "review_log_markdown": "# Test-spec review log r2\n",
        }
        changed_projection = _finding_projection("finding.boundary")
        changed_review = {
            "review_id": "review-r1",
            "outcome": "changes-requested",
            "material_finding_ids": ["finding.boundary"],
            "finding_projection": changed_projection,
            "finding_projection_identity": _projection_identity(
                changed_projection
            ),
            "correction_eligibility": "automatic-eligible",
            "review_record_markdown": (
                "# Changes requested\n\n"
                "## Finding finding.boundary\n\n"
                "- Finding ID: finding.boundary\n"
                "- Evidence: direct evidence\n"
                "- Required outcome: apply the bounded correction\n"
                "- Safe resolution path: update and rereview\n"
                "- needs-decision rationale: none\n"
            ),
            "review_log_markdown": "# Changes-requested log\n",
        }
        def authored_snapshot(
            snapshot_id: str,
            role: str,
            relative: str,
            raw: bytes,
        ) -> dict[str, object]:
            return {
                "snapshot_id": snapshot_id,
                "source": "behavior-output",
                "artifact_role": role,
                "path": f"docs/changes/example/artifacts/{relative}",
                "identity": "sha256:" + hashlib.sha256(raw).hexdigest(),
            }

        reviewed_snapshot = {
            "snapshot_id": "output.feature-spec.one",
            "identity": "sha256:" + "1" * 64,
        }
        with self.assertRaisesRegex(
            BoundaryRuntimeError, "protocol-shape-incompatible"
        ):
            _correction_review_bundle(
                authored_snapshot,
                "spec-review",
                1,
                reviewed_snapshot,
                changed_review,
                resolution_markdown=(
                    "Finding ID: finding.boundary\n"
                    "Closeout status: closed\n"
                ),
            )
        with self.assertRaisesRegex(
            BoundaryRuntimeError, "protocol-shape-incompatible"
        ):
            _correction_review_bundle(
                authored_snapshot,
                "spec-review",
                2,
                reviewed_snapshot,
                approved_spec_review,
                resolution_markdown=(
                    "Finding ID: finding.boundary\n"
                    "Closeout status: open\n"
                ),
                prior_finding_ids=["finding.boundary"],
            )
        stage_artifacts = {
            "feature-spec/portable-text-normalizer.md": final_feature,
            "test-spec/portable-text-normalizer.test.md": final_test_spec,
        }
        input_set = {"baseline_commit": "a" * 40}

        with tempfile.TemporaryDirectory() as raw:
            repo_root = Path(raw)
            candidate_root = (
                repo_root
                / "tests/fixtures/boundary-proof/simple-change/candidates"
            )
            candidate_root.mkdir(parents=True)
            (candidate_root / "feature-spec.md").write_text(
                final_feature, encoding="utf-8"
            )
            (candidate_root / "test-spec.md").write_text(
                final_test_spec, encoding="utf-8"
            )
            cases = (
                (
                    _assemble_feature_spec_correction_run,
                    {
                        "role": "feature-spec",
                        "initial_artifact_markdown": final_feature + "\n",
                        "initial_review": changed_review,
                        "initial_resolution_markdown": (
                            "# Resolution\n\n"
                            "Finding ID: finding.boundary\n"
                            "Closeout status: open\n"
                        ),
                        "corrected_resolution_markdown": (
                            "# Resolution\n\n"
                            "Finding ID: finding.boundary\n"
                            "Closeout status: closed\n"
                        ),
                    },
                    (
                        ("spec", 1),
                        ("spec-review", 1),
                        ("spec", 2),
                        ("spec-review", 2),
                        ("test-spec", 1),
                        ("test-spec-review", 1),
                    ),
                ),
                (
                    _assemble_test_spec_correction_run,
                    {
                        "role": "test-spec",
                        "initial_artifact_markdown": final_test_spec + "\n",
                        "initial_review": changed_review,
                        "initial_resolution_markdown": (
                            "# Resolution\n\n"
                            "Finding ID: finding.boundary\n"
                            "Closeout status: open\n"
                        ),
                        "corrected_resolution_markdown": (
                            "# Resolution\n\n"
                            "Finding ID: finding.boundary\n"
                            "Closeout status: closed\n"
                        ),
                    },
                    (
                        ("spec", 1),
                        ("spec-review", 1),
                        ("test-spec", 1),
                        ("test-spec-review", 1),
                        ("test-spec", 2),
                        ("test-spec-review", 2),
                    ),
                ),
            )
            for index, (assembler, correction, occurrences) in enumerate(cases):
                with self.subTest(role=correction["role"]):
                    change_id = f"2026-07-27-correction-{index}"
                    (repo_root / "docs/changes" / change_id).mkdir(
                        parents=True
                    )
                    payload = {
                        "stage_artifacts": stage_artifacts,
                        "stage_provenance": [
                            {
                                "stage": stage,
                                "attempt": attempt,
                                "thread_id": f"thread-{index}-{position}",
                                "skill_names": ["workflow", stage],
                            }
                            for position, (stage, attempt) in enumerate(
                                occurrences
                            )
                        ],
                        "spec_review": approved_spec_review,
                        "test_spec_review": approved_test_review,
                        "transport_attempts": [],
                    }
                    temporary, manifest = assembler(
                        repo_root,
                        change_id,
                        f"run-{'1' if index == 0 else '2'}" + "0" * 31,
                        input_set,
                        payload,
                        candidate_feature,
                        candidate_proof,
                        [],
                        [],
                        correction,
                        "publisher-" + ("1" if index == 0 else "2") * 32,
                        (
                            repo_root
                            / "docs"
                            / "changes"
                            / change_id
                            / "evidence"
                            / "simple-change"
                            / (
                                ".working-run-"
                                + ("1" if index == 0 else "2")
                                + "0" * 31
                            )
                        ),
                    )
                    self.assertTrue((temporary / "manifest.json").is_file())
                    self.assertFalse((temporary / "run.json").exists())
                    self.assertEqual(
                        json.loads(
                            (temporary / "manifest.json").read_text(
                                encoding="utf-8"
                            )
                        ),
                        manifest,
                    )
                    review_stage = (
                        "spec-review"
                        if correction["role"] == "feature-spec"
                        else "test-spec-review"
                    )
                    snapshots_by_id = {
                        snapshot["snapshot_id"]: snapshot
                        for snapshot in manifest["snapshots"]
                    }

                    def resolve_snapshot(
                        snapshot: dict[str, object],
                    ) -> Path:
                        relative = str(snapshot["path"]).split(
                            "/artifacts/", 1
                        )[1]
                        return temporary / "artifacts" / relative

                    def read_bundle(attempt: int) -> dict[str, object]:
                        snapshot = snapshots_by_id[
                            f"output.{review_stage}.attempt-{attempt}.bundle"
                        ]
                        return json.loads(
                            resolve_snapshot(snapshot).read_text(encoding="utf-8")
                        )

                    first_bundle = read_bundle(1)
                    second_bundle = read_bundle(2)
                    self.assertEqual(
                        first_bundle["material_finding_ids"],
                        ["finding.boundary"],
                    )
                    self.assertEqual(
                        second_bundle["material_finding_ids"],
                        ["finding.boundary"],
                    )
                    self.assertEqual(
                        second_bundle["finding_projection"], []
                    )
                    for bundle, expected in (
                        (
                            first_bundle,
                            "# Resolution\n\n"
                            "Finding ID: finding.boundary\n"
                            "Closeout status: open\n",
                        ),
                        (
                            second_bundle,
                            "# Resolution\n\n"
                            "Finding ID: finding.boundary\n"
                            "Closeout status: closed\n",
                        ),
                    ):
                        resolution_ref = bundle["artifact_refs"][
                            "review-resolution"
                        ]
                        relative = str(resolution_ref["path"]).split(
                            "/artifacts/", 1
                        )[1]
                        resolution_path = (
                            temporary / "artifacts" / relative
                        )
                        self.assertEqual(
                            resolution_path.read_text(encoding="utf-8"),
                            expected,
                        )
                        self.assertEqual(
                            "sha256:"
                            + hashlib.sha256(
                                expected.encode("utf-8")
                            ).hexdigest(),
                            resolution_ref["identity"],
                        )

    def test_review_bundle_byte_validator_rejects_malformed_subjects(
        self,
    ) -> None:
        for reviewed_snapshot_id in (None, 1, True, [], {}):
            with self.subTest(
                field="reviewed_snapshot_id",
                value=reviewed_snapshot_id,
            ):
                with self.assertRaisesRegex(
                    BoundaryRuntimeError, "runtime-identity-unstable"
                ):
                    _validate_review_bundle_payloads(
                        {
                            "bundle": {
                                "artifact_refs": {},
                                "reviewed_snapshot_id": reviewed_snapshot_id,
                                "material_finding_ids": [],
                            }
                        },
                        {},
                        lambda snapshot: Path("unused"),
                    )

        for findings in (
            None,
            "finding.one",
            [None],
            [{}],
            ["invalid"],
            ["finding.two", "finding.one"],
            ["finding.one", "finding.one"],
        ):
            with self.subTest(
                field="material_finding_ids", value=findings
            ):
                with self.assertRaisesRegex(
                    BoundaryRuntimeError, "runtime-identity-unstable"
                ):
                    _validate_review_bundle_payloads(
                        {
                            "bundle": {
                                "artifact_refs": {},
                                "reviewed_snapshot_id": "snapshot.one",
                                "material_finding_ids": findings,
                            }
                        },
                        {
                            "snapshot.one": {
                                "path": "reviews/snapshot.one.md",
                                "identity": "sha256:" + "1" * 64,
                            }
                        },
                        lambda snapshot: Path("unused"),
                    )

    def test_validator_help_and_fixture_validation(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate-boundary-proof.py"), "--help"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("boundary", result.stdout.lower())

    def test_only_validator_cli_serializes_synthetic_report(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            source = root / "report.json"
            output = root / "report.md"
            source.write_text(json.dumps(_report()), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "validate-boundary-proof.py"),
                    str(source),
                    "--write-report",
                    str(output),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            rendered = output.read_text(encoding="utf-8")
            self.assertEqual(rendered.count("```yaml"), 1)
            self.assertEqual(rendered.count("```"), 2)
            self.assertIn('"overall_result": "pass"', rendered)

            reordered_source = root / "report-reordered.json"
            reordered_output = root / "report-reordered.md"
            report = _report()
            report["checks"] = dict(  # type: ignore[assignment]
                reversed(list(report["checks"].items()))  # type: ignore[union-attr]
            )
            reordered_source.write_text(json.dumps(report), encoding="utf-8")
            reordered = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "validate-boundary-proof.py"),
                    str(reordered_source),
                    "--write-report",
                    str(reordered_output),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(reordered.returncode, 0, reordered.stderr)
            self.assertEqual(output.read_bytes(), reordered_output.read_bytes())


class BoundaryProofEnvironmentTests(unittest.TestCase):
    def test_workflow_request_owns_routing_without_normative_rendering(self) -> None:
        request = _workflow_request("normalize portable text")
        self.assertEqual(request["stage"], "workflow")
        self.assertEqual(request["skill_names"], list(PARTICIPATING_SKILLS))
        self.assertEqual(
            request["expected_outputs"],
            [
                "feature-spec/portable-text-normalizer.md",
                "reviews/spec-review.md",
                "review-log/spec-review.md",
                "test-spec/portable-text-normalizer.test.md",
                "reviews/test-spec-review.md",
                "review-log/test-spec-review.md",
            ],
        )
        self.assertNotIn("R1. The public normalizer", request["prompt"])
        self.assertNotIn("T1-CANONICAL-PAIR", request["prompt"])
        stage_request = _workflow_stage_request("spec", "normalize text")
        self.assertEqual(stage_request["skill_names"], ["workflow", "spec"])
        self.assertEqual(
            stage_request["expected_outputs"],
            ["feature-spec/portable-text-normalizer.md"],
        )
        self.assertNotIn("file-write tool", stage_request["prompt"])
        self.assertIn("artifact envelope", stage_request["prompt"])
        self.assertIn("`## Boundary model`", stage_request["prompt"])
        self.assertIn(
            "^[a-z][a-z0-9-]*(\\.[a-z][a-z0-9-]*)+$",
            stage_request["prompt"],
        )
        self.assertIn("literal ASCII `-`", stage_request["prompt"])
        self.assertIn("all twelve closed core dimension IDs", stage_request["prompt"])
        self.assertIn(
            "Each boundary ID must appear in exactly one boundary row",
            stage_request["prompt"],
        )
        self.assertIn("contiguous in that exact order", stage_request["prompt"])
        self.assertIn(
            "never put prose in the Rationale cell",
            stage_request["prompt"],
        )
        self.assertIn("must overlap each cited boundary", stage_request["prompt"])
        self.assertIn(
            "audit each example independently",
            stage_request["prompt"],
        )
        self.assertIn(
            "Extension ID | Title | Applicability | Rationale | Governing "
            "requirement IDs | Boundary IDs | Non-applicability rationale",
            stage_request["prompt"],
        )
        self.assertIn(
            "^x\\.[a-z][a-z0-9-]*(\\.[a-z][a-z0-9-]*)+$",
            stage_request["prompt"],
        )
        self.assertNotIn(
            "all twelve closed core dimension IDs exactly once, no extensions",
            stage_request["prompt"],
        )
        self.assertIn(
            "requirement-owner union",
            stage_request["prompt"],
        )
        self.assertIn("add no normative behavior", stage_request["prompt"])
        self.assertEqual(
            stage_request["artifact_policy_id"],
            "lifecycle-stage-artifacts-v1",
        )
        review_request = _workflow_stage_request(
            "spec-review",
            "review",
            artifact_context="Reviewed artifact identity: sha256:" + "a" * 64,
        )
        self.assertIn("Review ID: spec-review-r1", review_request["prompt"])
        rereview_request = _workflow_stage_request(
            "spec-review",
            "rereview",
            attempt=2,
        )
        self.assertIn("Review ID: spec-review-r2", rereview_request["prompt"])
        self.assertIn("Preserve independent judgment", review_request["prompt"])
        self.assertIn(
            "spec-review-record=reviews/spec-review.md",
            review_request["prompt"],
        )
        self.assertIn(
            "spec-review-log=review-log/spec-review.md",
            review_request["prompt"],
        )
        test_spec_request = _workflow_stage_request("test-spec", "author tests")
        self.assertIn(
            "Use `T1`, `T2`, and subsequent uppercase numeric IDs",
            test_spec_request["prompt"],
        )
        correction_request = _workflow_stage_request(
            "test-spec",
            "apply the recorded Required outcome exactly",
            attempt=2,
            governing_reference_ids=("interaction.mode-outcome",),
            governing_interaction_ids=("interaction.mode-outcome",),
        )
        self.assertIn(
            "interaction.mode-outcome",
            correction_request["prompt"],
        )
        test_rereview_request = _workflow_stage_request(
            "test-spec-review",
            "rereview",
            attempt=2,
        )
        self.assertIn(
            "Review ID: test-spec-review-r2",
            test_rereview_request["prompt"],
        )

    def test_stage_envelope_is_policy_bound_and_parent_materialized(self) -> None:
        envelope = {
            "schema_version": "boundary-stage-artifact-envelope-v1",
            "artifact_policy_id": "lifecycle-stage-artifacts-v1",
            "completed": True,
            "last_stage": "spec",
            "artifact_set_variant": "spec-initial",
            "artifacts": [
                {
                    "role": "feature-spec",
                    "path": "feature-spec/portable-text-normalizer.md",
                    "content_utf8": "# Feature\n",
                }
            ],
        }
        parsed, rows = _parse_stage_envelope(
            json.dumps(envelope), stage="spec", attempt=1
        )
        self.assertEqual(parsed, envelope)
        self.assertEqual(rows[0]["text"], "# Feature\n")
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            observation = _materialize_stage_envelope(root, parsed)
            self.assertEqual(observation["result"], "pass")
            self.assertEqual(
                (root / rows[0]["path"]).read_text(encoding="utf-8"),
                "# Feature\n",
            )
        for mutation in (
            {**envelope, "artifact_policy_id": "unknown"},
            {**envelope, "artifact_set_variant": "spec-correction"},
            {**envelope, "unknown": True},
        ):
            with self.subTest(keys=sorted(mutation)):
                with self.assertRaises(BoundaryRuntimeError):
                    _parse_stage_envelope(
                        json.dumps(mutation), stage="spec", attempt=1
                    )

    def test_materialization_preserves_bound_attempt_for_shared_review_variant(
        self,
    ) -> None:
        envelope = {
            "schema_version": "boundary-stage-artifact-envelope-v1",
            "artifact_policy_id": "lifecycle-stage-artifacts-v1",
            "completed": True,
            "last_stage": "spec-review",
            "artifact_set_variant": "spec-review-changes-requested",
            "artifacts": [
                {
                    "role": "spec-review-record",
                    "path": "reviews/spec-review.md",
                    "content_utf8": "# Review\n",
                },
                {
                    "role": "spec-review-log",
                    "path": "review-log/spec-review.md",
                    "content_utf8": "# Log\n",
                },
                {
                    "role": "spec-review-resolution",
                    "path": "review-resolution/spec-review.md",
                    "content_utf8": "# Resolution\n",
                },
            ],
        }
        with tempfile.TemporaryDirectory() as raw:
            observation = _materialize_stage_envelope(
                Path(raw), envelope, attempt=1
            )
        self.assertEqual(observation["result"], "pass")

    def test_timeout_reconciles_complete_output_without_reinvocation(self) -> None:
        calls = 0

        def invoke() -> tuple[dict[str, object], dict[str, object]]:
            nonlocal calls
            calls += 1
            raise _StageTurnTimeout(
                attestation={"identity": "current"},
                output_files=[{"path": "artifact.md", "text": "complete"}],
                termination_state="confirmed-stopped",
            )

        attestation, result, attempts = _invoke_with_reconciliation(
            invoke, ["artifact.md"]
        )
        self.assertEqual(calls, 1)
        self.assertEqual(attestation, {"identity": "current"})
        self.assertEqual(result["output_files"][0]["path"], "artifact.md")
        self.assertEqual(attempts[-1]["decision"], "reconcile")

    def test_reconciliation_accepts_each_mutually_exclusive_review_set(
        self,
    ) -> None:
        allowed = [
            ["reviews/spec-review.md", "review-log/spec-review.md"],
            [
                "reviews/spec-review.md",
                "review-log/spec-review.md",
                "review-resolution/spec-review.md",
            ],
        ]
        for paths in allowed:
            with self.subTest(paths=paths):
                calls = 0

                def invoke() -> tuple[dict[str, object], dict[str, object]]:
                    nonlocal calls
                    calls += 1
                    return (
                        {"identity": "current"},
                        {
                            "thread_id": "thread-1",
                            "runtime_process_id": "process-1",
                            "output_files": [
                                {"path": path, "text": "# Artifact\n"}
                                for path in paths
                            ],
                        },
                    )

                _, _, attempts = _invoke_with_reconciliation(
                    invoke,
                    allowed[0],
                    allowed_path_sets=allowed,
                )
                self.assertEqual(calls, 1)
                self.assertEqual(attempts[-1]["decision"], "accept")

    def test_timeout_with_no_variant_output_is_absent_and_retries(self) -> None:
        calls = 0
        allowed = [
            ["reviews/spec-review.md", "review-log/spec-review.md"],
            [
                "reviews/spec-review.md",
                "review-log/spec-review.md",
                "review-resolution/spec-review.md",
            ],
        ]

        def invoke() -> tuple[dict[str, object], dict[str, object]]:
            nonlocal calls
            calls += 1
            if calls == 1:
                raise _StageTurnTimeout(
                    attestation={"identity": "first"},
                    output_files=[],
                    termination_state="confirmed-stopped",
                )
            return (
                {"identity": "second"},
                {
                    "output_files": [
                        {"path": path, "text": "# Review\n"}
                        for path in allowed[0]
                    ]
                },
            )

        _, _, attempts = _invoke_with_reconciliation(
            invoke,
            allowed[0],
            allowed_path_sets=allowed,
        )
        self.assertEqual(calls, 2)
        self.assertEqual(
            [(row["output_state"], row["decision"]) for row in attempts],
            [("absent", "retry"), ("complete", "accept")],
        )

    def test_timeout_retries_only_absent_output_once(self) -> None:
        calls = 0

        def invoke() -> tuple[dict[str, object], dict[str, object]]:
            nonlocal calls
            calls += 1
            if calls == 1:
                raise _StageTurnTimeout(
                    attestation={"identity": "first"},
                    output_files=[],
                    termination_state="confirmed-stopped",
                )
            return (
                {"identity": "second"},
                {"output_files": [{"path": "artifact.md", "text": "complete"}]},
            )

        attestation, _, attempts = _invoke_with_reconciliation(
            invoke, ["artifact.md"]
        )
        self.assertEqual(calls, 2)
        self.assertEqual(attestation, {"identity": "second"})
        self.assertEqual(
            [row["decision"] for row in attempts], ["retry", "accept"]
        )

    def test_timeout_partial_output_and_second_timeout_fail_closed(self) -> None:
        with self.assertRaises(BoundaryRuntimeError):
            _invoke_with_reconciliation(
                lambda: (_ for _ in ()).throw(
                    _StageTurnTimeout(
                        attestation={"identity": "first"},
                        output_files=[{"path": "one.md", "text": "partial"}],
                        termination_state="confirmed-stopped",
                    )
                ),
                ["one.md", "two.md"],
            )

        calls = 0

        def absent() -> tuple[dict[str, object], dict[str, object]]:
            nonlocal calls
            calls += 1
            raise _StageTurnTimeout(
                attestation={"identity": str(calls)},
                output_files=[],
                termination_state="confirmed-stopped",
            )

        diagnostic = io.StringIO()
        with (
            mock.patch.dict(
                "os.environ", {"BOUNDARY_PROOF_DIAGNOSTICS": "1"}
            ),
            mock.patch("sys.stderr", diagnostic),
            self.assertRaises(BoundaryRuntimeError),
        ):
            _invoke_with_reconciliation(absent, ["artifact.md"])
        self.assertEqual(calls, 2)
        self.assertEqual(
            diagnostic.getvalue().splitlines(),
            [
                "transport-decision:attempt=1:"
                "termination_state=confirmed-stopped:"
                "output_state=absent:decision=retry",
                "transport-decision:attempt=2:"
                "termination_state=confirmed-stopped:"
                "output_state=absent:decision=fail-closed",
            ],
        )

    def test_controlled_transport_fixture_is_closed_and_noncanonical(self) -> None:
        fixture = _load_transport_fixture(
            ROOT
            / "tests"
            / "fixtures"
            / "boundary-proof"
            / "transport"
            / "timeout-complete-reconcile.json"
        )
        self.assertFalse(fixture["canonical_evidence_eligible"])
        self.assertEqual(
            fixture["expected_terminal_decision"], "reconcile"
        )
        for mutation in (
            {key: value for key, value in fixture.items() if key != "event_key"},
            {**fixture, "unknown": True},
            {**fixture, "canonical_evidence_eligible": True},
        ):
            with self.subTest(keys=sorted(mutation)):
                with tempfile.TemporaryDirectory() as raw:
                    path = Path(raw) / "fixture.json"
                    path.write_text(json.dumps(mutation), encoding="utf-8")
                    with self.assertRaises(BoundaryRuntimeError):
                        _load_transport_fixture(path)

    def test_transport_fixture_unknown_value_fails_closed(self) -> None:
        source = (
            ROOT
            / "tests"
            / "fixtures"
            / "boundary-proof"
            / "transport"
            / "timeout-complete-reconcile.json"
        )
        fixture = json.loads(source.read_text(encoding="utf-8"))
        fixture["transport_attempts"][0]["decision"] = "unknown-decision"
        fixture["expected_terminal_decision"] = "unknown-decision"
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "fixture.json"
            path.write_text(json.dumps(fixture), encoding="utf-8")
            with self.assertRaises(BoundaryRuntimeError):
                _load_transport_fixture(path)

    def test_test_spec_stage_assigns_preserve_to_canonical_proof(self) -> None:
        request = _workflow_request("normalize text")
        self.assertIn("test-spec", request["prompt"])
        self.assertIn("stage-owning skill", request["prompt"])

    def test_feature_contract_does_not_require_an_empty_unknown_mode_class(
        self,
    ) -> None:
        rendered = (
            FIXTURES
            / "simple-change"
            / "candidates"
            / "feature-spec.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "accept exactly `trim` and `preserve`", rendered
        )
        self.assertNotIn(
            "including empty, canonically equivalent, differently cased",
            rendered,
        )

    def test_stage_output_schemas_are_compact_closed_records(self) -> None:
        schema = _workflow_request("normalize text")["output_schema"]
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(
            schema["required"], ["completed", "last_stage"]
        )
        self.assertLess(len(json.dumps(schema)), 500)

    def test_simple_change_candidates_parse_to_the_closed_profile(self) -> None:
        feature_path = (
            FIXTURES / "simple-change" / "candidates" / "feature-spec.md"
        )
        test_path = (
            FIXTURES / "simple-change" / "candidates" / "test-spec.md"
        )
        feature = _parse_feature_markdown(
            feature_path.read_text(encoding="utf-8")
        )
        proof = _parse_test_spec_markdown(
            test_path.read_text(encoding="utf-8")
        )
        normalized_feature = normalize_feature_model(feature)
        normalized_proof = normalize_proof_map(proof, normalized_feature)
        self.assertEqual(
            {row.dimension_id for row in normalized_feature.core_dimensions},
            set(CORE_DIMENSION_IDS),
        )
        self.assertEqual(len(normalized_proof.proof_obligations), 4)

    def test_test_spec_parser_accepts_equivalent_markdown_test_headings(
        self,
    ) -> None:
        feature = normalize_feature_model(
            _parse_feature_markdown(
                (
                    FIXTURES
                    / "simple-change"
                    / "candidates"
                    / "feature-spec.md"
                ).read_text(encoding="utf-8")
            )
        )
        raw = (
            FIXTURES / "simple-change" / "candidates" / "test-spec.md"
        ).read_text(encoding="utf-8")
        for test_id in ("T1", "T2", "T3"):
            raw = raw.replace(f"\n{test_id}.", f"\n### {test_id}.")
        proof = normalize_proof_map(_parse_test_spec_markdown(raw), feature)
        self.assertEqual(len(proof.proof_obligations), 4)

    def test_feature_parser_preserves_canonical_interaction_table(self) -> None:
        raw = (
            FIXTURES / "simple-change" / "candidates" / "feature-spec.md"
        ).read_text(encoding="utf-8")
        raw = raw.replace(
            "None selected. The closed mode and outcome partitions do not "
            "create a\ncross-boundary hazard.",
            "| Interaction ID | Governing requirement IDs | Boundary IDs | "
            "Rationale |\n"
            "| --- | --- | --- | --- |\n"
            "| interaction.mode-outcome | R1, R4 | text.mode.unknown, "
            "text.outcome.error | composed-path |",
        )
        parsed = normalize_feature_model(_parse_feature_markdown(raw))
        self.assertEqual(
            [row.interaction_id for row in parsed.interactions],
            ["interaction.mode-outcome"],
        )
        unknown_rationale = raw.replace(
            "| composed-path |",
            "| prose rationale |",
        )
        with self.assertRaisesRegex(
            BoundaryProofError,
            "unknown interaction rationale",
        ):
            normalize_feature_model(
                _parse_feature_markdown(unknown_rationale)
            )
        malformed = raw.replace(
            "| Interaction ID | Governing requirement IDs | Boundary IDs | "
            "Rationale |",
            "| Interaction ID | Boundary IDs | Rationale | Governing "
            "requirement IDs |",
        )
        with self.assertRaises(BoundaryRuntimeError):
            _parse_feature_markdown(malformed)

    def test_feature_parser_preserves_canonical_extension_table(self) -> None:
        raw = (
            FIXTURES / "simple-change" / "candidates" / "feature-spec.md"
        ).read_text(encoding="utf-8")
        extension_table = (
            "Extensions:\n\n"
            "| Extension ID | Title | Applicability | Rationale | "
            "Governing requirement IDs | Boundary IDs | "
            "Non-applicability rationale |\n"
            "| --- | --- | --- | --- | --- | --- | --- |\n"
            "| x.text.normalization | Text normalization | applicable | "
            "Models the feature-specific text transformation partition. | "
            "R2, R3 | text.normalization | - |"
        )
        parsed = normalize_feature_model(
            _parse_feature_markdown(
                raw.replace("Extensions: none.", extension_table)
            )
        )
        self.assertEqual(
            [extension.extension_id for extension in parsed.extensions],
            ["x.text.normalization"],
        )
        malformed = extension_table.replace(
            "Extension ID | Title",
            "Title | Extension ID",
        )
        with self.assertRaises(BoundaryRuntimeError):
            _parse_feature_markdown(
                raw.replace("Extensions: none.", malformed)
            )

    def test_invariant_projection_accepts_stage_owned_alternative_modeling(
        self,
    ) -> None:
        feature_payload = _parse_feature_markdown(
            (
                FIXTURES / "simple-change" / "candidates" / "feature-spec.md"
            ).read_text(encoding="utf-8")
        )
        proof_payload = _parse_test_spec_markdown(
            (
                FIXTURES / "simple-change" / "candidates" / "test-spec.md"
            ).read_text(encoding="utf-8")
        )
        candidate_feature = normalize_feature_model(feature_payload)
        candidate_proof = normalize_proof_map(proof_payload, candidate_feature)

        alternative_payload = copy.deepcopy(feature_payload)
        rows = {
            row["dimension_id"]: row
            for row in alternative_payload["core_dimensions"]
        }
        canonical = rows["canonical-trust"]
        freshness = rows["identity-freshness"]
        canonical.update(
            {
                "applicability": "not-applicable",
                "governing_requirement_ids": [],
                "boundary_ids": [],
                "non_applicability_rationale": (
                    "The stage owns this alternative applicability rationale."
                ),
            }
        )
        freshness.update(
            {
                "applicability": "applicable",
                "governing_requirement_ids": ["R1", "R2", "R3"],
                "boundary_ids": ["text.canonical.requirements"],
                "non_applicability_rationale": None,
            }
        )
        alternative_payload["examples"][0]["example_id"] = "alt.example.trim"
        alternative_payload["extensions"].append(
            {
                "extension_id": "x.text.normalization",
                "title": "Text normalization",
                "applicability": "applicable",
                "rationale": (
                    "The stage models the stateless normalization partition "
                    "as a feature-specific extension."
                ),
                "governing_requirement_ids": ["R2", "R3"],
                "boundary_ids": ["alt.text.normalization"],
                "non_applicability_rationale": None,
            }
        )
        alternative_feature = normalize_feature_model(alternative_payload)

        alternative_proof_payload = copy.deepcopy(proof_payload)
        alternative_proof_payload["proof_obligations"][0][
            "proof_obligation_id"
        ] = "alt.proof.canonical"
        alternative_proof_payload["proof_obligations"][0]["test_case_ids"] = [
            "alt.t1",
            "alt.t2",
            "alt.t3",
        ]
        alternative_proof_payload["proof_obligations"].append(
            {
                "proof_obligation_id": "alt.proof.normalization",
                "governing_requirement_ids": ["R2", "R3"],
                "boundary_or_interaction_ids": ["alt.text.normalization"],
                "test_case_ids": ["alt.t1", "alt.t3"],
                "automation_level": "automated",
                "manual_procedure_ids": [],
            }
        )
        alternative_proof = normalize_proof_map(
            alternative_proof_payload, alternative_feature
        )

        self.assertNotEqual(candidate_feature, alternative_feature)
        self.assertNotEqual(candidate_proof, alternative_proof)
        self.assertTrue(
            boundary_invariant_projections_match(
                candidate_feature,
                alternative_feature,
                candidate_proof,
                alternative_proof,
            )
        )

    def test_invariant_projection_contains_only_the_closed_oracle_fields(
        self,
    ) -> None:
        feature = normalize_feature_model(
            _parse_feature_markdown(
                (
                    FIXTURES
                    / "simple-change"
                    / "candidates"
                    / "feature-spec.md"
                ).read_text(encoding="utf-8")
            )
        )
        proof = normalize_proof_map(
            _parse_test_spec_markdown(
                (
                    FIXTURES
                    / "simple-change"
                    / "candidates"
                    / "test-spec.md"
                ).read_text(encoding="utf-8")
            ),
            feature,
        )
        self.assertEqual(
            dataclasses.asdict(feature_invariant_projection(feature)),
            {
                "boundary_model_version": "v1",
                "boundary_model_scope": "R1-R4",
                "requirement_ids": ("R1", "R2", "R3", "R4"),
                "core_dimension_ids": tuple(sorted(CORE_DIMENSION_IDS)),
            },
        )
        self.assertEqual(
            dataclasses.asdict(proof_invariant_projection(proof)),
            {
                "boundary_model_version": "v1",
                "boundary_model_scope": "R1-R4",
                "governing_requirement_ids": ("R1", "R2", "R3", "R4"),
            },
        )

    def test_invariant_projection_rejects_every_unequal_closed_member(self) -> None:
        feature = normalize_feature_model(
            _parse_feature_markdown(
                (
                    FIXTURES
                    / "simple-change"
                    / "candidates"
                    / "feature-spec.md"
                ).read_text(encoding="utf-8")
            )
        )
        projection = feature_invariant_projection(feature)
        mutations = {
            field: dataclasses.replace(projection, **{field: replacement})
            for field, replacement in {
                "boundary_model_version": "legacy",
                "boundary_model_scope": "R1-R3",
                "requirement_ids": ("R1", "R2", "R3"),
                "core_dimension_ids": projection.core_dimension_ids[:-1],
            }.items()
        }
        for field, altered in mutations.items():
            with self.subTest(field=field):
                self.assertNotEqual(projection, altered)

    def test_generation_only_diagnostics_are_closed_and_phase_bound(self) -> None:
        self.assertEqual(
            DIAGNOSTIC_PHASES["boundary-oracle-mismatch"],
            frozenset({"in-turn"}),
        )
        self.assertEqual(
            DIAGNOSTIC_PHASES["unmanifested-input"],
            frozenset({"pre-turn-start"}),
        )
        self.assertEqual(
            DIAGNOSTIC_PHASES["review-nonapproval"],
            frozenset({"in-turn"}),
        )
        with self.assertRaises(ValueError):
            BoundaryRuntimeError("not-in-vocabulary")

    def test_candidate_values_are_rejected_from_every_child_visible_surface(
        self,
    ) -> None:
        clean = {
            "serialized_request": {"prompt": "author from the scenario"},
            "workspace_inventory": [("scenario.json", 10, "sha256:clean")],
            "child_access_observations": [{"root": "/isolated/workspace"}],
            "forbidden_candidate_values": ("candidate-secret",),
        }
        _assert_parent_only_candidate_isolation(**clean)
        for surface in (
            "serialized_request",
            "workspace_inventory",
            "child_access_observations",
        ):
            contaminated = copy.deepcopy(clean)
            if surface == "serialized_request":
                contaminated[surface] = {"prompt": "candidate-secret"}
            else:
                contaminated[surface] = ["candidate-secret"]
            with self.subTest(surface=surface):
                with self.assertRaises(BoundaryRuntimeError) as raised:
                    _assert_parent_only_candidate_isolation(**contaminated)
                self.assertEqual(
                    raised.exception.diagnostic_id, "unmanifested-input"
                )

    def test_scenario_is_bound_into_spec_and_both_formal_reviews(self) -> None:
        scenario = json.loads(
            (
                FIXTURES / "simple-change" / "scenario.json"
            ).read_text(encoding="utf-8")
        )["request"]
        spec_request = _workflow_stage_request("spec", scenario)
        spec_review_request = _workflow_stage_request(
            "spec-review",
            "review",
            artifact_context="Authoritative scenario request:\n" + scenario,
        )
        test_spec_request = _workflow_stage_request(
            "test-spec",
            "author proof",
            artifact_context="Governing feature specification",
            governing_reference_ids=(
                "boundary.mode-domain",
                "interaction.mode-outcome",
            ),
            governing_interaction_ids=("interaction.mode-outcome",),
        )
        self.assertIn(
            "must exactly match an ID defined by the attached governing "
            "feature's boundary record",
            test_spec_request["prompt"],
        )
        self.assertIn(
            "Do not invent, rename, infer, or repair an ID",
            test_spec_request["prompt"],
        )
        self.assertIn(
            "Closed governing boundary and interaction IDs:\n"
            "- boundary.mode-domain\n"
            "- interaction.mode-outcome",
            test_spec_request["prompt"],
        )
        self.assertIn(
            "The test spec does not own boundary or interaction definitions",
            test_spec_request["prompt"],
        )
        self.assertIn(
            "perform a final membership audit",
            test_spec_request["prompt"],
        )
        self.assertIn(
            "The governing feature selected these interactions:\n"
            "- interaction.mode-outcome",
            test_spec_request["prompt"],
        )
        no_interaction_request = _workflow_stage_request(
            "test-spec",
            "author proof",
            governing_reference_ids=("boundary.mode-domain",),
        )
        self.assertIn(
            "The governing feature selected no interactions",
            no_interaction_request["prompt"],
        )
        with self.assertRaises(BoundaryRuntimeError):
            _workflow_stage_request(
                "spec",
                "author",
                governing_reference_ids=("boundary.mode-domain",),
            )
        test_review_request = _workflow_stage_request(
            "test-spec-review",
            "review",
            artifact_context="Authoritative scenario request:\n" + scenario,
        )
        for request in (spec_request, spec_review_request, test_review_request):
            self.assertIn(scenario, request["prompt"])
        canonical_review_request = _workflow_stage_request(
            "test-spec-review",
            "Under approved R28y, perform the isolated behavior-evidence "
            "review. Architecture, plan, and plan-review are outside this "
            "scenario. `Implementation handoff: not-allowed`.",
        )
        self.assertIn(
            "Implementation handoff: not-allowed",
            canonical_review_request["prompt"],
        )

    def test_stage_output_rejects_label_only_generation(self) -> None:
        accepted = {
            "agent_message": json.dumps(
                {"completed": True, "last_stage": "test-spec-review"}
            )
        }
        payload = _load_generated_payload(
            accepted, {"completed", "last_stage"}
        )
        self.assertTrue(payload["completed"])
        label_only = {
            "agent_message": json.dumps(
                {"workflow_profile": "complete-boundary-first-v1"}
            )
        }
        with self.assertRaises(BoundaryRuntimeError) as raised:
            _load_generated_payload(label_only, {"completed", "last_stage"})
        self.assertEqual(
            raised.exception.diagnostic_id, "unexpected-prohibited-event"
        )

    def test_controlled_fixture_detects_stale_candidate_bytes(self) -> None:
        fixture = FIXTURES / "behavior" / "happy-path.json"
        with tempfile.TemporaryDirectory() as raw:
            output = Path(raw)
            exercise_fixture(fixture, output)
            self.assertEqual(validate_fixture(output)["result"], "pass")
            result_path = output / "fixture-result.json"
            result = json.loads(result_path.read_text(encoding="utf-8"))
            result["feature_ref"]["identity"] = "sha256:" + "0" * 64
            result_path.write_text(json.dumps(result), encoding="utf-8")
            with self.assertRaises(BoundaryRuntimeError) as raised:
                validate_fixture(output)
            self.assertEqual(
                raised.exception.diagnostic_id, "runtime-identity-unstable"
            )

    def test_validation_only_does_not_collect_runtime_attestation(self) -> None:
        change_id = (
            "2026-07-25-boundary-first-proof-modeling-for-published-"
            "lifecycle-skills"
        )
        current = (
            ROOT
            / "docs"
            / "changes"
            / change_id
            / "evidence"
            / "simple-change"
            / "current.json"
        )
        if not current.exists():
            self.skipTest("canonical M2 run is not generated yet")
        metrics = SimpleNamespace(
            false_blocking_count=0,
            new_universal_artifact_count=0,
            structure_only_correction_cycles=0,
        )
        with (
            mock.patch(
                "boundary_proof_behavior._collect_runtime_attestation",
                side_effect=AssertionError("validation reinvoked the runtime"),
            ),
            mock.patch(
                "boundary_proof_behavior._validate_run", return_value=metrics
            ),
        ):
            self.assertEqual(
                validate_behavior(change_id)["result"],
                "pass",
            )

    def test_parent_runtime_environment_forwards_only_closed_proxy_names(
        self,
    ) -> None:
        environment = _runtime_environment(
            Path("/runtime-home"),
            "/usr/bin:/bin",
            "transient-canary",
            parent_environment={
                "HTTPS_PROXY": "http://proxy.invalid",
                "no_proxy": "localhost",
                "OPENAI_API_KEY": "must-not-cross",
                "UNRELATED": "must-not-cross",
            },
        )
        self.assertEqual(
            set(environment),
            {
                "BOUNDARY_PROOF_CANARY",
                "CODEX_HOME",
                "HOME",
                "PATH",
                "HTTPS_PROXY",
                "no_proxy",
            },
        )
        self.assertNotIn("must-not-cross", environment.values())
        proxy_names = {
            "ALL_PROXY",
            "HTTPS_PROXY",
            "HTTP_PROXY",
            "NO_PROXY",
            "all_proxy",
            "https_proxy",
            "http_proxy",
            "no_proxy",
        }
        for proxy_name in proxy_names:
            with self.subTest(proxy_name=proxy_name):
                isolated = _runtime_environment(
                    Path("/runtime-home"),
                    "/usr/bin:/bin",
                    "transient-canary",
                    parent_environment={
                        proxy_name: "http://proxy.invalid",
                        "OPENAI_API_KEY": "must-not-cross",
                    },
                )
                self.assertEqual(
                    set(isolated),
                    {
                        "BOUNDARY_PROOF_CANARY",
                        "CODEX_HOME",
                        "HOME",
                        "PATH",
                        proxy_name,
                    },
                )

    def test_invocation_profile_uses_approved_exact_literals(self) -> None:
        manifest = _build_behavior_manifest(ROOT, self._attestation())
        self.assertEqual(
            manifest["manifest_id"], "boundary-behavior-implementation-v3"
        )
        self.assertEqual(manifest["artifact_policy"], ARTIFACT_POLICY)
        profile = manifest["invocation_profile"]
        self.assertEqual(
            profile["orchestration_mode"], "workflow-auto-isolated-v1"
        )
        self.assertEqual(
            profile["instruction_profile"],
            "repository-instructions-plus-runtime-default-v1",
        )
        self.assertEqual(
            profile["tool_profile"],
            "isolated-workspace-readonly-no-network-v1",
        )
        self.assertEqual(profile["python_implementation"], "cpython")
        self.assertEqual(
            manifest["transport_policy"],
            {
                "schema_version": "boundary-transport-policy-v1",
                "turn_deadline_ms": 120000,
                "termination_wait_deadline_ms": 10000,
            },
        )

    def test_behavior_scenario_owns_every_oracle_semantic(self) -> None:
        scenario = json.loads(
            (
                ROOT
                / "tests/fixtures/boundary-proof/simple-change/scenario.json"
            ).read_text(encoding="utf-8")
        )
        request = scenario["request"]
        for required in (
            "exactly four requirements, R1-R4",
            "exactly the closed modes `trim` and `preserve`",
            "leading and trailing Unicode whitespace",
            "return the input text unchanged",
            "fail with `unknown-mode` and return no text",
        ):
            with self.subTest(required=required):
                self.assertIn(required, request)
        self.assertIn("Keep normative behavior limited", request)

    def test_participating_skills_keep_boundary_completion_gate_inline(
        self,
    ) -> None:
        for skill in PARTICIPATING_SKILLS:
            with self.subTest(skill=skill):
                content = (
                    ROOT / "skills" / skill / "SKILL.md"
                ).read_text(encoding="utf-8")
                self.assertIn("## Boundary-first completion gate", content)
                normalized = " ".join(content.split())
                self.assertIn(
                    "If the required reference cannot be loaded", normalized
                )
                reference = (
                    ROOT
                    / "skills"
                    / skill
                    / "references/boundary-proof-model.md"
                ).read_text(encoding="utf-8")
                self.assertIn(
                    "| Dimension ID | Applicability | Governing requirement IDs | "
                    "Boundary IDs | Non-applicability rationale |",
                    reference,
                )
                normalized_reference = " ".join(reference.split())
                self.assertIn(
                    "must match `^[a-z][a-z0-9-]*(\\.[a-z][a-z0-9-]*)+$`",
                    normalized_reference,
                )
                self.assertIn(
                    "Test-case IDs may instead use the repository's "
                    "uppercase numeric grammar",
                    normalized_reference,
                )
                self.assertIn(
                    "literal ASCII `-` sentinel",
                    normalized_reference,
                )
                self.assertIn(
                    "| Proof obligation ID | Governing requirement IDs | "
                    "Boundary or interaction IDs | Test case IDs | "
                    "Automation level | Manual procedure IDs |",
                    reference,
                )

    def test_workflow_turn_binds_orchestrator_and_all_stage_owners(self) -> None:
        request = _turn_start_request(
            "thread-1",
            Path("/isolated-workspace"),
            "gpt-5.6-sol",
            Path("/runtime-home"),
            "Author the artifact.",
            "# Boundary-first proof model\n",
            {"type": "object"},
            PARTICIPATING_SKILLS,
        )
        skill_inputs = [
            item for item in request["input"] if item["type"] == "skill"
        ]
        self.assertEqual(
            [item["name"] for item in skill_inputs],
            list(PARTICIPATING_SKILLS),
        )
        text_inputs = [
            item for item in request["input"] if item["type"] == "text"
        ]
        self.assertEqual(len(text_inputs), 2)
        self.assertIn(
            "Required installed boundary-proof reference",
            text_inputs[0]["text"],
        )

    def test_review_payload_requires_durable_identity_bound_evidence(self) -> None:
        identity = "sha256:" + "a" * 64
        payload = {
            "review_id": "spec-review-r1",
            "outcome": "approved",
            "material_finding_ids": [],
            "finding_projection": [],
            "finding_projection_identity": _projection_identity([]),
            "correction_eligibility": "not-applicable",
            "review_record_markdown": (
                "# Review\n\nReview ID: spec-review-r1\nStage: spec-review\n"
                "Status: approved\n"
                f"Reviewed artifact identity: {identity}\n"
                "Material findings: none\nRecording status: recorded\n"
                "## Evidence\nAll closed boundary rows were reviewed.\n"
                "## Review result\nApproved.\n"
            ),
            "review_log_markdown": (
                "Review ID: spec-review-r1\nStage: spec-review\n"
                "Status: approved\n"
                f"Reviewed artifact identity: {identity}\n"
                "Material findings: none\n"
            ),
        }
        _validate_review_payload(
            payload, stage="spec-review", artifact_identity=identity
        )
        malformed = copy.deepcopy(payload)
        malformed["review_record_markdown"] = "Status: approved"
        with self.assertRaises(BoundaryRuntimeError):
            _validate_review_payload(
                malformed, stage="spec-review", artifact_identity=identity
            )
        nonapproval = copy.deepcopy(payload)
        nonapproval["outcome"] = "changes-requested"
        nonapproval["material_finding_ids"] = ["finding.missing-boundary"]
        nonapproval["review_record_markdown"] = nonapproval[
            "review_record_markdown"
        ].replace(
            "Status: approved",
            "Status: changes-requested",
        ).replace(
            "Material findings: none",
            "Material findings: finding.missing-boundary",
        )
        nonapproval["review_log_markdown"] = nonapproval[
            "review_log_markdown"
        ].replace(
            "Status: approved",
            "Status: changes-requested",
        ).replace(
            "Material findings: none",
            "Material findings: finding.missing-boundary",
        )
        projection = _finding_projection("finding.missing-boundary")
        nonapproval["finding_projection"] = projection
        nonapproval["finding_projection_identity"] = _projection_identity(
            projection
        )
        nonapproval["correction_eligibility"] = "automatic-eligible"
        with self.assertRaises(BoundaryRuntimeError) as raised:
            _validate_review_payload(
                nonapproval, stage="spec-review", artifact_identity=identity
            )
        self.assertEqual(raised.exception.diagnostic_id, "review-nonapproval")

    def test_review_finding_projection_owns_correction_authority(self) -> None:
        finding_id = "finding.boundary-ambiguity"
        record = (
            "# Review\n\n"
            "Review ID: spec-review-r1\n"
            "Stage: spec-review\n"
            "Status: changes-requested\n"
            "Reviewed artifact identity: sha256:" + "a" * 64 + "\n"
            f"Material findings: {finding_id}\n"
            "Recording status: recorded\n\n"
            f"## Finding {finding_id}\n\n"
            f"- Finding ID: {finding_id}\n"
            "- Evidence: R2 does not define the Unicode property.\n"
            "- Required outcome: Name the exact Unicode property.\n"
            "- Safe resolution path: Replace the ambiguous term in R2.\n"
            "- needs-decision rationale: none\n"
        )
        log = (
            "Review ID: spec-review-r1\n"
            "Stage: spec-review\n"
            "Status: changes-requested\n"
            "Reviewed artifact identity: sha256:" + "a" * 64 + "\n"
            f"Material findings: {finding_id}\n"
        )
        payload = _review_payload_from_markdown(
            "spec-review", record, log
        )
        self.assertEqual(
            payload["correction_eligibility"], "automatic-eligible"
        )
        self.assertEqual(
            payload["finding_projection"],
            _runtime_finding_projection(
                record, "changes-requested", [finding_id]
            ),
        )

        owner_record = record.replace(
            "- needs-decision rationale: none",
            "- needs-decision rationale: The owner must choose compatibility.",
        )
        owner_payload = _review_payload_from_markdown(
            "spec-review", owner_record, log
        )
        self.assertEqual(
            owner_payload["correction_eligibility"],
            "owner-decision-required",
        )

        incomplete = record.replace(
            "- Safe resolution path: Replace the ambiguous term in R2.",
            "- Safe resolution path:",
        )
        with self.assertRaises(BoundaryRuntimeError) as raised:
            _review_payload_from_markdown("spec-review", incomplete, log)
        self.assertEqual(
            raised.exception.diagnostic_id,
            "protocol-shape-incompatible",
        )

    def test_t52_authority_projection_rejects_every_recognized_field_defect(
        self,
    ) -> None:
        finding_id = "finding.boundary"
        base = (
            f"## Finding {finding_id}\n"
            f"- Finding ID: {finding_id}\n"
            "- Evidence: evidence\n"
            "- Required outcome: outcome\n"
            "- Safe resolution path: resolution\n"
            "- needs-decision rationale: none\n"
        )
        mutations = {
            "missing": base.replace("- Evidence: evidence\n", ""),
            "repeated": base.replace(
                "- Evidence: evidence\n",
                "- Evidence: evidence\n- Evidence: repeated\n",
            ),
            "empty": base.replace(
                "- Required outcome: outcome",
                "- Required outcome:",
            ),
            "out_of_order": base.replace(
                "- Evidence: evidence\n- Required outcome: outcome\n",
                "- Required outcome: outcome\n- Evidence: evidence\n",
            ),
            "extra_recognized": base.replace(
                "- Evidence: evidence\n",
                "- Evidence: evidence\n- Evidence: extra\n",
            ),
            "heading_label_mismatch": base.replace(
                f"- Finding ID: {finding_id}",
                "- Finding ID: finding.other",
            ),
        }
        for name, record in mutations.items():
            with self.subTest(name=name):
                with self.assertRaises(BoundaryRuntimeError) as raised:
                    _runtime_finding_projection(
                        record, "changes-requested", [finding_id]
                    )
                self.assertEqual(
                    raised.exception.diagnostic_id,
                    "protocol-shape-incompatible",
                )

        duplicate = base + "\n" + base
        with self.assertRaises(BoundaryRuntimeError):
            _runtime_finding_projection(
                duplicate,
                "changes-requested",
                [finding_id, finding_id],
            )

        unknown_prose = base.replace(
            "- Evidence: evidence\n",
            "- Evidence: evidence\n- Unknown label: ignored\n",
        )
        self.assertEqual(
            _runtime_finding_projection(
                unknown_prose, "changes-requested", [finding_id]
            ),
            _runtime_finding_projection(
                base, "changes-requested", [finding_id]
            ),
        )

    def test_t52_owner_decision_eligibility_covers_every_nonempty_subset(
        self,
    ) -> None:
        finding_ids = (
            "finding.alpha",
            "finding.beta",
            "finding.gamma",
        )
        for mask in range(8):
            blocks = []
            for index, finding_id in enumerate(finding_ids):
                rationale = (
                    "owner decision required"
                    if mask & (1 << index)
                    else "none"
                )
                blocks.append(
                    f"## Finding {finding_id}\n"
                    f"- Finding ID: {finding_id}\n"
                    "- Evidence: evidence\n"
                    "- Required outcome: outcome\n"
                    "- Safe resolution path: resolution\n"
                    f"- needs-decision rationale: {rationale}\n"
                )
            record = "\n".join(blocks)
            projection = _runtime_finding_projection(
                record, "changes-requested", list(finding_ids)
            )
            payload = {
                "review_id": "spec-review-r1",
                "outcome": "changes-requested",
                "material_finding_ids": list(finding_ids),
                "finding_projection": projection,
                "finding_projection_identity": _projection_identity(
                    projection
                ),
                "correction_eligibility": (
                    "owner-decision-required"
                    if mask
                    else "automatic-eligible"
                ),
                "review_record_markdown": (
                    "Review ID: spec-review-r1\n"
                    "Stage: spec-review\n"
                    "Status: changes-requested\n"
                    "Reviewed artifact identity: sha256:" + "a" * 64 + "\n"
                    "Material findings: " + ", ".join(finding_ids) + "\n"
                    "Recording status: recorded\n"
                    + record
                ),
                "review_log_markdown": (
                    "Review ID: spec-review-r1\n"
                    "Stage: spec-review\n"
                    "Status: changes-requested\n"
                    "Reviewed artifact identity: sha256:" + "a" * 64 + "\n"
                    "Material findings: " + ", ".join(finding_ids) + "\n"
                ),
            }
            with self.subTest(mask=mask):
                _validate_review_payload(
                    payload,
                    stage="spec-review",
                    artifact_identity="sha256:" + "a" * 64,
                    require_approval=False,
                )
        invalid = dict(payload)
        invalid["correction_eligibility"] = "unknown"
        with self.assertRaises(BoundaryRuntimeError):
            _validate_review_payload(
                invalid,
                stage="spec-review",
                artifact_identity="sha256:" + "a" * 64,
                require_approval=False,
            )
        missing = dict(payload)
        missing.pop("correction_eligibility")
        with self.assertRaises(BoundaryRuntimeError):
            _validate_review_payload(
                missing,
                stage="spec-review",
                artifact_identity="sha256:" + "a" * 64,
                require_approval=False,
            )

    def test_t52_correction_stop_package_and_discard_recovery(
        self,
    ) -> None:
        for stage in ("spec-review", "test-spec-review"):
            with self.subTest(stage=stage), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                change_id = "2026-07-25-example"
                (root / "docs/changes" / change_id).mkdir(parents=True)
                run_id = "run-" + ("1" if stage == "spec-review" else "2") * 32
                lease, working = _create_publisher_lease(
                    root,
                    change_id,
                    run_id,
                    "publisher-" + "3" * 32,
                    "sha256:" + "4" * 64,
                )
                artifact_identity = "sha256:" + "5" * 64
                payload, resolution = _owner_decision_review(
                    stage, artifact_identity
                )
                receipt = _write_correction_stop(
                    working,
                    lease,
                    stage=stage,
                    reviewed_artifact_identity=artifact_identity,
                    review_payload=payload,
                    resolution_markdown=resolution,
                )
                _validate_correction_stop_evidence(working, receipt)
                _working_tree_identity(working, lease)
                self.assertFalse(
                    (working.parent / f".prepared-{run_id}").exists()
                )
                self.assertFalse((working.parent / "runs" / run_id).exists())
                self.assertFalse((working.parent / "current.json").exists())

                authority = _recovery_authority(root, change_id)
                result = discard_interrupted_publication(
                    change_id,
                    authority,
                    authorized_by="test-maintainer",
                    repo_root=root,
                )
                quarantine = root / str(result["quarantine_path"])
                self.assertTrue(
                    (quarantine / "correction-stop.json").is_file()
                )
                self.assertEqual(
                    _completed_correction_stop_input_identities(
                        root, change_id
                    ),
                    frozenset({lease["input_set_identity"]}),
                )
                with self.assertRaises(BoundaryRuntimeError) as raised:
                    _assert_correction_input_is_fresh(
                        root,
                        change_id,
                        str(lease["input_set_identity"]),
                    )
                self.assertEqual(
                    raised.exception.diagnostic_id,
                    "correction-authorization-required",
                )
                _assert_correction_input_is_fresh(
                    root, change_id, "sha256:" + "6" * 64
                )

    def test_t52_correction_stop_package_rejects_boundary_mutations(
        self,
    ) -> None:
        mutations = ("missing", "extra", "symlink", "fifo", "stale")
        for mutation in mutations:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                lease = {
                    "run_id": "run-" + "1" * 32,
                    "publisher_instance_id": "publisher-" + "2" * 32,
                    "input_set_identity": "sha256:" + "3" * 64,
                }
                artifact_identity = "sha256:" + "4" * 64
                payload, resolution = _owner_decision_review(
                    "spec-review", artifact_identity
                )
                _write_correction_stop(
                    root,
                    lease,
                    stage="spec-review",
                    reviewed_artifact_identity=artifact_identity,
                    review_payload=payload,
                    resolution_markdown=resolution,
                )
                evidence = root / "correction-stop-evidence"
                target = evidence / "review-log.md"
                if mutation == "missing":
                    target.unlink()
                elif mutation == "extra":
                    (evidence / "extra").write_text("x", encoding="utf-8")
                elif mutation == "symlink":
                    target.unlink()
                    target.symlink_to(evidence / "review-record.md")
                elif mutation == "fifo":
                    target.unlink()
                    os.mkfifo(target)
                else:
                    target.write_text("stale", encoding="utf-8")
                with self.assertRaises(BoundaryRuntimeError):
                    _working_tree_identity(root, lease)

    def test_correction_stop_receipt_is_identity_bound_and_closed(self) -> None:
        lease = {
            "run_id": "run-" + "1" * 32,
            "publisher_instance_id": "publisher-" + "2" * 32,
            "input_set_identity": "sha256:" + "a" * 64,
        }
        receipt = {
            "schema_version": "simple-change-correction-stop-v1",
            **lease,
            "stage": "spec-review",
            "attempt": 1,
            "review_id": "spec-review-r1",
            "reviewed_artifact_identity": "sha256:" + "b" * 64,
            "material_finding_ids": ["finding.boundary-ambiguity"],
            "finding_projection_identity": "sha256:" + "c" * 64,
            "diagnostic_id": "correction-authorization-required",
        }
        _validate_correction_stop_receipt(receipt, lease=lease)

        unknown_field = dict(receipt, unexpected=True)
        with self.assertRaises(BoundaryRuntimeError):
            _validate_correction_stop_receipt(
                unknown_field, lease=lease
            )

        rebound = dict(receipt, input_set_identity="sha256:" + "d" * 64)
        with self.assertRaises(BoundaryRuntimeError):
            _validate_correction_stop_receipt(rebound, lease=lease)

    def test_working_tree_identity_accepts_only_closed_assembled_paths(
        self,
    ) -> None:
        allowed_files, allowed_directories = _assembled_working_paths()
        self.assertIn(
            "review-evidence/spec-review-bundle.json", allowed_files
        )
        self.assertEqual(
            allowed_directories,
            {"feature-spec", "test-spec", "review-evidence"},
        )
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            artifact = (
                root
                / "artifacts"
                / "review-evidence"
                / "spec-review-bundle.json"
            )
            artifact.parent.mkdir(parents=True)
            artifact.write_text("{}", encoding="utf-8")
            identity = _working_tree_identity(root)
            self.assertRegex(identity, r"^sha256:[0-9a-f]{64}$")

            prohibited = root / "artifacts" / "review-evidence" / "extra.json"
            prohibited.write_text("{}", encoding="utf-8")
            with self.assertRaises(BoundaryRuntimeError):
                _working_tree_identity(root)

    def test_scenario_expectations_compare_after_observation(self) -> None:
        observed_cases = {
            ("zero-correction", None): [
                {"stage": "spec", "attempt": 1},
                {"stage": "test-spec", "attempt": 1},
            ],
            ("one-correction", "feature-spec"): [
                {"stage": "spec", "attempt": 1},
                {"stage": "spec", "attempt": 2},
                {"stage": "test-spec", "attempt": 1},
            ],
            ("one-correction", "test-spec"): [
                {"stage": "spec", "attempt": 1},
                {"stage": "test-spec", "attempt": 1},
                {"stage": "test-spec", "attempt": 2},
            ],
        }
        for observed, events in observed_cases.items():
            self.assertEqual(_observed_scenario_outcome(events), observed)
            for expected in observed_cases:
                scenario = {
                    "expected_branch": expected[0],
                    "corrected_role": expected[1],
                }
                with self.subTest(observed=observed, expected=expected):
                    if expected == observed:
                        _validate_scenario_expectations(scenario, events)
                    else:
                        with self.assertRaises(
                            BoundaryRuntimeError
                        ) as raised:
                            _validate_scenario_expectations(scenario, events)
                        self.assertEqual(
                            raised.exception.diagnostic_id,
                            "boundary-oracle-mismatch",
                        )

        with self.assertRaises(BoundaryRuntimeError):
            _observed_scenario_outcome(
                [
                    {"stage": "spec", "attempt": 2},
                    {"stage": "test-spec", "attempt": 2},
                ]
            )

    def test_t52_request_only_projection_excludes_parent_expectations(
        self,
    ) -> None:
        request = "Author exactly the authoritative four-requirement record."
        scenario = {
            "scenario_id": "BFP-SIMPLE-001",
            "request": request,
            "expected_branch": "one-correction",
            "corrected_role": "test-spec",
        }
        projected = _workflow_stage_request(
            "spec",
            "Author the feature specification.",
            artifact_context=scenario["request"],
        )
        serialized = json.dumps(projected, sort_keys=True)
        self.assertIn(request, serialized)
        self.assertNotIn("expected_branch", serialized)
        self.assertNotIn("one-correction", serialized)
        self.assertNotIn("corrected_role", serialized)
        self.assertNotIn("test-spec", serialized)

        changed_expectations = {
            **scenario,
            "expected_branch": "zero-correction",
            "corrected_role": None,
        }
        projected_again = _workflow_stage_request(
            "spec",
            "Author the feature specification.",
            artifact_context=changed_expectations["request"],
        )
        self.assertEqual(projected, projected_again)

    def test_closed_artifact_classifier_covers_repository_boundaries(self) -> None:
        change_id = "2026-07-25-example"
        cases = {
            "specs/example.md": "feature-spec",
            "specs/example.test.md": "test-spec",
            f"docs/changes/{change_id}/reviews/spec-review-r1.md": "review-evidence",
            f"docs/changes/{change_id}/review-log.md": "review-evidence",
            "docs/proposals/example.md": "other-lifecycle",
            "docs/architecture/system/architecture.md": "other-lifecycle",
            f"docs/changes/{change_id}/change.yaml": "other-lifecycle",
            f"docs/changes/{change_id}/evidence/manifest.json": "non-lifecycle",
        }
        for path, expected in cases.items():
            with self.subTest(path=path):
                self.assertEqual(_artifact_kind(path, change_id), expected)

    def test_t51_publisher_identity_exact_schema_and_binding(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            (root / "docs/changes" / change_id).mkdir(parents=True)
            publisher_id = "publisher-" + "1" * 32
            lease, _ = _create_publisher_lease(
                root, change_id, "run-" + "a" * 32, publisher_id,
                "sha256:" + "b" * 64,
            )
            _validate_publisher_lease(root, change_id, lease)
            for field in tuple(lease):
                with self.subTest(field=field):
                    invalid = dict(lease)
                    invalid.pop(field)
                    with self.assertRaises(BoundaryRuntimeError):
                        _validate_publisher_lease(root, change_id, invalid)
            invalid = dict(lease)
            invalid["publisher_instance_id"] = "publisher-invalid"
            with self.assertRaises(BoundaryRuntimeError):
                _validate_publisher_lease(root, change_id, invalid)

    def test_t51_publisher_lock_reports_publisher_active(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            (root / "docs/changes" / change_id).mkdir(parents=True)
            with _publisher_lock(root, change_id):
                with self.assertRaises(BoundaryRuntimeError) as caught:
                    with _publisher_lock(root, change_id):
                        self.fail("a second publisher acquired the lock")
            self.assertEqual(caught.exception.diagnostic_id, "publisher-active")

    def test_t51_lease_before_stage_observation(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            (root / "docs/changes" / change_id).mkdir(parents=True)
            lease, working = _create_publisher_lease(
                root, change_id, "run-" + "a" * 32,
                "publisher-" + "1" * 32, "sha256:" + "b" * 64,
            )
            observed = json.loads(
                (working.parent / "publisher.json").read_text(encoding="utf-8")
            )
            self.assertEqual(observed, lease)
            self.assertTrue(working.is_dir())

    def test_t51_root_binding_rejects_each_substitution(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            (root / "docs/changes" / change_id).mkdir(parents=True)
            lease, _ = _create_publisher_lease(
                root, change_id, "run-" + "a" * 32,
                "publisher-" + "1" * 32, "sha256:" + "b" * 64,
            )
            for field in ("working_root", "staging_root", "target_root"):
                with self.subTest(field=field):
                    invalid = dict(lease)
                    invalid[field] = str(invalid[field]) + "-other"
                    with self.assertRaises(BoundaryRuntimeError):
                        _validate_publisher_lease(root, change_id, invalid)

    def test_t51_global_discovery_rejects_cross_run_and_unknown_transients(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            (root / "docs/changes" / change_id).mkdir(parents=True)
            lease, _ = _create_publisher_lease(
                root, change_id, "run-" + "a" * 32,
                "publisher-" + "1" * 32, "sha256:" + "b" * 64,
            )
            self.assertEqual(
                _discover_global_candidate(root, change_id), lease["run_id"]
            )
            simple = root / "docs/changes" / change_id / "evidence/simple-change"
            cross_run = simple / (".prepared-run-" + "c" * 32)
            cross_run.mkdir()
            with self.assertRaises(BoundaryRuntimeError):
                _discover_global_candidate(root, change_id)
            cross_run.rmdir()
            (simple / ".working-not-a-run").mkdir()
            with self.assertRaises(BoundaryRuntimeError):
                _discover_global_candidate(root, change_id)

    def test_t51_global_discovery_rejects_malformed_completed_history(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            simple = (
                root / "docs/changes" / change_id / "evidence/simple-change"
            )
            simple.mkdir(parents=True)
            run_id = "run-" + "a" * 32
            basis = {
                "run_id": run_id,
                "recovery_id": "not-a-recovery-id",
                "orphan_snapshot": {"quarantine_path": None},
            }
            basis_path = simple / f"manual-recovery-{run_id}.json"
            basis_path.write_text(
                json.dumps(basis, separators=(",", ":"), sort_keys=True),
                encoding="utf-8",
            )
            state = {
                "schema_version": "simple-change-manual-recovery-state-v1",
                "recovery_id": "not-a-recovery-id",
                "basis_identity": (
                    "sha256:" + hashlib.sha256(basis_path.read_bytes()).hexdigest()
                ),
                "state": "completed",
            }
            (
                simple / f"manual-recovery-state-{run_id}.json"
            ).write_text(
                json.dumps(state, separators=(",", ":"), sort_keys=True),
                encoding="utf-8",
            )
            with self.assertRaises(BoundaryRuntimeError):
                _discover_global_candidate(root, change_id)

    def test_t51_global_discovery_rejects_multiple_recovery_temps(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            (root / "docs/changes" / change_id).mkdir(parents=True)
            run_id = "run-" + "a" * 32
            _, working = _create_publisher_lease(
                root, change_id, run_id, "publisher-" + "1" * 32,
                "sha256:" + "b" * 64,
            )
            for value in ("2", "3"):
                (
                    working.parent
                    / f".manual-recovery-{run_id}-recovery-{value * 32}.tmp"
                ).write_text("{}", encoding="utf-8")
            with self.assertRaises(BoundaryRuntimeError):
                _discover_global_candidate(root, change_id)

    def test_t51_same_live_publisher_is_not_reconstructed_on_resume(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            (root / "docs/changes" / change_id).mkdir(parents=True)
            _create_publisher_lease(
                root, change_id, "run-" + "a" * 32,
                "publisher-" + "1" * 32, "sha256:" + "b" * 64,
            )
            with self.assertRaises(BoundaryRuntimeError):
                _reconcile_prepared(root, change_id)

    def test_t51_receipt_binding_rejects_lease_identity_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            (root / "docs/changes" / change_id).mkdir(parents=True)
            lease, _ = _create_publisher_lease(
                root, change_id, "run-" + "a" * 32,
                "publisher-" + "1" * 32, "sha256:" + "b" * 64,
            )
            identity = "sha256:" + "c" * 64
            receipt = {
                "publisher_instance_id": lease["publisher_instance_id"],
                "run_id": lease["run_id"],
                "input_set_identity": lease["input_set_identity"],
                "staged_manifest_snapshot": {
                    "path": str(lease["staging_root"]) + "/manifest.json",
                    "identity": identity,
                },
                "target_manifest": {
                    "path": str(lease["target_root"]) + "/manifest.json",
                    "identity": identity,
                },
                "prior_pointer": lease["prior_pointer"],
            }
            _validate_prepared_receipt(root, change_id, receipt, lease)
            for field in (
                "publisher_instance_id", "run_id",
                "input_set_identity", "prior_pointer",
            ):
                with self.subTest(field=field):
                    invalid = copy.deepcopy(receipt)
                    invalid[field] = "different"
                    with self.assertRaises(BoundaryRuntimeError):
                        _validate_prepared_receipt(
                            root, change_id, invalid, lease
                        )

    def test_t51_manual_recovery_intent_never_adopts_or_reinvokes(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            (root / "docs/changes" / change_id).mkdir(parents=True)
            run_id = "run-" + "a" * 32
            _, working = _create_publisher_lease(
                root, change_id, run_id, "publisher-" + "1" * 32,
                "sha256:" + "b" * 64,
            )
            child = working / "boundary-proof-workspace-abcdefgh"
            child.mkdir()
            marker = child / "manifested.txt"
            marker.write_text("untrusted", encoding="utf-8")
            authority = _recovery_authority(root, change_id)
            before = marker.read_bytes()
            result = discard_interrupted_publication(
                change_id,
                authority,
                authorized_by="test-maintainer",
                repo_root=root,
            )
            quarantine = root / str(result["quarantine_path"])
            self.assertEqual(
                (quarantine / child.name / marker.name).read_bytes(), before
            )
            self.assertFalse((working.parent / "runs" / run_id).exists())
            self.assertFalse((working.parent / "publisher.json").exists())
            state = json.loads(
                (
                    working.parent
                    / f"manual-recovery-state-{run_id}.json"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(state["state"], "completed")

    def test_t51_manual_recovery_rejects_unknown_working_descendant(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            (root / "docs/changes" / change_id).mkdir(parents=True)
            run_id = "run-" + "a" * 32
            _, working = _create_publisher_lease(
                root, change_id, run_id, "publisher-" + "1" * 32,
                "sha256:" + "b" * 64,
            )
            (working / "unknown-outside-approved-workspace").write_text(
                "untrusted", encoding="utf-8"
            )
            authority = _recovery_authority(root, change_id)
            with self.assertRaises(BoundaryRuntimeError):
                discard_interrupted_publication(
                    change_id,
                    authority,
                    authorized_by="test-maintainer",
                    repo_root=root,
                )

    def test_t51_manual_recovery_rejects_invalid_staged_run(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            (root / "docs/changes" / change_id).mkdir(parents=True)
            run_id = "run-" + "a" * 32
            lease, working = _create_publisher_lease(
                root, change_id, run_id, "publisher-" + "1" * 32,
                "sha256:" + "b" * 64,
            )
            staging = root / str(lease["staging_root"])
            working.rename(staging)
            (staging / "junk").write_text("not a staged run", encoding="utf-8")
            authority = _recovery_authority(root, change_id)
            with self.assertRaises(BoundaryRuntimeError):
                discard_interrupted_publication(
                    change_id,
                    authority,
                    authorized_by="test-maintainer",
                    repo_root=root,
                )

    def test_t51_manual_recovery_cleans_one_bound_malformed_temp(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            (root / "docs/changes" / change_id).mkdir(parents=True)
            run_id = "run-" + "a" * 32
            _, working = _create_publisher_lease(
                root, change_id, run_id, "publisher-" + "1" * 32,
                "sha256:" + "b" * 64,
            )
            recovery_id = "recovery-" + "2" * 32
            simple = working.parent
            (
                simple / f".manual-recovery-{run_id}-{recovery_id}.tmp"
            ).write_bytes(b"{")
            authority = _recovery_authority(root, change_id)
            result = discard_interrupted_publication(
                change_id,
                authority,
                authorized_by="test-maintainer",
                repo_root=root,
            )
            self.assertEqual(result["result"], "completed")
            self.assertFalse(
                (
                    simple / f".manual-recovery-{run_id}-{recovery_id}.tmp"
                ).exists()
            )

    def test_t51_manual_recovery_basis_and_state_schemas_are_exact(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            (root / "docs/changes" / change_id).mkdir(parents=True)
            run_id = "run-" + "a" * 32
            _, working = _create_publisher_lease(
                root, change_id, run_id, "publisher-" + "1" * 32,
                "sha256:" + "b" * 64,
            )
            authority = _recovery_authority(root, change_id)
            with self.assertRaises(BoundaryRuntimeError):
                discard_interrupted_publication(
                    change_id,
                    authority,
                    authorized_by="test-maintainer",
                    repo_root=root,
                    crash_at="after-recovery-authorized",
                )
            basis_path = working.parent / f"manual-recovery-{run_id}.json"
            state_path = (
                working.parent / f"manual-recovery-state-{run_id}.json"
            )
            basis = json.loads(basis_path.read_text(encoding="utf-8"))
            state = json.loads(state_path.read_text(encoding="utf-8"))
            _validate_recovery_basis(
                root, change_id, basis, expected_run_id=run_id
            )
            _validate_recovery_state(
                state,
                basis_identity=(
                    "sha256:" + hashlib.sha256(basis_path.read_bytes()).hexdigest()
                ),
                recovery_id=basis["recovery_id"],
            )
            for field in tuple(basis):
                with self.subTest(record="basis", field=field):
                    invalid = copy.deepcopy(basis)
                    invalid.pop(field)
                    with self.assertRaises(BoundaryRuntimeError):
                        _validate_recovery_basis(
                            root,
                            change_id,
                            invalid,
                            expected_run_id=run_id,
                        )
            for parent in (
                "publisher_lease_snapshot",
                "publisher_lock_proof",
                "orphan_snapshot",
            ):
                for field in tuple(basis[parent]):
                    with self.subTest(record=parent, field=field):
                        invalid = copy.deepcopy(basis)
                        invalid[parent].pop(field)
                        with self.assertRaises(BoundaryRuntimeError):
                            _validate_recovery_basis(
                                root,
                                change_id,
                                invalid,
                                expected_run_id=run_id,
                            )
            for field in tuple(state):
                with self.subTest(record="state", field=field):
                    invalid = dict(state)
                    invalid.pop(field)
                    with self.assertRaises(BoundaryRuntimeError):
                        _validate_recovery_state(invalid)
            invalid = dict(state)
            invalid["state"] = "unknown"
            with self.assertRaises(BoundaryRuntimeError):
                _validate_recovery_state(invalid)

    def test_t51_completed_history_rejects_changed_quarantine(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            (root / "docs/changes" / change_id).mkdir(parents=True)
            run_id = "run-" + "a" * 32
            _, working = _create_publisher_lease(
                root, change_id, run_id, "publisher-" + "1" * 32,
                "sha256:" + "b" * 64,
            )
            authority = _recovery_authority(root, change_id)
            result = discard_interrupted_publication(
                change_id,
                authority,
                authorized_by="test-maintainer",
                repo_root=root,
            )
            quarantine = root / str(result["quarantine_path"])
            (quarantine / "changed").write_text("tampered", encoding="utf-8")
            with self.assertRaises(BoundaryRuntimeError):
                _discover_global_candidate(root, change_id)

    def test_t51_completed_history_does_not_hide_same_run_staging(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            (root / "docs/changes" / change_id).mkdir(parents=True)
            run_id = "run-" + "a" * 32
            _, working = _create_publisher_lease(
                root, change_id, run_id, "publisher-" + "1" * 32,
                "sha256:" + "b" * 64,
            )
            authority = _recovery_authority(root, change_id)
            discard_interrupted_publication(
                change_id,
                authority,
                authorized_by="test-maintainer",
                repo_root=root,
            )
            (working.parent / f".prepared-{run_id}").mkdir()
            with self.assertRaises(BoundaryRuntimeError):
                _discover_global_candidate(root, change_id)

    def test_t51_manual_recovery_rejects_semantically_empty_staged_run(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            (root / "docs/changes" / change_id).mkdir(parents=True)
            run_id = "run-" + "a" * 32
            publisher_id = "publisher-" + "1" * 32
            fake_ref = {
                "path": "missing",
                "identity": "sha256:" + "b" * 64,
            }
            input_set = {
                "schema_version": "simple-change-input-v1",
                "scenario_ref": fake_ref,
                "baseline_commit": "git:" + "c" * 40,
                "skill_resource_refs": [],
                "oracle_refs": [],
                "implementation_manifest_ref": fake_ref,
            }
            input_identity = (
                "sha256:"
                + hashlib.sha256(
                    json.dumps(
                        input_set,
                        ensure_ascii=False,
                        separators=(",", ":"),
                        sort_keys=True,
                    ).encode()
                ).hexdigest()
            )
            lease, working = _create_publisher_lease(
                root,
                change_id,
                run_id,
                publisher_id,
                input_identity,
            )
            staging = root / str(lease["staging_root"])
            working.rename(staging)
            manifest = {
                "run_id": run_id,
                "publisher_instance_id": publisher_id,
                "input_set": input_set,
                "input_set_identity": input_identity,
                "baseline_commit": input_set["baseline_commit"],
                "before_artifact_inventory": [],
                "after_artifact_inventory": [],
                "snapshots": [],
                "events": [],
                "transport_attempts": [],
            }
            (staging / "manifest.json").write_text(
                json.dumps(
                    manifest,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    sort_keys=True,
                ),
                encoding="utf-8",
            )
            authority = _recovery_authority(root, change_id)
            with self.assertRaises(BoundaryRuntimeError):
                discard_interrupted_publication(
                    change_id,
                    authority,
                    authorized_by="test-maintainer",
                    repo_root=root,
                )

    def test_t51_manual_recovery_requires_change_local_authority(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            (root / "docs/changes" / change_id).mkdir(parents=True)
            _create_publisher_lease(
                root, change_id, "run-" + "a" * 32,
                "publisher-" + "1" * 32, "sha256:" + "b" * 64,
            )
            authority = root / "unrelated-owner-note.md"
            authority.write_text("# Unrelated\n", encoding="utf-8")
            with self.assertRaises(BoundaryRuntimeError):
                discard_interrupted_publication(
                    change_id,
                    authority,
                    authorized_by="test-maintainer",
                    repo_root=root,
                )

    def test_t51_manual_recovery_rejects_arbitrary_change_local_markdown(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            change_root = root / "docs/changes" / change_id
            change_root.mkdir(parents=True)
            _create_publisher_lease(
                root, change_id, "run-" + "a" * 32,
                "publisher-" + "1" * 32, "sha256:" + "b" * 64,
            )
            authority = change_root / "validation-note.md"
            authority.write_text(
                "# Unrelated change-local evidence\n", encoding="utf-8"
            )
            with self.assertRaises(BoundaryRuntimeError):
                discard_interrupted_publication(
                    change_id,
                    authority,
                    authorized_by="test-maintainer",
                    repo_root=root,
                )

    def test_t51_recovery_decision_schema_and_subject_are_exact(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            (root / "docs/changes" / change_id).mkdir(parents=True)
            _create_publisher_lease(
                root, change_id, "run-" + "a" * 32,
                "publisher-" + "1" * 32, "sha256:" + "b" * 64,
            )
            authority = _recovery_authority(root, change_id)
            valid = json.loads(authority.read_text(encoding="utf-8"))

            invalid_values = {
                "schema_version": "unknown",
                "change_id": "2026-07-25-other",
                "run_id": "run-" + "c" * 32,
                "publisher_instance_id": "publisher-" + "2" * 32,
                "input_set_identity": "sha256:" + "d" * 64,
                "action": "adopt",
                "authorized_by": "other-maintainer",
                "outcome": "denied",
            }
            candidates: list[tuple[str, dict[str, object]]] = []
            for field, value in invalid_values.items():
                invalid = dict(valid)
                invalid[field] = value
                candidates.append((f"changed-{field}", invalid))
            for field in valid:
                invalid = dict(valid)
                invalid.pop(field)
                candidates.append((f"missing-{field}", invalid))
            invalid = dict(valid)
            invalid["extra"] = True
            candidates.append(("extra-field", invalid))

            for case, invalid in candidates:
                with self.subTest(case=case):
                    authority.write_text(
                        json.dumps(
                            invalid,
                            ensure_ascii=False,
                            separators=(",", ":"),
                            sort_keys=True,
                        ),
                        encoding="utf-8",
                    )
                    with self.assertRaises(BoundaryRuntimeError):
                        discard_interrupted_publication(
                            change_id,
                            authority,
                            authorized_by="test-maintainer",
                            repo_root=root,
                        )
            authority.write_text(
                json.dumps(
                    valid,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    sort_keys=True,
                ),
                encoding="utf-8",
            )
            wrong_path = authority.with_name("other.json")
            wrong_path.write_bytes(authority.read_bytes())
            with self.assertRaises(BoundaryRuntimeError):
                discard_interrupted_publication(
                    change_id,
                    wrong_path,
                    authorized_by="test-maintainer",
                    repo_root=root,
                )

    def test_t51_recovery_decision_identity_cannot_drift_on_resume(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            (root / "docs/changes" / change_id).mkdir(parents=True)
            run_id = "run-" + "a" * 32
            _, working = _create_publisher_lease(
                root, change_id, run_id, "publisher-" + "1" * 32,
                "sha256:" + "b" * 64,
            )
            child = working / "boundary-proof-workspace-abcdefgh"
            child.mkdir()
            (child / "manifested.txt").write_text(
                "untrusted", encoding="utf-8"
            )
            authority = _recovery_authority(root, change_id)
            with self.assertRaises(BoundaryRuntimeError):
                discard_interrupted_publication(
                    change_id,
                    authority,
                    authorized_by="test-maintainer",
                    repo_root=root,
                    crash_at="after-recovery-authorized",
                )
            authority.write_bytes(authority.read_bytes() + b"\n")
            with self.assertRaises(BoundaryRuntimeError):
                discard_interrupted_publication(
                    change_id,
                    authority,
                    authorized_by="test-maintainer",
                    repo_root=root,
                )
            state = json.loads(
                (
                    working.parent
                    / f"manual-recovery-state-{run_id}.json"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(state["state"], "authorized")
            self.assertTrue((working.parent / "publisher.json").is_file())

    def test_t51_global_discovery_rejects_invalid_fixed_root_kind(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            simple = (
                root / "docs/changes" / change_id / "evidence/simple-change"
            )
            simple.mkdir(parents=True)
            (simple / "runs").write_text("not a directory", encoding="utf-8")
            with self.assertRaises(BoundaryRuntimeError):
                _discover_global_candidate(root, change_id)

    def test_t51_manual_recovery_resumes_every_durable_crash_row(self) -> None:
        boundaries = (
            "after-recovery-temp-fsync",
            "after-recovery-basis-install",
            "after-recovery-authorized",
            "after-recovery-quarantine-rename",
            "after-recovery-orphan-detached",
            "after-recovery-lease-delete",
        )
        for index, boundary in enumerate(boundaries):
            with self.subTest(boundary=boundary), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                change_id = "2026-07-25-example"
                (root / "docs/changes" / change_id).mkdir(parents=True)
                run_id = "run-" + format(index + 1, "032x")
                _, working = _create_publisher_lease(
                    root,
                    change_id,
                    run_id,
                    "publisher-" + format(index + 1, "032x"),
                    "sha256:" + "b" * 64,
                )
                child = working / "boundary-proof-workspace-abcdefgh"
                child.mkdir()
                (child / "manifested.txt").write_text(
                    f"attempt-{index}", encoding="utf-8"
                )
                authority = _recovery_authority(root, change_id)
                with self.assertRaises(BoundaryRuntimeError):
                    discard_interrupted_publication(
                        change_id,
                        authority,
                        authorized_by="test-maintainer",
                        repo_root=root,
                        crash_at=boundary,
                    )
                result = discard_interrupted_publication(
                    change_id,
                    authority,
                    authorized_by="test-maintainer",
                    repo_root=root,
                )
                self.assertEqual(result["result"], "completed")
                state = json.loads(
                    (
                        working.parent
                        / f"manual-recovery-state-{run_id}.json"
                    ).read_text(encoding="utf-8")
                )
                self.assertEqual(state["state"], "completed")
                self.assertFalse((working.parent / "publisher.json").exists())

    def test_prepared_publication_reconciles_without_reinvocation(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            simple = (
                root
                / "docs"
                / "changes"
                / change_id
                / "evidence"
                / "simple-change"
            )
            (root / "docs" / "changes" / change_id).mkdir(parents=True)
            run_id = "run-" + "a" * 32
            publisher_id = "publisher-" + "1" * 32
            input_identity = "sha256:" + "b" * 64
            _, temporary = _create_publisher_lease(
                root,
                change_id,
                run_id,
                publisher_id,
                input_identity,
            )
            manifest = {
                "run_id": run_id,
                "publisher_instance_id": publisher_id,
                "input_set_identity": input_identity,
                "snapshots": [],
            }
            (temporary / "manifest.json").write_text(
                json.dumps(
                    manifest,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    sort_keys=True,
                ),
                encoding="utf-8",
            )
            with (
                mock.patch(
                    "boundary_proof_behavior._validate_run",
                    return_value=SimpleNamespace(),
                ) as validate,
                mock.patch(
                    "boundary_proof_behavior._validate_staged_run"
                ),
            ):
                with self.assertRaises(BoundaryRuntimeError):
                    _publish_run(
                        root,
                        change_id,
                        temporary,
                        manifest,
                        crash_at="after-receipt-fsync",
                    )
                self.assertTrue((simple / "prepared.json").is_file())
                self.assertFalse((simple / "current.json").exists())
                competing = simple / ".competing"
                competing.mkdir()
                competing_manifest = {
                    "run_id": "run-" + "c" * 32,
                    "publisher_instance_id": "publisher-" + "2" * 32,
                    "input_set_identity": "sha256:" + "d" * 64,
                    "snapshots": [],
                }
                (competing / "manifest.json").write_text(
                    json.dumps(
                        competing_manifest,
                        ensure_ascii=False,
                        separators=(",", ":"),
                        sort_keys=True,
                    ),
                    encoding="utf-8",
                )
                with self.assertRaises(BoundaryRuntimeError):
                    _publish_run(
                        root,
                        change_id,
                        competing,
                        competing_manifest,
                    )
                _reconcile_prepared(root, change_id)
                self.assertTrue((simple / "current.json").is_file())
                self.assertFalse((simple / "prepared.json").exists())
                self.assertEqual(validate.call_count, 1)

    def test_t51_publication_states_recover_every_post_prepare_crash(
        self,
    ) -> None:
        boundaries = (
            "after-receipt-fsync",
            "after-run-install",
            "after-run-validation",
            "after-pointer-replace",
            "after-parent-fsync",
            "after-receipt-cleanup",
        )
        for index, boundary in enumerate(boundaries):
            with self.subTest(boundary=boundary), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                change_id = "2026-07-25-example"
                simple = (
                    root
                    / "docs"
                    / "changes"
                    / change_id
                    / "evidence"
                    / "simple-change"
                )
                (root / "docs" / "changes" / change_id).mkdir(parents=True)
                run_id = "run-" + format(index + 1, "032x")
                publisher_id = "publisher-" + format(index + 1, "032x")
                input_identity = "sha256:" + "e" * 64
                _, temporary = _create_publisher_lease(
                    root,
                    change_id,
                    run_id,
                    publisher_id,
                    input_identity,
                )
                manifest = {
                    "run_id": run_id,
                    "publisher_instance_id": publisher_id,
                    "input_set_identity": input_identity,
                    "snapshots": [],
                }
                (temporary / "manifest.json").write_text(
                    json.dumps(
                        manifest,
                        ensure_ascii=False,
                        separators=(",", ":"),
                        sort_keys=True,
                    ),
                    encoding="utf-8",
                )
                with (
                    mock.patch(
                        "boundary_proof_behavior._validate_run",
                        return_value=SimpleNamespace(),
                    ),
                    mock.patch(
                        "boundary_proof_behavior._validate_staged_run"
                    ),
                ):
                    with self.assertRaises(BoundaryRuntimeError):
                        _publish_run(
                            root,
                            change_id,
                            temporary,
                            manifest,
                            crash_at=boundary,
                        )
                    _reconcile_prepared(root, change_id)
                    pointer = json.loads(
                        (simple / "current.json").read_text(encoding="utf-8")
                    )
                    self.assertEqual(pointer["run_id"], manifest["run_id"])
                    self.assertFalse((simple / "prepared.json").exists())

    def test_codex_0_145_thread_metadata_binds_the_exact_reported_shape(
        self,
    ) -> None:
        workspace = Path("/isolated-workspace")
        thread = {
            "thread": {"id": "thread-1", "cliVersion": "0.145.0"},
            "model": "gpt-5.6-sol",
            "modelProvider": "openai",
            "serviceTier": None,
            "cwd": str(workspace),
            "runtimeWorkspaceRoots": [],
            "instructionSources": [],
            "approvalPolicy": "never",
            "approvalsReviewer": "user",
            "sandbox": {"type": "readOnly", "networkAccess": False},
            "activePermissionProfile": {
                "id": "boundary-proof-stage-readonly-v1",
                "extends": None,
            },
            "reasoningEffort": None,
            "multiAgentMode": "explicitRequestOnly",
        }
        normalized, thread_id = _validated_thread_metadata(
            thread,
            version="0.145.0",
            model_id="gpt-5.6-sol",
            workspace=workspace,
        )
        self.assertEqual(thread_id, "thread-1")
        self.assertEqual(normalized["workspace_root_roles"], [])

        widened = copy.deepcopy(thread)
        widened["runtimeWorkspaceRoots"] = [str(workspace)]
        with self.assertRaises(BoundaryRuntimeError) as raised:
            _validated_thread_metadata(
                widened,
                version="0.145.0",
                model_id="gpt-5.6-sol",
                workspace=workspace,
            )
        self.assertEqual(
            raised.exception.diagnostic_id,
            "thread-metadata-mismatch",
        )

    def test_runtime_projection_rejects_schema_and_protocol_drift(self) -> None:
        projection = dict(RUNTIME_PROJECTIONS[0])
        protocol_rows = [{"classification": "bound-protocol"}]
        feature_rows = [{"classification": "bound-features"}]
        with mock.patch(
            "boundary_proof_behavior._sha256",
            side_effect=[
                projection["protocol_item_classification_identity"],
                projection["feature_classification_identity"],
            ],
        ):
            complete = _validate_runtime_projection(
                str(projection["runtime_version"]),
                str(projection["runtime_launcher_identity"]),
                str(projection["runtime_package_identity"]),
                str(projection["schema_bundle_identity"]),
                protocol_rows,
            )
            self.assertEqual(complete(feature_rows), projection)

        complete = _validate_runtime_projection(
            str(projection["runtime_version"]),
            "sha256:" + "0" * 64,
            str(projection["runtime_package_identity"]),
            str(projection["schema_bundle_identity"]),
            protocol_rows,
        )
        with self.assertRaises(BoundaryRuntimeError) as raised:
            complete(feature_rows)
        self.assertEqual(
            raised.exception.diagnostic_id,
            "runtime-projection-unsupported",
        )

    def test_codex_0_145_projection_matches_approved_literal_oracle(
        self,
    ) -> None:
        self.assertEqual(
            RUNTIME_SCHEMA_IDENTITY_BY_VERSION,
            {
                "0.145.0": (
                    "sha256:"
                    "18d79891673d9d43a8e7a49864fef49a04305bd13571a8aef45824209f1bfae8"
                )
            },
        )
        self.assertEqual(
            RUNTIME_PROTOCOL_CLASSIFICATION_IDENTITY_BY_VERSION,
            {
                "0.145.0": (
                    "sha256:"
                    "35f1203d9c6abc62ef3f1aca94e2f3165e0213697d554ab11d0477d9cd7e4bf8"
                )
            },
        )
        self.assertEqual(len(CODEX_0_145_0_FEATURES), 96)
        self.assertEqual(len(set(CODEX_0_145_0_FEATURES)), 96)

    def test_turn_collection_enforces_every_observed_protocol_event(self) -> None:
        classifications = [
            {
                "item_variant": f"ServerNotification:{method}",
                "classification": "non-side-effect-protocol-traffic",
            }
            for method in (
                "remoteControl/status/changed",
                "item/completed",
                "turn/completed",
            )
        ]
        server = object.__new__(_AppServer)
        server._notifications = [  # type: ignore[attr-defined]
            {
                "method": "remoteControl/status/changed",
                "params": {"status": "disabled", "environmentId": None},
            },
            {
                "method": "item/completed",
                "params": {"item": {"type": "userMessage"}},
            },
            {
                "method": "item/completed",
                "params": {
                    "item": {"type": "agentMessage", "text": '{"ok":true}'}
                },
            },
            {
                "method": "turn/completed",
                "params": {
                    "threadId": "thread-1",
                    "turn": {"status": "completed", "error": None},
                },
            },
        ]
        result = server.collect_turn("thread-1", classifications)
        self.assertEqual(result["agent_message"], '{"ok":true}')

        for observed, classification in (
            ("unknown/value", None),
            ("mcp/tool/call", "prohibited-capability-event"),
        ):
            with self.subTest(observed=observed):
                server = object.__new__(_AppServer)
                server._notifications = [  # type: ignore[attr-defined]
                    {"method": observed, "params": {}}
                ]
                rows = list(classifications)
                if classification is not None:
                    rows.append(
                        {
                            "item_variant": f"ServerNotification:{observed}",
                            "classification": classification,
                        }
                    )
                with self.assertRaises(BoundaryRuntimeError) as raised:
                    diagnostic = io.StringIO()
                    with (
                        mock.patch.dict(
                            "os.environ",
                            {"BOUNDARY_PROOF_DIAGNOSTICS": "1"},
                        ),
                        mock.patch("sys.stderr", diagnostic),
                    ):
                        server.collect_turn("thread-1", rows)
                self.assertEqual(
                    raised.exception.diagnostic_id,
                    "unexpected-prohibited-event",
                )
                self.assertEqual(
                    diagnostic.getvalue(),
                    "prohibited-event:classification-rejected:"
                    + f"classification={classification}:"
                    + f"event_kind=ServerNotification:{observed}\n",
                )

    def test_turn_collection_distinguishes_retryable_timeout_from_bad_events(
        self,
    ) -> None:
        server = object.__new__(_AppServer)
        server._notifications = []  # type: ignore[attr-defined]
        with mock.patch.object(
            server,
            "_read_message",
            side_effect=BoundaryRuntimeError("experimental-api-unavailable"),
        ):
            with self.assertRaises(_StageTurnTimeout):
                server.collect_turn("thread-1", [], timeout=1)

    def test_thread_and_turn_requests_bind_one_exact_workspace_root(self) -> None:
        workspace = Path("/isolated-workspace")
        runtime_home = Path("/runtime-home")
        thread_request = _thread_start_request(workspace, "gpt-5.6-sol")
        turn_request = _turn_start_request(
            "thread-1",
            workspace,
            "gpt-5.6-sol",
            runtime_home,
            "Return a closed result.",
            "# Boundary-first proof model\n",
            {"type": "object"},
        )
        self.assertEqual(
            thread_request["runtimeWorkspaceRoots"], [str(workspace)]
        )
        self.assertEqual(
            turn_request["runtimeWorkspaceRoots"], [str(workspace)]
        )
        self.assertEqual(thread_request["cwd"], str(workspace))
        self.assertEqual(turn_request["cwd"], str(workspace))
        self.assertEqual(thread_request["dynamicTools"], [])
        self.assertEqual(thread_request["environments"], [])
        self.assertEqual(turn_request["environments"], [])
        self.assertEqual(thread_request["effort"], "low")
        self.assertEqual(turn_request["effort"], "low")
        self.assertEqual(
            {
                item["path"]
                for item in turn_request["input"]  # type: ignore[union-attr]
                if item["type"] == "skill"
            },
            {
                str(runtime_home / "skills" / skill / "SKILL.md")
                for skill in PARTICIPATING_SKILLS
            },
        )

    def test_boundary_reference_is_byte_identical_and_mapped(self) -> None:
        canonical = (
            ROOT / "templates" / "shared" / "boundary-proof-model.md"
        ).read_bytes()
        for skill in PARTICIPATING_SKILLS:
            with self.subTest(skill=skill):
                skill_root = ROOT / "skills" / skill
                reference = (
                    skill_root / "references" / "boundary-proof-model.md"
                )
                self.assertEqual(reference.read_bytes(), canonical)
                self.assertIn(
                    "references/boundary-proof-model.md",
                    (skill_root / "SKILL.md").read_text(encoding="utf-8"),
                )

    @staticmethod
    def _attestation() -> dict[str, object]:
        digest = "sha256:" + "a" * 64
        projection = dict(RUNTIME_PROJECTIONS[0])
        conformance = _run_file_change_handler_conformance(
            FILE_CHANGE_AUTHORIZATION_POLICY
        )
        return {
            "schema_version": "boundary-runtime-attestation-v3",
            "runtime_launcher_identity": projection[
                "runtime_launcher_identity"
            ],
            "runtime_package_identity": projection[
                "runtime_package_identity"
            ],
            "schema_bundle_identity": projection["schema_bundle_identity"],
            "generated_config_identity": digest,
            "managed_requirements_identity": digest,
            "active_permission_profile": "boundary-proof-stage-readonly-v1",
            "thread_metadata": {
                "cli_version": "0.145.0",
                "model_id": "gpt-5",
                "model_provider": "openai",
                "active_permission_profile": "boundary-proof-stage-readonly-v1",
                "workspace_root_roles": [],
                "instruction_source_refs": [],
                "runtime_default_instruction_source": "identified-runtime-substrate",
                "cwd_role": "isolated-workspace",
            },
            "feature_inventory_identity": digest,
            "capability_inventory_identity": digest,
            "skill_inventory_identity": digest,
            "feature_classification_identity": projection[
                "feature_classification_identity"
            ],
            "protocol_item_classification_identity": projection[
                "protocol_item_classification_identity"
            ],
            "runtime_projection_id": projection["projection_id"],
            "runtime_projection_identity": runtime_projection_identity(
                projection
            ),
            "file_change_capability_state": projection[
                "file_change_capability_state"
            ],
            "effective_tool_projection_identity": digest,
            "file_change_authorization_policy_identity": (
                "sha256:"
                + hashlib.sha256(
                    json.dumps(
                        FILE_CHANGE_AUTHORIZATION_POLICY,
                        ensure_ascii=False,
                        separators=(",", ":"),
                        sort_keys=True,
                    ).encode("utf-8")
                ).hexdigest()
            ),
            "file_change_handler_conformance_identity": conformance[
                "result_identity"
            ],
            "materialization_canary_policy_identity": (
                "sha256:"
                + hashlib.sha256(
                    json.dumps(
                        MATERIALIZATION_CANARY_POLICY,
                        ensure_ascii=False,
                        separators=(",", ":"),
                        sort_keys=True,
                    ).encode("utf-8")
                ).hexdigest()
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

    def test_environment_preflight_failure_uses_exact_closed_receipt(self) -> None:
        result = _preflight_failure("runtime-version-unsupported")
        self.assertEqual(tuple(result), PREFLIGHT_FIELDS)
        self.assertEqual(
            result,
            {
                "schema_version": "boundary-runtime-preflight-v3",
                "result": "environment-unavailable",
                "diagnostic_id": "runtime-version-unsupported",
                "phase": "pre-thread-start",
                "attestation_ref": None,
                "workspace_failure": None,
            },
        )
        with self.assertRaises(ValueError):
            _preflight_failure(
                "file-change-control-mismatch", "pre-thread-start"
            )

    def test_v2_policies_are_closed_and_identity_bound(self) -> None:
        self.assertEqual(
            FILE_CHANGE_AUTHORIZATION_POLICY["schema_version"],
            "stage-file-change-authorization-policy-v1",
        )
        self.assertEqual(
            MATERIALIZATION_CANARY_POLICY["policy_id"],
            "materialization-canary-v1",
        )
        self.assertEqual(
            ARTIFACT_POLICY["policy_id"], "lifecycle-stage-artifacts-v1"
        )
        self.assertEqual(len(ARTIFACT_POLICY["stage_occurrences"]), 8)

    def test_only_exact_registered_v1_history_is_recognized(self) -> None:
        expected_path = (
            "docs/changes/2026-07-25-boundary-first-proof-modeling-for-"
            "published-lifecycle-skills/evidence/"
            "behavior-implementation-manifest.json"
        )
        expected_identity = (
            "sha256:d4a98482700e711f6c1ec17f1309d56c"
            "64f67e9cc6181389cc74daf4f2c4cc0e"
        )
        self.assertEqual(
            _classify_historical_evidence(
                "behavior-implementation-manifest",
                expected_path,
                expected_identity,
            ),
            "registered-opaque-history",
        )
        for path, identity in (
            (expected_path + ".moved", expected_identity),
            (expected_path, "sha256:" + "0" * 64),
        ):
            with self.subTest(path=path, identity=identity):
                self.assertEqual(
                    _classify_historical_evidence(
                        "behavior-implementation-manifest", path, identity
                    ),
                    "unsupported-historical-evidence",
                )

    def test_runtime_attestation_rejects_unknown_nested_state(self) -> None:
        attestation = self._attestation()
        _validate_attestation(attestation)

        unknown_probe = copy.deepcopy(attestation)
        unknown_probe["probe_results"]["unknown_value"] = "pass"  # type: ignore[index]
        with self.assertRaises(BoundaryRuntimeError) as raised:
            _validate_attestation(unknown_probe)
        self.assertEqual(raised.exception.diagnostic_id, "sandbox-probe-failed")

        stale_thread = copy.deepcopy(attestation)
        stale_thread["thread_metadata"]["cli_version"] = "0.145.1"  # type: ignore[index]
        with self.assertRaises(BoundaryRuntimeError) as raised:
            _validate_attestation(stale_thread)
        self.assertEqual(
            raised.exception.diagnostic_id,
            "thread-metadata-mismatch",
        )
        with self.assertRaises(ValueError):
            _preflight_failure("unknown-diagnostic")

    def test_environment_preflight_validates_change_before_runtime_discovery(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            with mock.patch(
                "boundary_proof_behavior._collect_runtime_attestation"
            ) as collect:
                result = assess_environment("bad/id", repo_root=root)
        self.assertEqual(result["diagnostic_id"], "runtime-unavailable")
        collect.assert_not_called()

    def test_environment_preflight_publishes_exact_attestation_before_pass(
        self,
    ) -> None:
        change_id = "2026-07-25-boundary-proof"
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_root = root / "docs" / "changes" / change_id
            (change_root / "evidence").mkdir(parents=True)
            attestation = self._attestation()
            with mock.patch(
                "boundary_proof_behavior._collect_runtime_attestation",
                return_value=attestation,
            ):
                result = assess_environment(change_id, repo_root=root)
            attestation_path = (
                change_root / "evidence" / "runtime-preflight-attestation.json"
            )
            self.assertEqual(tuple(result), PREFLIGHT_FIELDS)
            self.assertEqual(result["result"], "pass")
            self.assertEqual(result["diagnostic_id"], "none")
            self.assertEqual(result["phase"], "pre-turn-start")
            self.assertEqual(
                result["attestation_ref"]["path"],
                f"docs/changes/{change_id}/evidence/"
                "runtime-preflight-attestation.json",
            )
            self.assertEqual(
                json.loads(attestation_path.read_text(encoding="utf-8")),
                attestation,
            )
            self.assertEqual(tuple(attestation), ATTESTATION_FIELDS)
            self.assertFalse(
                any(
                    path.name.startswith(".runtime-preflight-attestation.")
                    for path in attestation_path.parent.iterdir()
                )
            )

    def test_environment_preflight_never_promotes_failure_or_prior_evidence(
        self,
    ) -> None:
        change_id = "2026-07-25-boundary-proof"
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            evidence = root / "docs" / "changes" / change_id / "evidence"
            evidence.mkdir(parents=True)
            installed = evidence / "runtime-preflight-attestation.json"
            installed.write_bytes(b"prior evidence")
            with mock.patch(
                "boundary_proof_behavior._collect_runtime_attestation",
                side_effect=BoundaryRuntimeError(
                    "sandbox-probe-failed", "pre-turn-start"
                ),
            ):
                result = assess_environment(change_id, repo_root=root)
            self.assertEqual(result["result"], "environment-unavailable")
            self.assertIsNone(result["attestation_ref"])
            self.assertEqual(installed.read_bytes(), b"prior evidence")

    def test_semver_floor_and_prerelease_precedence_are_deterministic(self) -> None:
        self.assertLess(_parse_semver("0.138.0-rc.1"), _parse_semver("0.138.0"))
        self.assertEqual(
            _parse_semver("0.138.0+build.7"),
            _parse_semver("0.138.0+build.8"),
        )
        self.assertGreater(_parse_semver("0.144.0-rc.1"), _parse_semver("0.138.0"))
        for value in ("0.138", "v0.138.0", "0.138.0-", "0.138.0+"):
            with self.subTest(value=value):
                with self.assertRaises(BoundaryRuntimeError):
                    _parse_semver(value)

    def test_skill_inventory_requires_exact_enabled_and_disabled_rosters(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            home = Path(raw) / "home"
            workspace = Path(raw) / "workspace"
            home.mkdir()
            workspace.mkdir()
            skills = [
                {
                    "name": name,
                    "description": name,
                    "path": str(home / "skills" / name / "SKILL.md"),
                    "scope": "user",
                    "enabled": True,
                }
                for name in PARTICIPATING_SKILLS
            ]
            skills.extend(
                {
                    "name": name,
                    "description": name,
                    "path": str(
                        home / "skills" / ".system" / name / "SKILL.md"
                    ),
                    "scope": "system",
                    "enabled": False,
                }
                for name in RUNTIME_SYSTEM_SKILLS
            )
            result = {
                "data": [
                    {
                        "cwd": str(workspace),
                        "errors": [],
                        "skills": skills,
                    }
                ]
            }
            normalized = _normalize_skill_inventory(result, home, workspace)
            rows = normalized["data"][0]["skills"]
            self.assertEqual(len(rows), 11)
            self.assertEqual(
                {row["classification"] for row in rows},
                {
                    "manifested-lifecycle-skill",
                    "disabled-runtime-system-skill",
                },
            )

            mutations = []
            wrong_scope = copy.deepcopy(result)
            wrong_scope["data"][0]["skills"][0]["scope"] = "repo"
            mutations.append(wrong_scope)
            enabled_system = copy.deepcopy(result)
            enabled_system["data"][0]["skills"][-1]["enabled"] = True
            mutations.append(enabled_system)
            nonempty_error = copy.deepcopy(result)
            nonempty_error["data"][0]["errors"] = [
                {"path": "logical", "message": "failure"}
            ]
            mutations.append(nonempty_error)
            wrong_cwd = copy.deepcopy(result)
            wrong_cwd["data"][0]["cwd"] = str(home)
            mutations.append(wrong_cwd)
            omitted = copy.deepcopy(result)
            omitted["data"][0]["skills"].pop()
            mutations.append(omitted)
            duplicate_path = copy.deepcopy(result)
            duplicate_path["data"][0]["skills"][1]["path"] = duplicate_path[
                "data"
            ][0]["skills"][0]["path"]
            mutations.append(duplicate_path)
            for index, mutation in enumerate(mutations):
                with self.subTest(index=index):
                    with self.assertRaises(BoundaryRuntimeError) as raised:
                        _normalize_skill_inventory(mutation, home, workspace)
                    self.assertEqual(
                        raised.exception.diagnostic_id,
                        "skill-inventory-mismatch",
                    )

    def test_feature_inventory_rejects_unknown_and_enabled_prohibited_rows(
        self,
    ) -> None:
        class Server:
            def __init__(self, rows: list[dict[str, object]]) -> None:
                self.rows = rows

            def request(self, method: str, params: object) -> object:
                self.assertions = (method, params)
                return {"data": self.rows, "nextCursor": None}

        rows = [
            {
                "name": name,
                "enabled": name
                in {
                    "shell_tool",
                    "unified_exec",
                    "shell_snapshot",
                    "terminal_resize_reflow",
                    "tool_search_always_defer_mcp_tools",
                    "resize_all_images",
                    "tui_app_server",
                },
            }
            for name in CODEX_0_145_0_FEATURES
        ]
        pages, classifications = _feature_inventory(Server(rows))
        self.assertEqual(len(pages), 1)
        self.assertEqual(len(classifications), 96)

        missing = copy.deepcopy(rows)
        missing.pop()
        with self.assertRaises(BoundaryRuntimeError) as raised:
            _feature_inventory(Server(missing))
        self.assertEqual(
            raised.exception.diagnostic_id,
            "feature-classification-invalid",
        )

        additional = copy.deepcopy(rows)
        additional.append({"name": "unknown_value", "enabled": False})
        with self.assertRaises(BoundaryRuntimeError) as raised:
            _feature_inventory(Server(additional))
        self.assertEqual(
            raised.exception.diagnostic_id,
            "feature-classification-invalid",
        )

        unknown = copy.deepcopy(rows)
        unknown[-1]["name"] = "unknown_value"
        with self.assertRaises(BoundaryRuntimeError) as raised:
            _feature_inventory(Server(unknown))
        self.assertEqual(
            raised.exception.diagnostic_id,
            "feature-classification-invalid",
        )

        prohibited = copy.deepcopy(rows)
        next(row for row in prohibited if row["name"] == "apps")["enabled"] = True
        with self.assertRaises(BoundaryRuntimeError) as raised:
            _feature_inventory(Server(prohibited))
        self.assertEqual(
            raised.exception.diagnostic_id,
            "capability-inventory-mismatch",
        )

        with self.assertRaises(BoundaryRuntimeError) as raised:
            _feature_inventory(Server(rows), "0.145.1")
        self.assertEqual(
            raised.exception.diagnostic_id,
            "feature-classification-invalid",
        )

    def test_schema_bundle_ignores_object_order_but_preserves_array_order(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as left_raw, tempfile.TemporaryDirectory() as right_raw:
            left = Path(left_raw)
            right = Path(right_raw)
            (left / "schema.json").write_text(
                '{"properties":{"b":2,"a":1},"required":["a","b"]}',
                encoding="utf-8",
            )
            (right / "schema.json").write_text(
                '{"required":["a","b"],"properties":{"a":1,"b":2}}',
                encoding="utf-8",
            )
            self.assertEqual(
                _schema_bundle_projection(left)[1],
                _schema_bundle_projection(right)[1],
            )
            (right / "schema.json").write_text(
                '{"required":["b","a"],"properties":{"a":1,"b":2}}',
                encoding="utf-8",
            )
            self.assertNotEqual(
                _schema_bundle_projection(left)[1],
                _schema_bundle_projection(right)[1],
            )
            (right / "schema.json").write_text("{bad", encoding="utf-8")
            with self.assertRaises(BoundaryRuntimeError) as raised:
                _schema_bundle_projection(right)
            self.assertEqual(
                raised.exception.diagnostic_id,
                "schema-bundle-invalid",
            )
            for duplicate in (
                '{"a":1,"a":2}',
                '{"outer":{"a":1,"a":2}}',
            ):
                (right / "schema.json").write_text(duplicate, encoding="utf-8")
                with self.assertRaises(BoundaryRuntimeError) as raised:
                    _schema_bundle_projection(right)
                self.assertEqual(
                    raised.exception.diagnostic_id,
                    "schema-bundle-invalid",
                )

    def test_config_projection_normalizes_roots_and_consistent_origin_version(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            home = root / "home"
            package = root / "package"
            workspace = root / "workspace"
            for path in (home, package, workspace):
                path.mkdir()
            version = "sha256:" + "b" * 64
            result = {
                "config": {
                    "path": str(workspace),
                    "runtime": str(package),
                },
                "origins": {
                    f"projects.{workspace}.trust_level": {
                        "name": {
                            "type": "user",
                            "file": str(home / "config.toml"),
                            "profile": None,
                        },
                        "version": version,
                    },
                    "model": {
                        "name": {
                            "type": "user",
                            "file": str(home / "config.toml"),
                            "profile": None,
                        },
                        "version": version,
                    },
                },
            }
            raw_config = (
                'model = "gpt-5"\n'
                f'[projects.{json.dumps(str(workspace))}]\n'
                'trust_level = "trusted"\n'
            ).encode()
            normalized = _normalize_config_result(
                copy.deepcopy(result),
                raw_config,
                home,
                package,
                workspace,
            )
            rendered = json.dumps(normalized, sort_keys=True)
            self.assertNotIn(str(root), rendered)
            self.assertIn("runtime-generated-config-origin", rendered)

            mismatch = copy.deepcopy(result)
            mismatch["origins"]["model"]["version"] = "sha256:" + "c" * 64
            with self.assertRaises(BoundaryRuntimeError) as raised:
                _normalize_config_result(
                    mismatch,
                    raw_config,
                    home,
                    package,
                    workspace,
                )
            self.assertEqual(
                raised.exception.diagnostic_id,
                "config-equivalence-mismatch",
            )
            for invalid_origins in (
                {},
                {"model": copy.deepcopy(result["origins"]["model"])},
                {
                    **copy.deepcopy(result["origins"]),
                    "unknown.root": copy.deepcopy(result["origins"]["model"]),
                },
            ):
                invalid = copy.deepcopy(result)
                invalid["origins"] = invalid_origins
                with self.assertRaises(BoundaryRuntimeError) as raised:
                    _normalize_config_result(
                        invalid,
                        raw_config,
                        home,
                        package,
                        workspace,
                    )
                self.assertEqual(
                    raised.exception.diagnostic_id,
                    "config-equivalence-mismatch",
                )

    def test_config_origin_derivation_preserves_nested_array_and_quoted_segments(
        self,
    ) -> None:
        raw_config = b"""
title = "sample"
[nested]
leaf = true
"quoted.key" = "preserved"
[[items]]
name = "zero"
[[items]]
name = "one"
"""
        paths = _derive_config_origin_paths(raw_config)
        self.assertEqual(
            paths,
            {
                ("items", "0", "name"),
                ("items", "1", "name"),
                ("nested", "leaf"),
                ("nested", "quoted.key"),
                ("title",),
            },
        )
        self.assertIn(("nested", "quoted.key"), paths)
        self.assertNotIn(("nested", "quoted", "key"), paths)

    def test_freeze_baseline_is_immutable_and_exact(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            change_root = root / "docs" / "changes" / change_id
            change_root.mkdir(parents=True)
            with mock.patch(
                "boundary_proof_behavior._repository_head",
                return_value="a" * 40,
            ):
                first = freeze_baseline(change_id, repo_root=root)
                second = freeze_baseline(change_id, repo_root=root)
            self.assertEqual(first, second)
            self.assertEqual(
                first,
                {
                    "schema_version": "boundary-proof-baseline-v1",
                    "change_id": change_id,
                    "preservation_baseline_commit": "a" * 40,
                },
            )
            baseline = (
                change_root / "evidence" / "boundary-proof-baseline.json"
            )
            self.assertEqual(
                baseline.read_bytes(),
                json.dumps(
                    first,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode(),
            )
            with mock.patch(
                "boundary_proof_behavior._repository_head",
                return_value="b" * 40,
            ):
                with self.assertRaises(BoundaryRuntimeError):
                    freeze_baseline(change_id, repo_root=root)

    def test_preservation_materializes_and_validates_exact_forty_pairs(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            subprocess.run(
                ["git", "init", "-q"],
                cwd=root,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=root,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Boundary Test"],
                cwd=root,
                check=True,
            )
            for skill in EVALUATED_SKILLS:
                skill_root = root / "skills" / skill
                (skill_root / "references").mkdir(parents=True)
                (skill_root / "SKILL.md").write_text(
                    f"# {skill}\n\n## Handoff\n\nPreserve {skill}.\n",
                    encoding="utf-8",
                )
                (
                    skill_root / "references" / "boundary-proof-model.md"
                ).write_text(
                    "# Boundary model\n\nBoundary model version: v1\n",
                    encoding="utf-8",
                )
            subprocess.run(["git", "add", "skills"], cwd=root, check=True)
            subprocess.run(
                ["git", "commit", "-qm", "baseline"],
                cwd=root,
                check=True,
            )
            baseline = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            change_id = "2026-07-25-example"
            evidence = (
                root / "docs" / "changes" / change_id / "evidence"
            )
            evidence.mkdir(parents=True)
            (evidence / "boundary-proof-baseline.json").write_text(
                json.dumps(
                    {
                        "schema_version": "boundary-proof-baseline-v1",
                        "change_id": change_id,
                        "preservation_baseline_commit": baseline,
                    },
                    sort_keys=True,
                    separators=(",", ":"),
                ),
                encoding="utf-8",
            )
            for skill in EVALUATED_SKILLS:
                path = root / "skills" / skill / "SKILL.md"
                path.write_text(
                    path.read_text(encoding="utf-8")
                    + "\nBoundary model version: v1\n",
                    encoding="utf-8",
                )

            generated = generate_preservation(
                change_id,
                repo_root=root,
            )
            validated = validate_preservation(
                change_id,
                repo_root=root,
            )

            self.assertEqual(generated, validated)
            self.assertEqual(generated["result"], "structural-pass")
            self.assertEqual(generated["pair_count"], 40)
            self.assertEqual(generated["upstream_invocation_count"], 0)
            manifest = generated["manifest"]
            self.assertEqual(len(manifest["before_refs"]), 40)
            self.assertEqual(len(manifest["after_refs"]), 40)
            expected = {
                f"{skill}:{category}"
                for skill in EVALUATED_SKILLS
                for category in (
                    "behavior",
                    "claim-boundary",
                    "review-recording",
                    "isolation",
                    "handoff",
                )
            }
            self.assertEqual(
                expected,
                {
                    row["pair_key"]
                    for row in manifest["before_refs"]
                },
            )
            self.assertTrue(
                all(
                    "/evidence/preservation/" in row["snapshot_ref"]["path"]
                    for row in manifest["before_refs"]
                )
            )
            self.assertTrue(
                all(
                    json.loads(
                        (
                            root / row["artifact_ref"]["path"]
                        ).read_text(encoding="utf-8")
                    )["result"]
                    == "structural-pass"
                    for row in manifest["after_refs"]
                )
            )

            manifest_path = (
                evidence / "preservation" / "manifest.json"
            )
            canonical_manifest = copy.deepcopy(manifest)
            for mutate in (
                lambda value: value["before_refs"].pop(),
                lambda value: value["before_refs"].__setitem__(
                    1, copy.deepcopy(value["before_refs"][0])
                ),
                lambda value: value["before_refs"][0].__setitem__(
                    "origin_commit", "b" * 40
                ),
                lambda value: value["after_refs"][0].__setitem__(
                    "artifact_ref",
                    copy.deepcopy(
                        value["after_refs"][1]["artifact_ref"]
                    ),
                ),
            ):
                candidate = copy.deepcopy(canonical_manifest)
                mutate(candidate)
                manifest_path.write_text(
                    json.dumps(
                        candidate,
                        sort_keys=True,
                        separators=(",", ":"),
                    ),
                    encoding="utf-8",
                )
                with self.assertRaises(BoundaryRuntimeError):
                    validate_preservation(change_id, repo_root=root)
            manifest_path.write_text(
                json.dumps(
                    canonical_manifest,
                    sort_keys=True,
                    separators=(",", ":"),
                ),
                encoding="utf-8",
            )

            after_path = root / manifest["after_refs"][0]["artifact_ref"]["path"]
            after_path.write_text("stale\n", encoding="utf-8")
            with self.assertRaises(BoundaryRuntimeError) as raised:
                validate_preservation(change_id, repo_root=root)
            self.assertEqual(
                raised.exception.diagnostic_id,
                "runtime-identity-unstable",
            )

    def test_canonical_resource_manifest_covers_exact_eight_packages(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            change_id = "2026-07-25-example"
            (root / "docs" / "changes" / change_id).mkdir(
                parents=True
            )
            for skill in EVALUATED_SKILLS:
                skill_root = root / "skills" / skill
                (skill_root / "references").mkdir(parents=True)
                (skill_root / "SKILL.md").write_text(
                    f"# {skill}\n",
                    encoding="utf-8",
                )
                (
                    skill_root
                    / "references"
                    / "boundary-proof-model.md"
                ).write_text(
                    "Boundary model version: v1\n",
                    encoding="utf-8",
                )
            manifest = generate_canonical_skill_resource_manifest(
                change_id,
                repo_root=root,
            )
            self.assertEqual(
                manifest["skills"],
                list(EVALUATED_SKILLS),
            )
            self.assertEqual(len(manifest["files"]), 16)
            self.assertEqual(
                manifest,
                json.loads(
                    (
                        root
                        / "docs"
                        / "changes"
                        / change_id
                        / "evidence"
                        / "canonical-skill-resource-manifest.json"
                    ).read_text(encoding="utf-8")
                ),
            )


if __name__ == "__main__":
    unittest.main()
