"""Design resource.

Current Skill contracts own the protected structures, resources and authority.
Wording checks detect structural drift; independent review assesses semantics.
Existing class/case selectors remain stable, including historical names.
"""
from __future__ import annotations

import shutil
import unittest
import tempfile
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.validation import skill_validation
from skill_cli_tests import run_validator


# Design Method's Public resource table, independently of validator dispatch.
EXPECTED_DESIGN_RESOURCES = frozenset({
    "assets/design-skeleton.md",
    "assets/diagram-styles.mmd",
    "references/architecture-view-examples.md",
    "references/boundary-first-feature-authoring-v1.md",
    "references/boundary-first-method-v1.md",
    "references/governed-design-authoring.md",
    "references/legacy-source-reconciliation.md",
    "references/model-authoring.md",
    "references/system-composition.md",
    "references/technical-design.md",
    "references/test-quality.md",
})


class UnifiedDesignResourceTests(unittest.TestCase):
    def test_retired_standalone_resources_are_absent_and_cannot_be_reintroduced(self):
        retired = ("assets/legacy-architecture-skeleton.md", "assets/legacy-adr-skeleton.md",
                   "references/legacy-technical-authoring.md")
        for resource in retired:
            with self.subTest(resource=resource), tempfile.TemporaryDirectory() as tmp:
                source = ROOT / "skills/design"
                self.assertFalse((source / resource).exists())
                root = Path(tmp) / "design"
                shutil.copytree(source, root)
                (root / resource).write_text("# Retired standalone output resource\n")
                result = run_validator(root)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("unknown design resource: " + resource, result.stdout + result.stderr)
        for name in ("architecture.md", "adr.md"):
            self.assertFalse((ROOT / "templates" / name).exists())

    def test_unknown_design_resource_precedes_missing_resource_consistency(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "design"
            shutil.copytree(ROOT / "skills/design", root)
            (root / "references/unrecognized.md").write_text("# Unexpected resource\n")
            (root / "references/technical-design.md").unlink()
            result = run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            output = result.stdout + result.stderr
            self.assertLess(output.index("unknown design resource: references/unrecognized.md"),
                            output.index("required design resource missing: references/technical-design.md"))

    def test_complete_package_and_retired_names(self):
        root = ROOT / "skills/design"
        self.assertFalse((ROOT / "skills/spec").exists())
        self.assertFalse((ROOT / "skills/architecture").exists())
        self.assertEqual(run_validator(root).returncode, 0)
        self.assertEqual({p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}, {"SKILL.md", *EXPECTED_DESIGN_RESOURCES})

    def test_missing_each_conditional_design_resource_rejects(self):
        self.assertEqual(skill_validation.DESIGN_RESOURCES, EXPECTED_DESIGN_RESOURCES)
        for resource in sorted(EXPECTED_DESIGN_RESOURCES):
            with self.subTest(resource=resource), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp) / "design"
                shutil.copytree(ROOT / "skills/design", root)
                (root / resource).unlink()
                result = run_validator(root)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    "required design resource missing: " + resource,
                    result.stdout + result.stderr,
                )

    def test_unknown_value_design_resource_rejects(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "design"
            shutil.copytree(ROOT / "skills/design", root)
            (root / "references/unknown_value.md").write_text("unexpected resource")
            result = run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unknown", (result.stdout + result.stderr).lower())

    def test_legacy_boundary_projection_keeps_complete_format(self):
        root = ROOT / "skills/design/references"
        for name in ("boundary-first-method-v1.md", "boundary-first-feature-authoring-v1.md"):
            self.assertEqual((root / name).read_bytes(), (ROOT / "templates/shared" / name).read_bytes())
        body = (root / "boundary-first-feature-authoring-v1.md").read_text()
        headings = ("## Boundary model", "## Boundary definitions", "## Selected interactions", "## Example ownership")
        positions = [body.index(h) for h in headings]
        self.assertEqual(positions, sorted(positions))

    def test_governed_recording_stays_conditional_and_readable(self):
        root = ROOT / "skills/design"
        body = (root / "SKILL.md").read_text()
        self.assertIn("do not fall back to portable mode", body)
        self.assertIn("when one valid governed change", body)
        ref = (root / "references/governed-design-authoring.md").read_text()
        self.assertIn("expected_revision", ref)
        self.assertIn("Do not migrate", ref)
        self.assertIn("does not approve", ref)
        self.assertNotIn("record-store check|record", ref)
