"""Project map guidance.

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


class ProjectMapSkillSimplificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = ROOT / "skills" / "project-map"
        self.skill = (self.root / "SKILL.md").read_text(encoding="utf-8")
        self.reference_path = self.root / "references" / "map-maintenance-and-area-coordination.md"
        self.reference = self.reference_path.read_text(encoding="utf-8") if self.reference_path.is_file() else ""

    def test_package_and_loaded_assemblies_are_closed(self) -> None:
        self.assertEqual(sorted(path.name for path in (self.root / "assets").iterdir()), ["project-map-skeleton.md"])
        self.assertEqual(sorted(path.name for path in (self.root / "references").iterdir()), ["map-maintenance-and-area-coordination.md"])
        for value in ("PMA0-simple-root-create", "PMA1-maintenance-or-coordinated"):
            self.assertIn(value, self.skill)
        self.assertIn("READ `references/map-maintenance-and-area-coordination.md`", self.skill)
        self.assertIn("COPY `assets/project-map-skeleton.md`", self.skill)
        self.assertIn("Late coordination discovery", self.skill)

    def test_operation_scope_and_target_state_contract_is_closed(self) -> None:
        for value in ("`create`", "`refresh`", "`audit`", "`repository`", "`area:<slug>`"):
            self.assertIn(value, self.skill)
        for phrase in (
            "applies only when the resolved target is absent",
            "applies only when the resolved target exists",
            "complete rewrite of an existing map is a refresh",
            "is always read-only",
            "missing-map",
            "new refresh operation",
        ):
            self.assertIn(phrase, self.skill.lower())
        self.assertIn("Operation: <create | refresh | audit>", self.skill)
        self.assertIn("Map scope: <repository | area:<slug>>", self.skill)
        self.assertNotIn("Mode: <", self.skill)

    def test_coordination_preflight_is_bounded_and_fail_closed(self) -> None:
        for phrase in (
            "project-local workflow guidance",
            "root-map path",
            "area-map directory",
            "root registration",
            "area-map files",
            "request-supplied coordination evidence",
            "active change context",
            "must not broadly scan the repository merely to prove absence",
            "unavailable, conflicting, or ambiguous",
        ):
            self.assertIn(phrase, self.skill.lower())

    def test_universal_evidence_and_reliance_rules_remain_inline(self) -> None:
        for phrase in (
            "observed",
            "inferred",
            "unknown",
            "current",
            "partial",
            "stale",
            "configured command",
            "executed command",
            "<sha>+dirty",
            "source and runtime configuration",
            "must inspect source directly",
        ):
            self.assertIn(phrase, self.skill.lower())

    def test_conditional_reference_owns_maintenance_and_area_transaction(self) -> None:
        for phrase in (
            "refresh trigger comparison",
            "affected-section selection",
            "correction note",
            "audit procedure",
            "root registration",
            "overlap ownership",
            "previous and current baseline",
            "write the area map first",
            "registration last",
            "transaction commit point",
            "idempotent success",
            "must not adopt",
        ):
            self.assertIn(phrase, self.reference.lower())

    def test_required_resource_failure_stops_without_reconstruction(self) -> None:
        for phrase in (
            "missing",
            "unreadable",
            "escaped",
            "contradictory",
            "mixed-version",
            "stop",
            "must not reconstruct",
        ):
            self.assertIn(phrase, self.skill.lower())
