"""Route guidance.

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


class RouteSkillCutoverContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = ROOT / "skills" / "route"
        self.skill = (self.root / "SKILL.md").read_text(encoding="utf-8")

    def test_route_maps_only_routing_conditional_resources(self) -> None:
        expected = {
            "references/governed-lifecycle-routing.md": "READ",
            "references/bounded-workflow-automation.md": "READ",
            "references/boundary-first-method-v1.md": "READ",
        }
        for relative_path, verb in expected.items():
            with self.subTest(resource=relative_path):
                self.assertTrue((self.root / relative_path).is_file())
                self.assertIn(f"- {verb} `{relative_path}`", self.skill)

        self.assertFalse((self.root / "references/workflow-guide-authoring.md").exists())
        self.assertFalse((self.root / "assets/workflows-skeleton.md").exists())

    def test_route_declares_exact_predicates_and_assemblies(self) -> None:
        for predicate in (
            "governed_change_context",
            "automation_command_context",
            "armed_automation_context",
        ):
            self.assertIn(predicate, self.skill)
        self.assertNotIn("workflow_guide_authoring_context", self.skill)
        for assembly in (
            "WP0-generic-routing",
            "WP1-governed",
            "WP2-governed-automated",
            "WPB-automation-bootstrap",
            "WPS-stateless-automation-command",
        ):
            self.assertIn(assembly, self.skill)
        self.assertNotIn("WP3-guide-authoring", self.skill)
        self.assertNotIn("WP4-governed-guide-authoring", self.skill)

    def test_route_keeps_universal_stops_inline(self) -> None:
        for phrase in (
            "Conversational wording alone does not establish",
            "Unknown artifact types and unknown lifecycle stages are blockers",
            "Every predicate combination must match exactly one assembly row",
            "After classification and before resource-dependent interpretation or action",
            "contradiction among packaged resources",
            "stop rather than invent, recall, or partially reconstruct",
        ):
            self.assertIn(phrase, self.skill)

    def test_route_references_have_non_overlapping_owners(self) -> None:
        governed = (self.root / "references" / "governed-lifecycle-routing.md").read_text(encoding="utf-8")
        automation = (self.root / "references" / "bounded-workflow-automation.md").read_text(encoding="utf-8")
        self.assertIn("reviewed stable plan", governed)
        self.assertNotIn("architecture-required", governed)
        self.assertNotIn("architecture-not-required", governed)
        self.assertNotIn("architecture-ambiguous", governed)
        self.assertIn("Actor-owned updates", governed)
        self.assertIn("asks governed lifecycle procedure", automation)
        self.assertIn("must not redefine stage order", automation)

    def test_route_bootstrap_and_stateless_paths_are_explicit(self) -> None:
        automation = (self.root / "references" / "bounded-workflow-automation.md").read_text(encoding="utf-8")
        bootstrap_steps = (
            "Recognize the explicit target command",
            "Load bounded workflow automation procedure",
            "Resolve or create governed change identity",
            "Validate the governed record",
            "Reclassify as governed",
            "Load governed lifecycle procedure",
            "Only then persist authorization",
        )
        positions = [automation.index(step) for step in bootstrap_steps]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("no-active-run", automation)
        self.assertIn("creates no governed or automation state", automation)

    def test_route_consumes_cli_context_and_preserves_protocol_authority(self) -> None:
        self.assertIn("rigorloop workflow-context", self.skill)
        self.assertIn("Route owns explicit activity", self.skill)
        self.assertIn("targeted", self.skill)
        self.assertNotIn("docs/workflows.md", self.skill)

    def test_current_skill_validator_has_no_retired_guide_parser(self) -> None:
        validator = (ROOT / "scripts/lib/validation" / "skill_validation.py").read_text(encoding="utf-8")
        for retired in (
            "def validate_workflow_artifact_map_lookup",
            "def validate_workflow_artifact_map_contract",
            "def validate_workflow_guide_skeleton_contract",
            "WORKFLOW_GUIDE_SKELETON_REQUIRED_METADATA",
            "WORKFLOW_ARTIFACT_REQUIRED_REGISTRY_ENTRIES",
        ):
            with self.subTest(retired=retired):
                self.assertNotIn(retired, validator)
