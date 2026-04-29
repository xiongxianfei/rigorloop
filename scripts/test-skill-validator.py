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
    "vision",
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

    def test_architecture_review_skill_preserves_simple_finding_and_material_contract(self) -> None:
        body = (ROOT / "skills" / "architecture-review" / "SKILL.md").read_text(encoding="utf-8")
        required_terms = [
            "embedded or duplicated diagram source",
            "generic non-C4 flowchart",
            "wrong C4 level",
            "missing C4 role classes",
            "missing technology labels where relevant",
            "unlabeled relationships",
            "flat Building Block View",
            "duplicated ADR rationale",
            "weak quality-scenario content",
            "Deployment View repeats source layout",
            "Finding:",
            "Location:",
            "Severity:",
            "Recommendation:",
            "`blocker`, `material`, or `minor`",
            "Do not require mandatory C4-level classification",
            "does not replace the repository-wide material-finding contract",
            "evidence, required outcome, and a safe resolution path or `needs-decision` rationale",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, body)

    def test_vision_skill_defines_modes_boundaries_and_readme_marker_contract(self) -> None:
        body = (ROOT / "skills" / "vision" / "SKILL.md").read_text(encoding="utf-8")
        required_terms = [
            "name: vision",
            "project vision and matching README front-matter",
            "## Modes",
            "create",
            "revise",
            "mirror",
            "Do not create the initial `vision.md` just because this skill is installed",
            "`vision.md` is canonical",
            "`CONSTITUTION.md` outranks `vision.md`",
            "<!-- vision:start -->",
            "<!-- vision:end -->",
            "first H1 block",
            "Automatic marker insertion is allowed only in `create` mode.",
            "In `mirror` or `revise`, missing or malformed markers stop the skill before file modification",
            "explicitly authorizes marker insertion or skipping README mirroring",
            "malformed, nested, or multiple vision marker pairs",
            "Mode used:",
            "Files changed:",
            "README front-matter:",
            "Assumptions:",
            "Sections changed:",
            "secrets",
            "credentials",
            "private local filesystem paths",
            "private machine names",
            "personal data not explicitly intended for publication",
            "must not fetch external information unless",
            "distinguish researched facts from project assumptions",
            "plain Markdown",
            "rendered tables, diagrams, HTML layout, or generated assets",
            "compact project inputs",
            "full-file reads",
            "summary and stable-ID first",
            "When full-file read is required",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, body)

    def test_proposal_skills_define_vision_fit_contract(self) -> None:
        proposal_body = (ROOT / "skills" / "proposal" / "SKILL.md").read_text(encoding="utf-8")
        proposal_review_body = (
            ROOT / "skills" / "proposal-review" / "SKILL.md"
        ).read_text(encoding="utf-8")

        proposal_terms = [
            "`Vision fit`",
            "new or substantively revised proposals",
            "fits the current vision",
            "may conflict with the current vision",
            "intentionally proposes a vision revision",
            "no vision exists yet",
            "When root `vision.md` is absent, proposals must use the exact `Vision fit` value `no vision exists yet`.",
            "must not silently redefine project vision",
            "Legacy proposals",
        ]
        for term in proposal_terms:
            with self.subTest(skill="proposal", term=term):
                self.assertIn(term, proposal_body)

        proposal_review_terms = [
            "Check the proposal's `Vision fit` section",
            "created or substantively revised after the vision spec was adopted",
            "request revision",
            "When root `vision.md` is absent, proposal-review must request revision if `Vision fit` is missing or replaced with a claim that fits, conflicts with, or revises a nonexistent vision.",
            "revise proposal",
            "revise vision",
            "record explicit exception",
            "approving owner or owning stage",
            "evidence for the conflict",
            "why proposal revision is not chosen",
            "why vision revision is not chosen",
            "where the exception is recorded",
            "one-time",
            "future vision-revision trigger",
            "`explain-change.md`",
        ]
        for term in proposal_review_terms:
            with self.subTest(skill="proposal-review", term=term):
                self.assertIn(term, proposal_review_body)

    def test_governance_workflow_and_readme_define_vision_source_of_truth(self) -> None:
        constitution = (ROOT / "CONSTITUTION.md").read_text(encoding="utf-8")
        self.assertIn("2. `vision.md`", constitution)
        self.assertIn("3. `specs/`", constitution)
        self.assertIn("README front-matter", constitution)

        required_terms = [
            "`vision.md` is the canonical project-vision artifact",
            "created or substantively revised after this spec is adopted include `Vision fit`",
            "README content between `<!-- vision:start -->` and `<!-- vision:end -->` is generated from `vision.md`",
            "README front-matter is not the source of truth when it conflicts with `vision.md`",
        ]
        for relative_path in ["AGENTS.md", "docs/workflows.md", "README.md"]:
            body = (ROOT / relative_path).read_text(encoding="utf-8")
            for term in required_terms:
                with self.subTest(path=relative_path, term=term):
                    self.assertIn(term, body)


if __name__ == "__main__":
    unittest.main(verbosity=2)
