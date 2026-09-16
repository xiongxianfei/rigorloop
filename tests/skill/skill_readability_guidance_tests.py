"""Readability guidance.

Current Skill contracts own the protected structures, resources and authority.
Wording checks detect structural drift; independent review assesses semantics.
Existing class/case selectors remain stable, including historical names.
"""
from __future__ import annotations

import subprocess
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))


class MarkdownReadabilityGuidanceTests(unittest.TestCase):
    def test_generated_markdown_skeletons_declare_readability_shape(self) -> None:
        skeletons = [
            ROOT / "skills" / "proposal" / "assets" / "proposal-skeleton.md",
            ROOT / "skills" / "design" / "assets" / "design-skeleton.md",
            ROOT / "skills" / "plan" / "assets" / "plan-skeleton.md",
        ]
        required_terms = [
            "Readability contract:",
            "normal prose paragraphs",
            "complete sentences",
            "stable IDs",
            "tables",
        ]

        for skeleton in skeletons:
            text = skeleton.read_text(encoding="utf-8")
            for term in required_terms:
                with self.subTest(skeleton=skeleton, term=term):
                    self.assertIn(term, text)

    def test_generated_markdown_skills_include_readability_guidance(self) -> None:
        skill_paths = [
            ROOT / "skills" / "proposal" / "SKILL.md",
            ROOT / "skills" / "design" / "SKILL.md",
            ROOT / "skills" / "plan" / "SKILL.md",
            ROOT / "skills" / "code-review" / "SKILL.md",
            ROOT / "skills" / "verify" / "SKILL.md",
        ]
        required_terms = [
            "## Generated Markdown readability",
            "normal Markdown paragraphs",
            "Do not split a sentence across physical source lines",
            "stable IDs",
            "Do not require manual-proof contracts",
        ]

        for skill_path in skill_paths:
            text = skill_path.read_text(encoding="utf-8")
            for term in required_terms:
                with self.subTest(skill=skill_path, term=term):
                    self.assertIn(term, text)

            if skill_path.parent.name == "design":
                self.assertIn("Living models require the overview and every supporting view judged necessary", text)
                self.assertIn("other diagrams are optional", text)
            else:
                self.assertIn("Diagrams are optional", text)

            with self.subTest(skill=skill_path, term="legacy clause-per-line guidance"):
                self.assertNotIn("one sentence or natural clause per source line", text)

    def test_implementation_markdown_guidance_keeps_sentences_intact(self) -> None:
        skill_path = ROOT / "skills" / "implement" / "SKILL.md"
        text = skill_path.read_text(encoding="utf-8")

        self.assertIn("normal Markdown paragraphs", text)
        self.assertIn("Do not split a sentence across physical source lines", text)
        self.assertNotIn("use semantic source lines", text)

    def test_canonical_skill_prose_has_no_suspected_sentence_splits(self) -> None:
        skill_paths = sorted((ROOT / "skills").glob("*/SKILL.md"))
        command = [
            sys.executable,
            str(ROOT / "scripts" / "validate-documentation-prose.py"),
            "--mode",
            "audit",
        ]
        for skill_path in skill_paths:
            command.extend(("--path", str(skill_path.relative_to(ROOT))))

        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            f"documentation prose validation: errors=0 warnings=0 paths={len(skill_paths)}\n",
            result.stdout,
        )
