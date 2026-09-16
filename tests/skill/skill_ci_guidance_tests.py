"""Ci guidance.

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


class CiMaintenanceSkillSimplificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = ROOT / "docs" / "changes" / "2026-08-19-ci-maintenance-skill-simplification"
        self.skill_dir = ROOT / "skills" / "ci-maintenance"


    def test_package_split_and_closed_axes_are_present(self) -> None:
        skill = (self.skill_dir / "SKILL.md").read_text(encoding="utf-8")
        reference = (self.skill_dir / "references" / "github-workflow-authoring.md").read_text(encoding="utf-8")
        for value in (
            "create",
            "revise",
            "review",
            "invalid-or-ambiguous-target",
            "CIM8",
            "bounded-pr-ci-repair",
            "not-observed",
            "pending",
            "passed",
            "failed",
        ):
            self.assertIn(value, skill)
        self.assertIn("serializes", reference)
        self.assertIn("MUST NOT independently choose", reference)

    def test_minimal_skeleton_omits_privileged_and_boundary_examples(self) -> None:
        skeleton = (self.skill_dir / "assets" / "github-workflow-skeleton.yml").read_text(encoding="utf-8")
        for forbidden in ("pull_request:", "push:", "schedule:", "workflow_dispatch:", "pull_request_target", "secrets:", "id-token:"):
            self.assertNotIn(forbidden, skeleton)
        self.assertIn("permissions:\n  contents: read", skeleton)

    def test_risk_map_owns_semantic_placement(self) -> None:
        risk_map = (self.skill_dir / "references" / "risk-to-check-map.md").read_text(encoding="utf-8")
        self.assertIn("sole semantic owner", risk_map)
        self.assertIn("required execution boundary", risk_map)


    def test_write_and_batch_safety_guidance_is_present(self) -> None:
        skill = (self.skill_dir / "SKILL.md").read_text(encoding="utf-8")
        for phrase in ("Create uses commit-time atomic no-clobber", "Revise replaces only while identity matches", "Providers precede wrappers", "Unsafe states or cycles return `blocked-before-write`"):
            self.assertIn(phrase, skill)

    def test_partial_batch_and_retry_are_exact(self) -> None:
        skill = (self.skill_dir / "SKILL.md").read_text(encoding="utf-8")
        for phrase in ("partial-blocked", "completed and pending targets", "Retry rebuilds the entire graph", "adopts no stale manifest"):
            self.assertIn(phrase, skill)
