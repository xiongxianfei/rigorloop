"""Canonical guidance consistency, without claiming semantic adequacy."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.validation import skill_validation


# Independent published resource selection; Design has its own full procedure.
RECORDING_RESOURCES = {
    'code-review': 'references/governed-code-review-recording.md',
    'delivery-review': 'references/delivery-review-recording-and-settlement.md',
    'design': 'references/governed-design-authoring.md',
    'design-review': 'references/design-review-recording-and-settlement.md',
    'implement': 'references/governed-implementation-recording.md',
    'plan': 'references/governed-plan-authoring.md',
    'pr': 'references/governed-pr-readiness.md',
    'proposal': 'references/governed-proposal-authoring.md',
    'proposal-review': 'references/proposal-review-recording-and-settlement.md',
    'route': 'references/governed-lifecycle-routing.md',
    'verify': 'references/governed-verification-recording.md',
}


class SkillGuidanceTests(unittest.TestCase):
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


    # Structural drift guard for the published Code Review checklist and its
    # prohibition on automated semantic grading; adequacy remains review-owned.
