#!/usr/bin/env python3
"""Regression tests for local Codex skill mirror generation."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
BUILD_SKILLS_PATH = ROOT / "scripts" / "build-skills.py"


def load_build_skills_module():
    spec = importlib.util.spec_from_file_location("build_skills", BUILD_SKILLS_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to import {BUILD_SKILLS_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class BuildSkillsTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp(prefix="build-skills-test-"))
        self.addCleanup(lambda: shutil.rmtree(self.tmpdir, ignore_errors=True))
        self.build_skills = load_build_skills_module()

    def test_output_dir_generates_complete_skill_mirror(self) -> None:
        output_dir = self.tmpdir / "generated-skills"

        result = self.build_skills.main(["--output-dir", str(output_dir)])

        self.assertEqual(result, 0)
        self.assertTrue((output_dir / "proposal" / "SKILL.md").is_file())
        self.assertTrue((output_dir / "workflow" / "SKILL.md").is_file())
        self.assertFalse(self.build_skills.collect_drift(self.build_skills.CANONICAL_SKILLS_DIR, output_dir))

    def test_check_with_output_dir_generates_and_validates_non_tracked_output(self) -> None:
        output_dir = self.tmpdir / "check-output"

        result = self.build_skills.main(["--check", "--output-dir", str(output_dir)])

        self.assertEqual(result, 0)
        self.assertTrue((output_dir / "proposal" / "SKILL.md").is_file())
        self.assertFalse(self.build_skills.collect_drift(self.build_skills.CANONICAL_SKILLS_DIR, output_dir))

    def test_check_without_output_dir_does_not_read_tracked_generated_root(self) -> None:
        stale_generated_root = self.tmpdir / "stale-codex-skills"
        stale_generated_root.mkdir()
        (stale_generated_root / "unexpected.txt").write_text("stale", encoding="utf-8")

        with mock.patch.object(self.build_skills, "GENERATED_SKILLS_DIR", stale_generated_root):
            result = self.build_skills.main(["--check"])

        self.assertEqual(result, 0)

    def test_generated_output_validation_rejects_structurally_invalid_skill(self) -> None:
        invalid_root = self.tmpdir / "invalid"
        invalid_skill = invalid_root / "broken" / "SKILL.md"
        invalid_skill.parent.mkdir(parents=True)
        invalid_skill.write_text("# Missing frontmatter\n", encoding="utf-8")

        errors = self.build_skills.validate_generated_output(invalid_root)

        self.assertTrue(errors)
        self.assertIn("file must begin with YAML frontmatter", "\n".join(errors))

    def test_check_reports_structural_validation_errors(self) -> None:
        output_dir = self.tmpdir / "check-output"

        def write_invalid_output(_source_root: Path, generated_root: Path) -> None:
            invalid_skill = generated_root / "broken" / "SKILL.md"
            invalid_skill.parent.mkdir(parents=True)
            invalid_skill.write_text("# Missing frontmatter\n", encoding="utf-8")

        output = io.StringIO()
        with mock.patch.object(self.build_skills, "sync_generated_output", write_invalid_output):
            with contextlib.redirect_stdout(output):
                result = self.build_skills.main(["--check", "--output-dir", str(output_dir)])

        self.assertEqual(result, 1)
        self.assertIn("file must begin with YAML frontmatter", output.getvalue())

    def test_generated_resource_parity_reports_stale_mapped_resource_hashes(self) -> None:
        output_dir = self.tmpdir / "generated-skills"
        self.build_skills.sync_generated_output(
            self.build_skills.CANONICAL_SKILLS_DIR,
            output_dir,
        )
        generated_resource = output_dir / "architecture" / "assets" / "architecture-skeleton.md"
        generated_resource.write_text(
            generated_resource.read_text(encoding="utf-8") + "\nstale\n",
            encoding="utf-8",
        )

        errors = self.build_skills.collect_generated_resource_parity_errors(
            self.build_skills.CANONICAL_SKILLS_DIR,
            output_dir,
        )

        self.assertTrue(
            any(
                "mapped resource parity mismatch: architecture: assets/architecture-skeleton.md"
                in error
                and "canonical sha256=" in error
                and "generated sha256=" in error
                for error in errors
            ),
            errors,
        )

    def test_generated_resource_parity_reports_missing_mapped_resource(self) -> None:
        output_dir = self.tmpdir / "generated-skills"
        self.build_skills.sync_generated_output(
            self.build_skills.CANONICAL_SKILLS_DIR,
            output_dir,
        )
        (output_dir / "architecture" / "assets" / "adr-skeleton.md").unlink()

        errors = self.build_skills.collect_generated_resource_parity_errors(
            self.build_skills.CANONICAL_SKILLS_DIR,
            output_dir,
        )

        self.assertTrue(
            any(
                "mapped resource missing: architecture: assets/adr-skeleton.md "
                "in generated local skill mirror" in error
                for error in errors
            ),
            errors,
        )


if __name__ == "__main__":
    unittest.main()
