#!/usr/bin/env python3
"""Regression tests for the boundary-first proof model."""

from __future__ import annotations

import dataclasses
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from boundary_proof_model import (
    APPLICABILITY_VALUES,
    AUTOMATION_LEVELS,
    CHECK_IDS,
    CORE_DIMENSION_IDS,
    EVALUATED_SKILLS,
    EXAMPLE_ROLES,
    FIXTURE_GATES,
    INTERACTION_RATIONALES,
    RESULT_VALUES,
    BoundaryProofError,
    CoreBoundaryEntry,
    capability_report_result,
    normalize_feature_model,
    normalize_proof_map,
    validate_capability_report,
    validate_incident_registry,
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
    evidence = ["docs/evidence.md"]
    fixtures = [
        {
            "fixture_id": fixture_id,
            "result": result,
            "expected_gate": expected_gate,
            "detected_stage": expected_gate if result != "not-run" else "not-detected",
            "escaped_to_code_review": False,
            "sibling_bypass_remaining": False,
            "evidence_refs": evidence if result != "not-run" else ["blocked: fixture not run"],
        }
        for fixture_id, expected_gate in FIXTURE_GATES.items()
    ]
    return {
        "schema_version": "boundary-capability-baseline-v1",
        "boundary_model_version": "v1",
        "evaluated_skills": list(EVALUATED_SKILLS),
        "required_check_ids": list(CHECK_IDS),
        "checks": {
            check_id: {"result": result, "evidence_refs": evidence}
            for check_id in CHECK_IDS
        },
        "fixtures": fixtures,
        "preservation_results": {
            key: {"result": result, "evidence_refs": evidence}
            for key in (
                "behavior",
                "claim-boundary",
                "review-recording",
                "isolation",
                "handoff",
            )
        },
        "adapter_parity": {"result": result, "evidence_refs": evidence},
        "false_blocking_count": 0,
        "duplicate_normative_owner_count": 0,
        "new_universal_artifact_count": 0,
        "simple_fixture_structure_correction_cycles": 1,
        "overall_result": "pass" if result == "pass" else "fail",
    }


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

    def test_incident_registry_is_exact_and_evidence_bound(self) -> None:
        payload = json.loads((FIXTURES / "incident-registry.json").read_text())
        validate_incident_registry(payload)
        payload["fixtures"][0]["fixture_id"] = "BFP-FX-UNKNOWN-001"
        with self.assertRaisesRegex(BoundaryProofError, "unknown fixture"):
            validate_incident_registry(payload)

    def test_capability_report_result_is_computed_not_asserted(self) -> None:
        passing = _report()
        self.assertEqual(capability_report_result(passing), "pass")
        validate_capability_report(passing)

        for mutation in (
            lambda report: report["checks"]["boundary-traceability"].update(result="not-run"),  # type: ignore[index]
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

    def test_simple_fixture_is_compact_and_requires_at_most_one_cycle(self) -> None:
        payload = json.loads((FIXTURES / "simple-change.json").read_text())
        feature = normalize_feature_model(payload["feature_model"])
        normalize_proof_map(payload["proof_map"], feature)
        self.assertEqual(len(feature.core_dimensions), 12)
        self.assertEqual(payload["new_universal_artifact_count"], 0)
        self.assertLessEqual(payload["structure_only_correction_cycles"], 1)

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


if __name__ == "__main__":
    unittest.main()
