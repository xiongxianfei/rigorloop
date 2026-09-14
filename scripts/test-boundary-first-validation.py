#!/usr/bin/env python3
"""Regression tests for model and portable feature/proof structural validation."""

from __future__ import annotations

import json
import io
import contextlib
import os
import re
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

from boundary_first_validation import (
    validate_changed_spec,
    validate_feature_record,
    validate_model_record,
    validate_proof_map,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "scripts" / "fixtures" / "boundary-first"


def relevant_tree_snapshot(root: Path) -> dict[str, bytes]:
    snapshot: dict[str, bytes] = {}
    for top_level in ("specs", "dist", "docs"):
        base = root / top_level
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                snapshot[relative] = b"symlink:" + str(path.readlink()).encode("utf-8")
            elif path.is_file():
                snapshot[relative] = path.read_bytes()
            elif path.is_dir():
                snapshot[relative] = b"directory"
    return snapshot








def valid_feature() -> str:
    dimensions = [
        "| input-domain | applicable | FIX-R001 | BND-INPUT-001 | - |",
        "| state-lifecycle | not-applicable | - | - | No state exists. |",
        "| identity-authority | not-applicable | - | - | No authority exists. |",
        "| composition-path | not-applicable | - | - | One path exists. |",
        "| temporal-retry | not-applicable | - | - | No retry exists. |",
        "| failure-recovery | not-applicable | - | - | No mutation exists. |",
        "| compatibility-migration | not-applicable | - | - | No history exists. |",
        "| external-environment | not-applicable | - | - | No dependency exists. |",
    ]
    return "\n".join(
        [
            "# Fixture",
            "",
            "## Status",
            "",
            "approved",
            "boundary_contract: boundary-first-v1",
            "",
            "## Boundary model",
            "",
            "Boundary model version: boundary-first-v1",
            "Boundary model scope: FIX-R001",
            "",
            "| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |",
            "| --- | --- | --- | --- | --- |",
            *dimensions,
            "",
            "## Boundary definitions",
            "",
            "| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |",
            "| --- | --- | --- | --- | --- | --- | --- |",
            "| BND-INPUT-001 | input-domain | FIX-R001 | present, missing, unknown | known values only | accept, reject | FIX-R001 |",
            "",
            "## Selected interactions",
            "",
            "No interaction selected: Only one boundary is applicable.",
            "",
            "## Example ownership",
            "",
            "| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |",
            "| --- | --- | --- | --- | --- | --- |",
            "| FIX-E001 | illustration | FIX-R001 | BND-INPUT-001 | - | - |",
            "",
        ]
    )


def valid_proof() -> str:
    return "\n".join(
        [
            "# Fixture proof",
            "",
            "Boundary model version: boundary-first-v1",
            "Boundary model scope: FIX-R001",
            "",
            "## Proof map",
            "",
            "| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            "| PRF-001 | covered | FIX-R001 | BND-INPUT-001 | T1 | unit | automated | CMD1 | fixture-evidence | M3 | - | - |",
            "",
        ]
    )


class BoundaryFirstStructuralTests(unittest.TestCase):
    def test_durable_minimal_semantic_omission_and_gap_fixtures(self) -> None:
        minimal = (FIXTURES / "feature-records" / "minimal.md").read_text(
            encoding="utf-8"
        )
        semantic_omission = (
            FIXTURES / "feature-records" / "semantic-omission.md"
        ).read_text(encoding="utf-8")
        complex_feature = (
            FIXTURES / "feature-records" / "complex.md"
        ).read_text(encoding="utf-8")
        complete = (FIXTURES / "proof-maps" / "complete.md").read_text(
            encoding="utf-8"
        )
        complex_complete = (
            FIXTURES / "proof-maps" / "complex-complete.md"
        ).read_text(encoding="utf-8")
        gap = (FIXTURES / "proof-maps" / "gap.md").read_text(encoding="utf-8")
        self.assertEqual(validate_feature_record(minimal), ())
        self.assertEqual(validate_feature_record(semantic_omission), ())
        self.assertEqual(validate_feature_record(complex_feature), ())
        self.assertEqual(validate_proof_map(complete, minimal), ())
        self.assertEqual(
            validate_proof_map(complex_complete, complex_feature),
            (),
        )
        self.assertIn(
            "BFR-MISSING-DIRECT-PROOF",
            {issue.code for issue in validate_proof_map(gap, minimal)},
        )

    def test_valid_concise_feature_and_complete_proof_pass(self) -> None:
        feature = valid_feature()
        self.assertEqual(validate_feature_record(feature), ())
        self.assertEqual(validate_proof_map(valid_proof(), feature), ())

    def test_unknown_dimension_fails_before_consistency(self) -> None:
        text = valid_feature().replace("input-domain | applicable", "future-domain | applicable")
        issues = validate_feature_record(text)
        self.assertGreaterEqual(len(issues), 1)
        self.assertEqual(issues[0].code, "BFR-UNKNOWN-DIMENSION")

    def test_unknown_applicability_fails_before_consistency(self) -> None:
        text = valid_feature().replace("input-domain | applicable", "input-domain | undecidable")
        issues = validate_feature_record(text)
        self.assertEqual(issues[0].code, "BFR-UNKNOWN-APPLICABILITY")

    def test_unknown_contract_version_fails_before_consistency(self) -> None:
        issues = validate_feature_record(
            valid_feature().replace(
                "boundary_contract: boundary-first-v1",
                "boundary_contract: boundary-first-v2",
            )
        )
        self.assertEqual(issues[0].code, "BFR-UNKNOWN-CONTRACT-VERSION")

    def test_retired_marker_adapter_rejects_without_reading_archive(self):
        from unittest.mock import patch
        document = valid_feature().replace(
            "## Status\n\napproved\nboundary_contract: boundary-first-v1",
            "## Owning change record\n\n`docs/changes/example/change.yaml`\n\nboundary_contract: boundary-first-v1",
        )
        with patch.object(Path, "read_text", side_effect=AssertionError("must not read archived store")):
            issues = validate_feature_record(document, "specs/example.md", root=Path("."))
        self.assertEqual(issues[0].code, "BFR-MARKER-AUTHORITY")
        self.assertIn("unsupported", issues[0].message)

    def test_v2_marker_placement_is_document_structure_not_record_authority(self):
        from unittest.mock import patch
        document = valid_feature().replace(
            "## Status\n\napproved\nboundary_contract: boundary-first-v1",
            "## Owning change record\n\n`docs/changes/example/change.json`\n\nboundary_contract: boundary-first-v1",
        )
        with patch.object(Path, "read_text", side_effect=AssertionError("document validation must not inspect a store")):
            self.assertEqual(validate_feature_record(document, "specs/example.md", root=Path(".")), ())
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "specs").mkdir()
            (root / "specs/example.md").write_text(document)
            # Delivery Review owns v2 plan allocation; this feature-authoring
            # check must not require an obsolete standalone test-spec file.
            self.assertEqual(validate_changed_spec(root, "specs/example.md"), ())
            (root / "specs/example.test.md").write_text("malformed explicit proof map")
            self.assertTrue(validate_changed_spec(root, "specs/example.test.md"))
        malformed = document.replace("docs/changes/example/change.json", "docs/changes/../change.json")
        self.assertTrue(validate_feature_record(malformed, "specs/example.md", root=Path(".")))

    def test_marker_must_follow_lifecycle_value_inside_status(self) -> None:
        misplaced = valid_feature().replace(
            "approved\nboundary_contract: boundary-first-v1",
            "approved",
        ).replace(
            "## Boundary model",
            "## Boundary model\n\nboundary_contract: boundary-first-v1",
        )
        self.assertEqual(
            validate_feature_record(misplaced)[0].code,
            "BFR-MARKER-PLACEMENT",
        )
        duplicated = valid_feature().replace(
            "boundary_contract: boundary-first-v1",
            "boundary_contract: boundary-first-v1\nboundary_contract: boundary-first-v1",
            1,
        )
        self.assertEqual(
            validate_feature_record(duplicated)[0].code,
            "BFR-MARKER-COUNT",
        )






    def test_composed_example_requirements_may_span_the_union_of_cited_boundaries(self) -> None:
        text = valid_feature().replace(
            "| state-lifecycle | not-applicable | - | - | No state exists. |",
            "| state-lifecycle | applicable | FIX-R002 | BND-STATE-001 | - |",
        ).replace(
            "Boundary model scope: FIX-R001",
            "Boundary model scope: FIX-R001, FIX-R002",
        ).replace(
            "| BND-INPUT-001 | input-domain | FIX-R001 | present, missing, unknown | known values only | accept, reject | FIX-R001 |",
            "| BND-INPUT-001 | input-domain | FIX-R001 | present, missing, unknown | known values only | accept, reject | FIX-R001 |\n"
            "| BND-STATE-001 | state-lifecycle | FIX-R002 | initial, complete | completion is monotonic | continue, stop | FIX-R002 |",
        ).replace(
            "No interaction selected: Only one boundary is applicable.",
            "| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| INT-001 | FIX-R001, FIX-R002 | BND-INPUT-001, BND-STATE-001 | Input and state disagree. | Stop safely. |",
        ).replace(
            "| FIX-E001 | illustration | FIX-R001 | BND-INPUT-001 | - | - |",
            "| FIX-E001 | illustration | FIX-R001, FIX-R002 | BND-INPUT-001, BND-STATE-001 | - | - |",
        )
        self.assertEqual(validate_feature_record(text), ())

        uncovered = text.replace(
            "FIX-R001, FIX-R002 | BND-INPUT-001, BND-STATE-001 | - | - |",
            "FIX-R003 | BND-INPUT-001, BND-STATE-001 | - | - |",
        )
        self.assertIn(
            "BFR-EXAMPLE-OWNER-MISMATCH",
            {issue.code for issue in validate_feature_record(uncovered)},
        )

    def test_fenced_record_and_malformed_separator_fail_closed(self) -> None:
        fenced = "```md\n" + valid_feature() + "\n```\n"
        self.assertIn(
            validate_feature_record(fenced)[0].code,
            {"BFR-MARKER-COUNT", "BFR-MISSING-HEADING"},
        )
        malformed = valid_feature().replace(
            "| --- | --- | --- | --- | --- |",
            "| -- | --- | --- | --- | --- |",
            1,
        )
        self.assertEqual(
            validate_feature_record(malformed)[0].code,
            "BFR-INVALID-TABLE-SEPARATOR",
        )

    def test_valid_markdown_alignment_separators_pass(self) -> None:
        aligned_feature = valid_feature().replace(
            "| --- | --- | --- | --- | --- |",
            "| :--- | ---: | :---: | --- | --- |",
            1,
        )
        aligned_proof = valid_proof().replace(
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            "| :--- | ---: | :---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            1,
        )
        self.assertEqual(validate_feature_record(aligned_feature), ())
        self.assertEqual(
            validate_proof_map(aligned_proof, aligned_feature),
            (),
        )

    def test_unknown_model_version_fails_before_consistency(self) -> None:
        issues = validate_feature_record(
            valid_feature().replace(
                "Boundary model version: boundary-first-v1",
                "Boundary model version: boundary-first-v2",
            )
        )
        self.assertEqual(issues[0].code, "BFR-UNKNOWN-MODEL-VERSION")

    def test_unknown_heading_fails_closed(self) -> None:
        issues = validate_feature_record(
            valid_feature().replace(
                "## Boundary definitions",
                "## Future boundary definitions",
            )
        )
        self.assertEqual(issues[0].code, "BFR-MISSING-HEADING")

    def test_unknown_column_fails_before_consistency(self) -> None:
        issues = validate_feature_record(
            valid_feature().replace(
                "| Dimension ID | Applicability |",
                "| Future dimension | Applicability |",
                1,
            )
        )
        self.assertEqual(issues[0].code, "BFR-UNKNOWN-COLUMNS")

    def test_boundary_prefix_must_match_dimension(self) -> None:
        text = valid_feature().replace(
            "| BND-INPUT-001 | input-domain |",
            "| BND-STATE-001 | input-domain |",
        )
        issues = validate_feature_record(text)
        self.assertEqual(issues[0].code, "BFR-BOUNDARY-PREFIX-MISMATCH")

    def test_blank_and_unicode_sentinels_fail_closed(self) -> None:
        for sentinel in ("", "—"):
            with self.subTest(sentinel=sentinel or "blank"):
                text = valid_feature().replace(
                    "| state-lifecycle | not-applicable | - | - | No state exists. |",
                    f"| state-lifecycle | not-applicable | {sentinel} | - | No state exists. |",
                )
                self.assertEqual(
                    validate_feature_record(text)[0].code,
                    "BFR-INVALID-SENTINEL",
                )

    def test_extensions_and_imports_are_forbidden(self) -> None:
        for declaration in ("Extensions: future-domain", "Imports: other.md"):
            with self.subTest(declaration=declaration):
                text = valid_feature().replace(
                    "## Boundary definitions",
                    f"{declaration}\n\n## Boundary definitions",
                )
                self.assertEqual(
                    validate_feature_record(text)[0].code,
                    "BFR-FORBIDDEN-EXTENSION-IMPORT",
                )

    def test_boundary_record_headings_are_contiguous(self) -> None:
        text = valid_feature().replace(
            "## Boundary definitions",
            "## Interleaved notes\n\nNotes.\n\n## Boundary definitions",
        )
        self.assertEqual(
            validate_feature_record(text)[0].code,
            "BFR-NONCONTIGUOUS-RECORD",
        )

    def test_unknown_example_classification_fails_before_consistency(self) -> None:
        text = valid_feature().replace(
            "| FIX-E001 | illustration |",
            "| FIX-E001 | anecdote |",
        )
        self.assertEqual(
            validate_feature_record(text)[0].code,
            "BFR-UNKNOWN-EXAMPLE-CLASS",
        )

    def test_applicable_dimension_requires_requirement_and_boundary(self) -> None:
        text = valid_feature().replace(
            "| input-domain | applicable | FIX-R001 | BND-INPUT-001 | - |",
            "| input-domain | applicable | - | - | - |",
        )
        self.assertIn(
            "BFR-APPLICABLE-MISSING-OWNER",
            {issue.code for issue in validate_feature_record(text)},
        )

    def test_interaction_requires_two_defined_boundaries(self) -> None:
        text = valid_feature().replace(
            "No interaction selected: Only one boundary is applicable.",
            "\n".join(
                [
                    "| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |",
                    "| --- | --- | --- | --- | --- |",
                    "| INT-001 | FIX-R001 | BND-INPUT-001 | bypass | reject |",
                ]
            ),
        )
        self.assertIn(
            "BFR-INTERACTION-BOUNDARY-COUNT",
            {issue.code for issue in validate_feature_record(text)},
        )

    def test_duplicate_boundary_example_interaction_and_proof_ids_fail(self) -> None:
        duplicate_boundary = valid_feature().replace(
            "| BND-INPUT-001 | input-domain | FIX-R001 | present, missing, unknown | known values only | accept, reject | FIX-R001 |",
            "\n".join(
                [
                    "| BND-INPUT-001 | input-domain | FIX-R001 | present | known values only | accept | FIX-R001 |",
                    "| BND-INPUT-001 | input-domain | FIX-R001 | missing | known values only | reject | FIX-R001 |",
                ]
            ),
        )
        self.assertIn(
            "BFR-DUPLICATE-BOUNDARY",
            {issue.code for issue in validate_feature_record(duplicate_boundary)},
        )
        duplicate_example = valid_feature().replace(
            "| FIX-E001 | illustration | FIX-R001 | BND-INPUT-001 | - | - |",
            "\n".join(
                [
                    "| FIX-E001 | illustration | FIX-R001 | BND-INPUT-001 | - | - |",
                    "| FIX-E001 | illustration | FIX-R001 | BND-INPUT-001 | - | - |",
                ]
            ),
        )
        self.assertIn(
            "BFR-DUPLICATE-EXAMPLE",
            {issue.code for issue in validate_feature_record(duplicate_example)},
        )
        duplicate_interaction = valid_feature().replace(
            "No interaction selected: Only one boundary is applicable.",
            "\n".join(
                [
                    "| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |",
                    "| --- | --- | --- | --- | --- |",
                    "| INT-001 | FIX-R001 | BND-INPUT-001 | bypass | reject |",
                    "| INT-001 | FIX-R001 | BND-INPUT-001 | retry | reject |",
                ]
            ),
        )
        self.assertIn(
            "BFR-DUPLICATE-INTERACTION",
            {issue.code for issue in validate_feature_record(duplicate_interaction)},
        )
        duplicate_proof = valid_proof().replace(
            "| PRF-001 | covered | FIX-R001 | BND-INPUT-001 | T1 | unit | automated | CMD1 | fixture-evidence | M3 | - | - |",
            "\n".join(
                [
                    "| PRF-001 | covered | FIX-R001 | BND-INPUT-001 | T1 | unit | automated | CMD1 | fixture-evidence | M3 | - | - |",
                    "| PRF-001 | covered | FIX-R001 | BND-INPUT-001 | T2 | unit | automated | CMD1 | fixture-evidence | M3 | - | - |",
                ]
            ),
        )
        self.assertIn(
            "BFR-DUPLICATE-PROOF",
            {issue.code for issue in validate_proof_map(duplicate_proof, valid_feature())},
        )

    def test_semantic_omission_is_not_a_structural_error(self) -> None:
        text = valid_feature().replace(
            "No interaction selected: Only one boundary is applicable.",
            "No interaction selected: Reviewer must judge whether a hidden hazard exists.",
        )
        self.assertEqual(validate_feature_record(text), ())

    def test_unknown_proof_vocabulary_fails_first(self) -> None:
        text = valid_proof().replace("| PRF-001 | covered |", "| PRF-001 | future |")
        issues = validate_proof_map(text, valid_feature())
        self.assertEqual(issues[0].code, "BFR-UNKNOWN-COVERAGE")

    def test_unknown_proof_level_and_automation_fail_closed(self) -> None:
        mutations = (
            ("| unit | automated |", "| future | automated |", "BFR-UNKNOWN-PROOF-LEVEL"),
            ("| unit | automated |", "| unit | delegated |", "BFR-UNKNOWN-AUTOMATION-MODE"),
        )
        for old, new, expected in mutations:
            with self.subTest(expected=expected):
                issues = validate_proof_map(
                    valid_proof().replace(old, new),
                    valid_feature(),
                )
                self.assertEqual(issues[0].code, expected)

    def test_malformed_feature_does_not_crash_proof_validation(self) -> None:
        malformed_feature = valid_feature().replace(
            "| BND-INPUT-001 | input-domain | FIX-R001 | present, missing, unknown | known values only | accept, reject | FIX-R001 |",
            "| BND-INPUT-001 | input-domain |",
        )
        issues = validate_proof_map(valid_proof(), malformed_feature)
        self.assertTrue(issues)
        self.assertEqual(issues[0].code, "BFR-ROW-SHAPE")

    def test_proof_reference_serialization_and_gap_id_are_vocabulary_checked(
        self,
    ) -> None:
        feature = (FIXTURES / "feature-records" / "complex.md").read_text(
            encoding="utf-8"
        )
        proof = (FIXTURES / "proof-maps" / "complex-complete.md").read_text(
            encoding="utf-8"
        )
        malformed_refs = proof.replace(
            "BND-INPUT-001, BND-STATE-001",
            "BND-INPUT-001,BND-STATE-001",
        )
        # Use a valid multi-reference proof row so the mutation reaches the
        # proof-reference vocabulary rather than feature consistency.
        malformed_refs = malformed_refs.replace(
            "INT-001 | T3",
            "BND-INPUT-001,BND-STATE-001 | T3",
        )
        self.assertEqual(
            validate_proof_map(malformed_refs, feature)[0].code,
            "BFR-INVALID-PROOF-REFERENCE",
        )
        gap = (FIXTURES / "proof-maps" / "gap.md").read_text(encoding="utf-8")
        invalid_gap = gap.replace("FIX-GAP-001", "not a stable id")
        self.assertEqual(
            validate_proof_map(
                invalid_gap,
                (FIXTURES / "feature-records" / "minimal.md").read_text(
                    encoding="utf-8"
                ),
            )[0].code,
            "BFR-INVALID-GAP-ID",
        )

    def test_gap_row_cannot_carry_proof_metadata(self) -> None:
        text = valid_proof().replace(
            "| PRF-001 | covered | FIX-R001 | BND-INPUT-001 | T1 | unit | automated | CMD1 | fixture-evidence | M3 | - | - |",
            "| PRF-001 | gap | FIX-R001 | BND-INPUT-001 | T1 | unit | automated | CMD1 | fixture-evidence | M3 | - | FIX-GAP-001 |",
        )
        self.assertIn(
            "BFR-GAP-HAS-PROOF",
            {issue.code for issue in validate_proof_map(text, valid_feature())},
        )

    def test_cross_feature_boundary_reference_fails(self) -> None:
        text = valid_proof().replace("BND-INPUT-001 | T1", "BND-STATE-999 | T1")
        self.assertIn(
            "BFR-UNKNOWN-BOUNDARY-REFERENCE",
            {issue.code for issue in validate_proof_map(text, valid_feature())},
        )

    def test_automated_proof_rejects_manual_procedure(self) -> None:
        text = valid_proof().replace("| M3 | - | - |", "| M3 | FIX-MANUAL-001 | - |")
        self.assertIn(
            "BFR-AUTOMATED-MANUAL-PROCEDURE",
            {issue.code for issue in validate_proof_map(text, valid_feature())},
        )


class BoundaryFirstActivationTests(unittest.TestCase):
























    def test_issue_evidence_is_privacy_bounded(self) -> None:
        issue = validate_feature_record(
            valid_feature().replace("input-domain | applicable", "secret | applicable"),
            path="specs/fixture.md",
        )[0]
        self.assertEqual(
            set(issue.as_dict()),
            {"check_id", "path", "message", "offending_value", "expected"},
        )

    def test_unmarked_feature_routes_to_semantic_review(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "specs").mkdir()
            spec_path = root / "specs" / "historical.md"
            spec_path.write_text("# Historical\n", encoding="utf-8")
            issues = validate_changed_spec(root, "specs/historical.md")
            self.assertEqual(issues[0].code, "BFR-ADOPTION-REVIEW")


    def test_changed_adopting_test_spec_validates_against_feature(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "specs").mkdir()
            feature = (FIXTURES / "feature-records" / "minimal.md").read_text(
                encoding="utf-8"
            )
            proof = (FIXTURES / "proof-maps" / "complete.md").read_text(
                encoding="utf-8"
            )
            (root / "specs" / "feature.md").write_text(feature, encoding="utf-8")
            (root / "specs" / "feature.test.md").write_text(
                proof, encoding="utf-8"
            )
            self.assertEqual(
                validate_changed_spec(root, "specs/feature.test.md"),
                (),
            )


    def test_changed_spec_paths_are_repository_contained(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "specs").mkdir()
            outside = root.parent / "outside-boundary-first.md"
            outside.write_text("# outside\n", encoding="utf-8")
            self.addCleanup(outside.unlink, missing_ok=True)
            for path in (
                "/etc/passwd",
                "../outside-boundary-first.md",
                "README.md",
            ):
                with self.subTest(path=path):
                    self.assertEqual(
                        validate_changed_spec(root, path)[0].code,
                        "BFR-INVALID-CHANGED-PATH",
                    )
            (root / "specs" / "escape.md").symlink_to(outside)
            self.assertEqual(
                validate_changed_spec(root, "specs/escape.md")[0].code,
                "BFR-CHANGED-PATH-ESCAPE",
            )

    def test_derived_feature_and_proof_paths_are_contained(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "specs").mkdir()
            outside = root.parent / "outside-boundary-companion.md"
            outside.write_text(valid_feature(), encoding="utf-8")
            self.addCleanup(outside.unlink, missing_ok=True)
            (root / "specs" / "feature.md").symlink_to(outside)
            (root / "specs" / "feature.test.md").write_text(
                valid_proof(), encoding="utf-8"
            )
            self.assertEqual(
                validate_changed_spec(root, "specs/feature.test.md")[0].code,
                "BFR-CHANGED-PATH-ESCAPE",
            )
            (root / "specs" / "feature.md").unlink()
            (root / "specs" / "feature.md").write_text(
                valid_feature(), encoding="utf-8"
            )
            (root / "specs" / "feature.test.md").unlink()
            (root / "specs" / "feature.test.md").symlink_to(outside)
            self.assertEqual(
                validate_changed_spec(root, "specs/feature.md")[0].code,
                "BFR-CHANGED-PATH-ESCAPE",
            )

    def test_deleted_adopting_proof_and_orphaned_test_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "specs").mkdir()
            feature_path = root / "specs" / "feature.md"
            proof_path = root / "specs" / "feature.test.md"
            feature_path.write_text(valid_feature(), encoding="utf-8")
            self.assertEqual(
                validate_changed_spec(root, "specs/feature.test.md")[0].code,
                "BFR-PROOF-MAP-MISSING",
            )
            feature_path.unlink()
            proof_path.write_text(valid_proof(), encoding="utf-8")
            self.assertEqual(
                validate_changed_spec(root, "specs/feature.test.md")[0].code,
                "BFR-FEATURE-CONTRACT-MISSING",
            )
            proof_path.unlink()
            self.assertEqual(
                validate_changed_spec(root, "specs/feature.test.md"),
                (),
            )


    def test_specs_root_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            outside_specs = root.parent / f"{root.name}-outside-specs"
            outside_specs.mkdir()
            (outside_specs / "feature.md").write_text(valid_feature())
            self.addCleanup(shutil.rmtree, outside_specs, ignore_errors=True)
            (root / "specs").symlink_to(outside_specs, target_is_directory=True)
            self.assertEqual(
                validate_changed_spec(root, "specs/feature.md")[0].code,
                "BFR-SPECS-ROOT-UNSAFE",
            )

    def test_serialized_issue_redacts_private_payload(self) -> None:
        secret = "credential=super-secret-private-value"
        issue = validate_feature_record(
            valid_feature().replace("input-domain | applicable", f"{secret} | applicable"),
            path="specs/fixture.md",
        )[0]
        serialized = json.dumps(issue.as_dict(), sort_keys=True)
        self.assertNotIn(secret, serialized)
        self.assertIn("redacted:sha256:", serialized)


class AdoptionReviewHandoffTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "specs").mkdir()
        for name in ("historical", "other"):
            (self.root / f"specs/{name}.md").write_text("# Historical\n")
        self.main = runpy.run_path(str(ROOT / "scripts/validate-boundary-first.py"))["main"]

    def run_check(self, *paths: str) -> tuple[int, dict]:
        args = ["validate-boundary-first", "--check", "--root", str(self.root)]
        for path in paths:
            args.extend(["--path", path])
        output = io.StringIO()
        with mock.patch.object(sys, "argv", args), contextlib.redirect_stdout(output):
            result = self.main()
        return result, json.loads(output.getvalue())

    def test_review_required_is_structural_success_not_approval(self) -> None:
        before = relevant_tree_snapshot(self.root)
        code, output = self.run_check("specs/historical.md", "specs/other.md")
        self.assertEqual(code, 0)
        self.assertEqual(output["status"], "review-required")
        self.assertEqual(output["validation"], "structure-and-references-only")
        self.assertEqual({item["path"] for item in output["review_required"]},
                         {"specs/historical.md", "specs/other.md"})
        self.assertTrue(all(item["owner"] == "design-review" for item in output["review_required"]))
        self.assertEqual(relevant_tree_snapshot(self.root), before)

    def test_review_required_does_not_hide_mixed_structural_failure(self) -> None:
        code, output = self.run_check("specs/historical.md", "docs/design/missing.md")
        self.assertEqual(code, 1)
        self.assertEqual(output["status"], "failed")
        self.assertEqual(output["review_required"][0]["path"], "specs/historical.md")
        self.assertTrue(output["issues"])

    def test_unknown_value_marker_fails_for_explicit_features(self) -> None:
        for path in ("specs/new.md", "specs/historical.md"):
            with self.subTest(path=path):
                (self.root / path).write_text(valid_feature().replace("boundary_contract: boundary-first-v1", "boundary_contract: unknown_value"))
                code, output = self.run_check(path)
                self.assertEqual(code, 1)
                self.assertEqual(output["status"], "failed")
                self.assertTrue(output["issues"])
                self.assertFalse(output.get("review_required"))

    def test_malformed_boundary_content_is_not_review_only(self) -> None:
        for text in (valid_feature().replace("## Boundary definitions", "## Missing"),
                     "# Historical\n\n## Boundary model\n", "# Historical\nboundary_contract:\n"):
            with self.subTest(text=text):
                (self.root / "specs/historical.md").write_text(text)
                code, output = self.run_check("specs/historical.md")
                self.assertEqual(code, 1)
                self.assertFalse(output.get("review_required"))

    def test_unmarked_new_spec_requires_adoption_review(self) -> None:
        (self.root / "specs/new.md").write_text("# New\n")
        code, output = self.run_check("specs/new.md")
        self.assertEqual(code, 0)
        self.assertEqual(output["review_required"][0]["check_id"], "BFR-ADOPTION-REVIEW")


    def test_explicit_unmarked_proof_requires_review_and_partial_record_fails(self):
        path = "specs/historical.test.md"
        (self.root / path).write_text("# Customer proof\n")
        code, output = self.run_check(path)
        self.assertEqual(code, 0)
        self.assertEqual(output["status"], "review-required")
        self.assertEqual(output["review_required"][0]["path"], "specs/historical.md")
        for text in ("boundary_contract: unknown_value\n", "Boundary model version: unknown_value\n", "## Proof map\n", valid_proof()):
            with self.subTest(text=text[:40]):
                (self.root / path).write_text(text)
                code, output = self.run_check(path)
                self.assertEqual(code, 1, output)
                self.assertTrue(output["issues"])
                self.assertEqual(output["review_required"][0]["path"], "specs/historical.md")

    def test_unknown_value_diagnostic_is_not_demoted_to_review(self) -> None:
        issue = validate_changed_spec(self.root, "docs/design/missing.md")[0]
        unknown = type(issue)("unknown_value", issue.path, issue.message, issue.offending_value, issue.expected)
        with mock.patch.dict(self.main.__globals__, {"validate_changed_spec": lambda root, path: (unknown,)}):
            code, output = self.run_check("specs/historical.md")
        self.assertEqual(code, 1)
        self.assertEqual(output["issues"][0]["check_id"], "unknown_value")
        self.assertFalse(output["review_required"])


class ModelRecordTests(unittest.TestCase):
    """TG-06: model recognition is structural, explicit and independent of lifecycle."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="rigorloop-model-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / "docs/design/skill/workflow.md"
        self.path.parent.mkdir(parents=True)
        self.text = (ROOT / "docs/design/skill/workflow.md").read_text(encoding="utf-8")

    def check(self, text=None, relative="docs/design/skill/workflow.md"):
        self.path.write_text(self.text if text is None else text, encoding="utf-8")
        return validate_changed_spec(self.root, relative)

    def test_model_current_files_validate_without_activation_or_change_record(self):
        for relative in ['docs/design/system.md', 'docs/design/skill/design.md', 'docs/design/skill/workflow.md', 'docs/design/skill/assessment.md', 'docs/design/cli/records.md', 'docs/design/cli/installation.md', 'docs/design/engineering/validation.md', 'docs/design/engineering/packaging.md', 'docs/design/engineering/release.md', 'docs/design/skill/skill.md', 'docs/design/cli/cli.md', 'docs/design/engineering/engineering.md']:
            with self.subTest(relative=relative):
                (self.root / relative).parent.mkdir(parents=True, exist_ok=True)
                (self.root / relative).write_bytes((ROOT / relative).read_bytes())
                self.assertEqual(validate_changed_spec(self.root, relative), ())
        self.assertFalse((self.root / "docs/changes").exists())

    def test_model_retired_marker_rejects_before_table_checks(self):
        retired = self.text.replace("Model validation contract: model-document-v1",
                                    "Model validation contract: explicit-recording-v1", 1)
        for text in (retired, retired.replace("## Requirements", "## Broken requirements", 1)):
            issues = self.check(text)
            self.assertEqual([i.code for i in issues], ["BFR-MODEL-CONTRACT"])
            self.assertIn("model-document-v1", issues[0].message)

    def test_model_design_example_and_parent_validate_without_counting_fenced_marker(self):
        parent = (ROOT / "docs/design/skill/design.md").read_text()
        examples = re.findall(r"^(`{3,})markdown\n([\s\S]*?)^\1[ \t]*$", parent, re.MULTILINE)
        example, = [text.rstrip("\n") for _,text in examples if text.startswith("# Label Normalization Design")]
        self.assertEqual(validate_model_record(parent, "docs/design/skill/design.md"), ())
        self.assertEqual(validate_model_record(example, "docs/design/label-normalization/label-normalization.md"), ())
        invalid = example.replace("Model validation contract: model-document-v1",
                                  "Model validation contract: unknown_value", 1)
        self.assertEqual([i.code for i in validate_model_record(invalid, "docs/design/label-normalization/label-normalization.md")],
                         ["BFR-MODEL-CONTRACT"])
        for source in ("skills/design/references/model-authoring.md", "skills/design/assets/design-skeleton.md"):
            text = (ROOT / source).read_text()
            self.assertIn("Model validation contract: model-document-v1", text)
            self.assertNotIn("Model validation contract: explicit-recording-v1", text)

    def test_model_mismatched_directory_examples_and_extra_nesting_reject(self):
        for relative in ("docs/design/cli/workflow.md", "docs/design/skill/examples/workflow/sample.md",
                         "docs/design/workflow/nested/workflow.md", "docs/design/skill/unknown_value.md",
                         "docs/design/skill/authoring/unknown_value.md", "docs/design/skill/authoring/design.md",
                         "docs/design/cli/examples/records/records.md"):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(self.text)
            self.assertTrue(validate_changed_spec(self.root, relative))

    def test_model_flat_historical_path_remains_explicitly_valid(self):
        path = self.root / "docs/design/workflow.md"
        path.write_text(self.text)
        self.assertEqual(validate_changed_spec(self.root, "docs/design/workflow.md"), ())

    def test_model_unknown_value_marker_and_dimension_fail_closed(self):
        for text in (
            self.text.replace("Model validation contract: model-document-v1", "Model validation contract: unknown_value", 1),
            self.text.replace("| Input domain |", "| unknown_value |", 1),
        ):
            with self.subTest(text=text[:50]):
                codes = {i.code for i in self.check(text)}
                self.assertTrue(codes & {"BFR-MODEL-CONTRACT", "BFR-MODEL-DIMENSIONS"}, codes)

    def test_model_missing_duplicate_malformed_tables_and_references_reject(self):
        variants = (
            self.text.replace("Model validation contract: model-document-v1\n", "", 1),
            self.text + "\nModel validation contract: model-document-v1\n",
            self.text + "\n## Requirements\n",
            self.text.replace("| Dimension | Requirement basis |", "| Dimension | unknown_value |", 1),
            self.text.replace(next(l for l in self.text.splitlines() if l.startswith("| Input domain |")), "| Input domain | not_in_vocabulary |", 1),
            self.text.replace(next(l for l in self.text.splitlines() if l.startswith("| Input domain |")), "| Input domain | WF-SR-02, WF-SR-02 |", 1),
            self.text.replace("| State/lifecycle |", "| Input domain |", 1),
            self.text.replace("| WF-SR-01 |", "| WF-SR-02 |", 1),
            self.text.replace("| WF-SR-01 |", "| 1-invalid |", 1),
            self.text.replace("| --- | --- | --- |\n| Input domain", "| bad | --- | --- |\n| Input domain", 1),
            self.text.replace(next(l for l in self.text.splitlines() if l.startswith("| Input domain |")), "| Input domain | WF-SR-02 | outcome | extra |", 1),
        )
        for index, text in enumerate(variants):
            with self.subTest(index=index):
                self.assertTrue(self.check(text))

    def test_model_not_applicable_requires_reason(self):
        row = next(l for l in self.text.splitlines() if l.startswith("| Input domain |"))
        self.assertEqual(self.check(self.text.replace(row, "| Input domain | - | Not applicable: no input behavior in this fixture. |")), ())
        for outcome in ("Not applicable:", "", "No reason"):
            self.assertTrue(self.check(self.text.replace(row, f"| Input domain | - | {outcome} |")))

    def test_model_unsafe_missing_and_symlink_paths_reject(self):
        self.check()
        for relative in ("docs/design/../workflow.md", "docs/design/nested/workflow.md", "docs/design/UPPER.md", "docs/design/missing.md"):
            self.assertTrue(validate_changed_spec(self.root, relative))
        self.path.unlink()
        outside = self.root / "outside.md"
        outside.write_text(self.text, encoding="utf-8")
        self.path.symlink_to(outside)
        self.assertTrue(validate_changed_spec(self.root, "docs/design/skill/workflow.md"))
        self.path.unlink()
        self.path.parent.rmdir()
        other = self.root / "other"
        other.mkdir()
        (other / "workflow.md").write_text(self.text, encoding="utf-8")
        self.path.parent.symlink_to(other, target_is_directory=True)
        self.assertTrue(validate_changed_spec(self.root, "docs/design/skill/workflow.md"))

    def test_model_fenced_contract_or_tables_are_not_authority(self):
        self.assertTrue(self.check("```md\n" + self.text + "\n```\n"))
        self.assertTrue(self.check(self.text.replace("## Requirements", "```md\n## Requirements", 1) + "\n```\n"))

    def test_model_indented_code_cannot_supply_required_sections(self):
        headings = {"## Requirements", "### Boundary scan and acceptance scenarios"}

        def indent_sections(prefix, tables_only=False):
            lines = []
            selected = False
            for line in self.text.splitlines():
                if line.startswith("#"):
                    selected = line in headings
                indent = selected and line and (not tables_only or line.startswith("|"))
                lines.append(prefix + line if indent else line)
            return "\n".join(lines) + "\n"

        for prefix in ("    ", "\t", "  \t"):
            for tables_only in (False, True):
                with self.subTest(prefix=prefix, tables_only=tables_only):
                    issues = self.check(indent_sections(prefix, tables_only))
                    self.assertIn("BFR-MODEL-TABLE", {issue.code for issue in issues})
        # Up to three spaces remain ordinary Markdown, not an indented code block.
        self.assertEqual(self.check(indent_sections("   ")), ())

    def test_model_public_check_is_read_only_and_not_activation(self):
        self.check()
        before = relevant_tree_snapshot(self.root)
        result = subprocess.run([sys.executable, str(ROOT / "scripts/validate-boundary-first.py"), "--check", "--root", str(self.root), "--path", "docs/design/skill/workflow.md"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["validation"], "structure-and-references-only")
        self.assertNotIn("activation", data)
        self.assertEqual(relevant_tree_snapshot(self.root), before)


class CurrentBoundaryCommandTests(unittest.TestCase):
    def run_check(self, root, *paths):
        command = [sys.executable, str(ROOT / "scripts/validate-boundary-first.py"), "--check", "--root", str(root)]
        for path in paths:
            command.extend(["--path", path])
        result = subprocess.run(command, capture_output=True, text=True)
        return result.returncode, json.loads(result.stdout)

    def test_default_checks_complete_current_model_population_without_specs(self):
        from model_layout import PROJECT_MODEL_PATHS
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for relative in PROJECT_MODEL_PATHS.values():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes((ROOT / relative).read_bytes())
            code, output = self.run_check(root)
            self.assertEqual(code, 0, output)
            self.assertEqual(set(output["paths"]), set(PROJECT_MODEL_PATHS.values()))
            self.assertNotIn("activation", output)
            self.assertNotIn("rollback_release", output)
            (root / PROJECT_MODEL_PATHS["system"]).unlink()
            code, output = self.run_check(root)
            self.assertEqual(code, 1, output)
            self.assertTrue(output["issues"])

    def test_default_checks_owned_examples_and_redacts_parse_failures(self):
        from model_layout import PROJECT_MODEL_PATHS
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for relative in PROJECT_MODEL_PATHS.values():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes((ROOT / relative).read_bytes())
            example = root / "docs/design/cli/examples/case.json"
            example.parent.mkdir(parents=True)
            example.write_text('{"secret": "private-value"}')
            code, output = self.run_check(root)
            self.assertEqual(code, 0, output)
            self.assertIn(example.relative_to(root).as_posix(), output["examples"])
            self.assertTrue(any("#model-example-" in path for path in output["examples"]))
            example.write_text('{"secret": private-value}')
            code, output = self.run_check(root)
            self.assertEqual(code, 1)
            self.assertNotIn("private-value", json.dumps(output))
            example.unlink()
            example.symlink_to(root / PROJECT_MODEL_PATHS["system"])
            code, output = self.run_check(root)
            self.assertEqual(code, 1)
            self.assertIn("BFR-EXAMPLE-PATH", {item["check_id"] for item in output["issues"]})

    def test_empty_model_population_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            code, output = self.run_check(Path(temporary))
            self.assertEqual(code, 1)
            self.assertTrue(output["issues"])

    def test_explicit_customer_grammar_does_not_require_repository_activation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "specs").mkdir()
            (root / "specs/feature.md").write_text(valid_feature())
            (root / "specs/feature.test.md").write_text(valid_proof())
            code, output = self.run_check(root, "specs/feature.test.md")
            self.assertEqual(code, 0, output)
            self.assertEqual(output["status"], "passed")


if __name__ == "__main__":
    unittest.main(verbosity=2)
