#!/usr/bin/env python3
"""Canonical skill integrity and a meaningful missing-resource counterexample."""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]

def validate(path):
    return subprocess.run([sys.executable, str(ROOT / 'scripts/validate-skills.py'), str(path)], cwd=ROOT, text=True, capture_output=True)

class SkillIntegrityTests(unittest.TestCase):
    def test_canonical_skills_and_resources(self):
        result = validate(ROOT / 'skills')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((ROOT / 'skills/route/SKILL.md').is_file())
        self.assertTrue((ROOT / 'skills/verify/SKILL.md').is_file())

    def test_missing_declared_resource_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            skill = Path(temporary) / 'route'
            shutil.copytree(ROOT / 'skills/route', skill)
            control = validate(skill)
            self.assertEqual(control.returncode, 0, control.stdout + control.stderr)
            resource = skill / 'references/operational-recording.md'
            resource.unlink()
            result = validate(skill)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('operational-recording.md', result.stderr)
            self.assertFalse(resource.exists())
if __name__ == '__main__':
    unittest.main()
