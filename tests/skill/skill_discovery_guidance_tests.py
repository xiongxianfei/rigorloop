"""Discovery guidance.

Current Skill contracts own the protected structures, resources and authority.
Wording checks detect structural drift; independent review assesses semantics.
Existing class/case selectors remain stable, including historical names.
"""
from __future__ import annotations

import re
import unittest
import tempfile
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.validation import skill_validation


class OptionalDiscoverySkillContractTests(unittest.TestCase):
    """ER-R1-ER-R22 and ER-R27-ER-R34 canonical package contract."""

    def test_explore_uses_proportional_standalone_option_discovery(self) -> None:
        body = (ROOT / "skills/explore/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("docs/explorations/YYYY-MM-DD-slug.md", body)
        self.assertIn("enough materially distinct options", body)
        self.assertIn("explicit invocation", body)
        self.assertIn("decision owner", body)
        self.assertNotIn("Generate at least five options", body)
        self.assertNotIn("docs/proposals/YYYY-MM-DD-slug.explore.md", body)
        self.assertNotIn("inline exploration report", body)

    def test_research_uses_bounded_standalone_evidence(self) -> None:
        body = (ROOT / "skills/research/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("docs/research/YYYY-MM-DD-slug.md", body)
        self.assertIn("bounded", body)
        self.assertIn("explicit invocation", body)
        self.assertIn("confidence", body)
        self.assertIn("decision owner", body)
        self.assertNotIn("compact research section", body)
        self.assertNotIn("research artifact path or concise report", body)

    def test_discovery_packages_are_self_contained_and_share_exact_policy(self) -> None:
        canonical = (ROOT / "templates/shared/discovery-support.md").read_bytes()
        expected_resources = {
            "explore": {
                "assets/exploration-skeleton.md",
                "references/discovery-support.md",
                "references/option-discovery-methods.md",
                "references/high-impact-decision-method.md",
            },
            "research": {
                "assets/research-skeleton.md",
                "references/discovery-support.md",
                "references/source-and-repository-method.md",
                "references/experiment-and-confidence-method.md",
            },
        }
        for skill_name, resources in expected_resources.items():
            skill_dir = ROOT / "skills" / skill_name
            body = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=skill_name):
                self.assertEqual(
                    canonical,
                    (skill_dir / "references/discovery-support.md").read_bytes(),
                )
                for resource in resources:
                    self.assertTrue((skill_dir / resource).is_file(), resource)
                    self.assertIn(resource, body)
                self.assertIn("## Resource map", body)
                self.assertIn("## Stop conditions", body)
                self.assertIn("## Claims this skill must not make", body)

    def test_skill_contract_names_discovery_shared_policy(self) -> None:
        # Structural name-presence guard only. Admission meaning is assessed by
        # independent semantic review; this substring cannot establish it.
        contract = (ROOT / "docs/design/skill/skill.md").read_text(encoding="utf-8")
        self.assertIn("discovery-support", contract)

    def test_every_discovery_package_file_omits_maintainer_only_details(self) -> None:
        forbidden = {
            "canonical skill path": re.compile(r"\bskills/(?:explore|research)/SKILL\.md\b"),
            "shared template path": re.compile(r"\btemplates/shared\b"),
            "adapter package path": re.compile(r"\bdist/adapters\b"),
            "selector constraint": re.compile(r"\bselector[- ]path constraints\b", re.IGNORECASE),
            "shared-copy mechanics": re.compile(r"\bshared[- ]block implementation\b", re.IGNORECASE),
        }
        for skill_name in ("explore", "research"):
            for path in sorted((ROOT / "skills" / skill_name).rglob("*")):
                if not path.is_file():
                    continue
                body = path.read_text(encoding="utf-8")
                for label, pattern in forbidden.items():
                    with self.subTest(skill=skill_name, path=path.name, pattern=label):
                        self.assertIsNone(pattern.search(body))

    def test_canonical_validation_rejects_discovery_shared_policy_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            canonical = root / "discovery-support.md"
            canonical.write_text("canonical\n", encoding="utf-8")
            local = root / "local.md"
            local.write_text("drifted\n", encoding="utf-8")
            errors = skill_validation.validate_discovery_support_copy(
                local,
                "explore",
                canonical_path=canonical,
            )
        self.assertTrue(any("differs from canonical source" in error for error in errors))

    def test_canonical_validation_rejects_unknown_discovery_skill_name(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            canonical = root / "discovery-support.md"
            canonical.write_text("canonical\n", encoding="utf-8")
            local = root / "local.md"
            local.write_text("canonical\n", encoding="utf-8")
            errors = skill_validation.validate_discovery_support_copy(
                local,
                "unknown-discovery-skill",
                canonical_path=canonical,
            )
        self.assertTrue(any("unknown discovery support consumer" in error for error in errors))

    def test_route_distinguishes_explore_research_both_and_neither(self) -> None:
        route = (ROOT / "skills/route/SKILL.md").read_text(encoding="utf-8")
        expected = {
            "Explore": "the option space is materially unclear",
            "Research": "a material decision depends on an uncertain fact",
            "both": "research questions could materially change the option comparison",
            "neither": "direction and decision-relevant facts are sufficiently clear",
        }
        for route_case, phrase in expected.items():
            with self.subTest(route_case=route_case):
                self.assertIn(phrase, route)

    def test_current_guidance_agrees_on_explicit_optional_discovery_handoff(self) -> None:
        surfaces = {
            "workflow": ROOT / "skills/route/SKILL.md",
            "readme": ROOT / "README.md",
            "project-map": ROOT / "docs/project-map.md",
        }
        bodies = {
            name: path.read_text(encoding="utf-8")
            for name, path in surfaces.items()
        }
        for name, body in bodies.items():
            with self.subTest(surface=name, rule="optional"):
                self.assertIn("Explore", body)
                self.assertIn("Research", body)
        self.assertIn("explicit invocation", bodies["workflow"])
        self.assertIn("owning stage", bodies["workflow"])
        self.assertIn("docs/explorations/", bodies["project-map"])
        self.assertIn("docs/research/", bodies["project-map"])

    def test_route_keeps_incidental_discovery_artifact_free_and_owner_bounded(self) -> None:
        route = (ROOT / "skills/route/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("incidental fact check", route)
        self.assertIn("does not create a discovery artifact", route)
        self.assertIn("must explicitly adopt", route)
        self.assertIn("does not approve", route)
        self.assertIn("does not advance lifecycle state", route)
