"""Design resource.

Current Skill contracts own the protected structures, resources and authority.
Wording checks detect structural drift; independent review assesses semantics.
Current resource inventory and unknown-first admission are the protected outcomes.
"""
from __future__ import annotations

import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.validation import skill_validation
from skill_cli_tests import run_validator
from skill_fixture_helpers import copied_skill


# Design Method's Public resource table, independently of validator dispatch.
EXPECTED_DESIGN_RESOURCES = frozenset({
    "assets/design-skeleton.md",
    "assets/diagram-styles.mmd",
    "references/architecture-view-examples.md",
    "references/boundary-first-method-v1.md",
    "references/governed-design-authoring.md",
    "references/legacy-source-reconciliation.md",
    "references/model-authoring.md",
    "references/system-composition.md",
    "references/technical-design.md",
    "references/test-quality.md",
})


class UnifiedDesignResourceTests(unittest.TestCase):

    def test_unknown_design_resource_precedes_missing_resource_consistency(self):
        for missing in (False, True):
            with self.subTest(missing=missing), copied_skill("design") as root:
                baseline = run_validator(root)
                self.assertEqual(baseline.returncode, 0, baseline.stdout + baseline.stderr)
                (root / "references/unrecognized.md").write_text("# Unexpected resource\n")
                if missing:
                    (root / "references/technical-design.md").unlink()
                result = run_validator(root)
                self.assertNotEqual(result.returncode, 0)
                output = result.stdout + result.stderr
                unknown = "unknown design resource: references/unrecognized.md"
                self.assertIn(unknown, output)
                if missing:
                    self.assertLess(output.index(unknown), output.index(
                        "required design resource missing: references/technical-design.md"))

    def test_complete_package_and_retired_names(self):
        root = ROOT / "skills/design"
        self.assertFalse((ROOT / "skills/spec").exists())
        self.assertFalse((ROOT / "skills/architecture").exists())
        self.assertEqual(run_validator(root).returncode, 0)
        self.assertEqual({p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}, {"SKILL.md", *EXPECTED_DESIGN_RESOURCES})

    def test_missing_each_conditional_design_resource_rejects(self):
        self.assertEqual(skill_validation.DESIGN_RESOURCES, EXPECTED_DESIGN_RESOURCES)
        for resource in sorted(EXPECTED_DESIGN_RESOURCES):
            with self.subTest(resource=resource), copied_skill("design") as root:
                (root / resource).unlink()
                result = run_validator(root)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    "required design resource missing: " + resource,
                    result.stdout + result.stderr,
                )


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
