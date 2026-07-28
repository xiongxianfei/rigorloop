#!/usr/bin/env python3
"""Regression tests for the boundary-first shared-reference projection."""

from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from boundary_first_reference import (  # noqa: E402
    CANONICAL_REFERENCE,
    GOVERNED_SKILLS,
    METHOD_VERSION,
    PROJECTED_REFERENCE,
    ProjectionContractError,
    inventory_digest,
    project_reference,
)


class BoundaryFirstReferenceTests(unittest.TestCase):
    def make_repository(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        source = root / CANONICAL_REFERENCE
        source.parent.mkdir(parents=True)
        source.write_bytes(b"# portable boundary method\n")
        for skill in GOVERNED_SKILLS:
            (root / "skills" / skill).mkdir(parents=True)
        return temporary, root

    def make_outside_directory(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return Path(temporary.name)

    def test_closed_version_source_and_consumers(self) -> None:
        self.assertEqual(METHOD_VERSION, "boundary-first-v1")
        self.assertEqual(
            CANONICAL_REFERENCE,
            Path("specs/references/boundary-first-method-v1.md"),
        )
        self.assertEqual(
            GOVERNED_SKILLS,
            (
                "workflow",
                "spec",
                "spec-review",
                "plan",
                "plan-review",
                "test-spec",
                "test-spec-review",
                "implement",
                "code-review",
                "verify",
            ),
        )
        self.assertEqual(
            PROJECTED_REFERENCE,
            Path("references/boundary-first-method-v1.md"),
        )

    def test_write_is_raw_byte_exact_and_idempotent(self) -> None:
        _, root = self.make_repository()
        source = root / CANONICAL_REFERENCE
        raw = b"# method\r\n\xce\xbb portable bytes\n"
        source.write_bytes(raw)

        first = project_reference(root, mode="write")
        second = project_reference(root, mode="write")

        self.assertTrue(first.ok)
        self.assertTrue(second.ok)
        self.assertEqual(first.projection_sha256, second.projection_sha256)
        for skill in GOVERNED_SKILLS:
            self.assertEqual(
                (root / "skills" / skill / PROJECTED_REFERENCE).read_bytes(),
                raw,
            )

    def test_check_reports_missing_stale_and_unexpected_projections(self) -> None:
        _, root = self.make_repository()
        project_reference(root, mode="write")
        missing = root / "skills" / "workflow" / PROJECTED_REFERENCE
        missing.unlink()
        stale = root / "skills" / "spec" / PROJECTED_REFERENCE
        stale.write_bytes(b"stale")
        unexpected = (
            root
            / "skills"
            / "proposal"
            / "references"
            / "boundary-first-method-v1.md"
        )
        unexpected.parent.mkdir(parents=True)
        unexpected.write_bytes((root / CANONICAL_REFERENCE).read_bytes())

        result = project_reference(root, mode="check")

        self.assertFalse(result.ok)
        self.assertEqual(
            result.errors,
            (
                "BFR-PROJECTION-MISSING: skills/workflow/references/"
                "boundary-first-method-v1.md",
                "BFR-PROJECTION-STALE: skills/spec/references/"
                "boundary-first-method-v1.md",
                "BFR-PROJECTION-UNEXPECTED: skills/proposal/references/"
                "boundary-first-method-v1.md",
            ),
        )

    def test_check_rejects_symlink_projection(self) -> None:
        _, root = self.make_repository()
        project_reference(root, mode="write")
        target = root / "skills" / "workflow" / PROJECTED_REFERENCE
        target.unlink()
        target.symlink_to(root / CANONICAL_REFERENCE)

        with self.assertRaisesRegex(
            ProjectionContractError,
            "BFR-PATH-SYMLINK: skills/workflow/references/"
            "boundary-first-method-v1.md",
        ):
            project_reference(root, mode="check")

    def test_parent_symlink_escape_fails_without_outside_mutation(self) -> None:
        _, root = self.make_repository()
        outside = self.make_outside_directory()
        sentinel = outside / PROJECTED_REFERENCE.name
        sentinel.write_bytes(b"outside sentinel")
        references = root / "skills" / "workflow" / "references"
        references.symlink_to(outside, target_is_directory=True)

        for mode in ("check", "write"):
            with self.subTest(mode=mode):
                with self.assertRaisesRegex(
                    ProjectionContractError,
                    "BFR-PATH-SYMLINK: skills/workflow/references",
                ):
                    project_reference(root, mode=mode)
                self.assertEqual(sentinel.read_bytes(), b"outside sentinel")

    def test_source_parent_symlink_escape_fails_before_read(self) -> None:
        _, root = self.make_repository()
        source = root / CANONICAL_REFERENCE
        source.unlink()
        source.parent.rmdir()
        outside = self.make_outside_directory()
        (outside / CANONICAL_REFERENCE.name).write_bytes(b"outside method")
        source.parent.symlink_to(outside, target_is_directory=True)

        with self.assertRaisesRegex(
            ProjectionContractError,
            "BFR-PATH-SYMLINK: specs/references",
        ):
            project_reference(root, mode="check")

    def test_unexpected_consumer_symlink_topologies_fail_closed(self) -> None:
        for topology in ("skill-root", "references"):
            with self.subTest(topology=topology):
                _, root = self.make_repository()
                project_reference(root, mode="write")
                outside = self.make_outside_directory()
                if topology == "skill-root":
                    outside_reference = outside / PROJECTED_REFERENCE
                    outside_reference.parent.mkdir()
                    outside_reference.write_bytes(b"outside method")
                    (root / "skills" / "proposal").symlink_to(
                        outside,
                        target_is_directory=True,
                    )
                    expected_path = "skills/proposal"
                else:
                    outside_reference = outside / PROJECTED_REFERENCE.name
                    outside_reference.write_bytes(b"outside method")
                    proposal = root / "skills" / "proposal"
                    proposal.mkdir()
                    (proposal / "references").symlink_to(
                        outside,
                        target_is_directory=True,
                    )
                    expected_path = "skills/proposal/references"

                result = project_reference(root, mode="check")

                self.assertFalse(result.ok)
                self.assertIn(
                    f"BFR-UNEXPECTED-CONSUMER-SYMLINK: {expected_path}",
                    result.errors,
                )

    def test_inventory_digest_uses_sorted_posix_path_and_raw_hash_records(
        self,
    ) -> None:
        records = {
            "skills/z/reference.md": hashlib.sha256(b"z").hexdigest(),
            "skills/a/reference.md": hashlib.sha256(b"a").hexdigest(),
        }
        serialized = b"".join(
            (
                f"{path}\0{records[path]}\n".encode("utf-8")
                for path in sorted(records)
            )
        )

        self.assertEqual(
            inventory_digest(records),
            hashlib.sha256(serialized).hexdigest(),
        )

    def test_unknown_mode_fails_before_projection_consistency(self) -> None:
        _, root = self.make_repository()

        with self.assertRaisesRegex(
            ProjectionContractError,
            "BFR-MODE-UNKNOWN: unknown projection mode 'future'",
        ):
            project_reference(root, mode="future")

    def test_canonical_method_contains_portable_contract_without_stage_policy(
        self,
    ) -> None:
        text = (ROOT / CANONICAL_REFERENCE).read_text(encoding="utf-8")
        required = (
            "Boundary model version: boundary-first-v1",
            "## Core dimensions",
            "## Feature-spec boundary record",
            "## Test-spec proof record",
            "applicable",
            "not-applicable",
            "illustration",
            "regression",
            "discovery",
            "No interaction selected:",
            "covered",
            "gap",
            "Structural validation",
            "Semantic review",
        )
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, text)
        forbidden = (
            "Immediate next stage:",
            "Implementation handoff:",
            "Recording status:",
            "branch-ready",
            "PR readiness",
        )
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, text)


if __name__ == "__main__":
    unittest.main()
