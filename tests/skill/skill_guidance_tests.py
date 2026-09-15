"""Canonical guidance consistency, without claiming semantic adequacy."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.validation import skill_validation


class SkillGuidanceChecks:
    def test_optional_discovery_canonical_resources_are_portable(self):
        # Archive byte preservation belongs to the independent inventory test.
        expected_resources = {
            "explore": {"assets/exploration-skeleton.md", "references/discovery-support.md",
                        "references/option-discovery-methods.md", "references/high-impact-decision-method.md"},
            "research": {"assets/research-skeleton.md", "references/discovery-support.md",
                         "references/source-and-repository-method.md", "references/experiment-and-confidence-method.md"},
        }
        policy = (ROOT / "templates/shared/discovery-support.md").read_bytes()
        for name, resources in expected_resources.items():
            with self.subTest(skill=name):
                skill = ROOT / "skills" / name
                self.assertEqual((skill / "references/discovery-support.md").read_bytes(), policy)
                content = b"\n".join((skill / relative).read_bytes()
                                     for relative in sorted({"SKILL.md", *resources}))
                for forbidden in (b"skills/explore/SKILL.md", b"skills/research/SKILL.md",
                                  b"templates/shared", b"dist/adapters"):
                    self.assertNotIn(forbidden, content)
                expected = (b"docs/explorations/YYYY-MM-DD-slug.md" if name == "explore"
                            else b"docs/research/YYYY-MM-DD-slug.md")
                self.assertIn(expected, content)

    def test_targeted_canonical_profiles_use_primary_interface(self):
        names = ("proposal", "proposal-review", "design", "design-review", "plan", "delivery-review",
                 "implement", "code-review", "route", "verify", "bugfix", "ci-maintenance", "pr",
                 "research", "explore", "learn")
        references = {"plan": "references/governed-plan-authoring.md",
                      "implement": "references/governed-implementation-recording.md",
                      "code-review": "references/governed-code-review-recording.md",
                      "design": "references/governed-design-authoring.md",
                      "proposal": "references/governed-proposal-authoring.md",
                      "proposal-review": "references/proposal-review-recording-and-settlement.md"}
        for name in names:
            with self.subTest(skill=name):
                relative = references.get(name, "SKILL.md")
                body = (ROOT / "skills" / name / relative).read_text(encoding="utf-8")
                if relative == "SKILL.md":
                    body = body.split("## Explicit recording\n", 1)[1].split("\n## ", 1)[0]
                self.assertIn("subject inspect", body)
                self.assertNotIn("record-store check|record", body)

    # Retained pending an owner-backed replacement for this legacy checklist
    # drift guard. Phrase presence is not proof of instruction quality.
    def test_code_review_owns_published_skill_semantic_checklist(self) -> None:
        body = (ROOT / "skills" / "code-review" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        section = body.split("## Published-skill semantic review", 1)[1].split(
            "\n## ", 1
        )[0]
        for concept in (
            "description and trigger", "ownership", "prerequisites", "procedure",
            "packaged resources", "stop conditions", "claims", "output and handoff",
            "review finding", "Do not convert this checklist",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, section)


class ExplicitRecordingGuidanceTests(unittest.TestCase):
    def test_targeted_pilot_canonical_references_are_valid(self):
        # Real canonical-resource consistency; component faults use minimal fixtures.
        for name in ("proposal", "proposal-review", "implement", "code-review", "plan"):
            with self.subTest(skill=name):
                path = ROOT / "skills" / name / "SKILL.md"
                body = path.read_text(encoding="utf-8")
                self.assertNotIn("## Explicit recording", body)
                self.assertEqual(skill_validation.validate_targeted_recording_profile(path, body), [])

    def test_targeted_pilot_placement_uses_current_v3_without_inline_heading(self):
        path = ROOT / "skills/proposal-review/SKILL.md"
        body = path.read_text()
        self.assertNotIn("## Explicit recording", body)
        self.assertEqual(skill_validation.validate_installed_skill_artifact_placement_contract(path, "proposal-review", body), [])
        self.assertTrue(skill_validation.validate_installed_skill_artifact_placement_contract(path, "proposal-review", body.replace("reviews/proposal-review.json", "reviews/proposal-review.md")))

    def test_targeted_profile_validator_rejects_retired_normal_writer(self):
        from lib.validation.skill_validation import validate_targeted_recording_profile
        path = ROOT / "skills/route/SKILL.md"
        text = path.read_text()
        self.assertEqual(validate_targeted_recording_profile(path, text), [])
        self.assertTrue(validate_targeted_recording_profile(path, text.replace("rigorloop context", "record-store check|record", 1)))

    def test_explicit_profiles_are_scoped_and_use_model_owned_records(self):
        # Structural reachability only; the independent M3 walkthrough owns semantics.
        for skill in ("design", "route", "proposal", "proposal-review", "design-review", "plan", "delivery-review", "implement", "code-review", "verify", "bugfix", "ci-maintenance", "pr", "research", "explore", "learn"):
            with self.subTest(skill=skill):
                text = (ROOT / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
                if skill == "design":
                    text = "## Explicit recording\n" + (ROOT / "skills/design/references/governed-design-authoring.md").read_text()
                if skill in skill_validation.PILOT_RECORDING_REFERENCES:
                    text = (ROOT / "skills" / skill / skill_validation.PILOT_RECORDING_REFERENCES[skill]).read_text()
                self.assertEqual(text.count("## Explicit recording\n"), 1)
                block = text.split("## Explicit recording\n", 1)[1].split("\n## ", 1)[0]
                for phrase in ("project has adopted", "rigorloop-records-v3", "project's governing documents", "historical", "expected identities", "does not approve", "rigorloop-records-v3", "rigorloop context", "subject inspect", "targeted", "Do not migrate"):
                    self.assertIn(phrase, block)
                self.assertNotIn("roots retain their exact compatibility contract", block)
                self.assertNotIn("record-store check|record", block)
                self.assertNotIn("explicit writes", block)
                self.assertNotIn("templates/shared/", block)
                self.assertNotIn("specs/rigorloop-workflow.md", block)
