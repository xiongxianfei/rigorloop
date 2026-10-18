"""Canonical guidance consistency, without claiming semantic adequacy."""
from pathlib import Path
import importlib.util
import sys
import tempfile
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
    def test_split_rem_projection_preserves_links_and_retires_only_generated_resources(self):
        # A split source must remain navigable offline; stale generated guidance
        # must not survive while unrelated authored resources remain untouched.
        script = ROOT / 'scripts/project-operational-guidance.py'
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            spec = importlib.util.spec_from_file_location('rem_projection', script)
            projection = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(projection)
            projection.ROOT = root
            projection.CORE = ('architecture-design',)
            projection.SUPPORT = ()
            projection.REM_SOURCES = {'architecture-design': (
                'methods/architecture-views.md', 'methods/views/logical.md',
                'models/views/logical.md',
            )}
            contents = {
                'rem/methods/architecture-views.md': '# Views\n\n[Logical](views/logical.md#responsibility)\n',
                'rem/methods/views/logical.md': '# Logical\n\n## Responsibility\n\n[Method](../architecture-views.md)\n',
                'rem/models/views/logical.md': '# Separate model\n',
                'templates/shared/operational-recording.md': '# Recording\n',
                'schemas/targeted-recording-v2.schema.json': '{}\n',
                'schemas/rigorloop-records-v4.schema.json': '{}\n',
                'skills/architecture-design/references/rem-retired.md': '<!-- Generated from rem/retired.md; source SHA-256 old. -->\nOld guidance\n',
                'skills/architecture-design/references/rem-authored.md': '# Authored resource\n',
            }
            for relative, content in contents.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
            old_argv = sys.argv
            try:
                sys.argv = [str(script)]
                projection.main()
                reference_root = root / 'skills/architecture-design/references'
                views = reference_root / 'rem-methods-architecture-views.md'
                logical = reference_root / 'rem-methods-views-logical.md'
                self.assertIn('(rem-methods-views-logical.md#responsibility)', views.read_text())
                self.assertIn('(rem-methods-architecture-views.md)', logical.read_text())
                self.assertTrue((reference_root / 'rem-models-views-logical.md').exists())
                self.assertFalse((reference_root / 'rem-retired.md').exists())
                self.assertEqual((reference_root / 'rem-authored.md').read_text(), '# Authored resource\n')
                before = {p.name: p.read_bytes() for p in reference_root.iterdir()}
                projection.main()
                self.assertEqual(before, {p.name: p.read_bytes() for p in reference_root.iterdir()})
                stale = reference_root / 'rem-retired.md'
                stale.write_text(contents['skills/architecture-design/references/rem-retired.md'])
                sys.argv = [str(script), '--check']
                with self.assertRaisesRegex(SystemExit, 'obsolete generated resource'):
                    projection.main()
                self.assertTrue(stale.exists(), 'A freshness check must not mutate resources')
            finally:
                sys.argv = old_argv

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
