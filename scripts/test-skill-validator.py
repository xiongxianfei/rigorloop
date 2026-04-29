#!/usr/bin/env python3
"""Fixture-driven tests for the first-release skill validator."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-skills.py"
FIXTURES = ROOT / "tests" / "fixtures" / "skills"
SCAN_SENSITIVE_SKILLS = [
    "architecture",
    "architecture-review",
    "bugfix",
    "ci",
    "code-review",
    "explain-change",
    "implement",
    "plan",
    "plan-review",
    "pr",
    "project-map",
    "proposal",
    "proposal-review",
    "research",
    "spec",
    "spec-review",
    "test-spec",
    "verify",
    "workflow",
]


def run_validator(target: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(target)],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


class SkillValidatorFixtureTests(unittest.TestCase):
    maxDiff = None

    def assertFixturePasses(self, relative_path: str) -> None:
        result = run_validator(FIXTURES / relative_path)
        self.assertEqual(
            result.returncode,
            0,
            msg=f"expected fixture '{relative_path}' to pass\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def assertFixtureFails(self, relative_path: str, expected_text: str) -> None:
        result = run_validator(FIXTURES / relative_path)
        combined_output = f"{result.stdout}\n{result.stderr}"
        self.assertNotEqual(
            result.returncode,
            0,
            msg=f"expected fixture '{relative_path}' to fail",
        )
        self.assertIn(expected_text, combined_output)

    def test_valid_skill_passes(self) -> None:
        self.assertFixturePasses("valid-basic")

    def test_missing_name_fails(self) -> None:
        self.assertFixtureFails("missing-name", "name: missing required field")

    def test_missing_description_fails(self) -> None:
        self.assertFixtureFails("missing-description", "description: missing required field")

    def test_missing_title_fails(self) -> None:
        self.assertFixtureFails("missing-title", "expected exactly one top-level # title")

    def test_missing_expected_output_fails(self) -> None:
        self.assertFixtureFails(
            "missing-expected-output", "missing required '## Expected output' section"
        )

    def test_missing_skill_file_fails(self) -> None:
        self.assertFixtureFails(
            "missing-skill-file", "empty-skill/SKILL.md: missing required skill file"
        )

    def test_duplicate_name_fails(self) -> None:
        self.assertFixtureFails("duplicate-name", "duplicate skill name: duplicate-name")

    def test_placeholder_text_fails(self) -> None:
        self.assertFixtureFails("placeholder-text", "placeholder text is not allowed")

    def test_generated_output_path_is_rejected(self) -> None:
        result = run_validator(ROOT / ".codex" / "skills")
        combined_output = f"{result.stdout}\n{result.stderr}"
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("generated output path must not be used as authored source of truth", combined_output)

    def test_workflow_guidance_defines_bounded_extraction_and_output_budgets(self) -> None:
        workflow_text = (ROOT / "docs" / "workflows.md").read_text(encoding="utf-8")
        required_terms = [
            "bounded extraction",
            "stable IDs",
            "matching line numbers",
            "exact ranges",
            "full-file read",
            "routine command output target: 40 lines",
            "routine command output warning threshold: 80 lines",
            "single excerpt target: 12 lines",
            "single excerpt warning threshold: 20 lines",
            "one summary line per file",
            "--verbose",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, workflow_text)

    def test_scan_sensitive_skills_include_summary_id_reasoning_and_full_file_rules(self) -> None:
        for skill_name in SCAN_SENSITIVE_SKILLS:
            skill_path = ROOT / "skills" / skill_name / "SKILL.md"
            body = skill_path.read_text(encoding="utf-8")
            with self.subTest(skill=skill_name):
                self.assertIn("summary and stable-ID first", body)
                self.assertIn("check IDs", body)
                self.assertIn("requirement IDs", body)
                self.assertIn("file paths", body)
                self.assertIn("line citations", body)
                self.assertIn("When full-file read is required", body)
                self.assertIn("the whole file is the review target", body)
                self.assertIn("bounded searches disagree", body)
                self.assertIn("behavior-changing edit depends on the whole source-of-truth artifact", body)

    def test_architecture_skill_defines_concise_c4_arc42_adr_output_shape(self) -> None:
        body = (ROOT / "skills" / "architecture" / "SKILL.md").read_text(encoding="utf-8")
        required_terms = [
            "## When to Use / When Not to Use",
            "## Output Shape",
            "Produce or update:",
            "`docs/changes/<change-id>/architecture.md`",
            "canonical architecture package",
            "C4 system context diagram",
            "C4 container diagram",
            "ADRs when durable decisions are introduced",
            "Use `templates/architecture.md` for the full 12-section arc42 structure.",
            "```mermaid\nC4Context",
            "```mermaid\nC4Container",
            "## ADR Triggers",
            "skills/architecture/references/architecture-example.md",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, body)

        forbidden_terms = [
            "## Full Worked Example",
            "### Full Worked Example",
            "## Worked Example",
            "### Worked Example",
        ]
        for term in forbidden_terms:
            with self.subTest(term=term):
                self.assertNotIn(term, body)


if __name__ == "__main__":
    unittest.main(verbosity=2)
