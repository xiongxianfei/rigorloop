"""Portable feature/proof grammar and unknown-value rejection."""

from __future__ import annotations

import sys
from pathlib import Path
import tempfile
import unittest

from boundary_fixture_helpers import (
    ROOT,
    FIXTURES,
    valid_feature,
    valid_proof,
)

sys.path.insert(0, str(ROOT / "scripts"))

from lib.validation.boundary_first_validation import validate_changed_spec, validate_feature_record, validate_proof_map


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
