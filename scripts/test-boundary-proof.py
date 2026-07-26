#!/usr/bin/env python3
"""Regression tests for the boundary-first proof model."""

from __future__ import annotations

import dataclasses
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from boundary_proof_behavior import ENVIRONMENT_CHECK_IDS, assess_environment

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
    RESULT_VALUES,
    BoundaryProofError,
    CoreBoundaryEntry,
    capability_report_result,
    evaluate_boundary_state,
    evaluate_simple_change_trace,
    normalize_feature_model,
    normalize_proof_map,
    validate_capability_report,
    validate_incident_registry,
    validate_incident_fixture,
    validate_version_parity,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "boundary-proof"


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
        first_bundle.update(
            outcome="changes-requested",
            material_finding_ids=["simple.finding.missing-boundary"],
        )
        first_bundle["artifact_refs"]["review-resolution"] = _snapshot_ref(
            trace,
            "simple.snapshot.spec-review.resolution.v1",
        )
        trace["review_bundles"]["simple.snapshot.spec-review.bundle.v2"] = {
            "review_id": "simple.review.spec.v2",
            "outcome": "approved",
            "reviewed_snapshot_id": "simple.snapshot.feature.v2",
            "material_finding_ids": [],
            "artifact_refs": {
                "review-record": _snapshot_ref(
                    trace,
                    "simple.snapshot.spec-review.record.v2",
                ),
                "review-log": _snapshot_ref(
                    trace,
                    "simple.snapshot.spec-review.log.v2",
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
        ]
        _sync_event_evidence(trace, test_spec)
        test_review = trace["events"][5]
        test_review["input_snapshot_ids"] = [
            "simple.snapshot.test-spec.v1",
            "simple.snapshot.feature.v2",
            "simple.snapshot.spec-review.bundle.v2",
            "simple.snapshot.spec-review.record.v2",
            "simple.snapshot.spec-review.log.v2",
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
        second_bundle.update(
            outcome="changes-requested",
            material_finding_ids=["simple.finding.missing-proof"],
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
    def test_environment_preflight_rejects_advertised_but_unattested_controls(
        self,
    ) -> None:
        advertising_help = """
        --ignore-user-config --ignore-rules --ephemeral --json
        --sandbox-state-json --sandbox-state-readable-root
        --sandbox-state-disable-network --disable --runtime-metadata-json
        """
        with tempfile.TemporaryDirectory() as raw:
            executable = Path(raw) / "codex"
            executable.write_bytes(b"identified runtime")
            executable.chmod(0o755)
            with (
                mock.patch(
                    "boundary_proof_behavior.shutil.which",
                    return_value=str(executable),
                ),
                mock.patch(
                    "boundary_proof_behavior._run_runtime",
                    side_effect=[
                        (0, "codex-cli 1.0.0\n", ""),
                        (0, advertising_help, ""),
                    ],
                ),
            ):
                result = assess_environment()

        self.assertEqual(result["schema_version"], "boundary-environment-preflight-v1")
        self.assertEqual(result["result"], "environment-unavailable")
        self.assertEqual(
            result["diagnostic_id"],
            "effective-profile-attestation-unavailable",
        )
        self.assertEqual(list(result["checks"]), list(ENVIRONMENT_CHECK_IDS))
        self.assertEqual(result["checks"]["runtime-identity"], "pass")
        self.assertTrue(
            all(
                result["checks"][check_id] == "fail"
                for check_id in ENVIRONMENT_CHECK_IDS[1:]
            )
        )
        self.assertNotIn(str(executable.parent), json.dumps(result))

    def test_environment_preflight_fails_closed_without_workspace_read_confinement(
        self,
    ) -> None:
        current_help = """
        --ignore-user-config --ignore-rules --ephemeral --json
        --sandbox workspace-write --disable
        """
        with tempfile.TemporaryDirectory() as raw:
            executable = Path(raw) / "codex"
            executable.write_bytes(b"identified runtime")
            executable.chmod(0o755)
            with (
                mock.patch(
                    "boundary_proof_behavior.shutil.which",
                    return_value=str(executable),
                ),
                mock.patch(
                    "boundary_proof_behavior._run_runtime",
                    side_effect=[
                        (0, "codex-cli 1.0.0\n", ""),
                        (0, current_help, ""),
                    ],
                ),
            ):
                result = assess_environment()

        self.assertEqual(result["result"], "environment-unavailable")
        self.assertEqual(
            result["diagnostic_id"],
            "effective-profile-attestation-unavailable",
        )
        self.assertEqual(result["checks"]["runtime-identity"], "pass")
        self.assertEqual(
            result["checks"]["workspace-only-filesystem"],
            "fail",
        )
        self.assertNotIn("identified runtime", json.dumps(result))

    def test_environment_preflight_rejects_missing_and_unsafe_runtime_metadata(
        self,
    ) -> None:
        cases = (
            (False, [], "runtime-executable-unavailable"),
            (True, [(0, "bad\nversion\n", ""), (0, "", "")], "runtime-version-unsafe"),
        )
        for executable_present, responses, diagnostic in cases:
            with self.subTest(diagnostic=diagnostic):
                with tempfile.TemporaryDirectory() as raw:
                    executable = Path(raw) / "codex"
                    executable.write_bytes(b"identified runtime")
                    executable.chmod(0o755)
                    with mock.patch(
                        "boundary_proof_behavior.shutil.which",
                        return_value=str(executable) if executable_present else None,
                    ):
                        if responses:
                            runner = mock.patch(
                                "boundary_proof_behavior._run_runtime",
                                side_effect=responses,
                            )
                        else:
                            runner = mock.patch("boundary_proof_behavior._run_runtime")
                        with runner:
                            result = assess_environment()
                self.assertEqual(result["result"], "environment-unavailable")
                self.assertEqual(result["diagnostic_id"], diagnostic)

    def test_environment_preflight_rejects_identity_read_and_replacement(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            executable = Path(raw) / "codex"
            executable.write_bytes(b"identified runtime")
            executable.chmod(0o755)
            with (
                mock.patch(
                    "boundary_proof_behavior.shutil.which",
                    return_value=str(executable),
                ),
                mock.patch(
                    "boundary_proof_behavior._read_executable_identity",
                    side_effect=OSError("unreadable"),
                ),
            ):
                unreadable = assess_environment()
            self.assertEqual(
                unreadable["diagnostic_id"],
                "runtime-identity-unavailable",
            )

            def replace_after_version(argv: object) -> tuple[int, str, str]:
                executable.write_bytes(b"replacement runtime")
                return 0, "codex-cli 1.0.0\n", ""

            executable.write_bytes(b"identified runtime")
            with (
                mock.patch(
                    "boundary_proof_behavior.shutil.which",
                    return_value=str(executable),
                ),
                mock.patch(
                    "boundary_proof_behavior._run_runtime",
                    side_effect=replace_after_version,
                ),
            ):
                replaced = assess_environment()
            self.assertEqual(replaced["result"], "environment-unavailable")
            self.assertEqual(
                replaced["diagnostic_id"],
                "runtime-identity-changed",
            )

            def remove_after_version(argv: object) -> tuple[int, str, str]:
                executable.unlink()
                return 0, "codex-cli 1.0.0\n", ""

            executable.write_bytes(b"identified runtime")
            executable.chmod(0o755)
            with (
                mock.patch(
                    "boundary_proof_behavior.shutil.which",
                    return_value=str(executable),
                ),
                mock.patch(
                    "boundary_proof_behavior._run_runtime",
                    side_effect=remove_after_version,
                ),
            ):
                removed = assess_environment()
            self.assertEqual(removed["result"], "environment-unavailable")
            self.assertEqual(
                removed["diagnostic_id"],
                "runtime-identity-unavailable",
            )


if __name__ == "__main__":
    unittest.main()
