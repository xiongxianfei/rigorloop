"""Portable input containment, adoption and diagnostic privacy."""

from __future__ import annotations

import sys
from pathlib import Path
import json
import tempfile
import unittest

from boundary_fixture_helpers import (
    ROOT,
    FIXTURES,
    valid_feature,
    valid_proof,
)

sys.path.insert(0, str(ROOT / "scripts"))

from lib.validation.boundary_first_validation import validate_changed_spec, validate_feature_record


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
            root = Path(temporary) / "repo"
            root.mkdir()
            (root / "specs").mkdir()
            outside = root.parent / "outside-boundary-first.md"
            outside.write_text("# outside\n", encoding="utf-8")
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
            root = Path(temporary) / "repo"
            root.mkdir()
            (root / "specs").mkdir()
            outside = root.parent / "outside-boundary-companion.md"
            outside.write_text(valid_feature(), encoding="utf-8")
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
            root = Path(temporary) / "repo"
            root.mkdir()
            outside_specs = root.parent / "outside-specs"
            outside_specs.mkdir()
            (outside_specs / "feature.md").write_text(valid_feature())
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
