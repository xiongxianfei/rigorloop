"""Plan guidance.

Current Skill contracts own the protected structures, resources and authority.
Wording checks detect structural drift; independent review assesses semantics.
Existing class/case selectors remain stable, including historical names.
"""
from __future__ import annotations

import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))


class PlanSkillSimplificationContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = ROOT / "skills" / "plan"
        self.skill = (self.root / "SKILL.md").read_text(encoding="utf-8")
        self.reference = (
            self.root / "references" / "governed-plan-authoring.md"
        ).read_text(encoding="utf-8")
        self.change_root = (
            ROOT / "docs" / "changes" / "2026-08-12-plan-skill-simplification"
        )


    def test_plan_simplification_package_and_profiles_are_closed(self) -> None:
        self.assertEqual(
            sorted(path.name for path in (self.root / "assets").iterdir()),
            ["decision-log-row.md", "milestone.md", "plan-skeleton.md"],
        )
        self.assertIn("references/governed-plan-authoring.md", self.skill)
        self.assertIn("references/boundary-first-method-v1.md", self.skill)
        for operation in (
            "create-primary-plan",
            "revise-primary-plan",
            "initialize-approved-plan",
        ):
            self.assertIn(operation, self.skill)
        self.assertIn("change link", self.reference)
        self.assertIn("Conversational wording", self.skill)
        self.assertIn("does not establish governed authority", self.skill)

    def test_plan_simplification_governed_reference_owns_only_governed_procedure(self) -> None:
        for phrase in ("approved Delivery Review package", "change link", "Never initialize an unreviewed draft", "route owns subsequent work decisions", "exactly once"):
            self.assertIn(phrase, self.reference)
        self.assertNotIn("record-artifact-revision", self.reference)

    def test_plan_simplification_assets_are_stable_intent_only(self) -> None:
        milestone = (self.root / "assets" / "milestone.md").read_text(
            encoding="utf-8"
        )
        for required in (
            "Milestone kind",
            "Completion criteria",
            "Required evidence",
            "Review handoff",
            "Rollback/recovery",
        ):
            self.assertIn(required, milestone)
        for forbidden in (
            "Milestone state:",
            "validation passed",
            "progress updated",
            "milestone committed",
        ):
            self.assertNotIn(forbidden, milestone)
